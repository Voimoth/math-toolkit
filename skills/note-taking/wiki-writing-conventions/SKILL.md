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

## 3. vault 结构（2026-10-03）

```
/mnt/e/notes/
├── 数学/{分析,代数,概率}/          # 学科 → 课程 → 概念/ + 笔记/
├── 物理/理论力学/                  # 例外：扁平结构，概念页直接放课程目录
├── 共享/git-hooks/pre-commit       # 仓库护栏（唯一的非 md 文件）
├── 共享/记号约定.md                # 记号标准人读版，脚本 --emit-doc 生成，不手写
└── log.md                         # 变更日志（追加式）
```

- 笔记拆章用 `NN-章名.md`（**不带课程前缀**），入口页 `00-总览.md`；同门课若有正课＋习题课两套，各建子目录 `笔记/正课/`、`笔记/习题课/`。另有第三类子目录 `笔记/讲座/`（学术报告）：单次讲座直接放 `<YYYY-MM-DD>-<讲者>-<主题>.md`，不建 `00-总览`，同一系列多了再建；在该课正课 `00-总览` 的「讲座」组里加一行链接。
- **讲座笔记 = 原稿的思实整理，不是讲解稿（用户明确：「按原稿整理，而不是直接爆改我的笔记」）**：逐页编号（`## p.1`…）按原稿顺序搬，**照抄讲者的原语言**（他讲英/法就写英/法，不要翻译成中文），公式只做 LaTeX 化；**记号**照抄（他把 $\mathfrak{S}_n$ 手写成近似 $G_n$ 时，统一改写成标准记号并在文首说明），但**文字缩写要展开**——「照抄原语言」指的是语言与语气，不包括保留缩写（见下条与 `references/abbreviation-expansion.md`）。**不写**自己的「一句话总结」「最小例子」「为什么重要」「术语表」「你可能会问」这些段落。
- **速记缩写一律展开（用户明确：「所有笔记里的所有缩写都应该直接展开写」）**：正文、`\text{...}` 内、标题、callout 标签里的文字缩写都不保留；标准数学记号（GL_n、Hom、dim、ker、det、tr、Vect、Mat 等）与 LaTeX 命令 `\iff` 不是缩写，不动。**标签/展开词的语言跟该文件正文语言**（不是跟原标签），映射表、语言判定与正则统计坑、批量执行方式见 `references/abbreviation-expansion.md`。
- **讲解不进笔记，进对话与概念页**：整理完在回复里按用户当前知识水平口头讲一遍（从具体例子到术语，不堆名词）；可复用的数学内容沉淀到概念页（如 `Schur-Weyl对偶`、`Hopf代数`），而不是往讲座笔记里掺。
- **新建任何 `00-总览` 立刻做两件事**：链接写成全路径（`[[分析III/点集拓扑/笔记/习题课/00-总览|…]]`，否则 `check_wikilinks` 报「路径链接二义」——库里每个 `笔记/习题课/00-总览` 都是候选），并把它登记进 `references/concept-map-registry.json`（否则 `check_concept_sync` 报「未登记」；撤除该目录时同步从登记表删除）。
- **章级笔记缺口要写明**：若某一章的内容只落在概念页（例如从讲义抽出的 `紧性`、`连通性`）而 `笔记/` 里没有对应章文件，在 `00-总览` 与学习路径里明写「§X 只有概念页，章级笔记未写」——否则下个会话会把概念页当成整章已转写。
- vault 必须**自包含**：正文不写本地路径；`sources:` 写讲义名称而非文件名；agent 的 txt 誊本 / 脚本 / 模板一律不进 vault。

## 4. 其他必守项（速查）

- **callout 分层**：`> [!note] 定义/定理`、`> [!example] 例子`、`> [!tip] 想法/直觉`、`> [!warning] 陷阱`、`> [!info] 注记`；**证明不进 callout**（正文 `**Preuve :**`）。
- **callout 里放列表要留一个空 `>` 行**：`> [!note] 标题` 之后若紧跟 `> - …`，pandoc（预览用）会把列表并进同一个 Para、渲染成行内文字（PDF 里字面出现 `- `）；标记行与列表之间**必须**插一个只含 `>` 的空行（Obsidian 显示不变）。同理 **callout 内部不要再套 `>` 引用**——嵌套的 `>` 会原样印出来，引文直接写成普通行。原理与验收见 `nvim-config/references/pandoc-pdf-preview.md`。
- **法国记号**：全库记号标准见 `references/notation-standard.md`（含标准表、每课差异登记格式、迁移步骤）。最常用的几条：经典群正体 `\mathrm{GL}_n(K)`、对称群/交错群 `\mathfrak{S}_n`/`\mathfrak{A}_n`、`\ker`/`\operatorname{Im}`、张成 `\operatorname{Vect}`、转置 `{}^{t}P`（t 在左上角）；`Z(a)` 中心化子、`Z(G)` 中心；概念首次出现附法语名。**同一门课只允许一套写法**：老师本人的不同记号（习题课 `C_G(x)`、`D_n`、另一套换位子约定）保留，但必须登记在该课差异表里，不允许隐式混用。
- **源笔记的数学错误：先判数学，再直接改，不留标注（2026-10-21 用户明确「笔误直接改掉不用标注」）**：转写/整理时若某陈述与证明或后续命题矛盾，先用独立算一遍（阶/换位子/维数/计数）判对错，**直接把笔记改成正确版本**；页内**不写**「原稿作 X，应为 Y」这类 `> [!warning]`/`> [!info]` 整理注记（旧版约定已废），也不写「原稿此处失焦、按上下文补全」的说明。典型形态：生成元写反（平延只生成 SL）、pgcd/ppcm 混用、命题与紧随的证明矛盾。真正**无法判定**的疑点才用行内 `[?]`；若整页扫描不可读，向用户要重拍（他会拍），不要用推断填充正文。
- **用户会自己在 `[?]` 处批注与猜测，但不要照抄他的猜测**：他不懂具体数学，只是凭字形/记忆猜；正确做法是 **400dpi 重渲 + `vision_analyze(region=[x1,y1,x2,y2])` 局部裁切放大**核对原图（整页交给视觉模型会下采样，手写小字必丢），再根据上下文（同一记号、后续命题、定义链）定案，定案后删他的批注、不留整理痕迹。
- **建页阈值**：概念在 2+ 来源出现、或是一个来源的核心主题才建页；一笔带过的不建。
- **答疑即沉淀、无需询问**：数学/物理问答的可复用内容**当轮**写入对应课程概念页——**禁止**问「要不要整理进 wiki」；**边教边沉淀**，不攒到最后。用户自己的新想法/新证明同样沉淀。
  **概念页的补充与新建也一样，直接动手（2026-10-08 用户明确）**：需要补的判据/例子/推论直接补进既有那一页，不要先问「要不要补」。**一概念一文件是跨课程的**——同一概念只在最初那门课有一页，别门课（含新开课）的讲解要补就补这同一页，**不为新课复制同名页**（复制会让 `[[概念名]]` 变二义）；有疑问的只是「这概念值不值得建页」，那是建页阈值问题，不是询问问题。
- **git**：改完 `git add`（只加目标文件）＋ commit ＋ push；`log.md` 追加一条变更记录。（概念同步见 §6，子代理见 §7）
- **Obsidian 会自己重排 frontmatter，保留就行**：用户开着 Obsidian 时插件会把页面改写成 properties 格式（`id`、`aliases: []`、`tags` 变列表、日期加引号）。这是他的改动，**不要还原**成旧的紧凑写法，也不要当成 diff 噪音 revert；提交时照原样带上。
- **对外发布配套仓库**：工具库独立成库，不塞进 vault；发布前用 `git ls-files` 扫身份信息与绝对路径（同步脚本与排除表本身就是高发泄漏点，要本地化）；课程笔记用 CC BY-NC-SA + `NOTICE` 限定范围，代码用 MIT；README 只写「是什么/怎么用/许可」，**不写脱敏与上传流程**。**技能文本改完当轮跑 `bash sync/sync.sh`**——仓库不会自动跟，用户按仓库提交日期判断有没有更新；同步前核对 `SKILLS` 列表与现实一致（改名后的旧目录要 `git rm`）。细则见 `references/public-companion-repo.md`。
- **交换图**：一律 `\begin{array}{c...c}` + `\xrightarrow`/`\xleftarrow`/`\big\downarrow`/`\big\uparrow`/`\Big\Vert`/`=` 的方形画法，**不要用 amscd 的 `\begin{CD}`**（pandoc 的 LaTeX 模板不带 amscd，直接报 `Environment CD undefined`；Obsidian 的 MathJax full bundle 其实带 amsCd，所以 CD 是「能在 Obsidian 看、但编译不出 PDF」的单端写法，array 才是双端交集）；2026-10-21 已把全库 18 处 CD 全部换成 array。竖直箭头标签按 amscd 位置习惯放（`@V{lab}VV` 标注在左 → `{\scriptstyle lab}\big\downarrow`，`@VV{lab}V` 标注在右 → `\big\downarrow{\scriptstyle lab}`）。**改完要跑渲染色检并逐个核对箭头方向**。
- **史实/出处类内容要有来源，未查实的标 `[?]`**：往页里写「谁先提出某概念、术语的来历、某结论的标准出处」时，
  必须落得出**一手或权威来源**（原始论文/书信的书名+页码，或 MacTutor／Wikipedia 的条目名），不要凭记忆或搜索摘要下断言；
  查不实的部分一律用行内 `[?]` 并留一句查证线索（他讨厌被丢「请你确认」的清单，但行内 `[?]` 是他自己在笔记里的约定）。
  求证路线（判定网通/直连百科/关键词窗口）见 `web-fetching` 技能。
- **链接健康检查（写完就跑，不只清理时）**：`python3 <技能目录>/scripts/check_wikilinks.py /mnt/e/notes` —— 一次扫四类
  （裸链二义 / 路径链接二义 / 断链 / 数学记号误判），全 0 才是干净。**新写、新改的链接同样要过**：只顾「清理旧链接」
  时很容易在新增处再引入一条歧义（裸链指向两个同名页）。匹配规则与 nvim 侧的 obsidian.nvim 对齐，细节见 `references/vault-hygiene-and-git.md`。
- **中文自然度 / 改动过程泄漏（写完就跑）**：`python3 <技能目录>/scripts/lint_natural_chinese.py <改动文件>`
  —— 十类规则（英译腔/空名词/模板句/AI 总结腔/意义拔高/写作预告/修改过程泄漏/模糊归因/宣传腔/搭配不稳），
  只报到不改写，逐步跳过代码块与数学区；命中不等于写错（规则表和用法见 `references/natural-chinese-lint.md`）。
- **大编辑门槛（重写多小节 / 新建 >4 KB / 动编号 时必须走）**：候选先在 vault 外写好 → 跑完确定性检查 →
  由**无上下文子代理**独立评审 → 才落盘；落盘后重跑链接与自然度检查。表格单元格里的 wikilink alias 必须写 `[[目标\|别名]]`；
  TeX 当数据传（直接写文件，不过会解释转义的中间字符串）。完整流程与「三轮不过」的例外见 `references/large-edit-gate.md`。

## 5. 记号统一（机器可查，不靠记性）

- **单一数据源**：`references/notation-rules.json`（机器规则）。人读的两份都由它生成，**不手写**：`references/notation-standard.md` 与 vault 的 `共享/记号约定.md`；改规则只改 JSON，再跑 `--emit-doc`。
- **写完/改完含数学的文件就跑**：`python3 <技能目录>/scripts/check_notation.py --check`（默认扫全库，可给单课路径）；`--apply` 之前先出 dry-run 报表，`--apply` 会自动备份被改文件到 `~/.hermes/cache/notation-backup/`。
- **裸符号必须按课程限定作用域，并记住同形不同义**：`S_n` 在分析与概率课是部分和；`S_i` 在 Coxeter 群页是单反射；`S_1,S_2` 常是 Sylow 子群；`A_1,A_2` 在群论史里是 Cayley 的生成符号；`A_n` 在概率课是事件；`\mathcal{S}_n(K)` 是代数II 的对称矩阵空间。规则里只放能判死的形态（`S_n`、`S_[3-7]`），数字下标 1/2 一律留给人判。
- **规则要覆盖同一对象的全部宏包装与两种形态**：漏 `\mathcal{GL}`、`\text{GL}`、`\mathrm O`（空格不带花括号）是第一批迁移的典型漏网；写规则时枚举 `mathrm/operatorname/text/mathcal/mathbf/mathsf` × 花括号/空格。
- **`--apply` 前先聚合命中样例**：把每种规则的全部命中按上下标内容分组打印（例如列出 `e^` 后面跟的所有指数形态），再决定是否放开。否则 lookbehind 的一处误伤会在全库扩散（`_e^{e'}` 这种下标里的 e 不是自然常数）。
- **统计只看真改动**：替换后与原串相同的命中不能计数，否则「修复 400 处」里一半是 `\mathrm{GL}` 换 `\mathrm{GL}`。
- **lookbehind 用 `{` 排除会漏掉 `\frac{e^n}`**：正确做法是先允许、再补一条清理规则把双包 `\mathrm{\mathrm{e}}` 收回；靠排除字符集做边界一定会漏掉一类上下文。
- **迁移按课程分批**：概念 → 笔记 → 索引/地图 → 检查 → 单课 commit，可单课回滚。一次改几百处再提交的 diff 无法复核。
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

| 主题 | 文件 |
|---|---|
| 概念页/笔记的拆分规则、vault 自包含、建页阈值与更新政策、学习背景 | `references/notes-structure-and-purity.md` |
| Git 提交卫生、0 字节文件判定、空 wikilink 根因、删文件前核查、断链清理与验证 | `references/vault-hygiene-and-git.md` |
| **交换图规范（一律 array 写法，禁用 CD）＋ 渲染色检 ＋ 箭头方向核对** | `references/exchange-diagrams.md` |
| **缩写展开：判据、语言判定、映射表、正则统计坑、批量执行** | `references/abbreviation-expansion.md` |
| 编辑工具链的坑：双重转义扫描、patch/here-string 转义、无文件工具时写中文 | `references/editing-toolchain-pitfalls.md` |
| 讲义更新（＝课程推进）与讲义 PDF 提取 | `references/lecture-ingest-and-pdf.md` |
| Obsidian 图谱配色（graph.json）、社区插件安装 | `references/obsidian-ui-and-plugins.md` |
| 更新授权与「新想法」沉淀的判据 | `references/teaching-and-precipitation.md` |
| 既有概念页的规范整理（retrofit 工作流＋质检脚本） | `references/concept-page-retrofit.md` |
| 图谱/UI 配置完整手册（20 字段清单、颜色换算、五步验证） | `references/obsidian-graph-and-ui-config.md` |
| 分析 III Fourier §4–§5 的内容银行与建页映射 | `references/fourier-4-5-course-advance.md` |
| 全库 wikilink 健康检查（四类问题一次扫，可当护栏跑） | `scripts/check_wikilinks.py` |
| 中文自然度 lint 的十类规则与用法 | `references/natural-chinese-lint.md` |
| 大编辑门槛、独立评审、落盘后校验、证明状态标签 | `references/large-edit-gate.md` |
| 中文自然度检查器（十类规则，只读） | `scripts/lint_natural_chinese.py` |
| 记号检查/修复与文档生成 | `scripts/check_notation.py` |
| 概念地图同步检查（陈旧/未登记/孤儿） | `scripts/check_concept_sync.py` |
| **记号标准表、每课差异登记、迁移步骤与统计坑** | `references/notation-standard.md` |
| **地图类文件登记表（唯一名单）** | `references/concept-map-registry.json` |
| 概念同步流程与判据 | `references/concept-sync.md` |
| **子代理分工：只读边界、交付格式、核数方式** | `references/subagent-delegation.md` |
| **对外发布配套仓库：独立成库、发布前扫描、许可与 README 写法** | `references/public-companion-repo.md` |

## 相关技能

- `math-physics-wiki` — wiki 维护主技能（PDF 提取、概念页、索引、答疑归档流程）
- `math-coach` — 讲解/陪练后沉淀 wiki 的教学技能
- `math-notes-transcription` — 手写/扫描笔记转写与结构化（**整门课入库的分段并行流程**见其 `references/whole-course-batch-workflow.md`）
- `user-math-library` — `/mnt/e/书籍` 资料库整理
- `nvim-config` — obsidian.nvim 阅读 wiki 的配置
