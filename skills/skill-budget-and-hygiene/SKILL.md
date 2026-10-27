---
name: skill-budget-and-hygiene
description: 写或拆技能前先读:体量预算、分层、去重、时效、脚本化。
version: 1.0.0
author: Hermes Agent
created_by: agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [skills, budget, hygiene, maintenance, tokens]
    category: autonomous-ai-agents
    related_skills: [hermes-memory-maintenance, hermes-self-config, coaching-index]
---

# 技能体量预算与维护卫生

本机所有 SKILL.md 的**写入标准**：新建、改写、拆分、增补任何技能前先读这一份，不再各技能各自定规矩。
只管「怎么写、留多少、旧内容怎么退役」；记忆文件本体见 `hermes-memory-maintenance`，Hermes 结构配置见 `hermes-self-config`。

## When to Use

- 要新建技能、拆技能、给技能加一节、改 description；
- 发现自己在犹豫「这个技能该不该加载」；
- 要判断某条内容该进 SOUL / 技能正文 / references / wiki / 脚本 / 现场测。

## 工作方式（本机定死的两条）

1. **启停与规模我自己定，不问他。** 哪些技能启用/禁用、拆到多大、哪本内容下沉，都是我的判断：他只关心结果好用。判断依据是实测（用频 × 体量）与分层表，不是「他可能想要」。唯一需要问的：涉及删文件、改外部账号、不可逆动作。
2. **先立法，再施工。** 批量改造前先把方案落成一份可引用的文件（本技能或它的 references），再按批次执行、每批报前后数字与回退方式。他发现「揪着一处就开始改」会直接叫停——因为单点改动会让余下的批次彼此不一致。方案已经在文件里时，后续任何会话都从同一套标准出发。

**长会话中途再改同一个技能，先重新读当前文本。** 后台复盘轮（background review / curator）会在两次对话之间直接改写 SKILL.md 并新增 references，你手里记住的原文可能已经不存在，`old_string` 会失配。改前 `grep -n` 一下目标句子，或重新 `skill_view`。

## 口径：一律按 token / 字符量，不按直觉

中文 1 字 ≈ 1.6 token，纯中文文件 1 字符 ≈ 3 字节。**旧规矩写的「20KB」是字节**，换算约 2,500 tokens。下表统一为字符与 token：

| 项 | 上限 | 理由（本机实测） |
|---|---|---|
| SKILL.md 正文 | **8,000 字符**（≈3k tok） | 单次 skill_view 中位 9.7k 字符、p90 17.3k、最坏 33.5k |
| 一次加载总成本（正文 + 同时要读的 references） | **15,000 字符**（≈6k tok） | 重会话累积 40–110KB 技能文本，此后每轮重读 |
| `description` | **≤60 字符、不含空格** | 索引按 60 字符截断后**回退到最后一个空格**（已核实，57/57 条吻合）；中文描述带空格会在第一个空格处断掉，如「代数III...」「在本地 PDF...」 |
| 规则句密度（禁止/必须/不要…占正文比例） | >35% 即该拆 | 实测 original-math-idea-review 46.9%、koishi-hdsi-bot 45.4%、mechanics-coaching 39.5% |
| 技能索引总量 | 60 条以内为舒适区 | 现在 57 条 = 4,177 字符 ≈1.5k tok，够用；每新增一条都要为它腾出条数 |

判据不是「读起来长不长」，而是**一次加载会不会超过 15,000 字符**。超了就拆或下沉，没有例外。

## 分层：每类信息只有一个家

| 内容 | 家 | 判据 |
|---|---|---|
| 每轮都必须生效的硬约束 | `SOUL.md`（现 1.4KB，目标 ≤4KB） | 技能靠 description 匹配，匹配失败＝没约束；为拿三条规则先读 3–10k tok 正文是亏的 |
| 方法 / 流程 / 判据 / 陷阱 | 一个技能，同类只此一处（本机＝`math-coach` 式的「方法层」） | 会被多门课共用的操作纪律 |
| 内容层 | 每门课一个技能，**按课程命名，不按分支命名** | `algebra-iii` / `analysis-iii` / `mechanics-b`；主题漂移时改内部小节，不改名 |
| 进度账本（讲到哪、作业到第几周） | 只放 `coaching-index` 一处 | 训练/复习状态每天都在变，两处必矛盾 |
| 案例、快照、题地图、历史实战、长表格 | `references/`，正文只留主题索引 | 不是每轮都要用的深度内容 |
| 每轮必注入的记忆（MEMORY / USER） | 只放跨领域公用的事实、约定、元规则；领域细节一律外置，判据见 skill `hermes-memory-maintenance` 的「记忆的公用地带」 | **领域无关性**：每一类会话（只问数学/只问代码/只排桌面/只玩游戏/只维护机器人）读到它都不能觉得多余；**反向也要查**跨领域通用操作（镜像前缀、SSH 端口、提权、识图降级、渲图）必须留在记忆 |
| 会变的数值 / 路径 / 端口 / 版本 | **现场测**，不写死 | 本机实测 758 处路径引用已有 171 处（23%）失效 |
| 知识沉淀 | wiki 概念页（`/mnt/e/notes`），技能里只留「去哪找 + 教法纪律 + 陷阱」 | 否则技能会随沉淀线性膨胀（group-theory 20KB→25.6KB 就是这么来的） |

分组改名或新增技能时，主技能 `When to Use` 里已搬走的触发词要一并删掉，否则两个技能互相抢触发。

## 去重：判据是「会不会同时加载」

全局计数没有意义，单技能自包含是设计（只加载它时也要拿得到规则）。**同一次会话里会被一起加载的两个文件写同一条规则，才算浪费。**

本机已知共载组（近 30 天实读次数）：`wiki-writing-conventions` 48、`math-coach` 24、`coaching-index` 21、`linux-desktop-admin` 17、`algebra-iii-coaching` 15 —— 同组内规则只许出现一次，其余写成一行指针。

实测重复样例：`prose_lint` 跨 6 文件 12 次、「只给目标不铺路」8 次跨 6 文件、「概念页只写概念」13 次、`git add+commit+push` 25 次。

**覆盖式更新**：写新条目时删掉它取代的旧条目。日期戳（2026-10-xx 实战定型）不是免检牌——全库 265 处日期戳，读到两条冲突结论时模型只能猜。旧结论要么删，要么明确写「此法已废，改用 X」。

## 脚本化：可判定的约束换成退出码

能被机器判定的约束不要写成长散文。本机已在用且真跑过（近 30 天 176 个会话）：`check_notation` 71 次、`check_wikilinks` 58、`check_concept_sync` 54、`lint_natural_chinese` 38、`prose_lint` 32。

三条硬要求，缺一条就是负收益：

1. **输出是修好的文件或非零退出码**，不是「发现 3 处，请人工判断」——否则我要读输出、还要判断、还要记得跑，比散文更贵。
2. **触发点固定**（写完笔记/写完解答就跑），不依赖「记得跑」。
3. **脚本化后删掉对应的散文**，只留一行「跑 `check_x.py`」。

不可判定的（先讲动机、不铺路、把球踢回去、诚实标注不确定）**不进脚本**，留在 SOUL 或方法层技能。

## 时效：过时内容分三类，处理手段不同

| 类型 | 例子 | 手段 |
|---|---|---|
| 可机检事实 | 路径、端口、包是否装了、命令是否存在 | 脚本核查（`scripts/check-skill-facts.py`），直接给替代路径，不交待核清单 |
| 随课程推进变的账本 | 讲到哪、作业到第几周 | 单一真相源（`coaching-index`），课程技能只留指针 |
| 教训 / 纪律 | 教法、坑、用户校准 | 覆盖式更新；不会「过期」，只会被更好的一条取代 |

frontmatter 加自用字段 `reviewed: YYYY-MM-DD`（Hermes 不读，脚本与我从据此判多久没复核）。

## 生命周期：curator 只用来退役，不要批量纳管

本机 curator 已启用（7 天一轮；14 天未用→stale，30 天未用→归档到 `~/.hermes/skills/.archive/`，可恢复；最近一次「4 stale, 1 archived」），只管带 provenance marker 的 agent-created 技能。

- **不要 `adopt --all-unmanaged`**：实测待纳管的 19 个里含 `math-coach`、`coaching-index`、各科 coaching 这类**学期性低频**技能——一学期讲完就会 30 天不用，被静默归档才是真伤害。unmanaged 默认「永不自动处理」，对本机是安全默认，保持不动。
- 只有已确认「长期不用＝该退休」的技能才 `hermes curator adopt <name>`；要反向保住的用 pin。
- 它的判据是**使用频次，不是内容正确性**：解决「没人用」，解决不了「还在用但已过期」。后者靠上面的脚本核查 + 单一真相源 + 覆盖式更新。
- LLM 复盘（合并/打补丁）默认关。要用先 `hermes curator run --dry-run` 看报告不动库，再 `--consolidate`；一次全扫 50–100 次 API 调用，配 `auxiliary.curator` 指向便宜模型。

## 本机工具(scripts/，别手搬)

- `scripts/split-skill.py PATH [--move '节标题前缀=references/<文件名>.md' ...] [--dry]` —— 把超大 `##` 节搬到 references：原文零删改、正文留首段+指针、自动子串证全（丢失/残留都报）、末尾报前后字符数。不带 `--move` 则只列节表供选。文件名先 `ls references/` 避开同名已有文件，否则覆盖。
- `scripts/check-skill-facts.py [--all] [--skill N] [--deep]` —— 核查正文里断言的本机路径是否还在。只查 `/mnt/*`、`/home/_username/*`、`~/.hermes/tools|skills|installs`、`~/.local/bin|share`、`~/.dsh` 等「真布局」前缀；`~/Desktop`、`~/.config/<某应用>` 这类例子不查（实测全查 282 条中 90% 是举例）。省略号占位与空格截断的提取伪影自动跳过。**端口不查**：技能里的 `:8080`/`:5678` 指「服务启动后应监听」，按「现在是否监听」判 100% 误报。
- `scripts/measure-skill-bloat.py [--days 30] [--top 15]` —— 先量再答：索引条数与 description 总字符、system prompt 各段位移、每个技能的正文大小、近 N 天每个技能被加载的「次数 × 平均字符」与累积重读量、超 8,000 字符清单。判断「该先动哪个」「最近为什么变笨」先跑它，别凭感觉。
- 跨技能指针（形如「见 <技能B> 的 references/<文件>」）在本技能目录里找不到文件是**正常的**，不是 dangling；别为此复制一份文件。

## 改动的操作手册

改名 / 拆分 / 压缩成骨架 / 失效路径分类 / 回退，逐条命令与验收都在 `references/skill-surgery-playbook.md`。**拆编号列表前必读那一节的串号坑**：按空行切块会漏条，以编号为键会串号，只能逐行扫描并只接受严格递增的编号序列。

## 本机现状快照（2026-10 批量瘦身）

十个高频技能已全部拆到 ≤8,000 字符（最重 34,044→7,967；合计 ~223k→~66k，按 30 天实际加载次数回算每轮少重读 ~65 万 tokens）。**剩下的活**：

- `check-skill-facts.py` 残留 20 处，以示例、历史记录、运行时产物为主；真失效的逐条判「换新路径还是删整句」。
- **bundled 大件一律不用就关**（成本不在索引一行，而在误触发一次就 8–34k）。2026-10-27 已 disable：humanizer 34k、p5js 27k、computer-use 18k、python-debugpy 15k、grounded-citations 12.6k、manim-video 12k、powerpoint 10.8k、xlsx 9.6k、hermes-desktop-plugins 8.8k、inspecting-hermes-desktop-dom、jupyter-live-kernel、obsidian（本机已卸）、opencode（代码走 DSH）。**留着没禁**：pdf、docx、arxiv、spike、github、blocked-page-recovery、architecture-diagram —— 索引一行很便宜，真需要时是刚需。

## 交付前自检

- [ ] 正文 ≤8,000 字符，一次加载 ≤15,000 字符
- [ ] 新内容按「分层表」放对了家，没有第二份副本
- [ ] `description` ≤60 字符、无空格、前 12 字是触发词
- [ ] 被取代的旧条目已删（不是追加在下面）
- [ ] 可机检的事实改成脚本或现场测，正文里没有写死的路径/端口/版本
- [ ] 拆走的节：原文 `in` references 且 `not in` 正文；frontmatter 仍能 `yaml.safe_load`
- [ ] 压成骨架的：原文整节先存进 references 再重建正文，条数与编号核对过
- [ ] 改过名的：`grep -rn '<旧名>'` 在 skills/ 与 memories/ 为 0，`.usage.json` 与索引快照已同步
- [ ] `skill_view` 回读一遍，`linked_files` 与预期一致
- [ ] 拆分/新建体量变化后报前后数字与回退方式
