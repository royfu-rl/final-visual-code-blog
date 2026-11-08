# VLM 审美 judge：文字 rubric 之外再给多模态示例（exemplar）有没有用、协议怎么定

> 截至 2026-11-03。服务于博客论点「审美评估 = 专家 rubric + 多模态示例 → VLM」。
> 与前序笔记的关系：`VLM 审美 rubric 调研/rubric_judges_universality.md`、`web_ui.md` 已有的 GenArena、FRAME、TASTE、WebDevJudge、UIClip、ArtifactsBench、CheckEval 数字**不重抄**，只在需要时一句话引用并标「前序笔记」。本文聚焦 **exemplar 本身**。
> 核实标记
> - 【一手】本轮读过论文正文 / 表格
> - 【二手】只来自摘要页、搜索摘要、第三方综述，或转引前序笔记
> - 【未核实】来源有歧义或对不上
> - [本文计算] = 由引用数字换算；[推断] = 本文作者推理

---

## Q1 UI / 设计 / 审美判断里，多模态 few-shot / exemplar 的直接证据

### Takeaway
- 直接证据只有 4 篇能量化 exemplar 的作用，结论很一致：**exemplar 稳定提升「输出的形式与校准」，但对「二元偏好方向」只给 0~3 个点**。
  - UICrit：批评质量 0.24 → 0.44（8-shot、按视觉相似选例），用户研究 0.31 → 0.48。
  - DesignPref：同 4 个前沿 VLM、同测试集，rubric 零样本 → 8-shot 图像示例，二元准确率 −0.1 ~ +2.9 点，但四档强度准确率 +3 ~ +24 点。
  - ARR：T2I 偏好上，rubric 之外再加人选的正反例对，平均准确率再 +12.5 ~ +14.8 点、位置偏差 Δ 从约 30 降到约 9。
- 被点名的其余工作（Duan CHI 2024、WebDevJudge、ArtifactsBench、Design2Code、WiserUI-Bench、MLLM-as-UI-Judge、UIClip 里的 GPT-4V）**都没有 exemplar 消融**，有的根本没用 exemplar。

### Cited Findings

**1. UICrit（Duan et al., UIST 2024）——唯一系统比较「选例策略 × shot 数」的 UI 工作** — [arXiv HTML v3](https://arxiv.org/html/2407.08850v3)【一手】
- 设置
  - 模型：**Gemini Pro Vision**；GPT-4V 只列为 future work
  - shot 数：2 / 4 / 8；**8 是 Gemini 当时 context window 能塞下的上限**
  - prompt 里固定放三套准则（NN/g 10 heuristics、CrowdCrit、Apple HIG）——**没有「去掉准则」的对照组**
  - 选例方式
    - 区域级：random；visual similarity（裁剪 patch 的像素 RMS 差）；semantic similarity（patch 的 CLIP embedding）
    - 整屏级：random；visual similarity（截图 RMS）；task similarity（任务描述的 SentenceBERT 余弦）；visual + task（CLIP 图文联合 embedding）
  - 论文**没有明说** exemplar 的截图本身是否放进了 prompt（只说选中的 UI、框、批评作为 few-shot 示例）
- 区域级批评质量（Table 3，Avg. Comment Quality Score；zero-shot = **0.24**，45 条评论）
  - 8-shot visual similarity **0.44**
  - 8-shot semantic similarity 0.42
  - 4-shot visual similarity 0.36
  - 4-shot semantic similarity 0.34
  - 8-shot random **0.31**
  - 原文观察：shot 越少，「generates more comments for each patch, but they are of lower quality」
- 整屏级（Table 4，前 5 名设定；列 = 批评质量 / 评论数 / **Rating Accuracy**）
  - 8-shot visual + task similarity：**0.58** / 14 / **0.53**
  - 4-shot visual + task：0.48 / 10 / 0.22
  - 8-shot task：0.42 / 8 / 0.31
  - 4-shot task：0.38 / 12 / 0.17
  - 8-shot visual：0.38 / 10 / 0.17
  - Rating Accuracy 定义：与设计师分完全一致 = 1，差 1 分 = 0.5，否则 0
  - **表里没有 zero-shot 的 rating accuracy**，所以无法算「示例让打分准了多少」
- 用户研究（6 名设计专家，6 个 UI；Table 7）
  - zero-shot **0.31** → 8-shot visual + task + 坐标视觉提示 **0.48**（+0.17，p = 5e-4，原文「55 percent increase」）→ 人类设计师 **0.75**
  - 专家 67% 选 few-shot 而非 zero-shot；81% 选人类而非 few-shot
  - 一致性：标注者 Fleiss κ 0.30 / 0.31；专家打分 κ 0.29，排序 0.55

**2. DesignPref（Peng, Bigham, Wu, 2025）——同模型同数据「rubric 零样本 vs rubric + 8 张检索示例对」** — [arXiv HTML v1](https://arxiv.org/html/2511.20513v1)【一手】
- 设置
  - 20 名职业设计师；每人 360 条训练样本，合起来 7,200 条
  - zero-shot judge：给通用 rubric（clarity、readability、spacing & alignment、primary action emphasis、aesthetic balance、fit to prompt），要求只看可见特征、避免位置偏差、不许平局
  - few-shot judge：**k = 8**（直接沿用 UICrit 的最佳配置），每个示例 = **图 A + 图 B + 该用户的标签**；rubric 降级为 tie-breaker
  - 检索：屏幕描述用 Sentence-BERT，截图用 **UIClip 视觉编码器**；每个训练对按两种顺序各建一个索引向量，取最大相似度
  - personalized = 只检索同一个设计师的标注；pooled = 检索全部 20 人的标注（多人标签取平均再取整）
- 结果（测试集，按 20 名设计师宏平均；列 = 二元准确率 % / 四档准确率 % / SRCC）

  | 模型 | zero-shot（rubric） | 8-shot pooled | 8-shot personalized |
  |---|---|---|---|
  | GPT-5 | 57.70 / 31.35 / 0.216 | 57.62 / 34.36 / 0.203 | 58.89 / 38.53 / 0.211 |
  | Gemini-2.5-Pro | 53.65 / 17.76 / 0.135 | 56.15 / 22.56 / 0.169 | 56.53 / 22.35 / 0.170 |
  | Qwen3-VL-235B-Thinking | 55.36 / 22.09 / 0.131 | 55.78 / 41.59 / 0.122 | 56.83 / 42.67 / 0.132 |
  | Qwen3-VL-30B-Thinking | 54.82 / 16.17 / 0.117 | 54.78 / 38.79 / 0.110 | 56.20 / 40.41 / 0.128 |

  - 参照：微调 UIClip personalized（strength-aware margin）**60.16** / 34.37 / 0.217；pooled 全量 57.45 / 41.23 / 0.196
  - **没有 k 的消融；没有位置偏差的测量**

**3. ARR（Auto-Rubric as Reward, 2026）——rubric 之上再加正反例对** — [arXiv HTML](https://arxiv.org/html/2605.08354)【一手】
- guide 是什么
  - 原文：「a fixed set of human-curated preference exemplars drawn from a held-out subset of the training split of each benchmark」
  - 每个示例 =（prompt, preferred image, dispreferred image, preference rationale），**含图**，「embedded verbatim as in-context demonstrations」
  - **示例个数、是否按相似度检索：论文都没写**
- 唯一含 guide 的表是 Table 5（HPDv3 测试集 14,400 对；Forward / Reverse / Avg / Δ）
  - Qwen3-VL-8B：base 67.2 → +ARR 70.2 → **+ARR w/ guide 85.0**（Δ 34.6 → 31.6 → 10.3）
  - GPT-5：72.4 → 76.1 → **88.8**（Δ 32.6 → 28.2 → 9.3）
  - Gemini 3.1 Pro：76.6 → 78.3 → **90.8**（Δ 30.2 → 27.8 → 8.9）
- 局限
  - guide 结果**不在主表 Table 1 里**，只出现在位置偏差消融
  - 没有 guide-only（无 rubric）对照，没有示例数消融
  - 示例与测试同分布（同 benchmark 训练划分）；HPDv3 是 T2I 偏好，含图文对齐，不是 UI 审美

**4. 被点名、但没有 exemplar 证据的工作**
- Duan et al. CHI 2024「Generating Automatic Feedback on UI Mockups with LLMs」— [arXiv HTML](https://arxiv.org/html/2403.13139)【一手】
  - 输入是 Figma 的**精简 JSON 文本**，不是截图；作者试过多模态模型，「considerably worse than GPT-4's for this task (at the time)」
  - **没有用 few-shot**：GPT-4 只有 8.1k context，单个 UI 的 JSON 就占 3–5k token
  - 替代做法：把用户驳回的建议作为「不准确输出」的例子放回对话历史，加一步 self-reflection（一种文字形式的负例）
  - 结果：51 个 UI 上 52% 建议准确；迭代后期降到 **39%**；与 12 名专家比，GPT-4 precision 0.603 / recall 0.380 / F1 0.466，人类 0.829 / 0.336 / 0.478
- WiserUI-Bench（Jeon et al., ACL 2026）— [arXiv HTML v4](https://arxiv.org/html/2505.05026v4)【一手；正文末尾约 9.8k 字符未读】
  - 300 对真实 UI（移动 + 网页），胜者由**工业 A/B 测试**确定；另有 684 条专家解读
  - 平均准确率 AA：GPT-4o **60.11**、Qwen2.5-VL-32B 57.56、InternVL-2.5-38B 57.83、o1 57.17、Claude 3.5 Sonnet 56.39（随机 50）
  - 推理策略（只测 GPT-4o 和 Claude 3.5 Sonnet）：CoCoT、Self-Refine、DDCoT、Multi-Agent Debate；GPT-4o 最好 DDCoT AA 61.72，Claude 全部 ≤ 56.44
  - 已读部分**没有 few-shot 示例实验**
- MLLM as a UI Judge（2025）— [arXiv HTML](https://arxiv.org/html/2510.08783v1)【一手】
  - 30 个 UI、500 名 MTurk、保留 9,296 条评分、9 个因子（1–7 Likert）
  - 全部 zero-shot；pairwise 总准确率 Claude-3.5 **59.98**、GPT-4o 59.60、Llama-3.2-11B 52.96
  - 人类分差越大，模型越准：GPT-4o / Claude 从约 50% 升到约 90% / 93%
  - 作者把「chain-of-thought and few-shot learning」列为 future work
- WebDevJudge、ArtifactsBench、UIClip、Design2Code：前序笔记已核，**均无 exemplar 消融** — [WebDevJudge](https://arxiv.org/html/2510.18560v2)；[ArtifactsBench](https://arxiv.org/html/2507.04952v2)；[UIClip](https://arxiv.org/html/2404.12500v1)；[Design2Code](https://arxiv.org/abs/2403.03163v1)【二手：转引前序笔记】
  - WebDevJudge：rubric 在 pairwise 下与 Direct 提示「comparably」，无增益
  - UIClip：GPT-4V 拿到与设计师相同的 CRAP 文字描述，pairwise 仍只有 51.58%
- 2026 网页审美 reward 里「参考图」的用法（与 exemplar 相关但不等同）
  - AesCode（arXiv 2610.18860）：用同一 prompt 生成的图作为 aesthetic guidance；VLM judge 用样本级 Visual Graph Rubric；摘要称 reference 作为**生成器输入**和**视觉 reward 来源**都有益；AesCode-8B / 32B 比同尺寸 Qwen3-VL 高 31.1 / 22.4 个百分点 — [arXiv abs](https://arxiv.org/abs/2610.18860)【一手，仅摘要；消融数字未见】
  - WebRISE（arXiv 2606.03220）：有视觉参考时以「与参考页的布局一致性」为主、审美为辅 — [arXiv PDF](https://arxiv.org/pdf/2606.03220)【二手：搜索摘要】
  - WebGen-R1：VLM 0–5 审美分与人 Pearson 0.762 / Spearman 0.734 — [Moonlight 综述](https://www.themoonlight.io/review/webgen-r1-incentivizing-large-language-models-to-generate-functional-and-aesthetic-websites-with-reinforcement-learning)【二手】

### Inferences
- [本文计算] DesignPref 里 exemplar 的增益拆开看
  - 二元准确率
    - pooled：GPT-5 −0.08、Gemini +2.50、Qwen-235B +0.42、Qwen-30B −0.04
    - personalized：+1.19、+2.88、+1.47、+1.38
  - 四档准确率
    - pooled：+3.01、+4.80、**+19.50、+22.62**
    - personalized：+7.18、+4.59、+20.58、+24.24
  - SRCC：GPT-5 反而 0.216 → 0.203 / 0.211
- [推断] **exemplar 教会的是「标尺」，不是「品味方向」**
  - 四档（强弱程度）大涨、二元方向几乎不动 → 示例主要在校准「多强算强偏好」、标签分布和输出格式
  - 与 UICrit 同向：示例最明显改善的是批评的形式与密度（评论更少更准）
  - 与人-人天花板一致：设计类单人 vs 单人 pairwise 约 55–62%（前序笔记），GPT-5 零样本已到 57.7%，剩余空间本就很小
- [本文计算] ARR 的 guide 平均准确率增益（相对 +ARR）：Qwen +14.8、GPT-5 +12.7、Gemini +12.5
  - **更正前序笔记**：前序写「平均准确率再 +4~+12 点」，按 Table 5 的 Avg 列应为 +12.5~+14.8；+4.1/+3.2/+3.0 只是 Forward 列
  - 增益几乎全部来自 Reverse 列（+25.4 / +22.1 / +21.9）→ 示例的主要作用是**消除位置偏差**，而不是让「正序判断」更准
- [推断] UICrit 的选例结论可直接迁移到网页
  - 相似度选例 > 随机（0.44 vs 0.31），视觉 + 任务联合相似最好（0.58）
  - 8 > 4 > 2，但 8 是被 context 卡住的上限，不是收益饱和点
- [推断] 对博客论点的措辞建议
  - 能说：多模态示例**稳定显著**地降低位置偏差、校准打分尺度、提升批评质量
  - 不能说：示例能把 VLM 与设计师的二元一致率显著拉高——在低共识的 UI 偏好数据上，证据只有 0~3 个点

### Gaps
- 没有任何 UI / 网页工作报告「示例数 k」的完整曲线（UICrit 只有 2/4/8，DesignPref 固定 k = 8，ARR 未写 k）
- UICrit 的 zero-shot rating accuracy 未报，无法量化示例对「打分」的增益
- ArtifactsBench、WebDevJudge、Design2Code 的 judge 都没有测「加截图示例」
- AesCode 的「有 / 无 reference」消融数字只在正文，本轮只读到摘要
- WiserUI-Bench 正文末尾未读完；第三方摘要提到的 G-FOCUS 方法未在一手正文核实

---

## Q2 图像质量 / 审美 MLLM 如何用比较与锚点（anchor / reference），对比单图打分

### Takeaway
- **比较式输入普遍优于或至少不差于单图**：GPT-4V 在「两图对比 + CoT」下 IQA 的 SRCC 最高；Co-Instruct 专训多图比较后在 Q-Bench-PAIR 上追平非专家人类（80.18 vs 80.12）。
- **锚点的正确用法是「拿测试图去和固定锚点比」，而不是「把带分数的示例图放进 prompt」**
  - Compare2Score：5 张低方差锚点 × soft comparison → 概率矩阵 → MAP 得绝对分，9 个数据集 SOTA；同样的概率矩阵推断也把 Co-Instruct 的零样本 SRCC 从 0.58 提到 0.82（LIVE）
  - 反例：Wu et al. ECCV 2024 给 GPT-4V 看「一张示例图 + 人类分数 50」，几乎无效；放 8 张图的 in-context 版本 SRCC 大幅下降

### Cited Findings

**1. Compare2Score（Zhu, Wu et al., NeurIPS 2024）——锚点 + 软比较** — [arXiv HTML v1](https://arxiv.org/html/2405.19298v1)【一手】
- 锚点怎么选
  - 把参考数据集（KonIQ-10k 训练集）按 MOS 分成 α = 5 个质量区间
  - 每个区间取 β 张 **MOS 方差最低**的图（人类评分最一致的图），默认 β = 1 → **共 5 张锚点**
  - β 的消融只在 Fig. 4：增大 β 不提升，「β = 1 suffices」；推理时间随 β 线性增长
- 推理
  - 测试图与 5 张锚点逐一比较，取「测试图更好」的概率（soft comparison），组成 (m+1)×(m+1) 概率矩阵，MAP 估计出绝对分
  - 每张图 5 次比较；全配对需要 M(M−1)/2 次，作者认为不可行
- 与单图打分模型对比（Table 1，SRCC / PLCC）
  - KADID-10k：Compare2Score **0.952 / 0.939**，Q-Align 0.869 / 0.927，LIQE 0.930 / 0.931
  - CSIQ：0.950 / 0.943 vs Q-Align 0.915 / 0.936
  - KonIQ-10k：0.931 / 0.939 vs Q-Align **0.935** / 0.934（这里单图的 Q-Align 略好）
  - CLIVE：0.914 / 0.928 vs Q-Align **0.931** / 0.921（这里也是 Q-Align 好）
- 跨数据集 SRCC（Table 2）：TID2013 / SPAQ / AGIQA-3K = 0.823 / 0.906 / 0.730 vs Q-Align 0.801 / 0.813 / 0.725
- 零样本通用 LMM：概率矩阵 vs 计数矩阵（Table 3，SRCC，LIVE / CSIQ / BID / CLIVE）
  - Co-Instruct：0.582 / 0.569 / 0.820 / 0.694 → **0.822 / 0.768 / 0.866 / 0.768**
  - LLaVA-1.5：0.214 / 0.148 / 0.122 / 0.015 → 0.386 / 0.555 / 0.361 / 0.292
  - mPLUG-Owl2：0.408 / 0.013 / 0.217 / 0.221 → 0.449 / 0.129 / 0.551 / 0.355
  - **注意**：这是「软概率 vs 硬投票」的对比，**不是**「锚点比较 vs 直接单图打分」；论文没给后者；GPT-4V 没测

**2. Co-Instruct / MICBench / Q-Bench-PAIR（Wu et al., ECCV 2024）——多图质量比较** — [arXiv HTML](https://arxiv.org/html/2402.16641)【一手】
- 数据：Co-Instruct-562K；MICBench 2,000 组（1,000 组 3 图 + 1,000 组 4 图）；Q-Bench-PAIR A1 1,999 道选择题
- MICBench 总准确率（Table 6）
  - Co-Instruct **83.33%**、GPT-4V 78.82%、非专家人类 78.35%、Qwen-VL-Max 70.55%、Gemini-Pro 69.79%、InternLM-XComposer2-VL 51.76%、随机 31.47%
- Q-Bench-PAIR A1（Table 2）
  - Co-Instruct **80.18%**、非专家人类 80.12%、GPT-4V 78.07%、Qwen-VL-Max 66.99%、Gemini-Pro 60.46%
  - 同一基座「不加多图比较数据」只有 53.15% → 比较能力要专门训
- 3 图 → 4 图（MICBench）
  - GPT-4V 80.32 → 77.28；Co-Instruct 84.69 → 81.94
  - 开源模型掉得更多：LLaVA-v1.5-13B 46.81 → 41.90；InternLM-XComposer2-VL 55.70 → 46.51
  - 人类反而 77.18 → 79.55
- 换序一致性（2AFC-LMM，交换两图后判决一致的 κ）：Co-Instruct 0.864、GPT-4V 0.823、无多图数据版 0.432
- 图像标注方式：用「The first image: … The second image: …」交错标注，比直接堆图好
  - Q-Bench-PAIR 76.37 → 80.18；MICBench 78.92 → 83.33
- 长度偏差：A2 详细推理上 GPT-4V 4.89 vs Co-Instruct 4.82，作者归因于「outputs from GPT-4V are more than twice as long」
- 论文**没有**在同一批题目上直接比较「比较式 vs 单图绝对分」；只引用「comparative settings can effectively avoid the ambiguity on absolute evaluations」作动机

**3. Wu, Ma et al.「A Comprehensive Study of MLLMs for IQA」（ECCV 2024）——带分示例图（in-context）vs 标准 vs CoT** — [arXiv 2403.10854](https://arxiv.org/abs/2403.10854)（PDF 本地抽取）【一手】
- 设计：3 种心理物理协议（single / double / multiple stimulus）× 3 种提示（standard / CoT / in-context）= 9 套；FR 与 NR 两种场景；LLaVA-v1.6、mPLUG-Owl2、InternLM-XC2-VL、GPT-4V
- in-context 的具体形式：先给示例图与人类分数，例如「the human perceptual quality score of the first image is 50」，再让模型打第二张；multiple-stimulus 版本一次放 8 张图（FR 为 10 张）
- GPT-4V 的 SRCC（Table 1，均匀采样子集；列 = FR-KADID / Aug-KADID / TQD / SPCD / NR-KADID / SPAQ / AGIQA-3K）
  - Single-stimulus
    - Standard 0.745 / 0.786 / 0.773 / 0.098 / 0.467 / 0.860 / 0.420
    - CoT 0.809 / 0.782 / 0.809 / 0.121 / 0.517 / 0.869 / 0.677
    - In-context 0.771 / 0.753 / 0.738 / 0.028 / 0.590 / 0.845 / 0.650
  - Double-stimulus（两图比较）
    - Standard 0.679 / 0.743 / 0.655 / 0.031 / 0.552 / 0.834 / 0.599
    - **CoT 0.818 / 0.830 / 0.786 / 0.124 / 0.639 / 0.881 / 0.771**（作者认定的 GPT-4V 最优系统）
    - In-context **0.470 / 0.244 / 0.340** / 0.122 / 0.531 / 0.761 / 0.714
  - Multiple-stimulus
    - Standard 0.824 / 0.844 / 0.747 / 0.037 / 0.397 / 0.715 / 0.461
    - CoT 0.761 / 0.806 / 0.754 / 0.036 / 0.537 / 0.817 / 0.679
    - In-context **0.585 / 0.496 / 0.389 / 0.023 / 0.168 / 0.416 / 0.201**
- 作者结论原文
  - 「the inclusion of a human quality score has minimal impact on the GPT-4V inference」
  - 「eight images for multiple-stimulus in-context prompting, even GPT-4V finds difficulty in processing such substantial amount of visual information, resulting in a sharp performance drop」
  - 三个开源模型「single-stimulus method is the optimal choice due to their limited ability to analyze multiple images」；LLaVA-v1.6 和 mPLUG-Owl2 会「completely disregard the second image」
  - CoT「consistently enhances the performance of GPT-4V」

**4. 其它 IQA / 审美 MLLM**
- DepictQA（ECCV 2024）：通用 MLLM 带参考图时只在 18% 的回答里识别出真实失真，LLaVA-1.5 单图为 24%；作者归因于通用模型只在单图上训练 — [arXiv PDF](https://arxiv.org/pdf/2312.08962)【二手：搜索摘要；表格未核】
- Q-Align / UNIAA / AesBench / ArtiMuse：都是单图打分 / 单图问答范式（离散等级 token 加权等），数字见前序笔记 — [Q-Align](https://arxiv.org/html/2312.17090)；[UNIAA](https://arxiv.org/html/2404.09619)；[AesBench](https://arxiv.org/html/2401.08276)；[ArtiMuse](https://arxiv.org/abs/2507.14533)【二手：转引前序笔记】

### Inferences
- [推断] **「锚点」比「示例」更适合审美打分**
  - 示例（带分图放进 prompt）：模型基本不看分数（Wu et al.），多图还会拖垮性能
  - 锚点（测试页与固定锚点逐一 pairwise 比，再聚合）：把 VLM 最擅长的比较判断转成绝对分，且锚点固定 → 跨批次可比
  - 网页版做法：每个质量档选 1 张「人类评分方差最低」的参考页，共约 5 张；每个候选页做 5 次 A/B（再加换序就是 10 次）
- [推断] **比较 + CoT 是 GPT-4V 级模型在 IQA 上的最优组合**，但这与 MLLM-as-a-Judge 里 CoT 让打分变差（前序笔记 0.557 → 0.299）相反 → CoT 的作用随任务变，应各自 A/B 测
- [推断] 多图比较能力不是免费的：通用模型在 Q-Bench-PAIR 上 53–67%，专训后 80%；**开源 judge 若要吃多张示例图，最好先在多图比较数据上训过**

### Gaps
- Compare2Score 的 β（锚点数）消融精确数字只在图里
- 没找到「锚点比较 vs 直接单图打分」在**同一通用 VLM、同一数据**上的对照
- AesExpert、VisualCritic、AesMamba 关于 reference / anchor 的实验：本轮未检到
- 所有锚点工作都在照片 IQA 上做，网页 / UI 截图上的锚点协议**没有公开研究**

---

## Q3 多图 in-context learning 的上限：前沿 VLM 真的会用图像示例吗，多少算太多

### Takeaway
- **多模态 ICL 主要是「文字驱动」**：在 VQA 类任务里，把示例图删掉只掉 1.2–1.5 个点；把同等语义的示例换成纯文字，shot 曲线反而更陡更稳。
- **shot 数的经验上限**
  - 开源 / 中等模型：增益往往在 4–8 shot 前见顶，之后持平甚至下降
  - GPT-4V（2024）：IQA 里 8 张图一次输入就明显崩；MICBench 上 3 图 → 4 图掉 3 个点
  - Gemini 1.5 Pro 这类长上下文模型：在分类任务上可以 log-linear 地吃到约 1,000 个示例，但 GPT-4o 曲线不稳，开源模型完全不受益
- **相似度检索的示例收益里，有很大一部分是「抄邻居标签」**：kNN 多数投票在分类上甚至比 RICES ICL 更好。

### Cited Findings

**1. VL-ICL Bench（Zong et al., ICLR 2025）** — [arXiv HTML v4](https://arxiv.org/html/2403.13164v4)【一手】
- 覆盖 GPT-4V、LLaVA-OneVision 0.5B/7B/72B、IDEFICS 9B/80B、Qwen-VL-Chat、Mantis、Phi-3-Vision 等 20 余个模型；shot 1/2/4/8，附录到 16/32/64
- 原文结论
  - 「VLLMs often struggle to make use of a larger number of ICL examples」，增益常常早早见顶后下降
  - 部分模型 ICL efficiency 为负（shot 越多越差），例如 GPT-4V 在 CLEVR Count Induction 上
  - zero-shot 强 ≠ ICL 强：LLaVA-Next-7B 主流榜单强，ICL 最弱之一
  - 规模涌现：LLaVA-OV-72B 全面受益；0.5B / 7B 在两个任务上随 shot 增加跌到随机以下
- 原因分析
  - 图像 token 多：一张 LLaVA 图 576 token，8-shot 就能超过 4k 窗口
  - SelfExtend（4k → 16k）对部分模型有用（LLaVA-Next-7B 某任务峰值 37.2 → 51.0），但「necessary but not sufficient」
  - **把示例图换成语义等价的文字，性能「grows much more sharply and consistently with number of shots」**
- 参考峰值：GPT-4V Fast Open-Ended MiniImageNet 0 → 78.0；LLaVA-OV-72B 0 → 98.7

**2. Baldassini et al.「What Makes Multimodal In-Context Learning Work?」（CVPRW 2024）** — [ar5iv](https://ar5iv.labs.arxiv.org/html/2404.15736)【一手】
- 模型 IDEFICS-9B（附录 OpenFlamingo-9B），shot 0/4/8/16/32，主比较 16-shot
- 示例图的作用
  - VQA：删掉或替换示例图只掉约 **1.2–1.5** 点；删掉示例问题掉约 3.5 点，换成随机问题掉约 9.5 点
  - 分类 / caption 依赖图：COCO CIDEr 103.66（有图）→ 78.02（无图）→ 28.43（随机图）
- RICES（CLIP 相似度检索示例）vs 随机，16-shot
  - ImageNet 75.18 vs 23.90；CIFAR-100 75.68 vs 49.68；Hateful Memes 63.40 vs 52.00；VQAv2 56.26 vs 55.39
- kNN 多数投票（直接用检索到的邻居标签投票）vs RICES ICL
  - CIFAR-100 **81.24 vs 75.68**；ImageNet **79.52 vs 75.18**（投票更好）；生成类任务投票远差
- 近因偏差：RICES 下约 **12%** 的 VQA 回答直接复制最后一个示例的答案
- 原文结论：「M-ICL is primarily text-driven, and that images in the context have little impact on the overall performance」；「M-ICL is not better than a simple strategy based on majority voting over context examples」

**3. Many-Shot ICL in Multimodal Foundation Models（Jiang et al., 2024）** — [arXiv HTML v2](https://arxiv.org/html/2405.09798v2)【一手】
- GPT-4o（2024-05-13）与 Gemini 1.5 Pro（preview-0409），14 个数据集（医学、遥感、自然图、分子）
- 从 zero-shot 到最优 shot 数，两者平均约 **+17** 个点
- Gemini 1.5 Pro 在 9/10 个分类集上 log-linear 提升，8 个数据集一直涨到约 1,000 个示例；GPT-4o 曲线多为 V 形（先降后升）
- Llama 3.2-Vision 与 InternLM-XComposer2.5「do not benefit from the demonstration examples」
- 工程限制
  - Claude 3 Opus 被排除：当时「only accepts up to 20 images in one request」
  - GPT-4o 128k 窗口，长输入易超时
- 把最多 50 个 query 打包到一次请求里，zero-shot 和 many-shot 都能涨点，并大幅降成本
- 注意：都是**分类任务**，有明确标签，不是审美这种低共识判断

**4. 多图理解本身的上限**
- MuirBench（ICLR 2025）：11,264 张图、2,600 道选择题、12 个任务；GPT-4o **68.0%**、Gemini Pro 49.3%；只在单图上训过的开源 MLLM 低于 33.3% — [arXiv HTML v2](https://arxiv.org/html/2406.09411v2)【二手：搜索摘要引摘要；人类基线表述有歧义，未取】
- IQA 里的多图崩溃：GPT-4V 8 图 in-context SRCC 大幅下降（见 Q2-3）【一手】
- MICBench 3 → 4 图：GPT-4V −3.0，Co-Instruct −2.8，开源模型 −5 ~ −9（见 Q2-2）【一手】
- UI 场景的实际上限：UICrit 在 Gemini Pro Vision 上 8 shot 就到 context 上限；Duan 2024 因 8.1k 窗口完全放不下 few-shot（见 Q1）【一手】

### Inferences
- [推断] 对网页审美的 k 值建议
  - pairwise 示例每对 2 张图 → 8 对 = 16 张 + 待判 2 张 = 18 张图；已经超过 2024 年 GPT-4V 在 IQA 上崩溃的规模（8 张）
  - 建议起点：**3–4 对示例（6–8 张图）**，示例图降分辨率或只裁关键区域；在自己的验证集上扫 k = 0/2/4/8，看曲线是否见顶
  - 长上下文前沿模型（Gemini 系）可以试更多，但 many-shot 的正面证据都来自有标签的分类任务
- [推断] **示例的「图」和「理由文字」要分开看**
  - VL-ICL 与 Baldassini 都显示文字比图更容易被模型利用 → 示例里的**文字理由**（ARR 的 rationale）可能是主要有效成分
  - 这正是需要做「去图保文 / 保图去文」消融的原因（见 Q5）
- [推断] **相似度检索的风险**：在低共识的审美判断上，检索到的近邻标签本身就有噪声；如果模型主要在「抄邻居标签」（Baldassini 的 kNN 现象），等于把单人 / 少数人的偏好硬塞给 judge
  - 对策：示例里 A 胜 / B 胜的数量配平；示例顺序随机化；最后一个示例的标签不要总与待判对子的「表面相似答案」一致（防近因复制）

### Gaps
- 没有任何研究在**审美 / 设计**任务上画出 shot 数 → 一致率曲线
- 2026 年前沿模型（GPT-5.x、Gemini 3.x、Claude 4.x）在多图 ICL 上的系统评测：本轮未找到；单请求图片数上限的当前官方数字本轮未核
- MuirBench 人类基线的确切数字未核实

---

## Q4 与审美判断相关的偏差与攻击，以及缓解手段

### Takeaway
- **位置偏差是 pairwise 审美判断里最大的单一误差源**：WiserUI-Bench 上 o1 把胜者放第二位时对 97.78%、放第一位时只对 16.56%；ARR 里三个前沿 judge 的正反序差都在 30–35 个点。
- 已量化的缓解手段按效果排序
  - 正反例 exemplar（ARR）：Δ 30 → 9
  - 换序双跑 + 只算两次都对（consistent accuracy），把虚高的准确率还原
  - 交错图像标注（「The first image: …」）：+3.8 ~ +4.4 点
  - 专门的多图比较训练：换序一致 κ 0.43 → 0.86
- 装饰 / 视觉提示偏差（FRAME：bbox 让 GPT-4o 分数 +80.2%）与长度偏差（GPT-4V 回答长 2 倍得分更高）都能被提示词部分缓解但不能清零；自偏好在 VLM 上只有定性证据。

### Cited Findings

**1. 位置偏差（position bias）**
- WiserUI-Bench（Table 2，300 对；FA / SA = 胜者分别放在第一 / 第二位时的准确率，AA = 平均，CA = 两种顺序都判对；随机 AA 50、CA 25）— [arXiv HTML v4](https://arxiv.org/html/2505.05026v4)【一手；FA/SA 的含义按论文用法理解】
  - o1：FA 16.56 / SA **97.78** / AA 57.17 / CA **15.56**
  - GPT-4o：31.89 / 88.33 / 60.11 / 30.11
  - Claude 3.5 Sonnet：26.11 / 86.67 / 56.39 / 24.22
  - Qwen2.5-VL-32B：33.67 / 81.44 / 57.56 / 31.00
  - InternVL-2.5-8B：58.33 / 45.67 / 52.00 / 21.33（偏向第一张）
  - 原文：AA「inflated by strong position bias, especially in proprietary models and the Qwen2.5-VL family, which tend to pick the second image」
  - 最好的 CA 也只有 GPT-4o + MAD(R1) **39.00**
- ARR：base judge 的 HPDv3 正反序差 Δ = 34.6（Qwen3-VL-8B）/ 32.6（GPT-5）/ 30.2（Gemini 3.1 Pro）；+rubric 只降到 31.6 / 28.2 / 27.8；**+rubric + 正反例 guide 降到 10.3 / 9.3 / 8.9** — [arXiv HTML](https://arxiv.org/html/2605.08354)【一手】
- Co-Instruct 换序一致 κ：0.864（Co-Instruct）、0.823（GPT-4V）、0.432（无多图比较数据的同基座）— [arXiv HTML](https://arxiv.org/html/2402.16641)【一手】
- WebDevJudge：GPT-4.1 偏向第二位 15.8%、第一位 0.9% — [arXiv HTML v2](https://arxiv.org/html/2510.18560v2)【二手：转引前序笔记】
- ICL 内部的顺序偏差：RICES 示例下约 12% 的 VQA 回答复制最后一个示例的答案 — [ar5iv](https://ar5iv.labs.arxiv.org/html/2404.15736)【一手】

**2. 长度 / 冗长偏差（verbosity）**
- Co-Instruct：A2 详细推理上 GPT-4V 4.89 vs Co-Instruct 4.82，作者归因于 GPT-4V 输出长 2 倍以上 — [arXiv HTML](https://arxiv.org/html/2402.16641)【一手】
- MLLM-as-a-Judge：内容不变只加长，GPT-4V 分数 +0.6、Gemini +0.75 — [arXiv HTML v3](https://arxiv.org/html/2402.04788v3)【二手：转引前序笔记】

**3. 装饰 / 视觉提示偏差（FRAME）**
- 加 bbox 让 GPT-4o 对 T2I 图的打分 1.14 → 2.05（+80.2%）；叠加文字、黑边、亮度、美颜滤镜都能刷分；pairwise 同样受影响 — [arXiv HTML v2](https://arxiv.org/html/2505.15249v2)【二手：转引前序笔记】
- 缓解：给偏差定义最有效但不清零（GPT-4.1-mini padding +10.4% → +5.6%）；CoT 反而把 bbox 从 −1.0% 推到 +4.1% — 同上【二手：转引前序笔记】

**4. 自偏好（self-preference）**
- Philautia-Eval（arXiv 2604.11589，2026-04）：图像描述评测中，代表性 MLLM 在有参考 / 无参考两种设定下都表现出自偏好；举例 Gemini 2.5 Pro 给自己含幻觉的 caption 打分明显高于其他 judge；多 judge 集成（Pomms）可降低偏差 — [项目页](https://philautia.kinsta.page/)；[arXiv PDF](https://arxiv.org/pdf/2604.11589)【二手：项目页与聚合页；不同来源的数据规模说法不一致，未核实】
- MLLM-as-a-Judge：GPT-4V 自偏好「轻微」，无数字 — [arXiv HTML v3](https://arxiv.org/html/2402.04788v3)【二手：转引前序笔记】

**5. 其它可用的协议级缓解**
- 交错标注每张图：Q-Bench-PAIR 76.37 → 80.18；MICBench 78.92 → 83.33 — [arXiv HTML](https://arxiv.org/html/2402.16641)【一手】
- 强制二选一：允许 tie 时，在可区分对子上准确率 54.9%，强制选择 83.9% — [GenArena](https://arxiv.org/html/2602.06013)【二手：转引前序笔记】
- 用人类分差分层：模型准确率随人类分差从约 50% 升到约 90%（MLLM as a UI Judge）— [arXiv HTML](https://arxiv.org/html/2510.08783v1)【一手】

### Inferences
- [推断] **报 pairwise 准确率时必须报 CA（两种顺序都对）或正反序均值**；只报单序准确率会被位置偏差严重夸大（o1 单看 SA 是 97.78）
- [推断] exemplar 的最大价值可能就在这里：ARR 里 rubric 对位置偏差几乎无效（Δ 只降 3 点），正反例对把 Δ 降了 20+ 点
  - 可能机制：示例里同时出现「好图在前」和「好图在后」，相当于在 context 里做了顺序反事实
  - 对策是**示例里两种顺序各占一半**，否则示例自己会制造新的位置偏差
- [推断] 网页场景里装饰偏差的成本几乎为零（CSS 一行 `border`），exemplar 可以有针对性地放「装饰多但更差」的负例对，教 judge 不要奖励装饰——但这一点**没有实验验证**
- [推断] 自偏好：policy 与 judge 同家族时，至少加一个异族 judge 交叉；Pomms 式集成是目前唯一有报道的缓解

### Gaps
- 没有工作测过「exemplar 能否抵抗 FRAME 式视觉攻击」
- VLM 在**审美**任务上的自偏好定量数字：未找到
- 示例内部顺序（好图在前 / 在后的比例）对位置偏差的影响：ARR 未写示例构成，无法确认

---

## Q5 受控对照：纯文字 rubric vs rubric + 示例 vs 只给示例

### Takeaway
- **没有任何一篇工作在审美 / 设计数据上同时跑齐三组**（text-only rubric / rubric + exemplars / exemplars-only）。
- 能拼出的「部分对照」都指向同一结论
  - 示例相对纯 rubric：二元方向 +0 ~ +3 点（DesignPref），位置偏差与校准大幅改善（ARR、DesignPref 四档），批评质量 +0.13 ~ +0.20（UICrit）
  - rubric 相对无 rubric：+1.7 ~ +6.3 点（ARR）或无增益（WebDevJudge pairwise）
  - 只给「带分示例图」不给比较结构：无效甚至有害（Wu et al. IQA）
- 因此最稳妥的协议是 **rubric 定义维度 + 少量相似正反例对校准 + 强制选择 pairwise + 换序双跑**，并且要自己做三组消融。

### Cited Findings

**1. 可用的部分对照汇总**

| 研究 | 数据 / 模型 | 对照组 | 结果 | 缺的组 |
|---|---|---|---|---|
| DesignPref【一手】 | UI 偏好，20 名设计师；GPT-5 / Gemini-2.5-Pro / Qwen3-VL ×2 | rubric 零样本 vs 8-shot 检索示例（rubric 作 tie-breaker） | 二元 −0.1 ~ +2.9；四档 +3.0 ~ +24.2 | 无 rubric 的纯示例组；k 消融 |
| ARR【一手】 | HPDv3 T2I 偏好 14,400 对；Qwen3-VL-8B / GPT-5 / Gemini 3.1 Pro | base vs +rubric vs +rubric + 正反例 | 平均 67.2/72.4/76.6 → 70.2/76.1/78.3 → 85.0/88.8/90.8 | 纯示例组；示例数 |
| UICrit【一手】 | 移动 UI 批评；Gemini Pro Vision | 0-shot vs 随机 8-shot vs 相似 8-shot（准则始终在） | 0.24 → 0.31 → 0.44（区域级） | 去掉准则组 |
| Wu et al. IQA【一手】 | 照片 IQA；GPT-4V + 3 个开源 | standard vs in-context（带分示例图）vs CoT | in-context ≈ standard（单图）或明显更差（双图 / 多图） | 无 rubric 维度 |
| WebDevJudge【二手：前序笔记】 | 网页 654 例 | Direct vs rubric | pairwise 下「comparably」 | 示例组 |
| VL-ICL Bench【一手】 | 通用 ICL 任务 | 图像示例 vs 语义等价文字示例 | 文字示例 shot 曲线更陡更稳 | 审美任务 |
| Baldassini【一手】 | 通用 VQA / 分类 | 示例有图 vs 无图 vs 随机图 | VQA 只差 1.2–1.5 点 | 审美任务 |

- 来源：[DesignPref](https://arxiv.org/html/2511.20513v1)；[ARR](https://arxiv.org/html/2605.08354)；[UICrit](https://arxiv.org/html/2407.08850v3)；[Wu et al. 2403.10854](https://arxiv.org/abs/2403.10854)；[WebDevJudge](https://arxiv.org/html/2510.18560v2)；[VL-ICL Bench](https://arxiv.org/html/2403.13164v4)；[Baldassini](https://ar5iv.labs.arxiv.org/html/2404.15736)

**2. 文本 judge 的旁证（不是视觉，只作参考）**
- CheckEval：二元 checklist 让 judge 间 α 0.06–0.09 → 0.45–0.48，与人相关只 +0.03 ~ +0.18 — [arXiv HTML](https://arxiv.org/html/2403.18771)【二手：转引前序笔记】

### Inferences
- [推断] **三种成分各自的分工**（证据强度从强到弱）
  - pairwise + 强制选择 + 换序：决定「数字可不可信」（GenArena 0.36 → 0.86；WiserUI CA 揭示真实水平）
  - 正反例 exemplar：决定「位置偏差和打分尺度」（ARR Δ 30 → 9；DesignPref 四档 +3 ~ +24）
  - 文字 rubric：决定「看哪些维度、怎么写理由」（ARR +1.7 ~ +6.3；UICrit 准则作为底座）
  - 三者都**不能**突破人-人一致率天花板（设计类约 55–62%）
- [推断] **推荐协议（网页审美 judge）**
  - 输入
    - 专家 rubric：逐条二元可观察问句（前序笔记 `web_ui.md` Q5 的 R01–R20）
    - 示例：3–4 对（6–8 张图）正反例，每对附 1–2 句理由
      - 按视觉 + 任务联合相似度检索（UICrit 最佳；DesignPref 用 SBERT + UIClip 编码器）
      - A 胜 / B 胜各半，示例顺序随机
      - 优先选**人类高共识**的对子（标注方差低，同 Compare2Score 选锚点的原则）
    - 每张图交错标注「Image A: … Image B: …」
    - 截图 + 关键源码 / computed style（前序笔记：WebDevJudge 两者都给最好）
  - 判断：强制二选一；AB / BA 各跑一次，不一致记为平局或丢弃
  - 需要绝对分时：用 Compare2Score 式锚点（每档 1 张、共约 5 张低方差参考页），候选页与锚点逐一比较后聚合
  - 自检：报 CA 而不是单序准确率；按人类共识度分层报告
- [推断] **博客里该自己补的消融**（目前文献空白）
  - 同一 VLM、同一网页偏好集，四组：无 rubric 无示例 / 只 rubric / 只示例 / rubric + 示例
  - 再加两组拆示例成分：示例只有图无理由 / 只有理由无图
  - k = 0 / 2 / 4 / 8；随机选例 vs 相似选例
  - 指标：CA、正反序 Δ、与多数票的一致率、高共识子集上的一致率

### Gaps
- **核心空白**：审美 / 设计数据上「text-only rubric vs rubric + exemplars vs exemplars-only」的三组受控对照不存在
- 「示例的理由文字 vs 示例图本身」各贡献多少：在审美任务上无人拆分
- 示例跨分布（如照片 / T2I 示例 → 网页）是否还有效：ARR、DesignPref 都是同分布示例
- exemplar 作为 RL reward 时是否会被 policy 「模仿示例风格」刷分（模板塌缩）：无实验

