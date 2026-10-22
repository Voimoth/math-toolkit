#!/usr/bin/env python3
"""归档/改完 bookdex 索引后的自检（改过 index.py 逻辑、或刚刷过 OCR 语言包时必跑）。

1. 每条 `ocr:*` 记录的语种标签是否与 index.py 当前 `ocr_lang(path)` 一致。
   不一致 = 那本书需 `update books set dir_src=''` 后重跑增量才会重刷。
2. 库概况：本数/页数/书签/文本层/目录页兜底，以及 tier 与 dir_src 分布。
3. `--name 子串` 采样：列出匹配书的 dir_src 与 dir_text 长度。

必须用 bookdex 自己的 venv（要 import 它依赖 pymupdf 的 index 模块）：
  ~/.local/share/bookdex/venv/bin/python <skill>/scripts/check_bookdex_index.py --name Oraux
退出码 1 = 存在不一致。
"""
import os
import sqlite3
import sys

B = os.path.expanduser("~/.local/share/bookdex")
sys.path.insert(0, B)
import index  # noqa: E402  语种规则的唯一真相源

name_filter = None
if "--name" in sys.argv:
    name_filter = sys.argv[sys.argv.index("--name") + 1]

db = sqlite3.connect(os.path.join(B, "index.db"))

bad = [(p, s, "ocr:" + index.ocr_lang(p))
       for p, s in db.execute("select path, dir_src from books where dir_src like 'ocr:%'")
       if s != "ocr:" + index.ocr_lang(p)]

print("== 语种标签一致性 ==")
print(f"不一致 {len(bad)} 条")
for path, have, want in bad[:20]:
    print(f"  {have} -> {want}  {path}")

n, pages, toc, txt, anydir, ocrn = db.execute(
    "select count(*), sum(pages), sum(toc_n>0), sum(has_text), "
    "sum(dir_src!=''), sum(dir_src like 'ocr:%') from books").fetchone()
print("\n== 概况 ==")
print(f"{n} 本 / {pages} 页 / 有书签 {toc} / 有文本层 {txt} / 目录页文本 {anydir}（OCR {ocrn}）")
for tier, c in db.execute("select tier, count(*) from books group by tier order by tier desc"):
    print(f"  tier {tier}: {c} 本")
for src, c in db.execute("select dir_src, count(*) from books group by dir_src order by 2 desc"):
    print(f"  dir_src={src!r}: {c}")

if name_filter:
    print(f"\n== 采样: name like %{name_filter}% ==")
    for name, src, dlen, tn in db.execute(
            "select name, dir_src, length(dir_text), toc_n from books "
            "where name like ? order by name", (f"%{name_filter}%",)):
        print(f"  {name}  dir_src={src!r} dir_text={dlen} toc_n={tn}")

sys.exit(1 if bad else 0)
