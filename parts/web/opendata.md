## 1 Inventory

Web 的公开数据按产物技术栈分四类，不按输入模态分：html 与 webdev 是主力，ppt 与 manim 够用即可。公开的数据管线与 benchmark 常出自同一篇论文，因此并进一张表：供给几乎全压在单文件「截图 → 代码」，多文件工程只有 2 条管线。

| 技术栈 | 产物 | 验收能做到哪一步 | 数据管线 | Benchmark | 这意味着什么 |
|---|---|---|---|---|---|
| html（主力） | 单文件 HTML、SVG、React 组件、图表绘图代码、TikZ | 渲染一次就能比对，DOM 盒模型与逐值回读都可用 | 35 | 32 | 供给充足，但形态高度同质 |
| webdev（主力） | 多文件可运行 Web App | 要起服务、要 agent 操作，验收依赖运行时状态 | 2 | 13 | 题有人出，数据没人放——这正是真实生产的形态 |
| ppt（辅助） | 幻灯片、海报、演讲视频 | 产物是版面对象树，可逐对象回读 | 5 | 5 | 够做辅助能力，不够做主力 |
| manim（辅助） | 代码驱动的讲解动画 | 产物是视频，判据只能落在渲染成功、时长与关键帧 | 8 | 5 | 管线里有三条是渲染库本身 |

<!--ALL:html,webdev,ppt,manim-->

1. 分类看产物，不看输入：输入是截图还是文字，换的只是 Query；产物是单文件还是多文件工程，换的是整条验收链路。
2. 主力与辅助按能不能产出可训练的判定信号来分，不按难度分。
   - ppt 与 manim 够用即可，不自建，也不单开小节，只在本节的表里按技术栈列出
3. html 条目最多、Verifier 最成熟，但早期题目只适合做回归测试。
   - [Design2Code](https://arxiv.org/abs/2403.03163)：484 个真实网页按渲染相似度打分；厂商自报相似分已在 93 以上（GLM-5V-Turbo 94.8、Qwen3-VL-235B-Thinking 93.4）
   - 图表与 SVG 一支最确定：产物能逐值回读，不用看图
4. webdev 倒挂：benchmark 13 条，数据管线只有 2 条，且出自同一组作者。
   - WebGen-Instruct：训练集 6,600 余条、测试集 100 余条；WebGen-Agent：700 条轨迹、500 条指令
   - 这个量级撑不起一次完整的难度分桶
5. webdev 的分数还没饱和，模型差距拉得开。
   - [WebGen-Bench](https://arxiv.org/abs/2505.03733)：UI agent 执行 647 个测试用例，最好组合 27.8%
   - [Vibe Code Bench](https://www.vals.ai/benchmarks/vibe-code)：从规格说明构建并部署应用，论文最好模型 61.8%；接入外部服务后从 71% 降到 30%
6. 起点是合成，规模也靠合成。
   - 2017 年 pix2code 随机生成领域专用语言再渲染出截图；2024 年 WebSight 把同一思路推到约 200 万条
7. 2025 年后，管线报告的重心从数据量转向 Verifier。
   - 早期报数据量；近两年报渲染成功率、交互契约，并把渲染反馈直接当 RL reward
8. 同源的训练集与测试集必须分开用，因此去污染必须做。
   - 做法与效果数字见 Sources 页的 Curation Pipeline

## 2 Timeline

<div class="tl-wrap"><div class="tl"><div class="tl-band"><span>评测对象：输出是否与参考一致</span><i></i><span>输出能否使用</span></div><div class="tl-col" style="--c:#9aa1ab"><div class="tl-date">2023 – 2024-06</div><div class="tl-node"></div><div class="tl-title">截图转代码</div><div class="tl-chips"><span class="tl-chip m-vis">视觉相似度</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2403.03163">Design2Code</a><span>2024-03</span></div><p>484 个真实网页；标注者判 GPT-4V 生成页 49% 可替代原页</p><div class="tl-m later"><span class="bar"><i style="width:94.8%"></i></span><b>94.8</b><em>2026 厂商自报（GLM-5V-Turbo）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a><span>2024-04</span></div><p>2.56M 条图码配对</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2406.20098">Web2Code</a><span>2024-06</span></div><p>1179.7k 条指令对</p></div></div><div class="tl-col" style="--c:#7f8fc4"><div class="tl-date">2024-07 – 2024-12</div><div class="tl-node"></div><div class="tl-title">多轮交互反馈</div><div class="tl-chips"><span class="tl-chip m-vis">视觉相似度</span><span class="tl-chip m-vote">人工投票</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2410.16232">Sketch2Code</a><span>2024-10</span></div><p>731 张手绘草图 + 多轮反馈；10 个 VLM 均难读懂草图</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2411.03292">Interaction2Code</a><span>2024-11</span></div><p>374 个交互；交互部分得分低于整页生成</p></div><div class="tl-card"><div class="nm"><a href="https://arena.ai/blog/webdev-arena">WebDev Arena</a><span>2024-12</span></div><p>8 万+ 票；平局率 26%（Chatbot Arena 35%）</p></div></div><div class="tl-col" style="--c:#6380d6"><div class="tl-date">2025</div><div class="tl-node"></div><div class="tl-title">验收产物</div><div class="tl-chips"><span class="tl-chip m-agent">agent 实测</span><span class="tl-chip m-mllm">MLLM checklist</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2505.03733">WebGen-Bench</a><span>2025-05</span></div><p>647 个测试用例由 UI agent 执行</p><div class="tl-m"><span class="bar"><i style="width:27.8%"></i></span><b>27.8%</b><em>发布时最好</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2505.11935">ChartEdit</a><span>2025-05</span></div><p>1,405 条图表编辑指令</p><div class="tl-m"><span class="bar"><i style="width:59.96%"></i></span><b>59.96</b><em>发布时最好</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2507.04952">ArtifactsBench</a><span>2025-07</span></div><p>1,825 个任务；与 WebDev Arena 排名一致性 94.4%</p></div></div><div class="tl-col" style="--c:#4876ea"><div class="tl-date">2025-12 – 2026-04</div><div class="tl-node"></div><div class="tl-title">端到端交付与多轮编辑</div><div class="tl-chips"><span class="tl-chip m-agent">agent 实测</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2601.04203">FronTalk</a><span>2025-12</span></div><p>100 段多轮对话；模型会覆盖已实现的功能</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2603.04601">Vibe Code Bench</a><span>2026-03</span></div><p>964 条工作流由浏览器 agent 走查</p><div class="tl-m"><span class="bar"><i style="width:61.8%"></i></span><b>61.8%</b><em>论文最好</em></div><div class="tl-m later"><span class="bar"><i style="width:90.35%"></i></span><b>90.35%</b><em>v1.1 榜单 2026-09；差距成因口径待补</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2604.13648">Figma2Code</a><span>2026-04</span></div><p>213 例；闭源模型视觉保真高，响应式与可维护性差</p></div></div><div class="tl-col" style="--c:#2f6bff"><div class="tl-date">2026-06 – 2026-07</div><div class="tl-node"></div><div class="tl-title">长页面与多页状态</div><div class="tl-chips"><span class="tl-chip m-agent">agent 实测</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.17727">LongWebBench</a><span>2026-06</span></div><p>490 个长网页；页面越长，结构保真度越低</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2607.06306">UI2App</a><span>2026-07</span></div><p>45 组多页状态序列；跨页状态上一半模型得 0 分</p></div></div></div></div>
<div class="tl-legend"><span><i style="background:var(--brand)"></i>发布时最好成绩</span><span><i style="background:#b8bfc9"></i>后续成绩（厂商自报或榜单）</span></div>

## 3 Gaps

公开数据稳定提供的只有图码配对（一张截图与一份源码），因此它是无监督训练与蒸馏的素材，不是 RL 任务的来源。

- 补齐方式：Query 见 Sources 页，Verifier 见 Verifier 页，Harness 见 Train 页

可验证任务需要的 Query（题干）、Verifier（判据）、Harness（运行环境）与难度标注，公开数据都不稳定提供。

1. 公开管线的 Query 来自产物反推或模型改写，不来自真实用户。
   - 两种来源的占比，口径待补
2. 公开管线以视觉相似度或 MLLM 打分判定，不提供可程序化执行的 Verifier。
   - 两种判定方式的占比，口径待补
3. 公开基准常不记录 Harness 版本，因此结果不可复现。
   - BlenderGym（CVPR，3D 方向）未写明所用 Blender 版本；Web 方向的同类统计口径待补
4. 公开数据不提供难度分桶，而截图转代码偏易，因此不分桶时 RL 奖励没有区分度。
   - Design2Code 上厂商自报分数在 93 以上：GLM-5V-Turbo 94.8、Qwen3-VL-235B-Thinking 93.4

## 4 How To Choose

按目标能力选，不按名气选：执行类与 agent 实测类可以当主指标，MLLM checklist 要先与人工评审对齐，纯视觉相似度只作参考。

| 目标能力 | 用哪些 | 能不能当主指标 |
|---|---|---|
| 交互实现 | Interaction2Code、WebIGBench、UI2App | 能，由 agent 实测 |
| 功能正确与端到端交付 | WebGen-Bench、Vibe Code Bench | 能，但必须锁 harness 版本 |
| 多轮编辑 | FronTalk、1D-Bench、ChartEditBench | 能 |
| 图表与 SVG 精度 | ChartMimic、Chart2Code、SVGenius | 能，逐值回读 |
| 审美与设计质量 | ArtifactsBench、UI-Bench、WebDev Arena | 不能直接当，需先与人工评审对齐 |
| 视觉还原 | Design2Code、WebCode2M | 只能做回归测试 |

