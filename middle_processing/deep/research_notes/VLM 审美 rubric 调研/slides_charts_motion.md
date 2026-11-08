# VLM 审美 rubric 调研 · Slides / Charts / Explainer Motion

> 口径说明
> - 标记 `[新]` = 项目已有笔记 `middle_processing/notes/ppt_manim.md` 里没有；`[已有·补数]` = 该条目已有，但这里补了人评一致性等新数字。
> - 标记 `[未核验]` = 本次没抓到原文/一手页面，来自二手摘要或通识，写报告时需降级表述或补核。
> - rubric 可查性标签：`【P】` 程序可查（源码 / 渲染 DOM / chart spec / 帧几何）；`【V】` 只能 VLM 看图或帧；`【P+V】` 程序做主判、VLM 补语义。
> - 一手来源抓取日期：2026-11-02。

## Q1 · Slides：经典理论说了什么具体规则？学术 slide 评测用什么维度、与人一致到什么程度？

### Takeaway
- 经典理论能落成可查规则的只有几条硬指标：3 秒 Glance Test、≥30pt 字号（Kawasaki）、对齐/亲密/重复/对比（CRAP），其余靠 VLM。
- 学术评测里 VLM 判 **Design 维度最可靠**：PPTEval Design 的 Pearson 0.90；判 **Coherence 最弱**：Pearson 0.55。人与人之间本来就只有中等一致：PPTEval Fleiss κ 0.59，SlideAudit 只有 0.26。

### Cited Findings

**A. 经典理论（设计原则）**
- `[新]` Duarte **Glance Test**：观众应在 **3 秒或更短**内看懂一页的要点。页面列出的检查目标有：
  - 每页聚焦"single, precise point"
  - 用 contrast 和 whitespace 强调最关键的信息
  - 检查 unity 与 flow
  - 每个元素都要服务理解，视觉要能减噪
  - 该页没公开打分细则（下载件内容未抓到）
  — [Duarte · The Glance Test](https://www.duarte.com/resources/guides-tools/the-glance-test/)
- `[新]` Glance Test 由 Duarte 团队与 KLA Tencor 的 Glenn Hughes 共同开发，按 **signal-to-noise ratio** 给每页打分，标准包括 message singularity、audience relevance、visual clarity（来自搜索摘要，原页未逐字核对 `[未核验]`）— [Duarte · Slide Glance Test](https://www.duarte.com/resources/slide-glance-test/)；简化版做法（给人看 3 秒，看懂没）— [Storytelling with Data · slide:ology workshop](https://www.storytellingwithdata.com/blog/2011/02/slideology-workshop)
- `[新]` Guy Kawasaki **10/20/30 rule**：10 页、≤20 分钟、**字号不小于 30pt**。另有一句玩笑："最小字号 = 最年长听众年龄 / 2"。原帖 2005-12-30 发在 guykawasaki.com，本次没打开原帖，只见二手转述 — [AhaSlides 转述](https://ahaslides.com/blog/10-20-30-rule-presentations)；[SlideGenius 引原帖](https://www.slidegenius.com/?p=10342)
- `[新]` **SlideAudit**（UIST 2025，UW）的 flaw taxonomy 由 17 位专家的形成性研究得出：
  - 结构：**5 个维度 · 27 类 flaw**。5 个维度是 Composition & Layout / Typography / Color / Imagery / Animation & Interaction
  - LLM 评测用其中 **19 类**；**9 类**可标 bounding box
  - 正文点名的类别：Cluttered Layout、Misaligned Elements、Inconsistent or Distracting Text Styling、Insufficient Contrast、Illegible Typeface Usage、Lack of Visual Hierarchy、Excessive Text Density、Occluded Content、Inappropriate Font Sizing、Inconsistent Visual Style、Unbalanced Space or Margin Distribution、Content Overflow、Poor Color Usage、Mismatched Color Combinations
  - 与 Gestalt 的对应：Cluttered↔Proximity、Misaligned↔Continuity、Inconsistent text styling↔Similarity、Insufficient Contrast↔Figure-Ground
  - 对比度指标采用 **WCAG 2.1**
  - 正文**没有**引用 Duarte / Reynolds / Williams CRAP
  — [SlideAudit arXiv 2508.03630](https://arxiv.org/html/2508.03630v1)
- `[新]` SlideAudit 数据分布：
  - 2,400 张 slide，28.7% 无 flaw，平均每张 1.37 个 flaw
  - 最常见：**Occluded Content 15.5%**、**Inappropriate Font Sizing 15.2%**；最少：Inconsistent Visual Style 0.75%
  — [SlideAudit 摘要/搜索结果](https://arxiv.org/pdf/2508.03630)；数据在 [GitHub Ruiqi-Chen-0216/SlideAudit](https://github.yxlr123.workers.dev/Ruiqi-Chen-0216/SlideAudit)（镜像域名，正式仓库地址需核对）

**B. 学术 slide 生成评测**

| Benchmark | 维度 / 判据 | 判官 | 量程 | 与人一致性 | 来源 |
|---|---|---|---|---|---|
| PPTEval（PPTAgent，EMNLP 2025）`[已有·补数]` | Content（信息量、文字质量、图是否支撑文字）<br>Design（配色对比与和谐、几何视觉元素、整体设计含**避免重叠**）<br>Coherence（逻辑结构、上下文信息） | GPT-4o | 1–5，Content/Design 逐页打分取均值，Coherence 整套打分 | LLM–人 Pearson / Spearman：Content 0.70/0.73、**Design 0.90/0.88**、Coherence 0.55/0.57、Avg 0.71/0.74（p<0.05）<br>人–人 Fleiss κ：均值 0.59（Content 0.61 / Design 0.61 / Coherence 0.54） | [arXiv 2501.03936](https://arxiv.org/html/2501.03936) |
| SlidesBench（AutoPresent，CVPR 2025）`[已有·补数]` | reference-free 四项：<br>Text（标题清楚、正文简洁、字号/字体/颜色一致可读）<br>Image（高质量、比例合理）<br>Layout（**对齐、无重叠、边距充足、不出页**）<br>Color（文字与背景**高对比**、无刺眼颜色）<br>reference-based：element match、content（MiniLM / CLIP）、color（CIEDE2000）、position | GPT-4o 看 slide 图 | 0–5，报告时 ×20 换成 0–100 | 两名标注者与模型判官的 **ICC 73.8%–85.3%**（在 GT slide 上测） | [arXiv 2501.00912](https://arxiv.org/html/2501.00912) |
| SlideAudit（UIST 2025）`[新]` | 19 类 flaw 检测 | GPT-4o / Claude 3.7 / Gemini 2.0 Flash | macro F1 | baseline → taxonomy 提示：GPT-4o 0.476→**0.655**、Claude 3.7 0.492→0.612、Gemini 2.0 Flash 0.515→0.604<br>人–人 Fleiss **κ=0.26**（fair；UICrit 为 0.29）<br>人–LLM 比较器 Cohen κ=0.68（36 条） | [arXiv 2508.03630](https://arxiv.org/html/2508.03630v1) |
| Paper2Poster（NeurIPS 2025 D&B）`[已有·补数]` | VLM-as-judge 六项，5 分制，输出 JSON reason+score：<br>Aesthetic = element quality / layout balance / engagement<br>Information = clarity / content completeness / logical flow<br>另有 CLIP 视觉相似度、Figure Relevance、PPL、PaperQuiz（o3 出 100 题，长度惩罚，0–200） | VLM（具体型号见原文） | 1–5 | 未给相关系数；只说 PaperQuiz 人与 VLM "good consistency"。5 次重跑每项 std<0.024 | [arXiv 2505.21497](https://arxiv.org/html/2505.21497) |

- `[已有·补数]` PPTEval 的评分 prompt 只以图片形式出现（Figures 18–23），正文没有给出 1–5 每档的描述 — [arXiv 2501.03936](https://arxiv.org/html/2501.03936)
- `[新]` PPTEval Table 5 的 Avg 和三维均值对不上：Pearson 三维简单均值约 0.72，表里写 0.71 — 同上
- `[新]` PPTEval 用来校准的人评规模：4 名研究生评 250 套 PPT（50 真实 + 100 baseline + 100 PPTAgent），先单评再讨论 — 同上
- `[新]` SlidesBench 的 Overall 分把**不能执行的程序记 0**，reference-based / reference-free 分只在可执行 slide 上计算 — [arXiv 2501.00912](https://arxiv.org/html/2501.00912)
- `[新]` Paper2Poster 的 Commenter（VLM）看**放大的 panel 裁图**，对照两个 in-context 参考图（一张 overflow、一张 ideal），输出 "overflow" / "too blank" / "good to go"。布局用 binary-tree，因为让 LLM 直接预测坐标不稳定 — [arXiv 2505.21497](https://arxiv.org/html/2505.21497)

### Inferences
- **VLM 擅长什么、不擅长什么**
  - 擅长：单页整体观感（PPTEval Design r=0.90、SlidesBench ICC 最高 85.3%）
  - 不擅长：跨页叙事（Coherence r=0.55）、细粒度 flaw 定位（SlideAudit F1 ≤0.655）
  - 结论：几何类（溢出 / 遮挡 / 对齐 / 边距）交给程序；"一页一意""层级是否清楚"交给 VLM
- **人评上限本身就低**：SlideAudit 人–人 κ=0.26。flaw 级别的 rubric 要求 yes/no 判断，要配 bounding box 或明确阈值，否则连人都对不齐
- **taxonomy 提示比自由打分好**：SlideAudit 上 GPT-4o 从 0.476 涨到 0.655。所以给 VLM 的应该是逐条 checklist，不是一个总分

#### 候选 rubric · Slides（14 条）

| # | 检查项（yes/no 或可两两比较） | 来源 | 可查性 |
|---|---|---|---|
| S1 | **3 秒要点**：只看 3 秒（或单张低分辨率图）能复述出唯一主旨，并与标题/意图一致 | Duarte Glance Test | 【V】 |
| S2 | **一页一意**：标题是一句断言，正文全部服务于它，没有第二个独立论点 | Duarte Glance Test "single, precise point" | 【V】 |
| S3 | **文本密度**：正文词数 ≤ 阈值（建议中文 ≤80 字、英文 ≤40 词）且 bullet ≤6 条 | SlideAudit Excessive Text Density；Duarte "75 词即文档"`[未核验]` | 【P】数 pptx / DOM 文本 |
| S4 | **最小字号**：正文 ≥18pt（严格档 ≥24pt；Kawasaki 档 ≥30pt）、标题 ≥28pt | Kawasaki 10/20/30；SlideAudit Inappropriate Font Sizing（15.2%） | 【P】读 run.font.size / computed CSS |
| S5 | **不溢出、不出页**：所有元素 bbox ⊂ 画布；文本框 scrollHeight ≤ clientHeight | SlidesBench Layout；SlideAudit Content Overflow；Paper2Poster overflow | 【P】 |
| S6 | **无非预期遮挡**：文本–文本、文本–图片的 bbox 交并比 = 0（背景图层除外） | PPTEval Design；SlidesBench "no overlap"；SlideAudit Occluded Content（15.5%） | 【P】几何；"是否有意叠放"交给【V】 |
| S7 | **对齐**：元素左/中/右边缘吸附到 ≤K 条对齐线，偏差 ≤ 画布宽 0.5% | Williams Alignment `[未核验]`；SlideAudit Misaligned；SlidesBench "aligned" | 【P】 |
| S8 | **边距**：四边留白 ≥ 画布宽 5%；左右边距差 ≤ 2% | SlidesBench "sufficient margins"；SlideAudit Unbalanced Margin | 【P】 |
| S9 | **对比度**：文字/背景对比度 ≥4.5:1（大字 ≥3:1）；图上文字取渲染像素算 | SlideAudit 采用 WCAG 2.1；SlidesBench Color "high contrast" | 【P】 |
| S10 | **视觉层级**：标题字号 ≥ 正文 1.5×；全页只有一个最显著元素 | Williams Contrast `[未核验]`；SlideAudit Lack of Visual Hierarchy；Glance Test | 字号比【P】，显著性【V】 |
| S11 | **亲密性**：同组元素间距 < 组间间距 | Williams Proximity `[未核验]`；SlideAudit Cluttered Layout↔Proximity | 【P+V】 |
| S12 | **重复 / 一致**：整套字体族 ≤2；同一角色（标题/正文/注释）跨页样式相同；主色跨页一致 | Williams Repetition `[未核验]`；SlideAudit Inconsistent Visual Style | 【P】 |
| S13 | **配色克制**：每页非中性色 ≤3–4 种；无高饱和大面积背景 | SlidesBench "no highly glaring colors"；SlideAudit Mismatched Color Combinations | 计数【P】，和谐度【V】 |
| S14 | **图片质量与相关**：图片宽高比保持（误差 ≤2%）、源分辨率 ≥ 显示尺寸；图与本页文字相关 | SlidesBench Image；PPTEval Content "images support text"；Paper2Poster element quality | 比例/分辨率【P】，相关性【V】 |
| (deck 级) S15 | **叙事连贯**：只读标题串就能成一条论证线；有开头和结论页 | PPTEval Coherence（与人一致性最弱：r=0.55） | 【V】（LLM 读文本也可） |

### Gaps
- **Duarte *slide:ology* / Reynolds *Presentation Zen* / Williams *The Non-Designer's Design Book* 的章节级原文，本次没抓到**，以下只是通识，引用前需核对原书：
  - *slide:ology*：主要章节有 Creating Diagrams / Displaying Data / Arranging Elements（contrast、flow、hierarchy、unity、proximity、whitespace）/ Using Visual Elements；"slides are glance media"；"超过 75 词就成了文档（slideument）"
  - *Presentation Zen*：restraint / simplicity / naturalness；借 Tufte 的 signal-to-noise ratio；picture superiority effect；empty space；书里也讲 CRAP
  - Williams：Contrast / Repetition / Alignment / Proximity；Alignment 原则大意是"页面上不应随意放置任何元素，每个元素都应与页上另一元素有视觉关联"
- **DOC2PPT**（Fu et al., AAAI 2022）的指标和人评数据本次没抓到。印象中有 ROUGE 类与 layout 类指标 `[未核验]`
- PPTEval 的逐档 prompt 只在图里，文本里没有；Paper2Poster 六项判据除 element quality 外的定义被截断；SlideAudit 27 类完整定义只在 Fig. 2 里
- 没有找到"字号下限"的学术实证阈值。≥18/24/30pt 都来自从业者规则，不是实验结论

## Q2 · Charts：经典可视化理论的具体规则是什么？哪些能从 spec 程序化检查？有哪些 chart benchmark 用 VLM/LLM 判官、与人一致到什么程度？

### Takeaway
- 规则大多能程序化：编码排序（Cleveland–McGill / Munzner）、表达性（Mackinlay / Munzner）、零基线、lie factor、色数与色盲安全、文字重叠、刻度格式，都能从 spec 或 SVG 上查。
- VLM 判官的可靠性差别很大：
  - 跟参考图比相似度：MatPlotBench r=0.876，ChartMimic r≈0.70–0.77，Plot2Code 只有 r=0.479
  - 无参考审美打分：VisJudge-Bench 上 GPT-5 的相关只有 **0.428**，模型普遍打分虚高
  - VisEval 的做法值得照搬：先用程序把重叠和刻度查出来，再把结果喂给 VLM，SRCC 从 0.507 提到 0.843

### Cited Findings

**A. 经典理论**
- `[新]` Tufte **Lie Factor** = 图中呈现的效应大小 / 数据中的效应大小，理想值约等于 1。示例：图中 8.5 对应数据 1.52，lie factor ≈5.59。"0.95–1.05 之外即失真"这个阈值本次只在一处二手源看到 `[未核验]` — [Tufte 原则二手汇总（搜索结果）](https://www.medien.ifi.lmu.de/lehre/ws1415/iv/uebung/u1/slides_1.pdf)；[SAGE Encyclopedia 条目](https://sk.sagepub.com/ency/edvol/embed/the-sage-encyclopedia-of-research-design-2e/chpt/visual-display-quantitative-information)
- `[新]` **Data-ink ratio**：承载非冗余数据的墨水 / 全部墨水。主张擦掉 non-data ink 和冗余的 data ink。**Chartjunk** 指装饰性、会分散注意力的元素 — [eagereyes · definition of chart junk](https://eagereyes.org/blog/2013/definition-chart-junk)；[IEEE Spectrum · Tufteisms](https://spectrum.ieee.org/tufteisms)
- `[新]` 反对意见：严格最大化 data-ink ratio 会产生"terrible and nonsensical"的结果；data-ink 和 chart lies 都难以量化 — [eagereyes](https://eagereyes.org/blog/2013/definition-chart-junk)；[NN/g · clutter charts](https://www.nngroup.com/articles/clutter-charts/)
- `[新]` **Cleveland & McGill 1984**（JASA，"Graphical Perception: Theory, Experimentation, and Application…"）
  - 10 个 elementary perceptual tasks，按判断准确度排序：position on common scale > position on non-aligned scales > length / direction / angle > area > volume / curvature > shading / color saturation
  - 作者自己提醒：这个排序"does not result in a precise prescription…but rather is a framework"
  — [Cornell INFO3312 graphical perception](https://info3312.infosci.cornell.edu/slides/04-graphical-perception.html)；[PKU 课程 PDF](https://vis.pku.edu.cn/course/visclass_f25/material/Graphical_perception.pdf)
- `[新]` Heer & Bostock 用 Mechanical Turk 复现，排序基本成立。后续研究指出：discrimination 任务、多值比较（如均值）上这个排序不一定适用 — [Risks of Ranking, arXiv 2212.10533](https://arxiv.org/pdf/2212.10533)
- `[新]` Munzner *Visualization Analysis & Design*（2014）Ch.5 Marks and Channels
  - **Expressiveness**：channel 类型要匹配数据类型。有序数据用 magnitude channel（how much），类别数据用 identity channel（what）；不要用暗含顺序的方式编码类别
  - **Effectiveness**：最重要的属性给最显著的 channel
  - spatial position 在两张排序表里都排第一；color luminance / saturation、curvature、volume 排在后面
  — [Munzner UBC 课件 marks.pdf](https://www.cs.ubc.ca/~tmm/courses/436V-20/slides/marks.pdf)；[VAD-marks](https://cs.ubc.ca/~tmm/talks/vad/VAD-marks.pdf)
- `[新]` **Draco**（Moritz et al., InfoVis 2018 / TVCG 2019）
  - 把可视化表示成逻辑事实集合，设计准则写成约束：**hard constraints** 过滤设计空间，**soft constraints** 加权排序
  - soft 权重可以直接从 graphical perception 实验结果里学
  - 用 ASP + Clingo 求解，输出 Vega-Lite
  - 约束内容覆盖 expressiveness criteria、经感知实验验证的偏好、通用最佳实践
  — [Draco 项目页](https://idl.uw.edu/draco)；[论文 PDF](https://par.nsf.gov/servlets/purl/10074159)

**B. Chart 生成 / 质量 benchmark**

| Benchmark | 判据 | 判官 | 与人一致性 | 来源 |
|---|---|---|---|---|
| VisEval（VIS 2024）`[新]` | 三级：<br>Validity（能跑、真的出图）<br>Legality（SVG 解析出 chart type / data / order，与 GT 比）<br>Readability（布局重叠溢出 + scale & ticks + 整体评分） | GPT-4V 做 1–5 readability；**重叠/溢出用浏览器模拟测元素位置**，因为 VLM 不够准 | layout check 准确率 **100%**；scale & ticks **99%**（不给提取出的 tick 值时 92%）<br>readability 与人均分 **SRCC 0.843**；人–人 SRCC **0.782**<br>消融：去掉 scale&ticks 0.732、去掉 layout 0.675、两者都去 0.507 | [arXiv 2407.00981](https://arxiv.org/html/2407.00981) |
| ChartMimic `[新]` | low-level（code tracer 记录 text / layout / type / color，算 F1 取均值）+ high-level（GPT-4o 比 GT 图与生成图，0–100）；跑不通记 0 | GPT-4o | Pearson：high-level **0.7041**、low-level **0.7681**（1,200 图 × 3 人，p<0.0001） | [arXiv 2406.09961](https://arxiv.org/html/2406.09961) |
| MatPlotBench（MatPlotAgent）`[新]` | GPT-4V 对照 GT 图给生成图打 0–100；空白图记 0 | GPT-4V | 25 例子集重复 100 次：Pearson **0.876**（GPT-4 结果）/ 0.836（GPT-3.5 结果） | [arXiv 2402.11453](https://arxiv.org/html/2402.11453) |
| Plot2Code `[新]` | pass rate + text-match ratio + GPT-4V 1–10 整体相似度；pairwise 交换顺序，两次都赢才算赢 | GPT-4V | 920 样本：Kendall τ **0.437**、Pearson **0.479**、Spearman **0.469**（中等）；MSE、SSIM 区分不了高/低相似组（p=0.22/0.21） | [arXiv 2405.07990](https://arxiv.org/html/2405.07990) |
| VisJudge-Bench（ICLR 2026）`[新]` | **Fidelity**（截断基线、坐标轴不当等可见失真）<br>**Expressiveness**（Semantic Readability、Insight Discovery）<br>**Aesthetics**（Design Style、Visual Composition、Color Harmony）<br>5 分制；3,090 样本 / 32 子类（单图 1,041 / 多图 1,024 / dashboard 1,025） | 多个 MLLM | MAE / corr：GPT-5 0.553/**0.428**、GPT-4o 0.610/0.482、Claude-4-Sonnet 0.622/0.465、Gemini-2.5-Pro 0.662/**0.265**、Qwen2.5-VL-72B 0.702/0.440；微调的 VisJudge（Qwen2.5-VL-7B）**0.421/0.687** | [arXiv 2510.22373v3](https://arxiv.org/html/2510.22373v3) |

- `[新]` VisEval readability prompt 明确写了"Do not consider the correctness of the data and order…already verified"，做法是把提取出的 tick 值写进 prompt 来压幻觉。也就是**程序先做确定性检查，VLM 只管剩下的** — [arXiv 2407.00981](https://arxiv.org/html/2407.00981)
- `[新]` VisJudge-Bench 发现的判官偏差：
  - 普遍**分数虚高**：人均分 3.13，Qwen2.5-VL-7B 打 3.89、Claude-3.5-Sonnet 打 3.87，GPT-5 3.36 最接近
  - 分数集中在 4.0 附近，区分度低
  - Gemini-2.5-Pro 偏严（3.02），有时因为一个瑕疵整页扣分
  - 审美子维度最难；从单图到 dashboard，越复杂越差
  - 实例：人评 1.67 的混乱 treemap，Qwen2.5-VL-7B 打了 3.67
  — [arXiv 2510.22373v3](https://arxiv.org/html/2510.22373v3)
- `[新]` 指标冲突：VisJudge 表中 GPT-4o 的相关（0.482）高于 GPT-5（0.428），但 MAE 更差。不同 arXiv 版本的数字略有差异（搜索摘要里 VisJudge 是 0.687、GPT-5 是 0.429 / MAE 0.551）— [v3](https://arxiv.org/html/2510.22373v3)；[v1](https://arxiv.org/html/2510.22373v1)
- `[新]` MatPlotAgent 的 visual feedback agent 看当前图和 query（不看 GT），检查 data selection、plot type、customization（title / labels / colors），然后输出修改代码的步骤 — [arXiv 2402.11453](https://arxiv.org/html/2402.11453)

### Inferences
- **有参考 vs 无参考，是两件不同的事**
  - 有参考（与 GT 比相似）：VLM 判官 r 约 0.7–0.88，可以直接用
  - 无参考（判美丑 / 好坏）：只有 0.27–0.48，必须 checklist 化 + 程序先行，或者微调专门的判官（VisJudge 0.687）
- **重叠 / 出界不要交给 VLM 判**：VisEval 用浏览器测量做到 100%，并且明确说 VLM 不够准；它的消融也说明，把程序结果喂给 VLM，相关从 0.507 提到 0.843
- **从 spec 可查的规则最多**：Vega-Lite / matplotlib 对象树里能直接读到 channel 类型、domain、颜色数、tick 格式。所以 chart rubric 的程序化比例应该是三类里最高的

#### 候选 rubric · Charts（15 条）

| # | 检查项 | 来源 | 可查性 |
|---|---|---|---|
| C1 | **主量化变量用 position / length 编码**，不用 area / angle / 色深；饼图只在 part-to-whole 且 ≤5 扇区时允许 | Cleveland–McGill；Munzner effectiveness | 【P】读 spec 的 encoding / mark |
| C2 | **表达性**：nominal 字段不映射到有序 channel（如顺序色带、size）；有序 / 量化字段不只靠 hue 编码 | Munzner expressiveness；Mackinlay APT `[未核验]`；Draco hard constraints | 【P】 |
| C3 | **bar / area 的数值轴 domain 包含 0** | VisJudge Fidelity "truncated baselines"；Few `[未核验]` | 【P】 |
| C4 | **lie factor ∈ [0.95, 1.05]**：圆 / 图标按面积而不是半径缩放；数值轴非对数时等距 | Tufte Lie Factor（阈值 `[未核验]`） | 【P】有 spec 时可算 |
| C5 | **没有超出数据维度的视觉维度**：2D 数据不用 3D 柱 / 饼、无透视 | Tufte graphical integrity `[未核验]`；VisJudge Fidelity | 【P】检测 3D 投影 / bar3d；【V】兜底 |
| C6 | **无 chartjunk**：无背景图、无装饰阴影/渐变、网格线浅色或省略、不在数据标签已在时还加重网格 | Tufte data-ink / chartjunk | 【P+V】 |
| C7 | **类别色数 ≤ 8**（超过就分组、"其他"合并或 small multiples） | ColorBrewer 定性色板上限 12 `[未核验]`；Ware `[未核验]` | 【P】 |
| C8 | **色板类型与数据匹配，且色盲安全**：有序→sequential；有意义中点→diverging；类别→qualitative；模拟 deuteranopia / protanopia 后相邻类别 ΔE ≥ 阈值 | Brewer / ColorBrewer `[未核验]`；Munzner expressiveness | 【P】 |
| C9 | **文字不重叠、不溢出**：tick labels / legend / annotation / title 的 bbox 两两不交且都在画布内 | VisEval layout check（浏览器测量 100%） | 【P】SVG / DOM / matplotlib get_window_extent |
| C10 | **刻度合理**：除非意图明确否则不倒置坐标；年份不显示小数；tick 数 ≤ ~10；大数有千分位或单位缩写 | VisEval scale & ticks（99%） | 【P】 |
| C11 | **标注完备**：有标题；坐标轴有名称和单位；≥2 个颜色编码的系列时有 legend 或直接标注 | VisEval overall rating；MatPlotAgent visual agent | 【P】 |
| C12 | **数据保真**：绘制的数值、顺序、图表类型与源数据 / 查询一致 | VisEval legality；ChartMimic low-level | 【P】 |
| C13 | **small multiples 共享坐标尺度**（除非明确标注独立尺度） | Tufte small multiples `[未核验]`；VisJudge Fidelity | 【P】 |
| C14 | **关键洞察一眼可见**：主要趋势 / 极值 / 异常点能被识别；需要强调的系列用高亮色，其余降饱和 | VisJudge Insight Discovery；Duarte Displaying Data `[未核验]` | 【V】 |
| C15 | **构图与配色和谐**：留白均衡、图例不挤占数据区、配色协调（建议用两两比较，不用绝对分） | VisJudge Visual Composition / Color Harmony（VLM 最弱的子维度） | 【V】 |

### Gaps
- **Stephen Few *Show Me the Numbers*、Colin Ware *Information Visualization*、Mackinlay APT（1986，ACM TOG）、ColorBrewer 页面，本次都没抓原文**，以下是通识 `[未核验]`：
  - Few：bar 必须从 0 开始；避免 3D；按 7 类量化关系选图（time series / ranking / part-to-whole / deviation / distribution / correlation / nominal comparison）
  - Mackinlay：expressiveness（"编码全部且仅编码数据中的事实"）+ effectiveness，按 quantitative / ordinal / nominal 三类给出感知任务排序
  - Ware：preattentive features；文字亮度对比建议值
  - ColorBrewer：三类方案；colorblind-safe / print / photocopy 过滤；定性 ≤12、顺序 ≤9、发散 ≤11 级
- Tufte VDQI 的章节归属（lie factor 在 Ch.2 Graphical Integrity，data-ink 在 Ch.4，chartjunk 在 Ch.5，small multiples 在 Ch.8）是通识，未核对原书 `[未核验]`
- **ChartCoder、Lux、VizLinter / McNutt "Linting for Visualization"** 没查到具体数字，本次覆盖不到
- VisJudge-Bench 的标注者间一致性在附录里，本次没读到
- ChartMimic 的 high-level prompt 判据在附录 E.1，没读到

## Q3 · Explainer animation / motion：动画原则、Material motion、Mayer 多媒体原则说了什么？有哪些对生成的 Manim / 教学视频做 rubric 评测的 benchmark，一致性多少？

### Takeaway
- 教学动画最有实证依据的准则是 **Mayer 原则**，效应量 d 约 0.46–1.67。其中 temporal contiguity（d=1.30）、spatial contiguity、redundancy 都能从"讲稿时间轴 + 帧几何"程序化检查。
- UI 动效的时长 / 缓动有 Material 3 的 token 可以直接引用。
- 现有 Manim 评测的 VLM 判官**与人一致性很弱**：TheoremExplainBench 五维 Spearman 只有 0.14–0.72，视频级的 Visual Consistency 只有 0.17。Code2Video 没有报告人–VLM 一致性。

### Cited Findings

**A. 理论 / 规范**
- `[新]` Mayer 原则效应量（两套来源数字不同，引用时要标明出处）：

| 原则 | Cambridge Handbook 2014（中位数, 支持实验数） | Mayer 2017 *JCAL* 综述 |
|---|---|---|
| Coherence（删掉无关材料） | **0.86**（23/23） | d=0.70 |
| Signaling（突出结构的提示） | **0.86**（16/16） | d=0.46 |
| Redundancy（不在屏幕上重复旁白文字） | **1.22**（9/9） | d=0.87 |
| Spatial contiguity（文字紧挨对应图） | **1.10**（22/22） | d=0.79 |
| Temporal contiguity（旁白与画面同步） | — | d=1.30 |
| Segmenting（分段、学习者控制节奏） | — | d=0.70 |
| Multimedia（图文优于纯文） | — | d=1.67（5 个比较） |

  — [Cambridge Handbook 章节](https://resolve-he.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E)；[Mayer 2017 JCAL 10.1111/jcal.12197](https://zendy.io/title/10.1111/jcal.12197)
- `[新]` 2017 综述提到：部分原则对低先验知识学习者更有效 — [JCAL 2017](https://zendy.io/title/10.1111/jcal.12197)
- `[新]` **Material 3 motion tokens**（Android MDC 文档）
  - Duration：Short1–4 = 50/100/150/200ms；Medium1–4 = 250/300/350/400ms；Long1–4 = 450/500/550/600ms；ExtraLong1–4 = 700/800/900/1000ms
  - Easing：
    - Emphasized Decelerate `cubic-bezier(0.05,0.7,0.1,1)`
    - Emphasized Accelerate `(0.3,0,0.8,0.15)`
    - Standard `(0.2,0,0,1)`
    - Standard Decelerate `(0,0,0,1)`
    - Standard Accelerate `(0.3,0,1,1)`
    - Linear `(0,0,1,1)`
    - Emphasized 是两段 path
  - 规则：
    - "duration should increase as the area/traversal of an animation increases"
    - 进入屏幕用 decelerate，离开用 accelerate
    - linear 只用于简单、非风格化的运动
  — [material-components-android Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
- `[新]` 同一份文档有自相矛盾的地方：默认转场写的是"container transform 进入 = motionDurationLong1 (300ms)""fade 进入 = Short2 (150ms)"，跟 token 表（Long1=450、Short2=100）对不上，推测是旧版 M2 数值残留，引用时只引 token 表 — 同上
- M2 旧版 speed 页面（material.io/design/motion/speed）本次抓取为空，无法核对 — [m2.material.io speed](https://m2.material.io/design/motion/speed.html)

**B. 教学动画 / Manim 评测**
- `[已有·补数]` **TheoremExplainBench**（ACL 2025）各维度判官和人评一致性（40 个视频、12 名 STEM 学生；α 按 3 人计算）：

| 维度 | 判官与输入 | Spearman ρ（人 vs 判官） | Krippendorff α（人–人） |
|---|---|---|---|
| Accuracy & Depth | GPT-4o，纯文本 SRT | 0.14 | 0.45 |
| Visual Relevance | GPT-4o，关键帧 | **0.72**（p=0.001） | 0.36 |
| Logical Flow | GPT-4o，纯文本 SRT | 0.16 | 0.56 |
| Element Layout | GPT-4o，关键帧 | 0.42（p=0.03） | 0.31 |
| Visual Consistency | Gemini 2.0 Flash，视频切段 | 0.17 | 0.36 |

  - 文本维度 0–1 分，帧 / 段维度 1–5 分，人评取 {0, 0.5, 1}，总分是五维几何平均，判官 temperature 0
  - 常见视觉失败：文字或形状重叠、文字不对齐、对象尺寸不一致、位置不佳
  — [arXiv 2502.19400](https://arxiv.org/html/2502.19400)
- `[已有·补数]` **Code2Video** AES 判官是 **Gemini-2.5 Pro**，五维每项 **20 分**、合计 100：
  - **Element Layout**：文字 / 图的清晰可读、动画内容的位置与尺寸、平衡与留白
  - **Attractiveness**：配色和谐、动画吸引力
  - **Logic Flow**：引入–展开–结论、渐进脚手架
  - **Accuracy & Depth**：事实正确、深度与目标匹配
  - **Visual Consistency**：风格、色板、动画风格与 timing 统一
  - 冲突：正文又说每维"rated on a 100-point scale"，论文没有调和这两种说法
  — [arXiv 2510.01174](https://arxiv.org/html/2510.01174)
- `[已有·补数]` Code2Video **没有报告人–VLM 一致性**。唯一的相关是人评内部 Aesthetics 与 TeachQuiz r=0.971（p=0.0059，样本量没写）；随机视频对照的 TQ 增益约 2.0–5.0 — 同上
- `[新]` Code2Video 的 6×6 anchor critic 只检查三件事：同一格内元素重叠、讲稿行被动画遮挡、大面积空白导致失衡。occupancy table 把每个元素映射到 anchor / scale / 代码行 — 同上

### Inferences
- **VLM 在动画上的可靠性排序**
  - 看关键帧判"画面和概念是否相关"：最可信（ρ=0.72）
  - 看关键帧判布局：中等（0.42）
  - 看视频判运动流畅 / 风格一致：几乎无效（0.17）
  - 结论：时间维度的质量（缓动、时长、同步、风格一致）应改成从 Manim 源码 / 动画时间线程序化检查
- **Mayer 原则天然适合程序化**：temporal contiguity 要旁白时间戳 + 动画起止时间；spatial contiguity 要 label 与目标 mobject 的距离；redundancy 要 SRT 与屏幕文字的重合率。Manim 源码里这三样都拿得到
- **Disney 12 原则多数是角色动画用的**：squash & stretch、solid drawing、appeal 对公式动画意义不大。能迁移的主要是 slow in / slow out（= 缓动）、staging（一次只有一个焦点）、timing、follow through / overlapping（LaggedStart 错峰）

#### 候选 rubric · Explainer Animation（14 条）

| # | 检查项 | 来源 | 可查性 |
|---|---|---|---|
| A1 | **任意采样帧无非预期重叠**：Text / MathTex mobject 的 bbox 两两不交（每个 play 结束后都查） | TEB Element Layout；Code2Video critic | 【P】Manim 帧几何 |
| A2 | **不出画**：所有可见 mobject bbox 在画框内，四边留出 ≥ 画框 5% 的安全边距 | Code2Video 6×6 anchor；TEB 常见失败 | 【P】 |
| A3 | **无大面积空白失衡**：6×6 栅格中，有内容的格子不全挤在一侧（占用率左右差 ≤ 阈值） | Code2Video critic "large unused regions" | 【P】 |
| A4 | **讲稿–画面同步**：旁白提到某对象的时刻 ±1s 内，该对象出现或被高亮 | Mayer temporal contiguity（d=1.30） | 【P】需要 TTS 时间戳 + 动画时间线 |
| A5 | **标签紧邻对象**：解释性 label 到其目标 mobject 的距离 < 画框宽 10%，不集中放在远处的图例区 | Mayer spatial contiguity（d=0.79 / 1.10） | 【P】 |
| A6 | **屏幕文字不照抄旁白**：Text mobject 与同时段 SRT 的 token 重合率 < 阈值（字幕轨除外） | Mayer redundancy（d=0.87 / 1.22） | 【P】 |
| A7 | **无无关装饰**：没有和概念无关的图形、背景动效、花哨转场 | Mayer coherence（d=0.70 / 0.86） | 【V】 |
| A8 | **关键步骤有信号**：新引入的关键项有 Indicate / Circumscribe / 颜色变化等强调 | Mayer signaling（d=0.46 / 0.86）；Glance Test 的强调思想 | 【P】查源码动画类型 + 【V】 |
| A9 | **分段与停顿**：每个概念步骤后 wait ≥0.5s；单 Scene 只讲一个子概念；单段 ≤ ~60s | Mayer segmenting（d=0.70） | 【P】 |
| A10 | **非线性缓动**：位移 / 缩放类动画不用 linear rate_func（连续旋转、曲线描绘除外）；入场 decelerate、出场 accelerate | Material easing（linear 只用于简单运动）；Disney slow in / slow out `[未核验]` | 【P】 |
| A11 | **时长与运动量匹配**：小元素变化 ≤ 大范围位移的时长；文字停留时间 ≥ 阅读时间（建议 ≥0.3s/词，阈值为推断） | Material "duration should increase as the area/traversal…increases" | 【P】 |
| A12 | **一次一个焦点**：同一时刻独立运动的对象组 ≤ 2（LaggedStart 编组算一组） | Disney staging `[未核验]` | 【P】计数并发动画 + 【V】 |
| A13 | **跨场景风格一致**：同一概念同一颜色；全片色板 ≤ ~5 色；字体统一 | Code2Video Visual Consistency；TEB VC（视频 VLM 只有 ρ=0.17，所以改程序查） | 【P】 |
| A14 | **画面与概念相关**：关键帧确实在展示该步推导 / 概念，而不是装饰图 | TEB Visual Relevance（ρ=0.72，VLM 最可靠的一维） | 【V】 |

### Gaps
- **Thomas & Johnston *The Illusion of Life*（1981）的 12 原则原文本次没抓**。名单是通识 `[未核验]`：squash & stretch、anticipation、staging、straight ahead / pose to pose、follow through & overlapping action、slow in & slow out、arcs、secondary action、timing、exaggeration、solid drawing、appeal
- **3Blue1Brown / Manim 社区实践没有检索到一手材料**。以下 Manim 默认值是通识 `[未核验]`，需查 Manim Community 文档：
  - Animation 默认 run_time = 1s
  - 默认 rate_func = smooth
  - 默认画框约 14.22 × 8 单位、1920×1080
- Material M2 的旧时长建议（移动端约 300ms、入 225 / 出 195ms、桌面更短、可穿戴更短）抓取失败，是通识 `[未核验]`
- 没有找到"教学动画 VLM 判官 vs 人"在 TEB 之外的一致性数据；Code2Video、Paper2Video、DTVBench 均未报人–VLM 相关。项目已有笔记里的 Animation2Code 83.9% 是 Web 动画、和人类偏好的一致率，不是 Manim
- A11 的阅读速度阈值（0.3s/词）和 A9 的 60s 单段上限没有直接文献，是推断值

