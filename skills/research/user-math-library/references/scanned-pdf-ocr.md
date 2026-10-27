# 扫描版 PDF 的文字化:两条管线(2026-09 实测)

扫描版 PDF(pdfjs 提取只有 `===== PAGE n =====` 无正文)按内容类型选管线:
- **印刷体扫描件**(书、讲义)→ Tesseract OCR(快、免费、可批量)
- **手写体**(手写笔记、板书)→ 视觉模型转写(手写 OCR 不可靠,视觉模型按上下文推断)

## 管线 A:Tesseract OCR(印刷体)

### 环境(已装好,2026-09)
- Tesseract v5.4.0:`/usr/bin（tesseract）\tesseract.exe`(安装器强制路径,无法改)
- 语言包在 H 盘:`/mnt/h/tesseract/tessdata`(chi_sim/eng/fra/rus/osd),用户级环境变量 `TESSDATA_PREFIX=/mnt/h/tesseract/tessdata`
- pdftoppm 来自 texlive:`D:\texlive\2025\bin\windows`(已在 PATH)

### 用法
```powershell
$env:TESSDATA_PREFIX = "/mnt/h/tesseract/tessdata"
pdftoppm -png -r 300 "书.pdf" "page"          # PDF 转 300dpi 图片
tesseract "page-1.png" "out" -l chi_sim+eng   # 中文 OCR(法文用 fra+eng,俄文用 rus+eng)
```

### 限制(诚实告知用户)
- 公式/希腊字母/上下标识别不可靠,仅正文可读——数学公式仍以原图为准
- 中文+英文混排用 `-l chi_sim+eng`(多语言)

## 管线 B:视觉模型转写(手写体,首选)

本机用 `math-notes-transcription/scripts/vision_transcribe_batch.py`(纯标准库,--dir/--start/--end/--model/--prompt,key 自动从 `$HERMES_HOME/.env` 读,输出同名 .txt、已存在则跳过)。对**手写数学笔记**转写质量远好于 Tesseract(按上下文推断潦草字迹)。

### 流程
1. `pdftoppm -png -r 300 "笔记.pdf" "cours_ocr\page"`(每页一张图)
2. 逐页/批量调用 `python3 ~/.hermes/skills/research/math-notes-transcription/scripts/vision_transcribe_batch.py --dir <图目录> --model deepseek-flash --prompt "<prompt>"`
3. 合并各页 .txt 为完整 markdown,修正编码,归档到 vault(见下)

### 归档位置(2026-09 二次重构后)
`/mnt/e/notes/数学/<学科>/<课程>/笔记/`(如 `/mnt/e/notes/数学/代数/代数III/笔记/`)。注意:曾用过 `/mnt/e/notes/课程笔记/<学科>/`,vault 重构后此路径已废弃。agent 整理的概念页放同课程的 `概念\` 子目录(与用户笔记分离)。frontmatter 注明"OCR 转写,公式以原图为准"。

### 批量调用关键坑(2026-09 实测踩过)
- **嵌套 cmd 会失败**:`cmd /c "powershell -File ..."` 双层嵌套导致参数损坏,每页都"无输出文件"。**必须直接调用**(当前 PowerShell 会话里 `powershell -File ...` 或循环内直接调用)。

- **输出路径**:脚本输出「图片名去扩展名 + .txt」(`page-01.png` → `page-01.txt`),不是 `page-01.png.txt`;按此判断是否已完成,别重复调用浪费额度。
- **批量跑用 `terminal(background=True, notify=True)`**:长批(50+ 页)放后台并重定向日志;脚本按已存在的 .txt 断点续转,中断重跑安全。
- 每页约 30-60 秒(手写+公式),17 页约 10-15 分钟;后台跑 + notify_on_complete。
- 空白页识别会返回"I'm unable to transcribe"(封面页等),跳过即可;判断依据:图片文件极小(<50KB)或模型回复该话。

### 转写后整理(prompt 已要求但需复查)
- **LaTeX 分隔符必须用 `$...$`(Obsidian 兼容)**:视觉模型默认输出 `\(...\)`/`\[...\]`(LaTeX 原生),Obsidian markdown 渲染器不认 → 用户明确纠正"渲染不了"。合并后统一替换:
  `\(` → `$`,`\)` → `$`,`\[` → `$$`,`\]` → `$$`(Node 脚本一次替换,实测 234 处行内 + 34 处显示公式)。
- **跨行 `$` 单独占一行仍渲染不了(二次纠正)**:替换后若 `$` 单独占一行(公式在下一行才结束),Obsidian 也不渲染——**跨行公式必须用 `$$...$$`**。检测:某行 trim 后恰为 `$` → 转 `$$`。实测 66 处。
- **OCR 转写可能把内容包进 ```markdown 代码块**(模型偶尔输出),整段不渲染 → 合并时去掉 ```` ```markdown ```` 与闭合 ```` ``` ```` 标记。
- **清理模型噪音文本**:转写回复里可能混入 "Here is the transcription of..." 开场白、空白占位 → 合并时剥离。
- **格式验证(提交前必做)**:Node 脚本逐行统计 `$` 数,报"奇数 `$` 行";检查 `$$` 成对、单独 `$` 行数为 0、无 ``` 残留。见 `scripts/verify_math_format.js`。实测两个文件均 FORMAT_OK 后才算完成。
- **UTF-8 双重编码修正**:手写 OCR 常见 `Ã©`→é、`Ã `→à、`Ã¨`→è 等;用 Node/PS 正则统一修正后再归档。
- **归档时更新对应学科/课程的 `_索引.md` (顶层 README 已于 2026-10-03 删除)**。

### 结构化升级(用户要求:像傅里叶概念页那样)
转写文本只是原始素材。**用户明确要求**(2026-09):"像自己的 wiki 一样用 tip/note 文本框分隔,使结构更清晰;概念分条整理,就像你对傅里叶级数做的一样"。所以:
1. 原始转写 → `笔记\` 子目录(存档,修好公式即可)
2. 另建结构化概念页 → `概念\` 子目录:按主题分节(`## 1. 群的基础`),每节用 Obsidian callout 分层:
   - `> [!note] 定义/定理` — 陈述与公式
   - `> [!example] 例子` — 具体实例(计算、反例)
   - `> [!tip] 想法` — "为什么"/直觉/证明思路(因果链精神)
   - `> [!warning] 陷阱` — 易错点(如"正规性不传递")
   - 结尾加"本章主线"因果链图(`→` 箭头链)
3. `_索引.md` 同时列出:概念页(主入口)与笔记页(原始存档),分别标注

### 实测参考
2026-09-01:Marc Rosso《Cours de Groupes》手写法语 17 页 → 视觉转写 → 当时那份单文件 `/mnt/e/notes/数学/代数/代数III/笔记/代数III笔记.md`(15KB,16 页; **2026-10 已拆为 `笔记/正课/01–14.md`,不再存在**)。文本层存在但质量差(逐词乱序、大量错字),弃用;视觉模型转写质量高(定义/例子/定理编号齐全)。
