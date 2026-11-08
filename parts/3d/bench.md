## 1 Lab Reports

<!--FRONTIER-->

## 2 Three Stacks

3D 的三类技术栈按真值来源分，不按难度分：blender 与 3js 是主力，cad 只当方法来源。

| 技术栈 | 产物 | 真值从哪来 | 本文定位 |
|---|---|---|---|
| blender | Blender Python 脚本 | 场景图可直接读：几何、材质、修饰器、求解器状态 | 主力 |
| 3js | three.js 场景代码 | 无头浏览器里渲染加几何断言，还能读隐藏运行时状态 | 主力 |
| cad | CadQuery 等参数化 CAD 代码 | 尺寸、约束、B-Rep 有效性、可制造性，全部确定 | 辅助 |

1. cad 不是 blender 的简化版。
   - CAD 用精确的 B-Rep 曲面，面向加工；Blender 用多边形网格，面向渲染
   - 列在这里，是因为它的确定性验收与程序化合成可以直接搬到 blender 与 3js
2. 3js 的 benchmark 量程最好，模型差距拉得最开。
   - [3JSBench](https://3jsbench.com/)：744 条检查判 100 道题，必查项全过才算通过；GPT-6 Astra 80.0%、Claude Opus 5.5 49.0%、Kimi K3 23.0%
   - 一半以上检查在数部件、查结构：部件计数 223、结构 160、空间关系 157、任务专属几何 45、文字 12、渲染质量 98
   - 同批尝试的 SigLIP2 相似度均值都在 0.0774–0.1081，跨运行环境噪声 0.005 大于模型间差异 0.004
3. Verifier 确定只是必要条件，量程落在中段才能把模型分开。
   - [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 同样查运行时状态，最好系统不到 30%，前四名挤在 23.0%–27.8%
4. blender 方向的失败集中在 API 层。
   - 3DCodeBench（212 个类别）：首要失败原因是 API 不匹配，不是空间推理错
   - BlenderGym（245 个编辑任务）：最强 VLM 在人类认为简单的任务上仍然失败
5. cad 是唯一进了厂商发布页的 3D 指标，但两家数字不能直接比。
   - BenchCAD：OpenAI 报 GPT-6 Astra 95.9%（带工具，geometric overlap）；Anthropic 报 Claude Opus 5 的 Vision2Code 子任务 0.366 / 0.821（voxel IoU，不带工具 / 带工具，1,000 个文件的子集）
   - 官方榜把两家分数都标为厂商自报、未重新评测

## 3 How To Choose

按目标能力选：确定性检查类可以当主指标，VLM judge 只作参考。

| 目标能力 | 用哪些 | 能不能当主指标 |
|---|---|---|
| 程序化建模 | 3DCodeBench、BlenderGym | 能 |
| 几何精度与量程 | 3JSBench | 能，当前量程最好 |
| 动态场景与物理 | 4DBuildBench、WorldCoder-Bench | 能，但量程压在 30% 以下 |
| 精确参数与约束 | BenchCAD、CADTests、Text2CAD-Bench | 能，确定性最高 |
| 装配与部件连接 | P3D-Bench、CADEngBench | 能 |

