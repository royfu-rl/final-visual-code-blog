# 过夜迭代时移出正文的段落（10-28），可随时恢复

## 1 开头铺垫与收尾

## 1 The Same Three Parts, A Different Ground Truth

本章只回答一个问题：**怎么把一批 3D 场景与脚本，变成能训模型的题。**

一条可验证任务和 Web 一样由三件组成，缺一件就只是数据，不是任务。三个词含义同 Web 页第 1 章，后面三章各讲一件。


…


本页顺序与 Web 页一致：第 2 章 Query（3D 最弱的一环）→ 第 3 章 Verifier（3D 最强的一环）→ 第 4 章 Harness（版本适配只在这里出现）。

## 2 开头

Query 这一侧回答两个问题：

- 素材从哪来 → 决定供给的上限
- 参考给到什么程度 → 决定判据的来源

## 2.7 Reference Thickness（Web 已删，3D 同步）

### 2.7 Reference Thickness

Query 这一侧的另一个变量：参考给到什么程度。参考越厚，Verifier 能查的东西越多。

- 唯一能直接参考模态配比的公开素材是一份 Blender 创作基准：223 个任务里，纯文本 78 条、图加文 130 条、视频加文 15 条，另有 59 个任务带尺寸、材质、相机规格的附件。**图加文占一半以上。**
- 纯文本题目从零起极难过关：判据只能查题目钉死的字段，题目没写的不许查。这就是 3D 题目倾向于带参考的原因：不是为了好做，是为了判据有东西可查。

**纯图像档的证据以负面为主：像素比对没有可用的工作点。** 该过的相机移动单图相似度 0.9534，真错误的木色变蓝 0.9844。

- 替代方案三类，都有判别力数字：
  - 逐部件几何 18/22（对照：全局几何分检出 0/11）
  - 逐颜色体素占据 25/29
  - 开放边界边数 0 对 64
- 最该记的一组：杯子平移 30 厘米
  - 全局距离只从 0 变到 0.00018，全局几何分 0.9916（能过 0.99 的闸）
  - 逐部件距离 0.08375，逐部件分 0.2243，差 460 倍
  - **全局平均会掩盖小部件的误差**

**文加图档是打分模型的最佳工况。** 唯一一组「同一标注集、只换输入模态」的受控对照：

- 题面带参考图：判对率 94% 与 97%，抓错率 92% 到 95%
- 只有题面：判对率 68% 与 76%，抓错率只有 61% 到 63%，放对率几乎不动（四视角下 39/40）
- 所以无参考图的打分模型「几乎不误杀、但一半错误抓不到」，**只能当补抓，不能当闸**
- 造题形态：扰动即监督
  - 取一个已有场景扰动它，题面给起始场景加目标渲染图，要求改回去
  - 图在题面侧，reward 在状态侧
  - 准入可自动化：**只有被破坏的渲染在官方判据下判失败，才接受这个扰动**

**视频档：动画有更便宜的路。** 时间轴是声明式的，时序正确性走断言，不走视频判别：删掉两整条动画曲线，单视角、多视角、距离、体素占据全部给 1.0000，只有逐关键帧断言抓到。

## Benchmark 1 Lab Reports 解读

## 1 What The Frontier Labs Actually Report

核心发现：3D 方向只有 BenchCAD 被两家厂商同时报告；Blender 方向只有 Qwen 报了分数，其余厂商只放 demo。

<!--FRONTIER-->

数据解读：

- **BenchCAD 是唯一被两家厂商同时报告的 3D benchmark，但两家的数字不能直接比。** 一家报的是带工具的几何重叠百分比，另一家报的是体素交并比，并区分全集与一千个文件的子集、带工具与不带工具。官方榜把两家分数都标为厂商自报、未重新评测。
- **Blender 方向没有任何厂商采用公开 benchmark。** Qwen 用内部的 QwenBlenderBench，OpenAI 只放了 Blender 建模的 demo，其余几家连 demo 都只是发布页上的一段视频。
- **厂商选 CAD 不是偶然，和验收方式有关。** CAD 结果能按几何确定性判分，不依赖看图打分，适合放进发布页的对比表。
- **「未报告」那一组不是空白，是信号。** 六家厂商在 3D 上只给 demo 不给分数，说明这个方向还没有一把各家都认的尺子——这恰好是自建可验证环境的空间。

## Open Data 2 Timeline 原文字版（换成时间线图）

## 2 Timeline

核心发现：只看多视图截图的评测会高估模型，新 benchmark 普遍加了几何、状态或执行检查。

- **2023 年到 2024 年：先评外观。** Text2CAD 和 CADPrompt 把文本生成 CAD 定义为可量化任务，是这一阶段唯一的确定性判据。
- **2025 年：Blender 进入评测。** BlenderGym 的 245 个编辑任务按起始场景到目标场景判定。
- **2026 年上半年：程序化 3D 与 CAD 的 benchmark 集中出现。** BenchCAD 的 17.9K 个 CadQuery 程序全部按执行结果判分，不使用 LLM judge。P3D-Bench 发现模型能做出整体形状，但做不出精确参数的几何。WorldCoder-Bench 检查 three.js 的隐藏运行时状态，最好的系统 27.8%。
- **2026 年中：评测动态场景与工程级任务。** 4DBuildBench 检查物理求解器的运行时状态。CADEngBench 加入有限元分析与装配运动学。

数据解读：多视图视觉相似度查不出漂浮部件、背面空洞这类结构错误。本项目的 three.js 原型复现过同一现象：雪人任务的 6 个候选页面，单张截图相似度全落在 0.973 到 1.0 之间，完全分不开。

## Sources 2.2 GitHub 原文（拆成 2.2.1 / 2.2.2 前）

### 2.2 GitHub

| Repo | Datasize | Artifacts | Permitted |
| --- | --: | --- | --- |
| [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) | 2,564 图 / 839 场景（3.1 : 1），46 类 | <span class="art a-img">截图</span><span class="art a-run">.blend</span> | △ GPL |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js) | 916 图 / 906 份代码（1 : 1） | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-code">.ts</span> | △ Apache-2.0，代码在 Playground |
| [three.js examples](https://github.com/mrdoob/three.js) | 613 图 / 613 页（1 : 1） | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-run">.html</span> | ✓ MIT |
| Blender bpy 仓库 | 6,307 → 56 可用 | <span class="art a-code">bpy .py</span> | 逐仓许可 |
| three.js 仓库 | 89,622 → 23,983（主题标签）→ 2,401（星 > 10） | <span class="art a-run">.html</span><span class="art a-code">.js</span> | 逐仓许可 |
| Blender 官方扩展目录 | 1,533（1,256 插件 + 276 主题） | <span class="art a-code">.py（插件）</span> | ✗ 传染性许可 1,341，MIT 只有 4 |
| [Infinigen](https://github.com/princeton-vl/infinigen) | 无上限（生成器） | <span class="art a-run">Blender 场景</span><span class="art a-asset">网格（OBJ / USD）</span> | ✓ BSD-3 |

¹ 888/906 的代码在外部 Playground，仓库只存 id。

- **Golden Images 三行的图数与码数，2026-10-20 按各仓库 HEAD 逐个实数。**
  - 旧材料里 three.js 610、Babylon.js 975、Blender 2,596，实测分别是 613、916、2,564
  - 公开材料里的「约」常差一个数量级，引用这类数字必须核验
- **有基线却不能用的，不排掉会高估供给：**
  - react-three-fiber：0 张图
  - PlayCanvas：296 个示例、592 张缩略图，但没有比对
  - Godot：238 个文件，只有 1 张图
- Golden Images 只支撑最软的那一档判据：three.js 的 613 组配对是一比一的，但另一端是截图，只能支撑视觉相似度，支撑不了运行时契约
- bpy 仓库大多依赖工程文件、资产路径与插件，开箱即跑率很低

three.js 的形态直接决定 Harness 的单价：

- 全树 6,413 个文件
- 示例页 610 个（WebGL 298 / WebGPU 234 / WebXR 27 / 其他 23）
- 单页中位 6,137 字节，95 分位 13,651，最大 66,143，总体积 4.4 MB
- 可用接口 1,251 个
- **这个量级模型能在上下文里直接带着走，不需要先检索再用。**

## Sources 2.3 原文

### 2.3 Datasets

| Dataset | Datasize | Artifacts | Permitted |
| --- | --: | --- | --- |
| [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) | 12,059 | <span class="art a-txt">描述</span><span class="art a-code">bpy .py</span> | ✓ Apache-2.0 |
| [MeshCoder](https://huggingface.co/datasets/InternRobotics/MeshCoderDataset) | 100K（论文约 1M） | <span class="art a-asset">点云</span><span class="art a-code">bpy .py（分部件）</span> | △ CC-BY-SA-4.0，需申请 |
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) | 280（论文 245） | <span class="art a-img">多视角图</span><span class="art a-code">.py（起始）</span><span class="art a-code">bpy .py（编辑后）</span> | ？未声明许可 |
| [WorldCoder-Bench](https://huggingface.co/datasets/shuolucs/WorldCoder-Bench) | 205（论文 2,026） | <span class="art a-txt">描述</span><span class="art a-asset">网格（GLB）</span><span class="art a-run">.html</span> | ✓ CC-BY-4.0 |
| [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) | 970,937 + 968 | <span class="art a-asset">点云</span><span class="art a-code">CadQuery .py</span> | △ CC-BY-NC-4.0 |
| [Omni-CAD](https://huggingface.co/datasets/jingwei-xu-00/Omni-CAD) | 313,096（论文约 450K） | <span class="art a-txt">描述</span><span class="art a-img">多视角图</span><span class="art a-asset">点云</span><span class="art a-code">CAD 序列（命令）</span> | ✓ MIT |
| [DeepCAD](https://github.com/ChrisWu1997/DeepCAD) | 论文 17.8 万（未核实际条数） | <span class="art a-code">CAD 序列（构造）</span> | ？代码 MIT，数据未声明 |
| [Text2CAD](https://huggingface.co/datasets/SadilKhan/Text2CAD) | 论文约 170K 模型 / 660K 文本 | <span class="art a-txt">描述（多级）</span><span class="art a-code">CAD 序列（命令）</span> | △ CC-BY-NC-SA-4.0，需申请 |
| [GenCAD-Code](https://huggingface.co/datasets/CADCODER/GenCAD-Code) | 162,848 | <span class="art a-img">截图</span><span class="art a-txt">指令（固定）</span><span class="art a-code">CadQuery .py</span> | ？未声明许可 |
| [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | 21,048 | <span class="art a-img">多视角图</span><span class="art a-code">源码</span><span class="art a-txt">指令（编辑）</span><span class="art a-code">CadQuery .py</span> | ✓ CC-BY-4.0 |
| [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | 10,850,997 行元数据 | <span class="art a-asset">网格</span><span class="art a-meta">元数据</span> | △ ODC-By，单个对象各有许可 |

已知问题：

- WorldCoder-Bench：HF 只放了 205 题，论文的 2,026 题分 Core / Robust，未全部公开
- MeshCoder：README 称已发布 100K 条物体-代码对，论文约 100 万物体 / 41 类
- BlenderGym：压缩包里实数 280 个实例，论文写 245
- Omni-CAD：数据卡与论文写约 450K，切分文件里实数 313,096；图与点云要按脚本自行生成
- BenchCAD：由 17,900 条代码生成、748 条编辑、2,400 条问答组成；数据卡没写判分方式
- Objaverse-XL：论文写 1,020 万，元数据实数 10,850,997 行；代码托管侧索引 3,700 万个文件（去重后元数据 1,085 万行），能导入渲染的 550 万，约 15%；以元数据为分母约 51%。「550 万」在论文里只针对 GitHub 来源；Polycam 部分需申请、仅非商用
- CAD-Recode、Text2CAD：非商用许可，不能进商用训练

✓ 宽松许可　△ 有条件　？未声明。2026-10-20 读自各数据卡、文件列表与 LICENSE。

<!--SAMPLE:cad-recode|CAD-Recode-->
<!--SAMPLE:objaverse|Objaverse-->

## Sources 2.5 原文

### 2.5 Funnel

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
  - 真实素材这条线的产能是三位数，不是五位数：本项目 three.js 路线估算约 230 个任务

**二、合成扩产：槽位合成**

3D 的题目主力是槽位合成：把参考场景里可调的参数做成槽位表，每个槽位标注类别、容差和对应的自然语言句式。

| 槽位 | 类别 | 容差 | 句式 |
|---|---|--:|---|
| 桌面尺寸 | 变换 | 0.5% | 「一张 {长}×{宽} 的木桌」 |
| 桌面倒角 | 修改器 | 2% | 「桌面边缘倒角 {值}」 |
| 灯泡功率 | 灯光 | 2% | 「点光源 {值} W」 |
| 灯臂旋转 | 动画 | 1% | 「灯臂第 1–40 帧从 {a}° 转到 {b}°」 |
| 杯身细分 | 修改器 | 0 | 「杯身加 {n} 级细分」 |

**难度有两个旋钮：钉死多少个槽位，以及槽位之间的依赖深度。** 它们比「让题目听起来更难」可靠，因为直接决定判据要查几个字段。

## Sources 2.1 原文

### 2.1 Overview

**Artifacts 词表**：全书的来源表共用这六类标签，颜色即类别。

<!--ARTIFACTS-->

规范：一个标签只写一个物件；同义词归一（渲染结果、GUI 截图都写「截图」）；限定语写进括号（`bpy .py（分部件）`）；文件类型直接写扩展名。

**3D 的供给结构和 Web 完全不同：资产多、代码少，而题目要的是代码。**

核心发现：三个技术栈里只有 CAD 有成规模的公开配对数据；Blender 的代码来源收缩到两位数；three.js 没有任何公开的训练配对集。

| Source | Type | Datasize | Example | Artifacts |
| --- | --- | --: | --- | --- |
| **GitHub** | Golden Images | 2,564 图 · 916 图 · 613 图 | [Blender render tests](https://github.com/blender/blender/tree/main/tests/files/render) · [Babylon.js](https://github.com/BabylonJS/Babylon.js) · [three.js examples](https://github.com/mrdoob/three.js) | <span class="art a-img">截图</span><span class="art a-run">.blend</span><span class="art a-code">.ts</span><span class="art a-run">.html</span> |
|  | 带星脚本 / 页面仓库 | 56 仓 · 2,401 仓 | Blender bpy 仓库 · three.js 仓库 | <span class="art a-code">.py</span><span class="art a-run">.html</span> |
|  | 程序化生成器 | 无上限 | [Infinigen](https://github.com/princeton-vl/infinigen) | <span class="art a-run">Blender 场景</span><span class="art a-asset">网格（OBJ / USD）</span> |
| **HuggingFace** | 文本 / 点云 / 图 → 代码配对集 | 205 – 970,937 | [BlendNet](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) · [CAD-Recode](https://huggingface.co/datasets/filapro/cad-recode) · [BenchCAD](https://huggingface.co/datasets/BenchCAD/BenchCAD) | <span class="art a-txt">描述</span><span class="art a-asset">点云</span><span class="art a-img">截图</span><span class="art a-code">bpy .py</span><span class="art a-code">CadQuery .py</span> |
|  | 资产库（无代码） | 10.85M 行元数据 | [Objaverse-XL](https://huggingface.co/datasets/allenai/objaverse-xl) | <span class="art a-asset">网格</span><span class="art a-meta">元数据</span> |
| **Website** | 问答站 / 论坛 | 20.9k – 602k | [Blender StackExchange](https://blender.stackexchange.com/) · [BlenderArtists](https://blenderartists.org/) · [three.js 论坛](https://discourse.threejs.org/) | <span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-code">代码片段</span> |
|  | 资产站 | 2,387 – 500k | [Sketchfab](https://sketchfab.com/) · [Poly Haven](https://polyhaven.com/) | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-asset">网格</span><span class="art a-asset">HDRI</span> |

Golden Images：仓库为每份测试代码存一张标准截图，持续集成（Continuous Integration）每次渲染后逐像素比对（Visual Regression Testing），代码与截图因此天然成对。

读表：**Artifacts** 是这个渠道直接拿到的东西。



数据解读：

- **空位落在主力技术栈上**：Blender 与 three.js 是本文的核心栈，CAD 是辅助，而公开供给的厚度正好相反。所以 3D 的自建比例必须比 Web 高。
- **资产不是题目**：资产库给的是模型文件不是脚本，只能当素材池与渲染基线，当不了「指令 → 代码」的配对。
- **没有发现任何公开工作在批量挖掘 Blender 脚本**：这是缺口，不是一条可抄的路。

## Benchmark 2–3 原文

## 2 Three Stacks

3D 方向的三类技术栈不是难度递进，是**真值来源完全不同**。这决定了它们各自能给什么训练信号。

| 技术栈 | 产物 | 真值从哪来 | 本文定位 |
|---|---|---|---|
| blender | Blender Python 脚本 | 场景图可直接读：几何、材质、修饰器、求解器状态 | 主力 |
| 3js | three.js 场景代码 | 无头浏览器里渲染加几何断言，还能读隐藏运行时状态 | 主力 |
| cad | CadQuery 等参数化 CAD 代码 | 尺寸、约束、B-Rep 有效性、可制造性，全部确定 | 辅助 |

cad 不是 blender 的简化版。CAD 用精确的 B-Rep 曲面，面向加工制造；Blender 用多边形网格，面向渲染。cad 列在这里的理由只有一个：**它的确定性验收和程序化合成方法可以直接搬到 blender 和 3js 上**。

核心发现：三类里只有 cad 被前沿厂商写进发布页，而 blender 方向没有任何厂商采用公开 benchmark。按技术栈分组的学术 benchmark 总表在 Open Data 视图里，和数据管线并列。

数据解读：

- **3js 的量程最好，差距张得最开。** [3JSBench](https://3jsbench.com/) 用 744 条检查判 100 道题（696 条必查、其中 695 条分入六族，48 条 advisory 不参与判定），采乘法门控：全部必查项通过才算过。六个检查族的分布是部件计数 223、结构 160、空间关系 157、任务专属几何 45、文字 12、渲染质量 98——**一半以上的检查在数部件和查结构，不在看画面好不好**。Astra 80.0%、Claude Opus 5.5 49.0%、Kimi K3 23.0%，头尾差 57 个百分点。同一批尝试的 SigLIP2 相似度均值全落在 0.0774 到 0.1081 的窄带里，区分度接近零——它的 pinned checkpoint 跨 runtime 噪声最大 0.005，比模型间差异 0.004 还大。
- **换一个 3js 评测，差距又被压扁。** [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 查隐藏运行时状态契约，判据同样确定，但原文明说没有系统超过 30%，前四名挤在 23.0% 到 27.8%。判据确定只是必要条件，量程落在中段才能把模型分开。
- **blender 方向的失败集中在 API 层。** 3DCodeBench 覆盖 212 个类别，首要失败原因是 API 不匹配，不是空间推理错。BlenderGym 的 245 个编辑任务里，最强的 VLM 在人类认为简单的任务上仍然失败。
- **cad 是唯一进了厂商发布页的 3D 指标，但两家数字不能直接比。** BenchCAD 上 OpenAI 报 GPT-6 Astra 95.9%（带工具，geometric overlap），Anthropic 报 Claude Opus 5 的 Vision2Code 子任务 0.366 / 0.821（voxel IoU，不带工具 / 带工具，1000 个文件的子集）。BenchCAD 官方榜把两家分数都标为厂商自报、未重新评测。
- **厂商选 cad 不是偶然。** CAD 结果能按几何确定性判分，不依赖 VLM 看图，适合放进发布页的对比表。Blender 方向 Qwen 只报内部的 QwenBlenderBench（69.9），OpenAI 只放 demo。

## 3 How To Choose

| 目标能力 | 用哪些 | 能不能当主指标 |
|---|---|---|
| 程序化建模 | 3DCodeBench、BlenderGym | 能 |
| 几何精度与量程 | 3JSBench | 能，当前量程最好 |
| 动态场景与物理 | 4DBuildBench、WorldCoder-Bench | 能，但量程压在 30% 以下 |
| 精确参数与约束 | BenchCAD、CADTests、Text2CAD-Bench | 能，确定性最高 |
| 装配与部件连接 | P3D-Bench、CADEngBench | 能 |

确定性检查类可以当主指标，VLM judge 只作参考。

## Web Open Data 1 Inventory 原文

## 1 Inventory

先看分布，再看结论。公开世界在 Web 方向留下两类东西——给人训练用的数据管线，和给人评测用的题库——而**它们常常是同一篇论文的两面**：截图转代码方向最有名的那几项既是训练集又是测试集。所以这里把两类并进一张表，加一列「类型」，按发布日期混排。

核心发现：公开供给几乎全部压在「单文件、截图转代码」这一格，而真实生产最依赖的多文件工程那一格只有两条管线。

| 技术栈 | 数据管线 | Benchmark | 这意味着什么 |
|---|---|---|---|
| html（含截图转 html、SVG、图表代码、TikZ） | 35 | 32 | 供给充足，但形态高度同质 |
| webdev（多文件可运行工程） | 2 | 13 | 题有人出，数据没人放——这正是真实生产的形态 |
| ppt | 5 | 5 | 够做辅助能力，不够做主力 |
| manim | 8 | 5 | 管线里有三条是渲染库本身 |

<!--ALL:html,webdev,ppt,manim-->

数据解读：

- **这条线的起点是合成，终点也在合成。** 2017 年最早那条配对数据的做法就是随机生成领域专用语言再渲染出界面截图——截图与代码天然对齐。2024 年把这个思路推到两百万条的规模，仍然是合成。真实网页挖矿的留存率公开自报在 2% 到 5%，而合成与变异高一个数量级，这个差距从第一天就没有变过。
- **2024 年是「配对数据」的高峰，2025 年之后重心转向判据。** 早期管线报的是数据量，近两年的管线报的是渲染成功率、交互契约、以及把渲染反馈直接当强化学习奖励。产物没变，变的是这批数据被怎么用。
- **webdev 这一格是整张表里最刺眼的一处倒挂：题有 13 条，数据只有 2 条，而且是同一组作者的前后两步。** 一条给出训练集六千六百余条加测试集一百余条，另一条给出七百条轨迹加五百条指令。**这个量级连一次完整的难度分桶都支撑不起。** 它的分数也因此最有量程——用 UI agent 执行用例的那一类最好组合只有 27.8%，要求端到端构建并部署的那一类论文口径最好 61.8%。
- **html 这一格条目最多、判据最成熟，但分数已接近上限。** 早期的单页还原题只适合做回归测试：厂商自报的相似分已经挤在 93 以上，题目本身区分不出模型。其中判据最确定的一支是图表与 SVG——产物能逐值回读，画出来的数值对不对不需要看图，解析绘图对象就能判。
- **ppt 与 manim 两格的定位相同：够用即可。** 按本文的分工，这两格只需要「稍微有一定的能力」，现有公开素材刚好够，不需要自建。
- **同源的训练集与测试集必须分开用。** 混排之后最容易看出哪些名字在两类里都出现过——那正是最容易同时被训练又被评测的那些。这也是后面那条去污染为什么必须做的原因。

## 3D Open Data 1 Inventory 原文

## 1 Inventory

和 Web 那一章同一个读法：公开的数据管线与学术题库常常出自同一篇论文，所以并进一张表，加一列「类型」，按发布日期混排。3D 这边并完之后立刻看出一个空洞。

核心发现：**3js 有基准没有管线，blender 反过来有管线却没有一项基准进过厂商发布页**，而 cad 两头都厚。

| 技术栈 | 数据管线 | Benchmark | 形态 |
|---|---|---|---|
| blender | 8 | 8 | 两条程序化生成器加六条「文本或点云转脚本」 |
| 3js | 0 | 3 | 只有基准与像素基线仓库，没有任何管线 |
| cad | 8 | 8 | 从构造序列到参数化代码，规模最大、判据最确定 |

<!--ALL:blender,3js,cad-->

数据解读：

- **cad 是三格里唯一两头都有规模的。** 公开数据集的量级是十七万、十七万、一百万，产物都能按执行结果判分；它也是唯一进了厂商发布页的 3D 指标——判据最便宜。基准那一侧同样确定：近两万个参数化程序全部按执行结果判分，不用模型打分模型。
- **blender 的管线分成性质完全不同的两类。** 两条程序化生成器的产能标「无上限」，因为它们不是数据集而是生成器；剩下六条是真数据集，规模从一万二到一百万，输入侧从纯指令到点云不等。想要产能用生成器，想要分布贴近人写的代码用后者。而它的基准失败集中在 API 层，不是空间推理层——覆盖两百多个类别的那一项，首要失败原因是接口不匹配。
- **3js 这一格的零不是统计口径问题。** 公开世界给了基准（确定性检查、隐藏运行时状态契约）和像素基线仓库（六百余张参考图与示例页一比一），**但没有任何一条公开管线在批量产出 three.js 训练数据**。同一个空位在 Blender 脚本挖掘上也存在：没有发现任何公开工作在做这件事。而它的基准量程恰好是三格里最好的——确定性检查加乘法门控那一项头尾差 57 个百分点，查隐藏运行时状态契约那一项没有系统超过 30%。
- **空位恰好落在主力技术栈上。** blender 与 3js 是核心，cad 是辅助；而公开供给的厚度正好相反。所以 3D 这条线的自建比例必须比 Web 高。

一条配套的事实要和上表一起读：公开资产集在代码托管侧索引了三千七百万个文件，而**能被 Blender 成功导入并渲染的只有五百五十万，约 15%**；可商用的部分约一百九十万。分母要看清：去重后的元数据是一千零八十五万行，以它为分母算出来是约 51%，两个口径不能混用。这是「名义池不等于可用池」在 3D 上最大的一次收缩，也是估算任何 Blender 侧产出率时唯一的公开锚点。

## 3D Sources 2.4 原文

### 2.4 Website

核心发现：六家站点只有两家可用，而且都是资产站，一行代码都没有。

| Website | Datasize | Artifacts | Permitted |
| --- | --: | --- | :-: |
| [Poly Haven](https://polyhaven.com/) | 2,387 | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-asset">HDRI</span><span class="art a-asset">贴图</span><span class="art a-asset">网格</span> | ✓ CC0 |
| [Sketchfab](https://sketchfab.com/) | 500k 可下载 | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-asset">网格</span> | △ 剔除 NC 许可 |
| [Blender StackExchange](https://blender.stackexchange.com/) | 123,167 问 / 115,066 答（脚本相关 13,632 + 6,738，几何节点 5,967） | <span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-code">代码片段</span> | ✗ 2024 年起转储禁训 |
| [Stack Overflow](https://stackoverflow.com/) | 20.9k（three.js 标签） | <span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-code">代码片段</span> | ✗ 转储禁训 |
| [BlenderArtists](https://blenderartists.org/) | 602,128 帖 / 581 万回复 | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-run">.blend（少量）</span> | ✗ robots 全禁 |
| [three.js 论坛](https://discourse.threejs.org/) | 26k 帖 | <span class="art a-txt">标题</span><span class="art a-txt">描述</span><span class="art a-code">代码片段</span> | ✗ 无内容许可 |

✓ 可用　△ 有条件　✗ 不可用。desc = 正文或描述文本。† 站点对本机 403，未直连核实。

数据解读：

- **许可在 Blender 这条线上是决定性的**：官方扩展目录 MIT 只有 4 个、传染性许可 1,341 个；问答站要求数据不用于模型训练。能规模化的合法路径只剩官方测试资产与自建合成。
- 爬虫协议不是许可，但决定能不能合法拿到：BlenderArtists 的 60 万帖也许能引用，但抓取代理被全量封禁，整条路不可用，可用量归零
- 产物形态决定命运：
  - 资产站（两家）：一行代码都没有，是素材池与渲染基线，不是题库
  - 问答站与论坛拿到的是片段：跑不起来、过不了执行闸，只能当无监督语料或反向构造题干的素材

## Web Benchmark 2 Four Stacks 原文

## 2 Four Stacks

Web 方向的 benchmark 按产物技术栈分四类，不按输入模态分。输入是截图还是文字，换的只是 query；产物是单文件页面还是多文件工程，换的是整条验收链路。

| 技术栈 | 产物 | 验收能做到哪一步 | 本文定位 |
|---|---|---|---|
| html | 单文件 HTML、SVG、React 组件、绘图代码 | 渲染一次就能比对，DOM 盒模型与逐值回读都可用 | 主力 |
| webdev | 多文件 Web App | 要起服务、要 agent 操作，验收依赖运行时状态 | 主力 |
| ppt | 幻灯片、海报、演讲视频 | 产物是版面对象树，可逐对象回读 | 辅助 |
| manim | 代码驱动的讲解动画 | 产物是视频，判据只能落在渲染成功、时长与关键帧 | 辅助 |

主力与辅助的区分不是按难度，是按**它能不能产出可训练的判定信号**。html 和 webdev 两类合起来占了 Web 方向 benchmark 的绝大多数，判据链路也最完整；ppt 和 manim 两类有一定能力即可，所以本章不单开小节，只在 Open Data Pipeline 的两张总表里按技术栈分组列出，够选题就行。

核心发现：html 的题目数量和判据成熟度都远超其余三类，但分数已接近上限；webdev 的分数还在中段，差距张得开。按技术栈分组的学术 benchmark 总表在 Open Data 视图里，和数据管线并列。

数据解读：

- **html 类的早期题目只适合做回归测试。** [Design2Code](https://arxiv.org/abs/2403.03163) 的 484 个真实网页按渲染相似度打分，而厂商自报的相似分已经挤在 93 以上（GLM-5V-Turbo 94.8、Qwen3-VL-235B-Thinking 93.4，差 1.4 点）。判据本身是模型看图打分，量程又已耗尽，这类分数不能再当主指标。
- **webdev 类的分数还没饱和。** [WebGen-Bench](https://arxiv.org/abs/2505.03733) 用 UI agent 执行 647 个测试用例，最好的组合 27.8%。[Vibe Code Bench](https://www.vals.ai/benchmarks/vibe-code) 要求从规格说明构建并部署应用，论文里最好的模型 61.8%，接入外部服务后从 71% 降到 30%。
- **图表与 SVG 是 html 类里判据最确定的一支。** 产物能逐值回读：画出来的数值对不对，不需要看图，解析绘图对象就能判。


