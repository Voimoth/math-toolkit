# 评估开源模型/训练仓库能否本地部署

判断顺序：**取数 → 过三道硬门槛 → 给可搬资产清单 → 报「不建议/建议」**。
本文件给可执行的取数配方与体积参考，判断规则在 SKILL.md 那节。

## 1. 取数：HF 元数据与精确文件大小

本机 `huggingface.co` 被 hosts 指到 127.0.0.1（Watt Toolkit 类加速器的副作用，与 github.com 同因）：
`web_extract` 会回 `Blocked: URL targets a private or internal network address`，`curl` 直连回 502。
**不要去动 hosts（那是加速器的自签证书链，改了别的站一起坏）**，改用镜像站 `hf-mirror.com`，接口与官网同构：

```
curl -sS "https://hf-mirror.com/api/models/<owner>/<repo>"             # 元数据 JSON
curl -sS "https://hf-mirror.com/api/models?search=<词>&limit=50"       # 找同族仓库
curl -sS "https://hf-mirror.com/api/models?search=<词>&filter=gguf"    # 找量化
curl -sSL -o /dev/null -r 0-0 -D - \
  "https://hf-mirror.com/<owner>/<repo>/resolve/main/<file>.gguf" | grep -i content-range
```

最后一条是**不下载就拿到精确大小的办法**：`-r 0-0` 只取首字节，响应头
`Content-Range: bytes 0-0/4683075264` 即总字节数。判断「装不装得下」前先拿这个数，别靠模型名猜。

元数据里必读：`tags` 中的 `base_model:...`（底座）、`downloads` / `likes` / `lastModified`（冷热与维护）、
`siblings`（文件清单）。量化仓常由第三方维护（如 `mradermacher/<repo>-GGUF`、`<repo>-i1-GGUF`），
原仓不一定提供；没量化也不等于不能用，但要在报告里说清来源。

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

## 3. 体积参考（7B 级，用于「装得下吗」）

| 形式 | 体积 | 8 GB 显存 |
| --- | --- | --- |
| bf16 / fp16 | ≈ 15 GB | 不行 |
| Q8_0 | 8.10 GB | 不行（含 KV 超） |
| Q5_K_M | 5.44 GB | 勉强，上下文要压 |
| Q4_K_M | 4.68 GB | 可以，剩约 3 GB 给 KV |

KV 另算：8K 上下文约 1–3 GB。16 GB 系统内存下 CPU offload 会把长中文对话拖到不可用，别把 offload 当解法。

## 4. 结论的默认形态：搬提示词，不搬权重

这类仓库最值得拿的是 `prompt_templates/` 与 reward 设计，纯文本、语言无关、零成本可挂到现有 API 模型上：

- **判分/审核模板**（`judges/*.txt` 一类）：输入对话 → 输出 `{"reasoning":..., "decision":"OK|REJECT"}`。
  适合做**课后自检**：独立复查「这一轮我是在陪练，还是替他把题做掉了」。
- 任何评审型提示词都可以只当**判据**用，不必连它的模型一起搬。
- 模板里的样例与语言限制要一起换：英文数学题样例（分部积分、√3 无理、sin5x/x 极限）直接搬进中文场景会失真；
  英文专训的 judge 明确把「语言混用」列入 REJECT，中文＋法语术语的场景必须删掉该条，否则自检恒判失败。

## 5. 报告口径

五轴简报照旧，模型类额外给：底座、量化体积、本机能否装下（用实测数字）、可搬资产清单、一句明确结论。
**今天实测的（仓库内容、文件大小、显存数字）与凭记忆的旧结论要分开列**，旧结论标来源（记忆/未复测）；
没跑过的效果一律写「未核实」，不要用「应该能」「理论上会更好」填空。
