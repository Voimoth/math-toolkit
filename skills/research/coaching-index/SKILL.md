---
name: coaching-index
description: "Use when 开始某科辅导、问某科讲到哪、或要建内容库时:全科地图。"
version: 1.1.0
author: Hermes Agent
created_by: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [math, physics, tutoring, index, zh]
    category: research
---

# 学科辅导总索引（科目地图与材料位置）

新会话开始辅导前先看这里：每科去哪个技能、讲义与题在哪。**进度和待办不在这里**——单一账本是 vault 的 `共享/辅导进度.md`，讲透一段就直接改那里，不攒到会话末。

## When to Use

- 新会话要开某科辅导或复习 → 先读「科目地图」定位技能，再读 `共享/辅导进度.md` 看讲到哪。
- 用户问「某科我们讲到哪了 / 之前讲过什么」。
- 要决定是否给某科新建内容层技能；要找某科题源。

## 三层分工（勿改）

1. **方法层**：`math-coach` —— 怎么教（四条原则、决策序列、模式 A/B、硬约束）。只此一处，课程技能不重复方法。
2. **内容层**：每门课一个技能 —— 老师记号、讲义来源、已沉淀的卡点与教法。
3. **账本层**：`/mnt/e/notes/共享/辅导进度.md` —— 讲到哪、欠什么、下次复习日期。本索引只做地图，不复述进度。

## 科目地图

| 科目 | 内容层技能 | 一句话主线 | 入口 |
|---|---|---|---|
| 代数 III（群论） | `algebra-iii-coaching` | 把作用的轨道/稳定子/不动点翻译成群的结构信息 | `数学/代数/代数III/笔记/00-总览` |
| 理论力学 B | `mechanics-coaching` | 作用量取极值 → E-L 方程；刚体多出 $\boldsymbol\omega\times$；哈密顿在相空间变分 | `物理/理论力学/`（概念页 37 个平铺，速查在 `速查/`） |
| 点集拓扑（分析 III） | `point-set-topology-coaching` | 商空间与分离公理：从紧性、连通性走到 Urysohn 与 Tietze | `点集拓扑学习路径` |
| 情绪低谷陪伴（非教学） | `morale-crisis-coaching` | 倦怠与意义危机时先陪，不切辅导模式 | — |

## 只有 vault 内容、尚无内容库的科目

- **分析 III**：Fourier 全课程完成（概念页 27）；多变量微积分只有讲义、未开讲；点集拓扑有独立技能。
- **分析 I / 分析 II / 代数 I**：笔记与概念页已在 vault，讲课时直接读 vault，不另建技能。
- **代数 II**：目录已建、无内容。
- **概率**：他自建的 LaTeX 残稿在 `/mnt/e/latex/Mathématiques/Probabilités/`（`Ch.N <章名>/N.M <节名>/`，Ch.1 到 1.3，Ch.2–3 部分），宏在 `/mnt/e/latex/macro/macros.tex`。整理时以它的术语与章节划分为准，落盘仍写 vault `概率/`。

判断某科该不该立内容库：已有稳定的老师记号 + 已沉淀卡点 + 会长期复习 → 立；否则只留 vault。

## 往年讲义（整理或讲课时的参考材料）

- **代数 III**：`/mnt/e/书籍/代数/代数III/` 有同一老师往年讲义（`Cours USTC 01-09-26.pdf` 一类）。
- **代数 I**：亦有同一老师往年讲义。
- **分析 I**：有往年讲义，非同一老师，可适度补充。

整理或讲这几门课前先去 `/mnt/e/书籍/<学科>/<课程>/` 找，别只依赖当年手写扫描件。

## 题源（复习与混编题集）

- **代数 III**：`TD/Algebre1-TD1..TD12.pdf`（12 份，配往年讲义）与 `Exercices USTC Octobre 2026.pdf`；同级有 `往年考题/`、`习题课讲义/`、`手写笔记/`、`讲座/`。这道题的题源比分析多——他若说「代数没多少现成题」，先摆这份清单。
- **分析 III**：Fourier `Fourier/TD/td1–td7.pdf`；点集拓扑 `点集拓扑/TD/topo_td_02–05.pdf`；作业合集在 `书籍/分析/分析III/` 外层（`分析III-作业合集（第1-7周）.pdf` 等）。
- 混编题集怎么排（字段、有效条件、群论的三类判断边界）见 `math-coach/references/study-budget-and-review.md` §11。

## 手写笔记整理流水线

pdftoppm 300dpi 转图（中间产物放 `~/.hermes/cache/`，不进 vault）→ 视觉模型逐页转写 → 机械修复（去前言、水印、坏定界符）→ 按内容切章 → 派子代理并行规范化（整门课约 10 个，各自只读同一份规范文件）→ 父代理统一复核（断链、emoji、渲染宏、禁用词、抽查、交换图箭头方向）→ 建 `00-总览` 与 `_索引` → git 提交。完整流程与踩坑见 `math-notes-transcription/references/whole-course-batch-workflow.md`。

## 维护规则

- 本文件只放**地图与材料位置**；进度、待办、复习日期一律写 `共享/辅导进度.md`。
- 新建或删除课程技能时改「科目地图」；vault 新增科目先在 `_索引.md` 登记，再加行。
- 内容不复制进本文件，避免两处不一致。

## 相关

- `math-coach` — 方法层唯一出处
- `algebra-iii-coaching` / `mechanics-coaching` / `point-set-topology-coaching` — 已有内容库
- `bookdex` — 跨 8000 本参考书查「哪本书讲过 X」
- `math-physics-wiki` / `wiki-writing-conventions` — vault 落盘与写作约定
