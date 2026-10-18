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
| `math-library-search` | 本地数学书库检索（RAG） |
| `pdf-problem-search` | 在 PDF 资料库里定位定理/习题出处 |
| `group-theory-coaching` | 代数III 群论课程内容库 |
| `mechanics-coaching` | 理论力学课程内容库 |
| `coaching-index` | 各科进度总索引 |
| `user-math-library` | 数学书籍归档整理 |
| `arxiv` / `grounded-citations` | 论文检索、带出处的写作 |
| `study-tool-adoption` | 评估外部学习工具能否本地部署 |

技能格式就是 Hermes / DSH 的 `SKILL.md` 结构（YAML frontmatter + 正文 + `references/` + `scripts/`），
把需要的目录放进 agent 的技能目录即可；`nvim/` 可直接覆盖到 `~/.config/nvim`。

## 记号标准

`skills/note-taking/wiki-writing-conventions/references/notation-rules.json` 是唯一规则源，
`notation-standard.md` 是它的人读版。检查一份 vault：

```bash
python3 skills/note-taking/wiki-writing-conventions/scripts/check_notation.py --check /path/to/vault
```

同目录的 `check_wikilinks.py`（链接健康）与 `check_concept_sync.py`（概念地图同步）是配套的另外两项检查。

## 许可

MIT，见 `LICENSE`。技能里的数学内容整理自课程讲义与公开教材，仅供学习。
