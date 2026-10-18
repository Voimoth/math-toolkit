# 编辑工具链的坑（双重转义、patch/here-string、无文件工具写中文）

> 摘自 `wiki-writing-conventions` SKILL.md（2026-10-03 拆分），内容未改。

**用户纠正后的跨学科批量重命名流程**:用户要求将其他课程（分析、物理等）已有英文概念页标题也中文化时，先扫描所有目标学科的概念目录，建立明确的旧文件名→中文文件名映射；再重命名文件，并逐一更新全库 wikilink。不要只处理当前课程，也不要把一次批量操作误认为只适用于代数。重命名后必须搜索旧 basename 确认无残留，验证新文件存在、链接可解析，再提交推送。

**跨课程同名概念页 → wikilink 必须带路径（2026-10-03 用户选定）**：同一概念在两门课各有一页时（如 `群`/`商群`/`正规子群`/`同构定理`/`导群`/`群作用`/`模` 在代数 I 与代数 III 各一份），`[[群]]` 在 Obsidian 里解析到哪一个是不确定的。约定写成 `[[代数I/概念/群]]`（Obsidian 显示 basename，**不必加别名**）；学科级 `_索引.md` 要**按课程段落分别加前缀**（不能整文件一刀切），`[[00-总览]]`/`[[_索引]]` 等同名约定文件本来就该写全路径。改完全库复查两项：指向歧义 basename 的**裸链接数 = 0**、断链 = 0。

**双重转义扫描(接手其他会话/工具产出的数学 md 必做)**:写文件工具可能把 `\command` 写成 `\\command`,Obsidian 渲染成字面 `\command` 乱码。扫描 `\\[a-zA-Z]`(双反斜杠+字母)与 `\\[,!;\s]`(双反斜杠+间距标点)两类坏模式,修复为单反斜杠;**保留** cases/aligned 环境内合法的行尾 `\\`(其后是空格/行尾而非字母)。2026-09-02 实战:用户另一会话产出的 5 个傅里叶概念页共 446 处坏转义,两轮正则修复清零后复扫干净。
- **扫描脚本要区分「合法的 LaTeX 反斜杠」与「真坏转义」(2026-10-03 补)**:`\\[6pt]`(cases/matrix 里的行距)、以及 matrix 类环境里用 `\\` 换行后紧跟列内容(`a&b\\c&d` 这种)都会命中双反斜杠扫描模式,但**它们在数学环境内完全合法**——直接"修"会把公式改坏。判据:命中处是否落在 `$...$`/`$$...$$` 或 `matrix/cases/aligned/array` 环境内;环境内的一律放过,只有**纯文本**里的双反斜杠才是坏转义。同类误报:行距写法 `\\[Npt]`、`\\` 后接字母的换行——都可放过,别把它们当错误报给用户。
- **PowerShell 检查时的转义层次(2026-09-08 实测误报)**:单引号字符串 `'\\[a-zA-Z]'` 传给 .NET regex 后只匹配「单反斜杠+字母」——正常公式行(每个 `\mathrm` 都是单反斜杠)会全部误报(曾一次报 155 行)。要匹配真正坏模式「双反斜杠+字母」,PowerShell 源码必须写 `'\\\\[a-zA-Z]'`(regex 层 `\\` = 一个反斜杠,两个 `\\` 才匹配双反斜杠)。命中行里 pmatrix/cases/aligned 的行分隔 `\\`(如 `a&b\\c&d`、cases 换行)属合法,逐条目检排除后再报告。

**无文件工具会话的中文写入法(2026-09-08 实测)**:部分 Hermes 桌面会话只暴露 terminal,没有 write_file/patch 工具。写中文 markdown 用 PowerShell `[IO.File]::WriteAllText($p, $content, (New-Object Text.UTF8Encoding($false)))`(无 BOM,Obsidian/git 均正常),大文件分段:首段 WriteAllText + 后续 `[IO.File]::AppendAllText`;长文本一律用 here-string `@'...'@`(逐字保真,LaTeX/`$`/中文引号均安全)。注意本环境命令疑似经包装器执行:含长普通单引号字符串字面量(如 `.Replace('- [[商群]] — 商群', ...)`)会触发 Invoke-Expression 解析崩溃(`Missing ')' in method call`),把替换的 old/new 都定义为 here-string 或双引号变量即可绕开(实测成功)。避免在一条命令里堆多个长单引号字面量。另注:`[IO.File]::ReadAllText/WriteAllText` 等 .NET API 按**进程工作目录**解析相对路径,PowerShell 的 `cd`/`Set-Location` 不改变它——脚本里文件路径一律用绝对路径;git 操作用 `git -C /mnt/e/notes ...` 而不要先 `cd` 再跑(2026-09-08 实测相对路径抛 DirectoryNotFoundException)。

**优先用 write_file 工具,别用 here-string 硬塞(2026-09-14 实测:连续 9 次调用失败)**:本会话验证了一个更强的规则——**只要有 `write_file` 工具可用,就别用 PowerShell here-string 写长中文 markdown**。here-string 方案有三类反复踩中的坑,每次都要重试、烧 token:

| 坑 | 症状 | 规避 |
|---|---|---|
| 末尾多打一个 `'@` | `The string is missing the terminator: '.` 整条命令解析失败 | 不要在复杂命令里手工拼 here-string;改用 write_file |
| `$变量` 后紧跟中文或全角标点 | `Variable reference is not valid. ':' was not followed by a valid variable name character` / `InvalidVariableReferenceWithDrive` | 输出串里写 `"奇数$行:"` 会炸;改用 `${行}` 或换措辞 |
| 双引号字符串里含 `$L$`、`$\ddot{x}$` 等公式 | PowerShell 把 `$L`、`$\ddot` 当变量展开,**`.Replace()` 静默不匹配**(报 MISS 但文件没改) | 含 LaTeX 的 old/new 串一律用单引号 here-string 或单引号字符串 |

**诊断顺序**(本会话踩坑后总结):①若替换返回 MISS,先怀疑 `$` 展开而非"目标串不存在"——用 `$c.Contains()` 单独验证,并改用单引号;②`.Replace()` 返回 MISS 时**必须回读文件确认到底改没改**(本会话有一次前一轮的替换其实已生效,后一轮 MISS 造成"改了两次"的困惑);③清理临时文件用 `Remove-Item -ErrorAction SilentlyContinue` 一次列全,别逐条试。

**`write_file` 工具写 wiki 页是首选**:它直接落 UTF-8 无 BOM、不需要转义层、不受包装器解析影响。本会话最终改用 `write_file` 逐页写 11 个概念页,零失败。**唯一例外**:需在已有文件里做精确小替换时,用 `[IO.File]::ReadAllText` + `.Replace()` + `WriteAllText`(整写会丢掉未预期的其它改动)。

**文件编辑工具安全(patch 工具转义坑,2026-09 实测)**:`patch`(V4A)工具处理 old/new 字符串时会解析 backslash-r 类序列——实测把 LaTeX 右定界符 `\right)` 写成「回车+ight)」,公式被拆成两行破坏(如 `...|\mathrm{Fix}(g)|` 后接孤行 `ight).`)。凡替换串含 `\left`/`\right`/`\overline` 等反斜杠序列,不要走 patch 工具,改用 PowerShell `[IO.File]::ReadAllText` + `.Replace()`(或 write_file 整写);改完用 search_files 搜 `^ight`、孤立 `ight)` 等模式验证零残留,并回读该公式行。另:Obsidian 附件嵌入写 `![[附件/名.svg]]`;`![[名.svg|附件/名.svg]]` 会把路径当成别名,渲染成错误链接(2026-09 实测),修复只需去掉 `|` 及后段。同一文件的多个 patch 不能并行发——并发写同一文件触发 Windows 文件锁,后发的报 `atomic write failed: [WinError 5] 拒绝访问`;同文件多处修改必须串行(2026-09-05 实测,先发的成功、后发的失败,重试即过)。
