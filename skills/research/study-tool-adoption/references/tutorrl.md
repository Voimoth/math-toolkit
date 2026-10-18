# tutor-rl（ETH 教学型 RL）档案

案例：2026-10-07 用户问「能不能本地部署这个模型来优化 math-coach 的效果」。
结论：**不部署权重，只搬两份判分模板**（已落进 `math-coach` 的「陪练后的自检:双裁判」）。

## 硬数据（2026-10-07 实测）

- 仓库 `sidney-tio/tutor-rl`：**fork**（上游是 ETH NLPeople 的 tutor-rl），2 stars / 0 fork / open_issues 0，
  最后 push 2025-11-18，`license` 字段 null（仓库里无 license 文件）
  —— 上游 README 写 CC-BY-4.0，而 HF 权重卡 tag 是 apache-2.0，两处不一致，引用时分别标出处。
- 内容形态：**训练配方**（多轮 GRPO，`src/classroom.py` 状态机 START→TEACHER→STUDENT→…→JUDGE→
  GENERATE_SOLUTION→REWARD），不是可直接用的家教产品。
- 产物权重 `eth-nlped/TutorRL-7B` / `-think`：底座 `Qwen/Qwen2.5-7B-Instruct`，
  downloads 664 / 54，lastModified 2025-05-27。
- 论文 arXiv:2505.15607（EMNLP 2025），核心 claim：7B 无人工标注，教学表现接近 LearnLM；
  对 reasoning benchmark（GSM8K/MATH500）的措辞是 **maintain**（维持，不是提升）。
- 第三方量化（原仓不提供）：`mradermacher/TutorRL-7B-GGUF`（565 downloads）、`-i1-GGUF`、`-think-GGUF` 系列。
  实测精确体积：Q4_K_M = 4 683 075 264 B（4.68 GB）、Q5_K_M = 5 444 832 960 B、Q8_0 = 8 098 526 912 B。

## 本机可行性（一次算清）

- 训练：`config/train_rl/7b.yaml` 里 teacher 7B / student Llama-3.1-8B-FP8 / judge Qwen2.5-14B-AWQ
  **各占 4 张 GPU**（`number_of_gpus_per_instance: 4`，`gpu_memory_utilization: 0.325`）
  ⇒ 参考实现约 12 张 80G 级卡。8 GB 显存 + 16 GB 内存：**零可能**，不给模糊话。
- 推理：本机 RTX 4060 Laptop 8188 MiB，Q4_K_M 4.68 GB 装得下、剩约 3 GB 给 KV，8K 上下文勉强。
  但底座就是 Qwen2.5-7B-Instruct，**RL 只改教学行为不改数学能力**，且英文专训
  ⇒ 对代数III / 理论力学这个层级无价值（用户此前已实测「本地 7B 数学太弱」并卸掉）。

## 可搬资产一：两份 judge 模板（原文，用时可改中文样例）

`prompt_templates/judges/does_not_leak_answer.txt`（判「是否过早给答案」）要求：

- 教师应当：用提问/提示/反馈互动式引导；鼓励学生自己推理；
  **不得过早解掉主要部分或抛出大块最终解答**；可以确认正确推理、纠错、逐步澄清概念、学生不懂时讲细。
- **不可接受**：开场就给完整答案；一条消息里揭示全部关键步骤而无学生参与；
  走完整个解法却无有意义的互动。
- 样例：好（分部积分 ∫x·e^(2x) 的追问链）／坏（√3 无理的完整证明一次抛出）、
  坏（lim sin5x/x 直接 \boxed{5}）、好（De Morgan 律的追问链）。
- 输出 schema：{"reasoning": "…", "decision": "OK or REJECT"}。

`prompt_templates/judges/follows_pedagogical_values.txt`（判风格）要求：

- 可接受：消息简洁易懂；耐心尊重；**大部分话由学生说**（*Most of the talking is done by the student*），
  教师只回应或简短澄清；对话自然可信。
- REJECT 条件：**消息过长**（几句话够却写成多段）；**教师主导对话**；
  **语言混杂**（原文限定「必须全英文」——中文＋法语术语场景必须删掉该条，否则恒判失败）；
  不真实/不自然的互动；不完整或空消息。
- 输出 schema 同上。

## 可搬资产二：teacher system prompt 里的一条（已落进 math-coach A19）

原文要点：*You must not reveal the answer … Even if the student is already able to solve the problem,
 you should help them understand and improve the solution so that they get as high of a grade as possible.*
另有可选的 `<think>` 隐藏规划（先想好给哪个提示、不输出），与本机「先想清楚再问、别乱引话题」同类。

## 没有搬的部分及理由

- **合成学生 persona**（`initial_attempt_wrapper_prompt` / `student_final_prompt` 等）——
  它是为了在没有真实学生时造训练数据（「你最后会被评分，所以配合老师」），真实辅导用不上。
- **GRPO / reward 权重**（`generation.ignore_rejected_judge`、`generation.extra_penalty_for_rejected_judges`，
  λ 与 Pareto 前沿）—— 属于训练侧；它的等价物在本地就是「把判据写进 skill 当自检」，不需要梯度。
- 权重本身：见上「本机可行性」。
