#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""记号检查器：统一 vault 数学段内的记号写法。

规则唯一来源：同目录 ../references/notation-rules.json

用法（默认根目录 /mnt/e/notes）：
  check_notation.py --check [路径 ...]     只报违规；有违规则退出码 1
  check_notation.py --apply [路径 ...]     就地修复（先备份到 ~/.hermes/cache/notation-backup/）
  check_notation.py --emit-doc [--out F]   生成人读版《记号约定》文档
  check_notation.py --list-manual          列出需人工处理的项（如转置）

设计约束：
- 只改数学段（$...$ / $$...$$ / \\(...\\) / \\[...\\]），代码块与行内代码不动；
- 作用域按 JSON 里的 courses/files 前缀匹配，跨课程的差异靠 omissions 排除；
- 不做语义判断的项（转置、S_n 在非代数课）一律不进 fix，交给 --list-manual。
"""
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(HERE, "..", "references", "notation-rules.json")
DEFAULT_ROOT = "/mnt/e/notes"
SKIP_DIRS = {".git", ".obsidian", ".trash", "__pycache__"}
SKIP_FILES = {"log.md"}

MATH_RE = re.compile(
    r"\$\$(?:\\.|[^$])*?\$\$"          # $$...$$
    r"|\$(?:\\.|[^$\n])*?\$"           # $...$
    r"|\\\[(?:\\.|[^\]])*?\\\]"        # \[...\]
    r"|\\\((?:\\.|[^)])*?\\\)",        # \(...\)
    re.S,
)


def load_rules():
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


def iter_md(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for name in sorted(fn):
            if not name.endswith(".md"):
                continue
            if name in SKIP_FILES:
                continue
            yield os.path.join(dp, name)


def rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def in_scope(family, rpath):
    scope = family.get("scope", {})
    for exact in scope.get("files", []):
        if rpath == exact:
            return True
    for c in scope.get("courses", []):
        if rpath == c or rpath.startswith(c + "/"):
            return True
    return False


def mask_code(text):
    """把代码块/行内代码替换成等长空格，保持位置不变。"""
    out = list(text)

    def blank(a, b):
        for i in range(a, b):
            if out[i] != "\n":
                out[i] = " "

    for m in re.finditer(r"```.*?```", text, re.S):
        blank(m.start(), m.end())
    for m in re.finditer(r"`[^`\n]+`", text):
        blank(m.start(), m.end())
    return "".join(out)


def math_spans(text):
    masked = mask_code(text)
    return [(m.start(), m.end()) for m in MATH_RE.finditer(masked)]


def apply_families(seg, families, rpath):
    hits = []
    for fam in families:
        if not in_scope(fam, rpath):
            continue
        for fix in fam.get("fix", []):
            pat = re.compile(fix["pattern"])
            new, n = pat.subn(fix["repl"], seg)
            if n and new != seg:
                hits.append((fam["id"], fam["name"], n, seg[:80]))
                seg = new
    return seg, hits


def process(path, root, families, do_apply):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    spans = math_spans(text)
    if not spans:
        return 0, []
    out = []
    last = 0
    total = 0
    detail = []
    for a, b in spans:
        out.append(text[last:a])
        seg, hits = apply_families(text[a:b], families, rel(path, root))
        out.append(seg)
        if hits:
            total += sum(h[2] for h in hits)
            detail.extend(hits)
        last = b
    out.append(text[last:])
    new_text = "".join(out)
    if do_apply and new_text != text:
        backup(path, root)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return total, detail


BACKUP_DIR = None


def backup(path, root):
    global BACKUP_DIR
    if BACKUP_DIR is None:
        BACKUP_DIR = os.path.join(
            os.path.expanduser("~"), ".hermes", "cache", "notation-backup",
            time.strftime("%Y%m%d-%H%M%S"))
    dst = os.path.join(BACKUP_DIR, rel(path, root))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)


def emit_doc(rules, out_path):
    lines = ["---", "title: 记号约定", "created: 2026-10-19", "updated: " + rules["updated"],
             "type: convention", "tags: [notation, convention]", "confidence: high", "---", "",
             "# 记号约定", "",
             "全库统一写法的唯一权威。机器规则是技能里的 `notation-rules.json`，本文由",
             "`check_notation.py --emit-doc` 生成，不要手改；要改规则改 JSON 再重新生成。", "",
             "检查：`python3 ~/.hermes/skills/note-taking/wiki-writing-conventions/scripts/check_notation.py --check`。",
             "门禁：改完笔记或概念页后必须全 0 才能提交。", "",
             "## 1. 总表", "",
             "| 对象 | 标准写法 | 禁用/避免 |", "|---|---|---|"]
    for fam in rules["families"]:
        lines.append(f"| {fam['name']} | {fam['doc']} | {fam['doc_ban']} |")
    lines += ["", "## 2. 分课程的差异（允许存在，必须登记）", "",
              "| 课程 | 对象 | 保留写法 | 说明 |", "|---|---|---|---|"]
    for ex in rules.get("course_exceptions", []):
        lines.append(f"| {ex['course']} | {ex['item']} | {ex['kept']} | {ex['note']} |")
    lines += ["", "## 3. 脚本不管、需要人判的", ""]
    for m in rules.get("manual_checks", []):
        lines.append("- " + m)
    lines += ["", "## 4. 使用", "",
              "- 改笔记/概念页之前之后各跑一次 `--check`；`--apply` 会先备份到 `~/.hermes/cache/notation-backup/`。",
              "- 单课迁移完就提交一次，commit message 用「记号统一：<课程>」，可单课回滚。"]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out_path


def main():
    args = sys.argv[1:]
    mode = "--check"
    paths = []
    out = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--check", "--apply", "--emit-doc", "--list-manual"):
            mode = a
        elif a == "--out":
            i += 1
            out = args[i]
        else:
            paths.append(a)
        i += 1
    rules = load_rules()
    root = DEFAULT_ROOT
    if mode == "--list-manual":
        for m in rules.get("manual_checks", []):
            print("- " + m)
        return 0
    if mode == "--emit-doc":
        p = emit_doc(rules, out or os.path.join(root, "共享", "记号约定.md"))
        print("written:", p)
        return 0
    targets = paths or [root]
    files = []
    for t in targets:
        if os.path.isfile(t):
            files.append(t)
        else:
            files.extend(iter_md(t))
    per = {}
    grand = 0
    for f in files:
        n, detail = process(f, root, rules["families"], mode == "--apply")
        if n:
            grand += n
            key = rel(f, root).split("/")
            key = "/".join(key[:3]) if len(key) > 3 else "/".join(key[:2])
            per.setdefault(key, []).append((rel(f, root), n, detail))
    verb = "修复" if mode == "--apply" else "违规"
    for key in sorted(per):
        s = sum(x[1] for x in per[key])
        print(f"\n{key}: {verb} {s} 处 / {len(per[key])} 个文件")
        for rp, n, detail in per[key][:6]:
            fams = ", ".join(f"{h[1]}x{h[2]}" for h in detail[:4])
            print(f"  {rp}: {n}  ({fams})")
        if len(per[key]) > 6:
            print(f"  ... 另有 {len(per[key]) - 6} 个文件")
    print(f"\n合计{verb}: {grand} 处，涉及 {len(files)} 个文件")
    return 0 if (mode == "--apply" or grand == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
