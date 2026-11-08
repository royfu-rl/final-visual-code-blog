## 3 Verifier

Verifier 评估 Agent 在 Harness 里完成用户的多模态参考请求（Omni Reference Query）后交付的脚本或页面质量。

- 用于蒸馏轨迹质量评估，或 RL 训练过程的 reward function。
- 和 Web 最大的不同在真值：**3D 的真值是场景图，可直接读出；固定随机源、同一容器重渲时噪声为零。**

### 3.1 Overview

Verifier 围绕两个核心维度评判 Agent 交出的产物：

- **功能性（Functionality）**：东西、参数、动画、摆放、交互对不对；题目没钉死的部分不检查
- **审美性（Aesthetics）**：好不好看

两者的关系是：**功能性作为硬约束，审美性仅用于可行解之间的偏好排序。**

图 3.1 是评测流程：先用程序检查 L0–L3，层层截断；全过了，才让模型在 L4 比好不好看。

<figure class="paper-fig">
<svg viewBox="0 0 1000 320" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
<defs>
<marker id="g31" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker>
<marker id="r31" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#dc2626"/></marker>
</defs>
<rect x="20" y="14" width="760" height="30" rx="15" fill="#eff6ff" stroke="#2563eb"/>
<text x="400" y="34" text-anchor="middle" fill="#2563eb" font-weight="600">Functionality · L0–L3 · 程序检查</text>
<rect x="820" y="14" width="160" height="30" rx="15" fill="#faf5ff" stroke="#9333ea"/>
<text x="900" y="34" text-anchor="middle" fill="#9333ea" font-weight="600">Aesthetics · L4</text>
<g fill="#eff6ff" stroke="#2563eb" stroke-width="1.5">
<rect x="20" y="64" width="160" height="120" rx="12"/>
<rect x="220" y="64" width="160" height="120" rx="12"/>
<rect x="420" y="64" width="160" height="120" rx="12"/>
<rect x="620" y="64" width="160" height="120" rx="12"/>
</g>
<rect x="820" y="64" width="160" height="120" rx="12" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
<g stroke="#94a3b8">
<line x1="36" y1="132" x2="164" y2="132"/>
<line x1="236" y1="132" x2="364" y2="132"/>
<line x1="436" y1="132" x2="564" y2="132"/>
<line x1="636" y1="132" x2="764" y2="132"/>
<line x1="836" y1="132" x2="964" y2="132"/>
</g>
<g text-anchor="middle" fill="#0f172a">
<text x="100" y="94" font-size="16" font-weight="700">L0 执行</text>
<text x="100" y="118">能跑吗</text>
<text x="300" y="94" font-size="16" font-weight="700">L1 结构</text>
<text x="300" y="118">东西对吗</text>
<text x="500" y="94" font-size="16" font-weight="700">L2 几何</text>
<text x="500" y="118">摆得对吗</text>
<text x="700" y="94" font-size="16" font-weight="700">L3 行为</text>
<text x="700" y="118">用起来对吗</text>
<text x="900" y="94" font-size="16" font-weight="700">L4 美学</text>
<text x="900" y="118">好看吗</text>
</g>
<g text-anchor="middle" fill="#0f172a" font-size="12">
<text x="100" y="153">脚本退出状态</text>
<text x="100" y="171">非空白帧</text>
<text x="300" y="153">场景图 · 动画曲线</text>
<text x="300" y="171">渲染设置</text>
<text x="500" y="153">逐部件几何 · 体素</text>
<text x="500" y="171">拓扑</text>
<text x="700" y="153">输入重放 +</text>
<text x="700" y="171">状态差分</text>
<text x="900" y="162">模型两两比较</text>
</g>
<g stroke="#94a3b8" stroke-width="1.5" marker-end="url(#g31)">
<line x1="182" y1="124" x2="217" y2="124"/>
<line x1="382" y1="124" x2="417" y2="124"/>
<line x1="582" y1="124" x2="617" y2="124"/>
<line x1="782" y1="124" x2="817" y2="124"/>
</g>
<g stroke="#dc2626" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#r31)">
<line x1="100" y1="186" x2="100" y2="258"/>
<line x1="300" y1="186" x2="300" y2="258"/>
<line x1="500" y1="186" x2="500" y2="258"/>
<line x1="700" y1="186" x2="700" y2="258"/>
<line x1="900" y1="186" x2="900" y2="258"/>
</g>
<rect x="20" y="262" width="960" height="40" rx="10" fill="#fef2f2" stroke="#dc2626"/>
<text x="500" y="288" text-anchor="middle" fill="#dc2626" font-weight="600">不通过 → 0 分，后面不跑</text>
</svg>
<figcaption>图 3.1　3D 分层关卡：L0–L3 由程序读场景状态，L4 才交给模型比较；任一层不过即 0 分，后层不跑</figcaption>
</figure>

适用边界：本章的判别力数字只覆盖「修复单处破坏」类任务，从零生成见 3.2.6。

例题：Blender 脚本搭场景，木桌上放蓝色杯子，台灯灯臂第 1–40 帧从 0° 转到 40°。本例无交互，跳过 L3（L3 用于 three.js 游戏）。

图 3.2 是对照：[BlenderWorld](https://github.com/QwenLM/BlenderWorld) 的评测流水线，照其 `docs/assets/evaluation-pipeline.png` 重画成 draw.io，可直接编辑。

- 缺 `.blend` 直接记 0
- Rubric 打分模型逐条判 0/1、按权重算通过率：Agent-as-Judge 读 scene_summary 与 `.blend`，VLM-as-Judge 看渲染图
- Dimension 打分模型（VLM）给 8 个维度各打 1–10 分，两者 1:1 融合成任务分
- 和本文的区别：审美分直接进总分，而不是只在全过的作品之间排名次

<iframe src="../assets/figures/evaluation-pipeline.html" style="width:100%;height:460px;border:0" title="BlenderWorld 评测流水线"></iframe>
<p style="margin-top:8px;font-size:12.5px;color:var(--ink-soft);text-align:center">图 3.2　BlenderWorld 的评测流水线；图小，细看点「全屏编辑」。改动自动存在本浏览器；要留档点「下载 .drawio」，放回 <code>assets/figures/</code> 后重建即可更新正文</p>

#### 3.1.1 Glossary

前五条与 Web 页通用，后四条是 3D 的几何信号。

| 术语 | 含义 |
|---|---|
| 改坏的样本 | 故意改出真错误，应判挂 |
| 换写法的样本 | 写法变了、结果一样，应判过 |
| 抓错率 | 改坏的样本被判挂的比例 |
| 放对率 | 换写法的样本被判过的比例 |
| Critic | 模型评审：看渲染结果、自己操作页面、输出问题清单的 VLM Agent（打分场景叫「打分模型」） |
| 剪影交并比 | IoU：两张剪影的重叠 ÷ 合并 |
| 点云距离 | Chamfer 距离：两组点云间平均最近距离 |
| 逐部件 F 分数 | 按材质色分组，两组表面采样点在容差内能对上的比例，取最差组 |
| 逐颜色体素占据 | 把场景切成体素，比较各颜色占的位置；只比不分颜色的占位时叫体素交并比 |

#### 3.1.2 Reward Function

$$r = g\cdot(1+\lambda\,w),\qquad 0<\lambda\le 1$$

- $g=\prod_{k=0}^{3}\mathbf{1}[\,L_k\ \text{pass}\,]\in\{0,1\}$：功能闸，L0–L3 全部通过为 1，任一层不过为 0
- $w\in[0,1]$：审美胜率，只在组内通过者之间两两比较得出
- 公式与 Web 页相同，为本文建议，未实测

1. 功能全过才算，不加权、不给部分分。
   - 本项目 Blender verifier 每条检查都是「且」；题目钉死的项不过直接 0 分
2. 前层不过，后层不跑。
   - 脚本报错，后面的几何和渲染不算
   - 截断也会放大取证链路自己的漏洞：Train 页 4.2 的三个取证缺口都让正确页面在 L0 被整条判 0，看上去像模型连页面都写不对
3. 审美只在通过者之间排名次。
4. 阈值在跑改坏的样本前冻结，后定的要标出。
5. 代价是奖励稀疏：$r$ 近似二值；同一题的一组采样全部通过或全部失败时，组内相对优势为零，不产生梯度。
   - 实测：〔three.js〕16 道修复题 × 8 次，13 题全对或全错，只有 3 题有梯度；0.3–0.7 难度带内 0/16
   - 缓解：以被训模型自身的 pass@k 做难度过滤，配合动态采样

3D 阈值（本项目设定）：

| 阈值 | 值 | 怎么定 | 看样本前/后 | 单用判对 |
|---|--:|---|:-:|--:|
| 图像相似度 | ≥ 0.995 | 按等价定 | 前 | 12/22 |
| 剪影交并比 | ≥ 0.97 | 按等价定 | 前 | 14/22 |
| 点云距离 | ≤ 0.4% 对角线 | 按等价定 | 前 | 13/22 |
| 体素交并比 | ≥ 0.80 | 按等价定 | 前 | 15/22 |
| 逐部件 F 分数 | ≥ 0.99 | 换写法最低值 0.9989 反推 | 后 | 无独立验证 |

- 口径：〔Blender〕台灯桌面场景，n = 22 样本 × 1 次；单用判对 = 抓错 + 放对，满分 22
- 按等价定：按「什么算同一个场景」定，不从噪声推（见 3.2.3），具体依据原始记录未展开
- 点云距离 0.4% 是距离上限，不是 3.2.4 的 F 分数匹配容差 0.5%

### 3.2 Functionality

功能性回答「题目钉死的东西都对吗」：按 L0–L3 四层逐条判 0 或 1，判据是运行后的场景状态，不读代码，也不看渲染图。能写成断言的交给程序，VLM 只补程序读不出的外观。

#### 3.2.1 Judges & Rules

**1. Agentic Critic: Checklist Decomposition**

Critic 的做法同 Web 页 3.2.1：按 L0–L3 拆检查清单，每条对应题目里钉死的一个字段；同一道题只拆一次并冻结。3D 的差别在分派：

1. 能读场景图的，一律写成程序：场景图、动画曲线、逐部件几何、拓扑量
2. 只有看画面才能判的外观，才交给 VLM
3. **凡是能被透视或取景解释掉的检查，一律不交给模型**

**2. Layers**

| Layer | Checks | Method (Program / Agent / VLM) | Used by | Evidence |
|---|---|---|---|---|
| **L0 执行** | 能跑完、出帧吗 | <span class="judge j-prog">Program</span>执行检查：脚本退出状态、非空白帧 | [CAD-Coder](https://arxiv.org/abs/2505.19713) · [cadrille](https://arxiv.org/abs/2505.22914) | - |
| **L1 结构** | 物体参数、关键帧、渲染参数对不对 | <span class="judge j-prog">Program</span>场景图检查：如杯子材质是蓝色吗；动画曲线检查：如灯臂第 40 帧 40°；渲染设置检查：引擎、分辨率、帧范围，如帧范围恰为 1–40<br><span class="judge j-agent">Agent</span>[BlenderWorld](https://github.com/QwenLM/BlenderWorld) 的做法：读 scene_summary 与 `.blend` 逐条判 | [3JSBench](https://3jsbench.com/) · [WorldCoder-Bench][wcb] · [Code4Scene](https://arxiv.org/abs/2609.36777) · [MoVer](https://arxiv.org/abs/2502.13372) | 场景图在渲染图里看不见：删掉两条动画曲线，视觉指标全是 1.0000，只有逐关键帧检查抓到（[本项目 Blender 实测 · 3.2.2](#verifier-experiments)） |
| **L2 几何** | 形状、位置、占位、破洞对不对 | <span class="judge j-prog">Program</span>逐部件几何：如抓到杯子放错桌角；逐颜色体素占据：如蓝块在杯子处；拓扑量：如封口杯破洞边数为 0<br><span class="judge j-vlm">VLM</span>多视角渲染看程序漏掉的外观，如雪人头顶破洞 | [MeshCoder](https://arxiv.org/abs/2508.14879) · [Hi3DEval](https://arxiv.org/abs/2508.05609) · [CAD-Coder](https://arxiv.org/abs/2505.19713) · [BlenderGym](https://arxiv.org/abs/2504.01786) · [cadrille](https://arxiv.org/abs/2505.22914) · [BenchCAD](https://arxiv.org/abs/2605.10865) · [CAD-RL](https://arxiv.org/abs/2508.10118) · [CADTests](https://arxiv.org/abs/2605.07807) · [CADEngBench](https://arxiv.org/abs/2608.09296) | 拓扑量抓到像素和剪影都漏掉的破洞：〔three.js〕参考 0、候选 64（n = 1 样本）；体素交并比已有在线强化学习先例（3.4） |
| **L3 行为** | 按键反应对不对 | <span class="judge j-prog">Program</span>输入重放 + 状态差分：如按「开灯」后灯亮 | [PlayCoder](https://arxiv.org/abs/2604.19742) · [A2Z GameSpec-Bench](https://arxiv.org/abs/2609.39564) | 为什么要发输入，见 Web 页 3.2.1 |
| **L4 美学** | 好不好看 | <span class="judge j-vlm">VLM</span>模型两两比较，只给过关场景排名次 | [UI2Code^N](https://arxiv.org/abs/2511.08195) · [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 比较比打分准，见 Web 页 3.2.1 |

- 一句话：程序读场景状态，VLM 只管只有看画面才知道的
- 产物：`.py` = Blender 脚本（L0 另含 CadQuery `.py`），`.html` = three.js 页面；L3 只用于 three.js 游戏；动画曲线检查是时间轴上的静态检查
- Used by 的口径
  - L1 场景状态检查只用于评测，尚无当 RL reward 的先例（未核实）
  - CAD-Coder、BlenderGym 是全局几何，cadrille、BenchCAD、CAD-RL 的体素不分颜色，都是简化版
  - MoVer（2D 动画）、CADTests 与 CADEngBench（CAD）是同类检查的旁证

**3. Rubric Rules**

Critic 做功能性校验时依据的 rubric，共八条，每条附佐证。其中第 1、2、3 条是硬约束：任一条不满足，这道题就不能进 RL。

| Rules | Source | Details |
|---|---|---|
| 1. 读运行后的场景状态 | | 按场景图和几何判分，不看代码文本；等价写法极多，按代码比对会误杀正确解 |
| | 本项目实测（n = 1） | 代码比对会误杀正确解：〔Blender〕一个世界几何逐点等同的替代实现通过了全部几何信号（逐部件 F 分数 0.9993），只被代码比对类判据误杀 |
| | [3JSBench](https://3jsbench.com/) | 确定性检查能区分模型，相似度不能：Astra / Opus 5.5 / GPT-6 Sol 通过率 80.0% / 49.0% / 27.0%，SigLIP2 相似度 Astra 0.1081 对 Opus 5.5 0.1067，只差约 0.001 |
| 2. 只查题目钉死的字段 | | 判据能查的信息量不超过题目给出的信息量：题目写明的才检查，不把九类场景状态全拿来和参考比 |
| | 反例 | 题目只说加一盏日光、没钉死功率，判据照查功率，「日光功率 3.0 调成 3.5」被判挂 |
| | 本项目实测（3.2.2 第 3–5 项） | 全查会把对的判错：〔Blender〕九类全查放对 0/11，只查钉死字段的白名单组合放对 10/11 |
| 3. 渲染图只给模型看，不判分 | | 像素看不出场景状态，也比读几何贵 |
| | 本项目实测（3.2.2 第 1、6 项） | 〔Blender〕删掉两条动画曲线，视觉指标全是 1.0000；读几何每样本约 0.4 秒、十视角渲染 1.1–1.2 秒，改坏的 11 个里逐部件 F 分数抓 7 个，多视角剪影只抓 3 个 |
| 4. 多种检查组合使用 | | L0–L3 各层的检查同时上，不靠任何一种单独判 |
| | 本项目实测（3.2.2 第 7–8 项） | 单一信号必有漏网：〔three.js〕最好的单项 25/29，四层组合 29/29 |
| | [CAD-Coder 附录 B](https://arxiv.org/abs/2505.19713) | 单个几何指标会被钻空子：只用点云距离当 reward，约 200 步后模型开始产出跑不起来的代码，训练中止（3.2.5） |
| 5. 阈值按等价定，看样本前冻结 | | 按「什么算同一个场景」定，不从噪声推；后定的要标出 |
| | 本项目实测（3.2.3） | 条件满足时噪声逐位为零，推不出阈值；条件不满足时噪声会抵消分辨力 |
| | [Blender 官方渲染测试](https://github.com/blender/blender/tree/main/tests/files/render) | 阈值固定，某设备复现不了的测试进该设备黑名单，不放宽阈值（推断） |
| 6. 模型评审只做两两比较 | | VLM 不判题目钉死的属性对不对，这类判断的失败是系统性的；只在全部通过的作品之间相对排序，问题清单用来补程序检查 |
| | 本项目实测（3.2.2 第 9–12 项） | 〔three.js〕几何错误会被「透视」解释掉，判对不等于说对原因；价值在于发现遗漏的检查项 |
| 7. 先复核标签，再下「判据不准」的结论 | | 换写法的样本有 3 个以上模型一致判挂时，先复核标签再谈放对率；打标签前先看多视角渲染 |
| | 本项目实测（3.2.2 第 13 项） | 一个错标签就能让结论反过来：〔three.js〕雪人破洞样本 |
| 8. 初始状态必须判挂 | | 什么都不改的起始场景要判挂，否则原样交回也能拿分 |
| | 本文建议（未实测） | 只适用于修复类题目 |

<a class="anchor" id="verifier-experiments"></a>

#### 3.2.2 Experiments

实测结论：程序检查只有多种组合使用、只查题目钉死的字段，才能既抓到错误、又不误判正确作品；模型评审会被透视解释带偏、判定不稳定，价值在于发现程序检查遗漏的问题。

| 规则 | 发现 | 关键数据 |
|---|---|---|
| 3 渲染图只给模型看 | 1. 场景状态在渲染图里看不见 | 〔Blender〕删掉两条动画曲线，视觉指标全是 1.0000，只有逐关键帧检查抓到（n = 1 样本，取自下表 22 个） |
| | 2. 截图分不开好坏 | 〔three.js〕雪人任务 6 个候选页面，单张截图相似度全落在 0.973–1.0 |
| 2 只查题目钉死的字段 | 3. 全查会把对的判错 | 〔Blender〕九类全查抓错 11/11、放对 0/11；白名单组合抓错 11/11、放对 10/11 |
| | 4. 全查败在等价写法多 | 〔Blender〕按名字比败给自动改名（同名材质节点自动加后缀），按局部变换比败给等价父子层级，按顶点数比败给等价细分 |
| | 5. 修法是移出白名单，不是放宽容差 | 〔Blender〕白名单组合唯一放错的是留出集「日光功率 3.0 调成 3.5」：题目没钉死功率，却照查了 |
| 3 渲染图只给模型看 | 6. 读几何又便宜又准 | 〔Blender〕每样本几何全套约 0.4 秒、十视角渲染 1.1–1.2 秒；11 个改坏的里逐部件 F 分数抓 7/11、多视角剪影 3/11 |
| 4 多种检查组合使用 | 7. 单一信号必有漏网 | 〔three.js〕单张像素比对 12/29、几何类别多重集 14/29、多视角剪影交并比 19/29、逐颜色体素占据 25/29，四层组合 29/29；换场景（小车）留出 18/18，累计 47/47 |
| | 8. 几何看不见的，由场景状态补上 | 〔Blender〕逐部件几何单独漏的 4 个几何上看不见（灯泡调暗、动画删光、相机焦距改短、倒角删掉），由灯光与相机、动画曲线、修改器栈抓到 |
| 6 模型评审只做两两比较 | 9. 几何错误会被「透视」解释掉 | 〔three.js〕漏放（应挂判过）的判定里，理由拿取景、相机、透视或朝向说事的，单视角 4/8（50%）、多视角 4/6（67%）；原话「透视带来的视觉大小差异属于相机取景角度范畴，不算错误」 |
| | 10. 判对不等于说对原因 | 〔three.js〕「鼻子长在后脑勺」（1 样本 × 4 模型 × 2 次 = 8 次判定）单视角全判挂，0/8 的理由提到朝向或背面，都说「缺少鼻子」（页面相机看不到后脑勺）；训练数据要按原因对不对打标 |
| | 11. 程序稳定判挂，模型不稳定 | 〔three.js〕底球放大 20%、中球缩小 20%：逐颜色体素交并比 0.679、0.897，都在阈值外，都判挂（确定性，每例 1 次）；模型单视角每例 8 次判定，底球判对 4/7（1 次未解析），中球 8/8 |
| | 12. VLM 的价值在于发现遗漏的检查项 | 〔three.js〕雪人头顶未封口，人工标成「通过」：单视角像素分 1.000、多视角剪影交并比 0.998，程序检查全漏；模型多视角 8 次判定 7 次判挂，单视角 8 次全放过；据此新增「只被一个三角形用到的边数」，封口参考 0、该候选 64 |
| 7 先复核标签 | 13. 一个错标签就能让结论反过来 | 〔three.js〕同一样本：多视角应放行的有效判定 64 次，放对 57 次（0.891），漏的 7 次全是它；复核确认标签标错，剔掉它的 8 次后 56/56（1.000） |

- 第 7 项口径：雪人 13 + 桌子 16 共 29 个带标签样本，含两类，n = 29 × 1 次；组合阈值在这些样本上看过，不算独立验证。留出集 n = 18 样本 × 1 次，两类都有，标签先贴、阈值未动；累计 47/47（29 + 18），18 个是真留出
- 第 9–13 项口径：〔three.js〕雪人场景，温度 0；n = 18 样本 × 4 模型 × 2 视角 × 2 次 = 288 次判定，281 次有效；单视角 = 页面相机一张图，多视角 = 4 视角拼图，均与参考图上下并排

**Blender：九类场景状态逐类单开**

台灯桌面场景，n = 22 样本 × 1 次，确定性：开发集 15 个（8 改坏 + 7 换写法）+ 留出集 7 个（3 + 4），合计改坏 11、换写法 11。

| 类别 | 查什么 | 关卡 | 抓错 /11 | 放对 /11 | 判对 /22 |
|---|---|:-:|--:|--:|--:|
| 层级与命名 | 名字集合、物体类型、父子关系、集合归属 | 条件进：只查点名物体 | 2 | 10 | 12 |
| 变换 | 世界包围盒八个角点 | 不进：不查局部位置与缩放，改用包围盒或几何指标 | 3 | 7 | 10 |
| 网格统计 | 非流形边、体积符号、面数预算 | 不进：只留不变量与不等式 | 2 | 6 | 8 |
| 修改器栈 | 修改器类型与关键参数 | 进 | 2 | 11 | 13 |
| 材质节点树 | 节点类型与连边 | 条件进：按类型与连边、不按节点名比，只查钉死的接口 | 1 | 10 | 11 |
| 灯光与相机 | 功率、色温、焦距、当前相机 | 进：只查白名单字段 | 2 | 10 | 12 |
| 动画曲线 | 逐关键帧的时间、取值、插值，按帧求值 | 进 | 1 | 11 | 12 |
| 物理与约束 | 约束类型、目标、影响系数、刚体字段 | 进 | 0 | 11 | 11 |
| 渲染设置 | 引擎、分辨率、帧率、帧范围、采样、色彩管理 | 进：精确相等，无容差 | 0 | 11 | 11 |
| 逐部件几何（单独） | 按材质色分组的 F 分数 | — | 7 | 11 | 18 |
| 白名单组合 | 逐部件几何 + 修改器栈 + 灯光与相机 + 动画曲线 + 渲染设置 | 进 | **11** | **10** | **21** |
| 九类全查 | 全部字段 | 反面教材 | 11 | 0 | 11 |

- 关卡 = 进不进推荐的最终判定：进 = 按字段比；条件进 = 只查一部分；不进 = 不按字段比，改用别的信号
- 逐部件几何读表面采样点，不在九类内，白名单组合的 11/11 不能直接比各类的 0–3/11；未测四类单独组合（不含逐部件几何）
- 物理与约束「进」但不在实测组合：本批无针对它的改坏样本（抓错 0/11），收它是因为静帧看不见约束

**CAD：真值最确定**

尺寸、约束、实体有效性、可制造性全部确定；[BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) 约 1.8 万个参数化程序都经执行校验，「全部按执行结果判分，不用模型打分」（未核实）。

#### 3.2.3 Insight：Zero Noise Is Conditional

**阈值不能从噪声推：噪声在条件满足时是零，所以阈值只能按「什么算等价」来定；条件不满足时，噪声会抵消分辨力。**

| Insight | Source | Details |
|---|---|---|
| 两个条件都满足时，噪声逐位为零 | 本项目实测 | 〔Blender〕参考解跑两遍（n = 1 样本 × 2 次）：图像 1.0000、点云距离 0.0000、体素交并比 1.0000 |
| 条件 1：显式传采样种子 | 本项目实测 | 〔Blender〕表面采样用采样库自己的随机源，全局种子管不到；不传时参考解自比点云距离 0.00167，与样本分布 0.0016–0.0065 同量级，而两类样本本就在此区间重叠 |
| 条件 2：在任务容器里重渲 | 本项目实测 | 〔Blender〕换 CPU 或图形栈版本像素会漂，参考图须在容器内用同一引擎重渲，不能用仓库存图 |
| 官方同样不靠放宽阈值 | [Blender 官方渲染测试](https://github.com/blender/blender/tree/main/tests/files/render) | 阈值固定：单像素误差 > 0.016 的像素不超过 1%；某设备复现不了的测试进该设备黑名单（推断） |

#### 3.2.4 Insight：Tolerance Can Invert

**点云 F 分数的容差选错，结论会反过来：取对角线 0.5%，逐部件算；下限不低于平均最近邻距离的 3 倍，该距离用参考解自采样两次估出，每个场景单算。**

<figure class="paper-fig">
<svg viewBox="0 0 1000 340" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
  <g stroke="#94a3b8" stroke-width="1">
    <line x1="100" y1="40" x2="100" y2="280"/><line x1="100" y1="280" x2="720" y2="280"/>
    <line x1="95" y1="40" x2="100" y2="40"/><line x1="95" y1="120" x2="100" y2="120"/>
    <line x1="95" y1="200" x2="100" y2="200"/><line x1="95" y1="280" x2="100" y2="280"/>
  </g>
  <g fill="#0f172a" font-size="12" text-anchor="end">
    <text x="90" y="44">1.0</text><text x="90" y="124">0.8</text><text x="90" y="204">0.6</text><text x="90" y="284">0.4</text>
  </g>
  <text x="40" y="160" text-anchor="middle" fill="#0f172a" transform="rotate(-90 40 160)">F 分数</text>
  <g fill="#0f172a" text-anchor="middle">
    <text x="220" y="302">0.1%</text><text x="420" y="302">0.5%（本文取值）</text><text x="620" y="302">1%</text>
    <text x="410" y="330">F 分数容差（场景对角线的 %）</text>
  </g>
  <line x1="420" y1="40" x2="420" y2="280" stroke="#2563eb" stroke-width="1" stroke-dasharray="4 4"/>
  <circle cx="220" cy="241" r="7" fill="#2563eb"/><text x="234" y="246" fill="#0f172a">0.4977</text>
  <circle cx="220" cy="54" r="7" fill="#dc2626"/><text x="234" y="59" fill="#0f172a">0.9639</text>
  <rect x="140" y="120" width="180" height="54" rx="6" fill="#fef2f2" stroke="#dc2626"/>
  <text x="230" y="142" text-anchor="middle" fill="#dc2626">反转：应该过 &lt; 应该挂</text>
  <text x="230" y="162" text-anchor="middle" fill="#0f172a" font-size="12">容差 &lt; 点距 3–5 毫米</text>
  <circle cx="408" cy="41" r="6" fill="#dc2626"/><circle cx="420" cy="41" r="6" fill="#dc2626"/>
  <circle cx="432" cy="40" r="6" fill="#2563eb"/>
  <rect x="345" y="66" width="150" height="54" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="420" y="88" text-anchor="middle" fill="#0f172a">全局算：三点重叠</text>
  <text x="420" y="108" text-anchor="middle" fill="#0f172a" font-size="12">0.9985–0.9993</text>
  <circle cx="612" cy="46" r="6" fill="#dc2626"/><circle cx="628" cy="52" r="6" fill="#dc2626"/>
  <rect x="540" y="78" width="160" height="72" rx="6" fill="#ffffff" stroke="#94a3b8"/>
  <text x="620" y="100" text-anchor="middle" fill="#0f172a">记录里 7 个应该挂的</text>
  <text x="620" y="120" text-anchor="middle" fill="#0f172a" font-size="12">只有 2 个低于 0.99</text>
  <text x="620" y="138" text-anchor="middle" fill="#0f172a" font-size="12">0.9847 · 0.9704</text>
  <circle cx="770" cy="110" r="7" fill="#2563eb"/><text x="786" y="115" fill="#0f172a">换写法的样本（应该过）</text>
  <circle cx="770" cy="140" r="7" fill="#dc2626"/><text x="786" y="145" fill="#0f172a">改坏的样本（应该挂）</text>
</svg>
<figcaption>图 3.3　点云 F 分数的容差（本项目实测）：0.1% 时结论反转；0.5% 全局算仍重叠，须逐部件算；1% 时 7 个应该挂的（含留出集）只有 2 个低于 0.99。横轴三档不按比例</figcaption>
</figure>

| 容差 | 现象 | 关键数据 |
|---|---|---|
| 0.1%（2.2 毫米） | 小于采样间距，测的是采样密度而非几何 | 换写法的细分样本 0.4977，反而低于改坏的灯罩转反 0.9639；六万个点铺在 2.18 米场景上，平均点距就有 3–5 毫米 |
| 0.5% 全局算 | 没有全局容差能分开两类 | 改坏的 0.9993、0.9985 与换写法的 0.9993 重叠 |
| 0.5% 逐部件算（本文取值） | 每种材质色一组，取最差组 | 换写法最低 0.9989，阈值取 0.99：抓错 7/11、放对 11/11 |
| 1% | 太大，多数改坏的分不出 | 7 个只有 2 个低于 0.99（灯罩转反 0.9847、桌腿少一条 0.9704），其余 5 个都在 0.99 以上 |

- 口径：〔Blender〕n = 12 样本 × 4 档容差（0.1%、0.2%、0.5%、1%），各算 1 次；12 个取自 3.2.2 的 22 个，原始记录只列了 7 个改坏的（含留出集 2 个）和 5 个换写法的，未列另 4 个改坏的（换色、灯泡调暗、动画删光、相机焦距改短）
- 两条取值规则可能冲突（推断）：本场景 0.5% 对角线 ≈ 10.9 毫米（对角线 2.18 米），而「不低于 3 倍平均点距」在点距 3–5 毫米时是 9–15 毫米，所以取二者较大者
- 外推边界：按材质色分组会把同色部件合成一块，少一个同色部件就看不出；three.js 相对关系原型因此改为按颜色取连通块当部件（桌面与四条腿同色会合成一块，是原型设计时的描述，未单独测量）；逐部件 F 分数照此拆分的效果、部件多的复杂场景均未测

#### 3.2.5 Insight：Single Metric Collapses

**单个几何指标不能单独当 reward：它会被钻空子，必须和执行检查、难度过滤一起用。**

| Insight | Source | Details |
|---|---|---|
| 只用点云距离当 reward 会崩 | [CAD-Coder 附录 B](https://arxiv.org/abs/2505.19713) | 〔CAD〕约 200 步后模型开始产出跑不起来的代码，训练中止 |
| 配套做法是难度过滤 | [cadrille](https://arxiv.org/abs/2505.22914) | 〔CAD〕只留 3 次采样平均 reward 低于 7.5 的题（reward = 10×交并比，满分 10） |
| 跑不起来的代码记 0 还是记负分，未对比 | CAD-Coder · cadrille | CAD-Coder 记 0、cadrille 记 −10；本文默认记 0，记负分能否更快压掉不可执行输出未测 |

#### 3.2.6 Insight：Evidence Has A Boundary

**本页判别力数字（29/29、47/47、18/18、Blender 21/22）都来自「修复单处破坏」类任务；只有阈值冻结后才见到的样本算独立证据。**

验收指标用抓错率、放对率、Youden 指数，各配置信区间：一般用 Wilson 95% 区间；一次都没出错时，出错率的 95% 上界 ≈ 3 ÷ n。

| 证据 | 算不算独立 | 关键数据 |
|---|---|---|
| 〔three.js〕组合判定，换场景留出 | 算，但跨场景独立样本数为 1 | 18/18（n = 18 样本 × 1 次，都是小车这一个场景的改动）：Wilson 95% 下界 0.824，即准确率 ≥ 82.4%；出错率 95% 上界 ≈ 3 ÷ 18 ≈ 16.7%；抓错 11/11（下界 74.1%）、放对 7/7（下界 64.6%）；换到别的场景没有统计保证 |
| 〔Blender〕白名单组合 | 不算 | 成员看过开发集 15 个样本才选定，逐部件 F 的 0.99 后定 |
| 〔Blender〕先冻结的四个阈值 | 算 | 22 个样本都在冻结后才见到，但单用只判对 12–15/22 |

从零生成不在这些数字的覆盖范围内：

- 〔three.js〕现有判据 0/26，其中 23 组挂在剪影层；抽看的 4 个产物人看都对，挂的原因是比例与参考不重合
- 〔three.js〕只看相对关系的原型救回 13/80，代价是三场景带标签样本 47/47 → 35/47
- 分母：32 组（场景 × 模型 × 有无参考图）中有效 26 组，0/26 按组计（每组最多 3 轮）；13/80 按同一批实验的每次尝试计，80 的精确构成原始记录未交代（未核实）

### 3.3 Aesthetics

**本项目素材没覆盖 3D 审美：能程序查的只是「物理上自不自洽」，公开 3D 评测器与人的两两一致率，已发表最高是 GPTEval3D 自报的 78.9%，换到别家数据只有 65%–69%。**

#### 3.3.1 Aesthetic Evaluation

| Insight | Source |
|---|---|
| 公开 3D 评测器测资产质量，不测交互与功能 | [GPTEval3D](https://arxiv.org/abs/2401.04092)：自家数据两两一致 78.9%、Kendall τ（排序一致性系数）0.710；别家数据复测 3DGen-Bench 67.7%、Hi3DEval 65%–69% |
| | [3DGen-Bench](https://arxiv.org/abs/2503.21745)：自家评分器 72.5%；1,020 条提示、11,220 个资产、68,000+ 偏好投票 |
| | [Hi3DEval](https://arxiv.org/abs/2508.05609)：自家数据物体级 70%–77%；[MATE-3D](https://arxiv.org/abs/2412.11170)：1,280 个网格、107,520 条多维度标注 |
| 「3D 低一截」只是推断 | 网页侧模型评审两两一致 91%–94%（[ArtifactsBench](https://arxiv.org/abs/2507.04952) / [UI2Code^N](https://arxiv.org/abs/2511.08195)）；数据集不同，这是实测一致率，不是门槛，测的是网页评审，与 3D 偏好数据口径不同 |
| 能程序查的是「物理自洽」，不是审美 | [3JSBench](https://3jsbench.com/) 有 98 条渲染质量检查（网格预算、可见背面、绘制顺序） |
| | 五大失败：穿插 20%、可见背面 19%、闪烁 17%、朝向 16%、断开 16%；前三类属渲染层面的物理不自洽（本项目归类，非站方原话） |
| | 网格预算：Muse Spark 1.3 中位 995 个网格、177,000 个三角面，Astra 45 个，Fable 5.1 24 个；Muse 有 33% 的尝试出现闪烁 |
| 嵌入相似度当 3D 质量关卡没用 | 3JSBench 上 11 个模型的 SigLIP2 均值全在 0.0774–0.1081；Astra / Opus 5.5 / GPT-6 Sol 减去每题平均后三者只高 +0.011 / +0.009 / +0.007 |

#### 3.3.2 Insight：Filter, Not Reward

**本项目素材里，3D 美学分只见于数据过滤，未见用作 reward。**

- [Objaverse-XL](https://arxiv.org/abs/2307.05663) 用 LAION 美学分分三档，外加坏渲染分类器（1,200 条人工标注训练，阈值 0.5）；Polycam 来源的渲染图 38.20% 被判坏
- 3D 的 L4 目前只做模型两两比较；网页侧的排版类程序检查在 3D 场景里没有对应物，未实测

### 3.4 Frontier Lab

**所查来源都没披露 3D 训练方法，只有演示和基准分数；国内没有一家披露 Blender 训练数据（推断）。**

每条 Insight 落在哪一环见 Taxonomy 列：<span class="tx tx-data">数据</span> <span class="tx tx-verifier">Verifier</span> <span class="tx tx-harness">Harness</span>

| Lab | Blog | Taxonomy | Insight |
|---|---|---|---|
| <img height="14" src="../assets/logos/openai.png" align="center" alt="OpenAI" title="OpenAI"> OpenAI | [Building games with Astra](https://developers.openai.com/blog/how-to-build-games-with-astra) | <span class="tx tx-verifier" data-b="0">Verifier</span> | three.js 渲染计数器（绘制调用、三角面、几何体、纹理）、90 个帧间隔采样、特效开关像素差分；无阈值。未披露 Blender 与游戏训练数据、视觉 reward 模型 |
|  | [Architectural visualization with Astra](https://developers.openai.com/blog/architectural-visualization-with-astra) | <span class="tx tx-harness" data-b="1">Harness</span> | bpy 建场景，computer use 打开 Blender 检查；原文：几何检查「不替代看渲染图」。未披露项同上 |
| <img height="14" src="../assets/logos/anthropic.png" align="center" alt="Anthropic" title="Anthropic"> Anthropic | [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) | <span class="tx tx-data" data-b="2">数据</span> | 提到 shaders、3D 原型能力；检索 Claude 4 到 Opus 5.5 共 9 份 system card，无一讲 3D 训练（本项目检索） |
|  | [Claude Opus 5 System Card](https://www.anthropic.com/claude-opus-5-system-card) | <span class="tx tx-verifier" data-b="3">Verifier</span> | 唯一的 3D 量化：BenchCAD Vision2Code 工具消融，体素交并比 0.366 → 0.821；1,000 个文件的子集，5 次平均（8.12 节） |
| <img height="14" src="../assets/logos/moonshot.png" align="center" alt="Moonshot AI" title="Moonshot AI"> Moonshot AI | [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) | <span class="tx tx-data" data-b="4">数据</span> | 唯一把 3D 资产、游戏、CAD 的「代码 ↔ 渲染」配对写进预训练（3.1 节）；3D 侧的 reward 设计未披露 |
| <span class="org-mark" title="Xiaomi">X</span> Xiaomi | [MiMo-V2-Flash Technical Report](https://arxiv.org/abs/2601.02780) | <span class="tx tx-verifier" data-b="5">Verifier</span> | 录屏判别，可解 three.js 动态场景单帧看不全（本项目推断）；3D 专项数据未披露 |
| <img height="14" src="../assets/logos/qwen.png" align="center" alt="Alibaba Qwen" title="Alibaba Qwen"> Alibaba Qwen | Qwen3.8-Max | <span class="tx tx-verifier" data-b="6">Verifier</span> | QwenBlenderBench 69.9（未核实）：内部基准，未找到公开出处，打分方法未披露 |

1. BenchCAD 是两家都报过分的唯一 3D 基准，口径不同、不能直接比。
   - OpenAI 发布页（[GPT-6 Astra](https://openai.com/index/gpt-6-astra/)）：Astra 95.9%、GPT-5.6 Sol 83.3%，转引 Fable 5.1 84.3%（几何重叠分）
   - Anthropic：体素交并比 0.366 → 0.821
2. 3JSBench 用同一套确定性检查：Astra 80.0%、Fable 5.1 69.3%、Opus 5.5 49.0%、GPT-6 Sol 27.0%、Kimi K3 23.0%。
3. 学术侧 CAD 已有「能执行才给分 × 交并比」的在线强化学习，three.js 和 shader 只有基准。
   - CAD：[cadrille](https://arxiv.org/abs/2505.22914)、[CAD-RL](https://arxiv.org/abs/2508.10118)；three.js 和 shader 没有强化学习论文（本项目检索，截至 2026-10）
4. 可照抄的仍是网页侧做法（见 Web 页 3.4）：出题与收题、判据写法、打分系统本身；「用什么模型、配比多少」所查来源都没公开。

[wcb]: https://arxiv.org/abs/2606.01869

