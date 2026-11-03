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
## 结构化整理(用户明确要求,2026-09)

> 详细内容：概念页拆分、内容纯度、作业材料处理、标点与图示规则的全文见 `references/wiki-content-and-formatting-rules.md`。

→ 全文（含实测细节与命令）见 `references/structured-organization.md`

## 当前机器(Linux/CachyOS)首选路径

- **批量视觉转录**: `scripts/vision_transcribe_batch.py`（纯标准库，无需 pip；key 自动从 `$HERMES_HOME/.env` 读）
  ```bash
  python3 ~/.hermes/skills/research/math-notes-transcription/scripts/vision_transcribe_batch.py \
      --dir <图片目录> --start 45 --end 52 --model deepseek-fl

→ 全文（含实测细节与命令）见 `references/machine-paths.md`

