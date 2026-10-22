# pika 数学学习工具包（资产地图）

个案：用户丢来 `pika_math_learning_toolkit-<ver>/payload`（6 个子技能、421 文件、6.9MB），
问「有哪些可借鉴的地方」。下面是可搬资产的坐标与落点，下次他说「搬吧」直接按这个执行，别重查。

## 先看结论：六个子技能里只有四小撮纯规则文本值钱

| 子技能 | 体量 | 判断 |
| --- | --- | --- |
| `manage-personal-knowledge` | 948KB，其中 `scripts/` 480KB（registry.py 102KB、operations.py 88KB、manage_kb.py 92KB）+ tests | 重型 KB 服务，**不搬**；只挑两个 references |
| `math-research-solve` | 1.9MB，`references/` 里全是 Windows/DSH 运行时与打包耦合 JSON | 几乎全**不搬**；只借「失败路径归档」的思想 |
| `math-coach` | 1.7MB，含 105KB appserver + 65KB web UI + 50KB Windows 运行时 | 只搬 `references/attempt-graph.md` 的两条规则 |
| `math-science-computation` | 252KB，scripts 是后端探测 | 只借「先探测后端再声明能不能算」的纪律（本机无 Mathematica） |
| `obsidian-vault-notes` | 914KB，`references/` 里全是风格/编辑/校验文本 | **最值钱的一包**，见下 |
| `pdf-problem-search` | 427KB，`references/` 是检索方法论 | 第二值钱，见下 |

## A. 中文「AI 味 / 英译腔」lint 规则集（可搬，零依赖）

`obsidian-vault-notes/references/natural-chinese-lint.json`（10.2KB）+ `style_terms.yml`（0.3KB）

- 24 条短语规则 + 20 条正则，带 `category`（英译腔 / 空名词 / 搭配不稳 / 模板句 / 泛化结论 / 宣传腔 /
  模糊归因 / 修改过程泄漏）、`confidence`、以及「该怎么改」的 message。
- 最值得抄的一条是 `diff_anchored_prose`：匹配「本节/本文/这一段新增了…」—— **改动过程泄漏**，
  正是本地 wiki 铁律里禁的「夹带改动过程」。
- 另有 `allowed_phrases` 白名单机制：把已确认的专业术语列进去，防 lint 误伤（值得一并照搬）。
- **落点**：`math-physics-wiki` / `wiki-writing-conventions`（落盘前跑一遍）。规则本身是中文长篇散文向的，
  用于概念页时把「宣传腔/泛化结论」那几类降级为提示即可。

## B. 编辑协议与大编辑门槛（搬流程，不搬脚本）

`obsidian-vault-notes/references/editing-protocol.md` + `large-edit-verification.md`（11.9KB / 9.7KB）

可直接搬成 wiki 流程的一整套：

- 编辑前**从磁盘读目标**（索引文本不能当编辑基线）；dry-run → 前后 SHA256 + 竞态检查 → 才写。
- 只动最小 span；**改写前就存在的 hunk 一律当成用户的**，不许覆盖。
- **大编辑门槛**：完整候选先在 vault 外准备好 → 跑完确定性检查 → 独立子代理（绑 hash 与 gate）评审 → 才落盘。
  三轮失败后的 `accepted_after_three_reviews` 必须明说「不是 verifier 批准」。
- 落盘后必跑两类 checker：wikilink/embed 解析（heading/block anchor 唯一性）＋ Obsidian 数学分隔符与 TeX 组结构；
  并写明「agent 自己数分隔符、散文 lint、肉眼检查都不是替代品」。
- 表格单元格里的 wikilink alias 必须 `\|` 转义（不转义会让 cell 提前结束）。内部编号引用用中文引号「命题1.1」。
- **落点**：`math-physics-wiki`（或 `wiki-writing-conventions`）。本地已有 `verify_math_format.js`，这套是它的超集。

## C. 数学笔记的「证明状态」纪律（搬规则）

`obsidian-vault-notes/references/math-note-style.md`（8KB）

- 只在有用处时加状态标签：`已证明` / `证明草图` / `待检查` / `猜想·启发式`；
  **正式 callout（命题/定理/引理/推论）里绝不放「证明状态：…」** —— 那里只放数学陈述本身。
- 不确定的推导、记忆里的定理陈述必须显式标注，**不许把不确定磨平成自信的证明**（与本地「指出论证缺口不圆场」同条）。
- 明确三分来源：笔记里已有的 / 从相邻笔记检索来的 / 新推断的。
- **TeX 传输**：反斜杠是数据；用「控制词 shadow」检测反斜杠丢失（`\name` 在别处出现、该位置只剩裸 `name`）
  —— agent 生成 LaTeX 最阴的一类 bug。
- 短公式用紧凑段内 display（`text$$公式$$text`），长推导/矩阵/分段才用独立块。
- **落点**：`math-coach`（讲义的输出质量节）与 `wiki-writing-conventions`。

## D. 检索的评测契约 + 失败分层改进法（搬方法论）

`pdf-problem-search/references/query-normalization.md`（5.9KB）、`improvement-strategy.md`（4.2KB）、
`manage-personal-knowledge/references/search-evaluation-contract.md`（4.8KB），另有两份现成回归样例
`math-anchor-contract-v1.json`、`math-locate-v1-fixture.json`

- **结果契约**：库内相对路径 + 1-based 页码 + 精确原文摘录 + 匹配原因 + 提取状态 + 覆盖警告。
- **空结果只能声称**「在已检查、当前已索引的正文里没找到」；`no_text`/`error`/索引缺口是**覆盖状态**，
  不是「不相关」；同名文件必须靠相对路径/资源 ID。
- **硬概念不许提前放宽**（Borel vs Lebesgue、右连续 vs 连续…）：命中更弱命题就不算 exact hit。
- **页面角色分层**：overview / 提示页 / 解答页 / 证明成分页降权，编号题面与定理陈述页升权。
- **改进循环**：失败**当轮就冻结成回归用例** → 定位失败层（语料覆盖 / 查询归一化 / 页面理解 / 打分）→
  优先做可复用特征而非特例补丁 → 「让 benchmark 成长，别让 SKILL.md 变成历史错误目录」。
- **落点**：本地 `pdf-problem-search`（现在只有 2.5KB 精简版）与数学书库 RAG（`math-library-search`）。
  - 2026-10-20 追记：那个跨库 RAG 已拆掉（建成后 18 天零次真实检索），改用 skill `bookdex`（书目卡 + 目录索引，`~/.local/share/bookdex/`）。

## 借思想但别整搬

- **结论门 + 有界上下文预算**（`math-coach/references/attempt-graph.md`，7.4KB）：
  用户宣称「证完了」时，只有它是当前分支最新的已验证证明节点**且没有未闭合义务**才接受；未解决/条件性节点
  算未闭合，除非有已验证 resolver 边指向它（fail-closed 递归闭包，浅层 verified 标签不能掩盖未解决依赖）。
  上下文预算：全局摘要 ≤1500 token、活动分支周围 ≤24 节点、最近 5 轮、总包 ≤12000 token，先丢旧轮次、
  永不丢模式/精确问题/当前输入/开放义务 —— 对上本地实测的「长会话推理变差」。
  **别整搬**：它建在 SQLite + 事务 + 闭词汇节点/边之上，Hermes 没有对应存储，借这两条规则就够。
- **术语 registry + 校验脚本**（各子技能的 `terminology.md` + `terminology-registry.json` + `validate_terminology.py`）：
  术语表单独机器可读 + 写入前校验。可用在中法对照（中文 ↔ 法语原名 ↔ 记号）。
- **计算后端「先探测再声明」**（`math-science-computation/references/backend-{inventory,routing}.md`）：
  先探测本机有什么 CAS 再决定路线，不许凭假设说「能做符号计算」。本机无 Mathematica、SageMath 也没装。

## 明确不搬

- 全部 Windows/DSH 运行时与兼容层（`windows-dsh-runtime.md` 50KB、`windows-dsh-compatibility.md` 20KB、
  `windows-dsh-runtime/collector-policy.md` 66KB）。
- 各子技能的 `version-coupling-manifest.json`（10–100KB，他们打包体系的耦合清单）。
- `observer-*`（他们自建的运行观测框架，与 Hermes 日志重复）。
- 重型 python 基建：`registry.py` 102KB / `operations.py` 88KB / `manage_kb.py` 92KB / `appserver.py` 105KB
  + 65KB web UI，以及整个 KB 服务与题库联邦 —— 那是给无状态 agent 加护栏用的；Hermes 已有 skills+memory+vault。
- `agents/openai.yaml`（他们的 agent 配置）。

## 安全检查（顺手做的）

脚本**没有出网遥测**：全文域名只有 `example.com` / `127.0.0.1` / `json-schema.org`，都是本地 CLI 与测试桩；
无硬编码密钥。
