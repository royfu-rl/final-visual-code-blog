## 1 Inventory

3D 的公开数据按真值来源分三类，不按难度分：blender 与 3js 是主力，cad 够用即可。公开的数据管线与 benchmark 常出自同一篇论文，因此并进一张表：3js 有 benchmark 没有管线，blender 有管线但没有一项 benchmark 进过厂商发布页，只有 cad 两头都有规模。

| 技术栈 | 产物 | 验收能做到哪一步 | 数据管线 | Benchmark | 这意味着什么 |
|---|---|---|---|---|---|
| blender（主力） | Blender Python 脚本 | 场景图可直接读：几何、材质、修改器、求解器状态 | 12 | 8 | 两条程序化生成器加十条「文本、点云、布局或教程转脚本」 |
| 3js（主力） | three.js 场景代码 | 无头浏览器里渲染加几何断言，还能读隐藏运行时状态 | 0 | 3 | 只有基准与像素基线仓库，没有任何管线 |
| cad（辅助） | CadQuery 等参数化 CAD 代码 | 尺寸、约束、B-Rep 有效性、可制造性，全部确定 | 8 | 8 | 从构造序列到参数化代码，规模最大、判据最确定 |

<!--ALL:blender,3js,cad-->

1. cad 不是 blender 的简化版。
   - CAD 用精确的 B-Rep 曲面，面向加工；Blender 用多边形网格，面向渲染
   - 列在这里，是因为它的确定性验收与程序化合成可以直接搬到 blender 与 3js
2. cad 是唯一两头都有规模的技术栈。
   - 公开数据集量级约 17 万、17 万、100 万，产物都能按执行结果判分
   - BenchCAD 近 2 万个参数化程序全部按执行结果判分，不用模型打分
3. blender 的管线分生成器与真数据集两类：要产能用生成器，要贴近人写代码的分布用数据集。
   - 两条程序化生成器产能无上限；十条真数据集里最大的约 203 万行（3DCodeVerse，非商用），输入从纯指令、点云到整屋布局
   - 2026 年 9–10 月新增四条：3DCode（MIT）、3D-Front-Code、3DCodeVerse、BlenderLore，许可只有 3DCode 干净
4. 3js 倒挂：benchmark 3 条，数据管线 0 条。
   - 公开的只有 benchmark（确定性检查、隐藏运行时状态）与像素基线仓库（three.js examples 613 组图与页）
5. 3js 的分数还没饱和，模型差距拉得最开。
   - [3JSBench](https://3jsbench.com/)：744 条检查判 100 道题，必查项全过才算通过；GPT-6 Astra 80.0%、Claude Opus 5.5 49.0%、Kimi K3 23.0%
   - 一半以上检查在数部件、查结构：部件计数 223、结构 160、空间关系 157、任务专属几何 45、文字 12、渲染质量 98
   - 同批尝试的 SigLIP2 相似度均值都在 0.0774–0.1081，跨运行环境噪声 0.005 大于模型间差异 0.004
6. Verifier 确定只是必要条件，量程落在中段才能把模型分开。
   - [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 同样查运行时状态，最好系统不到 30%，前四名挤在 23.0%–27.8%
7. blender 方向的失败集中在 API 层。
   - 3DCodeBench（212 个类别）：首要失败原因是 API 不匹配，不是空间推理错
   - BlenderGym（245 个编辑任务）：最强 VLM 在人类认为简单的任务上仍然失败
8. cad 是唯一进了厂商发布页的 3D 指标，但两家数字不能直接比。
   - BenchCAD：OpenAI 报 GPT-6 Astra 95.9%（带工具，geometric overlap）；Anthropic 报 Claude Opus 5 的 Vision2Code 子任务 0.366 / 0.821（voxel IoU，不带工具 / 带工具，1,000 个文件的子集）
   - 官方榜把两家分数都标为厂商自报、未重新评测
9. 公开供给与主力技术栈错位，因此 3D 的自建比例必须比 Web 高。

## 2 Timeline

<div class="tl-wrap"><div class="tl"><div class="tl-band"><span>评测对象：渲染看起来像不像</span><i></i><span>场景状态对不对</span></div><div class="tl-col" style="--c:#9aa1ab"><div class="tl-date">2024</div><div class="tl-node"></div><div class="tl-title">文本转 CAD</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-vote">人工评审</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2402.09052">UFO（L3GO）</a><span>2024-02</span></div><p>50 条非常规物体描述；Blender 里调 API 搭积木，人评</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2409.17106">Text2CAD</a><span>2024-09</span></div><p>约 170K 个模型、约 660K 条文本标注</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2410.05340">CADPrompt</a><span>2024-10</span></div><p>200 条 prompt；按点云距离与成功率判分</p></div></div><div class="tl-col" style="--c:#7f8fc4"><div class="tl-date">2025</div><div class="tl-node"></div><div class="tl-title">Blender 编辑</div><div class="tl-chips"><span class="tl-chip m-vis">视觉相似度</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2504.01786">BlenderGym</a><span>2025-04</span></div><p>245 个手工场景、5 类任务；改脚本把起始场景对齐到目标场景</p></div></div><div class="tl-col" style="--c:#6380d6"><div class="tl-date">2026-01 – 2026-05</div><div class="tl-node"></div><div class="tl-title">程序化建模与 CAD</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-vis">视觉相似度</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2601.11109">BlenderBench（VIGA）</a><span>2026-01</span></div><p>看图迭代写 Blender 代码重建场景</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2605.10865">BenchCAD</a><span>2026-05</span></div><p>17,900 个 CadQuery 程序；全部按执行结果判分</p><div class="tl-m later"><span class="bar"><i style="width:95.9%"></i></span><b>95.9%</b><em>厂商自报（GPT-6 Astra，带工具）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.01057">3DCodeBench</a><span>2026-05</span></div><p>212 个类别；失败多来自 API 不匹配</p></div></div><div class="tl-col" style="--c:#4876ea"><div class="tl-date">2026-06 – 2026-08</div><div class="tl-node"></div><div class="tl-title">运行时状态与工程验证</div><div class="tl-chips"><span class="tl-chip m-state">运行时状态</span><span class="tl-chip m-geo">几何与执行检查</span></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.01869">WorldCoder-Bench</a><span>2026-06</span></div><p>2,026 个任务；查 three.js 隐藏运行时状态</p><div class="tl-m"><span class="bar"><i style="width:27.8%"></i></span><b>27.8%</b><em>发布时最好（Core）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2606.11152">P3D-Bench</a><span>2026-06</span></div><p>1,003 题；整体形状对，精确参数做不出</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2607.01766">4DBuildBench</a><span>2026-07</span></div><p>50 个场景；审计物理求解器状态</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2608.09296">CADEngBench</a><span>2026-08</span></div><p>600 个任务；有限元与装配运动学</p></div></div><div class="tl-col" style="--c:#2f6bff"><div class="tl-date">2026-09 – 2026-10</div><div class="tl-node"></div><div class="tl-title">确定性门控与 agent</div><div class="tl-chips"><span class="tl-chip m-geo">几何与执行检查</span><span class="tl-chip m-agent">agent 实测</span></div><div class="tl-card"><div class="nm"><a href="https://3jsbench.com/">3JSBench</a><span>2026-09</span></div><p>744 条检查，必查项全过才算通过</p><div class="tl-m later"><span class="bar"><i style="width:80.0%"></i></span><b>80.0%</b><em>榜单（GPT-6 Astra）</em></div><div class="tl-m later"><span class="bar"><i style="width:49.0%"></i></span><b>49.0%</b><em>榜单（Claude Opus 5.5）</em></div></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2609.06535">3DHarnessBench</a><span>2026-09</span></div><p>4 级工具权限；把 3D 几何还原为 Blender 代码</p></div><div class="tl-card"><div class="nm"><a href="https://arxiv.org/abs/2610.10622">WorldBench</a><span>2026-10</span></div><p>three.js 体素世界；看图与读代码在 32% 的必查项上判断不一致</p></div><div class="tl-card"><div class="nm"><a href="https://huggingface.co/datasets/Qwen/BlenderWorld">BlenderWorld</a><span>2026-10</span></div><p>223 个任务、2,651 条二值 rubric</p></div></div></div></div>
<div class="tl-legend"><span><i style="background:var(--brand)"></i>发布时最好成绩</span><span><i style="background:#b8bfc9"></i>后续成绩（厂商自报或榜单）</span></div>

## 3 Gaps

公开 3D 数据给的是资产，不是代码：能导入渲染的资产只占索引的约 15%，three.js 没有一条公开训练配对，因此 3D 的 Query 与 Verifier 比 Web 更依赖自建。

- 补齐方式：Query 见 Sources 页，Verifier 见 Verifier 页，Harness 见 Train 页

可验证任务需要的 Query（题干）、Verifier（判据）、Harness（运行环境）与难度标注，公开 3D 数据都不稳定提供；许可、可运行、版本三项都要在训练前核对。

1. 资产库只有网格与元数据，没有生成它的代码。
   - [Objaverse-XL](https://arxiv.org/abs/2307.05663)：代码托管侧索引 3,700 万个文件，能被 Blender 导入并渲染的 550 万（14.9%），可商用约 190 万
2. 代码来源规模小，three.js 没有一条公开训练配对。
   - Blender bpy 仓库 6,307 → 56 个可用；three.js 仓库星数 > 10 的 2,401 个；两者都只筛标签与星数，没做可运行性检查
3. 公开基准多用视觉相似度，不提供读场景状态的 Verifier。
   - 本项目 three.js 原型：雪人任务的 6 个候选页面，单张截图相似度全落在 0.973–1.0，分不开好坏
4. 公开基准常不记录 Blender 版本，因此结果不可复现。
   - BlenderGym 未写明所用 Blender 版本
5. 训练前还要核对许可。
   - Blender 官方扩展目录 1,533 个，传染性许可 1,341 个，MIT 4 个
   - Sketchfab 须剔除 NC 许可；问答站条款要求数据不用于模型训练
6. Blender 按版本分叉，每道题须钉死运行时版本。
   - 做法见 Train 页 4.1

## 4 How To Choose

按目标能力选，不按名气选：确定性检查类可以当主指标，VLM judge 只作参考。

| 目标能力 | 用哪些 | 能不能当主指标 |
|---|---|---|
| 程序化建模 | 3DCodeBench、BlenderGym | 能 |
| 几何精度与量程 | 3JSBench | 能，当前量程最好 |
| 动态场景与物理 | 4DBuildBench、WorldCoder-Bench | 能，但量程压在 30% 以下 |
| 精确参数与约束 | BenchCAD、CADTests、Text2CAD-Bench | 能，确定性最高 |
| 装配与部件连接 | P3D-Bench、CADEngBench | 能 |

