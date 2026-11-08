# VLM 审美 rubric 调研 · Video（电影书 → 可检查 rubric）

> 调研日期 2026-11-02。标注约定：
> - `[新]` = 项目已有笔记 `middle_processing/notes/video.md` 里没有的内容（本文绝大部分是新的）
> - `[已有]` = 已有笔记里出现过，这里只为对照引用
> - `[二手]` = 来源是课程笔记 / 书评 / 目录页，不是书的原文；`[未核实]` = 只见于搜索摘要，没打开原文
> - 已有笔记覆盖的是「代码渲染视频的确定性 verifier」，**完全没有电影书规则和视频审美 benchmark**，所以本文不与之重复。

---

## Q1. 经典电影书具体说了什么？哪些能写成可观察的检查项？

### Takeaway
九本书里能直接变成「看得见、可判是非」的规则集中在三类：**构图**（headroom / look room / rule of thirds，Bowen）、**剪辑连续性**（180° 轴线、30° 规则、eyeline match、match on action，Bowen / Bordwell / Arijon）、**剪辑优先级**（Murch Rule of Six 的六项排序）；Block 的 contrast/affinity 则给出一个可量化的「视觉强度曲线」框架。多数书的原文只能拿到目录和二手摘要，精确措辞和页码要回书核对。

### Cited Findings

- **Walter Murch — In the Blink of an Eye（1995 初版）** `[新]` `[二手]`
  - Rule of Six（理想的切点按权重排序）：
    - Emotion 51% → Story 23% → Rhythm 10% → Eye-trace 7% → 2D plane of screen 5% → 3D space of action 4% — [filmdaft](https://filmdaft.com/?p=33138)；[No Film School](https://nofilmschool.com/editing-emotion-using-walter-murchs-rule-six-non-narrative-content)
  - 取舍规则：一个切点满足不了全部六条时，「从底部往上逐条牺牲」（先丢 3D 空间连续，最后才丢情感）— [filmdaft](https://filmdaft.com/?p=33138)
  - Murch 自己说这些百分比「slightly tongue-in-cheek, but not completely」— 同上（搜索摘要转述）
  - Eye-trace：观众视线在画面中的落点要跨切点衔接 — [Artlist](https://artlist.io/blog/eye-trace-and-rule-of-six-editing/)
  - ⚠️ ScriptReader.ai 上的引文「Emotion is 51% of every editing decision」无法对上原书，不要引用 — [scriptreader](https://scriptreader.ai/guides/blink-of-an-eye-murch)

- **Joseph V. Mascelli — The Five C's of Cinematography（1965；Silman-James 1998 重印）** `[新]` `[二手]`
  - 五章：Camera Angles / Continuity / Cutting / Close-ups / Composition — [Silman-James](https://silmanjamespress.com/the-five-cs-of-cinematography/)
  - Camera Angles 一章的子项：objective / subjective / point-of-view 三种视角；subject size、subject angle、camera height — [Centre County Library 目录](https://search.centrecountylibrary.org/Record/325484/TOC)
  - Continuity 一章的子项：cinematic time & space、filming action、master scenes、**screen direction**、transitional devices — 同上
  - 书评：书中逐例演示 angle / continuity / cutting / close-up / composition 的「对与错」，并与 sight lines 关联 — [animatedspirit 书评](https://animatedspirit.com/2015/09/page/3)

- **Bruce Block — The Visual Story（2001 初版，2020 第 3 版）** `[新]` `[二手]`
  - 七个 basic visual components：space、line、shape、tone、color、movement、rhythm — [O'Reilly Ch.2 预览](https://www.oreilly.com/library/view/the-visual-story/9780240807799/009_9780080551692_chapter2.html)；[Routledge](https://www.routledge.com/The-Visual-Story/Block/p/book/9781138014152)
  - Principle of Contrast & Affinity（第 2 章）：
    - contrast = 差异；任何一个 component 的对比越大 → 视觉强度（intensity）越高；affinity（相似）越大 → 强度越低 — [scriptreader 摘要](https://scriptreader.ai/guides/visual-story-block)
    - 该原则适用于全部七个 component — [O'Reilly Ch.2 预览](https://www.oreilly.com/library/view/the-visual-story/9780240807799/009_9780080551692_chapter2.html)
  - 章节顺序：basic visual components → contrast & affinity → space（两章）→ line & shape → tone → color → movement → rhythm → story & visual structure — 同上

- **Christopher J. Bowen（& Roy Thompson）— Grammar of the Shot** `[新]` `[二手·目录]`
  - 第 2 版目录：Simple Rules for Framing Human Subjects p.24 / **Headroom p.25** / **Look Room p.28** / **Rule of Thirds p.30**；**180° rule p.102**、**30° rule p.106** — [O'Reilly Ch.4e](https://www.oreilly.com/library/view/grammar-of-the/9780240521213/Chapter04e.html)；[O'Reilly Ch.4g](https://www.oreilly.com/library/view/grammar-of-the/9780240521213/Chapter04g.html)
  - 180° 线（又称 imaginary line / action line / axis of action）用于保持镜头间的视线与 screen direction 一致 — [O'Reilly Ch.4e](https://www.oreilly.com/library/view/grammar-of-the/9780240521213/Chapter04e.html)
  - 30° 规则原文预览：在 180° 弧内换角度拍同一主体时，「ideally move the camera at least 30 degrees around the semicircle」— [O'Reilly Ch.4g](https://www.oreilly.com/library/view/grammar-of-the/9780240521213/Chapter04g.html)
  - 30° 的阈值各家不一（有人说 >10°、有人说 ≥25°）；Wikipedia 另记「20 mm 焦距变化」变体 — [Wikipedia: 30-degree rule](https://en.wikipedia.org/wiki/30-degree_rule)

- **Bowen — Grammar of the Edit** `[新]` `[二手·目录]`
  - 第 3 版 Ch.3「When to Cut and Why?」列出好剪辑的六个因素：information、motivation、shot composition、camera angle、continuity、sound — [schweitzer-online 目录](https://www.schweitzer-online.de/buch/Bowen/Grammar-Edit/9780240526003/A1348826)（搜索摘要转述，`[未核实]` 具体出自哪一页目录）
  - 版本：2 版（2009，Thompson & Bowen）→ 3 版（2013）→ 4 版（2018）→ 5 版 — [O'Reilly 2nd ed](https://www.oreilly.com/library/view/grammar-of-the/9780240521206/)
  - 经典剪辑原则：切点应近乎不可见，靠动作跨切点延续（cut on action）— [Jim Stinson, Edit Suite](https://www.personal.kent.edu/~lhanson/grammar.htm)

- **Daniel Arijon — Grammar of the Film Language（1976；Silman-James 1991）** `[新]` `[二手·目录]`
  - 1,500+ 插图的「视觉叙事公式」集 — [Silman-James](https://www.silmanjamespress.com/grammar-of-the-film-language)
  - 目录：Line of interest → Five basic variations of the **triangle principle** → external / internal reverse、parallel camera positions → 三机位 / 四机位方法 — [Scribd 扫描目录](https://www.scribd.com/document/319078206/Grammar-of-the-Film-Language)
  - 被虚拟摄影（virtual cinematography）专利当作「镜头公式 idiom 库」引用，例如 external reverse = 越过 A 的肩拍 B — [US Patent 6040841](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6040841)

- **David Bordwell & Kristin Thompson — Film Art** `[新]` `[二手]`
  - 镜头间四种关系：graphic、rhythmic、spatial、temporal；**graphic 与 rhythmic 存在于一切剪辑**，spatial / temporal 在非叙事抽象片里可以无关 — [P.O.V. No.6](https://pov.imv.au.dk/Issue_06/section_1/artc6A.html)
  - Continuity editing：围绕 axis of action（180° 线）构建空间，机位不越线；eyeline match = 人物看 → 切到其所看之物 — [Emory 课程博客](https://scholarblogs.emory.edu/introtofilm2024/?p=288)；[hackmd 课程笔记](https://hackmd.io/a4erbUZKQ_isoTk4bq0PoQ)
  - Graphic match：两镜头在明暗、线条/形状、体积/纵深、运动/静止上相似 — [hackmd 课程笔记](https://hackmd.io/a4erbUZKQ_isoTk4bq0PoQ)

- **Blain Brown — Cinematography: Theory and Practice（2002 初版；第 3 版 2016）** `[新]` `[二手·目录]`
  - 第 3 版章节（库目录，与另一份目录有出入）：Filmspace / Visual language / Lens language / Camera dynamics / Cinematic continuity / **Exposure** / **Color theory** — [Petra 图书馆](https://dewey.petra.ac.id/view/96554)；另一版目录 — [MPDL](https://ebooks.mpdl.mpg.de/ebooks/Record/EB001913628/TOC)
  - 初版 Filmspace 章覆盖 ISO、inverse square law、Zone System 等曝光内容 — 同上（搜索摘要）

- **Steven Katz — Film Directing Shot by Shot（1991；25 周年版）** `[新]` `[二手]`
  - Part I：Visualization / Production Design / Storyboards；Part IV（moving camera）：The Pan / The Crane Shot / The Tracking Shot / Tracking Shot Choreography / Transitions — [opencourser](https://opencourser.com/book/xtvuus/film-directing-shot-by-shot)
  - 用 **A、I、L 三种调度 pattern** 简化对话场面的机位选择 — [Goodreads](https://www.goodreads.com/book/show/84110)

- **Gustavo Mercado — The Filmmaker's Eye（2010；第 2 版 2022）** `[新]` `[二手·目录]`
  - 约 25 章「一章一种镜头」：ECU / CU / MCU / M / MLS / LS / ELS、OTS、establishing、subjective、two-shot、group、canted、emblematic、abstract、macro、zoom、pan、tilt、dolly、dolly zoom、tracking、Steadicam、crane、sequence shot — [TAMU 目录](https://libcat.library.tamu.edu/Record/in00005747744/TOC)
  - 每章都附「breaking the rule」案例 — [Hunter College](https://fm.hunter.cuny.edu/?p=4324)
  - 第 2 版新增 overhead shot 一章，扩写 aspect ratio、rule of thirds — 同上（搜索摘要）

### Inferences
- **可程序化的书规则**（几何 / 统计可算）：
  - headroom / look room / 三分法 → 主体 bbox 与画框的相对位置
  - 180° / 30° → 相邻镜头的机位位姿差（Blender 里直接读相机 transform）
  - eye-trace → 切点前后显著性质心距离
  - Block contrast/affinity → 逐帧 tone / color / motion 强度曲线
- **只能 VLM 看的书规则**：Murch 的 emotion / story、match cut 是否「有意义」、graphic match 的语义匹配。
- **Murch 排序可直接当 pairwise 的 tie-break 权重**：两段剪辑在低位项（3D 空间）上打平时，看高位项（rhythm、emotion）。
- **对代码渲染短片的迁移性**：
  - 能迁移：构图三条、Block 的强度曲线、rhythm、eye-trace、曝光（Blain Brown）
  - 有条件迁移：180° / 30°（只在多镜头、有主体运动时适用；单镜头 motion graphics 不适用）
  - 基本不迁移：Katz 的对话调度 A/I/L、Mascelli 的 close-up 表演、VADB 的人物妆发表情类
- Bowen 书里所有构图规则都以「人物」为对象；网页动效里的等价物是 **安全区 / 留白 / 文字不贴边**，这是推断，书里没写。

### Gaps
- 九本书都没拿到正文原文：页码只有 Bowen（Grammar of the Shot 2 版）可靠；Murch 的 Rule of Six 所在章节名、Bordwell 的章号均未核实。
- Mascelli 的 Close-ups、Composition 两章没找到具体规则摘要。
- Grammar of the Edit 的六因素来自搜索摘要转述的目录，未打开原页确认。

---

## Q2. 现有视频审美 / 质量 benchmark：维度、方法、与人一致性

### Takeaway
- 「审美」与「技术质量」在人评里高度纠缠（DIVIDE-3k 两者 SROCC 0.8752），但能分开标；
- 帧级审美模型（LAION）与人的视频审美相关只有 ≈0.45，MLLM 判官可达 ≈0.70；
- **VLM 对电影语言的识别仍不可靠**：镜头运动约 50%、构图 55–68%、焦距最低 31.9%。
- 构图对模型最难：VBench-2.0 中 composition 与人相关 0.817，是 18 维里最低；Claude-Sonnet-4.5 的最弱项是构图；CineTechBench 中 GPT-4o 的构图只有 57.5。人标构图一致性 α=0.61，在 VADB 里属中等（最低的是色彩 0.54）。

### Cited Findings

#### A. 视频审美 / 质量数据集（人评） `[新]`

- **DOVER / DIVIDE-3k（ICCV 2023）** — [arXiv 2211.04894](https://arxiv.org/abs/2211.04894)
  - 规模：3,590 个 UGC 视频（YFCC-100M + Kinetics-400），450,000 条人评
  - 协议：in-lab，35 名受训标注员（19 男 16 女）；每组 40 视频、每阶段 9 组；每阶段插 10 个 golden video 抽检，偏差大者淘汰
  - 三种分 + 一种归因：
    - Aesthetic：「based on aesthetic perspective (e.g., semantic preference)」，用 AVA 好/中/差各 20 张图校准
    - Technical：只看失真；**8 类失真**：noise、artifacts、low sharpness、out-of-focus、motion blur、**stall**、**jitter**、**over/under-exposure**
    - Overall：用 LSVQ 好/中/差各 20 视频校准
    - Subjective reasoning：技术因素占总分比例，选项 {0, 0.25, 0.5, 0.75, 1}
  - 关键数字：
    - MOS_A vs MOS_T：SROCC **0.8752**，KROCC 0.7011
    - 对 overall MOS 的 SROCC：MOS_A 0.9350 / MOS_T 0.9642 / A+T 0.9827 / **0.428·A + 0.572·T = 0.9834**
    - 每个视频的技术影响占比区间 **[0.364, 0.698]**
  - 定性结论：审美分与语义、构图相关；技术分与低层纹理、失真相关

- **VADB（NeurIPS 2025）** — [arXiv 2510.25238v2](https://arxiv.org/html/2510.25238v2)；数据 [GitHub BestiVictory/VADB](https://github.com/BestiVictory/VADB)（80% 公开）
  - 规模：10,490 视频，37 名专业标注员，每视频 ≥13 人；7 或 11 个分、平均 22 条评语、7 个客观 tag
  - 维度：overall（1–10）+ 10 个 attribute
    - General 6：Composition（元素和谐、主体突出）/ Shot Size（景别是否适合内容）/ Lighting（突出主体、无过曝欠曝）/ Visual Tone（明暗与色温是否贴合情绪）/ Color（自然或风格化，无干扰性失真）/ Depth of Field（背景虚化是否适合主体）
    - Character 4：Expression / Movement / Costume / Makeup
  - 客观 tag：34 个，来自 camera movement、composition、lighting 三类
  - 标注一致性（Krippendorff α，ordinal）：Overall 0.59；Com 0.61；SS 0.61；Lig 0.57；V&T 0.57；D&F 0.55；**Col 0.54（最低）**；Exp 0.66（最高）
  - 模型：VADB-Net SRCC 0.93 / PLCC 0.93；FastVQA 0.92 / 0.93；未测 MLLM

- **T2VQA-DB** — [arXiv 2403.11956](https://arxiv.org/html/2403.11956)
  - 10,000 视频、9 个 T2V 模型、1,000 prompt；27 名受试者，0–100 滑条同时考虑文本对齐与保真度，Z-score 化
  - SRCC：CLIPSim **0.1047** / FAST-VQA 0.7173 / DOVER 0.7609 / T2VQA 0.7965

#### B. 生成视频评测套件（含自动指标与人评对齐） `[新]`（`[已有]` 仅提到 VBench 名字）

- **VBench（CVPR 2024）** — [arXiv 2311.17982](https://arxiv.org/html/2311.17982)
  - 16 维 = Video Quality 7（Subject Consistency、Background Consistency、Temporal Flickering、Motion Smoothness、Dynamic Degree、Aesthetic Quality、Imaging Quality）+ Video-Condition Consistency 9
  - 计算方法（都可直接复用为程序检查）：
    - Subject Consistency：DINO 特征，每帧与首帧、前一帧余弦相似度取均值
    - Background Consistency：同上，换 CLIP 特征
    - **Temporal Flickering**：相邻帧 MAE 均值，归一化 (255 − S)/255；只用静态场景 prompt，并用 RAFT 剔除有明显运动的视频
    - **Motion Smoothness**：丢掉奇数帧，用 AMT 插帧重建，与原帧算 MAE
    - **Dynamic Degree**：RAFT 光流，取最大 5% 光流均值判静/动，得分 = 非静态视频比例
    - **Aesthetic Quality**：LAION aesthetic predictor 逐帧 0–10 → 归一化均值（**纯帧级，无时间维**）
    - **Imaging Quality**：MUSIQ（SPAQ 训练）逐帧 /100 均值
  - 人评协议：每 prompt 4 模型一组，抽 5 组，每组 6 对 pairwise；左右随机；**只判当前维度**；维度专属培训 + 预标注 + 两轮复检；胜=1、负=0、平=0.5 算 win ratio
  - 与人对齐：逐维 Spearman ρ（win ratio）只画在 Fig.5，正文无数值
- **VBench++** — [arXiv 2411.13503](https://arxiv.org/html/2411.13503)
  - 新增 I2V 与 trustworthiness（Culture Fairness、Gender Bias、Skin Tone Bias、Safety）；ρ 同样只在图里
- **VBench-2.0** — [arXiv 2503.21755v2](https://arxiv.org/html/2503.21755v2)
  - 5 大类 18 维：Human Fidelity（Anatomy / Clothes / Identity）、Creativity（Diversity / **Composition**）、Controllability（含 **Camera Motion** 等 7 项）、Physics（Mechanics / Thermotics / Material / Multi-View Consistency）、Commonsense（Motion Rationality / Instance Preservation）
  - 评测器：SOTA VLM/LLM（generalist）+ 异常检测等 specialist
  - 与人 Spearman（4 个模型的 win ratio）：**Composition 81.70%（18 维最低）**、Motion Rationality 87.97%、Camera Motion 97.95%、Human Identity 99.46%
- **Video-Bench（MLLM 判官）** — [arXiv 2504.04907](https://arxiv.org/html/2504.04907v1)
  - 方法：chain-of-query（MLLM 先描述 → LLM 出问题集 → MLLM 带反思作答 → 打分）+ few-shot scoring（同 prompt 多视频互为参照）
  - 与人 Spearman（Video-Bench vs 传统指标）：
    - Aesthetic：**0.702** vs LAION **0.446**
    - Imaging：0.733 vs MUSIQ 0.363
    - Temporal：0.402 vs CLIP 0.260
    - Motion：0.514 vs RAFT / AMT 0.329
  - 原文：「textual guidelines alone are insufficient」，需要多模态参照
- **EvalCrafter** — [arXiv 2310.11440](https://arxiv.org/abs/2310.11440)
  - 700 prompt、17 个客观指标、4 方面（visual / content / motion quality、text-video alignment）；用人评拟合线性系数组合指标；摘要无相关数值
- **FETV** — [arXiv 2311.01813](https://arxiv.org/abs/2311.01813)
  - prompt 按 major content / attribute control / prompt complexity 三正交维分类；结论：**CLIPScore、FVD 与人评相关很差**
- **VideoPhy** — [arXiv 2406.03520](https://arxiv.org/abs/2406.03520)
  - 判「语义贴合 + 物理常识」；最好的 CogVideoX-5B 只有 **39.6%** 同时满足两者

#### C. 学出来的视频判官（reward / scorer） `[新]`

- **VideoScore** — [arXiv 2406.15252](https://arxiv.org/html/2406.15252)
  - VideoFeedback：37.6K 视频、11 模型；5 维：Visual Quality / Temporal Consistency / Dynamic Degree / Text-to-Video Alignment / Factual Consistency；1–3 分（后补 4）
  - 人人一致性（Trial 2，n=100）Fleiss κ：VQ **0.088** / TC 0.562 / DD 0.565 / TVA 0.125 / FC **−0.089**
  - 与人 Spearman（avg）：VideoScore **77.1** / GPT-4o **23.0** / Gemini-1.5-Pro **16.9** / CLIP-sim 8.9 / DINO-sim 7.5
- **VideoScore2** — [arXiv 2509.22799](https://arxiv.org/abs/2509.22799)
  - VideoFeedback2：27,168 人标视频，3 维（visual quality、text alignment、physical/common-sense）+ CoT 理由；SFT → GRPO
  - VideoScore-Bench-v2 准确率 44.35（+5.94）；4 个 OOD benchmark 平均 50.37（+4.32）

#### D. VLM 的电影语言识别能力 `[新]`

- **ShotBench / ShotVL（2025）** — [arXiv 2506.21356](https://arxiv.org/html/2506.21356)
  - 3.5k+ 专家标注 QA（图 + 视频），8 维，测 24 个 VLM；ShotQA 约 70k QA；ShotVL = SFT + GRPO
  - 准确率（%）：

    | 维度 | GPT-4o | Qwen2.5-VL-72B | ShotVL-3B |
    |---|---|---|---|
    | Shot Size | 69.3 | 75.1 | 77.9 |
    | Shot Framing | 83.1 | 82.9 | 85.6 |
    | Camera Angle | 58.2 | 56.7 | 68.8 |
    | Lens Size | 48.9 | 46.8 | 59.3 |
    | Lighting Type | 63.2 | 59.0 | 65.7 |
    | Lighting Condition | 48.0 | 49.4 | 53.1 |
    | Composition | 55.2 | 54.1 | 57.4 |
    | Camera Movement | 48.3 | 48.9 | 51.7 |
    | **Average** | **59.3** | **59.1** | **65.1** |

  - Gemini-2.0-flash 的 Lens Size 只有 **31.9**；论文称 camera movement 是「全体模型的突出弱项」
- **CineTechBench（2025）** — [arXiv 2505.15145](https://arxiv.org/html/2505.15145)
  - 600+ 电影图像 + 120 片段，7 维；测 15+ MLLM、5+ 视频生成模型
  - 静帧：GPT-4o overall 70.16（Scale 75.00 / Angle 82.50 / **Composition 57.50** / Color 93.33 / Lighting 71.82 / **Focal Length 33.33**）；Gemini-2.5-Pro 69.67（Composition 67.50）
  - 镜头运动：Gemini-2.5-Pro overall **56.69**（Rotation 45.16、Zoom **14.29**）；GPT-4o 50.00（Rotation **25.81**）；**Rotation 是三家共同最弱**
- **CameraBench（2025）** — [arXiv 2504.15376](https://arxiv.org/html/2504.15376)
  - ~3,000 视频，与摄影师共建的运动原语 taxonomy：
    - translation：dolly / pedestal / truck
    - rotation：pan / tilt / roll
    - intrinsic：zoom
    - object-centric：arc、lead / tail / side / aerial tracking
    - 另有 steadiness 五档（static → very unsteady）、speed、dolly-zoom、motion-blur
  - 人：专家比非专家准确率高 **>15%**；训练可提升 10–15%（正文）或 15–20%（附录，两处不一致）
  - 机器（二分类 AP，8 FPS）：MegaSAM **50.2**；Qwen-2.5-7B Full SFT **59.3**；LoRA 56.7
  - SfM 弱在依赖语义的原语（如 tracking），VLM 弱在几何原语（精确轨迹）
- **VideoAesBench（2026-01）** — [arXiv 2601.21915](https://arxiv.org/html/2601.21915)
  - 1,804 QA / 1,641 视频，12 维：Visual Form（composition、elements & structure、shot size、depth of field、visual subject）/ Visual Style（lighting、color、visual tone、creativity）/ Visual Affectiveness（emotion、theme & communication、viewer interest）；测 23 个 LMM
  - Overall：**Claude-Sonnet-4.5 67.88%**、Qwen3-VL-32B 66.69%、随机 33.59%
  - Claude 最强 color 77.21%、**最弱 visual composition 63.98%**；Qwen3-VL 最弱 viewer interest 58.93%
  - 按题型（Claude）：单选 73.33 / 多选 64.91 / 判断 68.83 / 开放 **58.43**

#### E. 与已有笔记的对照 `[已有]`
- ManimAgent 的 VLM 判官与人评相关 **−0.17**；SimWorlds vs VIGA 的 VLM 分只差 0.04（MPR 差 0.20）；Blender 关键帧删光的变异 VLM **0/8** 全漏 — 本地 `middle_processing/notes/video.md` §1.3 / §4.2 / §4.4

### Inferences
- **人类审美分本身被技术质量污染**：DIVIDE-3k 中 A 与 T 的 SROCC 0.8752，最优融合权重技术 0.572 > 审美 0.428。rubric 应先设「技术底线」门控，再单独评审美，否则 VLM 的审美分会被模糊 / 闪烁拖着走。
- **绝对分不可靠，pairwise 更稳**：VideoFeedback 的 VQ κ 只有 0.088、FC 为负；VBench、VBench-2.0、VideoArgus（见 Q3）都用 pairwise / 组内排序对齐人评。
- **别让 VLM 判镜头运动和焦距**：最好的模型约 50–57%（ShotBench / CineTechBench），旋转、变焦最差。代码渲染场景里这些是**已知量**（Blender 相机 F-curve、CSS transform），应直接读代码。
- **帧级审美模型不够**：LAION 与人视频审美 ρ 0.446，且 VBench 的 Aesthetic Quality 没有时间维；节奏 / 剪辑类审美必须让 VLM 看多帧或接程序信号。
- **数据域不匹配**：所有 benchmark 都是实拍 UGC、电影或扩散生成视频，**没有一个面向网页 / Blender 渲染的短片**。人物类属性（VADB 的 Character 4 项）和 DOVER 的 noise / out-of-focus 对 motion graphics 基本不适用；但 stall、jitter、曝光、aliasing 照样适用。

### Gaps
- VBench / VBench++ 逐维人评 ρ 只在图里，正文无数值。
- CameraBench 主表（GPT-4o / Gemini 零样本 AP）没取到，只有 SFT 消融表。
- EvalCrafter、FETV 的具体人评相关数值没取到（只读了摘要）。
- 没有找到任何面向「代码渲染视频（web / Blender）」的审美人评数据集。
- TransNetV2 等镜头切分工具的 F1 没取到（摘要无数字）。

---

## Q3. 给 VLM 显式的电影 rubric / checklist，能否提高与人一致性？

### Takeaway
有正面证据，但**没有严格对照**：同一判官「直接打分 vs rubric」的对比只有 MSAVBench 一组（叙事连贯 ρ 0.600 → 0.850）；工具取证（tool-grounded）带来的提升更大（+0.34~0.38）；VisionReward 显示二值问题越多、偏好预测越准。反面证据是：VLM 本身识别电影语言约 50–65%，rubric 里凡是「识别类」条目都会继承这个误差。

### Cited Findings
- **MSAVBench（2026，多镜头音视频生成）Table 6，同判官 Qwen3.5** `[新]` — [arXiv 2605.20183](https://arxiv.org/html/2605.20183)
  - Narrative Coherence：直接打分 **0.600** → instance-wise rubric **0.850**（换成 Qwen2.5-VL-32B 仍有 0.820）
  - Cross-Shot Layout Consistency：直接打分 0.429 → tool-grounded 0.767
  - Intra-Shot Text-Layout Alignment：0.405 → 0.786
  - 整体 benchmark 与人 ρ = 0.915
  - 镜头级指标含 camera parameter adherence（shot scale / angle / movement）、跨镜头 visual consistency（主体、背景、风格、光照、色彩）
- **VideoArgus（2026）** `[新]` — [arXiv 2608.05485](https://arxiv.org/html/2608.05485v1)
  - 每个输入先生成「output-blind、sample-specific」rubric（criteria、scoring rules、failure modes、evidence plans），再逐条 VLM QA + 视觉工具；rubric 生成器 Claude Opus 4.8，判官 Qwen3.6-27B
  - 组内排序 Spearman（vs 原 benchmark 评测器）：
    - T2V（VBench）：0.162 → 0.436（仅 VLM）→ **0.496**（+工具）
    - TI2V（VBench-I2V）：**−0.060** → 0.590 → 0.605
    - TSV2V（EditVerseBench）：0.686 → 0.715 → 0.749
  - ⚠️ 没有「去掉 rubric、同一 VLM 直接打分」的消融，提升不能全部归因于 rubric
- **VisionReward** `[新]` — [arXiv 2412.21059](https://arxiv.org/html/2412.21059v4)
  - 视频：9 维 / 20 子维 / **64 个二值问题**（Alignment 4、Composition 2、Quality 14、Fidelity 9、Safety & Emotion 4、Stability 12、Dynamic 8、Physics 4、Preservation 7）
  - 每个 yes/no 当特征，用 1,795 对视频做 logistic regression 学权重
  - 偏好预测准确率比 VideoScore 高 **17.2%**；用它做 reward 的 T2V pairwise 胜率高 31.6%
  - Fig.5：准确率随二值问题数增加而上升
- **Video-Bench 消融** `[新]` — [arXiv 2504.04907](https://arxiv.org/html/2504.04907v1)
  - chain-of-query（先拆成问题再答）：对齐类均值 0.671 → 0.734
  - few-shot 参照：均值 0.639 → 0.733（⚠️ 原表列对齐疑似错位）
- **RULER-Bench** `[新]` `[未核实]` — [arXiv 2512.02622](https://arxiv.org/pdf/2512.02622)
  - 搜索摘要称：逐条 checklist + GPT-o3 打分，与人一致约 85%
- **反面：VLM 判官本身的可靠性** `[新]` — [arXiv 2503.05977（ICLR 2025）](https://arxiv.org/abs/2503.05977v1)
  - 把强弱 VLM 判官混合投票不能稳定提升，弱判官引入噪声；微调 Video-LLaVA 提升理解力也不能让它成为可靠判官
- **反面（项目本地）** `[已有]`：ManimAgent VLM 判官 −0.17；VLM 对动画缺失 0/8 — 本地 `notes/video.md`

### Inferences
- rubric 起作用的机制是**把整体判断拆成可回答的小问题**（MSAVBench、VisionReward、Video-Bench 的 chain-of-query 都是这一形态），不是「给 VLM 读电影理论」。所以 rubric 条目必须是可观察的 yes/no，不能是「构图是否优美」。
- **工具取证 > 纯 rubric**：MSAVBench 中 tool-grounded 提升（+0.34~0.38）大于纯 rubric（+0.25）。对代码渲染视频，工具就是程序信号（光流、直方图、bbox、相机位姿），应优先。
- 证据都来自扩散生成视频；对代码渲染短片的迁移效果**没有数据**。

### Gaps
- 没有找到同一判官、同一数据「无 rubric vs 电影 rubric」的严格消融（MSAVBench 只覆盖 3 个指标，且非审美类）。
- 没有找到「把 Murch / Bowen 规则写进 prompt」后与专家剪辑师一致性的研究。

---

## Q4. 候选 rubric：短片（代码渲染）的 18 条可检查项 + pairwise 版

### Takeaway
按「技术底线门控 → 单帧构图 → 运动与镜头 → 剪辑（仅多镜头）→ 视觉结构与情感」五层组织；18 条里 6 条纯程序（1、2、3、4、6、16），5 条优先读代码或场景状态（8、9、11、14、15），6 条程序初筛加 VLM 复核，只有第 7 条以 VLM 为主。镜头运动、焦距这类 VLM 认不准的条目，一律改成读代码。

### Cited Findings
- 每条 rubric 的出处见下表「来源」列，对应 Q1–Q3 已引用的原始链接；本节无新增事实。

### Inferences

**标记说明**
- 检查方式：`P` = 程序（帧统计 / 光流 / 镜头切分 / 直方图 / 闪烁）；`C` = 读代码或场景状态（DOM bbox、bpy 相机）；`V` = 只能 VLM 看帧；`P+V` = 程序初筛、VLM 复核
- 迁移性（对网页 / Blender 渲染短片）：✔ 直接适用；△ 有条件；✘ 基本不适用

**L0 技术底线（门控：任何一条 fail → 整段判不合格，不进入审美比较）**

| # | 检查项（yes/no） | 来源 | 方式 | 迁移 |
|---|---|---|---|---|
| 1 | 无闪烁：静止区域相邻帧 MAE 无尖峰，无整帧亮度跳变 | VBench Temporal Flickering；DOVER 失真 | P | ✔（WebGL 绘制顺序、z-fighting 闪烁是代码渲染高发问题） |
| 2 | 无卡顿：意图运动段内无连续重复帧（stall），帧间运动量无突降为 0 | DOVER「stall」 | P | ✔（截帧时序不稳会导致） |
| 3 | 运动平滑：插帧重建误差低于阈值，无抖动（jitter） | VBench Motion Smoothness；DOVER「jitter」；CameraBench steadiness | P | ✔ |
| 4 | 曝光正常：每帧亮度直方图两端裁剪像素占比低于阈值（如 <2%，阈值需标定），无意外过曝 / 欠曝 | DOVER「over/under-exposure」；VADB Lighting；Blain Brown Exposure | P | ✔（Blender 高光溢出、网页纯白背景需豁免） |
| 5 | 清晰无伪影：无锯齿、无文字模糊、Cycles 无 firefly 噪点 | VBench Imaging Quality（MUSIQ）；DOVER artifacts / low sharpness / noise | P+V | ✔ |
| 6 | 不是静图：最大 5% 光流均值超过阈值 | VBench Dynamic Degree | P | ✔ |

**L1 单帧构图（在关键帧上判）**

| # | 检查项 | 来源 | 方式 | 迁移 |
|---|---|---|---|---|
| 7 | 主体唯一且可指认：抽帧里能说出「这一帧的主体是什么」，且显著性峰值落在它上面 | VADB Composition（主体突出）；VideoAesBench visual subject；DOVER 审美≈语义 + 构图 | V（+P 显著性图） | ✔ |
| 8 | 关键元素不被画框意外裁切；人物有 headroom（ECU 豁免） | Bowen Headroom p.25 | C / P | △（网页 = 安全区留白，Blender = 主体 bbox 投影） |
| 9 | 运动主体前方留白 ≥ 后方（look / lead room） | Bowen Look Room p.28 | C（bbox + 运动方向）/ V | △（有方向性运动时才适用） |
| 10 | 主体质心落在三分线附近或明显有意居中，不是「随手贴边」 | Bowen Rule of Thirds p.30；Mercado 2 版 | P（弱信号）+V | ✔（只作 pairwise 参考，不作硬门槛） |

**L2 运动与镜头**

| # | 检查项 | 来源 | 方式 | 迁移 |
|---|---|---|---|---|
| 11 | 镜头运动可归为一个明确原语（pan / tilt / dolly / truck / arc / zoom / static），且与 brief 一致 | CameraBench taxonomy；Mercado shot 章；Katz Part IV | **C**（读相机 F-curve / CSS transform），**不要用 V** | ✔ Blender；△ 网页（多数无「相机」） |
| 12 | 同一时刻运动焦点不超过一个，次要元素运动幅度明显小于主体 | Murch eye-trace；Block movement | P（光流分区统计）+V | ✔ |

**L3 剪辑（仅多镜头；单镜头直接跳过）**

| # | 检查项 | 来源 | 方式 | 迁移 |
|---|---|---|---|---|
| 13 | 镜头长度不随机：切分后镜头时长序列有节奏规律（或与音乐节拍对齐） | Murch Rhythm 10%；Bordwell rhythmic relations | P（镜头切分 + 时长统计）+V | ✔ |
| 14 | 不越轴：跨切点运动主体的 screen direction 一致 | Bowen 180° p.102；Bordwell axis of action；Arijon line of interest | C（Blender 相机相对动作轴）/ V | △（需有主体和多机位） |
| 15 | 无意外 jump cut：同一主体相邻镜头机位角差 ≥30° 或景别明显变化 | Bowen 30° p.106；Wikipedia | C（相机位姿差）/ V | △ |
| 16 | eye-trace 衔接：切点前一帧与后一帧的显著性质心距离小（或有意引导） | Murch Eye-trace 7% | P | ✔ |

**L4 视觉结构与情感（只做 pairwise，不做绝对分）**

| # | 检查项 | 来源 | 方式 | 迁移 |
|---|---|---|---|---|
| 17 | 色彩统一：主色调数量有限、全片一致，无干扰性偏色 | VADB Color；VideoAesBench color；Block color | P（k-means 色相）+V | ✔ |
| 18 | 强度曲线有设计：tone / color / motion 的对比度随时间有升有收（有高潮），而不是全程平 | Block Contrast & Affinity | P（逐帧对比度、饱和度、光流强度曲线）+V 判意图 | ✔ |

（情感 / 故事 = Murch 51% + 23% 的大头，但 VideoAesBench 显示 LMM 在 affectiveness 类与开放题最弱，所以不单列条目，只在 pairwise 的总体偏好里体现。）

**Pairwise 版本（A vs B，同 brief）**
- 流程：
  1. L0 门控：任一方有 fail → 另一方直接胜；双方都 fail → 记「都差」
  2. L1–L4 逐条问「哪一段更满足第 k 条」，选项 A / B / 平；**只判当前条目**（照 VBench 协议）
  3. 每对左右互换各判一次，结果不一致记「平」（处理位置偏差）
  4. 汇总：各条胜负加权；平局时按 Murch 排序 tie-break（rhythm > eye-trace > 2D 平面 > 3D 空间）
- 权重来源：可照 VisionReward 用少量人标 pair 做 logistic regression 学，而不是手设
- 问法示例（第 9 条）：「两段视频中运动主体的前进方向一侧留出的空白，哪一段更充分？如果都没有方向性运动，选『不适用』。」

**为什么这样分层（推断依据）**
- L0 门控：DIVIDE-3k 中技术权重 0.572 > 审美 0.428，且两者相关 0.8752，不先门控审美分会被技术缺陷带偏。
- L2 / L3 尽量用 C：ShotBench / CineTechBench 中 VLM 认镜头运动约 50–57%，焦距最低 31.9%。
- L4 只做 pairwise：VideoFeedback VQ κ=0.088，VADB 各维 α 也只有 0.54–0.66，绝对分噪声大。

### Gaps
- 阈值（MAE 尖峰、裁剪像素比、光流阈值、30° 的具体角度）全部需要在本项目渲染数据上标定，文献里没有面向代码渲染短片的阈值。
- 第 16 条（eye-trace 质心距离）和第 18 条（Block 强度曲线）没有找到前人实现或人评验证，属本文提出的程序化方案。
- rubric 整体与人评的一致性尚无数据，需要在项目内做小规模 pairwise 人标验证（可参考 VBench：每组 4 模型、6 对）。

