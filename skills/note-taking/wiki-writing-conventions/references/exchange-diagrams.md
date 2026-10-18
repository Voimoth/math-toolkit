# 交换图规范、渲染色检、箭头方向核对

> 摘自 `wiki-writing-conventions` SKILL.md（2026-10-03 拆分），内容未改。

**交换图规范(2026-09-02 二次反转后最终拍板:一律方形)**:交换图**一律用 `\begin{CD}`(AMScd)方形画法**,array+斜箭头的三角画法已废弃——用户在 Obsidian 实际渲染中发现三角画法与预览差距大(标签/箭头错位),原话"还是换回方形的好了"(当天早些时候"尽量用三角形"的决定即被推翻)。CD 语法:`@>>>` 右箭头、`@VVV` 下箭头(`@V\pi VV` 带标签)、`@AAA` 上箭头(`@AA\bar{\pi}_1A` 带标签)、`@|` 竖双线(同一映射)、`@=` 横双线(同一对象);V 形图也画成方形(`G @>\pi_1>> G/H \\ @V\pi VV @AA\bar{\pi}_1A \\ G/\mathfrak{D}(G) @= G/\mathfrak{D}(G)`)。`\rotatebox` 在 MathJax 渲染异常,禁用作旋转箭头。写在 `$$...$$` 内,行间换行 `\\` 合法,勿被双重转义扫描误修。若未来想试新画法,先用无头浏览器渲染截图给用户确认,不要直接写进笔记。极端难画的图备选:渲染成图片插入 md(默认不用,文本可检索优先)。

**交换图渲染色检(2026-10-03,改完必跑)**：`\begin{array}`+`\downarrow` 手画的交换图，**竖直箭头只有字符宽、不随两端对象伸展**，视觉上悬空且对不齐——这是「图看起来有问题」的主因，一律改用 `\begin{CD}`。
- **Obsidian 支持 CD 已实证**：`grep -a amsCd /usr/lib/obsidian/obsidian.asar` 能命中，且它加载的是 `mathjax/tex-chtml-full.js`（full bundle 含 amsCd + autoload），`\begin{CD}...\end{CD}` 直接可用、**不需要** `\require{amsCd}`。
- **渲染色检手法**：把待检公式抽进一个 HTML（MathJax 3 CDN + **`tex-svg.js`**），`browser_exec` 打开后：① 等 `document.querySelectorAll("mjx-container").length` 达到公式数；② 用 `js` 扫 `document.body.innerText` 里有没有 `Unknown macro` / `Undefined control`（**别数 `merror`**——MathJax 自带 CSS 里就含这个词，会误报）；③ `cdp('Emulation.setDeviceMetricsOverride', width=1240, height=900, deviceScaleFactor=1, mobile=False)` 放大视口后 `capture_screenshot()` **目视检查箭头对齐**（这是唯一能看出「悬空/错位」的办法）。
  - **一次调用跑完的配方（实测可用）**：HTML 里内嵌 `window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]},svg:{fontCache:'none'}}` + jsdelivr 的 `mathjax@3/es5/tex-svg.js`，然后 `browser_exec`：`new_tab('file:///<绝对路径>')` → 轮询 `mjx-container` 数到公式数 → `js('document.body.innerText')` 扫上述错误词 → 设视口 → `capture_screenshot()`，截图直接回到当前会话自视。**CD 图在 tex-svg 下能正常出图、不需要 `\require{amsCd}`**；把新写的 CD 图与几个 inline 公式放进同一页可一并验完。
- **用 SVG 输出而不是 CHTML**：无头环境里 CHTML 常因 web font 加载失败而导致**斜体变量全部空白**（只剩数字与箭头），会让人误判成「图坏了」；`tex-svg.js` 用路径绘制文字，不依赖字体文件。
- 改完顺手复查 `$$` 配对：替换 `array` 块时若 new 串自带 `\n$$\n`，极易产生 `$$\n$$` 空块或把原文的 `$$` 顶错位（本轮就踩了，还顺带查出正课 23 一处**未闭合的 `$$`**）。扫描：每个文件 `t.count('$$')%2==0`，且逐行去 `$$` 后 `$` 数仍为偶。

**但「渲染色检」查不出「图说反话」——箭头方向必须逐个核对语义（2026-10-03 被用户当场指出）**：`\swarrow`/`\searrow`/`\nearrow`/`\nwarrow` 只是**方向字符**，**写反了照样渲染成功、也没有 merror**。实测：余积泛性质图里 $g_X:X\to N$ 被写成 `\nwarrow`（放在中间列），于是箭头“从 $M$ 指向左上空气”。
- **核对法**：对每个箭头问两件事——**它连接的两个对象是谁？方向对不对？** 尤其两类：
  - **锥形图**（顶点在上、底部几个对象）：顶点在上时 `\swarrow`/`\searrow` 是“从顶点射出”，`\nearrow`/`\nwarrow` 是“从底部射入顶点”；纤维积图（$p_X:E\to X$ 用 `\swarrow`）与余积图（$g_X:X\to N$ 用 `\nearrow`）**正好互为镜像**，最易写反——修完最好把两张图并排渲染对照。
  - **`array` 里“箭头在第几列”**：竖直/斜箭头必须落在它真正连接的两列之间，否则指向空列。
- 扫描入口：`grep -rl 'nearrow\|nwarrow\|swarrow\|searrow'` 找出所有斜箭头图，逐个过；斜箭头图数量少，人工核对成本低。

**数学渲染质检工作流**:判断 LaTeX 画法"好不好看"不用猜——①写 HTML(内嵌 MathJax 3 CDN 降级链 bootcdn→staticfile→jsdelivr→unpkg);②用本机 chromium(`~/.hermes/tools/chromium-1208/`)无头截图:`chrome --headless=new --disable-gpu --window-size=1000,2600 --virtual-time-budget=15000 --screenshot=out.png file:///...`;③用 Hermes 的 `vision_analyze` 读截图质检;④判渲染错误看 DOM 里 `Unknown macro|Undefined control`,别数 `merror`(MathJax 自带 CSS 含该词)。
