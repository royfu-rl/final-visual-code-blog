# 3D 高质量作品来源调研：three.js / Blender（附 CAD）

**这是素材笔记，不是博客正文。** 交给整合 agent 用。

- 核验日期：除特别注明，全部数字为 **2026-10-28** 本机实测（curl / GitHub API / HF API / 各站 API）
- 口径写在每个数字旁边；没打开过的写「口径待补」，不估
- 与已有章节的关系：`parts/3d/verified.md` §2.1–2.7 已覆盖 Objaverse、BlendNet、MeshCoder、BlenderGym、WorldCoder-Bench、CAD-Recode 等，**本篇不重复**，只补「高质量 / 难 / 可合法拿到」的作品源
- 许可记号：✓ 可训练（CC0 / CC-BY / MIT / BSD / Apache）　△ 有条件（SA、逐条许可、权属存疑、配额）　✗ 不可用（NC、付费墙、无许可、站点封禁）

---

## 0 先看结论

1. **three.js 侧最好的新货是 pmndrs/examples**
   - 211 个 R3F 示例，每个都有 `thumbnail.webp` + `pmndrs.json` 元数据，1:1，MIT
   - 博客现在写「react-three-fiber：0 张图」，说的是主仓；示例早就搬到这个 monorepo 了，**这条需要更正**
2. **2026 年的 GitHub three.js 仓库已被模型产物大量渗透**
   - `topic:threejs` 星 > 100：2026 年新建的 122 个里 **53 个（43%）** 在描述/主题里提到 Claude / Opus / Codex / GPT / agent 等；2023–2024 年新建的 82 个里 **0 个**
   - 口径：仅正则匹配 description + topics，提到 ≠ 全由模型生成；但足以说明**挖 GitHub 必须加日期截断或来源过滤**，否则是在蒸馏别家模型
3. **Blender 侧最硬的是官方 demo 页的 22 个几何节点文件**
   - 程序化、仿真区、重复区、SDF，作者多为 Blender Studio（Simon Thommes），CC0 / CC-BY 为主
   - 配合 NodeToPython（节点树 → Python）可直接变成「代码重建」题
4. **2026 年 9–10 月冒出三个大体量 Blender 代码/工程集，许可三种命运**
   - 3DCode（YipengGao）：12,720 实例 × 2 份脚本，**MIT**，Infinigen 派生，最干净
   - 3DCodeVerse：文本 split 2,028,286 行，**CC-BY-NC-SA**，商用训练不可用
   - BlenderLore：21,449 个 `.blend` + 预览图，声明 Apache-2.0，但来源是 B 站教程配套工程，**权属存疑**
5. **BlenderKit 已改名 Blendkit（2026-06）**，新域名对本机 Cloudflare 403，旧域名 API 仍能查；条款里有无 AI 条款无法核实

---

## 1 three.js

### 1.1 来源排名表

| # | 名称 + 链接 | 拿到什么 | 规模（日期 · 口径） | 许可 | 质量信号 | 难度信号 | 获取方式 | 示例 |
|---|---|---|---|---|---|---|---|---|
| 1 | [pmndrs/examples](https://github.com/pmndrs/examples) | R3F 工程（`src/App.tsx` 等）+ 缩略图 + 元数据（标题/描述/标签/作者/资产许可） | 211 个示例、211 张 `thumbnail.webp`、211 个 `package.json`（git tree 实数） | ✓ MIT；外部资产逐条记在 `pmndrs.json.assets` | pmndrs 官方维护；Chromatic 视觉测试徽章；多为 Paul Henschel 等作者 | 焦散、软阴影烘焙、动态环境图、物理（ballpit）、小游戏 | `npx degit pmndrs/examples/examples/<name>`；整仓 git clone | [caustics](https://github.com/pmndrs/examples/tree/main/examples/caustics) · aquarium |
| 2 | [three.js 官方 examples](https://github.com/mrdoob/three.js/tree/dev/examples) | 单文件 `.html` + 1:1 截图 | `files.json` 616 条（无重复，616 页全部拉下）：webgl 221 · webgpu 238 · advanced 48 · postprocessing 26 · webxr 27 · physics 13 | ✓ MIT | 库作者亲写；CI 像素比对 | 正则打标（616 页）：着色器 GLSL/TSL 199（32%）· 程序化几何 103（17%）· 后处理 94（15%）· GPU 计算 30（5%）· 蒙皮/变形 19 · 物理 16；同时含 ≥3 类难点的 16 页；**不加载外部资产的纯代码页 313（51%）**；中位 224 行，P90 383 行 | raw 直取 | [webgpu_compute_cloth](https://threejs.org/examples/webgpu_compute_cloth.html) · webgpu_tsl_vfx_linkedparticles |
| 3 | [threejs.org 首页精选](https://threejs.org/) × 作者 MIT 仓 | 发现索引（链接 + 缩略图）→ 部分作者仓的完整源码 | 首页精选 421 个项目；其中 24 个托管在 `*.github.io` | 索引本身无许可；逐仓：holtsetio 4/4 MIT，dgreenheck 26/45 MIT | **mrdoob 亲选**，最强的「优雅」信号 | holtsetio：MLS-MPM 流体、程序化水母、软体、布料（WebGPU）；dgreenheck：程序化树 | 解析首页 → 过滤 github.io/GitHub → GitHub API 查许可 | [holtsetio/flow](https://github.com/holtsetio/flow) · [dgreenheck/ez-tree](https://github.com/dgreenheck/ez-tree) |
| 4 | Bruno Simon folio | 完整作品站源码（Three.js + 物理 + 交互） | 2 仓：folio-2019 ★4,750 · folio-2025 ★1,987 | ✓ MIT（两仓 GitHub API） | 业界标杆个人站 | 车辆物理、整站交互、多物体组合 | git clone | [folio-2025](https://github.com/brunosimon/folio-2025) |
| 5 | [ThreeUI Community](https://github.com/MengTo/threeui) | Hero 级 3D 组件源码（React）+ 在线预览 | README：50 个父组件 · 164 个浏览条目（141 变体 + 23 单例） | ✓ MIT（仓）；Pro/Beta 不开源 | Design+Code 出品；README 称日均约 9 万访问（2026-08-26 自报） | 着色器、粒子、滚动联动 | npm `@designcodeio/threeui` / clone | 仓内 `AtTheHorizon` |
| 6 | [Codrops](https://github.com/codrops) | 教程配套 demo 源码 | org 348 仓：MIT 129 / 无许可 219；**2023 年后新建 60 仓里 58 个 MIT**；描述/README 含 three.js 的只有 10 仓 | △ 授权页称「下载 demo 默认 MIT，另有说明除外」（搜索摘要所见，站点 403）；老仓有「不得原样转发」条款 | 编辑精选教程 | 滚动 3D、着色器转场 | GitHub API 按 org + 创建日期过滤 | [CinemaSeatPreview](https://github.com/codrops/CinemaSeatPreview) |
| 7 | [Khronos glTF-Sample-Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) | glTF/GLB 资产（three.js 场景素材，不是代码） | 150 个模型（`model-index.json`）；24 个 showcase | 逐资产（149 份 metadata）：纯 CC0 62 · CC0+商标声明 17 · CC0+Stanford 条款 2 · CC-BY 系 61 · **限制性 7**（CRYENGINE、Adobe Stock、Poser EULA、SCEA、3DRT、NC、NC-SA） | Khronos 官方；标签 showcase / pbrtest | PBR 扩展、动画、KTX/Draco 变体 | raw + 每模型 `metadata.json` | [ABeautifulGame](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/ABeautifulGame)（CC-BY-4.0）；Sponza 为 CRYENGINE 协议，要剔除 |
| 8 | CodePen 公开 Pen | 单页 HTML/JS/CSS | 口径待补（`codepen.io/tag/threejs` 本机 403） | ✓ 官方授权页：「Public pens are automatically MIT licensed」 | Picked Pens | 不定 | 只能经站内/搜索发现 | 博客 web 章已有 CodePen 样例，3D 未单独统计 |
| 9 | GitHub `topic:threejs` | 作品仓 | 星 > 1000：106 仓（MIT 65 · Apache 13 · 无许可 14 · AGPL 5）；星 > 100 且 2026 年新建：122 仓，**43% 提到 AI 模型** | 逐仓 | 星数 | 不定 | search API（未鉴权 10 次/分） | [xr843/insect-world](https://github.com/xr843/insect-world)（MIT，63 种昆虫，程序化身体） |

**补充（非作品，但能直接用）**

- [Rapidata/text-to-3d-with-llm-code](https://huggingface.co/datasets/Rapidata/text-to-3d-with-llm-code)：44,482 组两两对比、780,424 张人工票、14 个模型、500 条 prompt；三个问题：几何错误 / 对齐 / 美观；✓ CC-BY-4.0；代码语言卡片未写（口径待补）→ **奖励模型 / 判别力校准用**
- [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)：703 条真实用户 prompt（其中 3D 场景精选 14 条），MIT → **只取 query 侧**；产物是别家模型输出，不能当答案

### 1.2 Top 5 推荐

1. **pmndrs/examples** — 唯一同时有「工程 + 缩略图 + 结构化描述 + 资产许可」的 three.js 系作品库，MIT
2. **three.js 官方 examples** — 难度分布已能量化（32% 着色器、5% GPU 计算），一半是纯代码页，最适合作为难题种子
3. **threejs.org 精选 × MIT 作者仓** — 质量信号最强（mrdoob 亲选），holtsetio 四个仓全是 WebGPU 物理/程序化，是「难」的上限
4. **Bruno Simon folio** — 整站级多物体组合 + 物理 + 交互，适合做长任务 / 分部件拆题
5. **ThreeUI Community** — 「优雅」维度的代表：hero 级视觉组件，MIT，可直接 npm 安装渲染

### 1.3 怎么挖成可验证任务

- **发现**
  - 官方：`examples/files.json`；pmndrs：遍历 `examples/*/pmndrs.json`
  - 精选：解析 threejs.org 首页 → 留 GitHub / github.io → API 查许可，只留 MIT/Apache/BSD
  - 过滤日期：仓库 `created_at < 2025-01-01`，或描述/README 不含模型名，避免蒸馏污染
- **拉取**
  - 单文件页 raw 直取；工程用 degit，锁定 three 版本（importmap / lockfile）
  - 外部资产逐条对许可（pmndrs.json.assets、glTF metadata.json）
- **运行 / 渲染**
  - 无头 Chromium，固定时钟与随机种子，四视角截图
  - 读运行时场景图（traverse 计数网格、材质、灯光、动画轨道）→ 生成确定性断言
- **筛选**
  - 零 JS 报错、非空帧、两次运行像素一致（确定性）
  - 按难点打标（着色器 / 计算 / 物理 / 蒙皮），分档出题
- **出题形态**
  - 截图 + 描述 → 重写（判据：运行时断言，不只看像素）
  - 扰动即监督：改一个参数或删一段着色器，给目标图，要求改回
  - 工程级：pmndrs 示例按组件拆成补全题

### 1.4 诱人但不能用（或慎用）

| 来源 | 原因 |
|---|---|
| three.js 论坛 Showcase | 本机 403（两个代理都被封，Discourse 报 IP 受限）；博客已标「无内容许可」 |
| [img2threejs 展示库](https://github.com/img2threejs/img2threejs-showcase) | 30 个图生 three.js 代码作品，质量很高；但**仓库无 LICENSE（API license=None，LICENSE 文件 404）**，题材含游戏 IP（CS2 皮肤、英雄联盟角色）；主仓 img2threejs 是 Apache-2.0 的工具，不是作品 |
| Shadertoy | 未声明许可的 shader 默认 **CC BY-NC-SA 3.0**（官方条款页，经搜索摘要确认；站点对本机 403） |
| Three.js Journey | 付费课（Three.js $95 / 打包 $120，共 87 课）；课程代码未见开源许可 |
| Spline 社区 | 文档写「社区文件 CC BY 4.0」，条款页（搜索摘要）写默认「Standard Commercial License」，两处冲突；代码导出从 Spline 托管地址加载场景，不是可编辑的 three.js |
| js13kGames WebXR | org 227 仓，抽前 100 个：**83 个无许可**、MIT 只有 12 |
| Awwwards / FWA 获奖站 | GitHub 搜「awwwards threejs」星 > 100 只有 6 仓，全是书签/清单，没有作品源码 |
| 3DCodeVerse `threejs_coding_agent` | 490 页，标 CC-BY-4.0，但全由 Codex / Fable / Opus 等编码 agent 生成——**是别家模型输出** |
| [threejs-gamecode-instruct-v3-ultra](https://huggingface.co/datasets/agagasf123123/threejs-gamecode-instruct-v3-ultra) | 52,200 行，卡片自称「模板程序化合成」，license: other |

---

## 2 Blender

### 2.1 来源排名表

| # | 名称 + 链接 | 拿到什么 | 规模（日期 · 口径） | 许可 | 质量信号 | 难度信号 | 获取方式 | 示例 |
|---|---|---|---|---|---|---|---|---|
| 1 | [Blender 官方 demo files](https://www.blender.org/download/demo-files/) | `.blend` / `.zip` 工程 | 页面直链 87 个（去重）：几何节点 22 · 启动画面 16 · EEVEE 11 · 仿真 6 · 物理 6 · 雕刻 6 · Cycles 6 · 渲染 4 · 资产包 3 | 页面逐条标注：CC-BY 30 · CC0 20 · CC-BY-SA 10 · **未标 27**（多在 EEVEE / 物理 / 雕刻区） | 官方挑选；启动画面 = 每个版本的封面作品 | 仿真区（布料撕裂、碎裂、2D 烟雾）、重复区分形 raymarch、SDF 布尔、毛发节点、4D 高斯 | 解析页面 → HTTP 直下（抽 4 个均 200） | [jiggly_pudding.blend](https://www.blender.org/download/demo/geometry-nodes/jiggly_pudding.blend)（CC0）· mesh_fracturing.blend（CC0） |
| 2 | [3DCode / 3DCodeData](https://huggingface.co/datasets/YipengGao/3DCode) | **独立可运行的 bpy 脚本**（全材质 + 纯几何两版）+ 2 种描述 + 4 视角渲染 + GLB | 212 工厂 × 60 种子 = 12,720 实例；HF 可见 `.py` ≥ 14,994、`.glb` ≥ 14,778（siblings 截断在 10 万文件，实际更多）；另含 81,605 份模型生成脚本日志 | ✓ MIT（卡片）；上游 Infinigen BSD-3 | 由 Infinigen 程序化生成器转写，脱离 infinigen 可独立跑（Blender 5.0） | 程序化植物、家具等 212 类 | `datasets` / `huggingface-cli` | [ArmChair_seed0.py](https://huggingface.co/datasets/YipengGao/3DCode/blob/main/3DCodeBench/ArmChair_seed0/ArmChair_seed0.py) |
| 3 | [Poly Haven](https://polyhaven.com/) | 模型 `.blend` + glTF + USD + FBX；HDRI；贴图 | API：模型 521 · HDRI 997 · 贴图 869；抽 25 个模型 **25/25 同时有 .blend 与 glTF** | ✓ CC0；用实时 API 需署名「Powered by Poly Haven」 | 下载量（最高 grass_medium_01 约 24.7 万次）；成套主题集（project_lighthouse 112 件、the_shed 69 件） | 植被高面数（tree_small_02 约 465 万面）、写实材质 | 公开 API | [jacaranda_tree](https://polyhaven.com/a/jacaranda_tree) |
| 4 | [Blender Open Data 基准场景](https://download.blender.org/release/BlenderBenchmark2.0/scenes/) | 生产级 `.blend` 场景 | 9 个：barbershop_interior · bmw27 · classroom · fishy_cat · junkshop · koro · monster · pavillon_barcelona · victor | demo 页标注：classroom CC0、fishy cat CC0、barbershop CC-BY、pavillon CC-BY；**其余 5 个口径待补** | 官方性能基准，34.7 万次社区跑分 | 开放电影镜头级复杂度（junkshop 352 MB） | 目录直下 | [junkshop.tar.bz2](https://download.blender.org/release/BlenderBenchmark2.0/scenes/junkshop.tar.bz2) |
| 5 | [Blender Studio](https://studio.blender.org/characters/) | 带绑定角色 `.blend`、开放电影资产 | 角色库 52 个，**标 Free 的 22 个**；影片生产文件多为「Subscribe to view」 | 条款：「除另行说明，所有数字内容（含 3D 数据）CC-BY 4.0」；但生产文件付费墙 | 开放电影原资产 | 绑定、毛发、着色 | 免费角色可直接下；生产文件需订阅 | [Rain v3](https://studio.blender.org/characters/rain/v3/)（Free） |
| 6 | [BlendSwap](https://www.blendswap.com/) | 社区 `.blend` | 首页 25,869 资产；按许可筛选末页号 × 24 估上界：CC0 ≈ 7.8k · CC-BY ≈ 13.0k · CC-BY-SA ≈ 1.6k · CC-BY-NC ≈ 0.7k；场景类 CC0 ≈ 456 / CC-BY ≈ 816 | △ 上传者自选 CC（含 NC/ND）；FAQ 明说「能否用于模型训练取决于上传者声明的许可」 | Staff Pick 标签；渲染器与 Blender 版本标注 | 写实室内 + FLIP 流体等 | **免费账号每日 5 个（About 页）/ 7 个（MCP 页），两处不一致**；有 API key / MCP | [Peach & Navy Bathroom – Cycles + FLIP](https://www.blendswap.com/blend/33038)（CC0, Staff Pick） |
| 7 | BlenderKit → [Blendkit](https://www.blendkit.com/) | `.blend` + glTF 资产 | 旧域名 API：模型 ≥ 10,000（计数封顶）；**CC0 模型 4,067（免费 2,563）**；场景 4,721（免费 1,086，CC0 76）；节点组 363（免费 217，CC0 4） | △ 两种：Royalty Free（不得原样转售/再分发）与 CC0；条款页 403，**AI 条款无法核实** | API 带 `ratingsAverage.quality` 与作者自报工时（如 Ship Pinnace：quality 10、200 h） | 场景级资产（Character Sci-Fi visualization 等） | API 搜索；下载需账号 | [Ship Pinnace（CC0）](https://www.blenderkit.com/api/v1/assets/179aa581-9052-48dc-8c4e-ef40c0470ebe/) |
| 8 | [Sketchfab](https://sketchfab.com/) | glTF/GLB/USDZ/源文件（下载需登录 OAuth） | search API 二分（offset 上限约 1 万，仅对小查询有效）：**Staff Pick 且可下载 2,514**，其中 CC-BY 1,837 · CC0 89 · CC-BY-SA 46；同条件下带 NoAI 标签 323；可下载 CC0 共 8,677 | △ 逐模型；**NoAI 标签受站方条款约束不得用于生成式 AI**（2023-03 条款，搜索核实） | Staff Pick、点赞数 | 室内全场景（Abandoned Warehouse 约 62 万面） | API | [Abandoned Warehouse（CC-BY, Staff Pick）](https://sketchfab.com/3d-models/none-1d5285f2e0fd4211a27c8042496d5959) |
| 9 | [CGArtPython/blender_plus_python](https://github.com/CGArtPython/blender_plus_python) | 生成艺术 bpy 脚本 | 24 个项目、76 个 `.py`；**30 组 `_start.py` / `_done.py` 成对** | ✓ MIT（作者 11 仓全 MIT） | 教程系列，人写 | Truchet 拼贴、形变循环、几何节点 | git clone | [truchet_tiles_done.py](https://github.com/CGArtPython/blender_plus_python/blob/main/art_projects/truchet_tiles/truchet_tiles_done.py) |
| 10 | [BlenderLore](https://huggingface.co/datasets/FreedomIntelligence/BlenderLore) | `asset.blend` + `preview.png` + `tutorial.md` | 已传 21,449 组（目标 22,360），614 GB；2,286 组目录名含 B 站 BV 号 | △ 卡片声明 Apache-2.0，但是「视频配套工程」，**原作者权属未说明**；抽查的 tutorial.md 是模板化套话 | 来自真实教程作者 | 不定 | HF | [00001_rw1-BV1124y1M7Tf](https://huggingface.co/datasets/FreedomIntelligence/BlenderLore/tree/main/assets/00001_rw1-BV1124y1M7Tf) |
| 11 | [3D-Front-Code](https://huggingface.co/datasets/KevinFan111/3d-front-code) | 物体 bpy 程序 + 房间布局代码 + 渲染 | 物体 13,917 · 房间 21,202 | △ 卡片 Apache-2.0，但写明「第三方源数据与渲染衍生物可能另有条款」，上游 3D-FRONT 需按原条款取得 | — | 室内整屋布局 | HF tar 分片 | 数据集页 |
| 12 | [NASA-3D-Resources](https://github.com/nasa/NASA-3D-Resources) | GLB / STL / 少量 .blend | 227 个模型目录；`.glb` 257 · `.stl` 342 · `.blend` 13 | △ 仓库无 LICENSE，按 NASA 媒体使用指南 | 官方 | 航天器结构 | git / tree API | 仓库页 |

**工具（不是作品，但决定 .blend 能不能变成代码题）**

- [NodeToPython](https://github.com/BrendanParmer/NodeToPython)：把几何节点/着色器节点组转成 Python 插件代码，GPL-3.0（工具许可，不约束输入）
- [geometry-script](https://github.com/carson-katri/geometry-script)：用 Python 写几何节点，GPL-3.0
- [ProcFunc](https://github.com/princeton-vl/procfunc)（arXiv 2604.26943，2026-04-29）：Infinigen 团队的函数式程序化生成库，BSD-3；论文称 VLM 用它编辑程序化代码出错更少
- [Infinigen](https://github.com/princeton-vl/infinigen)：已在博客；2026 有新渲染数据 [infinigen2-flying-indoors](https://huggingface.co/datasets/infinigen/infinigen2-flying-indoors)（视频 + 真值，BSD-3，不含代码）

### 2.2 Top 5 推荐

1. **官方 demo files 的几何节点 + 仿真区（28 个）** — 难度最高、作者最权威、许可最清楚（多数 CC0/CC-BY），可经 NodeToPython 变代码
2. **3DCode（3DCodeData）** — 现成「描述 + bpy 脚本 + 4 视角 + GLB」四元组，MIT，规模万级，唯一可直接当 SFT 配对的干净大集
3. **Poly Haven** — CC0 + 每个模型都有 .blend，成套主题集适合做多物体组合题
4. **Blender Open Data 场景 + 启动画面文件（9 + 16）** — 生产级完整场景，当「编辑类」题的起始状态最合适
5. **BlendSwap / Blendkit 的 CC0 子集** — 规模最大的人写 .blend 池（CC0 合计数千），有 Staff Pick / 质量评分可排序；受下载配额限制，适合小批精选

### 2.3 怎么挖成可验证任务

- **发现**
  - demo 页：按区块解析直链与许可（脚本已验证可行）
  - Poly Haven：`api.polyhaven.com/assets?t=models` + `/files/<id>`
  - Blendkit：`query=license:cc_zero` + 按 quality 排序；BlendSwap：`?license=CC-0` + Staff Pick
  - 只留 CC0 / CC-BY；SA 单独桶；NC、ND、未标注一律丢
- **拉取**
  - 记录页面上的「Requires Blender X.Y」，按版本分桶（博客 §4.1：Blender 按版本分叉）
- **运行 / 渲染**
  - `blender -b --factory-startup`，**保持 autoexec 关闭**（.blend 可内嵌 Python；注意 Open Data 官方离线命令用的是 `--enable-autoexec`，不要照抄）
  - 多视角渲染 + 导出场景图 JSON（物体、修改器、节点树、仿真区）
- **转成代码**
  - 节点组 → NodeToPython → bpy；或把 .blend 当起始状态，题目要求写编辑脚本
- **筛选**
  - 渲染非空、两次渲染一致、外部贴图不缺
  - 难度打标：节点数、是否含仿真/重复区、修改器栈深度
- **出题形态**
  - 节点树重建：给渲染 + 描述，写出等价 bpy / 几何节点代码，按场景图字段判分
  - 扰动即监督：改 demo 文件里一个节点参数，给目标渲染，要求改回
  - CGArtPython 的 30 组 start/done：天然的「补全到成品」题

### 2.4 诱人但不能用（或慎用）

| 来源 | 原因 |
|---|---|
| Blender Studio 开放电影生产文件（Charge、Sprite Fright、Gold、Singularity…） | 许可 CC-BY 4.0，但镜头文件大多「Subscribe to view」——要付订阅；只有角色库 22 个与少量 Freebie 可免费拿 |
| [3DCodeVerse](https://huggingface.co/datasets/ilabai/3dcodeverse)（arXiv 2610.22341） | 文本 split 2,028,286 行，覆盖 Blender / three.js / Shadertoy / CadQuery / OpenSCAD；**整体 CC-BY-NC-SA**，卡片有门禁表单（API 显示 gated=False）；其内 Blender 子集来源（3dcodebench BSD-3、bioinspired3d MIT）可绕回上游直接取 |
| BlenderLore | 见上表：许可声明与来源权属不匹配 |
| Sketchfab NoAI 标签模型 | 条款明确禁止用于生成式 AI；Staff Pick 可下载里约 13%（323 / 2,514）带此标签 |
| Blendkit Royalty Free 资产 | 禁止原样再分发 → 不能打包成数据集分发；AI 条款页 403 未核 |
| [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial) | 3 个相关仓全部无 LICENSE |
| Blender 内置 Essentials 资产库 | 许可未找到明确声明（口径待补） |
| download.blender.org 老开放电影 | `demo/bbb/blender.zip`（830 MB，2013-12-16）等可直下；内容未展开核实，且是 2.4x–2.6x 时代文件，新版兼容性未知 |
| Smithsonian 3D、McGuire 图形档案、NVIDIA ORCA | 本机 403 / API 限流 / 页面无许可信息，**口径待补**，未入表 |

---

## 3 CAD（辅助，只记新增）

| 名称 | 拿到什么 | 规模 | 许可 | 结论 |
|---|---|---|---|---|
| [Thingiverse OpenSCAD（经 redcathode 整理）](https://huggingface.co/datasets/redcathode/thingiverse-openscad) | `.scad` 源码 + 缩略图 + 合成 prompt | 7,378 行 | 逐条：CC-BY 3,023 · CC-BY-SA 2,143 · **NC 系 1,880（25%）** · 公有领域 254 · BSD 78；数据集本身 CC-BY-NC-SA-4.0 | 要用就回 Thingiverse 按原许可重取，剔 NC（Thingiverse 对本机 403） |
| [Fusion 360 Gallery](https://github.com/AutodeskAILab/Fusion360GalleryDataset) | 构造序列 / B-Rep | 口径待补 | ✗ LICENSE.md：「仅限非商业研究」 | 不可用 |
| 3DCodeVerse 路线图 | deepcad 174k（MIT）· articraft 10k（CC-BY）· thingiverse 50 题 | 卡片标「Captioning」中 | 见各源 | 只当线索 |

---

## 4 2025–2026 新数据集 / 基准（博客未收）

- **数据**
  - 3DCodeVerse（2026-10-15，arXiv 2610.22341）：见 2.4
  - 3DCode 数据侧（arXiv 2606.01057 的配套）：见 2.1 #2；博客只收了 3DCodeBench 的基准侧
  - BlenderLore（HF 建于 2026-09-05）、3D-Front-Code（2026-09-05）：见 2.1
  - Rapidata text-to-3d-with-llm-code（2026-10-20）：见 1.1 补充
- **基准**
  - [WorldBench](https://arxiv.org/abs/2610.10622)（2026-10-07）：three.js 体素世界；摘要称图像视角与读代码视角在 **32%** 的必查项上不一致
  - [VoxelCodeBench](https://arxiv.org/abs/2604.02580)（2026-04-02）：执行环境是 Unreal，不是 three.js / Blender
  - [aDSL](https://arxiv.org/abs/2608.17975)（2026-08-18）：面向 agent 的 3D DSL，方法论文，非数据

---

## 5 URL 核验清单（2026-10-28）

| URL | 状态 | 方式 / 备注 |
|---|---|---|
| https://www.blender.org/download/demo-files/ | 200 | curl；解析 87 个直链 |
| …/geometry-nodes/jiggly_pudding.blend · …/simulation/mesh_fracturing.blend · …/splash/blender-5.2-splash.blend · …/test/classroom.zip | 200 | HEAD |
| https://download.blender.org/demo/ · /demo/movies/ · /demo/bbb/ · /demo/test/ | 200 | 目录列表 |
| https://download.blender.org/release/BlenderBenchmark2.0/scenes/ · junkshop.tar.bz2 | 200 | 目录列表 / HEAD |
| https://opendata.blender.org/ · /about/ | 200 | curl |
| https://studio.blender.org/films/ · /characters/ · /films/charge/ · /terms-and-conditions · /remixing/ | 200 | curl / WebFetch |
| https://studio.blender.org/characters/rain/v3/ | 200 | curl |
| https://api.polyhaven.com/assets?t=models（及 hdris / textures、/files/<id>） | 200 | API |
| https://github.com/Poly-Haven/Public-API | 200 | WebFetch（API 条款） |
| https://www.blenderkit.com/api/v1/search/ · /api/v1/assets/179aa581-… | 200 | API 仍可用 |
| https://www.blenderkit.com/ | 301 → blendkit.com | curl |
| https://www.blendkit.com/docs/licenses/ · /terms-and-conditions-2026/ | 403 | Cloudflare（两个代理都拦） |
| https://api.sketchfab.com/v3/search | 200 | API |
| https://sketchfab.com/3d-models/none-1d5285f2e0fd4211a27c8042496d5959 | 200 | curl |
| https://www.blendswap.com/ · /3d-mcp-api · /about · /3d/scenes · /blend/33038 | 200 | curl |
| https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/model-index.json（+150 个 metadata.json） | 200 | 149/150 解析成功 |
| https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/files.json（+616 个 html） | 200 | raw |
| https://threejs.org/ · /examples/webgpu_compute_cloth.html | 200 | curl |
| https://github.com/pmndrs/examples（git tree，未截断，4,505 项）· /tree/main/examples/caustics | 200 | API / curl |
| https://github.com/MengTo/threeui · img2threejs/img2threejs · yihui-dev/awesome-opus5-5-videos | 200 | README raw |
| https://img2threejs.io/demos.json | 200 | 30 条 |
| https://raw.githubusercontent.com/img2threejs/img2threejs-showcase/main/LICENSE | 404 | 无许可文件 |
| https://github.com/brunosimon/folio-2019 · folio-2025 · holtsetio/flow · dgreenheck/ez-tree · codrops/CinemaSeatPreview · xr843/insect-world | 200 | API / curl |
| GitHub search：topic:threejs / react-three-fiber / webgl / creative-coding / blender / geometry-nodes / org:codrops / org:js13kGames 等 | 200 | 未鉴权，曾触发 10 次/分限流 |
| https://discourse.threejs.org/（categories.json、/c/showcase/7） | 403 | IP 受限，两个代理均失败 |
| https://tympanus.net/codrops/licensing/ | 403 | WebFetch；许可内容来自搜索摘要 |
| https://blog.codepen.io/documentation/licensing/ | 200 | WebFetch |
| https://codepen.io/tag/threejs | 403 | curl |
| https://www.shadertoy.com/terms | 403 | WebFetch；默认许可来自搜索摘要 |
| https://threejs-journey.com/ · https://docs.spline.design/basics/community-platform | 200 | WebFetch |
| HF：FreedomIntelligence/BlenderLore · ilabai/3dcodeverse · YipengGao/3DCode · KevinFan111/3d-front-code · Rapidata/text-to-3d-with-llm-code · redcathode/thingiverse-openscad · agagasf123123/threejs-gamecode-instruct-v3-ultra · infinigen/infinigen2-flying-indoors · Qwen/BlenderWorld | 200 | HF API + README；3dcodeverse 用 tree API 列目录 |
| arXiv 2610.22341 · 2606.01057 · 2604.26943 · 2610.10622 · 2604.02580 · 2608.17975 · 2605.00632 | 200 | export.arxiv.org API |
| https://raw.githubusercontent.com/AutodeskAILab/Fusion360GalleryDataset/master/LICENSE.md | 200 | 非商业条款 |
| https://api.github.com/repos/nasa/NASA-3D-Resources（git tree） | 200 | 1,199 个文件 |
| https://api.github.com/repos/CGArtPython/blender_plus_python（git tree） | 200 | 76 个 .py |
| https://www.thingiverse.com/thing:1339 | 403 | 本机被拦 |
| https://api.si.edu/openaccess/…（DEMO_KEY） · https://3d.si.edu/ | 限流 / 403 | 未核 |
| https://developer.nvidia.com/orca · https://casual-effects.com/data/ | 200 | 页面无许可信息 / JS 渲染无内容 |

