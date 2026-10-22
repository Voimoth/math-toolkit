# math-toolkit

数学学习用的 AI 技能库与 Neovim 配置，配合 [math_wiki](https://github.com/Voimoth/math_wiki)（Obsidian 数学笔记）使用：
wiki 放内容，本仓库放「怎么维护内容」和「怎么读内容」。

## 目录

```
skills/                  Hermes / DSH 的技能目录（SKILL.md + references/ + scripts/）
  research/              数学辅导、资料检索、笔记转写
  note-taking/           wiki 写作约定与检查脚本
nvim/                    Neovim 配置（mini.deps 管理插件，obsidian.nvim 读 wiki）
```

## 技能（13 个）

| 技能 | 作用 |
|---|---|
| `math-coach` | 数学/物理辅导方法：因果链讲解、引导式陪练（不代劳） |
| `math-physics-wiki` | wiki 维护主流程：答疑归档、概念页、索引 |
| `wiki-writing-conventions` | 写作约定、记号标准、概念同步、检查脚本 |
| `math-notes-transcription` | 手写/扫描笔记转写与结构化 |
| `bookdex` | 参考书目录检索：哪本书讲过 X（8300 本 / 201 万页） |
| `pdf-problem-search` | 在 PDF 资料库里定位定理/习题出处 |
| `group-theory-coaching` | 代数III 群论课程内容库 |
| `mechanics-coaching` | 理论力学课程内容库 |
| `coaching-index` | 各科进度总索引 |
| `user-math-library` | 数学书籍归档整理 |
| `arxiv` / `grounded-citations` | 论文检索、带出处的写作 |
| `study-tool-adoption` | 评估外部学习工具能否本地部署 |

技能格式就是 Hermes / DSH 的 `SKILL.md` 结构（YAML frontmatter + 正文 + `references/` + `scripts/`），
把需要的目录放进 agent 的技能目录即可；`nvim/` 可直接覆盖到 `~/.config/nvim`。

## 工具：bookdex（参考书目录检索）

`tools/bookdex/` 是上面 `bookdex` 技能的完整实现：只索引**书名 + PDF 书签目录**，没有书签的
取前 20 页目录页文本（扫描件走 tesseract OCR），所以索引库只有几十 MB。

**仓库里不放书（PDF）**：书籍本身有版权，体量也是几十 GB 到几 TB 量级。工具留在这里，
自己拿私有书库跑一遍就能得到同样的查询能力：

```bash
cd tools/bookdex
python3 -m venv venv && ./venv/bin/pip install pymupdf
BOOKDEX_ROOT=/path/to/你的书库 ./venv/bin/python index.py      # 建库（增量，可 --limit 先试水）
./venv/bin/python query.py "正规子群"
```

目录布局、层级权重（课程在用 > MPSI 预科 > 普通参考书）、OCR 语言选择、已知限制都在
`tools/bookdex/README.md`。

## 记号标准

`skills/note-taking/wiki-writing-conventions/references/notation-rules.json` 是唯一规则源，
`notation-standard.md` 是它的人读版。检查一份 vault：

```bash
python3 skills/note-taking/wiki-writing-conventions/scripts/check_notation.py --check /path/to/vault
```

同目录的 `check_wikilinks.py`（链接健康）与 `check_concept_sync.py`（概念地图同步）是配套的另外两项检查。

## 说明

仓库里的技能文本与配置注释主要由 DeepSeek 生成，少量内容来自 GPT 与 GLM，再经人工挑选与修改。

Neovim 配置单独放出来，是因为同一份 Markdown 在不同编辑器里的 LaTeX 渲染差别很大：行内公式的定界符、反斜杠转义、MathJax 支持的宏，各家实现并不一致。
照这套配置能拿到与笔记一致的显示效果；不想折腾环境的话，直接照抄 `nvim/` 即可。

## 许可

MIT，见 `LICENSE`。代码、脚本与配置按 MIT 授权；技能里整理的数学内容来自课程讲义与公开教材，其著作权归原作者，仅供学习。
