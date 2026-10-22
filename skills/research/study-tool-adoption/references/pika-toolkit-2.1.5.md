# pika 数学学习工具包 2.1.5（外部分享包）研判与已搬项

位置：`/mnt/e/pika_math_learning_toolkit-2.1.5/`（442 文件 / 7.1 MB；`payload/` 占 6.9 MB）。2026-10-07 全面检查。

## 它是什么

- `pika_math_learning_toolkit-2.1.5`：**portable-skill-suite**（`package-manifest.json` schema v3）：把六个
  **Codex/DSH 向的英文技能**打包，配一个事务式安装器（`install.py` 27 KB，exit code 10/11/21/31/40/50/51/52）、
  checksums、`SOURCE_VERSIONS.json`、`PORTABLE_ADAPTATIONS.json`、`TEST_MATRIX.md`、`INSTALL_TEST_RECEIPT.json`（四平台全 passed）。
- 六个 payload：`manage-personal-knowledge` v1.11.5（主）、`obsidian-vault-notes` v1.13.5、`pdf-problem-search` v1.12.3、
  `math-science-computation` v1.11.4、`math-coach` v1.13.0、`math-research-solve` v3.2.1。
- 形态：每个技能 = SKILL.md + `references/` + 大量 python CLI（registry.py 102 KB、operations.py 88 KB、
  manage_kb.py 92 KB、appserver.py 105 KB）+ 单元测试 + `terminology-registry.json` + `version-coupling-manifest.json`。

## 不要做的事

- **不要跑 `install.sh` / `install.py`**：它会把六个同名技能装进 agent 的 skills 目录，与我们自己那套中文技能
  （`math-coach`、`pdf-problem-search` 等）同名冲突；它问的「知识库根目录」也和本机 `/mnt/e` 布局不同。
  本机只需要**从 payload 里挑内容**（下面）。
- 它的 `payload/` 是只读快照，别在里面改东西（checksums 会失效，也破坏了以后的对照）。

## 已搬走的东西（2026-10-07，全部改写成中文/本机工具链版）

| 来源 | 落地处 |
|---|---|
| `obsidian-vault-notes/references/natural-chinese-lint.json`（24 短语 + 20 正则） | `wiki-writing-conventions` 的 `scripts/lint_natural_chinese.py`（十类、可跑）+ `references/natural-chinese-lint.md`（规则表与用法） |
| `obsidian-vault-notes/references/editing-protocol.md`、`large-edit-verification.md` | `wiki-writing-conventions/references/large-edit-gate.md`（候选出库 → 独立子代理评审 → 落盘 → 复核） |
| `obsidian-vault-notes/references/math-note-style.md` | 同上文件 §5（证明状态标签、正式 callout 不放状态行、三种来源分清）+ §3（TeX 控制词 shadow） |
| `pdf-problem-search/references/query-normalization.md` + SKILL.md 的 Verification Rules / Common Failure Modes | `pdf-problem-search/SKILL.md` 新增三节（查询归一化、验证规则、空结果话术、失败冻结回归） |
| `pdf-problem-search/references/improvement-strategy.md` | 同上（失败分层 + 优先可复用特征） |
| `manage-personal-knowledge/references/search-evaluation-contract.md` | `math-library-search/SKILL.md` 新增「结果契约与置信度」节（该技能 2026-10-20 已删，内容随 RAG 一起弃用） |
| `math-coach/references/attempt-graph.md` | 只搬思想（结论门 + 未闭合义务 fail-closed + 有界上下文预算），未引入其 SQLite 图存储 |

## 判定不值得搬的（与理由）

- **Windows/DSH 运行时**：`math-coach/references/windows-dsh-runtime.md` 50 KB、`windows-dsh-compatibility.md` 20 KB、
  `scripts/windows-dsh-runtime/collector-policy.md` 66 KB —— 与 Linux/Hermes 无关。
- **`version-coupling-manifest.json`**（各技能 10–100 KB）、`observer-*`（他们的运行观测框架）：与 Hermes 日志/skill 体系重复。
- **重型 python 基建**（KB 服务、题库联邦、appserver + 65 KB web UI）：那是给无状态 agent 加护栏用的；
  Hermes 已有 skills + memory + vault，再造一套只增加维护面。
- `agents/openai.yaml`（他们的 agent 配置）。
- `math-science-computation` 的 Wolfram MCP 策略：本机没有 Mathematica；只借「先探测后端再声明能做计算」的纪律。

## 复查入口（下次再有人问这个包）

- 包的定位与安装边界：`START_HERE.md`、`AGENT_INSTALL.md`、`package-manifest.json`（依赖图：
  manage-personal-knowledge → obsidian-vault-notes + pdf-problem-search；math-research-solve → math-science-computation + obsidian-vault-notes）。
- 安全（已核）：脚本无出网遥测，全文域名只有 `example.com` / `127.0.0.1` / `json-schema.org`，无硬编码密钥。
- 六技能版本与哈希：`SOURCE_VERSIONS.json`；安装测试结论：`INSTALL_TEST_RECEIPT.json`。
