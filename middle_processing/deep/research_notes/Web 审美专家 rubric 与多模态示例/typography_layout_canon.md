# 排版经典（Typography & Layout Canon）→ 可验证的 Web 页面审美 rubric

> 写作约定
> - 核实等级：**一手** = 读到了原文（含经授权/学术读本转载的原文全文）；**二手** = 二手转述/摘要；**未核实** = 找不到可靠出处
> - 规则 ID：`BR`=Bringhurst，`RU`=Rutter，`BU`=Butterick，`LU`=Lupton，`MB`=Müller-Brockmann，`TS`=Tschichold，`SA`=Samara，`SP`=Spiekermann，`TB`=Tim Brown，`W3C`=WCAG（作为 web 端数值锚点对照）
> - 每条规则统一格式：
>   - 原文 / 出处 / 阈值 / 等级
>   - 好坏对照页（同内容，只改这一条）
>   - 判定方式：`DOM`（computed style / 几何量可程序判）· `VLM`（只能看截图判）· `DOM+VLM`（程序能定位，好坏要视觉判）
> - 一个通用测量口径（后文所有 cpl 判定都用它）：在浏览器里对正文段落用 `Range.getClientRects()` 拿到每一行的矩形，按行统计字符数（含空格），取段落内中位数作为 characters-per-line（cpl）。这比 `width / (0.5em)` 的估算准，因为 Rutter 自己也说 0.5em/字符只是"平均"。

---

## Q1. Bringhurst《The Elements of Typographic Style》+ Rutter 的 webtypography.net 改编：measure、leading、vertical rhythm、scale、hierarchy、emphasis、caps/letterspacing、alignment

### Takeaway
"45–75 字符、66 最理想"这句话**属实**，但原文带三个限定条件（single-column、serifed text face、text size）并用 "widely regarded" 措辞，是对行业惯例的转述而不是 Bringhurst 自己的公式；多栏时他另给 40–50。Bringhurst 的规则标题大量带 "suits the typeface, text and measure" 这类条件从句，本质是原则；真正可直接程序化的是 measure、caps letterspacing 5–10%、"用一套有限的字号 scale"、"垂直空间按整数行距增减"这几条。

### Cited Findings

**BR-01 Measure（行长）** — 等级：一手（Bringhurst 原文经 webtypography.net 转录，未对照纸本页码）
- 原文（§2.1.2 "Choose a comfortable measure"）：
  - "Anything from 45 to 75 characters is widely regarded as a satisfactory length of line" … "for a single-column page set in a serifed text face in a text size." — [webtypography.net 2.1.2](http://webtypography.net/2.1.2)
  - "The 66-character line (counting both letters and spaces) is widely regarded as ideal." — [同上](http://webtypography.net/2.1.2)
  - "For multiple column work, a better average is 40 to 50 characters." — [同上](http://webtypography.net/2.1.2)
- 未在 webtypography.net 转录中出现、但被二手来源归给 Bringhurst 的后半段：
  - 书目/参考文献等 discontinuous text 可到 85–90 字符；连续正文平均超过约 75（或 "75 or 80"）字符则太长。措辞在不同转述里不一致 — 等级：**二手** — [ConTeXt 邮件列表转引](https://mailman.ntg.nl/archives/list/ntg-context@ntg.nl/thread/QBUJNFYPW3F3G3BNEKHNQLFOYTJQOLMC)
  - Wikipedia 把这套数字引到 1992 年版 "Horizontal Motion" pp. 25–36，并有 "between 20 and 40 times is considered acceptable"（语境不清，疑为 measure 与字号的倍数）— 等级：**二手** — [Wikipedia: Line length](https://en.wikipedia.org/wiki/Line_length)
- Rutter 的 CSS 改编：
  - "From a typographical perspective, the most appropriate method is to set box width in ems (elastic layout)" — [webtypography.net 2.1.2](http://webtypography.net/2.1.2)
  - 示例 `#col3 { width:33em; }`，理由 "On average one character takes up 0.5 em so this box will have a measure of 66 characters per line." — [同上](http://webtypography.net/2.1.2)
  - 同页也承认 liquid layout（百分比宽度）把控制权交给读者，且该站本身用的是 liquid layout — [同上](http://webtypography.net/2.1.2)
- 好坏对照页：
  - 好：1440px 视口，文章正文容器 `max-width: 33em`（≈66 cpl），左右留白
  - 坏：同一段文字铺满 1440px（≈170+ cpl）
- 判定：`DOM`（按上文口径算 cpl；阈值：单栏 45–75，多栏 40–50）

**BR-02 Leading（行距）** — 等级：一手
- 原文（§2.2.1 "Choose a basic leading that suits the typeface, text and measure"）：leading 是 "the distance from one baseline to the next"，并是 "a basic rhythmical unit" — [webtypography.net 2.2.1](http://webtypography.net/2.2.1)
  - **Bringhurst 本条没有给数字**，只给"随字体、文本、行长调整"的原则
- Rutter 的 CSS 改编：
  - 用 unitless：`line-height: 1.25;`，因为 "the line-height … will always be proportional to the text size" — [同上](http://webtypography.net/2.2.1)
  - "Text on the web almost always benefits from an increase in line height, and figures upwards of 1.3 are common." — [同上](http://webtypography.net/2.2.1)
  - 小于 1 的负 leading 只可用于短文本，且要防止 ascender/descender 相撞 — [同上](http://webtypography.net/2.2.1)
- 好坏对照页：
  - 好：18px 正文、66 cpl、`line-height: 1.5`
  - 坏：同排版 `line-height: 1.0`（行间挤压）；或反向坏例 `line-height: 2.4`（行与行散开，段落失去整体"灰度"）
- 判定：`DOM`（computed line-height ÷ font-size）；"是否 suits the measure" 可加一条联动规则：cpl 越大 line-height 应越大（见 Q7 推论）

**BR-03 Vertical rhythm（垂直节奏）** — 等级：一手
- 原文（§2.2.2 "Add and delete vertical space in measured intervals"）：
  - "Headings, subheads, block quotations, footnotes, illustrations, captions and other intrusions into the text" 打断行距节奏，但 "the main text should also return after each variation precisely on beat and in phase." — [webtypography.net 2.2.2](http://webtypography.net/2.2.2)
- Rutter 的 CSS 改编（同页 + 24ways 2006）：
  - 段落 `margin-top/bottom` = 行高（12px/1.5 → 18px）；浏览器默认 1em 边距会破坏节奏 — [webtypography.net 2.2.2](http://webtypography.net/2.2.2)
  - 14px 小标题 `line-height: 1.286`（=18/14），margin 同值；不对称 margin 可以，只要总和是整数行 — [同上](http://webtypography.net/2.2.2)
  - "The basic unit of vertical space is line height." ；水平 border 会 "effectively act as shims pushing the subsequent text downwards" — [Rutter, Compose to a Vertical Rhythm, 24ways 2006](https://24ways.org/2006/compose-to-a-vertical-rhythm/)
  - 引 Bringhurst："Space in typography is like time in music." — [同上](https://24ways.org/2006/compose-to-a-vertical-rhythm/)
- 好坏对照页：
  - 好：所有段落/标题/图片的上下间距都是 24px（=基准行高）的整数倍，正文基线落在同一网格
  - 坏：同内容，间距随手取 13 / 27 / 9 / 41px，标题下方比上方大（标题"漂"向下一段之外）
- 判定：`DOM`（取所有块级元素的 margin/padding 与正文 line-height 求余；或取每行基线 y 坐标 mod 基准行高）。注意：严格基线网格偏差几 px 时人眼几乎不可见，`VLM` 判这一条信度低；但"标题与其所属段落的远近关系"VLM 能看出来（这其实是 proximity，见 Q4/Q5）

**BR-04 Scale（字号刻度）** — 等级：一手（规则文本）/ 二手（经典刻度数值）
- 原文（§3.1.1 "Don't compose without a scale"）：
  - "Use the old familiar scale, or use new scales of your own devising," "but limit yourself, at first, to a modest set of distinct and related intervals." — [webtypography.net 3.1.1](http://webtypography.net/3.1.1)
  - 关键：Bringhurst 要求的是**"有限、离散、彼此相关"**，并不指定某个比例
- Rutter 的 CSS 改编：`h1 2.25em(36) / h2 1.5em(24) / h3 1.125em(18) / h4 0.875em(14) / p 0.75em(12)`（基于 16px）— [同上](http://webtypography.net/3.1.1)
- 经典刻度的具体数值（webtypography.net 页面**没有**列出）：
  - 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72 — 引 §3.1 — 等级：二手 — [fontscale LaTeX 手册](https://ctan.math.illinois.edu/macros/latex/contrib/fontscale/fontscale-manual.pdf)；[OEIS A053407](https://oeis.org/A053407)
  - 另一转录在 24 与 36 之间多一个 **30** — 等级：二手 — [Spencer Mortensen, The typographic scale](https://spencermortensen.com/articles/typographic-scale)。两种版本互相矛盾，未能对照纸本确认
- 好坏对照页：
  - 好：全页只用 5 个字号 12 / 14 / 18 / 24 / 36px，每级之间差异肉眼明显
  - 坏：全页出现 13 / 14 / 15 / 16 / 17 / 19 / 22 / 23 / 29px 九个字号，相邻级别只差 1px，看起来像"手滑"
- 判定：`DOM`（收集所有可见文本节点的 computed font-size → 去重计数；检测相邻级比值 < 1.07 的"近重复"字号；可选：拟合几何级数的残差）

**BR-05 Caps / small caps 的字距** — 等级：一手
- 原文（§2.1.6 "Letterspace all strings of capitals and small caps, and all long strings of digits"）：
  - "The normal value for letterspacing these sequences of small or full caps is 5% to 10% of the type size." — [webtypography.net 2.1.6](http://webtypography.net/2.1.6)
  - 长串数字（序列号、电话、日期）也建议加字距 — [同上](http://webtypography.net/2.1.6)
- 反向规则（§2.1.7 标题）："Don't letterspace the lower case without a reason" — [webtypography.net 目录](http://webtypography.net/toc/)
- Rutter 的 CSS：`abbr { letter-spacing: 0.1em; }` — [webtypography.net 2.1.6](http://webtypography.net/2.1.6)
- 好坏对照页：
  - 好：导航/标签/eyebrow 全大写，`letter-spacing: 0.08em`
  - 坏 A：同一行全大写，`letter-spacing: 0` 或负值（字母挤成一条）
  - 坏 B：正文小写加了 `letter-spacing: 0.1em`（违反 2.1.7）
- 判定：`DOM`（`text-transform: uppercase` 或文本全为大写字母的节点 → letter-spacing/font-size ∈ [0.05, 0.10]；小写正文 letter-spacing ≈ 0）

**BR-06 Ragged vs justified（对齐/齐行）** — 等级：一手
- 原文（§2.1.3 "Set ragged if ragged setting suits the text and page"）：
  - "In justified text, there is always a trade-off between evenness of word spacing and frequency of hyphenation." — [webtypography.net 2.1.3](http://webtypography.net/2.1.3)
  - "Narrow measures – which prevent good justification – are commonly used when the text is set in multiple columns." — [同上](http://webtypography.net/2.1.3)
  - "Many unserifed faces look best when set ragged no matter what the length of the measure." — [同上](http://webtypography.net/2.1.3)
- Rutter（2000 年代 CSS2 语境）："So don't justify text on the web." 理由是当时浏览器没有自动断字 — [同上](http://webtypography.net/2.1.3)
  - 注：此结论的前提（无 hyphenation）在今天已部分过时（现有 `hyphens: auto`），但 Rutter 2017 书里的新立场未能读到 → 见 Gaps
- 好坏对照页：
  - 好：375px 手机宽度、无衬线正文、`text-align: left`
  - 坏：同内容 `text-align: justify`、无 `hyphens: auto` → 词间出现大白洞、纵向 "rivers"
- 判定：`DOM+VLM`（DOM 能判"窄栏 + justify + 无 hyphens"这一风险组合；词间空洞/rivers 是否真的出现，要看截图或逐行算 word-spacing 拉伸量）

**BR-07 段落标记** — 等级：一手（仅规则标题）
- §2.3.1 "Set opening paragraphs flush left"；§2.3.2 "In continuous text mark all paragraphs after the first with an indent of at least one en"；§2.3.3 "Add extra lead before and after block quotations" — [webtypography.net 目录](http://webtypography.net/toc/)
- 好坏对照页：
  - 好：段落用段间距分隔，无首行缩进；或标题后首段不缩进、后续段缩进 1em
  - 坏：标题后第一段也缩进，且同时有段间距（双重标记）
- 判定：`DOM`（`text-indent` 与 `margin-block` 同时 > 0 → 违规；标题后首段 text-indent > 0 → 违规）

**BR-08 "break the rules" 的总体立场** — 等级：二手（未找到页码）
- "By all means break the rules, and break them beautifully, deliberately and well." — [Quotepark](https://quotepark.com/fr/citations/837566-robert-bringhurst-by-all-means-break-the-rules-and-break-them-beaut/)；[Luc Devroye 页](https://luc.devroye.org/fonts-39788.html) 补充其后一句大意为 "one of the ends for which [rules] exist"

### Inferences
- Bringhurst 规则里真正带硬数字的只有：measure（45–75 / 66 / 40–50）、caps 字距（5–10%）、段落缩进（≥ 1 en）。其余（leading、scale、ragged）都是条件式原则，rubric 里应写成"相对一致性"检查（例如"是否使用有限的字号集合"），而不是绝对阈值。
- "66 cpl ideal" 的前提是**衬线体、单栏、正文字号**；用于 web 时：多栏卡片/侧栏应切换到 40–50 的阈值；无衬线 UI 正文没有 Bringhurst 本人的单独数字。
- Rutter 的 `33em = 66 字符` 依赖 "0.5em/字符" 的平均值，换字体就会偏；rubric 实测 cpl 应以渲染结果为准（见文首口径）。
- 对 VLM 而言，measure 与 leading 的"明显违规"（铺满大屏、行距 1.0）截图上很容易看出，但 66 vs 80 cpl 这种细差要靠 DOM。

### Gaps
- 未能读到纸本或扫描页，因此 §2.1.2 中 "85 or 90 / 75 or 80" 的原句、以及各节在第 3/4 版中的页码无法一手确认。
- Bringhurst 关于 headings/subheads（第 4 章 Structural Forms）和 emphasis（italic/bold 使用）的规则，webtypography.net 未覆盖，未能取得原文；网上流传的 "change one parameter at a time" 找不到出处（检索只命中一个 skill 作者自己的转述 [skills.cat](https://skills.cat/skills/agrimsingh/bringhurst-typography)），应视为**未核实**，不要归给 Bringhurst。意思相近、有一手出处的是 Spiekermann："every time you change one spacing parameter, you have to look closely at all the others and adjust them accordingly"（见 SP-01）——但那讲的是间距参数联动，不是"强调时一次只改一个属性"。
- 经典字号刻度是否含 30pt，二手来源互相矛盾。

---

## Q2. Matthew Butterick《Practical Typography》：关键规则与数字

### Takeaway
Butterick 是这批书里**最"可程序化"**的：网页正文 15–25px、行距 120–145%、平均行长 45–90 字符、字体 ≤2（第三种很少能成立）、caps 加 5–12% 字距、粗/斜体尽量少且不叠用、标题 ≤3 级。他自己把这些称作 "rules"，但 "Maxims of page layout" 那一组（smallest visible increments、try it both ways、imitate what you like）是判断型原则，只能靠视觉对比。

### Cited Findings

**BU-01 正文四要素** — 等级：一手
- "The four most important typographic considerations for body text are point size, line spacing, line length, and font" — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- "if you learn and follow these five typography rules, you will be a better typographer than nearly every writer" — [Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html)

**BU-02 字号** — 等级：一手
- "Point size should be 10–12 points in printed documents, 15–25 pixels on the web." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 好坏对照：好 = 正文 18px；坏 = 正文 12px（桌面端过小）或 28px（营销页正文过大）
- 判定：`DOM`（主正文节点 computed font-size ∈ [15, 25]px）

**BU-03 行距** — 等级：一手
- "Line spacing should be 120–145% of the point size." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 判定：`DOM`（line-height/font-size ∈ [1.2, 1.45]）— 注意与 WCAG 的 ≥1.5 冲突（见 Q7）

**BU-04 行长** — 等级：一手
- "The average line length should be 45–90 characters (including spaces)." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 替代量法：一行放 "between two and three alphabets"（小写 a–z）；他称对行长关注不足是许多 responsive layout 的主要缺陷 — [Line length](https://practicaltypography.com/line-length.html)
- 判定：`DOM`

**BU-05 字体数量与搭配** — 等级：一手
- "Most documents can tolerate a second font. Few can tolerate a third." / "Almost none can tolerate four or more." — [Mixing fonts](https://practicaltypography.com/mixing-fonts.html)
- "Font mixing is most successful when each font has a consistent role in the document." — [同上](https://practicaltypography.com/mixing-fonts.html)
- "It rarely works to have multiple fonts in a single paragraph." — [同上](https://practicaltypography.com/mixing-fonts.html)
- 反直觉点："If you've heard that you can only mix a serif font with a sans serif font, it's not true."；"lower contrast between fonts can be more effective than higher contrast." — [同上](https://practicaltypography.com/mixing-fonts.html)
- 字体选择："Avoid goofy fonts, monospaced fonts, most free fonts, and system fonts—especially Times New Roman and Arial." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 好坏对照：
  - 好：标题一种字体 + 正文一种字体，角色固定
  - 坏：同页 4 种字体（标题 serif、正文 sans、按钮 slab、引用 script），且正文段落中夹杂另一字体
- 判定：`DOM`（统计实际渲染字体 `document.fonts` / computed font-family 的首个可用族 → 去重；同一 `<p>` 内多字体 → 违规）；"goofy font" 的判断需 `VLM` 或字体白名单

**BU-06 强调** — 等级：一手
- "Use bold or italic as little as possible, and not together." / "Never underline, except perhaps for web links." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 好坏对照：好 = 段落里 1–2 处 `<em>`；坏 = 同段 5 处 bold-italic 混用 + 非链接下划线
- 判定：`DOM`（同一节点 font-weight ≥ 600 且 font-style: italic → 违规；非 `<a>` 的 text-decoration: underline → 违规；强调字符占比可设阈值）

**BU-07 全大写** — 等级：一手
- "All caps are fine for less than one line of text." / "Use 5–12% extra letterspacing with all caps and small caps." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 理由："Capitalization homogenizes these shapes, leaving a rectangular contour." — [All caps](https://practicaltypography.com/all-caps.html)
- 判定：`DOM`（全大写文本块渲染行数 > 1 → 违规；字距 ∈ [0.05, 0.12]em）

**BU-08 居中** — 等级：一手
- "Use centered text sparingly." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 可接受：短语、标题；不可接受：整块正文居中，因为 "both edges of the text block are uneven"；**未给行数上限** — [Centered text](https://practicaltypography.com/centered-text.html)
- 好坏对照：好 = hero 标题居中、下方正文左对齐；坏 = 6 行正文段落全部居中
- 判定：`DOM`（text-align:center 且渲染行数 ≥ 3 的正文段落 → 违规；"3 行"是 rubric 自定阈值，非 Butterick 原文）

**BU-09 段落分隔** — 等级：一手
- "Use first-line indents that are one to four times the point size of the text," "or use 4–10 points of space between paragraphs." "Don't use both." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 判定：`DOM`

**BU-10 对齐** — 等级：一手
- "Always use hyphenation with justified text." — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- 判定：`DOM`（justify 且 hyphens ≠ auto → 违规）

**BU-11 标题** — 等级：一手
- "Limit yourself to three levels of headings. Two is better." — [Headings](https://practicaltypography.com/headings.html)
- "The best way to emphasize a heading is by putting space above and below." / "Use bold, not italic." / "Don't use all caps." / "Don't underline." / "Don't center"（有例外）— [同上](https://practicaltypography.com/headings.html)
- "Use the smallest increment necessary to make a visible difference." 例："If your text is set in 12 point, you needn't go up to 14 or 15 point." — [同上](https://practicaltypography.com/headings.html)
- 好坏对照：
  - 好：正文 18px、h2 22px bold、h3 18px bold，标题上方空间 > 下方空间
  - 坏：正文 16px、h2 48px、h3 36px、h4 28px、h5 22px（五级、跳级过大、每级都抢戏）
- 判定：标题级数、bold/italic、caps、underline → `DOM`；"smallest increment necessary to make a visible difference" → `VLM`（"可见差异"是知觉判断）

**BU-12 页面布局 maxims（判断型原则）** — 等级：一手
- "Decide first how the body text will look." — [Maxims of page layout](https://practicaltypography.com/maxims-of-page-layout.html)
- "Don't let the background elements upstage the foreground elements." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- "The difference between not enough and too much can be small." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- "There's no substitute for making samples of two options and getting a visual reaction." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- "Things that are the same should look the same. Things that look different should actually be different." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- "If you think you need three colors and five fonts, think again." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- "Work outward from the text, not inward from the page edges." — [同上](https://practicaltypography.com/maxims-of-page-layout.html)
- 好坏对照：
  - foreground/background：好 = 背景装饰渐变低对比，正文卡片清晰；坏 = 背景大面积高饱和插画、毛玻璃、动效抢过正文
  - consistency：好 = 所有卡片同 padding、同圆角、同标题样式；坏 = 三张卡片三种圆角、两种标题字号
- 判定：foreground/background → `VLM`；consistency → `DOM+VLM`（DOM 可按同类组件聚类比较 computed style 方差；"应该相同的是否相同"需要语义归类，VLM 更稳）

### Inferences
- Butterick 的 26 条 key rules 中，大约 15 条可直接写成 DOM 断言（字号、行距、行长、字体数、bold+italic、underline、caps 行数/字距、段落分隔、justify+hyphen、标题级数），剩余的 curly quotes / 破折号 / 省略号等属于字符级细节，对"截图审美"影响较小，可做低权重项。
- Butterick 的 "smallest visible increment" 与 modular scale 派（golden ratio 1.618）方向相反：前者倾向小步长，后者天然大跨度。rubric 不应同时把两者当硬约束（见 Q7）。

### Gaps
- Butterick 在 All caps 页说 caps "suitable for headings shorter than one line"，在 Headings 页又说 "Don't use all caps"——两页之间的不一致没有找到他本人的解释。
- 15–25px 这一 web 字号范围，Butterick 未给出它是基于何种视距/设备的推导。

---

## Q3. Richard Rutter《Web Typography》（2017）：web 专属规则（responsive measure、vertical rhythm、typographic scale）

### Takeaway
2017 年书的正文**没有免费在线全文**（官网只提供目录 + 一章 "Numerals and tables" 样章），因此书中 "Responsive paragraphs" "Hierarchy and scale" "Vertical rhythm" 各章的具体数字本次**未能一手核实**。能一手核实的 Rutter web 规则来自他更早/更晚的公开文本：webtypography.net（em 定 measure、unitless line-height、margin = 行高）、24ways 2006（vertical rhythm）、Clagnut 2024（用 rem 而非 ch 定行长）。

### Cited Findings
- 书目结构（一手，仅目录）：Part 1 "Setting Type to be Read" 含 "Designing paragraphs: line length / text size / line spacing"、"Alignment, justification and hyphenation"、"Responsive paragraphs"；Part 2 含 "Hierarchy and scale"、"Vertical rhythm"、"Arrangement and composition"；Part 3 含 "Combining typefaces" — [book.webtypography.net](https://book.webtypography.net/)
- **RU-01 Measure 用相对单位且受字号约束** — 等级：一手
  - webtypography.net：用 em 定盒宽（elastic layout），33em ≈ 66 字符 — [webtypography.net 2.1.2](http://webtypography.net/2.1.2)
  - 2024 修正：`ch` 是 "the width of the zero '0' character within the selected font, or `0.5em` if no '0' is present"，同为 34ch 的两个文本块会因字体不同而宽度不同；他更推荐 `max-inline-size: 30rem` 这类写法，得到 "a line length accessibly tied to text size, but independent of font design" — [Rutter, Use of ch unit considered inappropriate, Clagnut 2024-06-14](https://clagnut.com/blog/2432/)
  - 好坏对照：
    - 好：正文容器 `max-inline-size` 用 rem/em，用户放大字号后 cpl 不变
    - 坏：容器 `width: 600px`；用户把字号从 16px 放大到 24px 后，每行只剩约 40 字符且段落右侧大片留白（或反过来：容器 `width: 90vw`，宽屏时 cpl 失控）
  - 判定：`DOM`（在两个视口宽度 × 两个根字号下各测一次 cpl，看是否都落在区间内——这是 web 特有、印刷书无法表达的"responsive measure"检查）
- **RU-02 Vertical rhythm** — 等级：一手
  - "we must use ems for all our vertical measurements, including line-height, padding and margins" — [24ways 2006](https://24ways.org/2006/compose-to-a-vertical-rhythm/)
  - 规则细节见 BR-03
- **RU-03 Scale 在 CSS 中的落地** — 等级：一手（webtypography.net 版本）
  - 36/24/18/14/12 的 em 实现见 BR-04 — [webtypography.net 3.1.1](http://webtypography.net/3.1.1)
- **RU-04 不要在 web 上 justify** — 等级：一手（但为 CSS2 时代结论）— [webtypography.net 2.1.3](http://webtypography.net/2.1.3)
- **RU-05 caps 字距 0.1em** — 等级：一手 — [webtypography.net 2.1.6](http://webtypography.net/2.1.6)
- 网络转述（二手）：某 slide deck 把 Rutter 风格容器写成 `max-width: 45em` 并注释防止行过长；另一 deck 给出 "45–75 characters (30–50 ems)" 并建议配合 min-width/max-width — 来源是 web search 摘要，未打开验证 — [Responsive Web Design slides](https://www.slideshare.net/slideshow/typography-responsive-web-design/15014926)；[Matthew Buchanan, Web Typography deck](https://speakerdeck.com/matthewbuchanan/web-typography)

### Inferences
- web 与印刷的关键差异是"测量对象会变"：视口宽度和用户字号都在变。所以 Rutter 系规则落到 rubric 时应写成**"多条件下保持不变量"**：任一视口下正文 cpl ∈ [45,75]；行高为 unitless；垂直间距 = 行高整数倍。这类规则 `DOM` 能测、`VLM` 只能看单张截图，天然测不到"放大后是否崩"。
- 截图式审美评测若只渲染一个视口，会漏掉 RU-01 一类问题；建议至少 375 / 1440 两个宽度各截一张。

### Gaps
- 2017 书中 "Responsive paragraphs"（是否推荐 vw/clamp 流体字号、具体系数）、"Hierarchy and scale"（是否推荐某个 ratio）、"Vertical rhythm"（是否仍坚持严格基线网格）的原文与数字均**未核实**。
- Rutter 是否在 2017 书中修正了 "don't justify text on the web" 的立场，未核实。
- 官网样章 PDF（Numerals and tables）未读取，与本题关系不大。

---

## Q4. Ellen Lupton《Thinking with Type》：hierarchy、grid、text block

### Takeaway
本次**未能取得 Lupton 原文**（thinkingwithtype.com 被代理拦截，archive.org 不可用，网上 PDF 多为可疑镜像，未使用）。能确认的只有书的结构（Letter / Text / Grid 三部分，Text 部分含 Hierarchy、Scale 等小节）。网上广泛流传、归给 Lupton 的两句话经检索都只能追到课程讲义，**不能当作 Lupton 原话引用**。

### Cited Findings
- 书分三部分 Letter、Text、Grid；Text 部分含 paragraphs、captions、hierarchy；Grid 部分含 "Grid as frame / Dividing space / Grid as program / Grid as table" — 等级：二手（web search 摘要对图书馆目录的转述，页面本身未打开）— [CCA 图书馆目录](https://library.cca.edu/bib/74791)
- issuu 上出版社上传本的目录显示 "Hierarchy" 约在 p.132、"Scale" 约在 p.118，Grid 部分有 Single-Column / Multicolumn / Modular Grid、Golden Section — 等级：二手（web search 摘要，issuu 页面未打开）— [issuu: papress / Thinking with Type](https://issuu.com/papress/docs/thinking_with_type)
- 第 2 版：Princeton Architectural Press, 2010 — 等级：二手 — [LASALLE 图书馆目录](https://elib.lasalle.edu.sg/cgi-bin/spydus.exe/FULL/WPAC/BIBENQ/122137763/100553)
- Creative Bloq 转述 Lupton 建议正文左对齐，让读者每行都有一致的起点 — 等级：二手（检索摘要，未打开原文）— [Creative Bloq, UX typography explained](https://www.creativebloq.com/web-design/ux-typography-explained-21619368)
- 常被归给 Lupton 的 "Typographic hierarchy expresses the organization of content…" 与 "each level of the hierarchy should be signaled by one or more cues, applied consistently across a body of text"（cue 可以是 spatial：缩进、行距、位置；或 graphic：字号、样式、颜色）— 检索只命中 CUNY City Tech 的课程讲义且未署名 Lupton — 等级：**未核实**（作为 Lupton 原话）— [CUNY City Tech 讲义 ct_type1_hierarchy.pdf](https://openlab.citytech.cuny.edu/clarkeadv1227/files/2012/11/ct_type1_hierarchy.pdf)

### Inferences
- 即使不归给 Lupton，"每个层级用一个或多个 cue 区分、且在全文一致应用"这一条本身可以作为 rubric 规则（来源标为"设计教学通行做法"），并且可程序化：
  - 好坏对照：好 = 所有 h2 都是 22px/700/上方 48px 间距；坏 = 第一个 h2 用 24px 蓝色，第二个 h2 用 20px 斜体，第三个 h2 只靠加粗
  - 判定：`DOM`（同语义级别元素的 computed style 方差）+ `VLM`（当 HTML 语义标签缺失、层级只靠视觉表达时）

### Gaps
- Lupton 关于 text block（行长、行距、对齐、rag 形状、段落标记）和 grid 的具体规则与页码，全部**未核实**。如需引用，必须查纸本或出版社授权预览。

---

## Q5. 网格派：Müller-Brockmann《Grid Systems in Graphic Design》、Samara《Making and Breaking the Grid》、Tschichold：网格为何存在、违规长什么样、"客观/秩序"论证

### Takeaway
Müller-Brockmann 与 Tschichold 的原文（经学术读本转载）读到了：二者都把"清晰、客观、按内容逻辑组织"作为核心价值，Müller-Brockmann 还声称网格让信息"读得更快、记得更牢"并称其为 "scientifically proved fact"（但读本中**未给出研究出处**）。Tschichold 1928 年书里有一组现成的"坏 vs 好"对照图注：坏版 = 装饰 + 7 种字型字号 + 居中；好版 = 无装饰 + 只用 5 种 + 易读。Samara 的一手文本未取得。

### Cited Findings

**MB-01 网格的目的：系统化与客观性** — 等级：一手（原文经 Graphic Design Theory 读本 pp. 62–63 转载）
- "Working with the grid system means submitting to laws of universal validity." — [Müller-Brockmann, Grid and Design Philosophy (1981)，读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)
- "The use of the grid system implies the will to systematize, to clarify / the will to penetrate to the essentials, to concentrate / the will to cultivate objectivity instead of subjectivity …" — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)
- 设计应有 "the clearly intelligible, objective, functional, and aesthetic quality of mathematical thinking." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)
- 网格示例图注："musica viva" 海报 "built up on a grid 4.5 fields wide and 4 fields deep"，小字节目单与大字母对齐，形成 "a severe but elegant architecture" — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)

**MB-02 网格的效果主张：可信度与阅读效率** — 等级：一手（Texts on Type 摘录的转载页）
- 网格 "creates a sense of compact planning, intelligibility, and clarity" — [neugraphic.com 转载（标注出自 Texts on Type, 2001）](https://mail.neugraphic.com/muller-brockmann/muller-brockmann-text2.html)
- "This orderliness lends added credibility to the information and induces confidence." — [同上](https://mail.neugraphic.com/muller-brockmann/muller-brockmann-text2.html)
- 结构清晰的信息 "will not only be read more quickly and easily" 且 "will also be better understood and retained in the memory"，并称这是 "a scientifically proved fact"——**原文未引研究**，此主张本身视为未核实 — [同上](https://mail.neugraphic.com/muller-brockmann/muller-brockmann-text2.html)

**MB-03 "网格是工具不是保证"** — 等级：二手
- "The grid system is an aid, not a guarantee." 后接大意 "It permits a number of possible uses…"、"one must learn how to use the grid; it is an art that requires practice" — 出自书前言，页码未知 — [Draw Down 书店页（检索摘要）](https://draw-down.com/products/grid-systems-in-graphic-design)；[Medium 书评](https://medium.com/@kostas.ladauskas/grid-systems-in-graphic-design-my-honest-book-review-d022a1e65459)
- 书的基本信息：Niggli 1981，176 页；出版社称提供 8 到 32 grid fields 的使用说明 — 等级：二手 — [Draw Down](https://draw-down.com/products/grid-systems-in-graphic-design)

**MB 网格规则 → web 好坏对照**
- 好：12 栏网格（gutter 24px），所有卡片、标题、图片左缘都落在栏线上，全页只有约 4–6 个不同的左缘 x 坐标
- 坏：同内容，卡片左缘分别在 x = 120 / 124 / 131 / 117px（差几像素的"差一点对齐"），图片宽度不是栏宽的整数倍
- 判定：`DOM`（取所有可见块的 bounding box 左/右缘 → 聚类；统计"相差 1–8px 的近邻但不相等"的边缘对数，越多越差；不同 x 坐标数越少越有序）；`VLM` 对大偏差敏感，对 2–4px 偏差不敏感

**TS-01 清晰是第一目标；反对中轴** — 等级：一手（原文经读本 pp. 35–38 转载，英译本）
- "The essence of the New Typography is clarity." — [Tschichold, The New Typography (1928)，读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- "Axial arrangements are illogical because the distance of the stressed, central parts from the beginning and end of the word sequences is not usually equal but constantly varies from line to line." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- "Every piece of typography that originates in a preconceived idea of form, of whatever kind, is wrong." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- "The function of printed text is communication, emphasis (word value), and the logical sequence of the contents." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)

**TS-02 书中自带的"坏 vs 好"对照（最接近本任务需要的示例形式）** — 等级：一手
- 坏："unnecessary ornaments, too many kinds of type and type sizes (7), centered design, which makes reading difficult and is unsightly." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- 好（同一广告重设计）："no use of ornament, clear type, few sizes (in all, only 5 different types), good legibility, good appearance." — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- 另一反例："Centered layout using lightweight sans serif has no visual effectiveness and reaches a 'typographic low'" — [同上](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- web 化对照页：
  - 好：落地页左对齐不对称构图，≤5 种字号/字重组合，无装饰分隔线/花边/emoji 堆砌
  - 坏：同内容全部居中，7+ 种字号，四处装饰元素（渐变描边、星星图标、花体分隔符），细字重无衬线小字居中
- 判定：字号/字重组合计数、居中比例 → `DOM`；"装饰是否多余""是否 clear" → `VLM`

**TS-03 层级必须反映内容逻辑** — 等级：一手
- "Every part of a text relates to every other part by a definite, logical relationship of emphasis and value, predetermined by content. It is up to the typographer to express this relationship clearly and visibly through type sizes and weight, arrangement of lines, use of color, photography, etc."（"New Life in Print", 1930）— [读本 PDF p.37](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- 好坏对照：好 = 视觉显著度顺序与内容重要度一致（标题 > 副标题 > 正文 > 注释）；坏 = 一个次要的"限时优惠"角标比页面主标题更大更粗更亮
- 判定：`DOM`（heading level 与 font-size×weight 的单调性检查）+ `VLM`（"内容上谁更重要"需要语义理解）

**TS-04 不对称 ≠ 混乱；客观 ≠ 贫乏** — 等级：一手
- "This movement must not, however, degenerate into unrest or chaos. A striving for order can, and must, also be expressed in asymmetrical form." — [读本 PDF p.37](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- 对一个去掉了所有装饰但效果平淡的信头，他说那不是他要的 objectivity，"A better name for it would be 'meagerness.'" — [读本 PDF p.38](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- 判定：`VLM`（"有序的不对称" vs "乱"、"克制" vs "寒酸"只能整体看）
- 背景提醒：读本导言指出 Tschichold 晚年转回古典（对称）排版 — [同上 p.35](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)

**SA-01 Samara** — 等级：二手 / 未核实
- Goodreads 用户整理的引文："The greatst [sic] danger in using a grid is to succumb to its regularity." — 用户整理、带错字，**未核实** — [Goodreads quotes](https://www.goodreads.com/work/quotes/211129)
- 书的前提：要有效打破网格规则，必须先理解规则并看到其应用；前半 "Making the Grid" 讲定义、历史、类型与使用原则，后半讲 breaking — 等级：二手（书籍描述）— [Goodreads 书页](https://www.goodreads.com/book/show/218062)
- Smashing Magazine 2022 的层级练习引用 Samara 讲网格（2–5 栏），并把"只用 3 个字号"作为课堂约束，同时声明 "use your discernment" — 等级：二手 — [Alma Hoffmann, Typographic Hierarchies, Smashing 2022-10-26](https://www.smashingmagazine.com/2022/10/typographic-hierarchies/)
- 好坏对照（若采用 "succumb to its regularity"）：好 = 12 栏网格上有一处有意的跨栏大图打破节奏；坏 = 全页 3×N 等大卡片无限重复，无焦点
- 判定：`VLM`（"单调 / 无焦点"是知觉判断）

### Inferences
- 网格派给 rubric 的可程序化遗产主要是两条：**对齐边缘数少且精确**（MB）、**字号/字型种类少**（TS 的 7 vs 5）。"客观""清晰""不贫乏""不单调"属于 VLM 题。
- Tschichold 的 7 vs 5 计的是 "kinds of type and type sizes"，与 Butterick 的"字体族 ≤ 2"不是同一计数单位：rubric 里应分开统计"字体族数"与"字号×字重样式数"。
- Müller-Brockmann 的"读得更快记得更牢"是作者主张而非可引用的实证结论；写报告时不能把它当作研究证据。

### Gaps
- Müller-Brockmann "aid, not a guarantee" 的原书页码未核实。
- Samara 书中的具体规则（如网格类型选择、何时打破）没有一手文本；Goodreads 引文可靠性低。
- Tschichold《The Form of the Book》中关于页面比例/版心的古典规则（如 2:3 页面、Van de Graaf canon）本次未检索，不作结论。

---

## Q6. Spiekermann《Stop Stealing Sheep》与 Tim Brown 的 modular scale：字体搭配与刻度一致性

### Takeaway
Tim Brown 的 modular scale 一手可查：定义为 "a sequence of numbers that relate to one another in a meaningful way"，他自己强调 scale 是 "tools—not dogma"、数值是可取整或忽略的 "educated suggestions"。modularscale.com 列出 17 个具名比例（1.067 … 4）。Spiekermann（第 4 版，2022，Google Fonts 以 CC BY-ND 4.0 发布全文 PDF）给的是**关系型规则**而非固定数：行距必须大于词距、每行字越多行距越大、改一个间距参数就要重调其他参数、90 字符一行 "almost too wide"；字体搭配上主张用同一大家族或同设计师/同时代的字体，并警告别让对比变成 gimmick。

### Cited Findings

**TB-01 Modular scale 定义与立场** — 等级：一手
- "A modular scale is a sequence of numbers that relate to one another in a meaningful way." 并引 Bringhurst："A modular scale, like a musical scale, is a prearranged set of harmonious proportions." — [Tim Brown, More Meaningful Typography, A List Apart 2011-05-03](https://alistapart.com/article/more-meaningful-typography/)
- 示例：以 1:1.618 从 10 出发得 16.180 → 26.179 → 42.358；其文章正文 18px — [同上](https://alistapart.com/article/more-meaningful-typography/)
- 论证：历史/文化上有共鸣的比例带来 "visual harmony not found in layouts that use arbitrary, conventional, or easily divisible numbers" — [同上](https://alistapart.com/article/more-meaningful-typography/)
- 限定：scale 是 "tools—not dogma"，数值是 "educated suggestions"，可取整、组合或忽略；数学不能替代有经验设计师的眼睛 — [同上](https://alistapart.com/article/more-meaningful-typography/)

**TB-02 具名比例清单** — 等级：一手
- 15:16 minor second 1.067；8:9 major second 1.125；5:6 minor third 1.2；4:5 major third 1.25；3:4 perfect fourth 1.333；1:√2 augmented fourth 1.414；2:3 perfect fifth 1.5；5:8 minor sixth 1.6；golden section 1.618；3:5 major sixth 1.667；9:16 minor seventh 1.778；8:15 major seventh 1.875；1:2 octave 2；2:5 major tenth 2.5；3:8 major eleventh 2.667；1:3 major twelfth 3；1:4 double octave 4 — [modularscale.com](https://www.modularscale.com/)
- 工具由 Tim Brown 于 Build 2010 首发，后与 Scott Kellum 合作重做 — [同上](https://www.modularscale.com/)

**TB 好坏对照**
- 好：base 16px，ratio 1.25 → 16 / 20 / 25 / 31.25 / 39px，全页字号都落在这条序列上（允许取整）
- 坏：同内容，字号 16 / 19 / 21 / 26 / 33 / 40px，彼此比值 1.10–1.27 杂乱
- 判定：`DOM`（对去重后的字号排序，取相邻比值；比值方差小 / 能被单一 ratio 的整数幂以 ±3% 误差解释 → 一致）。注意：Brown 本人不把它当硬规则，rubric 建议作为加分项而非扣分项

**Spiekermann 版本说明** — 等级：一手
- 读的是《Stop Stealing Sheep & Find Out How Type Works》第 4 版（© 2022 Erik Spiekermann, p98a.berlin；3/4 版合著 Ferdinand Ulrich），Google Fonts 托管、CC BY-ND 4.0 许可的全文 PDF — [Google Fonts Knowledge PDF](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- PDF 每页是一个跨页，下文页码写作"印刷页约 X–Y"（由页内印刷页码反推，误差 ±1 页）

**SP-01 行距 vs 词距 vs 行长：关系型规则** — 等级：一手（印刷页约 146–149）
- "One rule to remember about line space is that it needs to be larger than the space between words" — [Stop Stealing Sheep 4e](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- "the more words per line, the more space needed between the lines." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- "if you increase your word spacing, you have to have more space between the lines as well." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- "every time you change one spacing parameter, you have to look closely at all the others and adjust them accordingly. Longer lines need wider spaces" — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 好坏对照：
  - 好：宽屏正文 80 cpl 时 line-height 1.6；手机端 35 cpl 时 line-height 1.4
  - 坏：同一套 `line-height: 1.2` 同时用于 35 cpl 与 100 cpl；或 `word-spacing: 0.4em` 但行距不变（词间缝比行间缝还宽，视线会往下一行"跳"）
- 判定：`DOM`（断言 line-height 与 cpl 正相关；断言 行距空白 = line-height − font-size > word-spacing + 空格宽度）

**SP-02 行长示例（含数字）** — 等级：一手（印刷页约 152–153）
- 四个示例块：约 5 词（25+ 字符）set 8 on 9；8 词（45 字符）set 8 on 10；约 11 词（60 字符）set 8 on 11；15 词（90 字符）set 8 on 12，"which is almost too wide." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
  - 注意这组示例本身就同时演示了 SP-01：行越长，leading 从 9pt 逐级加到 12pt
- 字号（印刷）："Type for extended reading in print should be no smaller than 9 point and no larger than 14 point."，且只适用于 "normal" book typefaces，x-height 特大或特小的字体需另评（印刷页约 156–157）— [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)

**SP-03 文本"灰度"一致；齐行导致忽松忽紧** — 等级：一手（印刷页约 148–149）
- "One of the best ways to keep the reader's attention on the content of your message is to keep the color of the printed text consistent." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 报纸窄栏强制 justify："The result is words and lines that are erratically letterspaced."；读者可能误以为有意图："are the loose lines more important than the tight ones?" — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 判定：`DOM+VLM`（同 BR-06）

**SP-04 字距与大写** — 等级：一手（印刷页约 7、104–105、138–139）
- 卷首引 Goudy："Anyone who would letterspace lower case would steal sheep."（书名由来）— [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- "as the space between letters increases, so does the difficulty comprehending single words" — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 全大写 + 每字母加框 ≈ 去掉词形："there would be no help from the overall word shapes"；"words are like faces: the more features we can see, the easier it is to tell who is who." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 与 BR-05、BU-07 一致，判定同为 `DOM`

**SP-05 字体搭配与对比** — 等级：一手（印刷页约 94–95、120–121、126–127）
- 最稳妥的加强方式：用扩展大家族（如 Lucida、ITC Stone、Rotis 这类同时含 sans 与 serif 的家族）— [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 跨家族："It is generally alright to mix different types from the same designer (Eric Gill's Joanna and Gill Sans work well together, as do most of Adrian Frutiger's types), or from the same period, or even very different periods." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 不混也有代价："magazine pages all set in one kind of type tend to look very gray." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 对比要克制："Whatever typographic device you come up with, don't let it turn into a gimmick. A well-coordinated range of fonts will give you the scope for contrast as well as rhythm" — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 书中的讽刺性反例（小报风格）："take bold, preferably condensed typefaces, randomly distort the shapes electronically, put outlines around them, mix several together, and insert on the same page." — [同上](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 好坏对照：
  - 好：全站只用一个超级家族（如同时有 Sans/Serif 的家族）的 2–3 个成员，角色固定
  - 坏 A（gimmick）：标题用压缩粗体 + 描边 + 变形，三个不同展示字体同屏
  - 坏 B（too gray）：长文页面从标题到注释全是同字体同字重，仅靠字号区分，整页一片灰
- 判定：字体族数、描边/变形（`-webkit-text-stroke`、`transform: skew/scale` 作用于文字）→ `DOM`；"是否 gimmick / 是否太灰"→ `VLM`

### Inferences
- Bringhurst 的 "modest set of distinct and related intervals" 与 Brown 的 modular scale 目标一致（离散 + 相关），区别只是 Brown 给出了生成方法；两者都不要求某个特定比例。rubric 可统一写成："字号集合小（≤ 6–7 级）且相邻级比值稳定"。
- Spiekermann 与 Butterick 在搭配上基本一致（同设计师的字体好配；角色固定），但 Spiekermann 额外指出"只用一种字体会太灰"——这给 VLM 题提供了一个"过度克制也是缺陷"的反向维度，与 Tschichold 的 "meagerness" 呼应。
- SP-01 是这批书中最适合 web 的关系型规则：响应式页面里 cpl 随视口变化，line-height 应随之联动；这一点 Bringhurst（"suits the … measure"）、Spiekermann、Butterick 的区间写法都能兼容。

### Gaps
- Spiekermann 的页码由 PDF 跨页反推，未对照纸本；第 3 版与第 4 版之间的措辞差异未比对。
- Tim Brown 2018 年的《Flexible Typesetting》未检索，其关于 web 响应式字号/行长的更新观点未纳入。

---

## Q7. 各书数字规则的分歧，以及哪些被作者明确当作原则而非公式

### Takeaway
真正冲突的数字集中在 **行长上限（75 vs 80 vs 90）**、**行距（Butterick 上限 1.45 vs WCAG 下限 1.5）**、**段落间距（4–10pt vs 一整行 vs 1.5×行距）**、**标题字号跳跃（最小可见增量 vs 1.618 黄金比）**、**齐行（有断字即可 vs web 上别用）**。几乎所有作者都在原文里把数字降格为"惯例/建议/工具"：Bringhurst 用 "widely regarded"，Brown 说 "tools—not dogma"，Müller-Brockmann 说 "aid, not a guarantee"（二手），只有 Butterick 明确称之为 "rules"。

### Cited Findings

**分歧 1：行长**
- Bringhurst：单栏 45–75，66 理想；多栏 40–50 — 一手 — [webtypography.net 2.1.2](http://webtypography.net/2.1.2)
- Butterick：平均 45–90 — 一手 — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- WCAG 2.2 SC 1.4.8（AAA）："Width is no more than 80 characters or glyphs (40 if CJK)." — 一手 — [W3C Understanding 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)
- Spiekermann：90 字符一行 "almost too wide"（且需配 8 on 12 的大行距）；45 与 60 字符的示例被视为正常 — 一手 — [Stop Stealing Sheep 4e](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)
- 小结：Butterick 的 90 上限恰是 Spiekermann 的"几乎太宽"，也高于 Bringhurst 的 75 与 WCAG 的 80
- 屏幕阅读研究：Dyson & Haselgrove (2001) 建议约 55 cpl 平衡速度与理解；Dyson & Kipping (1998) 报告 100 cpl 读得比 25 cpl 快、理解相当；Shaikh (2005) 读者偏好两极（35 或 95 cpl）— 等级：二手（经 Wikipedia 转述）— [Wikipedia: Line length](https://en.wikipedia.org/wiki/Line_length)

**分歧 2：行距**
- Butterick：120–145% — 一手 — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- Rutter：web 上 "figures upwards of 1.3 are common" — 一手 — [webtypography.net 2.2.1](http://webtypography.net/2.2.1)
- WCAG SC 1.4.8（AAA）："Line spacing (leading) is at least space-and-a-half within paragraphs," — 一手 — [W3C](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)
- Bringhurst：不给数字，"suits the typeface, text and measure" — 一手 — [webtypography.net 2.2.1](http://webtypography.net/2.2.1)
- Spiekermann：不给比例，给关系——行距 > 词距；每行越长行距越大（示例从 8/9 到 8/12，即 112.5%–150%）— 一手 — [Stop Stealing Sheep 4e](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)

**分歧 3：段落分隔与段间距**
- Bringhurst：首段齐左；后续段缩进至少 1 en — 一手（标题）— [webtypography.net 目录](http://webtypography.net/toc/)
- Butterick：缩进 1–4× 字号 **或** 段间 4–10pt，"Don't use both." — 一手 — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- Rutter：段间距 = 一整行行高（如 1.5em）— 一手 — [webtypography.net 2.2.2](http://webtypography.net/2.2.2)
- WCAG 1.4.8（AAA）："paragraph spacing is at least 1.5 times larger than the line spacing." — 一手 — [W3C](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)

**分歧 4：大写字距**
- Bringhurst 5–10%；Butterick 5–12%；Rutter 0.1em — 一手 — [webtypography.net 2.1.6](http://webtypography.net/2.1.6)；[Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)

**分歧 5：标题字号跨度**
- Butterick："Use the smallest increment necessary to make a visible difference."（12pt 正文不必上 14/15pt）— 一手 — [Headings](https://practicaltypography.com/headings.html)
- Bringhurst 经典刻度相邻级 12→14→16→18（≈1.14），Rutter 的 CSS 示例 12/14/18/24/36 — 一手（CSS）/二手（刻度表）— [webtypography.net 3.1.1](http://webtypography.net/3.1.1)
- Tim Brown 示例用 1.618 — 一手 — [A List Apart 2011](https://alistapart.com/article/more-meaningful-typography/)

**分歧 6：齐行（justify）**
- Butterick：可以，但必须配断字 — 一手 — [Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- Rutter（webtypography.net）："So don't justify text on the web." — 一手 — [webtypography.net 2.1.3](http://webtypography.net/2.1.3)
- WCAG 1.4.8（AAA）："Text is not justified" — 一手 — [W3C](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)
- Bringhurst：条件式（窄栏、无衬线、等宽倾向 ragged）— 一手 — [webtypography.net 2.1.3](http://webtypography.net/2.1.3)

**分歧 7：字体/字号"种类"计数**
- Butterick：字体 ≤2，第三种少见 — 一手 — [Mixing fonts](https://practicaltypography.com/mixing-fonts.html)
- Tschichold：好例 "only 5 different types"，坏例 7 种 type and type sizes — 一手 — [Tschichold 读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)
- Smashing 课堂练习：只用 3 个字号（并声明可打破）— 二手 — [Smashing 2022](https://www.smashingmagazine.com/2022/10/typographic-hierarchies/)

**分歧 8：衬线/无衬线搭配**
- Butterick 明确否定"只能 serif + sans"，并说低对比搭配可能更有效 — 一手 — [Mixing fonts](https://practicaltypography.com/mixing-fonts.html)
- Spiekermann 同样认可同设计师/同时代甚至跨时代混用，并首推同一扩展家族；与 Butterick 的"同一设计师的字体搭配"法（他称这种机械方法 "works reliably"）一致（**此处两书是共识，不是分歧**）— 一手 — [Stop Stealing Sheep 4e](https://fonts.google.com/knowledge/stop_stealing_sheep.pdf)；[Mixing fonts](https://practicaltypography.com/mixing-fonts.html)

**原则 vs 公式（作者自述）**
- Bringhurst：数字用 "widely regarded" 措辞；scale 规则说 "Use the old familiar scale, or use new scales of your own devising" — 一手 — [webtypography.net 2.1.2](http://webtypography.net/2.1.2)；[3.1.1](http://webtypography.net/3.1.1)；"break the rules … beautifully, deliberately and well" — 二手 — [Quotepark](https://quotepark.com/fr/citations/837566-robert-bringhurst-by-all-means-break-the-rules-and-break-them-beaut/)
- Tim Brown："tools—not dogma"、"educated suggestions" — 一手 — [A List Apart 2011](https://alistapart.com/article/more-meaningful-typography/)
- Butterick：自称 "rules"（ten minutes 页），但 maxims 页的 "When in doubt, try it both ways"、"Imitate what you like" 是判断法 — 一手 — [Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html)；[Maxims](https://practicaltypography.com/maxims-of-page-layout.html)
- Müller-Brockmann：一面说 "laws of universal validity"（一手），一面说 "aid, not a guarantee"（二手）— [读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/MullerBrockmann_Grid_Des-Phil.pdf)；[Draw Down](https://draw-down.com/products/grid-systems-in-graphic-design)
- Tschichold：反对一切 "preconceived idea of form"，同时提倡单元构造的 "standardization" — 一手 — [读本 PDF](https://openlab.citytech.cuny.edu/langecomd3504fa2019/files/2018/10/Tschichold_NewTypo.pdf)

### Inferences

**冲突处理建议（写 rubric 时）**
- 行长：硬区间取交集更稳 → 正文 **45–75 cpl** 为"好"，75–90 为"可接受"，> 90 或 < 40 为"差"；多栏/卡片 40–50。中文/CJK 另用 WCAG 的 40 上限思路（Bringhurst/Butterick 都没有给 CJK 数字）。
- 行距：Butterick 与 WCAG 不可同时满足（1.45 < 1.5）。审美 rubric 建议 **1.3–1.6** 为"好"带，< 1.2 或 > 1.8 为"差"；WCAG AAA 作为可访问性加分项而非审美扣分项。
- 段间距：Butterick 的 4–10pt 明显小于 Rutter 的"一整行"。建议只判**"缩进与段间距二选一"**和**"段间距 > 行内行距"**（即段落之间要比行之间明显更开），不判具体 px。
- 标题跨度：只判"字号集合小且离散 + 层级单调"，不判具体 ratio；"相邻级是否有可见差异" 交给 VLM。
- justify：只在 "窄栏 + 无 hyphens" 时扣分（三方都能同意的交集）。

**汇总：可验证 rubric 规则表（按判定方式分组）**
- 程序可判（`DOM`）
  - 正文 cpl ∈ [45,75]（单栏）/ [40,50]（多栏） — BR-01、BU-04、W3C
  - 多视口 × 多根字号下 cpl 保持在区间内 — RU-01
  - line-height/font-size ∈ [1.3,1.6] 且 unitless — BR-02、BU-03、RU
  - line-height 随 cpl 增大而增大；行间空白 > 词间空白 — SP-01
  - 正文字号 ∈ [15,25]px（桌面） — BU-02
  - 垂直间距为基准行高整数倍 — BR-03、RU-02
  - 去重字号 ≤ 6–7 个且无 ±1px 近重复；相邻比值稳定 — BR-04、TB、TS-02
  - 字体族 ≤ 2（3 为上限）；段内不混字体 — BU-05
  - 全大写块 ≤ 1 行且 letter-spacing ∈ [0.05,0.12]em；小写正文不加字距 — BR-05、BU-07
  - 无 bold+italic 叠用；非链接无下划线 — BU-06
  - 多行正文不居中 — BU-08、TS-01
  - 缩进与段间距二选一 — BR-07、BU-09
  - justify 必须配 hyphens，窄栏不 justify — BR-06、BU-10、RU-04
  - 标题样式级数 ≤ 3；同级标题样式一致 — BU-11、（LU 未核实）
  - heading level 与视觉显著度单调一致 — TS-03
  - 块元素左/右缘聚类：近邻不等边缘少 — MB
- 程序定位 + 视觉判好坏（`DOM+VLM`）
  - justify 是否真的产生 rivers — BR-06
  - 同类组件是否"看起来一样" — BU-12 consistency
  - 层级是否表达了内容重要度 — TS-03
- 只能视觉判（`VLM`）
  - 背景是否抢正文（foreground/background）— BU-12
  - 相邻层级是否"刚好可见、不过度" — BU-11
  - 装饰是否多余 / 整体是否 clear — TS-01、TS-02
  - 不对称是否有序而非混乱；克制是否沦为 "meagerness" — TS-04
  - 字体对比是否成了 gimmick / 全页是否"太灰" — SP-05
  - 网格是否单调、缺少焦点（succumb to regularity，未核实出处）— SA-01

### Gaps
- 本次未检索 WCAG 2.2 SC 1.4.12 Text Spacing（AA）的具体数值，未纳入。
- CJK（中文）排版的行长/行距数字，本批西文经典均未涉及；若评测对象含中文页面，需要另找来源（如 W3C《Requirements for Chinese Text Layout》）。
- 没有找到任何一本书给出"居中正文最多几行"的数字；rubric 中的"≥3 行即扣分"是自定阈值。

