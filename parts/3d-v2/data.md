Task = Query + Verifier + Harness，三件都从同一批素材里切出来；本页只讲素材。

- 素材：可公开获取的原始物件，如场景文件、脚本、网格、渲染图；同一份素材可拆成 Query、Verifier 的参考答案或 Hint（训练时给模型的部分答案信息，评测时不给）
- 其余两页：Verifier 给轨迹打 reward；Train 讲 Harness 与三件的组合用法

## 1 Three Parts

缺任何一件，素材只是数据，不是可验证任务。和 Web 比，3D 的题目更难凑，Verifier 更好做，Harness 最贵。

| 件 | 3D 上的形态 | 缺了会怎样 |
|---|---|---|
| Query（全称 Omni Reference Query） | 需求描述，加上参考：参考图或多视角图、起始场景与脚本、点云、参考视频 | 资产库再大也只有模型文件，凑不成「指令 → 代码」的配对 |
| Verifier | 读场景图与几何的程序检查（L0–L3），全过之后才让模型比好不好看（L4） | 没有 reward，只能人看渲染图 |
| Harness | Blender 按版本分叉的无头运行时；three.js 无头浏览器加取证事件靶；显式采样种子、容器内重渲 | 产物跑不起来，场景图读不出来 |

| | Web (2D) | 3D |
|---|---|---|
| Query 来源 | 有真实线上 Query 分布 | 几乎没有真实 Query 分布，主要靠参考素材反推与槽位合成 |
| 真值形态 | DOM 与计算样式 | 场景图：几何、材质、修饰器、求解器、动画曲线 |
| 噪声地板 | 231 个可观测字段里 4 个会变 | 参考解跑两遍，图像、点云距离、体素占据全部逐位相同 |
| 运行环境 | 一个浏览器镜像挂几百道题 | Blender 要按版本分叉，three.js 不必 |
| 单题成本 | 4.9 秒 | Blender 2.3 秒，three.js 383 毫秒 |

## 2 Material

供给上限由来源决定：3D 素材资产多、代码少，高质量作品集中在官方与头部维护者手里，题目主力因此靠合成。

### 2.1 Overview

可挖来源分 GitHub、HuggingFace、Website 三类，资产多、代码少：只有 CAD 有成规模的公开配对数据，Blender 的代码来源收缩到两位数，three.js 没有公开的训练配对集。

- 图码配对：一张截图与生成它的源码
- Golden Images：渲染引擎的仓库为每份测试代码存的标准答案截图；每次改代码后重新渲染、与它逐像素比对，这种测试叫视觉回归测试（Visual Regression Testing，VRT），因此代码与截图天然成对

**Artifacts 词表**：全书来源表共用六类标签，颜色即类别。

<!--ARTIFACTS-->

1. 一个标签只写一个物件。
2. 同义词归一：渲染结果、GUI 截图都写「截图」。
3. 限定语写进括号，如 `bpy .py（分部件）`；文件类型直接写扩展名。

| Source | Type | Datasize | Example | Artifacts |
| --- | --- | --: | --- | --- |
| **GitHub** | Golden Images | 2,564 图 · 916 图 · 613 图 | [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) · [Babylon.js](https://github.com/BabylonJS/Babylon.js) · [three.js examples](https://github.com/mrdoob/three.js) | <span class="art a-img">截图</span><span class="art a-run">.blend</span><span class="art a-code">.ts</span><span class="art a-run">.html</span> |
|  | 带星脚本 / 页面仓库 | 56 仓 · 2,401 仓 | Blender bpy 仓库 · three.js 仓库 | <span class="art a-code">.py</span><span class="art a-run">.html</span> |
|  | 程序化生成器 | 无上限 | [Infinigen](https://github.com/princeton-vl/infinigen) | <span class="art a-run">Blender 场景</span><span class="art a-asset">网格（OBJ / USD）</span> |
| **HuggingFace** | 文本 / 点云 / 图 → 代码配对集 | 205 – 970,937 | [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) · [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) · [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | <span class="art a-txt">描述</span><span class="art a-asset">点云</span><span class="art a-img">截图</span><span class="art a-code">bpy .py</span><span class="art a-code">CadQuery .py</span> |
|  | 资产库（无代码） | 10.85M 行元数据 | [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | <span class="art a-asset">网格</span><span class="art a-meta">元数据</span> |
| **Website** | 问答站 / 论坛 | 20.9k – 602k | [Blender StackExchange](https://blender.stackexchange.com/) · [BlenderArtists](https://blenderartists.org/) · [three.js 论坛](https://discourse.threejs.org/) | <span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-code">代码片段</span> |
|  | 资产站 | 2,387 – 500k | [Sketchfab](https://sketchfab.com/) · [Poly Haven](https://polyhaven.com/) | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-asset">网格</span><span class="art a-asset">HDRI</span> |

- Artifacts 列：该渠道直接拿到的物件

1. 资产不是题目：资产库给的是模型文件不是脚本，只能当素材池与渲染基线。
2. 公开供给与主力技术栈错位：Blender 与 three.js 是主力，公开配对数据却集中在 CAD，因此 3D 的自建比例必须比 Web 高。
3. 没有找到批量挖掘 Blender 脚本的公开工作，这是缺口，不是可抄的路。

### 2.2 GitHub

GitHub 上有三类来源，成熟度各不相同：

- **Golden Images**（测试用的标准答案截图）：截图和代码天然配对，但只能检查「像不像」，且一部分拿不到
- **脚本仓库**：数量大，但只筛过标签与星数，可运行比例没有核验
- **程序化生成器**：Infinigen 这类，产能没有上限，给的是场景，不是题

#### 2.2.1 Golden Images

Golden Images 是测试里存的「标准答案截图」。渲染引擎的测试仓库为每个测试场景或每份代码存一张截图，持续集成每次渲染后逐像素比对，所以这类仓库里代码和截图天然配对。

3 个仓库共 4,093 张截图，一图一码的只有 three.js 与 Babylon.js。

| Repo | Datasize | Artifacts | Permitted |
| --- | --: | --- | --- |
| [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) | 2,564 图 / 839 场景（3.1 : 1），46 类 | <span class="art a-img">截图</span><span class="art a-run">.blend</span> | △ GPL | — |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js) | 916 图 / 906 份代码（1 : 1） | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-code">.ts</span> | △ Apache-2.0，代码在 Playground | — |
| [three.js examples](https://github.com/mrdoob/three.js) | 613 图 / 613 页（1 : 1） | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-run">.html</span> | ✓ MIT | — |

- 口径：图数与码数为 2026-10-20 各仓库 HEAD 实数（three.js 示例 10-28 已增至 616 页）；Babylon.js 906 份代码里 888 份存在外部 Playground，仓库只存 id

1. 配对的另一端是截图，因此只能支撑视觉相似度，不能支撑运行时契约。
2. 有基线却不能用的仓库必须排除，否则高估供给。
   - react-three-fiber 主仓：0 张图；示例已迁到 pmndrs/examples，211 个示例一例一图（见 2.4）
   - PlayCanvas：296 个示例、592 张缩略图，但没有比对
   - Godot：238 个文件，只有 1 张图
3. three.js 示例库小到能整个放进上下文，因此模型不用先检索再写。
   - 全树 6,413 个文件；示例页单页中位 6,137 字节、95 分位 13,651、最大 66,143，总体积 4.4 MB；可用接口 1,251 个
   - 示例页按渲染后端分：WebGL 298 / WebGPU 234 / WebXR 27 / 其他 23（共 610，早于 613 的实数，口径待统一）

#### 2.2.2 Scripts

脚本仓库数量大，但筛到能用的只剩两到四位数，且可运行比例没有核验。

| Repo | Datasize | Artifacts | Permitted |
| --- | --: | --- | --- |
| Blender bpy 仓库 | 6,307 → 56 可用 | <span class="art a-code">bpy .py</span> | 逐仓许可 |
| three.js 仓库 | 89,622 → 23,983（主题标签）→ 2,401（星 > 10） | <span class="art a-run">.html</span><span class="art a-code">.js</span> | 逐仓许可 |
| Blender 官方扩展目录 | 1,533（1,256 插件 + 276 主题） | <span class="art a-code">.py（插件）</span> | ✗ 传染性许可 1,341，MIT 只有 4 |
| [Infinigen](https://github.com/princeton-vl/infinigen) | 无上限（生成器） | <span class="art a-run">Blender 场景</span><span class="art a-asset">网格（OBJ / USD）</span> | ✓ BSD-3 | — |

1. bpy 仓库大多依赖工程文件、资产路径与插件，开箱即跑的比例口径待补。
   - 口径：GitHub 搜「blender addon」→ Python + 星 > 10，6,307 → 56
2. three.js 仓库只按主题标签与星数筛过，可运行比例口径待补。
   - 89,622 → 23,983（主题标签）→ 2,401（星 > 10）
3. 官方扩展目录以传染性许可为主，不能直接用。
   - 1,533 个里传染性许可 1,341 个，MIT 4 个
4. Infinigen 是生成器而不是数据集，产能没有上限。

### 2.3 Datasets

公开 3D 配对数据集中在 CAD：十万量级的有五个；Blender 有 BlendNet（1.2 万）、3DCode（1.27 万，MIT）与 MeshCoder（10 万）；three.js 只有 WorldCoder-Bench 公开的 205 题。

| Dataset | Datasize | Artifacts | Permitted | Example |
| --- | --: | --- | --- | --- |
| [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) | 12,059 | <span class="art a-txt">描述</span><span class="art a-code">bpy .py</span> | ✓ Apache-2.0 | — |
| [MeshCoder](https://huggingface.co/datasets/InternRobotics/MeshCoderDataset) | 100K（论文约 1M） | <span class="art a-asset">点云</span><span class="art a-code">bpy .py（分部件）</span> | △ CC-BY-SA-4.0，需申请 | — |
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) | 280（论文 245） | <span class="art a-img">多视角图</span><span class="art a-code">.py（起始）</span><span class="art a-code">bpy .py（编辑后）</span> | ？未声明许可 | — |
| [WorldCoder-Bench](https://huggingface.co/datasets/shuolucs/WorldCoder-Bench) | 205（论文 2,026） | <span class="art a-txt">描述</span><span class="art a-asset">网格（GLB）</span><span class="art a-run">.html</span> | ✓ CC-BY-4.0 | — |
| [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) | 970,937 + 968 | <span class="art a-asset">点云</span><span class="art a-code">CadQuery .py</span> | △ CC-BY-NC-4.0 | <!--EX:CAD-Recode--> |
| [Omni-CAD](https://huggingface.co/datasets/jingwei-xu-00/Omni-CAD) | 313,096（论文约 450K） | <span class="art a-txt">描述</span><span class="art a-img">多视角图</span><span class="art a-asset">点云</span><span class="art a-code">CAD 序列（命令）</span> | ✓ MIT | — |
| [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) | 论文 17.8 万（未核实际条数） | <span class="art a-code">CAD 序列（构造）</span> | ？代码 MIT，数据未声明 | — |
| [Text2CAD](https://huggingface.co/datasets/SadilKhan/Text2CAD) | 论文约 170K 模型 / 660K 文本 | <span class="art a-txt">描述（多级）</span><span class="art a-code">CAD 序列（命令）</span> | △ CC-BY-NC-SA-4.0，需申请 | — |
| [GenCAD-Code](https://huggingface.co/datasets/CADCODER/GenCAD-Code) | 162,848 | <span class="art a-img">截图</span><span class="art a-txt">指令（固定）</span><span class="art a-code">CadQuery .py</span> | ？未声明许可 | — |
| [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | 21,048 | <span class="art a-img">多视角图</span><span class="art a-code">源码</span><span class="art a-txt">指令（编辑）</span><span class="art a-code">CadQuery .py</span> | ✓ CC-BY-4.0 | — |
| [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | 10,850,997 行元数据 | <span class="art a-asset">网格</span><span class="art a-meta">元数据</span> | △ ODC-By，单个对象各有许可 | <!--EX:Objaverse-XL--> |

- 标记：✓ 宽松许可，△ 有条件，？未声明
- 口径：2026-10-20 读自各数据卡、文件列表与 LICENSE

1. 非商用许可的数据集不能进商用训练。
   - CAD-Recode（CC-BY-NC-4.0）、Text2CAD（CC-BY-NC-SA-4.0）、3DCodeVerse（CC-BY-NC-SA）；Objaverse-XL 的 Polycam 部分仅非商用
2. BenchCAD 带代码生成、编辑、问答三类任务，但数据卡没写判分方式。
   - 17,900 条代码生成、748 条编辑、2,400 条问答

### 2.4 Website

高质量 3D 作品按能拿到什么分档：three.js 看 pmndrs/examples 与官方示例，都是一个示例配一份可运行代码；Blender 现成的代码配对只有 3DCode，其余多是只有 .blend 的场景与资产；问答站与论坛只给片段。

<!--SITE:3d-->

- 标记：✓ 可用，△ 有条件，✗ 不可用；NC 类许可科研可用、不可商用
- 口径：2026-10-28 本机实测（GitHub API、raw 文件、HF API、站点 API 与页面）

**一、慎用**

慎用来源的问题都出在许可与获取上：条款禁训、只许非商用、权属不清、要付费，或内容本身是别家模型的输出。

1. 条款禁止训练，或抓取被封。
   - Blender StackExchange 与 Stack Overflow 的转储禁止用于训练；BlenderArtists 的抓取代理被全量封禁
   - Sketchfab 带 NoAI 标签的模型禁用于生成式 AI（Staff Pick 可下载 2,514 个里 323 个）
2. 只许非商用：科研可用，不可商用。
   - Shadertoy 与 three.js 论坛的用户内容默认 CC BY-NC-SA 3.0；[3DCodeVerse](https://huggingface.co/datasets/ilabai/3dcodeverse) 约 203 万行，整体 CC-BY-NC-SA
3. 许可声明与来源权属不符。
   - [BlenderLore](https://huggingface.co/datasets/FreedomIntelligence/BlenderLore)：21,449 个 .blend 标 Apache-2.0，但来自 B 站教程配套工程
   - img2threejs 展示库：没有 LICENSE，题材含游戏 IP
   - Blender 官方扩展目录 1,533 个里传染性许可 1,341 个、MIT 4 个
4. 拿不到或要付费。
   - Blender Studio：可下载文件里带 .blend 的 164 个，免费的只有 15 个；Three.js Journey 付费
5. 内容是别家模型的输出，不能当答案。
   - 3DCodeVerse 的 three.js 子集全由编码 agent 生成

**二、按题型选**

three.js 两个来源分别适合着色器题与工程题，Blender 的代码题靠 3DCode，编辑题与节点题靠官方 .blend。

| 题型 | 首选来源 | 依据 |
|---|---|---|
| 写着色器 | three.js 官方 examples | 32% 自写着色器，51% 是不加载外部资产的纯代码页 |
| 工程补全、后处理 | pmndrs/examples | 后处理 36%，一个示例一个可运行工程 |
| 长上下文程序化建模 | 3DCode | 脚本中位 919 行，48% 用几何节点 |
| 编辑题的起始场景 | 官方 demo 文件、Open Data 场景、Big Buck Bunny | 生产级 .blend，扰动后让模型改回 |
| 节点树重建 | 官方 demo 的几何节点区、内置资产 | 几何节点文件 22 个；内置资产 CC0 |

## 3 Funnel

3D 素材从仓库或资产索引走到可训任务，同样要过标签、星数、可运行几道关。真实挖矿只筛标签与星数就剩 0.9%–2.7%，可运行性还没核验，因此真实素材只定分布，题目主力靠合成。

- 口径：留存率 = 终点 ÷ 起点；GitHub 各行只筛标签、星数或许可，没有可运行性检查；Website 三行止于许可干净的可用素材，不产出任务

| Source | Name | Unit | Filter | Funnel | Retention |
|---|---|:-:|---|--:|--:|
| **GitHub** | three.js | 仓 | GitHub 搜「three.js」→ 主题标签 → 星 > 10 | 89k → **2.4k** | 2.7% |
| | Blender bpy | 仓 | GitHub 搜「blender addon」→ Python + 星 > 10 | 6.3k → **56** | 0.9% |
| | 本项目 three.js（估） | 页 | 上面 three.js 的 2.4k 仓 × 3 页 → 可用 | 7.2k → **≈230** | 3.2% |
| | three.js 高星仓库 | 仓 | topic:threejs 且星 > 1000 → MIT | 106 → **65** | 61% |
| **HuggingFace** | [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) | 题 | 候选题 → 筛选 | > 10k → **2,026** | ≲ 20% |
| | [Objaverse-XL](https://arxiv.org/abs/2307.05663) | 文件 | GitHub 侧 3D 文件索引 → Blender 导入并渲染 | 37M → **5.5M** | 14.9% |
| **Website** | [Experiments with Google](https://experiments.withgoogle.com/) | 实验 | 全部实验 → WebGL 标签 → 带 GitHub 源码 → 宽松许可 | 1,654 → 664 → 85 → **30** | 1.8% |
| | [Blender 官方 demo 文件](https://www.blender.org/download/demo-files/) | 文件 | 页面直链 → 标 CC0 / CC-BY | 87 → **50** | 57% |
| | [Sketchfab](https://sketchfab.com/) | 模型 | Staff Pick 且可下载 → CC-BY / CC0（NoAI 标签未剔除） | 2,514 → **1,926** | 77% |
| **合成** | 槽位合成（本项目） | 题 | 参考场景 → 准入检查 | — | 88% – 96% |

**一、真实挖矿**

真实挖矿的产能是三位数，只够定分布，撑不起题库。

1. 只筛标签与星数就剩 0.9%–2.7%。
   - three.js：89,622 → 23,983（主题标签，关键词噪音 3.7 倍）→ 2,401（星 > 10，再收 10 倍）
   - 端到端可执行率另有估算：three.js 1%–8%、Blender 0.3%–2%；估算口径待补
2. 唯一的可运行实测锚点是 Objaverse-XL 的 14.9%。
   - 3,700 万个文件里，550 万个能被 Blender 导入并渲染
3. 本项目 three.js 路线估算约 230 个任务。
   - 2.4k 个仓库 × 每仓 3 页 → 可用（估）

**二、合成扩产**

槽位合成把参考场景里可调的参数做成槽位表，准入留存 88%–96%，产能可控。

| 槽位 | 类别 | 容差 | 句式 |
|---|---|--:|---|
| 桌面尺寸 | 变换 | 0.5% | 「一张 {长}×{宽} 的木桌」 |
| 桌面倒角 | 修改器 | 2% | 「桌面边缘倒角 {值}」 |
| 灯泡功率 | 灯光 | 2% | 「点光源 {值} W」 |
| 灯臂旋转 | 动画 | 1% | 「灯臂第 1–40 帧从 {a}° 转到 {b}°」 |
| 杯身细分 | 修改器 | 0 | 「杯身加 {n} 级细分」 |

1. 每个槽位标注类别、容差与对应句式，题面由句式填值生成。
2. 难度由两个旋钮决定：钉死多少个槽位，以及槽位之间的依赖深度。
   - 两者直接决定 Verifier 要查几个字段，因此比改写措辞更可靠

## 4 Curation Pipeline

3D 素材有三个问题：资产大多导入不了，Objaverse-XL 只有 14.9% 能被 Blender 导入并渲染；官方扩展目录 1,533 个里传染性许可 1,341 个；bpy 脚本常依赖工程文件、资产路径与插件。所以原始素材要过八道闸才能进训练集，按运行前、导入渲染、运行后、入库前四段排开。顺序比闸本身更要紧：最大的一刀在导入渲染，许可、版本、依赖这类便宜的闸必须排在它前面。

<div class="wide"><div class="gp-wrap"><div class="gp gf">
<div class="gp-grp" style="grid-column:2/3;--g:var(--brand)">运行前 · 文件与脚本</div>
<div class="gp-grp" style="grid-column:3/4;--g:#e8913a">导入渲染</div>
<div class="gp-grp" style="grid-column:4/5;--g:#6a4fd6">运行后 · 渲染图</div>
<div class="gp-grp" style="grid-column:5/6;--g:#d6455d">入库前 · 全库比对</div>
<div class="gp-end gp-in arr">原始<br>素材</div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">01</span><b>许可过滤</b></div><div class="gf-r">Blender 官方扩展目录 1,533 个里传染性许可 1,341 个；Sketchfab 须剔除 NC 许可</div><div class="gf-src"><a href="https://extensions.blender.org/">Blender Extensions</a> · <a href="https://sketchfab.com/">Sketchfab</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">02</span><b>版本钉死</b></div><div class="gf-r">Blender 按版本分叉，一个版本对应一个 Python 运行时</div><div class="gf-src">Train 4.1</div></div>
<div class="gf-gate no-src"><div class="gf-h"><span class="gp-step">03</span><b>依赖与路径</b><span class="gf-tag warn">无出处</span></div><div class="gf-r">bpy 脚本常依赖工程文件、资产路径与插件，缺一样就跑不起来</div></div>
</div>
<div class="gp-g gp-hot arr"><div class="gp-step">04 · 最大的一刀</div><div class="gp-name">导入并渲染</div><div class="gp-big">14.9%<small>能被 Blender 导入并渲染</small></div><div class="gp-row"><span>成功率</span><b>14.9%</b><span class="gp-bar"><i style="width:14.9%;background:#e8913a"></i></span></div><div class="gp-cap"><a href="https://arxiv.org/abs/2307.05663">Objaverse-XL</a>：3,700 万个文件 → 550 万；单题成本 Blender 2.3 秒、three.js 383 毫秒（本项目实测）</div></div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">05</span><b>坏渲染过滤</b></div><div class="gf-r">用 1,200 条人工标注训练坏渲染分类器；Polycam 来源的渲染图 38.20% 被判坏</div><div class="gf-src"><a href="https://arxiv.org/abs/2307.05663">Objaverse-XL</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">06</span><b>美学分档</b></div><div class="gf-r">按 LAION 美学分把资产分三档，只用于过滤，不进 reward</div><div class="gf-src"><a href="https://arxiv.org/abs/2307.05663">Objaverse-XL</a></div></div>
</div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">07</span><b>去重</b></div><div class="gf-r">代码托管侧 3,700 万个文件，去重后元数据 1,085 万行</div><div class="gf-src"><a href="https://arxiv.org/abs/2307.05663">Objaverse-XL</a></div></div>
<div class="gf-gate no-src"><div class="gf-h"><span class="gp-step">08</span><b>去污染</b><span class="gf-tag warn">无出处</span></div><div class="gf-r">3D 方向未见去污染实践；评测集与训练集同源时风险同 Web</div></div>
</div>
<div class="gp-end gp-out">可用<br>素材</div>
<div class="gp-lock">顺序锁定：许可、版本、依赖闸排在导入渲染之前</div>
</div></div></div>

**数据清洗心得**

1. 挖 GitHub 必须按创建日期截断：2026 年新建的 three.js 仓库大量混入模型产物。
   - topic:threejs 且星数 > 100：2026 年新建的 122 个里 53 个（43%）在描述或主题里提到 Claude、Codex、GPT 或 agent；2023–2024 年新建的 82 个里 0 个
   - 口径：只匹配描述与主题字段，提到不等于全由模型生成
   - Blender 侧同样出现：topic:blender 加 procedural-generation 的结果里已有 2026 年新建的 agent 工具仓库
2. 公开数量常与实数不符，引用前须核验。
   - 旧材料里 three.js 610、Babylon.js 975、Blender 2,596，实测分别为 613、916、2,564
   - WorldCoder-Bench：HF 只放 205 题，论文 2,026 题（Core / Robust 未全部公开）
   - MeshCoder：README 称已发布 100K 条，论文约 100 万物体 / 41 类
   - BlenderGym：压缩包实数 280，论文 245
   - Omni-CAD：数据卡与论文约 450K，切分文件实数 313,096；图与点云要按脚本自行生成
   - Objaverse-XL：论文 1,020 万，元数据实数 10,850,997 行
3. 美学分只用于过滤，不进 reward。
   - [Objaverse-XL](https://arxiv.org/abs/2307.05663) 按 LAION 美学分把资产分三档，本项目素材里未见用作 reward（Verifier 3.3.2）

