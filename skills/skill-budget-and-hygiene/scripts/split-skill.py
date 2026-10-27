#!/usr/bin/env python3
"""把一个 SKILL.md 的超大节搬到 references/，正文只留首段 + 指针。

用法:
    python3 split-skill.py PATH \
        --move '## 0. 先认清=references/machine-config-model.md' \
        --move '## 坑（全部实测踩过）=references/pitfalls.md' [--dry]

规则（不可协商，来自 skill-budget-and-hygiene）：
- 切割边界只落在 `## ` 标题行上；搬走的整节**原文零删改**进 references。
- 正文保留：节标题 + 该节第一段（截断 260 字符）+ `→ 全文见 references/...`。
- 多个 --move 指向同一 references 文件时合并进同一个文件。
- 完成后自动做子串证全：每个搬走的节必须在 references 里、且不在正文里。
- 目标：正文 ≤8,000 字符（脚本末尾会报，超了自己继续 --move）。
"""
import argparse
import os
import re
import sys


def parse_blocks(t):
    heads = [(m.start(), t[m.start():t.find('\n', m.start())]) for m in re.finditer(r'(?m)^## ', t)]
    if not heads:
        raise SystemExit('没有 ## 节标题可切')
    blocks = [(h, t[s:(heads[i + 1][0] if i + 1 < len(heads) else len(t))]) for i, (s, h) in enumerate(heads)]
    return t[:heads[0][0]], blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--move', action='append', default=[], help='节标题前缀=references/文件.md')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    path = os.path.expanduser(a.path)
    t = open(path, encoding='utf-8').read()
    pre, blocks = parse_blocks(t)
    if not a.move:
        print(f'{path}  {len(t)} 字符；节:')
        for h, b in blocks:
            print(f'  {len(b):6d}  {h[:70]}')
        return 0
    used, groups = set(), {}
    for spec in a.move:
        prefix, _, rf = spec.partition('=')
        if not rf.startswith('references/'):
            raise SystemExit(f'--move 的目标必须是 references/…: {spec}')
        for h, b in blocks:
            if h.startswith(prefix) and h not in used:
                used.add(h)
                groups.setdefault(rf, []).append((h, b))
                break
        else:
            raise SystemExit(f'没找到节: {prefix!r}（用不带 --move 跑一次看节标题）')
    out = pre + ''.join(b for h, b in blocks if h not in used)
    for rf, items in groups.items():
        for h, b in items:
            body = b.split('\n', 1)[1].strip('\n')
            paras = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
            summ = paras[0][:260] if paras else ''
            out += f'{h}\n\n{summ}\n\n→ 全文（含实测细节与命令）见 `{rf}`\n\n'
        fn = os.path.join(os.path.dirname(path), rf)
        txt = f"# {os.path.basename(rf).replace('.md', '')}（自 SKILL.md 搬家，原文零删改）\n\n"
        txt += '\n'.join(b for _, b in items)
        if not a.dry:
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            open(fn, 'w', encoding='utf-8').write(txt)
    # 子串证全
    refs = ''.join(open(os.path.join(os.path.dirname(path), rf), encoding='utf-8').read()
                   for rf in groups) if not a.dry else ''.join(b for items in groups.values() for _, b in items)
    lost, still = [], []
    for items in groups.values():
        for h, b in items:
            if b.strip() not in refs:
                lost.append(h)
            if b.strip() in out:
                still.append(h)
    print(f'{len(t)} -> {len(out)} 字符（上限 8000：{"OK" if len(out) <= 8000 else "仍超"}）')
    print(f'验证：丢失 {len(lost)} 节；正文残留 {len(still)} 节')
    for h in lost:
        print('  LOST', h)
    for h in still:
        print('  STILL-IN-BODY', h)
    if not a.dry:
        open(path, 'w', encoding='utf-8').write(out)
    return 0 if not (lost or still) else 1


if __name__ == '__main__':
    sys.exit(main())
