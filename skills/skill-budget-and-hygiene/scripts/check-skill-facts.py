#!/usr/bin/env python3
"""核查技能里断言的本机路径是否还存在。

端口不做检查：技能里的 `:8080`/`:5678` 指的是「该服务启动后应监听」，
会话语境下没起服务是常态，按「现在是否监听」判会 100% 误报（实测）。

用法:
    python3 check-skill-facts.py            # 全部启用的本地技能
    python3 check-skill-facts.py --all      # 连 disabled / bundled 一起
    python3 check-skill-facts.py --skill NAME

退出码: 0 = 无失效; 1 = 有失效引用(应修)。
输出即结果：每个失效引用给出旧路径、所属文件、以及按 basename 搜到的候选替代。
不生成「请人工核对」清单——要么能给出替代，要么明确标 UNRESOLVED 并给下一步命令。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict

SKILLS = os.path.expanduser('~/.hermes/skills')
CONFIG = os.path.expanduser('~/.hermes/config.yaml')
PATH_RE = re.compile(r'(?<![\w/])((?:/mnt/[a-z]|/home/_[a-z]+|~/)[\w\-./\u4e00-\u9fff]*)')
# 只核查「断言本机真实布局」的前缀；`~/Desktop`、`~/.config/<某应用>` 这类在
# 技能里绝大多数是举例，全查会出几百条误报（实测 282 条中 90% 是例子）。
CHECK_PREFIXES = ('/mnt/e/', '/mnt/g/', '/mnt/h/', '/home/_username/', '/opt/',
                  '~/.hermes/tools/', '~/.hermes/skills/', '~/.hermes/installs/',
                  '~/.local/bin/', '~/.local/share/', '~/.dsh/')
CAND_ROOTS = ['/mnt/e', '/mnt/h', '/mnt/g', os.path.expanduser('~/.hermes'), os.path.expanduser('~/.local/share'), '/opt']
SKIP_DIRS = {'.archive', '.hub', 'node_modules', '.git', '__pycache__'}


def disabled_names():
    try:
        import yaml
        cfg = yaml.safe_load(open(CONFIG, encoding='utf-8')) or {}
        return set((cfg.get('skills') or {}).get('disabled') or [])
    except Exception:
        return set()


def skill_files(include_all, only=None):
    out = []
    for root, dirs, files in os.walk(SKILLS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if 'SKILL.md' not in files:
            continue
        name = os.path.basename(root)
        if only and name != only:
            continue
        for f in ['SKILL.md'] + [os.path.join(dp, x)[len(root) + 1:]
                                 for dp, _, xs in os.walk(root) for x in xs if x.endswith('.md')]:
            p = os.path.join(root, f)
            if os.path.exists(p):
                out.append((name, p))
    return out


def _looks_like_path_tail(txt, end):
    """路径后面跟空格、且空格后是纯 ASCII 词（无标点）→ 原文路径被空格截断。"""
    m = re.match(r'\s+([A-Za-z0-9_.\-]{2,})\s', txt[end:end + 60])
    return bool(m)


def find_alternatives(old):
    base = os.path.basename(old.rstrip('/'))
    if len(base) < 6:
        return []
    hits = []
    for root in CAND_ROOTS:
        if not os.path.isdir(root):
            continue
        try:
            for dp, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                if base in dirs or base in files:
                    hits.append(os.path.join(dp, base))
                    if len(hits) >= 3:
                        return hits
        except Exception:
            continue
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--skill')
    ap.add_argument('--no-alternatives', action='store_true')
    ap.add_argument('--deep', action='store_true', help='连示例型路径一起列（噪音大）')
    a = ap.parse_args()
    disabled = disabled_names()
    dead_paths = defaultdict(list)   # skill -> [(file, path)]
    low_conf = []                    # 不在确认前缀里的引用（只计数，默认不报）
    artifacts = []                   # 省略号占位 / 被空格截断的提取伪影（只计数）
    seen = set()
    for name, p in skill_files(a.all, a.skill):
        if name in disabled and not (a.all or a.skill):
            continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        for m in PATH_RE.finditer(txt):
            s = re.sub(r'/+', '/', m.group(1)).rstrip('.,)」』、。；:：/')
            if len(s) < 6 or (name, s) in seen:
                continue
            # 省略号占位（`/mnt/h/.../x`）与空格截断（`common/Monster Hunter`）都是提取伪影，不是失效
            line_start = txt.rfind('\n', 0, m.start()) + 1
            line_end = txt.find('\n', m.end())
            line = txt[line_start:line_end if line_end > 0 else len(txt)]
            if re.search(r'已删|删掉|已废弃|不再存在|不存在|已清理|旧路径|原路径|移入回收站|运行时|才生成|若你|如果要', line):
                artifacts.append((name, p, s))
                continue
            if re.search(r'\.(log|db|pid|sock|probe|html|tmp)$', s):
                artifacts.append((name, p, s))
                continue
            if '...' in s or '…' in s:
                artifacts.append((name, p, s))
                continue
            tail = txt[m.end():m.end() + 1]
            if tail == ' ' and _looks_like_path_tail(txt, m.end()):
                artifacts.append((name, p, s))
                continue
            if not s.startswith(CHECK_PREFIXES):
                low_conf.append((name, p, s))
                continue
            seen.add((name, s))
            if os.path.exists(os.path.expanduser(s)):
                continue
            # 父目录存在、且目录里有以该 basename 开头的条目 → 原文路径被空格/标点截断，不是失效
            parent = os.path.dirname(os.path.expanduser(s))
            base = os.path.basename(s)
            if base and os.path.isdir(parent):
                try:
                    if any(e.startswith(base) for e in os.listdir(parent)):
                        artifacts.append((name, p, s))
                        continue
                except OSError:
                    pass
            dead_paths[name].append((p, s))

    total = sum(len(v) for v in dead_paths.values())
    if not total:
        print('OK: 无失效路径/端口引用')
        return 0
    print(f'失效路径 {total} 处，分属 {len(dead_paths)} 个技能\n')
    for name in sorted(dead_paths, key=lambda k: -len(dead_paths[k])):
        print(f'== {name}  ({len(dead_paths[name])} 处)')
        for f, s in dead_paths[name]:
            rel = f.replace(SKILLS + '/', '')
            alts = [] if a.no_alternatives else find_alternatives(s)
            if alts:
                print(f'   {s}\n     in {rel}\n     → 候选: {alts[0]}' + (f' (另有 {len(alts) - 1} 个)' if len(alts) > 1 else ''))
            else:
                print(f'   {s}  ← UNRESOLVED\n     in {rel}')


if __name__ == '__main__':
    sys.exit(main())
