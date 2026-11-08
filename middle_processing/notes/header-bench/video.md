# VibeVideoBench：头图柱状图取数

> 抓取日期 2026-11-08。数据来自 arXiv v2（2026-10-27）的 Table 2 / E.1 / C.1 / E.3，并和项目页内嵌数据逐行核对过。

## 1 推荐

- **指标**：L3 Overall，计分规则为 **No video = 0**，取三个评委组的均值
  - 论文把它叫作 headline score（Tab. 2 右栏、Tab. E.1、E.3、F.1、G.1）
  - 用它是因为它对整条链路都计分：没交出视频的任务记 0 分，留在均值里
- **坐标轴**：0 – 5
  - L3 五个维度各打 1–5 分，Overall 取这五个分的平均；没交视频的任务记 0 分
  - 实测分数在 2.790 到 4.109 之间。柱状图从 0 画到 5，不要截断坐标轴
- **来源**：https://arxiv.org/html/2610.35864v2#S4.T2 （Table 2，最右一列）
- **备选**（想用 0–100 的轴时）：L2 strict (%)
  - 含义：一个任务里没有任何 core check 失败、且至少一条通过，才算成功；没交视频算失败
  - 区分度更大，从 26.6 到 76.3。用这个指标时 Opus 第一（76.3），Astra 第二（74.5）
- **作图时要注意**
  - Astra 和 Opus 只差 0.035，配对 bootstrap 下 P(Astra > Opus) = 0.911，不算决定性领先
  - DeepSeek 对 Sonnet 是 P = 0.697，Gemini 3.8 Flash 对 GLM 是 P = 0.498，基本打平
  - 想画误差条可以用 Tab. E.3 的 95% CI（见第 3 节）

## 2 指标怎么算

- **L1 Program**：只用程序判定，不用模型
  - Delivered：一小时内交出能解码、能评分的 MP4
  - Spec (%)：这个任务的所有程序检查都通过（分辨率、帧率、时长、音轨等）；没交视频算全部不通过
- **L2 Rubric**：每个任务平均约 54 条二值检查，全部 239 个任务共 12,985 条
  - Pass = pass / (pass + fail)，unknown 和 n/a 不计入
  - Strict = 按任务判定，没有 core check 失败、且至少一条通过
- **L3 Quality**：五个维度，各打 1–5 分，每档都有锚点（1 / 3 / 5）
  - VQ 画质与可读性 · VA 视觉美感 · CL 内容组织与逻辑 · TM 运动与节奏 · AQ 音质与音画同步
  - Overall = 五个维度的平均分，不是 L1–L3 的加权总分
- **两种计分规则**
  - Delivered only：只对交出视频的任务取平均。项目页表格默认显示这一种
  - No video = 0：没交视频的任务各维度都记 0 并留在均值里。论文的 headline 用这一种
- **三个评委组**：J1 Gemini 4 Argon、J2 Gemini 3.8 Flash、J3 GPT-5.6 Sol（看画面）+ Qwen3.8-Omni-Flash（听音频）
  - 主表的分数是三组的均值
  - Gemini 既当评委又参赛，论文做了自偏好检验：去掉每个系统自家的评委组后，排名只有最后两名（Gemini 3.8 Flash 和 GLM）互换

## 3 主结果表

- 每一行都是**模型 + 厂商原生 harness**，不是裸模型
  - 统一用 Docker 沙箱：8 CPU、无 GPU、60 分钟，不允许调用图像或视频生成模型
  - 每个系统都用厂商接受的最高 effort
- 分数 = L3 Overall（No video = 0，三组均值），按分数从高到低排

| 模型 / Agent | 分数 | 设置 | 来源 URL |
|---|---|---|---|
| GPT-6 Astra | 4.109 | Codex CLI 0.162，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| Claude Opus 5.5 | 4.074 | Claude Code 2.1.301，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| DeepSeek-V4.1-Flash | 3.911 | DSH 0.2.1，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| Claude Sonnet 5.5 | 3.880 | Claude Code 2.1.301，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| Kimi K3 | 3.440 | Kimi Code 2.2.0，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| GPT-5.6 Sol | 3.317 | Codex CLI 0.162，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |
| Gemini 4 Argon | 3.069 | Antigravity CLI，effort high（不接受 xhigh） | https://arxiv.org/html/2610.35864v2#S4.T2 |
| Gemini 3.8 Flash | 2.798 | Antigravity CLI，effort high | https://arxiv.org/html/2610.35864v2#S4.T2 |
| GLM-5.3-Flash | 2.790 | ZCode 0.17.0，effort max | https://arxiv.org/html/2610.35864v2#S4.T2 |

补充列（同样来自 Table 2 / E.1 / E.3，方便换指标）：

| 模型 / Agent | Delivered-only Overall | L2 strict (%) | 交付视频数 (/239) | Human Elo | $/task | 95% CI（No video = 0） |
|---|---|---|---|---|---|---|
| GPT-6 Astra | 4.126 | 74.5 | 238 | 1242 | 8.19 | [4.052, 4.156] |
| Claude Opus 5.5 | 4.074 | 76.3 | 239 | 1203 | 15.38 | [4.037, 4.109] |
| DeepSeek-V4.1-Flash | 3.961 | 57.6 | 236 | 1022 | 0.47 | [3.826, 3.978] |
| Claude Sonnet 5.5 | 3.999 | 67.0 | 232 | 1121 | 8.26 | [3.769, 3.977] |
| Kimi K3 | 3.864 | 46.3 | 213 | 997 | 3.53 | [3.267, 3.593] |
| GPT-5.6 Sol | 3.735 | 39.0 | 213 | 705 | 11.84 | [3.174, 3.479] |
| Gemini 4 Argon | 3.989 | 55.2 | 184 | 1081 | 2.94 | [2.854, 3.269] |
| Gemini 3.8 Flash | 3.470 | 26.6 | 193 | 723 | 2.44 | [2.609, 2.979] |
| GLM-5.3-Flash | 3.736 | 33.5 | 179 | 905 | 0.32 | [2.582, 3.007] |

- 论文内部有几处小出入，都在舍入范围内
  - Table 2 和 E.1：Sonnet strict 67.0 / 66.9，GPT-5.6 Sol strict 39.0 / 39.1，Gemini 3.8 Flash L2 pass 80.5 / 80.4
  - E.3 的 CI 按每个任务的均值计算，和主表的汇总值最多差 0.011（例如 DeepSeek 3.907 / 3.911）
  - 柱状图统一用 Table 2 的数

## 4 映射到我们的模型列表

| 我们的模型 | 论文中的对应行 | 分数（No video = 0） |
|---|---|---|
| Claude Opus 5.5 | Claude Opus 5.5 + Claude Code | 4.074（第 2） |
| Claude Fable 5.1 | 未收录 | — |
| GPT-6 Astra | GPT-6 Astra + Codex CLI | 4.109（第 1） |
| Gemini 4 Argon | Gemini 4 Argon + Antigravity CLI | 3.069（第 7） |
| Gemini 4 Carbon | 未收录 | — |
| Kimi K3.1 Pro / K3 | 只测了 Kimi K3 + Kimi Code，K3.1 Pro 未收录 | 3.440（第 5，K3） |
| GLM-5.x | 只测了 GLM-5.3-Flash + ZCode（Flash 版，不是旗舰） | 2.790（第 9） |
| Qwen3.8-Max | 未收录 | — |
| Seed2.1 Pro | 未收录 | — |
| DeepSeek V4.x | 只测了 DeepSeek-V4.1-Flash + DSH（Flash 版） | 3.911（第 3） |
| MiniMax-M3 | 未收录 | — |
| Kling / Keye / 快手模型 | 未收录（没有参赛模型） | — |

- Qwen 在论文里出现过，但都不是参赛模型
  - Qwen3.8-Omni-Flash 是 J3 评委组的音频评委
  - Qwen3-TTS-Flash 是沙箱里提供给 agent 的 TTS 工具
- 快手 / Kling 在论文里只以两种身份出现
  - 作者单位：BUPT、ZGCA、PKU、JLU、**Kling Team**
  - 参考文献 [34]：Kuaishou Technology, *Kling AI*，仅被引用
- 表里有、但不在我们列表里的行：Claude Sonnet 5.5、GPT-5.6 Sol、Gemini 3.8 Flash

## 5 版本核对：项目页并不比论文新

- 项目页 HTTP Last-Modified 是 2026-10-31，比 v2 晚，但内嵌数据（`window.VVB`）和 v2 Table 2 / E.1 逐行一致
  - 都是同样 9 个系统、239 个任务，没有新增行或新分数
  - 项目页"三组均值"视图下的 No video = 0 分数和 Table 2 右栏完全相同
- 项目页的表格默认显示 **Delivered only**，直接照抄会拿到另一套数（Astra 4.126，Argon 3.989）。要拿 headline，得切到 "No video = 0"
- v1（2026-10-26）和 v2 的 Table 2 数字完全相同。v2 只改了 L2 strict 的定义措辞（补上"至少一条 core check 通过"）和 C.1 的 harness 参数说明
- GitHub README 没有成绩表，只有动态：10.26 项目页上线，10.27 arXiv 发布，10.30 发布数据集、rubric 和评测代码
- 结论：**以 arXiv v2 为准**

## Sources

- arXiv 摘要页（版本历史 v1 / v2）：https://arxiv.org/abs/2610.35864
- arXiv HTML v2，Table 2 主结果：https://arxiv.org/html/2610.35864v2#S4.T2
- arXiv HTML v2，Table C.1 系统与 harness：https://arxiv.org/html/2610.35864v2#A3.T1
- arXiv HTML v2，Table E.1 完整榜单：https://arxiv.org/html/2610.35864v2#A5.T1
- arXiv HTML v2，Table E.3 置信区间：https://arxiv.org/html/2610.35864v2#A5.T3
- arXiv HTML v1（用于对比）：https://arxiv.org/html/2610.35864v1
- 项目页 leaderboard（内嵌 `window.VVB` 数据）：https://vibevideobench.github.io/#leaderboard
- GitHub 仓库 README：https://github.com/vibevideobench/VibeVideoBench
- 本地背景材料（只读）：/mmu_mllm_hdd_4/deep-research/final-visual-code-blog/parts/video/vibe.md

