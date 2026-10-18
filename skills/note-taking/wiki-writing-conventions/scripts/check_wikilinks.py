#!/usr/bin/env python3
"""检查 Obsidian vault 的 wikilink 健康度（用户 /mnt/e/notes 专用，通用参数化）。

用法:  python3 check_wikilinks.py [/mnt/e/notes]
输出四类问题（都应为 0），任一非 0 时 exit 1:
  1. 裸链二义  —— 链接文字命中 ≥2 个文件。按 obsidian.nvim 的 Note.reference_ids
                 规则匹配 {stem, 文件名, frontmatter id, frontmatter title, 首个 H1, aliases}；
                 Obsidian 桌面版只按文件名/路径/别名，所以这类问题往往只在 nvim 里暴露
                 （典型：概念页 映射.md 与讲义笔记 05-映射.md 的 H1 同名）。
                 修法：写成带路径形式 [[代数I/概念/映射]]。
  2. 路径链接二义 —— 带 "/" 的链接文字是 ≥2 个文件路径的后缀（如 [[概念/群]] 同时命中 代数I 与 代数III）。
  3. 断链 —— 链接文字既不是任何文件/路径后缀，也不是任何 alias。
  4. 数学记号误判 —— 行内数学 $...$ 里的 [[...]]（如 $K[[X]]$）会被 Obsidian 当成链接 ⇒ 显示为 $K[\\![X]\\!]$。
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/e/notes")
SKIP_DIRS = {".git", "node_modules", ".obsidian", "_archive", "raw", "scripts"}
ATTACH = re.compile(r"\.(?:svg|png|jpe?g|gif|webp|pdf|mp3|mp4|canvas|excalidraw)$", re.I)
LINK = re.compile(r"(?<!\\)\[\[([^\[\]]+)\]\]")
CODE = re.compile(r"`[^`]*`")
FM = re.compile(r"^---\n(.*?)\n---", re.S)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)([^$\n]+?)(?<!\\)\$")


def field(fm_text: str, key: str):
    m = re.search(rf"^{key}:\s*(.+)$", fm_text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if v.startswith("["):
        return [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
    return v.strip("\"'")


def main() -> int:
    md = [
        p
        for p in ROOT.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts)
    ]
    ref = collections.defaultdict(set)      # obsidian.nvim 视角
    obsidian_ref = collections.defaultdict(set)  # Obsidian 桌面版视角（文件名/路径/别名）
    suffix = collections.defaultdict(set)   # 路径后缀
    for p in md:
        t = p.read_text(encoding="utf-8", errors="replace")
        m = FM.match(t)
        f = m.group(1) if m else ""
        h1 = re.search(r"^#\s+(.+)$", t, re.M)
        ids = {p.stem, p.name}
        for x in (field(f, "id"), field(f, "title"), (h1.group(1).strip() if h1 else None)):
            if x:
                ids.add(x)
        aliases = field(f, "aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        ids.update(a for a in aliases if a)
        for x in ids:
            ref[x].add(p)
        for x in {p.stem, p.name} | {a for a in aliases if a}:
            obsidian_ref[x].add(p)
        parts = p.relative_to(ROOT).with_suffix("").parts
        for i in range(len(parts)):
            suffix["/".join(parts[i:])].add(p)

    bare, path_amb, broken, math_bad = [], [], [], []
    for p in md:
        t = p.read_text(encoding="utf-8", errors="replace")
        stripped = CODE.sub(lambda m: " " * len(m.group(0)), t)
        for m in INLINE_MATH.finditer(stripped):
            if "[[" in m.group(1):
                math_bad.append((str(p.relative_to(ROOT)), t[: m.start()].count("\n") + 1, m.group(0)[:60]))
        for m in LINK.finditer(stripped):
            raw = m.group(1)
            target = raw.split("|")[0].split("#")[0].strip()
            if not target or ATTACH.search(target):
                continue
            ln = t[: m.start()].count("\n") + 1
            rel = str(p.relative_to(ROOT))
            if "/" in target:
                cands = suffix.get(target, set()) - {p}
                if len(cands) > 1:
                    path_amb.append((rel, ln, raw, sorted(str(c.relative_to(ROOT)) for c in cands)))
                elif not cands:
                    broken.append((rel, ln, raw))
            else:
                nvim = ref.get(target, set()) - {p}
                obs = obsidian_ref.get(target, set()) - {p}
                if len(nvim) > 1:
                    bare.append((rel, ln, raw, sorted(str(c.relative_to(ROOT)) for c in nvim),
                                 "Obsidian 也会歧义" if len(obs) > 1 else "只有 nvim 会歧义"))
                elif not obs:
                    broken.append((rel, ln, raw))

    def dump(title, rows):
        print(f"\n【{title}】{len(rows)} 处")
        seen = set()
        for r in rows[:25]:
            key = str(r[2:4])
            if key in seen:
                continue
            seen.add(key)
            if len(r) == 5:
                print(f"   {r[0]}:{r[1]}  [[{r[2]}]]  ({r[4]})")
                for c in r[3]:
                    print(f"        候选 {c}")
            elif len(r) == 4:
                print(f"   {r[0]}:{r[1]}  [[{r[2]}]]")
                for c in r[3]:
                    print(f"        候选 {c}")
            else:
                print(f"   {r[0]}:{r[1]}  片段 {r[2]}")
        if len(rows) > 25:
            print(f"   …另有 {len(rows) - 25} 处")

    total = len(md)
    print(f"扫描 {ROOT}：{total} 篇笔记")
    dump("裸链二义", bare)
    dump("路径链接二义", path_amb)
    dump("断链", broken)
    dump("数学记号误判", math_bad)
    bad = len(bare) + len(path_amb) + len(broken) + len(math_bad)
    print("\n合计问题：%d 处%s" % (bad, "" if bad == 0 else "（需要修）"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
