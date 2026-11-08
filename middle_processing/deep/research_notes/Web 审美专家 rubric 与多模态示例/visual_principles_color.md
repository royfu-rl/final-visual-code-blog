# 视觉设计原则与色彩理论经典 → 可验证的 Web 审美 rubric 规则

> 图例
> - 核实等级：**[一手]** 本次会话读到原文 / 官方文档 / 官方代码；**[二手]** 二手转述、课程讲义、搜索摘要；**[未核实]** 凭既有知识、本次未能找到原文
> - 可检查性：**DOM** = 程序读 DOM / computed style 即可判；**PIX** = 程序读截图像素可判；**VLM** = 只能靠视觉模型看截图判；可组合，如 DOM+VLM
> - 规则编号：W=Williams，R=Refactoring UI，U=Universal Principles of Design，G=Gestalt/Arnheim，C=色彩，D=设计系统
> - 每条规则都配一对"好 / 坏"页面：内容相同，只有这一条规则不同

---

## Q1 Robin Williams《The Non-Designer's Design Book》：C.R.A.P. 四原则与常见错误

### Takeaway
Williams 的四原则（Proximity → Alignment → Repetition → Contrast，书中按这个顺序讲，缩写倒过来是 C.R.A.P.）几乎都能落成 DOM 级别的几何或样式检查：间距比、对齐线数量、同角色样式的唯一值个数、层级之间的尺寸比。只有"整体有没有焦点"这一项要交给 VLM。Alignment 原则的原句已从多个独立来源确认；其余三条的原句只拿到二手引文，书的全文在 archive.org 是借阅受限的（403）。

### Cited Findings
- **Alignment 原则原句**：「Nothing should be placed on the page arbitrarily. Every item should have a visual connection with something else on the page.」第 3 版（2008，Peachpit）O'Reilly 电子版 ch.3 "Alignment"。**[二手]**：O'Reilly 页面 403，原句取自搜索摘要，另有 Goodreads 读者划线和 UNCW 课程页的同文复述 — [O'Reilly ch03](https://www.oreilly.com/library/view/the-non-designers-design/9780321563088/ch03.html)；[Goodreads highlight](https://www.goodreads.com/notes/23846768-the-non-designer-s-design-book/20574378-rachel-robbins/74d690a5-c90e-40e3-b982-21c6f45cd5fa)；[UNCW course page](https://people.uncw.edu/atkinsa/319/crap/alignment.htm)
  - 措辞有版本差异：Proper Sky 的报告引作 "Every element should have some visual connection with another element on the page."（以第 4 版 2015 为参考文献）**[二手]** — [Proper Sky, TNDDB Applied (PDF)](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
- **Proximity**：「Group related items together.」**[二手]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
  - 讲义转述：purpose of proximity is to organize；"avoid leaving (exactly) equal amounts of white space between elements unless each group is part of a subset" **[二手]** — [Horizons Foundation handout (PDF)](https://www.horizonsfoundation.org/wp-content/uploads/2014/09/Producing_Great_Materials_on_a_Shoestring.pdf)；[SlideShare: Basic principles](https://www.slideshare.net/slideshow/basic-principles-of-graphic-design/65710713)
  - Proper Sky 的"眯眼数视觉单元，超过 3–5 个就继续归组"（"squint and count the visual units. More than three to five, keep grouping"）。这条门槛是该报告自己的转述，**不能确定**是书里的数字 **[二手/存疑]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
- **Repetition**：「Repeat some aspect of the design throughout the entire piece.」**[二手]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
  - 讲义转述："repetition of visual elements throughout the design unifies and strengthens a piece by tying together otherwise separate parts" **[二手]** — [Layers Magazine: Building Blocks](https://layersmagazine.com/building-blocks.html)
- **Contrast**：「If two items are not exactly the same, then make them different. Really different.」并有「Don't be a wimp.」**[二手]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
  - 另一种常见表述「If the elements (type, color, size, line thickness, shape, space, etc.) are not the same, then make them very different.」**[未核实]**：凭记忆，本次没有找到可抓取的原文
- **常见错误（书中 "what to avoid" 清单）**：以下几条我凭记忆整理，本次**全部未能对照原文 [未核实]**
  - Proximity："Avoid too many separate elements on a page"；"Don't stick things in the corners and in the middle"
  - Alignment："Avoid using more than one text alignment on the page"；"try very hard to break away from a centered alignment unless you are consciously trying to create a more formal, sedate presentation"
  - Repetition："Avoid repeating the element so much that it becomes annoying or overwhelming"
  - Contrast："Don't be a wimp"（有二手佐证）；避免 "sort-of-heavy vs sort-of-heavier" 这类弱对比
  - Proper Sky 的转述把"全部居中"列为初学者的主要病灶："Williams singles out the beginner's default — centering everything — as the main offender … mixing alignments is the real crime" **[二手]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)
- 书目信息：第 1 版 1994（archive.org 条目 `nondesignersdesi00will`，access-restricted，全文和 search-inside 均返回 403）**[一手：元数据]** — [archive.org item](https://archive.org/details/nondesignersdesi00will)

### Inferences
（以下规则卡是我的提案，依据为上面的引文）
- **W1 Proximity：组内间距明显小于组间间距**
  - 好 / 坏对：同一张"活动信息"页
    - 好：标题→正文 8px，组与组之间 32px（组间/组内 ≥ 2–3×）
    - 坏：所有块之间一律 16px；表单 label 离上一个输入框比离自己的输入框还近
  - 可检查性：**DOM**。相邻兄弟块的垂直 gap 序列 → 判断是否双峰；组间/组内中位数比；label 到所属控件的距离 < label 到上一控件的距离
- **W2 Alignment：每个元素都与另一个元素共享边线；避免混用多种对齐**
  - 好 / 坏对：同一个 hero + 三栏特性区
    - 好：标题、正文、按钮全部左对齐在 x=48px 一条线上
    - 坏：标题居中、正文左对齐、按钮右对齐，图标和文字差 3px
  - 可检查性：**DOM**。收集可见文本 / 控件 bbox 的 left / right / center-x 并聚类，统计"孤立边"占比、1–6px 的 near-miss 数、同一 section 内 `text-align` 的种类数
- **W3 Repetition：同角色元素复用同一套样式**
  - 好 / 坏对：同一组 3 张卡片
    - 好：圆角、阴影、标题字号字重完全一致
    - 坏：圆角 4/12/20px，阴影三种，标题字体两种
  - 可检查性：**DOM**。按角色（同 tag + 同 class 前缀 / 同结构位置）分组，统计 `border-radius` / `box-shadow` / `font-family` / `font-size` 的唯一值个数
- **W4 Contrast：不同就要"非常不同"，禁止近似值（wimpy contrast）**
  - 好 / 坏对：同一个文章页
    - 好：H1 40px/700，正文 16px/400
    - 坏：H1 18px/500，正文 16px/400；同页同时出现 15/16/17px 三种正文字号
  - 可检查性：**DOM + VLM**
    - DOM：相邻层级字号比（例如 <1.2 判为弱）、相邻字号的最小间隔、字重差
    - VLM："第一眼落在哪里"、是否存在单一焦点
- **W5 常见错误合成**
  - 好 / 坏对：同一张传单式落地页
    - 好：一条强左对齐轴
    - 坏：全部居中，四角各塞一个小元素
  - 可检查性：**DOM**。居中文本块占比、视口四角附近的孤立小元素数

### Gaps
- Proximity / Repetition / Contrast 的原句和页码都没能一手核对：O'Reilly 403，archive.org 借阅限制
- "What to avoid" 清单是凭记忆整理的 [未核实]，需要拿到实体书或 Peachpit 样章核对
- "3–5 个视觉单元"这个数字的出处不明（可能是 Proper Sky 自己加的）

---

## Q2 Wathan & Schoger《Refactoring UI》：具体战术

### Takeaway
Refactoring UI 是这些经典里最"可编程"的一本：作者的官方文章给出了明确的数字（2–3 个文字颜色、2 个字重、≥400 字重、阴影用垂直偏移、每色 5–10 个色阶、灰色 8–10 阶、9 阶最合适）。书的目录本身就是一张现成的 rubric 清单（带页码）。

### Cited Findings
- **书目录（官方页，带页码）[一手]** — [refactoringui.com/book](https://www.refactoringui.com/book)
  - 过程与风格："Start with a feature, not a layout" p7；"Detail comes later" p10；"Don't design too much" p13；"Choose a personality" p17；"Limit your choices" p24
  - Hierarchy："Not all elements are equal" p30；"Size isn't everything" p32；"Don't use grey text on colored backgrounds" p36；"De-emphasize to emphasize" p39；"Labels are a last resort" p41；"Separate visual hierarchy from document hierarchy" p46；"Balance weight and contrast" p48；"Semantics are secondary" p52
  - Layout & Spacing："Start with too much white space" p56；"Establish a spacing and sizing system" p60；"You don't have to fill the whole screen" p65；"Grids are overrated" p72；"Relative sizing doesn't scale" p79；"Avoid ambiguous spacing" p83
  - Text："Establish a type scale" p88；"Use good fonts" p94；"Keep your line length in check" p99；"Baseline, not center" p102；"Line-height is proportional" p105；"Not every link needs a color" p109；"Align with readability in mind" p111；"Use letter-spacing effectively" p115
  - Color："Ditch hex for HSL" p119；"You need more colors than you think" p123；"Define your shades up front" p129；"Don't let lightness kill your saturation" p133；"Greys don't have to be grey" p139；"Accessible doesn't have to mean ugly" p142；"Don't rely on color alone" p146
  - Depth："Emulate a light source" p150；"Use shadows to convey elevation" p158；"Shadows can have two parts" p163；"Even flat designs can have depth" p167；"Overlap elements to create layers" p170
  - Images："Text needs consistent contrast" p176；"Everything has an intended size" p181；"Beware user-uploaded content" p187
  - Finishing："Add color with accent borders" p195；"Decorate your backgrounds" p198；"Don't overlook empty states" p203；"Use fewer borders" p206；"Think outside the box" p210
  - 同页对 "Use fewer borders" 的摘要："Borders are a great way to distinguish two elements from one another, but using too many of them can make your design feel busy and cluttered. Instead, try adding a box shadow, using contrasting background colors, or simply adding more space between elements."
- **"7 Practical Tips for Cheating at Design"（作者署名 Adam Wathan & Steve Schoger，Medium / Refactoring UI 专栏；经 Wayback 2020 快照阅读）[一手]** — [Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)；[Wayback](https://web.archive.org/web/2020/https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)
  - **1. Use color and weight to create hierarchy instead of size**
    - "A common mistake when styling UI text is relying too much on font size to control your hierarchy."
    - 颜色："Try and stick to two or three colors: A dark (but not black) color for primary content … A grey for secondary content … A lighter grey for ancillary content"
    - 字重："two font weights is usually enough for UI work: A normal font weight (400 or 500 depending on the font) for most text; A heavier font weight (600 or 700) for text you want to emphasize"
    - "Stay away from font weights under 400 for UI work"；想弱化文字时 "use a lighter color or smaller font size instead"
  - **2. Don't use grey text on colored backgrounds**
    - "the effect we're actually seeing with grey on white is reduced contrast. Making the text closer to the background color is what actually helps create hierarchy, not making it light grey."
    - 两种做法："Reduce the opacity of white text"；"Hand-pick a color that's based on the background color … same hue as the background, adjusting saturation and lightness"
  - **3. Offset your shadows**
    - "Instead of using large blur and spread values to make box shadows more noticeable, add a vertical offset."
    - "simulates a light source shining down from above"
  - **4. Use fewer borders**
    - "using too many of them can make your design feel busy and cluttered"
    - 替代方案：box shadow、"Use two different background colors"、"increase the separation"（拉开间距）
    - "If you're already using different background colors in addition to a border, try removing the border"
  - **5. Don't blow up icons that are meant to be small**
    - "icons that were drawn at 16–24px are never going to look very professional when you blow them up to 3x or 4x their intended size … disproportionately 'chunky'"
    - 解法：把小图标放进带背景色的形状里
  - **6. Use accent borders to add color to a bland design**
    - 例：alert 侧边、激活中的导航项、整个布局顶部的彩色条
  - **7. Not every button needs a background color**
    - "Most pages only have one true primary action, a couple of less important secondary actions, and a few seldom used tertiary actions."
    - Primary："Solid, high contrast background colors"；Secondary："Outline styles or lower contrast background colors"；Tertiary："Styling these actions like links"
- **"Building your color palette"（refactoringui.com 官方节选，标注 adapted from the book）[一手]** — [refactoringui.com/previews/building-your-color-palette](https://www.refactoringui.com/previews/building-your-color-palette)
  - 灰色："almost everything in an interface is grey"；"you want 8-10 shades to choose from"
  - 主色："Most sites need one, maybe two colors that are used for primary actions"
  - 强调色："every site needs a few accent colors for communicating different things"
  - 色阶："at least 5 shades per color, and probably closer to 10"；"Nine is a great number"；复杂 UI "as many as ten different colors with 5-10 shades each"
  - 基准色："pick a shade that would work well as a button background"；最深一阶 "usually reserved for text"；最浅一阶 "used to tint the background of an element"
  - 反对生成器："You can't build anything with five hex codes."；"don't get clever using CSS preprocessor functions like 'lighten' or 'darken'"；"If you're not dilligent about limiting your palette, you might as well have no color system at all."
- **书中正文里的具体数值 [未核实]**：凭记忆，本次没有拿到正文
  - "Start with too much white space"：先给过量留白，再往回收
  - 间距 / 尺寸体系：类似 4, 8, 12, 16, 24, 32, 48, 64, 96, 128… 的非线性尺度，相邻值相差约 ≥25%
  - 字号尺度：类似 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
  - 行长：约 45–75 字符
  - 阴影：用约 5 级阴影表示 elevation

### Inferences
- **R1 层级先靠颜色 / 字重，再靠字号**
  - 好 / 坏对：同一个用户列表
    - 好：姓名 16px/600 深灰 #1f2937；元信息 14px/400 灰 #6b7280
    - 坏：全部同色同字重，只靠 24/20/18/16px 区分
  - 可检查性：**DOM**。可见文字的颜色种类（建议 ≤3 个灰阶）、字重种类（建议 2 种）、<400 字重且 <24px 的文本数、纯黑 #000 正文
- **R2 彩色背景上不用中性灰字**
  - 好 / 坏对：同一个蓝色 hero
    - 好：次要文字用白色 70% 不透明度，或浅蓝色调
    - 坏：#999 灰字压在 #2563eb 上
  - 可检查性：**DOM**。文字色饱和度≈0（中性灰）且有效背景色饱和度高 → 违规；再算 WCAG 对比度
- **R3 阴影带垂直偏移、模拟顶光**
  - 好 / 坏对：同一张卡片
    - 好：`0 4px 6px rgba(0,0,0,.1)`
    - 坏：`0 0 24px 8px rgba(0,0,0,.4)` 四周晕光
  - 可检查性：**DOM**。解析 `box-shadow`：y-offset > 0、spread 小、全页光源方向一致（x-offset 同号）
- **R4 少用边框**
  - 好 / 坏对：同一个设置页
    - 好：分组靠背景色差和间距
    - 坏：每行、每卡、每个输入框都有 1px #ccc 边框，且边框套边框
  - 可检查性：**DOM**。视口内有可见 border 的元素数、带边框祖先的嵌套深度、"边框 + 背景色差"冗余对
- **R5 按钮按层级金字塔设计，不按语义上色**
  - 好 / 坏对：同一个表单底部的 4 个动作
    - 好：1 个实心主按钮 + 1 个描边次按钮 + 2 个链接式按钮
    - 坏：4 个实心按钮，分别是绿 / 蓝 / 红 / 灰
  - 可检查性：**DOM**。同一动作组内"高饱和实心背景"按钮数 ≤ 1
- **R6 图标不放大超过设计尺寸**
  - 好 / 坏对：同一个特性区
    - 好：24px 图标放在 48px 浅色圆底里
    - 坏：16px 风格的线性图标直接放大到 96px
  - 可检查性：**DOM + VLM**
    - DOM：SVG 渲染尺寸 / icon-font 字号 > 48px 的次数
    - VLM："chunky" 感
- **R7 留白充足（宁多勿少）**
  - 好 / 坏对：同一个 landing 页
    - 好：section 上下 padding 64–96px
    - 坏：全站 8px 紧贴
  - 可检查性：**DOM + VLM**
    - DOM：section padding 分布、文字区面积占比
    - VLM："拥挤 / 透气"判断
- **R8 间距取自一套尺度**
  - 好 / 坏对：同一页
    - 好：所有 margin/padding/gap ∈ {4, 8, 12, 16, 24, 32, 48, 64}
    - 坏：出现 7, 13, 18, 22, 37px
  - 可检查性：**DOM**。落在尺度上的取值占比（容差 ±1px）
- **R9 字号取自一套尺度**
  - 好 / 坏对：同一页
    - 好：字号 ∈ {12, 14, 16, 20, 24, 30, 36}
    - 坏：出现 13, 15, 17, 19, 22, 23px 等十几种
  - 可检查性：**DOM**。唯一字号数（建议 ≤ 6–8）、落在尺度上的占比
- **R10 调色板：1–2 个主色 + 少量强调色 + 8–10 阶灰，每色有成套色阶**
  - 好 / 坏对：同一个仪表盘
    - 好：蓝色系 9 阶 + 灰 9 阶 + 红 / 绿各 1 个语义色
    - 坏：7 个互不相关的色相，外加 `lighten()` 临时调出来的随机浅色
  - 可检查性：**DOM**。抽取所有 computed 颜色 → 按 HSL 色相聚类；非灰色相簇数；同簇内是否构成有序明度阶
- **R11 阴影大小与 elevation 单调对应**
  - 好 / 坏对：同一页
    - 好：卡片小阴影 < 下拉菜单 < 模态框最大阴影
    - 坏：卡片阴影比模态框还重
  - 可检查性：**DOM**。z-index / 层叠顺序 与 shadow blur 的秩相关
- **R12 避免歧义间距（p83）**：同 W1，DOM 可查

### Gaps
- 书正文（间距尺度具体值、字号尺度、行长 45–75 字符、阴影分级）未能一手核对，只有目录和官方节选
- Medium 文章的原始发布日期未核实：只确认了 2020 年的 Wayback 快照
- Steve Schoger 的推文系列（大量单张 before/after 图）未抓取：X/Twitter 不可抓

---

## Q3 Lidwell, Holden & Butler《Universal Principles of Design》：相关条目与实证

### Takeaway
本次读到的是 Pocket 版（Rockport）全文：每个条目先给一句定义，再给 4–6 条要点。它对对齐、接近、相似、信噪比、图底、一致性的表述很适合直接转成规则。它还明确给出了两条"反规则"：golden ratio 的偏好证据很弱；颜色分组最多 3–4 色。Pocket 版不带参考文献，所以每个条目的实证引用（Kurosu & Kashimura 等）本次未能一手核对。

### Cited Findings
（以下原文都来自 Pocket 版全文 **[一手]** — [archive.org: The Pocket Universal Principles of Design](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)；完整版 Signal-to-Noise 条目在 2010 修订版 ch.106 — [O'Reilly](https://oreilly.com/library/view/universal-principles-of/9781592535873/xhtml/ch106.html)）
- **Alignment**："The placement of elements such that edges line up along common rows or columns, or their bodies along a common center."
  - "Left- and right-aligned text blocks provide better alignment cues than center-aligned text blocks."
  - "Justified text provides more alignment cues than unjustified text, and should be used in complex compositions with many elements."
  - "Treat the edges of the design medium (e.g., edge of a page) and the natural positions on the medium (e.g., centerlines) as alignment elements."
  - "Align every element in your designs with one or more other elements. This will improve the design's perceived stability and overall aesthetic."
- **Proximity**（#108）："Things that are close together are perceived to be more related than things that are farther apart."
  - "Proximity is one of the most powerful means of indicating relatedness in design, and will generally overwhelm competing visual cues."
  - "Degrees of proximity imply degrees of relatedness."
  - "touching or overlapping elements are interpreted as sharing one or more attributes; whereas proximal but nontouching elements are interpreted as related but independent."
  - "Ensure that labels and supporting information are near the elements they describe. Favor direct labeling over legends or keys."
- **Similarity**（#127）："Things that are similar are perceived to be more related than things that are dissimilar."
  - "Color similarity is an effective grouping strategy when there are no more than 3-4 colors, and the design is still usable by the color blind."
  - "Use the fewest colors and simplest shapes possible for the strongest grouping effects"
- **Signal-to-Noise Ratio**（#126）："The ratio of relevant to irrelevant information. Good designs have high signal-to-noise ratios."
  - "Signal degradation occurs when information is presented inefficiently: unclear writing, inappropriate graphs, unnecessary elements, or ambiguous icons."
  - "Maximize signal-to-noise ratio in design. Increase signal by keeping designs simple … redundant coding and highlighting. Minimize noise by removing unnecessary elements, and minimizing the expression of elements."
  - 图注："Reduce noise in graphs by removing unnecessary elements and quieting the expression of necessary elements."
- **Figure-Ground**（编号推断为 #049）："Elements are perceived as either figures (objects of focus) or ground"
  - "Figure elements receive more attention and are better remembered than ground elements."
  - "Elements below a horizon line or in the lower regions of a design are more likely to be perceived as figures."
  - "Clearly differentiate between figure and ground elements to focus attention and minimize perceptual confusion."
- **Hierarchy**（编号推断为 #067）："three types of hierarchical structures: trees, nests, and stairs"
  - "Nest structures locate child elements within parent elements … used to group information"
  - "Stair structures stack child elements vertically below parent elements, as in an outline"
- **Consistency**（编号推断为 #027）
  - "Make things aesthetically consistent to enhance recognition and communicate membership."
  - "Make things internally consistent to improve usability, and to signal that a thing has been well designed and not cobbled together."
- **Aesthetic-Usability Effect**（#005）："Aesthetic things are perceived to be easier to use than ugly things."
  - "often subjectively rated as easier to use, even when no usability advantage can be objectively measured"
  - "more tolerant when problems are encountered"
- **Golden Ratio**（编号推断为 #061）："approximating 0.618"
  - "The prevalence of golden proportions over other proportions may, however, be illusory—a result of cherry-picked evidence and confirmation bias."
  - "Psychological evidence supporting a preference for golden proportions over other proportions is weak. If a preference exists, it is small."
  - "Explore golden ratio proportions in your designs, but not at the expense of other design objectives."
- **完整版条目的实证引用 [未核实]**（凭记忆，Pocket 版不带参考文献）
  - Aesthetic-usability：Kurosu & Kashimura 1995（CHI，"Apparent usability vs. inherent usability"，日本 ATM 界面）；Tractinsky 1997（CHI，以色列复制实验）；Tractinsky, Katz & Ikar 2000（*Interacting with Computers*，"What is beautiful is usable"）
  - Golden ratio 的心理学证据综述：Green 1995（*Perception*）
  - 反向证据：Tuch 等 2012（*Computers in Human Behavior*）发现可用性反过来影响美感评价
  - 以上均需核对原文

### Inferences
- **U1 对齐优先左 / 右对齐，而不是居中**
  - 好 / 坏对：同一篇多段落正文
    - 好：左对齐
    - 坏：多段长文全部居中
  - 可检查性：**DOM**。行数 > 3 的文本块里 `text-align:center` 的占比
- **U2 标签贴近被描述对象，图表优先直接标注**
  - 好 / 坏对：同一张多系列折线图
    - 好：系列名直接标在线尾
    - 坏：右下角图例，配 6 种相近颜色
  - 可检查性：**DOM**（SVG/HTML 图表可算 label–mark 距离）**+ VLM**（canvas / 位图图表）
- **U3 颜色分组 ≤ 3–4 种**
  - 好 / 坏对：同一组分类标签
    - 好：3 色
    - 坏：9 色彩虹
  - 可检查性：**DOM**。分类色（badge/tag/legend 背景色）的唯一色相数
- **U4 信噪比：去掉多余元素、弱化必要元素的表现**
  - 好 / 坏对：同一个数据仪表盘
    - 好：浅色细网格线、无 3D、无装饰渐变
    - 坏：粗黑网格、3D 柱、阴影、渐变、装饰图标
  - 可检查性：**DOM + VLM**
    - DOM 代理指标：装饰性元素数、边框 / 阴影 / 渐变数、颜色数
    - VLM："哪些元素不承载信息"
- **U5 图底分明**
  - 好 / 坏对：同一个 hero
    - 好：大标题压在照片上，但有 40% 黑色遮罩
    - 坏：无遮罩，文字直接压在杂乱的照片上
  - 可检查性：**PIX**。按文字 bbox 采样截图背景像素，算局部对比度和纹理方差（DOM 不知道图片内容）**+ VLM**
- **U6 内部一致性（"not cobbled together"）**：同 W3，**DOM**
- **U7 反规则：不要因为 1.618 比例给页面加分**：rubric 应显式排除"黄金比例"类评分项（UPD 原文说证据弱）
- **U8 Aesthetic-usability 是 rubric 的"存在理由"，不是一条检查项**：可用于说明为什么美感分会影响用户对可用性的判断

### Gaps
- 完整版（2003 / 2010 / 2023 第 3 版）各条目的参考文献未能一手核对：O'Reilly 不可抓，archive.org 上只有中文版 `shejidefazeunive0000lidw` 和 Pocket 版
- Pocket 版的出版年份未核实：文中图表数据到 2012，推测为 2015 年左右
- 部分条目编号是按相邻条目推断的

---

## Q4 Gestalt 感知科学（Wagemans et al. 2012）、Arnheim、Dondis

### Takeaway
感知科学给出的不只是"接近 / 相似"这些名称，还有可量化的结论：
- **Pure Distance Law**：接近性分组只由**相对距离**决定，与网格整体结构无关。所以 rubric 应该检查"组间/组内距离比"，而不是绝对像素
- **接近和相似的效应是可加的**：两个线索冲突时会产生歧义，所以 rubric 应该检查"线索是否一致"

Arnheim 提供了"视觉重量"的来源清单（大小、颜色、孤立、规则形状、内在兴趣、位置），适合做截图级的平衡判断。Dondis 本次未能核实。

### Cited Findings
- **出处**：Wagemans J, Elder JH, Kubovy M, Palmer SE, Peterson MA, Singh M, von der Heydt R. "A Century of Gestalt Psychology in Visual Perception I. Perceptual Grouping and Figure-Ground Organization." *Psychol Bull.* 2012 Nov;138(6):1172–1217. doi:10.1037/a0029333 **[一手]** — [PMC3482144](https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/)（PMC 有 reCAPTCHA，经 [Wayback](https://web.archive.org/web/2023/https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3482144/) 读取全文）
  - 原则清单："classical (e.g., proximity, similarity, common fate, good continuation, closure, symmetry, parallelism) and new (e.g., synchrony, common region, element and uniform connectedness)"
  - 相似性："all else being equal, the most similar elements (in color, size, and orientation …) tend to be grouped together"
  - 共同命运："all else being equal, elements that move in the same way tend to be grouped together"；"both common fate and proximity can actually be considered special cases of similarity grouping, with velocity and position as the relevant properties"
  - Common region（§3.2.3）："the tendency for elements that lie within the same bounded area (or region) to be grouped together (Palmer, 1992)"
  - Element connectedness（Palmer & Rock 1994）："Connectedness can be considered as the limiting case of the classic factor of proximity"
  - 量化定律（§3.3）
    - "the outcome is determined by the relative distance alone, not by the angle between the competing organizations"，即 **Pure Distance law**（Kubovy et al. 1998）
    - "when grouping by proximity and grouping by similarity are concurrently applied to the same pattern, the two principles are combined additively"（Kubovy & van den Berg 2008）
  - 图底（§5.2 / §5.3）
    - 经典构形线索："convexity, symmetry, small region, surroundedness"
    - 新线索："lower region, top-bottom polarity, extremal edges and gradient cuts, edge-region grouping, articulating motion, advancing region motion, contour entropy"
  - Prägnanz："the perceptual field and objects within it will take on the simplest and most encompassing ('ausgezeichnet') structure permitted by the given conditions"
- **与 UPD 的张力**：UPD 说 proximity "will generally overwhelm competing visual cues"；Wagemans 综述的实验结果是接近和相似**可加地权衡**，而不是一方总是压倒另一方 — [Pocket UPD](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)；[Wagemans 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/)
- **Arnheim《Art and Visual Perception: A Psychology of the Creative Eye, The New Version》**（UC Press, 1974；初版 1954）。全文取自 archive.org 社区上传本 **[一手]** — [archive.org](https://archive.org/details/art-and-visual-perception-rudolf-arnheim)
  - 第 I 章 "Balance" 目录："Why balance? 20. Weight, 23. Direction, 26. Patterns of balance…"
  - Why balance："An unbalanced composition looks accidental, transitory, and therefore invalid. Its elements show a tendency to change place or shape…"；"In a balanced composition all such factors as shape, direction, and location are mutually determined in such a way that no change seems possible"
  - Weight（约 p.23–25）
    - 大小："Weight depends also on size. Other factors being equal, the larger object will be the heavier."
    - 颜色："red is heavier than blue, and bright colors are heavier than dark ones"；"A black area must be larger than a white one to counterbalance it"
    - 内在兴趣："compositional weight is affected by intrinsic interest"（引 Puffer）
    - 孤立："Isolation makes for weight. The sun or moon in an empty sky is heavier than an object of similar appearance surrounded by other things."
    - 形状："The regular shape of simple geometrical figures makes them look heavier."
    - 位置：
      - 上方更重："weight counts more in the upper part of perceived space than in the lower"
      - 右侧更重（约 p.33–34）："Any pictorial object looks heavier at the right side of the picture."
- **Donis A. Dondis《A Primer of Visual Literacy》**（MIT Press, 1973）：archive.org 条目 `primerofvisualli0000dond` 为借阅受限，全文和 search-inside 均 403 **[一手：元数据]** — [archive.org](https://archive.org/details/primerofvisualli0000dond)
  - 内容 **[未核实]**（凭记忆）
    - 视觉"技法"成对列出：balance/instability、symmetry/asymmetry、regularity/irregularity、simplicity/complexity、unity/fragmentation、economy/intricacy、consistency/variation、sharpness/diffusion 等
    - 把 contrast 视为最核心的技法
    - 有 "sharpening and leveling" 的讨论

### Inferences
- **G1 以距离比而非绝对值判断分组（Pure Distance Law）**
  - 好 / 坏对：同一个 3×3 卡片网格
    - 好：卡片内 12px，卡片间 32px
    - 坏：卡片内 24px，卡片间 20px，结果读成"错误分组"
  - 可检查性：**DOM**。每个容器内 gap 与容器间 gap 的比
- **G2 分组线索须一致**
  - 好 / 坏对：同一张价目表
    - 好：同色即同组，且同组在空间上相邻
    - 坏：颜色按套餐分，间距按功能分，两种线索互相冲突
  - 可检查性：**DOM**（颜色聚类与空间聚类的一致性，如 ARI）**+ VLM**
- **G3 Common region：用容器包裹相关项**
  - 好 / 坏对：同一个设置页
    - 好：5 组设置各有浅底卡片
    - 坏：30 个开关平铺成一长列
  - 可检查性：**DOM**。相关控件是否有共同的可见背景 / 边界祖先
- **G4 图底：模态框、浮层应小、被包围、凸**
  - 好 / 坏对：同一个确认弹窗
    - 好：居中小卡 + 背景遮罩
    - 坏：全宽、无遮罩，与页面同色
  - 可检查性：**DOM**（遮罩元素、尺寸比）**+ VLM**
- **G5 构图平衡（Arnheim）**
  - 好 / 坏对：同一个 hero
    - 好：左文右图，视觉重心接近中轴
    - 坏：大标题、按钮、图片全部挤在左 1/3，右侧空白而且没有任何"重量"
  - 可检查性：**PIX**（用对比度 / 饱和度 / 面积加权的视觉重心偏离中心的距离，可近似 Arnheim 的重量因子）**+ VLM**（最终判断，因为"内在兴趣"无法像素化）
- **G6 孤立制造重量：主 CTA 周围留白**
  - 好 / 坏对：同一个 CTA
    - 好：周围 ≥48px 净空
    - 坏：CTA 夹在 6 个同级链接中间
  - 可检查性：**DOM**。主按钮 bbox 到最近兄弟元素的距离
- **G7 Prägnanz / 简单性**：整体能否被读成最简结构，**仅 VLM**

### Gaps
- Dondis 原文完全未能核实：借阅受限
- Wagemans Part II（理论基础）未读
- Arnheim 引文的精确页码以目录页码推断（Weight 一节从 p.23 起），OCR 文本没有逐页页码

---

## Q5 色彩：Albers、Itten、60-30-10、设计系统的色彩克制

### Takeaway
- **色彩经典的核心是"相对性"**（Albers），以及"面积与明度的平衡"（Itten 的 contrast of extension）。所以色彩判断必须在**渲染后的截图**上做，DOM 里的 hex 值不够
- **60-30-10 没有可考的源头**，只是室内设计的民间经验，rubric 里最多作为弱启发
- **设计系统层面**，Apple HIG 明确要求色彩克制和语义一致；Material 3 用成对的 color roles（X / On X / X Container）把对比度编进 token；Carbon 用 4 层 layering 管理表面色

### Cited Findings
- **Albers《Interaction of Color》（Yale, 1963）**：开篇为 "In visual perception a color is almost never seen as it really is — as it physically is. This fact makes color the most relative medium in art."，后接 color "deceives continually" **[二手]**：多个机构页面复述，包括 Albers Foundation、MIT List — [Josef & Anni Albers Foundation](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)；[MIT List](https://listart.mit.edu/node/1124)
- **Itten 七种对比**
  - 七种：contrast of hue、light-dark、cold-warm、complementary、simultaneous、saturation、extension（第 7 种来自 Goethe）**[二手]** — [Wikipedia: Johannes Itten](https://en.wikipedia.org/wiki/Johannes_Itten)
  - Contrast of extension：按 Goethe 的明度值，yellow 9 : orange 8 : red 6 : violet 3 : blue 4 : green 6；求和谐面积要用**倒数**，例如黄:紫 面积 = 1:3 **[二手]** — [OLLI color theory handout (PDF)](https://www.olli-dc.org/uploads/PDFs/2024_Spring/599_Miklitsch/599colortheoryweek3handout.pdf)；[Univ. Catania paper (PDF)](https://www.iris.unict.it/retrieve/dfe4d229-1aaa-bb0a-e053-d805fe0a78d9/17_CCS_Itten.pdf)
  - 争议
    - Catania 论文指出这组数值可能源自 Schopenhauer 而非 Goethe
    - 分光光度测量得到的比例与 Itten 的 9:8:6:3:4:6 有量化差异
    - Itten 自己称这些值是近似值
    - **[二手]** — [Catania paper](https://www.iris.unict.it/retrieve/dfe4d229-1aaa-bb0a-e053-d805fe0a78d9/17_CCS_Itten.pdf)；[Color Culture and Science Journal](https://jcolore.gruppodelcolore.it/ojs/index.php/CCSJ/article/view/ccsj.i82017.02)
  - Itten 原书（`elementsofcolort00itte`、`artofcolorsubjec00itte`）在 archive.org 受限（401）**[一手：元数据]**
- **60-30-10 规则**
  - 所有能找到的来源都只说"来自室内设计、历史悠久"，没有任何来源给出发明人、年代或原始文献；都是博客、家居媒体在互相转述 **[二手]** — [Apartment Therapy](https://www.apartmenttherapy.com/interior-design-rule-60-30-10-explained-37504313)；[Homebuilding.co.uk](https://www.homebuilding.co.uk/home-improvements/60-30-10-rule)；[Gulf News](https://gulfnews.com/amp/friday/home/60-30-10-the-one-simple-rule-for-your-perfect-home-colour-palette-1.1646387851196)
  - Web 化的转述：60% 主色 / 中性背景、30% 辅色、10% 强调色（CTA） **[二手]** — [Paige Brunton](https://paigebrunton.com/blog/60-30-10-color-rule-for-web-designers/)
  - 设计师自己也称其为 guideline，"not always an exact mathematical equation" **[二手]** — [Homebuilding.co.uk](https://www.homebuilding.co.uk/home-improvements/60-30-10-rule)
- **Apple HIG – Color [一手]** — [developer.apple.com/design/human-interface-guidelines/color](https://developer.apple.com/design/human-interface-guidelines/color)（经官方 DocC JSON 读取）
  - "Avoid using the same color to mean different things. Use color consistently throughout your interface, especially when you use it to help communicate information like status or interactivity."
  - "if you use your brand color to indicate that a borderless button is interactive, using the same or similar color to stylize noninteractive text is confusing."
  - "Apply color sparingly … reserve it for elements that truly benefit from emphasis, such as status indicators or primary actions. … Refrain from adding color to the background of multiple controls."
  - "too much color can be overwhelming and make control labels more difficult to read"；内容本身色彩丰富时 "prefer a monochromatic appearance for toolbars and tab bars"
  - visionOS："Use color sparingly, especially on glass."
  - "Avoid relying solely on color to differentiate between objects, indicate interactivity, or communicate essential information."
  - "insufficient contrast can cause icons and text to blend with the background"
  - "Avoid redefining the semantic meanings of dynamic system colors."
- **Material 3 color roles [一手]**：官方 MDC-Android 文档与 material-web 文档；m3.material.io 是 SPA，WebFetch 只拿到标题
  - "Color creates meaning and communicates hierarchy, state, and brand."；color scheme = "key color tones assigned to specific roles that get mapped to components" — [material-web docs/theming/color.md](https://github.com/material-components/material-web/blob/main/docs/theming/color.md)
  - "three accent color groups (Primary, Secondary, Tertiary), each with 4-5 color roles"
  - 角色成对出现，基线色调示例（light / dark）：
    - Primary = primary40 / 80，On Primary = white / primary20
    - Primary Container = primary90 / 30，On Primary Container = primary10 / 90
    - Error 组同理
    - 来源 — [MDC-Android Color.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md)
- **IBM Carbon – Color layering [一手]** — [carbondesignsystem.com/elements/color/usage](https://carbondesignsystem.com/elements/color/usage/)
  - "There are four layers within a theme: base layer, layer 01, layer 02, and layer 03. Layers stack one on top of the other in a set order."
  - "A field is considered a layer on top of the background it is placed on"
  - "Non-layer tokens [type, icons] will be the same across variants because they have enough contrast"
- **WCAG 对比度门槛**：正文 4.5:1（另有大字 3:1、非文本 UI 3:1）。Proper Sky 报告将 "Don't be a wimp" 的下限定为 "4.5 : 1 for body text" **[二手]** — [Proper Sky PDF](https://brand.propersky.com/assets/downloads/TNDDB-Applied.pdf)；WCAG 原文本次未抓取 **[未核实]**

### Inferences
- **C1 色彩在语境中判断（Albers 相对性）**
  - 好 / 坏对：同一个品牌橙按钮
    - 好：放在白底上，鲜亮
    - 坏：放在浅橙 / 米黄底上，发灰、发脏；或者同一个 #888 在深底和浅底上，明暗感完全相反
  - 可检查性：**PIX + VLM**。DOM 能算 WCAG 对比度，但无法给出"感知色偏 / 发脏"；同时对比效应只能在截图上判
- **C2 高明度、高饱和色只占小面积（Itten extension）**
  - 好 / 坏对：同一个促销页
    - 好：深紫大面积背景，亮黄只用于 CTA 和价格
    - 坏：亮黄铺满全屏背景，紫色当小字
  - 可检查性：**PIX**。按像素统计高饱和、高明度色相的面积占比
- **C3 主 / 辅 / 强调的面积分层（60-30-10 作为弱启发）**
  - 好 / 坏对：同一个 SaaS 落地页
    - 好：中性底约 60%+，品牌色块约 30%，强调色仅 CTA 约 ≤10%
    - 坏：三种颜色各占三分之一
  - 可检查性：**PIX**。截图像素按色相聚类后的面积分布
  - 注意：没有经典出处，权重应低，且不应要求精确比例
- **C4 一色一义（HIG）**
  - 好 / 坏对：同一个文档页
    - 好：品牌蓝只用于可点击元素
    - 坏：品牌蓝同时用于链接、不可点击的小标题和装饰图标
  - 可检查性：**DOM**。可交互元素（a / button / [role=button] / cursor:pointer）的文字色集合，与不可交互文字的色集合的交集
- **C5 彩色背景只给一个主控件（HIG + RUI R5）**
  - 好 / 坏对：同一个工具栏
    - 好：只有 "Done" 是实心强调色
    - 坏：5 个按钮全是实心彩色
  - 可检查性：**DOM**
- **C6 不只靠颜色传达信息**
  - 好 / 坏对：同一个状态列表
    - 好：红点 + "Failed" 文字 + 图标
    - 坏：只用红 / 绿圆点
  - 可检查性：**DOM**（状态元素是否带文本或 aria-label / 图标）**+ VLM**
- **C7 "On X" 配对 / 前景与底色成对设计（M3）**
  - 好 / 坏对：同一个主色按钮
    - 好：文字用 on-primary（白，对比度 ≥ 4.5:1）
    - 坏：文字用 primary 的浅色阶，对比度约 2:1
  - 可检查性：**DOM**。逐个文本节点算 WCAG 对比度（背景要沿祖先链取实色；遇到图片背景时转 PIX）
- **C8 表面层级逐层步进（Carbon layering）**
  - 好 / 坏对：同一个嵌套面板
    - 好：页面 → 卡片 → 卡内输入框，每层背景色明度只差一档
    - 坏：嵌套层用跳跃的、不相关的底色，或全部同色，只能靠边框区分
  - 可检查性：**DOM**。嵌套容器背景色的明度序列是否单调且步长小

### Gaps
- Albers 和 Itten 原书均未能一手阅读：版权受限
- 60-30-10 的真实起源未找到，可以明确写"无可靠出处"
- Shopify Polaris 的色彩指南未能获取：polaris.shopify.com 已重定向到 shopify.dev 的 API 参考页，polaris-react.shopify.com 返回的是空壳
- m3.material.io 上 color roles 页的正文（例如 "on" 颜色用法的原句）未能渲染

---

## Q6 设计系统作为"成文的审美"：间距、字号、elevation、圆角

### Takeaway
主流设计系统都把审美写成了**离散 token**：
- **Carbon**：13 级间距（2–160px），配套理由"有意图的空白"
- **Material 3**：15 个字号角色、圆角 0/4/8/12/16/20/28/32/48dp/全圆、6 级 elevation 0/1/3/6/8/12dp
- **Apple HIG**：用文字规定层级（按重要性排序）、对齐（缩进表达从属）、分组（留白 / 容器 / 分隔线）

这些 token 让"是否取自一套尺度、唯一值是否少"成为可以直接用 DOM 判定的规则。

### Cited Findings
- **Carbon 间距 [一手]** — [carbondesignsystem.com/elements/spacing/overview](https://carbondesignsystem.com/elements/spacing/overview/)
  - 尺度：`$spacing-01..13` = 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 160 px
  - 与网格的关系："complements the 2x Grid and typography scale by using multiples of two, four, and eight"
  - 理由与规则
    - "Every part of a UI should be intentional including the empty space between elements."
    - "deviating from the spacing scales should be avoided whenever possible"
    - "it is acceptable at page breakpoints to jump a step(s) on the spacing scale"
    - "As more space is added between elements, their perceived relationship weakens."
    - "Elements that have more spacing around them tend to be perceived as higher in importance."
    - "White space helps with information processing"
- **Carbon 字体 [一手]** — [carbondesignsystem.com/elements/typography/type-sets](https://carbondesignsystem.com/elements/typography/type-sets/)
  - 两套字号："The productive type set uses a base type size of 14px, while the expressive type set uses a base type size of 16px."
  - body-long 样式："It is always left-aligned."
  - fluid / display 标题："Do not use these styles inside a container."
- **Material 3 字号尺度 [一手]** — [MDC-Android Typography.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Typography.md)
  - Display L / M / S：57 / 45 / 36sp
  - Headline：32 / 28 / 24sp
  - Title：22sp（Regular）/ 16 / 14sp（Medium）
  - Body：16 / 14 / 12sp（Regular）
  - Label：14 / 12 / 11sp（Medium）
  - 另有 Emphasized 变体，只提一级字重（Regular→Medium，Medium→Bold）
- **Material 3 圆角尺度 [一手]** — [MDC-Android Shape.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Shape.md)
  - None 0dp、ExtraSmall 4、Small 8、Medium 12、Large 16、LargeIncreased 20、ExtraLarge 28、ExtraLargeIncreased 32、ExtraExtraLarge 48、Full 50%
  - 全局共用一个 `shapeCornerFamily`（rounded / cut）
- **Material 3 elevation [一手：官方代码]**：Compose `ElevationTokens` 中 Level0..Level5 = 0, 1, 3, 6, 8, 12 dp — [androidx ElevationTokens.kt](https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/ElevationTokens.kt)
  - 有第三方资料称 M3 主要用 tonal surface 表达 elevation、阴影只留给浮层；也有资料称 2023 年后改为 surface-container 角色。两说冲突，官方原文未核实 **[二手]** — [docs.rs frust-material metrics.rs](https://docs.rs/crate/frust-material/latest/source/src/tokens/metrics.rs)
- **Material 3 4dp 间距网格**：只有第三方 token 包这样写，m3 官方页未能读取 **[二手]** — [pub.dev material_design](https://pub.dev/packages/material_design/versions/0.7.1)
- **Apple HIG – Layout [一手]** — [developer.apple.com/design/human-interface-guidelines/layout](https://developer.apple.com/design/human-interface-guidelines/layout)
  - 排序："Order content by relative importance … place the most important items near the top and leading side of the window"
  - 对齐与缩进："Align elements to make them easier to scan, and use indentation to convey hierarchy. … People assume that aligned items are related to each other, and conversely, they perceive indented items as subordinate to the item they follow."
  - 分组："Group related items … you might use negative space, container shapes, or separator lines"
  - 渐进披露："Use progressive disclosure … An interface with too much content and too many choices makes it harder to find information quickly"
  - 区分控件与内容："Differentiate controls from content."
- **"8pt grid" 的源头**：本次未找到一手出处。Carbon 原文是 "multiples of two, four, and eight"（见上）**[一手]**；常被引用的 Bryn Jackson "The 8-Point Grid"（spec.fm, 2016）**[未核实]**

### Inferences
- **D1 间距 token 化**：同 R8，以 Carbon 13 级或 4/8 倍数为参照，**DOM**
- **D2 字号角色数受限**
  - 好 / 坏对：同一篇文章页
    - 好：只用 display / headline / title / body / label 中的 5–7 种
    - 坏：14 种字号
  - 可检查性：**DOM**
- **D3 圆角一致且取自尺度**
  - 好 / 坏对：同一组组件
    - 好：按钮、输入框 8px，卡片 12px，对话框 28px（按组件尺寸分级）
    - 坏：同一级组件混用 3 / 5 / 6 / 10 / 14px
  - 可检查性：**DOM**。同角色元素 `border-radius` 唯一值数；全页唯一值数（建议 ≤ 3–4）；是否落在 0/4/8/12/16/28 附近
- **D4 elevation 离散分级**
  - 好 / 坏对：同一页
    - 好：全页阴影只有 2–3 种，并与层级对应
    - 坏：每张卡片阴影都不同
  - 可检查性：**DOM**。`box-shadow` 唯一值数及其与层叠顺序的单调性
- **D5 长段落左对齐（Carbon body-long + UPD Alignment）**：同 U1，**DOM**
- **D6 重要内容在顶部 / 前沿（HIG）**
  - 好 / 坏对：同一个产品页
    - 好：主信息和主 CTA 在首屏左上
    - 坏：首屏是大图，主 CTA 在第三屏
  - 可检查性：**DOM**（主 CTA 的 y 坐标 / 是否在首屏）**+ VLM**
- **D7 缩进表从属**
  - 好 / 坏对：同一个嵌套列表
    - 好：子项缩进 16–24px
    - 坏：子项与父项同一左边线，只靠字号区分
  - 可检查性：**DOM**
- **跨源汇总**：可以由程序判定的规则（DOM / PIX）约占上面规则卡的 2/3。只有 VLM 能判的集中在四类：焦点 / 第一眼、构图平衡的最终判断、色彩在语境中的观感（Albers）、Prägnanz / 整体简洁度

### Gaps
- Shopify Polaris 的间距 / 色彩 / 圆角 token 本次未能获取（站点迁移）。印象中 Polaris 以 4px 为基准（`space-100` = 4px），但 **[未核实]**
- m3.material.io 官方页面（spacing、elevation、color roles 正文）是 JS 渲染，未能读取；M3 数值取自官方 Android / Compose 仓库代码与文档
- Apple HIG 没有给出 Web 适用的具体间距尺度（Layout 页只有 tvOS 安全边距 60 / 80pt 等平台数值）

