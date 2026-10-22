#!/usr/bin/env python3
"""prose_lint.py — 中文数学文本的翻译腔 / 分段体检。

用法：
    prose_lint.py FILE            # 体检一个文本文件
    ... | prose_lint.py -         # 读 stdin

输出：每行一条命中，按行号排序，形如
    L12 名词化      的成立
    L14 长句(52字)  如果有偶数长度的循环且……
    L20 因果过密    本段 3 处「所以/因此/故」
末尾打印汇总。退出码：有 error 级命中返回 1，否则 0。标 (?) 的是提醒级。

设计原则：翻译腔不能靠「注意避免」——那靠每次自觉，收效甚微；
只能靠**发出前机械扫一遍**，命中就逐条改写。误报手动忽略，别纵容自己。
"""
from __future__ import annotations

import argparse
import re
import sys

# 级别 error = 直接改写；warn = 看情况，输出时标 (?)

# ---------- 句内层：翻译腔的机械特征 ----------
RULES: list[tuple[str, str, re.Pattern[str]]] = [
    # 名词化：「…的成立 / 的应用」是英文 nominalization 的直译
    ("名词化", "error", re.compile(r"的(成立|应用|证明|存在|满足|给出|定义|获取|达到|完成|扮演|实现)")),
    # 冠词直译：英文 a/an 的直译，中文多数场合不需要
    ("冠词直译", "warn", re.compile(
        r"一个(?!人|问题|群|元素|循环|轨道|集合|向量|矩阵|例子|猜想|步骤|动作|定理|命题|引理|条件|性质|结论|事实|对象|置换|函数|映射|子群|子空间|点)")),
    # 进行 + 名词：perform/conduct 直译
    ("进行+名词", "error", re.compile(r"进行(证明|讨论|分析|研究|处理|计算|验证|构造|说明|考虑)")),
    # 空转被动
    ("空转被动", "error", re.compile(r"被(证明|认为|称为|叫做|称作|给出|定义|发现|验证|使用|采用)")),
    # 译入虚词
    ("译入虚词", "warn", re.compile(
        r"(对[^，。]{1,12}而言|在[^，。]{1,12}的意义上|关于[^，。]{1,12}的问题|在[^，。]{1,12}的情况下|在[^，。]{1,12}的基础上|据我们所知|众所周知)")),
    # 铺垫套话
    ("铺垫套话", "error", re.compile(
        r"(事实上|实际上|总的来说|综上所述|值得注意的是|需要指出的是|不难看出|可以看出|由此可见|换句话说|值得一提的是)")),
    # 主语是「我们」
    ("我们做主语", "warn", re.compile(r"(^|[。；，])我们")),
    # 英→中直译动词：send / carry → 「送」在中文数学里不说（2026-10-22 用户点破）
    ("直译动词", "error", re.compile(r"(送(到|成|给|入)|搬运|给与|尊重(?!意见))")),
    # 模糊限定
    ("模糊限定", "warn", re.compile(r"(某种程度|较为|颇|一定程度上|或多或少|相应的)")),
]

# 因果/连接词：一段里出现多次 = 论证糊成一块
CAUSAL = re.compile(r"(所以|因此|故|于是|从而|由此)")
CONNECTORS = re.compile(r"(此外|然而|而且|并且|同时|另外)")

MAX_SENT_CHARS = 55      # 单句上限（warn）
MAX_PARA_LINES = 4       # 单段上限（error：人类推理不会糊成一块）
MAX_CAUSAL_PER_PARA = 1  # 每段因果词上限（error）


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[。！？；\n]", text) if s.strip()]


def paragraphs(lines: list[str]) -> list[tuple[int, list[str]]]:
    """按空行切段，返回 (起始行号, 行列表)。"""
    out, buf, start = [], [], None
    for i, ln in enumerate(lines, 1):
        if ln.strip() == "":
            if buf:
                out.append((start, buf))
                buf, start = [], None
        else:
            if start is None:
                start = i
            buf.append(ln)
    if buf:
        out.append((start, buf))
    return out


def lint(text: str) -> list[tuple[int, str, str]]:
    """返回 [(行号, 类型, 样本)]，未排序。"""
    hits: list[tuple[int, str, str]] = []
    lines = text.split("\n")

    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith(("MEDIA:", "```")):
            continue
        for name, level, pat in RULES:
            for m in pat.finditer(ln):
                label = name if level == "error" else f"{name}(?)"
                hits.append((i, label, m.group(0)[:24]))

    for i, ln in enumerate(lines, 1):
        for s in sentences(ln):
            core = re.sub(r"[\s\d\W]", "", s)
            if len(core) > MAX_SENT_CHARS:
                hits.append((i, f"长句({len(core)}字)(?)", s[:34] + "…"))

    for start, buf in paragraphs(lines):
        body = "\n".join(buf)
        n_causal = len(CAUSAL.findall(body))
        if n_causal > MAX_CAUSAL_PER_PARA:
            hits.append((start, "因果过密", f"本段 {n_causal} 处「所以/因此/故」→ 拆段"))
        if len(buf) > MAX_PARA_LINES:
            hits.append((start, "段落过长", f"{len(buf)} 行 → 一个动作一段"))
        n_conn = len(CONNECTORS.findall(body))
        if n_conn >= 2:
            hits.append((start, "连接词堆叠(?)", f"本段 {n_conn} 处「此外/然而/并且」"))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="文本文件路径，或 - 表示 stdin")
    a = ap.parse_args()
    text = sys.stdin.read() if a.path == "-" else open(a.path, encoding="utf-8").read()

    hits = sorted(lint(text), key=lambda h: (h[0], h[1]))
    for loc, kind, sample in hits:
        print(f"L{loc:<4} {kind:<16} {sample}")
    n_err = sum(1 for _, k, _ in hits if "(?)" not in k)
    print(f"\n合计 {len(hits)} 条（必须改 {n_err} 条，提醒 {len(hits) - n_err} 条）", file=sys.stderr)
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
