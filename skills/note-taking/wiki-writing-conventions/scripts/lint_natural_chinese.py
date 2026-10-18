#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中文自然度检查器（只读，**绝不改写**）。

来源与改造：2026-10-07 借鉴 pika_math_learning_toolkit-2.1.5 的
`obsidian-vault-notes/references/natural-chinese-lint.json`（AGPL 项目的规则集），
按本 vault 的写作场景（数学概念页/课程笔记/答疑沉淀）重写：
  - 只扫散文，自动跳过 fenced code block、行内代码、$...$ 与 $$...$$ 数学区、callout 标记行
  - 规则分十类：英译腔 / 空名词 / 搭配不稳 / 模板句 / AI 总结腔 / 意义拔高 /
    写作预告 / 修改过程泄漏 / 模糊归因 / 宣传腔
  - 每条给「怎么改」的提示；低置信度规则只在 --all 时输出
  - 输出只是提示，**不是判定**：命中不等于写错，需人工判断是否真该改

用法：
    python3 lint_natural_chinese.py <文件或目录> [...]        # 只报中/高置信度
    python3 lint_natural_chinese.py --all <路径>              # 连低置信度一起报
    python3 lint_natural_chinese.py --json <路径>             # 机器可读
退出码：0 = 无命中；1 = 有命中；2 = 用法/读取错误。
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

# ---------------------------------------------------------------- 规则表
# kind: "phrase" 字面包含；"regex" 正则
# level: "high" / "medium" / "low"（--all 才报 low）
RULES = [
    # ---- 英译腔（calque）
    ("calque_into", "英译腔", "regex", r"把[^。；！？\n]{1,24}(?:接入|接到|引入到)[^。；！？\n]{0,24}上",
     "英译腔：改写为「把工具用在问题上」这类自然搭配", "high"),
    ("calque_make_possible", "英译腔", "regex", r"使[^。；！？\n]{0,16}成为可能",
     "英译腔：直接写「因此可以……」，或写清前提", "high"),
    ("calque_give_meaning", "英译腔", "regex", r"赋予了?[^。；！？\n]{0,16}(?:的)?(?:意义|价值|含义)",
     "英译腔：说明它具体改变了什么判断", "medium"),
    ("calque_conduct", "英译腔", "regex", r"进行(?:一个|一次)[^。；！？\n]{0,10}(?:操作|处理|计算|验证)",
     "英译腔：直接写「算一遍」「验证一下」", "medium"),
    ("calque_regarding", "英译腔", "regex", r"(?:关于|对于)这一点[，,]?我们(?:可以|将)",
     "英译腔：去掉「关于这一点」，直接写判断", "medium"),

    # ---- 空名词（empty noun）
    ("empty_content", "空名词", "phrase", "候选内容",
     "「内容」过空：说明是定义、反例还是思路", "medium"),
    ("empty_work", "空名词", "regex", r"(?:局部|相关|一段(?:可靠|重要)的)工作",
     "「工作」过空：说明是哪些具体任务", "medium"),
    ("empty_degree", "空名词", "regex", r"(?:渗透|参与|影响|抽象)程度",
     "抽象名词：说明具体到什么程度、体现在哪", "medium"),
    ("empty_signal", "空名词", "regex", r"(?:提供|给出|发出)的?信号",
     "「信号」缺所指：说明它用来判断什么", "medium"),
    ("empty_level", "空名词", "regex", r"在[^。；！？\n]{0,10}(?:层面|维度|角度)上",
     "「层面/维度/角度」常是空壳：直接写实际关系", "low"),

    # ---- 搭配不稳（collocation）
    ("colloc_quantifier_intent", "搭配不稳", "phrase", "对量词的意图有歧义",
     "歧义在表述，不在「意图」", "medium"),
    ("colloc_cheap", "搭配不稳", "regex", r"(?:筛查|筛选|检索)[^。；！？\n]{0,8}(?:更便宜|成本更低)",
     "成本隐喻：说明省的是时间、算力还是维护成本", "medium"),
    ("colloc_passive_no_actor", "搭配不稳", "regex", r"(?:问题|题目|路线|思路)[^。；！？\n]{0,20}被(?:查找|测试|搜索|继续检查)",
     "被动句缺施事者：写明是谁在做", "medium"),

    # ---- 模板句（template）
    ("tpl_essence", "模板句", "phrase", "本质上是",
     "若只是给后文加抽象包装，直接写具体关系；确实概括了已论证的关系才留", "low"),
    ("tpl_core", "模板句", "phrase", "核心在于",
     "若只是强调引子，直接写原因或条件", "low"),
    ("tpl_dimensions", "模板句", "regex", r"从(?:三个|几个|多个)(?:维度|方面|角度)(?:来看|来说)",
     "模板化结构：直接展开实际关系", "high"),
    ("tpl_reflect", "模板句", "phrase", "这背后反映了",
     "没有新增具体对象或证据时删去包装", "low"),
    ("tpl_never_but", "模板句", "regex", r"从来不是[^。；！？\n]{0,60}(?:而是|而在于)",
     "绝对反转：检查「从来」是否有证据；能否直接写判断", "low"),

    # ---- AI 总结腔（本 vault 最痛的一类：把讲义嚼碎喂回来）
    ("sum_in_conclusion", "AI 总结腔", "regex", r"^(?:综上(?:所述)?|总而言之|总的来说|一句话总结)[，,:：]",
     "总结腔：概念页不写收尾总结；把结论并进它该在的那一步", "medium"),
    ("sum_worth_noting", "AI 总结腔", "phrase", "值得注意的是",
     "空转过渡：后半句若本身重要就直接写；不重要就删", "medium"),
    ("sum_purpose_of", "AI 总结腔", "regex", r"本(?:讲|节|文|章)(?:的)?(?:目的|目标)(?:是|在于)",
     "讲义导语腔：直接进入问题本身", "high"),
    ("sum_we_can_see", "AI 总结腔", "regex", r"(?:我们|读者)(?:可以|能)(?:看到|发现|注意到)",
     "讲义腔：直接陈述看到的结论", "medium"),
    ("sum_obvious", "AI 总结腔", "phrase", "显而易见",
     "数学文里慎用：要么补出检查步骤，要么说清为什么平凡", "low"),

    # ---- 意义拔高（significance）
    ("sig_milestone", "意义拔高", "regex", r"(?:标志着|代表着|构成了)[^。；！？\n]{0,30}(?:重要|关键|历史性|里程碑式)[^。；！？\n]{0,4}(?:时刻|转折|节点|一步)",
     "意义拔高：保留事实，删掉无证据的历史性评价", "medium"),
    ("sig_broader", "意义拔高", "regex", r"(?:反映|体现|彰显|凸显)了?[^。；！？\n]{0,24}(?:更广泛|深远|持久|重要)(?:趋势|意义|影响|价值)",
     "抽象拔高：写出具体关系或来源", "medium"),

    # ---- 写作预告（announcement）
    ("ann_dive", "写作预告", "phrase", "让我们深入探讨",
     "写作预告：直接开始讲对象", "high"),
    ("ann_next", "写作预告", "regex", r"(?:下面|接下来)(?:我们)?(?:将|来)(?:讨论|分析|探讨|介绍|说明)",
     "写作预告：让正文直接开始工作", "high"),

    # ---- 修改过程泄漏（本 vault 明令禁止夹带改动过程）
    ("edit_leak", "修改过程泄漏", "regex", r"(?:本节|本文|这一段|这里|上面)(?:新增|补充|修改|重写|加入|删除)了",
     "改动过程泄漏：描述对象现在是什么，而不是这次改了什么", "high"),
    ("edit_leak_patch", "修改过程泄漏", "regex", r"(?:已|刚刚)(?:更新|修正|修复)(?:了)?(?:此处|这一?段|上面)",
     "改动过程泄漏：同上，改成对象本身的陈述", "high"),

    # ---- 模糊归因（vague attribution）
    ("attr_vague", "模糊归因", "regex", r"(?:专家|业内人士|观察者|多方|一些批评者|有观点)(?:普遍)?(?:认为|指出|表示|强调)",
     "模糊归因：给出笔记里的明确来源；无来源时不要把观点写成事实", "high"),
    ("attr_general", "模糊归因", "phrase", "一般认为",
     "需要出处：写清是谁的结果、在哪本书/哪篇论文", "medium"),

    # ---- 宣传腔（promotional / 商业黑话）
    ("promo_buzz", "宣传腔", "regex", r"(?:赋能|抓手|飞轮效应|闭环生态|全方位赋能)",
     "商业黑话：改写为可观察的事实", "high"),
    ("promo_praise", "宣传腔", "regex", r"(?:充满活力|令人叹为观止|璀璨)[^。；！？\n]{0,30}(?:丰富|文化遗产|体验|魅力)",
     "宣传词成组出现：改写为可观察的事实", "medium"),
    ("promo_future", "宣传腔", "regex", r"(?:前景(?:十分|非常)?光明|未来可期|未来(?:值得期待|充满希望))",
     "万能乐观结尾：改成已知计划、结果，或删除", "medium"),
]

# 白名单：出现这些词时不判（防误伤专业术语/代码词汇）
ALLOW = ["FTS5", "wikilink", "frontmatter", "block anchor", "Git", "LaTeX",
         "callout", "vault", "Obsidian", "commit", "push", "token"]

FENCE = re.compile(r"^\s*(```|~~~)")
CALLOUT = re.compile(r"^\s*>\s*\[!")
MATH_INLINE = re.compile(r"\$[^$\n]*\$")
MATH_BLOCK = re.compile(r"\$\$.*?\$\$", re.S)
CODE_INLINE = re.compile(r"`[^`\n]*`")


def strip_nonprose(line: str) -> str:
    """去掉行内代码与数学区，避免把公式当散文扫。"""
    line = CODE_INLINE.sub(" ", line)
    line = MATH_INLINE.sub(" ", line)
    return line


def iter_lines(path: str):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        in_fence = False
        buf, start = [], 1
        for n, line in enumerate(fh, 1):
            if FENCE.match(line):
                in_fence = not in_fence
                yield start, "".join(buf)  # 交出代码块之前的散文
                buf, start = [], n + 1
                continue
            if in_fence:
                continue
            if CALLOUT.match(line):
                yield n, ""            # callout 标记行不扫
                continue
            yield n, line


def scan_text(text: str):
    """整块文本里的 $$...$$ 单独处理：逐行扫时先挖掉块级数学。"""
    return MATH_BLOCK.sub(" ", text)


def check_file(path: str, level_all: bool):
    hits = []
    for lineno, raw in iter_lines(path):
        line = strip_nonprose(scan_text(raw))
        if not line.strip():
            continue
        if any(a in line for a in ALLOW):
            continue
        for rid, cat, kind, pat, hint, level in RULES:
            if level == "low" and not level_all:
                continue
            found = None
            if kind == "phrase":
                if pat in line:
                    found = pat
            else:
                m = re.search(pat, line)
                if m:
                    found = m.group(0)
            if found:
                hits.append({"file": path, "line": lineno, "rule": rid, "category": cat,
                             "evidence": found, "hint": hint, "level": level})
    return hits


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                for f in sorted(files):
                    if f.endswith(".md"):
                        out.append(os.path.join(root, f))
        elif os.path.isfile(p):
            out.append(p)
        else:
            print(f"跳过（不存在）: {p}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description="中文自然度检查（只读）")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--all", action="store_true", help="连低置信度规则一起报")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    files = collect(args.paths)
    if not files:
        print("没有可检查的 .md 文件", file=sys.stderr)
        return 2

    hits = []
    for f in files:
        try:
            hits.extend(check_file(f, args.all))
        except OSError as exc:
            print(f"读取失败 {f}: {exc}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps({"files": len(files), "hits": hits}, ensure_ascii=False, indent=2))
    else:
        for h in hits:
            print(f"{h['file']}:{h['line']}  [{h['category']}/{h['rule']}]  「{h['evidence']}」")
            print(f"    → {h['hint']}")
        by_cat = {}
        for h in hits:
            by_cat[h["category"]] = by_cat.get(h["category"], 0) + 1
        print(f"\n合计 {len(hits)} 处命中，{len(files)} 个文件" +
              ("；分类：" + "、".join(f"{k} {v}" for k, v in sorted(by_cat.items(), key=lambda x: -x[1])) if hits else ""))
        print("提示：命中只是提示，不是判定；改不改由写作者判断。")

    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
