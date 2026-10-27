# 评估开源模型/训练仓库能否本地部署

判断顺序：**取数 → 过三道硬门槛 → 给可搬资产清单 → 报「不建议/建议」**。
本文件给可执行的取数配方与体积参考，判断规则在 SKILL.md 那节。

## 1. 取数：HF 元数据与精确文件大小

本机 `huggingface.co` 被 hosts 指到 127.0.0.1（Watt Toolkit 类加速器的副作用，与 github.com 同因）：
`web_extract` 会回 `Blocked: URL targets a private or internal network address`，`curl` 直连回 502。
**不要去动 hosts（那是加速器的自签证书链，改了别的站一起坏）**，改用镜像站 `hf-mirror.com`，接口与官网同构：

```
curl -sS "https://hf-mirror.com/api/models/<owner>/<repo>"              # 元数据 JSON
curl -sS "https://hf-mirror.com/api/models?search=<词>&limit=8&sort=downloads&direction=-1"   # 找同族各档位
curl -sS "https://hf-mirror.com/api/models?search=<词>&filter=gguf"     # 找量化
curl -sS "https://hf-mirror.com/api/models/<owner>/<repo>/tree/main"     # 文件清单＋每个文件 bytes
curl -sSL "https://hf-mirror.com/<owner>/<repo>/raw/main/README.md"      # 模型卡原文
curl -sSL "https://hf-mirror.com/<owner>/<repo>/raw/main/config.json"    # 层结构、上下文全是真值
```

**量体积优先用 `tree/main`**：返回的 JSON 里每个条目带 `size`，一次列出全部量化档（Q4_K_M / UD-Q4_K_XL /
IQ4_XS / Q8_0）的精确字节，比逐个文件发 `Content-Range` 探针快一个数量级。只有镜像不返回 size 时
才退回探针法：`curl -sSL -o /dev/null -r 0-0 -D - "…/resolve/main/<file>.gguf" | grep -i content-range`，
响应头 `bytes 0-0/4683075264` 即总字节数。

**摸梯队别只看一个仓库**：`search=<家族名>` 一次就能看出该家族有哪几个档位、谁在榜首（Qwen3.5 的
0.8B/2B/4B/9B/27B/35B-A3B 就是这么一次拿到的）。然后只对拟报的档位取 `config.json` 与 README 里的
上下文长度、`layer_types`、license —— 报告里的「262K 上下文」「32 层里 24 层线性注意力」这类话都要能落到文件上。

元数据里必读：`tags` 中的 `base_model:...`（底座）、`pipeline_tag`（text-generation vs image-text-to-text vs
any-to-any）、`language`（`en` 单一语言就要在报告里点名，中文场景直接判废）、`license`、
`downloads` / `likes`（冷热）、`lastModified`、`siblings`（文件清单）。
量化仓常由第三方维护（`unsloth/…-GGUF`、`bartowski/…-GGUF`、`mradermacher/…-i1-GGUF`），原仓不一定提供；
没量化也不等于不能用，但要在报告里说清来源。

**搜出来的「特化微调」先看底座再谈价值**：`search=Qwen3.5-Math` 之类命中的多是个人 GRPO 小实验
（downloads 三位数），底座还停在上代；这类一句话排掉，别当候选列进简报。

## 2. 仓库侧：整仓一次拉，别逐个文件拉

调研仓库内容别逐个调 contents API（未认证限流约 60 次/小时），下整个分支的 tarball，一次拿全
`prompt_templates/`、`config/`、`src/`：

```
curl -sSL "https://gh-proxy.com/https://github.com/<owner>/<repo>/archive/refs/heads/main.tar.gz" -o r.tar.gz
tar xzf r.tar.gz && ls <repo>-main
```

（实测 668 KB 级仓库秒下；gh-proxy 只代理 raw/archive/release/clone，不代理网页。）
仓库元信息仍走 `api.github.com/repos/<owner>/<repo>`，读 `fork`、`stargazers_count`、`pushed_at`、
`license` —— **`license` 字段为 null 就是仓库里没有 license 文件**（常见，别当成 MIT）。
顺带核一下 README 写的 license 与模型卡标签是否一致，不一致就分别标明出处。

**网页抓取与 API 取数是两回事**：`github.com` 网页、`raw.githubusercontent.com`、`huggingface.co`
在本机都被 hosts 指到 127.0.0.1，但 `curl https://api.github.com/repos/<owner>/<repo>` 实测能返回真实 JSON
（加速器的本地代理会转发）。所以**取数以 curl 为准**，别因为 `web_extract` 报
「private or internal network address」就判定整站不可达、因而放弃查仓库元数据。
**但这依赖加速器开着**：没开时 `api.github.com` 同样不通，此时用 gh-proxy 前缀取
（`https://gh-proxy.com/https://api.github.com/...` 能拿到完整 JSON，含 release 资产名与 size）。
下完资产先 `wc -c` 确认落盘 —— 写 `/tmp` 可能静默失败，日志放 `$HERMES_HOME/cache/scratch/`。

## 3. 体积参考（按参数量，用于「装得下吗」）

Qwen3.5 / Gemma 4 一代的实测 Q4_K_M 大小（`tree/main` 取 size）：

| 档位 | Q4_K_M | 8 GB 显存 |
| --- | --- | --- |
| 2B | 1.28 GB | 宽松，可跑 8K 以上上下文 |
| 4B | 2.74 GB | **舒适档**，剩约 5 GB 给 KV 与其他进程 |
| 9B | 5.68 GB | 能装下但没余量，长上下文溢到内存、掉到个位数 tok/s |
| Gemma 4 E4B（4.5B 有效） | 4.98 GB | 名字像 4B，实测比 9B 轻不了多少（带 embedding/多模态） |
| 12B 级 | ≈ 9.5 GB | 不行 |

旧一代表（7B 级）作对照：bf16 ≈ 15 GB 不行｜Q8_0 8.10 GB 不行｜Q5_K_M 5.44 GB 勉强｜Q4_K_M 4.68 GB 可以。

## 3b. 上下文能开多大：KV 只按 full attention 层算

线性/循环注意力层（Gated DeltaNet 一类）的状态与序列长度无关，只有 `full_attention` 层进 KV cache：

```
每 token KV = n_full × 2 × num_key_value_heads × head_dim × 2 bytes
```

Qwen3.5-4B（32 层中 8 层 full、`full_attention_interval: 4`、kv_heads 4、head_dim 256）= **32 KB/token**：

| 上下文 | KV | 加 2.74 GB 权重后 |
| --- | --- | --- |
| 16K | 0.50 GB | 3.24 GB |
| 32K | 1.00 GB | 3.74 GB |
| 64K | 2.00 GB | 4.74 GB |
| 128K | 4.00 GB | 6.74 GB（塞得进但没余量） |

⇒ 8 GB 卡上 4B 开 64K 很轻松。**别照搬 7B 时代「8K 上下文吃 1–3 GB」的口径**——混血架构的 KV 与线性层无关，
这是它在大显存受限机器上的真实优势。报数前用 `config.json` 的 `layer_types` / `num_key_value_heads` /
`head_dim` 现算，不要估；Ollama 那种带视觉投影的 tag 还要再加投影部分的显存。

## 3c. 后端与安装体积（Linux/Arch）

- **pacman 的 `ollama-cuda` 先算依赖**：包本身 1.03 GB，但依赖系统 `cuda` 包（2.43 GB 下载 / 5.2 GB 安装）。
  为跑一个 2.7 GB 的模型装 5 GB CUDA 全家桶不划算 ⇒ 这条直接排除，报给用户时就报这两个数。
  推荐前一律先 `pacman -Si <pkg>` 看下载/安装大小与依赖，别看包名想当然。
- **Ollama 官方脚本**（`curl -fsSL https://ollama.com/install.sh | sh`）自带 CUDA 运行时，不碰系统 cuda；
  代价是装一个 systemd 服务，装完 disable、改成用到时手动 `ollama serve`（不留常驻进程这条纪律照旧）。
  它的下载体积 HEAD 拿不到（`content-length` 回 0），要精确值就读脚本里的 zst/tgz URL 或装完自己 `du`。
- **llama.cpp 官方构建（解压即用，最轻）**：
  ```
  curl -sL 'https://api.github.com/repos/ggml-org/llama.cpp/releases?per_page=5'
  ```
  **`releases/latest` 现在只回一个 `nightly-tag.txt`、不带二进制** —— 必须按 `releases?per_page=N` 取最近几个
  `bNNNNN` 构建才有资产。实测一个构建：`ubuntu-vulkan-x64` 35.2 MB（免 CUDA）｜
  `ubuntu-cuda-12.8-x64` 182.2 MB + 配套 `cudart-…-cuda-12.8-x64` 594.4 MB｜纯 CPU 22.5 MB。
  新架构（线性注意力一类）在 Vulkan 后端的 kernel 支持要先试再承诺，别拍胸脯说「解压就能跑」。
- **Ollama 库里的档位要探 manifest 才知道真实下载量**：
  ```
  curl -s -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
    https://registry.ollama.ai/v2/library/<model>/manifests/<tag>
  ```
  `/v2/library/<m>/tags/list` 回 404 **不代表**库里没有，按 `manifests/<tag>` 探。返回的 `layers` 逐条带 size：
  实测 `qwen3.5:4b` = model 2649 MB + **projector 676 MB** + 模板/许可证 ≈ 3.32 GB。
  **视觉投影会让同一个 tag 比纯文本 GGUF（2.74 GB）大 0.6 GB，运行时还多占显存**，
  报体积时别只抄 GGUF 数字，说清是哪一种。

## 4. 后训练可行性：显存档位与 LoRA 目标模块

他问「部署完能不能自己后训练调成我要的样子」时用这张表，报数一律标「估算，未实测」。

| 手段 | 8 GB 本机 | 说明 |
| --- | --- | --- |
| QLoRA(4bit) 2B | 宽松 | seq 4k、batch 2 |
| QLoRA 4B | 可行，即上限 | seq 2–4k、batch 1 + 梯度检查点 |
| QLoRA 9B | 不行 | 社区口径单卡 24 GB 才舒服，最小 12–16 GB |
| GRPO / RL | 任何档位都不行 | 要 policy + reference 双份权重，再叠 rollout |

**混血架构的 target_modules 必须显式列全**（以 Qwen3.5 为例，`config.json` 的 `layer_types` 给出
32 层里 24 层 `linear_attention` + 8 层 `full_attention`，`full_attention_interval: 4`）：

```yaml
lora_target_modules:
  - q_proj / k_proj / v_proj / o_proj
  - linear_attn.in_proj_qkv
  - linear_attn.in_proj_z
  - linear_attn.out_proj
```

只写 q/k/v/o_proj 就只训到四分之一层。训练侧还要 flash-linear-attention（FLA）类依赖做 kernel，
Unsloth 首次跑会先编译 Gated DeltaNet kernel（首轮慢属正常，不是卡死）。

**训完回部署三步**：`merge_and_unload`（在 16bit 底座上合并）→ `convert_hf_to_gguf` → 再量化，
才能进 llama.cpp / Ollama。adapter 本体几十 MB，llama.cpp 直接吃不了。

**数据成本才是主项**：改行为要 500–2000 条样本，来源只能是强模型按本地 skill 生成 + 人工筛，
本质是把强模型的文体蒸馏进小模型，天花板仍是它的底座。所以先跑零成本闸门（20 个真问题 + 严格
system prompt + few-shot），错在格式/啰嗦才值得训，错在内容/推理就别训。

## 5. 结论的默认形态：搬提示词，不搬权重

这类仓库最值得拿的是 `prompt_templates/` 与 reward 设计，纯文本、语言无关、零成本可挂到现有 API 模型上：

- **判分/审核模板**（`judges/*.txt` 一类）：输入对话 → 输出 `{"reasoning":..., "decision":"OK|REJECT"}`。
  适合做**课后自检**：独立复查「这一轮我是在陪练，还是替他把题做掉了」。
- 任何评审型提示词都可以只当**判据**用，不必连它的模型一起搬。
- 模板里的样例与语言限制要一起换：英文数学题样例（分部积分、√3 无理、sin5x/x 极限）直接搬进中文场景会失真；
  英文专训的 judge 明确把「语言混用」列入 REJECT，中文＋法语术语的场景必须删掉该条，否则自检恒判失败。

## 6. 报告口径

五轴简报照旧，模型类额外给：底座、量化体积、本机能否装下（用实测数字）、可搬资产清单、一句明确结论。
**今天实测的（仓库内容、文件大小、显存数字）与凭记忆的旧结论要分开列**，旧结论标来源（记忆/未复测）；
没跑过的效果一律写「未核实」，不要用「应该能」「理论上会更好」填空。

**排名类数字要标评测口径**：官方模型卡的 HMMT / GPQA-D / PolyMATH 是短答案竞赛题，答对率高不代表
能带你走 Arnold 级证明；写进简报时要加一句「这是短答案题，考的是长链一致性之外的东西」。
同时把他已有的先验摆出来（「本地 7B 数学太弱」已实测过），换代只从一个档位挪到隔壁档位，别暗示翻盘。

**内容农场不可信**：搜「best small model 8GB」前排多是 SEO 站（modelfit / promptquorum / localaimaster /
tinyweights 一类），数字互相抄且常与官方卡不符。**排名只引官方模型卡或论文，体积只引 `tree/main` 的 size**，
两者都拿不到时宁可写「未核实」。
