# 规则定维度，示例校标尺，比较出胜负

**结论先行。** 「专家 rubric + 多模态正反例」这个判断对了一半：两者确实是 VLM 网页审美 judge 的核心部件，但它们各管一件事，而且都抬不高天花板。rubric 管「看什么」。经典书里真正带硬数字的规则只有十来条：Bringhurst 行长 45–75 字符；Butterick 正文 15–25px、行距 120–145%、字体 ≤2；大写加 5–12% 字距；WCAG 对比度 4.5:1。其余都是条件式原则，作者自己也写 "widely regarded"、"tools—not dogma"。所以大部分条目应写成 DOM 一致性检查，只把焦点、层级、留白、装饰、平衡、配色冲突这几条交给 VLM。正反例管「尺子怎么量」。在 rubric 之上加人选的正反例后，三个前沿 VLM 的正反序准确率差从约 30 点降到约 9 点（ARR）；给作文评分加 anchor，GPT-4o 的 QWK 从 0.40 升到 0.69–0.72（人–人 0.79）。但在职业设计师的 UI 偏好上，8 对检索示例只让二元方向准确率变化 −0.1 到 +2.9 点（DesignPref）。瓶颈在数据本身：20 名设计师两两只有 62.4% 意见一致（κ 0.248），网页审美量表的单人评分者间 ICC 只有约 0.08–0.15，而 GPT-5 零样本已经做到 57.7%。人在「哪里坏了」上的一致程度远高于在「哪个更好」上。由此推荐的协议是：
- 程序门控兜底
- VLM 只在同组候选之间，按 9 条可观察规则两两比较
- 每次附 3–4 对「最小对」示例：与待判页视觉相似，示例里 A 胜、B 胜各占一半
- 强制二选一，AB / BA 各跑一次
- 只在高共识子集上考核，目标 ≥80%；风格条目只用来破平

> **标记约定**
> - 〔二手〕= 转述或摘要；〔未核实〕= 找不到可靠出处；〔推断〕= 本文推理；〔本文计算〕= 由引用数字换算；〔推断阈值〕= rubric 自定的阈值，需在参考页上标定后冻结
> - 判定方式：**DOM** = 程序读 DOM / computed style；**PIX** = 程序读截图像素；**VLM** = 只能看截图判
> - 书籍原文保留英文；来源检索截至 2026-11-03

---

## 1 经典书只给出十来个硬数字，其余规则只能写成一致性检查

十几本书和设计规范里，能直接写成阈值的规则集中在三处：排版（行长、行距、字号、字距、字体数、标题级数）、对比度、间距尺度。版式、层级、装饰、平衡类原则全都是条件式或关系式。作者们自己也把数字降格为惯例：
- Bringhurst 写行长时用 "widely regarded"
- Tim Brown 说 modular scale 是 "tools—not dogma" ([A List Apart](https://alistapart.com/article/more-meaningful-typography/))
- Bringhurst 还有一句 "By all means break the rules, and break them beautifully, deliberately and well."〔二手〕([Quotepark](https://quotepark.com/fr/citations/837566-robert-bringhurst-by-all-means-break-the-rules-and-break-them-beaut/))
- 只有 Butterick 明确把自己的条目叫 "rules" ([Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html))

所以 rubric 的写法分三类：
- 硬数字 → DOM 区间检查
- 关系式（行越长行距越大、组间距大于组内距）→ DOM 一致性检查
- 整体判断 → VLM 两两比较

下面四张表给出每条规则的原文与出处。

### 1.1 排版：数字最硬的一块

| 规则 | 原文 | 出处 | 核实 | 判定 |
|---|---|---|---|---|
| 行长 | "Anything from 45 to 75 characters is widely regarded as a satisfactory length of line" … "for a single-column page set in a serifed text face in a text size."；"The 66-character line (counting both letters and spaces) is widely regarded as ideal."；"For multiple column work, a better average is 40 to 50 characters." | Bringhurst §2.1.2 ([webtypography.net](http://webtypography.net/2.1.2)) | 一手（经 Rutter 转录，未对纸本页码） | DOM |
| 行长（宽松版） | "The average line length should be 45–90 characters (including spaces)." | Butterick ([Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)) | 一手 | DOM |
| 行长（无障碍） | "Width is no more than 80 characters or glyphs (40 if CJK)." | WCAG 2.2 SC 1.4.8 AAA ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)) | 一手 | DOM |
| 行距 | Bringhurst 只给原则："Choose a basic leading that suits the typeface, text and measure"；Butterick："Line spacing should be 120–145% of the point size."；Rutter："figures upwards of 1.3 are common" | [webtypography.net 2.2.1](http://webtypography.net/2.2.1)；[Butterick](https://practicaltypography.com/summary-of-key-rules.html) | 一手 | DOM |
| 行距随行长变化 | "One rule to remember about line space is that it needs to be larger than the space between words"；"the more words per line, the more space needed between the lines." | Spiekermann《Stop Stealing Sheep》4e ([Google Fonts PDF](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)) | 一手（页码由 PDF 跨页反推） | DOM |
| 正文字号 | "Point size should be 10–12 points in printed documents, 15–25 pixels on the web." | [Butterick](https://practicaltypography.com/summary-of-key-rules.html) | 一手 | DOM |
| 字号尺度 | "Use the old familiar scale, or use new scales of your own devising," "but limit yourself, at first, to a modest set of distinct and related intervals." | Bringhurst §3.1.1 ([webtypography.net](http://webtypography.net/3.1.1)) | 一手 | DOM |
| 字号种类 | 坏例："unnecessary ornaments, too many kinds of type and type sizes (7), centered design, which makes reading difficult and is unsightly."；好例："no use of ornament, clear type, few sizes (in all, only 5 different types), good legibility, good appearance." | Tschichold《The New Typography》1928 ([读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)) | 一手（英译读本） | DOM |
| 字体数 | "Most documents can tolerate a second font. Few can tolerate a third."；"Font mixing is most successful when each font has a consistent role in the document." | Butterick ([Mixing fonts](https://practicaltypography.com/mixing-fonts.html)) | 一手 | DOM |
| 大写字距 | "The normal value for letterspacing these sequences of small or full caps is 5% to 10% of the type size."；Butterick："All caps are fine for less than one line of text." "Use 5–12% extra letterspacing with all caps and small caps." | Bringhurst §2.1.6 ([webtypography.net](http://webtypography.net/2.1.6))；[Butterick](https://practicaltypography.com/summary-of-key-rules.html) | 一手 | DOM |
| 强调 | "Use bold or italic as little as possible, and not together." | [Butterick](https://practicaltypography.com/summary-of-key-rules.html) | 一手 | DOM |
| 居中与齐行 | "Use centered text sparingly."；"Always use hyphenation with justified text."；Bringhurst："Many unserifed faces look best when set ragged no matter what the length of the measure." | [Butterick](https://practicaltypography.com/summary-of-key-rules.html)；[webtypography.net 2.1.3](http://webtypography.net/2.1.3) | 一手 | DOM |
| 标题 | "Limit yourself to three levels of headings. Two is better."；"Use the smallest increment necessary to make a visible difference." | Butterick ([Headings](https://practicaltypography.com/headings.html)) | 一手 | DOM + VLM |

**冲突**集中在三处：
- 行长上限：Bringhurst 75、WCAG 80、Butterick 90；而 Spiekermann 说 90 字符一行已经 "almost too wide"
- 行距：Butterick 的上限 145% 与 WCAG AAA 的下限 1.5 不能同时满足
- 标题跨度：Butterick 主张最小可见增量，Brown 的示例却用 1.618

处理办法：
- 各家区间的交集算「好」带：行长 45–75，行距 1.3–1.6
- 交集外、仍在各家上限以内算「可接受」
- 超出所有上限才判失败
- 字号比例不判具体 ratio，只判「集合小、离散、单调」〔推断〕

**中文页面**：西文经典都没给 CJK 数字，只有 WCAG 给了 "40 if CJK"。中文的行长和行距要另找来源，W3C 的中文排版需求（clreq）本轮没有检索。

### 1.2 空间、分组与网格：判的是比例和一致，不是像素

| 规则 | 原文 | 出处 | 核实 | 判定 |
|---|---|---|---|---|
| 纵向节奏 | 标题、引文等插入后，"the main text should also return after each variation precisely on beat and in phase."；Rutter："The basic unit of vertical space is line height." | Bringhurst §2.2.2 ([webtypography.net](http://webtypography.net/2.2.2))；[Rutter, 24ways 2006](https://24ways.org/2006/compose-to-a-vertical-rhythm/) | 一手 | DOM |
| 响应式行长 | 用 `ch` 定行长会随字体变；推荐 `max-inline-size: 30rem` 这类写法，得到 "a line length accessibly tied to text size, but independent of font design" | Rutter ([Clagnut 2024](https://clagnut.com/blog/2432/)) | 一手 | DOM（多视口 × 多根字号） |
| 间距尺度 | "Every part of a UI should be intentional including the empty space between elements."；"deviating from the spacing scales should be avoided whenever possible"；13 级尺度 2–160px | IBM Carbon ([Spacing](https://carbondesignsystem.com/elements/spacing/overview/)) | 一手 | DOM |
| 接近性 | "Things that are close together are perceived to be more related than things that are farther apart."；"Degrees of proximity imply degrees of relatedness." | Lidwell 等《Universal Principles of Design》Pocket 版 ([archive.org](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)) | 一手 | DOM |
| 接近性的定量规律 | 分组 "is determined by the relative distance alone"（Pure Distance law）；接近与相似同时出现时 "the two principles are combined additively" | Wagemans 等 2012, *Psychol Bull* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/)) | 一手 | DOM（判组间 / 组内距离比，不判绝对像素） |
| 对齐 | "Align every element in your designs with one or more other elements."；"Left- and right-aligned text blocks provide better alignment cues than center-aligned text blocks." | [UPD Pocket](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools) | 一手 | DOM |
| 对齐（Williams） | "Nothing should be placed on the page arbitrarily. Every item should have a visual connection with something else on the page." | 《The Non-Designer's Design Book》3e ch.3 ([O'Reilly](https://www.oreilly.com/library/view/the-non-designers-design/9780321563088/ch03.html)) | 〔二手〕（O'Reilly 403，原句取自检索摘要与读者划线） | DOM |
| 网格 | "the will to cultivate objectivity instead of subjectivity"；"This orderliness lends added credibility to the information and induces confidence." | Müller-Brockmann ([读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)；[neugraphic 转载](https://mail.neugraphic.com/muller-brockmann/muller-brockmann-text2.html)) | 一手 | DOM（边缘聚类） |
| 一致性 | "Things that are the same should look the same. Things that look different should actually be different."；UPD："Make things internally consistent … to signal that a thing has been well designed and not cobbled together." | Butterick ([Maxims](https://practicaltypography.com/maxims-of-page-layout.html))；[UPD](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools) | 一手 | DOM + VLM |
| 阴影与边框 | "Instead of using large blur and spread values to make box shadows more noticeable, add a vertical offset."；边框太多 "can make your design feel busy and cluttered" | Wathan & Schoger, Refactoring UI ([Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)) | 一手 | DOM |

### 1.3 颜色：书里几乎只有「克制」和「相对」

| 规则 | 原文 | 出处 | 核实 | 判定 |
|---|---|---|---|---|
| 对比度 | 正文 4.5:1、大字 3:1；非文本组件 3:1 | WCAG 1.4.3 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html))；1.4.11 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)) | 一手 | DOM |
| 彩色底上的灰字 | "Making the text closer to the background color is what actually helps create hierarchy, not making it light grey." | Refactoring UI ([Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)) | 一手 | DOM |
| 一色一义、少用色 | "Avoid using the same color to mean different things."；"Apply color sparingly" | Apple HIG ([Color](https://developer.apple.com/design/human-interface-guidelines/color)) | 一手 | DOM |
| 分组色数 | "Color similarity is an effective grouping strategy when there are no more than 3-4 colors" | [UPD Pocket](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools) | 一手 | DOM |
| 色阶 | 灰色 "you want 8-10 shades to choose from"；"You can't build anything with five hex codes." | Refactoring UI ([官方节选](https://www.refactoringui.com/previews/building-your-color-palette)) | 一手 | DOM |
| 相对性 | "In visual perception a color is almost never seen as it really is" | Albers《Interaction of Color》1963 ([Albers Foundation](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)) | 〔二手〕 | PIX + VLM |
| 面积平衡 | Itten 的 contrast of extension：黄 : 紫面积约 1 : 3 | [OLLI 讲义](https://www.olli-dc.org/uploads/PDFs/2024_Spring/599_Miklitsch/599colortheoryweek3handout.pdf) | 〔二手〕，数值来源与精度有争议 ([Catania 论文](https://www.iris.unict.it/retrieve/dfe4d229-1aaa-bb0a-e053-d805fe0a78d9/17_CCS_Itten.pdf)) | PIX，低权重 |

### 1.4 层级、装饰、平衡：只能交给 VLM 的几条

| 规则 | 原文 | 出处 | 核实 | 判定 |
|---|---|---|---|---|
| 层级反映内容 | "Every part of a text relates to every other part by a definite, logical relationship of emphasis and value, predetermined by content." | Tschichold 1930 ([读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)) | 一手 | DOM + VLM |
| 层级手段 | "A common mistake when styling UI text is relying too much on font size to control your hierarchy."；"two font weights is usually enough for UI work" | Refactoring UI ([Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)) | 一手 | DOM + VLM |
| 一个主操作 | "Most pages only have one true primary action, a couple of less important secondary actions, and a few seldom used tertiary actions." | 同上 | 一手 | DOM + VLM |
| 前景压过背景 | "Don't let the background elements upstage the foreground elements." | Butterick ([Maxims](https://practicaltypography.com/maxims-of-page-layout.html)) | 一手 | VLM |
| 信噪比 | "Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility."；"Communicate; don't decorate." | NN/g heuristic #8 ([NN/g](https://www.nngroup.com/articles/aesthetic-minimalist-design/)) | 一手 | VLM |
| 装饰不成噱头 | "Whatever typographic device you come up with, don't let it turn into a gimmick." | [Spiekermann 4e](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf) | 一手 | VLM |
| 过度克制也是缺陷 | 一个去掉所有装饰却很平淡的信头，Tschichold 说 "A better name for it would be 'meagerness.'"；Spiekermann："magazine pages all set in one kind of type tend to look very gray." | [Tschichold](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)；[Spiekermann](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf) | 一手 | VLM |
| 平衡 | "An unbalanced composition looks accidental, transitory, and therefore invalid."；"Isolation makes for weight." | Arnheim《Art and Visual Perception》1974 ([archive.org](https://archive.org/details/art-and-visual-perception-rudolf-arnheim)) | 一手 | PIX + VLM |
| 有序的不对称 | "A striving for order can, and must, also be expressed in asymmetrical form." | [Tschichold](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf) | 一手 | VLM |

「装饰要少」和「不能寒酸、不能太灰」同出一批作者。所以装饰和密度都是**区间题**，不能写成「越少越好」〔推断〕。

### 1.5 不能当依据的流传说法

- **Lupton**：「each level of the hierarchy should be signaled by one or more cues…」只追到一份 CUNY 课程讲义，讲义没署 Lupton 的名 ([讲义](https://openlab.citytech.cuny.edu/clarkeadv1227/files/2012/11/ct_type1_hierarchy.pdf))。规则本身可以用，但不能署 Lupton
- **Samara**：「The greatst [sic] danger in using a grid is to succumb to its regularity.」只见于 Goodreads 用户整理，还带错字 ([Goodreads](https://www.goodreads.com/work/quotes/211129))
- **60-30-10**：所有来源都只说「来自室内设计」，给不出发明人和年代 ([Apartment Therapy](https://www.apartmenttherapy.com/interior-design-rule-60-30-10-explained-37504313))
- **黄金比例**：UPD 原文写 "Psychological evidence supporting a preference for golden proportions over other proportions is weak. If a preference exists, it is small." ([UPD](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools))。rubric 应**显式排除**这一项
- **Müller-Brockmann**：他说网格让信息读得更快、记得更牢，并称这是 "a scientifically proved fact"，但原文没引任何研究 ([neugraphic](https://mail.neugraphic.com/muller-brockmann/muller-brockmann-text2.html))
- **「一次只改一个参数」**：常被归给 Bringhurst，找不到出处。意思相近、有一手出处的是 Spiekermann："every time you change one spacing parameter, you have to look closely at all the others and adjust them accordingly" ([PDF](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf))

### 1.6 专家实践：评审靠聚合和样例，不靠 rubric 文本

真实评审团的 rubric 都很粗，没有一家公布逐档描述：
- **Awwwards**
  - 公开权重："Design: 40% points"、"Usability: 30% points"、"Creativity: 20% points"、"Content: 10% points."
  - 每件作品发给 "a minimum of 18 jury members"，离均值最远的 3 个分自动剔除
  - Honorable Mention 门槛 6.5 分 ([Awwwards](https://www.awwwards.com/about-evaluation/))
- **Webby**：网站类 7 个维度，Round 1 每件作品由多名评委独立打分 ([Webby](https://www.webbyawards.com/judging-criteria/))
- **Red Dot**：24 名专家逐件讨论，由团队做决定；页面明说每位评委带着由经历和文化背景形成的个人预期，讨论就是用来平衡这些预期的 ([Red Dot](https://red-dot.org/magazine/how-to-convince-the-red-dot-jury-this-is-what-the-experts-for-communication-design-pay-attention-to))

把评委对齐的是三样东西〔推断〕：
- 多人聚合并去掉离群分
- 当面讨论
- 往届获奖作品库：Awwwards 的 SOTD、CSSDA 的 WOTD 本身就是公开的视觉 anchor 库

从业者讲原则时也配图：
- NN/g 的视觉设计五原则（scale、visual hierarchy、balance、contrast、Gestalt），每条都配了 Medium、Uber、Dropbox 等产品的真实截图 ([NN/g](https://www.nngroup.com/articles/principles-visual-design/))
- Tschichold 1928 年的书里直接给了一组同内容的坏 / 好对照图注（见 1.1）
- Butterick 写道："There's no substitute for making samples of two options and getting a visual reaction." ([Maxims](https://practicaltypography.com/maxims-of-page-layout.html))

**前沿实验室写给模型的设计指南恰好相反，只有文字：**
- Anthropic 的 `frontend-design` skill 目录里只有 SKILL.md 和 LICENSE.txt，没有一张图，却要求模型截图自审："a picture is worth 1000 tokens" ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md))
- OpenAI 建议 "Reference screenshots or mood boards help the model infer layout rhythm, typography scale"，但博文里只有一张 mood board，没有好坏对照 ([OpenAI](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4))
- 两家的风格规则互相冲突，而且变得很快：
  - 字体：OpenAI 的 GPT-5 cookbook 推荐 Inter ([cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_frontend))；Anthropic 2025-12 版 skill 写 "NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts)"
  - 背景：OpenAI GPT-5.4 要求 "Don't rely on flat, single-color backgrounds; use gradients, images, or subtle patterns"；Anthropic 2026-09 版把渐变洗底列为 AI 默认特征 ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md))
- 结论：风格类的文字规则半年就会变，不能做硬条目〔推断〕

---

## 2 共享核心来自加工流畅性，设计师两两却只有 62% 同意

### 2.1 共享的部分：低复杂度、高原型性、清晰

共享部分有清楚的机制。Reber 等人的加工流畅性理论认为："The more fluently perceivers can process an object, the more positive their aesthetic response."。图形好形、图底对比、重复、对称、原型性都被归到这一条之下 ([Reber, Schwarz & Winkielman 2004](https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf))。

网页上，流畅性表现为**低视觉复杂度 + 高原型性**。Tuch 等人用 120 个网页做了 3×2 设计 ([Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf))：
- 原型性主效应 η²p = **.812**，复杂度 η²p = .581
- 复杂度高时，原型性几乎救不回来：高、低原型性之间的 d 从低复杂度时的 1.96 降到 **.24**
- 17 ms 呈现时，复杂度效应（η²p .38）已经强于原型性（.19）

Thielsch 与 Hirschfeld 用滤波实验证明，50 ms 时只有低空间频率在起作用 ([Thielsch & Hirschfeld 2012](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf))。可见最早进入审美判断的是全局布局和杂乱程度，字形、图标这类细节要到半秒以后才起作用。rubric 里「布局、留白、杂乱度」应排在「细节精致度」前面〔推断〕。

「首印象一致」常被误读，需要两点修正：
- 这种一致是**跨网页平均分**的一致，不是人人看法相同。Tractinsky 等人报告 500 ms 与 10 s 的网页平均分相关 r = .92 ([Tractinsky 2004](http://www.ise.bgu.ac.il/faculty/noam/papers/04_ntacmk_final.pdf))
- 「50 ms 定型」不成立。加 backward mask、改为组间设计后，50 ms 与 500 ms 只相关 **.12**（不显著），500 ms 与 10 s 相关 .53 ([Thielsch & Hirschfeld 2012](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf))。能说的是「半秒」，不是「50 毫秒」

classical aesthetics（clean、clear、pleasant、symmetrical）的特殊之处，在于它和可用性绑在一起：
- 可用性与 classical 相关 .68 / .78，与 expressive 只有 .46 / .40 ([Lavie & Tractinsky 2004](http://www.ise.bgu.ac.il/faculty/noam/papers/04_tl_nt_ijhcs.pdf))
- 审美–可用性效应只发生在**感知**层面：感知审美与感知可用性在使用前相关 .66、使用后 .71，但审美对完成时间完全没有影响，F(2,118) = 0.01，p = .987 ([Tractinsky et al. 2000](http://www.ise.bgu.ac.il/faculty/noam/papers/00_nt_ask_di_iwc.pdf))
- UICrit 数据里，设计师给的 aesthetics 分与 usability 分相关 **.875** ([UICrit](https://arxiv.org/html/2407.08850v3))
- 对 judge 的含义：分维打分时，「好看」会污染「好用」，两个维度的分不能当独立证据〔推断〕

### 2.2 主观的部分：颜色、密度、风格调性

**个人口味占比很大。**
- Reinecke 与 Gajos 的样本是 3.2 万人、179 个国家，作者的结论原话："appeal is largely subjective even after a short exposure time of 500ms" ([Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf))
  - 色彩度、复杂度、人口学这些固定效应只解释 **7%** 的方差（marginal R²）
  - 加上「网站」和「被试」两个随机截距，解释量到 47%（conditional R²）
  - 也就是说，可计算的知觉特征只占一小块；大块是「这个网站本身」的共享效应，加上「这个人整体打分偏高或偏低」的个人效应
- 曲线形状各国相似，峰值位置不同（同一来源）：
  - 复杂度：俄罗斯偏好最低（峰值 2.5），塞尔维亚、波黑、墨西哥、智利最高（4.6–4.8）
  - 色彩度：芬兰、俄罗斯、波兰、丹麦 3.6–4.4，美国 6.1，马其顿 7.6
- 复杂度的倒 U 曲线是平均出来的：30 名被试里，20 人越简单越喜欢（r = −.789），10 人越复杂越喜欢（r = +.874）([Güçlütürk et al. 2016](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00112/full))

**单人评分噪声很大。** VisAWI 研究 5 中，512 人评 42 个网站，每人只评一个。由网站间 F 值换算出的单人评分者间 ICC 如下〔本文计算〕([Moshagen & Thielsch 2010](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf))：
- Simplicity ≈ .145
- Diversity ≈ .146
- Craftsmanship ≈ .112
- Colorfulness ≈ **.082**（最低）

量表手册建议每个网站至少 20 名评价者 ([VisAWI Manual](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf))。换算下来，20 人均值的信度约 .64–.77〔本文计算〕。另一个反直觉的结果是：偏 classical 的 Simplicity 和偏 expressive 的 Diversity，评分者间一致性几乎相同。所以「classical 更客观」没有直接证据，classical 的价值在于它和可用性绑在一起。

**设计师在「明显程度」上收敛，在风格上分歧。** DesignPref 让 20 名职业设计师评 AI 生成的 UI ([DesignPref](https://arxiv.org/html/2511.20513v1))：
- 一致性
  - 二元偏好两两一致 **.624**，κ .248
  - 四档强度：κ 只有 .114
  - 28.5% 的对子两两分歧率 ≥96%
- 按屏幕类型
  - 表单类一致率 72.11%
  - 条款、相机、媒体播放器、登录等 54–57%
  - 20 类屏幕的一致率与「强偏好」选项占比相关 r = **.774**
- 理由分析
  - 收敛主题：clean layout and readability、primary actions and controls、perceived modernity and polish
  - 分歧主题：information density、visual style and tone、decorative imagery vs focused utility

| 判断对象 | 共识程度 | 证据 | rubric 写法 |
|---|---|---|---|
| 能不能读、主操作在哪、整不整洁 | 高 | DesignPref 收敛主题；classical 与可用性 r .68–.78 | 正常权重 |
| 品类惯例（原型性） | 高 | Tuch PT η²p .812 | 有依据，但会把输出推向模板 |
| 杂乱度 / 复杂度 | 方向共享，阈值不共享 | Reinecke 峰值随国家、年龄平移；Güçlütürk 两簇 | 区间题，阈值在目标人群上标定 |
| 信息密度、风格调性、装饰 vs 功能 | 低 | DesignPref 分歧主题 | 只破平 |
| 配色 | 最低 | VisAWI Colorfulness ≈.082；TASTE Color Harmony τ .103 ([TASTE](https://arxiv.org/html/2605.20731))；颜色偏好均值能被生态价值解释 r = .893，但跨人群预测降到 .47–.64 ([Palmer & Schloss 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2889342/)) | 只判明显冲突 |
| 新意、表达 | 与 classical 相同（ICC ≈.146） | VisAWI〔本文计算〕 | 不是更主观，而是「谁的口味」的问题；只破平 |

网页这类人造物，本来就落在「低共享」一端：
- 风景视频的可重复方差里，只有 12% 是共享的，88% 是个人的 ([Isik & Vessel 2021](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.676032/full))
- 私人口味在面孔上占 40%，在抽象艺术上占 75% ([Leder et al. 2016](https://www.frontiersin.org/articles/10.3389/fnhum.2016.00155/full))

### 2.3 专家并不更一致，只是更会说

「专家 rubric」的价值不是来自专家之间更一致：
- DesignPref 的职业设计师之间，二元 κ 只有 .248
- 创造力共识评估（CAT）里，10 名专家内部 α = .832，但专家与新手的评分只相关 **r = .216** ([Kaufman et al. 2008](https://www.rider.edu/sites/default/files/2024-05/CATRatersPoems.pdf))
- 训练会系统地改变偏好：无艺术训练者偏好简单、对称，受训者偏好复杂、不对称；音乐新手偏好原型和弦进行，专家没有这种偏好 ([Reber 2004](https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf))
- 执业建筑师预测外行对大型当代建筑的评价，预测值与外行实际评分 "poorly correlated"〔二手〕([Notre Dame 摘要](https://housingandcommunityregeneration.nd.edu/research/architects-predict-lay-evaluations-of-large-contemporary-buildings-whose-conceptual-properties/))
- 网页上唯一的 EEG 研究（10 名专家对 10 名外行）：作者文字称专家更常把「美」网页判为不美，但 ERP 在任何时间窗都没有组 × 审美交互；抓到的原表方向与文字相反，引用时要谨慎 ([Bölte et al. 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5463973/))

专家 rubric 的真正价值是**把共享的知觉规律说出来、写成条目**，而不是「专家口味更标准」。如果 rubric 由设计师写、目标用户是普通人，风格新意就不该写成硬规则〔推断〕。

### 2.4 天花板：judge 与单个设计师的一致率很难超过 62%

| 口径 | 数字 | 来源 |
|---|---|---|
| 设计师单人 vs 单人，二元偏好 | 62.4%，κ .248 | [DesignPref](https://arxiv.org/html/2511.20513v1) |
| 设计师单人 vs 单人，四档强度 | 38.6%，κ .114 | 同上 |
| AI 生成平面设计排序 | α ≈ .19；Color Harmony τ .103（无平局时折合两两一致约 55%〔本文计算〕） | [TASTE](https://arxiv.org/html/2605.20731) |
| 网页量表单人 ICC | ≈ .08–.15；20 人均值 ≈ .64–.77〔本文计算〕 | [VisAWI](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) |
| 知觉特征可解释的部分 | marginal R² .07 | [Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) |
| 当前 VLM 零样本 | GPT-5 57.70% | [DesignPref](https://arxiv.org/html/2511.20513v1) |
| 预测多数票 vs 预测单人（通用 T2I 图像） | 单人 vs 单人 78.1%，单人 vs 均值 85.0% | [HPSv2](https://arxiv.org/html/2306.09341) |
| 人类分差拉大时的 VLM | GPT-4o / Claude 从约 50% 升到约 90% / 93% | [MLLM as a UI Judge](https://arxiv.org/html/2510.08783v1) |

全量数据上，GPT-5 零样本离人–人水平只剩约 5 个点，rubric 和示例能争取的空间本来就小。但在人类分差大的对子上，VLM 能到九成。所以考核应**按共识度分层**：
- 高共识对子：目标 ≥80%
- 风格对子：只报告，不考核〔推断〕

天花板也不是固定的。WebDevJudge 里，同一批标注员拿到 rubric 后，相互一致率从 65.0% 升到 92.0% ([WebDevJudge](https://arxiv.org/html/2510.18560v2))。这说明相当一部分「主观分歧」只是判据没说清楚。正确顺序是先用 rubric 和示例把人拉齐，再拿拉齐后的标注去测 VLM〔推断〕。

---

## 3 正反例对压住位置偏差、校准标尺，却几乎不改偏好方向

教育测量和 VLM 是两条独立的证据线，结论相同。样例主要在校准「尺子」：每一档长什么样、强弱怎么分、顺序不该影响判断。它不会在没有共识的地方凭空造出共识。

### 3.1 人类评分：先有样例，后有 rubric

**综述结论。** Jonsson 与 Svingby 综述了 75 项研究，结论原文 ([ERIC](https://eric.ed.gov/?id=EJ796733))：
- "the reliable scoring of performance assessments can be enhanced by the use of rubrics, especially if they are analytic, topic-specific, and complemented with exemplars and/or rater training"
- 但 "rubrics do not facilitate valid judgment of performance assessments per se."

**AP Studio Art 是艺术评分里最成熟的做法** ([CRESST 402](https://cresst.org/wp-content/uploads/TECH402.pdf))：
- 做法：主阅卷人与组长 "spend two full days examining, discussing, and selecting sample portfolios"，用这些作品集 "exemplify the various points on the 0-4 rating scale"
- 历史：1992 年以前，标准只靠培训和讨论传递 "(i.e., via an oral tradition)"。也就是先有样例，后有文字 rubric
- 一致性：即便如此，两位阅卷人的相关也只有约 .65（小节 .58）

**LLM 评分里的 anchor 效应。** GPT-4o 给作文打分，结果如下（人–人 QWK 0.79）([Choi et al. 2025，预印本](https://doi.org/10.35542/osf.io/cbhgz_v1))：

| 提示内容 | QWK | 完全一致 % |
|---|---|---|
| 只给 rubric | 0.40 | 29.08 |
| rubric + 原文材料 | 0.46 | 30.96 |
| rubric + 每档 3 篇 anchor | 0.69 | 44.81 |
| rubric + 原文材料 + 每档 3 篇 anchor | **0.72** | 46.37 |
| rubric + 只锚两端（1 分和 6 分） | 0.59 | 41.14 |
| rubric + 只锚 1、3、6 分 | **0.39** | 32.79 |
| 人–人（经 3 小时 rubric + anchor 培训） | 0.79 | 51 |

三点规律：
- 每一档都给样例最好
- 只给两端也有用
- 随便挑几档反而不如不给

从每档 1 篇增加到每档 3 篇，QWK 只多 0.07。

**其他证据。**
- 校准样例：17 个 calibrated exemplars 让评委间相关达到 .835 / .863，但宽严差异还在（SD 16 / 14，有的评委平均比别人低约 30 分）([Humphry & Heldsinger 2020](https://www.frontiersin.org/articles/10.3389/feduc.2020.00006/full))
- 比较判断（ACJ），本身就源自设计与技术课程的作品集评估：
  - 评委只需 "decide which of them is the better" ([Pollitt 2012](https://doi.org/10.1080/0969594x.2012.665354))
  - e-scape 项目报告信度 0.93 ([Kimbell](https://doi.org/10.24377/dteij.article2337))
  - 49 个 CJ 评估的 meta 分析：信度 .70 需要每件作品比较 10–14 次，.90 需要 26–37 次 ([Verhavert et al. 2019](https://doi.org/10.1080/0969594x.2019.1602027))
  - 注意：自适应算法会虚高信度指标，真实信度 0.70 时 SSR 可能显示 0.95〔二手〕([Frontiers 2022 转引 Bramley](https://www.frontiersin.org/articles/10.3389/feduc.2022.854378))
- 反面提醒：资深评分者的隐性标准差异很大，"assessment decisions at this level are so complex, intuitive and tacit that variability is inevitable" ([Bloxham et al. 2016](https://doi.org/10.1080/02602938.2015.1024607))

### 3.2 VLM：示例改变的是尺度与顺序，不是品味

| 研究 | 对照 | 示例改变了什么 | 没改变 / 缺什么 |
|---|---|---|---|
| UICrit（移动 UI 批评，Gemini Pro Vision）([arXiv](https://arxiv.org/html/2407.08850v3)) | 0-shot vs 随机 8-shot vs 相似 8-shot | 区域级批评质量 0.24 → 0.31（随机）→ **0.44**（视觉相似）；整屏按视觉 + 任务相似选例最好（0.58）；用户研究 0.31 → 0.48（人类设计师 0.75） | 三套准则始终在 prompt 里，没有去掉准则的对照组；没有 0-shot 打分准确率 |
| DesignPref（UI 偏好，4 个前沿 VLM）([arXiv](https://arxiv.org/html/2511.20513v1)) | rubric 零样本 vs 8 对检索示例（图 A + 图 B + 该设计师标签，rubric 降为 tie-breaker） | 四档强度准确率 **+3.0 ~ +24.2** 点〔本文计算〕 | 二元方向只 −0.1 ~ +2.9 点；GPT-5 的 SRCC 0.216 → 0.203 / 0.211，没有升 |
| ARR（T2I 偏好，HPDv3 14,400 对）([arXiv](https://arxiv.org/html/2605.08354)) | +rubric vs +rubric + 正反例 guide | 平均准确率 Qwen3-VL-8B 70.2 → **85.0**、GPT-5 76.1 → 88.8、Gemini 3.1 Pro 78.3 → 90.8；正反序差 Δ 31.6 / 28.2 / 27.8 → **10.3 / 9.3 / 8.9** | 增益几乎全部来自反序列（+21.9 ~ +25.4），正序列只 +3 ~ +4；示例与测试同分布；只出现在位置偏差消融里 |
| Wu 等，图像质量 MLLM（ECCV 2024）([arXiv](https://arxiv.org/abs/2403.10854)) | 带人类分数的示例图 vs 标准 vs CoT | — | "the inclusion of a human quality score has minimal impact on the GPT-4V inference"；双图 in-context 在 FR-KADID 上 SRCC 0.470，而双图 CoT 为 0.818 |
| Compare2Score（NeurIPS 2024）([arXiv](https://arxiv.org/html/2405.19298v1)) | 测试图逐一对比 5 张固定锚点（每档取 1 张人类评分方差最低的），用软概率聚合 | 9 个 IQA 数据集上 SOTA；锚点数 β = 1 就够 | KonIQ、CLIVE 上单图打分的 Q-Align 仍略好 |

> 注：上一份调研写的「ARR 示例让平均准确率 +4 ~ +12 点」应更正。按 Table 5 的 Avg 列，增益是 +12.5 ~ +14.8 点；+3 ~ +4 只是正序列（Forward）的增益。

**为什么示例能动标尺、动不了方向？** 有四个机制：

- **多模态 in-context learning 主要靠文字驱动**
  - Baldassini 等：在 VQA 上删掉示例图只掉 1.2–1.5 点；原话 "M-ICL is primarily text-driven, and that images in the context have little impact on the overall performance" ([Baldassini et al. 2024](https://ar5iv.labs.arxiv.org/html/2404.15736))
  - VL-ICL Bench：把示例图换成语义等价的文字后，shot 曲线 "grows much more sharply and consistently with number of shots" ([VL-ICL Bench](https://arxiv.org/html/2403.13164v4))
  - 推论：示例里的**文字理由**可能才是主要有效成分〔推断〕
- **相似检索的收益有一部分是「抄邻居标签」**
  - kNN 多数投票在分类上比检索式 ICL 更好（ImageNet 79.52 vs 75.18）
  - 约 12% 的 VQA 回答直接复制最后一个示例的答案 ([Baldassini et al.](https://ar5iv.labs.arxiv.org/html/2404.15736))
  - 审美标签本身噪声大，抄过来的就是少数人的偏好〔推断〕
- **图像预算很紧**
  - GPT-4V 一次放 8 张图做 in-context 打分，作者称出现 "a sharp performance drop" ([Wu et al.](https://arxiv.org/abs/2403.10854))
  - 多图比较从 3 张变 4 张，GPT-4V 从 80.32 降到 77.28 ([Co-Instruct](https://arxiv.org/html/2402.16641))
  - Gemini 1.5 Pro 能在**分类任务**上 log-linear 地吃到约 1,000 个示例 ([Jiang et al. 2024](https://arxiv.org/html/2405.09798v2))，但没有审美任务上的同类证据
- **天花板本来就低**：GPT-5 零样本 57.7%，设计师之间 62.4%

**位置偏差是示例最有价值的战场。**
- 偏差有多大：WiserUI-Bench 有 300 对真实 UI，胜者由工业 A/B 测试确定。其中 o1 在胜者放第二位时对 97.78%，放第一位时只对 16.56%；两种顺序都判对（CA）只有 **15.56%**；所有设定里最好的 CA 也只有 39.00 ([WiserUI-Bench](https://arxiv.org/html/2505.05026v4))
- rubric 几乎无效：ARR 里加 rubric 只把正反序差降约 3 点，加正反例降了 20 点以上
- 可能的机制〔推断〕：示例里同时出现「好图在前」和「好图在后」，相当于在 context 里做了顺序反事实。所以示例中 A 胜、B 胜必须各占一半，否则示例自己会制造新的位置偏差
- 两个协议级手段也有效：
  - 给每张图交错标注「The first image: …」：Q-Bench-PAIR 76.37 → 80.18
  - 专门训练多图比较：换序一致 κ 从 0.432 升到 0.864 ([Co-Instruct](https://arxiv.org/html/2402.16641))

### 3.3 示例不改变的东西，以及它带来的新风险

- **不改变偏好方向**：在低共识的 UI 偏好上只有 0–3 点（DesignPref）
- **不突破人类天花板**：任何 rubric + 示例组合，与单人的一致都超不过人–人一致率
- **不消除宽严偏移**：人类校准样例之后，宽严 SD 仍有 14–16 分（Humphry & Heldsinger 2020）。VLM 打绝对分普遍偏高，仍要用锚点比较来定档
- **跨分布没有证据**：ARR、DesignPref 的示例都与测试同分布。照片或 T2I 的示例迁到网页上是否有效，没有数据
- **新风险**〔推断〕：抄邻居标签；近因复制；把示例的风格当成质量。在 RL 里，policy 会去模仿「好例」的风格，这和流畅性理论预测的「共享 reward 推向原型」是同一个方向
- **最大的证据空白**：没有任何工作在审美或设计数据上同时跑齐三组对照（只给 rubric / rubric + 示例 / 只给示例），也没人拆开「示例图」和「示例理由」各自的贡献

---

## 4 一份四层 rubric 和一套七步评判协议

### 4.1 四层架构

- **L0 程序门控**：一票否决，不进 VLM
  - T15（文本对比度）、T17（工艺底线）、T18（防刷分）
- **L1 程序区间**：打分，并作为「已验证事实」写进 VLM prompt
  - T01–T14、T16
  - 依据：把程序检查结果写进 prompt，图表可读性 SRCC 从 0.507 升到 0.843 ([VisEval](https://arxiv.org/html/2407.00981))；对齐、留白这类小扰动，GPT-4o 判不出 ([Haraguchi et al.](https://arxiv.org/html/2410.08885))
- **L2 VLM 高共识规则**：两两比较，正常权重
  - V01–V05
- **L3 VLM 中低共识规则**
  - V06、V07：低权重
  - V08：只做扣分闸
  - V09：只用来破平

### 4.2 程序层 rubric（T01–T18）

依据的原文和链接见第 1 节，这里只列规则名。

| ID | 规则 | 初始阈值 | 依据 | 层 |
|---|---|---|---|---|
| T01 | 正文行长 | 单栏 45–75 字符为好；75–90 可接受；>90 或 <40 失败。多栏 / 卡片 40–50。中文 ≤40 字 | Bringhurst §2.1.2；Butterick；WCAG 1.4.8 | L1 |
| T02 | 响应式行长 | 375 / 1440 两个宽度 × 根字号 16 / 24px，四种组合下 T01 都成立 | Rutter（Clagnut 2024） | L1 |
| T03 | 行距 | line-height ÷ font-size 1.3–1.6 为好；<1.2 或 >1.8 失败；不带单位；行越长行距越大 | Butterick；Rutter；WCAG；Spiekermann | L1 |
| T04 | 正文字号 | 15–25px | Butterick | L1 |
| T05 | 字号集合 | 去重后 ≤7 种；相邻比 <1.07 的近重复字号为 0〔推断阈值〕 | Bringhurst §3.1.1；Tschichold 5 vs 7 | L1 |
| T06 | 字体族 | ≤2（3 是上限）；同一段落不混字体；每种字体角色固定 | Butterick | L1 |
| T07 | 全大写 | 渲染 ≤1 行；letter-spacing 0.05–0.12em；小写正文字距 ≈0 | Bringhurst §2.1.6；Butterick | L1 |
| T08 | 强调 | 不同时用粗体和斜体；链接以外不加下划线 | Butterick | L1 |
| T09 | 对齐 | ≥3 行的正文不居中〔推断阈值〕；两端对齐必须开 `hyphens: auto`，窄栏不两端对齐 | Butterick；Bringhurst §2.1.3；UPD | L1 |
| T10 | 标题 | 标题样式 ≤3 级；同级 computed style 相同；层级与「字号 × 字重」单调对应 | Butterick Headings；Tschichold | L1 |
| T11 | 间距尺度 | ≥70% 的 margin / padding / gap 落在一套尺度上（±1px）〔推断阈值〕 | Carbon；Bringhurst §2.2.2 | L1 |
| T12 | 接近性 | 组间 / 组内间距中位数之比 ≥2〔推断阈值〕；标题到下方内容的距离 < 到上方区块的距离 | Wagemans；UPD Proximity | L1 |
| T13 | 对齐边缘 | 各块左右边缘聚类后，相差 1–8px 的「差一点对齐」边缘对 ≈0 | Müller-Brockmann；UPD Alignment | L1 |
| T14 | 组件一致 | 同角色元素的 radius / shadow / padding 只有 1 个取值；全页 radius ≤4 种；阴影 ≤3 级、y-offset >0、与层叠顺序单调 | UPD Consistency；Butterick maxims；Refactoring UI；Material Shape ([MDC](https://github.com/material-components/material-components-android/blob/master/docs/theming/Shape.md)) | L1 |
| T15 | 对比度 | 文本 ≥4.5:1（大字 3:1）；非文本 ≥3:1；彩色背景上没有中性灰字 | WCAG 1.4.3 / 1.4.11；Refactoring UI | 文本 L0，其余 L1 |
| T16 | 颜色角色 | 可交互元素的颜色与不可交互文字的颜色不重合；每个动作组的实心高饱和按钮 ≤1；分类色 ≤4 | Apple HIG；Refactoring UI；UPD Similarity | L1 |
| T17 | 工艺底线 | 375 / 1440 下无溢出、截断、遮挡、横向滚动 | Anthropic frontend-design 质量底线 "responsive down to mobile" | L0 |
| T18 | 防刷分 | 没有全局 border / outline，没有把 prompt 原文渲染成大字，没有重复装饰堆叠 | FRAME：加 bbox 让 GPT-4o 分数 +80.2% ([arXiv](https://arxiv.org/html/2505.15249v2)) | L0 |

### 4.3 VLM 层 rubric（V01–V09）：每条配一个最小对

「最小对」= 同一页内容，只改这一条规则。形式上就是 Tschichold 那组坏 / 好图注的 web 版。

| ID | 两两问句 | 好例 | 坏例（同内容只改这一条） | 依据 | 共识 / 用法 |
|---|---|---|---|---|---|
| V01 焦点 | 哪页首屏更一眼知道先看哪、点哪？ | 主标题最显著；1 个实心主按钮，周围有净空 | 4 个等权的实心彩色按钮并排；「限时优惠」角标比主标题更大更亮 | Refactoring UI "one true primary action"；Arnheim "Isolation makes for weight."；Tschichold 层级反映内容 | 高；正常权重 |
| V02 层级 | 哪页主次更一眼可辨，相邻层级的差异刚好可见又不过度？ | H1 40px/700，正文 16px/400，元信息用灰色 | A：H1 18px/500 对正文 16px/400（差异太弱）；B：五级标题每级都抢戏 | Butterick "smallest increment necessary to make a visible difference"；Refactoring UI；Williams "make them different. Really different."〔二手〕([Proper Sky](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)) | 高 |
| V03 分组与疏密 | 哪页分组更清楚、疏密更合适？ | 组内 8px、组间 32px | A：所有块之间一律 16px；B：满屏紧贴，或大片空白 | VisAWI "The layout appears too dense."；UPD Proximity；Reinecke U 形 | 分组：高；密度只判极端 |
| V04 前景 / 背景 | 哪页的背景和装饰更不抢正文？ | 低对比背景；压在照片上的文字有遮罩 | 高饱和插画或毛玻璃铺满；文字直接压在杂乱照片上 | Butterick "upstage"；UPD Figure-Ground | 高 |
| V05 信噪比 | 哪页更少「去掉也不影响理解」的装饰？ | 没有多余描边、渐变、伪编号 | 同内容加渐变描边、星星图标、花体分隔线、无顺序意义的「01 / 02 / 03」 | NN/g "Communicate; don't decorate."；Tschichold "unnecessary ornaments"；Spiekermann "gimmick" | 中高；与 V07 合看，防止反向塌缩成寒酸 |
| V06 平衡 | 哪页构图更稳、更像有意为之？ | 左文右图，或有序的不对称 | 标题、按钮、图片都挤在左 1/3，右侧没有任何视觉重量 | Arnheim "looks accidental"；Tschichold "order … in asymmetrical form" | 中；低权重 |
| V07 统一概念 | 哪页更像「一套」、看得出有统一构思？ | 字体角色、色板、圆角全页一致 | A：三张卡片三种风格；B：全页同字体同字重，一片灰 | VisAWI "Everything goes together on this site." 与 "The design of the site lacks a concept."（反向条目）；Spiekermann "very gray"；Tschichold "meagerness" | 中；低权重 |
| V08 配色冲突 | 哪页有明显不协调的颜色搭配？（只判明显冲突） | 品牌橙放在白底上 | 品牌橙放在米黄底上，发灰发脏；高饱和互补色大面积贴在一起 | VisAWI "The colors do not match."；Albers 相对性〔二手〕 | 低；只做扣分闸 |
| V09 视觉身份 | 去掉导航后，哪页首屏更不可能属于别的品牌？ | 有与主题相关的视觉身份 | 通用 SaaS 卡片套件；点名的 AI 默认样式 | OpenAI："Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak."；Lavie & Tractinsky expressive | 低；只破平 |

VisAWI 条目原文见 [Moshagen & Thielsch 2010](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf)。

### 4.4 示例库怎么建

- **形式**
  - 每条 V 规则做最小对，每对配 1–2 句「可观察事实」式理由，例如「坏例首屏有 4 个等权实心按钮」
  - 违规要明显：大扰动 VLM 判得准，小扰动判不出（Haraguchi）；2–4px 量级的问题交给 DOM
  - 不放「单图 + 分数」式示例，模型基本不看分数（Wu et al.）
- **数量与配平**
  - 每条规则 ≥4 对：2 对 A 胜、2 对 B 胜
  - 好例横跨 ≥3 种风格，例如极简、编辑感、高饱和品牌风，避免把某一种风格当成质量〔推断〕
- **共识筛选**
  - 每对 ≥5 人盲评，只保留同意率 ≥80% 的〔推断阈值〕
  - 优先选人类评分方差最低的，与 Compare2Score 选锚点的原则一致
- **检索**
  - 按「截图视觉 + 页面任务描述」联合相似度，每次取 3–4 对（UICrit 中视觉 + 任务相似最好）
  - 编码器可沿用 DesignPref 的做法：文字用 Sentence-BERT，截图用 UIClip 视觉编码器
- **图像预算**
  - 示例加待判，总图数 ≤10
  - 示例图降分辨率，或只裁违规区域
  - 在自己的验证集上扫 k = 0 / 2 / 4 / 8，确认收益是否见顶
- **防近因复制**
  - 示例顺序随机
  - 最后一个示例的胜方，不要总和待判对里「表面更像它」的那张一致

### 4.5 评判协议

1. **先拉齐人**
   - 用同一套 rubric 和示例库培训标注员，再标测试集
   - 每对多人标注，按共识度分层（WebDevJudge：rubric 让人–人一致从 65% 升到 92%）
2. **渲染取证**
   - 375 与 1440 两个宽度，各截首屏和整页
   - 导出 computed style 与关键 CSS
3. **程序门控与区间**
   - L0 任一失败，直接判负
   - L1 的数值写成「已验证事实」，VLM 不重判
4. **组对**
   - 只在同一 prompt、L0 全过的候选之间配对
5. **VLM 比较**
   - 每张图交错标注 Image A / Image B
   - 每次 5–10 条 V 规则
   - 每条先写 ≤1 句证据并指出位置，再强制选 A 或 B，不给平局（强制选择 83.9% vs 允许平局 54.9%，[GenArena](https://arxiv.org/html/2602.06013)）
   - AB / BA 各跑一次，不一致记平
   - 不做长 CoT 后给总分（3 步 CoT 让 GPT-4V 打分相关从 0.557 掉到 0.299，[MLLM-as-a-Judge](https://arxiv.org/html/2402.04788v3)）
6. **聚合**
   - 条目权重用人标对子学，用逻辑回归，不要拍脑袋（VisionReward：训练对从 200 增到 4k，准确率 77.6 → 81.3，[arXiv](https://arxiv.org/html/2412.21059v4)）
   - V08 只扣分，V09 只破平
   - 候选之间用 Bradley–Terry 排序
   - 需要绝对档位时，与 5 张锚页逐一比较后聚合，不让 VLM 直接打分（两两比较与人类排名的 Spearman 0.86，打分只有 0.36，[GenArena](https://arxiv.org/html/2602.06013)）
7. **监控**
   - 报 CA 与正反序差 Δ，不报单序准确率
   - 按共识层分别报准确率
   - judge 与 policy 不同家族，至少两家交叉，借鉴 Awwwards 去掉离群分
   - 定期用 FRAME 式攻击（加 border、叠文字）做回归测试

### 4.6 prompt 模板

```text
[角色] 你是网页视觉设计评审。只判下列条目，每条只看一个可观察事实。
[已验证事实，不要重判]（来自程序 L1）
  Image A：正文 64 字符/行；行距 1.55；字号 6 种；实心主按钮 1 个
  Image B：正文 96 字符/行（超出上限 90）；行距 1.25；字号 11 种；实心主按钮 4 个
[参考示例]（检索得到 3 对最小对，胜方已配平）
  示例 1 —— Image X: <图>  Image Y: <图>
    结论：X 更好（V01）。理由：Y 首屏有 4 个等权实心按钮，看不出主操作。
  示例 2 —— Image X: <图>  Image Y: <图>
    结论：Y 更好（V05）。理由：X 每个区块都加了渐变描边和无顺序意义的编号。
  示例 3 —— …
[待判]
  Image A: <首屏截图> <整页缩略图>   关键 CSS A: <…>
  Image B: <首屏截图> <整页缩略图>   关键 CSS B: <…>
[条目] 对每一条：先写 ≤1 句证据并指出位置，再选 A 或 B，必须二选一。
  V01 哪页首屏更一眼知道先看哪、点哪？
  V02 哪页主次更一眼可辨，相邻层级差异刚好可见、不过度？
  V03 哪页分组更清楚（组内紧、组间松），疏密更合适？
  V04 哪页的背景和装饰更不抢正文？
  V05 哪页更少「去掉也不影响理解」的装饰？
[输出] 只输出 JSON：{"V01":{"evidence":"…","winner":"A"}, …}
```

- 把 A / B 互换再跑一次
- V06–V07 单独一轮；V08 作扣分闸单独问；V09 只在总分打平时问

### 4.7 上线前必须补的消融

文献里没有、本项目必须自己跑：
- **主对照**：同一 VLM、同一网页偏好集，四组
  - 无 rubric 无示例
  - 只给 rubric
  - 只给示例
  - rubric + 示例
- **拆示例成分**
  - 只给示例图、不给理由
  - 只给理由、不给图
- **扫参数**
  - k = 0 / 2 / 4 / 8
  - 随机选例 vs 相似选例
- **指标**
  - CA
  - 正反序差 Δ
  - 与多数票的一致率
  - 高共识子集上的一致率
- **阈值**：T 系列所有〔推断阈值〕在参考页与改坏样本上标定后冻结

---

## 结论

用户的判断需要换一种说法：rubric 是问卷，示例是尺子，两两比较是量具，人类共识是天花板。决定 judge 能走多远的，是评测数据里有多少高共识对子；rubric 和示例的作用，是让 VLM 在这些对子上稳定、不受顺序影响、刻度对齐。设计师自己就是这样教审美的：Tschichold 印出同一广告的坏版和好版，Butterick 说 "There's no substitute for making samples of two options"，AP Studio Art 先有样例作品集、后有文字 rubric。所以示例最该采用「最小对」形态：它把「哪个更美」的口味题，变成「哪一处坏了」的知觉题，而这恰好是 VLM 最擅长、人也最一致的那类题。

示例同时是一种风格编码。流畅性理论预测，共享审美会把输出推向原型。如果「好例」都是同一种风格，在 RL 里 policy 很快就会学会模仿示例，而不是学会好设计。示例库因此必须风格多样，风格条目（V08、V09）权重要最低。真正缺的是一个干净实验：同一 VLM、同一批网页，只给 rubric、只给示例、两者都给。在设计数据上，这三组对照目前还没有人跑过；谁先跑出来，谁就能回答「示例究竟教的是品味还是刻度」。

