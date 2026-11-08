# WebDev 头图 benchmark 选型

抓取日期：2026-11-08　·　模型池 10 个席位（Gemini 4 Carbon 作为附加）

---

## 1 推荐

### 1.1 选这两个

1. **Code Arena · WebDev**（arena.ai，人类盲测偏好）
   - 覆盖：10/10 + Carbon（Seed 只有 `Seed2.1 Pro Preview`）
   - 可比性：同一个 Bradley-Terry 榜、同一天快照（2026-11-06）、同一类别 `webdev`
   - 声望：厂商发布时引用最多（OpenAI / Google / Kimi / Seed 的模型卡都引用它）
   - 指标：Arena Score（Bradley-Terry 分，量纲与 Elo 相同，但不是严格的 Elo）
   - 坐标轴：**1400 → 1850**
     - 模型池分数在 1484–1814 之间，零基线会把差距压平
     - 非零基线必须在图上标明，建议加 ±95% CI 误差线

2. **Vibe Code Bench v1.1**（Vals.ai，从零搭 Web App + 自动化点击测试）
   - 覆盖：9/10 + Carbon（缺 Seed2.1 Pro）
   - 可比性：同一个 OpenHands harness、同一套测试集、同一天更新（2026-11-05）
   - 互补：Arena 测"人更喜欢谁"，Vibe Code 测"能不能真跑通"
   - 指标：Accuracy（%）
   - 坐标轴：**0 → 100**（模型池分数在 47.6–91.9 之间）

### 1.2 落选原因（一句话）

- SWE-bench Multimodal：覆盖 8/10，但测的是修前端 bug，不是生成
- Arena Image-to-WebDev：缺两款 Gemini 4、Kimi K3.1、GLM-5.3、DeepSeek V4.1 1017
- Vision2Web / ArtifactsBench / Design2Code：同一张表覆盖 ≤ 1 个模型

### 1.3 画图注意

- **版本规则**：同一模型有多个版本时，两张图统一取最新快照
  - Qwen3.8-Max → `0902`
  - DeepSeek → `V4.1-Flash-20261017`（目前没有 V4.1 Pro）
  - GLM → `GLM-5.3`（不用 Flash）
  - Kimi → `K3.1 Pro`（K3 写在备注里）
- **统计上打平的组**（Arena 分差小于 CI）
  - GPT-6 Astra 1769.8±8.8 ≈ Gemini 4 Carbon 1767.2±14.9
  - Kimi K3.1 Pro 1683.9 ≈ Gemini 4 Argon 1682.7 ≈ Qwen3.8-Max 1677.1
- **Vibe Code 头部很挤**：前 6 名都在 89.6–91.9 之间，差距不到 2.5 个百分点
- **`output/webdev.html` 里的 Arena 旧值要更新**
  - GPT-6 Astra 1793（1st）→ 现在是 1769.8（3rd）
  - Kimi K3 1678（厂商引用的 07-23 快照）→ 现在是 1656.5
  - Seed2.1 Pro 1539（8th，模型卡引用）→ 现在是 Preview 1518.7（59th）

---

## 2 数据表

### 2.1 Code Arena · WebDev（Arena Score）

- 快照：`leaderboard_publish_date = 2026-11-06`，共 153 个模型，类别 `webdev`
- 数据来源：arena.ai 页面被 Cloudflare 拦截（403），数值取自 lmarena-ai 官方 HF 数据集 `webdev/latest`
- `overall` 和 `webdev` 两个类别下，模型池的分数完全一致

| 模型 | 分数 | 设置/备注 | 来源 URL | 抓取日期 |
|---|---|---|---|---|
| Claude Opus 5.5 | 1814.3 | `(Max)` · 排名 1/153 · ±11.9 · 4,132 票 | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset （展示页 https://arena.ai/leaderboard/code/webdev ） | 2026-11-08 |
| Claude Fable 5.1 | 1745.7 | `(Max)` · 排名 5 · ±8.1 · 9,764 票 | 同上 | 2026-11-08 |
| GPT-6 Astra | 1769.8 | `(Max)` · 排名 3 · ±8.8 · 8,364 票 | 同上 | 2026-11-08 |
| Gemini 4 Argon | 1682.7 | `(High)` · 排名 11 · ±10.0 · 4,702 票 | 同上 | 2026-11-08 |
| Gemini 4 Carbon（附加） | 1767.2 | `(High)` · 排名 4 · ±14.9 · 2,240 票（10-28 才上榜，票数少） | 同上 | 2026-11-08 |
| Kimi K3.1 Pro | 1683.9 | `(Max)` · 排名 10 · ±10.0 · 4,595 票；Kimi K3 (Max) 1656.5，排名 18 | 同上 | 2026-11-08 |
| GLM-5.3 | 1620.7 | `(Max)` · 排名 28 · ±6.9 · 12,658 票；GLM-5.3-Flash 1606.6 | 同上 | 2026-11-08 |
| Qwen3.8-Max | 1677.1 | `(0902)` · 排名 13 · ±6.3 · 22,197 票；无后缀版 1671.4，排名 15 | 同上 | 2026-11-08 |
| Seed2.1 Pro | 1518.7 | **仅收录 `Seed2.1 Pro Preview`** · 排名 59 · ±5.6 · 17,773 票；历史快照里从未出现正式版 | 同上 | 2026-11-08 |
| DeepSeek V4.1 | 1665.1 | `V4.1-Flash-20261017 (Max)` · 排名 16 · ±6.8 · 13,670 票 | 同上 | 2026-11-08 |
| MiniMax-M3 | 1484.1 | 排名 70 · ±5.4 · 21,776 票；M3.1-Flash 1582.0，排名 39 | 同上 | 2026-11-08 |

### 2.2 Vibe Code Bench v1.1（Accuracy %）

- 版本 v1.1，Vals 页面标注更新于 2026-11-05，共 125 条记录
- 所有模型统一用 OpenHands harness
- 数值取自页面主榜表格；页面另有一张按 effort 分档的图，数值不同，不要混用

| 模型 | 分数 | 设置/备注 | 来源 URL | 抓取日期 |
|---|---|---|---|---|
| Claude Opus 5.5 | 90.29% | OpenHands · 排名 5/125 · $35.77/题 | https://www.vals.ai/benchmarks/vibe-code | 2026-11-08 |
| Claude Fable 5.1 | 90.26% | OpenHands · 排名 6 · $33.37/题 | 同上 | 2026-11-08 |
| GPT-6 Astra | 89.59% | OpenHands · 排名 7 · $38.51/题 | 同上 | 2026-11-08 |
| Gemini 4 Argon | 91.91% | OpenHands · 排名 2 · $8.11/题 | 同上 | 2026-11-08 |
| Gemini 4 Carbon（附加） | 89.06% | OpenHands · 排名 8 · $8.25/题 | 同上 | 2026-11-08 |
| Kimi K3.1 Pro | 84.89% | OpenHands · 排名 18；Kimi K3 84.97%，排名 17 | 同上 | 2026-11-08 |
| GLM-5.3 | 78.13% | `GLM 5.3` · OpenHands · 排名 36；GLM 5.3 Flash 30.76% | 同上 | 2026-11-08 |
| Qwen3.8-Max | 77.14% | `Qwen 3.8 Max 0902` · 排名 39；无后缀版 64.70%，排名 56 | 同上 | 2026-11-08 |
| Seed2.1 Pro | 未收录 | 全榜没有任何 Seed 条目 | 同上 | 2026-11-08 |
| DeepSeek V4.1 | 87.73% | `DeepSeek V4.1 Flash 1017` · 排名 12；V4.1 Flash 84.74%，V4 Pro 0813 82.30% | 同上 | 2026-11-08 |
| MiniMax-M3 | 47.57% | OpenHands · 排名 73；M3.1-Flash 73.94%，排名 45 | 同上 | 2026-11-08 |

---

## 3 其他候选

| 候选 | 覆盖（/10） | 有分的模型 | 没选的原因 |
|---|---|---|---|
| Arena · Image-to-WebDev | 7（另有 2 个变体） | Opus 5.5 1747.7、Fable 5.1 1724.9、Astra 1718.2、Qwen3.8-Max(0902) 1636.2、Kimi K3 1583.8、Seed2.1 Pro Preview 1505.3、MiniMax-M3 1472.5；变体：DeepSeek V4.1-Flash-0910 1607.4、GLM-5.3-Flash 1581.4 | 两款 Gemini 4、K3.1 Pro 都没有；票数少，CI 宽到 ±19 |
| SWE-bench Multimodal（Vals，11-05） | 8 | Opus 5.5 70.21、Fable 5.1 61.25、Argon 56.04、DeepSeek V4.1 Flash 46.46、Kimi K3 44.17、Astra 43.33、Qwen 3.8 Max 42.50、MiniMax-M3 33.33 | 测的是 JS 仓库修 issue，不是生成；缺 GLM、Seed |
| Vision2Web（官方榜 S4-2026，10-01） | 1（另有 1 个变体） | Kimi K3 79.0；变体 GLM-5.3-Flash 77.8 | 同一赛季几乎没有新模型；MiniMax-M3 59.0 在 S3、Qwen3.8-Max 69.0 是厂商自报，都不可比 |
| ArtifactsBench（官方榜） | 0 | — | 榜单停在 2025 年（最新是 GPT-5、Claude Opus 4.1、MiniMax-M2）；Seed2.0 Pro 66.6 只出现在论文里 |
| Design2Code | 0 | — | 只有 GLM-5V-Turbo 自报 94.8，没有统一的榜 |
| 厂商自建（Kimi Webdev / QwenReact / Trae Web / VIBE-V2 / CC-Frontend） | 各 1 | 各家只报自己 | 协议各不相同，不能横向比 |

---

## 4 来源

- Code Arena WebDev
  - 展示页：https://arena.ai/leaderboard/code/webdev
  - 官方数据集：https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset （`webdev/latest`、`webdev/full`，publish 2026-11-06）
  - 变更日志：https://arena.ai/company/leaderboard-changelog/
- Vibe Code Bench v1.1：https://www.vals.ai/benchmarks/vibe-code
- SWE-bench Multimodal（Vals）：https://www.vals.ai/benchmarks/swebench-multimodal
- Vision2Web
  - 榜单：https://vision2web-bench.github.io （数据 `data/leaderboard.json`）
  - 提交仓库：https://huggingface.co/datasets/zai-org/Vision2Web-Leaderboard
- ArtifactsBench：https://artifactsbenchmark.github.io/leaderboard.html
- 已有收集（只作对照）：`/mmu_mllm_hdd_4/deep-research/final-visual-code-blog/output/webdev.html` 中的「1 Lab Reports」表

