---
name: wiki-writing-conventions
description: "用户 wiki/Obsidian vault(/mnt/e/notes)的写作与维护约定:禁止 emoji、概念页≠题解汇编、一概念一文件、笔记拆章、vault 自包含、git 提交卫生、交换图用 array 写法且须核对箭头方向。触发:写/更新 wiki 页面、创建概念页、整理既有页面、统一记号、同步概念地图、git 提交 wiki 改动、改交换图时。"
version: 2.0.0
author: Hermes Agent
created_by: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, writing, conventions, zh, markdown]
    category: note-taking
---

# Wiki 写作约定（用户明确要求，2026-08）

本技能是用户 Obsidian vault（`/mnt/e/notes`，覆盖全部数学与物理课程）写作与维护的**唯一权威**。任何写/更新 vault 页面的操作都要遵守。
**正文只放最高频的铁律；细节按主题在 `references/`，见文末索引**（2026-10-03 从 59 KB 的单一文件拆分而来）。

## 1. 禁止 emoji（最高优先级）

> 用户原话：「你之后写文件的时候不要往里面插奇怪的emoji, 比如index.md里面那个五角星排版不太好看」

wiki 页面、文件、回复中**不插 emoji / 符号表情**（★ ⚠️ ✅ ❌ 📚 🎉 等）；改用纯文字（「注意」/「严格」/「五星推荐」）。

## 2. 概念页 ≠ 题解汇编（最常踩的边界）

- **删掉**：题号、题目专属数值与算例、凑题过程、作业建议、「与题面对照」的措辞。
- **保留**：概念本身（定义、为什么成立、证明要点、方法对比）＋**概念性**陷阱。
- **判据**：这句话**换个题目还成立吗**？不成立 ⇒ 属于题解，不进概念页（题解留在课程级 coaching 技能的 `references/`）。
- **笔记里也不要单独的「作业/练习」章**：只把与正文强相关的题作为 `> [!example]` 内嵌进对应小节，不写题号/出处。
- **但习题课笔记不适用「删题号」**：以助教印发的**编号讲义**为来源的习题课笔记（`笔记/习题课/NN-篇名.md`）本来就按讲义条目与编号组织，保留题面与 `（…，讲义 X.Y）` 标注（含往年考题出处）。判据是**来源形态**：手写习题流水 → 提炼成知识条目；编号讲义 → 按编号保留。详见 `math-notes-transcription` 的 `references/wiki-content-and-formatting-rules.md`「并入既有课程笔记系列」。
- **哪些课的习题课才建笔记，逐课定**：代数 I/III 的习题课建 `笔记/习题课/`；**分析 III 的 TD（法语习题课）不建笔记**（用户 2026-10-21 明确：「不要整理成笔记，建概念页就好」）——TD 只归档到资料库，其中的数学只以概念页形式落库（如由 TD 04/05 带出的 `紧性`、`连通性`）。新开课先问一次，别默认建 TD 笔记；已经建了的按此撤。
- **一概念一文件**（文件名用中文或法语）：概念页超 ~4 KB、或含 3 个以上独立概念，就该拆。

## 3. vault 结构

三个根:`数学/`、`物理/`、`共享/`;一概念一文件、概念页不夹题号与数值。
目录细则、每课子目录与命名、`_索引.md` 的写法 → `references/vault-structure.md`。


## 4. 其他必守项（速查）

- **callout 分层**：`> [!note] 定义/定理`、`> [!example] 例子`、`> [!tip] 想法/直觉`、`> […
- **callout 里放列表要留一个空 `>` 行**：`> [!note] 标题` 之后若紧跟 `> - …`，pandoc（预览用）会把列表…
- **法国记号**：全库记号标准见 `references/notation-standard.md`（含标准表、每课差异登记格式、迁移步骤）。最…
- **源笔记的数学错误：先判数学，再直接改，不留标注（2026-10-21 用户明确「笔误直接改掉不用标注」）**：转写/整理时若某陈述与证明或后…
- **用户会自己在 `[?]` 处批注与猜测，但不要照抄他的猜测**：他不懂具体数学，只是凭字形/记忆猜；正确做法是 **400dpi 重渲 + …
- **建页阈值**：概念在 2+ 来源出现、或是一个来源的核心主题才建页；一笔带过的不建。
- **答疑即沉淀、无需询问**：数学/物理问答的可复用内容**当轮**写入对应课程概念页——**禁止**问「要不要整理进 wiki」；**边教边沉…
- **git**：改完 `git add`（只加目标文件）＋ commit ＋ push；`log.md` 追加一条变更记录。（概念同步见 §6，…
- **Obsidian 会自己重排 frontmatter，保留就行**：用户开着 Obsidian 时插件会把页面改写成 properties …
- **对外发布配套仓库**：工具库独立成库，不塞进 vault；发布前用 `git ls-files` 扫身份信息与绝对路径（同步脚本与排除表本身…
- **交换图**：一律 `\begin{array}{c...c}` + `\xrightarrow`/`\xleftarrow`/`\big\d…
- **史实/出处类内容要有来源，未查实的标 `[?]`**：往页里写「谁先提出某概念、术语的来历、某结论的标准出处」时，
- **链接健康检查（写完就跑，不只清理时）**：`python3 <技能目录>/scripts/check_wikilinks.py /mnt/e…
- **中文自然度 / 改动过程泄漏（写完就跑）**：`python3 <技能目录>/scripts/lint_natural_chinese.py…
- **取改动文件清单要按 `-z` 解析，别 `awk '{print $2}'`**：仓库开了 `core.quotePath`，中文路径在 `…
- **检查脚本在 vault 根跑、传相对 vault 根的路径**：`check_wikilinks`/`check_notation`/`ch…
- **整篇重写地图类文件前先 `read_file` 全文**：`_索引` / `00-总览` / 学习路径 这类文件若本会话没读过全量，`wri…
- **callout 里的编号列表中间不要插独立公式行**：`> $$…$$` 另起一行会截断列表、后续编号从 1 重排；写成行内公式，或把公式缩…
- **自己新写的推导与原稿同一标准：先算对再落盘**：显式乘积、特征值、维数先在草稿里验算（矩阵逐项乘、迹与特征值之和互校），页内只留正确版本；不…
- **大编辑门槛（重写多小节 / 新建 >4 KB / 动编号 时必须走）**：候选先在 vault 外写好 → 跑完确定性检查 →


每条完整内容(含写法示例、验收方式、反例) → `references/must-follow-rules.md`。


## 5. 记号统一（机器可查，不靠记性）

- **单一数据源**：`references/notation-rules.json`（机器规则）。人读的两份都由它生成，**不手写**：`references/notation-standard.md` 与 vault 的 `共享/记号约定.md`；改规则只改 JSON，再跑 `--emit-doc`。
- **写完/改完含数学的文件就跑**：`python3 <技能目录>/scripts/check_notation.py --check`（默认扫全库，可给单课路径）；`--apply` 之前先出 dry-run 报表，`--apply` 会自动备份被改文件到 `~/.hermes/cache/notation-backup/`。
- **裸符号必须按课程限定作用域，并记住同形不同义**：`S_n` 在分析与概率课是部分和；`S_i` 在 Coxeter 群页是单反射；`S_1,S_2` 常是 Sylow 子群；`A_1,A_2` 在群论史里是 Cayley 的生成符号；`A_n` 在概率课是事件；`\mathcal{S}_n(K)` 是代数II 的对称矩阵空间。规则里只放能判死的形态（`S_n`、`S_[3-7]`），数字下标 1/2 一律留给人判。
- **规则要覆盖同一对象的全部宏包装与两种形态**：漏 `\mathcal{GL}`、`\text{GL}`、`\mathrm O`（空格不带花括号）是第一批迁移的典型漏网；写规则时枚举 `mathrm/operatorname/text/mathcal/mathbf/mathsf` × 花括号/空格。
- **符号要搬位置的改写不进规则**：正则只能就地替换，`A^T` → `{}^{t}A` 要把被转置对象整体搬到后面（`(AB)^T` 还会丢括号），`^T` 在分析课里又可能是积分上限（`\int_0^T`）。这类列成 manual 清单逐处改，脚本只负责把它们扫出来。
- **违规报表只给 family 名与计数，不给行号**（形如 `经典群 x1, 经典群x1`）——定位办法：从 `references/notation-rules.json` 找出该 family 的 `fix[].pattern`，把 pattern 原样交给 `grep -nP` 在报错文件上跑，命中的行就是违规处。刚手写进去的裸符号（`$GL_n/SL_n$` 这种，数学段内的裸 `GL`/`SL` 也算）是高发源；改完重跑 `--check` 确认 0，否则下一次会被当成存量汇总混过去。
- 判据：同一门课（正课＋习题课算一门）内同一对象只有一种写法；跨课可以不同，但差异要在 `共享/记号约定.md` 的登记表里写明。

## 6. 概念同步（收尾硬门槛）

笔记/讲义入库之后、或任何一次讲解答疑之后，**同一轮内**走完四步，缺一步不算收尾：

1. 列出这次涉及的概念，逐个落到 `概念/` 页（更新既有页优先，新建按建页阈值）；
2. 更新该课 `_索引.md` 的概念清单；
3. 更新**地图类文件**（学习路径 / 承担概念清单职责的 `00-总览` / 概念页索引）——名单与归属见 `references/concept-map-registry.json` 的登记表；新出现的地图类文件不登记，检查时会被报出；
4. `log.md` 一条 ＋ `git add`（只加目标文件）＋ commit ＋ push。

收尾自检三项，全绿才算完：

- 每个地图文件的 `updated` 不早于它所覆盖的概念目录里最新的 `updated`；
- 登记表与磁盘上的地图类文件一一对应（没有漏登记，也没有文件消失）；
- 没有孤儿概念页：既不在 `_索引`，也不被任何地图链接。

以上三项由 `scripts/check_concept_sync.py` 一次跑完（退出码非 0 即未收尾）；流程细节见 `references/concept-sync.md`。

**链接形态**：新页要同时进 `_索引` 与学习路径；表格/清单里引用可能跨课同名的概念必须写全路径（`[[代数III/概念/群]]`），裸链 `[[群]]` 会因为代数I/III 各有一页而被 `check_wikilinks` 判二义——本库有 11 组这样的存量重名页。

**为什么会漏**：只写「答疑即沉淀」时，讲义入库被当成机械转写，概念页与地图就永远滞后。这条规则的判据是**同一轮**，不是「下次整理」——用户看得出来哪个环节被跳过了。

## 7. 子代理分工（用户要求写进技能）

批量机械改动、跨课程调查、独立评审都派子代理省主上下文（用户明确要求：「这种重复工作你扔给子代理就好，直接跑浪费上下文」）。规则见 `references/subagent-delegation.md`。三条最要紧：①调查/评审类子代理**只读**、报告写到 cache、交付机器可读的 TSV/JSON 而不要散文；②**批量改 vault 可以交给子代理直接写**，前提是按文件清单切分且互不重叠、子代理只改自己清单里的文件、禁一切 git 操作，父代理统一复核后一次性 commit（实测 133 文件 / 5 并行安全落地）；③子代理自报不算证据，主代理自己跑脚本核数，且不同子代理的口径会飘（标签语言、单复数），父代理必须用同一判据再收口一遍。

## 参考文件索引

- `references/notes-structure-and-purity.md`
- `references/vault-hygiene-and-git.md`
- `references/exchange-diagrams.md`
- `references/abbreviation-expansion.md`
- `references/editing-toolchain-pitfalls.md`
- `references/lecture-ingest-and-pdf.md`
- `references/obsidian-ui-and-plugins.md`
- `references/teaching-and-precipitation.md`
- `references/concept-page-retrofit.md`
- `references/obsidian-graph-and-ui-config.md`
- `references/fourier-4-5-course-advance.md`
- `scripts/check_wikilinks.py`
- `references/natural-chinese-lint.md`
- `references/large-edit-gate.md`
- `scripts/lint_natural_chinese.py`
- `scripts/check_notation.py`
- `scripts/check_concept_sync.py`
- `references/notation-standard.md`
- `references/concept-map-registry.json`
- `references/concept-sync.md`
- `references/subagent-delegation.md`
- `references/public-companion-repo.md`

每个文件讲什么、踩过的坑 → `references/README-index.md`。


## 相关技能

- `math-physics-wiki` — wiki 维护主技能（PDF 提取、概念页、索引、答疑归档流程）
- `math-coach` — 讲解/陪练后沉淀 wiki 的教学技能
- `math-notes-transcription` — 手写/扫描笔记转写与结构化（**整门课入库的分段并行流程**见其 `references/whole-course-batch-workflow.md`）
- `user-math-library` — `/mnt/e/书籍` 资料库整理
- `nvim-config` — obsidian.nvim 阅读 wiki 的配置
