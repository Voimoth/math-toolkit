#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""概念地图同步检查器。

三件事：
1. 地图类文件是否比它覆盖的概念页旧（陈旧）；
2. 磁盘上的地图类文件与 registry 是否一一对应（漏登记/文件被删）；
3. duty=concept-index 的文件是否漏链了概念页（孤儿页）。

用法：check_concept_sync.py [--root /mnt/e/notes] [--verbose]
退出码：0 全绿；1 有陈旧/未登记/缺失。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "..", "references", "concept-map-registry.json")
DEFAULT_ROOT = "/mnt/e/notes"
SKIP = {".git", ".obsidian", ".trash", "__pycache__"}

DATE_RE = re.compile(r"^updated:\s*\"?(\d{4}-\d{2}-\d{2})", re.M)
LINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:[#\|][^\]]*)?\]\]")


def load_registry():
    with open(REG, encoding="utf-8") as f:
        return json.load(f)


def frontmatter_date(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(3000)
    m = DATE_RE.search(head)
    return m.group(1) if m else None


def all_md(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for n in fn:
            if n.endswith(".md"):
                yield os.path.join(dp, n)


MAP_FILE_RE = re.compile(r"(学习路径|概念页索引|_索引|00-总览)$")


def concept_pages(root, rel_dir):
    d = os.path.join(root, rel_dir)
    if not os.path.isdir(d):
        return []
    out = []
    for x in os.listdir(d):
        if not x.endswith(".md"):
            continue
        stem = x[:-3]
        if MAP_FILE_RE.search(stem):
            continue
        out.append(os.path.join(d, x))
    return sorted(out)


def main():
    root = DEFAULT_ROOT
    verbose = "--verbose" in sys.argv
    if "--root" in sys.argv:
        root = sys.argv[sys.argv.index("--root") + 1]
    reg = load_registry()
    entries = reg["entries"]
    known = {e["path"] for e in entries}
    problems = 0

    # 1) registry 与磁盘比对
    pats = [re.compile(p) for p in reg["patterns"]]
    for p in all_md(root):
        rp = os.path.relpath(p, root).replace(os.sep, "/")
        base = os.path.basename(p)
        if any(pt.search(base) for pt in pats) and rp not in known:
            print(f"[未登记] {rp}  —— 是地图类文件但不在 registry 里")
            problems += 1

    # 2) 逐项检查
    for e in entries:
        path = os.path.join(root, e["path"])
        rp = e["path"]
        if not os.path.exists(path):
            print(f"[缺失] {rp}")
            problems += 1
            continue
        if e["duty"] == "notes-entry":
            continue
        d = frontmatter_date(path)
        pages = concept_pages(root, e["covers"])
        dates = [frontmatter_date(x) for x in pages]
        dates = [x for x in dates if x]
        if not d:
            print(f"[无日期] {rp}（frontmatter 缺 updated，无法判断新旧）")
            problems += 1
            continue
        if dates:
            latest = max(dates)
            if latest > d:
                stale = [os.path.basename(x) for x, dd in zip(pages, [frontmatter_date(y) for y in pages])
                         if dd and dd > d]
                print(f"[陈旧] {rp}: updated={d} < 概念页最新={latest}；过期页 {len(stale)} 个")
                if verbose:
                    for s in stale[:20]:
                        print(f"        - {s}")
                problems += 1
        if e["duty"] == "concept-index":
            text = open(path, encoding="utf-8").read()
            linked = {os.path.basename(m.group(1).strip()) for m in LINK_RE.finditer(text)}
            orphans = [os.path.basename(x)[:-3] for x in pages
                       if os.path.basename(x)[:-3] not in linked
                       and os.path.basename(x) != os.path.basename(path)]
            if orphans:
                print(f"[孤儿] {rp}: {len(orphans)} 个概念页没被链接：{', '.join(orphans[:8])}"
                      + (" ..." if len(orphans) > 8 else ""))
                problems += 1

    # 4) 提示：概念目录内跨课重名（一概念一文件铁律的存量违例，不计入退出码）
    import collections
    names = collections.defaultdict(list)
    for p in all_md(root):
        rp = os.path.relpath(p, root).replace(os.sep, "/")
        if "/概念/" in rp:
            names[os.path.basename(p)].append(rp)
    dups = {k: v for k, v in names.items() if len(v) > 1}
    if dups:
        print(f"\n[提示] 概念目录内跨课重名 {len(dups)} 组（合并需人工判断，不计入退出码）：")
        for k, v in sorted(dups.items()):
            print(f"  {k}: {', '.join(v)}")

    print(f"\n共 {len(entries)} 个登记项，问题 {problems} 处")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
