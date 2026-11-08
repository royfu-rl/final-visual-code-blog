# Web / UI 审美 rubric 调研：经典书目 → 心理测量量表 → 计算指标 → VLM 评测 → 候选 rubric

> 截至 2026-11。数字均从一手 PDF / arXiv HTML 摘出，摘不到的单列在 Gaps。
> 项目已有 11 条程序判据（`hier / scale / family / lh / len / hue / contrast / spacing / ink / radius / grid`）不重推，只在第 5 节做映射。

---

## Q1 经典书目与设计规范给了哪些「可量化」的规则

### Takeaway
真正能落成数字的规则集中在排版（行长、行高、字号、字距）、间距网格（4/8 基数）和对比度（WCAG）三块。版式类原则（CRAP、Gestalt、栅格）只能写成「可观察的是/否」问句，量不出单一阈值；配色和谐（Albers）几乎只能靠像素判断。

### Cited Findings

**1. 排版：Bringhurst / Butterick / WCAG（数字最硬的一块）**
- Bringhurst《The Elements of Typographic Style》的规则编号与标题（网页版对照表）— [webtypography.net TOC](https://webtypography.net/toc)
  - 2.1.2 "Choose a comfortable measure"（行长）
  - 2.1.6 "Letterspace all strings of capitals and small caps, and all long strings of digits"
  - 2.1.7 "Don't letterspace the lower case without a reason"
  - 2.1.3 "Set ragged if ragged setting suits the text and page"
  - 2.2.1 "Choose a basic leading that suits the typeface, text and measure"
  - 2.2.2 "Add and delete vertical space in measured intervals"（纵向节奏）
  - 3.1.1 "Don't compose without a scale"（字号必须来自尺度）
- Butterick《Practical Typography》"Summary of key rules"（数字原文）— [practicaltypography.com](https://practicaltypography.com/summary-of-key-rules.html)
  - 正文字号：印刷 10–12 pt，网页 **15–25 px**
  - 行距：字号的 **120–145%**
  - 平均行长：**45–90 字符**（含空格）
  - 全大写只用于不到一行的文本；全大写和小型大写加 **5–12%** 字距
  - 居中少用；两端对齐必须开连字符
  - 粗体/斜体尽量少用，且不能同时用；除链接外不加下划线
  - 段落要么首行缩进（1–4 倍字号），要么段间距（4–10 pt），不能两者都用
- Anthropic `frontend-design` skill（2026-11 抓取的当前版本）— [SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md)
  - 字体：一个字体家族，或两个明显不同的家族，并有清晰的字号尺度
  - 行长控制在约 **80 字符**以内；衬线正文可以稍长，但行高要比无衬线略大
  - 不用单词式标题强调、全大写小标签、内容上方多余的标签

**2. 间距与栅格：Material / Müller-Brockmann / Refactoring UI**
- Material Design "Spacing methods" — [material.io](https://material.io/design/layout/spacing-methods.html)
  - 组件排在 **8dp** 方形基线网格上，padding 按 8dp 或 4dp 递增
  - 图标、文字、组件局部可以用 **4dp** 网格；文字对齐 4dp 基线，但在按钮、列表项里居中时可以离网
- Müller-Brockmann《Grid Systems in Graphic Design》— [书商页](https://abbeys.com.au/book/grid-systems-in-graphic-design.do)；[二手综述](https://madegooddesigns.com/grid-systems/)
  - 书商页：覆盖 **8 到 32 个 grid field** 的栅格系统
  - 二手综述：内容放进栏中，栏数决定灵活度；页边距框住版面
  - 出版年说法冲突：多数书商写 1981（Niggli 版），一篇综述写 1961
- Refactoring UI（Wathan & Schoger）— [第三方 wiki](https://github.com/s0xDk/refactoring-ui-skill/wiki)、[DEV 书评](https://dev.to/updivision/book-review-refactoring-ui-by-adam-wathan-steve-schoger-2f7m)（**都是二手**）
  - 层级优先用字重和颜色，而不只是字号
  - 间距从一个基数出发，按倍数建尺度，例如 4/8/12/16/24/32/48/64/96；先给太多留白，再往回收
  - 字号用有限集合，例如 12/14/16/18/20/24/30/36/48/60/72 px

**3. 对比度与无障碍：WCAG / Apple HIG（W3C 原文，本次未重新抓取）**
- WCAG 2.2 SC 1.4.3：正文 **4.5:1**，大字（≥18pt，或 ≥14pt 粗体）**3:1** — [W3C Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- SC 1.4.6（AAA）：**7:1** — [W3C 1.4.6](https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html)
- SC 1.4.11：非文本 UI 组件与图形对象 **3:1** — [W3C 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- SC 1.4.8（AAA）：行宽 ≤ **80 字符**，段内行距 ≥ **1.5**，段间距 ≥ 行距的 1.5 倍，不两端对齐 — [W3C 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)
- SC 1.4.12：用户把行高调到 1.5、段距调到 2 倍、字距 0.12em、词距 0.16em 时内容不能丢失 — [W3C 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)
- Apple HIG：按钮可点区域至少 **44×44 pt**（visionOS 为 60×60 pt），这条是开发者论坛转引 HIG 的原话 — [Apple Developer Forums](https://developer.apple.com/forums/thread/739201)
  - 默认正文 17pt、最小 11pt 只在第三方摘要里出现，见 Gaps

**4. 版式原则：Williams CRAP / Gestalt / Nielsen #8**
- Williams《The Non-Designer's Design Book》的四原则：Contrast、Repetition、Alignment、Proximity（CRAP）— [visualcommunicationguy 书评](https://thevisualcommunicationguy.com/2013/05/15/the-non-designers-design-book/)；[Pearson 第 4 版](https://pearson.com/us/higher-education/program/Williams-Non-Designer-s-Design-Book-The-4th-Edition/PGM240391.html)
  - UIClip 拿 CRAP 当合成缺陷的理论来源，并把一段 CRAP 描述同时给了人类设计师和 GPT-4V — [UIClip](https://arxiv.org/html/2404.12500v1)
- Gestalt：VisAWI 的 Simplicity 维度明确写成 Gestalt 的 figural goodness（unity、homogeneity、clarity、orderliness、balance，引 Arnheim 1974）— [Moshagen & Thielsch 2010 草稿 §4.1.1](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf)
- Nielsen heuristic #8 "Aesthetic and minimalist design"（Fessenden，2021-01-24）— [NN/g](https://www.nngroup.com/articles/aesthetic-minimalist-design/)
  - 定义原文："Interfaces should not contain information which is irrelevant or rarely needed"，每个多余元素都会和有用信息"compete"
  - 可执行部分
    - 提高信噪比：杂乱图片、无关细节、未解释的术语、纯装饰都算噪声
    - 用 "scale, visual hierarchy, balance, contrast, and Gestalt principles" 来传达
    - 少见功能做渐进披露；"Every piece of content should have a purpose, including negative space"
    - 可点和不可点的元素不要用同一种视觉处理；不要滥用字体和颜色变化

**5. 「反 AI 味」清单：Anthropic / OpenAI 一手**
- Anthropic `frontend-design` 当前版本的点名禁用项 — [SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md)
  - 配色：奶油底配赤陶色；近黑底配酸绿或朱红；带色偏的近黑（如 `#111`）
  - 版式：发丝线加密排多栏的「报纸风」；圆角相同、阴影统一、渐变洗底的「SaaS 卡片套件」
  - 编号、分隔线、标签必须承载真实信息；数字只用于真实的顺序
  - 动效只做一个编排好的时刻，不要每个区块都淡入、每张卡都有 hover
  - 质量底线：响应式、可见的 focus 状态、支持 reduced-motion、对比度达标、配色和谐
  - 生成前先起 **4–6 个命名颜色**的 token 系统
- 和项目已引的 Anthropic 博客有出入：博客点名 Inter 字体和白底紫渐变（[blog](https://claude.com/blog/improving-frontend-design-through-skills)，经 `parts/web/verifier.md` §3.3.2 转引），当前 SKILL.md 已经不提 Inter 和紫渐变，改成上面的清单 — [SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md)
- OpenAI GPT-5.4 前端指南给出的可计数约束：一个 H1、≤6 个 section、≤2 种字体、一个强调色、首屏只有一个主 CTA；letter-spacing 为 0 且不能为负；border-radius ≤ 8px — 转引自本项目 [`verifier_reward.md` §3.4](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)（原链 [OpenAI blog](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)）

### Inferences
- 能直接变成 DOM 阈值的规则
  - 行长 45–75（Bringhurst）/ 45–90（Butterick）/ ≤80（WCAG、Anthropic）
  - 行高 1.2–1.45（Butterick）/ ≥1.5（WCAG AAA）
  - 正文 ≥15–16px
  - 全大写加 5–12% 字距
  - 对比度 4.5 / 3 / 7
  - 点击区域 44pt
  - 间距基数 4/8
- 来源之间数字不一致（行长上限 75/80/90；行高 1.45 对 1.5）
  - 印证了项目的工程铁律：阈值要在参考页上反推，教条只能给初始区间
- CRAP、Gestalt、Nielsen #8 只能拆成可观察的子问题，比如「标题离下方正文比离上方区块近」，没有单一阈值

### Gaps
- 以下内容本次没有抓到一手页面，只凭书目常识，**未核实**，引用前要查原书
  - Bringhurst 2.1.2 的原文数字：「45–75 字符算满意，66 字符最理想」；多栏 40–50 字符
  - Bringhurst 3.1.1 的传统字号尺度（6/7/8/9/10/11/12/14/16/18/21/24/36/48/60/72）
  - Lupton《Thinking with Type》的 Letter / Text / Grid 三部分结构
  - Lidwell、Holden、Butler《Universal Principles of Design》里的 Aesthetic-Usability Effect、Signal-to-Noise Ratio、Alignment、Golden Ratio 等条目
  - Albers《Interaction of Color》的颜色相对性：同一颜色在不同底色上看起来不同（非数值规则）
  - Krug《Don't Make Me Think》第 3 章 "Billboard Design 101"：惯例、视觉层级、分区清晰、可点击物明显、降噪
- Apple HIG 的默认正文 17pt、最小 11pt：只见于第三方摘要，没在 developer.apple.com 原页核实
- Material 3 的具体 type scale token（如 Body Large 16/24）没抓到原页
- Refactoring UI 的具体数字全部来自二手摘要；书的原文（饱和度、灰阶的调法）没核实

---

## Q2 有哪些经过验证的网页审美量表，维度和信度数字是多少

### Takeaway
VisAWI 是唯一系统验证过、专门针对网页的多维量表：18 条目，4 个维度，α 在 .85–.94。但作者自己承认没有测重测信度，而且 Diversity 条目抽象到「无法指导设计」。Lavie & Tractinsky 的经典/表达二分（α .85–.87）是 VisAWI 的效标。首印象研究（Lindgaard、Tractinsky、Reinecke）证明 50–500ms 的判断稳定，其中视觉复杂度比色彩丰富度更关键，而且呈倒 U 形。

### Cited Findings

**1. VisAWI（Moshagen & Thielsch 2010, IJHCS 68(10):689–709）** — [作者草稿 PDF](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf)；[量表主页](https://aupsy.uni-wuppertal.de/en/instrumente/visawi/)
- 规模：七个研究，合计 **2,000 多名参与者、70 多个网站**
- 结构：18 条目，4 个一阶维度加 1 个二阶总因子；载荷 .63–.89，没有明显交叉载荷
- CFA 拟合（Table 3）
  - Study 3：CFI 0.951，RMSEA 0.065，SRMR 0.053
  - Study 4（N=512，42 个网站，9 类领域）：CFI 0.945，RMSEA 0.064，SRMR 0.052
- Cronbach's α（Table 5）
  - Simplicity **.89**
  - Diversity **.87**
  - Colorfulness **.89**
  - Craftsmanship **.85**
  - 总分 **.94**
  - 最差站与最好站的标准化差 d 在 1.86–2.57，说明区分力强
- 条目（英译，`(r)` 表示反向计分）
  - Simplicity
    - layout too dense (r)
    - easy to grasp
    - everything goes together
    - appears patchy (r)
    - well structured
  - Diversity
    - pleasantly varied
    - inventive
    - uninspired (r)
    - dynamic
    - uninteresting (r)
  - Colorfulness
    - color composition attractive
    - colors do not match (r)
    - choice of colors is botched (r)
    - colors are appealing
  - Craftsmanship
    - professionally designed
    - not up-to-date (r)
    - designed with care
    - lacks a concept (r)
- 效度（Study 5，N=512）
  - Simplicity 与 classical aesthetics 相关 **.82**
  - Diversity 与 expressive aesthetics 相关 **.80**
  - 总因子与 appeal 相关 .80，与感知可用性相关 .64
- 作者自述局限
  - **没有测重测信度**（"test-retest stability were not examined"）
  - Diversity 条目 "quite abstract and may be too general to guide designers"

**2. VisAWI-S（Moshagen & Thielsch 2013, BIT 32(12):1305–1311）** — [IDEAS/RePEc](https://ideas.repec.org/a/taf/tbitxx/v32y2013i12p1305-1311.html)
- 4 条目，每个维度 1 条；三个研究合计 **1,673 人**
- 摘要结论：单维、可靠，"good approximation" 全量表
- 一篇 2026 年的研究把 VisAWI-S 改成 10 点量表来用，α = .94。这是改编用法，不是原始数字 — [arXiv 2609.03918](https://arxiv.org/abs/2609.03918)

**3. Lavie & Tractinsky 2004（IJHCS 60(3):269–298）** — [作者 PDF](http://www.ise.bgu.ac.il/faculty/noam/papers/04_tl_nt_ijhcs.pdf)
- 四个研究的样本
  - S1：125 名工科生
  - S2：212 名
  - S3：145 名
  - S4：384 名普通网民，对半拆成两个各 192 人的子样本做交叉验证
- 两个维度，每维 5 条目
  - Classical：clean、clear、pleasant、symmetrical、aesthetic
  - Expressive：original、sophisticated、fascinating、creative、uses special effects
- α（Table 3，初始样本 / 交叉验证样本）
  - Classical **.85 / .86**
  - Expressive **.87 / .86**
- 相关
  - 两维之间 **r = .69 / .63**
  - Classical 与其他构念的相关一直偏高（0.60–0.78），Expressive 偏低（0.37–0.59）
  - 可用性与 classical 的相关明显高于与 expressive 的相关

**4. 首印象的稳定性**
- Lindgaard et al. 2006（BIT 25(2):115–126）— [Crossref](https://api.crossref.org/works/10.1080%2F01449290500330448)；[摘要](https://typeset.io/papers/attention-web-designers-you-have-50-milliseconds-to-make-a-3axej7ku89)
  - 三个研究：500ms 呈现、两轮评分；Study 3 加了 50ms 条件
  - 摘要原意：跨轮评分高度相关，50ms 与 500ms 之间也高度相关，结论是视觉吸引力 50ms 内就能判断
  - 具体 r 值见 Gaps
- Tractinsky et al. 2006（IJHCS）— [BGU 页](https://www.bgu.ac.il/researcher/noam-tractinsky/publications/349269701/)
  - 40 人评 50 个网页
  - 500ms 与 10s（另一来源说是不限时）的平均吸引力评分高度相关
  - 但个体差异和个体一致性差异都很大
- Reinecke et al. CHI 2013 — [PDF](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf)
  - 材料：450 个网站，548 名志愿者，**500ms** 呈现，9 点量表，两轮评分
  - 感知色彩丰富度模型（N=184）：R² = **.78**（adj .77）
    - 预测变量：Hasler-Süsstrunk colorfulness（β = .58）、若干颜色占比、饱和度、图像区域数、quadtree 叶数
  - 感知视觉复杂度模型（N=122）：R² = **.65**（adj .64）
    - Zheng 等人的 quadtree 叶数与感知复杂度只有 **r = .28**
    - 按空间分解得到的叶数 r = **.50**
  - 吸引力模型（N=242，34 个国家）：用 complexity 和 colorfulness 的二次项，加上人口学交互，**adj R² = .48**
    - 复杂度的作用远大于色彩丰富度，"inverted U-shape" / 中等复杂度最好
    - 年龄与复杂度强交互，教育程度与色彩丰富度交互
    - 连 Webby 获奖网站都被很多人讨厌
  - 重测：两轮评分差的标准差为 0.55（色彩）、0.63（复杂度）、0.5（吸引力）；吸引力实验剔除了 218/3630 对相差超过 2 分的评分
- Reinecke & Gajos 2014 "Quantifying Visual Preferences Around the World"：约 40,000 人评 430 张截图。这组数字来自搜索摘要，没打开原文 — [PDF](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf)

### Inferences
- VisAWI 的 4 维直接给出了 rubric 骨架
  - Simplicity（结构、密度、统一）和 Craftsmanship（专业、用心、有概念）最容易拆成可观察项
  - Colorfulness 有一半能量化（色相数、对比度），另一半（"colors do not match"）只能靠像素判断
  - Diversity 和 expressive 只适合 pairwise，绝对打分没有锚点
- 复杂度呈倒 U 形（Reinecke），色彩和密度有上下限（项目 `ink` 0.06–0.78）
  - 合起来看：「留白、密度、复杂度」类条目必须写成区间题（太空、太满都挂），不能写成「越简洁越好」
- 量表信度（α ≈ .85–.94）是同一个人对同一页、多条目之间的一致性，不是不同人之间的一致性
  - 跨人一致性见 Q4，Krippendorff α 只有 0.25–0.37。所以 rubric 可以用这些量表做维度定义，但不能指望单个评委的分数稳定

### Gaps
- VisAWI-S 的原始 α、与全量表的相关：只读到摘要，没拿到数字
- Lindgaard 2006 各研究的具体相关系数（常被转引成 r ≈ .9x）：没拿到原文，**未核实**
- Tractinsky 2006 的具体 r 值，以及第二阶段是 10s 还是不限时：两个来源冲突
- 没有找到任何 VisAWI 或 Lavie-Tractinsky 量表的重测信度数据（VisAWI 作者明说没做）
- 本次没找到把 VisAWI 条目直接喂给 VLM、再和人类 VisAWI 分对比的研究

---

## Q3 计算式 UI 审美指标有哪些，哪些可刷、和人相关弱

### Takeaway
经典几何指标（Ngo 的 14 项、quadtree 复杂度）和人的相关性弱，而且能单向推高。最好的组合模型（Miniukovich 8 项、Reinecke 复杂度 + 色彩）也只能解释约 50% 的方差，单项指标更差。这类指标只适合做诊断量或区间闸，不能做单调 reward。

### Cited Findings
- Ngo, Teo & Byrne 2003（Information Sciences 152:25–46）— [作者网页版](https://www.mi.sanu.ac.rs/vismath/ngo/index.html)；[MMU 仓储](https://shdl.mmu.edu.my/2562)
  - 14 项指标，每项归一到 0（最差）到 1（最好）
  - 名单：balance、equilibrium、symmetry、sequence、cohesion、unity、proportion、simplicity、density、regularity、economy、homogeneity、rhythm、order & complexity
- Miniukovich & De Angeli CHI 2015 "Computation of Interface Aesthetics"（Honorable Mention）— [UniTN 仓储](https://iris.unitn.it/handle/11572/116796)
  - 8 项自动指标
  - 最佳模型解释网页审美方差 **最高 49%**；iPhone app 加上 genre 后 **最高 32%**
- AIM：Aalto Interface Metrics（Oulasvirta et al., UIST'18 Adjunct, pp.16–19）— [PDF](https://acris.aalto.fi/ws/portalfiles/portal/30261274/ELEC_oulasvirta_et_al_2018_002_.pdf)
  - 输入 URL，提供 **17 项指标**，从 visual clutter 到 visual learnability；服务地址 interfacemetrics.aalto.fi
- Reinecke 2013：经典 quadtree 复杂度与人类感知复杂度只有 **r = .28** — [PDF](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf)
- 本项目已整理的反例（经 [`parts/web/verifier.md` §3.3.1](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/parts/web/verifier.md) 转引）
  - [Salimun 2013](https://theses.gla.ac.uk/4256)：72 人，指标最高的布局最不受欢迎，中等对称最受欢迎
  - [Purchase et al. 2011](https://eprints.gla.ac.uk/54578)：14 项指标用在真实网页上，只有 1 项和好看程度对得上
  - [Duan et al. CHI 2024](https://arxiv.org/abs/2403.13139)：设计越改越好，模型反馈准确率反而从 52% 降到 39%
  - 纯规则 lint 召回只有 22.9%–32.3%（DesignRepair 的 UIS-Hunter 基线）— [`verifier_reward.md` §1.1.4](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)
- 可刷性的直接证据
  - RULER（SVG）用 CLIP + aesthetic + HPS 当 reward：美学分 4.424 → 6.210，按检查项算的分 0.395 → 0.262，输出长度变成 21 倍，堆满描边和重复装饰 — [verifier.md §3.3.2](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/parts/web/verifier.md)（原链 [arXiv 2609.25270](https://arxiv.org/abs/2609.25270)）
  - 项目自己的 `grid` 对齐率：最糟的 A10（抹掉所有边距）对齐率反而是 1.000，所以已作废，不再当闸 — [`verifier_reward.md`](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)
- 相关但不是 VLM 方向：Wang et al. 2026 用答案集编程（ASP）优化对齐、分组、配色和谐、留白，用户评分高于随机和简单启发式 — [arXiv 2609.03918](https://arxiv.org/abs/2609.03918)

### Inferences
- 可刷形态按指标归类
  - symmetry、balance、economy、对齐率：空白单列页都能推到最优
  - simplicity / density：极简白页
  - colorfulness 下降：灰阶页
  - 这和项目 H12 的五种可刷形态一致
- 因此 rubric 里带这些指标的条目必须满足三点
  - 形式是区间或一票否决
  - 配一个反塌缩下界（文本节点数、内容覆盖率）
  - 配一个 VLM 的像素复核

### Gaps
- Ngo 2003 原文里和设计师评分的相关数据没拿到
- Miniukovich 8 项指标的具体名单、单项相关没拿到；AIM 17 项指标的逐项验证数据没拿到
- 没找到 AIM 指标与 VLM 评分的直接对比

---

## Q4 UI 审美的 LLM/VLM 评测数据集与 benchmark：给 rubric 有没有用

### Takeaway
目前没有任何一篇工作干净地证明「给 VLM 设计准则或 rubric 能显著提高它与设计师的一致性」。
- UICrit 把准则放进 prompt，但没做消融
- UIClip 里 GPT-4V 拿到了 CRAP 描述，仍然接近随机
- WebDevJudge 的结果最清楚：rubric 让**人类**标注一致率从 65.0% 涨到 92.0%，但对模型在 pairwise 下几乎没有增益；单点打分时二元 rubric 明显好过 Likert
- 真正有效的是 few-shot 示例、输入源码、做 pairwise

### Cited Findings

**1. UICrit（Duan et al., UIST 2024）** — [arXiv HTML v3](https://arxiv.org/html/2407.08850v3)
- 数据：**983** 个移动 UI，**3,059** 条批评，7 名设计师（1–16 年经验）
  - aesthetics / usability / design quality 用 10 点量表，learnability / efficiency 用 5 点量表，均值都接近 6.0
- prompt 里放了三套准则：NN/g 10 heuristics、CrowdCrit Visual Design Critiques、Apple HIG
  - **没有做有无准则的消融**
- 结果
  - 区域评论质量：zero-shot **0.24**；8-shot 随机 0.31；按语义相似选例 0.42；按视觉相似选例 **0.44**
  - 视觉提示的 bbox IoU：只给截图 0.004；加网格 1.1e-5；patches 0.222；坐标 0.186
  - 6 名专家的用户研究：zero-shot **0.31** → few-shot + 视觉提示 **0.48**（+0.17，p = 5e-4，即「55%」的相对提升）；人类设计师 **0.75**
  - 偏好：专家 67% 选 few-shot 而不是 zero-shot；81% 选人类而不是 few-shot
  - 评分者一致性：Fleiss κ 在 0.29–0.31（批评评分），排序偏好 0.55
- 本项目重算 UICrit：aesthetics ICC(1,1) = **+0.024**，组内 SD 1.00 ≈ 总 SD 1.02 — [`verifier_reward.md` §7.10](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)

**2. UIClip（Wu et al., UIST 2024）** — [arXiv HTML](https://arxiv.org/html/2404.12500v1)
- 数据
  - JitterWeb：**2.3M** 合成样本，约 30 万网页，按 CRAP 做了 9 类 jitter（换色、色噪、字号、文字噪声、文字色、背景色、间距、复杂度、布局），每页最多叠 3 个
  - BetterApp：12 名设计师，约 1,200 条评分，保留 892 对
  - 设计师间 **Krippendorff α = 0.37**
- pairwise 设计质量准确率
  - UIClip **75.12%**（检测网页缺陷 87.1%）
  - 只做 CLIP 预训练 65.42%
  - LLaVA 54.59%
  - **GPT-4V 51.58%**：prompt 里有和设计师一样的 CRAP 描述，结果仍接近随机，约 10% 直接拒答
- 真实 app 截图明显比合成截图难：UIClip 57.89% 对 67.65%

**3. DesignPref（Peng, Bigham, Wu, 2025）** — [arXiv](https://arxiv.org/abs/2511.20513)
- 20 名职业设计师，12k 对比较，二元偏好的 **Krippendorff α = 0.25**
- 个性化模型（微调或按设计师做 RAG）稳定优于聚合模型，且只用 1/20 的样本
- 项目笔记补充：600 对全员评、两两一致 0.624；聚合训练 57.45%，个性化 60.16% — [verifier.md §3.3.2](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/parts/web/verifier.md)

**4. WebDevJudge（Li et al., ICLR 2026）** — [arXiv HTML v2](https://arxiv.org/html/2510.18560v2)
- 数据：从 webdev-arena-preference-10k 筛到 **654** 例（269 A / 276 B / 109 平局），另有 WebDevJudge-Unit 502 例
- **rubric 对人类的效果**（Table 1，含平局）
  - 无 rubric：标注员间一致 **65.0%**，与原始标签一致 53.0%
  - 有 rubric：人写 rubric **92.0%**，LLM 生成 rubric 90.0%
  - 不含平局：91.3% → 95.5% / 95.1%
- 人类 pairwise 平均 84.56%
- 最佳模型
  - pairwise：GPT-4.1 **70.34%**，Claude-4-Sonnet 70.18%
  - 单点打分：Claude-3.7-Sonnet 63.91%
  - pairwise 平均比单点打分高约 8 个点
- **rubric 对模型的效果**
  - pairwise 下 Direct 提示与 rubric 引导 "comparably"，无增益
  - 单点打分下二元 rubric 明显好过多点 Likert
  - 推理模型用 Direct 更好
  - 逐模型的精确数字只在图 3，没拿到
- 输入模态（Table 4，pairwise）
  - 只给截图 59.5–62.1%
  - 只给代码 64.5–69.6%
  - 两者都给最好（如 GPT-4.1 70.34%）
  - 例外：Gemini-2.5-pro 只给图比只给代码好
- 位置偏差：一致性 83–90%；GPT-4.1 偏向第二个位置的比例是 15.8%，偏向第一个只有 0.9%

**5. ArtifactsBench（Tencent Hunyuan, 2025）** — [arXiv HTML v2](https://arxiv.org/html/2507.04952v2)；[GitHub](https://github.com/Tencent-Hunyuan/ArtifactsBenchmark)
- 1,825 个任务、9 个主题
- 每个任务都有一份 10 维 checklist，覆盖视觉、交互、代码；双评委 Gemini-2.5-Pro 和 Qwen2.5-VL-72B 看交互截图打分
- 与 WebDev Arena 的排名一致性 **94.4%**；280 例专家研究里 pairwise 一致率最高 **90.95%**
- 没找到 checklist 对比无 checklist 的消融

**6. Design2Code（Si et al., 2024）** — [arXiv](https://arxiv.org/abs/2403.03163v1)；[alphaXiv 概览](https://www.alphaxiv.org/overview/2403.03163)
- 484 个真实网页
- 人评：GPT-4V 生成页 **49%** 可以替代原页，**64%** 被认为好于原页
- 这两个数字来自镜像和概览页，PDF 原句没逐字核对

**7. 一手厂商做法（项目已有）**
- Anthropic harness 的四维 rubric（design quality / originality / craft / functionality）同时给 generator 和 evaluator
  - 每一维都有硬阈值，任一维不过就整体失败
  - craft 和 functionality 降权，理由是基线已经及格 — [`verifier_reward.md` §3.6](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)
- RULER：实例级 rubric 与人类 Spearman **0.7929**，标量 aesthetic 预测器 0.6051，CLIP 0.5518 — [`verifier_reward.md`](/mmu_mllm_hdd_4/deep-research/visual-coder-blog-v2/middle_processing/notes/verifier_reward.md)

### Inferences
- rubric 的价值可能主要在两处（推断）
  - 把**人类**标注拉齐，WebDevJudge：65% → 92%
  - 把单点打分改成二元逐项判断
  - 它不太能提升 VLM 在 pairwise 上的一致率
- 所以本 rubric 应该做成「逐项二元 + pairwise 汇总」，同时给源码和截图
- 每条只问一个可观察的事实，避免 Likert
- 评测协议里应该固定三件事
  - 交换 A/B 位置、各跑一次（位置偏差 1–16%）
  - 同时给截图和关键源码或 computed style
  - few-shot 示例按视觉相似度挑（UICrit 的最佳设置）
- 审美标注的跨人一致率上限（α 0.25–0.37）决定了：主观条目（和谐、原创）只能做 pairwise 或区间，不能当回归 reward

### Gaps
- WebDevJudge 逐模型 rubric 对比无 rubric 的精确数字（图 3）没拿到
- 没找到 UICrit 有无准则的消融
- 没找到 ArtifactsBench 有无 checklist 的消融
- WebDev Arena 本身的投票规模、平局率没查
- 没找到「把 VisAWI 或 Lavie 条目当 VLM rubric」的实证

---

## Q5 候选 rubric：单页（逐项二元）与 pairwise 版，及其与项目 11 条程序判据的映射

### Takeaway
下面给出 20 条可观察条目，分四组（排版 / 空间 / 颜色 / 整体）。
- 11 条已有判据能覆盖其中 11 条的「程序半边」
- **新增程序判据 7 条**：正文字号、大写字距、长段居中、亲密性间距、溢出/重叠、非文本对比、首屏 CTA 计数
- **纯 VLM 条目 3 条**：配色和谐、装饰无信息量、表达性/原创，且只建议走 pairwise

### Cited Findings
- 各条目的来源见下表的「来源」列，链接都在 Q1–Q4，这里不重复

### Inferences

**使用约定**
- 单页版：每条只答 `是 / 否 / 不适用`，不打 1–7 分（依据：WebDevJudge 二元好过 Likert）
- pairwise 版：每条答 `A 更好 / B 更好 / 平局`；A/B 交换后各跑一次，两次不一致就记为平局
- 区间题（标 ⇔）：太少、太多都判「否」，不能出现越多越好的单调分
- 「判定方式」列的含义
  - **P**：程序读 DOM、computed style 或几何就能判
  - **V**：只能 VLM 看像素判断
  - **P+V**：程序给数，VLM 复核视觉效果
- 「映射」列：写已有判据名，或写 **新增**

**A. 排版**

| # | 单页问句（是 = 通过） | pairwise 问句 | 来源 | 判定 | 映射 |
|---|---|---|---|---|---|
| R01 | 标题层级单调：h1 ≥ h2 ≥ … ≥ 正文，而且一眼能分出 ≥3 级（字号、字重或颜色有差） | 哪页的主次更一眼可辨 | Refactoring UI；NN/g #8；VisAWI「easy to grasp」 | P+V | `hier`（V 补「视觉主次」） |
| R02 | 字号来自有限尺度：种类 ≤ ~10，相邻比例大致恒定 | 哪页字号更像一套尺度 | Bringhurst 3.1.1；Refactoring UI | P | `scale` |
| R03 | 字体族 ≤2；如果有 2 个，两者角色分明（标题/正文），而且风格明显不同 | 哪页的字体搭配更有分工 | Anthropic skill；OpenAI「≤2 typefaces」 | P+V | `family`（V 补「是否明显不同」） |
| R04 | 正文行长 45–80 字符（上限 90） ⇔ | 哪页的正文更好读 | Bringhurst 2.1.2；Butterick；WCAG 1.4.8 | P | `len`（判别力未验证） |
| R05 | 正文行高在区间内（教条 1.2–1.5，项目实测 1.35–1.8） ⇔ | 同上 | Butterick；WCAG 1.4.8/1.4.12；Bringhurst 2.2.1 | P | `lh` |
| R06 | 正文字号 ≥ 15–16px（移动端 ≥16px） | 哪页的正文字号更舒适 | Butterick 15–25px；Material/Apple 默认正文 | P | **新增** |
| R07 | 全大写只用于单行短标签，且有正字距（约 5–12%）；小写正文没有负字距 | — | Butterick；Bringhurst 2.1.6/2.1.7；OpenAI letter-spacing ≥0 | P | **新增** |
| R08 | 多行正文段落不居中；两端对齐时开了连字符 | — | Butterick；Bringhurst 2.1.3；WCAG 1.4.8 | P | **新增** |

**B. 空间与结构**

| # | 单页问句 | pairwise 问句 | 来源 | 判定 | 映射 |
|---|---|---|---|---|---|
| R09 | 间距有节奏：存在一个基数（2/4/8），≥70% 的 margin/padding/gap 是它的倍数 | 哪页的间距更统一 | Material 8dp/4dp；Refactoring UI；Bringhurst 2.2.2 | P | `spacing`（基数自动选，不写死 4） |
| R10 | 亲密性：每个区块标题离下方内容的距离 < 离上方区块的距离；组内间距 < 组间间距 | 哪页的分组更清楚 | Williams Proximity；Gestalt；VisAWI「well structured」 | P+V | **新增**（几何可算） |
| R11 | 主要内容块的左边缘落在少数几条纵线上；没有肉眼可见的错位 | 哪页对齐更整齐 | Williams Alignment；Müller-Brockmann | V（P 只做诊断） | `grid`（已作废当闸，余量 0.058） |
| R12 | 密度在区间：既不是大片空白，也不过密 ⇔ | 哪页的疏密更合适 | VisAWI「too dense (r)」；Reinecke 倒 U；NN/g #8 | P+V | `ink`（0.06–0.78） |
| R13 | 同类组件（卡片、按钮、输入框）的圆角、阴影、边框、内边距一致 | 哪页的组件更像一套 | Williams Repetition；VisAWI「everything goes together」「patchy (r)」 | P+V | `radius`（未进闸）→ 建议**扩展**为「同类组件样式离散度」 |
| R14 | 工艺底线：没有文字溢出或截断、元素重叠遮挡、横向滚动条；375 和 1440 两个宽度下都成立 | 哪页更「做完了」 | VisAWI「designed with care」；Anthropic 质量底线；OpenAI 四项验收 | P+V | **新增**（审美侧；功能侧可能已有，需要核对） |

**C. 颜色**

| # | 单页问句 | pairwise 问句 | 来源 | 判定 | 映射 |
|---|---|---|---|---|---|
| R15 | 文本对比度 ≥4.5:1（大字 ≥3:1）；按钮边界、图标、输入框边框 ≥3:1 | 哪页更易辨识 | WCAG 1.4.3 / 1.4.11 | P | `contrast`（文本）+ **新增**（非文本 1.4.11） |
| R16 | 配色克制：色相家族 ≤3；只有一种强调色，而且只用在主要操作或关键信息上 | 哪页的强调色用得更准 | OpenAI「one accent」；Anthropic 4–6 色 token；VisAWI Colorfulness | P+V | `hue`（V 补「强调色是否只给 CTA」） |
| R17 | 颜色之间不打架：没有刺眼的互补色贴邻，底色与前景色协调 | 哪页的配色更和谐 | VisAWI「colors do not match (r)」「botched (r)」；Albers（未核实） | V | **新增（纯 VLM）** |

**D. 整体与表达**

| # | 单页问句 | pairwise 问句 | 来源 | 判定 | 映射 |
|---|---|---|---|---|---|
| R18 | 首屏有一个主视觉焦点和一个主 CTA，没有多个等权重元素抢注意力 | 哪页首屏更一眼知道该看哪、点哪 | Krug Billboard（未核实）；NN/g #8；OpenAI「one primary CTA above the fold」 | P+V | **新增**（P 只数首屏 CTA） |
| R19 | 没有无信息量的装饰：去掉任意一处描边、阴影、渐变、编号或卡片，不影响理解；没有点名的 AI 默认样式（SaaS 卡片套件、渐变洗底、报纸风发丝线、奶油加赤陶） | 哪页的装饰更少而准 | Anthropic skill；NN/g #8 信噪比；OpenAI 反事实删除 | V | **新增（纯 VLM）** |
| R20 | （只做 pairwise）哪页有和主题相关的视觉身份，而不是通用模板 | 同左 | Lavie & Tractinsky expressive；VisAWI Diversity；Anthropic originality | V | **新增（纯 VLM，只做 pairwise）** |

**映射汇总**
- 已有 11 条 → rubric 条目
  - `hier`→R01、`scale`→R02、`family`→R03、`len`→R04、`lh`→R05
  - `spacing`→R09、`grid`→R11、`ink`→R12、`radius`→R13
  - `contrast`→R15、`hue`→R16
- 新增程序判据（7）：R06、R07、R08、R10、R14、R15 的非文本部分、R18 的 CTA 计数
- 纯 VLM（3）：R17、R19、R20
- 需要 VLM 补视觉半边（7）：R01、R03、R11、R12、R13、R16、R18
- VisAWI 维度 → rubric
  - Simplicity → R01、R09–R12
  - Craftsmanship → R13、R14、R19
  - Colorfulness → R15–R17
  - Diversity → R20

**落地注意**（推断）
- 闸和分的分工
  - P 类条目继续当零噪声硬闸
  - V 类条目只进 pairwise 排序，不做绝对分；跨人 α 只有 0.25–0.37，绝对分不可信
- R20 和 R17 预计人与人之间的一致率最低（DesignPref、UICrit ICC ≈ 0），建议权重最小，或者只用来破平局
- R12 和 R04、R05 必须是区间；R19 要防止反向塌缩成极简白页，跟 `ink` 下界一起用

### Gaps
- 这 20 条都还没在本项目的 20 个变异上实测判别力；新增的 7 条程序判据阈值还没从参考页反推
- R10（亲密性）的几何算法在 Tailwind 的 `space-y` 或 `gap` 布局下怎么取「组」，还没定义
- 没有数据说明 VLM 在 R17、R19、R20 上与设计师的一致率，需要自己标一个小集（项目估计每题 8 次、30 题时最小可分辨差距约 15.4 个百分点）

