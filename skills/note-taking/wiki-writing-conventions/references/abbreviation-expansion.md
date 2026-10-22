# 缩写展开（vault 文字规范）

用户的硬要求：**所有笔记里的所有文字缩写都展开写，不保留缩写**。适用于正文、`\text{...}` 内、标题、callout 标签。

## 判据：什么算「缩写」，什么不算

**展开**：Prop./Th./Thm./Déf./Def./Théor./Lem./Cor./Rem./Rq.、s.t.、tq（法语 tel que）、i.e.、e.g.、iff、ssi、resp.、coeff、fcts、mult.、w.r.t.、o.n.b.、reps/repn、f.d.、h.w.、ind rep、Irr rep、`\text{Part}_n`、ex.、Démo、v.a.、s.e.v/sev、CNS（除非在解释句里）。

**保留（是记号不是缩写）**：

- 标准数学记号：GL_n、SL_n、Hom、End、Aut、ker、Im、coker、dim、rg、tr、det、id、sup、inf、max、min、Vect、Mat、Card、pgcd、ppcm。
- LaTeX 命令：`\iff`、`\implies`、`\Longleftrightarrow`。
- 拉丁/统计学通行写法：`etc.`、`p.s.`（presque sûrement）、`i.i.d.`。
- **正在解释缩写本身的句子**：`（if and only if，iff；si et seulement si，ssi）`、`condition nécessaire et suffisante (CNS)`。
- 代码块、URL、frontmatter 的 tags 与 wikilink 目标不动。

## 语言判定（最容易搞错，必须先做）

**callout 标签/展开词的语言跟该文件的正文语言，不跟原标签。**

- 判据：剥掉代码块与 `$...$` / `$$...$$` 后，中文字符占非空白字符比例 >15% → 中文笔记（标签用「定义/命题/定理/推论/注记/引理」，s.t.→使得、i.e.→即）；否则按法语（Définition/Proposition/Théorème/Corollaire/Remarque，s.t.→tel que、i.e.→c'est-à-dire、ssi→si et seulement si）或英语。
- **不要用整篇 CJK 比例**：数学笔记公式密集，会把比例压到 0.08 以下误判成外文。
- **不要用「现有标签投票」**：标签已被上一轮改成外文时，投票会自指，产出「中文正文 + Définition」混排。

## 映射表

中文：定义 / 命题 / 定理 / 推论 / 引理 / 注记；s.t.→使得、i.e.→即、e.g.→例如、resp.→分别、iff→当且仅当、Démo→证明

法语：Définition / Proposition / Théorème / Corollaire / Lemme / Remarque；s.t.→tel que、tq→tel que、i.e.→c'est-à-dire、e.g.→par exemple、resp.→respectivement、ssi→si et seulement si、ex.→exemple、Démo→Démonstration、coeff→coefficients、**v.a.→variable(s) aléatoire(s)**（按 une/des/les/deux/ces 判单复数）、**sev/s.e.v→sous-espace(s) vectoriel(s)**（同样按量词判复数）

英语：Definition / Proposition / Theorem / Corollary / Lemma / Remark；s.t.→such that、i.e.→that is、iff→if and only if、e.g.→for example

数学内容里的缩写：reps/repn→representations、f.d.→finite dimensional、h.w.→highest weight、o.n.b.→orthonormal basis、ind rep→induced representation、Irr rep→irreducible representations、`\text{Part}_n`→`\lambda` a partition of `n`、mult.→multiplication、fcts→functions、w.r.t.→with respect to

## 统计与扫描的正则坑

- `\biff\b` 会命中 LaTeX 的 `\iff`（`\` 与 `i` 之间有词边界）→ 必须写 `(?<!\\)\biff\b`。
- 带点缩写**不要用尾部 `\b`**：`s\.t\.\b` 在「s.t. + 空格」处不成立（`.` 与空格都不是 word 字符）→ 用 `(?<![\w\\.])s\.t\.`。
- 别名要一次列全：`Prop.|Th.|Thm.|Déf.|Def.|Théor.|Lem.|Cor.|Rem.|Rq.|ex.|Démo|tq|ssi|iff|v\.a\.|s\.?e\.?v|coeff|fcts?|mult\.|i\.e\.|e\.g\.|resp\.|etc\.` —— 漏 `Th.`/`Rq.`/`Démo`/`v.a.`/`sev` 每一项都会多跑一轮返工。
- 数「处数」用 `re.finditer`，不要 `grep -c`（按行计，一行多处被压成 1）。
- 标签替换的正则要允许 `（`、`(`、空格、行尾，以及 `Définition/Proposition` 这种斜杠连写。

## 批量执行（上百文件时）

- 先按目录/文件数切成互不重叠的清单文件（`/tmp/abbr/T1.txt` …），每个子代理读同一份规则文件 + 自己的清单。
- 子代理只改清单里的文件、**禁止 git 操作**；父代理统一复核后一次性 commit + push。
- **子代理之间的口径一定会飘**（同一任务里一批用法语全词、一批用中文标签；单复数、冠词也各异）：父代理必须用同一判据再跑一遍收口，并复核每个文件的正文语言，别信汇总口径。
- 复核门槛：所有改动文件跑 `check_formulas.js`（0 失败）+ `check_notation.py --check`（0 违规）+ `check_wikilinks.py`（0 问题）+ `git diff --numstat` 增删行数相等（纯行内替换）+ 抽 2–3 组 diff 看展开后的句子（单复数、冠词）是否自然。
- 公式引擎校验脚本与安装方式见 `math-notes-transcription` 的 `references/formula-render-check.md`（`check_formulas.js`）。
