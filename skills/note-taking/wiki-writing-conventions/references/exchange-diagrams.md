# 交换图规范、渲染色检、箭头方向核对

## 规范（2026-10-21 更新：一律 array，禁用 amscd 的 `CD`）

**写法：`\begin{array}{c...c}` + `\xrightarrow`/`\xleftarrow`/`\big\downarrow`/`\big\uparrow`/`\Big\Vert`/`=`，标注用 `{\scriptstyle ...}` 夹在箭头旁。**

为什么改（实情，不要写成“Obsidian 不支持 CD”）：
- **pandoc → xelatex 编译不了**：默认模板不 `\usepackage{amscd}` → `! LaTeX Error: Environment CD undefined.`
- **Obsidian 其实支持 CD**：2026-10-03 实证 `grep -a amsCd /usr/lib/obsidian/obsidian.asar` 命中，它加载的是 `mathjax/tex-chtml-full.js`（full bundle 含 amsCd），`\begin{CD}` 不加 `\require` 也能渲染。
- 但同一份 md 要能双端渲染（Obsidian 读 + pandoc 出 PDF），**array 是唯一交集**，所以全库 18 处 CD 已在 2026-10-21 全换成 array。

已知代价（接受，不要再为此改回 CD）：MathJax 下 array 里的竖箭头只有字符宽、不随两端对象伸展，观感比 amscd 的连线条略松；LaTeX/xelatex 下 `\big\downarrow` 尺寸正常。

### amscd → array 映射

| amscd | array | 备注 |
|---|---|---|
| `@>{lab}>>` | `\xrightarrow{lab}` | 无标注用 `\longrightarrow` |
| `@<{lab}<<` | `\xleftarrow{lab}` | |
| `@V{lab}VV` | `{\scriptstyle lab}\big\downarrow` | 标注在**左** |
| `@VV{lab}V` | `\big\downarrow{\scriptstyle lab}` | 标注在**右** |
| `@A{lab}AA` | `{\scriptstyle lab}\big\uparrow` | 标注在左 |
| `@AA{lab}A` | `\big\uparrow{\scriptstyle lab}` | 标注在右 |
| `@=` | `=` | |
| `@\|` | `\Big\Vert` | |
| `@.` | 空 array 单元 | |

行列规则：列数 = 对象列数 × 2 − 1，全用 `c`、不加竖线；行间 `\\[6pt]`；callout 内的图每行保留 `> ` 前缀；含空格的标签包 `\text{}`。

## 交换图渲染色检（改完必跑）

- **渲染色检手法**：把待检公式抽进一个 HTML（MathJax 3 CDN + **`tex-svg.js`**），`browser_exec` 打开后：① 等 `document.querySelectorAll("mjx-container").length` 达到公式数；② 用 `js` 扫 `document.body.innerText` 里有没有 `Unknown macro` / `Undefined control`（**别数 `merror`**——MathJax 自带 CSS 里就含这个词，会误报）；③ `cdp('Emulation.setDeviceMetricsOverride', width=1240, height=900, deviceScaleFactor=1, mobile=False)` 放大视口后 `capture_screenshot()` **目视检查箭头对齐**。
  - **一次调用跑完的配方（实测可用）**：HTML 里内嵌 `window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]},svg:{fontCache:'none'}}` + jsdelivr 的 `mathjax@3/es5/tex-svg.js`，然后 `browser_exec`：`new_tab('file:///<绝对路径>')` → 轮询 `mjx-container` 数到公式数 → `js('document.body.innerText')` 扫上述错误词 → 设视口 → `capture_screenshot()`。
- **更省事的本机等价手段**：md 全文 `pandoc --pdf-engine=xelatex` 出 PDF → `pdftoppm -r 110 -png` → 直接看页面图。既验了渲染又验了编译（这也是日常首选，HTML 色检只在需要看 MathJax 行为时才用）。
- **用 SVG 输出而不是 CHTML**：无头环境里 CHTML 常因 web font 加载失败而导致**斜体变量全部空白**（只剩数字与箭头），会让人误判成「图坏了」；`tex-svg.js` 用路径绘制文字，不依赖字体文件。
- 改完顺手复查 `$$` 配对（`check_formulas.js` 与 `check_tex_format.js`）。

## 「渲染色检查不出图说反话」——箭头方向必须逐个核对语义

`\swarrow`/`\searrow`/`\nearrow`/`\nwarrow` 只是**方向字符**，写反了照样渲染成功、也没有 merror。实测：余积泛性质图里 $g_X:X\to N$ 被写成 `\nwarrow`（放在中间列），箭头“从 $M$ 指向左上空气”。
- **核对法**：对每个箭头问两件事——**它连接的两个对象是谁？方向对不对？** 尤其两类：
  - **锥形图**（顶点在上、底部几个对象）：顶点在上时 `\swarrow`/`\searrow` 是“从顶点射出”，`\nearrow`/`\nwarrow` 是“从底部射入顶点”；纤维积图与余积图**正好互为镜像**，最易写反。
  - **array 里“箭头在第几列”**：竖直/斜箭头必须落在它真正连接的两列之间，否则指向空列。
- 扫描入口：`grep -rl 'nearrow\|nwarrow\|swarrow\|searrow'` 找出所有斜箭头图，逐个过。

## 数学渲染质检工作流

判断 LaTeX 画法"好不好看"不用猜——①写 HTML（内嵌 MathJax 3 CDN 降级链 bootcdn→staticfile→jsdelivr→unpkg）；②用本机 chromium（`~/.hermes/tools/chromium-1208/`）无头截图：`chrome --headless=new --disable-gpu --window-size=1000,2600 --virtual-time-budget=15000 --screenshot=out.png file:///...`；③用 Hermes 的 `vision_analyze` 读截图质检；④判渲染错误看 DOM 里 `Unknown macro|Undefined control`，别数 `merror`。
