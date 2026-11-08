# PPT 与 Manim 两个方向 · 调研素材库

> 性质：**素材库**，不是博客正文。所有数字都带口径与出处，未在本地笔记中出现的内容一律标 `[笔记无·待补]`。
> 整理时间：2026-10-19。只用本地只读素材，未联网。

## 0. 出处简写与文件对照

| 简写 | 绝对路径 |
|---|---|
| `deep_video.md` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/deep_video.md |
| `benchmarks.md` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/benchmarks.md |
| `pipelines.md` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/pipelines.md |
| `bench_meta_video.json` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/bench_meta_video.json（21 条，索引从 0 起） |
| `pipe_meta_video.json` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/pipe_meta_video.json（27 条，索引从 0 起） |
| `env/video.md` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/env/video.md |
| `video_assets_sources.md` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/video_assets_sources.md |
| `vc_data/*` | /mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/*（**非本次指定数据源**，同仓库的 verifier 调研笔记，本文中凡引用都单独标注） |

两点口径说明：

1. `visual-coder-blog-v2/middle_processing/benchmarks.md` 与 `pipelines.md` 与 v1 版**逐行相同**（同为 188 / 288 行，相关条目行号一致），所以下文行号对两份都适用。
2. `benchmarks.md` 文件头自述：「关键发现 / SOTA」只摘论文摘要或官方页原文数字，摘要没数字的只写定性结论（`benchmarks.md:1-6`）。所以表里缺分数的条目是**原文没给**，不是漏抄。

---

# 一、PPT 方向（幻灯片 / 海报 / 演示文稿代码生成）

## 1.1 Benchmark 清单（本地笔记里共 5 条）

全部来自 `benchmarks.md` 的「### 11. 视频即代码 · 幻灯片与演讲视频」小节（`benchmarks.md:174-182`）。

### B1 · AutoPresent · SlidesBench（2025-01，UC Berkeley，CVPR 2025）
- 考什么：自然语言指令 → 幻灯片**绘图程序**（SlidesLib / python-pptx 风格 API），而不是直接出图像。
- 规模：310 份 deck / 10 个领域，拆成 **7k 训练对 + 585 测试**（`benchmarks.md:178`）。
- 评测方式：reference-based 相似度 + reference-free 设计质量（**VLM 判**）两套并行（`benchmarks.md:178`）。
- 最好成绩：**8B 的 AutoPresent 达到与 GPT-4o 相当**；结论是「程序化出片优于端到端图像」。
  口径注意：**原文只给相对结论，没给绝对分数**（`benchmarks.md:178`、`bench_meta_video.json` 第 4 条 capability 字段同样只写「8B 达 GPT-4o 水平」）。
- 另一处交叉引用：`vc_data/07_capability_spec.md:400` 把 AutoPresent 归入「窄域专项」，写法是「AutoPresent（8B ≈ GPT-4o）」，并给出规律——**任务一旦窄到有确定性 verifier，小模型就能打平前沿**。
- 影响力：GitHub 181 star（`pipe_meta_video.json` 第 1 条 / `bench_meta_video.json` 第 4 条）。

### B2 · PPTAgent · PPTEval（2025-01，ISCAS，EMNLP 2025）
- 考什么：给定参考 PPT + 输入文档，产出**可执行的编辑动作**套进模板（不是从零排版）。
- 规模：**50 份参考 PPT + 50 份文档 = 500 个任务**；源集是 Zenodo10K（`benchmarks.md:179`）。
- 评测方式：PPTEval 三维（Content / Design / Coherence）由 **VLM 打分**，另加**成功率**（`benchmarks.md:179`）。
- 最好成绩：**成功率 95.0%**（其中 GPT-4o 97.8%），**PPTEval 均分 3.67**。
  口径注意：3.67 的量程笔记里没写满分值（按 PPTEval 常规为 1–5，**本地笔记未明示，属 `[笔记无·待补]`**）；95.0% 是「能不能跑完编辑动作」的执行成功率，不是质量分。
- 影响力：GitHub **5.1k star**，是本方向 star 最高的系统（`pipe_meta_video.json` 第 2 条）。

### B3 · Paper2Poster · PaperQuiz（2025-05，Oxford，NeurIPS 2025 D&B）
- 考什么：论文 PDF → 学术海报（可编辑 .pptx）。
- 规模：**约 100 对论文–海报**（取自近期会议）（`benchmarks.md:180`）。
- 评测方式：四轴 Visual / Textual / Holistic + **PaperQuiz（让模型看海报答题）**（`benchmarks.md:180`）。
- 最好成绩：**开源 Qwen2.5 版在多项指标上超过 GPT-4o 多 agent 基线，并省 87% token**。
  口径注意：**只有相对结论与成本比，没有绝对分数**（`benchmarks.md:180`、`bench_meta_video.json` 第 7 条）。
- 影响力：GitHub 4.0k star。

### B4 · PresentAgent · PresentEval（2025-07，AIGeeksGroup，EMNLP 2025 Demo）
- 考什么：文档 → 带配音的演讲视频（Doc2Present 任务）。
- 规模：**30 对文档–演讲**（`benchmarks.md:181`）——本方向规模最小的一条。
- 评测方式：VLM 三维 + **quiz 答题** + 音视频打分（`benchmarks.md:181`）。
- 最好成绩：**quiz 0.64，人类参考为 0.56**（即生成视频的答题正确率反超人类录制）。
  口径注意：这是「看视频答题正确率」，属内容召回型指标，不衡量观感；且样本仅 30 对，统计意义弱。
- 影响力：GitHub 146 star。

### B5 · Paper2Video（2025-10，NUS，NeurIPS 2025 SEA WS）
- 考什么：一篇论文 → 作者风格的演讲视频（Beamer 幻灯片 + 字幕 + TTS + 讲者数字人）。本方向唯一端到端出视频的（`deep_video.md:38`）。
- 规模：**101 篇论文**，每篇配作者本人录制的视频与幻灯片（`benchmarks.md:182`、`deep_video.md:38`）。
- 评测方式：四指标——Meta Similarity、**PresentArena**（对人类的成对胜率）、**PresentQuiz**（看视频答题）、**IP-Memory**；对照组含人类真视频、端到端视频模型 Veo3 / Wan2.2、以及 PresentAgent（`deep_video.md:47`）。
- 最好成绩（全部出自 `deep_video.md:48-52`）：
  - PresentQuiz **0.842 / 0.951**，超过人类作者 **0.738 / 0.908**；端到端视频模型 Veo3 只有 **0.367 / 0.585**。（两个数是两档口径，笔记未标名，原样抄录。）
  - IP-Memory **50.0%**，与人类持平；Veo3 **31.3%**。
  - PresentArena 整体观感成对胜率只有 **17.0%**（人类 50%）；**去掉数字人与光标降到 15.2%**。
  - 成本：约 **48 分钟 / 62K token** 每篇。
- 口径背离（可直接引用的结论）：**PresentQuiz 超人类、PresentArena 只有 17%**，笔记自己给了解释——答题式指标偏向内容召回、对整体呈现不敏感（`deep_video.md:53`）。
- 影响力：GitHub 2.4k star。

### 旁证 · 厂商侧
- 没有任何厂商在发布材料里报告过本方向的公开 benchmark（`env/video.md:73`，原话针对 code-video 全域：MMMC / TeachQuiz / TheoremExplainBench 都没出现在厂商材料里）。
- `[vc_data·非指定源]` GPT-5.6 发布页点名幻灯片能力：能从参考 deck 反推 design system（layouts / typography / spacing / colors，含 Slide Master 里的规则）；笔记作者当场指出这个任务形式**正好可验证**（`vc_data/16_primary_sources.md:1721-1723`）。
- `[vc_data·非指定源]` GLM-5（arXiv 2602.15763）§4.2.5 的标题是 **Slide Generation**，三级奖励（静态 → 运行时 DOM/bbox → 感知）**针对的是 HTML 幻灯片而非通用网页**；已有方案当成 WebDev 视觉奖励引用属迁移用法（`vc_data/01_frontier_labs.md:284-288`）。这是本地笔记里唯一一条「厂商把幻灯片当成专门的可验证训练任务」的证据。

## 1.2 公开数据管线（本地笔记里共 5 条，**5 条标「是」可下载**）

出处均为 `pipelines.md` 的「总表 · 视频即代码」。

| # | 名称 | 产物语言 / 框架 | 数据规模 | 能否下载 | 生成方式要点 | 出处 |
|---|---|---|---|---|---|---|
| P1 | AutoPresent | **Python（SlidesLib）→ .pptx** | 训练 **7k 指令–代码对** | **是** GitHub `para-lost/AutoPresent` | 自然语言指令生成 Python 绘图程序渲染幻灯片，带自我迭代修正 | `pipelines.md:263`、`pipe_meta_video.json` 第 1 条 |
| P2 | PPTAgent | **Python（python-pptx）→ .pptx** | **Zenodo10K 10,448 份 PPT** | **是** GitHub `icip-cas/PPTAgent` | 两阶段：分析参考 PPT 聚类抽 schema → 套模板执行编辑动作，**每页 ≤ 2 次自校正** | `pipelines.md:264`、`pipe_meta_video.json` 第 2 条 |
| P3 | Paper2Poster | **Python（python-pptx）→ 海报 .pptx** | 约 **100** 论文–海报对 | **是** GitHub `Paper2Poster/Paper2Poster` | Parser → Planner（**二叉树版式**）→ Painter-Commenter 环（**VLM 修溢出与对齐**） | `pipelines.md:267`、`pipe_meta_video.json` 第 5 条 |
| P4 | PresentAgent | **Python（python-pptx）→ 配音视频 mp4** | **30** 文档–演讲对 | **是** GitHub `AIGeeksGroup/PresentAgent` | 切分文档 → 渲染幻灯片帧 → LLM 旁白 + TTS → **音画对齐合成视频** | `pipelines.md:269`、`pipe_meta_video.json` 第 7 条 |
| P5 | Paper2Video | **LaTeX（Beamer）+ Python → 演讲视频 mp4** | **101** 篇论文 | **是** GitHub `showlab/Paper2Video`；元数据表另有 HF `ZaynZhu/Paper2Video`（`data/paper2video.xlsx`，101 行，**视频为外链、无静帧**） | 版式树搜索 + 光标 grounding + 字幕 + TTS + 数字人，**逐页并行** | `pipelines.md:272`、`video_assets_sources.md:28`、`deep_video.md:42-46` |

补充数字：
- Paper2Video 的**逐页并行把单条耗时从约 287 分钟压到约 48 分钟**（约 6 倍）（`deep_video.md:46`）。
- 框架分布：本方向 5 条管线里 **3 条用 python-pptx**（PPTAgent / Paper2Poster / PresentAgent）、1 条用自建 SlidesLib（AutoPresent）、1 条用 Beamer LaTeX（Paper2Video）。即**产物格式集中在 .pptx 与 Beamer 两种**（`pipe_meta_video.json` 第 1/2/5/7/10 条的 `lang` 与 `art` 字段）。
- 管线总表的「开源」列口径：`是` = 数据可下载；`仅模型/代码` = 数据未放出；`承诺` = 论文说将开源但找不到链接（`pipelines.md:3`）。PPT 这 5 条全部是 `是`，**这是 PPT 方向相对 Manim 方向最硬的一个优势**。

## 1.3 可做成确定性判据的信号

### 笔记里**明确有**的（可直接引用）
1. **执行 / 编译成功率**。PPTAgent 把「成功率」与质量分并列为指标，最好 97.8%、系统 95.0%（`benchmarks.md:179`）。Paper2Video 的 Beamer 流程**编译报错时按反馈修复**（`deep_video.md:43`）——编译通过是天然的二值判据。
2. **每页自校正次数上限**可计数。PPTAgent「每页 ≤ 2 次自校正」（`pipelines.md:264`）。
3. **版式树 / 二叉树版式结构**存在显式结构化中间表示：Paper2Video「版式树搜索精修布局」（`deep_video.md:43`）、Paper2Poster「Planner 二叉树版式」（`pipelines.md:267`）——说明对象层级是可程序读取的。
4. **文字溢出与元素对齐**被当作要修的缺陷族，但本地笔记里**修它的是 VLM**：Paper2Poster 的 Painter-Commenter 环「VLM 修溢出对齐」（`pipelines.md:267`）。即「信号存在、但公开做法不是确定性的」。
5. `[vc_data·非指定源]` **幻灯片对象树可回读有现成实现路径**：Visual-SDPO（arXiv 2606.10334）把「像素区域 → 代码语句」的运行时插桩分三类写死——matplotlib 拦截对象构造函数记源码行号配 `get_window_extent()`、HTML 在 DOM 加 `data-src-*` 配 `getBoundingClientRect()`、**pptx 拦截 shape 构造**；没插桩的工具链才退回 VLM 映射（`vc_data/05_trajectory_repair.md:864-866`）。这是本地笔记中唯一一条直接支持「幻灯片对象树可回读并归因到代码行」的证据。
6. `[vc_data·非指定源]` **三级奖励分层已有厂商实践**：GLM-5 的 Slide Generation 用静态 → 运行时 DOM/bbox → 感知三级（`vc_data/01_frontier_labs.md:285`）。「运行时 DOM/bbox」这一级就是确定性几何判据。
7. `[vc_data·非指定源]` **回读比截图便宜两个数量级**：17 个页面各起一次浏览器，单页全流程中位 840 毫秒（渲染约 470ms、截图约 110ms），而**回读只要 1–4 毫秒，是渲染耗时的千分之四**（`vc_data/17_chart_verifier.md:245`、`vc_data/draft_domains.md:24`）。这条是 Web/图表线的实测，但对「对象树回读能进 RL 每一步、截图不行」这个论断同样适用。
8. `[vc_data·非指定源]` **几何判据的两个已知坑**（抄过来会踩）：文字包围盒**必须过变换矩阵**，否则旋转文本全堆在原点，参考解会被误报 171 对文字重叠而实际 0 对（`vc_data/17_chart_verifier.md:65`、`:320`、`vc_data/draft_verifier.md:260`）；「溢出」要分**画布边界**与**绘图区边界**两套，否则轴标题类本就在区外的元素会假阳性（`vc_data/17_chart_verifier.md:66`）。
9. `[vc_data·非指定源]` **两两重叠的可操作阈值**：相交面积 / 较小者面积 ≤ 0.05，且判据只能限定在「文本与交互元素之间」，否则徽章叠卡片角这类合法设计会误判（`vc_data/14_web_verifier.md:108`）。

### 笔记里**没有**的（你要自己补；我只标空缺，不编造）
- `[笔记无·待补]` **页数、标题文案、字数上限是否符合要求**这类指令遵循型硬判据——PPT 线的 5 条 benchmark 没有一条把它列为指标。
- `[笔记无·待补]` **纯程序化（无 VLM）的幻灯片版式检查套件**：公开工作里溢出/重叠全交给 VLM，本地笔记没有任何一条 PPT benchmark 声明用确定性几何判据。
- `[笔记无·待补]` **字体族数 / 字号尺度 / 配色数 / 对比度**等排版规范检查在 PPT 线的落地（Web 线有：`vc_data/draft_verifier.md:331` 的十一条探针，但那是网页）。
- `[笔记无·待补]` **母版 / design system 一致性比对**的现成判据（GPT-5.6 的能力声明有，判据没有，`vc_data/16_primary_sources.md:1723` 只是说「可以这么做」）。
- `[笔记无·待补]` **幻灯片动画与切换的时序判据**。

## 1.4 已知难点与失败模式

1. **观感与内容召回严重背离，这是本方向最硬的失败模式。** Paper2Video：PresentQuiz 0.842 超人类 0.738，但 PresentArena 成对胜率只有 **17.0%**（人类 50%）；作者自述「整体呈现仍可辨为机器产物」「答题式指标偏向内容召回、对整体呈现不敏感」（`deep_video.md:49,51,53`）。
2. **设计质量只能靠 VLM 判。** SlidesBench 的 reference-free 设计质量是 VLM 判（`benchmarks.md:178`），PPTEval 三维是 VLM 判（`benchmarks.md:179`），PresentEval 三维 + 音视频打分是 VLM 判（`benchmarks.md:181`）。而本地笔记对 VLM 判官的总体结论是「与人评经常不相关，只能作参考」（`env/video.md:10,44`）。
3. **基准规模极小。** 30 对（PresentAgent）、约 100 对（Paper2Poster）、101 篇（Paper2Video）；Paper2Video 作者自述「基准仅 101 对」是局限之一（`deep_video.md:53`）。
4. **依赖商业大模型。** Paper2Video 自述局限（`deep_video.md:53`）。
5. **成本不低。** Paper2Video 约 48 分钟 / 62K token 每篇，且这已经是并行优化后的结果（原 287 分钟）（`deep_video.md:46,52`）。
6. **数字人与光标这类「呈现增强」是有用的但收益有限**：去掉后 PresentArena 从 17.0% 掉到 15.2%（`deep_video.md:51`）——即贴装饰救不了观感。
7. **缺失败后如何修复的轨迹数据**（全域结论，PPT 线同样适用）：公开数据几乎全是一次成功的配对（`env/video.md:53`）。
8. `[vc_data·非指定源]` **幻灯片 RL 已被实测 reward hack**：GLM-5 在 HTML 幻灯片 RL 中出现**硬截断溢出内容、操纵间距**，对策是修补渲染器消除可利用漏洞 + 加视觉感知信号检测异常留白（`vc_data/04_verifier.md:23,238`、`vc_data/01_frontier_labs.md:288`）。这条对「为什么幻灯片的版式判据必须自己做硬、不能只给感知奖励」是最有力的证据。

## 1.5 它作为 V2 辅助方向：最成熟 / 最不成熟

**最成熟的部分（可以认为「稍微有一定能力即可」）**
- **执行层已经基本不是问题**：套模板编辑的执行成功率 95.0%（GPT-4o 97.8%）（`benchmarks.md:179`）。
- **产物格式与工具链收敛且全部开源可下载**：5 条管线 5 条数据可下，3 条共用 python-pptx（§1.2）。
- **内容召回型指标已达到或超过人类**：PresentQuiz 0.842 > 人类 0.738（`deep_video.md:49`）、PresentEval quiz 0.64 > 人类 0.56（`benchmarks.md:181`）。
- **小模型已能打平前沿**：8B AutoPresent ≈ GPT-4o（`benchmarks.md:178`）、Paper2Poster 开源 Qwen2.5 版多指标超 GPT-4o 多 agent 且省 87% token（`benchmarks.md:180`）；`vc_data/07_capability_spec.md:400` 把这条总结成「全表最一致的规律」。
  → **这四条合起来就是「PPT 不需要作为主力攻坚」的直接依据：执行门已过、数据齐、小模型够用。**

**最不成熟的部分**
- **整体呈现 / 美学**：PresentArena 17.0%（人类 50%）是全方向最刺眼的差距（`deep_video.md:51`）。
- **评测方法本身**：设计质量全靠 VLM，没有一条公开的确定性版式判据（§1.3 空缺清单）；而 VLM 判官与人评的可靠性在本地笔记里被反复否定（`env/video.md:44`、ManimAgent 实测 −0.17 见 §2.4）。
- **基准规模**：30 / 100 / 101 这个量级做不了可靠的模型对比。
- **指标口径互相打架**：答题超人类而观感 17%，意味着「现有 SOTA 数字」不能直接当能力证明。

## 1.6 PPT 方向 · 量化数字清单

| 数字 | 说明什么 | 出处 |
|---|---|---|
| 585 | SlidesBench 测试样本数（配 7k 训练对、310 份 deck、10 领域） | `benchmarks.md:178` |
| 7k | AutoPresent 训练用指令–代码对数量（可下载） | `pipelines.md:263` |
| 8B ≈ GPT-4o | AutoPresent 8B 模型达到 GPT-4o 水平；原文无绝对分 | `benchmarks.md:178` |
| 500 | PPTEval 任务数（50 参考 PPT × 50 文档） | `benchmarks.md:179` |
| 10,448 | PPTAgent 源集 Zenodo10K 的 PPT 份数 | `pipelines.md:264` |
| 95.0% | PPTAgent 执行成功率（GPT-4o 97.8%），是本方向最硬的「可执行」数字 | `benchmarks.md:179` |
| 3.67 | PPTEval 三维均分（量程笔记未写明，按常规为 1–5） | `benchmarks.md:179` |
| ≤ 2 | PPTAgent 每页自校正次数上限 | `pipelines.md:264` |
| 5.1k star | PPTAgent GitHub star，本方向最高 | `pipe_meta_video.json` 第 2 条 |
| ~100 | Paper2Poster 论文–海报对数量 | `benchmarks.md:180` |
| 87% | Paper2Poster 开源版相对 GPT-4o 多 agent 节省的 token 比例 | `benchmarks.md:180` |
| 4.0k star | Paper2Poster GitHub star | `bench_meta_video.json` 第 7 条 |
| 30 | PresentAgent / Doc2Present 文档–演讲对数量（本方向最小） | `benchmarks.md:181` |
| 0.64 / 0.56 | PresentEval quiz：生成视频 0.64 对人类 0.56 | `benchmarks.md:181` |
| 101 | Paper2Video 基准论文篇数（配作者本人录制视频） | `benchmarks.md:182` |
| 0.842 / 0.951 | Paper2Video PresentQuiz 两档得分 | `deep_video.md:49` |
| 0.738 / 0.908 | 同口径下人类作者的 PresentQuiz 得分（被超过） | `deep_video.md:49` |
| 0.367 / 0.585 | 端到端视频模型 Veo3 的 PresentQuiz 得分 | `deep_video.md:49` |
| 50.0% / 31.3% | IP-Memory：PaperTalker 与人类持平 50.0%，Veo3 仅 31.3% | `deep_video.md:50` |
| 17.0% | PresentArena 整体观感对人类的成对胜率（人类 50%）——本方向最大短板 | `deep_video.md:51` |
| 15.2% | 去掉数字人与光标后的 PresentArena 胜率（即装饰收益仅 1.8 点） | `deep_video.md:51` |
| 287 → 48 分钟 | Paper2Video 逐页并行前后的单条耗时 | `deep_video.md:46` |
| 62K token | Paper2Video 单篇 token 成本 | `deep_video.md:52` |
| 2.4k star | Paper2Video GitHub star | `bench_meta_video.json` 第 12 条 |
| 5 / 5 | PPT 线公开管线条数 / 其中数据可下载条数（全可下） | `pipelines.md:263,264,267,269,272` |
| 3 / 5 | 用 python-pptx 的管线占比（另 1 条 SlidesLib、1 条 Beamer） | `pipe_meta_video.json` 第 1/2/5/7/10 条 |
| 1–4ms vs 470ms | `[vc_data]` 对象树回读耗时 vs 渲染耗时（千分之四），决定回读能进 RL 每一步 | `vc_data/17_chart_verifier.md:245` |
| 171 对 → 0 对 | `[vc_data]` 文字包围盒不过变换矩阵造成的假阳性重叠量级 | `vc_data/17_chart_verifier.md:320` |
| ≤ 0.05 | `[vc_data]` 两两重叠判据阈值（相交面积 / 较小者面积） | `vc_data/14_web_verifier.md:108` |
| 49.5 → 58.2 → 60.7 | `[vc_data]` AeSlides 上零样本 → GRPO（视觉相似度）→ Visual-SDPO 的分数；同法 ChartMimic 67.9→78.6、Design2Code 72.1→82.6，且**达到 GRPO 训满效果只用约 29% rollout 预算** | `vc_data/05_trajectory_repair.md:870-871` |

---

# 二、Manim 方向（代码驱动的动画 / 讲解视频）

## 2.1 Benchmark 清单（本地笔记里共 4 条教学动画基准 + 2 条 `[vc_data]` 补充）

指定源里的 4 条全部来自 `benchmarks.md` 的「### 9. 视频即代码 · 教学动画」（`benchmarks.md:149-157`）。

### B1 · TheoremExplainBench（TEB，2025-02，U. Waterloo，ACL 2025 Oral）
- 考什么：定理 → 超过 5 分钟的 Manim 讲解视频；是首个该类基准（`deep_video.md:21`）。
- 规模：**240 个定理**，覆盖计算机 / 化学 / 数学 / 物理 **4 学科**，每科按高中 / 本科 / 研究生 **3 难度各 80**（`benchmarks.md:153`、`deep_video.md:29`）。
- 评测方式：5 项自动指标（LLM 评文本 / 视频 / 关键帧）取**几何平均**——准确与深度、视觉相关性、逻辑流、元素布局、视觉一致性（`benchmarks.md:153`、`deep_video.md:29`）。另有渲染成功率。
- 最好成绩（`deep_video.md:31`）：
  - **o3-mini（medium）成功率 93.8% / 总分 0.77**（成功率最高）
  - GPT-4o **55.0% / 0.78**
  - Claude-3.5-Sonnet **仅 2.1% / 0.79**（分最高但几乎渲染不出来——这是「总分口径骗人」的教科书例子）
  - Gemini-2.0-Flash **14.6% / 0.76**
  - 普遍弱项是**元素布局，各模型 0.57–0.73**（`deep_video.md:32`）
- 人类实验：15 名参与者先全把一段有错的文字解释判为正确，看完对应动画视频后 **9 人（60%）改判为错**（`deep_video.md:33`）。
- 数据可下载：HF `TIGER-Lab/TheoremExplainBench`（`bench_meta_video.json` 第 6 条；样例口径见 `video_assets_sources.md:26`，字段为定理名 / 描述 / 学科 / 难度，纯文本）。

### B2 · Code2Video · MMMC（2025-10，NUS，ICML 2026）
- 考什么：主题 → 3Blue1Brown 风格的长讲解视频，全部走可执行 Manim 代码（`deep_video.md:3`）。
- 规模：**117 主题 / 13 学科 / 339 子片 = 456 单元**，全部取自 3Blue1Brown（`benchmarks.md:154`、`deep_video.md:11`）。
- 评测方式：**TeachQuiz**（评测模型先屏蔽已有知识得到基线，再只看生成视频答十道选择题，**答对率之差**即知识传递量）+ **VLM 观感 5 轴**（元素布局 / 吸引力 / 逻辑流 / 视觉一致 / 准确深度）+ 代码效率（`benchmarks.md:154`、`deep_video.md:11`）。
- 最好成绩（`deep_video.md:13-14`）：
  - TeachQuiz：Claude Opus 4.1 **40.0 → 86.0**（直接写码 → Code2Video）；GPT-4.1 **37.0 → 82.0**；GPT-5 **36.5 → 80.0**
  - 人类 3Blue1Brown **97.1**；扩散基线 **Veo3 仅 2.5、OpenSora-v2 为 0.0**
  - 观感均分：Opus 4.1 **37.8 → 87.9**（人类 **99.7**）
- 消融（GPT-4.1，口径为「TeachQuiz / 观感」两数）（`deep_video.md:15`）：去掉 Planner 掉到 **38.1 / 40.5**（最吃重）；去掉外部图标库 **68.1 / 52.0**；去掉锚点栅格 **69.2 / 55.2**；去掉 Critic **72.5 / 60.7**。
- 成本：每主题约 **13.8 分钟 / 43.1K token**，比直接写码**慢 5–8 倍、多耗 15–20 倍 token**（`deep_video.md:16`）。
- 数据可下载：HF `YanzheChen/MMMC`（`video_assets_sources.md:25`，字段为主题 / 学科，纯文本无图）。

### B3 · DTVBench · JanusCoder（2025-10，Shanghai AI Lab，ICLR 2026）
- 考什么：可视化 ↔ 代码的双向任务，**引擎含 Manim 与 Mathematica**（`benchmarks.md:155`、`bench_meta_video.json` 第 13 条）。
- 规模：**102 个可视化任务**。
- 评测方式：文本 / 视觉双向代码任务（`benchmarks.md:155`）。
- 最好成绩：**7–14B 开源模型逼近或超过商用模型**。
  口径注意：**没有绝对分数**，只有相对结论（两处记录一致）。
- 下载：GitHub `InternLM/JanusCoder`（`bench_meta_video.json` 第 13 条，无 star 数记录）。

### B4 · VisualEDU（2025-11，South China Normal Univ.，EMNLP 2025 Findings）
- 考什么：数学题 → 分步解题的 Manim 动画视频（`bench_meta_video.json` 第 14 条）。
- 规模：**200 题，6 类 × 3 难度**（`benchmarks.md:156`）。
- 评测方式：时间一致性 / 逻辑正确性 / 视觉清晰度，评了 **9 个 VLM**（`benchmarks.md:156`）。
- 最好成绩：**难题上 Claude-3.7-Sonnet、GPT-4o 均 < 56%**（`benchmarks.md:156`）——即最强模型在难档不过半。
- 下载：本地笔记只给 ACL Anthology 链接，**无代码 / 数据下载入口记录**（`bench_meta_video.json` 第 14 条无 download 字段）。

### 边界条目（相关但不算 Manim 基准）
- **manimator**（2025-07，PES University）：**无自建评测集，直接在 TEB 上评**（`pipelines.md:268`）。
- **ManimAgent**（2026-06，Southeast Univ.）：不是公开基准，是自建任务流——建库 **39** / 固定探针 **33** / 交叉测试 **40**，记忆快照 0 / 50 / 100 / 200 条；**25 个任务由 54 名评分者盲评**，指标为**一次通过率**与**反思轮数**（`deep_video.md:121`）。
- **ManiBench（2603.13251）被明确排除**：ID / 日期自相矛盾、来源可疑、仅 12 题 pilot，未收入（`benchmarks.md:147`）。`[vc_data]` 另一处记录更细：官方拼写是 ManiBench 不是 ManimBench，摘要称 150–200 题而 HF 上只有 **12 题** pilot（`vc_data/13_scaling_tasks.md:1147`、`:1776`）。**引用时别把这条当数据源。**

### `[vc_data·非指定源]` 两条本次指定源里没有的 Manim 相关基准
- **PRISM（arXiv 2605.19382，2026-05）**：**确定性坐标检查，刻意不用 VLM**；Spatial Pass = 渲染成功且审计帧无 overlap / out-of-bounds / leakage。**Exec 最高 GPT-5.4 0.945，但 Spatial 最高 Gemini 3.1 Pro 仅 0.572，Exec → Spatial 平均掉 41.24 点（95% CI [40.41, 42.11]）**；GLM-5 为 0.720 / 0.341。数据 **10,372 条 instruction-code 对，Apache-2.0，全量可下**，且是 Manim 同域语料（比 ManiBench 大 800 倍）（`vc_data/07_capability_spec.md:122,745`、`vc_data/13_scaling_tasks.md:1143,1147`、`vc_data/STATE.md:38`）。
- **ManimBench（arXiv 2604.18364，2026-04）**：评测法是 **5FPS 抽帧 → SSIM 矩阵双向最佳匹配 → fastDTW 对齐**；**Qwen3-Coder-30B-A3B + GRPO + RITL 拿到 94% / 85.7%，全场最好**（`vc_data/07_capability_spec.md:122,622,746`）。
- 相邻可借的 Web 侧时间指标：**Animation2Code（2606.28593）**，214 测试题 / 1,069 条动画视频，headless Chromium 1024×768@30fps **确定性渲染**，与人类偏好一致约 83.9%；Appearance = DreamSim + DTW，**Temporal = CoTracker3 在 30×30 网格抽 tracklet 比位移方向 cos 与幅值比**；**Temporal 全场天花板只有 0.31**（`vc_data/07_capability_spec.md:122,673,744`）。

## 2.2 公开数据管线（本地笔记里共 7 条相关，**数据可下载 2 条、代码可下载 5 条、1 条未开源**）

| # | 名称 | 产物语言 / 框架 | 数据规模 | 能否下载 | 要点 | 出处 |
|---|---|---|---|---|---|---|
| P1 | TheoremExplainAgent | **Python（Manim）→ mp4** | 240 定理基准 | **是**（GitHub `TIGER-AI-Lab/TheoremExplainAgent` + HF 数据集） | Planner + Coder 写 Manim + TTS，**agentic RAG 查 Manim 文档**，渲染失败**重试 ≤ 5** | `pipelines.md:265`、`pipe_meta_video.json` 第 3 条 |
| P2 | manimator | **Python（Manim）→ mp4** | **无自建集**，在 TEB 上评 | **是（代码）** GitHub `HyperCluster-Tech/manimator`，74 star | 两步 LLM：读 PDF 产结构化场景描述 → 转 Manim 代码；多后端，**无验证环** | `pipelines.md:268`、`pipe_meta_video.json` 第 6 条 |
| P3 | Code2Video | **Python（Manim）→ mp4** | MMMC 456 单元 | **是**（GitHub `showlab/Code2Video` 2.1k star + HF MMMC） | Planner 分镜 → Coder **分段并行**写码 + **作用域分级自修复** → Critic 用 **6×6 锚点栅格**回修 | `pipelines.md:270`、`pipe_meta_video.json` 第 8 条 |
| P4 | ManimAgent | **Python（Manim）→ mp4** | 任务流 + **记忆库 200 条** | **否 · 计划开源**（`pipelines.md` 口径）/「承诺开源」（`env/video.md:63`） | **双通道 episodic 记忆**（正例软参考 / 负例硬禁区），不改权重、不喂人工样本 | `pipelines.md:278`、`pipe_meta_video.json` 第 16 条 |
| P5 | JanusCoder（DTVBench 侧） | 可视化 → 代码（含 Manim 引擎） | 102 任务 | **是（代码）** GitHub `InternLM/JanusCoder` | 视觉-程序接口；7–14B 开源逼近商用 | `bench_meta_video.json` 第 13 条 |
| E1 | **3b1b/manim**（引擎） | **Python（OpenGL）** | 渲染引擎 | **是**，**94.9k star** | 3Blue1Brown 原版；场景对象图经 OpenGL/GLSL **原生栅格化逐帧** + ffmpeg | `pipelines.md:282`、`pipe_meta_video.json` 第 20 条 |
| E2 | **Manim Community**（引擎） | **Python（Cairo / OpenGL）** | 渲染引擎 | **是**，**41.5k star** | 原生 scene-graph 栅格化逐帧 + ffmpeg，**文档稳定、教学主力** | `pipelines.md:283`、`pipe_meta_video.json` 第 21 条 |

参照用的同族渲染器（非 Manim，但在同一张表里，可用来对比生态成熟度）：Remotion 63.4k star（每帧是帧号的纯函数，无头 Chromium 逐帧截图，**公司许可、按席位/按次收费**）、Motion Canvas 19.3k star、ranim 0.7k star（Rust / wgpu，**实验性、API 不稳**）、HyperFrames 61.2k star（**唯一把「给 agent 自动化用」写进设计**：命令行默认非交互、逐帧定位可复现）（`pipelines.md:284-287`、`env/video.md:52`）。

`[vc_data·非指定源]` 可下载的 Manim 域语料补充：**PRISM 10,372 条 instruction-code 对，Apache-2.0 全量可下**（`vc_data/13_scaling_tasks.md:1143`）——这是本地所有笔记里**规模最大、许可最干净的 Manim 相关数据集**，但它不在本次指定数据源里，正文引用前建议再核一次。

## 2.3 可做成确定性判据的信号

### 笔记里**明确有**的
1. **渲染是否成功**（本方向第一判据，且数据充分）：
   - TEB 的成功率是一等指标：o3-mini 93.8%、GPT-4o 55.0%、Claude-3.5-Sonnet 2.1%、Gemini-2.0-Flash 14.6%（`deep_video.md:31`）。
   - **重试策略直接决定成功率**：不重试时成功率极低，**重试 5 次后可达九成**（`deep_video.md:27`）。
   - `env/video.md:8` 把「渲染成功率：代码能否无错渲染」明确列为**可执行、可复现**的验收方式。
2. **版式几何检查（元素是否重叠、出框）**：`env/video.md:8` 明确列为**可执行**判据。落地实现是 Code2Video 的 Critic——把画布切成 **6×6 锚点栅格**，对照「**元素到代码行的占用表**」判断重叠与出框，并给出「某元素该移到哪个格子」的**可定位指令**再回改代码（`deep_video.md:10`）。
   口径注意：**判重叠的那一步是 VLM 在看**（原文「让视觉语言模型对照占用表判断」），但「元素 → 代码行」的占用表本身是程序侧的，所以这是半确定性，不是纯几何。
3. **消融证明几何判据有价值**：去掉锚点栅格，GPT-4.1 掉到 69.2 / 55.2（满配 82.0 / 对应观感）（`deep_video.md:15`）。
4. **知识传递答题可执行可复现**：TeachQuiz / PaperQuiz 被 `env/video.md:9,44` 列为**可以作为主指标**的一类（屏蔽知识得基线 → 只看视频答十题 → 取差值）。
5. **逐帧确定性是这条路线的根**：每一帧是帧号与代码的纯函数，同代码同帧永远渲染出相同像素，所以可逐帧复现、可测试、可迭代——扩散视频没有这个性质（`env/video.md:21`）。这是「为什么 Manim 线可以做硬判据」的总论点。
6. **渲染反馈可以直接当 RL 奖励**（邻域已验证）：VAnim 用渲染感知 RL（GRPO），成功率 **100%**（对 Gemini 3 Pro 的 86.2%）（`deep_video.md:106`）；SimuScene 用代码渲染视频后逐条 VLM 二元 Code-Video-Judge 做 GRPO，**最强 LLM 仅 21.5% Avg@8，RL 后 32B 达 72.2% Pass@8**（`benchmarks.md:157`）。
7. `[vc_data·非指定源]` **纯确定性的坐标检查已有现成基准**：PRISM 刻意不用 VLM，Spatial Pass = 渲染成功 + 审计帧无 **overlap / out-of-bounds / leakage**；并给出最有用的那条结论——**Exec → Spatial 平均掉 41.24 点，只报执行率的指标没有信息量**（`vc_data/07_capability_spec.md:122`）。
8. `[vc_data·非指定源]` **时间维度有可抄的确定性做法**：ManimBench 的 5FPS 抽帧 + SSIM 双向最佳匹配 + fastDTW；Animation2Code 的 CoTracker3 位移方向 cos + 幅值 min/max 比 + Chamfer 匹配。两者都是现成实现，但**没人把它做成通用 codegen 的时间子分**（`vc_data/07_capability_spec.md:622`）。

### 笔记里**没有**的
- `[笔记无·待补]` **时长是否符合要求**：指定源里只有「超过 5 分钟的长视频」这种定位描述（`deep_video.md:21`），**没有任何基准把时长当判据**。
- `[笔记无·待补]` **关键帧元素是否出现**的程序化判据：ManimAgent 确实查四张关键帧，但是**VLM 按逻辑流 / 布局遮挡 / 准确性打分**（`deep_video.md:119`），不是确定性断言。
- `[笔记无·待补]` **音画是否对齐**的确定性判据：TTS 配音在多条管线里都有（TEA、Paper2Video、PresentAgent），PresentAgent 流程写了「音画对齐合成视频」（`pipelines.md:269`）、PresentEval 有「音视频打分」（`benchmarks.md:181`），但**没有任何一条给出对齐的可执行判据或阈值**。
- `[笔记无·待补]` **场景对象树（Mobject 树）回读**作为判据——两个引擎都是原生 scene-graph 栅格化（`pipelines.md:282-283`），结构上可读，但笔记里没有任何工作这么用。（PPT 侧有对应证据：`vc_data/05_trajectory_repair.md:864` 的 pptx 拦截 shape 构造；**Manim 侧无对应记录**。）
- `[笔记无·待补]` **字幕 / 讲稿与画面的文本一致性**判据。
- `[笔记无·待补]` **渲染耗时 / 资源预算**作为判据（成本数字有，判据没有）。

## 2.4 已知难点（按你点的四类组织）

### (a) Manim 版本 / API 漂移
- **笔记里有的间接证据**：TheoremExplainAgent 专门做了 **Agentic RAG，以 Manim 文档为知识库**，在分镜、技术实现、纠错三个阶段各自生成检索查询并缓存（`deep_video.md:28`）——即「模型不掌握当前 API」被当成一个需要专门机制解决的问题。但该机制自身也是失败源：**RAG 检索常不相关且抬高成本**（`deep_video.md:34`）。
- **两个引擎并存且都在活跃**：3b1b/manim 94.9k star（OpenGL 原生）vs Manim Community 41.5k star（Cairo/OpenGL，**文档稳定、教学主力**）（`pipelines.md:282-283`）。笔记给 Community 的描述是「文档稳定」，隐含 3b1b 版不稳。
- **ManimAgent 的负通道记忆就是在存 API 陷阱**：检索正通道前 2 条成功经验 + 负通道前 3 条失败模式，负例以「已知陷阱」注入（`deep_video.md:116-117`）；**乱序记忆退回 69.6，说明生效的是检索到相关经验而不是多塞上下文**（`deep_video.md:122`）。
- `[笔记无·待补]` **没有一条笔记直接写「Manim 版本 / API 漂移」四个字，也没有版本间断裂的量化数据。** 这一条你要自己补证据，我只能给上面三条间接信号。

### (b) 渲染耗时与成本
- Code2Video：每主题约 **13.8 分钟 / 43.1K token**，比直接写码**慢 5–8 倍、多耗 15–20 倍 token**（`deep_video.md:16`）。
- Paper2Video（同一实验室、Beamer 线）：逐页并行把 **287 分钟压到 48 分钟**，仍需 62K token（`deep_video.md:46,52`）。
- `[vc_data·非指定源]` 同一仓库的 Web 侧实测给了「为什么耗时决定判据选型」的量级：渲染约 470ms / 截图约 110ms / **回读 1–4ms**，回读是渲染耗时的千分之四，**所以回读能放进 RL 每一步、截图不行**（`vc_data/draft_domains.md:24`）。
- `[笔记无·待补]` **Manim 单条渲染的墙钟耗时没有直接数字**（13.8 分钟是整条 agent 管线，含模型调用）。

### (c) 评测只能靠人或 VLM 看视频
这是本方向证据最充分的一条难点，有四条独立数字：
1. **ManimAgent 实测其 VLM 判官与人评相关系数为 −0.17**，故仅内部使用，最终质量以 **54 名评分者盲评**为准（`deep_video.md:123`、`:121`）。`env/video.md:51` 把这条升级成全域结论：「VLM 看图打分不可靠……并明确把 VLM 排除在头部评测证据之外」。
2. **TEB 的部分自动指标与人评相关弱**：只有视觉相关性 **0.72**、元素布局 **0.42** 显著，准确深度 **0.14**、逻辑流 **0.16** 近乎无关（`deep_video.md:34`）。
3. **Code2Video 的 0.971 不是你以为的那个相关**：观感与 TeachQuiz 相关 0.971 是**人评内部一致性**，不是对 VLM 判官的验证（`deep_video.md:17`）。引用时必须带这句口径。
4. **短暂遮挡下视频语言模型常漏检而人眼能看出**（`deep_video.md:17`）。
5. 总论：`env/video.md:44` —— 可执行检查（渲染成功率、版式几何）和知识传递测试（TeachQuiz / PaperQuiz）**可以作为主指标**；VLM 看图打分**只能作参考**。这句话是两个方向共用的最有力论断。

### (d) 其他失败模式
- **元素布局是全线普遍弱项**：TEB 各模型 0.57–0.73（`deep_video.md:32`）；**版式错位与元素重叠，化学尤甚**（`deep_video.md:34`）。
- **代码脆弱**：**重试五次仍有渲染失败**（`deep_video.md:34`）。
- **一处报错拖垮整段**是显式要解决的问题：Code2Video 的调试器分三级自修复——先改行、再改块、不行整段重写（`deep_video.md:9`）。
- **规划比修补重要**：消融里去掉 Planner 掉到 38.1 / 40.5，是最吃重的一环（`deep_video.md:15`）。
- **叙事与编排仍逊人类**，吸引力与视觉一致性偏弱；闭源模型的「遗忘」只能靠提示而非改参数（`deep_video.md:17`）。
- **最缺的是失败后如何修复的轨迹数据**：公开数据几乎全是一次成功的配对；ManimAgent 的双通道记忆是少数带迭代过程的工作（`env/video.md:53`）。
- **记忆路线自身的局限**：只测 Manim 与 5 个英文领域；记忆规模仅约百条，更大需去重或层级索引；**写回门控依赖当前 VLM，模型升级后可能记忆腐化**（`deep_video.md:123`）。
- **厂商侧完全空白**：MMMC、TeachQuiz、TheoremExplainBench 等**没有出现在任何厂商的发布材料里**；厂商的信号只有两种——社区的全代码成片技能潮、发布页的动画 demo（`env/video.md:73-75`）。

## 2.5 它作为 V2 辅助方向：最成熟 / 最不成熟

**最成熟的部分（可以认为「稍微有一定能力即可」）**
- **渲染引擎与逐帧确定性**：3b1b/manim 94.9k star、Manim Community 41.5k star，都是原生 scene-graph 栅格化 + ffmpeg，文档稳定（`pipelines.md:282-283`）；`env/video.md:52` 直接说「渲染器基础设施已成熟」。逐帧是帧号的纯函数这条性质使它天生可测（`env/video.md:21`）。
- **「能不能跑」这一闸已被打穿**：o3-mini 成功率 93.8%（`deep_video.md:31`）；加 5 次重试就能到九成（`deep_video.md:27`）。
- **知识传递已接近人类**：TeachQuiz 86.0 对人类 97.1，而扩散基线 Veo3 只有 2.5、OpenSora-v2 为 0.0（`deep_video.md:13`）——「写代码出视频」对「直接生成像素」的优势是数量级的，这一点已无争议。
- **窄域小模型够用**：DTVBench 上 7–14B 开源逼近或超过商用（`benchmarks.md:155`）；`[vc_data]` ManimBench 上 30B + GRPO 全场最好（`vc_data/STATE.md:38`）、SimuScene RL 后 32B 72.2% Pass@8 对最强闭源 21.5%（`benchmarks.md:157`）。`vc_data/07_capability_spec.md:398` 的结论是「**开源 + 专项 RL 在动画与时间这一维已全面反超**」。
  → **这组数字正是「Manim 不必当主力」的依据：引擎成熟、执行门已过、专项小模型就能赢，主力模型只需具备一定基础能力。**

**最不成熟的部分**
- **版式几何（元素布局）**：TEB 全线 0.57–0.73，是「普遍弱项」的原话（`deep_video.md:32`、`benchmarks.md:153`）。
- **「能执行」到「空间正确」之间有巨大落差**：`[vc_data]` PRISM 实测 **Exec 0.945 → Spatial 0.572，平均掉 41.24 点**（`vc_data/07_capability_spec.md:122`）。这是反驳「渲染成功率高就等于做得好」的最锋利一个数字。
- **时间维度几乎是空白**：`[vc_data]` Animation2Code 的 Temporal 全场天花板只有 **0.31**（Appearance 已到 0.84），是「全行业最弱的一格」（`vc_data/07_capability_spec.md:122,673`）；本次指定源里**没有任何一条时长 / 音画对齐的确定性判据**（§2.3 空缺清单）。
- **评测可信度**：VLM 判官与人评 −0.17（`deep_video.md:123`），TEB 的准确深度 / 逻辑流与人评近乎无关（0.14 / 0.16）（`deep_video.md:34`），最终仍要 54 人盲评（`deep_video.md:121`）。
- **成本**：13.8 分钟 / 43.1K token 每主题，慢 5–8 倍、多 15–20 倍 token（`deep_video.md:16`）。
- **缺修复轨迹数据**，且唯一做了的 ManimAgent 只「计划开源」（`pipelines.md:278`、`env/video.md:53`）。

## 2.6 Manim 方向 · 量化数字清单

| 数字 | 说明什么 | 出处 |
|---|---|---|
| 240 | TheoremExplainBench 定理数（4 学科 × 3 难度 × 80） | `benchmarks.md:153`、`deep_video.md:29` |
| 93.8% / 0.77 | TEB 上 o3-mini(medium) 的渲染成功率 / 5 指标几何平均总分（成功率最高） | `deep_video.md:31` |
| 55.0% / 0.78 | TEB 上 GPT-4o 的成功率 / 总分 | `deep_video.md:31` |
| 2.1% / 0.79 | TEB 上 Claude-3.5-Sonnet：**总分最高但几乎渲染不出来**，证明总分口径会骗人 | `deep_video.md:31` |
| 14.6% / 0.76 | TEB 上 Gemini-2.0-Flash | `deep_video.md:31` |
| 0.57–0.73 | TEB 元素布局分区间，全模型普遍弱项 | `deep_video.md:32` |
| 5 次 → 九成 | 渲染失败重试次数与成功率的关系（不重试时成功率极低） | `deep_video.md:27` |
| 9/15（60%） | 看动画视频后把错误文字解释改判为错的人数比例 | `deep_video.md:33` |
| 456 | MMMC 单元数（117 主题 / 13 学科 / 339 子片），全部取自 3Blue1Brown | `benchmarks.md:154`、`deep_video.md:11` |
| 40.0 → 86.0 | Code2Video 上 Claude Opus 4.1 的 TeachQuiz（直接写码 → 三 agent 闭环） | `deep_video.md:13` |
| 37.0 → 82.0 / 36.5 → 80.0 | 同口径 GPT-4.1 / GPT-5 | `deep_video.md:13` |
| 97.1 | 人类 3Blue1Brown 的 TeachQuiz 上界 | `deep_video.md:13` |
| 2.5 / 0.0 | 扩散基线 Veo3 / OpenSora-v2 的 TeachQuiz——代码路线对像素路线的数量级优势 | `deep_video.md:13` |
| 37.8 → 87.9（人类 99.7） | Code2Video 观感均分（VLM 5 轴） | `deep_video.md:14` |
| 38.1 / 40.5 | 去掉 Planner 后的消融（最吃重的一环） | `deep_video.md:15` |
| 69.2 / 55.2 | 去掉 6×6 锚点栅格后的消融——几何判据的价值量化 | `deep_video.md:15` |
| 72.5 / 60.7 | 去掉 Critic 后的消融 | `deep_video.md:15` |
| 13.8 分钟 / 43.1K token | Code2Video 每主题成本；比直接写码慢 5–8 倍、多 15–20 倍 token | `deep_video.md:16` |
| 0.971 | 观感与 TeachQuiz 的相关系数，**但这是人评内部一致性，不是对 VLM 判官的验证** | `deep_video.md:17` |
| 0.72 / 0.42 / 0.14 / 0.16 | TEB 自动指标与人评的相关：视觉相关性 / 元素布局（显著）/ 准确深度 / 逻辑流（近乎无关） | `deep_video.md:34` |
| −0.17 | ManimAgent 的 VLM 评分与人评相关系数——VLM 判官不可信的最硬一个数字 | `deep_video.md:123`、`env/video.md:51` |
| 62.0 → 84.9 | ManimAgent 从空记忆到满库 200 条的一次通过率 | `deep_video.md:122` |
| 12.2 → 6.5 | 同上的反思轮数（砍掉近一半） | `deep_video.md:122` |
| 3.26 → 3.88 | 同上的人评质量分 | `deep_video.md:122` |
| 83.3 / 11.4 | 等预算代码检索基线的一次通过率 / 反思轮数（ManimAgent 仅打平通过率但轮数更少） | `deep_video.md:122` |
| 69.6 | 乱序记忆的一次通过率——证明生效的是检索相关性而非上下文量 | `deep_video.md:122` |
| 25 任务 / 54 名评分者 | ManimAgent 最终质量的盲评规模 | `deep_video.md:121` |
| 39 / 33 / 40 | ManimAgent 任务流切分：建库 / 固定探针 / 交叉测试 | `deep_video.md:121` |
| 102 | DTVBench 可视化任务数（含 Manim、Mathematica）；结论「7–14B 开源逼近商用」无绝对分 | `benchmarks.md:155` |
| 200 题 | VisualEDU 规模（6 类 × 3 难度）；难题上 Claude-3.7-Sonnet、GPT-4o 均 < 56% | `benchmarks.md:156` |
| 12 题 | ManiBench 在 HF 上的真实规模（摘要称 150–200），**已被排除，别引用** | `benchmarks.md:147`、`vc_data/13_scaling_tasks.md:1147` |
| 94.9k star | 3b1b/manim（引擎） | `pipe_meta_video.json` 第 20 条 |
| 41.5k star | Manim Community（引擎，文档稳定、教学主力） | `pipe_meta_video.json` 第 21 条 |
| 2.1k / 1.5k / 74 star | Code2Video / TheoremExplainAgent / manimator 的 GitHub star | `pipe_meta_video.json` 第 8 / 3 / 6 条 |
| 21.5% → 72.2% | SimuScene：最强 LLM Avg@8 对 RL 后 32B Pass@8——渲染反馈当 RL 奖励的收益 | `benchmarks.md:157` |
| 100% vs 86.2% | VAnim（渲染感知 RL）渲染成功率 vs Gemini 3 Pro（邻域证据） | `deep_video.md:106` |
| 0.945 → 0.572（−41.24 点） | `[vc_data]` PRISM 的 Exec → Spatial 落差，95% CI [40.41, 42.11]——「只报执行率没有信息量」 | `vc_data/07_capability_spec.md:122` |
| 10,372 / Apache-2.0 | `[vc_data]` PRISM 的 instruction-code 对数量与许可，全量可下，Manim 同域 | `vc_data/13_scaling_tasks.md:1143` |
| 94% / 85.7% | `[vc_data]` ManimBench 上 Qwen3-Coder-30B-A3B + GRPO + RITL，全场最好 | `vc_data/07_capability_spec.md:122` |
| 0.31 | `[vc_data]` Animation2Code 的 Temporal 全场天花板（Appearance 已 0.84）——时间维度是全行业最弱一格 | `vc_data/07_capability_spec.md:122,673` |

---

# 三、两个方向的横向对比（写正文时可直接用的一张表）

| 维度 | PPT 方向 | Manim 方向 |
|---|---|---|
| 公开 benchmark 条数（指定源内） | **5**（SlidesBench / PPTEval / PaperQuiz / PresentEval / Paper2Video） | **4**（TEB / MMMC / DTVBench / VisualEDU）+ 1 自建任务流（ManimAgent） |
| 基准规模量级 | 30 ~ 585（最大 SlidesBench 585 测试） | 102 ~ 456（最大 MMMC 456 单元） |
| 数据可下载的管线条数 | **5 / 5 全可下** | **2 条数据可下（TEB 240、MMMC 456）+ 4 条代码/引擎可下 + 1 条未开源（ManimAgent）** |
| 产物语言 | python-pptx（3）、SlidesLib（1）、Beamer LaTeX（1） | Python + Manim（全部）；引擎两套（3b1b / Community） |
| 执行层成熟度 | 高：套模板编辑成功率 95.0%（GPT-4o 97.8%） | 高：o3-mini 93.8%，重试 5 次可达九成 |
| 最强「超人类」证据 | PresentQuiz 0.842 > 人类 0.738 | TeachQuiz 86.0（人类 97.1，**未超**） |
| 最大短板 | 整体观感 PresentArena 17.0%（人类 50%） | 元素布局 0.57–0.73；`[vc_data]` Exec→Spatial 掉 41.24 点 |
| 确定性判据现状 | 只有执行/编译成功率是硬的；溢出对齐靠 VLM | 渲染成功率 + 版式几何（6×6 栅格，半确定性）；时间维度空白 |
| 单位成本 | 48 分钟 / 62K token 每篇（Paper2Video） | 13.8 分钟 / 43.1K token 每主题（Code2Video） |
| 厂商是否报分 | 否（GPT-5.6 / GLM-5 只有能力声明与内部训练口径） | 否（MMMC / TeachQuiz / TEB 未出现在任何厂商材料） |

**给 V2「这两个方向只需稍微有一定能力即可」的三条共用论据：**
1. 执行门槛已被打穿（95.0% / 93.8%），剩下的差距是观感与版式，不是「能不能跑」。
2. 窄域小模型已能打平或反超前沿（8B ≈ GPT-4o、Paper2Poster 开源版超 GPT-4o 多 agent、7–14B 逼近商用、`[vc_data]` 30B+GRPO 全场最好）——`vc_data/07_capability_spec.md:400` 的原话是「任务一旦窄到有确定性 verifier，小模型就能打平前沿，这是全表最一致的规律」。
3. 两个方向的评测可靠的那一半（渲染成功率、版式几何、看产物答题）和 html / webdev 主力线的判据是同一套机制（DOM/对象树回读 + 几何检查），**主力线做强了会顺带带起这两个方向**；而它们各自不可靠的那一半（VLM 观感打分）投入也换不来可信提升（−0.17）。

---

# 四、本地笔记在「确定性判据」这块的覆盖程度（自评）

| 判据 | PPT 方向 | Manim 方向 |
|---|---|---|
| 渲染 / 编译是否成功 | **有**（PPTAgent 95.0%、Beamer 编译反馈修复） | **有，且有横向数据**（4 个模型的成功率、重试收益） |
| 元素重叠 / 出框 | 信号有、**做法是 VLM**（Paper2Poster Painter-Commenter） | **有半确定性做法**（6×6 锚点栅格 + 元素→代码行占用表，判定仍由 VLM 做）；`[vc_data]` PRISM 有纯确定性版 |
| 文字溢出版面 | 信号有、做法是 VLM；`[vc_data]` 有坑与阈值 | 笔记无单独的文字溢出判据 |
| 对象树可回读 | `[vc_data]` 有实现路径（pptx 拦截 shape 构造） | **无**（引擎结构上可读，但没人这么用） |
| 页数 / 标题 / 字数等指令遵循 | **无** | **无** |
| 时长是否符合 | **无** | **无** |
| 关键帧元素是否出现 | **无** | 有但是 **VLM 打分**（ManimAgent 四关键帧） |
| 音画是否对齐 | 流程里有、**判据无** | 流程里有、**判据无** |
| 时间 / 运动正确性 | **无** | 指定源**无**；`[vc_data]` 有两套现成做法（ManimBench SSIM+fastDTW、Animation2Code CoTracker3） |
| 看产物答题（可复现） | **有**（PaperQuiz / PresentQuiz / PresentEval quiz） | **有**（TeachQuiz，含屏蔽知识取基线的完整口径） |
| 几何判据的工程坑与阈值 | 指定源无；`[vc_data]` 有（变换矩阵、双边界、≤0.05） | 指定源无；`[vc_data]` 有（同上，Web/图表侧实测） |

**一句话总结**：本地笔记对「**能不能跑**」和「**看产物答题**」这两族确定性判据覆盖得很好（有横向数据、有口径、有消融）；对「**版式几何**」只覆盖到「存在且重要」的程度，落地做法基本都挂在 VLM 上；对「**时长 / 音画对齐 / 指令遵循型硬约束**」在指定数据源里是**零覆盖**，只有同仓库的 `vc_data/` verifier 笔记里能借到可抄的做法（PRISM、ManimBench、Animation2Code），但那几条不在你给的数据源清单里，正文引用前建议再核一遍原文。

