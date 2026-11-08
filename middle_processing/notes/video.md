# Video 章素材库（V2）

> 这是**素材库**，不是博客正文。整理日期 2026-10-19。
> 本地素材标 `[本地]` 并给出文件路径；外部抓取标 `[网页 2026-10-19]` 并给出 URL。
> 未核实的一律写「未核实」，不补记忆。
>
> V2 的 Video 章只分两条路线：**From Web**（Web 技术栈产出动画/视频）与 **From Blender**（Blender/bpy 产出动画/视频）。
>
> 本地素材来源：
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/deep_video.md`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/pipe_meta_video.json`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/bench_meta_video.json`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/video_assets_sources.md`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/env/video.md`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/91_3jsbench_verified.md`
> - 补充（Blender 线用）：`vc_data/10_blender_tasks.md`、`vc_data/05_trajectory_repair.md`、`vc_data/12_self_verification.md`、`vc_data/07_capability_spec.md`

---

## 0. 两条路线的分界

| | From Web | From Blender |
|---|---|---|
| 技术栈 | JS/Canvas/WebGL、p5.js、SVG/CSS、Lottie JSON、Remotion(TS/React)、Motion Canvas、ECharts、ranim(Rust/wgpu)、HyperFrames、Hypit(.svml) | Blender/bpy、Python 脚本、Cycles/EEVEE |
| 产出 | 逐帧截图→mp4、SVG/CSS 动画、Lottie JSON、浏览器内渲染 | .blend 工程 + 渲染序列/mp4 |
| 确定性抓手 | 冻结时钟 + 固定种子 + 固定 DPR + 页面 `setTime` 钩子 + `canvas.toDataURL` 直读 | `bpy` 读活状态：F-curve、修改器栈、物理缓存、BVH 测距 |
| 本地素材厚度 | **厚**（11 篇论文级细讲 + 27 条管线 + 22 条基准） | **基本空白**（见 §2） |

本地 `env/video.md` 的核心论断（可直接引用）：**逐帧确定性是这条路线的根 —— 每一帧是帧号与代码的纯函数，同代码同帧永远渲染出相同像素，所以可逐帧复现、可测试、可迭代，这是扩散视频没有的性质。** `[本地 env/video.md]`

---

## 1. From Web

### 1.1 速查表（按本地 `pipe_meta_video.json` 的 7 个字段）

| 名称 | 日期 | 机构 | 语言/栈 | 产物 | 开源 | 采用度 |
|---|---|---|---|---|---|---|
| Keyframer | 2024/2 | Apple | SVG + CSS | CSS 动画（网页） | [GitHub `apple/ml-keyframer`](https://github.com/apple/ml-keyframer) | 76 star |
| MoVer | 2025/2 | Stanford | JavaScript(GSAP) | 网页矢量动画 | [GitHub `jama1017/MoVer`](https://github.com/jama1017/MoVer) | 39 star |
| OpusAnimation | 2025/10 | Opus AI Research | HTML/JS(ECharts) | 逐帧截图 → mp4 | **无下载入口** | 未报告 |
| InternSVG | 2025/10 | Shanghai AI Lab | SVG | SVG（含动画） | [GitHub `hmwang2002/InternSVG`](https://github.com/hmwang2002/InternSVG) | 127 star |
| OmniLottie | 2026/3 | StepFun | Lottie JSON | Lottie 动画 | [GitHub `OpenVGLab/OmniLottie`](https://github.com/OpenVGLab/OmniLottie) + HF | 798 star |
| LottieGPT | 2026/4 | Tsinghua | Lottie JSON | Lottie 矢量动画 | [GitHub `yisuanwang/LottieGPT`](https://github.com/yisuanwang/LottieGPT) | 39 star |
| VAnim | 2026/5 | Beihang | SVG | SVG 动画 | **无下载入口**（论文称开源数据集，未定位到仓库） | 未报告 |
| Lemo-Opuscar | 2026/9 | lemomo-ai | JavaScript(canvas/WebGL) | 逐帧成片 mp4 | [GitHub `lemomo-ai/lemo-opuscar`](https://github.com/lemomo-ai/lemo-opuscar) | 1.95k star（本地快照）→ **3,405 star**（2026-10-19 实查） |
| PDoomVideo | 2026/9 | JohnHeibel | JavaScript(p5.js) | 逐帧 MV mp4 | [GitHub `JohnHeibel/PDoomVideo`](https://github.com/JohnHeibel/PDoomVideo) | 2.0k star（本地快照）→ **2,212 star**（2026-10-19 实查） |
| huashu-art-motion | 2026/10 | AlchainHust | JavaScript(Canvas) | 逐帧截图 → mp4 | [GitHub `alchaincyf/huashu-art-motion`](https://github.com/alchaincyf/huashu-art-motion) | 3.44k star |
| **渲染器 / 框架** | | | | | | |
| Remotion | 2021/1 | Remotion AG | TypeScript / React | 视频 mp4 | [GitHub `remotion-dev/remotion`](https://github.com/remotion-dev/remotion) | 63.4k star |
| Motion Canvas | 2022/5 | Motion Canvas | TypeScript | 视频 mp4 | [GitHub `motion-canvas/motion-canvas`](https://github.com/motion-canvas/motion-canvas) | 19.3k star |
| ranim | 2026/1 | AzurIce | Rust(wgpu) | 视频 mp4 | [GitHub `AzurIce/ranim`](https://github.com/AzurIce/ranim) | 0.7k star |
| HyperFrames | 2026/6 | HeyGen | HTML/CSS/JS | 视频 mp4 | [GitHub `heygen-com/hyperframes`](https://github.com/heygen-com/hyperframes) | 61.2k star |
| Hypit | 2026/9 | hypit-ai | `.svml` DSL（框架） | 成片 mp4 | [GitHub `hypit-ai/hypit`](https://github.com/hypit-ai/hypit) | 21.4k star |

来源：`[本地 pipe_meta_video.json]`（star 数为该文件记录的快照，未标日期）；Lemo-Opuscar / PDoomVideo 的最新 star 为 2026-10-19 GitHub API 实查。

### 1.2 逐条细节（产出 / 规模 / 下载 / 评测 / 确定性信号）

#### Keyframer（2024/2，Apple）
- **产出**：静态 SVG + 自然语言意图 → GPT-4 生成 CSS/SVG 动画代码，内联渲染预览。`[本地 deep_video.md]`
- **定位**：这条线最早、被引最多，但**是 HCI 设计研究，不是基准**。全程人在环，**无自动验证器**。
- **规模**：13 人用户研究（新手+专家混合），90 分钟会话，任务是给土星、火箭两个 SVG 加动画；定性评估为主。
- **数字**：提示类型分布 Movement 68.4% / Direction 30.1% / Timing 27.5% / Coordination 19.7%；人均 15.8 条提示、每条 16.7 词、约 90 行代码；**6.7% 有语法错误**，**69.2% 用户会手动编辑生成的代码**。
- **下载**：✅ `apple/ml-keyframer`（76 star）。素材样例取自 `components/defaultSVGs.js`（galaxy/rocket）+ 生成提示词。`[本地 video_assets_sources.md]`
- **许可**：⚠️ **Apple 自定义样例许可，不是标准开源许可。**
- **确定性信号**：仅「CSS 能否编译/渲染」+ 人工。可直接复用的判据：语法错误率（实测 6.7%）。

#### MoVer（2025/2，Stanford）
- **本地素材仅有 meta 一行**：JavaScript(GSAP)、网页矢量动画、系统类、[GitHub](https://github.com/jama1017/MoVer)、39 star。`[本地 pipe_meta_video.json]`
- ⚠️ **本地没有细讲、没有规模数字、没有评测方式。** `deep_video.md`、`bench_meta_video.json`、`env/video.md` 均无 MoVer 条目。要写进正文必须补抓论文/仓库。**标：待补**。
- 注：名字读作 "Motion Verifier"，若确属「运动断言 DSL」则是本章确定性判据的关键引用，但**本次未核实**，不得据此下笔。

#### OpusAnimation / DCG-Bench（2025/10，Opus AI Research）
- **产出**：HTML/JS + ECharts 动画图表，逐帧截图合成 mp4。`[本地 pipe_meta_video.json]`
- **规模**：DCG-Bench **700 条测试**。`[本地 bench_meta_video.json]`
- **任务形态**：文本/视频 → 动画图表代码。
- **评测方式**：**执行率 + 代码 QA + 视频 QA**。
- **数字**：**本方向唯一的动画图表代码基准**；3B 专家模型平均 **+8.31%**。
- **下载**：❌ 无下载入口（`pipe_meta` 与 `bench_meta` 两处都没有 `download_url`）。
- **确定性信号**：执行率（能否跑出图表）、图表动画逐帧截图可比对 —— ECharts 走的是声明式 option，option 对象可回读，是本章「结构可回读」类判据的一个候选。

#### InternSVG（2025/10，Shanghai AI Lab）
- **产出**：SVG（含动画）。`[本地 pipe_meta_video.json]`，[GitHub](https://github.com/hmwang2002/InternSVG)，127 star。
- ⚠️ **本地无细讲、无规模、无评测方式。标：待补。**
- 相关但不同条目：同实验室的 **DTVBench · JanusCoder**（2025/10，102 任务，Manim 引擎，「视觉-程序接口」，7–14B 开源逼近或超过商用模型）`[本地 bench_meta_video.json]` —— 不要混为一条。

#### OmniLottie / MMLottieBench（2026/3，StepFun）
- **产出**：把矢量动画生成做成**自回归语言建模**。核心是参数化 Lottie tokenizer，把冗长 Lottie JSON 压成紧凑 token 喂给 VLM。`[本地 deep_video.md]`
- **管线**：① tokenizer 把 Lottie 命令与参数展平、对偏移量化，单条样本从约 **2,562 token 压到 486（省 81%）**；② 扩展 Qwen2.5-VL 的 Lottie token 嵌入，next-token 训练，支持文本 / 文本+图 / 视频三种输入。
- **规模**：数据集 **MMLottie-2M 约 200 万条**；基准 **MMLottieBench 900 条**（真 450 + 合成 450）。
- **评测方式**：FVD、CLIP、Claude-3.5 判对象与运动对齐（0–10）；视频任务另加 PSNR / SSIM / DINO。
- **数字**：Text-to-Lottie **成功率 88.3%**，而直接吐裸 JSON 的 GPT-5 仅 **12.7%**；FVD **180** 优于优化法 AniClipart 的 **266**；单条约 **31 秒**，比优化法快 **52–530 倍**。`bench_meta` 另记「矢量动画成功率 93.3%」——**与 deep_video 的 88.3% 不一致，引用时要选一个口径并注明**。
- **局限**：成功率口径在正文与附录间有出入（**88.3% vs 97.3%**），无效生成被从对齐指标里剔除；判对齐仍靠 Claude-3.5 看图打分。
- **下载**：✅ GitHub `OpenVGLab/OmniLottie`（798 star）+ HF `OmniLottie/MMLottieBench`、`OmniLottie/MMLottie-2M`（本地已抓过 Lottie/train 的 0,1,2 条，字段含渲染预览图 + `lottie_json`）`[本地 video_assets_sources.md]`
- **确定性信号**（这条路线最强的一个）：**Lottie JSON 结构可回读** —— 生成物本身是结构化 JSON，可以不渲染就断言图层数、关键帧时间、属性曲线类型、时长；「成功率」在这里的含义就是「JSON 能否被 Lottie runtime 解析」，是纯确定性的二值判据。88.3% vs 12.7% 这组对比正是「紧凑表示 vs 裸 JSON」在这个确定性判据上的落差。

#### LottieGPT（2026/4，Tsinghua）
- **本地素材仅有 meta 一行**：Lottie JSON、Lottie 矢量动画、[GitHub](https://github.com/yisuanwang/LottieGPT)、39 star。`[本地 pipe_meta_video.json]`
- ⚠️ **无细讲、无规模、无评测方式。标：待补。**

#### VAnim / SVGAnim-134k（2026/5，Beihang）
- **产出**：结构保持的开放域文生矢量动画。**不生成整帧、也不输出 Lottie**，而在一棵持久 SVG DOM 树上只写变化的属性差分（稀疏状态更新 SSU），支持非刚性路径编辑。`[本地 deep_video.md]`
- **管线**：① 识别优先规划（先把文本意图映射到具体 SVG 元素，再规划运动）；② 稀疏状态更新（逐帧只写变化的属性差分 + 控制标签）；③ **渲染感知强化学习**（基座 Qwen3-VL-8B-Thinking，GRPO，奖励来自渲染结果的语义对齐）。
- **规模**：**SVGAnim-134k**（SFT 123k / RL 10k / 测试 1k）。
- **评测方式**：视频感知编码器的语义对齐、**渲染成功率**、15 人用户研究；另用一个不同编码器做交叉检查以减少度量循环。
- **数字**：语义对齐 **0.281**，优于 Gemini 3 Pro **0.243**、GPT-5.2 **0.234**；**成功率 100% vs 86.2%**；24 帧序列**压缩 9.86 倍**（86.0k → 9.2k token）；用户研究三项均分 **4.62 / 4.48 / 4.55**，远高于 Gemini 3 Pro 的 **3.42 / 3.85 / 3.68**。
- **局限**：主评测指标的编码器与训练奖励的编码器同属一家族，**有度量循环风险**；论文称已开源数据集但**未定位到可用仓库**。
- **下载**：❌ 无（`pipe_meta` 无 `download_url`）。
- **确定性信号**：**渲染成功率 100% vs 86.2%** 是本章最干净的二值判据之一（SVG 能否被渲染器解析并渲出帧）；SSU 的差分序列本身是可回读的结构（可断言「第 N 帧哪个元素的哪个属性变了」）；「token 压缩 9.86 倍」也是可测量量。

#### Lemo-Opuscar（2026/9，lemomo-ai）
- **产出**：JS canvas/WebGL 逐帧成片 mp4。`[本地 pipe_meta_video.json]`
- **2026-10-19 实查更新**（GitHub API + README）：
  - **star 3,405**，fork 376，**许可 MIT · CC BY 4.0**，创建 2026-09-26，最后推送 2026-10-18。
  - README 自述是 **Claude Code skill**，**51 种影片风格**（⚠️ 小红书摘要写的「39 种」已过期），每种 = 一条风格提示词 + 一支纯代码样片。
  - 旗舰作 **OPUSCAR 98**：1927–2025 共 **98 部奥斯卡最佳影片**，每部一种风格，片长 **6:31**；**98 种风格里 77 个 2D、4 个 2.5D、17 个 3D**，并提供 [`styles.json`](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/styles.json) 机读清单。
  - 2026-10-16 新增 **Evidence Films** 子集：**8 种新风格**，主张「拍真实素材，每个数字可测量或有出处」。
  - 技术自述：画面 = canvas/WebGL 页面逐帧渲染；音乐 = 免费采样库原创配乐；旁白 = TTS。**「无视频生成、无素材库镜头」**。
  - ⚠️ 作者明示「风格是针对 Claude Opus 5.5 调的，其他模型可能复现不出来」。
- **确定性信号**：风格→样片是一一对应的公开配对数据，`styles.json` 是结构化可回读的；逐帧渲染天然可复现。可做判据：渲染成功、帧数/时长与配置一致。

#### PDoomVideo（2026/9，JohnHeibel）
- **产出**：p5.js 逐帧 MV mp4 —— 音乐视频《I'm Upping My P(doom)》。`[本地 pipe_meta_video.json]`
- **2026-10-19 实查**：`JohnHeibel/PDoomVideo` **2,212 star**，fork 230，**无许可声明（license: None）**，创建 2026-09-22，最后推送 2026-09-25。描述：「Source code for the Claude Opus 5.5 music video for I'm Upping My P(doom)」。
- ⚠️ **同名项目有两个，必须区分**（见 §3.4）：另有 `mexicat/pdoom-video`，**2,894 star**（更高），MIT，描述「Code-rendered music video for "I'm Upping My P(doom)"」，推送到 2026-10-05，且已派生出多个二创（`lycfyi/power-video`、`amemiya02/pdoom-video-win95`、`nonunsaram/feel-the-agi-video`）。小红书摘要说的「PDM Video」**无法确定指哪一个**。
- **确定性信号**：完整源码 + 故事板 + 渲染脚本公开 → 可复现「同代码同帧同像素」；歌词 MV 有天然的「音节对齐」时序断言（音节时间戳 ↔ 帧号）。

#### huashu-art-motion（2026/10，AlchainHust）
- **产出**：JS Canvas 逐帧截图 → mp4。[GitHub](https://github.com/alchaincyf/huashu-art-motion)，**3.44k star**。`[本地 pipe_meta_video.json]`
- ⚠️ **本地无细讲、无规模、无评测方式。标：待补。**

#### 渲染器 / 框架（这条路线的基础设施）
- **Remotion**（2021/1，63.4k star，TypeScript/React）：React 组件写视频，确定性来自「帧号 → 组件 props」的纯函数模型。`[本地 pipe_meta_video.json]`
- **Motion Canvas**（2022/5，19.3k star，TypeScript）：生成器函数描述时间轴。
- **ranim**（2026/1，0.7k star，Rust + wgpu）：Rust 版 Manim 思路。
- **HyperFrames**（2026/6，HeyGen，**61.2k star**，HTML/CSS/JS）：**本地明确结论 ——「渲染器基础设施已成熟，但面向 agent 的只有一个」，HyperFrames 是唯一把「给 agent 自动化用」写进设计的渲染器（命令行默认非交互、逐帧定位可复现）**。`[本地 env/video.md]`
- **Hypit**（2026/9，21.4k star，`.svml` DSL → 成片 mp4）：框架类，不是渲染器。
- 对照组（非 Web，属 Manim 生态）：`3b1b/manim` 94.9k star、`Manim Community` 41.5k star。

### 1.3 From Web 的确定性判据清单（可直接做 verifier 的信号）

按可靠度排序，全部有本地出处。

| 层级 | 判据 | 怎么测 | 本地证据 / 数字 |
|---|---|---|---|
| L1 二值 | **渲染/执行成功** | 代码能否无错渲染出帧 | VAnim 100% vs 86.2%；OmniLottie 88.3% vs 裸 JSON 的 GPT-5 12.7%；TheoremExplainAgent 不重试成功率极低、重试 5 次可达九成；o3-mini 93.8% `[deep_video.md]` |
| L1 二值 | **Lottie / SVG JSON 结构可回读** | 不渲染，直接断言图层数、关键帧时间戳、插值类型、时长、属性曲线 | OmniLottie 生成物即 Lottie JSON；VAnim 的 SSU 差分序列本身可回读 `[deep_video.md]` |
| L1 二值 | **时长 / 帧数与配置一致** | ffprobe 读 mp4 时长、帧率、帧数，对照任务规格 | `env/video.md` 把「渲染成功率」列为可执行、可复现的主指标 |
| L1 二值 | **关键帧元素出现** | 固定时刻截图 + 元素到代码行的占用表 | Code2Video 的 **6×6 锚点栅格** + 占用表，判重叠与出框，给「某元素该移到哪个格子」的可定位指令 `[deep_video.md]` |
| L1 几何 | **版式几何检查**（重叠 / 出框） | 元素 bbox 相交 / 越界 | `env/video.md` 列为「可执行」；TheoremExplainBench 实测**元素布局是各模型普遍弱项（0.57–0.73）** |
| L1 几何 | **几何正确性（three.js 场景）** | 捕获 three.js 场景，九个固定视角 + 部件计数/结构/空间关系断言 | 3JSBench **696 条必查项**（见 §3.2），**乘法门控：全部必查项通过才算过** |
| L2 答题 | **知识传递 / 看产物答题** | 先屏蔽知识得基线，再只看视频答题，差值即传递量 | TeachQuiz：Opus 4.1 **40.0 → 86.0**；人类 3B1B **97.1**；Veo3 **2.5**、OpenSora-v2 **0.0**。PresentQuiz：PaperTalker **0.842 / 0.951** 超人类作者 **0.738 / 0.908** `[deep_video.md]` |
| L3 参考 | **VLM 看图打分** | VLM 给画面打分 | ⚠️ **不可做主指标**。ManimAgent 实测其 VLM 判官与人评**相关系数 −0.17**，作者明确把 VLM 排除在头部证据外；TheoremExplainAgent 自动指标与人评只有视觉相关性 0.72、元素布局 0.42 显著，准确深度 0.14、逻辑流 0.16 近乎无关 `[deep_video.md]` |
| L3 参考 | **嵌入相似度（CLIP / SigLIP）** | 渲染图与文本的余弦 | ⚠️ **等于没有闸**。3JSBench：Astra/Opus 5.5/GPT-6 Sol 通过率 80.0% / 49.0% / 27.0%（差 53 个百分点），SigLIP2 均值差只有 **+0.011 / +0.009 / +0.007**（差 0.004）`[91_3jsbench_verified.md]` |

### 1.4 From Web 的 harness 实测（确定性怎么拿到手）`[本地 06_harness.md]`

调研日期 2026-10-15，star 数为当日 GitHub API 实查；实测脚本在 `visual-coder-blog/scripts/vc_verifier/`。

- **纯 CPU 够用**：three.js 走 Chrome headless + **SwANGLE**（SwiftShader 上的 ANGLE）。8 视角转台约 **0.2 s**；复用浏览器后 48 核配额下稳态约 **14 任务/s**。**RL rollout 的视觉验证不必上 GPU 沙箱。**
- **必加 flag**：`--use-gl=angle --use-angle=swiftshader(-webgl) --enable-unsafe-swiftshader`。Chrome M139 起不显式 opt-in 就建不了 WebGL；本机 Chrome 148 实测不加就没有 WebGL。**不要加 `--disable-gpu`**（会把 SwANGLE 一起关掉）。
- **确定性阶梯实测**（`bench_clock.js`，动画页用 rAF + `performance.now` + `Math.random`、不暴露钩子）：

  | 方案 | 截图 md5 种类数 |
  |---|---|
  | 不控制 | 3/3、20/20 **全不同** |
  | 只调 Playwright `clock.install` | 3/3 **不同**（加载耗时 113–432 ms 漏进了 `performance.now`） |
  | `install + pauseAt + runFor(1500)` + 种子 random | 20 次里 **2 种**（11/9），推测是 rAF 帧相位差一帧 |
  | **页面钩子 `setTime` + `canvas.toDataURL` 直读** | **3/3 逐字节一致** |

  → **结论：clock 只能把方差压下来，压不到零；要逐字节复现，必须在任务契约里要求页面暴露 `setTime` / `view` 钩子并直读 canvas 像素。对模型自由写的页面，verifier 只能用感知容差（SSIM / pHash），不能比 hash。**
- **其他确定性手段**：固定 viewport、`deviceScaleFactor=1`、`--font-render-hinting=none --disable-lcd-text`；镜像里打包固定字体集、禁止页面联网拉 Google Fonts；`addInitScript` 注入带种子的 `Math.random`。虚拟时间（`--deterministic-mode` / `--virtual-time-budget`）只在 `chrome-headless-shell` 里有，属实验性。
- **并发吞吐实测**：

  | 配置 | 吞吐 | p50 | p95 |
  |---|---|---|---|
  | 1 浏览器 × 1 页 | 2.4 任务/s | 383 ms | — |
  | 1 浏览器 × 8 页 | 3.4 任务/s | — | — |
  | 4 浏览器 × 8 页 | 11.6 任务/s | — | — |
  | 8 浏览器 × 8 页 | **14.3 任务/s** | 4.1 s | 4.9 s |

  每个浏览器只有一个 GPU 进程，SwiftShader 在里面串行 → 必须多浏览器 × 多页。
- **体积**：`chrome-linux64` 目录 552 MB；`node_modules`（puppeteer-core + three + playwright-core）65 MB。
- **自检工具设计**：核心不是截图 —— 要同时给结构化观测（scene graph、console、bbox），返回 JSON 成本毫秒级，看图要 token；多视角**拼成一张 contact sheet，token 只有逐张发送的 1/8 左右**。
- **训练与评测的工具必须同构**：同一模型换 scaffold，分差可达数个百分点；建议训练时就用「一套 MCP 工具 + 两种 transport」，评测时原样复用。

### 1.5 From Web 的四条本地结论（可直接引用）`[本地 env/video.md]`

1. **紧凑表示是制胜招，不是写代码本身。** 直接让模型吐裸 Lottie JSON 成功率接近零；OmniLottie 加 tokenizer 升到 88.3%，VAnim 改稀疏状态更新 token 效率提升 9.86 倍。**模型学不动的是长串低层代码，不是代码这个媒介。**
2. **验收分成两半，可靠的那半是可执行检查。** 渲染成功率、版式几何、答题正确率可复现；VLM 看图打分不可靠（ManimAgent 实测 −0.17）。
3. **渲染器基础设施已成熟，但面向 agent 的只有一个**（HyperFrames）。
4. **最缺的是失败后如何修复的轨迹数据。** 公开数据几乎全是一次成功的配对；ManimAgent 的双通道记忆是少数带迭代过程的工作。

### 1.6 厂商信号（From Web 相关）`[本地 env/video.md]`

- **没有任何厂商报告公开的 code-video benchmark。** MMMC、TeachQuiz、TheoremExplainBench 都没出现在任何厂商发布材料里。
- 厂商信号只有两种，**都不是在测做视频**：① 全代码成片的社区技能潮（由 Claude Opus 5.5 的编码时长跨过门槛触发，社区用它写 HTML/Canvas/Three.js 动画代码逐帧渲染出片，无视频模型）；② 发布页的动画 demo（Gemini 3.8 Flash 一句提示生成 Three.js 动画与可交互 3D 场景；GPT-6 Astra 的 Three.js + WebGPU 动画与游戏）。
- 自建子类：Moonshot Kimi K3 的 Kimi Webdev Bench 有 SVG / 动画子类，**题目不公开**。
- 未报告相关分数：ByteDance Seed、MiniMax、DeepSeek 等。

---

## 2. From Blender

### 2.1 结论先行：**本地素材基本空白**

把 6 个指定本地文件全部检索过 `blender|bpy|4DBuild|SimWorlds` 后的结果：

| 文件 | 命中 | 说明 |
|---|---|---|
| `deep_video.md` | **0** | 11 篇细讲全是 Manim / SVG / Lottie / Beamer，**无一篇 Blender** |
| `pipe_meta_video.json` | **0** | 27 条管线+渲染器，**无 Blender 条目** |
| `bench_meta_video.json` | **0** | 22 条基准，**无 Blender 条目** |
| `video_assets_sources.md` | **0** | 配图与样例全是 arXiv HTML / HF / GitHub SVG |
| `env/video.md` | **0** | 渲染器维度列的是「Manim、SVG+CSS、Lottie、Beamer、HTML/Canvas、游戏引擎」——**Blender 根本没进这张表** |
| `vc_data/06_harness.md` | 有（§1.2、§4.2） | 但只讲**无头渲染基础设施**，不讲「Blender 产出视频」这个任务 |

→ **V2 的 From Blender 这条线，在 Video 章的本地素材里是一条全新的线，必须靠外部素材（主要是 BlenderWorld）撑。**

### 2.2 本地**有**的 Blender 素材（都不在指定 6 文件里，需从 vc_data 其他文件取）

#### (a) `06_harness.md` §1.2 + §4.2：Blender 无头渲染可行性（这是唯一直接可用的指定文件内容）
- 调用方式：`blender -b --factory-startup --python x.py -- args`，或 `pip install bpy` 在 Python 里直接 import。
- **EEVEE 能否无头**：Blender 3.4 起 Linux 的 `-b` 模式有 **headless EGL 后端**，其他后端失败时自动回退（提交 D15555）。本地结论：**apt 版 4.0 和 pip 版 bpy 4.5 都能在无 GPU、无显示的环境里跑 Workbench / EEVEE / Cycles**；EEVEE 走 Mesa 的 surfaceless swrast（llvmpipe）。
- **确定性**：`--write-movie` 配 **`--fixed-fps`**。4.x 后续版本有没有原生离屏渲染：**未核实**。
- ⚠️ `--headless` 等于 dummy 渲染器，**读不回贴图、不能截图**。
- 本机实测：`/usr/bin/blender` 4.0.2（apt，EEVEE Legacy）；另用 uv 建 Python 3.11.14 venv 装 **bpy 4.5.14 LTS**（EEVEE Next），海外代理 uv pip install 用时 **121 s，包体 784 MB**。场景：桌子+环面+太阳光，8 视角转台（`bench_blender.py`）。
- 对照：Unity `-batchmode -nographics` **不初始化图形设备，不能渲染或截图**；KasmVNC 桌面镜像不是批处理镜像、不支持 GPU 渲染。
- MCP 工具面（当前）：`execute_blender_code`、`look`（视口/相机/多角度自动取景/渲染图）、`get_scene_info`（可按 root / query 下钻）、`generate_3d`（Tripo / Hunyuan3D / Rodin）、`search_assets` / `import_asset`（Poly Haven / Sketchfab / Poly Pizza）。

#### (b) SimWorlds / 4DBuildBench（arXiv 2607.01766，2026-07）—— **动态 bpy 的核心引用** `[本地 05_trajectory_repair.md, 12_self_verification.md, 07_capability_spec.md]`
> ⚠️ 这条**不在指定 6 文件里**，在 `vc_data/05_trajectory_repair.md`（L748–L766）、`12_self_verification.md`、`07_capability_spec.md`。

- **定位**：**刻意放弃图像 critique 循环**，直接查 Blender 活状态。
- **四族规则**：
  1. **结构**：集合层级、父子链；
  2. **几何**：**BVH 测距** —— 声明接触的必须真接触，没声明却穿插的判失败；
  3. **软规则**（只警告）：落地、连通性、缺相机或灯光；
  4. **计划与状态比对**（含**运动时序**）：例如 settle 阶段最后几帧速度必须接近 0。
- **工具**：`blender_scene_state` 读**修改器栈 / 物理缓存 / 动画曲线**；`motion_sheet` 按阶段边界逐帧采样。
- **防作弊规则**（直接可抄）：**求解器驱动的对象不许有密集关键帧；布料和软体不许用 shape key 驱动运动。**
- **数字（4DBuildBench 50 场景）**：

  | 指标 | SimWorlds（读 Blender 活状态） | VIGA（纯视觉 verifier，Opus 4.7，15 轮） |
  |---|---|---|
  | 机制通过率 MPR | **0.87** | 0.67 |
  | 结构通过率 SPR | **0.89** | 0.70 |
  | VLM 评分 | 0.82 | 0.78 |

  **本地标注「这组对比是全篇最有说服力的一个数据点」：MPR 差 0.20，而 VLM 评分只差 0.04 —— 均匀抽 5 帧的 VLM judge 判断不了运动是怎么产生的，手打关键帧的假物理也能拿高分。**
  分材质：**流体类 MPR 0.95 vs 0.56；刚体 0.83 vs 0.61**。
  消融（15 场景子集）：去掉 verifier → SPR **0.97 → 0.87**（两个最难场景的 SPR 直接归零）；去掉分阶段 → VLM 评分 **0.87 → 0.76**。

#### (c) 本机 Blender 变异实验：**单帧渲染的 verifier 对动画完全失明** `[本地 10_blender_tasks.md]`
> ⚠️ 这条也**不在指定 6 文件里**，但它是 From Blender 线最硬的本地实测。

**A7 动画 F-curve 断言**：
```python
act = o.animation_data.action
for c in act.fcurves:
    print(c.data_path, c.array_index, c.extrapolation,
          [(k.co[0], k.co[1], k.interpolation) for k in c.keyframe_points])
val = c.evaluate(20)   # 也可按帧求值
```
- **能验证**：「第 1 帧到第 40 帧绕 X 轴从 −20° 转到 15°」「关键帧必须是线性插值」「循环外推 `extrapolation == 'CYCLIC'`」「25 fps、1 秒的动画」；也能查驱动器 `o.animation_data.drivers[i].driver.expression`。
- **为什么必须有**：本机变异 `anim_missing`（两条关键帧整条删掉）的 **view0 / 多视角 / Chamfer / 体素 IoU 全部是 1.0000，只有 A7 抓到**；VLM **0/8 全漏**。要用渲染抓动画，**得渲一整段序列，成本至少翻 N 倍**。
- **实测保真**：检出 1/8、保真 **7/7 和 4/4**（两批都是满分保真）。
- 三条配套结论：① **三者盲区几乎正交，必须组合** —— 断言独占的是「光照强度、动画、修改器、约束、物理、渲染设置、相机参数」，这些**在静帧里不存在**；几何独占的是「朝向、小部件挪位、定量尺寸、形状对不对」，这些**写不成等式断言**；**VLM 独占：没有**（22 个变异里 VLM 抓到的每一个都被程序化信号同时抓到）。② **全量断言 = 零判别力**（九族全查在两批上保真 0/11 和 0/4）—— 断言必须按题干裁字段，这个清单要在**造题干的时候**生成。③ **单张截图是最差的视觉信号**（view0 在 22 个变异上只判对 12 个）。

#### (d) 能力谱 D8「动画与时间维度」`[本地 07_capability_spec.md]`
- 判据：**固定时钟逐帧读状态**（Playwright `page.clock` / Blender `frame_set`）+ 机制断言 —— 「运动是否由正确机制产生（物理 / 插值 / 状态机），而不是某一帧看起来对」。
- 该维度标注为 **L1 级 + 需 RL 环境**。
- 同维度邻居（Web 侧，可与 Blender 侧对照）：**Animation2Code**（arXiv 2606.28593，**214 测试题 / 1,069 条网页动画视频，86% 纯 CSS**，headless Chromium **1024×768@30fps** 确定性渲染，与人类偏好一致约 **83.9%**）；**PRISM**（2605.19382，**确定性坐标检查，刻意不用 VLM**，Spatial Pass = 渲染成功且审计帧无 overlap / out-of-bounds / leakage）。
  关键落差数字：**Animation2Code 的 Appearance 最高 GPT-5.4 0.84，但 Temporal 最高只有 Gemini 3 Flash 0.31** —— 时间维度是全行业最弱的一格。**PRISM 的 Exec 最高 GPT-5.4 0.945，但 Spatial 最高 Gemini 3.1 Pro 0.572，Exec→Spatial 平均掉 41.24 点**（95% CI [40.41, 42.11]）—— **只报执行率的指标没有信息量。**

### 2.3 明确标注的空白（From Blender）

| 缺什么 | 状态 |
|---|---|
| 「Blender/bpy 产出动画视频」的**管线类工作** | ❌ 本地 0 条。`pipe_meta_video.json` 里 Blender 条目为空。**需外部补**（见 §3.1 BlenderWorld，但 BlenderWorld 是 3D 创作基准、动画只是 9 个 domain 之一，不是视频生成管线） |
| 「Blender 产出视频」的**基准** | ❌ 本地 0 条。最近的是 4DBuildBench（50 场景，4D/物理，不是视频产出） |
| Blender 侧的**star / 采用度数字** | ❌ 本地无 |
| Blender 渲染的**确定性实测**（同代码同帧同像素） | ⚠️ 只有「`--write-movie` 配 `--fixed-fps`」一句，**没做过逐字节复现实验**（Web 侧做了，见 §1.4） |
| Blender **动画渲染的吞吐/成本实测** | ⚠️ 只有 8 视角静帧转台，**没有序列渲染的吞吐数字** |
| Blender → mp4 的**具体 pipeline 素材**（脚本、配置、样例） | ❌ 本地 0 条 |
| 社区侧「用 Blender 脚本做视频」的项目 | ⚠️ 仅在 `opus-video-prompts` README 里被提到一句「Blender 脚本也有人用」（见 §3.4），**无具体项目** |

---

## 3. 外部链接抓取结果

### 3.1 BlenderWorld（Blender 方向的开源数据管线）

**抓取状态：✅ 成功（多源交叉）。抓取时间 2026-10-19。**

抓到的源：
| 源 | URL | 状态 |
|---|---|---|
| GitHub 仓库页 | https://github.com/QwenLM/BlenderWorld | ✅ WebFetch |
| GitHub README（raw） | https://raw.githubusercontent.com/QwenLM/BlenderWorld/main/README.md | ✅ HTTP 200 全文 |
| 评测协议文档 | https://raw.githubusercontent.com/QwenLM/BlenderWorld/main/docs/evaluation.md | ✅ HTTP 200 全文 |
| HF 数据集卡 | https://huggingface.co/datasets/Qwen/BlenderWorld | ✅ WebFetch |
| 项目主页 | https://blenderworld.github.io/ | ✅ curl（静态文案） |
| 主榜单数据 | https://blenderworld.github.io/data/leaderboard.json | ✅ HTTP 200，13 模型完整表 |
| GitHub API | https://api.github.com/repos/QwenLM/BlenderWorld | ✅ 136 star / 5 fork / MIT |

#### 一句话定位
**「Benchmarking Visual Agents for 3D Creation from Real-World References」** —— 首个专门评测前沿模型在**真实 3D 创作任务**上的综合基准。agent 拿到任务简报 + 参考媒体 + 可选规格文件，交付**可编辑的 Blender 工程**加要求的导出件。

#### 作者与机构（项目页）
Xinyu Fang(1,2)、Yuchi Wang(2,3)、Weihao Yu(2,3)、Rongyao Fang(2)、Zhaohai Li(2)、Zhixun Li(2,3)、Tiancheng Gu(2)、Xilin Wei(2,4)、Yuhang Zang(5)、Hongsheng Li(3)、Dahua Lin(3,†)、Guofeng Zhang(1,†)、Shuai Bai(2)、Zhibo Yang(2,†)、Dayiheng Liu(2)。
机构：1 浙江大学 · 2 **Alibaba Token Hub, Alibaba Group** · 3 香港中文大学 · 4 复旦大学 · 5 南洋理工大学。

#### 任务形态
- 输入：**文本、图像、视频、结构化规格**四类。
- 模态拆分：**文本 78 / 图像+文本 130 / 视频+文本 15 = 223**（多模态合计 **145**）。
- **59 个任务**额外带**规格附件**（尺寸、材质、相机设置方面的硬要求），可与视觉参考共存。
- 覆盖域：产品、建筑、环境、角色、**动画**、科学可视化 —— **9 个 category / 22 个 subcategory**；**11 个最大应用场景覆盖 223 个任务中的 213 个**。
- 9 个 category 的确切名称（从 `leaderboard.json` 的 `categories` 字段读出）：`Architecture & Interiors`、`Art & Animation`、`Products & Manufacturing`、`Characters & Animals`、`Nature & Landscapes`、`Rendering & Simulation`、`Vehicles & Machinery`、`Procedural & Game Assets`、`Science & Visualization`。
- 任务 ID：中立编号 **`bw_0001` – `bw_0223`**。
- 单任务目录结构：`instruction.md`、`task.toml`、`environment/`（Dockerfile + inputs）、`tests/`（verifier）。输入含 `query.txt`、`input.json`、`instruction.html`（图片 Base64 内嵌）、可选 `references/` 与 `attachments/`。
- agent 读 `/workspace/inputs/`，把工程写到 `/workspace/exports/final.blend`；提交物打成**一个 ZIP/任务**（`final.blend` 在根，可选 `textures/`、`outputs/`）。
- **评测 rubric 在生成期间对 agent 隐藏。**

#### 数据规模
- **223 个真实世界任务**
- **2,651 条二值 rubric 判据**（task-specific binary criteria）
- **9 个 category / 22 个 subcategory**
- **13 个前沿模型**上榜
- 公开展厅：**181 份提交，来自 7 个模型，覆盖 26 个任务**（策展样本，非随机抽样）
- HF 包：**总文件体积 617 MB**，上月下载 **2,422** 次，likes **24**，size category `n<1K`，语言 English + Chinese，tags `benchmark / harbor / blender / 3d-generation / multimodal`。**Dataset Viewer 关闭**。
- 另含 `reference_images.base64.json`（**130 张输入图**）+ `bw_0182` 的 1 张 verifier-only 图；`taxonomy.csv` / `taxonomy.json` / `index.html` 可浏览任务。
- ⚠️ **无 train/val/test 切分**（页面只提到一个 `validation.json` 记录校验结果，未给切分规模）。**不捆绑 oracle 解。**

#### 怎么造的
- 构造流程图的说法：**「From production briefs to verifiable requirements」** —— **多样任务与参考先过「结构 + 语义双重校验」，再经「独立 rubric 评审」**（Diverse tasks and references undergo structural and semantic validation, followed by independent rubric review）。
- ⚠️ **README 与 HF 卡都只给到这一句 + 一张流程图，没有给出标注人数、每任务工时、rubric 作者数、一致性系数等细节。更细的要看 `docs/*.pdf` 技术报告（本次未读 PDF）。**
- 数据统计图的三面（图注）：(a) 11 个最大应用场景，覆盖 213/223；(b) 参考与规格类型可共现；(c) 内环 = category，外环 = importance。

#### verifier 怎么设计的（**这是最该抄的部分**）
三个 evaluator 角色 + 两级判据 + 50:50 加权：

1. **渲染 agent（Render Agent）**
   - 从**实际场景**里自选 **8 个自适应视角**，**Cycles，1024 × 1024，64 samples**。
   - **每个视角在首次尝试后最多纠正 2 次**（up to two corrective re-renders per view）；Blender 启动钩子记录实际 engine / samples / device / 渲染完成情况，并**拒绝对同一输出路径的第 4 次尝试**。
   - **允许改**：相机位置、取景、裁剪面、evaluator 的渲染设置。**必须不变**：几何、材质、贴图、可见性、灯光、动画、色彩管理。
   - 输出校验器要求**全部 8 张 1024×1024 PNG 都在**且运行时记录匹配。渲染器**逐张打开 PNG 做检查**。
   - 丢失的贴图路径**只能从同一份提交的 workspace 里**按无歧义路径匹配恢复；**不重写已保存的工程**；**作者自己画出来的视觉瑕疵保留**（Authored visual defects are retained）。
2. **场景审查 agent（Agent-as-Judge / Scene Inspector）**
   - 处理 **`scene_summary`** 类判据 —— 通过 **Blender 工具读结构**，保存原始判断、审查证据与 CLI 日志。
   - **结构判据缺失 → 直接判评测失败，不允许用视觉猜测顶替**（Missing structural verdicts fail evaluation instead of being substituted with visual guesses）。← **这是硬门控。**
3. **视觉判官（VLM）**
   - 处理 **`render`** 与 **`either`** 类判据 + **盲描述** + **8 个整体质量维度**。
   - 8 个维度（项目页列出）：**Scene fidelity、Physical plausibility、Style & color、Realism、Spatial layout、Proportion & scale、Lighting & materials、Completeness**。
   - 证据侧：图像参考**直接送判官**；视频参考**抽成 4 个有序帧**；作者自己产出的视频**最多 16 个有序帧**送视觉判官；声明的文件与原生工程**对场景审查器可见**。作者图与 evaluator 视角**分开选取**，这样「final image 要求」能对着作者交付物判。
   - **每条判据只路由一次**（Each criterion is routed once）。

**打分公式（README 原文）**
```text
Rubric score    = 100 × Σ(weight × pass) / Σ(weight)
Dimension score = 10 × mean(eight ratings from 1 to 10)
Final score     = 0.5 × rubric score + 0.5 × dimension score
```
- 每条二值判据带 **importance weight = 1 / 2 / 3**。
- **公开协议不设分数上限**（no score cap）—— 即**没有** catastrophic-failure 或 scene-fidelity 封顶。
- **缺失或失败的提交得 0 分且留在分母里**（Missing or failed submissions receive zero and remain in the selected denominator）。← 反作弊的关键一条。
- 「只算成功任务的均值」**不得替代** benchmark 均值。
- 不完整的 dimension 输出、缺失的 evaluator 渲染 → 判为**工程失败**，不是低分。
- 论文里**三个 evaluator 角色全部用 `gpt-5.6-terra`**；公开实现默认同款，可用 `--render-agent-model` / `--agent-judge-model` / `--judge-model` 换别名（**报告结果时必须记录别名**）。

**人类一致性校验**：主判官的 overall 分与**多数人类偏好在 147 个合格配对里一致 122 个 = 82.99%**。150 个同输入配对由 3 名评审打分；skip 记作 tie；3 个无多数的配对被排除。判官只有在 A-win / B-win / tie 预测与多数**完全一致**时才算 agree。另报 Spearman ρ（Pearson 与 Kendall 全量在论文里）。

**提交防护与可复现**：
- ZIP 校验 manifest 校验和、保留相对路径、校验 ZIP 与解压文件未变；**拒绝**逃出压缩包的路径、链接、重复成员、缺主工程、无效 manifest。上限 **100,000 个归档成员 / 20 GiB 未压缩数据**。
- 任何模型调用前，evaluator 先核对**实际的 Blender / Node.js / Claude Code 版本**并写进 `runtime.json`；**版本不匹配直接中止**为配置错误。
- `plan.json` 固定代码 hash、任务与 rubric hash、原始提交 hash、模型名与协议；**resume 要求精确匹配**；进程锁防同一 run 多主。
- 输出：`/logs/verifier/reward.json` 含 `reward` / `rubric_score` / `dimension_score`，各为 0–1；overall = mean(`reward`) × 100。证据在 `metrics.json` 与 `run/`。`summary.json` 给 overall / text / multimodal 三个聚合；`results.csv` 给逐任务分数与错误；逐任务证据在 `tasks/<task_id>/`。部分聚合标 `complete=false`，未完成任务**留在分母**。

#### 能不能下载
**✅ 可以，全开。**
```bash
git clone https://github.com/QwenLM/BlenderWorld.git
cd BlenderWorld && python -m pip install -e .
bw download --output data/BlenderWorld
bw verify data/BlenderWorld
bw list data/BlenderWorld --modality image
bw prepare --dataset data/BlenderWorld --task-id bw_0001 --output work/bw_0001
bw pack-submission --source model-output --task-id bw_0001 --output submissions/bw_0001.zip
bw evaluate --dataset data/BlenderWorld --submissions submissions --output runs/full --resume
```
镜像入口：HF `Qwen/BlenderWorld`（617 MB）、ModelScope `Qwen/BlenderWorld`、项目页 https://blenderworld.github.io/ 、技术报告 PDF 在 `docs/`。`bw download --revision <sha>` 可钉版本。**Harbor 适配器可选**（`docs/harbor.md`）。

#### 许可
**MIT**（GitHub API 实查 `spdx_id: MIT`；HF 卡注明 MIT 覆盖 adapter 与 evaluator 代码）。

#### 环境钉版（可复现的硬约束）
- 生成：**Blender 4.2.10**；用自带 coding-agent 环境时另钉 **Node.js 22.17.0、Codex CLI 0.147.0、Claude Code 2.1.220**；`DISABLE_AUTOUPDATER=1`。
- 评测：Blender 4.2.10 + Node.js 22.17.0 + ffmpeg/ffprobe + Claude Code 2.1.220 CLI + 一个 vision-capable Chat Completions 端点。推荐 GPU Cycles，**CPU Cycles 也支持，同分辨率同采样数**。
- Harbor 路线：Harbor 0.23.0、Python 3.12+、GPU Linux sandbox（示例用 Modal 后端）、MCP for Blender 2.1.3。生成与 verifier **各要 8 CPU / 16 GiB RAM / 100 GiB 存储 / 1 GPU**；**生成超时 28,800 秒（8 小时）/任务**，verifier 超时 8 小时，环境构建超时 1 小时。
- 打包旧 rollout **不会**转换其 Blender 版本 —— 要生成与评测版本一致，必须用 4.2.10 重新生成。

#### 主榜单（13 模型，`leaderboard.json`，0–100 制）
> 列义：Overall = 223 任务均分（每任务 50% Rubric + 50% Dimension）；Text / MM = 78 文本 / 145 多模态任务均分；Full pass = 通过**全部** rubric 判据的任务占比（≠ overall 100）；Turns / Tools = 每任务平均 agent 轮数与工具调用数；Output tokens = 每任务平均生成 token（千）。失败评测得 0 且留在分母。

| # | 模型 | Overall | Text | MM | Rubric | Dimension | Full pass | Turns | Tokens(K) | Tools |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **GPT-6-Astra** | **79.9** | 78.6 | 80.7 | **87.3** | **72.6** | **42.2%** | 45.6 | 84.5 | 79.1 |
| 2 | **Opus-5** | **73.0** | 74.8 | 72.1 | 80.9 | 65.1 | 25.6% | 158.0 | 241.0 | 155.0 |
| 3 | GPT-5.6-Sol | 67.7 | 71.7 | 65.5 | 74.7 | 60.7 | 15.7% | 44.9 | 39.9 | 44.0 |
| 4 | DeepSeek-V4.1-Flash | 65.7 | 66.0 | 65.5 | 72.0 | 59.4 | 11.7% | 171.0 | 209.0 | 168.0 |
| 5 | Qwen3.8-Max | 60.6 | 59.6 | 61.1 | 65.9 | 55.3 | 10.3% | 75.1 | 90.6 | 72.8 |
| 6 | GLM-5.3-Flash | 59.7 | 63.1 | 57.8 | 64.8 | 54.4 | 6.28% | 102.0 | 145.0 | 101.0 |
| 7 | Grok-4.6 | 57.0 | 60.0 | 55.4 | 61.4 | 52.7 | 6.73% | 93.4 | 120.0 | 89.8 |
| 8 | Opus-4.8 | 57.0 | 58.6 | 56.1 | 60.2 | 53.7 | 5.38% | 97.7 | 164.0 | 95.6 |
| 9 | Seed2.1pro-0915 | 51.3 | 54.7 | 49.5 | 54.9 | 47.7 | 3.59% | 196.0 | 122.0 | 194.0 |
| 10 | Qwen3.8-27B | 47.7 | 46.1 | 48.6 | 50.0 | 45.5 | 1.35% | 90.0 | 112.0 | 87.4 |
| 11 | Kimi-K3 | 46.5 | 41.3 | 49.4 | 47.9 | 45.2 | 1.79% | 60.5 | 54.3 | 58.3 |
| 12 | Gemini-3.8-Flash | 34.2 | 35.9 | 33.2 | 29.8 | 38.5 | 0.45% | 56.6 | 35.9 | 54.5 |
| 13 | MiniMax-M3 | 31.8 | 34.1 | 30.6 | 28.9 | 34.7 | 0.45% | 132.0 | 72.2 | 127.0 |

**三条可直接引用的读数**：
1. **即使最强的 GPT-6-Astra，也只在不到一半（42.2%）的任务上通过全部 rubric 判据。** 项目页原话：「Even the leading model passes every criterion on fewer than half of all tasks.」
2. **Astra 在多模态输入（图/视频）上领先 Opus-5 +8.6 分**（80.7 vs 72.1）；而在纯文本任务上 **Opus-5 反而更高（74.8 vs 78.6 → 差 3.8，是 Astra 领先最小的一格）**，Opus-5 是 13 个模型里唯一 **Text > MM** 幅度明显的头部模型（74.8 vs 72.1）。
3. **成本结构差一个量级**：Astra 45.6 turns / 84.5K tokens 拿 79.9，Opus-5 要 **158 turns / 241K tokens** 才拿 73.0（**3.5 倍轮数、2.9 倍 token，分数反而低 6.9**）；最费的 Seed2.1pro 196 turns 只拿 51.3。
4. **Rubric 与 Dimension 的分化**：Gemini-3.8-Flash 的 Dimension(38.5) **高于** Rubric(29.8)，MiniMax-M3 同样（34.7 > 28.9）—— 弱模型「画面看着还行但要求没满足」，而头部模型是 Rubric 远高于 Dimension（Astra 87.3 vs 72.6）。**这正是 50:50 加权要防的那件事。**

**Astra 的 9 个 category 分项**（供「哪类最难」用）：Procedural & Game Assets 86.8 > Products & Manufacturing 83.9 > Science & Visualization 81.9 > Architecture & Interiors 81.3 > Vehicles & Machinery 80.9 > Characters & Animals 78.7 > Nature & Landscapes 78.4 > **Art & Animation 76.8** > **Rendering & Simulation 71.1（最难）**。
→ **「Art & Animation」和「Rendering & Simulation」是最弱两格，正好是 Video 章关心的动态维度。**

#### GitHub 侧元信息
136 star、5 fork、1 watcher、`main` 上 6 个 commit；创建 **2026-10-14**，最后推送 **2026-10-16**。**很新，star 数会快速变，引用必须带日期。**

---

### 3.2 3jsbench.com/methodology

**抓取状态：⚠️ WebFetch 失败 / curl + JS bundle + 数据文件解析成功。抓取时间 2026-10-19。**

| 方式 | 结果 |
|---|---|
| `WebFetch https://3jsbench.com/methodology` | ❌ **失败** —— 只拿到 `<title>`，无正文（React SPA，HTML 只有 `<div id="root">` 骨架，2,072 字节） |
| `curl https://3jsbench.com/methodology` | ⚠️ HTTP 200 但只有 2,072 字节骨架 |
| `curl /assets/main-DpGvyVm6.js`（677,482 字节） | ✅ **成功** —— methodology 正文、六族定义、失败统计、榜单数据全在 bundle 里 |
| `curl /data/benchmark.json`（630,272 字节） | ✅ **成功** —— 100 任务的逐条 checks，可自行统计 |

> 方法说明：和本地核验笔记一样，直接抓 HTML 只有骨架。本次没用无头浏览器，而是**抓 JS bundle + 数据文件，自行统计**，所以下面的 check 计数是**从原始数据重算出来的**，不是读页面文字。

#### 方法论原文（从 bundle 提取，4 步）
1. 「A model receives a written brief and writes a Three.js program.」
2. 「The program runs in an **isolated headless browser**, which records its scene and renders **nine fixed views**.」
3. 「Checks make **deterministic measurements** on the captured Three.js scene: part geometry, literal text, visible backfaces and draw-order flicker. **A mapper model only links the parts named in the task to the scene's meshes.**」
4. 「**An attempt passes only when every required check passes.** Advisory diagnostics do not affect the grade, and attempts lost to infrastructure failures are excluded.」

榜单口径原文：「The benchmark is a collection of **100** tasks. Each model makes **three one-shot attempts** at every task **at high reasoning**, and the verifier suite grades each attempt **pass / fail / unverified**（no check failed, but one could not be measured）. Pass rate is the share of attempts that pass; its ± is a **95% interval that treats attempts as independent**. **Tasks solved (pass@3)** counts the tasks with at least one passing attempt.」

#### 六族必查项（族定义取自 bundle 的 `So` 数组，计数由 `benchmark.json` 重算）

| 族 | key | 查什么（原文） | 必查条数 | 覆盖题数 |
|---|---|---|---|---|
| 部件计数 | counts | The number of bound instances of each required part | **223** | 100 |
| 结构 | structure | Connections and clearance between parts, within each check's tolerances | **160** | 84 |
| 空间关系 | relations | Contacts, support, angles and positions specified for the task | **157** | 52 |
| 任务专属几何 | geometry | Task-specific geometry that a shared check cannot measure | **45** | 35 |
| 文字 | text | Visible lettering against the task's text requirements | **12** | 10 |
| 渲染质量 | render | Mesh budgets, visible backfaces and changes caused by draw order | **98** | 98 |
| **六族合计** | | | **695** | |

每族包含的 check kind（可直接抄的判据清单）：
- **counts**：`count`
- **structure**：`objects-connected`(80)、`objects-clear`(63)、`surfaces-clear`(11)、`scene-connected`(3)、`assemblies-attached`(1)、`ends-attached`(1)、`details-clear`(1)
- **relations**：`connected`(56)、`touching`(32)、`clear`(17)、`grounded`(14)、`tilt`(7)、`supported`(7)、`top-support`(7)、`contact`(5)、`atRim`(4)、`openTop`(3)、`scene-grounded`(2)、`hanging-by`(1)、`seated`(1)、`alignedBelow`(1)
- **geometry**：`geometry-kernel`(36)、`scene-aspect`(7)、`awning-slope`(1)、`partAspect`(1)
- **text**：`text-literal`(12)
- **render**：`surface-budget`(98)

示例（bundle 原文）：counts「A chest body and one lid. Three bells on a jester hat.」；structure「A frog's legs attach to its body. A sword's blade does not cut into the shield it leans on.」；relations「A lid propped open. A frog resting on a leaf. A lantern hanging from a hook.」；geometry「The ends of a chest lid are closed. An awning slopes down and away from the wall.」；text「SHOW TONIGHT on a marquee. Soup of the Day: Tomato on a chalkboard.」；render「No inside faces showing through, and no flicker when the draw order changes.」

**一个任务的完整 check 列表示例**（`benchmark.json` 原始记录，`capx-001-make-a-dungeon-treasure-chest-with-its-lid-propped-open`）：
```json
{"prompt":"Make a dungeon treasure chest with its lid propped open.",
 "parts":["chest-body","lid","lid measurement scope"],
 "checks":[{"id":"count-chest-body","kind":"count","required":true},
           {"id":"count-lid","kind":"count","required":true},
           {"id":"key-objects-clear","kind":"objects-clear","required":true},
           {"id":"key-objects-connected","kind":"objects-connected","required":true},
           {"id":"verifier-chest-lid-closed-ends","kind":"geometry-kernel","required":true},
           {"id":"verifier-mesh-count","kind":"surface-budget","required":true},
           {"id":"relation-001","kind":"openTop","required":true}],
 "category":"Assemblies","tier":"detailed"}
```
→ **一个任务 7 条必查项，六族里命中五族。** 平均每任务 **6.95 条必查项**（695/100）。

#### 任务分层 / 分类
- `benchmark.json` 里 100 个任务 **tier 全部是 `detailed`**（无 simple/detailed 混合）；但部分任务 key 带 `capx-simple100--NNN` 前缀（如 `capx-simple100--039-make-a-bunk-bed`），**说明题库来源有「simple100」这一批，当前发布的 100 题统一按 detailed tier 判**。
- category 三类：**Objects & geometry 45 / Assemblies 44 / Text & symbols 11**。
- 部件总数 **326 个**（100 题的 `parts` 之和，平均每题 3.26 个被绑定部件）。
- **「分层」的真正含义是判据的乘法门控，不是题目难度分层**：必查项全过才算 pass，advisory 诊断不影响判定，基础设施故障的尝试单独排除。

#### 榜单（**和本地笔记有出入，见下**）
bundle 里有三块榜单数据，合起来 13 个模型：
- `benchmark.json`（release `five-models-convex-20260923`，`verifiedAt` **2026-09-23T22:44:09Z**，`status: Beta`）：astra / fable / grok47 / grok / inkling。
- bundle 内嵌 `w9` 数组：opus55 / sol6 / kimik3 / musespark13 / gemini38flash / inkling。
- bundle 内嵌 `z9` 数组：musewonder / gemini4argon / hy4preview。

| 模型 | 通过率 | 通过/总数 | pass@3（tasksWithPass） | 全三次都过 | infra 排除 | withheld |
|---|---|---|---|---|---|---|
| Astra（OpenAI GPT-6-Astra） | **80.0%** | 240/300 | — | — | 0 | 11 |
| Fable 5.1（Anthropic） | **69.3%** | 208/300 | — | — | 0 | 5 |
| **Opus 5.5（Anthropic）** | **49.0%** | **147/300** | **75/100** | 23 | 0 | 11 |
| GPT-6 Sol | 27.0% | 81/300 | 50/100 | 8 | 1 | 14 |
| Kimi K3 | 23.0% | 69/300 | 49/100 | 4 | 21 | 11 |
| Grok 4.7 | 22.0% | 66/300 | — | — | 0 | 8 |
| Muse Wonder（Meta） | 18.7% | 56/300 | 39/100 | 5 | 0 | 9 |
| **HY4 Preview（Tencent）** | **18.0%** | **54/300** | **41/100** | 1 | 0 | 6 |
| Grok 4.6 | 13.7% | 41/300 | — | — | 0 | 2 |
| **Gemini 4 Argon（Google）** | **11.0%** | **33/300** | **27/100** | 1 | 3 | 9 |
| **Muse Spark 1.3（Meta）** | **10.67%** | **32/300** | 23/100 | 1 | 3 | 6 |
| Gemini 3.8 Flash | 8.67% | 26/300 | 21/100 | 0 | 5 | 10 |
| **Inkling（Thinking Machines）** | **2.0%** | **6/300** | 6/100 | 0 | 4 | 13 |

> ⚠️ Inkling 在 `benchmark.json`（9-23 convex release）里是 16/297 = 5.39%，在 bundle 的当前 `w9` 里是 6/300 = 2.0%。**两处口径不同，引用用 bundle 的当前值 2.0%。**

**改判记录**（bundle 的 `amendment` / `amendments` 字段，这是本地笔记没有的）：
- `3jsbench.rule-fixes.2026-10-14`（本地笔记记到了这一次）
- `3jsbench.task-reviews.2026-10-16` ← **新增**
- `3jsbench.avocado-reviews.2026-10-16` ← **新增**

**失败模式（3,000 次尝试，bundle 原文）**：intersecting objects **20%**、see-through surfaces **19%**、flickering surfaces **17%**、parts not oriented according to the brief **16%**、disconnected parts **16%**。

**模型行为（bundle 原文）**：
- Muse Spark 1.3「builds the heaviest objects: a median of **995 meshes and 177,000 triangles**」；**Inkling 951 meshes**；**Astra 45**、**Fable 5.1 just 24**。Muse Spark 有 **33%** 的尝试 flicker，高于任何模型。
- Gemini（3.8 Flash）**在 300 次里有 55 次**把程序包进没要求的 Markdown 代码围栏；grader 会剥掉围栏再判，**但这 55 次只有 1 次通过**。Gemini 的 see-through surfaces 比例 **54%**、inside-out meshes **14%**，均为最高。
- 另有一个模型「has disconnected parts in **37%** of its attempts」（bundle 里该句的模型名在 JSX 变量里，**未核实是哪个模型**）。

**SigLIP2 相似度（bundle 原文）**：渲染场景与 brief 的 SigLIP2 嵌入余弦，**在九个固定视角上取平均；九个视角都要打上分，这次尝试才有值**。「This is a **descriptive image signal**. It **does not establish geometric correctness or change a grade**.」pinned SigLIP2 base checkpoint 用 224 px 图 + uint8 ONNX 推理；**40 次尝试的跨 runtime 比较发现差异最大 0.005**。榜单图里减去每题均值作归一。Opus 5.5 的 SigLIP2：mean **0.1067**、relative **+0.0092**、95% CI [0.0073, 0.0109]；Fable mean 0.100、relative +0.0024、CI [0.0006, 0.0043]。

**第三类信号：人类成对偏好（本地笔记没有记，补）**：Instaplay 登录创作者对同一 brief 的两个可交互资产做成对比较，可选任一方、平局，或标记两个都差。模型名隐藏、左右随机、优先展示「被比较次数最少」的配对。投票拟合成 **Bradley-Terry / Elo** 评分，平局算各半胜；**加载失败的对象不参与评分**；区间由**重抽样整个评分者**得到。采集两组：**展示 prompt 的**（可把贴合度算进判断）与**不展示 prompt 的**（纯审美），overall 对两组拟合同一个评分。榜单 Arena 评分从外部拉取：`https://www.instaplay.ai/api/public/3jsbench/arena-ratings.json`。

**成本（bundle `Yo` / `Go` 表，mean USD/次尝试）**：Fable 5.1 **$1.2822**（126 次计价）> Astra **$0.8031**（126）> Grok 4.7 **$0.6509** > Gemini 4 Argon **$0.3476** > Muse Wonder **$0.3441** > **Opus 5.5 $0.3099** > Kimi K3 $0.2979 > Grok 4.6 $0.1931 > Gemini 3.8 Flash $0.1265 > Muse Spark 1.3 $0.1141 > GPT-6 Sol $0.1057 > Inkling $0.048。**Opus 5.5 的单次成本只有 Fable 5.1 的 24%，通过率 49.0% vs 69.3%。**

**溯源**：`sourceUrl` 指向 `https://github.com/GeneralContext/instaplay-assets-evals/blob/3b7c7332.../evidence/threejag/releases/five-models-convex-20260923.json`；联系邮箱 `research@generalcontextlabs.com`。选择策略：Grok 4.7 取 `first-non-timeout`，其他模型取 `saved historical rollout`，每题取 `first three attempts by attempt number`；Grok 4.7 的选中轮次分布为 turn1 **265**、turn2 **33**、turn3 **2**。排除的 5 次尝试全是 Grok 4.6 在 `capx-simple100--039-make-a-bunk-bed` 上的 attempt 4–8。

#### ⚠️ 与本地核验笔记 `91_3jsbench_verified.md`（2026-10-15）的逐项对照

| 项 | 本地笔记（2026-10-15） | 2026-10-19 实抓 | 判定 |
|---|---|---|---|
| 必查项总数 | **695 条** | **六族合计 695**（必查项 `required:true` 总数 **696**，差的 1 条是 `flatFace`，不属任何族） | ✅ **本地正确**；⚠️ 但页面渲染的那句话用的是 `required` 总数，即显示 **696**，不是 695。**正文最好写「695 条分入六族，另 1 条不入族，合计 696 条必查项」** |
| 六族分布 | 223 / 160 / 157 / 45 / 12 / 98 | **223 / 160 / 157 / 45 / 12 / 98** | ✅ **逐族完全一致** |
| 覆盖题数 | 100 / 84 / 52 / 35 / 10 / 98 | **100 / 84 / 52 / 35 / 10 / 98** | ✅ 完全一致 |
| Astra 通过率 | 80.0% ±4.5，240/300，pass@3 96/100 | **80.0%，240/300** | ✅ 一致 |
| Fable 5.1 | 69.3% ±5.2，208/300 | **69.3%，208/300** | ✅ 一致 |
| **Opus 5.5** | **49.0% ±5.7，147/300，pass@3 75/100** | **49.0%，147/300，tasksWithPass 75/100** | ✅ **完全一致** |
| GPT-6 Sol | 27.0%，81/300，50/100 | **27.0%，81/300，50/100** | ✅ 一致 |
| Kimi K3 | 23.0%，69/300，49/100 | **23.0%，69/300，49/100** | ✅ 一致 |
| Grok 4.7 / 4.6 | 22.0% 66/300 / 13.7% 41/300 | **22.0% 66/300 / 13.7% 41/300** | ✅ 一致 |
| Muse Wonder | 18.7%，56/300，39/100 | **18.7%，56/300，39/100** | ✅ 一致 |
| **Muse Spark 1.3** | **10.0%，30/300，22/100** | **10.67%，32/300，23/100** | ❌ **有出入**。本地记的是 10-14 改判后的值；10-16 又有两次改判（`task-reviews` / `avocado-reviews`），**多过了 2 次、多解出 1 题** |
| Gemini 3.8 Flash | 8.7%，26/300，21/100 | **8.67%，26/300，21/100** | ✅ 一致 |
| **榜单模型数** | **10 个** | **13 个** | ❌ **本地缺 3 个**：**HY4 Preview（Tencent）18.0% 54/300**、**Gemini 4 Argon（Google）11.0% 33/300**、**Inkling（Thinking Machines）2.0% 6/300** |
| 改判记录 | 只记「Amended 14 October 2026」一次 | **三次**：`rule-fixes.2026-10-14`、`task-reviews.2026-10-16`、`avocado-reviews.2026-10-16` | ❌ **本地缺 10-16 的两次改判** |
| 失败模式五项 | 20/19/17/16/16% | **20/19/17/16/16%** | ✅ 完全一致 |
| Mesh 预算 | Muse Spark 中位 995 mesh / 177,000 三角面；Inkling 951；Astra 45；Fable 24；Muse Spark 33% flicker | **逐字一致** | ✅ |
| Gemini 代码围栏 | 300 次里 55 次，只有 1 次通过 | **逐字一致** | ✅ 另补到：Gemini see-through 54%、inside-out 14%，均最高 |
| SigLIP2 | 标为「描述性图像信号，不确立几何正确性，不改变判定」；Astra +0.011 / Opus 5.5 +0.009 / Sol +0.007 | **定性结论一致**；**Opus 5.5 relative 实测 +0.0092**（本地四舍五入 +0.009，✅）；**补充：pinned checkpoint 224 px + uint8 ONNX，跨 runtime 差异最大 0.005；九视角全部要打分才有值** | ✅ 一致，可补细节 |
| 九视角 | 「记录场景并渲染九个固定视角」 | **"records its scene and renders nine fixed views"** | ✅ 一致 |
| mapper 模型 | 「用一个 mapper 模型把题面里点名的部件绑到场景的 mesh 上」，LLM 只绑定不打分 | **"A mapper model only links the parts named in the task to the scene's meshes"** | ✅ 一致 |
| 乘法门控 | 「只有全部必查项通过才算过」 | **"An attempt passes only when every required check passes"** | ✅ 一致 |
| 口径状态 | 「榜单是站方维护的，不是论文，没有同行评议；改判发生过一次，说明判据本身还在动」 | **`status: "Beta"`；改判已发生三次** | ⚠️ **本地结论方向正确但低估了变动频率**。四天内又改了两次 → **引用必须带日期，且最好不引细到小数点的弱模型数字** |
| 本地笔记里的历史口径 | 「之前笔记里写的 743 条确定性几何检查与当前页面不符，当前值是 695 条必查项」 | `benchmark.json` 里**全部 check（含非必查）共 744 条**（required 696 + 非必查 48） | ✅ **本地的更正是对的，而且找到了 743/744 这个旧数字的来源 —— 那是「含 advisory 的全部 check 数」，不是「必查项数」。两个数都真实，口径不同。正文可以写：744 条 check，其中 696 条必查（695 条分入六族），48 条是不影响判定的 advisory。** |
| 本地没记的第三类信号 | — | **人类成对偏好 Arena（Bradley-Terry / Elo，prompt 组 + 无 prompt 组）** | ➕ **补充项** |
| 本地没记的成本表 | — | **每次尝试均价：Fable $1.2822 / Astra $0.8031 / Opus 5.5 $0.3099 / Inkling $0.048 等** | ➕ **补充项** |

**总评：本地核验笔记的核心数字（695 六族分布、Astra 80.0%、Opus 5.5 49.0%、失败模式、mesh 预算、SigLIP2 无区分度）全部对得上，质量很高。三处要修**：① 榜单从 10 个模型扩到 13 个（补 HY4 Preview / Gemini 4 Argon / Inkling）；② Muse Spark 1.3 从 10.0%(30/300) 改为 10.67%(32/300)；③ 改判从 1 次变 3 次（新增 2026-10-16 两次）。另加一条口径澄清：**744 条 check = 696 必查 + 48 advisory，695 是分入六族的必查项数**。

**本地笔记里「它的管线 vs 本项目原型」那张对照表（7 行），本次实抓没有发现任何需要推翻的地方**，唯一的结构差异仍是「mapper 模型做部件绑定」—— 本地标注「值得抄的折中：LLM 只负责哪个 mesh 是题面说的那个盖子，判定仍然是确定性的」，这句现在有了原文背书。

---

### 3.3 happycapy.ai/models/qwen-3.8

**抓取状态：✅ 抓到了，但内容对「3D 资产质量评测/打分」几乎无用。抓取时间 2026-10-19。**
URL：https://happycapy.ai/models/qwen-3.8

- **这个页面是什么**：Happycapy 给阿里 **Qwen 3.8 Max** 做的**营销落地页** —— 产品文案 + FAQ + 嵌入的 X（Twitter）社区帖。**不是技术报告，不是 3D 资产评测。**
- **关于 3D 资产质量评测的内容**：
  - ❌ **没有任何 rubric 或评分方法**（不定义几何、拓扑、贴图、渲染保真的判据）。
  - ❌ **没有逐资产分数或指标**。质量说法全是定性的，如「real shading」「orbit controls」「no manual edits」。
  - ⚠️ **唯一一个数字基准**：一张「Score Index across 10+ Benchmarks」复合指数图 —— **SFT 基线 0.474，最佳 checkpoint 升到约 0.725**，之后末期略有回落。**但基准名称未列出，这个指数也不是 3D 专用的。**
  - 社区帖轶事：一位用户称 Qwen 3.8 Max 在一个 **Three.js** 任务上**成本约为 Kimi K3 的一半**；另一位称两个模型都**零样本**写出正确 shader，但 **Qwen 用的 token 多得多**。
  - 代码体量：一个帖子引用了「约 **35k 行**、不用任何库」的太阳系项目 —— **这是输出量，不是质量**。
  - 主观评价：有帖子称它是「the first non-Claude model with this level of taste」—— 观点，非测量。
  - 社区报价：输入约 **$2 / 百万 token**，输出约 **$6 / 百万 token**。
- **缺口**：页面**无方法论、无样本量、无基准名、无日期**，大部分质量说法来自营销文案或社交帖，**无法从该页独立核实**。
- **结论：这条链接不适合作为「3D 资产质量评测」的出处。**唯一可引用的是「0.474 → 0.725 复合指数」，而且必须注明是厂商/第三方营销页上的无名复合基准。若 Video 章需要 Qwen3.8 的 3D 分数，**改用 BlenderWorld 榜单**（Qwen3.8-Max 60.6 / Qwen3.8-27B 47.7，见 §3.1），那是有完整方法论的。

---

### 3.4 小红书笔记里的 4 个开源项目（不抓笔记，直接记录 + GitHub 核实）

**核实方式与时间**：GitHub REST API（`/repos/{owner}/{repo}` 与 `/search/repositories`）+ raw README，**2026-10-19**。

| # | 笔记里的名字 | 笔记里的描述 | GitHub 核实 | star（2026-10-19） | 许可 | 状态 |
|---|---|---|---|---|---|---|
| 1 | **Lemon Opuscar** | 39 种影片风格，带提示词和示例短片 | ✅ **`lemomo-ai/lemo-opuscar`** | **3,405**（fork 376） | **MIT · CC BY 4.0** | ✅ 核实；⚠️ **「39 种」已过期，README 现为 51 种** |
| 2 | **Awesome Opus 5.5 Videos** | 热门视频附原始 prompt | ✅ **`yihui-dev/awesome-opus5-5-videos`** | **6,385**（fork 669） | **MIT** | ✅ 核实（最佳匹配，见下） |
| 3 | **PDM Video** | 音乐视频《I'm Upping My P(doom)》完整源码、故事板、渲染脚本公开 | ⚠️ **两个同主题仓库，无法确定指哪个** | `mexicat/pdoom-video` **2,894**（MIT）/ `JohnHeibel/PDoomVideo` **2,212**（无许可） | 见左 | ⚠️ **部分核实，仓库归属未核实** |
| 4 | **Opus Video Prompts** | 54 个可复制提示词案例 | ✅ **`joeseesun/opus-video-prompts`** | **421**（fork 37） | **无许可声明** | ✅ 核实，**「54 个案例」与 README 完全对上** |

#### 逐条细节

**① Lemon Opuscar → `lemomo-ai/lemo-opuscar`**
- 创建 2026-09-26，最后推送 2026-10-18。许可 **MIT · CC BY 4.0**。
- 自述：**Claude Code skill**，做「没有视频模型的短片」。**51 种影片风格**，每种 = 一条风格提示词 + 一支纯代码样片。
- 旗舰作 **OPUSCAR 98**：1927–2025 **98 部奥斯卡最佳影片**，每部一种风格，片长 **6:31**；**98 种风格 = 77 个 2D + 4 个 2.5D + 17 个 3D**；提供机读 [`styles.json`](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/styles.json)、1080p mp4 release 下载。
- 2026-10-16 新增 **Evidence Films**：**8 种新风格**，主张「拍真实素材，每个数字可测量或有出处」。
- 技术栈自述：**画面 = canvas / WebGL 页面逐帧渲染；音乐 = 免费采样库原创配乐；旁白 = TTS。「No video generation, no stock footage.」**
- ⚠️ 作者明示：**风格是为 Claude Opus 5.5 调的，其他模型可能复现不出来。**
- ⚠️ 作者明示：**「Not an awesome list」** —— 每支片子都是作者本人做的，不是收录别人的。
- 本地 `pipe_meta_video.json` 记的是 **1.95k star**，现为 3,405 → **约一个月翻了 1.75 倍**。

**② Awesome Opus 5.5 Videos → `yihui-dev/awesome-opus5-5-videos`**
- **6,385 star / 669 fork / MIT**，创建 2026-09-27，最后推送 2026-10-13。
- 描述：「A growing collection of viral videos made with Claude Opus 5.5 and the prompts behind them. Watch each original next to a live remake on Skillry. Updated regularly.」→ **与笔记「热门视频附原始 prompt」完全吻合，且是同名仓库里 star 最高的，判定为该条。**
- ⚠️ **同名/近名仓库很多，引用时必须写全 owner**：`athemeroy/awesome-claude-5-5-videos` 553、`guanmo-ai/awesome-ai-motion` 389、`zhuyansen/awesome-opus-5.5-video` 211、`opusvideo/awesome-claude-video` 209、`chuspeeism/awesome-opus-5-5-videos` 108、`xianyu110/awesome-claude-opus-5.5` 70、`LeaddeOpenLab/awesome-opus-5-5-video-prompts` 59。

**③ PDM Video —— ⚠️ 仓库归属未核实**
- 候选 A：**`mexicat/pdoom-video`** —— **2,894 star / 322 fork / MIT**，创建 2026-09-24，最后推送 2026-10-05。描述「Code-rendered music video for "I'm Upping My P(doom)"」。**已成为一个「引擎」被二创**：`lycfyi/power-video`（Grimes《We Appreciate Power》，"on the pdoom-video engine"）、`amemiya02/pdoom-video-win95`、`nonunsaram/feel-the-agi-video`（three.js，"built on mexicat/pdoom-video"）。
- 候选 B：**`JohnHeibel/PDoomVideo`** —— **2,212 star / 230 fork / 无许可声明**，创建 2026-09-22（**更早**），最后推送 2026-09-25。描述「Source code for the Claude Opus 5.5 music video for I'm Upping My P(doom)」。**本地 `pipe_meta_video.json` 收录的是这一个**（标 p5.js、逐帧 MV mp4、2.0k star）。
- 还有一个 0 star 的 `yipingheijiang/PDoomVideo`（同描述，疑似 fork/镜像）。
- → **笔记说的「PDM Video」对应哪个，本次无法确定。正文若要写，建议写「`JohnHeibel/PDoomVideo`（本地素材库收录，p5.js，2,212 star，无许可）与 `mexicat/pdoom-video`（2,894 star，MIT，已被二创成引擎）两个同主题仓库」，并标「归属未核实」。**
- 笔记说的「完整源码、故事板、渲染脚本公开」—— **本次未逐文件核实这三样是否都在**，标**未核实**。

**④ Opus Video Prompts → `joeseesun/opus-video-prompts`**
- **421 star / 37 fork / 无许可声明**，创建 2026-09-27，**最后推送也是 2026-09-27**（**一次性快照，之后没再更新**）。
- README 自述口径（**比笔记更细，建议用这个**）：**18 份完整提示词 · 54 个公开案例 · 9 种技术路线 · 持续更新**。→ **笔记的「54 个可复制提示词案例」对上的是「54 个公开案例」。**
- 采集范围：**Opus 5.5 发布后第一周（2026-09-22 至 09-25）**，来源 X、B 站、Linux.do、GitHub、YouMind 等；**只收作者本人公开的提示词原文，每条附原帖链接**。
- ⭐ **README 里有一段对 From Web / From Blender 两条路线都极有价值的技术总结（原文）**：
  > 「Opus 5.5 本身**不输出视频文件**。它的做法是写代码画出每一帧：**HTML Canvas、p5.js、Three.js、Remotion、Manim、Blender 脚本**都有人用。然后用**无头浏览器逐帧截图，再用 FFmpeg 合成 MP4**；配乐一般用 **Web Audio 或 Python 合成**，旁白接 **TTS**。所以它擅长**动态图形、手绘/线稿/水墨动画、科普讲解、产品发布片、歌词 MV**，不擅长写实的真人镜头。真要写实画面，常见做法是让它调用 **Seedance、Runway、Higgsfield** 这类视频模型，自己负责编排和剪辑。」
  → **这是本次抓到的唯一一处把「Blender 脚本」明确列入社区实际技术路线的素材**，但它**只是一句枚举，没有具体项目**。
- 上手口径：「装好 Claude Code，模型切到 Opus 5.5，**effort 调到 high / xhigh**；本机准备 **Node.js、Chrome、FFmpeg**」。
- 最短测试提示词（作者注：Deedy 用它做出了发布片，**约 1 分钟、2 美元**）：`make a modern slick and punchy video for a modern startup that works on inference`。

---

## 4. 量化数字清单

> 格式：数字 → 说明什么 → 出处。`[本地 X]` = 本地文件；`[网页 2026-10-19]` = 本次实抓。

### 4.1 From Web · 确定性与渲染成功率

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **100% vs 86.2%** | VAnim 的渲染成功率 vs 基线 —— 二值判据上的最大落差 | `[本地 deep_video.md]` |
| **88.3% vs 12.7%** | OmniLottie（带 Lottie tokenizer）vs GPT-5 直吐裸 JSON 的 Text-to-Lottie 成功率 —— 「紧凑表示是制胜招」的核心证据 | `[本地 deep_video.md]` |
| **93.3%** | `bench_meta` 记录的 OmniLottie 矢量动画成功率 —— ⚠️ **与 deep_video 的 88.3% 不一致** | `[本地 bench_meta_video.json]` |
| **88.3% vs 97.3%** | OmniLottie 成功率在正文与附录间的自相矛盾 | `[本地 deep_video.md]` |
| **2,562 → 486 token（省 81%）** | Lottie tokenizer 对单条样本的压缩 | `[本地 deep_video.md]` |
| **9.86 倍 / 86.0k → 9.2k token** | VAnim 稀疏状态更新对 24 帧序列的压缩 | `[本地 deep_video.md]` |
| **93.8%** | o3-mini (medium) 在 TheoremExplainBench 上的渲染成功率（最高） | `[本地 deep_video.md]` |
| **2.1%** | Claude-3.5-Sonnet 在 TheoremExplainBench 上的成功率（总分 0.79 却几乎跑不起来）—— 「能跑」与「做对」是两件事 | `[本地 deep_video.md]` |
| **5 次重试 → 九成** | TheoremExplainAgent 的报错自纠：不重试成功率极低，重试 5 次可达九成 | `[本地 deep_video.md]` |
| **6.7%** | Keyframer 生成的 CSS 动画代码里有语法错误的比例 | `[本地 deep_video.md]` |
| **3/3 全不同 → 3/3 逐字节一致** | 本机 Chrome headless 确定性阶梯：不控制 vs 页面 `setTime` 钩子 + `canvas.toDataURL` 直读 | `[本地 06_harness.md]` |
| **20 次里 2 种（11/9）** | `clock.install + pauseAt + runFor(1500)` + 种子 random 的残余方差，推测 rAF 帧相位差一帧 | `[本地 06_harness.md]` |
| **113–432 ms** | 只调 `clock.install` 时漏进 `performance.now` 的加载耗时波动 | `[本地 06_harness.md]` |
| **约 0.2 s** | 本机 8 视角 three.js 转台耗时（纯 CPU，SwANGLE） | `[本地 06_harness.md]` |
| **14.3 任务/s** | 8 浏览器 × 8 页的稳态吞吐（p50 4.1 s / p95 4.9 s） | `[本地 06_harness.md]` |
| **1/8** | contact sheet 相对逐张发图的 token 成本 | `[本地 06_harness.md]` |
| **552 MB / 65 MB** | `chrome-linux64` 目录 / `node_modules` 体积 | `[本地 06_harness.md]` |

### 4.2 From Web · 评测有效性（哪些判据可信）

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **−0.17** | ManimAgent 实测其 VLM 判官与人评的相关系数 —— **VLM 打分不能做主指标**的最硬证据 | `[本地 deep_video.md]` |
| **0.72 / 0.42 / 0.14 / 0.16** | TheoremExplainAgent 自动指标与人评的相关：视觉相关性 / 元素布局（显著）/ 准确深度 / 逻辑流（近乎无关） | `[本地 deep_video.md]` |
| **40.0 → 86.0** | TeachQuiz：Claude Opus 4.1 从直接写码到 Code2Video 闭环的知识传递量 | `[本地 deep_video.md]` |
| **97.1 / 2.5 / 0.0** | TeachQuiz 对照：人类 3Blue1Brown / 扩散基线 Veo3 / OpenSora-v2 —— **扩散视频在知识传递上几乎归零** | `[本地 deep_video.md]` |
| **37.8 → 87.9（人类 99.7）** | Code2Video 的 VLM 观感均分 | `[本地 deep_video.md]` |
| **0.842 / 0.951 vs 人类 0.738 / 0.908** | Paper2Video 的 PresentQuiz 超过论文作者本人 | `[本地 deep_video.md]` |
| **17.0%（人类 50%）** | 同一个 Paper2Video 在 PresentArena 成对胜率只有 17% —— **答题式指标超人类而观感仅 17%，是指标口径背离的典型** | `[本地 deep_video.md]` |
| **0.57–0.73** | TheoremExplainBench 各模型的元素布局得分区间 —— 版式是普遍弱项 | `[本地 deep_video.md]` |
| **0.82 / 33.8 / 12.6** | Vector Prism 的聚类 Davies–Bouldin 指数 vs 原始 SVG vs 多数投票 | `[本地 deep_video.md]` |
| **76.1 vs 69.1** | Vector Prism 的 GPT-T2V 保真 vs Sora 2 | `[本地 deep_video.md]` |
| **83.4% vs 53.4%** | GPT-T2V 与人评一致率 vs CLIP-T2V —— **CLIP 类指标与人评基本脱钩** | `[本地 deep_video.md]` |
| **54 倍** | Vector Prism 矢量输出文件体积比 Sora 2 视频小（⚠️ 是相对视频基线的体积优势，不是压缩比） | `[本地 deep_video.md]` |
| **0.84 vs 0.31** | Animation2Code 的 Appearance 最高分 vs Temporal 最高分 —— **时间维度是全行业最弱的一格** | `[本地 07_capability_spec.md]` |
| **0.945 vs 0.572，平均掉 41.24 点** | PRISM 的 Exec 最高 vs Spatial 最高（95% CI [40.41, 42.11]）—— **只报执行率的指标没有信息量** | `[本地 07_capability_spec.md]` |
| **214 题 / 1,069 条 / 86% 纯 CSS / 1024×768@30fps / 83.9%** | Animation2Code 的规模、构成、确定性渲染配置、与人类偏好一致率 | `[本地 07_capability_spec.md]` |

### 4.3 From Web · 规模与成本

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **约 200 万条** | MMLottie-2M 数据集规模（本章最大的公开矢量动画数据集） | `[本地 deep_video.md]` |
| **900 条（真 450 + 合成 450）** | MMLottieBench 规模 | `[本地 deep_video.md]` |
| **134k（SFT 123k / RL 10k / 测试 1k）** | SVGAnim-134k 切分 | `[本地 deep_video.md]` |
| **700 条** | DCG-Bench 测试规模（唯一的动画图表代码基准） | `[本地 bench_meta_video.json]` |
| **114 对** | Vector Prism 测试集（纯测试集，无训练数据） | `[本地 bench_meta_video.json]` |
| **102 任务** | DTVBench · JanusCoder（Manim 引擎） | `[本地 bench_meta_video.json]` |
| **约 50 任务 / Lottie FrameSSIM 仅 0.598** | Graphic-Design-Bench 的动画轴 —— **动画远难于静态** | `[本地 bench_meta_video.json]` |
| **1,825 任务 / 排名一致 94.4%** | ArtifactsBench 规模与与 WebDev Arena 的排名一致率（时序截图捕动态） | `[本地 bench_meta_video.json]` |
| **13.8 分钟 / 43.1K token** | Code2Video 每主题成本（比直接写码慢 5–8 倍、多耗 15–20 倍 token） | `[本地 deep_video.md]` |
| **287 → 48 分钟** | Paper2Video 逐页并行把单条耗时压下来；总成本约 48 分钟 / 62K token | `[本地 deep_video.md]` |
| **约 31 秒，快 52–530 倍** | OmniLottie 单条生成耗时 vs 优化法 | `[本地 deep_video.md]` |
| **62.0 → 84.9 / 12.2 → 6.5 / 3.26 → 3.88** | ManimAgent 记忆库 0 → 200 条：一次通过率 / 反思轮数 / 人评质量；乱序记忆退回 69.6 | `[本地 deep_video.md]` |
| **94.9k / 63.4k / 61.2k / 41.5k / 21.4k / 19.3k / 0.7k star** | manim(3b1b) / Remotion / HyperFrames / Manim Community / Hypit / Motion Canvas / ranim 的采用度 | `[本地 pipe_meta_video.json]` |
| **3,405 / 2,212 / 6,385 / 421 star** | lemo-opuscar / JohnHeibel-PDoomVideo / awesome-opus5-5-videos / opus-video-prompts | `[网页 2026-10-19 GitHub API]` |
| **51 种风格 / 98 部影片 / 6:31 / 77+4+17** | Lemo-Opuscar 的风格数、OPUSCAR 98 的片目数、片长、2D/2.5D/3D 构成 | `[网页 2026-10-19 README]` |
| **18 份提示词 / 54 个案例 / 9 种技术路线** | `joeseesun/opus-video-prompts` 的自述规模 | `[网页 2026-10-19 README]` |
| **约 1 分钟 / 2 美元** | 社区报告的「一句提示生成发布片」成本（Deedy） | `[网页 2026-10-19 opus-video-prompts README]` |

### 4.4 From Blender

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **223 / 2,651 / 9 / 22** | BlenderWorld 的任务数 / 二值 rubric 判据数 / category 数 / subcategory 数 | `[网页 2026-10-19 README + HF]` |
| **78 / 130 / 15（多模态 145）** | BlenderWorld 输入模态拆分：文本 / 图像+文本 / 视频+文本 | `[网页 2026-10-19]` |
| **59** | 带规格附件（尺寸/材质/相机）的任务数 | `[网页 2026-10-19]` |
| **213 / 223** | 11 个最大应用场景的覆盖 | `[网页 2026-10-19]` |
| **8 视角 / 1024×1024 / 64 samples / 最多 2 次纠正重渲** | BlenderWorld 渲染 agent 的确定性配置 | `[网页 2026-10-19 README + evaluation.md]` |
| **权重 1/2/3；Final = 0.5×Rubric + 0.5×Dimension；Dimension = 10 × mean(8 项 1–10)** | BlenderWorld 的打分公式 | `[网页 2026-10-19 README]` |
| **82.99%（122/147）** | BlenderWorld 主判官与多数人类偏好的一致率（150 对同输入、3 名评审、3 对无多数被排除） | `[网页 2026-10-19 项目页]` |
| **79.9 / 42.2% / +8.6** | GPT-6-Astra 的 overall 最高分 / 全 rubric 通过率 / 在多模态输入上领先 Opus-5 的点数 | `[网页 2026-10-19 leaderboard.json]` |
| **Opus-5 73.0（Rubric 80.9 / Dim 65.1 / Full pass 25.6%）** | BlenderWorld 第 2 名 | `[网页 2026-10-19 leaderboard.json]` |
| **45.6 turns / 84.5K tokens vs 158 turns / 241K tokens** | Astra vs Opus-5 的每任务成本 —— **3.5 倍轮数、2.9 倍 token，分数反而低 6.9** | `[网页 2026-10-19 leaderboard.json]` |
| **Art & Animation 76.8 / Rendering & Simulation 71.1** | Astra 九个 category 里最弱的两格，正是 Video 章关心的动态维度 | `[网页 2026-10-19 leaderboard.json]` |
| **617 MB / 2,422 次月下载 / 24 likes / MIT** | BlenderWorld 的 HF 包体积、采用度与许可 | `[网页 2026-10-19 HF]` |
| **136 star / 5 fork / 6 commit / 创建 2026-10-14** | BlenderWorld 的 GitHub 元信息（**很新，引用必须带日期**） | `[网页 2026-10-19 GitHub API]` |
| **Blender 4.2.10 / Node 22.17.0 / Codex CLI 0.147.0 / Claude Code 2.1.220 / MCP for Blender 2.1.3** | BlenderWorld 的环境钉版（版本不匹配直接中止） | `[网页 2026-10-19 evaluation.md]` |
| **8 CPU / 16 GiB / 100 GiB / 1 GPU；生成超时 28,800 s（8 h）** | Harbor 路线的资源与超时 | `[网页 2026-10-19 HF]` |
| **100,000 成员 / 20 GiB** | 提交 ZIP 的归档成员数与未压缩体积上限 | `[网页 2026-10-19 evaluation.md]` |
| **MPR 0.87 vs 0.67；SPR 0.89 vs 0.70；VLM 0.82 vs 0.78** | SimWorlds（读 Blender 活状态）vs VIGA（纯视觉 verifier，Opus 4.7，15 轮），4DBuildBench 50 场景 —— **MPR 差 0.20，VLM 评分只差 0.04** | `[本地 05_trajectory_repair.md]` |
| **流体 0.95 vs 0.56；刚体 0.83 vs 0.61** | SimWorlds 分材质的 MPR | `[本地 05_trajectory_repair.md]` |
| **SPR 0.97 → 0.87；VLM 0.87 → 0.76** | SimWorlds 消融（15 场景子集）：去掉 verifier / 去掉分阶段 | `[本地 05_trajectory_repair.md]` |
| **全部信号 1.0000，VLM 0/8，只有 A7 抓到** | 本机 `anim_missing` 变异（关键帧删光）：view0 / 多视角 / Chamfer / 体素 IoU 全部失明 —— **单帧渲染的 verifier 对动画完全失明** | `[本地 10_blender_tasks.md]` |
| **检出 1/8、保真 7/7 和 4/4** | A7 动画 F-curve 断言的实测判别力与保真 | `[本地 10_blender_tasks.md]` |
| **22 个变异里 VLM 独占 0 个；view0 只判对 12/22** | VLM 没有任何独占盲区；单张截图是最差的视觉信号 | `[本地 10_blender_tasks.md]` |
| **全量断言保真 0/11 和 0/4** | 九族断言全查 = 零判别力 → 断言必须在**造题干时**按字段裁 | `[本地 10_blender_tasks.md]` |
| **121 s / 784 MB** | 本机 `uv pip install bpy 4.5.14 LTS` 的耗时与包体 | `[本地 06_harness.md]` |
| **0.9254/0.0199/0.7038 → 0.9419/0.0077/0.8387** | 3DHarnessBench：GPT-5.6 Sol 加相机位姿后的 SigLIP/Chamfer/Uni3D | `[本地 05_trajectory_repair.md]` |
| **Betti 0.9050 → 0.4186** | 3DHarnessBench：Opus 5 加部件量测后的拓扑误差 | `[本地 05_trajectory_repair.md]` |

### 4.5 3JSBench（两条路线的共同判据参照）

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **100 任务 / 每模型 3 次 one-shot / 高推理档 / 共 300 次尝试 / 全体 3,000 次** | 3JSBench 的评测口径 | `[网页 2026-10-19 bundle]` |
| **744 条 check = 696 必查 + 48 advisory；695 条分入六族** | ⚠️ **口径澄清** —— 本地笔记的 695 指「分入六族的必查项」，旧笔记的 743 指「含 advisory 的全部 check」，两个都真实 | `[网页 2026-10-19 benchmark.json 重算]` |
| **223 / 160 / 157 / 45 / 12 / 98** | 六族必查项分布：部件计数 / 结构 / 空间关系 / 任务专属几何 / 文字 / 渲染质量。**前三族 540 条 = 78%，全是「有几个、接在哪、挨着谁」，一条「看起来像不像」都没有** | `[网页 2026-10-19 重算，与本地逐族一致]` |
| **九个固定视角** | 捕获 three.js 场景后的渲染视角数（本地原型用同样的 9 个） | `[网页 2026-10-19 bundle]` |
| **平均每任务 6.95 条必查项 / 3.26 个绑定部件** | 695/100 与 326/100 | `[网页 2026-10-19 重算]` |
| **45 / 44 / 11** | 任务 category 分布：Objects & geometry / Assemblies / Text & symbols | `[网页 2026-10-19 重算]` |
| **Astra 80.0%（240/300）/ Opus 5.5 49.0%（147/300）** | 两个头部模型在**不含 LLM 打分**的判据下相差 **31 个百分点** | `[网页 2026-10-19 bundle]`，与 `[本地 91_3jsbench_verified.md]` **一致** |
| **Opus 5.5 pass@3 = 75/100，全三次都过 = 23/100** | 从「解出过」到「稳定解出」的落差 | `[网页 2026-10-19 bundle]` |
| **13 个模型**（本地笔记只有 10 个） | 补：**HY4 Preview 18.0%（54/300）、Gemini 4 Argon 11.0%（33/300）、Inkling 2.0%（6/300）** | `[网页 2026-10-19 bundle]` ❌ 本地缺 |
| **Muse Spark 1.3：10.67%（32/300）** | ❌ **与本地笔记的 10.0%（30/300）不一致** —— 本地是 10-14 改判后的值，10-16 又改了两次 | `[网页 2026-10-19 bundle]` |
| **改判 3 次**：`rule-fixes.2026-10-14`、`task-reviews.2026-10-16`、`avocado-reviews.2026-10-16` | ❌ 本地只记了 1 次 —— **榜单仍在动，引用必须带日期** | `[网页 2026-10-19 bundle]` |
| **20% / 19% / 17% / 16% / 16%** | 3,000 次尝试的五大失败：物体互相穿插 / 表面透视（可见背面）/ 表面闪烁（绘制顺序）/ 部件朝向与题面不符 / 部件断开。**前三名全是渲染层面的物理不自洽，不是审美问题，且全都能用确定性规则查出、都无法从单张截图可靠看出** | `[网页 2026-10-19 bundle]`，与本地**完全一致** |
| **995 mesh / 177,000 三角面 vs Astra 45 / Fable 24** | 网格预算差两个数量级；Muse Spark 33% 的尝试闪烁（最高）—— **堆 mesh 与闪烁同时出现，指向共面重叠** | `[网页 2026-10-19 bundle]`，与本地一致 |
| **55/300，只有 1 次通过** | Gemini 3.8 Flash 把程序包进没要求的 Markdown 围栏的次数；grader 会剥围栏再判。另：Gemini see-through 54%、inside-out 14%，均最高 | `[网页 2026-10-19 bundle]`，与本地一致 |
| **SigLIP2 差 0.004，通过率差 53 个百分点** | Astra +0.011 / Opus 5.5 +0.0092 / GPT-6 Sol +0.007 vs 通过率 80.0% / 49.0% / 27.0% —— **把 CLIP 或 SigLIP 当质量闸，等于没有闸** | `[网页 2026-10-19 bundle]`，与本地一致 |
| **224 px / uint8 ONNX / 跨 runtime 差异最大 0.005（40 次尝试比较）** | SigLIP2 pinned checkpoint 的配置与数值稳定性 —— **噪声量级 0.005 比模型间差异 0.004 还大** ➕ 本地未记 | `[网页 2026-10-19 bundle]` |
| **$1.2822 / $0.8031 / $0.3099 / $0.048** | 每次尝试均价：Fable 5.1 / Astra / Opus 5.5 / Inkling。**Opus 5.5 单次成本只有 Fable 5.1 的 24%，通过率 49.0% vs 69.3%** ➕ 本地未记 | `[网页 2026-10-19 bundle]` |
| **turn1 265 / turn2 33 / turn3 2** | Grok 4.7 的 `first-non-timeout` 选择策略下的轮次分布 | `[网页 2026-10-19 benchmark.json]` |

### 4.6 happycapy.ai（可引用的唯一数字）

| 数字 | 说明什么 | 出处 |
|---|---|---|
| **0.474 → 约 0.725** | Qwen 3.8 Max 的「Score Index across 10+ Benchmarks」复合指数，SFT 基线 → 最佳 checkpoint。⚠️ **基准名未列、非 3D 专用、营销页、无日期无样本量 —— 不建议作为 3D 资产质量证据** | `[网页 2026-10-19 happycapy.ai]` |
| **约 $2 / $6 每百万 token** | 社区报告的 Qwen 3.8 Max 输入/输出价格（未经厂商确认） | `[网页 2026-10-19 happycapy.ai]` |

---

## 5. 待补清单（写正文前最好补上的）

| # | 缺什么 | 为什么要 | 怎么补 |
|---|---|---|---|
| 1 | **MoVer**（Stanford，GSAP，39 star） | 本地只有一行 meta。若它确是「运动断言/验证 DSL」，是 From Web 确定性判据的关键引用 | 抓 `jama1017/MoVer` README + 论文 |
| 2 | **InternSVG**（Shanghai AI Lab，127 star） | 本地只有一行 meta，无规模无评测 | 抓 `hmwang2002/InternSVG` |
| 3 | **LottieGPT**（Tsinghua，39 star） | 同上；与 OmniLottie 同赛道，有对照价值 | 抓 `yisuanwang/LottieGPT` |
| 4 | **huashu-art-motion**（3.44k star） | 本地只有一行 meta；star 高，是社区侧重要样本 | 抓 `alchaincyf/huashu-art-motion` |
| 5 | **BlenderWorld 技术报告 PDF** | README 只给了「结构+语义校验 → 独立 rubric 评审」一句，**造题细节（标注人数、工时、一致性系数）缺失** | 读 `docs/BlenderWorld__...pdf` |
| 6 | **PDM Video 的仓库归属** | `mexicat/pdoom-video`(2,894) vs `JohnHeibel/PDoomVideo`(2,212) 无法确定小红书指哪个 | 回看小红书原帖链接 |
| 7 | **「Blender 产出视频」的管线/基准** | From Blender 这条线**本地 0 条**，BlenderWorld 也只是 3D 创作基准（动画是 9 个 domain 之一） | 需新一轮检索（关键词：bpy video generation / Blender animation agent / 4DBuildBench 原文） |
| 8 | **Blender 渲染的逐字节确定性实测** | Web 侧做了（3/3 一致），Blender 侧只有「`--write-movie` 配 `--fixed-fps`」一句 | 本机实验：同脚本渲两次序列比 md5 |
| 9 | **3JSBench 的 `/data/battle.json` 与 Arena 评分** | 第三类信号（人类成对偏好 Bradley-Terry/Elo）本次只抓到方法论，没抓数值 | 抓 `https://3jsbench.com/data/battle.json` 与 `https://www.instaplay.ai/api/public/3jsbench/arena-ratings.json` |
| 10 | **OmniLottie 成功率口径** | 88.3%（deep_video）/ 93.3%（bench_meta）/ 97.3%（附录）三个数 | 读论文原文定口径 |

