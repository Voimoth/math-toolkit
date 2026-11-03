# machine-paths（自 SKILL.md 搬家，原文零删改）

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

