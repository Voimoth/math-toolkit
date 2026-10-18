---
name: math-physics-wiki
description: "维护用户的中科大中法班数学与物理 wiki(/mnt/e/notes):把数学/物理答疑沉淀为对应课程概念页,维护课程索引、互链与 git 提交;Fourier 文献摄入是专题流程。触发:用户要求把问答整理进 wiki、精读傅里叶/调和分析材料、更新概念页或检查 vault 时。"
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [math, physics, wiki, vault, learning, zh]
    category: research
---

# 数学与物理 Wiki 维护(/mnt/e/notes)

用户(中科大中法班数学系)的 Obsidian vault `/mnt/e/notes` 按学科/课程组织,由 agent 维护。数学和物理答疑的可复用内容直接沉淀为概念页;本技能是 wiki 维护的主流程。

## 总原则(最高优先级)

- **问答即沉淀**:用户提出的数学和物理问题,凡含可复用的定义、因果解释、证明要点、方法判断、例子或易错点,回答后直接写入对应课程的 `概念/` 页,不询问是否写入。
- **概念页与笔记分离**:`概念/` 是 agent 整理的知识库页;`笔记/` 只放用户课程笔记与讲义提取文本,不把新增讲解混入。
- 已有页面优先更新;新主题新建概念页并加入索引。
- 概念页用中文,数学术语首次出现附法语名,物理术语首次出现可附英文名。

## 环境事实(务必遵守)

- vault 根: `/mnt/e/notes`;学科目录 `数学\{分析,代数,概率}\`、`物理\{理论力学}\`,每课程目录含 `概念\` 与 `笔记\`,每学科有 `_索引.md`,`log.md`(变更日志,追加式)。
- 布局与写作约定见 skill `wiki-writing-conventions`(**2026-09-11 起这是唯一权威**;原 `/mnt/e/notes/共享/SCHEMA.md` 已删除——它一半是 llm-wiki 模板残留与 vault 现状不符,有效部分已全部迁入该技能,不要再去找该文件)。
- 本地资料库 `/mnt/e/书籍/`(8590+ PDF)。现行分析III Fourier 讲义: `sofar.pdf`(殷浩),提取文本在 `数学\分析\分析III\Fourier\笔记\sofar_extracted.txt`。
- PDF 提取(含中文):系统 poppler —— `pdftotext -layout in.pdf out.txt`(实测中文/法文正常);扫描版走 `pdftoppm -r 300 -png` + `tesseract -l chi_sim+eng`。详见技能 pdf-text-extraction。





- 网络:arXiv 可访问;Semantic Scholar 可访问但约 1 req/s、易 429;维基百科被墙(000,勿重试)。

- git: vault 根即仓库,远端 https://github.com/USTC25010409/math_wiki.git(私有),GCM 免密;改完 `git add`(只加目标文件)+ commit + push。已配 pre-commit 钩子(>5MB 文件拒绝提交)、`.gitignore` 大文件规则、`.gitattributes` 锁 LF;详见下文「git 卫生与 .git 膨胀」。

## 答疑归档流程(标准)

1. 回答数学/物理问题(教学法见 math-coach 技能)。
2. 决定落点:对应课程 `概念/` 下已有相关页 → 更新并 bump `updated`;无 → 新建概念页(frontmatter:title/created/updated/type/tags/sources/confidence)。
3. 页面结构:问题驱动开篇 + 定义/直觉/证明要点/例子/陷阱 + 相关概念 `[[wikilinks]]`(每页至少 2 出链);公式用 `$...$`/`$$...$$`,禁止 emoji。
4. 更新所属 `_索引.md` 与根 `log.md`(追加条目,中文;用 write_file/patch,勿用 Add-Content)。
5. 质量检查:断链(`check_wikilinks.py`)、emoji 扫描、LaTeX 双重转义、**记号**(`check_notation.py --check` 必须 0)。
6. 概念地图收尾:该课 `学习路径`/`概念页索引` 若涉及本次概念,同步更新并 bump `updated`(名单见 `wiki-writing-conventions/references/concept-map-registry.json`)。
7. git add + commit + push;汇报改了哪些文件。

## Fourier 文献摄入(专题)

适用:用户给傅里叶级数/分析文献、讲义章节、arXiv 论文要求精读。

1. 读上下文:对应 `_索引.md`、根 `log.md` 末尾、技能 `wiki-writing-conventions`(写作约定与建页阈值的唯一权威;原 `共享/SCHEMA.md` 已于 2026-09-11 删除)。
2. 获取文献:arXiv 用 `curl.exe -s "https://export.arxiv.org/api/query?id_list=XXXX.XXXXX"`;网页/PDF 被墙则告知用户;教材章节用用户提供文本/PDF。
3. 提炼:对照现有 `概念/` 页更新或新建(2+ 来源或核心主题);Fourier 概念页在 `数学\分析\分析III\Fourier\概念\`。
4. 互链、索引、log、git(同归档流程)。
5. 汇报:改了什么、为什么、下一步。

## 页面 frontmatter 模板

```yaml
---
title: 概念名(中英/法)
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [学科主题, proof-technique, ...]
sources: [Fourier笔记.md]
confidence: high|medium|low
---
```

概念页含:定义、直觉、证明要点、学习提示(中法班视角)、相关概念(互链)。

## 常见任务

- **出题**:基于概念页出 3 道变式题(概念辨析+证明+计算)。
- **复习**:读学习路径/索引页按阶段抽查(如 [[傅里叶学习路径]])。
- **断链检查**:`grep -rhoE "\[\[[^]]+\]\]" <vault>` 取出全部 wikilink,对照现存页 basename(或直接跑 `wiki-writing-conventions/scripts/check_wikilinks.py`)。**`log.md` 是变更日志,里面的 `[[...]]` 是历史记录(含有意保留的"已删除页面"记述,如"删除了对 [[Fourier讲义2026]] 的引用"),不算断链,不要改。**
- **生成关系图谱**:`node scripts/gen_graph.js`(本技能随附,默认 `/mnt/e/notes`,输出 `graph.html`)。Obsidian 桌面版自带 Graph View;nvim/无 GUI 场景用脚本。
- **lint**:孤立页/断链/陈旧页(updated 超 90 天)/标签分类。

## git 卫生与 .git 膨胀(2026-09-11 实战)

`.git` 体积远超笔记本体(本例 **159 MB** vs 工作区 1 MB)。**这类膨胀不在工作区里,扫工作区永远找不出来,必须去 `.git/objects` 查。**

**诊断与回收的完整手法**(三步诊断、可达性权威判据、孤儿对象二进制安全导出、魔数识别、回收命令与事后验证)见
**`math-notes-transcription` 技能的 `references/git-repo-bloat-and-lost-objects.md`** —— 那份是权威版,勿在此重复。
三条最容易错的:**用 `verify-pack` 而不是 `rev-list` 列大对象**(rev-list 会被截断给出错误结论);
`fsck` 报 **unreachable**(被 reflog 吊着)与 dangling 处置不同,前者必须先 `reflog expire`;
**先把大对象导出给用户过目再删** —— 可能是用户的照片,删了永久没了。

**本 vault 已落地的状态(换机器时需重建)**:
- **pre-commit 钩子**:活动位置 `.git/hooks/pre-commit`,存档 `共享/git-hooks/pre-commit`(换机器复制过去即可)。单文件 >5 MB 拒绝提交,`--no-verify` 可绕过。装完必须实测(造 6 MB 文件 `git add -f` 试提交,确认退出码非 0 且未生成提交)。
  两个实现坑:读 diff 列表加 `git -c core.quotepath=false`(否则中文名被八进制转义、匹配失败);用 `while read < 临时文件` 而非管道(管道内变量传不出子 shell)。
- **`.gitignore`**:大文件类型(`*.mp4/*.mov/*.avi/*.mkv/*.flv/*.wmv/*.gif/*.zip/*.7z/*.rar/*.iso/*.exe/*.msi/*.dmg/*.heic/*.raw`)、`wikilinks.md`(Obsidian 反复自动生成的 0 字节产物)。
- **`.gitattributes`**:`共享/git-hooks/* text eol=lf` 等 —— shell 脚本必须 LF,否则 sh 报 "bad interpreter"。

**清洁性检查**:`git status --short` 是入口,能同时暴露空目录(llm-wiki 模板残留的 `docs/ example/ queries/`)与未跟踪生成物。
**顺手清理也要克制**:vault 是用户心血且已 push,只读扫描 → 交用户过目 → 再动手;与 `/mnt/e/书籍` 重复的副本可用 MD5 比对确认后删除。

## 陷阱

- 别用最新 arXiv 研究论文当入门材料——对 L2 学生不合适,优先教材(Stein-Shakarchi 等)。
- 维基百科被墙不要反复重试(zh:000);Semantic Scholar 加 --max-time 与间隔。
- log.md 用 write_file 重写或 patch 追加;Add-Content 在中文编码下有坑。
- 用户强调"陪练不代劳":总结/整理可以,解证明题应引导用户自己完成(见 math-coach)。
- 视觉模型转写数学内容时,prompt 必须要求公式用 `$...$`(行内)和 `$$...$$`(显示)格式;已产出 `\(...\)`/`\[...\]` 则用脚本替换为 `$`/`$$`。
- 写文件工具双重转义坑:写完数学 md 必须扫描 `\\[a-zA-Z]`(双反斜杠+字母)修复为单反斜杠;保留 cases/aligned 环境内合法的行尾 `\\`(其后是空格/行尾)。
- **绝不在 vault 内留临时文件**:临时脚本与中间输出一律放 agent 自己的目录(如 `~/.hermes/cache/` 下按任务命名),写文件用绝对路径;收尾用 `git status --short` 兜底确认没有意外产物落进 vault。
- 收藏夹式的"顺手清理"要**只读扫描 → 交用户过目 → 再动手**:vault 是用户的心血且已 push,任何删除都要用户确认,大对象先导出留底。
- /mnt/e/书籍(8590+ PDF)等大目录严禁 search_files 全树扫描;找文件用 `find <限定子目录> -maxdepth 3 -name \'*关键词*.pdf\'`;库内容检索走 pdf-problem-search 技能。

## 相关技能

- `math-coach` — 教学/陪练/出题与答疑沉淀的触发端
- `wiki-writing-conventions` — 写作格式约定与 git 提交卫生
- `math-notes-transcription` — OCR 转写与笔记结构化
- `pdf-problem-search`、`user-math-library` — 本地 PDF 资料库检索与整理
- `llm-wiki`(bundled)— llm-wiki 结构约定参考
