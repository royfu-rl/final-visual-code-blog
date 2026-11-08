# 视觉 / UI 设计书籍对 A1–A10 审美 rubric 的覆盖度

> 图例
> - 核实等级
>   - **一手**：本次（或前序笔记）读到原文、官方目录或出版社页面
>   - **二手**：搜索摘要、书评、课程讲义、其他版本的图书馆目录
>   - **未核实**：凭记忆或推断，本次没找到原文
> - 覆盖强度：● 有专门章节 / 条目直接讲；◐ 顺带讲到或只讲一部分；○ 没找到
> - 规则：A1 视觉层级 · A2 对齐 · A3 接近 / 分组 · A4 行长与行距 · A5 字号尺度与字体数 · A6 色彩克制（中性底 + 一个强调色留给主操作）· A7 文字对比 / 可读 · A8 组件样式一致 / 重复 · A9 信噪比（无信息的装饰）· A10 贴合品牌的独特视觉身份
> - 已有笔记（`visual_principles_color.md`、`typography_layout_canon.md`）里的 RUI 目录页码、UPD 条目原文、Williams 四原则引文、Bringhurst §2.1.2 / §2.2.1 / §3.1.1，本文只引用，不重复展开
> - **关于 archive.org 社区上传本**：Pocket UPD、Lupton《Thinking with Type》第 3 版、Bringhurst v3.0、Krug《Don't Make Me Think》的原文核对用的是 archive.org 上的社区上传扫描本，**授权状态不明（文件名带 z-lib / Anna's Archive 字样）**。它们只用来核对措辞，最终报告应改引官方目录或纸本页码

---

## Q1 覆盖矩阵：每本书 × A1–A10 对应到哪一章 / 哪一节

### Takeaway
- 唯一一本对 A1–A10 每条都有对应章节、而且每条都有一手页码的书是 **Refactoring UI**（下称 RUI，只有官方目录带页码）
- **Universal Principles of Design**（下称 UPD）是唯一能把 A2 对齐、A8 一致、A9 信噪比各对上一个**同名条目**、并且一手核对过原文的书
- 其余书要么只讲印刷 / 排版（Bringhurst、Lupton、Williams），要么偏可用性（Krug、Laws of UX），要么内容对得上但原文无法核对（Mullet & Sano、About Face、Designing Interfaces）

### Cited Findings

**表 1　书目元数据**

| 书 | 首版 → 最新版 | 屏幕 / 印刷 | 原文能否在线核对 |
|---|---|---|---|
| RUI（Wathan & Schoger） | 只有一个版本，年份未核实（印象中是 2018） | 屏幕 / Web | 官方目录带页码（一手）＋官方节选＋作者 Medium 文章；正文要付费 — [refactoringui.com/book](https://www.refactoringui.com/book) |
| UPD（Lidwell, Holden, Butler） | 2003 → Revised & Updated 2010 → "Updated and Expanded Third Edition"（O'Reilly 有条目，年份未核实）；另有 Pocket 版 150 条 | 跨学科通用，非 Web 专书 | Pocket 版全文有 archive.org 社区本；完整版只有 O'Reilly 条目 — [O'Reilly 2010](https://oreilly.com/library/view/universal-principles-of/9781592535873)；[O'Reilly 3rd ed](https://oreilly.com/library/view/universal-principles-of/9780760375174)；[archive.org Pocket](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools) |
| Williams《The Non-Designer's Design Book》 | 1994 → 第 4 版（Peachpit，2014-11-20 出版，©2015） | 印刷为主（第 8 章 Extra Tips & Tricks） | Pearson 官方目录（一手）；1994 版在 archive.org 借阅受限 — [Pearson](https://www.pearson.com/en-us/subject-catalog/p/non-designer-s-design-book-the/P200000000691)；[archive.org 1994](https://archive.org/details/nondesignersdesi00will) |
| Mullet & Sano《Designing Visual Interfaces》 | 1995，只有一个版本（SunSoft Press / Prentice Hall） | 屏幕（1990 年代 GUI：对话框、图标、窗口） | archive.org 借阅受限，元数据里的目录只到第 3 章 — [archive.org](https://archive.org/details/designingvisuali00mull) |
| Cooper 等《About Face》 | 1995 → 2.0（2003）→ 3（2007）→ 第 4 版（Wiley，2014） | 屏幕（桌面、移动；第 20 章讲 Web） | archive.org 借阅受限；第 4 版目录在 Kinokuniya 有一手页码 — [archive.org](https://archive.org/details/aboutfaceessenti0000coop)；[Kinokuniya](https://www.kinokuniya.co.jp/f/dsg-12-EY00060894) |
| Tidwell 等《Designing Interfaces》 | 2005 → 2011 → 第 3 版（O'Reilly，2019-12；零售标 2020） | 屏幕 / Web / 移动 | O'Reilly 403；第 3 版第 5 章的节名只拿到书店转录（二手） — [archive.org 2011](https://archive.org/details/designinginterfa0000tidw_r7u8)；[O'Reilly 3rd](https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954) |
| Lupton《Thinking with Type》 | 2004 → 2010 → 第 3 版 Revised and Expanded（扫描本标 2023；导言说首版之后 "Twenty years later"） | 印刷＋屏幕（第 3 版新增 Responsive Layouts、Inclusive Design） | 第 3 版社区扫描本（全文）；第 2 版 archive.org 借阅受限 — [archive.org 3rd 社区本](https://archive.org/details/20260126_20260126_1723)；[archive.org 2nd](https://archive.org/details/thinkingwithtype0000lupt_h9e8) |
| Lupton & Phillips《Graphic Design: The New Basics》 | 2008 →（第 2 版 2015，未核实） | 平面基础，非 Web 专书 | archive.org 元数据有第 1 版目录（一手） — [archive.org](https://archive.org/details/graphicdesignnew0000lupt) |
| Krug《Don't Make Me Think》 | 2000 → 2006 → Revisited（第 3 版，2014） | Web / 移动可用性 | archive.org 借阅本元数据（一手）＋社区扫描本 — [archive.org 2014](https://archive.org/details/dontmakemethinkr0000krug)；[社区本](https://archive.org/details/SteveKrugDontMakeMeThink) |
| Bringhurst《The Elements of Typographic Style》 | 1992 → 1996 → v3.0（2004）→（v4.0 2012，未核实） | 印刷 / 书籍排版 | v3.0 社区扫描本（全文）＋ webtypography.net 转录（第 2–3 章）— [社区本](https://archive.org/details/the-elements-of-typographic-style-robert-bringhurst-z-lib.org)；[webtypography.net](http://webtypography.net/toc/) |
| Yablonski《Laws of UX》 | 第 1 版 2020-04（二手）→ 第 2 版 2024（作者页写 "March 2024"，O'Reilly 标 January 2024） | 屏幕 UX 心理学 | 作者页没有目录 — [作者页](https://jonyablonski.com/articles/2024/laws-of-ux-the-2nd-edition/)；[lawsofux.com/book](https://lawsofux.com/book/) |
| **（新增）** Dannaway《Practical UI》 | 版次和年份未核实 | 屏幕 / Web / App | 官网有 8 章简介和样例规则（一手）；正文要付费 — [practical-ui.com](https://www.practical-ui.com/) |

**表 2　覆盖矩阵**（格式：强度 / 出处 / 核实等级）

| 书 | A1 层级 | A2 对齐 | A3 分组 | A4 行长行距 | A5 字号与字体数 | A6 色彩克制 | A7 对比 | A8 一致 | A9 信噪比 | A10 身份 |
|---|---|---|---|---|---|---|---|---|---|---|
| RUI | ● p30–52 一手 | ◐ p72 / p102 / p111 一手 | ● p83 一手 | ● p99 / p105 一手 | ● p88 尺度；◐ p94 字体 一手 | ● p119–146＋p52 一手 | ● p36 / p142 / p176 一手 | ◐ p24 / p60 / p129 一手 | ◐ p206（＋p41）一手 | ● p17 一手（内容二手） |
| UPD | ● #069 / #049 / #143 一手 | ● #007 一手 | ● #108 一手 | ● #082 一手 | ◐ #082 一手 | ◐ #127 一手；完整版 Color p48 二手 | ◐ #082 一手 | ● #027 一手 | ● #126 / #096 一手 | ○–◐ #027 / #070（间接）一手 |
| Williams 4e | ● ch5 Contrast 二手 | ● ch3 二手 | ● ch2 二手 | ○ ch9 未核实 | ◐ ch12 Type Contrasts 二手 | ◐ ch7（只有章名）一手 | ○ | ● ch4 Repetition 二手 | ○ | ○ |
| Mullet & Sano | ● Scale, Contrast & Proportion 一手 | ● Organization / Module & Program 二手 | ● Organization 二手 | ○ | ○ | ◐ "Restraint" 一手（是否讲色彩未核实） | ● "Insufficient Contrast" 一手 | ● "Regularizing…" 一手＋grid 二手 | ● "Clutter and Visual Noise" 一手 | ● "Style" 二手 |
| About Face 4e | ● ch17 p411 二手 | ◐ 未核实 | ● ch17 p411 二手 | ○ 未核实 | ◐ 未核实 | ◐ 未核实 | ◐ 未核实 | ● ch17 p428 一手 | ● ch17 二手 | ◐ 未核实 |
| Designing Interfaces 3e | ● ch5 Visual Hierarchy 二手 | ◐ ch4 / Composition 未核实 | ◐ ch4 未核实 | ◐ ch5 Readability 二手 | ◐ ch5 Typography 二手 | ◐ ch5 Color 二手 | ◐ ch5 Accessibility 二手 | ◐ 未核实 | ○ 未核实 | ● ch5 Evoking a Feeling 二手 |
| Lupton TWT 3e | ● Hierarchy and Structure 一手 | ● Aligning Elements / Grids 一手 | ● Grouping 一手 | ● Line Length（约 p128）一手 | ● Type Scale / Choosing / Pairing 一手 | ○ | ◐ Legibility and Readability / Inclusive Design 一手 | ◐ Serial Design 一手（只有节名） | ○ | ◐ Branding with Type 一手 |
| Lupton New Basics | ● Hierarchy / Scale / Figure-ground 一手 | ● Grid 一手 | ○ 未核实 | ○ | ○ | ◐ Color 一手（只有章名） | ○ | ◐ Modularity / Pattern 一手 | ○ | ○ |
| Krug 3e | ● ch3 一手 | ◐ ch3 "grids to align" 一手 | ● ch3 一手 | ○ | ○ | ◐ ch3 / 链接色 一手 | ○ 未核实 | ◐ ch3 conventions 一手 | ● ch3 "noise" 一手 | ○ |
| Bringhurst v3.0 | ◐ §4.2.1–4.2.2 一手 | ◐ ch8 §8.6.1 一手 | ○ | ● §2.1.2 / §2.2.1 一手 | ● §3.1.1 / §6.5.1 一手 | ○ | ○ | ◐ §4.2.2 一手 | ◐ §1.1.1 一手 | ◐ §1.2.4 / §6.4.1 一手 |
| Laws of UX | ◐ von Restorff 二手 | ○ | ○（书里有没有 Gestalt 未核实） | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Practical UI | ● ch8 Buttons 一手（简介） | ● ch4 一手（简介） | ◐ ch4 一手（简介） | ● "40 – 80 characters per line" 一手 | ◐ ch5 一手（简介） | ● ch3 一手（简介） | ◐ 只有泛述 | ● ch4 "consistent spacing system" 一手 | ● ch2 一手（简介） | ○ |

**逐书证据**

- **RUI**：目录页码全部 **一手**，来自 [refactoringui.com/book](https://www.refactoringui.com/book)，前序笔记已列全
  - A1　Hierarchy is Everything 一章：p30 "Not all elements are equal"、p32 "Size isn't everything"、p39 "De-emphasize to emphasize"、p48 "Balance weight and contrast"
    - 作者文章原句："A common mistake when styling UI text is relying too much on font size to control your hierarchy." — [Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)
  - A2　没有"共享边线"专节
    - p72 "Grids are overrated" 反而是在劝人别死守 12 栏网格
    - p102 "Baseline, not center"、p111 "Align with readability in mind" 只讲局部的对齐
  - A3　p83 "Avoid ambiguous spacing"；p56 "Start with too much white space"
  - A4　p99 "Keep your line length in check"；p105 "Line-height is proportional"
    - 正文数字（45–75 字符）**未核实**
  - A5　p88 "Establish a type scale"；p94 "Use good fonts"
    - 有没有讲"用几种字体"**未核实**
  - A6　Color 一章 p119–146；p52 "Semantics are secondary"（按钮按层级上色）
    - "Most sites need one, maybe two colors that are used for primary actions"
    - "almost everything in an interface is grey"
    - 以上两句 — [官方节选](https://www.refactoringui.com/previews/building-your-color-palette)
    - "Most pages only have one true primary action" — [Medium](https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886)
  - A7　p36 "Don't use grey text on colored backgrounds"；p142 "Accessible doesn't have to mean ugly"；p176 "Text needs consistent contrast"
    - 书里有没有写 4.5:1 这个数字：**未核实**
  - A8　没有"重复 / 一致"专节，靠"系统"间接覆盖
    - p24 "Limit your choices"、p60 "Establish a spacing and sizing system"、p129 "Define your shades up front"
  - A9　p206 "Use fewer borders"："using too many of them can make your design feel busy and cluttered"；p41 "Labels are a last resort"
    - 同一章又有 p195 "Add color with accent borders"、p198 "Decorate your backgrounds"，**与 A9 存在张力**
  - A10　p17 "Choose a personality"（**一手**：节名）
    - 内容是用字体、颜色、圆角、文案语气来定"个性"，并且要从严肃到俏皮选一个点然后全站坚持（**二手**） — [rfui-docs 摘要](https://rfui-docs.onrender.com/choose-a-personality)；[DEV 摘要](https://dev.to/christianmay21/top-4-design-choices-you-should-make-before-building-a-website-according-to-refactoring-ui-2beo)

- **UPD**：Pocket 版条目原文，本次从社区全文核对 **一手** — [archive.org](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)
  - A1
    - #069 Highlighting："Highlight no more than 10 percent of a visible display. When everything is highlighted, nothing is highlighted."；"Use bold to highlight titles, labels, and short word sequences."
    - #049 Figure-Ground（前序笔记已引）
    - #143 von Restorff Effect（只有条目名）
    - #067 Hierarchy 讲的是 trees / nests / stairs 这类**结构**层级，不是视觉强调
  - A2　#007 Alignment："Align every element in your designs with one or more other elements."（前序笔记）
  - A3　#108 Proximity："Degrees of proximity imply degrees of relatedness."（前序笔记）
  - A4　#082 Legibility
    - "Make line lengths 10-12 words per line, or 35-55 characters per line."
    - "Set leading (space between text lines, baseline to baseline) to the type size plus 1-4 points."
  - A5　#082 Legibility 只讲字号和字体选择："Use 9- to 12-point type for high-resolution media such as print."；"There is no performance difference between serif and sans serif typefaces"
    - **没有** type scale，也没有字体数上限
  - A6
    - #127 Similarity："Color similarity is an effective grouping strategy when there are no more than 3-4 colors"（前序笔记）
    - **Pocket 版没有 Color 条目**（本次读了 150 条的全目录）
    - 完整版 Color 条目在 2010 版 p48，**二手**：UW 课程作业引作 "The Universal Principles of Design (p. 48)" — [UW CSE441](https://courses.cs.washington.edu/courses/cse441/12sp/assignments_files/10-studio-assign5-color.pdf)
    - 常被转述的 "use color conservatively … ~5 colors" **未核实**：只在一份未注明出处的 GMU 讲义里看到 — [GMU SWE432](https://people.cs.gmu.edu/~tlatoza/teaching/swe432f16/Lecture%2027%20-%20Design%20Languages.pdf)
    - 没有"强调色只留给主操作"这一层意思
  - A7　#082："Favor dark text on a light background for optimal legibility. Avoid patterned or textured backgrounds."；#069："Ensure high contrast when using color to highlight."
    - 没有给数值
  - A8　#027 Consistency："Make things aesthetically consistent to enhance recognition and communicate membership."；"Make things internally consistent … not cobbled together."
  - A9
    - #126 Signal-to-Noise Ratio（前序笔记）
    - #096 Ockham's Razor："Applying Ockham's razor means cutting unnecessary elements from a design."；"Proficient designers favor simplicity over ornamentation"
    - #070 Horror Vacui："As horror vacui increases, perceived value decreases."
  - A10　只有间接内容
    - #027 "communicate membership"（这是"一致"，不是"独特"）
    - #070 "Favor minimalism to signal high-priced products"
    - #090 Mimicry 讲的是借用既有形式，方向与 A10 相反

- **Williams 第 4 版**
  - 目录 **一手** — [Pearson](https://www.pearson.com/en-us/subject-catalog/p/non-designer-s-design-book-the/P200000000691)
    - ch1 Introduction · ch2 Proximity · ch3 Alignment · ch4 Repetition · ch5 Contrast · ch6 Review · ch7 Design with Color · ch8 Extra Tips & Tricks
    - ch9 The Essentials of Typography · ch10 Type (& Life) · ch11 Categories of Type · ch12 Type Contrasts · ch13 Does it Make Sense? · ch14 Answers · ch15 Typefaces in this Book
  - A1 / A2 / A3 / A8：四原则的原句见前序笔记，均为**二手**
    - Contrast："If two items are not exactly the same, then make them different. Really different."
    - Alignment："Nothing should be placed on the page arbitrarily…"
  - A5　ch12 Type Contrasts
    - 1994 版图书馆目录里 Concord / Conflict / Contrast 约在 p146 / p148（**二手**）
    - Conflict 指"两种相似但不相同的字体同页"（**二手**） — [ybrikman 书评](https://www.ybrikman.com/blog/2015/01/27/the-non-designers-design-book/)；[O'Reilly 3e ch11](https://www.oreilly.com/library/view/the-non-designers-design/9780321563088/ch11.html)
  - A6　只确认 ch7 Design with Color 这个章名
    - 有没有讲"克制"、"一个强调色"：**未核实**
  - A4 / A7 / A9 / A10：没找到对应内容
    - ch9 是否讲行长、行距：**未核实**

- **Mullet & Sano 1995**
  - ch1–3 的细目 **一手**，来自 archive.org 元数据 — [archive.org](https://archive.org/details/designingvisuali00mull)
    - Elegance and Simplicity
      - Principles：Unity, Refinement, Fitness
      - Common Errors：**Clutter and Visual Noise**, Interference Between Competing Elements, Using Explicit Structure as a Crutch, Belaboring the Obvious, **Excessive Detail and Embellishment**, **Gratuitous Dimensionality**
      - Techniques：Reducing a Design to Its Essence, **Regularizing the Elements of a Design**, Combining Elements for Maximum Leverage
      - 对应 A9、A8
    - Scale, Contrast, and Proportion
      - Principles：Clarity, Harmony, Activity, **Restraint**
      - Common Errors：**Insufficient Contrast**, Excessive Contrast, Visual Interference…
      - Techniques：**The Squint Test**, **Establishing Perceptual Layers**, Sharpening Visual Distinctions
      - 对应 A1、A7、A6（部分）
  - 后 4 章 **二手**：一份 OCR 很差的 Scribd 扫描，加上 SIGCHI Bulletin 1996 书评 — [Scribd](https://www.scribd.com/document/251030693/Designing-Visual-Interfaces)；[SIGCHI 书评](https://homepages.cwi.nl/~steven/sigchi/bulletin/1996.2/book-review.html)
    - Organization and Visual Structure：grouping、hierarchy、balance、symmetry
    - Module and Program：modular units、grid-based layout programs
    - Image and Representation
    - Style
  - 书评转述
    - "Visual elements should be based on a flexible grid so that different screens have a consistent look"（A2 / A8）
    - "For maintaining a graphic style, the forms must be distinctive, integrated, appropriate"（A10）
  - 书评说该书 "only covers principles for design of static dialogue boxes, icons and windows layout"，排版（行长、字号）不是它的议题（A4 / A5 = ○）

- **About Face 第 4 版**
  - ch17 "Integrating Visual Design" p405，**一手**页码 — [Kinokuniya](https://www.kinokuniya.co.jp/f/dsg-12-EY00060894)
    - Visual Art and Visual Design 405
    - The Elements of Visual Interface Design 406
    - **Visual Interface Design Principles 411**
    - Visual Information Design Principles 425
    - **Consistency and Standards 428**
  - ch20 Designing for the Web p569
  - p411 下的原则小标题
    - **二手**（搜索摘要转述的第 3 版 Wiley 目录）："Use visual properties to group elements and provide clear hierarchy"、"Avoid visual noise and clutter" — [GBV 目录 PDF（About Face 2.0；本次 429 打不开）](https://www.gbv.de/dms/ilmenau/toc/607638559.PDF)
    - **未核实**：其余小标题，例如 Text / Color in visual interfaces、Integrate style and function、品牌
  - 内容上可能覆盖面很广，但本次能核对到的只有 A1、A3、A8、A9

- **Designing Interfaces 第 3 版**
  - 第 5 章 "Visual Style and Aesthetics" 的节名，**二手**（书店页的目录转录，经搜索摘要） — [wristers.nl](https://www.wristers.nl/boek/9781492051961)
    - The Basics of Visual Design · Visual Hierarchy · Composition · Color · Typography · Readability · **Evoking a Feeling** · Images · Visual Design for Enterprise Applications · Accessibility
  - 第 4 章（版面 / Gestalt）的节名，以及第 2 版里 "Few Hues, Many Values" 等模式名：**未核实**
  - 第 2 版对应章叫 "Making it look good: visual style and aesthetics"（**二手**，图书馆记录）

- **Lupton《Thinking with Type》第 3 版**：从社区扫描本核对，**一手**；页码由 OCR 页脚推断，误差较大 — [archive.org](https://archive.org/details/20260126_20260126_1723)
  - 目录：Letter / Text / Layout
    - Text：Columns, Lines, and Spacing（Aligning Columns, **Line Length**, Vertical Space…）· **Legibility and Readability** · Hierarchy and Structure（Minimal Hierarchy, Layered Hierarchy, **Type Scale**, Visual and Semantic Hierarchy, **Inclusive Design**）
    - Layout：Balance and Alignment（Symmetry and Asymmetry, **Grouping**, **Aligning Elements**, Borders）· Grids（… Responsive Layouts, Serial Design）
    - Letter：Choosing Typefaces, Type Families, exercise "**Branding with Type**"
  - A4（约 p128）："Opinions vary about readable line lengths. Emil Ruder recommends 50 to 60 characters, John Kane suggests 35 to 65, and Robert Bringhurst prefers 45 to 75. We chose a permissive range (35 to 75)."
  - A5
    - "A type scale is a selection of type sizes based on history or mathematics."；"Working with type scales is a matter of personal preference."
    - "A publication, brand, or website can function beautifully with a single family of typefaces. … Pick a primary typeface or family first, and add other styles as needed."
  - A1："A minimal hierarchy uses just a few weights or sizes of type."
  - A3 / A2："Grouping combines two or more smaller blocks into a bigger set, helping readers connect headlines with articles or captions with images. Aligning elements along their centers or edges creates relationships and builds coherent compositions."
  - A10："When designing a poster, brand identity, or social media campaign, start by choosing a headline font. Look for a memorable typeface with a strong voice."
  - A6 / A9：在这本书里没找到
    - 用 grep 查 "contrast ratio / WCAG" 都没有命中，A7 只有定性讨论

- **Lupton & Phillips《Graphic Design: The New Basics》第 1 版**：目录 **一手** — [archive.org](https://archive.org/details/graphicdesignnew0000lupt)
  - Point, line, plane · Rhythm and balance · **Scale** · Texture · **Color** · **Figure/ground** · Framing · **Hierarchy** · Layers · Transparency · **Modularity** · **Grid** · Pattern · Diagram · Time and motion · Rules and randomness
  - 没有排版（A4 / A5）、可读性（A7）、信噪比（A9）相关的章

- **Krug《Don't Make Me Think》Revisited**
  - 目录 **一手**（archive.org 元数据） — [archive.org](https://archive.org/details/dontmakemethinkr0000krug)
  - 原句来自社区扫描本，**一手** — [社区本](https://archive.org/details/SteveKrugDontMakeMeThink)
  - ch3 "Billboard Design 101" 的小标题
    - Take advantage of conventions · Create effective visual hierarchies · Break pages up into clearly defined areas · Make it obvious what's clickable · Eliminate distractions · Format content to support scanning
  - A1："The more important something is, the more prominent it is. The most important elements are either larger, bolder, in a distinctive color, set off by more white space, or nearer the top of the page"
  - A3："Things that are related logically are related visually. … grouping them together under a heading, displaying them in the same visual style, or putting them all in a clearly defined area."
  - A9："One of the great enemies of easy-to-grasp pages is visual noise."；Shouting 一类噪音："Lots of exclamation points, different typefaces, and bright colors!"
  - A2（作为噪音的一种出现）："Disorganization … a sure sign that the designer doesn't understand the importance of using grids to align the elements on a page."
  - A6（只到链接这一层）：建议所有文字链接用同一种颜色，并把 "using the same color for links and nonclickable headings" 列为低级错误

- **Bringhurst v3.0**：从社区扫描本核对，**一手** — [社区本](https://archive.org/details/the-elements-of-typographic-style-robert-bringhurst-z-lib.org)
  - 章节页码：The Grand Design 17 · Rhythm & Proportion 25 · Harmony & Counterpoint 45 · Structural Forms & Devices 61 · Choosing & Combining Type 93 · Shaping the Page 143
  - A5
    - §6.5.1 "Start with a single typographic family." — "Most pages, and most entire documents, can be set perfectly well with only one family of type."
    - §3.1.1 scale（见前序笔记）
  - A1 / A8
    - §4.2.1 "Set headings in a form that contributes to the style of the whole."
    - §4.2.2 "Use as many levels of headings as you need: no more and no fewer." — "Mixing the two haphazardly leads to stylistic as well as logical confusion."
  - A9　§1.1.1 "Typography exists to honor content." — typography "aspires to a kind of statuesque transparency"
  - A10（只到"字体性格要贴合文本"这一层，与品牌无关）
    - §1.2.4 "Choose a typeface or a group of faces that will honor and elucidate the character of the text."
    - §6.4.1 "Choose faces whose individual spirit and character is in keeping with the text."
  - A2　§8.6.1 "Use a modular scale if you need one to subdivide the page."（页面网格）
  - A4　§2.1.2 / §2.2.1（见前序笔记）

- **Laws of UX**
  - 第 1 版（2020）目录含 Aesthetic–Usability Effect（ch7）、von Restorff Effect（ch8）（**二手**） — [O'Reilly 1e](https://oreilly.com/library/view/laws-of-ux/9781492055303)
  - 第 2 版作者页只列新增概念：Paradox of Choice、Complexity Bias、Flow，以及 Accessibility 等考量；没有提排版、色彩、对齐（**一手**） — [作者页](https://jonyablonski.com/articles/2024/laws-of-ux-the-2nd-edition/)；[lawsofux.com/book](https://lawsofux.com/book/)
  - 网站上有 Gestalt 系列条目，但书里有没有收录：**未核实**

- **Practical UI**（新增）：官网信息，**一手** — [practical-ui.com](https://www.practical-ui.com/)
  - 8 章：1 Fundamentals · 2 Less is more · 3 Colour · 4 Layout and spacing · 5 Typography · 6 Copywriting · 7 Forms · 8 Buttons
  - 各章简介的原句
    - ch2：Less is more —"Practical techniques to simplify interfaces by removing unnecessary details"（A9）
    - ch3："Learn how to use colour sparingly and purposefully to add meaning to an interface"（A6）
    - ch4："Create a consistent spacing system and learn about alignment and layout"（A2 / A8）
    - ch8："descriptive and accessible buttons with a clear visual hierarchy"（A1）
  - 样例规则（A4）："Ensure text is 40 – 80 characters per line (including spaces) to improve readability."
  - 全书宣称有 "100+ design guidelines"

### Inferences
- 只看"有没有专门章节"，**RUI 是 7● + 3◐**，Mullet & Sano 也是 7●，但后者 4 条依据是二手、而且是 1995 年的 GUI 语境；UPD 是 6● + 3◐ + 1 弱，Practical UI 是 6● + 3◐ + 1○，Lupton TWT 是 5● + 3◐ + 2○
- **A10 是区分度最高的一条**
  - 有专门章节的：RUI p17（一手节名）、Mullet & Sano "Style"（二手）、Designing Interfaces "Evoking a Feeling"（二手）
  - UPD、Williams、Krug、Bringhurst 基本不讲"独特 / 贴合品牌"
- **A2 / A9 是 RUI 的短板**
  - p72 "Grids are overrated" 和 p198 "Decorate your backgrounds" 的立场甚至与 A2 / A9 的措辞相反
  - 所以引 RUI 作 A2 / A9 的出处会被挑刺
- **A4 的数字各书不一致**，rubric 要写数值时只能择一引用
  - UPD：35–55 字符
  - Lupton：35–75
  - Bringhurst：45–75（66 最佳）
  - Practical UI：40–80
  - Butterick：45–90（见前序笔记）

### Gaps
- RUI 正文没有在线全文：A4 的 45–75、A7 的 4.5:1、A10 的具体做法，都只能引节名和页码
- UPD 完整版（2010 / 第 3 版）的 Color 条目原文和第 3 版出版年都没能核对：O'Reilly 403
- About Face 第 4 版 ch17 p411 下的原则小标题、Designing Interfaces 第 3 版第 4 章的节名、Mullet & Sano 第 4–7 章的准确标题和页码，都没有一手来源
  - O'Reilly 网页和 TOC API 均 403，Google Books API 当日配额耗尽，GBV 目录 PDF 返回 429
- Williams 第 4 版各章页码、ch7 Design with Color 和 ch9 的内容都未核实
- Lupton TWT 第 3 版的页码来自 OCR 页脚，有错位；出版年（2023 还是 2024）未核实
- Practical UI 的版次 / 年份，以及 ch5 有没有讲字体数和 type scale、有没有讲 4.5:1，都未核实

---

## Q2 哪一本书单独覆盖最多？哪两本组合能以最少重叠覆盖全部十条？

### Takeaway
- **单本最佳是 Refactoring UI**
  - 10 条每条都能落到一个带页码的节名（一手目录）
  - 7 条是专门章节，A2 / A8 / A9 三条偏弱
- **最佳组合是 Refactoring UI + Universal Principles of Design**
  - UPD 用三个同名、一手核对过原文的条目补上 RUI 的三条短板：#007 Alignment、#027 Consistency、#126 Signal-to-Noise（另加 #096 Ockham's Razor）
  - 其余 7 条（A1、A3–A7、A10）全部引 RUI

### Cited Findings
- RUI 对 10 条的页码见 Q1 表 2（**一手**目录） — [refactoringui.com/book](https://www.refactoringui.com/book)
- UPD 补位条目的原文（**一手**，Pocket 版）
  - A2："Align every element in your designs with one or more other elements." — [archive.org Pocket UPD](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)
  - A8："Make things internally consistent to improve usability, and to signal that a thing has been well designed and not cobbled together." — [同上](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)
  - A9："Maximize signal-to-noise ratio in design. … Minimize noise by removing unnecessary elements, and minimizing the expression of elements."；Ockham："Applying Ockham's razor means cutting unnecessary elements from a design." — [同上](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)
- 其他候选组合的比较依据：Q1 表 2
  - RUI + Williams
    - Williams 补 A2 / A8（ch3、ch4），但不补 A9
    - Williams 四原则的原句只有二手来源 — [Pearson 目录](https://www.pearson.com/en-us/subject-catalog/p/non-designer-s-design-book-the/P200000000691)
  - RUI + Krug
    - Krug 补 A9（ch3 "Keep the noise down to a dull roar"）
    - A2 只有一句提到 grids，A8 只是 "conventions"（外部一致，不是同类组件样式一致） — [Krug 社区本](https://archive.org/details/SteveKrugDontMakeMeThink)
  - RUI + Mullet & Sano
    - 内容上补位最强：Clutter and Visual Noise、Regularizing、grid、Style
    - 但这是 1995 年的 GUI 书，archive.org 借阅受限，第 4–7 章只有二手来源 — [archive.org](https://archive.org/details/designingvisuali00mull)；[SIGCHI 书评](https://homepages.cwi.nl/~steven/sigchi/bulletin/1996.2/book-review.html)
  - Lupton TWT + Lupton New Basics
    - 两本合起来覆盖 A1–A5、A6（只有章名）、A10（只到字体）
    - **A9 两本都没有**，A7 没有数值 — [TWT 3e 社区本](https://archive.org/details/20260126_20260126_1723)；[New Basics 目录](https://archive.org/details/graphicdesignnew0000lupt)

### Inferences
- **推荐分配（每条只引一本，零重复引用）**
  - RUI → A1 层级、A3 分组、A4 行长行距、A5 字号尺度、A6 色彩克制、A7 对比、A10 个性
  - UPD → A2 对齐、A8 一致、A9 信噪比
- **重叠评估**
  - 两本在 A1、A3、A4、A7 上都有内容，但分配后不必双引
  - A4 两本数字冲突（UPD 35–55 字符），只引 RUI 可以避开；但 RUI 正文的数字未核实，若 rubric 要写 "45–75"，需要补引 Bringhurst §2.1.2（一手，见前序笔记）
- **为什么不是 RUI + Williams**：Williams 补不了 A9；她的四原则原句至今只有二手来源；书本身面向印刷品
- **为什么不是 RUI + Mullet & Sano**：内容上最互补，可作"学术味更重"的备选；但核实成本高，读者也难以拿到原书
- 如果坚持只用一本，RUI 的 A2、A9 只能引 p72 / p102 / p206 这类边缘节，说服力弱；所以**一本不够，两本刚好**
- **RUI + UPD 仍补不上的两处**
  - A7 的数值门槛（4.5:1）：两本都没有一手数值，要么接受定性表述，要么另引 WCAG（已超出"1–2 本书"）
  - A6 中"强调色只留给主操作"的措辞：RUI 官方节选只说 "one, maybe two colors … for primary actions"，要接受这个近似

### Gaps
- 没能拿到 RUI 正文来确认 A2（p72 的实际立场）和 A9（p206 的完整论述）的细节；推荐组合正是为了绕开这一点
- UPD 第 3 版（"Updated and Expanded"）有没有改动 Alignment / Consistency / Signal-to-Noise 的措辞或编号，未核实；引用时应注明用的是哪一版

---

## Q3 每本书缺哪些规则、哪些只覆盖得很弱？

### Takeaway
- **一句话分组**
  - 偏排版的书（Bringhurst、Lupton TWT）：缺 A6 色彩、A9 信噪比
  - 偏原则 / 可用性的书（UPD、Krug、Laws of UX）：缺 A5 type scale 和 A10 身份
  - Williams：缺 A4 / A7 / A9 / A10
  - RUI：A2 对齐、A9 信噪比偏弱
- **A10 和 A6 是全体样本里最稀缺的两条**

### Cited Findings
（证据和出处同 Q1 逐书证据，这里只列缺口）
- **RUI**
  - 弱：A2，没有"共享边线"专节，p72 "Grids are overrated"
  - 弱：A8，只有 system 类节名，没有"同类组件样式相同"的专节
  - 弱：A9，p206 "Use fewer borders"，同章还有 p195 / p198 鼓励装饰
  - 出处 — [refactoringui.com/book](https://www.refactoringui.com/book)
- **UPD**
  - 缺：A10，只有 #027 "communicate membership"、#070 Horror Vacui 这类间接内容
  - 弱：A5，#082 只讲字号与衬线 / 无衬线，没有尺度、没有字体数
  - 弱：A6，Pocket 版没有 Color 条目，完整版 p48 未核实；没有"强调色留给主操作"
  - 弱：A7，有定性、无数值
  - 出处 — [archive.org Pocket UPD](https://archive.org/details/the-pocket-universal-principles-of-design-150-essential-tools)；[UW CSE441](https://courses.cs.washington.edu/courses/cse441/12sp/assignments_files/10-studio-assign5-color.pdf)
- **Williams 第 4 版**
  - 缺：A9、A10
  - 未找到：A4、A7（ch9 内容未核实）
  - 弱：A5，Type Contrasts 讲字体搭配，不讲尺度
  - 弱：A6，ch7 只确认了章名
  - 出处 — [Pearson](https://www.pearson.com/en-us/subject-catalog/p/non-designer-s-design-book-the/P200000000691)
- **Mullet & Sano**
  - 缺：A4、A5，排版不是该书议题
  - 弱：A6，"Restraint" 原则是否专讲色彩未核实
  - 时代局限：1995 年的 GUI，不讲网页
  - 出处 — [archive.org](https://archive.org/details/designingvisuali00mull)；[SIGCHI 书评](https://homepages.cwi.nl/~steven/sigchi/bulletin/1996.2/book-review.html)
- **About Face 第 4 版**
  - 缺 / 未核实：A4、A5、A6、A7、A10，ch17 小标题拿不到一手来源
  - 能核对的只有 A1、A3（二手）以及 A8（p428，一手）、A9（二手）
  - 出处 — [Kinokuniya](https://www.kinokuniya.co.jp/f/dsg-12-EY00060894)
- **Designing Interfaces 第 3 版**
  - 缺 / 未核实：A9
  - A2 / A3 / A8 依赖第 4 章，节名未核实
  - 其余各条只有第 5 章的节名（二手），没有原句
  - 出处 — [wristers.nl](https://www.wristers.nl/boek/9781492051961)
- **Lupton《Thinking with Type》第 3 版**
  - 缺：A6、A9
  - 弱：A7，没有对比度数值
  - 弱：A8，只有 Serial Design 节名
  - 弱：A10，只讲到字体层面的品牌
  - 出处 — [archive.org 社区本](https://archive.org/details/20260126_20260126_1723)
- **Lupton《Graphic Design: The New Basics》**
  - 缺：A4、A5、A7、A9、A10
  - A3 没有独立章节
  - 出处 — [archive.org](https://archive.org/details/graphicdesignnew0000lupt)
- **Krug**
  - 缺：A4、A5、A10
  - A7 未核实
  - 弱：A2，只作为"Disorganization"一句带过
  - 弱：A6，只讲链接颜色
  - 弱：A8，只讲 conventions
  - 出处 — [Krug 社区本](https://archive.org/details/SteveKrugDontMakeMeThink)
- **Bringhurst v3.0**
  - 缺：A3、A6、A7
  - 弱：A1 / A8，只到标题层级
  - 弱：A2，只到页面网格
  - 弱：A9 / A10，只到"尊重内容、字体性格贴合文本"
  - 定位：印刷书籍排版
  - 出处 — [社区本](https://archive.org/details/the-elements-of-typographic-style-robert-bringhurst-z-lib.org)
- **Laws of UX**
  - 只有 A1（von Restorff）勉强对得上
  - Aesthetic-Usability Effect 是"为什么要有审美分"的理由，不是一条可检查的规则
  - 其余 8–9 条缺失
  - 出处 — [O'Reilly 1e](https://oreilly.com/library/view/laws-of-ux/9781492055303)；[作者页](https://jonyablonski.com/articles/2024/laws-of-ux-the-2nd-edition/)
- **Practical UI**
  - 缺：A10，8 章里没有品牌 / 个性章
  - A3 / A5 / A7 只有章级简介，细则未核实
  - 出处 — [practical-ui.com](https://www.practical-ui.com/)

### Inferences
- 如果只缺 A10 一条，**Practical UI + UPD** 也能覆盖 A1–A9；但 Practical UI 补不了 A10，而 RUI 能（p17），所以 RUI 优先
- Laws of UX、Bringhurst、New Basics 都不适合做"单一出处"
  - 这三本覆盖面窄（Laws of UX 只有 1 条），或者面向印刷（Bringhurst、New Basics）
  - 只适合给个别条目补数值或补理论背书，比如 Bringhurst 补 A4 的 45–75

### Gaps
- 有几本书的"缺"是"在可得材料里没找到"，不是"确认书里没有"
  - Williams ch9、About Face ch17 的小标题、Designing Interfaces ch4、Practical UI ch5
  - 要最终下结论，需要纸本或出版社预览
- 没有检索的其他候选
  - Jason Beaird《The Principles of Beautiful Web Design》（SitePoint）：archive.org 只有借阅受限的 2008 版元数据，且没有目录
  - 《White Space Is Not Your Enemy》、Kadavy《Design for Hackers》
  - 这几本可能也覆盖 A1–A10 的大部分，本次没有评估

