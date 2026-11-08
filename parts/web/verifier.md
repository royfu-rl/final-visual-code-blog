## 3 Verifier

Verifier 评估 Agent 在 Harness 里完成用户的多模态参考请求（Omni Reference Query）后交付的代码产物质量。

- 用于蒸馏轨迹质量评估，或 RL 训练过程的 reward function。

### 3.1 Overview

Verifier 围绕两个核心维度评判 Agent 交出的产物：

- **功能性（Functionality）**：题目要求的是否都实现；没要求的部分不检查，除非它破坏了要求项
- **审美性（Aesthetics）**：美学质量评估

两者的关系是：**功能性作为硬约束，审美性仅用于可行解之间的偏好排序。**

图 3.1 是评测流程：

Agent Rollout Task（执行任务）→ Prepare artifacts（准备产物）→ Verifier（评审功能性和审美性）→ Reward

<div class="wide-embed"><iframe src="../assets/figures/webdev-pipeline.html" style="height:640px;border:0" title="WebDev workflow"></iframe></div>
<p style="margin-top:8px;font-size:12.5px;color:var(--ink-soft);text-align:center">图 3.1　Web 的 Verifier 评测流程</p>

#### 3.1.1 Glossary

本章与 3D 页通用。

| 术语 | 含义 |
|---|---|
| 改坏的样本 | 故意改出真错误，应判挂 |
| 换写法的样本 | 写法变了、结果一样，应判过 |
| 抓错率 | 改坏的样本被判挂的比例 |
| 放对率 | 换写法的样本被判过的比例 |
| Critic | 模型评审：看渲染结果、自己操作页面、输出问题清单的 VLM Agent（打分场景叫「打分模型」） |

#### 3.1.2 Reward Function

$$r = g\cdot(1+\lambda\,w),\qquad 0<\lambda\le 1$$

- $g=\prod_{k=0}^{3}\mathbf{1}[\,L_k\ \text{pass}\,]\in\{0,1\}$：功能闸，L0–L3 全部通过为 1，任一层不过为 0
- $w\in[0,1]$：审美胜率，只在组内通过者之间两两比较得出
- 由于 $\lambda\le 1$，任一通过者 $r\ge 1$、任一失败者 $r=0$；公式为本文建议，未实测

1. 功能全过才算，不加权、不给部分分。
   - 加权会让强项补弱项；同 [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) harness「任一维度低于硬阈值即整体失败」，本项目跑通的 verifier 亦然
   - 部分分和真实满足的关系接近抛硬币（〔外部〕游戏任务里源码分落在 0 到 1 之间的规则，真玩满足率 54.3%，[A2Z GameSpec-Bench](https://arxiv.org/abs/2609.39564) §4.3）
2. 前层不过，后层不跑。
3. 审美只在通过者之间排名次。
4. 代价是奖励稀疏：$r$ 近似二值；同一题的一组采样全部通过或全部失败时，组内相对优势为零，不产生梯度。
   - 实测：three.js 修复题（16 题 × 8 次采样，温度 1.0）仅 3/16 = 19% 有非零梯度（Wilson 95% CI 6.6%–43.0%）；Web 未测
   - 推算：组大小 8、通过率 0.1 时，整组失败的概率为 $0.9^8\approx 43.0\%$
   - 缓解：以被训模型自身的 pass@k 做难度过滤，配合动态采样；跨模型汇总的通过率会虚构出中等难度，不宜使用

### 3.2 Functionality

功能性回答「需求有没有都实现、有没有多做」：按 L0–L3 四层逐条判 0 或 1，判据是页面运行后的状态。能写成断言的交给程序，写不死的交给 Agent 动手操作，VLM 只补程序读不出的外观。

#### 3.2.1 Judges & Rules

**1. Agentic Critic: Checklist Decomposition**

Critic 本身是 Agent：能写程序、派 subagent 动手操作、调 VLM 看画面，用这些能力完成 L0–L3 四层功能校验。

1. Critic 按 L0–L3 拆检查清单：评审时读题目和参考文件，每层拆出若干条，每条对应题目里的一句话；同一道题只拆一次并冻结（规则 7）
2. 逐条分派给三类判别方：能写成断言或固定脚本的，Critic 直接写成程序，每份作品执行一遍；写不死的多步流程，交给 Agent 自己操作页面；只有看画面才能判的外观，交给 VLM 看截图
3. 每条输出 0 或 1，按 L0 → L3 的顺序判，前一层不过，后面的层不再判

**2. Layers**

| Layer | Checks | Method (Program / Agent / VLM) | Used by | Evidence |
|---|---|---|---|---|
| **L0 执行** | 能打开、出画面吗 | <span class="judge j-prog">Program</span>执行检查：页面能打开、控制台无报错、画面非空白 | [MiMo-V2-Flash](https://arxiv.org/abs/2601.02780) | - |
| **L1 结构** | 元素属性、图表数值对不对 | <span class="judge j-prog">Program</span>DOM / 样式回读：元素在不在、文字内容、属性与计算样式（字号、颜色）、元素个数，如标题是 32px 吗；图表逐值回读：图表数值，如柱值 120 / 150 / 90 / 200<br><span class="judge j-agent">Agent</span>结构因作品而异、断言写不死的项，如「有一个可筛选的表格」，要先读懂页面才能定位<br><span class="judge j-vlm">VLM</span>图片、图标画的是什么，如「首图是一张山景照片」；DOM 里只有图片地址 | [WebRenderBench](https://arxiv.org/abs/2510.04097) · [ChartMaster](https://arxiv.org/abs/2508.17608) | 像素看不出数据错：改一个数据点像素差极小（[本项目图表实测 · 3.2.2](#verifier-experiments)） |
| **L2 布局** | 摆放对不对 | <span class="judge j-prog">Program</span>布局几何：元素重叠、出框、横向溢出、对齐与顺序，如按钮压没压图表<br><span class="judge j-agent">Agent</span>交互之后的布局，如展开菜单后有没有遮住正文<br><span class="judge j-vlm">VLM</span>整体乱不乱、文字有没有被截断、图片有没有拉伸变形 | [WebRenderBench](https://arxiv.org/abs/2510.04097) | 需逐元素比，整体比会被大元素稀释（[本项目 Blender 实测 · 3.2.2](#verifier-experiments)） |
| **L3 行为** | 点击反应对不对 | <span class="judge j-prog">Program</span>点击 + 状态差分：能写成固定脚本的路径，如点按钮后回读数据换没换、提交空表单后出现校验提示<br><span class="judge j-agent">Agent</span>写不死的多步流程，如按需求走一遍下单流程，或在编辑器里新建 → 保存 → 重新打开 | [WebGen-Bench](https://arxiv.org/abs/2505.03733) · [Interaction2Code](https://arxiv.org/abs/2411.03292) | 不发输入测不了行为：[V-GameGym](https://arxiv.org/abs/2509.20136) 打分时从没发过输入；[VideoGameBench](https://arxiv.org/abs/2505.18134) 上最好的模型游戏完成度仅 0.48% |
| **L4 美学** | 好不好看 | <span class="judge j-vlm">VLM</span>照专家 rubric（3.3），在通过 L0–L3 的作品之间两两比较 | [UI2Code^N](https://arxiv.org/abs/2511.08195) · [Anthropic][hd] | 比较比打分准：普通打分 83.0 → 两两比较 85.5 → 循环赛 86.0‡（[UI2Code^N][ui2] 图 3a） |

<small style="color:#64748b">‡ 另有只做监督微调的基线，见 3.2.1；读自论文图 3a，未核实</small>

- 一句话：程序管能读出来的，Agent 管要动手探索的，VLM 只管只有看画面才知道的
- 3D 的分层见 3D 页 3.1（场景图、动画曲线、逐部件几何、体素、拓扑）；全局几何见 [CAD-Coder](https://arxiv.org/abs/2505.19713) · [BlenderGym](https://arxiv.org/abs/2504.01786)，不分颜色的体素见 [3D-R2N2](https://arxiv.org/abs/1604.00449)
- 真实网页的渲染一致性可以直接当 reward：[WebRenderBench](https://arxiv.org/abs/2510.04097) 的奖励全部从最终渲染页算，不看代码、不用模型打分，按 0.6 : 0.2 : 0.2 加权区域对齐、几何对齐与样式对齐；样式项比的是匹配元素的前景色、背景色、字号与圆角，元素配对用文字的最长公共子序列大于 0.80（几何对齐一项的口径本项目未记，口径待补）
- L0–L4 是默认分层；游戏等场景可把 L3 拆细，用输入重放 + 状态差分：[PlayCoder](https://arxiv.org/abs/2604.19742) · [GameWorld](https://arxiv.org/abs/2604.07429)

**3. Rubric Rules**

Critic 做功能性校验时依据的 rubric，共八条，每条附佐证。其中第 1、2、8 条是硬约束：任一条不满足，这道题就不能进 RL。

| Rules | Source | Details |
|---|---|---|
| 1. 读运行时状态 | | 按页面跑起来后的 DOM 与计算样式判分，不看源码文本，也不给截图打分；等价实现极多，按代码比对会误杀正确解 |
| | [WorldCoder-Bench][wcb] 表 2 | 只有运行状态与真值相关：读隐藏运行状态 1.000；Agent 探索 +0.111，仅读 DOM −0.021，截图打分 −0.068（three.js，状态不在 DOM 中） |
| | [3JSBench](https://3jsbench.com/) | 确定性检查能区分模型，相似度不能：Astra 80.0% vs. Opus 5.5 49.0%，SigLIP2 相似度仅差约 0.001 |
| | [OpenAI 前端提示文档](https://developers.openai.com/api/docs/guides/frontend-prompt) | 厂商验收清单同样基于运行时：非空白、取景正确、画面在动、资源不重叠（three.js） |
| | [DreamSim](https://arxiv.org/abs/2306.09344) 表 5 | 像素指标与人类判断几乎无关：PSNR、SSIM 一致率 57.1%、57.3%（随机 50%） |
| | [UI2Code^N][ui2] | 相似度作 reward 反而有害：CLIP reward 在 Design2Code、Flame 上均不及纯监督微调 |
| | 反例：AesCoder、WebGen-Agent | VLM 截图分可用于整体质量：作 reward 有效，但评的是整体质量，不是题目明确要求的属性 |
| | 本项目实测（n = 1） | 代码比对会误杀正确解：〔Blender〕一个在世界几何上逐点等同的替代实现通过了全部几何信号（逐部件 F 分数 0.9993），只被代码比对类判据误杀 |
| 2. 只查题目要求的属性 | | 判据能查的信息量不超过题目给出的信息量：题目写明的才检查（如「标题 32px」），不把所有可查属性都拿来和参考页比 |
| | 反例 | 题目只写「杯子要用有别于桌面木色的独立颜色」，判据却要求恰好是参考图里那个蓝：该题无解，reward 与模型行为无关 |
| | 本项目实测（3.2.2 第 2–3 项） | 全查会把对的判错：〔Blender〕所有属性都和参考比时，11 个写法不同但结果正确的作品全被判错 |
| 3. 多种检查组合使用 | | L0–L3 各层的检查同时上，不靠任何一种单独判 |
| | 本项目实测（3.2.2 第 4 项） | 单一检查必有漏网：任一单项检查最多抓到 11 个错误中的 4 个，组合使用后全部判对 |
| 4. 每项检查只输出对错或数值 | | 给出 0/1 或可比较的数（如误差 0.5%），不输出文字评语 |
| | 工程约束 | 文字评语无法自动算 reward |
| 5. 模型评审只做两两比较 | | 判断两个作品哪个更好，不打绝对分；上线前先测与人工判断的一致率 |
| | [UI2Code^N][ui2] 图 3a | 比较优于打分：打分 83.0 → 两两比较 85.5 → 循环赛 86.0（监督微调 82.5；读自图，未核实） |
| | [Error Dependence in LLM Judge Consensus](https://arxiv.org/abs/2609.22512) | 多模型投票增益有限：模型间错误相关 0.206，10 个模型约等效 3.5 个独立模型 |
| | [WorldBench](https://arxiv.org/abs/2610.10622) | 模型评审会改判：未改动的 32 项中 7 项两次判定不一致（21.9%） |
| | [Rubric RL 钻空子研究](https://arxiv.org/abs/2605.12474) | 上线前须验收一致率：专家组内部 95%–97%，强评分模型 92%，弱评分模型 76%–82% |
| 6. 评审与生成分离 | | 判分的 agent 与写代码的 agent 分开，评审亲自操作运行中的页面 |
| | [Anthropic][hd] | 独立评审更易调严：生成器自评倾向自我肯定；评审经 Playwright 实操页面，单次至多 4 小时、迭代 5–15 轮（质检成本见 3.4） |
| | [MiMo-V2-Flash][mimo] | 评审看录屏而非截图：同时评估视觉、功能与可运行性 |
| | 本项目实测（3.2.2 第 10 项） | VLM 能发现遗漏的检查项：雪人头顶未封口，据此新增「网格破洞边数」 |
| 7. 检查清单按题生成、按题冻结 | | 评审时由 Critic 从题目和参考文件拆出清单，每条对应题目里的一句话；同一道题只生成一次，同组作品与重跑共用 |
| | [OpenAI playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) | 清单可由 Critic 临场合成：由题目要求、实现声明与产物合成清单，每条声明对应一项可见检查 |
| | [Anthropic eval 设计博客](https://claude.dev/blog/automating-eval-design-and-hillclimbing/) | 评审查的每一项都须在题目里说出来 |
| | 本文建议（未实测） | 按题冻结、只从题目拆、参考解先过：保证同组作品用同一份清单，作品无法影响查什么 |
| 8. 参考代码只给 Verifier 用 | | 不进 reward，也不进题面；允许的用途有五个：证明题目可解、生成断言、改出改坏的样本、做 verifier 自检、当示范轨迹 |
| | [RaR](https://arxiv.org/abs/2507.17746) 表 1 | 拿参考来生成评分项，好于拿参考当比较对象：参考当比较对象打李克特量表 31.7%，无参考生成评分项 32.0%，用参考生成评分项 35.9%；三者相差不超过 4.2 个百分点，指标与样本量口径待补，口径确认前不据此下结论 |

<a class="anchor" id="verifier-experiments"></a>

#### 3.2.2 Experiments

实测结论：程序检查只有多种组合使用、只查题目明确要求的属性，才能既抓到错误、又不误判正确作品；模型评审会漏判题目要求的属性、判定不稳定，价值在于发现程序检查遗漏的问题。Web 侧样本最少，部分结论借用 three.js、图表与 Blender 的数据。

| 规则 | 发现 | 关键数据 |
|---|---|---|
| 1 读运行时状态 | 1. 像素差与错误大小不对应 | 〔three.js〕鼻子挪到后脑勺，截图相似度仍 0.999；〔图表〕改一个数据点像素差仅 0.75%，换配色却差 30.51% |
| 2 只查题目要求的属性 | 2. 全查会把对的判错 | 〔Blender〕所有属性都比时，写法不同但正确的作品判对 0/11；只查题目要求的属性时，11 个错误全部抓到，正确作品判对 10/11 |
| | 3. 判别力来自修正实现，而非调阈值 | 〔Web〕唯一误判源于 verifier 绑定类名，改成按结构定位后判对 22/22，阈值未动；「类名序列一致」这类确定性信号抓错 0/11 |
| 3 多种检查组合使用 | 4. 单一检查必有漏网 | 任一单项检查最多抓到 11 个错误中的 4 个；组合后 22 个样本全部判对（Web），图表 16/16 |
| 5 模型评审只做两两比较 | 5. 模型评审会漏判题目要求的属性 | 〔Blender〕11 个真错误只抓到 3–6 个 |
| | 6. 模型评审判定不稳定 | 〔three.js〕同一模型判两次，结论改变的比例 0–20.8% |
| | 7. 多数投票无法补救 | 〔three.js〕八票多数投票判对 44/48（单视角）、46/48（多视角）；桌腿缩至 70%，8 票全判通过，程序检查抓到 |
| | 8. VLM 优于像素比对，但依赖参考图 | 〔three.js〕单个模型判对 74–92 次（满分 96），像素比对 12/29；去掉参考图，判对率单张 94% → 68%、多角度 97% → 76%，主要掉在抓错 |
| | 9. 多角度拼图未见收益 | 〔three.js〕最强两个模型 84/95 → 92/96、88/96 → 92/96，逐模型均不显著 |
| 6 评审与生成分离 | 10. VLM 的价值在于发现遗漏的检查项 | 〔three.js〕雪人头顶未封口：多角度 8 次判定 7 次判挂、单张全放过；程序检查全漏，据此新增「网格破洞边数」 |

### 3.3 Aesthetics

**审美评估的核心是一份带示例的专家 rubric：规则从设计经典里沉淀，每条配一对同题的好坏网页，VLM 照着示例，只在通过功能检查的作品之间两两比较。**

#### 3.3.1 Aesthetic Evaluation

**1. Why Expert Rubrics**

| Insight | Source | Used |
|---|---|---|
| 审美有一层多数人一致的部分，集中在可读、可辨、有秩序；分歧集中在配色 | [Tuch et al.](https://research.google.com/pubs/archive/38315.pdf) · 2012：低视觉复杂度、高原型性的网页最受欢迎 | [Anthropic harness][hd]「aesthetics can't be fully reduced to a score—and individual tastes will always vary」 |
| | [Chen et al.](https://ycc.vision/files/papers/Chen_etal_2022_CB_crossmodelTasteTypicality.pdf) · 2022：200 人评 88 张场景图，个人口味与群体均值相关 0.664，无人负相关 | |
| | [VisAWI](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) · 2010：网页审美量表，7 项研究、2,000 多人，四维为简洁、多样、色彩、工艺 | |
| | [TASTE](https://arxiv.org/abs/2605.20731) · 2026-05：各维度里配色和谐的人与人一致最低（τ = 0.103） | |
| 设计经典早把这层共识写成规则；书里的数字只是惯例，说不清的部分靠示例补 | [Williams](https://archive.org/details/nondesignersdesi00will) · 1994：对比、重复、对齐、亲密性四原则 | [Anthropic harness][hd]「grading criteria that encode design principles and preferences」 |
| | [Refactoring UI](https://www.refactoringui.com/book) · 2018：层级、间距、文字、配色各一章，配改前改后对比图 | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「set a clear type scale following the default guidance of The Elements of Typographic Style」 |
| 只给文字 rubric，VLM 判断不稳；配上样例才稳 | [Choi et al.](https://doi.org/10.35542/osf.io/cbhgz_v1) · 2025-04 · GPT-4o，作文评分：只给 rubric QWK 0.40，每档加一篇样例 0.69–0.72，人与人 0.79 | [OpenAI GPT-5.4][g54]「Reference screenshots or mood boards help the model infer layout rhythm, typography scale, spacing systems」 |
| | [ARR](https://arxiv.org/abs/2605.08354) · 2026-05 · GPT-5、Gemini 3.1 Pro：加正反例对，换序准确率差约 30 → 9 点 | |
| 人类评审也靠「标准 + 样例」对齐 | [Awwwards](https://www.awwwards.com/about-evaluation/)：设计 40%、可用性 30%、创意 20%、内容 10%；每件至少 18 名评委，去掉离均值最远的 3 个分 | |
| | [AP Studio Art](https://cresst.org/wp-content/uploads/TECH402.pdf) · 1995：先有样例作品集，后有文字 rubric，用样例锚定 0–4 每一档 | |
| | [Jonsson & Svingby](https://eric.ed.gov/?id=EJ796733) · 2007，75 项研究综述：rubric 提升评分可靠性，尤其配有样例时 | |

**2. The Rubric**

出处只用两本书，各是一个圈子里影响最大的视觉设计书：Williams 定原则，表中写章名；Refactoring UI 管网页落地，表中写页码。

<iframe src="../assets/figures/book-gallery.html" style="width:100%;height:280px;border:0" title="Rubric 出处书"></iframe>

| ID | Rule | Detail | Source | Used | Example Pairs |
|---|---|---|---|---|---|
| A1 | 视觉层级 | 1. Not all elements are equal，元素并不平等。<br>2. A common mistake when styling UI text is relying too much on font size to control your hierarchy，常见错误是过度依赖字号来控制层级。<br>3. Most pages only have one true primary action，多数页面只有一个真正的主操作。 | [Refactoring UI](https://www.refactoringui.com/book) p30、p32；[作者节选](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886) | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「Let one element be the memorable thing」<br>[OpenAI GPT-5.4][g54]「one H1 headline … one primary CTA above the fold」 | <iframe src="../assets/figures/aesthetic-pairs/hierarchy-thumb.html" style="width:160px;height:52px;border:0" title="A1 示例对"></iframe> |
| A2 | 对齐 | 1. Nothing should be placed on the page arbitrarily. Every item should have a visual connection with something else on the page，页面上任何东西都不应随意摆放，每一项都要和页面上的另一项有视觉上的连接。 | [Williams](https://archive.org/details/nondesignersdesi00will)「Alignment」 | [OpenAI GPT-5.4][g54]「Use whitespace, alignment, scale, cropping, and contrast before adding chrome」 | <iframe src="../assets/figures/aesthetic-pairs/alignment-thumb.html" style="width:160px;height:52px;border:0" title="A2 示例对"></iframe> |
| A3 | 亲密性 | 1. Group related items together，把相关的东西放在一起。<br>2. Avoid ambiguous spacing，避免含糊的间距。 | [Williams](https://archive.org/details/nondesignersdesi00will)「Proximity」；[Refactoring UI](https://www.refactoringui.com/book) p83 | — | <iframe src="../assets/figures/aesthetic-pairs/proximity-thumb.html" style="width:160px;height:52px;border:0" title="A3 示例对"></iframe> |
| A4 | 行长与行距 | 1. Keep your line length in check，控制行长。<br>2. Line-height is proportional，行高与字号成比例。<br>3. Anything from 45 to 75 characters is widely regarded as a satisfactory length of line，每行 45 到 75 个字符被普遍认为是合适的行长。 | [Refactoring UI](https://www.refactoringui.com/book) p99、p105；[Bringhurst 2.1.2](http://webtypography.net/2.1.2)（数字） | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「Default to line lengths of less than 80 characters」 | <iframe src="../assets/figures/aesthetic-pairs/measure-thumb.html" style="width:160px;height:52px;border:0" title="A4 示例对"></iframe> |
| A5 | 字号尺度与字体数 | 1. Limit your choices，限制选择。<br>2. Establish a type scale，建立一套字号尺度。 | [Refactoring UI](https://www.refactoringui.com/book) p24、p88 | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「use one family or two」「set a clear type scale」<br>[OpenAI GPT-5.4][g54]「two typefaces maximum」 | <iframe src="../assets/figures/aesthetic-pairs/typescale-thumb.html" style="width:160px;height:52px;border:0" title="A5 示例对"></iframe> |
| A6 | 配色克制 | 1. Most sites need one, maybe two colors that are used for primary actions，多数网站只需要一种、最多两种用于主操作的颜色。<br>2. almost everything in an interface is grey，界面里几乎所有东西都是灰色。 | [Refactoring UI](https://www.refactoringui.com/book) p123（[官方节选](https://www.refactoringui.com/previews/building-your-color-palette)） | [OpenAI GPT-5.4][g54]「one accent color」<br>[Anthropic harness][hd]「color harmony」 | <iframe src="../assets/figures/aesthetic-pairs/color-thumb.html" style="width:160px;height:52px;border:0" title="A6 示例对"></iframe> |
| A7 | 对比度 | 1. Don't use grey text on colored backgrounds，不要在彩色背景上用灰字。<br>2. a contrast ratio of at least 4.5:1，对比度至少 4.5:1。 | [Refactoring UI](https://www.refactoringui.com/book) p36；[WCAG 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)（数字） | [Anthropic harness][hd]「contrast ratios」<br>[OpenAI GPT-5.4][g54]「All text over imagery must maintain strong contrast」 | <iframe src="../assets/figures/aesthetic-pairs/contrast-thumb.html" style="width:160px;height:52px;border:0" title="A7 示例对"></iframe> |
| A8 | 一致性 | 1. Repeat some aspect of the design throughout the entire piece，在整件作品里重复设计的某些方面。<br>2. Establish a spacing and sizing system，建立一套间距与尺寸体系。 | [Williams](https://archive.org/details/nondesignersdesi00will)「Repetition」；[Refactoring UI](https://www.refactoringui.com/book) p60 | [Anthropic harness][hd]「spacing consistency」<br>[OpenAI GPT-5.4][g54]「consistent, scalable UI patterns」 | <iframe src="../assets/figures/aesthetic-pairs/consistency-thumb.html" style="width:160px;height:52px;border:0" title="A8 示例对"></iframe> |
| A9 | 信噪比 | 1. Use fewer borders: using too many of them can make your design feel busy and cluttered，少用边框，用得太多会让设计显得忙乱。<br>2. De-emphasize to emphasize，弱化其余，才能突出重点。 | [Refactoring UI](https://www.refactoringui.com/book) p206、p39 | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「Visual structure is information」<br>[OpenAI GPT-5.4][g54]「If removing a border, shadow, background, or radius does not hurt interaction or understanding, it should not be a card」 | <iframe src="../assets/figures/aesthetic-pairs/noise-thumb.html" style="width:160px;height:52px;border:0" title="A9 示例对"></iframe> |
| A10 | 风格辨识度（只破平） | 1. Choose a personality，选定一种个性。 | [Refactoring UI](https://www.refactoringui.com/book) p17 | [Anthropic harness][hd]「telltale signs of AI generation like purple gradients over white cards—fail here」<br>[OpenAI GPT-5.4][g54]「Brand test」 | <iframe src="../assets/figures/aesthetic-pairs/identity-thumb.html" style="width:160px;height:52px;border:0" title="A10 示例对"></iframe> |

**3. Judging Protocol**

把 rubric 和示例交给 VLM 之后怎么问、怎么记分；Source 写明发表时间和测试的模型，标「早期」的是 2024 年 GPT-4V 一代模型上的结论，还没在新一代模型上复核。

| Protocol | Detail | Source |
|---|---|---|
| 图片标成「图 A」「图 B」 | 多图输入逐张标注「The first image / The second image」，两图比较准确率 76.37% → 80.18% | [Co-Instruct](https://arxiv.org/abs/2402.16641) · 2024-02 · 自训模型 · 早期 |
| A/B 换位置各判一次，两次一致才记胜负 | 位置偏差：o1 在胜者排第二时判对 97.78%，排第一时只有 16.56% | [WiserUI-Bench](https://arxiv.org/abs/2505.05026) · 2025-05 · o1 |
| | 只给 rubric 时偏差仍在：同一对图换个顺序，准确率差约 28–32 点 | [ARR](https://arxiv.org/abs/2605.08354) 表 5 不加示例 · 2026-05 · GPT-5、Gemini 3.1 Pro |
| 每条规则附一对正反示例 | rubric 之外再给正反例对：换序准确率差降到约 9 点，平均准确率高 12.5–14.8 点 | [ARR](https://arxiv.org/abs/2605.08354) 表 5 加示例 · 2026-05 · GPT-5、Gemini 3.1 Pro |
| | 示例不改口味：只给 rubric 时 GPT-5 已到 57.70%，设计师之间也只有 62.4%；再加 8 对示例只变化 −0.1 到 +2.9 点 | [DesignPref](https://arxiv.org/abs/2511.20513) · 2025-11 · GPT-5、Gemini-2.5-Pro |
| | 只给文字原则：两两比较 51.58%，接近随机（已被上一行的新结果取代） | [UIClip](https://arxiv.org/abs/2404.12500) · 2024-04 · GPT-4V · 早期 |
| 示例挑 3–4 对，与待比较页面相似 | 同样 8 个示例：随机挑 0.31，按视觉相似 0.44，按视觉加任务相似 0.58 | [UICrit](https://arxiv.org/abs/2407.08850) · 2024-07 · Gemini Pro Vision · 早期 |
| 强制二选一，不给平局 | 在人能分出高下的对子上：允许平局 54.9%，强制二选一 83.9% | [GenArena](https://arxiv.org/abs/2602.06013) · 2026-02 · Qwen3-VL，图像生成评测 |
| 先写一句证据，不写长推理 | 三步思维链让打分与人的相关从 0.557 掉到 0.299 | [MLLM-as-a-Judge](https://arxiv.org/abs/2402.04788) · 2024-02 · GPT-4V · 早期 |
| 不用：经典计算美学指标 | 对称、平衡、密度都能单向刷高，最优解是空白单列页；72 人实验里指标最高的布局最不受欢迎 | [Salimun](https://theses.gla.ac.uk/4256) · 2013 · 人类实验 |
| | 14 项指标放到真实网页上，只有 1 项和好不好看对得上 | [Purchase et al.](https://eprints.gla.ac.uk/54578) · 2011 · 人类实验 |
| 不用：让 VLM 单独给一页挑错 | 设计越改越好，模型反馈的准确率从 52% 掉到 39% | [Duan et al.](https://arxiv.org/abs/2403.13139) · 2024-03 · GPT-4 · 早期 |

合起来喂给 VLM 的样子：

```text
[规则] A6 配色克制：中性色撑起全页，只用一种强调色，且只落在主操作和关键信息上
[问题] 哪一页更符合这条规则？
[示例] 图 1（胜）中性色撑起全页，墨绿只在主按钮和一个关键数字上
       图 2（负）每块一种饱和色，五根分类条五种颜色
[待比较] 图 A <截图>  图 B <截图>
[输出] {"A6": {"evidence": "一句话，指出位置", "winner": "A 或 B"}}
```

#### 3.3.2 Insight：Aesthetics Band

**美学分只能设上下限或一票否决，不能分越高越好。**

| Insight | Source | Used |
|---|---|---|
| 审美有主观性：职业设计师两两只有约六成一致，这就是任何审美判官的上限 | [DesignPref](https://arxiv.org/abs/2511.20513) · 2025-11：20 位职业设计师判 600 对，两两一致 62.4%（κ 0.248）；模型统一训 57.45%，按个人训 60.16% | [Anthropic harness][hd]「individual tastes will always vary」 |
| | 同上：表单页一致 72%，登录、播放器页 54–57%；收敛在整洁、可读、主操作，分歧在密度、调性、装饰 | |
| 分越高越好的美学分会被钻空子，只能设上下限或一票否决 | [RULER](https://arxiv.org/abs/2609.25270) · 2026-09，SVG 生成：美学分 4.424 → 6.210，按检查项算的分 0.395 → 0.262，输出长 21 倍，堆满描边与重复装饰 | [Anthropic harness][hd]「a competence check rather than a creativity check … failing means broken fundamentals」 |
| | 同上：换成更严的评分表后，钻空子换花样，把题目里的词画成风格化标签 | |
| 「AI 味」只能在一批作品上看，不能看单个 | 本项目实测，两批各 11 / 12 页：一批 100% 用 Inter，字体集中度 0.50；另一批一次没用，集中度 1.00，反而更单调 | [Anthropic skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)「AI-generated design right now clusters around some traits」 |
| | [Wenger & Kenett](https://arxiv.org/abs/2501.19361) · 2025-01，文字创意：模型间差异度 0.459，人与人 0.738 | [OpenAI GPT-5.4][g54]「models often fall back to high-frequency patterns from the training data」 |
| 评测上，多出题比多找评分人划算 | 本项目按 [AUV-Bench](https://arxiv.org/abs/2609.34854) 估算：评分人 3 → 16，人力 5.3 倍，题量只省 30% | [Anthropic eval](https://claude.dev/blog/automating-eval-design-and-hillclimbing/)「the eval's noise … is smaller than the smallest improvement you'd act on」 |
| | 本项目按二项分布估算：30 题 × 每题 8 次，最小可分辨差距约 15.4 个百分点；分辨 5 个点要两千多次 | |

### 3.4 Frontier Lab

每条 Insight 落在哪一环见 Taxonomy 列：<span class="tx tx-data">数据</span> <span class="tx tx-verifier">Verifier</span> <span class="tx tx-harness">Harness</span> <span class="tx tx-env">环境</span> <span class="tx tx-algo">算法</span>

| Lab | Blog | Taxonomy | Insight |
|---|---|---|---|
| <img height="14" src="../assets/logos/anthropic.png" align="center" alt="Anthropic" title="Anthropic"> Anthropic | [Harness design for long-running apps][hd] | <span class="tx tx-verifier" data-b="0">Verifier</span> | 前端实验四个维度加权、迭代 5–15 轮；全栈实验四个维度各设硬阈值，任一项低于及格线即整体不及格；模型默认就能及格的维度降权 |
|  | [Harness design for long-running apps][hd] | <span class="tx tx-harness" data-b="0">Harness</span> | · 生成与评审分离：生成器自评倾向自我肯定，独立评审更容易调严<br>· 评审用 Playwright 实操运行中的页面再打分，并用 few-shot 校准<br>· 质检只占整套运行成本的 8.3%，每轮都找出真问题 |
|  | [Improving frontend design through Skills][fd] | <span class="tx tx-data" data-b="1">数据</span> | 前端产出千篇一律，归因于分布收敛：模型倾向于采样训练分布里最常见的样式 |
|  | [Improving frontend design through Skills][fd] | <span class="tx tx-harness" data-b="1">Harness</span> | 用 frontend-design skill 在提示层点名避开默认样式 |
|  | [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/) | <span class="tx tx-verifier" data-b="2">Verifier</span> | · 每个检查项都须在题目里说出来；写成程序检查，不写五分制<br>· 好题 = 两个领域专家会给出同样判断的题；分数一直不涨的题，是题或判据坏了<br>· 评测的波动必须小于值得采取行动的最小提升；同一作品判两遍看结论变不变，机器故障与模型本身的波动分开统计 |
|  | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | <span class="tx tx-harness" data-b="3">Harness</span> | 规则和状态存成结构化文件（如 JSON），模型不太会篡改 |
|  | [Claude Opus 5 System Card](https://www.anthropic.com/claude-opus-5-system-card) | <span class="tx tx-data" data-b="4">数据</span> | 自我检查会过头：24 小时蛋白设计实验目标 30 个，Opus 5 一组只交 17 个未排序的，另一组什么都没交，最后 8 小时卡在自我验证循环里（2.2.6 节）；裁剪训练过程时，该剪的是没有新信息的反复检查 |
|  | [Claude Opus 5 System Card](https://www.anthropic.com/claude-opus-5-system-card) | <span class="tx tx-env" data-b="4">环境</span> | 最终阶段约 150 万条训练过程记录、数千个训练环境；约 400 条由多个 Claude 模型通读，人只核对关键论断（6.3 节） |
|  | [Claude Opus 5.5 System Card](https://www.anthropic.com/claude-opus-5-5-system-card) | <span class="tx tx-verifier" data-b="5">Verifier</span> | · 模型会猜判据：按猜的规则改答案 2/695，主动找线索 1/695，猜中标准答案并成功约 0.3%<br>· 被安全拦截挡下的尝试单独报出，并算作失败（8.14.5 节） |
|  | [Claude Opus 5.5 System Card](https://www.anthropic.com/claude-opus-5-5-system-card) | <span class="tx tx-env" data-b="5">环境</span> | · 坏题的代价：缺文件、做不成的题，尝试钻空子的比例高 3–6 倍，钻空子成功率高 1.5–3 个百分点，约 80% 是「明知没做完还交」；官方做法是修环境，不修模型（6.2.2 节）<br>· 跨模型比较钻空子比例时，只用三个模型都跑过的环境（6.2 节） |
|  | [Claude Fable 5 / Mythos 5 System Card](https://anthropic.com/claude-fable-5-mythos-5-system-card) | <span class="tx tx-verifier" data-b="6">Verifier</span> | 模型会声称检查过、实际没有：内部使用审计的 886 个会话里 16 个「说做完了或验证过了，其实没有」（2.3.3.2 节）；只靠模型自评造训练信号不可靠 |
|  | [Claude Fable 5 / Mythos 5 System Card](https://anthropic.com/claude-fable-5-mythos-5-system-card) | <span class="tx tx-env" data-b="6">环境</span> | 按钻空子的风险把训练环境分成高低两组（6.4.2 节） |
| <img height="14" src="../assets/logos/openai.png" align="center" alt="OpenAI" title="OpenAI"> OpenAI | [Designing delightful frontends with GPT-5.4][g54] | <span class="tx tx-verifier" data-b="7">Verifier</span> | 能数的硬约束写具体数目：一个主标题、不超过六个区块、最多两种字体、一个强调色、首屏一个主按钮 |
|  | [Designing delightful frontends with GPT-5.4][g54] | <span class="tx tx-algo" data-b="7">算法</span> | 原话「专门训练过 UI 与图像使用」「为 computer use 训练，可配合 Playwright 反复检查自己的产物」（另见 [GPT-5.6 发布页](https://openai.com/index/gpt-5-6/)） |
|  | [Building games with Astra](https://developers.openai.com/blog/how-to-build-games-with-astra) | <span class="tx tx-verifier" data-b="8">Verifier</span> | · 特效开关的像素差分、渲染计数器、90 个帧间隔采样<br>· 故意删掉一部分（删图片、藏导航、去边框阴影、砍三成文案、开关特效），看判据会不会跟着变 |
|  | [playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) | <span class="tx tx-verifier" data-b="9">Verifier</span> | · 题目、实现、意图里的每个要求至少对应一个检查项<br>· 视觉上重要但主观的要求转成看得见的检查项，不能略过<br>· 视觉检查与功能检查分开，功能过了不等于视觉过了 |
| <img height="14" src="../assets/logos/google-deepmind.png" align="center" alt="Google DeepMind" title="Google DeepMind"> Google DeepMind | [Gemini 2.5: Pushing the Frontier](https://arxiv.org/abs/2507.06261) | <span class="tx tx-env" data-b="10">环境</span> | 训练里加入端到端的 web 与移动应用任务 |
|  | [Gemini 2.5: Pushing the Frontier](https://arxiv.org/abs/2507.06261) | <span class="tx tx-algo" data-b="10">算法</span> | 强化学习同时用可验证奖励与生成式奖励 |
| <img height="14" src="../assets/logos/moonshot.png" align="center" alt="Moonshot AI" title="Moonshot AI"> Moonshot AI | [Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276)<br>[Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) | <span class="tx tx-data" data-b="11">数据</span> | 代码与渲染结果配对预训练；K3 扩到 3D、游戏、CAD |
|  | [Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276)<br>[Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) | <span class="tx tx-verifier" data-b="11">Verifier</span> | 强化学习先过确定性检查，构建失败或伪造实现直接记 0 |
| <img height="14" src="../assets/logos/qwen.png" align="center" alt="Alibaba Qwen" title="Alibaba Qwen"> Alibaba Qwen | [Qwen3-VL Technical Report](https://arxiv.org/abs/2511.21631) | <span class="tx tx-data" data-b="12">数据</span> | 代码与渲染结果配对预训练 |
| <img height="14" src="../assets/logos/minimax.png" align="center" alt="MiniMax" title="MiniMax"> MiniMax | [The MiniMax-M2 Series](https://arxiv.org/abs/2605.26494) | <span class="tx tx-data" data-b="13">数据</span> | 在真实沙箱里跑代码来过滤数据 |
| <span class="org-mark" title="Xiaomi">X</span> Xiaomi | [MiMo-V2-Flash Technical Report][mimo] | <span class="tx tx-data" data-b="14">数据</span> | 在沙箱里跑代码来过滤数据 |
|  | [MiMo-V2-Flash Technical Report][mimo] | <span class="tx tx-verifier" data-b="14">Verifier</span> | 评审看录屏而非截图，同时判视觉、功能与可运行性 |

[hd]: https://www.anthropic.com/engineering/harness-design-long-running-apps
[ui2]: https://arxiv.org/abs/2511.08195
[mimo]: https://arxiv.org/abs/2601.02780
[wcb]: https://arxiv.org/abs/2606.01869
[fd]: https://claude.com/blog/improving-frontend-design-through-skills
[g54]: https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4

