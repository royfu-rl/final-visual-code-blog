# 专家评审团怎么评 Web 视觉设计，rubric 加 anchor 示例怎么校准评审

> 检索日期：2026-11-03
> 核实等级：**一手** = 本人读过原始页面、原文或摘要；**二手** = 只见于转述、聚合页或搜索摘要；**未核实** = 记忆中有印象，但没找到来源
> 说明：WebFetch 工具对长引文有 125 字符限制，所以部分奖项页面是"首句原文 + 意译"，下文会逐条标明

---

## Q1 设计奖评审团用什么 rubric（标准、权重、分制、评审构成、终选机制）

### Takeaway
真实的 Web 设计奖都有明文标准。Awwwards 是唯一公开权重的：Design 40 / Usability 30 / Creativity 20 / Content 10，评审 ≥18 人，去掉 3 个离群分。但几乎所有奖项都只公布"维度名 + 一两句定义 + 分数阈值"，没有公布每一档分数的描述。真正把标准对齐的，是评审之间的讨论、往届获奖作品库（事实上的 anchor）和多人聚合，而不是 rubric 文本本身。

### Cited Findings

- **Awwwards**（[about-evaluation](https://www.awwwards.com/about-evaluation/)，一手）
  - 权重原文："Design: 40% points"、"Usability: 30% points"、"Creativity: 20% points"、"Content: 10% points."
  - 评审人数：提交作品发给 "a minimum of 18 jury members"
  - 聚合规则：3 个离均值最远的分 "furthest from the average are automatically eliminated by our system"
  - 公众票：只计 "votes made by Professional users (who have passed through our validation system)"
  - 获奖阈值
    - Honorable Mention：jury 分 "6.5 or more"
    - Site of the Day：jury 分最高者；"a high score from the jury and at least 10 PRO users" 可以提前定 SOTD，否则等 5 天投票期结束
    - Developer Award：SOTD 站点再交给 developer jury，"higher than a 7" 获奖
    - Site of the Month：当月最高分的 8 个站点再评一轮，用户票最多者获得额外权重
  - 分制：官方页面没写明是 1–10 分制。1–10 分制只见于 Wikipedia 和评委个人博客（二手，[Wikipedia](https://en.wikipedia.org/wiki/Awwwards)、[hontran.dev](https://www.hontran.dev/blog/awwwards-judging-criteria)）
  - 冲突：部分二手来源把 Mobile 列为额外维度，和官方四维不一致（二手，同上）

- **CSS Design Awards**（[about](https://www.cssdesignawards.com/about)，一手）
  - Public Awards 三个类别 UI / UX / Innovation：需要在至少一个类别获得 "more than 20 votes"，并且 judge 平均分 "above 6"
  - WOTD：评审团打分取平均，门槛平均分 above 8.00，页面注明门槛 "varies depending on quality of the sites submitted"
  - Special Kudos：原文 "Sites, except WOTDs, that receive an average of above 6 receive an official Special Kudos certificate."
  - WOTY：从 WOTM 和部分 WOTD 中产生，具体决选方式页面未写
  - 评审构成：[2026 judges 页](https://www.cssdesignawards.com/judges)标题为 "CSSDA Official Judging Panel For 2026"，共 4 页，第 1 页列出 28 人（一手，不完整）
  - UI / UX / Innovation 三个维度的定义文字没有找到（见 Gaps）

- **The Webby Awards**（[judging-criteria](https://www.webbyawards.com/judging-criteria/)，一手；首句为原文，其余为意译）
  - 网站类共 7 个维度，比常见说法多一个 Innovation
    - Content："Content is the information provided on the site." 不只是文字，还包括音视频和动画；要吸引人、贴合受众、有明确立场
    - Structure & Navigation："Sites with good structure and navigation are consistent, intuitive, and transparent." 用户能预判内容在哪并快速到达
    - Visual Design："Visual design is the appearance of the site." 要高质量、贴合受众和信息，兼顾学习、认知、低视力障碍用户；不必追潮流
    - Functionality："Good functionality means the site works well." 加载快、链接有效、跨平台跨浏览器、照顾低带宽用户
    - Interactivity："Good interactivity is more than a rollover or choosing what to click on next." 新版加入了是否用 LLM、ML 等 AI 打造下一代体验
    - Innovation："Innovative work often pushes the boundaries of what's been done before." 用了 AI 的话，要能提升创造力或可用性，并且用得正当
    - Overall Experience："Demonstrating that sites are frequently more or less than the sum of their parts" 包括回访、收藏、分享、停留时长等无形因素
  - 评审流程（[judging-process](https://www.webbyawards.com/judging-process/)，一手）
    - Round 1：Associate Members 独立评审，"rating each one based on its respective judging criteria"，"Every entry is evaluated by multiple Associate Academy Members."
    - Round 2：有该类别专长的 Executive Members 评审 shortlist，投票决出 Honorees / Nominees / Winners；每个类别 5 个 nominee、1 个 winner；Honoree 名额 "No more than 20% of entries"；平票由 Jury President 裁决
    - "Consulting for the voting process ... is provided by KPMG."
  - 页面没给出权重、Round 1 分制或分数归一化方法
  - 二手补充：总评审规模约 2,000 人；终轮用 approval voting；Webby 自述引入了"更精细的数学方法处理评委打分差异"（[iadas.net](https://www.iadas.net/webbyoverview/)、[webbyawards.com 博文](https://www.webbyawards.com//mathematicians-engineers-and-logic-nerds/)，均来自搜索摘要）

- **Red Dot：Brands & Communication Design**
  - 评审方式（[Red Dot magazine](https://red-dot.org/magazine/how-to-convince-the-red-dot-jury-this-is-what-the-experts-for-communication-design-pay-attention-to)，一手）
    - 24 名国际专家连续多天现场评审，每件作品单独讨论，最终只以团队方式决定
    - 考量点：design concept、implementation、choice of medium、originality、recognition value、能否向目标人群清楚传达信息、能否留下持久情感印象
    - 页面明说：标准随项目类型变化，每位评委带着由经历和文化背景形成的个人预期，团队讨论用来平衡这些个人视角
    - 评委原话举例："Sometimes, it is enough when it is simple and well thought through."（Damon Aval）
  - 2023 年 Communication Design 三条标准："Idea: originality & creativity; Form: design quality & innovation; Impact: understandability & emotionality"（二手，[Red Dot 2023 页](https://red-dot.org/communication-snippets-bcd-2023)的搜索摘要）
  - 2026 年评审团为 30 人（二手，搜索摘要）

- **D&AD**
  - 三条评审标准："a good idea, well executed, and relevant to the brief"；Yellow Pencil 授予 "outstanding, nails all the judging criteria" 的作品（二手，[dgi.or.id 转载的 D&AD 指南](https://dgi.or.id/?p=5998)）
  - 不设名额，某些评审团可能一个 Yellow Pencil 都不发；Black Pencil 由各评审团 foreman 再选（二手，同上；[LBB](https://lbbonline.com/news/The-DandAD-Jury-Room-Translated)）
  - 只有 0.47% 的参赛作品获得 Yellow Pencil（二手，评论文章 [manifest-media](https://manifest-media.in/advertising/250526/opinion-why-a-slick-case-video-wont-crack-dads-code.html)）

- **Communication Arts（Interactive）**
  - 评审独立投 "in / out"，过半数进入决赛；决赛重新独立评审，简单多数决出获奖者（二手，第三方竞赛列表 [internshala](https://internshala.com/competitions/communication-arts-ca-2027-interactive-competition/)）
  - 官方 [2026 interactive 页](https://www.commarts.com/competition/2026-interactive)称评审团是 "internationally representative panel of distinguished developers, interface designers and creative directors"（二手，搜索摘要）

### Inferences
- 各奖项的维度高度重合，都是视觉 / 设计质量、可用性 / 结构、创意 / 创新、内容。可以看作业界事实上的"四维 rubric"；只有 Awwwards 给了权重
- 奖项 rubric 是**粗粒度**的，只有维度名和一句定义，没有逐档描述。一致性来自三个机制
  - ① 多评委聚合加去离群分（Awwwards 去 3 个，Webby 多人 Round 1）
  - ② 评审讨论对齐（Red Dot、D&AD）
  - ③ 往届获奖作品库作为隐性 anchor。Awwwards 和 CSSDA 公开的 SOTD / WOTD 作品集，本身就是事实上的视觉 exemplar 库
- 所以给 AI judge 一份"维度 + 权重 + 阈值"的 rubric，只复刻了第一层；要复刻人类评审，还需要可比对的视觉样例

### Gaps
- CSSDA 对 UI / UX / Innovation 的定义文字和分制没找到
- Awwwards 的 1–10 分制没在官方页面核实
- Webby 网站类 7 个维度是否加权、Round 1 用几分制、分数怎么归一化，都没找到官方说明
- ADC（The One Club）的评审标准没检索到
- Red Dot 2026 年最新标准没核实
- 没有找到任何奖项公开的评委间一致性数据（kappa、ICC 等）

---

## Q2 业界从业者怎么评（NN/g、设计评审框架、公司设计 QA 清单）

### Takeaway
从业者框架分两类。一类是原则 / 启发式，比如 NN/g 的 heuristic #8 和五条视觉设计原则；值得注意的是，NN/g 讲每一条原则都配了真实产品截图。另一类是工程化 QA 清单，比如 Vercel Web Interface Guidelines，可检查性强，但几乎不涉及审美。设计评审框架（Connor & Irizarry）强调评价要锚定目标，不能只是个人反应。

### Cited Findings

- **NN/g heuristic #8 "Aesthetic and Minimalist Design"**（[NN/g，2021-01-24](https://www.nngroup.com/articles/aesthetic-minimalist-design/)，一手）
  - 定义："Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility."
  - 要点
    - "Clarity will always win over visual flourish."
    - "Every piece of content should have a purpose, including negative space."
    - "Communicate; don't decorate."
  - 该启发式写于 1994 年

- **NN/g 视觉设计五原则**（[Kelley Gordon，2020-03-01，2026-09-01 复审](https://www.nngroup.com/articles/principles-visual-design/)，一手）
  - Scale："Using relative size to signal importance and rank in a composition."
  - Visual hierarchy："Guiding the eye on the page so that it attends to different design elements in the order of their importance."
  - Balance："A satisfying arrangement or proportion of design elements."
  - Contrast："The juxtaposition of visually dissimilar elements in order to convey the fact that these elements are different."
  - Gestalt："Principles that explain how humans simplify and organize complex images that consist of many elements."
  - **每条原则都配了真实视觉样例**：Medium、Uber、Dropbox、Nike、iOS Reminders、IRS Form 1040 等截图

- **Connor & Irizarry《Discussing Design》（O'Reilly，2015）**
  - 评审框架是四个问题：目标是什么 → 哪些元素与目标相关 → 这些元素是否有效 → 为什么（二手，[UIE](https://uxi.uie.com/blog/improve-your-designs-using-critique)、[书评](https://www.designative.info/2025/07/03/book-review-discussing-design-by-adam-connor-aaron-irizarry/)）
  - 核心区分："Critique is about evaluating a design against its goals"，而 feedback 可以只是情绪反应（二手，书评）
  - 引用该书的学术文章说："design feedback that lacks a framework is nothing more than a reaction"（二手，[UMN Libraries](https://umnlibraries.manifoldapp.org/read/effective-design-critique-strategies-across-disciplines-67a61290-9f8f-4550-b00c-ec5e50277482/section/fede7300-cdcc-42fb-8698-8ef74b177d9d)）

- **Vercel Web Interface Guidelines**（[GitHub README](https://github.com/vercel-labs/web-interface-guidelines)，一手）
  - 自述："a living, non-exhaustive list of those decisions"
  - 结构：Interactions / Animations / Layout / Content / Forms / Performance / Design / Copywriting，共约 130 条加粗规则
  - 与审美相关的条目
    - "Optical alignment. Adjust ±1px when perception beats geometry."
    - "Deliberate alignment. Every element aligns with something intentionally ... No accidental positioning."
    - "Balance contrast in lockups."
    - "Layered shadows. Mimic ambient + direct light with at least two layers."
    - "Nested radii. Child radius ≤ parent radius & concentric so curves align."
    - "Hue consistency. On non-neutral backgrounds, tint borders/shadows/text toward the same hue."
    - "Minimum contrast. Prefer APCA over WCAG 2"
  - README 里没有嵌入图片，只有部分条目外链到 X 上的演示视频或帖子
  - 配套给 agent 用的 `web-design-guidelines` skill，用来审查 UI 代码

### Inferences
- 从业者的"原则"天然是配图讲的（NN/g）。抽象词像 balance、hierarchy，脱离样例几乎无法操作化
- 工程化清单（Vercel）适合做底线 QA，可自动检查，但覆盖不了"好不好看"。审美判断仍要靠原则加样例

### Gaps
- GOV.UK Design System / Service Standard 的设计评审清单、Atlassian design review 流程，这次没检索
- 《Discussing Design》原书没读，四问框架只有二手转述

---

## Q3 前沿 AI 实验室写给模型的设计指南（具体标准、有没有视觉示例）

### Takeaway
Anthropic 和 OpenAI 都公开了给模型的前端设计指南。内容是"反默认值"清单加流程（先规划、再自审、截图自评），都**不含好 / 坏设计的对比图**。OpenAI 明确建议给模型 "reference screenshots or mood boards"，Anthropic 要求模型截图自评（"a picture is worth 1000 tokens"）。也就是说，两家都承认视觉输入有用，但都没把视觉 anchor 写进指南本身。

### Cited Findings

- **Anthropic `frontend-design` skill**（[GitHub anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)，一手，原文全文已读）
  - 版本：当前版本来自 2026-09-03 的 commit 41bbe19 "Update frontend-design skill to avoid generic design defaults (#1713)"；目录里只有 SKILL.md 和 LICENSE.txt，**没有任何图片或示例**
  - 当前版本的具体标准
    - 角色设定："the design lead at a design studio known for giving every client a distinct visual identity"
    - 字体："use one family or two, and if two, make them clearly distinct"；"set a clear type scale following ... The Elements of Typographic Style"；"Default to line lengths of less than 80 characters."
    - 列为生成页面 "commonest tells" 的排版：只强调标题中一个词、标签全大写、多余的标签
    - "Visual structure is information." 编号 01 / 02 / 03 只在内容真是序列时才用
    - 动效："A single orchestrated moment ... lands better than scattered effects; fade-and-slide-up entrances on each section ... read as AI-generated."
    - 给模型 "For calibration" 列出 5 类 AI 生成设计的聚集特征
      - ① 暖奶油底（near #F4F1EA）+ 高对比衬线 + 陶土色强调（near #D97757）
      - ② 近黑底 + 单一酸绿或朱红强调
      - ③ 报纸式细线、零圆角
      - ④ SaaS 卡片套件：统一圆角、rgba(0,0,0,.1) 阴影、渐变装饰
      - ⑤ 模板化装饰：全大写 eyebrow、"A · B · C"、"WORD — fragment"、#0B0B0B、等宽小标签、"→"
    - 流程：先写 4–6 个具名 hex 色、字体角色、ASCII 线框、原则 → 对照 brief 复查是否落入默认值 → 再写代码
    - 自评："taking screenshots to review if your environment supports it — a picture is worth 1000 tokens"；"Spend your boldness in one place"；Chanel 的建议："remove one accessory"
    - 质量底线："responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes"
  - 旧版（2025-12-04 commit 0075614，一手）风格不同
    - "avoid generic 'AI slop' aesthetics"
    - "NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds)"
    - "NEVER converge on common choices (Space Grotesk, for example) across generations."
    - 鼓励 "Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic..."，以及 gradient meshes、noise textures、grain overlays
  - 演变：从"大胆、极端、加纹理"转向"克制、有据、反模板"。新版明确说 cream + terracotta 是 "Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell"

- **OpenAI《Frontend coding with GPT-5》cookbook**（[developers.openai.com](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_frontend)，一手，页面已标 archived；cookbook 索引日期为 2025-08-07，二手）
  - 没有具体审美规则，只推荐技术栈
    - 字体："San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope"
    - Tailwind、shadcn/ui、Radix Themes；Material Symbols、Heroicons、Lucide；Motion
  - **与 Anthropic 旧版冲突**：OpenAI 推荐 Inter，Anthropic 旧版禁用 Inter
  - 含视觉示例：附有生成结果截图（复古暗色和亮色落地页、用输入的 dashboard 图生成的登录页、霓虹贪吃蛇）

- **OpenAI《Designing delightful frontends with GPT-5.4》**（[developers.openai.com/blog](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)，一手；页面无日期，The Decoder 报道日期为 2026-03-22，[the-decoder](https://the-decoder.com/openai-publishes-a-prompting-playbook-that-helps-designers-get-better-frontend-results-from-gpt-5-4/)，二手）
  - Hard rules 原文
    - "Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak."
    - "Cards: Default: no cards. Never use cards in the hero."
    - "Background: Don't rely on flat, single-color backgrounds; use gradients, images, or subtle patterns to build atmosphere."
    - "Do not use inset hero images, side-panel hero images, rounded media cards"
  - 其他规则（意译）：首屏只放品牌、一个标题、一句辅助文案、一组 CTA、一张主图；每个 section 只做一件事；至少 2–3 处有意图的动效；用 CSS 变量；避免 purple-on-white；避开 Inter / Roboto / Arial / system 字体
  - 视觉输入："Reference screenshots or mood boards help the model infer layout rhythm, typography scale"；建议先让模型 "first generate a mood board or several visual options"
  - 自审：用 Playwright "iteratively inspect its work, validate behavior, and refine implementations"；`frontend-skill` 里有 "Litmus Checks"，比如 "Is the brand or product unmistakable in the first screen?"、"Would the design still feel premium if all decorative shadows were removed?"
  - 视觉示例：只有 1 张 GPT-5.4 生成的 mood board 图，**没有好 / 坏对比**
  - 注意冲突：OpenAI 5.4 鼓励用渐变或图案做背景，Anthropic 新版把 "gradient washes as decoration" 列为 AI 默认特征

- **Google / Gemini**：没找到官方前端设计 prompting 指南。检索结果只有第三方博客，其中一篇甚至建议把 Anthropic 的 frontend-design skill 粘进 Gemini 的 system instruction（二手，[recapio](https://recapio.com/digest/gemini-3-0-flash-designer-easiest-cheapest-way-to-make-awesome-frontends-by-aicodeking)）

### Inferences
- 两家实验室的指南本质上都是"负面清单 + 生成流程"，是写给生成器的，不是写给评审器的 rubric：没有维度权重，也没有分档描述
- 两家都依赖视觉回路（截图自评、mood board），但没有提供已校准的视觉 anchor（这张 = 好、这张 = 差，以及原因）
- 两家规则会互相冲突（Inter、渐变背景），而且会快速迭代，Anthropic 一年内就改了两次。用文字列表定义审美不稳定；视觉 anchor 能更直接地传递目标分布

### Gaps
- OpenAI 5.4 博文的确切发布日期、`frontend-skill` 的完整 Litmus Checks 原文，没拿到
- Google DeepMind 或其他实验室（xAI、Meta）有没有官方设计指南，没找到
- 没有找到任何实验室公开"给 judge 模型用的设计评分 rubric"

---

## Q4 rubric + anchor / exemplar 能否提升评分一致性（教育测量证据）

### Takeaway
最常被引用的综述 Jonsson & Svingby（2007，75 项研究）的结论是：rubric 能提升评分可靠性，"especially if they are analytic, topic-specific, and complemented with exemplars and/or rater training"。艺术类最成熟的大规模评分 AP Studio Art 的做法，正是用 sample portfolios 锚定 0–4 分的每一档。

最直接的量化证据来自 LLM 评分：只给 rubric 时 QWK = 0.40，加入 anchor papers 后 QWK = 0.69–0.72，接近人–人一致性 0.79。

反方提醒：CAT（创造力共识评估）故意不给 rubric，靠领域专家的隐性标准，也能达到 α ≈ .8–.9；前提是评委必须是真专家。

### Cited Findings

- **Jonsson & Svingby（2007），Educational Research Review 2(2):130–144**（[ERIC 摘要](https://eric.ed.gov/?id=EJ796733)，一手，原文）
  - "Several databases were searched for empirical research on rubrics, resulting in a total of 75 studies relevant for this review."
  - "Conclusions are that: (1) the reliable scoring of performance assessments can be enhanced by the use of rubrics, especially if they are analytic, topic-specific, and complemented with exemplars and/or rater training; (2) rubrics do not facilitate valid judgment of performance assessments per se."
  - "rubrics make expectations and criteria explicit, which also facilitates feedback and self-assessment."

- **Brookhart（2018），Frontiers in Education**（[链接](https://www.frontiersin.org/articles/10.3389/feduc.2018.00022/full)，一手摘要）
  - 综述 2005–2017 年高教 rubric 研究，共 51 个 rubric，其中 "7 out of 51" 用的是 rating-scale 式语言，不是质量描述
  - "no relationship was found between type or quality of rubric and study results"

- **AP Studio Art（Myford & Mislevy 1995，CRESST Tech Report 402）**（[PDF](https://cresst.org/wp-content/uploads/TECH402.pdf)，一手，全文已读）
  - Anchor 机制
    - Chief Reader 和 Table Leaders "spend two full days examining, discussing, and selecting sample portfolios"
    - 这些作品集 "exemplify the various points on the 0-4 rating scale"
    - 再由 25 名阅卷人讨论样例，"to clarify meanings of each of the scoring criteria and to attempt to reach consensus"
    - 目标是 "to have the readers internalize the standards, so that they can use the scoring rubrics in a consistent fashion"
  - 历史
    - "Before 1992, the meanings of rating scale values were conveyed only through training procedures, discussions, and feedback ... (i.e., via an oral tradition)."
    - 1992 年才引入书面通用 rubric，1994 年改为分部分 rubric
    - 也就是说，是先有 exemplar，后有文字 rubric
  - 一致性数据
    - 同一部分两位阅卷人的相关 "average about .65"
    - 小节 C-1："between-reader correlation of .58 and a reliability of .73"（Spearman-Brown 校正）
    - 相差 ≥2 分的分歧约 1–2%："about 500 of the 50,000 ratings made in the 1992 reading"，由 Chief Reader 复核
  - 现行做法：每份作品集至少 7 位阅卷人（二手，[EdWeek 2013](https://www.edweek.org/teaching-learning/thousands-of-ap-studio-art-portfolios-assessed-in-salt-lake-city/2013/07)）

- **LLM 评分中的 anchor 效应：Choi, Tate, Ritchie, Nixon, Warschauer（UC Irvine，2025-04-20，EdArXiv 预印本）**（[OSF](https://doi.org/10.35542/osf.io/cbhgz_v1)，一手，全文已读；未见同行评审信息）
  - 人类基线
    - 评分员经过 "a three-hour training session where they used the rubric and anchor papers"
    - 人–人：exact 51%，within-1 92%，QWK 0.79
  - GPT-4o（temperature 0.1）结果，原文 Table 3

    | Prompt | QWK | Exact % | Within-1 % |
    |---|---|---|---|
    | Rubric | 0.40 | 29.08 | 74.69 |
    | Rubric + Source | 0.46 | 30.96 | 76.99 |
    | Rubric + Full Anchors（每档 3 篇，共 18 篇） | 0.69 | 44.81 | 92.46 |
    | Rubric + Source + Full Anchors | **0.72** | 46.37 | 93.68 |
    | Rubric + Source + 1 Anchor / 档 | 0.65 | 41.14 | 88.59 |
    | Rubric + 只锚 1 分和 6 分 | 0.59 | 41.14 | 87.78 |
    | Rubric + 只锚 1、3、6 分 | 0.39 | 32.79 | 76.78 |
    | Rubric + 每档 1 篇 | 0.69 | 46.23 | 92.26 |

  - 结论原文："adding full anchors to the rubric increased QWK by 0.29"；"including at least one anchor per score is more effective than relying solely on rubric and source materials"
  - 关键细节
    - 每档都给 anchor 最好
    - 只给两端也有用（0.59）
    - 给 1、3、6 分反而更差（0.39）
    - 从 1 篇 / 档增加到 3 篇 / 档，QWK 只多 0.07

- **校准过的 exemplar 替代大量培训：Heldsinger & Humphry**
  - 2013，Educational Research（[DOI](https://doi.org/10.1080/00131881.2013.825159)，一手摘要）
    - 两阶段：先用成对比较把作品校准成量表，作为 "calibrated exemplars"；教师再 "judging which calibrated exemplar a performance was most alike"
    - "Teachers were not given extensive training and moderation."
    - exemplar 判断与 criterion-based rubric 判断 "correlated well"
  - 2020，Frontiers in Education（[链接](https://www.frontiersin.org/articles/10.3389/feduc.2020.00006/full)，一手）
    - 17 个 calibrated exemplars + 描述语
    - 12 名教师：平均评委间相关 0.835（范围 0.614–0.972）
    - 37 名评委：0.863（范围 0.602–0.997）
    - rater-average 相关 0.902 / 0.927
    - 但宽严差异仍在：SD 16 / 14，部分评委平均比别人低约 30 分
    - 每份约 7.4 分钟
    - **没有与纯 rubric 评分的直接对照**

- **其他 exemplar / 校准研究（只有摘要，缺数字）**
  - Bird & Yucel（AEHE，2012 online / 2013 刊期，DUAL 项目）（[DOI](https://doi.org/10.1080/02602938.2012.658155)，一手摘要）
    - rubric + "sample reports" + moderation 讨论之后，"demonstrators marking laboratory reports significantly closer to the marks awarded by an expert marker"
  - Sadler（2013，Assessment in Education）（[DOI](https://doi.org/10.1080/0969594x.2012.714742)，一手摘要）
    - 提出 "calibrated" 评审：无需持续 moderation，也能做出与同样经过校准的同事一致的判断
  - To, Panadero & Carless（AEHE 2022 online 2021）（[DOI](https://doi.org/10.1080/02602938.2021.2011134)，一手摘要）
    - 系统综述 40 项 exemplar 研究，exemplar 常与 rubric 联用
    - 但主要研究的是学生理解标准，不是评分者一致性
    - 并指出需要 "controlled manipulation of variables to disentangle the effects of exemplars"

- **反面 / 限制证据**
  - Bloxham et al.（AEHE 2016）（[DOI](https://doi.org/10.1080/02602938.2015.1024607)，一手摘要）
    - 24 名资深评分者的隐性标准在选择、排序、打分上都有差异
    - "assessment decisions at this level are so complex, intuitive and tacit that variability is inevitable"
  - **CAT（Amabile）**：Kaufman, Baer, Cole & Sexton（2008，Creativity Research Journal）（[PDF](https://www.rider.edu/sites/default/files/2024-05/CATRatersPoems.pdf)，一手，全文已读）
    - 程序：不给 rubric，评委 "use their own personal sense of what is creative in the domain ... to rate the creativity of the products in relation to one another"，独立评分、随机顺序、1–6 分
    - 专家组：10 人，α = .832
    - 新手组：106 人，α = .935；按 Spearman-Brown 标准化到 10 人后，专家 .804，新手降到 .575
    - 专家与新手评分的相关只有 r = .216
    - 文中综述："interrater reliabilities that typically exceed .70, and often range as high as the .90s"
    - 引用的早期研究：拼贴画的艺术家组 vs 心理学家组，组间相关只有 .44–.65

### Inferences
- "rubric + exemplar" 优于 "纯 rubric"，是教育测量的主流共识（J&S 2007），也是 AP Studio Art 这类艺术评分的实际做法（样例锚定每一档）
- 最干净的前后对照数字来自 LLM 评分：anchor 让 QWK 提高 0.29，从 0.40 到 0.69。这几乎就是"给 AI judge 加 anchor 示例"的直接实证，虽然对象是作文，不是视觉设计
- anchor 怎么放有讲究：要覆盖每一档，或至少覆盖两端；随便挑几档可能反而更差
- CAT 说明了另一条路：没有 rubric、只有专家的隐性品味也能一致，但要求评委是真专家。新手的一致性来自人数堆叠，和专家判断几乎无关（r = .216）。模型不是天然的专家，所以要用 exemplar 把专家的隐性标准外化
- exemplar 主要改善**排序 / 相关**，对宽严偏移（harshness）作用有限（Humphry 2020 中 SD 仍有 14–16）。AI judge 可能需要额外校准分数尺度

### Gaps
- 没找到在**视觉设计 / 艺术**领域、同一批评委下"纯 rubric vs rubric + exemplar"的 kappa 或 ICC 前后对照
- Jonsson & Svingby 全文没拿到（ScienceDirect 403），文中具体的一致性区间（如 percent agreement 范围）无法核实
- Weigle（1994 / 1998）等经典"培训前后"评分员研究没取到数据
- AP Studio Art 现行的一致性统计，只有 1992 年数据
- Choi et al. 2025 是预印本，未确认是否已发表

---

## Q5 比较判断（ACJ）在设计 / 艺术评估中的信度，与 rubric 打分对比

### Takeaway
ACJ 起源于 Design & Technology 作品集评估（Goldsmiths 的 e-scape 项目），报告的信度为 0.93 到 "0.95 or better"，远高于 AP Studio Art 的 rubric 评分（人–人相关约 .58–.65）。但 adaptive 算法会虚高 SSR：真实信度 0.70 时，SSR 可能显示 0.95。meta 分析给出的工程参数是：SSR 0.70 需要每件作品 10–14 次比较，0.90 需要 26–37 次。

### Cited Findings

- **Pollitt（2012），"The method of Adaptive Comparative Judgement"，Assessment in Education**（[DOI](https://doi.org/10.1080/0969594x.2012.665354)，一手摘要）
  - "a judge is asked to compare the work of two students and simply to decide which of them is the better"
  - "ACJ achieves extremely high levels of reliability, often considerably higher than practicable operational marking can achieve. It therefore offers a radical alternative to the pursuit of reliability through detailed marking schemes."
  - "ACJ is clearly appropriate for performances like writing or art, and for complex portfolios or reports"

- **Kimbell，e-scape（Goldsmiths TERU）**
  - "producing reliability statistics of 0.93: far higher than can be achieved in normal coursework assessment"（一手摘要，[Design and Technology Education 期刊](https://doi.org/10.24377/dteij.article2337)；OpenAlex 标的年份是 2024，疑为旧文重新上线，原始年份未核实）
  - "typically our trials have produced reliability statistics of 0.95 or better"（二手，[IAEA 会议文献](https://iaea.info/documents/adaptive-comparative-judgment-for-reliable-on-line-assessment/)的搜索摘要）
  - CJ 首次直接用于评估学生作品就是 e-scape，"in a Design & Technology context"（二手，[Wikipedia](https://en.wikipedia.org/wiki/Adaptive_comparative_judgement)）

- **信度虚高的批评**
  - Bramley（2015）：adaptive 机制会虚高 scale separation reliability，"for true reliability of 0.70, an SSR of 0.95 may be expected when using ACJ"（二手，转引自 [Frontiers 2022](https://www.frontiersin.org/articles/10.3389/feduc.2022.854378)；Bramley 原报告 [Cambridge Apollo](https://doi.org/10.17863/cam.110782) 没读到摘要）
  - IJTDE 2022 称该问题已被软件公司修正（二手，[Springer](https://link.springer.com/article/10.1007/s10798-021-09654-w)）
  - Wikipedia 称 ACJ 是否真的提升信度 "is not certain"（二手）

- **Verhavert et al.（2019）meta 分析，Assessment in Education 26(5):541–562**（[DOI](https://doi.org/10.1080/0969594x.2019.1602027)，一手摘要）
  - 共 49 个 CJ 评估
  - "For reliability levels of .70 between 10 and 14 comparisons per performance are needed. This rises to 26 to 37 comparisons for a reliability of .90."
  - 专家和同伴比新手更快到达信度渐近线
  - 2021 年有研究建议把指标上调到每件 41 次比较（二手，Frontiers 2021 的搜索摘要）

- **对照：AP Studio Art 的 rubric + exemplar 评分**（[CRESST 402](https://cresst.org/wp-content/uploads/TECH402.pdf)，一手）
  - 两位阅卷人在同一部分的相关约 .65，小节约 .58
  - 多人取平均后的信度约 .73

- **混合路线**：Humphry & Heldsinger 先用 CJ 校准出 exemplar 量表（PSI = 0.963），再让教师对照 exemplar 打分，评委间相关 0.835–0.863（[Frontiers 2020](https://www.frontiersin.org/articles/10.3389/feduc.2020.00006/full)，一手）

### Inferences
- 两个数字不能直接比：CJ 的 SSR（多评委、多次比较后的量表信度）和 rubric 的单对评分者相关，统计口径不同；而且 SSR 可能被 adaptive 机制虚高
- 但方向一致：对艺术 / 设计这类整体性、隐性标准强的作品，"相对比较"往往比"对照文字标准绝对打分"更可靠
- 对 AI 审美 judge 的启示
  - ① pairwise 判断（A 比 B 好）可以作为 rubric 打分的补充或替代
  - ② "CJ 校准 exemplar 量表 → 对照 exemplar 定档" 的两阶段法，正是 "rubric + 视觉 anchor" 的成熟人类范式

### Gaps
- Pollitt 2012 和 Kimbell 原文里具体的 D&T 作品集信度表没读到
- 没有找到同一批设计作品上"ACJ vs rubric 打分"严格对照的研究
- Bramley 2015 原文没读到
- No More Marking 在艺术或设计科目的具体信度数字没找到

