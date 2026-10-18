# 尝试图 + 结论门（本地实现说明）

来源：外部包 `pika_math_learning_toolkit-2.1.5` 的 `payload/math-coach/references/attempt-graph.md`。
本实现在 `scripts/attempt_graph.py`（SQLite，标准库，无第三方依赖；测试 `scripts/tests/test_attempt_graph.py`，19 条全过）。

## 它治什么

你说「证完了」时，我可能直接说「好」——但推理链中间可能存在：未证的假设、到不了命题的断链、
或者前面被指出过的错还没清。结论门把这些变成机械判据：
**从 `checkpoint` 出发，沿活跃依赖边能不能走到 `problem`，沿途每个点是否都已核、且没有未闭合义务**。
浅层打上 verified **不能**掩盖上游 unresolved —— 闭包是 fail-closed 的。

## 什么时候用（不要每轮都建）

- 他在做**证明题**（模式 B）且**声称完成/提交结论**时：建一次会话，登记关键步骤，跑门。
- 被指出错误、或他说「重新来」时：用 `reject` 留下修复障碍，然后从起点重建（不要在被怀疑的路径上续写）。
- 纯概念讨论、计算题、讲课（模式 A）**不用**——那些没有「结论闭包」这回事。
- 会话名建议 `题目关键词-日期`；一个题目一个会话，不要跨题混用（分支会乱）。

## CLI

```
DB=~/.local/share/math-attempt-graph/graph.db          # 默认值，可用 --db 覆盖
AG="python3 <技能目录>/scripts/attempt_graph.py"
$AG --db $DB init  --session S --problem "证明：…" [--mode GUIDED|STRICT|HARD_LOCK]
$AG --db $DB patch --session S --json '<补丁 JSON>'
$AG --db $DB gate  --session S [--node N]              # 不给 --node 就用最新 checkpoint
$AG --db $DB reject --session S --node N --reason '…'  # 拒绝一个结论 => 建修复障碍
$AG --db $DB obligations --session S
$AG --db $DB context --session S --input '他这一轮说的话' [--old-branch ID] [--turns-file f.json]
$AG --db $DB assess  --session S --verdict VALID_SO_FAR --note '…'
$AG --db $DB show    --session S
```

**补丁 JSON 的键**：`nodes`（`kind/status/origin/label/tmp/meta`）、`edges`（`src/dst/kind`）、
`branches`、`memberships`（`node/branch`）、`updates`（`node/status/note`）、
`corrections`（`edge/reason/replacement`）、`merges`（`candidate_edge/branch/user_confirmed`）。

**引用结点的三种写法**：本补丁内的 `tmp` 名 / 已有数字 id / **唯一标签**（标签不唯一就报错，不猜）。
> 跨调用推荐用唯一标签——LLM 记不住数字 id；用完「补丁返回的 tmp_ids」也行。

结点/边/分支必须在**同一个补丁**里带上 membership（存储要求每个非 problem 结点至少属于一个分支）；
任何一条校验不过 ⇒ **整个补丁回滚**，不留半成品。

## 结论门的判定条件（照抄原 contract）

1. 是一个 `checkpoint` 结点；
2. `origin = user`（只有他本人能声明闭合）；
3. 状态 `verified`；
4. 是**该分支上最新的**学习者证明结点（否则要重新声明）；
5. 有**实质性前驱**（不能从 problem 直接跳到结论）；
6. 沿活跃的 dependency/resolution 边**能到达 problem**；
7. 这条链上每个点都已经闭合（fail-closed 递归；成环 ⇒ 永远算未闭合）；
8. 该分支**无未闭合义务**（`unresolved` / `conditional` 且没有被「已验证、且自身依赖也闭合的解析器」清掉）。

被拒的结论会生成一个 session 级修复障碍（`obstacle/origin=coach`），**下一个主张不继承失败路径**；
这个障碍只能由**教练侧**的受控解析器清掉，学习者自说自话不算清除。

## 哪些是照抄、哪些是我自己定的（重要）

照抄：结点/状态/origin/边/分支的闭词汇；依赖闭包用哪些边；未闭合义务的定义与 fail-closed 递归；
「最新用户证明结点」「实质性前驱」「成环算未闭合」；拒绝后续结口与修复障碍；只追加历史（修正=旧边标 inactive + 追加替代边 + 记事件）；
合并需用户显式确认且必须指向 `possibly_equivalent_to` 候选边；有界上下文预算（活动分支周围 ≤24 结点、旧分支 ≤12、
总包 ≤12000 token、先丢旧轮次/旧分支细节、**永不丢** mode/problem/current input/open obligations、分支摘要 ≤1500）。

我定的（原 contract 未给或未明写）：

- **模式映射**：GUIDED/STRICT/HARD_LOCK 下教练都只能建 `obstacle/question/checkpoint`（对应本地「不得命名新对象/方法/方向」）；
  工具 origin 只能建 `operation/result`。
- **状态迁移表**：proposed→{verified,refuted,unresolved,conditional}；conditional→{verified,refuted,unresolved}；
  unresolved→{verified,refuted,conditional}；verified→{refuted}；refuted 是终态（要重新验必须新建结点）。
- **实质性前驱的集合**（claim/operation/result/subgoal/strategy/insight/goal）。
- **token 估算**用 `len(json)/4`；上下文不接对话历史（`recent_turns` 由调用方用 `--turns-file` 传入）。
- `assess` 的 MATHEMATICALLY_BLOCKED 需要一条 meta 里 `scoped`/`excludes_all` 为真的障碍——单个被反驳结点不够。

未做（也不需要）：他们的 appserver、前端、多角色（学生/裁判）合成、共享内存、跨机。

## 实测记录（2026-10-07）

- 单测 19 条全过（`python3 scripts/tests/test_attempt_graph.py`）：闭词汇、引用回滚、成环拒绝、分支归属、
  教练权限、浅层 verified 不掩盖上游、解析器清义务、重新声明闭合、实质性前驱、拒绝后阻挡、只追加修正、
  状态迁移与事件、合并需确认、上下文预算不超且不丢必需项、完成度标签。
- CLI 端到端（144 阶群那题）：提交 5 结点 → 门拦住（指出 `假设各 3-子群两两交平凡` 是 conditional）
  → 补证并挂解析器 → 重新声明闭合 → `pass=True`、未闭合义务 0。
- 真实的坑（已修）：依赖边方向（`edge.src` 依赖 `edge.dst`）；`branches` 没有 `active` 列；相对路径下 `makedirs('')`；
  结点与 membership 必须同补丁；跨调用临时名失效（改为支持唯一标签）。

## 维护与清理

- 库在 `~/.local/share/math-attempt-graph/graph.db`（WAL 模式，附带 `-wal`/`-shm`）；不要放进 vault。
- 不想留数据：直接删 `graph.db*`；想保留历史就整个目录留着（每会话一份记录，可当审计）。
- 改了脚本后必须重跑单测；新增规则先加测试再改代码。
