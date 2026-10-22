#!/usr/bin/env python3
"""bookdex 查询：在 8000 本参考书的书名/作者/章节目录里找「哪本书可能讲到 X」。

用法：
  python query.py "正规子群"
  python query.py "variational principle" --limit 15
  python query.py "复分析" --json
  python query.py "group*" --books        # 只列书，不列章节

排序：章节目录命中 > 书名命中 > 路径命中。
输出带 PDF 页号（书签页号是 1-based 的物理页）。
"""
import os, sys, json, sqlite3, re, unicodedata

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.db")
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
# 书签里常混进 PDF 的控制字符（\x00 等），显示前清掉
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean(s):
    return CTRL.sub("", s).strip()


def fold(s):
    """去重音 + 折叠 œ/æ：法语资料里 théoreme/théorème/theoreme 必须互通，
    否则 OCR 出的无重音词和手输的带重音词永远互相找不到。"""
    s = (s or "").replace("œ", "oe").replace("æ", "ae").replace("’", "'")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def terms(q):
    """把查询切成匹配单元：中文保留原串（子串匹配）；拉丁文字统一 fold 后分词，
    多词作短语，单词用词边界 + 可选复数（`Riemann` 不该命中 `Riemannian`）。"""
    q = q.strip()
    if CJK.search(q):
        return [q], []
    raw = fold(q).lower()
    words = [w for w in re.split(r"[^\w]+", raw) if w]
    if len(words) >= 2:
        return [], ["PHRASE:" + " ".join(words)]
    return [], [w for w in words if len(w) >= 2]


def _matcher(w):
    """单词：词边界 + 可选复数（Riemann 不配 Riemannian）；
    多词：短语，词间允许空格/连字符混排（Riemann-Roch / Riemann Roch / Riemann–Roch）。"""
    if w.startswith("PHRASE:"):
        parts = [re.escape(x) for x in w[7:].split()]
        rx = re.compile(r"\b" + r"[\s\-–—]*".join(parts), re.I)
    else:
        rx = re.compile(r"\b" + re.escape(w) + r"(?:s|es)?\b", re.I)
    return lambda t: rx.search(t) is not None


def score_record(rec, zh, en):
    """返回 (分值, 命中章节列表)。封面/版权页（page<=5）的条目权重大幅降低——
    它们往往把书名重复一遍，看起来命中其实什么都没说。"""
    toc = rec["toc"]
    hits = []
    s = 0
    name_l = fold(rec["name"]).lower()
    meta_l = fold(rec["title"] + " " + rec["author"]).lower()

    def add(lvl, title, page):
        w = 1.0 if page > 5 else 0.2
        hits.append((w, lvl, clean(title), page))

    toc_f = [(lvl, title, fold(title), page) for lvl, title, page in toc]
    for t in zh:
        for lvl, title, _, page in toc_f:
            if t in title:
                add(lvl, title, page)
        if t in rec["name"] or t in meta_l:
            s += 6
    for w in en:
        m = _matcher(w)
        for lvl, title, title_f, page in toc_f:
            if m(title_f):
                add(lvl, title, page)
        key = w[7:] if w.startswith("PHRASE:") else w
        if m(name_l) or (key in meta_l):
            s += 6
    s += 2 * sum(h[0] for h in hits)
    if hits:
        s += 5

    # 目录页文本（无书签时的兜底，来自文本层或 OCR）：权重低，只作召回
    dt = rec.get("dir_text") or ""
    dir_hit = False
    if dt:
        if any(t in dt for t in zh):
            dir_hit = True
        if any(_matcher(w)(fold(dt)) for w in en):
            dir_hit = True
        if dir_hit:
            s += 2.5
    rec["_dir_hit"] = dir_hit

    # 层级加权：课程在用（3） > MPSI 预科（2） > 普通参考书（1）
    s *= 1 + 0.6 * (rec.get("tier", 1) - 1)

    hits.sort(key=lambda h: (-h[0], h[3]))
    return s, hits


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return
    q = args[0]
    limit = 10
    as_json = "--json" in sys.argv
    books_only = "--books" in sys.argv
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    if not os.path.exists(DB):
        print("索引不存在，先跑 index.py", file=sys.stderr)
        return 1
    zh, en = terms(q)
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = db.execute(
        "select path,dir,name,pages,has_text,toc_json,title,author,toc_n,tier,dir_text,dir_src "
        "from books").fetchall()
    out = []
    for (path, d, name, pages, has_text, toc_json, title, author, toc_n,
         tier, dir_text, dir_src) in rows:
        rec = {"path": path, "dir": d, "name": name, "pages": pages,
               "has_text": has_text, "toc": json.loads(toc_json or "[]"),
               "title": title or "", "author": author or "",
               "tier": tier or 1, "dir_text": dir_text or "", "dir_src": dir_src or ""}
        s, hits = score_record(rec, zh, en)
        if s > 0:
            out.append((s, rec, hits))
    out.sort(key=lambda x: (-x[0], x[1]["name"]))
    if as_json:
        print(json.dumps([{"score": round(s, 1), "path": r["path"], "pages": r["pages"],
                           "tier": r["tier"], "has_text": r["has_text"],
                           "dir_hit": bool(r.get("_dir_hit")), "dir_src": r["dir_src"],
                           "hits": [{"level": h[1], "title": h[2], "page": h[3]} for h in hits[:8]]}
                          for s, r, hits in out[:limit]], ensure_ascii=False, indent=2))
        return 0
    if not out:
        print(f"「{q}」在已索引的书名/目录里没有命中。")
        return 0
    print(f"「{q}」命中 {len(out)} 本，列前 {min(limit, len(out))} 本：\n")
    for s, r, hits in out[:limit]:
        flag = "文字版" if r["has_text"] else "扫描件"
        tag = {3: "【课程】", 2: "【MPSI】"}.get(r["tier"], "")
        print(f"■ {tag}{r['name']}  [{r['pages']}页/{flag}]")
        if not books_only:
            for w, lvl, title, page in hits[:5]:
                print(f"    p.{page:<5} {'  ' * min(lvl, 3)}{title[:80]}")
            if not hits and r.get("_dir_hit"):
                src = "OCR" if r["dir_src"].startswith("ocr") else "文本层"
                print(f"    （无书签；前 20 页{src}目录页里出现该词，自己去翻）")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
