# 程序守底线，VLM 只做两两比较

**结论先行。** 人的审美有共性，但在本项目这类人造物上很薄。日常场景图上，个体评分与其他人均值的相关（taste typicality）平均 **0.66**；职业设计师对同一批 UI / 平面设计的评分者间一致只有 **Krippendorff α 0.19–0.37**，折成两两一致率约 **55–62%**。共享的部分集中在「可读、可辨、没缺陷」：对比度、层级、对齐、不溢出、不闪烁、曝光正常、几何无破面。经典书籍（Bringhurst、WCAG、Tufte、Cleveland–McGill、Mayer、Birn、Bowen、Murch）里能落成阈值的规则也几乎都在这一层。分歧集中在配色和谐与风格取向，设计师之间也对不齐。rubric 能不能让 VLM 更像人，要分情况看。判「整体好不好看」时增益小（**+1.7~+6.3 个百分点**），有时为零（TASTE **−0.003**）。判「有没有缺陷」、或把程序结果写进 prompt 时增益大（SlideAudit macro F1 **0.476→0.655**，VisEval SRCC **0.507→0.843**）。效果最确定的是把评委拉齐（WebDevJudge 人–人一致 **65%→92%**，CheckEval judge 间 α **0.06→0.45**）。比 rubric 内容更大的杠杆是评判形式：同一 VLM 从打绝对分改成两两比较，与人类排名的 Spearman 从 **0.36 升到 0.86**。推荐协议如下：

- 程序条目做门控
- VLM 只在通过门控的同组候选之间两两比较
- 逐条二值短答，强制二选一，AB/BA 各判一次
- 附一对视觉相似的正反样例
- 每个 prompt 放 5–10 条 VLM 条目

verifier 的目标应定为「高共识子集上 ≥80%」，不追求全量逼近 100%。

> **标记约定**
> - 〔未核实〕只见二手来源或没打开原文；〔二手〕来自书评 / 目录 / 课程笔记；〔推断〕本文推理；〔本文计算〕由引用数字换算；〔项目已有〕出自本项目已有笔记
> - 检查方：**P** = 程序（DOM / computed style / 源码 / scene graph / 帧统计）；**V** = 只能 VLM 看像素；**P+V** = 程序出数、VLM 复核语义
> - 条目后缀：**⇔** = 区间题（太少、太多都不过）；**◇** = 只做两两比较、不做单图判定
> - 来源抓取日期 2026-11-02

---

## 1 经典书籍的共识落在「可读性与连续性」，审美方向没有阈值

六个领域的经典文献都给了大量规则，能写成「可判对错」的只有三类：

- **感知与可读性阈值**：字号、行长、对比度、编码精度、曝光、主辅光比
- **一致性与连续性语法**：间距网格、跨页样式、180° 轴线、30° 规则、风格统一
- **反冗余原则**：Nielsen #8、Tufte data-ink、Mayer coherence

「appeal」「情绪」「和谐」这类目标，书里只有原则，没有阈值。作者们自己也反对把规则当公式：

- Birn：「don't think of three-point lighting as an excuse to light by formula」
- Murch：Rule of Six 的百分比「slightly tongue-in-cheek」
- Cleveland & McGill：编码排序「does not result in a precise prescription」

另外，只有 Mayer 多媒体原则和 Cleveland–McGill 编码排序是**实验结论**，其余都是从业者共识。所以书里的规则适合做门控和软约束，不适合做单调递增的 reward〔推断〕。

### 1.1 Web / UI：数字最硬的是排版、间距、对比度

| 来源 | 可提炼的可操作条目 | 核实状态 |
|---|---|---|
| Bringhurst《The Elements of Typographic Style》 | 2.1.2 舒适行长；2.2.1 行距要配合字体与行长；2.2.2 纵向间距按固定间隔增减；3.1.1「Don't compose without a scale」；2.1.6 全大写加字距 ([webtypography.net](https://webtypography.net/toc)) | 规则标题一手；「45–75 字符、66 最佳」〔未核实〕 |
| Butterick《Practical Typography》 | 网页正文 15–25 px；行距为字号的 120–145%；行长 45–90 字符；全大写只用于短于一行的文本，并加 5–12% 字距 ([Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)) | 一手 |
| WCAG 2.2 | 1.4.3 正文对比 4.5:1、大字 3:1 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html))；1.4.11 非文本组件 3:1 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html))；1.4.8 行宽 ≤80 字符、行距 ≥1.5、不两端对齐 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)) | 一手 |
| Material Design spacing | 组件排在 8dp 网格上，局部可用 4dp ([material.io](https://material.io/design/layout/spacing-methods.html)) | 一手 |
| Williams《The Non-Designer's Design Book》 | Contrast / Repetition / Alignment / Proximity（CRAP），只能拆成可观察问句 ([书评](https://thevisualcommunicationguy.com/2013/05/15/the-non-designers-design-book/)) | 原则名一手，原文〔未核实〕 |
| Nielsen heuristic #8 | 「Interfaces should not contain information which is irrelevant or rarely needed」；每个元素（含留白）都要有目的；可点与不可点不用同一种视觉处理 ([NN/g](https://www.nngroup.com/articles/aesthetic-minimalist-design/)) | 一手 |
| Refactoring UI；Müller-Brockmann《Grid Systems in Graphic Design》 | 层级先靠字重和颜色，再靠字号；间距与字号用有限尺度（4/8/12/16/24/32…） ([wiki 摘要](https://github.com/s0xDk/refactoring-ui-skill/wiki)) | 〔二手〕 |
| Krug、Lidwell《Universal Principles of Design》、Albers《Interaction of Color》、Lupton | Billboard Design、Signal-to-Noise、颜色相对性 | 〔未核实〕，不作 rubric 依据 |
| 厂商「反 AI 味」清单 | Anthropic frontend-design：禁奶油底配赤陶、SaaS 卡片套件、渐变洗底；编号和标签必须承载信息；先定 4–6 色 token ([SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md))。OpenAI GPT-5.4 前端指南：一个 H1、≤2 种字体、一个强调色、首屏一个主 CTA ([OpenAI blog](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)，经项目笔记转引) | 一手 / 转引 |

- 各来源的数字互相不一致：行长上限有 75 / 80 / 90 三种说法，行高有 1.45 / 1.5 两种 → 只能当初始区间，阈值要在参考页上反推〔推断〕

### 1.2 PPT：3 秒看懂是唯一有名有姓的检验法

| 来源 | 可提炼的可操作条目 | 核实状态 |
|---|---|---|
| Duarte Glance Test（slide:ology 体系） | 3 秒或更短看懂一页要点；每页一个「single, precise point」；用对比和留白突出关键信息 ([Duarte](https://www.duarte.com/resources/guides-tools/the-glance-test/)) | 一手；按 signal-to-noise 打分的细则、「超过 75 词就是文档」〔未核实〕 |
| Kawasaki 10/20/30 | 10 页、≤20 分钟、字号 ≥30pt ([AhaSlides 转述](https://ahaslides.com/blog/10-20-30-rule-presentations)) | 〔二手〕 |
| Reynolds《Presentation Zen》 | restraint、simplicity、留白、signal-to-noise | 〔未核实〕 |
| SlideAudit flaw taxonomy（17 位专家形成性研究） | 5 维、27 类 flaw：Cluttered Layout、Misaligned Elements、Insufficient Contrast（采用 WCAG 2.1）、Lack of Visual Hierarchy、Excessive Text Density、Occluded Content、Content Overflow 等；与 Gestalt 一一对应（如 Cluttered↔Proximity）。2,400 张真实 slide 里，flaw 出现率最高的是 Occluded Content **15.5%** 和 Inappropriate Font Sizing **15.2%** ([SlideAudit](https://arxiv.org/html/2508.03630v1)) | 一手 |

- 字号下限 18 / 24 / 30pt 都是从业者规则，没找到实验依据

### 1.3 图表：理论最成体系，规则大多能从 spec 程序化检查

| 来源 | 可提炼的可操作条目 | 核实状态 |
|---|---|---|
| Tufte《The Visual Display of Quantitative Information》 | Lie Factor = 图中呈现的效应 / 数据中的效应，理想值 ≈1；data-ink ratio；chartjunk ([LMU 课件](https://www.medien.ifi.lmu.de/lehre/ws1415/iv/uebung/u1/slides_1.pdf)；[eagereyes](https://eagereyes.org/blog/2013/definition-chart-junk)) | 概念一手；「0.95–1.05」阈值〔未核实〕；反对意见：严格最大化 data-ink 会得到「terrible and nonsensical」的图（eagereyes） |
| Cleveland & McGill 1984（JASA） | 编码精度排序：共同尺度上的位置 > 非对齐位置 > 长度 / 方向 / 角度 > 面积 > 体积 / 曲率 > 明暗 / 饱和度 ([Cornell 课件](https://info3312.infosci.cornell.edu/slides/04-graphical-perception.html))；Heer & Bostock 众包复现基本成立，但多值比较任务上不一定成立 ([Risks of Ranking](https://arxiv.org/pdf/2212.10533)) | 实验结论 |
| Munzner《Visualization Analysis & Design》Ch.5 | Expressiveness：有序数据用 magnitude channel，类别数据用 identity channel；Effectiveness：最重要的属性给最显著的 channel ([UBC 课件](https://www.cs.ubc.ca/~tmm/courses/436V-20/slides/marks.pdf)) | 一手课件 |
| Draco（InfoVis 2018） | 准则写成 hard constraints（过滤）+ soft constraints（加权排序，权重可从感知实验中学） ([Draco](https://idl.uw.edu/draco)) | 一手 |
| Few、Ware、Mackinlay APT、ColorBrewer | bar 从 0 起；避免 3D；定性色板 ≤12 级 | 〔未核实〕 |

### 1.4 Manim / 解说动画：Mayer 原则是少有的实验级证据

| Mayer 多媒体学习原则 | 对应的程序检查 | 效应量 Cohen's d（Cambridge Handbook 2014 中位数 / Mayer 2017 综述） |
|---|---|---|
| Coherence：删掉无关材料 | 无无关装饰与背景动效 | 0.86 / 0.70 |
| Signaling：突出结构 | 关键项有 Indicate / 变色 | 0.86 / 0.46 |
| Redundancy：屏幕不照抄旁白 | 屏幕文字与同时段字幕重合率低 | 1.22 / 0.87 |
| Spatial contiguity：文字紧挨对应图 | label 到目标 mobject 的距离 | 1.10 / 0.79 |
| Temporal contiguity：旁白与画面同步 | 旁白提及后 ±1s 内对象出现 | — / 1.30 |
| Segmenting：分段 | 每步后停顿；单 Scene 一个子概念 | — / 0.70 |

- 出处：[Cambridge Handbook 章节](https://resolve-he.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E)；[Mayer 2017 JCAL](https://zendy.io/title/10.1111/jcal.12197)
  - 注意：这些 d 值衡量的是**学习效果**，不是审美〔推断〕
- Material 3 motion tokens ([MDC Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md))
  - 时长档位：Short 50–200ms、Medium 250–400ms、Long 450–600ms、ExtraLong 700–1000ms
  - 进入用 decelerate，离开用 accelerate；linear 只用于简单、非风格化的运动
  - 「duration should increase as the area/traversal of an animation increases」
  - 同一文档里的默认转场数值与 token 表矛盾，只引 token 表
- Disney 12 principles（Thomas & Johnston《The Illusion of Life》）〔未核实〕
  - 能迁移到公式动画的只有 slow in / slow out、staging、timing、follow-through（错峰）〔推断〕

### 1.5 3D：灯光和 PBR 有数字，构图和形体只有原则

| 来源 | 可提炼的可操作条目 | 核实状态 |
|---|---|---|
| Birn《Digital Lighting and Rendering》3rd ed. | 「Start in Darkness」：不留默认光和全局环境光；主光在顶视、侧视都偏离相机 15–45°；辅光「at most … about half as bright as your Key (2:1)」，暗场景可到 8:1；rim 用来「visually separate the object from the background」；先看场景里哪些光有动机 ([3dRender.com](https://3drender.com/light/3point.html))；白平衡 3200K / 5500K ([色温表](https://3drender.com/glossary/colortemp.htm)) | 作者站上经出版社许可改写的教程；书中 Ch1 / Ch7 小节〔未核实〕 |
| Adobe《The PBR Guide》Part 2；Pharr 等《Physically Based Rendering》 | dielectric base color 不低于 30–50 sRGB、不高于 240；金属反射率 70–100%（sRGB 180–255）；metallic 基本二值；dielectric F0 默认 0.04 ([Adobe](https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2))；BRDF 能量守恒 ([pbr-book](https://pbr-book.org/3ed-2018/Color_and_Radiometry/Surface_Reflection)) | 一手 |
| Gurney《Color and Light》 | gamut masking：每幅画只用一个受限色域；「You rarely need those full strength colors」 ([Gurney Journey](https://gurneyjourney.blogspot.com/2011/09/part-3-gamut-masking-method.html)) | 博客一手；书目录〔未核实〕 |
| Blender Camera 手册 | 构图辅助线 Thirds / Golden Ratio / Diagonal / Harmony Triangle；Safe Areas ([Blender Manual](https://docs.blender.org/manual/en/latest/render/cameras.html)) | 一手 |
| Dieter Rams 十条；Rhino GCon | 「as little design as possible」「honest」「thorough down to the last detail」 ([Vitsoe](https://www.vitsoe.com/us/about/good-design))；G0 位置 / G1 切线 / G2 曲率连续 ([McNeel](https://docs.mcneel.com/rhino/8/help/en-us/commands/gcon.htm))；Class-A 曲面要求 G2 及以上〔二手〕 | 一手 / 二手 |
| Mateu-Mestre《Framed Ink》；Disney / Pixar shape language；Calahan「Storytelling Through Lighting」 | 叙事构图、剪影、明暗结构 | 〔未核实〕，不作 rubric 依据 |

### 1.6 Video：剪辑语法最可操作，Murch 排序可当破平权重

| 来源 | 可提炼的可操作条目 | 核实状态 |
|---|---|---|
| Murch《In the Blink of an Eye》 | Rule of Six：Emotion 51% > Story 23% > Rhythm 10% > Eye-trace 7% > 2D plane 5% > 3D space 4%；六条满足不了时，从最底下一条开始往上牺牲 ([filmdaft](https://filmdaft.com/?p=33138)) | 〔二手〕；Murch 自称百分比半开玩笑 |
| Bowen《Grammar of the Shot》2nd ed. | Headroom p.25、Look Room p.28、Rule of Thirds p.30、180° rule p.102、30° rule p.106（换角度拍同一主体时「ideally move the camera at least 30 degrees」） ([O'Reilly](https://www.oreilly.com/library/view/grammar-of-the/9780240521213/Chapter04g.html))；30° 的阈值各家不一 ([Wikipedia](https://en.wikipedia.org/wiki/30-degree_rule)) | 目录与预览一手 |
| Bowen《Grammar of the Edit》 | 切点六因素：information、motivation、composition、camera angle、continuity、sound | 〔未核实〕 |
| Mascelli《The Five C's of Cinematography》 | Camera Angles / Continuity（含 screen direction）/ Cutting / Close-ups / Composition ([Silman-James](https://silmanjamespress.com/the-five-cs-of-cinematography/)) | 目录一手 |
| Block《The Visual Story》 | 7 个视觉要素：space、line、shape、tone、color、movement、rhythm；某要素的 contrast 越大，视觉强度越高，affinity 越大越低 ([O'Reilly Ch.2](https://www.oreilly.com/library/view/the-visual-story/9780240807799/009_9780080551692_chapter2.html)) | 预览一手 |
| Bordwell & Thompson《Film Art》 | 镜头间 graphic / rhythmic / spatial / temporal 四种关系，前两种存在于一切剪辑；axis of action、eyeline match ([P.O.V.](https://pov.imv.au.dk/Issue_06/section_1/artc6A.html)) | 〔二手〕 |
| Arijon、Blain Brown、Katz、Mercado | 三角机位、曝光、对话调度 A/I/L、镜头类型目录 | 〔二手·目录〕 |

- 对代码渲染短片的迁移性〔推断〕
  - 直接迁移：构图三条（headroom / look room / 三分）、曝光、rhythm、eye-trace、Block 强度曲线
  - 有条件迁移：180° / 30°，只适用于多镜头且有主体运动的片子
  - 不迁移：Katz 对话调度、Mascelli 特写表演、人物妆发类属性
  - Bowen 的构图规则都以人物为对象；网页动效里对应的是安全区与文字不贴边

---

## 2 学术工作：VLM 判「缺陷」接近人，判「好看」接近随机

同一个 VLM 在不同问题上的表现差别很大，可以接近人，也可以接近随机。决定一致度的主要是问题类型，而不是模型：

- **VLM 接近人**：有参考图的相似度判断、单图整体观感、纹理审美、带 taxonomy 的缺陷识别
- **VLM 接近随机**：构图、视觉层级、配色和谐、镜头运动、多视角几何、跨页 / 跨时间一致性

### 2.1 经过心理测量验证的量表只有网页这一类

- **VisAWI**（Moshagen & Thielsch 2010，IJHCS）：唯一系统验证过的网页审美多维量表 ([作者草稿](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf))
  - 规模：7 个研究，2,000 多名参与者，70 多个网站；18 条目，4 个维度
  - 内部一致性 Cronbach α：Simplicity **.89**、Diversity **.87**、Colorfulness **.89**、Craftsmanship **.85**、总分 **.94**；CFA 拟合 CFI 0.945–0.951
  - 效度：Simplicity 与 classical aesthetics 相关 r **.82**，Diversity 与 expressive 相关 r **.80**
  - 条目本身就是现成的 rubric 骨架（`(r)` = 反向计分）
    - Simplicity：layout too dense (r)、easy to grasp、everything goes together、appears patchy (r)、well structured
    - Colorfulness：colors do not match (r)、choice of colors is botched (r)
    - Craftsmanship：professionally designed、designed with care、lacks a concept (r)
  - 作者自述局限：**没有测重测信度**；Diversity 条目「too general to guide designers」
- **VisAWI-S**：4 条目短版，3 个研究共 1,673 人 ([RePEc](https://ideas.repec.org/a/taf/tbitxx/v32y2013i12p1305-1311.html))；原始 α 只读到摘要〔未核实〕
- **Lavie & Tractinsky 2004**：classical（clean、clear、pleasant、symmetrical、aesthetic）与 expressive（original、sophisticated、fascinating、creative、special effects）两维 ([PDF](http://www.ise.bgu.ac.il/faculty/noam/papers/04_tl_nt_ijhcs.pdf))
  - α：classical **.85 / .86**，expressive **.87 / .86**（初始样本 / 交叉验证样本）；两维相关 r .69 / .63
- **图像与视频审美属性体系**（不是量表，但给了维度定义）
  - PARA：每张图约 25 人标，属性为 composition、light、color、depth of field、content ([PARA](https://arxiv.org/abs/2203.16754))
  - VADB：视频 6 个通用属性（Composition、Shot Size、Lighting、Visual Tone、Color、Depth of Field），每个视频 ≥13 名专业标注员 ([VADB](https://arxiv.org/html/2510.25238v2))
  - VisionReward：图像 61 个、视频 64 个二值问题 ([VisionReward](https://arxiv.org/abs/2412.21059))
- **读法**：α .85–.94 是同一个人在多个条目之间的一致性，不是不同评委之间的一致性。可以借这些量表的维度来定义条目，但不能据此认为单个评委的分数稳定〔推断〕

### 2.2 MLLM 审美评测基准：一致性数字

| 领域 | 基准 | VLM / 设定 | VLM 与人（指标） | 人与人（指标） |
|---|---|---|---|---|
| 通用图像 | AesBench ([arXiv](https://arxiv.org/html/2401.08276)) | GPT-4V | 感知选择题准确率 **72.08%**；打分档位选择准确率 **50.86%**（随机 33.33%） | 未报 |
| 通用图像 | UNIAA ([arXiv](https://arxiv.org/html/2404.09619)) | GPT-4V | 感知题准确率 74.74%；最弱属性 Composition 70.14% | 资深 **87.39%** / 初级 79.01% |
| 通用图像 | Q-Align ([arXiv](https://arxiv.org/html/2312.17090)) | 专训 | AVA 上 SRCC **0.822**；LAION Aesthetic Predictor 0.721 | — |
| T2I | HPSv3 Table 4 ([arXiv](https://arxiv.org/html/2508.03789)) | 各 reward model 跨数据集 | pairwise 准确率 57–77%；LAION aesthetic 57.4 / 56.8 / 76.8 / 59.9 | HPDv2 单人–单人 **78.1%**；ImageReward 测试集 65.3% ([HPSv2](https://arxiv.org/html/2306.09341)) |
| 网页 | UIClip ([arXiv](https://arxiv.org/html/2404.12500v1)) | GPT-4V，prompt 内给 CRAP 描述 | pairwise **51.58%**；专训 UIClip 75.12% | Krippendorff α **0.37** |
| 网页 | WebDevJudge ([arXiv](https://arxiv.org/html/2510.18560v2)) | GPT-4.1 | pairwise **70.34%**；只给截图 59.5–62.1%，只给代码 64.5–69.6% | 人 pairwise 平均 **84.56%** |
| 网页 | ArtifactsBench ([arXiv](https://arxiv.org/html/2507.04952v2)) | Gemini-2.5-Pro + Qwen2.5-VL-72B，10 维 checklist | 与 WebDev Arena 排名一致 **94.4%**；280 例专家 pairwise 一致 90.95% | — |
| UI / 平面 | TASTE ([arXiv](https://arxiv.org/html/2605.20731)) | Qwen3-VL、Gemma-3 等 | 与设计师多数票一致率 **0.50–0.54**（随机 0.50）；Visual Hierarchy 维度 0.48–0.55 | Krippendorff α **≈0.19** |
| 移动 UI | UICrit ([arXiv](https://arxiv.org/html/2407.08850v3)) | 生成设计批评，专家打分 | zero-shot 0.31 → few-shot + 视觉提示 0.48；人类设计师 0.75（批评质量评分） | 批评评分 Fleiss κ 0.29–0.31 |
| PPT | PPTEval ([arXiv](https://arxiv.org/html/2501.03936)) | GPT-4o，1–5 分 | Pearson：Design **0.90**、Content 0.70、Coherence **0.55** | Fleiss κ 0.59 |
| PPT | SlidesBench ([arXiv](https://arxiv.org/html/2501.00912)) | GPT-4o，0–5 分 | ICC 73.8%–85.3% | — |
| PPT | SlideAudit ([arXiv](https://arxiv.org/html/2508.03630v1)) | GPT-4o + taxonomy | flaw 检测 macro F1 0.655 | Fleiss κ **0.26** |
| 图表 | VisEval ([arXiv](https://arxiv.org/html/2407.00981)) | GPT-4V + 程序检查结果 | readability SRCC **0.843** | 人–人 SRCC 0.782 |
| 图表 | VisJudge-Bench ([arXiv v3](https://arxiv.org/html/2510.22373v3)) | 无参考，5 分制 | 相关：GPT-5 **0.428**、Gemini-2.5-Pro 0.265；微调 VisJudge 0.687 | 附录，未读到 |
| 图表 | ChartMimic / MatPlotBench / Plot2Code | 与参考图比相似度 | Pearson 0.70–0.77 ([ChartMimic](https://arxiv.org/html/2406.09961)) / 0.876 ([MatPlotBench](https://arxiv.org/html/2402.11453)) / 0.479 ([Plot2Code](https://arxiv.org/html/2405.07990)) | — |
| Manim | TheoremExplainBench ([arXiv](https://arxiv.org/html/2502.19400)) | GPT-4o 看关键帧；Gemini 2.0 Flash 看视频 | Spearman：Visual Relevance **0.72**、Element Layout 0.42、Visual Consistency **0.17**、Accuracy 0.14 | Krippendorff α 0.31–0.56 |
| 3D 资产 | GPTEval3D ([arXiv](https://arxiv.org/abs/2401.04092)) | GPT-4V，多视角 + 法线图 | 自家数据 Kendall τ 0.710、pairwise 78.9%；在 3DGen-Bench 人类数据上 67.7% ([3DGen-Bench](https://arxiv.org/abs/2503.21745)) | — |
| 3D 资产 | Eval3D ([arXiv](https://arxiv.org/abs/2504.18509)) | GPT-4V | pairwise 一致率：审美 **85.6%**，几何 **46.9%** | 审美维度 **83.8%** |
| 3D 资产 | MATE-3D ([arXiv](https://arxiv.org/abs/2412.11170)) | GPTEval3D 与图像美学模型 | GPTEval3D KRCC 0.355–0.432；LAION aesthetic Overall SRCC **0.150** | — |
| Blender | BlenderAlchemy ([arXiv](https://arxiv.org/abs/2404.17672)) | GPT-4V 状态评估器 | 与人选择一致 71%（592 次比较） | — |
| 3D 场景 | SceneEval ([arXiv](https://arxiv.org/abs/2503.14756)) | GPT-4o / Qwen2.5-VL-7B | 与人工核验一致 83.5–94.6%（κ 0.56–0.77）；Qwen 的属性判断 κ **0.26** | — |
| 视频 | Video-Bench ([arXiv](https://arxiv.org/html/2504.04907v1)) | MLLM chain-of-query | Aesthetic Spearman **0.702**；LAION 帧级 0.446 | — |
| 视频 | VideoScore ([arXiv](https://arxiv.org/html/2406.15252)) | GPT-4o 零样本 | Spearman 平均 23.0（×100）；专训 VideoScore 77.1 | Visual Quality Fleiss κ **0.088**，Factual Consistency −0.089 |
| 视频 | ShotBench ([arXiv](https://arxiv.org/html/2506.21356)) | GPT-4o | 电影语言识别准确率平均 59.3%；camera movement 48.3%，lens size 48.9% | — |
| 视频 | CineTechBench ([arXiv](https://arxiv.org/html/2505.15145)) | GPT-4o / Gemini-2.5-Pro | 静帧 Composition 57.5% / 67.5%；镜头运动 Zoom 14.29%（Gemini） | — |
| 视频 | VideoAesBench ([arXiv](https://arxiv.org/html/2601.21915)) | Claude-Sonnet-4.5 | 准确率 67.88%（随机 33.59%）；最弱 visual composition 63.98% | — |
| 视频 | VBench-2.0 ([arXiv](https://arxiv.org/html/2503.21755v2)) | VLM 评测器 | Composition Spearman 0.817，18 维中最低（只在 4 个模型的 win ratio 上算） | — |
| 视频 | VADB ([arXiv](https://arxiv.org/html/2510.25238v2)) | 未测 MLLM | — | Krippendorff α：Overall 0.59，Color **0.54**（最低） |

规律：

- **有参考比无参考可靠得多**：图表上与参考图比相似度，Pearson 0.70–0.88；无参考判好坏只有 0.27–0.48
- **维度差异大于模型差异**
  - 跨领域最弱的维度：构图、视觉层级、镜头运动、多视角几何、跨时间一致性
  - 最强的维度：整体观感、纹理审美、画面与概念是否相关
  - 3D 纹理审美上，VLM 已追平人与人之间（Eval3D：85.6% vs 83.8%）
- **换数据集掉 10 个点以上是常态**：GPTEval3D 78.9% → 67.7%；T2I reward model 跨数据集只剩 57–77%
- **VLM 打绝对分普遍虚高**：VisJudge 上人类平均分 3.13，Qwen2.5-VL-7B 给 3.89，分数挤在 4.0 附近
- **数据域空白**：没有任何公开 benchmark 面向网页 / Blender 渲染的短视频；图表、幻灯片、3D 代码产物也没有设计师间一致性数据

### 2.3 把 rubric 喂给 VLM：拆成缺陷有用，拆成审美偏好没用

已发表的做法有五类：

- 每个输入自动生成实例级 rubric（ARR、VideoArgus）
- 固定 taxonomy（SlideAudit、ArtifactsBench）
- 二值题库 + 学出来的权重（VisionReward）
- 程序先查、VLM 补判（VisEval、SceneEval）
- 原则描述 + 分数锚点（Haraguchi）

| 做法 | 有 / 无 rubric 对照（指标） | 读法 |
|---|---|---|
| ARR，每个 prompt 自动生成 5 条 rubric ([arXiv](https://arxiv.org/html/2605.08354)) | 偏好准确率 +1.7~+6.3 点；Gemini 3.1 Pro 在 HPDv3 上 76.6→78.3 | 整体偏好：增益小 |
| TASTE，提示里指明按哪条审美维度判 ([arXiv](https://arxiv.org/html/2605.20731)) | 标量头 0.583→0.580；pairwise 头 0.611→0.586 | 设计偏好：零或负 |
| UIClip，GPT-4V 拿到 CRAP 描述 ([arXiv](https://arxiv.org/html/2404.12500v1)) | pairwise 51.58%，约 10% 拒答 | 只给原则描述：无效 |
| WebDevJudge rubric ([arXiv](https://arxiv.org/html/2510.18560v2)) | **人–人一致 65.0%→92.0%**；模型 pairwise 有无 rubric「comparably」；单点打分时二值 rubric 好于 Likert | 对人增益大，对模型 pairwise 无增益 |
| CheckEval 二值 checklist，文本任务 ([arXiv](https://arxiv.org/html/2403.18771)) | 12 个 judge 间 Krippendorff α 0.09→0.48、0.06→0.45；与人 Spearman：GPT-4o 0.32→0.50，Mistral-Small 0.58→0.47 | 降噪大，与人对齐不稳 |
| SlideAudit taxonomy 提示 ([arXiv](https://arxiv.org/html/2508.03630v1)) | flaw 检测 macro F1：GPT-4o 0.476→0.655，Claude 3.7 0.492→0.612 | 缺陷识别：增益中等 |
| VisEval，把程序检查结果写进 prompt ([arXiv](https://arxiv.org/html/2407.00981)) | readability SRCC 0.507→**0.843** | 程序先行：增益大 |
| MSAVBench，实例级 rubric / 工具取证 ([arXiv](https://arxiv.org/html/2605.20183)) | 叙事连贯 Spearman 0.600→0.850；跨镜头布局一致 0.429→0.767（工具取证） | 拆题 + 工具：增益大 |
| VideoArgus，rubric + 视觉工具 ([arXiv](https://arxiv.org/html/2608.05485v1)) | 组内排序 Spearman 0.162→0.436（仅 VLM）→0.496（+工具）；没有去掉 rubric 的消融 | 不能全归因于 rubric |
| VisionReward，64 个二值问题 + 逻辑回归 ([arXiv](https://arxiv.org/html/2412.21059v4)) | 视频偏好准确率 72.1 vs VideoScore 54.9；问题越多越准；训练对从 200 增到 4k，准确率 77.6→81.3 | 学权重的 checklist：有效 |
| Haraguchi，GPT-4o + 设计原则 + 分数锚点 ([arXiv](https://arxiv.org/html/2410.08885)) | 与 60 名众包评分者均值的相关高于启发式指标；扰动越大相关越高；小幅对齐 / 留白扰动上 pairwise 不如启发式（r 值只在图中） | 大缺陷能判，小瑕疵判不出 |

评判形式比 rubric 内容更重要：

- **两两比较 > 绝对分**
  - GenArena：同一 judge 与 LMArena 排名的 Spearman，pointwise **0.36** → pairwise **0.86**；5 次运行的自洽 α 提高 0.13–0.14 ([GenArena](https://arxiv.org/html/2602.06013))
  - MLLM-as-a-Judge：GPT-4V 打分与人的 Pearson 0.490，pair 准确率（不含 tie）77.3% ([arXiv](https://arxiv.org/html/2402.04788v3))
- **强制二选一 > 允许平局**：在人类可区分的对子上，允许 tie 时准确率 54.9%，强制选择 83.9% ([GenArena](https://arxiv.org/html/2602.06013))
- **参考样例压位置偏差**
  - ARR：基础 VLM 正序 / 反序准确率差 30–35 点；加同分布的正反样例后降到 9–10 点 ([ARR Table 5](https://arxiv.org/html/2605.08354))
  - UICrit：按视觉相似度挑 few-shot 样例最好（区域评论质量 0.24→0.44）
- **长 CoT 有害**
  - 3-step CoT 让 GPT-4V 打分 Pearson 从 0.557 掉到 0.299 ([MLLM-as-a-Judge](https://arxiv.org/html/2402.04788v3))
  - CoT 还会放大 bbox 偏差：−1.0% → +4.1% ([FRAME](https://arxiv.org/html/2505.15249v2))
- **视觉刷分成本极低**
  - 给图加 bounding box，GPT-4o 分数涨 **+80.2%**；提示里写明偏差定义，只能减轻，不能清零 ([FRAME](https://arxiv.org/html/2505.15249v2))
  - 在 HTML/CSS 里，这类攻击只需要一个 `border`〔推断〕

**判断**：rubric 能提升 VLM 与人的一致性，但要满足三个条件：

- 每条是可观察的事实，最好是缺陷
- 逐条判，不是读完原则后给一个总分
- 有程序或工具给证据

对「整体好不好看」的偏好，rubric 几乎拉不动 VLM。最关键的空白：**没有任何工作在同一 VLM、同一审美数据上，干净地对比「rubric 分解」与「单一整体分」**。

---

## 3 审美共性：约一半共享，越接近设计越少

### 3.1 直接测量：共享口味真实存在，按领域递减

- Hönekopp 2006：31 人给 77 张面孔打分，一周后重测。用「与自己重测的一致」对比「与他人的一致」，私人口味与共享口味**大约各占一半**；单次测量的 Cronbach α 会高估共享程度 ([APA Monitor](https://www.apa.org/monitor/may06/beauty))
- Leder et al. 2016，同一方法：私人口味占比面孔 **40%**、抽象艺术 **75%** ([Frontiers](https://www.frontiersin.org/articles/10.3389/fnhum.2016.00155/full))
- Vessel et al. 2018：面孔、风景高度共享，建筑和艺术品个体差异大；而风景和建筑的重测可靠性没有差别，说明差异不是噪声 ([MPG](https://www.aesthetics.mpg.de/en/newsroom/news/news-article/article/beautiful-nature-controversial-art.html))
  - 风景静图 MM1（个体与其余人均值的相关）**0.60**（95% CI 0.53–0.66）；风景视频整体评分 0.40，连续评分 0.61 ([Isik & Vessel 2021](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.676032/full))
  - 面孔 0.84、抽象艺术 0.28〔未核实〕
- Chen et al. 2022：200 人评 88 张日常场景图 ([PDF](https://ycc.vision/files/papers/Chen_etal_2022_CB_crossmodelTasteTypicality.pdf))
  - taste typicality 平均 **0.664**（范围 0.315–0.839），复制实验 0.663
  - 个体重测可靠性 0.856；**没有一个人与平均口味负相关**
- Bignardi et al. 2024，双生子研究：遗传解释 taste typicality 方差的 26–41%；个体间偏好的相似度是场景 > 面孔 > 抽象图 ([Communications Biology](https://www.nature.com/articles/s42003-023-05710-4))

### 3.2 群体均值好学，个人难学

- 纯视觉 DNN 线性读出能解释群体均值 **53%**（最好 **72%**）的可解释方差，但对个体的预测力只相当于最「典型」的 32.5% 被试 ([Graham et al. CCN 2024](https://2024.ccneuro.org/pdf/524_Paper_authored_DeepAesthetics_CCN2024.pdf))
- PARA：预测群体均值 SROCC **0.879**（ResNet-50）；预测个人 0.681，用 100 个样本个性化后只到 **0.695** ([PARA](https://arxiv.org/abs/2203.16754))
  - 高分区间 (4,5] 的方差明显更低 → 对「什么是好」的共识强于对「什么是差」
- DesignPref：个性化模型稳定优于聚合模型 ([arXiv](https://arxiv.org/abs/2511.20513))；聚合 57.45% vs 个性化 60.16%〔项目已有〕

### 3.3 很多「普适规律」是平均出来的

- **复杂度倒 U**：聚类后发现，一组人越复杂越不喜欢，另一组越复杂越喜欢；倒 U 是两组平均的产物 ([Güçlütürk et al. 2016](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00112/full))
- **黄金比例**：群体偏好很弱；个体偏好强且跨时间稳定，但人与人差异极大 ([McManus et al. 2010](https://pubpeer.com/publications/EBCD4B31EC80AC07FF8A5B70FD7066))
- **颜色**
  - 生态价值理论能解释美国成年人**平均**颜色偏好方差的 80% ([Palmer & Schloss 2010](https://palmerlab.berkeley.edu/pdf/Palmer%26Schloss%282010%29.pdf))；复测只有 61% ([Frontiers 2022 复述](https://www.frontiersin.org/articles/10.3389/fpsyg.2022.1010108/full))
  - 双色和谐有可建模的一般规律（1,431 个组合）([Ou & Luo 2006](https://zendy.io/title/10.1002/col.20208))；但跨 8 国研究显示，like / dislike 有文化差异，也受设计背景影响 ([Ou et al. 2012](https://research.chalmers.se/en/publication/154421))
- **网页首印象**
  - Tuch et al. 2012：119 张网页截图，**低视觉复杂度 + 高原型性**最受欢迎，判断在 50ms 内形成 ([Google Research](https://research.google/pubs/pub38315/))
  - Reinecke et al. 2013：复杂度 + 色彩度的二次项加人口学交互，解释审美吸引力 adj R² **.48**；复杂度呈倒 U，且与年龄强交互 ([PDF](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf))

### 3.4 本项目产物上的人–人一致性

| 领域 | 数据集 | 人–人一致（指标） |
|---|---|---|
| UI / 平面设计 | TASTE ([arXiv](https://arxiv.org/html/2605.20731)) | 排序 α ≈0.19；各维 pair-τ 0.10–0.22，折合两两一致率约 55–61%〔本文计算，无 tie 时 P = (1+τ)/2〕；**Color Harmony τ 0.103 最低**，Typography 0.224 |
| UI | DesignPref ([项目笔记](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)) | 二元一致 0.624，α 0.248；4 档量表 α **0.104**；28.5% 的对子两两分歧率 ≥96%〔项目已有〕 |
| UI | UIClip | α 0.37 |
| 移动 UI | UICrit | aesthetics ICC(1,1) +0.024〔项目重算，见项目笔记〕 |
| 网页 | WebDevJudge | 无 rubric 65.0%，有 rubric **92.0%**（含平局的标注员间一致率） |
| PPT | PPTEval / SlideAudit | Fleiss κ 0.59 / 0.26 |
| 图表 | VisEval | readability SRCC 0.782 |
| Manim | TheoremExplainBench | Krippendorff α 0.31–0.56 |
| 3D 资产 | Eval3D | 审美维度两两一致 83.8% |
| 视频 | VADB / VideoScore | α 0.54–0.66 / Visual Quality Fleiss κ 0.088 |
| T2I 图像（对照） | HPDv2 / ImageReward | 单人–单人 78.1% / 65.3% |

- 规律：问「有没有缺陷」「技术质量」时一致度高，问「偏好」「配色」时低
  - TASTE 和 VADB 里色彩都是最低维度
- 视频的审美分被技术质量污染：DIVIDE-3k 里审美分与技术分的 SROCC 为 **0.8752**；拟合总分的最优权重是技术 0.572、审美 0.428 ([DOVER](https://arxiv.org/abs/2211.04894))
- 3D 的人类偏好有系统偏向：带纹理比无纹理高 **144.1 Elo**；从业者口头重视拓扑，投票却偏向视觉冲击 ([3D Arena](https://arxiv.org/abs/2506.18787))

### 3.5 对 verifier 一致性上限的含义

- **上限 1：verifier 与单个评委的一致不可能显著超过人–人一致**〔推断〕
  - 设计类产物约 55–62%
  - 通用图像约 65–78%
- **上限 2：预测「多数票」可以高出单人–单人约 7 点**
  - 依据：HPSv2 单人–单人 78.1%，单人–均值 85.0% ([HPSv2](https://arxiv.org/html/2306.09341))
  - 只在人群确实有共识的对子上成立
- **上限 3：与个体的相关最多约等于 taste typicality**〔推断〕
  - 场景约 0.66、风景约 0.60，人造物更低
- **天花板不是固定的**
  - WebDevJudge 里，同一批人有了 rubric，一致率从 65% 到 92%。相当一部分「主观分歧」其实是**判据没说清楚**，不是口味不同〔推断〕
  - 所以先用 rubric 拉齐标注员，再用拉齐后的标注测 VLM
- **考核要按共识度分层**〔推断〕
  - 高共识对子（质量差大、缺陷明显）：目标 ≥80–85%
  - 低共识对子（风格取向）：只报不考核。TASTE 上所有模型在这类对子上都接近随机（0.50–0.54）
- **共识本身有副作用**〔推断〕
  - 群体最喜欢「低复杂度 + 高原型性」，对平均人优化必然把输出推向原型，也就是模板化、AI 味
  - 风格类条目必须单独处理（见 §4）

---

## 4 落到本项目：四层判定、三份 rubric、一套协议

### 4.1 判定架构

- **L0 程序硬闸**（P，一票否决，不进 VLM）
  - 溢出 / 遮挡 / 对比度 / 拓扑 / 穿插 / 闪烁 / 卡顿
  - **防刷分负向闸**：prompt 原文被渲染成大字、全局描边 / 边框 / 黑边、重复装饰堆叠
  - 依据：FRAME 加 bbox 使 GPT-4o 分数 +80.2%；项目里把 reward 换成整体审美分后，输出长度变为 21 倍、堆满描边〔项目已有，RULER 实验 ([arXiv](https://arxiv.org/abs/2609.25270))〕
- **L1 程序区间分**（P，区间题 ⇔，不单调）
  - 行长、行高、密度、曝光、色数
  - 配反塌缩下界：文本节点数、ink 下界
- **L2 VLM 逐条二值**（P+V / V 中的可观察项）
  - 程序结果作为「已验证事实」写进 prompt，VLM 不重判
- **L3 VLM 两两偏好**（◇ 风格项）
  - 只在 L0 全过的同组候选之间比较
  - 权重最低或只用来破平
- **为什么这样分**
  - VLM 判构图 / 层级 / 几何近乎随机（§2.2）
  - 程序把缺陷查出来再喂给 VLM，相关从 0.507 升到 0.843（VisEval）
  - SceneEval 明确只在「truly necessary」时用 VLM

### 4.2 Web / 2D rubric

#### 4.2.1 通用核心 W

适用范围：

- 网页：用全部条目
- PPT：W01–W03、W09–W20
- 图表：W01、W14–W17、W19
- Manim 关键帧：W01、W14、W16、W19

「查」列里的反引号名是项目已有的程序判据；「新增」是要补写的程序判据。

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| W01 | 层级：标题字号 / 字重单调递减，一眼分得出 ≥3 级；全页只有一个最显著元素 | P+V（P `hier`；V 判视觉主次） | NN/g #8；VisAWI「easy to grasp」；SlideAudit Lack of Visual Hierarchy |
| W02 | 字号来自有限尺度：种类 ≤ ~10，相邻比例大致恒定 | P `scale` | Bringhurst 3.1.1 |
| W03 | 字体族 ≤2；有 2 个时，标题 / 正文分工明确且风格明显不同 | P+V `family` | OpenAI ≤2 typefaces；Anthropic skill |
| W04 ⇔ | 正文行长 45–80 字符（上限 90） | P `len` | Butterick；WCAG 1.4.8 |
| W05 ⇔ | 正文行高在区间内（文献 1.2–1.5；项目实测 1.35–1.8〔项目已有〕） | P `lh` | Butterick；WCAG 1.4.8 |
| W06 | 正文 ≥16px（网页）；PPT 见 S04 | P 新增 | Butterick 15–25px |
| W07 | 全大写只用于单行短标签，且有 5–12% 正字距；小写文本无负字距 | P 新增 | Butterick；Bringhurst 2.1.6 / 2.1.7 |
| W08 | 多行正文不居中；两端对齐时开连字符 | P 新增 | Butterick；WCAG 1.4.8 |
| W09 | 间距有基数：≥70% 的 margin / padding / gap 是某个基数（2/4/8）的倍数 | P `spacing`（70% 为〔推断阈值〕） | Material 8dp / 4dp；Bringhurst 2.2.2 |
| W10 | 亲密性：区块标题离下方内容比离上方区块近；组内间距 < 组间间距 | P+V 新增 | Williams Proximity；VisAWI「well structured」 |
| W11 | 主要内容块的左边缘落在少数几条纵线上，无肉眼可见的错位 | P+V（P 出候选；`grid` 对齐率可被刷满，已作废当闸〔项目已有〕；V 要看高分辨率局部裁图） | Williams Alignment；Haraguchi：小幅对齐扰动 GPT-4o 判不出 |
| W12 ⇔ | 密度在区间内：既没有大片空白，也不过密 | P+V `ink`（0.06–0.78〔项目已有〕） | VisAWI「too dense (r)」；Reinecke 倒 U |
| W13 | 同类组件（卡片 / 按钮 / 输入框）的圆角、阴影、边框、内边距一致 | P+V（`radius` 扩展为同类组件样式离散度） | Williams Repetition；VisAWI「appears patchy (r)」 |
| W14 | 工艺底线：无文字溢出 / 截断、无元素遮挡、无横向滚动；375 与 1440 两个宽度下都成立 | P 新增（L0） | VisEval 浏览器测量准确率 100%；SlideAudit Occluded 15.5% |
| W15 | 对比度：文本 ≥4.5:1（大字 ≥3:1）；按钮边界、图标、输入框边框 ≥3:1 | P `contrast` + 非文本部分新增（L0） | WCAG 1.4.3 / 1.4.11 |
| W16 | 配色克制：色相家族 ≤3；只有一种强调色，且只用在主操作或关键信息上 | P+V `hue` | OpenAI one accent；VisAWI Colorfulness |
| W17 ◇ | 配色不打架：无刺眼的互补色贴邻，底色与前景协调 | V，最低权重 | VisAWI「colors do not match (r)」；TASTE Color Harmony τ 0.103 |
| W18 | 焦点唯一：首屏 / 每页一个主视觉焦点、一个主 CTA，没有多个等权重元素抢注意力 | P+V（P 数 CTA） | NN/g #8；OpenAI one primary CTA；Duarte Glance Test |
| W19 | 无无信息量装饰：去掉任一处描边 / 阴影 / 渐变 / 编号 / 卡片都不影响理解；无点名的 AI 默认样式 | V | Anthropic skill；NN/g #8；Mayer coherence |
| W20 ◇ | 有与主题相关的视觉身份，不是通用模板 | V，最低权重 | Lavie & Tractinsky expressive；VisAWI Diversity |

#### 4.2.2 PPT 附加 S

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| S01 | 3 秒要点：只看 3 秒（或只看低分辨率缩略图）就能复述唯一主旨，且与标题一致 | V | Duarte Glance Test |
| S02 | 一页一意：标题是一句断言，正文全部服务于它 | V | Duarte「single, precise point」 |
| S03 | 文本密度：正文 ≤80 字（中文）/ ≤40 词（英文），bullet ≤6 条 | P（阈值〔推断〕） | SlideAudit Excessive Text Density |
| S04 | 字号：正文 ≥18pt（严格档 24pt），标题 ≥28pt | P | Kawasaki〔二手〕；SlideAudit Inappropriate Font Sizing |
| S05 | 不出页、无非预期遮挡：所有 bbox 都在画布内；文本框不溢出；文字–文字、文字–图片 IoU = 0（背景层除外） | P（L0）；是否有意叠放交 V | SlidesBench Layout；SlideAudit Occluded 15.5% |
| S06 | 边距：四边留白 ≥ 画布宽 5%，左右差 ≤2% | P（阈值〔推断〕） | SlidesBench「sufficient margins」 |
| S07 | 跨页一致：同一角色（标题 / 正文 / 注释）样式跨页相同，主色跨页一致 | P | SlideAudit Inconsistent Visual Style |
| S08 | 图片保持宽高比（误差 ≤2%），源分辨率 ≥ 显示尺寸，且与本页文字相关 | P+V | SlidesBench Image；PPTEval Content |
| S09（整套） | 只读标题串就能连成一条论证线；有开头和结论页 | V（纯文本 LLM 也可） | PPTEval Coherence，VLM–人 Pearson 0.55，最弱 |

#### 4.2.3 图表附加 C

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| C01 | 主量化变量用 position / length 编码；饼图只用于部分-整体关系且 ≤5 个扇区 | P（读 spec 的 encoding / mark） | Cleveland–McGill；Munzner |
| C02 | 表达性：类别字段不映射到有序 channel；有序 / 量化字段不只靠 hue 区分 | P | Munzner expressiveness；Draco hard constraints |
| C03 | bar / area 的数值轴包含 0 | P | VisJudge Fidelity「truncated baselines」 |
| C04 | 图形面积按数值面积缩放（lie factor ≈1）；非对数轴等距 | P | Tufte（阈值〔未核实〕） |
| C05 | 2D 数据不用 3D 柱 / 饼或透视 | P（+V 兜底） | VisJudge Fidelity |
| C06 | 类别色 ≤8，超过就分组或改用 small multiples | P（8 为〔推断阈值〕） | ColorBrewer 上限〔未核实〕 |
| C07 | 色板类型匹配数据（有序→sequential，有中点→diverging，类别→qualitative）；模拟色盲后相邻类别仍可区分 | P | Munzner；ColorBrewer〔未核实〕 |
| C08 | tick label / legend / 标注 / 标题的 bbox 两两不交，且都在画布内 | P（L0） | VisEval layout check 准确率 100% |
| C09 | 刻度合理：tick 数 ≤ ~10；年份不显示小数；大数有千分位或单位缩写；不无故倒置坐标 | P | VisEval scale & ticks 准确率 99% |
| C10 | 标注完备：有标题；坐标轴有名称和单位；≥2 个颜色系列时有 legend 或直接标注 | P | VisEval；MatPlotAgent |
| C11 | 数据保真：数值、顺序、图表类型与源数据 / 查询一致 | P | VisEval legality；ChartMimic |
| C12 | 无 chartjunk：无背景图、装饰阴影 / 渐变；网格线浅色或省略 | P+V | Tufte data-ink |
| C13 | 关键洞察一眼可见：主趋势 / 极值能被识别；要强调的系列高亮，其余降饱和 | V | VisJudge Insight Discovery |
| C14 ◇ | 构图与配色：留白均衡，legend 不挤占数据区，配色协调 | V | VisJudge Aesthetics（VLM 最弱的子维度） |

#### 4.2.4 Manim 附加 M

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| M01 | 每个 play 的结束帧上，Text / MathTex 的 bbox 两两不交 | P（L0） | TEB Element Layout；Code2Video critic |
| M02 | 所有可见 mobject 在画框内，四边留出 ≥5% 安全边距 | P（L0） | Code2Video 6×6 anchor |
| M03 | 无大面积空白失衡：6×6 栅格里，有内容的格子不全挤在一侧 | P | Code2Video critic |
| M04 | 讲稿–画面同步：旁白提到某对象后 ±1s 内，该对象出现或被高亮 | P（TTS 时间戳 + 动画时间线） | Mayer temporal contiguity，d = 1.30 |
| M05 | 解释性 label 到目标 mobject 的距离 < 画框宽 10% | P（阈值〔推断〕） | Mayer spatial contiguity |
| M06 | 屏幕文字不照抄同时段旁白（字幕轨除外） | P | Mayer redundancy |
| M07 | 新引入的关键项有 Indicate / Circumscribe / 变色等信号 | P+V | Mayer signaling |
| M08 | 每个概念步骤后 wait ≥0.5s；单个 Scene 只讲一个子概念 | P（阈值〔推断〕） | Mayer segmenting |
| M09 | 位移 / 缩放不用 linear rate_func（连续旋转、曲线描绘除外）；入场减速、离场加速 | P | Material easing |
| M10 | 时长随运动范围增大；文字停留时间 ≥ 阅读时间 | P（阅读速度阈值〔推断〕） | Material duration 规则 |
| M11 | 同一时刻独立运动的对象组 ≤2（LaggedStart 编组算一组） | P+V | Disney staging〔未核实〕 |
| M12 | 跨场景风格一致：同一概念同一颜色，全片色板 ≤ ~5 色，字体统一 | P（视频 VLM 判这一项 ρ 仅 0.17） | TEB / Code2Video Visual Consistency |
| M13 | 关键帧确实在展示这一步的概念 / 推导，而不是装饰图 | V（VLM 最可靠的一维，ρ 0.72） | TEB Visual Relevance |
| M14 | 无无关装饰：没有与概念无关的图形、背景动效、花哨转场 | V | Mayer coherence |

### 4.3 3D rubric（Blender / three.js / CAD）

- **输入协议**（照搬已发表做法）
  - 4–9 视角 RGB + world-space normal 拼图，或 16 帧环绕视频（GPTEval3D、3DGen-Bench、Hi3DEval）
  - 至少一个能看清多数物体和空间关系的「comprehensive view」（BlenderGym）
  - 材质题加 2 盏点光 + 若干 HDRI 下的重打光图（Hi3DEval）；拓扑题加 wireframe 图（3D Arena）

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| D01 | 网格无非流形边、无非设计的边界洞、无翻转法线、无退化面 | P（L0） | Blender 3D Print Toolbox ([手册](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html))；项目雪人破洞〔项目已有〕 |
| D02 | 物体之间无穿插（允许 ≤ε 的接触），单物体无自相交 | P（L0） | SceneEval COL；3JSBench 穿插 20%〔项目已有〕 |
| D03 | 非悬挂物有支撑：最低点向下 raycast 到支撑面的距离 ≤ε | P（L0；支撑类型可交 V） | SceneEval SUP；BlenderGym「球卡在篮筐上」漏检 |
| D04 | 所有物体在地面 / 房间边界内 | P（L0） | LayoutGPT / SceneEval OOB |
| D05 | 无 z-fighting：没有共面重叠的异物面；固定相机连续帧无闪烁 | P（L0） | three.js polygonOffset / logarithmicDepthBuffer；3JSBench 闪烁 17%〔项目已有〕 |
| D06 | 主体完整入画：包围盒 8 个角点的投影都在 action-safe 框内；屏幕占比在 [10%, 70%] | P（占比〔推断阈值〕） | Blender Safe Areas |
| D07 | 曝光：主体 mask 内高光裁切 <1%、死黑 <5% | P（〔推断阈值〕） | Birn「uses all of the grays in between」 |
| D08 | PBR 取值：dielectric base color p1 ≥30、p99 ≤240 sRGB；metallic ≈0 或 ≥235；金属 base color ≥180 | P | Adobe PBR Guide |
| D09 | 有可辨认的主光：不只靠默认光或纯环境光；有一盏灯明显最亮、投主阴影 | P | Birn「Start in Darkness」 |
| D10 | 主辅光关系：主光 ≥2× 任一辅光；主光相对相机偏 15–45°、高 15–45°；有动机的逆光 / 夜景由 V 判是否例外 | P+V，软约束 | Birn 三点布光 + motivation |
| D11 | 主体与背景可分离：主体边界内外的亮度或色相差 ≥ 阈值（rim、背景明度、色温差任一即可） | P+V | Birn Rim |
| D12 | 灯光色温能归入 ≤2 组（如暖主光 + 冷补光），没有无动机的高饱和彩色灯 | P+V | Birn Kelvin、consistent color scheme |
| D13 | 纹理贴合几何：texel density 离散度低，无明显拉伸 / 接缝；纹理特征落在合理部位 | P+V（阈值无文献） | GPTEval3D Texture–geometry coherency；Hi3DEval |
| D14 ◇ | 主体投影重心落在三分 / 黄金比交点附近，或明显有意居中（±5% 画幅） | P 弱信号 + V | Blender Composition Guides |
| D15 | 多视角一致、几何可信：无 Janus、无漂浮碎片，细节是有意的而不是噪声（看 RGB + 法线拼图） | V（+P 多视角特征方差），低权重 | GPTEval3D；Eval3D 中 GPT-4V 几何仅 46.9% |
| D16 ◇ | 空间层次：≥2 个深度层，或用大气透视 / 明度递减 / 尺度递减区分远近 | V（+P 深度缓冲分层） | SceneCraft Scaling；Birn Ch4〔未核实细节〕 |
| D17 ◇ | 配色克制：主色在一个受限色域内，高饱和色只作点缀 | V（+P 色相统计） | Gurney gamut masking；Hi3DEval Colorfulness |
| D18 ◇ | 材质可信：多种光照下，高光、粗糙度、金属感像 prompt 描述的材料 | V | Hi3DEval Material Plausibility |
| D19（CAD） | 主曲面过渡 ≥G1，主要 A 面达到 G2，zebra 条纹跨缝不断不折；没有无功能的装饰件 | P（GCon）+ V（zebra 图、Rams） | Rhino GCon；Rams |
| D20 ◇ | 整体：如果只能放一张进作品集，选哪个 | V | Eval3D 审美维度 85.6% |

- 拓扑、可编辑性只能靠 D01–D05 兜住；人类偏好偏重纹理，VLM judge 会继承这一点（3D Arena +144.1 Elo）

### 4.4 Video rubric（网页 / Blender 渲染短片）

| ID | 条目（是 = 通过） | 查 | 依据 |
|---|---|---|---|
| V01 | 无闪烁：静止区域相邻帧 MAE 无尖峰，无整帧亮度跳变 | P（L0） | VBench Temporal Flickering ([arXiv](https://arxiv.org/html/2311.17982))；DOVER 失真 |
| V02 | 无卡顿：意图运动段内无连续重复帧 | P（L0） | DOVER stall |
| V03 | 运动平滑：插帧重建误差低于阈值，无 jitter | P（L0） | VBench Motion Smoothness |
| V04 | 曝光：每帧直方图两端的裁切像素 <2%（网页纯白底豁免） | P（〔推断阈值〕） | DOVER over / under-exposure |
| V05 | 清晰无伪影：无锯齿、无文字模糊、无 Cycles firefly | P+V | VBench Imaging Quality；DOVER |
| V06 | 不是静图：最大 5% 光流的均值超过阈值 | P（L0） | VBench Dynamic Degree |
| V07 | 每个关键帧的主体能用一句话指认，显著性峰值落在它上面 | V（+P 显著性图） | VADB Composition；VideoAesBench visual subject |
| V08 | 关键元素不被画框意外裁切；人物有 headroom（大特写豁免）；网页元素在安全区内 | P（DOM bbox / bpy 投影） | Bowen Headroom p.25 |
| V09 | 有方向性运动的主体，前方留白 ≥ 后方 | P（bbox + 运动方向） | Bowen Look Room p.28 |
| V10 ◇ | 主体质心落在三分线附近，或明显有意居中 | P 弱信号 + V | Bowen Rule of Thirds p.30 |
| V11 | 镜头运动能归为一个明确原语（pan / tilt / dolly / truck / arc / zoom / static），且与 brief 一致 | **P（读相机 F-curve / CSS transform），不用 V** | CameraBench taxonomy；ShotBench 中 GPT-4o 认镜头运动 48.3% |
| V12 | 同一时刻运动焦点 ≤1，次要元素的运动幅度明显小于主体 | P（光流分区统计）+ V | Murch eye-trace；Block movement |
| V13 | 位移 / 缩放用非线性缓动；时长随运动范围增大 | P | Material motion |
| V14（多镜头） | 镜头时长序列有节奏规律，或与音乐节拍对齐 | P+V | Murch Rhythm；Bordwell rhythmic relations |
| V15（多镜头） | 不越轴：跨切点时，运动主体的 screen direction 一致 | P（相机相对动作轴的位置） | Bowen 180° p.102 |
| V16（多镜头） | 无意外 jump cut：同一主体相邻镜头的机位角差 ≥30°，或景别明显变化 | P（相机位姿差） | Bowen 30° p.106 |
| V17（多镜头） | 切点前后两帧的显著性质心距离小，或有意引导视线 | P（无前人验证） | Murch Eye-trace |
| V18 ◇ | 色彩统一：主色调数量有限，全片一致，无干扰性偏色 | P（k-means 色相）+ V | VADB Color（人–人 α 0.54，最低） |
| V19 ◇ | 强度曲线有设计：tone / color / motion 的对比随时间有起有收，不是全程平 | P（逐帧强度曲线）+ V 判意图（无前人验证） | Block Contrast & Affinity |
| V20 ◇ | 整体：哪一段更想看完（情感 / 故事） | V，只用来破平 | Murch Emotion + Story；VideoAesBench 中 LMM 在 affectiveness 类最弱 |

- L0 先门控：审美分与技术分 SROCC 0.8752，不先门控，审美判断会被模糊 / 闪烁带着走（DIVIDE-3k）
- 镜头运动、焦距这类 VLM 认不准的条目（ShotBench 约 50%，CineTechBench 中 Zoom 14.29%），一律读代码
- 两两比较打平时，按 Murch 排序破平：rhythm > eye-trace > 2D 平面 > 3D 空间

### 4.5 推荐评判协议

| 决策 | 推荐 | 依据（指标） |
|---|---|---|
| 判定形式 | P 条目逐个判；V 条目只做同组两两比较，不打绝对分 | GenArena Spearman 0.36→0.86；AesBench 中 GPT-4V 打分档准确率 50.86%（随机 33.33%），感知题 72.08%；WebDevJudge pairwise 比单点打分高约 8 点 |
| 选项 | 强制二选一，不给「平」；平局只在 AB / BA 结论不一致时产生 | GenArena：可区分对子上允许 tie 54.9%，强制选择 83.9% |
| 量程 | 二值；如果要训打分头，用 Q-Align 式 5 档文字等级 + 概率加权，不用 Likert 回归 | CheckEval judge 间 α 0.06–0.09→0.45–0.48；DesignPref 4 档 α 0.104 < 二元 0.248〔项目已有〕；Q-Align 跨数据集 (SRCC+PLCC)/2 平均提升约 10% |
| 条目数 | 每个 prompt 放 5–10 条 V 条目，一次只问一条或一组同类；P 条目不限，进门控；全局 checklist 到几十条时，用人标对子学权重 | ARR K=5；HealthBench 平均每例约 9.7 条〔本文计算，48,562 条 / 5,000 段 ([HealthBench](https://arxiv.org/abs/2505.08775))〕；VisionReward 训练对 200→4k，准确率 77.6→81.3；按「有用性」人工加权比不加权还差〔项目已有〕 |
| 参考样例 | 每个领域给 1 对正反样例（同 brief、视觉相似），各附一句理由；不要把参考图当相似度目标 | ARR + guide：位置差 30–35→9–10 点；UICrit 按视觉相似挑例最好；RaR：参考图当比较目标 31.7% < 无参考 rubric 32.0% < 用参考生成 rubric 35.9%〔项目已有〕 |
| 顺序 | AB 与 BA 各判一次，不一致记平；3D 再换视角排布 / 种子判 ≥2 次，取多数 | 基础 VLM 正反序准确率差 30–35 点（ARR）；WebDevJudge 中 GPT-4.1 偏向第二位 15.8%；GPTEval3D 集成 |
| 推理 | 每条先写 ≤1 句可观察证据（指出位置），再给结论；不做长 CoT 后给总分 | MLLM-as-a-Judge：3-step CoT 让 Pearson 0.557→0.299；FRAME：CoT 放大 bbox 偏差 |
| 输入 | 截图 + 源码摘要 + 程序结果；3D 给多视角 RGB + 法线；视频给关键帧 + 程序曲线 | WebDevJudge：只给截图 59.5–62.1%，只给代码 64.5–69.6%，两者都给最好 70.34%；VisEval 0.507→0.843 |
| judge | 与 policy 不同家族；至少两家交叉 | VLM 自偏好没有定量数据〔推断〕；强弱 judge 混合投票不能稳定提升 ([ICLR 2025](https://arxiv.org/abs/2503.05977v1)) |
| 考核 | 按人类共识度分层：高共识子集目标 ≥80%；风格子集只报不考核 | TASTE 上所有模型 0.50–0.54；DesignPref 28.5% 对子分歧率 ≥96%〔项目已有〕 |

### 4.6 可直接使用的 prompt 模板（以 Web 为例）

前提：A 和 B 都已通过 L0。程序结果只放 L1 的数值，并标为已验证事实。

```text
[角色] 你是视觉设计评审。只判下面列出的条目；每条只看一个可观察事实，不评价其他方面。
[已验证事实，不要重判]
  A：正文行长 62 字符；行高 1.6；最低文本对比 4.8:1；强调色出现在 1 个元素上
  B：正文行长 88 字符（超出 45–80 区间）；行高 1.4；最低文本对比 5.2:1；强调色出现在 5 个元素上
[参考样例]
  正例 <图>；反例 <图>
  理由：反例同一强调色用在了 5 个元素上，看不出主操作
[输入]
  图 A <截图>   源码摘要 A <关键 CSS>
  图 B <截图>   源码摘要 B <关键 CSS>
[条目] 对每一条：先写 ≤1 句证据并指出位置，再选 A 或 B。必须二选一。
  W01 哪一页的主次更一眼可辨：标题、主视觉、正文三级分得开？
  W10 哪一页的分组更清楚：组内元素比组与组之间更紧？
  W16 哪一页的强调色更少，而且只落在主操作或关键信息上？
  W18 哪一页的首屏更一眼知道该看哪、该点哪？
  W19 哪一页没有无信息量的装饰（去掉后不影响理解的描边、阴影、渐变、编号）？
[输出] 只输出 JSON：{"W01":{"evidence":"…","winner":"A"}, "W10":{…}, …}
```

- 同一请求把 A / B 互换再跑一次；两次一致才记胜负，不一致记平
- ◇ 条目（W17、W20）单独一轮，结果只用于破平
- 3D 换成 D10–D20、输入换成多视角拼图；视频换成 V07–V20 中的 V 条目、输入换成关键帧 + 程序强度曲线

### 4.7 上线前必须补的验证

- 所有阈值都是占位，要在项目的改坏 / 换写法样本上标定后冻结
- 新增程序判据要先测判别力：W06–W08、W10、W14、W15 非文本部分，D11–D13，V17、V19
- 自建小规模人标集
  - 每对多人标注，按共识度分层
  - 分别在 rubric 前、rubric 后各标一次，量出「判据未定义」带来的分歧有多大
- 补上文献里缺的受控实验：同一 VLM、同一批产物，「逐条 rubric + pairwise」vs「整体 pairwise」vs「整体打分」

---

## 结论

「主观」不是铁板一块。WebDevJudge 里，同一批标注员有了 rubric 后，一致率从 65% 升到 92%，说明相当一部分审美分歧来自「没说清在判什么」，而不是口味差异。所以 rubric 的第一个用户是标注员，第二个才是 VLM。先拉齐人、再测 VLM，能测到的天花板比 α 0.2–0.4 显示的高。剩下真正的口味差异，主要是配色偏好和极简 / 繁复取向，不该进 reward。VLM 在这套系统里的位置也就清楚了：它不是审美专家，而是在程序已证明无缺陷的候选之间做受限比较。一致性主要由评判形式决定（两两比较、强制选择、正反各判一次、参考样例），条目写得多精彩是次要的。

把共识做成 reward 有一个结构性副作用。群体最一致的偏好是「低复杂度 + 高原型性」，对平均人优化就会把输出推向原型，也就是项目担心的模板化和 AI 味。共识越强，这种同质化压力越大。因此 verifier 要拆成两条线：共识线（L0–L2：程序门控 + 高共识 V 条目）可以放心强优化；风格线（W17、W20、D14–D20 中的 ◇ 条目、V18–V20）只用于两两破平，权重最低，必要时还要配多样性约束。

