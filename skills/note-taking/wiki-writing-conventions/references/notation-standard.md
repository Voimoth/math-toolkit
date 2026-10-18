---
title: 记号约定
created: 2026-10-19
updated: 2026-10-19
type: convention
tags: [notation, convention]
confidence: high
---

# 记号约定

全库统一写法的唯一权威。机器规则是技能里的 `notation-rules.json`，本文由
`check_notation.py --emit-doc` 生成，不要手改；要改规则改 JSON 再重新生成。

检查：`python3 ~/.hermes/skills/note-taking/wiki-writing-conventions/scripts/check_notation.py --check`。
门禁：改完笔记或概念页后必须全 0 才能提交。

## 1. 总表

| 对象 | 标准写法 | 禁用/避免 |
|---|---|---|
| 经典群 | `\mathrm{GL}_n(K)`、`\mathrm{SL}_n`、`\mathrm{PGL}_n`、`\mathrm{PSL}_n`、`\mathrm{O}`、`\mathrm{SO}`、`\mathrm{U}`、`\mathrm{SU}`、`\mathrm{Sp}`：字母正体，阶数作下标 | `\mathcal{GL}`、`\text{GL}`、裸 `GL`（数学段内） |
| 对称群 | `\mathfrak{S}_n`（哥特体 S） | `S_n`、`\mathcal{S}_n`、`\mathbb{S}_n` |
| 交错群 | `\mathfrak{A}_n` | `A_n`、`\mathcal{A}_n` |
| 自同构群 | `\operatorname{Aut}`、`\operatorname{Int}`、`\operatorname{Out}` | `\mathrm{Aut}`、`\text{Aut}`、裸 `Aut` |
| 同态与自同态 | 群/模：`\operatorname{Hom}`、`\operatorname{End}`；向量空间：`\mathcal{L}(E,F)` | `\mathrm{Hom}`、裸 `Hom`；向量空间用 `\operatorname{Hom}` 与 `\mathcal{L}` 混用 |
| 核与像 | `\ker`（LaTeX 原生算子）、`\operatorname{Im}`、`\operatorname{coker}` | `\operatorname{Ker}`（大写 K）、`\mathrm{Im}`、`\text{Im}`、裸 `Im` |
| 恒等映射 | `\mathrm{Id}_E`（大写 I） | `\operatorname{id}`、`\mathrm{id}`、裸 `id`/`Id` |
| 张成子空间 | `\operatorname{Vect}` | `span`、`\mathrm{Vect}`、裸 `Vect` |
| 基数 | `\operatorname{Card}(X)`，或元素个数 `|X|` | 裸 `Card`、`\mathrm{Card}` |
| 自然常数的底 | `\mathrm{e}^x`（正体 e） | 斜体 `e^x` |
| 置换的符号 | `\varepsilon(\sigma)`（同页只用一种，定义处注明也叫 signe） | 同一门课内混用 `\operatorname{sgn}` 与 `\varepsilon`（代数I 用 sgn、代数III 用 ε，属跨课差异，各自课内统一即可） |
| 导群 | `\mathfrak{D}(G)`（讲义另写作 `\mathcal{D}`，只保留一种） | `\mathcal{D}(G)` 与 `\mathfrak{D}(G)` 混用 |

## 2. 分课程的差异（允许存在，必须登记）

| 课程 | 对象 | 保留写法 | 说明 |
|---|---|---|---|
| 代数III | 中心化子 | 正课 `Z_G(a)` / 习题课 `C_G(a)` | 正课为准，习题课保留并在此登记；`Z(G)=\bigcap_a Z(a)` |
| 代数III | 二面体群 | 正课 `D_{2n}`（2n 阶）/ 习题课 `D_n` | 正课为准 |
| 代数III | 换位子 | `[a,b]=aba^{-1}b^{-1}` | 代数I 习题课用 `a^{-1}b^{-1}ab`；互为逆、互换，生成同一子群 |
| 代数II | 对称/反对称矩阵 | `\mathcal{S}_n(K)`、`\mathcal{A}_n(K)` | 与对称群 `\mathfrak{S}_n` 区分：带 `(K)` 的是矩阵空间 |
| 物理/理论力学 | 离心率 | 斜体 `e` | 轨道力学里的 e 不是自然常数 |

## 3. 脚本不管、需要人判的

- 转置 `^T` 改成左上 t：需按出现处逐个改（涉及被转置对象成组），脚本不动，见 `--list manual`
- `S_n`/`A_n` 在分析、概率课不是群（部分和、事件），作用域已限定在代数课程
- `\mathcal{S}_n(K)`/`\mathcal{A}_n(K)` 是代数II 的对称/反对称矩阵，不是群，规则用 `(?!\s*\()` 排除后仍需抽查

## 4. 使用

- 改笔记/概念页之前之后各跑一次 `--check`；`--apply` 会先备份到 `~/.hermes/cache/notation-backup/`。
- 单课迁移完就提交一次，commit message 用「记号统一：<课程>」，可单课回滚。
