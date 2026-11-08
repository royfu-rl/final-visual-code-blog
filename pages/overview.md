# Visual Coding

## Contents

- [Scope](#scope)
- [Why Judgment Is The Bottleneck](#why-judgment-is-the-bottleneck)
- [A Verifiable Task Is Three Parts](#a-verifiable-task-is-three-parts)
- [What Each Chapter Answers](#what-each-chapter-answers)

## Scope

模型写出的代码能跑，不等于产物可用。视觉交互场景里，代码要被渲染、被操作，最后交付成网页、3D 资产或视频，验收只能落在渲染结果、交互行为和运行时状态上。

本文按产物的技术栈分三章，每章只收「模型写代码、代码产出视觉结果」的任务。

| 章节 | 主力技术栈 | 辅助技术栈 | 产物 |
|---|---|---|---|
| [Web (2D)](web.md) | html、webdev | ppt、manim | 单文件页面、多文件 Web App、幻灯片、讲解动画 |
| [3D](3d.md) | blender、3js | cad | Blender 场景、three.js 场景、参数化零件 |
| [Video](video.md) | video_web | video_blender | 代码驱动的动画与成片 |

三类任务不在范围内，理由都一样：它们不考「写代码」。

- **神经 3D 资产生成。** text-to-3D、image-to-3D 这类直接输出 mesh、NeRF 或 Gaussian 的模型不写代码，评的是外观质量与文本一致性。
- **专业软件 GUI 操作。** 在 Blender、CAD、剪辑软件界面里长程点击，考的是 GUI grounding。
- **游戏开发。** Pygame、Godot、UE5 这条线自成体系，判据和本文三章重合度低。

## Why Judgment Is The Bottleneck

[SWE-bench](https://arxiv.org/abs/2310.06770) 的每道题都带至少一个 fail-to-pass 测试，所以「改对了没有」是一个布尔值。视觉产出没有这个布尔值。一个页面、一段 three.js 场景、一个 Blender 渲染，对不对要靠人看。而看一眼就能判的东西，最难写成脚本。

常见的两条替代路线都被实测否掉了：把判定外包给像素指标，或让模型看着截图自评。

核心发现：现成的「看图打分」类信号与真值的相关性要么接近零，要么是负的。

下表四行全部出自 [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)。相关性是与隐藏契约覆盖率的逐对 Kendall τ_b，假阳性率是低覆盖率产物被判通过的比例，成本以只读 DOM 为 1。

| 判定方式 | 与真值的相关性 | 假阳性率 | 相对成本 |
|---|---|---|---|
| 隐藏运行时状态契约 | Kendall τ_b 1.000 | 0 | 约 2 倍 |
| 八步 agent 自主探查 | +0.111 | 45.6% | 约 400 倍 |
| 只读 DOM | −0.021 | 33.7% | 1 倍（基线） |
| 截图加 VLM judge | −0.068 | 3.2% | 约 50 倍 |

数据解读：截图加 VLM judge 的假阳率并不高，只有 3.2%，问题是它与真值的相关性为负——它不是乱放行，是排序方向错了，而且比读运行时状态贵 25 倍。只读 DOM 更糟，三分之一的坏产物被它放过。

换一套判据，同一批产物上的模型差距会整个变样。[3JSBench](https://3jsbench.com/) 用 100 道 three.js 题、每题三次一次成型的尝试、744 条确定性检查判定——其中 696 条必查（695 条分入六个检查族），48 条是不影响判定的 advisory（[方法论](https://3jsbench.com/methodology)）。Astra 通过 80.0%（240/300），Claude Opus 5.5 通过 49.0%（147/300），差 31 个百分点；而同一批尝试的 SigLIP2 相似度均值，Astra 0.1081 对 Opus 5.5 0.1067，只差约 0.001，站方自己把这个信号标为不参与判定的描述性指标。

这个榜单在四天内改判过三次（2026-10-14 到 2026-10-16），所以引用它必须带日期。本文的数字读自 2026-10-19，且不引用弱模型之间小数点级别的差异。

确定性判据能把模型分开，嵌入相似度不能。这是全文的出发点。

但结论要比直觉弱一档：**判定做确定了，差距不会自己消失。**

| 评测 | 判据性质 | 最高分 | 第二梯队最好 | 差距 |
|---|---|---|---|---|
| [3JSBench](https://3jsbench.com/) | 696 条必查的确定性检查，不含模型打分 | Astra 80.0% | Kimi K3 23.0% | 57.0 个百分点 |
| [WorldCoder-Bench 表 1](https://arxiv.org/abs/2606.01869) | 隐藏运行时状态契约，确定性断言 | GPT-5.4 覆盖率 27.8% | Qwen3.6-Plus 25.3% | 2.5 个百分点 |
| [Design2Code](https://arxiv.org/abs/2403.03163)（对照，非确定性） | 厂商报的是模型看图打的相似分 | GLM-5V-Turbo 94.8 | Qwen3-VL-235B-Thinking 93.4 | 1.4 个百分点 |

数据解读：差异不由判定方式解释，由动态范围解释。WorldCoder-Bench 的原文明说没有系统在隐藏契约上超过 30%，前四名挤在 23.0% 到 27.8%，差距被压扁；Design2Code 反过来，头部挤在 93 以上的上限，差距同样被压扁。只有 3JSBench 的最高分到了 80%，量程足够，差距才张得开。

所以先做判定的理由不是「结构不是瓶颈」，而是更朴素的一条：没有判定，既测不出差距，也训不动。

## A Verifiable Task Is Three Parts

一条可验证任务由三件组成，缺一件就不算。后面三章全部用这套词。

| 术语 | 定义 | 它不是什么 |
|---|---|---|
| Verified Task | 一道可自动判定的任务，由 Query、Harness、Verifier 三件组成 | 不是「一条 prompt 加一个参考答案」 |
| Query | 交给模型的需求描述，可带多模态参考（参考图、参考页面、参考视频） | 不是评分标准。模型看得到 Query，看不到 Verifier |
| Harness | 把产物跑起来并采集证据的那层：无头浏览器、冻结时钟、固定视口、多视角渲染、运行时状态读取 | 不是中性容器，它本身就是能力的一部分 |
| Verifier | 把证据判成通过或不通过的规则 | 不是 reward 模型 |
| 程序化信号 | 确定性规则给出的判定：执行是否成功、几何断言、DOM 盒模型、规则引擎、渲染计数器 | 不是静态代码分析，它读的是运行后的状态 |
| VLM judge | 用视觉语言模型看渲染结果给判定 | 不是 Verifier 的替代品 |

三件套里最容易被跳过的是 Harness，而它的影响量级和模型差距同级。

- [MTAC-IFBench](https://arxiv.org/abs/2609.14992) 上同一个 GLM-5.2，在 Claude Code 下严格全满足率 12.7，换 OpenCode 掉到 6.7，腰斩。
- [Vibe Code Bench 榜单](https://www.vals.ai/benchmarks/vibe-code)（2026-10-12）上同一个 Claude Opus 4.8，OpenHands 下 82.72%、Claude Code 下 77.48%；GPT-5.5 在 OpenHands、Factory、Codex 三个脚手架上分别是 69.85%、67.39%、58.19%，极差 11.7 点。

任何一个数字离开 harness 版本就没有意义。

Query 与 Verifier 之间还有一条硬约束：**Verifier 能查的信息量必须小于等于 Query 给出的信息量。** 需求写「杯子应使用有别于桌面木色的独立颜色」，Verifier 却要求恰好是参考里那个蓝，这道题就不可解。这类任务进了 RL 就是纯噪声。

## What Each Chapter Answers

Web 与 3D 两章用同一套五个视图：Benchmark、Open Data、Sources、Verifier、Train；Video 按两条路线分视图。

| 章节 | Benchmark | Open Data | Sources | Verifier · Train |
|---|---|---|---|---|
| [Web (2D)](web.md) | 厂商报的分只有两个第三方榜单可横比 | 公开供给压在单文件「截图 → 代码」 | 高质量开源页面从哪来、怎么筛 | 分层 reward、harness、选题蒸馏 |
| [3D](3d.md) | 只有 cad 进了厂商发布页 | 资产多、代码少，3js 没有公开管线 | three.js / Blender 高质量作品与槽位合成 | 读场景图不读渲染图，Blender 按版本分叉 |
| [Video](video.md) | — | Web 栈与 Blender 栈各自的公开工作 | — | 时序判据能做到哪一步 |

三类任务不在范围内，理由都一样：它们不考「写代码」。

- **神经 3D 资产生成。** text-to-3D、image-to-3D 这类直接输出 mesh、NeRF 或 Gaussian 的模型不写代码，评的是外观质量与文本一致性。
- **专业软件 GUI 操作。** 在 Blender、CAD、剪辑软件界面里长程点击，考的是 GUI grounding。
- **游戏开发。** Pygame、Godot、UE5 这条线自成体系，判据和本文三章重合度低。

## Why Judgment Is The Bottleneck

[SWE-bench](https://arxiv.org/abs/2310.06770) 的每道题都带至少一个 fail-to-pass 测试，所以「改对了没有」是一个布尔值。视觉产出没有这个布尔值。一个页面、一段 three.js 场景、一个 Blender 渲染，对不对要靠人看。而看一眼就能判的东西，最难写成脚本。

常见的两条替代路线都被实测否掉了：把判定外包给像素指标，或让模型看着截图自评。

核心发现：现成的「看图打分」类信号与真值的相关性要么接近零，要么是负的。

下表四行全部出自 [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)。相关性是与隐藏契约覆盖率的逐对 Kendall τ_b，假阳性率是低覆盖率产物被判通过的比例，成本以只读 DOM 为 1。

| 判定方式 | 与真值的相关性 | 假阳性率 | 相对成本 |
|---|---|---|---|
| 隐藏运行时状态契约 | Kendall τ_b 1.000 | 0 | 约 2 倍 |
| 八步 agent 自主探查 | +0.111 | 45.6% | 约 400 倍 |
| 只读 DOM | −0.021 | 33.7% | 1 倍（基线） |
| 截图加 VLM judge | −0.068 | 3.2% | 约 50 倍 |

数据解读：截图加 VLM judge 的假阳率并不高，只有 3.2%，问题是它与真值的相关性为负——它不是乱放行，是排序方向错了，而且比读运行时状态贵 25 倍。只读 DOM 更糟，三分之一的坏产物被它放过。

换一套判据，同一批产物上的模型差距会整个变样。[3JSBench](https://3jsbench.com/) 用 100 道 three.js 题、每题三次一次成型的尝试、744 条确定性检查判定——其中 696 条必查（695 条分入六个检查族），48 条是不影响判定的 advisory（[方法论](https://3jsbench.com/methodology)）。Astra 通过 80.0%（240/300），Claude Opus 5.5 通过 49.0%（147/300），差 31 个百分点；而同一批尝试的 SigLIP2 相似度均值，Astra 0.1081 对 Opus 5.5 0.1067，只差约 0.001，站方自己把这个信号标为不参与判定的描述性指标。

这个榜单在四天内改判过三次（2026-10-14 到 2026-10-16），所以引用它必须带日期。本文的数字读自 2026-10-19，且不引用弱模型之间小数点级别的差异。

确定性判据能把模型分开，嵌入相似度不能。这是全文的出发点。

但结论要比直觉弱一档：**判定做确定了，差距不会自己消失。**

| 评测 | 判据性质 | 最高分 | 第二梯队最好 | 差距 |
|---|---|---|---|---|
| [3JSBench](https://3jsbench.com/) | 696 条必查的确定性检查，不含模型打分 | Astra 80.0% | Kimi K3 23.0% | 57.0 个百分点 |
| [WorldCoder-Bench 表 1](https://arxiv.org/abs/2606.01869) | 隐藏运行时状态契约，确定性断言 | GPT-5.4 覆盖率 27.8% | Qwen3.6-Plus 25.3% | 2.5 个百分点 |
| [Design2Code](https://arxiv.org/abs/2403.03163)（对照，非确定性） | 厂商报的是模型看图打的相似分 | GLM-5V-Turbo 94.8 | Qwen3-VL-235B-Thinking 93.4 | 1.4 个百分点 |

数据解读：差异不由判定方式解释，由动态范围解释。WorldCoder-Bench 的原文明说没有系统在隐藏契约上超过 30%，前四名挤在 23.0% 到 27.8%，差距被压扁；Design2Code 反过来，头部挤在 93 以上的上限，差距同样被压扁。只有 3JSBench 的最高分到了 80%，量程足够，差距才张得开。

所以先做判定的理由不是「结构不是瓶颈」，而是更朴素的一条：没有判定，既测不出差距，也训不动。

## A Verifiable Task Is Three Parts

一条可验证任务由三件组成，缺一件就不算。后面三章全部用这套词。

| 术语 | 定义 | 它不是什么 |
|---|---|---|
| Verified Task | 一道可自动判定的任务，由 Query、Harness、Verifier 三件组成 | 不是「一条 prompt 加一个参考答案」 |
| Query | 交给模型的需求描述，可带多模态参考（参考图、参考页面、参考视频） | 不是评分标准。模型看得到 Query，看不到 Verifier |
| Harness | 把产物跑起来并采集证据的那层：无头浏览器、冻结时钟、固定视口、多视角渲染、运行时状态读取 | 不是中性容器，它本身就是能力的一部分 |
| Verifier | 把证据判成通过或不通过的规则 | 不是 reward 模型 |
| 程序化信号 | 确定性规则给出的判定：执行是否成功、几何断言、DOM 盒模型、规则引擎、渲染计数器 | 不是静态代码分析，它读的是运行后的状态 |
| VLM judge | 用视觉语言模型看渲染结果给判定 | 不是 Verifier 的替代品 |

三件套里最容易被跳过的是 Harness，而它的影响量级和模型差距同级。

- [MTAC-IFBench](https://arxiv.org/abs/2609.14992) 上同一个 GLM-5.2，在 Claude Code 下严格全满足率 12.7，换 OpenCode 掉到 6.7，腰斩。
- [Vibe Code Bench 榜单](https://www.vals.ai/benchmarks/vibe-code)（2026-10-12）上同一个 Claude Opus 4.8，OpenHands 下 82.72%、Claude Code 下 77.48%；GPT-5.5 在 OpenHands、Factory、Codex 三个脚手架上分别是 69.85%、67.39%、58.19%，极差 11.7 点。

任何一个数字离开 harness 版本就没有意义。

Query 与 Verifier 之间还有一条硬约束：**Verifier 能查的信息量必须小于等于 Query 给出的信息量。** 需求写「杯子应使用有别于桌面木色的独立颜色」，Verifier 却要求恰好是参考里那个蓝，这道题就不可解。这类任务进了 RL 就是纯噪声。

## What Each Chapter Answers

每章同一套结构：先看厂商自己报了哪些分，再看公开数据管线与学术题库能给什么，最后讲自研的可验证环境管线怎么造。

| 章节 | Benchmarks | Open Data Pipeline | Verified Environment Pipeline |
|---|---|---|---|
| [Web (2D)](web.md) | 厂商报的分只有两个第三方榜单可横比 | 四类技术栈各自有多少可下载数据与题库 | 逆向挖矿、(query, html) 的四种用法、omni 参考 query、分层 reward、harness、选题蒸馏 |
| [3D](3d.md) | 只有 cad 进了发布页，blender 只有 demo | 程序化合成为什么能给零成本真值 | 状态断言、版本适配、几何 reward |
| [Video](video.md) | — | Web 栈与 Blender 栈各自的公开工作 | 时序判据能做到哪一步 |

