# DeepTutor 档案（评估结论，尚未在本机安装）

## 它是什么／不是什么

- **不是模型**，是**工作台**：自己不带「脑子」，LLM 用你配的（所以能直接接现有的 DeepSeek，不必另买订阅）。
  纠正这一条很重要——用户提问时说的「这个模型是开源的」是误解，它决定了他对「智能程度」的预期怎么画。
- 港大 HKUDS 实验室出品，**Apache-2.0**，star 量级 16K。同实验室还有 LightRAG / nanobot / AutoAgent。
- 定位：装在本地、数据在自己机器上的 AI 家教工作台（后端 + Web 前端 + CLI）。

## 插件与技能模型（很值得评估的一点）

- **两层插件模型：Tools（RAG / 网页 / 代码执行 / 推理 / 论文检索 / 记笔记…）+ Capabilities
  （解题 / 出题 / 研究 / 可视化），可自由组合。**
- **Skills：写 SKILL.md 定义教学人格**，激活时注入 system prompt ——
  **和 Hermes 的 skill 机制几乎同构**，所以他那套「因果链教学法／引导式陪练／不代劳」的约定可以搬过去复用。
- **TutorBot**：每个 bot 有独立 workspace / memory / personality / skills，并能自主设提醒（Heartbeat）。
- CLI 能跑大量外部 app；较新版本还有 per-account 的 MCP Services store。

## 依赖与安装路径

- 命令行：`pip install -U deeptutor && deeptutor init && deeptutor start`（PyPI 有 CLI，克隆非必需）。
  也有源码安装与 Docker 两条路。
- **Python 3.11–3.13**（比本机系统 Python 旧）、**Node.js 20+ / 22 LTS**（本机 node 偏新，大概率可用）。
  装了 CLI-only 就不起 Next.js 前端，更省内存。
- 默认前端 `http://127.0.0.1:3782`，后端端口默认 8001。
- **必填**：LLM（可用现有 DeepSeek key）＋ **Embedding**（知识库/RAG 要它；用户 `.env` 里已有 GLM key，
  智谱有 embedding API，可直接用）。
- ⚠ **以上安装步骤来自官方文档与第三方评测，本机尚未实装，不要当成已验证流程。**

## 与 Hermes 的分工（这是推荐形态，不是二选一）

| DeepTutor 有、Hermes 没有 | Hermes 有、DeepTutor 没有 |
|---|---|
| 教科书 PDF 的 **RAG 检索** | **长期记忆**（用户画像、学习史） |
| **自动出题 + 题库** | **wiki 铁律 + Obsidian vault 维护** |
| **Manim 数学动画** | **因果链教学法、卡点沉淀、作业题地图** |
| **多 agent 解题 + 验证流水线** | **终端/文件/git/网络工具链** |

桥的做法：Hermes 调它的 CLI、拿 JSON 结果，再按 wiki 铁律落盘到 `/mnt/e/notes`。
两套 memory 各自独立、互不污染，但**也不会自动同步**，桥要自己搭。

## 已知风险（转述官方与评测，未自验）

- **迭代极快**（半年几十个版本，release notes 常年每周修上一批的漏）→
  重要场景要**钉住一个稳的版本**，别天天升级。
- 成熟度不均是评测者的一致评价（动画模块尤其）；文档相对滞后。
- 它的「让模型写代码再执行」在单机默认配置下沙箱只是缓冲、不是保票；多人部署应走容器或关掉。

## 替代品对照（都不如它贴合「教」这个字）

- **NotebookLM** —— 闭源、不能本地。
- **AnythingLLM** —— MIT，但只是纯 RAG，没有教学结构（如果他其实只想要「教科书问答」，这个更轻）。
- **Open WebUI** —— 界面好，同样没有教学结构。
