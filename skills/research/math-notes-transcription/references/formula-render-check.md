# 公式渲染级校验：从「$ 配对」到「引擎真的能解析」

`scripts/check_tex_format.js` 只查 `$` 配对（每行偶数、无单独 `$` 行）。它查不出下面这类真正让 Obsidian 标红、让 pandoc 编译失败的错：

- `\left\{ ... \right\}` 内部花括号被 OCR 塞进杂物（例：`\begin{pmatrix}t_1&&{ \\& } ;\ddots&\\&&t_n\end{pmatrix}`）
- `pmatrix` 行内的 `&` 数目不齐
- 用了引擎不认的环境（`CD`、`tikzcd`）或宏包（`\require{amscd}`）

判据只有一个：**让引擎自己解析一遍**。三路都要跑，缺一层就会漏。

## 一键检查公式

```bash
export PATH=$HOME/.hermes/tools/node-26.7.0-linux-x64/bin:$PATH
export NODE_PATH=$HOME/.local/share/formula-check/node_modules
node ~/.hermes/skills/research/math-notes-transcription/scripts/check_formulas.js 文件.md [更多.md]
# 退出码 0 = 全过；1 = 有失败，逐条打印「行号 / 引擎 / 报错 / 原式」
```

依赖只需装一次（55 MB，常驻）：

```bash
mkdir -p ~/.local/share/formula-check && cd ~/.local/share/formula-check && npm i katex mathjax-full
```

它做三件事：
1. **KaTeX** 逐条 `renderToString`（最严格，语法级错误几乎全抓）；
2. **MathJax**（Obsidian 的实际引擎）逐条 `convert`，查 `data-mjx-error` / `mjx-merror`；
3. **可移植性扫描**：`\begin{CD}`、`\begin{tikzcd}`、`\require{}` —— 它们能过 MathJax（AllPackages 含 amscd），但 pandoc 默认 LaTeX 模板不带 amscd，Obsidian 默认包集也不带，实际会坏。

## 整体编译验证（pandoc → xelatex）

```bash
pandoc 笔记.md -o 笔记.pdf --pdf-engine=xelatex \
  -V CJKmainfont='Noto Sans CJK SC' --standalone
pdfinfo 笔记.pdf | grep Pages          # 有页数就说明 LaTeX 全过了
pdftoppm -r 110 -png 笔记.pdf /tmp/chk  # 再抽 2–3 页用眼睛看矩阵/分段/交换图
```

编译报错给的行号是**生成的 .tex 行号**（中间还插了 template 与长段落），不是 md 行号 —— 按报错里回显的公式片段去 md 里定位，别按 l.141 去找。

## 已踩过的坑

- **MathJax-full 的 `packages` 参数别手写**：`new TeX({packages:['base','ams']})` 会让 `pmatrix`/`cases`/`\operatorname`/`\xrightarrow` 全报 `Unknown environment` / `Undefined control sequence`（假阳性）。用 `AllPackages` 或干脆不传。
- **`CD` 环境必须替换**：改写成 `\begin{array}{ccc}` + `\xrightarrow{\ \Delta\ }` + `\big\downarrow` + `{\scriptstyle\Delta}` 标注，KaTeX/MathJax/pandoc 三边都过。**2026-10-21 已把 vault 里 12 个文件 18 处 `CD` 全换成 array（含 callout 内的图），新写交换图直接用 array，不要再引入 CD**。amscd 位置约定：`@V{lab}VV` 标注在左 → `{\scriptstyle lab}\big\downarrow`；`@VV{lab}V` 标注在右 → `\big\downarrow{\scriptstyle lab}`；`@AA{lab}A` 向上右标 → `\big\uparrow{\scriptstyle lab}`；`@|` → `\Big\Vert`；`@=` → `=`；`@<{lab}<<` → `\xleftarrow{lab}`。批量改装（18 处以上）派子代理并行做，每个子代理改完必须自己跑 check_formulas.js + pandoc 编译才能交回。
- **行内 `pmatrix` 会撑开行距**、括号越界：正文里的对角矩阵改用 `$\left(\begin{smallmatrix}t_1&&\\&\ddots&\\&&t_n\end{smallmatrix}\right)$`；块级公式里保留 `pmatrix`。
- **Obsidian callout 语法在 pandoc 里是字面文字**（`[!note]` 原样输出）。要出 PDF 就改**编译副本**（不要动 vault 原件）：`^> \[!\w+\] (.*)$` → `> **$1**`。
- **KaTeX 通过 ≠ 视觉正确**：矩阵对齐、`\ddots` 位置、交换图箭头方向只能看图确认；每次改完公式都 `pdftoppm` 抽页看一遍，别只信脚本的 0 失败。
