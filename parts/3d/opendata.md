## 1 Inventory

3D 的公开管线与 benchmark 并进一张表后有两处错位：3js 有 benchmark 没有管线，blender 有管线但没有一项 benchmark 进过厂商发布页；cad 两头都有规模。

| 技术栈 | 数据管线 | Benchmark | 形态 |
|---|---|---|---|
| blender | 12 | 8 | 两条程序化生成器加十条「文本、点云、布局或教程转脚本」 |
| 3js | 0 | 3 | 只有基准与像素基线仓库，没有任何管线 |
| cad | 8 | 8 | 从构造序列到参数化代码，规模最大、判据最确定 |

<!--ALL:blender,3js,cad-->

1. cad 是唯一两头都有规模的技术栈。
   - 公开数据集量级约 17 万、17 万、100 万，产物都能按执行结果判分
   - BenchCAD 近 2 万个参数化程序全部按执行结果判分，不用模型打分
2. blender 的管线分生成器与真数据集两类。
   - 两条程序化生成器产能无上限；十条真数据集里最大的约 203 万行（3DCodeVerse，非商用），输入从纯指令、点云到整屋布局
   - 2026 年 9–10 月新增四条：3DCode（MIT）、3D-Front-Code、3DCodeVerse、BlenderLore，许可只有 3DCode 干净
   - 要产能用生成器，要贴近人写代码的分布用数据集
3. 3js 没有一条公开管线在批量产出训练数据。
   - 公开的只有 benchmark（确定性检查、隐藏运行时状态）与像素基线仓库（three.js examples 613 组图与页）
4. 公开供给与主力技术栈错位，因此 3D 的自建比例必须比 Web 高。

## 2 Timeline

<div class="tl-wrap"><div class="tl"><div class="tl-band"><span>评测对象：渲染看起来像不像</span><i></i><span>场景状态对不对</span></div><div class="tl-col" style="--c:#9aa1ab"><div class="tl-date">2024</div><div class="tl-node"></div><div class="tl-title">文本转 CAD</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-vote">人工评审</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2402.09052">UFO（L3GO）</a><span>2024-02</span></div><p>50 条非常规物体描述；Blender 里调 API 搭积木，人评</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2409.17106">Text2CAD</a><span>2024-09</span></div><p>约 170K 个模型、约 660K 条文本标注</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2410.05340">CADPrompt</a><span>2024-10</span></div><p>200 条 prompt；按点云距离与成功率判分</p></div></div><div class="tl-col" style="--c:#7f8fc4"><div class="tl-date">2025</div><div class="tl-node"></div><div class="tl-title">Blender 编辑</div><div class="tl-chips"><span class="tl-chip m-vis">视觉相似度</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2504.01786">BlenderGym</a><span>2025-04</span></div><p>245 个手工场景、5 类任务；改脚本把起始场景对齐到目标场景</p></div></div><div class="tl-col" style="--c:#6380d6"><div class="tl-date">2026-01 – 2026-05</div><div class="tl-node"></div><div class="tl-title">程序化建模与 CAD</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-vis">视觉相似度</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2601.11109">BlenderBench（VIGA）</a><span>2026-01</span></div><p>看图迭代写 Blender 代码重建场景</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2605.10865">BenchCAD</a><span>2026-05</span></div><p>17,900 个 CadQuery 程序；全部按执行结果判分</p><div class="tl-m later"><span class="bar"><i style="width:95.9%"></i></span><b>95.9%</b><em>厂商自报（GPT-6 Astra，带工具）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.01057">3DCodeBench</a><span>2026-05</span></div><p>212 个类别；失败多来自 API 不匹配</p></div></div><div class="tl-col" style="--c:#4876ea"><div class="tl-date">2026-06 – 2026-08</div><div class="tl-node"></div><div class="tl-title">运行时状态与工程验证</div><div class="tl-chips"><span class="tl-chip m-state">运行时状态</span><span class="tl-chip m-geo">几何与执行检查</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.01869">WorldCoder-Bench</a><span>2026-06</span></div><p>2,026 个任务；查 three.js 隐藏运行时状态</p><div class="tl-m"><span class="bar"><i style="width:27.8%"></i></span><b>27.8%</b><em>发布时最好（Core）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.11152">P3D-Bench</a><span>2026-06</span></div><p>1,003 题；整体形状对，精确参数做不出</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2607.01766">4DBuildBench</a><span>2026-07</span></div><p>50 个场景；审计物理求解器状态</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2608.09296">CADEngBench</a><span>2026-08</span></div><p>600 个任务；有限元与装配运动学</p></div></div><div class="tl-col" style="--c:#2f6bff"><div class="tl-date">2026-09 – 2026-10</div><div class="tl-node"></div><div class="tl-title">确定性门控与 agent</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-agent">agent 实测</span></div><div class="tl-card"><div class="nm"><a href="https://3jsbench.com/">3JSBench</a><span>2026-09</span></div><p>744 条检查，必查项全过才算通过</p><div class="tl-m later"><span class="bar"><i style="width:80.0%"></i></span><b>80.0%</b><em>榜单（GPT-6 Astra）</em></div><div class="tl-m later"><span class="bar"><i style="width:49.0%"></i></span><b>49.0%</b><em>榜单（Claude Opus 5.5）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2609.06535">3DHarnessBench</a><span>2026-09</span></div><p>4 级工具权限；把 3D 几何还原为 Blender 代码</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2610.10622">WorldBench</a><span>2026-10</span></div><p>three.js 体素世界；看图与读代码在 32% 的必查项上判断不一致</p></div><div class="tl-card"><div class="nm"><a href="https://huggingface.co/datasets/Qwen/BlenderWorld">BlenderWorld</a><span>2026-10</span></div><p>223 个任务、2,651 条二值 rubric</p></div></div></div></div>
<div class="tl-legend"><span><i style="background:var(--brand)"></i>发布时最好成绩</span><span><i style="background:#b8bfc9"></i>后续成绩（厂商自报或榜单）</span></div>

## 3 Gaps

公开 3D 数据给的是资产，不是代码：能导入渲染的资产只占索引的约 15%，three.js 没有一条公开训练配对，因此 3D 的 Query 与 Verifier 比 Web 更依赖自建。

**一、缺的东西**

Query、Verifier、Harness 与难度标注，公开 3D 数据都不稳定提供。

1. 资产库只有网格与元数据，没有生成它的代码。
   - [Objaverse-XL](https://arxiv.org/abs/2307.05663)：代码托管侧索引 3,700 万个文件，能被 Blender 导入并渲染的 550 万（14.9%），可商用约 190 万
2. 代码来源规模小，three.js 没有一条公开训练配对。
   - Blender bpy 仓库 6,307 → 56 个可用；three.js 仓库星数 > 10 的 2,401 个；两者都只筛标签与星数，没做可运行性检查
3. 公开基准多用视觉相似度，不提供读场景状态的 Verifier。
   - 本项目 three.js 原型：雪人任务的 6 个候选页面，单张截图相似度全落在 0.973–1.0，分不开好坏
4. 公开基准常不记录 Blender 版本，因此结果不可复现。
   - BlenderGym 未写明所用 Blender 版本

**二、前置条件**

许可、可运行、版本三项都要在训练前核对。

1. 许可：Blender 生态以传染性许可为主。
   - 官方扩展目录 1,533 个，传染性许可 1,341 个，MIT 4 个
   - Sketchfab 须剔除 NC 许可；问答站条款要求数据不用于模型训练
2. 可运行：资产要能在无头 Blender 里导入并渲染。
   - Objaverse-XL 的导入渲染成功率为 14.9%
3. 版本：Blender 按版本分叉，每道题须钉死运行时版本。
   - 做法见 Train 页 4.1

