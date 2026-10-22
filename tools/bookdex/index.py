#!/usr/bin/env python3
"""bookdex — 书目卡 + 目录索引（v2：多根目录 + 权重 + 目录页兜底）。

不抽正文，只索引：书名 / 作者 / PDF 书签；**没有书签的去抽「目录页」**——
有文本层的用 pymupdf 取文本（精确），扫描件用 tesseract OCR（会脏，只作召回）。
OCR 失败的少数才值得上视觉模型，见 skill bookdex。

产物：~/.local/share/bookdex/index.db

用法：
  python index.py                # 增量（新增文件 + 缺目录页文本的）
  python index.py --rebuild      # 全量重建
  python index.py --limit 200    # 只处理前 N 个待办
  python index.py --no-ocr       # 跳过 OCR（只做文本层目录页）
  python index.py --workers 6    # OCR 并发数
"""
import os, sys, json, time, sqlite3, subprocess, re
import pymupdf
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "index.db")
_TESS_CANDIDATES = ["/mnt/h/tesseract/tessdata", "/usr/share/tesseract-ocr/5/tessdata",
                    "/usr/share/tesseract-ocr/4.00/tessdata", "/usr/share/tessdata"]
TESSDATA = (os.environ.get("TESSDATA_PREFIX")
            or next((p for p in _TESS_CANDIDATES if os.path.isdir(p)), "/usr/share/tessdata"))

# 书库根目录：默认本机路径，可用环境变量 BOOKDEX_ROOT 指到别处
BOOKS_ROOT = os.environ.get("BOOKDEX_ROOT", "/mnt/e/书籍")

# (根目录, 权重层级)。tier 3 = 课程在用、tier 2 = MPSI 预科、tier 1 = 普通参考书
ROOTS = [
    (os.path.join(BOOKS_ROOT, "代数"), 3),
    (os.path.join(BOOKS_ROOT, "分析"), 3),
    (os.path.join(BOOKS_ROOT, "物理"), 3),
    (os.path.join(BOOKS_ROOT, "数学学习方法"), 3),
    (os.path.join(BOOKS_ROOT, "数学专业书籍"), 1),
]
# 路径/文件名命中这些片段的，层级往上提（MPSI 是中法班大部分数学课的直接参考）
TIER_HINTS = [("/MPSI", 2), ("MPSI", 2), ("Mathématiques MP", 2), ("Mathématiques PSI", 2)]

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
DIR_PAGES = 20  # 只在没书签时看前 20 页找目录

# 法语资料：OCR 用 fra+eng（保留重音），否则 eng 会把 «théorème» 认成 «theoreme»，
# 查询里带重音的法文词就永远命中不了。中法班的法文参考书走这条。
FR_CHARS = re.compile(r"[àâäçéèêëîïôöûùüÿœæ]", re.I)
FR_WORDS = re.compile(r"(\bmath[ée]matiques\b|\bexercices\b|\boraux\b|\balg[èe]bre\b|"
                      r"\banalyse\b|\bmpsi\b|\bpolytechnique\b|\bnormales?\s+sup[ée]rieures\b|"
                      r"\bg[ée]om[ée]trie\b|\bprobabilit[ée]s\b|\ble[çc]ons\b|"
                      r"\bprobl[èe]mes\b|\bpr[ée]pas\b|\bcours\b)", re.I)


def ocr_lang(path):
    base = os.path.basename(path)
    if CJK.search(base):
        return "chi_sim+eng"
    # 判法语特征时先剔掉路径里的中文目录名（/mnt/e/书籍/…），否则中文会盖住法语线索
    probe = CJK.sub(" ", path)
    if FR_CHARS.search(probe) or FR_WORDS.search(probe):
        return "fra+eng"
    return "eng"


# 扫描仪自动生成的书签（"01" / "202512280213"）是噪声：有它就不抽目录页等于把书藏了
JUNK_TOC = re.compile(r"[\d\s\-_.:/]{1,24}")


def toc_junk(toc):
    """toc = [(level, title, page)]；全部条目都是数字/时间戳时判为垃圾书签。"""
    return bool(toc) and all(JUNK_TOC.fullmatch(t or "") for _, t, _ in toc)

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
  path TEXT PRIMARY KEY,
  dir TEXT, name TEXT, size INTEGER, mtime REAL,
  pages INTEGER, has_text INTEGER, text_chars INTEGER,
  toc_n INTEGER, toc_json TEXT, title TEXT, author TEXT,
  tier INTEGER DEFAULT 1,
  dir_text TEXT DEFAULT '', dir_src TEXT DEFAULT '',
  indexed_at REAL
);
CREATE INDEX IF NOT EXISTS idx_name ON books(name);
"""


def clean(s):
    return CTRL.sub("", s or "").strip()


def tier_for(path, base):
    for frag, t in TIER_HINTS:
        if frag in path:
            return max(base, t)
    return base


def walk(root):
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(".pdf") and not f.startswith("._"):
                # ._xxx.pdf 是 macOS 的 AppleDouble 资源叉，0 字节垃圾
                yield os.path.join(dp, f)


def ocr_page(doc, idx, lang):
    pix = doc[idx].get_pixmap(dpi=150, colorspace=pymupdf.csGRAY)
    png = pix.tobytes("png")
    env = dict(os.environ, TESSDATA_PREFIX=TESSDATA)
    r = subprocess.run(["tesseract", "stdin", "stdout", "-l", lang],
                       input=png, capture_output=True, timeout=180, env=env)
    return r.stdout.decode("utf-8", "replace")


def dir_pages(doc, name, do_ocr):
    """抽前 DIR_PAGES 页的文字充当「目录页文本」。返回 (text, src)。"""
    n = min(DIR_PAGES, doc.page_count)
    txt = []
    for i in range(n):
        try:
            txt.append(doc[i].get_text())
        except Exception:
            txt.append("")
    joined = "\n".join(txt)
    if len(joined.strip()) > 300:
        return clean(joined)[:20000], "text"
    if not do_ocr or n == 0:
        return "", ""
    lang = ocr_lang(name)
    out = []
    for i in range(n):
        try:
            out.append(ocr_page(doc, i, lang))
        except Exception:
            out.append("")
    return clean("\n".join(out))[:20000], "ocr:" + lang


def card(path, do_ocr):
    rec = {"path": path, "size": os.path.getsize(path), "mtime": os.path.getmtime(path)}
    try:
        d = pymupdf.open(path)
        try:
            rec["pages"] = d.page_count
            toc = d.get_toc(simple=True)  # [(level, title, page)]
            rec["toc_n"] = len(toc)
            rec["toc_json"] = json.dumps([[l, clean(t), p] for l, t, p in toc], ensure_ascii=False)
            md = d.metadata or {}
            rec["title"] = clean(md.get("title", ""))[:200]
            rec["author"] = clean(md.get("author", ""))[:200]
            txt = ""
            mid = max(d.page_count // 2, 0)
            for p in range(mid, min(mid + 2, d.page_count)):
                txt += d[p].get_text()
            rec["text_chars"] = len(txt.strip())
            rec["has_text"] = 1 if rec["text_chars"] > 200 else 0
            # 只有没书签（或书签是扫描仪垃圾）的才抽目录页：真书签本身更准
            if rec["toc_n"] == 0 or toc_junk(toc):
                rec["dir_text"], rec["dir_src"] = dir_pages(d, path, do_ocr)
            else:
                rec["dir_text"], rec["dir_src"] = "", ""
        finally:
            d.close()
    except Exception as e:
        rec.update(pages=-1, toc_n=0, toc_json="[]", title="", author="",
                   text_chars=0, has_text=0, dir_text="", dir_src="",
                   err=f"{type(e).__name__}: {e}"[:100])
    return rec


FIELDS = ("path dir name size mtime pages has_text text_chars toc_n toc_json "
          "title author tier dir_text dir_src indexed_at").split()


def main():
    rebuild = "--rebuild" in sys.argv
    do_ocr = "--no-ocr" not in sys.argv
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    workers = 6
    if "--workers" in sys.argv:
        workers = int(sys.argv[sys.argv.index("--workers") + 1])

    if rebuild and os.path.exists(DB):
        os.remove(DB)
        print("已删旧库，全量重建")
    if do_ocr:
        os.environ.setdefault("TESSDATA_PREFIX", TESSDATA)
    db = sqlite3.connect(DB)
    db.executescript(SCHEMA)
    # 老库迁移
    cols = {r[1] for r in db.execute("PRAGMA table_info(books)")}
    for c, ddl in (("tier", "INTEGER DEFAULT 1"), ("dir_text", "TEXT DEFAULT ''"),
                   ("dir_src", "TEXT DEFAULT ''")):
        if c not in cols:
            db.execute(f"ALTER TABLE books ADD COLUMN {c} {ddl}")
    db.commit()
    have = {r[0]: (r[1], r[2], r[3], r[4], r[5]) for r in db.execute(
        "select path, mtime, size, toc_n, dir_src, toc_json from books")}

    files = []
    for root, base in ROOTS:
        if not os.path.isdir(root):
            print(f"缺目录，跳过：{root}")
            continue
        for f in walk(root):
            files.append((f, tier_for(f, base)))
    files.sort()

    todo = []
    for f, tier in files:
        old = have.get(f)
        if old is None:
            todo.append((f, tier))
            continue
        mtime, size, toc_n, dir_src, toc_json = old
        changed = abs(mtime - os.path.getmtime(f)) > 1 or size != os.path.getsize(f)
        # 还没抽到目录页文本、且书签缺失或只是扫描仪垃圾的，重试一次
        try:
            junk = toc_junk(json.loads(toc_json or "[]"))
        except Exception:
            junk = False
        want_dir = (dir_src == "" and (toc_n == 0 or junk))
        if changed or want_dir:
            todo.append((f, tier))
    if limit:
        todo = todo[:limit]
    print(f"扫描 {len(files)} 本，需处理 {len(todo)} 本，OCR={'开' if do_ocr else '关'}，并发 {workers}", flush=True)

    t0 = time.time()
    done = 0

    def work(item):
        f, tier = item
        try:
            return tier, card(f, do_ocr)
        except Exception:
            return tier, {"path": f, "size": os.path.getsize(f), "mtime": os.path.getmtime(f),
                          "pages": -1, "toc_n": 0, "toc_json": "[]", "title": "", "author": "",
                          "text_chars": 0, "has_text": 0, "dir_text": "", "dir_src": ""}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for tier, r in ex.map(work, todo):
            vals = {
                "path": r["path"], "dir": os.path.dirname(r["path"]), "name": os.path.basename(r["path"]),
                "size": r["size"], "mtime": r["mtime"], "pages": r.get("pages", -1),
                "has_text": r.get("has_text", 0), "text_chars": r.get("text_chars", 0),
                "toc_n": r.get("toc_n", 0), "toc_json": r.get("toc_json", "[]"),
                "title": r.get("title", ""), "author": r.get("author", ""), "tier": tier,
                "dir_text": r.get("dir_text", ""), "dir_src": r.get("dir_src", ""),
                "indexed_at": time.time(),
            }
            db.execute(
                f"INSERT OR REPLACE INTO books({','.join(FIELDS)}) VALUES ({','.join('?' * len(FIELDS))})",
                [vals[k] for k in FIELDS])
            done += 1
            if done % 50 == 0:
                db.commit()
                el = time.time() - t0
                print(f"  {done}/{len(todo)}  {el:.0f}s  剩余约 {el / done * (len(todo) - done) / 60:.1f} 分钟", flush=True)
    db.commit()

    tot = db.execute("select count(*), sum(pages), sum(toc_n>0), sum(has_text), "
                     "sum(dir_src!=''), sum(dir_src like 'ocr:%') from books").fetchone()
    print(f"\n完成 {done} 本，用时 {time.time() - t0:.0f}s")
    print(f"库里 {tot[0]} 本 / {tot[1]} 页 / 有书签 {tot[2]} / 有文本层 {tot[3]} / "
          f"有目录页文本 {tot[4]}（其中 OCR {tot[5]}）")
    for t, n in db.execute("select tier, count(*) from books group by tier order by tier desc"):
        print(f"  tier {t}: {n} 本")
    db.close()


if __name__ == "__main__":
    main()
