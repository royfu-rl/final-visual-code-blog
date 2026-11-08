# 界面 / 网页视觉审美的实证科学：共享核心、机制、主观天花板

> 服务目标：给 blog 两个论点提供证据——(1) 界面审美有一大块是共享的、能用知觉机制解释（所以专家 rubric 有意义）；(2) 有一块是主观的（所以任何审美 judge 都有天花板）。另外给每条 rubric 规则找「机制理由」。
> 与前序笔记 `VLM 审美 rubric 调研/rubric_judges_universality.md` 的关系：那里已有 Hönekopp 2006、Leder 2016、Chen 2022、Bignardi 2024、Güçlütürk 概要、Palmer & Schloss 80%、Ou & Luo、黄金比例、TASTE、DesignPref 基础数字。**本文只在需要时一句话引用（标「前序已有」），重点补一手数字、复现状态和机制。**
> 核实标记：**[一手]** = 本轮读过原文 / 作者 PDF；**[二手]** = 经另一篇论文或摘要页转述；**[未核实]** = 只见于检索摘要或聚合页。**[本文计算]** = 由原文数字换算；**[推断]** = 笔者推理。

---

## Q1. 首印象：50 ms 之类的数字是多少，复现得怎么样？

### Takeaway
- **「平均评分在 500 ms 就稳定」是稳的**：多项研究里，500 ms 与 10 s / 不限时的「跨网页平均评分」相关 r ≈ .53–.98，即使组间设计也有 r = .53。
- **「50 ms 就定型」不稳**：原始高相关（r ≈ .95–.97）来自重复呈现、无 mask 的被试内设计；加 mask、改组间后，50 ms 与 500 ms 只有 r = .12，与 10 s 只有 r = −.03。
- 但**复杂度和原型性的效应在 17–50 ms 已经存在**（Tuch 2012），说明粗粒度的布局信息（低空间频率）确实被极快加工。
- 所有这些「一致性」都是**跨人平均后**的一致性，不是人与人之间的一致。

### Cited Findings

**1. Lindgaard et al. 2006（BIT 25:115–126）**
- 三个研究，均 500 ms 呈现；研究 3 加了 50 ms 条件，用于检验 mere exposure 解释 — [Nature news 2006](https://www.nature.com/news/2006/060109/full/news060109-13.html) [二手]
- 相关系数（Tuch 2012 的转述）— [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [二手]
  - 研究 1：同一批网页 500 ms 看两遍，r = .97
  - 研究 2：500 ms vs 不限时，r = .98
  - 研究 3：50 ms vs 500 ms，r = .97
- Thielsch & Hirschfeld 2012 对同一结果的转述是「50 ms 组与 500 ms 组两阶段均 r = .95」，与 Tuch 的 .97 不一致 — [Thielsch & Hirschfeld 2012](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf) [二手]
- 7 个设计维度与 visual appeal 的 r²（聚合层面）— [websiteoptimization 摘要](https://websiteoptimization.com/speed/tweak/blink/) [未核实：第三方转述]
  - good–bad design .92、interesting–boring .91、good–bad color .90、good–bad layout .88、imaginative–unimaginative .86
  - clear–confusing .39
  - **simple–complex .01（p > .80）** —— 与后来 Tuch / Reinecke 的复杂度效应矛盾
- Lindgaard 等 2011 自己的复现降到 r = .73 — [Thielsch & Hirschfeld 2012 转述](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf) [二手]

**2. Tractinsky et al. 2004 / 2006（IJHCS 64:1071–1083）**
- 设计：40 名以色列被试，50 个网页，500 ms 与 10 s 两阶段 — [Tractinsky et al. 2004 workshop 版](http://www.ise.bgu.ac.il/faculty/noam/papers/04_ntacmk_final.pdf) [一手]
  - 跨网页平均分两阶段相关：z 分 r = .92，原始分 r = .92，R² = .85
  - 复现了 Fernandes et al. 2003（加拿大）的 r = .97
  - 越极端的评分反应越快：F(4, 1995) = 10.815, p < .001
  - 作者自己区分两类一致性：「跨用户平均后网页排序的一致」vs「个体内部一致」；后者见下条
- 期刊版摘要：平均层面一致，但「individual differences in evaluations and their consistency were considerable」 — [BGU 出版页](https://www.bgu.ac.il/researcher/noam-tractinsky/publications/349269701/) [未核实：经检索摘要]
- Tuch 2012 对其「反应时倒 U」的批评 — [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [一手]
  - 把所有人所有网页混在一起分析，2,261 个数据点只来自 19 人，自由度被严重夸大
  - 效应量很小：η²p = .02（Tractinsky 数据）/ .04（Tuch 数据）
  - 某一端点的 58 个评分里 16 个来自同一个人

**3. 关键复现：Thielsch & Hirschfeld 2012（Ergonomics 55:731–742）** — [作者 PDF](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf) [一手]
- 设计：N = 92，50 个网页，3 呈现时间（50 / 500 / 10,000 ms）× 3 滤波（原图 / 低通 LF / 高通 HF），**加 backward mask**，Latin square
- 批评早期研究的两个方法问题
  - 无 mask：≤ 50 ms 的刺激实际可见时间约多 250 ms
  - 同一人看同一网页两遍：被试想保持一致 + repetition priming → 一致性被高估
- 原图评分在不同呈现时间之间的相关（跨网页平均分）

  | 比较 | 被试内（全部 block） | 组间（仅第一个 block） |
  |---|---|---|
  | 50 ms vs 500 ms | .66 | **.12（n.s.）** |
  | 50 ms vs 10 s | .60 | **−.03** |
  | 500 ms vs 10 s | .83 | **.53** |

- 50 ms 时只有低空间频率有贡献：组间 原图–LF r = .32（p < .05），原图–HF r = .05
- 10 s 时 HF 更重要：原图–HF r = .76，原图–LF r = .53
- 被试内估计的相关在 LF 与短呈现条件下约是组间估计的 2 倍

**4. 其他复现**
- van Schaik & Ling 2009：先 500 ms 截图、后真实交互，两次评分只相关 .04 ≤ r ≤ .32；实验 2 为 .18–.54 — [Thielsch & Hirschfeld 2012 转述](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf) [二手]

**5. Tuch et al. 2012（IJHCS 70:794–811）：复杂度 × 原型性** — [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [一手]
- 刺激准备
  - 270 个公司网站由 267 名在线被试评 visual complexity（VC）和 prototypicality（PT），分 9 组、每组 ≥ 14 人
  - 组内一致性：**VC ICC = .82（SD .09），PT ICC = .78（SD .06）**（论文未写明是单人还是平均测量）
  - 选 120 个网页进 3（VC）× 2（PT）设计，每格 20 个
- 研究 1：N = 59，呈现时间 50 / 500 / 1000 ms（组间）
  - VC 主效应 F = 77.6，η²p = .581；PT 主效应 F = 241.4，**η²p = .812**；VC × PT 交互 η²p = .604
  - 呈现时间无主效应（η²p = .052）
  - 低 VC：高 vs 低 PT 的 d = 1.96；中 VC d = 1.79；**高 VC 时 d 只有 .24**（复杂度高时原型性救不回来）
- 研究 2：N = 82，80 个网页，17 / 33 / 50 ms
  - 17 ms：VC η²p = .38 > PT η²p = .19（复杂度先被加工）
  - 33 ms：VC .65 ≈ PT .66；50 ms：VC .57、PT .66
- 结论：低 VC + 高 PT 最美

**6. Reinecke et al. 2013 / 2014 的模型拟合**
- 2013（CHI）：复杂度 + 色彩度 + 人口学变量，**adj. R² = .48** — [Reinecke & Gajos 2014 脚注转述](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) [二手：同作者转述]
- 2014（CHI）：同一类模型在 3.2 万人数据上 — [Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) [一手]
  - **conditional R² = .47，marginal R² = .07**（Nakagawa 法）
  - 即：色彩度 + 复杂度 + 人口学这些**固定效应只解释约 7%**；剩下约 40 个百分点来自「网站 ID」和「被试 ID」两个随机截距
  - 作者明说该 R² 不能与 2013 的 adj. R² .48 直接比
  - 数据清洗：删掉了两轮评分相差 > 2 分（9 点量表）的 47,510 对评分（4.9%）；剩余两轮差值 SD = 0.7

### Inferences
- [推断] blog 里可以说「网页的相对好看程度在半秒内就基本定了」，**不宜**再说「50 ms」：最干净的组间 + mask 设计里，50 ms 和 500 ms 只相关 .12。
- [推断] 「首印象一致」被广泛误读：这些 r 都是**跨网页的平均分**之间的相关，衡量的是「群体均值稳定」，不是「人人看法相同」。这正好对应 blog 的两层论点：群体均值稳定 → rubric 有意义；个体分散 → 天花板。
- [推断] Reinecke 的「解释约一半方差」**不能**写成「复杂度 + 色彩度解释了一半审美」。可解释的知觉特征只占 7%；大块是「这个网站本身」的效应（共享但未被这两个特征捕获）和「这个人打分偏高 / 偏低」。
- [推断] Tuch 的 17 ms 结果 + Thielsch 的低频结果指向同一个机制：**最早进入审美的是全局布局（低空间频率）和杂乱程度**，细节（高频，如字体细节、图标）要到 500 ms 以后才起作用。所以 rubric 里「整体布局 / 留白 / 杂乱度」应排在「细节精致度」之前。

### Gaps
- Lindgaard 2006 原文本轮未取到；r = .97 vs .95 的出入无法裁决，两者都是二手。
- Tractinsky 2006 期刊版的个体层面一致性数字未取到（只有摘要定性描述）。
- Tuch 的 ICC .82 / .78 是单人还是平均测量，论文未写明（见 Q3 换算）。
- Reinecke 2013 原文 PDF 下载失败（404），其 R² 分解（复杂度单独 / 色彩度单独）未取到。

---

## Q2. 审美-可用性效应，以及 classical vs expressive aesthetics

### Takeaway
- 「好看的看起来更好用」在**使用前的感知层面**很稳（r ≈ .59–.88），但**不影响实际绩效**；方向和机制仍有争议（可能经由整体「goodness」评价中介）。
- **classical aesthetics = aesthetic, pleasant, clean, clear, symmetrical**（秩序 / 清晰）；**expressive aesthetics = creative, uses special effects, original, sophisticated, fascinating**（创意 / 新奇）。classical 与可用性的相关明显更高（.68–.78 vs .40–.46）。
- **没找到直接比较两者人际一致性的研究**。用 VisAWI 的组间 F 值换算，偏 classical 的 Simplicity 与偏 expressive 的 Diversity 的单人 ICC 几乎相同（.145 vs .146），所以「classical 更客观」目前没有直接证据。

### Cited Findings

**1. 审美-可用性效应**
- Kurosu & Kashimura 1995（CHI'95 短文，日立）：26 种 ATM 布局，美感与 apparent usability r = .589；美感对 apparent usability 的影响强于 inherent usability — [CHI'95 页面](https://chi1995.chistatic.hosting.acm.org/proceedings/shortppr/mk_bdy.htm) [二手：经检索摘要]；r = 0.59 另见 [Tractinsky et al. 2000 引述](http://www.ise.bgu.ac.il/faculty/noam/papers/00_nt_ask_di_iwc.pdf) [二手]
  - 「252 名被试」只见于二手博客 [未核实]
- Tractinsky 1997（CHI'97）：在以色列复现，「very high correlations」，日本与以色列的相关强度不同但方向与假设相反 — [Tractinsky 研究页](https://www.ise.bgu.ac.il/faculty/noam/research/aesthetics.html) [二手：作者页摘要，无数字]
- Tractinsky, Katz & Ikar 2000（Interacting with Computers 13:127–145） — [作者 PDF](http://www.ise.bgu.ac.il/faculty/noam/papers/00_nt_ask_di_iwc.pdf) [一手]
  - 132 名工科学生；从 26 个 ATM 布局里选 9 个；3（审美高 / 中 / 低）× 2（可用性高 / 低）
  - 使用前 感知审美–感知可用性 r = .66；使用后 r = .71
  - 使用后满意度与感知可用性 r = .87、与感知审美 r = .71
  - **审美对完成时间无影响**：F(2, 118) = 0.01, p = .987；对错误数也无主效应
  - 「信息量」与审美 r = −.26、与可用性 r = −.18 → 被试能区分概念，不是方法偏差
- UICrit（983 个移动 UI，7 名设计师）：数据集中 aesthetics 与 usability 评分 r = 0.875 — [UICrit 附录 A](https://arxiv.org/html/2407.08850v3) [一手]
- 方向与机制的争议
  - Hassenzahl & Monk 2010：美与感知可用性可能不直接相关，而经由整体评价「goodness」中介 — [Grishin 2019 转述](https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Grishin_Feb2019.pdf) [二手]
  - Tuch 等 2012（另一篇，CHB）：审美不影响感知可用性，反而可用性影响使用后的审美 — [检索摘要](https://uxpajournal.org/?p=4392) [未核实]

**2. Lavie & Tractinsky 2004（IJHCS 60:269–298）** — [作者 PDF](http://www.ise.bgu.ac.il/faculty/noam/papers/04_tl_nt_ijhcs.pdf) [一手]
- 四个研究的样本：125（2 个网站，41 个形容词 EFA）→ 212（Gap / Macy's 电商任务）→ 145（以色列网站，确认因素结构）→ 384（普通网民，效度）
- 研究 2 的命名依据：一个因子聚了「well organized, clear, clean, symmetrical」→ classical；另一个聚了「originality, fascinating design, using special effects」→ expressive；删掉所有负向措辞的条目
- 最终两个 5 条目量表
  - classical：aesthetic, pleasant, clean, clear, symmetrical；对应 Nasar 的「visual clarity」
  - expressive：creative, using special effects, original, sophisticated, fascinating；对应 Nasar 的「visual richness」
  - 作者把它们对应到环境美学里的 order / complexity（Arnheim、Kaplan、Nasar）
- 信度与相关（初始样本 / 交叉验证样本）
  - Cronbach α：classical .85 / .86；expressive .87 / .86；usability .95 / .95
  - classical–expressive r = .69 / .63（两者并不独立）
  - **usability–classical r = .68 / .78；usability–expressive r = .46 / .40**
  - classical 与其他构念相关 .60–.78；expressive 与其他构念 .37–.59
  - 性别、年龄与两者均无显著相关
- Moshagen & Thielsch 后来批评「symmetrical」「uses special effects」不是审美判断本身 — [BeauVis 论文转述](https://arxiv.org/pdf/2207.14147) [二手]

**3. classical vs expressive 的人际一致性（间接证据）**
- VisAWI 研究 5：512 人、42 个网站、每人只评 1 个网站；各分面在网站间的单因素 ANOVA F(41, 470) — [Moshagen & Thielsch 2010 Table 5](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) [一手]
  - Simplicity 3.07、Diversity 3.09、Colorfulness 2.09、Craftsmanship 2.54、总分 2.72
  - 最美 vs 最丑网站的 Cohen's d：1.86–2.57
- VisAWI 与 Lavie & Tractinsky 量表的相关：classical .52–.82，expressive .52–.82；Simplicity 主要对应 classical，Diversity 主要对应 expressive — [VisAWI Manual](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf) [一手]；[Moshagen & Thielsch 2010](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) [一手]

### Inferences
- [本文计算] 由 F 值换算单人 ICC(1) = (F − 1) / (F + k − 1)，k ≈ 512 / 42 ≈ 12.2 人 / 网站：
  - Simplicity ≈ .145、Diversity ≈ .146、Craftsmanship ≈ .112、**Colorfulness ≈ .082（最低）**、总分 ≈ .124
  - 即「偏 classical」与「偏 expressive」的人际一致性**几乎相同**；真正低的是**颜色**
  - 局限：组大小不等，k 是平均值；F 是 Table 5 报告值
- [推断] classical aesthetics 的价值不在于「更多人同意」，而在于它**和可用性绑在一起**（r .68–.78）。所以 rubric 里 clean / clear / organized 一类规则有双重理由：既是审美、也是可用性。
- [推断] 审美-可用性效应提醒 judge 设计者：**判「好用」的 judge 会被「好看」污染**（UICrit r = .875，Tractinsky r ≈ .66–.71）。如果 rubric 要分维度打分，审美和可用性维度的分数会高度相关，不能当作独立证据。

### Gaps
- Kurosu & Kashimura 原文的被试数、Tractinsky 1997 的具体 r 值本轮未取到。
- 没有找到任何直接比较「classical 条目」vs「expressive 条目」评分者间一致性（ICC / α across raters）的研究；上面的结论是由 VisAWI 分面换算的间接证据。

---

## Q3. 验证量表：VisAWI / VisAWI-S

### Takeaway
- VisAWI = 4 分面 18 条目，分面 α .85–.89，总分 α .94；VisAWI-S = 4 条目（每分面 1 条），α .76–.81，与全版 r = .91。
- 量表的「信度」都是**条目间内部一致性**（同一个人的条目之间），不是评分者间一致。用其 ANOVA 换算，**单个用户的评分者间 ICC 只有约 .08–.15**；手册建议每个网站 ≥ 20 人，换算后 20 人均值的信度约 .64–.77。

### Cited Findings

**1. VisAWI 18 条目（7 点同意度量表；英文为德文原版的翻译；(r) = 反向计分）** — [Moshagen & Thielsch 2010 Table 4](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) [一手]
- Simplicity（α = .89）
  - 1 The layout appears too dense. (r)
  - 5 The layout is easy to grasp.
  - 9 Everything goes together on this site.
  - 13 The site appears patchy. (r)
  - 17 The layout appears well structured.
- Diversity（α = .87）
  - 2 The layout is pleasantly varied.
  - 6 The layout is inventive.
  - 10 The design appears uninspired. (r)
  - 14 The layout appears dynamic.
  - 18 The design is uninteresting. (r)
- Colorfulness（α = .89）
  - 3 The color composition is attractive.
  - 7 The colors do not match. (r)
  - 11 The choice of colors is botched. (r)
  - 15 The colors are appealing.
- Craftsmanship（α = .85）
  - 4 The layout appears professionally designed.
  - 8 The layout is not up-to-date. (r)
  - 12 The site is designed with care.
  - 16 The design of the site lacks a concept. (r)
- 因素载荷 .63–.89，无明显交叉载荷；二阶总因子，四个分面载荷相近

**2. 构建与效度** — [Moshagen & Thielsch 2010](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) [一手]；[VisAWI Manual](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf) [一手]
- 7 个研究；研究 4 / 5 = 512 人、42 个德国网站（9 类内容域）
- 定义：「immediate pleasurable subjective experience that is directed toward an object and not mediated by intervening reasoning」（沿用 Reber et al. 2004）
- 收敛：与 AttrakDiff attractiveness .60 ≤ r ≤ .80
- 区分效度只部分成立：与 usability（Flavián）.04 ≤ r ≤ .48、与 pragmatic quality .41 ≤ r ≤ .77
- 与再访意愿 .40 ≤ r ≤ .48
- 人口学影响很小（手册，2,843 人、102 个网站）：与年龄 r = .05–.12；性别 d = 0.06–0.18
- 手册：新网站的临界值 4.5（高于则更可能被正面评价）

**3. VisAWI-S** — [VisAWI Manual Table 5 / §3](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf) [一手]
- 3 个研究、共 1,673 人（Moshagen & Thielsch 2013，BIT 32:1305–1311）
- 4 条目（只测总因子）
  - Everything goes together on this site.（Simplicity）
  - The layout is pleasantly varied.（Diversity）
  - The color composition is attractive.（Colorfulness）
  - The layout appears professionally designed.（Craftsmanship）
- α = .76–.81；与全版 r = .91
- 与 AttrakDiff attractiveness r = .72；与 usability r = .54、pragmatic quality .53、再访意愿 .52
- 手册建议每个网站至少 20 名评价者

**4. 评分者间一致性**
- 没有找到 VisAWI 作者或他人报告的 between-person ICC / rWG
- 可用的最接近数据：研究 5 的网站间 F 值（见 Q2）

### Inferences
- [本文计算] 由 Q2 的单人 ICC 用 Spearman-Brown 推到 20 人均值：总分 ≈ .74、Simplicity ≈ .77、Colorfulness ≈ .64；12 人均值（即原研究）ICC(k) = 1 − 1/F：.52（Colorfulness）–.68（Diversity）。
  - 含义：**单人评分噪声很大，十几到二十人的均值才稳定**——与手册「≥ 20 人」的建议吻合
- [本文计算] Tuch 2012 的 VC / PT ICC 若是平均测量（每组约 267 / 9 ≈ 30 人，最少 14 人），反推单人 ICC ≈ VC .13–.25、PT .11–.20；若是单人 ICC，则非常高。原文没说明，**只能给区间**。
- [推断] VisAWI 18 条目可以直接当 rubric 的骨架：
  - 每条都是一句**可二元判断**的陈述（「颜色不搭」「布局太密」「缺乏统一概念」）
  - 反向条目天然就是「缺陷检测」（dense / patchy / do not match / botched / not up-to-date / lacks a concept）
  - 依据 Q2 换算，Colorfulness 分面的人际一致性最低 → rubric 里颜色规则应只写「明显冲突」类负向闸

### Gaps
- Moshagen & Thielsch 2013 原文（VisAWI-S）本轮未读到，数字来自作者手册。
- Hirschfeld & Thielsch 2015（Ergonomics 58:310–320，cut points）具体阈值未取到。
- 没有 VisAWI 在 AI 生成网页 / 截图上的使用数据。

---

## Q4. 机制：共享核心由什么解释？

### Takeaway
- 共享的部分主要能用**处理流畅性（processing fluency）**统一解释：对比、对称、图形好形（Gestalt）、重复 / 熟悉、原型性都让加工更容易，加工容易 → 正向情感。网页上它表现为「低视觉复杂度 + 高原型性」。
- 共享并不等于「有一条普适曲线」：Berlyne 的复杂度倒 U 在个体层面分解成两类相反偏好的人；颜色偏好的均值能被生态价值解释（r = .893），但群体间差异显著。
- 专家与新手的差异也能用流畅性解释：训练让复杂刺激变得流畅，且专家会套用「品味规范」压低简单刺激。

### Cited Findings

**1. Processing fluency（Reber, Schwarz & Winkielman 2004, PSPR 8:364–382）** — [作者 PDF](https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf) [一手]
- 核心命题（摘要原文）：「The more fluently perceivers can process an object, the more positive their aesthetic response.」
- 被归因到流畅性的变量：figural goodness、figure–ground contrast、stimulus repetition、symmetry、prototypicality；visual / semantic priming 也会提高审美评价
- 立场：美「grounded in the processing experiences of the perceiver, which are in part a function of stimulus properties」——介于客观论与主观论之间
- 关于专家（§Experts and Novices）
  - 无艺术训练者偏好简单、对称；有训练者偏好复杂、不对称（McWhinnie 1968）
  - 音乐新手偏好原型和弦进行，专家没有这个偏好（Smith & Melara 1990）
  - 两个解释：(a) 训练提高了复杂刺激的流畅性；(b) 专家更会考虑「good / bad taste 的规范」，所以即使简单刺激加工愉快也会给低分
- VisAWI 直接采用了这一定义 — [VisAWI Manual](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf) [一手]
- 网页上的证据
  - Thielsch & Hirschfeld 2012 明确把「50 ms 只有低频起作用」与流畅性 / 视觉通路联系；并写「As all humans use the same visual system, there may be a set of fundamental relationships that are true in any population」 — [Thielsch & Hirschfeld 2012](https://uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/thielsch_hirschfeld_2012.pdf) [一手]
  - Tuch 2012：低 VC + 高 PT 最美（数字见 Q1） — [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [一手]

**2. Berlyne 复杂度倒 U 及其批评**
- Güçlütürk, Jacobs & van Lier 2016（Front. Hum. Neurosci.） — [Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00112/full) [一手]
  - 30 人、144 张灰度统计几何图；复杂度 = 主观评分 + PNG 压缩大小（与 zip 大小 r = 0.999）
  - k-means 最优 k = 2
    - 簇 1：20 人，喜好–复杂度 r = −.789（PNG 法 −.849）→ 越简单越喜欢
    - 簇 2：10 人，r = +.874（PNG 法 +.842）→ 越复杂越喜欢
  - 模型比较：二次（倒 U）AIC 1923.5 vs 分簇模型 AIC 1708；模拟 LRT = 217.49, p < .001
  - 原话：跨被试平均「gives an impression of high agreement between individuals」；倒 U「can in fact be an artifact」
- 网页上的倒 U：Reinecke & Gajos 2014 每个国家都呈 U 形关系，但峰值位置不同（见 Q7） — [Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) [一手]
- Tuch 2012：高 PT 下复杂度越低越美（近似单调）；低 PT 下高 VC 反而略好于中 VC（d = .34） — [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [一手]

**3. 原型性 + 新颖性（MAYA）**
- Hekkert, Snelders & van Wieringen 2003（BJP 94:111–124）：偏好来自 typicality 与 novelty 的最优组合；研究 2 中观察者的专业程度不改变两者的相对贡献 — [VU 研究门户](https://research.vu.nl/en/publications/most-advanced-yet-acceptable-typicality-and-novelty-as-joint-pred/) [二手：摘要级]
  - typicality + novelty 共解释偏好的 56%；两者强负相关 — [Jim Davies 摘要](https://www.jimdavies.org/summaries/HekkertSneldersVanwieringen2003.html) [未核实：第三方摘要]

**4. 颜色：生态价值理论（Palmer & Schloss 2010, PNAS 107:8877–8882）** — [PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC2889342/) [一手]
- 48 人评 32 种颜色（Berkeley Color Project）；另有 74 人做颜色-物体联想、98 人评物体好恶、31 人做匹配
- WAVE 与平均偏好 **r = +0.893（约 80% 方差）**，无自由参数
- 竞争模型：cone-contrast 37%；color-appearance 60%（multiple r = .774）；Ou 等 color-emotion 55%
- 群体差异（初步）
  - 按偏好相似度聚成两组（17 人 / 12 人）：本组 WAVE 预测本组 r = .77 / .83，跨组只有 .47 / .64
  - 美国 WAVE 预测美国 r = .89、日本 r = .74；日本 WAVE 预测日本 r = .66、美国 r = .55
  - Berkeley / Stanford 学生对本校颜色的偏好随「school spirit」变化
- 前序已有：Taylor & Franklin 2012 复测只有 61%；Ou & Luo 2006 双色和谐模型；Ou 2012 跨 8 国 like / dislike 存在文化差异

**5. Leder et al. 2004 审美体验模型（BJP 95:489–508）**
- 五阶段：Perceptual Analysis → Implicit Memory Integration（前两步自动、内隐）→ Explicit Classification → Cognitive Mastering → Evaluation（后三步有意识） — [Vienna 实验室页](https://aesthetics.univie.ac.at/research/models-of-aesthetic-appreciation) [二手]；[PubMed 摘要](https://pubmed.ncbi.nlm.nih.gov/15527534/) [二手：摘要措辞与实验室页略有不同]
- 两种输出：aesthetic emotion 与 aesthetic judgment 分开
- cognitive mastering 与 evaluation 构成反馈环 — [Frontiers 2015 转述](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2015.00600/pdf) [二手]

**6. 「为什么自然领域共享更多」的解释**
- Vessel et al. 2018（Cognition 179:121–131）：自然领域（面孔、风景）的行为相关性导致「information processing, and hence aesthetic experience, that is highly conserved across individuals」；人造文化产物没有这种统一相关性 — [检索摘要 / 论文 highlights](https://katalog.lib.cas.cz/KNAV/EdsRecord/edselp,S0010027718301616) [二手]

### Inferences
- [推断] **每条 rubric 规则的「机制理由」对照表**（只列有本轮证据支撑的）：

  | rubric 规则 | 机制 | 证据 |
  |---|---|---|
  | 降低杂乱 / 信息密度适中 | 复杂度最早被加工（17 ms）；流畅性 | Tuch η²p .38 @17 ms；Reinecke F = 23.96 |
  | 遵循品类惯例（导航位置、页面骨架） | 原型性 → 流畅性 | Tuch PT η²p .812；Reber 2004 |
  | 全局布局清晰、分组明确（Gestalt 接近 / 相似） | figural goodness → 流畅性；低频布局主导首印象 | Reber 2004；Thielsch LF r = .32 @50 ms |
  | 足够的图底 / 文字对比 | figure–ground contrast → 流畅性 | Reber 2004 |
  | 对齐、对称、一致的重复 | symmetry / repetition → 流畅性 | Reber 2004；Lavie classical 条目 |
  | 「整体是一个概念」「看得出用心」 | Craftsmanship 分面 | VisAWI 条目 4/8/12/16 |
  | 配色避免明显冲突（而非追求某种「好看」配色） | 均值由生态价值解释，但群体差异大 | Palmer & Schloss r .893 vs 跨组 .47 |
  | 原型之上加少量新意 | MAYA | Hekkert 2003 |

- [推断] 流畅性理论自带一条**风险**：它预测「越典型越美」。对代码生成网页，这意味着以「共享审美」训练的 reward 会推向原型 / 模板（前序笔记的「模板塌缩」）。MAYA 和 Reber 对专家的论述是唯一给「新意」留位置的理论依据。
- [推断] Leder 模型给 rubric 分层一个理论框架：早期阶段（知觉分析、内隐记忆）≈ 跨人共享、可程序化检查；后期阶段（显式分类、认知掌握）依赖知识和风格，正是专家与新手、人与人分歧的来源。这一映射是笔者推理，Leder 2004 原文本轮未读。

### Gaps
- Leder 2004、Berlyne 1971 原文未读；Ou & Luo 2006 的模型拟合数字未取（前序笔记只有定性）。
- 网页 / UI 领域专门检验 Gestalt 原则（对齐、接近）与审美关系、并报效应量的研究本轮未检索到（Bauerly & Liu 2006 只被 Thielsch 提及）。
- 流畅性在网页上的**直接**操纵实验（如 priming 提高网页审美评分）未找到。

---

## Q5. 共享 vs 私人口味：一般领域与设计产物；「找缺陷」vs「偏好风格」

### Takeaway
- 一般领域（前序已有）：私人口味占比 面孔约 40–50%、抽象艺术约 75%；日常场景 taste typicality ≈ .66。**本轮新增**：风景视频的可重复方差里只有 12% 是共享的、88% 是个人的。
- 设计产物落在「低共享」一端：职业设计师对 AI 生成 UI 的二元偏好只有 62.4% 一致（κ = .248）；UIClip 的 α = .37 只基于 10 对。
- **一致性随差异的「明显程度」上升**：DesignPref 里表单类屏幕一致率 72%、登录 / 媒体播放器等 54–57%；一致率与「强偏好」选项占比 r = .774。设计师在「整洁布局、可读性、主操作」上收敛，在「信息密度、风格调性、装饰 vs 功能」上分歧。

### Cited Findings

**1. 一般领域的新数字**
- Isik & Vessel 2021（Front. Hum. Neurosci.） — [Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.676032/full) [一手]
  - 风景视频（N = 24）：整体评分 MM1 = .40（95% CI .31–.48）；连续评分 MM1c = .61（.52–.69）
  - 用重复播放的视频拆分可重复方差：**共享 12%、个人 88%**
  - 引 Vessel 2018 风景静图 MM1 = .60（.53–.66）
- Vessel et al. 2018：面孔共享最高、风景次之，建筑和艺术品「very little shared taste」；各领域重测信度相近，所以差异不是噪声 — [MPG 新闻稿](https://www.aesthetics.mpg.de/en/newsroom/news/news-article/article/beautiful-nature-controversial-art.html) [二手]
- 前序已有（不重复数字）：Hönekopp 2006、Leder 2016、Chen 2022、Bignardi 2024、Graham et al. CCN 2024

**2. 网页上的直接表述**
- Reinecke & Gajos 2014 结论原话：「appeal is largely subjective even after a short exposure time of 500ms」，并称这挑战了「individual variability in aesthetic taste is small during the initial visceral reaction」的旧假设 — [Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) [一手]
- 与之对照：VisAWI 手册在 2,843 人上发现年龄、性别效应可忽略（r ≤ .12，d ≤ .18） — [VisAWI Manual](http://www.thielsch.org/download/VisAWI/VisAWI_Manual_EN.pdf) [一手]
  - 两者不矛盾：Reinecke 的人口学效应显著但 marginal R² 只有 .07（见 Q1）

**3. 设计产物的一致性**
- DesignPref（arXiv 2511.20513） — [DesignPref HTML](https://arxiv.org/html/2511.20513v1) [一手]
  - 20 名职业设计师 × 600 对 = 12,000 次判断；UI 由 GPT-5 / Gemini-2.5-Pro 按 100 个屏幕描述生成，每描述 4 个变体、6 个组内对
  - 一致性：二元方向 平均两两一致 .624、Cohen κ .248、Krippendorff α .248；四档强度 一致 .386、κ .114、α .104
  - 28.5% 的对子两两分歧率 ≥ 96%
  - 标签使用：75.5% 选「中间档」（A > B / B > A）；个人差异极大（中间档占比 6.0%–99.5%）
  - **按屏幕类型**：Form 72.11%（强偏好占比也最高 32.71%）；List / Dialer / Search 约 66–68%；Terms / Camera / Media Player / Login 约 54–57%
  - **一致率与强偏好占比在 20 类屏幕间 r = 0.774**
  - 理由分析（13 名设计师、106 个有争议对、1,378 条理由）
    - 收敛主题（按频次）：clean layout and readability；primary actions and controls；perceived modernity and polish；color, contrast, theme；information architecture and scannability；icon clarity and affordance
    - 分歧主题：information density；visual style and tone；decorative imagery vs focused utility；how strongly actions / task scope are foregrounded
  - 模型（测试集，20 人宏平均二元准确率）：GPT-5 zero-shot 57.70%；UIClip 预训练 55.07%；个性化 UIClip 60.16%（最好）；Gemini-2.5-Pro zero-shot 53.65%
- UIClip：约 1,200 次评分保留 892 对；**每名被试都评同样 10 对**，Krippendorff α = 0.37 — [UIClip](https://arxiv.org/pdf/2404.12500) [二手：经检索摘要]
- UICrit（7 名设计师、983 个 UI、3,059 条批评） — [UICrit](https://arxiv.org/html/2407.08850v3) [一手]
  - **数据采集每个 UI 只有 1 名设计师**，论文没有报告设计师之间的评分一致性
  - 只报告了下游评估的一致性：LLM 评论质量 Fleiss κ = .30 / .31；6 名专家评批评质量 κ = .29；排序 .55
  - 作者原话：「design evaluation is inherently subjective, leading to disagreement regarding design issues present in the UI」

**4. 「找缺陷」vs「偏好风格」的其他证据**
- Bölte et al. 2017（PeerJ，EEG）：作者文字称专家与外行对「不美」网页判断一致、在「美」网页上专家更常判为不美 — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5463973/) [一手]（细节见 Q6，表格与文字有出入）
- Tractinsky 2004：越极端的评分越快（F(4, 1995) = 10.8） — [workshop 版](http://www.ise.bgu.ac.il/faculty/noam/papers/04_ntacmk_final.pdf) [一手]；但效应量只有 η²p .02–.04 — [Tuch et al. 2012](https://research.google.com/pubs/archive/38315.pdf) [一手]
- VisAWI 反向条目全是缺陷式表述（dense, patchy, do not match, botched, not up-to-date, lacks a concept） — [Moshagen & Thielsch 2010](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf) [一手]
- 前序已有：PARA 高分区间方差更低；Haraguchi 2024 扰动越大 GPT-4o 与人相关越高；TASTE Color Harmony τ 最低（.103）

### Inferences
- [推断] blog 可以用一句话概括这条证据链：**人在「哪里坏了」上的一致远高于在「哪个更好」上的一致**。
  - 证据：DesignPref 屏幕类型的一致率与「强偏好」占比 r = .774（差异越明显越一致）；收敛主题全是可用性 / 清晰度类，分歧主题全是风格类
  - 局限：DesignPref 没有直接按「缺陷 vs 风格」给一致率，这是由屏幕类型和理由主题推出的
- [推断] **颜色是最主观的维度**，三条独立证据同向：
  - VisAWI Colorfulness 单人 ICC ≈ .08（四个分面最低，本文计算）
  - TASTE Color Harmony τ = .103（最低，前序已有）
  - Palmer & Schloss 跨组 WAVE 预测从 .77–.83 降到 .47–.64
- [推断] 天花板的量级（供 blog 用）：
  - 设计产物上，judge 与单个设计师的二元一致率很难超过 ~62%（DesignPref 人-人水平）
  - 若目标是「群体均值」，需要 ≥ 12–20 名评价者的均值才稳定（VisAWI 换算 ICC(k) ≈ .52–.77）
- [冲突] 前序笔记写「UICrit ICC ≈ 0.02」，本轮读 UICrit 全文**没找到设计师间 ICC**（每个 UI 只有 1 名设计师）。该数字可能来自其他论文的转述，引用前需溯源。

### Gaps
- Vessel 2018 面孔 / 建筑 / 艺术品的 MM1 精确值：原文付费墙，仍**未核实**。
- 没有找到把评测对子按「有无明显缺陷」分层、分别报人-人一致率的 UI 研究（这是论点「找缺陷更一致」最需要的直接数字）。
- UIClip α = .37 的原文段落本轮未直接读到。

---

## Q6. 专家效应：设计师之间更一致吗？专家与外行有系统差异吗？

### Takeaway
- **「专家更一致」没有在界面审美上得到证明**：DesignPref 的 20 名职业设计师之间 κ 只有 .248；Tanner & Landay 报告新手区分网站审美质量「几乎与专家一样准」。
- **系统差异是有的，但证据多来自艺术 / 建筑**：受训者偏好更复杂、不对称、新颖的刺激；建筑师与外行看同一栋楼的结论基本不相关，且建筑师预测不准外行。
- 网页上唯一的直接 EEG 研究（10 vs 10）：专家更「严格」，但没有专家 × 审美的交互。

### Cited Findings

**1. 网页 / UI**
- Bölte, Hösker, Hirschfeld & Thielsch 2017（PeerJ） — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5463973/) [一手]
  - 10 名专家（设计 / 平面 / 数字媒体从业或学生，平均 10.8 年经验）vs 10 名学历匹配的外行
  - 150 张截图（75 美 / 75 不美，由另外 136 人预评）
  - 网页审美 OR = 12.94（p < .001）；组 × 网页审美 OR = 1.88（p < .01）；组主效应不显著（OR = .97）
  - 作者文字：两组对不美网页判断相似，专家更常把美网页判为不美
  - [未核实] 抓取到的 Table 1 计数方向与文字相反（看起来两组在「美」网页上几乎相同、在「不美」网页上不同），可能是列标签解析错误，引用前需看原表
  - ERP：150–370 ms、370–600 ms 窗口有组效应（专家更负），但任何时间窗都没有组 × 审美交互
- Tanner & Landay 2019（Design Thinking Research, Springer）：53 名新手设计师 vs 52 名专家设计师在线评网站审美；「novices are almost as accurate as experts when discerning between the aesthetic qualities of two websites」，评分者间「high degree of agreement」 — [Springer 章节镜像](https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/978-3-319-97082-0_13)；[RePEc 记录](https://ideas.repec.org/h/spr/undchp/978-3-319-97082-0_13.html) [未核实：只见检索摘要，未读到数字]
- DesignPref：职业设计师之间二元 κ = .248（见 Q5） — [DesignPref](https://arxiv.org/html/2511.20513v1) [一手]
- 前序已有：UNIAA 资深 87.39% vs 初级 79.01%（照片审美感知选择题，不是偏好）

**2. 艺术 / 音乐 / 建筑**
- Reber 2004 综述：无训练者偏好简单、对称；受训者偏好复杂、不对称；音乐新手偏好原型和弦进行而专家不 — [Reber et al. 2004](https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf) [一手：综述引用 McWhinnie 1968、Smith & Melara 1990]
- Silvia 2006：艺术专家觉得艺术（尤其复杂 / 抽象作品）更有趣、更好懂，但情绪评估相近 — [PMC 2016 转述](https://pmc.ncbi.nlm.nih.gov/articles/PMC4876367) [二手]
- Hekkert 2003：专业程度不改变 typicality 与 novelty 的相对权重 — [VU 门户](https://research.vu.nl/en/publications/most-advanced-yet-acceptable-typicality-and-novelty-as-joint-pred/) [二手]
- Gifford et al. 2000（Environment & Behavior）：42 栋现代办公楼、59 个客观特征，建筑师与外行用不同特征做判断，结论差异大 — [Notre Dame 研究摘要](https://housingandcommunityregeneration.nd.edu/research/why-architects-and-laypersons-judge-buildings-differently-cognitive-properties-and-physical-bases/) [二手]
- Brown & Gifford 2001：执业建筑师预测外行对大型当代建筑的评价，预测与外行实际评分「poorly correlated」 — [Notre Dame 研究摘要](https://housingandcommunityregeneration.nd.edu/research/architects-predict-lay-evaluations-of-large-contemporary-buildings-whose-conceptual-properties/) [二手]
- 创造力评分（Consensual Assessment Technique）：10 名专家 vs 106 名非专家评 205 首诗，两组评分「quite different」，非专家评分不一致 — [Kaufman et al. 2008 PDF](https://typeset.io/pdf/a-comparison-of-expert-and-nonexpert-raters-using-the-1gh8l5ls8r.pdf) [未核实：检索摘要]

### Inferences
- [推断] 对 blog 有用的结论是「**专家 rubric 有意义，但不是因为专家之间更一致**」。它的价值在于：
  - 专家能把共享的知觉规律（Q4）**说出来、写成条目**，而外行只能凭感觉
  - 专家对「哪里坏了」更敏感（Bölte：专家更严格）
- [推断] 但要警惕**专家偏差**：艺术与建筑的证据都指向「专家偏好更复杂 / 新颖、且预测不准外行」。如果 rubric 由设计师写、目标用户是普通人，应避免把「风格新意」写成硬规则；Gifford 的结果是这一风险最强的证据。
- [推断] 「专家 vs 新手」对 VLM judge 的直接启示：judge 学的是「谁的」审美要说清楚。DesignPref 的个性化模型（60.16%）> 群体模型，说明设计师之间的差异是系统性的而非纯噪声。

### Gaps
- Tanner & Landay 2019 的具体一致率 / 准确率数字未取到。
- 没找到在**网页 / UI** 上同时测「专家组内一致性」与「外行组内一致性」并直接比较的研究。
- Gifford 2000 / Brown & Gifford 2001 的相关系数未取到。

---

## Q7. 跨文化差异：Reinecke & Gajos 2014 及其他

### Takeaway
- 3.2 万人、179 国的数据显示：复杂度 / 色彩度与吸引力的**曲线形状各国相似**（U 形），但**峰值位置**显著不同；地理相邻、文化交流多的国家偏好相近。
- 但这些人口学差异只占评分方差的很小一部分（固定效应 marginal R² = .07），量级上是「同一曲线的平移」，不是「审美标准不同」。

### Cited Findings
- 数据 — [Reinecke & Gajos 2014](https://iis.seas.harvard.edu/papers/reinecke14visual.pdf) [一手]
  - LabintheWild，2012-06 至 2013-08；39,975 名志愿者（54% 女性）、179 国，年龄 12–91
  - 430 张网站截图（350 英文、60 非拉丁文字、20 Webby 提名）；500 ms 呈现，1–9 分；每人评 30 张、两轮
  - 清洗后 1,542,166 次观测（771,083 对、32,222 人）；国家分析用 43 国、18,448 人、441,478 对
  - 模型：lme4 混合模型，网站 ID 与被试 ID 为随机效应；年龄、性别、国家、教育经 AIC 保留
- 总体结果
  - 最受欢迎：**中-高色彩度 + 低-中复杂度**
  - 复杂度是比色彩度更强的预测因子（F(1) = 23.96）
  - 人口学显著改善拟合：χ²(290) = 7408.7, p < .0001
- 国家
  - 复杂度 × 国家：F(32) = 20.50
  - 俄罗斯偏好最低复杂度（峰值 2.5）；塞尔维亚、波黑、墨西哥、智利偏好最高（4.6–4.8）
  - 芬兰、俄罗斯、波兰、丹麦偏好低色彩度（峰值 3.6–4.4）；美国 6.1；智利、马来西亚 6.9；**马其顿 7.6（最高）**
  - 北欧 < 南欧、北欧 < 亚洲（中、新、马）；香港和日本低于其他亚洲国家；英语国家高于北欧
- 年龄
  - 色彩度 × 年龄 F = 198.3；复杂度 × 年龄 F = 1721.1
  - 12–40 岁复杂度峰值 4.1–4.2；41–50 岁 4.5；50 岁以上 4.7（越老越偏好复杂）——与 2013 年「45 岁以上偏好低复杂度」**相反**，作者归因于本次样本更异质、受教育程度更低
- 性别：色彩度 × 性别 F = 658.9，女性更喜欢高饱和
- 教育
  - 色彩度 × 教育 F(7) = 113.04：高中以下峰值 6.9，博士 5.0
  - 复杂度 × 教育 F(7) = 28.80：高中以下 4.7，博士 4.0
- 其他跨文化证据
  - Palmer & Schloss 2010：美国 WAVE 预测日本偏好 r = .74（vs 本国 .89） — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2889342/) [一手：作者标注为初步结果]
  - Tractinsky 1997：日本与以色列的审美-可用性相关强度不同 — [Tractinsky 研究页](https://www.ise.bgu.ac.il/faculty/noam/research/aesthetics.html) [二手]
  - 前序已有：Ou 2012 跨 8 国颜色 like / dislike 有文化差异

### Inferences
- [推断] 对 rubric 的含义：「降低杂乱」「中等以上色彩」这类方向性规则是跨文化成立的（曲线形状一致）；具体「多少算杂乱、多饱和算合适」的阈值是文化 / 人群相关的，**不宜写成固定数值**。
- [推断] 2013 与 2014 在「年龄 × 复杂度」上方向相反，说明这类人口学结论对样本构成很敏感，blog 引用时应只引「峰值会随人群平移」这个稳健结论，不引具体方向。
- [推断] 代码生成网页的 judge 若主要由某一人群（如中国设计师）标注，其色彩度阈值可能系统性偏离其他市场；这是天花板之外的另一种「偏差」。

### Gaps
- 国家峰值的标准误、Cohen's d 完整表在作者资源页（iis.seas.harvard.edu/resources），本轮未取。
- 没有找到 Reinecke 之后用现代网页（2020 年后风格）重复跨国研究的工作。
- 东亚（中国大陆）用户的网页审美偏好专门研究本轮未检索。

