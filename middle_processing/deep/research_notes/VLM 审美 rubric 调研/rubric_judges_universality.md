# VLM 审美 judge：rubric 是否有用 × 人类审美有多少是共享的

> 范围：(1) 给 VLM 显式审美 rubric / checklist 是否提高与人类的一致性、rubric 怎么设计；(2) 人类审美的共享成分 vs 个人成分的科学证据。
> 服务对象：为代码生成视觉产物（网页 / 幻灯片 / 图表 / 3D / 短视频）设计审美 reward / verifier 的团队。
> 与项目已有笔记的关系：`notes/verifier_reward.md` 已有 DesignPref（二元一致 0.624、α=0.248）、UIClip（α=0.37）、RULER（Spearman 0.7929）、WebDevJudge（rubric 65%→92%）、UICrit（ICC≈0.02）、AUV-Bench、RaR（31.7/32.0/35.9）等数字。**本文不重复，只补新数字**；引用到它们时只写「（项目已有）」。
> 标记约定：[推断] = 本文作者推理；[未核实] = 只有二手来源或表格列对不齐；[本文计算] = 由引用数字换算。

---

## Q1. MLLM 图像审美 benchmark / 模型 / reward model：属性分类法与得分

### Takeaway
- 通用 MLLM 在「审美感知」选择题上约 72–75%，离资深人类（87%）差 12 个点以上；在「打绝对分」上只比随机高 15–20 个点。
- 专训模型（Q-Align）在 AVA 上 SRCC 0.822，是 LAION aesthetic predictor（0.721）之上一档；**用离散文字等级（excellent…bad）训练比直接回归分数在跨数据集上平均好约 10%**。
- 所有 T2I 偏好 reward model（ImageReward / PickScore / HPSv2/v3 / MPS）在**跨数据集**测试上都掉到 57–77%，说明它们学到的「审美」高度依赖数据集分布。

### Cited Findings

**1. 属性分类法（taxonomy）对照**
- AADB：10,000 张图，190 名 worker，**平均每图 5 人**；11 个属性 = interesting content, object emphasis, good lighting, color harmony, vivid color, shallow depth of field, motion blur, rule of thirds, balancing element, repetition, symmetry；外加 1–5 总分 — [PARA 论文 §2.1 对 AADB 的转述](https://arxiv.org/abs/2203.16754)
- PARA（CVPR 2022）：31,220 张图、438 名被试、**平均每图约 25 人**；每图 13 个标签 — [PARA](https://arxiv.org/abs/2203.16754)
  - 图像侧属性（1–5）：composition, light, color, depth of field, content；object emphasis 是二值
  - 人侧属性：emotion（8 类单选）、difficulty of judgement（−1/0/+1）、content preference（「I like the content of this photo」5 级同意度）、willingness to share
  - 总分 aesthetics score 1–5，**每两个整数之间加了半档**以应对模糊；另有 quality score
  - 质控：446 个 session，每个 = 70 张待标 + 5 张标准图 + **5 张重复图测自洽**
- AesBench（EAPD）：2,800 张图（自然 ≈1,246 / 艺术 ≈802 / AIGC ≈752）、8,400 QA、2,800 条解读，**32 名专业审美专家** — [AesBench](https://arxiv.org/abs/2401.08276)
  - 四层能力：Perception (AesP) / Empathy (AesE) / Assessment (AesA) / Interpretation (AesI)
  - AesP 维度：Technical quality, Color & light, Composition, Content
  - AesE 维度：Emotion, Interest, Uniqueness, Vibe
- UNIAA：感知题覆盖 Content & Theme, Composition, Color, Light, Focus, Sentiment 六属性；IDCP 把 AVA/AADB/ICAA17K/PARA/PCCD 的**属性与评论**（刻意不用原始分数，因为跨数据集分数无法统一）转成 278,181 条指令数据 — [UNIAA](https://arxiv.org/abs/2404.09619)
- VisionReward：图像 **5 维 / 18 子维 / 61 个二元问题**；视频 **9 维 / 20 子维 / 64 个二元问题** — [VisionReward](https://arxiv.org/abs/2412.21059)
- ArtiMuse：10K 张图，5 大类 / 15 子类，专家标注 **8 维属性分析 + 1 个整体分** — [ArtiMuse](https://arxiv.org/abs/2507.14533)

**2. MLLM 在审美 benchmark 上的分数**
- AesBench AesP（感知选择题）准确率：Q-Instruct 72.61%、GPT-4V 72.08%、Gemini Pro Vision 71.99%、Qwen-VL 63.21%、随机 35.02% — [AesBench](https://arxiv.org/html/2401.08276)
- AesBench AesA（打分档位选择）准确率：Q-Instruct 52.86%、GPT-4V 50.86%、Gemini 49.38%、Qwen-VL 46.25%、随机 33.33% — [AesBench](https://arxiv.org/html/2401.08276)
  - 论文只说「与人类仍有显著差距」，**没有报人类基线数字**
- UNIAA-QA 感知准确率 — [UNIAA](https://arxiv.org/html/2404.09619)
  - 资深人类 **87.39%**、初级人类 **79.01%**、UNIAA-LLaVA 78.48%、GPT-4V 74.74%（只算它没拒答的题）、最佳开源 mPLUG-Owl2 67.24%
  - 最难属性是 **Composition**：UNIAA-LLaVA 66.82%、GPT-4V 70.14%（其余属性 72–85%）
- UNIAA 零样本打分（5 个等级词 logits 加权，PLCC/SRCC）— [UNIAA](https://arxiv.org/html/2404.09619)
  - UNIAA-LLaVA：AVA 0.704/0.713（见过）、PARA 0.895/0.864（见过）、**TAD66K 0.425/0.411（未见过）**、Flickr-AES 0.751/0.724（未见过）
  - Q-Instruct：AVA 0.330/0.313
- Q-Align 在 AVA（官方划分训练）SRCC/PLCC — [Q-Align](https://arxiv.org/html/2312.17090)
  - Q-Align **0.822/0.817**；10% 数据 few-shot 0.776/0.775
  - VILA 0.774/0.774、LIQE 0.776/0.763、MLSP 0.756/0.757、**LAION Aesthetic Predictor 0.721/0.723**、MUSIQ 0.726/0.738、CLIP-IQA+ 0.619/0.586、NIMA 0.612/0.636
- Q-Align 消融「文字等级 vs 直接分数」（指标 = (SRCC+PLCC)/2）— [Q-Align](https://arxiv.org/html/2312.17090)
  - KonIQ 训练 → KADID 跨集：分数 0.524 vs 等级 0.679；SPAQ 训练 → KADID：0.485 vs 0.741
  - 跨数据集平均提升约 10%，最大 +29.6% / +52.8%
  - 推断方式：5 个 ITU 等级（excellent/good/fair/poor/bad → 5..1），只在这 5 个 token 上 softmax，分数 = Σ i·p(level i)
- ArtiMuse 在 ArtiMuse-10K 上 SRCC 0.614 — [Wizwand 榜单](https://www.wizwand.com/paper/68fa7a7d1e209131cea836d3) [未核实：第三方聚合，未与论文表格对上]

**3. T2I 偏好 reward model 的准确率（pairwise accuracy, %）**
- HPSv3 论文 Table 4（列 = ImageReward-test / Pick-a-Pic(PickScore)-test / HPDv2-test / HPDv3-test）— [HPSv3](https://arxiv.org/html/2508.03789)
  - CLIP ViT-H/14：57.1 / 60.8 / 65.1 / 48.6
  - **LAION Aesthetic Score Predictor：57.4 / 56.8 / 76.8 / 59.9**
  - ImageReward：65.1 / 61.1 / 74.0 / 58.6
  - PickScore：61.6 / 70.5 / 79.8 / 65.6
  - HPSv2：65.7 / 63.8 / 83.3 / 65.3
  - MPS：67.5 / 63.1 / 83.5 / 64.3
  - HPSv3：66.8 / 72.8 / 85.4 / 76.9
- HPDv3 规模：1.08M 图文对、1.17M 成对比较；每个决策由 **9–19 名专业标注员**验证 — [HPSv3](https://arxiv.org/html/2508.03789)
- HPDv2 规模：798,090 次选择 / 433,760 对 — [HPSv2](https://arxiv.org/abs/2306.09341)
- VisionReward（二元 checklist + 逻辑回归线性加权）— [VisionReward](https://arxiv.org/html/2412.21059v4)
  - 视频偏好准确率 72.1 vs VideoScore 54.9（即摘要里的「+17.2%」，实为百分点）
  - 用 VisionReward 训练的 T2V 模型 pairwise 胜率比用 VideoScore 训练的高 31.6%
  - **问题数越多准确率越高**（Fig.5）；mask 掉最小权重不掉点
  - 训练对数 200 → 77.6，4k → 81.3，8k 饱和
  - 图像侧与 HPSv2/MPS 的逐列对比 [未核实：抓取到的表头错位]

### Inferences
- [推断] 「感知题能答对」≠「能打分」：同一个 GPT-4V，AesP 72% 但 AesA 51%（随机 33%）。**审美 verifier 不应让 VLM 直接输出绝对分**，最多让它回答可判定的属性问题。
- [推断] Composition 是 MLLM 最弱的属性（UNIAA 两个模型都最低）。网页 / 幻灯片的审美主要就是构图与层级 → 这部分更该交给程序化几何判据（项目已有 L1 硬闸），而不是 VLM。
- [推断] LAION aesthetic predictor 在 HPDv2 上 76.8% 看似不错，但在 HPDv3 / ImageReward / Pick 上只有 57–60%，几乎是 CLIP 水平；**它不适合作为网页 / 图表审美的 reward**（分布完全不同）。
- [推断] 如果要训审美打分头，**用 Q-Align 式「离散等级 + 概率加权」**而不是回归分数：跨分布泛化是 verifier 最关键的性质，而这正是等级法优势最大的地方（+10% 平均，最大 +50%）。

### Gaps
- AesBench、AesExpert、AesMamba 的人类基线和完整 SRCC 表本轮未取到；AesExpert（AesMMIT）与 AesMamba 的具体数字**未检索到**。
- MPS（CVPR 2024）四维（aesthetics / semantic alignment / detail quality / overall）各维分别的准确率本轮未取到。
- 「Aesthetic Post-Training」（SPO 系列）的具体数字未检索。
- 没找到任何**直接面向网页 / 幻灯片 / 图表截图**的 MLLM 审美 SRCC benchmark（AesBench/UNIAA 都是照片 / 艺术 / AIGC 图）。

---

## Q2. rubric / checklist 是否让 VLM judge 更接近人类？pairwise vs 绝对分？偏差与刷分

### Takeaway
- **pairwise > pointwise 的证据最强、最一致**：同一 VLM 从打绝对分改成两两比，与人类排名的 Spearman 从 0.36 升到 0.86，自洽 α 提高 0.13–0.14。
- **rubric 有用但增益不大且不稳定**：自动生成的 per-prompt rubric 让前沿 VLM 的偏好准确率 +1.7~+6.3 点；二元 checklist 的主要收益是**评分者间一致性**（α 0.06–0.09 → 0.45–0.48），而不是与人的相关（多数只 +0.03~+0.18，个别还变差）。在**设计师标注的平面设计**上，给 criterion 的提示几乎零收益（−0.003）。
- **参考样例（reference exemplars）是被低估的杠杆**：在 rubric 外加人类挑选的正 / 反样例，把 pairwise position bias 从约 30 点降到约 9 点，平均准确率再 +4~+12 点。
- **VLM judge 很容易被视觉手段刷分**：加边框、黑边、把指令文字叠到图上，能让 GPT-4o 的分数 +80%；「请忽略这些偏差」类提示只能减轻，无法消除。

### Cited Findings

**1. pairwise vs pointwise vs batch ranking**
- MLLM-as-a-Judge（ICML 2024），各数据集平均 — [MLLM-as-a-Judge](https://arxiv.org/html/2402.04788v3)
  - Scoring（Pearson）：GPT-4V **0.490**、Gemini 0.304、LLaVA-1.5-13b 0.225
  - Pair（准确率）：GPT-4V 带 tie **0.636**、不带 tie **0.773**；Gemini 0.509 / 0.615
  - Batch ranking（归一化 Levenshtein，越低越好）：GPT-4V 0.361、Gemini 0.432
  - 6 次重复的自洽（MCC）：Scoring 0.611、Pair 0.675、Batch 0.418（GPT-4V）
  - **多步 CoT 反而变差**：GPT-4V Scoring 0.557 → 0.299（3-step CoT）；Gemini 0.299 → 0.144
  - **长度偏差**：内容不变只加长，GPT-4V 分数 +0.6、Gemini +0.75
  - 去掉图像（只给文字）：GPT-4V Scoring 0.490 → 0.299（不同表格设定，仅作量级参考）
  - LLaVA 在 batch 任务里 **88.2%** 原样复制提示里的「ABCD」顺序（位置偏差的极端形态）
  - 自偏好（egocentric）：只给定性描述（GPT-4V「轻微」），**无数字**
- GenArena（视觉生成 judge）— [GenArena](https://arxiv.org/html/2602.06013)
  - 与 LMArena 人类排名的 Spearman（GEdit-Bench-EN）：**pointwise 0.36 → pairwise Elo 0.86**
  - Qwen3-VL-8B pointwise → pairwise 准确率：GenAI-Bench 49.1% → 60.5%；EditScore-Bench 58.3% → 83.7%；VideoGen-RewardBench 57.0% → 61.5% [列对齐有歧义，按正文数字]
  - 5 次运行的自洽 Krippendorff α，pointwise → pairwise：0.7256 → 0.8628；0.5753 → 0.7087；0.5707 → 0.7040；0.5169 → 0.6553
  - **允许 tie 是坏事**：人类强偏好（A≫B）的对子里，允许 tie 的 judge 有 37.9% / 39.2% 选了 tie；在可区分对子上，允许 tie 54.9% vs 强制二选一 83.9%（+29.0）
  - judge 规模：4B 60.9% → 8B 63.6% → 32B 67.6%
  - 失败例：pointwise 把 Nano Banana 在 GEdit-EN 排第 4，LMArena 排第 1

**2. rubric / checklist 的效果**
- Auto-Rubric as Reward（ARR，每个 prompt 自动生成 K=5 条 rubric）偏好准确率 % — [ARR](https://arxiv.org/html/2605.08354)
  - HPDv3：Qwen3-VL-8B 67.2 → 70.2；GPT-5 72.4 → 76.1；Gemini 3.1 Pro 76.6 → **78.3**（超过专训 HPSv3 的 76.9）
  - MM-RB2 (T2I)：GPT-5 70.5 → 74.7；Gemini 75.1 → 78.9
  - 总增益区间 **+1.7 ~ +6.3 点**；K 从 1 到 5 的收益「modest but non-negligible」
  - 当 RL reward（FLUX.1-dev）：GenEval 0.66 → 0.80；judge 越强增益越大（Qwen 0.74 / GPT-5 0.78 / Gemini 0.80）
  - 只声称「降低 reward hacking 风险」，**没有专门的 hacking 实验**；且论文 §3.2 与 §3.3 对 rubric 是否逐例重生成的描述自相矛盾
- **参考样例（w/ guide）对位置偏差的效果**，HPDv3 正序 / 反序准确率（Δ = 差值）— [ARR Table 5](https://arxiv.org/html/2605.08354)
  - Qwen3-VL-8B：84.5 / 49.9（Δ34.6）→ +ARR 86.0 / 54.4（Δ31.6）→ **+ARR w/ guide 90.1 / 79.8（Δ10.3）**
  - GPT-5：88.7 / 56.1（Δ32.6）→ 90.2 / 62.0（Δ28.2）→ **93.4 / 84.1（Δ9.3）**
  - Gemini 3.1 Pro：91.7 / 61.5（Δ30.2）→ 92.2 / 64.4（Δ27.8）→ **95.2 / 86.3（Δ8.9）**
  - guide = 来自同数据集 held-out 训练划分的（prompt, 好图, 差图, 理由）in-context 样例
- CheckEval（文本任务，二元 yes/no checklist vs G-Eval 式 Likert）— [CheckEval](https://arxiv.org/html/2403.18771)
  - 评分者间一致性（12 个 judge 模型之间，Krippendorff α）：SummEval **0.09 → 0.48**；Topical-Chat **0.06 → 0.45**；只看大模型可到 0.67
  - 与人的相关（Spearman ρ）：GPT-4o SummEval 0.32 → 0.50；Mistral-Large 0.52 → 0.55；Llama3.1-70B 0.40 → 0.46；**Mistral-Small Topical-Chat 0.58 → 0.47（变差）**
  - checklist 规模：**每个维度约 25–28 个问题**
  - 生成流程：人定维度 / 子维度（不许 LLM 定）→ 人写种子问题 → GPT-4o 扩写（diversify + elaborate）→ GPT-4o 过滤冗余
  - 摘要说「agreement 平均 +0.45」与表格平均对不上，谨慎引用
- TASTE（设计师标注的 AI 平面设计偏好，UI + 广告）— [TASTE](https://arxiv.org/html/2605.20731)
  - criterion-conditioned prompt（告诉模型按哪条审美维度判）：标量头 0.580 vs 基线 0.583（**−0.003**）；加到 pairwise 头上 0.586 vs 单 pairwise 头 0.611（**变差**）
  - criterion 前缀数据增强：验证准确率变化 < 0.01
- 「Can GPTs Evaluate Graphic Design Based on Design Principles?」（SIGGRAPH Asia 2024）— [Haraguchi et al.](https://arxiv.org/html/2410.08885)
  - 设定：GPT-4o，prompt 内含按 O'Donovan 2014 改写的 alignment / overlap / white space 原则描述 + 分数锚点（完美 10、平庸 7、明显缺陷 4、很差 1–2）
  - 结果：与 60 名众包评分者的均值相关高于启发式指标，**扰动越大相关越高**；小扰动（对齐、留白）上 pairwise 不如启发式
  - 规模：700 样本（100 原图 + 600 合成扰动），每图 5 人；temperature 1，绝对分 5 次平均、pairwise 5 次多数票
  - 具体 r 值只在图里，文字未给
- VisionReward：二元问题的数量与准确率正相关（见 Q1）— [VisionReward](https://arxiv.org/html/2412.21059v4)
- Prometheus-Vision：Perception Collection 含 **15K 条定制 score rubric**；「开源模型中与人类及 GPT-4V 的 Pearson 最高」，摘要未给数字 — [Prometheus-Vision](https://arxiv.org/abs/2401.06591)
- RLCF（Checklists Are Better Than Reward Models，Qwen2.5-7B-Instruct）：FollowBench hard satisfaction **+4**、InFoBench **+6**、Arena-Hard 胜率 **+3**；「唯一在所有 benchmark 上都提升的方法」；每条 checklist 由 AI judge + 专门的 verifier 程序打分后合成 reward — [RLCF](https://arxiv.org/abs/2507.18624)
- HealthBench：5,000 段对话、262 名医生写 rubric、**48,562 条不重复 criteria** — [HealthBench](https://arxiv.org/abs/2505.08775)
  - [本文计算] 平均每段对话约 9.7 条 criteria
  - GPT-4.1 作 grader 与医生的 macro F1 = **0.709**，与医生之间的一致程度相当；但医生分歧本身构成结构性天花板，部分来自 criteria 措辞歧义 — [二手：arXiv 2602.22758](https://arxiv.org/abs/2602.22758)

**3. 位置偏差 / 自偏好**
- 基础 VLM 的 pairwise 正反序差 Δ 约 **30–35 个点**（Qwen3-VL-8B / GPT-5 / Gemini 3.1 Pro 均如此，「severe and scale-invariant」）— [ARR](https://arxiv.org/html/2605.08354)
- TASTE 的 position-bias rate（定义：翻转图像顺序后判决不变的比例）：Qwen3-VL-4B 0.775、8B 0.679、32B 0.463、Gemma-3-27B 0.439、Kimi-VL-A3B 0.868、InternVL3.5-14B 0.551；按 criterion 范围 0.315–0.927；该指标与 conditional accuracy 的 Spearman ρ = +0.94 — [TASTE](https://arxiv.org/html/2605.20731) [未核实：抓取文本对「判决不变」指位置还是指选中的图有歧义，引用前需看原文定义]
- 文本 LLM judge 的系统研究：15 个 judge、22 个任务、15 万+ 评测实例；位置偏差**强烈依赖两个候选的质量差**（质量越接近越严重），与 prompt 长度关系弱 — [Shi et al. 2024](https://arxiv.org/abs/2406.07791)
- 其它报告的数字：移动端 App benchmark 23.3% 位置偏差需要 swap 重跑；WebDevJudge 显式指令后仍有约 5% — [检索摘要汇总](https://www.emergentmind.com/topics/vlm-as-a-judge) [未核实：二手汇总]

**4. 刷分（reward hacking）**
- 视觉偏差刷 VLM judge（FRAME benchmark，T2I 打分）— [Fooling the LVLM Judges](https://arxiv.org/html/2505.15249v2)
  - 手段：brightness / gamma、叠加文字（「Reference Image」、prompt 关键词、完整指令）、黑边 padding、bounding box、美颜滤镜
  - 单域最大涨幅：**GPT-4o +80.2%**（bbox，1.14 → 2.05）、GPT-4o-mini +41.4%、GPT-4.1 +18.0%、GPT-4.1-mini +17.1%、o3 +16.6%、Qwen2.5-VL-32B +12.6%、LLaVA-1.5-13B +109.6%
  - 偏差叠加会放大：GPT-4.1-mini Indoor 单一 +17.1% → 三重 +23.3%
  - pairwise 同样受影响，在 4 个域里把基线排名翻转
  - **提示缓解（GPT-4.1-mini）**：「给出偏差定义」最有效（padding +10.4% → +5.6%；brightness +5.9% → +0.8%），但**都没清零**；「bias-aware」提示几乎无效；**CoT 反而让 bbox 从 −1.0% 变成 +4.1%**
- LAION aesthetic predictor 被 RL 优化后 — [DDPO / BAIR blog](https://bair.berkeley.edu/blog/2023/07/14/ddpo)
  - 输出趋向「minimalist black-and-white line drawings」
  - 「in all the tasks, the model eventually destroys any meaningful image content to maximize reward」
  - 「There is currently no general-purpose method for preventing overoptimization」
  - VLM（LLaVA）reward 被 typographic attack 骗：画出「像数字的文字」来通过计数题
- DRaFT：微调后多样性丧失，**塌缩到生成某一张高 reward 图** — [DRaFT](https://arxiv.org/abs/2309.17400)；DRaFT / ReFL 常过优化出「over-detailed、带高频噪声」的图；加大 KL 权重 β 可缓解 — [PRDP](https://arxiv.org/abs/2402.08714)
- HPSv3：开源 CLIP+MLP 审美模型「strong preference for oil painting」；用 HPSv2 当 DanceGRPO reward 时，模型开始**加无意义的配饰和 prompt 没提的物体**（作者明确称为 reward hacking），HPSv3 明显减轻 — [HPSv3 附录](https://arxiv.org/html/2508.03789)

### Inferences
- [推断] **形式选择**：主信号用 **组内 pairwise、强制二选一、AB/BA 双向**；不要 pointwise 绝对分、不要允许 tie。这与项目 L4 设计一致，GenArena 的 0.36 vs 0.86 是目前最直接的量化支持。
- [推断] **rubric 的真实价值是「降噪」而不是「对齐」**：CheckEval α 提高 0.4，但相关只提高几个百分点；ARR 只 +2~6 点。所以 rubric 适合放在「需要稳定、可复现」的位置（硬闸、诊断），不要指望它把 VLM 拉到人类水平。
- [推断] **二元 > Likert**：证据链 = CheckEval（二元 α 0.45 vs Likert 0.06–0.09）+ Q-Align（离散等级 > 连续分数）+ GenArena（强制选择 > tie）+ DesignPref（项目已有：4 档 α 0.104 < 二元 0.248）。四条独立证据同向。
- [推断] **条目数量**：已知工作点 = ARR 每 prompt 5 条、HealthBench 每例约 10 条、CheckEval 每维 25–28 条、VisionReward 每模态 61–64 条（配线性权重）。建议：
  - 每例实例级 rubric 5–10 条（让 VLM 逐条二元判）
  - 全局固定 checklist 可到几十条，但**必须用人类偏好数据学权重**（VisionReward 式逻辑回归），不能等权或按「重要性」拍权重（项目已有：按有用性加权比不做还差）
- [推断] **参考样例要用**，但用法有讲究：
  - 用来**生成 rubric**（项目已有 RaR：带参考 rubric 35.9 > 无参考 32.0 > 参考-Likert 31.7）
  - 或作为**in-context 正反例对**稳住位置偏差（ARR：Δ 30 → 9）
  - 风险：ARR 的 guide 来自同分布训练集，跨分布（换到网页 / 幻灯片）效果未验证
- [推断] **CoT 不是免费的**：MLLM-as-a-Judge（Scoring 0.557 → 0.299）和 FRAME（CoT 放大 bbox 偏差）两条独立证据都显示「让 judge 多想几步」可能变差。rubric 应该是「逐条短答」，不是「长推理后给总分」。
- [推断] **代码生成产物的特有刷分面**：FRAME 里最有效的攻击（叠加指令文字、加边框、黑边）在 HTML/CSS 里成本几乎为零（一个 `border`、一段文字）。所以：
  - judge 输入必须同时给源码（项目已有 WebDevJudge 消融支持）
  - 必须有程序化负向闸：检测「把 prompt 原文渲染成大标题」「全局描边 / outline」等
  - 项目已有的「RULER 换成整体美学分 → 堆叠描边与重复装饰」与 FRAME 的 bbox 攻击是同一类现象
- [推断] **自偏好**：VLM 场景缺数字。若 judge 与 policy 同家族，至少要用异族 judge 做交叉校验。

### Gaps
- **没有找到任何针对「审美」的受控 A/B：同一 VLM、同一数据，rubric 分解 vs 单一整体分，报 SRCC 或 pairwise 准确率**。最接近的是 ARR（偏好，含语义对齐）、TASTE（criterion 提示无效）、Haraguchi（只有 rubric 条件，无整体分对照）。这是本问题最关键的空白。
- VLM judge 自偏好（self-preference）的定量数字：未找到可靠来源。
- OpenPipe RULER（相对打分）的独立人类一致性数字：本轮未检索；项目里的 RULER 0.7929 来自另一工作，未确认是否同一个东西。
- 「优化 LAION aesthetic → 过饱和」这一具体说法：本轮来源只说「黑白线稿」「破坏内容」「高频噪声」「塌缩」，**没有找到「oversaturated」的一手描述**。
- Rubrics as Rewards（Gunjal et al. 2025）原文数字本轮未复核，沿用项目已有。
- Shi et al. 位置偏差的具体 position consistency 数字未取到（只有摘要）。

---

## Q3. 人类审美有多少是共享的？（普遍性 vs 主观性）

### Takeaway
- **共享成分真实存在且可观，但随领域单调下降**：自然场景 / 风景 > 面孔 > 建筑 / 艺术品 / 抽象图。个体与「其他人平均」的相关（taste typicality / MM1）在日常场景上约 0.66，风景约 0.60；私人口味占方差的比例在面孔上约 40–50%，在抽象艺术上约 75%。
- **群体均值是高度可预测的，个体不是**：纯视觉 DNN 线性读出能解释群体均值 53%（最好 72%）的可解释方差；同一套模型预测个人时，个性化 100-shot 只多约 0.014 SROCC（PARA）。
- **很多「普适审美规律」其实是平均出来的**：复杂度的倒 U 曲线是两类相反偏好人群平均的产物；黄金比例没有群体规范性；颜色偏好的平均值可被生态价值理论解释 80%，但「喜欢 / 不喜欢」跨文化差异最大。
- 网页首印象有稳定的共享规律：**低视觉复杂度 + 高原型性**最受欢迎，判断在 50 ms 内形成；复杂度 + 色彩度模型（加人口学变量）可解释约一半方差。

### Cited Findings

**1. 共享 vs 私人口味的直接测量**
- Hönekopp 2006：31 人给 77 张面孔打 1–7 分，一周后重测；用「自身重测一致 vs 与他人一致」拆分 → **private taste ≈ shared taste，约各占一半**；并指出单次 Cronbach α 会**高估**共享程度 — [APA Monitor 报道](https://www.apa.org/monitor/may06/beauty)；[论文页](https://researchportal.northumbria.ac.uk/en/publications/once-more-is-beauty-in-the-eye-of-the-beholder-relative-contribut/)
- Leder et al. 2016（同法）：私人口味比例 **面孔 40%**、**抽象艺术 75%** — [Private and Shared Taste in Art and Face Appreciation](https://www.frontiersin.org/articles/10.3389/fnhum.2016.00155/full)
- Vessel et al. 2018（Cognition 179:121–131）：面孔、风景高度共享；建筑、艺术品个体差异强；实验 2 被试内比较风景 vs 外部建筑：**风景一致性显著更高，而两者的重测可靠性没有差别**（即差异不是噪声造成的）— [MPG 新闻稿](https://www.aesthetics.mpg.de/en/newsroom/news/news-article/article/beautiful-nature-controversial-art.html)
  - 风景静图 **MM1 = 0.60（95% CI 0.53–0.66）**（Isik & Vessel 2021 引述）— [Isik & Vessel 2021](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.676032/full)
  - 同文：风景视频整体评分 MM1 = 0.40（0.31–0.48），连续评分 MM1c = 0.61（0.52–0.69）
  - 面孔约 0.84、抽象艺术低至 0.28 等数字 [未核实：仅见于二手综述的检索摘要]
- Chen et al. 2022（Current Biology）「taste typicality」：200 人（100 主实验 + 100 复制），88 张日常场景图 + 88 段环境声，1–6 分 — [Chen et al. 2022](https://ycc.vision/files/papers/Chen_etal_2022_CB_crossmodelTasteTypicality.pdf)
  - 视觉 taste typicality（个体 z 分与其他人均值的相关）：**M = 0.664，范围 0.315–0.839**；复制实验 M = 0.663
  - 个体重测可靠性：图像 **0.856**
  - **没有任何人与平均口味负相关**
  - 视觉与听觉 typicality 相关 r_corrected = 0.367 / 0.518 → 存在跨模态的「一般性口味典型度」
- Bignardi et al. 2024（双生子）：遗传解释 taste typicality 与评价偏置方差的 26–41%；抽象图的 typicality 只有环境影响；个体间偏好**抽象图最不相似、面孔居中、场景最相似** — [Communications Biology](https://www.nature.com/articles/s42003-023-05710-4)

**2. 群体均值 vs 个体的可预测性**
- Graham, Conwell, Boccagno, Vessel（CCN 2024）：180 个只做过视觉任务的 DNN，线性读出预测 beauty / arousal / valence — [Affectless Visual Machines](https://2024.ccneuro.org/pdf/524_Paper_authored_DeepAesthetics_CCN2024.pdf)
  - 平均解释群体均值 **53%** 的可解释方差，最好 **72%**
  - 平均模型对群体均值的预测力 ≈ **最「典型」的 32.5% 被试**
  - 两种天花板要分开：MM1（个体 vs 其余人均值）是「共享口味」上限；split-half 是「预测群体均值」的噪声上限
  - Vessel 数据集里：场景 / 风景最可预测，人物和艺术最难
- PARA 基准（同一 backbone 家族）— [PARA](https://arxiv.org/abs/2203.16754)
  - 预测群体均值（GIAA）SROCC：ResNet-50 **0.879**、MobileNet-V2 0.871、ResNet-18 0.854
  - 预测个人（PIAA）SROCC：ResNet-50 不微调 **0.681** → 10-shot 0.681 → 100-shot **0.695**；Swin-T 0.686 → 0.699
  - 高分区间 (4,5] 的分数方差明显更低 → 「对什么是美有共同认知」；1–4 分区间分歧更大
- Iigaya et al. 2021（Nature Human Behaviour）：1,500+ MTurk 被试评印象派 / 立体派 / 抽象 / 色域画；**一个共享的、可解释的低层 + 高层特征回归模型可同时在个体内和个体间预测评分**；作者称与语义、个人经历相关的特异成分不跨个体泛化 — [Caltech 记录](https://authors.library.caltech.edu/109241/)；[ScienceDaily](https://sciencedaily.com/releases/2021/06/210616143236.htm)
- AVA：25 万+ 张图，每图 **78–549 票、平均 210 票** — [Jin et al. 2017 对 AVA 的统计](https://arxiv.org/abs/1708.07089)；[Murray et al. CVPR 2012](https://mlanthology.org/cvpr/2012/murray2012cvpr-ava)
- 两个人之间的 pairwise 一致率（T2I 生成图）：HPDv2 单人 vs 单人 **78.1%**，单人 vs 平均 85.0%；ImageReward 测试集单人 vs 单人 **65.3%**，单人 vs 平均 53.9% — [HPSv2 Table 6](https://arxiv.org/html/2306.09341)
- 标注「收敛率」：HPDv2 59.9%、HPDv3 76.5% — [HPSv3](https://arxiv.org/html/2508.03789)

**3. 经典「普适规律」的现状**
- 复杂度倒 U（Berlyne 传统）：30 名被试、数字生成灰度图；**倒 U 是平均的产物**——聚类后一组人越复杂越不喜欢，另一组越复杂越喜欢；作者原话是「跨被试平均会制造高一致的假象」— [Güçlütürk et al. 2016](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00112/full)
- 颜色偏好：Palmer & Schloss 生态价值理论（WAVE）解释美国成年人**平均**颜色偏好方差的 **80%**；Taylor & Franklin 2012 复测只有 **61%** — [SPIE 2010](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/7527/752718/Human-preference-for-individual-colors/10.1117/12.849110.full)；[Frontiers 2022 复述](https://www.frontiersin.org/articles/10.3389/fpsyg.2022.1010108/full)；[PNAS 原文](https://palmerlab.berkeley.edu/pdf/Palmer%26Schloss%282010%29.pdf)
- 色彩和谐：Ou & Luo 2006 用 1,431 个双色组合、10 档量表，得到「一般性的双色和谐模式」并建立定量模型，独立数据集验证「满意」— [Color Res. Appl.](https://zendy.io/title/10.1002/col.20208)
  - 跨文化（英国、台湾、法国、德国、西班牙、瑞典、阿根廷、伊朗）：warm/cool、heavy/light、active/passive 较稳定（反应层）；**like/dislike 有文化差异**，也受性别、设计背景、年龄影响 — [Ou et al. 2012](https://research.chalmers.se/en/publication/154421)
- 黄金比例：群体对黄金矩形的偏好**很弱**；个体偏好函数强且跨时间稳定，但**人与人差异极大**；分两类（偏近正方形 / 偏细长）；与大五人格等个体差异变量都不相关 — [McManus, Cook & Hunt 2010, PACA, doi 10.1037/a0017316](https://pubpeer.com/publications/EBCD4B31EC80AC07FF8A5B70FD7066)；综述结论「一个世纪的实验表明它几乎没有规范作用」— [Frontiers 2016](https://www.frontiersin.org/articles/10.3389/fnhum.2016.00350/full)
- 网页首印象：
  - Tuch et al. 2012（IJHCS）：119 张真实网页截图，**低视觉复杂度 + 高原型性最受欢迎**；判断在 50 ms 内形成；17–33 ms 时复杂度效应强于原型性（复杂度更早加工）；复杂度高时即便很「典型」也被认为不美 — [Google Research](https://research.google/pubs/pub38315/)；[Google 博客](https://research.google/blog/users-love-simple-and-familiar-designs-why-websites-need-to-make-a-great-first-impression/)
  - Reinecke et al. 2013（CHI）：450 个网站、548 名志愿者；复杂度与色彩度计算模型 + 年龄 / 教育等人口学变量，解释 500 ms 曝光下审美吸引力**约一半方差**；复杂度比色彩度更重要 — [Reinecke et al. 2013](https://www.eecs.harvard.edu/~kgajos/papers/2013/reinecke13predicting.shtml)

### Inferences
- [推断] **审美 verifier 的目标应是「群体均值」而不是「某个人」**：
  - 群体均值可预测性高（DNN 解释 53–72% 可解释方差；PARA GIAA SROCC 0.88）
  - 个人部分几乎学不动（PARA 100-shot 个性化只 +0.014 SROCC；项目已有：DesignPref 个性化只 +2.7 点）
- [推断] **代码生成产物落在光谱的「人造物」一端**（网页、幻灯片 ≈ 设计 / 建筑类）。按 Vessel 与 Leder 的领域梯度，**应预期共享成分低于照片和风景**，接近建筑 / 艺术。与项目已有 DesignPref α=0.248、UIClip α=0.37 一致。
- [推断] **可共享的部分集中在「流畅性」类低层属性**：低复杂度、高原型性、对比 / 对齐 / 层级清晰。这些正适合程序化判据。分歧大的是风格取向（极简 vs 繁复、配色喜好）——倒 U 分解和颜色偏好的文化差异都指向这里。
- [推断] **对「平均人」的单 reward 必然会把风格推向众数**（低复杂度、典型布局）。Tuch 的「原型性」正是这个机制。这与项目里关注的「模板塌缩 / AI 味」是同一件事的两面：共享审美 = 原型 = 同质化。
- [推断] 天花板的直观换算：若 verifier 完美预测群体均值，它与**单个人**的相关最多约等于 taste typicality（日常场景 ≈ 0.66，风景 ≈ 0.60，人造物更低）。

### Gaps
- Vessel 2018 面孔 / 建筑 / 艺术品的 MM1 精确值：原文付费墙，二手数字不一致，**未核实**。
- Reber, Schwarz & Winkielman 2004（PSPR，processing fluency）、Leder et al. 2004（审美体验阶段模型）、Berlyne 1971：本轮**未取到一手原文**，只能作为理论背景提及，不能引具体数字。
- Lindgaard et al. 2006「50 ms 形成网页印象」及其重测相关：本轮未检索。
- Reinecke & Gajos 2014（全球约 4 万人、跨国网页偏好差异）的具体数字未检索。
- AVA 的逐人一致性指标（如 rater 间 Spearman）：AVA 只给分布，不公开 rater ID，本轮未找到。
- 没有找到在**网页 / 幻灯片 / 图表**上直接测 private vs shared taste（Hönekopp 法）的研究。

---

## Q4. DesignPref 及类似 UI / 设计偏好数据集：设计师之间一致性与 verifier 天花板

### Takeaway
- 新增证据（TASTE，2026）与项目已有的 DesignPref 同向：**职业设计师对 AI 生成平面设计的排序一致性极低**（Krippendorff α ≈ 0.19，pair-τ 0.10–0.22），而所有开源 VLM 和 T2I reward model 与设计师多数票的一致率只有 **0.50–0.54（随机 0.50）**。
- 可用的天花板经验值：在设计 / UI 类产物上，**单人 vs 单人 pairwise 一致约 55–62%**；在通用 T2I 图像上约 65–78%；资深 vs 初级人类在审美感知题上差约 8 个点（87% vs 79%）。

### Cited Findings
- TASTE（AI 生成 UI + 广告平面设计）— [TASTE](https://arxiv.org/html/2605.20731)
  - 规模：4 个生成器（FLUX.2 max、GPT Image 1.5、Nano Banana 2、Seedream 5.0 Lite）、10 名设计师（两组各 5 人）、9 个子维度（Aesthetics 5 个 + Descriptions 4 个）、每维 80 prompt × 5 人 × 4 图 = 1,600 个评分
  - 一致性：排序 **α ≈ 0.19**；幻觉标记 α 0.141 / 0.165
  - 各维平均 pair-τ（Aesthetics 组）：UI+Ad 整体偏好 0.159、Mood & Tone 0.147、Visual Hierarchy 0.128、Typography 0.119、**Color Harmony 0.103（最低）**
  - Descriptions 组：整体偏好 0.163、色彩准确 0.144、空间准确 0.182、Typography 0.224
  - 参照：Sushi 偏好 0.144、MovieLens 0.216、**HPSv2 测试集 top-4 0.302**
  - 所有维度都在 p < 10⁻¹⁰ 下显著高于随机 → 一致性低但不是零
  - 模型与设计师多数票的宏平均一致率（随机 0.50）：Qwen3-VL-4B / 8B / 32B = 0.530 / 0.539 / 0.536；Gemma-3-27B 0.528；InternVL3.5-14B 0.525；Kimi-VL-A3B 0.509；**HPSv2.1 0.543**；PickScore 0.522；**LAION-Aesthetic-V2 0.499**
  - 按维度看 VLM 最好的是整体审美偏好（Qwen3-VL-32B 0.593），**Visual Hierarchy 上全部模型 ≈ 0.48–0.55**
  - LoRA 微调编码器 0.528 反而低于冻结 + MLP 基线 0.583；pairwise 头 0.611 是最好设定
- UNIAA 人类基线：资深 87.39% vs 初级 79.01%（审美感知选择题）— [UNIAA](https://arxiv.org/html/2404.09619)
- Haraguchi 2024：60 名众包者对平面设计（对齐 / 重叠 / 留白）评分，GPT-4o 的评分标准差**低于人类**；小扰动上 GPT 判不出 — [Haraguchi et al.](https://arxiv.org/html/2410.08885)
- HPSv2 人类基线：单人 vs 单人 78.1%（HPDv2）/ 65.3%（ImageReward 测试集）— [HPSv2](https://arxiv.org/html/2306.09341)
- Reinecke 2013：人口学变量（年龄、教育）进入网页审美吸引力模型 → 网页偏好有可测的群体差异 — [Reinecke et al. 2013](https://www.eecs.harvard.edu/~kgajos/papers/2013/reinecke13predicting.shtml)
- 项目已有（不重复列数）：DesignPref（20 名设计师 × 600 对，二元一致 0.624，α 0.248，4 档 α 0.104，个性化 +2.7 点）、UIClip α 0.37、UICrit ICC ≈ 0.02、AUV-Bench（绝对分 2.78–3.18/5 而 pairwise 胜率近 80%）、WebDevJudge 人类 pairwise 84.56%、Human Creativity Benchmark（收敛在技术正确与视觉层级，分歧在审美方向）— 见 `notes/verifier_reward.md` §7.10

### Inferences
- [本文计算] Kendall τ 换算成 pairwise 一致率（无 tie 时 P(一致) = (1+τ)/2）：
  - TASTE 色彩和谐 τ 0.103 → **约 55%**；整体偏好 0.159 → 约 58%；Typography 0.224 → 约 61%
  - HPSv2 top-4 τ 0.302 → 约 65%
  - 与 DesignPref 二元一致 0.624（项目已有）同一量级 → **设计类产物的人-人 pairwise 天花板约 55–62%**
- [推断] **verifier 与单个设计师的一致率不可能显著超过人-人一致率**；更合理的目标是预测「多数票」。按 HPSv2 的结构（单人 vs 单人 78.1，单人 vs 平均 85.0），预测多数票能比单人 vs 单人高约 7 个点——但只在人群确实有共识的对子上成立。
- [推断] **应把评测集按「人类共识度」分层**：
  - 高共识对子（质量差大、技术缺陷明显）→ 用来当 verifier 的硬指标，目标 ≥ 80–85%
  - 低共识对子（风格取向）→ 只报不考核，因为任何模型在上面都只能 ≈ 随机（TASTE：0.50–0.54）
  - 依据：位置偏差和人类分歧都随质量差减小而加剧（Shi et al.；项目已有：DesignPref 28.5% 的对子分歧率 ≥ 96%）
- [推断] **哪些维度能做 rubric**：TASTE 里 Typography、空间准确、整体偏好 τ 相对高；**Color Harmony 最低**、Visual Hierarchy 的模型一致率 ≈ 随机。所以：
  - 文字排版、空间 / 对齐 → 可做二元 rubric 或程序化闸
  - 配色和谐 → 人自己都不一致，不要放进 reward，至多做「明显冲突」的负向闸
  - 视觉层级 → 人有一定共识但 VLM 判不出 → 交给 DOM / computed style 几何判据
- [推断] **设计决策速查**（汇总 Q1–Q4）：

  | 决策 | 建议 | 主要依据 |
  |---|---|---|
  | rubric vs 整体分 vs pairwise | 主信号 = 组内 pairwise（强制选择、AB/BA）；rubric 用于降噪和诊断；不用 pointwise 绝对分 | GenArena 0.36→0.86；AesA 51%；ARR +2~6 点 |
  | 条目数 | 实例级 5–10 条；全局 checklist 可几十条但须用偏好数据学权重 | ARR K=5；HealthBench ≈9.7/例；VisionReward 61 题 + 逻辑回归 |
  | 二元 vs Likert | 二元（或 Q-Align 式离散等级 + 概率加权，用于训练打分头） | CheckEval α 0.06→0.45；Q-Align 跨集 +10%；DesignPref 4 档 α 0.104 |
  | 参考样例 | 用：生成 rubric + 作 in-context 正反例对；注意跨分布未验证 | ARR Δ 30→9；RaR 35.9 vs 32.0 |
  | CoT | 逐条短答，不要长推理后给总分 | MLLM-as-a-Judge 0.557→0.299；FRAME CoT 放大偏差 |
  | 防刷分 | 源码 + 截图双输入；程序化负向闸（叠文字、全局描边、黑边）；KL 约束 | FRAME GPT-4o +80%；DDPO / DRaFT 塌缩 |
  | 一致率天花板 | 设计类单人-单人 pairwise ≈ 55–62%；通用图像 65–78%；只在高共识子集上考核 | TASTE τ 换算；DesignPref；HPSv2 |

### Gaps
- 幻灯片、图表、3D 渲染、短视频的**设计师 / 专家间一致性**：本轮没有找到专门数据集（TASTE 是平面设计，DesignPref 是 UI）。图表与幻灯片美观度的人-人一致性是空白。
- TASTE 的 position-bias rate 定义方向（见 Q2 Gaps）需看原文确认。
- 没找到「把评测集按人类共识度分层后，VLM / reward model 在高共识子集上准确率是多少」的公开报告——这正是判断 verifier 是否「到顶」所需的数字。

