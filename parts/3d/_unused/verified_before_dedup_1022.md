## 1 The Same Three Parts, A Different Ground Truth

本章只回答一个问题：**怎么把一批 3D 场景与脚本，变成能训模型的题。**

一条可验证任务和 Web 一样由三件组成，缺一件就只是数据，不是任务。三个词含义同 Web 页第 1 章，后面三章各讲一件。

| 件 | 在 3D 这条线上具体是什么 | 缺了它会怎样 |
|---|---|---|
| Omni Reference Query | 需求描述，加上参考：参考图或多视角图、起始场景与脚本、点云、参考视频 | 资产库再大也只有模型文件，凑不成「指令 → 代码」的配对 |
| Verifier | 读场景图与几何的程序检查（L0–L3），全过之后才让模型比好不好看（L4） | 没有梯度，只能靠人看渲染图 |
| Harness | Blender 按版本分叉的无头运行时；three.js 无头浏览器加取证事件靶；显式采样种子、容器内重渲 | 产物跑不起来，场景图读不出来 |

三条硬约束：

1. **Verifier 只查 Query 钉死的字段。**
   - 反例：题目只说加一盏日光、没钉死功率，判据照查功率，「日光功率 3.0 调成 3.5」被判挂（3.3.2）
   - 九类场景状态全查，换写法的样本放对 0/11；只查钉死字段的白名单组合放对 10/11（3.3.1）
2. **判据读运行后的场景状态，不读代码。**
   - 实测：一个世界几何逐点等同的替代实现，通过了全部几何信号（逐部件 F 分数 0.9993），只被代码比对类判据误杀
   - 等价写法极多：同名材质节点自动改名、等价父子层级、等价细分（3.3.2）
3. **渲染图只给模型看，不判分。**
   - 删掉两条动画曲线，视觉指标全是 1.0000，只有逐关键帧检查抓到（3.1）
   - 读几何每样本约 0.4 秒、十视角渲染 1.1–1.2 秒；改坏的 11 个里逐部件 F 分数抓 7 个，多视角剪影只抓 3 个（3.3.1）

和 Web 比，三件事的难度分配完全不同：**题目更难凑，检查规则更好做，运行环境最贵。**

核心发现：3D 的检查规则可以做到零方差，而它的运行环境是全文三条技术线里唯一需要按版本分叉的。

| | Web(2D) | 3D |
|---|---|---|
| 题目来源 | 真实线上 query 分布有反馈 | 几乎没有真实 query 分布，主要靠参考素材反推与槽位合成 |
| 真值形态 | DOM 与计算样式 | 场景图：几何、材质、修饰器、求解器、动画曲线 |
| 噪声地板 | 231 个可观测字段里 4 个会变 | 参考解跑两遍，图像、点云距离、体素占据全部逐位相同 |
| 运行环境 | 一个浏览器镜像挂几百道题 | Blender 要按版本分叉，three.js 不必 |
| 单题成本 | 4.9 秒 | Blender 2.3 秒，three.js 383 毫秒 |

本页顺序与 Web 页一致：第 2 章 Query（3D 最弱的一环）→ 第 3 章 Verifier（3D 最强的一环）→ 第 4 章 Harness（版本适配只在这里出现）。

## 2 Omni Reference Query: Where The Material Comes From

Query 这一侧回答两个问题：

- 素材从哪来 → 决定供给的天花板
- 参考给到什么程度 → 决定检查规则的来源

### 2.1 Overview

**3D 的供给结构和 Web 完全不同：资产多、代码少，而题目要的是代码。**

核心发现：三个技术栈里只有 CAD 有成规模的公开配对数据；Blender 的代码来源收缩到两位数；three.js 没有任何公开的训练配对集。

| Source | Type | Datasize | Example | 详见 |
|---|---|--:|---|:-:|
| **GitHub** | Golden Images | 2,564 图 · 613 图 | [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) · [three.js examples](https://github.com/mrdoob/three.js) | 2.2 |
| | 带星脚本 / 页面仓库 | 56 仓 · 2,401 仓 | Blender bpy 仓库 · three.js 仓库 | 2.2 |
| | 程序化生成器 | 无上限 | [Infinigen](https://github.com/princeton-vl/infinigen) | 2.2 |
| **HuggingFace** | 文本 / 点云 / 图 → 代码配对集 | 205 – 970,937 | [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) · [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) · [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | 2.3 |
| | 资产库（无代码） | 10.85M 行元数据 | [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | 2.3 |
| **Website** | 问答站 / 论坛 | 123k – 602k | [Blender StackExchange](https://blender.stackexchange.com/) · [BlenderArtists](https://blenderartists.org/) | 2.4 |
| | 资产站 / 作品站 | 2,387 – 1M+ | [Sketchfab](https://sketchfab.com/) · [Poly Haven](https://polyhaven.com/) · [Shadertoy](https://www.shadertoy.com/) | 2.4 |

Golden Images：仓库为每份测试代码存一张标准截图，CI 每次渲染后逐像素比对，代码与截图因此天然成对（同 Web 页 2.1）。

数据解读：

- **空位落在主力技术栈上**：Blender 与 three.js 是本文的核心栈，CAD 是辅助，而公开供给的厚度正好相反。所以 3D 的自建比例必须比 Web 高。
- **资产不是题目**：资产库给的是模型文件不是脚本，只能当素材池与渲染基线，当不了「指令 → 代码」的配对。
- **没有发现任何公开工作在批量挖掘 Blender 脚本**：这是缺口，不是一条可抄的路。

### 2.2 Github Repo

| Repo | Reference | Datasize | Output | Permitted |
|---|---|--:|---|---|
| [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) | image（只有文件名） | 2,564 图 / 839 场景（3.1 : 1），46 类 | `.blend` | △ GPL |
| [three.js examples](https://github.com/mrdoob/three.js) | image + title | 613 图 / 613 页（1 : 1） | `.html` | ✓ MIT |
| Blender bpy 仓库 | — | 6,307 → 56 可用 | `.py` | 逐仓许可 |
| three.js 仓库 | — | 89,622 → 23,983（主题标签）→ 2,401（星 > 10） | `.html` / `.js` | 逐仓许可 |
| Blender 官方扩展目录 | — | 1,533（1,256 插件 + 276 主题） | 插件 `.py` | ✗ 传染性许可 1,341，MIT 只有 4 |
| [Infinigen](https://github.com/princeton-vl/infinigen) | 无（随机种子驱动） | 无上限（生成器） | Blender 场景，可导出 OBJ / USD | ✓ BSD-3 |

- Golden Images 两行的图数与码数 2026-10-20 按仓库 HEAD 实数（见 Web 页 2.2.1）。
- three.js 示例页单页中位 6,137 字节，可用接口 1,251 个：一个模型能在上下文里直接带着走的量级。
- bpy 仓库大多依赖工程文件、资产路径与插件，开箱即跑率很低。

### 2.3 Huggingface

| Dataset | Reference | Datasize | Output | Permitted |
|---|:-:|--:|:-:|---|
| [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) | text | 12,059 | bpy 脚本 | ✓ Apache-2.0 |
| [MeshCoder](https://huggingface.co/datasets/InternRobotics/MeshCoderDataset) | 点云 | 100K（论文约 1M） | 分部件 bpy 脚本 | △ CC-BY-SA-4.0，需申请 |
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) | 多视角图 + 起始脚本 | 280（论文 245） | 编辑后的 bpy 脚本 | ？未声明许可 |
| [WorldCoder-Bench](https://huggingface.co/datasets/shuolucs/WorldCoder-Bench) | text + 可选 GLB 资产 | 205（论文 2,026） | three.js `.html` | ✓ CC-BY-4.0 |
| [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) | 点云（由代码执行后采样） | 970,937 + 968 | CadQuery 代码 | △ CC-BY-NC-4.0 |
| [Omni-CAD](https://huggingface.co/datasets/jingwei-xu-00/Omni-CAD) | text + 多视角图 + 点云 | 313,096（论文约 450K） | CAD 命令序列 | ✓ MIT |
| [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) | 无（无条件生成） | 论文 17.8 万（未核实际条数） | CAD 构造序列 | ？代码 MIT，数据未声明 |
| [Text2CAD](https://huggingface.co/datasets/SadilKhan/Text2CAD) | text（初学到专家多级） | 论文约 170K 模型 / 660K 文本 | CAD 命令序列 | △ CC-BY-NC-SA-4.0，需申请 |
| [GenCAD-Code](https://huggingface.co/datasets/CADCODER/GenCAD-Code) | image + 固定指令 | 162,848 | CadQuery 代码 | ？未声明许可 |
| [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | 4 视角图 / 原代码 + 编辑指令 | 21,048 | CadQuery 代码 | ✓ CC-BY-4.0 |
| [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | 无（资产库） | 10,850,997 行元数据 | 网格文件，需自行下载 | △ ODC-By，单个对象各有许可 |

已知问题：

- WorldCoder-Bench：HF 只放了 205 题，论文的 2,026 题分 Core / Robust，未全部公开
- MeshCoder：README 称已发布 100K 条物体-代码对，论文约 100 万物体 / 41 类
- BlenderGym：压缩包里实数 280 个实例，论文写 245
- Omni-CAD：数据卡与论文写约 450K，切分文件里实数 313,096；图与点云要按脚本自行生成
- BenchCAD：由 17,900 条代码生成、748 条编辑、2,400 条问答组成；数据卡没写判分方式
- Objaverse-XL：代码托管侧索引 3,700 万个文件（去重后元数据 1,085 万行），能导入渲染的 550 万，约 15%；以元数据为分母约 51%。「550 万」在论文里只针对 GitHub 来源；Polycam 部分需申请、仅非商用
- CAD-Recode、Text2CAD：非商用许可，不能进商用训练

✓ 宽松许可　△ 有条件　？未声明。2026-10-20 读自各数据卡、文件列表与 LICENSE。

### 2.4 Website

| Website | Reference | Datasize | Output | Permitted |
|---|:-:|--:|---|:-:|
| [Poly Haven](https://polyhaven.com/) | image + title | 2,387 | HDRI / 贴图 / 模型，无代码 | ✓ CC0 |
| [js13kGames](https://js13kgames.com/) | image + title | 2,799 | 单文件 `.html`（≤ 13 KB） | ✓ 逐件核许可 |
| [Sketchfab](https://sketchfab.com/) | image + title | 500k 可下载 | 3D 模型，无代码 | △ 剔除 NC 许可 |
| [OpenProcessing](https://openprocessing.org/) | image + title + desc | 1M+ | p5 草图 `.js` | △ 逐件核；限速 6 s |
| [Blender StackExchange](https://blender.stackexchange.com/) | title + desc | 123,167 问 / 115,066 答（脚本相关 13,632 + 6,738，几何节点 5,967） | 脚本片段 | ✗ 2024 年起转储禁训 |
| [Shadertoy](https://www.shadertoy.com/) | image + title† | 52,000+ | GLSL 片段着色器 | ✗ CC BY-NC-SA |
| [BlenderArtists](https://blenderartists.org/) | image + title + desc | 602,128 帖 / 581 万回复 | 帖子 + 少量 `.blend` | ✗ robots 全禁 |

✓ 可用　△ 有条件　✗ 不可用。desc = 正文或描述文本。† 站点对本机 403，未直连核实。Reference 列的核实过程见 Web 页 2.4。

- **许可在 Blender 这条线上是决定性的**：官方扩展目录 MIT 只有 4 个、传染性许可 1,341 个；问答站要求数据不用于模型训练。能规模化的合法路径只剩官方测试资产与自建合成。

### 2.5 Two Contractions

核心发现：真实素材挖矿在 3D 上的产出率比 Web 低一个数量级，所以主力必须是合成。

| Source | Name | Unit | Filter | Funnel | Retention |
|---|---|:-:|---|--:|--:|
| **GitHub** | three.js | 仓 | GitHub 搜「three.js」→ 主题标签 → 星 > 10 | 89k → **2.4k** | 2.7% |
| | Blender bpy | 仓 | GitHub 搜「blender addon」→ Python + 星 > 10 | 6.3k → **56** | 0.9% |
| | 本项目 three.js（估） | 页 | 上面 three.js 的 2.4k 仓 × 3 页 → 可用 | 7.2k → **≈230** | 3.2% |
| **HuggingFace** | [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) | 题 | 候选题 → 筛选 | > 10k → **2,026** | ≲ 20% |
| | [Objaverse-XL](https://arxiv.org/abs/2307.05663) | 文件 | GitHub 侧 3D 文件索引 → Blender 导入并渲染 | 37M → **5.5M** | 14.9% |
| **合成** | 槽位合成（本项目） | 题 | 参考场景 → 准入检查 | — | 88% – 96% |

Retention = 终点 ÷ 起点。three.js 一行分两段收缩：关键词噪音 3.7 倍（89,622 → 23,983）、星数门槛 10 倍。three.js 与 bpy 两行只筛标签与星数，没有可运行性检查；端到端可执行率另估为 three.js 1% – 8%、Blender 0.3% – 2%，唯一的实测锚点是 Objaverse-XL 的 14.9%。

- **真实挖矿决定分布，合成决定产能**：四条路线里只有合成的产能可控。

### 2.6 Slot Synthesis

3D 的题目主力是槽位合成：把参考场景里可调的参数做成槽位表，每个槽位标注类别、容差和对应的自然语言句式。

| 槽位 | 类别 | 容差 | 句式 |
|---|---|--:|---|
| 桌面尺寸 | 变换 | 0.5% | 「一张 {长}×{宽} 的木桌」 |
| 桌面倒角 | 修改器 | 2% | 「桌面边缘倒角 {值}」 |
| 灯泡功率 | 灯光 | 2% | 「点光源 {值} W」 |
| 灯臂旋转 | 动画 | 1% | 「灯臂第 1–40 帧从 {a}° 转到 {b}°」 |
| 杯身细分 | 修改器 | 0 | 「杯身加 {n} 级细分」 |

**难度有两个旋钮：钉死多少个槽位，以及槽位之间的依赖深度。** 它们比「让题目听起来更难」可靠，因为直接决定检查规则要查几个字段。

### 2.7 Reference Thickness

Query 这一侧的另一个变量：参考给到什么程度。参考越厚，Verifier 能查的东西越多。

- 唯一能直接参考模态配比的公开素材是一份 Blender 创作基准：223 个任务里，纯文本 78 条、图加文 130 条、视频加文 15 条，另有 59 个任务带尺寸、材质、相机规格的附件。**图加文占一半以上**，与 Web 页「文加图是模型评审的最佳工况」一致。
- 纯文本题目从零起极难过关：检查规则只能查题目钉死的字段，题目没写的不许查。这就是 3D 题目倾向于带参考的原因：不是为了好做，是为了检查规则有东西可查。

## 3 Verifier

Verifier 评估 Agent 在 Harness 里完成 3D Query 后交出的脚本或页面。与 Web 最大的不同在真值：**3D 的真值是场景图，可直接读出；固定随机源、同一容器重渲时噪声为零（条件见 3.3.3）。**

### 3.1 Overview

**问题**：3D 产物怎么分层评？

**结论**：先用程序检查 L0–L3，层层截断；全过了，才让模型在 L4 比好不好看。

术语（改坏的样本 / 换写法的样本、抓错率 / 放对率、Critic）见 Web 页 3.1。

- Functionality（功能性）：东西、参数、动画、摆放、交互对不对 → L0–L3（L0 能跑是前提）
- Aesthetics（审美性）：好不好看 → L4

本章：3.2 谁来评 → 3.3 功能 → 3.4 审美 → 3.5 验收 verifier → 3.6 前沿对照。

组合规则（同 Web 页 3.1）：

1. 全部满足才算过，不加权求和（本项目 Blender verifier 每条检查都是「且」）
2. 前层失败即截断：脚本报错，后面的几何和渲染不算
   - 截断也会放大取证链路自己的漏洞：第 4 章 4.2 的三个取证缺口（库引入方式、CDN 路径、断网拦截附加模块）都让正确页面在 L0 被整条判 0，看上去像模型连页面都写不对
3. 核心检查（题目钉死的项）不过直接 0 分；L4 只给全过的作品排名次
   - L4 与组内相对优势怎么拼（无人通过、仅 1 人通过、全组通过三种情况），见 Web 页 3.1 规则 3
4. 阈值在跑改坏的样本前冻结，后定的要标出。3D 阈值（本项目设定；通用规则见 Web 页 3.5）：

   | 阈值 | 值 | 怎么定 | 看样本前/后 | 有无独立验证 |
   |---|--:|---|:-:|---|
   | 图像相似度 | ≥ 0.995 | 按等价定 | 前 | 有：单张截图 12/22 |
   | 剪影交并比 | ≥ 0.97 | 按等价定 | 前 | 有：14/22 |
   | 点云距离 | ≤ 0.4% 对角线 | 按等价定 | 前 | 有：13/22 |
   | 体素交并比 | ≥ 0.80 | 按等价定 | 前 | 有：15/22 |
   | 逐部件 F 分数 | ≥ 0.99 | 换写法最低值 0.9989 反推 | 后 | 无 |

   <small style="color:#64748b">〔Blender〕台灯桌面场景，n = 22 样本 × 1 次（本项目实测）<br>剪影交并比：IoU，重叠 ÷ 合并；点云距离：Chamfer 距离，两组点云间平均最近距离；逐部件 F 分数：两组表面采样点在容差内能对上的比例，0.99 由换写法的样本里逐部件 F 最低值 0.9989 反推（本项目实测）<br>点云距离 0.4% 是距离上限，不是 3.3.4 的 F 分数匹配容差 0.5%<br>按等价定：按「什么算同一个场景」定，不从噪声推（见 3.3.3），具体依据原始记录未展开<br>有无独立验证：该信号单用的判对数（抓错 + 放对，满分 22）</small>

5. 代价：全部满足才给分 → reward 近似 0/1 → 整组全 0 或全 1 时没有梯度；对策：用要训练的模型自己的 pass@k 做难度过滤，再加动态采样（数字见 Web 页 3.1）
   - 〔three.js〕16 道修复题 × 8 次：13 题全对或全错，只有 3 题有梯度；0.3–0.7 难度带内 0/16（本项目实测，见 Web 页 3.1）

适用边界：本章的判别力数字只覆盖「修复单处破坏」类任务，从零生成见 3.5 第 5 条。

例题：Blender 脚本搭场景，木桌上放蓝色杯子，台灯灯臂第 1–40 帧从 0° 转到 40°。按图 3.1 逐层判；本例无交互，跳过 L3（L3 用于 three.js 游戏）。

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

| Taxonomy | Reward | Detail | Reference | Output | Used | Example |
|---|---|---|:-:|:-:|---|---|
| **L0 执行** | 执行检查 | 能跑完、出帧吗 | 任意 | `.py` / `.html` | [CAD-Coder](https://arxiv.org/abs/2505.19713) 等 | 不报错、非空白 |
| **L1 结构** | 场景图检查 | 物体参数对不对 | 文本 | `.py` / `.html` | [3JSBench](https://3jsbench.com/)† 等 | 杯子材质是蓝色吗 |
| | 动画曲线检查 | 关键帧对不对¶ | 文本 | `.py` | [MoVer](https://arxiv.org/abs/2502.13372)§ | 灯臂第 40 帧 40° |
| | 渲染设置检查 | 渲染参数对不对 | 文本 | `.py` | — | 帧范围恰为 1–40 |
| **L2 几何** | 逐部件几何 | 形状、位置对不对 | 图像 / 参考解 | `.py` / `.html` | [MeshCoder](https://arxiv.org/abs/2508.14879) 等 | 抓到杯子放错桌角 |
| | 逐颜色体素占据 | 各颜色的占位 | 图像 / 参考解 | `.html` | [cadrille](https://arxiv.org/abs/2505.22914)‡ 等 | 蓝块在杯子处 |
| | 拓扑量 | 网格有没有破洞 | 文本 | `.py` / `.html` | [CADTests](https://arxiv.org/abs/2605.07807)§ 等 | 封口杯破洞边数为 0 |
| **L3 行为** | 输入重放 + 状态差分 | 按键反应对不对 | 视频 | `.html` | [PlayCoder](https://arxiv.org/abs/2604.19742) 等 | 按「开灯」后灯亮 |
| **L4 美学** | 模型相对排序 | 挑更好看的 | 文加图 | `.py` / `.html` | [UI2Code^N](https://arxiv.org/abs/2511.08195) 等 | 过关场景只排名 |

<small style="color:#64748b">Output：`.py` = Blender 脚本（L0 另含 CadQuery `.py`），`.html` = three.js 页面（L3 为 three.js 游戏）<br>Used 其余出处：L0 [cadrille](https://arxiv.org/abs/2505.22914)；L1 [WorldCoder-Bench](https://arxiv.org/abs/2606.01869)†、[Code4Scene](https://arxiv.org/abs/2609.36777)†（未核实）；L2 逐部件几何 [Hi3DEval](https://arxiv.org/abs/2508.05609)、[CAD-Coder](https://arxiv.org/abs/2505.19713)‡、[BlenderGym](https://arxiv.org/abs/2504.01786)‡，体素 [BenchCAD](https://arxiv.org/abs/2605.10865)‡、[CAD-RL](https://arxiv.org/abs/2508.10118)‡，拓扑 [CADEngBench](https://arxiv.org/abs/2608.09296)§；L3 [A2Z GameSpec-Bench](https://arxiv.org/abs/2609.39564)；L4 [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)<br>渲染参数：引擎、分辨率、帧范围<br>† 只用于评测，L1 场景状态检查尚无当 RL reward 的先例（未核实）<br>‡ 简化版：逐部件几何行是全局几何，体素行不分颜色<br>§ 旁证：MoVer（2D 动画）、CADTests / CADEngBench（CAD）上的同类检查<br>¶ 时间轴上的静态检查</small>

依据：

- L1：〔Blender〕场景图与动画曲线在渲染图里看不见：删掉两条动画曲线，视觉指标全是 1.0000，只有逐关键帧检查抓到（本项目实测，n = 1 样本，取自 3.3.1 的 22 个）
- L2：〔Blender〕读几何又便宜又准（3.3.1 第 4 条）；〔CAD〕体素交并比已有在线强化学习先例（3.3.5、3.6）；〔three.js〕拓扑量能抓到像素和剪影都漏掉的破洞：参考 0、候选 64（n = 1 样本，3.2 第 4 条）
- L3：为什么要发输入，见 Web 页 3.1 依据

分层定了，谁来评？→ 3.2

### 3.2 Agentic Critic

**问题**：能不能让 VLM 当 3D 场景的评审？

**结论**：**VLM 不判题目钉死的属性对不对**（这类判断的失败是系统性的，见下面 1–3）；**可以在全部通过的作品之间做相对排序（即 L4）**；问题清单用来补程序检查（见 4）。相对排序的证据见 Web 页 3.3.3。

本项目实测（three.js 雪人场景，温度 0）：n = 18 样本 × 4 模型 × 2 视角 × 2 次 = 288 次判定，281 次有效。单视角 = 页面相机一张图，多视角 = 4 视角拼图，均与参考图上下并排。

1. 〔three.js〕几何错误会被「透视」解释掉：漏放（应挂判过）的判定里，理由拿取景、相机、透视或朝向说事的，单视角 4/8（50%）、多视角 4/6（67%）；原话「透视带来的视觉大小差异属于相机取景角度范畴，不算错误」
2. 〔three.js〕判对不等于说对原因：「鼻子长在后脑勺」（1 样本 × 4 模型 × 2 次 = 8 次判定）单视角全判挂，**但 0/8 的理由提到朝向或背面**，都说「缺少鼻子」（页面相机看不到后脑勺）。训练数据要按原因对不对打标，不能只按结论
3. 〔three.js〕程序检查稳定判挂，模型不稳定：两个改坏的样本（底球放大 20%、中球缩小 20%）逐颜色体素交并比 0.679、0.897，都在阈值外、都判挂（确定性，每例 1 次）；模型（单视角，每例 8 次判定）底球判对 4/7（1 次未解析），中球 8/8
4. 〔three.js〕真正的价值是发现漏掉的检查项，例：雪人破洞
   - 现象：旋转成型的雪人头顶有未封口的圆洞，人工标成「通过」；单视角像素分 1.000、多视角剪影交并比 0.998，程序检查全漏。模型多视角 8 次判定 7 次判挂，单视角 8 次全放过；复核多视角渲染，确认标签标错
   - 补检查：拓扑量「只被一个三角形用到的边数」，封口参考 0，该候选 64
   - 回正：多视角应放行的有效判定 64 次，放对 57 次（0.891），漏的 7 次全是该样本；剔掉它的 8 次后 56/56（1.000）

**凡是能被透视或取景解释掉的检查，一律不交给模型。**

那检查本身怎么做？→ 3.3

### 3.3 Functionality

**问题**：场景做对了没有，怎么评？

**结论**：读场景图和几何，不读代码，也不看渲染图；只查题目钉死的字段。

#### 3.3.1 How To Evaluate

1. 〔Blender〕九类场景状态每类单开（本项目实测，台灯桌面场景，n = 22 样本 × 1 次，确定性）：开发集 15 个（8 改坏 + 7 换写法）+ 留出集 7 个（3 + 4），合计改坏 11、换写法 11

   | 类别 | 查什么 | 关卡 | 抓错 /11 | 放对 /11 | 判对 /22 |
   |---|---|:-:|--:|--:|--:|
   | 层级与命名 | 名字集合、物体类型、父子关系、集合归属 | 条件进：只查点名物体 | 2 | 10 | 12 |
   | 变换 | 世界包围盒八个角点 | 不进† | 3 | 7 | 10 |
   | 网格统计 | 非流形边、体积符号、面数预算 | 不进‡ | 2 | 6 | 8 |
   | 修改器栈 | 修改器类型与关键参数 | 进 | 2 | 11 | 13 |
   | 材质节点树 | 节点类型与连边 | 条件进§ | 1 | 10 | 11 |
   | 灯光与相机 | 功率、色温、焦距、当前相机 | 进：只查白名单字段 | 2 | 10 | 12 |
   | 动画曲线 | 逐关键帧的时间、取值、插值，按帧求值 | 进 | 1 | 11 | 12 |
   | 物理与约束 | 约束类型、目标、影响系数、刚体字段 | 进 | 0 | 11 | 11 |
   | 渲染设置 | 引擎、分辨率、帧率、帧范围、采样、色彩管理 | 进：精确相等，无容差 | 0 | 11 | 11 |
   | 逐部件几何（单独） | 按材质色分组的 F 分数 | — | 7 | 11 | 18 |
   | 白名单组合 | 逐部件几何 + 四类¶ | 进 | **11** | **10** | **21** |
   | 九类全查 | 全部字段 | 反面教材 | 11 | 0 | 11 |

   <small style="color:#64748b">关卡 = 进不进推荐的最终判定：进 = 按字段比；条件进 = 只查一部分；不进 = 不按字段比，改用别的信号<br>† 不查局部位置与缩放，改用包围盒或几何指标<br>‡ 不进等式，只留不变量与不等式<br>§ 按类型与连边、不按节点名比，只查钉死的接口<br>¶ 修改器栈 + 灯光与相机 + 动画曲线 + 渲染设置</small>

   - 口径：逐部件几何读表面采样点，不在九类内，白名单组合的 11/11 不能直接比各类的 0–3/11
   - 物理与约束「进」但不在实测组合：本批无针对它的改坏样本（抓错 0/11），收它是因为静帧看不见约束
   - 抓错来源：逐部件几何单独漏的 4 个几何上看不见（灯泡调暗、动画删光、相机焦距改短、倒角删掉），由灯光与相机、动画曲线、修改器栈抓到。未测四类单独组合（不含逐部件几何）

2. 〔three.js〕四层信号，组合才满格（本项目实测：雪人 13 + 桌子 16 共 29 个带标签样本，含两类；n = 29 × 1 次；组合阈值在这些样本上看过，不算独立验证）

   | 信号 | 判对 |
   |---|--:|
   | 单张像素比对 | 12/29 |
   | 几何类别多重集 | 14/29 |
   | 多视角剪影交并比 | 19/29 |
   | 逐颜色体素占据 | 25/29 |
   | 四层组合 | **29/29** |

   - 留出 18/18：换场景（小车），n = 18 样本 × 1 次，两类都有，标签先贴、阈值未动；累计 47/47（29 + 18），18 个是真留出

3. 〔CAD〕真值最硬：尺寸、约束、实体有效性、可制造性全部确定；[BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) 约 1.8 万个参数化程序都经执行校验，「全部按执行结果判分，不用模型打分」（未核实）
4. 〔Blender〕读几何比看渲染又便宜又准（本项目实测，同上 22 个样本）：每样本几何全套约 0.4 秒、十视角渲染 1.1–1.2 秒；11 个改坏的里逐部件 F 分数抓 7/11、多视角剪影 3/11。**渲染图只给模型看，不判分**

为什么不干脆全查？→ 3.3.2

#### 3.3.2 Insight：Whitelist, Not All Fields

**问题**：九类状态能不能全开？

**结论**：不能。**全开会把换写法的样本全判错；只查题目钉死的字段，才能两头都对。**

本项目实测（Blender 22 个样本，n 同 3.3.1 第 1 条）：

- 〔Blender〕九类全查与白名单组合的抓错、放对数见 3.3.1 表；白名单组合唯一放错的是留出集「日光功率 3.0 调成 3.5」：题目只说加一盏日光、没钉死功率，却照查了。修法是移出白名单，不是放宽容差
- 〔Blender〕全查败在等价写法多：按名字比败给自动改名（同名材质节点自动加后缀），按局部变换比败给等价父子层级，按顶点数比败给等价细分

字段定了，阈值从哪来？→ 3.3.3

#### 3.3.3 Insight：Zero Noise Is Conditional

**问题**：阈值能不能从噪声推？

**结论**：不能。噪声在条件满足时是零，所以**阈值只能按「什么算等价」来定**；条件不满足时，噪声会吃掉分辨力。

本项目实测：

- 〔Blender〕参考解跑两遍（n = 1 样本 × 2 次）：图像 1.0000、点云距离 0.0000、体素交并比 1.0000，逐位为零
- 〔Blender〕条件 1 显式传采样种子：表面采样用采样库自己的随机源，全局种子管不到；不传时参考解自比点云距离 0.00167，与样本分布 0.0016–0.0065 同量级，而两类样本本就在此区间重叠
- 〔Blender〕条件 2 在任务容器里重渲：换 CPU 或图形栈版本像素会漂，参考图须在容器内用同一引擎重渲，不能用仓库存图
- 〔外部〕[Blender 官方渲染测试](https://github.com/blender/blender/tree/main/tests/files/render)阈值固定（单像素误差 > 0.016 的像素不超过 1%），某设备复现不了的测试进该设备黑名单，不放宽阈值（推断）

那容差选错会怎样？→ 3.3.4

#### 3.3.4 Insight：Tolerance Can Invert

**问题**：点云 F 分数的容差（多近算「对上了」）怎么选？

**结论**：选错，结论会反过来。**取对角线 0.5%，逐部件算**；下限不低于平均最近邻距离的 3 倍，该距离用参考解自采样两次估出，每个场景单算。

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
<figcaption>图 3.2　点云 F 分数的容差（本项目实测）：0.1% 时结论反转；0.5% 全局算仍重叠，须逐部件算；1% 时 7 个应该挂的（含留出集）只有 2 个低于 0.99。横轴三档不按比例</figcaption>
</figure>

本项目实测：n = 12 样本 × 4 档容差（0.1%、0.2%、0.5%、1%），各算 1 次。12 个取自 3.3.1 的 22 个：原始记录只列了 7 个改坏的（含留出集 2 个）和 5 个换写法的，未列另 4 个改坏的（换色、灯泡调暗、动画删光、相机焦距改短）。

1. 〔Blender〕容差小于采样间距，测的是采样密度而非几何（图 3.2）：取对角线 0.1%（2.2 毫米），换写法的细分样本 0.4977，**反而低于改坏的灯罩转反 0.9639**；六万个点铺在 2.18 米场景上，平均点距就有 3–5 毫米
2. 〔Blender〕容差太大，多数改坏的分不出：取 1% 时上述 7 个只有 2 个低于 0.99（灯罩转反 0.9847、桌腿少一条 0.9704），其余 5 个都在 0.99 以上
3. 〔Blender〕没有全局容差能分开两类：取 0.5% 时改坏的 0.9993、0.9985 与换写法的 0.9993 重叠；改逐部件算（每种材质色一组，取最差组）后换写法最低 0.9989，阈值取 0.99：抓错 7/11、放对 11/11（22 个样本，见 3.3.1 表）
   - 外推边界：按材质色分组会把同色部件合成一块，少一个同色部件就看不出；three.js 相对关系原型因此改为按颜色取连通块当部件（桌面与四条腿同色会合成一块，是原型设计时的描述，未单独测量）。逐部件 F 分数照此拆分的效果、部件多的复杂场景均未测
4. 两条取值规则可能冲突（推断）：本场景 0.5% 对角线 ≈ 10.9 毫米（对角线 2.18 米），而「不低于 3 倍平均点距」在点距 3–5 毫米时是 9–15 毫米，所以按结论取二者较大者

能否只用它当 reward？→ 3.3.5

#### 3.3.5 Insight：Single Metric Collapses

**问题**：能不能只用一个几何指标当 reward？

**结论**：不能。单指标会被钻空子，必须和执行检查、难度过滤一起用。

- 〔CAD〕只用点云距离当 reward：约 200 步后模型开始产出跑不起来的代码，训练中止（[CAD-Coder 附录 B](https://arxiv.org/abs/2505.19713)）
- 〔CAD〕配套做法：难度过滤只留 3 次采样平均 reward 低于 7.5 的题（[cadrille](https://arxiv.org/abs/2505.22914)，reward = 10×交并比，满分 10）；跑不起来的代码 CAD-Coder 记 0、cadrille 记 −10；本文默认记 0（与组合规则一致），记负分能否更快压掉不可执行输出，本项目未对比（未测）

功能之外，好看怎么评？→ 3.4

### 3.4 Aesthetics

**问题**：3D 场景好不好看，怎么评？

**结论**：**本项目素材没覆盖 3D 审美。** 能程序查的只是「物理上自不自洽」；公开 3D 评测器和人的两两一致率，已发表最高是 GPTEval3D 自报的 78.9%，换到别家数据只有 65%–69%。

1. 〔外部〕公开 3D 评测器测资产质量，不测交互与功能
   - [GPTEval3D](https://arxiv.org/abs/2401.04092)：自家数据两两一致 78.9%、Kendall τ（排序一致性系数）0.710；别家数据复测 3DGen-Bench 67.7%、Hi3DEval 65%–69%
   - [3DGen-Bench](https://arxiv.org/abs/2503.21745)：自家评分器 72.5%；1,020 条提示、11,220 个资产、68,000+ 偏好投票
   - [Hi3DEval](https://arxiv.org/abs/2508.05609)：自家数据物体级 70%–77%；[MATE-3D](https://arxiv.org/abs/2412.11170)：1,280 个网格、107,520 条多维度标注
   - 〔外部〕对照：网页侧模型评审两两一致 91%–94%（[ArtifactsBench](https://arxiv.org/abs/2507.04952) / [UI2Code^N](https://arxiv.org/abs/2511.08195)）；数据集不同，「3D 低一截」只是推断；这是实测一致率，不是门槛，测的是网页评审，与 3D 偏好数据口径不同
2. 〔外部〕能程序查的是「物理自洽」，不是审美：[3JSBench](https://3jsbench.com/) 有 98 条渲染质量检查（网格预算、可见背面、绘制顺序）
   - 五大失败：穿插 20%、可见背面 19%、闪烁 17%、朝向 16%、断开 16%；前三类属渲染层面的物理不自洽（本项目归类，非站方原话）
   - 网格预算：Muse Spark 1.3 中位 995 个网格、177,000 个三角面，Astra 45 个，Fable 5.1 24 个；Muse 有 33% 的尝试出现闪烁
3. 〔外部〕嵌入相似度当 3D 质量关卡没用：3JSBench 上 11 个模型的 SigLIP2 均值全在 0.0774–0.1081；Astra / Opus 5.5 / GPT-6 Sol 通过率 80.0% / 49.0% / 27.0%，SigLIP2 原始均值 Astra 0.1081 对 Opus 5.5 0.1067 只差约 0.001，减去每题平均后三者只高 +0.011 / +0.009 / +0.007
4. 〔外部〕数据过滤用的美学分：[Objaverse-XL](https://arxiv.org/abs/2307.05663) 用 LAION 美学分分三档，外加坏渲染分类器（1,200 条人工标注训练，阈值 0.5）；Polycam 来源的渲染图 38.20% 被判坏

3D 的 L4 目前只做模型两两比较（见图 3.1）；网页侧的排版类程序检查在 3D 场景里没有对应物，未实测。

检查本身怎么验收？→ 3.5

### 3.5 Discrimination

**问题**：怎么知道 3D verifier 本身靠谱？

**结论**：**标签也会出错，一个错标签就能让结论反过来**（本项目 1 例）；先复核标签，再下「检查规则不准」的结论。

1. 验收指标同 Web 页 3.5：抓错率、放对率、Youden 指数，各配置信区间（一般 Wilson 95% 区间；一次都没出错时，出错率的 95% 上界 ≈ 3 ÷ n）
2. 〔three.js〕一个错标签就能让结论反过来：雪人破洞样本（本项目实测，见 3.2 第 4 条）
3. 两条事先定的规矩：换写法的样本有 3 个以上模型一致判挂时，先复核标签再谈放对率；给换写法的样本打标签前，先看多视角渲染
4. 独立证据只算阈值冻结后才见到的样本，后定的逐部件 F 分数（见 3.1 组合规则 4）不算
   - 〔three.js〕组合判定只有换场景留出的 18/18 算独立（本项目实测，n = 18 样本 × 1 次）；但 18 个都是小车这一个场景的改动，跨场景独立样本数为 1
     - 在该场景的改动上：Wilson 95% 下界 0.824，即准确率 ≥ 82.4%；出错率 95% 上界 ≈ 3 ÷ 18 ≈ 16.7%（均为本项目推算）
     - 分开给：抓错 11/11（Wilson 下界 74.1%）、放对 7/7（下界 64.6%）（计数来自本项目原始记录，下界为本文推算）；换到别的场景没有统计保证
   - 〔Blender〕白名单组合不算：成员看过开发集 15 个样本才选定，逐部件 F 的 0.99 后定
   - 〔Blender〕先冻结的四个阈值算独立（22 个样本都在冻结后才见到），但单用只判对 12–15/22（见 3.1 阈值表）
5. 适用边界：本页判别力数字（29/29、47/47、18/18、Blender 21/22）都来自「修复单处破坏」类任务
   - 〔three.js〕从零生成时现有检查规则 0/26，其中 23 组挂在剪影层；抽看的 4 个产物人看都对，挂的原因是比例与参考不重合（本项目实测）
   - 〔three.js〕只看相对关系的原型救回 13/80，代价是三场景带标签样本 47/47 → 35/47（本项目实测）
   - 分母：32 组（场景 × 模型 × 有无参考图）中有效 26 组，0/26 按组计（每组最多 3 轮）；13/80 按同一批实验的每次尝试计，80 的精确构成原始记录未交代（未核实）
6. 准入：初始状态（什么都不改）必须判挂，否则原样交回也能拿分（本文建议）

阈值来源见 3.1 组合规则 4 的阈值表。

前沿实验室也这么做吗？→ 3.6

### 3.6 Frontier Lab

**问题**：前沿实验室在 3D 方向披露了什么？

**结论**：**所查来源都没披露 3D 训练方法**，只有演示和基准分数；国内没有一家披露 Blender 训练数据（推断）。

| 来源 | 披露了什么 | 没披露什么 | 出处 |
|---|---|---|---|
| OpenAI 游戏 | 渲染计数器、帧间隔采样、像素差分‡ | 训练数据、视觉 reward 模型§ | [Astra 游戏博客](https://developers.openai.com/blog/how-to-build-games-with-astra) |
| OpenAI 建筑可视化 | bpy 建场景，computer use 打开 Blender 检查¶ | 同上 | [Astra 建筑可视化博客](https://developers.openai.com/blog/architectural-visualization-with-astra) |
| Anthropic 产品 | 提到 shaders、3D 原型能力 | 3D 训练‖ | [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) |
| Anthropic 系统卡 | BenchCAD 体素交并比 0.366 → 0.821† | 同上 | [Opus 5 系统卡 §8.12](https://www.anthropic.com/claude-opus-5-system-card) |
| Kimi K3 | 3D「代码 ↔ 渲染」配对进预训练※ | 3D 侧的 reward 设计 | [Kimi K3 §3.1](https://arxiv.org/abs/2607.24653) |
| MiMo-V2-Flash | 录屏判别# | 3D 专项数据 | [MiMo-V2-Flash](https://arxiv.org/abs/2601.02780) |
| Qwen3.8-Max | QwenBlenderBench 69.9（未核实） | 打分方法 | —* |

<small style="color:#64748b">† 唯一的 3D 量化：BenchCAD Vision2Code 工具消融，Opus 5；1,000 个文件的子集，5 次平均<br>‡ three.js 渲染计数器（绘制调用、三角面、几何体、纹理）、90 个帧间隔采样、特效开关像素差分；无阈值<br>§ Blender 与游戏训练数据、视觉 reward 模型（建筑可视化行同）<br>¶ 原文：几何检查「不替代看渲染图」<br>‖ 检索 Claude 4 到 Opus 5.5 共 9 份 system card，无一讲 3D 训练（本项目检索；系统卡行同）<br>※ 唯一把 3D 资产、游戏、CAD 的「代码 ↔ 渲染」配对写进预训练<br># 可解 three.js 动态场景单帧看不全（本项目推断）<br>* 内部基准，未找到公开出处</small>

基准对照：

- 〔CAD〕BenchCAD 是两家都报过分的唯一 3D 基准，口径不同、不能直接比：OpenAI 发布页（[GPT-6 Astra](https://openai.com/index/gpt-6-astra/)）Astra 95.9%、GPT-5.6 Sol 83.3%，转引 Fable 5.1 84.3%（几何重叠分）；Anthropic 体素交并比 0.366 → 0.821（见上表）
- 〔外部〕3JSBench（同一套确定性检查）：Astra 80.0%、Fable 5.1 69.3%、Opus 5.5 49.0%、GPT-6 Sol 27.0%、Kimi K3 23.0%

〔外部〕学术侧：CAD 已有「能执行才给分 × 交并比」的在线强化学习（[cadrille](https://arxiv.org/abs/2505.22914)、[CAD-RL](https://arxiv.org/abs/2508.10118)）；three.js 和 shader 只有基准，没有强化学习论文（本项目检索，截至 2026-10）。

可照抄的仍是网页侧做法（见 Web 页 3.6）：出题与收题、检查规则写法、打分系统本身；「用什么模型、配比多少」所查来源都没公开。

## 4 Harness: Blender Forks By Version, three.js Need Not

- 这是 3D 运行环境和 Web 最不一样的一处：Blender 要按版本分叉。
- 证据强度先交代：Blender 侧的多版本适配有多条本机实测；three.js 侧的「免适配」只有一条半实测加一条推断，而且本项目在 three.js 侧也踩到过三个适配坑。
- 所以正确的说法不是「three.js 不需要版本适配」，而是「**three.js 的版本适配成本可以压到接近零，Blender 的不能**」。

### 4.1 Blender: One Version, One Python Runtime

核心发现：**支持 N 个 Blender 版本，等于要维护 N 个 Python 运行时。** 这是镜像分层的硬约束，不是可以调的参数。

- 起因是被迫的，不是为了做实验：系统包管理器给的是旧版的旧渲染引擎，另装的长期支持版带新渲染引擎，本机只能两个版本并存
- 硬约束在 Python：发行包的每个版本只绑一个 Python 小版本
  - 4.0 绑 3.10
  - 4.1 到 5.0 绑 3.11
  - 5.1 与 5.2 绑 3.13
- 版本可得性本身就是供给风险
  - 4.0 和 4.1 已从公共包索引下架，要去官方站点取
  - 内网镜像列着 4.2 到 4.4 但下载全部失败，只能走海外代理：一次装机 121 秒、包体 784 兆

不适配的后果，全部是实测踩到的：

| 不兼容 | 症状 |
|---|---|
| 渲染引擎标识符跨版本改名 | 同一份脚本在两个版本上必须传不同的引擎名，而分支判断不匹配时是**静默失败**，不报错 |
| 新渲染引擎的图形能力要求更高 | 新引擎官方要求的图形接口版本与扩展，旧引擎不要求；无 GPU 环境只能走软件光栅，而官方没说这条路支不支持 |
| 新引擎在软件光栅上慢 4 到 5 倍 | 八视角 512 分辨率：旧引擎 7.3 秒，新引擎 33.1 秒；首帧着色器编译 3.2 秒对 13.3 秒；之后每视角 0.6 秒对 2.8 秒 |
| 无头回退路径是实测出来的，不是文档写的 | 两个版本的日志走的是两条不同的回退链 |
| 运行时是全局单例 | 一个脚本把全局设置调歪了会污染后面所有任务，所以每个候选必须起独立进程——而 2.3 秒里约 0.5 秒就是进程启动与运行时导入 |
| 指定渲染引擎只改当前场景 | 工程文件里其他场景照旧要求显示，无头环境下直接失败 |
| 视口着色取的是视口颜色，不是材质基色 | 不同步过去渲出来全是默认灰 |

### 4.2 three.js: Pick The Capture Channel, Not The Version

核心发现：**three.js 的免适配不是天生的，是选对取证通道换来的。** 走原型补丁的路线需要版本适配，走库自己派发的取证事件就不需要。

- 本项目的做法：运行环境预先放好一个事件靶，库的场景与渲染器构造函数会主动向它派发事件
  - 这条通道不依赖库的版本细节，也不依赖模型配合
  - 三种引入方式结果一致：公共 CDN、模块映射、把库整个内联进页面不发任何网络请求，三者读出的网格数与体素完全相同
  - 这一步的保留率约 95%
- 反面教材恰恰是版本适配：早期把钩子打在原型方法上
  - 在某个版本上捕获不到场景，因为那个版本把渲染方法挂在了实例上，要在构造后再包一层
  - 换成库自己派发的事件之后，这个问题消失
- 公开对照印证：有一个基准走「锁死本地库版本 + 页面加载前打补丁原型方法」这条路，所以**它必须锁版本**

三个取证缺口必须一起写：它们都在取证链路而不是检查规则里，表现出来是「模型连页面都写不对」，很容易被当成模型能力问题记下来。

| 缺口 | 模型写的是什么 | 症状 |
|---|---|---|
| 只拦模块那条引入路径 | 用经典脚本标签引入 | 库未定义、超时无渲染，执行门判不通过 |
| 拦截规则写死了路径结构 | 从另一个 CDN 引入，路径结构不同 | 同上 |
| 断网把附加模块一起拦了 | 用了库自带的几何工具模块 | 模块加载失败，执行门判不通过 |

- 修法：同时服务另一种构建；只按文件名判、不按路径判；本地有的模块直接服务
- 改完三个变异集回归仍是 13/13、16/16、18/18
- 由此得到一条验收要求：**运行环境的覆盖面要单独验收**
  - 至少覆盖：库的各种引入方式、常见的渲染循环写法、模型可能用的各种版本
  - 拿真实策略的产出去跑，不拿自己写的参考解去跑

### 4.3 Two Discounts

- **跨 three.js 版本的确定性从没测过。**
  - 公开证据是反向的：超越函数的精度不被语言规范要求，跨引擎版本会分叉；某物理库在两个相隔较远的引擎版本之间结果不同，简单场景一致、复杂场景分叉
  - 所以版本要钉死，不要假设能跨；本项目也只测过一个浏览器版本
- **「两条线的产出率差 3 到 5 倍」只是估计。**
  - 可执行率那一列整列都是估，唯一的实测锚点是公开资产集的 15%
  - 引用时必须带上这个标注

### 4.4 Cost: Blender Per Task, three.js Per Step

核心发现：**39 倍的差距来自技术栈，不来自算法。**

| | three.js | Blender |
|---|---|---|
| 单题耗时 | 383 毫秒 | 2.3 秒 |
| 折成单位成本 | 3.35 核秒 | 24.7 核秒 |
| 一轮 1024 条 rollout | 多轮形态 43 核 | 单轮形态 1670 核 |
| 多视角 | 八视角一次求值内渲完再导出 192 到 202 毫秒 | 十视角 1.2 秒，每视角 0.1 秒 |
| 读场景图 | 1.8 毫秒 | 0.1 到 1 毫秒 |

数据解读：

- 这个差距直接决定难度估计的预算
  - Blender 线单视角单题 24.7 核秒，照 256 次采样乘 3 个种子算是每题 5.3 核时
  - 三千道题就是一万六千核时，和跑一轮 RL 同量级
- 所以 3D 侧只能用训练中的在线正确率估难度，离线跑高预算通过率这条路不可行

GPU 这件事可以定论：

- Blender 的多个版本都能在无 GPU、无显示的机器上跑三种渲染引擎；three.js 走软件光栅后端
- 公开沙箱平台里没有一家写明支持 GPU 加图形栈：**想要真 GPU 光栅得自己做镜像，CPU 方案能省掉这一整套**

