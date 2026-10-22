---
name: math-notes-transcription
description: "数学笔记转写与结构化整理:手写/扫描 PDF 转文字(视觉模型/Tesseract)、LaTeX 分隔符修复、拆分为概念页+wikilink 互链。触发:用户给出手写笔记/扫描版 PDF 要求整理成文字、笔记渲染不了($ 公式)、要求按概念拆分整理成 wiki/知识库结构。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ocr, transcription, notes, obsidian, latex, zh]
    category: research
---

# 数学笔记转写与结构化整理

## 当前机器(Linux/CachyOS)首选路径

- **批量视觉转录**: `scripts/vision_transcribe_batch.py`（纯标准库，无需 pip；key 自动从 `$HERMES_HOME/.env` 读）
  ```bash
  python3 ~/.hermes/skills/research/math-notes-transcription/scripts/vision_transcribe_batch.py \
      --dir <图片目录> --start 45 --end 52 --model deepseek-flash \
      --prompt '逐字转写这一页的全部文字，公式用 LaTeX，不要翻译/总结/补全看不清的内容'
  ```
  输出与图片同名的 `.txt`；已存在则跳过（`--redo` 强制重做）；失败会重试 3 次并汇总。
  区间过滤按文件名结尾的数字（无编号的图当作在区间内），与旧 PowerShell 版语义一致。
- **法文/手写扫描档的 prompt 用英文并显式要求「无前言」**：`--prompt 'Transcribe this handwritten French mathematics page verbatim into Markdown. Use LaTeX for inline $...$ and display $$...$$. Do not translate, do not summarize, do not complete unreadable parts (write [?] instead). Output only the transcription, with no preamble.'`——否则模型会在开头加一行 `Voici la transcription du manuscrit…` 类前言，合并前必须剔除。
  - **正文是中文手写、术语夹法语时**，把语言那句换成 `Keep Chinese text in Chinese and French terms in French exactly as written`，其余照旧（既防模型把中文笔记译成英文，又保法语术语原样）。
  - **页首的模型元评论行照用不误**：模型偶尔输出 `The image has been rotated 90 degrees counterclockwise. Here is the recognized text:` / `OCR result` 之类整页说明。**看到它不要重转或旋转该页**——先核对正文与邻页首尾是否衔接；衔接得上就只删掉这一行、内容照用。整批 50+ 页放 `terminal(background=True, notify=True)` 跑、日志重定向到文件（`> translog.txt 2>&1`）；脚本按已存在的 `.txt` 断点续转，中途重跑/超时都安全。**同时跑两份（如两门课各一个进程）时，别把两个任务塞进同一个 `background=true` 调用、也不要用 `( cmd & )` 包**——外层 `wait` 无可等会立即返回、session 被标记 exited，完成通知永远不来（进程成孤儿，只能自己轮询）；每个任务单独一次 `background=true, notify=true` 调用，或用前台 `while pgrep -f '<脚本名> --dir <目录>'; do sleep 15; done` 等待。详见 `references/handwritten-scan-workflow.md` §2。
- **少量/单张**: 直接在当前会话读图自己转写（默认走主模型原生视觉）。
- **扫描件纯 OCR**: `pdftoppm -r 300 -png in.pdf /tmp/pg` + `tesseract /tmp/pg-45.png stdout -l chi_sim+eng`
  （tesseract 5.5.3 已装；语言包 chi_sim/eng/fra/osd 在 `/mnt/h/tesseract/tessdata`，**必须先 `export TESSDATA_PREFIX=/mnt/h/tesseract/tessdata`**，否则报找不到语言包；公式不可靠，手写体走视觉模型）
- **印刷体也要先测再决定要不要上视觉模型**：实测英文印刷体（含 1916 年的老数学书）tesseract 近乎逐字正确，中文印刷体能认出章节行与标题但常错在数字与标点（`15.4` 读成 `15:4`、页码错位）。判据是**用途**：只要求「搜索能召回」→ tesseract 就够（150 dpi 约 1 秒/页）；要求当正文读、要页码精确 → 才上视觉模型。**批量上千页时全量走视觉既不划算也不更准**，分层降级才是对的：文本层 → tesseract → 只剩读不出的少数才贴图问模型。
- 旧 Windows 版的 `.ps1` 脚本与只讲 Windows 的参考文档已于 2026-10-06 删除；Linux 下按上面列出的 `.py` 与系统工具走。

服务对象:中科大中法班数学系大二学生。处理场景:手写法语/中文数学讲义 → 可读文字 → 结构化的 Obsidian 知识库。

## 触发条件

- 用户提供手写笔记/扫描版 PDF,要求"整理成文字"
- 笔记在 Obsidian 渲染不了(`$...$` 公式问题、代码块包裹)
- 用户要求"把概念拆分成小文件,用关系图互链"(不要一个大讲义文件)
- 用户要求按学科/课程归档笔记

## 核心工作流

> 详细内容：第零步（确认输入与通道/密钥自检）、第三步（逐页转写）、第四步（批量调用的坑）见 `references/handwritten-scan-workflow.md` 与 `references/whole-course-batch-workflow.md`。

### 第一步:判断 PDF 类型(有文本层 or 纯扫描)

```bash
# 用 poppler 提取,看是否真有文字(扫描版几乎提不出正文)
pdftotext -layout 输入.pdf 输出.txt
# 检查:看输出是否有连贯正文;几乎为空/只有页码 => 无文字层
```

- **有文本层**但质量差(每行一个词、错字多)→ 手写体的文本层不可靠,**必须用视觉模型重转**
- **纯扫描版**(无文本层,只有页码标记)→ 印刷体用 Tesseract,手写体用视觉模型
- **电子排版讲义**(文本层完整、叙述连贯,如 LaTeX 生成的中文讲义 PDF)→ **直接以提取文本为底稿人工重建 LaTeX**,无需视觉模型/Tesseract。pdfjs 会把公式打成碎片行(上标/分数/矩阵散成多行,如 `z\n n\n= 1`、表格列错位),需逐段按数学含义重排为 `$...$`/`$$...$$`;保留讲义编号(定义 1.1/例 1.5)与讲义记号约定(如"本文采用 $|D_n|=2n$")。2026-09-08 实战:17 页中文习题课讲义,提取 794 行,人工重建后 373 行结构化笔记,零视觉调用。

### 第二步:转图片(pdftoppm,texlive 自带)

```bash
pdftoppm -png -r 300 输入.pdf /tmp/page   # 300dpi 手写体清晰度够
# 生成 page-01.png, page-02.png...
```

- **来源字号越小,分辨率和校对密度都要相应提高**:手机翻拍、缩印讲义、笔记字小的扫描档,OCR 出错率显著高于正常版式,布局也可能被斜拍/阴影干扰。做法:转图 ppi 调高(整页读不清就先整页预览定位,再对可疑区域裁剪放大后单独问);**校对的判据从「整页通读一遍」改成「每一处符号级可疑都回原图」**——这类档里 $\neq$/\geqslant/$=$,下标 $m$/$n$、花体字母这类差异几乎每页都有,凭上下文补全会静默改掉数学含义。用户交这类档时会明确提醒「字比较小, 更加需要仔细校对」,把这句当成提高一档校对强度的信号。
- **判读小字/公式必须局部裁切，别把整页丢给视觉模型**：整页图会被下采样到约 640 px 宽，手写体的小字、上标、`∃`/`𝔽_p`、`Irr rep` 这类短词全部糊掉，读出来就是错的（实测把存在量词 `∃` 读成 `\mathbb F_p`，要靠 400 dpi 重渲才看清）。做法：`pdftoppm -r 400 -png` 重渲 → `vision_analyze(image_url=<页图>, region=[x1,y1,x2,y2])` 按**原图像素坐标**裁一条横带问模型（或先 PIL 裁图放大 2× 再传）；一页两三处存疑就各裁一次。注意返回的坐标提示是「相对裁切原点」的，不要拿它当整页坐标继续裁。
- **用户在手写稿 `[?]` 处自己写的批注/猜测不能照抄**：他不懂具体数学，只是凭字形猜；正确做法是带着他的批注回原图（上一条的裁切法）+ 上下文（同一记号、后续命题、定义链）定案，定案后删掉他的批注与所有整理痕迹，不在页内写「原稿作 X」。
- **定稿后再做一遍「分带重抄」校对，不要只回看 `[?]` 处**：每页切 2–4 条横带各问一次、照抄重写，再与已有文本逐行比对。只回看 `[?]` 会漏掉整句级别的错——实测抓到过：Bruhat 分解写成 $B\mathfrak S_nU$ 而原稿是 $BG_nB$（三角分解 vs 双陭集之并，数学含义不同）、整行 $\Lambda(x)\otimes\Lambda(y)=R(x,y)^{G_\infty\cdot G_\infty}$ 漏抄、关系编号 $(\star)$ 抄成 $(*)$、`p\leftarrow q` 抄成 `p=q`、存在量词 $\exists$ 抄成 $\mathbb F_p$、花体 $\mathfrak{S}_n$ 字形近似 $G$ 而被读成 $G_n$。**关于花体 S**：用户 2026-10-21 澄清原稿就是 $\mathfrak{S}_n$，不存在 $G_n$ 这套记号——凡见 $G_n$、$G_\infty$、$G_{|G|}$、$R[G_n]$ 一律改回 $\mathfrak{S}_n$、$\mathfrak{S}_\infty$、$\mathfrak{S}_{|G|}$、$R[\mathfrak{S}_n]$，也别在整理稿开头写「原稿记作 $G_n$」这类说明；全库搜索时注意区分合法的 $G_x$（稳定子）、$G_M$（半直积）、$G_i$（正合列）。

### 第五步:合并 + 编码修复

- **UTF-8 双重编码修复**(旧 PowerShell 双重编码的遗留):`Ã©`→`é`、`Ã¨`→`è`、`Ã `→`à`、`Ã¢`→`â`、`Ã§`→`ç`、`Ã»`→`û` 等,用 Python/Node 脚本批量替换
- 合并各页为单文件,加 frontmatter(title/created/type/tags/sources/confidence)

### 第六步:LaTeX 分隔符修复(Obsidian 渲染)

Obsidian 只认 `$...$`(同行)和 `$$...$$`(块级),**不认** `\(...\)`/`\[...\]`:
- `\(` → `$`, `\)` → `$`, `\[` → `$$`, `\]` → `$$`
- **跨行 `$` 是最大坑**:某行单独一个 `$`(公式在中间行)→ 必须转 `$$`。Obsidian 行内 `$` 要求起止同行
- **少用细空格 `\,`**：源码里 `$\exists\,p$` 看着像多打了一个逗号/空格，用户会手动删掉（改成了 `$\exists p$`）。非排版必需就不加，`\quad`、`\;` 同理能用自然间距代替就用
- 检查残留的 ` ```markdown ` 代码块包裹(视觉模型有时会把整段内容包进代码块,导致不渲染)——必须去除
- 验证公式配对:统计每行 `$` 数为偶数、无单独 `$` 行、`$$` 成对(Node 脚本 check)
- **配对检查只算第一层**：`$` 配齐仍可能编译不过——OCR 会把杂物塞进 `\left\{...\right\}` 或 `pmatrix`（`{ \\& } ;\ddots` 这种，xelatex 报 `Missing } inserted`），或用了引擎不认的 `CD`/`tikzcd` 环境。改完必跑 `scripts/check_formulas.js`（KaTeX + MathJax + 可移植性三路）再用 `pandoc --pdf-engine=xelatex` 实测编译一遍，配方与坑见 `references/formula-render-check.md`。用户说「编译不了 / 左右大括号没对齐」时直接照那份走。
- **patch 工具会损坏含 `\left`/`\right` 的行(2026-09 实测,踩坑后修复过)**:patch 工具的替换逻辑把 LaTeX 序列 `\right)` 中的 `\r` 当成回车转义,**new_string 写入时变成「换行 + `ight)`」**,公式被拦腰截断(症状:diff 里出现 `|\r+ight)`)。实测补充:**old_string 含 `\right` 可以正常匹配**(patch 只对 new_string 做 `\r` 转义)。因此修复损坏处或重写含 `\left`/`\right` 的整行时,new_string 里要么改写为不含 `\left`/`\right` 的等价式(普通括号或 `\Bigl(...\Bigr)`),要么改用 PowerShell `[IO.File]::ReadAllText` + `.Replace()`(无转义解析)整文件读改写,写后读回验证 `\right` 完整。write_file 无此问题。

> 详细内容：讲义出新版本时的推进摄入流程见 `references/lecture-update-workflow.md`。

## 结构化整理(用户明确要求,2026-09)

> 详细内容：概念页拆分、内容纯度、作业材料处理、标点与图示规则的全文见 `references/wiki-content-and-formatting-rules.md`。

> 详细内容：常见 OCR 错误模式与修复法见 `references/ocr-error-patterns.md`。

> 详细内容：有限群论断的枚举核验（含脚本用法）见 `references/group-enumeration-verification.md`。

### 并入某课已有的笔记系列(新讲义 → 已有 `NN-篇名` 序列)

来源是一份**新课程材料**（新的习题课讲义、单章讲义），而目标课程 vault 里**已经有成套笔记**时，不要按本技能的通用模板从头写，而是**续写这个系列**：

- **先读该系列最近 2–3 篇再动笔**，复制它们的 frontmatter 字段集、H1 写法（`# N 主题（日期）`）、callout 标签格式与条目编号方式。**同课程既有文件是格式的唯一权威**：与本技能或偏好文件里的通用条目冲突时，以既有文件为准——例：通用条目说正文不带「（讲义 X.Y）」出处，而代数 III 正课/习题课笔记的既有形态恰恰是 `> [!note] 定义 5.1（轨道与稳定子群，讲义 1.1）`。
- **续号并同步总览**：新篇接既有最大编号（`06-…` → `07-…`），该套的 `00-总览.md` 加一行。
- **篇内条目重排为** `N.1`、`N.2`…，原讲义编号放括号里（既有笔记一律这么写）。
- **来源是助教印发的编号讲义时，保留题面与讲义编号**（含「某年期中考试题」「某年丘赛…」这类出处），不要套用针对**手写习题课流水**的「删题号、只留知识条目」规则；判据是**来源形态**，见 `references/wiki-content-and-formatting-rules.md` 的「并入既有课程笔记系列」。
- **归属靠内部编号对齐，不靠文件名**：一份无名 PDF 属于哪门课、哪套讲义，看它内部的编号体系能否与既有笔记引用的「讲义 X.Y」对上（如某 PDF 的 `§1.3` 与既有笔记的「讲义 1.1.x」同源，即是同一套习题课讲义的一节）。

### 讲座/学术报告的整理（海报截图 + 现场手写笔记）

输入通常是三件套：报告海报截图（题目、讲者、时间、摘要）、现场手写笔记的扫描 PDF、（可能还有拍照）。流程：

1. **先读海报拿准框架**：题目、讲者、单位、时间地点、摘要四段。海报给的是讲者打算讲的结构，笔记给的是他实际讲了什么；两者对不上时以笔记为准，并在笔记里一句话点明差异。
2. **读笔记**：页数少（≤ 10 页）就在当前会话逐页读图，不要为几页起批量脚本；页数多才转 300 dpi 后走 `scripts/vision_transcribe_batch.py` 或分页子代理。**逐页读也要按上文「判读小字」那条分带裁切**：整页图被下采样到 ~640 px 宽，速记的小字、上下标、`∃`、`Irr rep` 这类短词全是错的。
3. **文件里只放原稿层；解释层不进文件（用户明确：「按原稿整理，而不是直接爆改我的笔记」）**：
   - 忠实转写：速记、箭头、只有名词没有谓语的条目原样保留，**照抄讲者的原语言**（英/法就写英/法），公式只做 LaTeX 化，读不清写 `[?]`；**但文字缩写一律展开**（rep→representation、f.d.→finite dimensional、Thm.→Theorem、s.t.→such that、h.w.→highest weight 等，含 callout 标签与 `\text{}` 内；标准记号 GL_n/ker/dim 与 `\iff` 不动）。「照抄原语言」指语言与语气，**不包括保留缩写**；映射表、标签语言判定（跟文件正文语言）、批量展开流程见 `wiki-writing-conventions` 的 `references/abbreviation-expansion.md`；
   - 不讲自己的动机链、最小例子、术语表，也不加「一句话总结」「为什么重要」「你可能会问」这类小节；
   - **禁止把速记笔记改写成一气呵成的叙述**——讲座笔记本身就是速记，把它“翻译”成顺句等于替讲者编造他没说的话；
   - 要讲就**在回复里按用户当前知识水平口头讲一遍**，并把可复用的数学沉淀成概念页（如由讲座带出的 `Schur-Weyl对偶`、`Hopf代数`）。曾把两层写进同一文件、用「原稿层/解释层」两个标题隔开，仍被要求删掉解释层（用户第二次纠正），所以不要两层的折中方案。
   - **分节用原稿自带的标题**（Symmetric group、Bruhat decomposition、Schur-Weyl duality、Coproduct、Quantization…），**不要用 `## p.1`…`## p.6` 页号标题**：页号对读者没有信息量，用户会要求删掉；原稿没有标题就在该页内容里找一个自然的主题句。
4. **落库**：`<课>/笔记/讲座/<YYYY-MM-DD>-<讲者>-<主题>.md`；单次讲座不需要 `00-总览`（同一系列多了再建），在该课正课 `00-总览` 里加一行「讲座」链接。frontmatter 用 `confidence: medium`（讲座内容不保证准确）。原件（PDF 与海报截图）归档到 `书籍/<学科>/<课>/讲座/`。
5. **只抽 1–2 个真新概念建页**：选讲座主题的核心定理/结构建概念页（带最小例子），其余术语在讲座笔记的术语表里一句话解释——不要为一次讲座批量建空壳页。
6. **补全与笔误直接写正稿，不标注**：讲座速记里系数、符号、下标几乎必漏，按标准约定补全后**直接写成正文**；原稿笔误（如把 $m_{(1)}(x)$ 写成 $m_{(1)}(1)$）也直接改。用户明确要求「笔误直接改掉不用标注」，页内不写「原稿作 X」「按标准约定应是 Y」这类注记；只有真正无法判定的字形才留 `[?]`，而整页不可读时应当请他重拍（他一次就拍来），不要用推断填充。

### Vault 结构约定(2026-09 重构后)

```
/mnt/e/notes/                      # vault 根没有 README.md(已删);agent 一切工具/产物都不在此
├── 数学\{分析,代数,概率}\          # 按学科
│   ├── _索引.md                    # 学科导航
│   ├── 分析I\分析II\分析III\       # 按课程细分
│   │   ├── 概念\                   # 整理的知识库页(拆分的概念小文件)
│   │   └── 笔记\                   # 一套笔记:00-总览.md + NN-章名.md;两套时:正课\ 与 习题课\ 各含自己的 00-总览.md
├── 物理\{理论力学}\
├── 共享\git-hooks\pre-commit      # 仓库护栏(拦 >5MB 文件),唯一的非 md 保留项
└── log.md                        # 变更日志(追加式)
```

- **笔记 vs 概念分目录**:原始转写(OCR/视觉模型输出)放 `笔记\`,整理后的概念页放 `概念\`
- **但 OCR 誊本(txt)本身不进 vault(2026-10-03 用户明确)**:提取/转写产生的 `*.txt` 放在 **agent 自己的工作目录**(`~/.hermes/cache/`),不要留在 vault;`sources:` 字段也写**讲义名称**(如 `殷浩《分析 2》上册`),不写文件名或路径。vault 必须能脱离用户本地文件独立阅读。
- 新增学科:建目录 + `_索引.md`(vault 根无 README,不要再写 README 登记)
- **正课/习题课的总览各放在各自文件夹里,「笔记」根下不放总览**(用户 2026-10 明确:「我更希望正课和习题课各自有一个总览, 放在各自的文件夹里面」)。判定:只有一套笔记的课程 → `笔记\00-总览.md`;同时有正课与习题课的课程 → **必须**是 `笔记\正课\00-总览.md` 与 `笔记\习题课\00-总览.md` 两份,各自只列本套篇目(正课总览按主题分节,习题课总览列各次)。**这不是「新建课程才遵守」的约定:发现既有课程不满足也要改**——把放在外层的合并总览拆成两份放进对应子目录、删掉外层文件、再把学科 `_索引.md` 的引用改成全路径(如 `[[代数III/笔记/正课/00-总览|代数 III 正课]]`);改完重跑断链扫描(`log.md` 里的历史记录链接断属正常)。
- 每次变更 git add+commit+push(GitHub math_wiki 私有仓库,GCM 免密)

> 详细内容：用户在笔记整理上的全部偏好见 `references/user-preferences-note-taking.md`。

## 相关技能

- `nvim-config` — Neovim/obsidian.nvim 配置与排障
- `math-physics-wiki` — 数学物理 wiki 维护(vault 结构、PDF 提取、gen_graph.js 关系图脚本)
- `pdf-problem-search` — 本地 PDF 题库检索
- `user-math-library` — /mnt/e/书籍 资料库结构

## 参考文件


- **`references/ocr-error-patterns.md`** — 数学 OCR 转写的常见错误模式与修复（2026-09 实战汇编）
- **`references/formula-render-check.md`** — 公式渲染级校验：KaTeX/MathJax/pandoc 三路验证、`CD` 环境替换、`smallmatrix`、callout 出 PDF（配 `scripts/check_formulas.js`）
- **`references/group-enumeration-verification.md`** — 有限群论断的枚举核验（写群论内容前先跑）
- **`references/wiki-content-and-formatting-rules.md`** — 笔记/概念页的内容纯度与格式规则（用户逐次明确）
- **`references/lecture-update-workflow.md`** — 讲义推进摄入（同一门课的讲义出新版本）
- **`references/user-preferences-note-taking.md`** — 用户在笔记整理上的偏好（务必遵守）

- **`references/whole-course-batch-workflow.md`** — **整门课（100+ 页）入库**的完整打法：300 dpi→批量转写→清洗→切块→写一份统一规范文件→≤10 子代理并行→父代理收尾（断链/坏模式/总览/索引/log/提交/清理）。含关键教训：`delegation.model` 切非思考路由防死循环、子代理自行改公式必须回原图复核、同义与跨课程同名概念页的处理；以及**习题课「提炼知识而非转写」的规范**（删题号、按主题分篇、判据「换个题目还成立吗」）。
- **`references/handwritten-scan-workflow.md`** — 手写扫描档的全流程与**校对纪律**；末节「复核存疑点的判读手法」给的是**客观判据**（原生分辨率提取 `pdfimages`、点采样放大 `magick -filter point`、列方向墨迹簇计数、等尺寸框比墨迹像素数、同页同字符字形对照）——用于判 `≥` vs `>`、𝕂 vs ℝ、以及「某处到底是 x 还是 2x」这类只差几像素的存疑点。
- **`references/git-repo-bloat-and-lost-objects.md`** — vault/仓库体积异常膨胀时的诊断与回收:
  `.git` 远大于工作区（本例 159 MB vs 1 MB）时的三步诊断（`count-objects` → `verify-pack` → `fsck --unreachable`）、
  可达性交叉验证、孤儿对象的**二进制安全导出**（`Start-Process -RedirectStandardOutput`，绕开 `&` 网关拦截与管道损坏）、
  按魔数识别类型、清理前的远程同步检查、`reflog expire + gc --prune=now` 回收。**含"别自行删除可能是用户照片的对象"的安全纪律。**
