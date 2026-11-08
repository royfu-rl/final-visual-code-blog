# 素材库：Harness × 「值得蒸馏的题目」

**这不是博客正文，是素材库。** 每条都带出处（文件名:行号）和口径标记，供写正文时直接取用。

整理日期 2026-10-19。数据源（只读）：
- `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/`（下文引用只写文件名）
- `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/`（下文引用写 `vc_verifier/...`）

## 口径标记约定

| 标记 | 含义 |
|---|---|
| 【本机实测】 | 这批笔记自己跑出来的，有脚本和日志可复跑 |
| 【公开引用】 | 论文 / 榜单 / 官方文档里的数字 |
| 【估】 | 笔记自己标明是估计或外推 |
| 【未核实】 | 笔记自己标了「未核实」「推测」 |
| 【已更正】 | 与 `92_number_audit.md` 交叉核对后换成更正后的版本，原值一并列出 |
| ⚠️ | 本次整理过程中新发现的口径问题，见文末附录 |

---
---

# 主题 A：Harness

---

## A1. Web 生成类任务的 sandbox 形态：参考素材多、没有繁复代码仓库、上下文比 SWE 短

论点要三条腿：**(a) 素材供给侧是「代码+参考图成对、单文件」而不是「整仓」；(b) 环境侧是一个镜像管所有任务，而不是每实例一个镜像；(c) 轨迹侧的上下文量级比 SWE 少一个数量级。** 三条都有数字。

### A1.1 素材供给：成对、单文件、体积小

- **three.js 官方 examples：610 个 html ↔ 610 张截图，配对率 1:1。** 走 git tree API 全树 6,413 条、`truncated=false`。`13_scaling_tasks.md:1232-1239`【本机实测】
  - 已被 `92_number_audit.md:12` 独立核过（读 dev 分支文件树，未截断）：610，一致。
- **单条体积：中位 6,137 字节（约 150~200 行），p95 13,651，最大 66,143；全部 examples 总计 4.4 MB。** `13_scaling_tasks.md:1240-1241`【本机实测】
  - 这是「没有繁复代码仓库」最直接的计价：**一道题的全部上下文就是一个 6 KB 的单文件页面**。
- **API 面：`examples/jsm/*.js` 496 个 + `src/*.js` 755 个 = 1,251 个 API 面**，可以直接当多样性覆盖率的分母。`13_scaling_tasks.md:1242-1247`【本机实测】
- **笔记自己的读法：「610 条是种子池的天花板，不是规模池」。** `13_scaling_tasks.md:1245`
- **像素基线仓库的总供给：9 个仓库改过基线的 commit 合计 3,413 个，参考图合计约 1.9 万张。** `02_task_sources.md:26`、`02_task_sources.md:223`【本机实测】
  - 分仓明细 `02_task_sources.md:28-41`：primer/react 7,766 张、maplibre 1,950、pixi 1,711、plotly 1,324、Chart.js 约 667、p5.js 604、deck.gl 252、openlayers 235 个 case；three.js 610、Babylon 975、Blender 2,596。
  - `92_number_audit.md:12-14` 独立核过三项：three.js 610、Babylon.js 975、Blender 2,596，**全部一致**。
- **three.js 自己的 e2e 判据就是现成的像素闸**：puppeteer 渲 400×250，`pixelThreshold=0.1`、`maxDifferentPixels=0.1%`，注入确定性随机数与时钟，54 个 example 在豁免名单，README 自称覆盖 97% 的 example。`02_task_sources.md:30`【公开引用】

### A1.2 环境侧：SWE 是「每实例一个镜像」，Web 是「一个镜像挂几百道题」

- **SWE 系训练 harness 的镜像规模**（`06_harness.md:233-238`【公开引用】）：
  - SWE-Gym：2,438 个实例，**每个实例一个预构建镜像**
  - R2E-Gym：8.1K 题
  - SWE-smith：50k 实例
  - **OpenSWE：45,320 个 Docker 环境**
- **SWE-smith 的环境存储实测：50,137 个实例 → 环境存储 295 GB**（另约 20 人工小时、1,360 美元）。`13_scaling_tasks.md:1262`【公开引用】
  - 折算约 **6 MB/实例的环境存储**，且这是压缩后的增量口径，不含基础层。
- **本项目的对照做法：按「依赖集」而不是按「任务」建镜像——一个 three 版本 + 一套 vendored 资产 = 一个镜像，下面挂几百个任务。** `08_rl_recipe.md:1120-1121`
- **镜像体积实测**（`06_harness.md:321-323`、`08_rl_recipe.md:1122`【本机实测】）：
  - `chrome-linux64` 目录 **552 MB**
  - `node_modules`（puppeteer-core + three + playwright-core）**65 MB**
  - → **Web 层整套约 0.6 GB，一次性**，不随任务数增长
  - 对照 3D 层：bpy 4.5 的 site-packages **784 MB**；apt blender + blender-data 约 **181 MB** 安装体积（`06_harness.md:83`）
- **社区 Blender 镜像体积**（【公开引用】，`06_harness.md:76-81`）：nytimes/blender 约 **514 MB**（已停更 3 年以上）；linuxserver/blender 有 5.1.0 tag、约 **1.3 GB**，但那是 KasmVNC 桌面镜像、不是批处理镜像、也不支持 GPU 渲染。
- **任务产物存储**（`13_scaling_tasks.md:1600-1602`【本机实测折算】）：
  - three.js 单任务 = 源码约 5 KB + 9 视角 JPEG 约 9×15 KB + 48³ 稀疏体素约 50 KB ≈ **0.2 MB** → 10 万任务约 **20 GB**
  - Blender 单任务 = ref.py 约 4 KB + state.json 约 30 KB + 10 视角 PNG 约 10×30 KB + points.npz 6 万点约 700 KB ≈ **1 MB** → 10 万任务约 **100 GB**（`.blend` 不存，由 ref.py 确定性重建）
  - → **Web/three.js 的单任务存储是 Blender 的 1/5，是 SWE-smith 环境存储的 1/30**

### A1.3 启动耗时

| 环节 | 实测 | 出处 | 口径 |
|---|---|---|---|
| 启动 chrome | **172 ~ 191 ms** | `06_harness.md:279` | 【本机实测】 |
| 加载场景直到 ready 钩子 | **401 ~ 420 ms** | `06_harness.md:280` | 【本机实测】 |
| 浏览器启动（Web/DOM 线独立复测） | **181 ms** | `14_web_verifier.md:638`、`vc_verifier/web/BENCH_LOG.md:30` | 【本机实测】 |
| 新开页 + 加载 | **61 ms** | `14_web_verifier.md:639` | 【本机实测】 |
| 复用浏览器开 5 个页 | **248 ms（约 50 ms/页）** | `14_web_verifier.md:642` | 【本机实测】 |
| Blender 单进程启动 + bpy 导入 | 2.3 s 里约 **0.5 s** | `10_blender_tasks.md:871` | 【本机实测】 |
| 每个 blender 进程启动和加载 | 约 **1 s** | `06_harness.md:357` | 【本机实测】 |
| E2B 沙箱冷启动 | 300 ~ 500 ms（自报） | `06_harness.md:112` | 【公开引用，厂商自报】 |
| Morph Cloud snapshot/branch | < 250 ms | `06_harness.md:116` | 【公开引用，厂商自报】 |

读法：**Web 侧「冷启动一道题」是百毫秒量级（启动 180 ms + 加载 60 ms），复用浏览器后降到 50 ms/页。** 而 SWE 类任务的单位是「拉起一个预构建的实例镜像」，笔记里没有这一项的本机实测数字——**这是论点的一处证据缺口**。

### A1.4 上下文量级：和 SWE 差一个数量级（最硬的一组对照）

**本项目推算的一条 visual coding 轨迹的 token 账**（40 步多轮，图像走 3 张滑窗 contact sheet）。`08_rl_recipe.md:1143-1154`【估，基于本机实测的单位成本】

| 项 | 数量 |
|---|---|
| 系统提示 + 任务（含参考图） | 3,000 |
| 每步模型输出（think + 代码 + 工具调用） | 800 |
| 每步文本观察（scene graph 摘要 + console） | 300 |
| 常驻图像（3 张 1024×512 contact sheet） | 2,109 |
| **终局上下文** | **约 49,000** |
| **累计输出** | **32,000** |
| **累计输入（无 prefix cache）** | **约 1.06 M** |
| 其中图像部分 | 约 84 k（3 × 703 × 40，滑窗内的图每步重读） |

**公开的 SWE 轨迹 token 账（对照）**。`08_rl_recipe.md:1160-1167`【公开引用】

| 来源 | 每条轨迹 |
|---|---|
| SWE-Gym | 491 条 SFT 轨迹平均约 **19 轮、约 19,000 token** |
| **SWE-Master 表 6**（SWE-bench Verified，resolve 61.4%） | **输入 5,549.6k（≈5.55 M）、输出 32.5k、平均 111.2 轮** |
| 同上 + LSP 工具 | **4,232.1k / 27.2k / 91.7 轮**（输入 −23.7%、输出 −16.3%、轮数 −17.5%），resolve 61.0% |
| SWE-Master 表 5（前沿模型在 R2E-Gym scaffold） | MiniMax-M2.1 **82.0 轮**、GLM-4.7 **97.3 轮** |

**可直接写进正文的三句读法**（`08_rl_recipe.md:1169-1176`）：
1. **输出量几乎一致（32 k vs 32.5 k），但输入少 5 倍**（1.06 M vs 5.55 M）——因为步数假设是 40 而不是 111。
2. **「输入 token 基本等于步数的平方量级」，所以控制步数比控制单步长度重要得多。** 降 20% 轮数 ≈ 降 36% 输入 token（`08_rl_recipe.md:1513`）。
3. **图像只占累计输入的 8%；上下文爆炸的主因是文本历史，不是图像。** `08_rl_recipe.md:1157`
4. 配套事实：SWE-Master 剪掉超过 **80 K token 或 100 turn** 的实例，这类只占已解决实例的 **5%** 但 OOM 风险不成比例。`08_rl_recipe.md:1175`
5. 配套事实：**给 agent 更强的结构化观测工具等于直接省 token**——SWE-Master 加 LSP 后输入 −23.7%、轮数 −17.5%，分数基本不变（61.4% → 61.0%）。笔记的类比是「`get_scene_graph` 就是 three.js 的 LSP」。`08_rl_recipe.md:1173-1174`、`08_rl_recipe.md:1501-1513`

### A1.5 构造漏斗：Web 侧「真实挖矿」的天花板和 SWE 一样低，但「合成/变异」高得多

| 管线 | 起始 | 关键步 | 总保留率 | 最终 | 出处 / 口径 |
|---|---|---|---|---|---|
| SWE-bench | 12 仓 / 爬 **93,139 PR** | attribute filter → 11,407（12.25%）；执行校验（≥1 条 F2P）→ 2,294（占上步 20.1%） | **2.46%** | 2,294 | `13_scaling_tasks.md:1259`【公开引用】 |
| SWE-bench Verified | 2,294 | 抽 1,699 条人工标注（每条 3 名标注员），判废 **68.3%** | **21.8%**（500/2,294） | 500 | `13_scaling_tasks.md:1260`【公开引用】 |
| SWE-smith | 128 仓 → **100,074 个 bug 候选** | 执行校验 | **50.1%** | 50,137 | `13_scaling_tasks.md:1262`【公开引用】 |
| SWE-bench M | 135k PR | → 1,478 候选 → 617 实例；人工核验 **83.5%** 的实例图像对解题必要；**69 个实例**用像素级截图测试判功能 | — | 617 | `03_verifiable_construction.md:69`【公开引用】 |
| **本项目 three.js 真实素材线** | 2,401 个仓库（`topic:threejs stars:>10`） | 六步，见下 | **端到端约 3.2%** | **约 230 个任务** | `13_scaling_tasks.md:1328-1341` |
| **本项目合成/变异线** | — | 自动造题 + 三条准入 | **本机实测 88~96%** | — | `13_scaling_tasks.md:1311`【本机实测】 |

本项目 three.js 真实素材线的逐步保留率（`13_scaling_tasks.md:1328-1341`）：
```
GitHub three.js 仓库（topic:threejs stars:>10）        2,401 个仓库  【实测】
  ↓ 抽单文件自包含页面（<script type="module"> 且无私有资产）  约 20%  【估】
  ↓ 无头浏览器能跑起来且渲出 >=1 个 mesh（L0 执行门）          约 60%  【估】
  ↓ 能被 __THREE_DEVTOOLS__ 抓到 scene                        约 95%  【半实测】
  ↓ 冻结时钟后两次渲染逐字节一致                              约 70%  【估】
  ↓ 自动造题（LLM 提破坏）+ 三条准入                          约 90%  【实测 88~96%】
  ↓ 去重 + 可解性闸 + 难度带                                  约 45%  【估】
                                                   端到端约 3.2%
```
笔记自己的结论（`13_scaling_tasks.md:1340-1341`）：**「这就是真实素材路线的真实量级：三位数，不是五位数。它的价值不在产能，在多样性注入，所以配比应该按『多样性需求』定，不按产能定。」**

- 名义池 vs 真·可用池的收缩倍数（`13_scaling_tasks.md:1223-1230`【本机实测 + 公开】）：
  - three.js 代码仓库：`q=three.js` 89,622 / `topic:threejs` 23,983 → `topic:threejs stars:>10` **2,401**，**约 37 倍收缩**
  - bpy 脚本仓库：`q=blender addon` 6,307 / `q=bpy` 1,299 → `bpy language:Python stars:>10` **56**，**约 10~100 倍收缩**
  - CodePen：1,000 万 pen（2016-11 官方数字，此后无更新）→ 公开 dump 约 2.5 万，**约 400 倍收缩**，且无列举/搜索 API
  - Objaverse-XL：元数据 10,850,997 行 → **只有 5.5 M 能被 Blender 成功导入渲染**；商用可用 CC 约 1.9 M
- **带截图的 issue 能成型的量级：约 1,400 个。** `92_number_audit.md:84`【已更正】
  - 原稿写「约 1 万量级」（见 `02_task_sources.md:224`「候选 issue 约 30 万；能成型的估计在 1 万量级」），与自己引的 0.457% 转化率矛盾，**已更正为约 1,400 个**。**引用这个数时必须用 1,400。**

---

## A2. Blender 的版本适配 vs three.js 的免适配

**先给结论（这是本次整理最需要向读者交代的一处）：这个对比在本地笔记里是「半实测」——Blender 侧有多条本机实测的跨版本不兼容证据；three.js 侧的「免适配」只有一条半实测（取证通道跨引入方式通用）加一条推断（浏览器环境统一），而且笔记里还记了三处 three.js 侧确实需要适配的坑。** 详见 A2.4。

### A2.1 为什么要适配多个 Blender 版本

- **本机就同时装了两个版本，而且不是为了做实验，是被迫的**：系统 apt 的 `/usr/bin/blender` 是 **4.0.2（EEVEE Legacy）**；另用 uv 建 Python 3.11.14 venv 装 **bpy 4.5.14 LTS（EEVEE Next）**。`06_harness.md:327`、`10_blender_tasks.md:4-5`、`vc_verifier/BENCH_LOG.md:14-19`【本机实测】
- **pip bpy 每个版本只绑一个 Python 小版本**（PyPI JSON 实查）：**4.0 → 3.10；4.1 ~ 5.0 → 3.11；5.1 / 5.2 → 3.13**。`06_harness.md:71-73`、`10_blender_tasks.md:860`【本机实测】
  - 本机 Python 是 3.12，所以**必须另建 venv**。`06_harness.md:76`
  - 含义：**「支持 N 个 Blender 版本」= 要维护 N 个 Python 运行时**，这是镜像分层的硬约束，不是可以调的参数。
- **4.0、4.1 已从 PyPI 下架**，要到 `download.blender.org/pypi/bpy/` 取。`06_harness.md:74`【本机实测】
- **内网 pypi 镜像列出了 bpy 4.2 ~ 4.4，但下载全部返回 502（未缓存）**，只能走海外代理 `uv pip install "bpy==4.5.*"`，**用时 121 s、包体 784 MB**。`06_harness.md:328-329`、`10_blender_tasks.md:861`、`vc_verifier/BENCH_LOG.md:18`【本机实测】
  - 含义：**版本可得性本身就是一个供给风险**，不是「想装哪个装哪个」。
- **素材侧也绑版本**：3DCodeBench 的管线是「代码简化 → **Blender 5.0 沙箱**执行 → 视觉 critique → mesh 分析 → 人工审核」。`13_scaling_tasks.md:1297`【公开引用】——公开素材是在某个具体版本下验证过的，换版本要重验。
- **BlenderGym 没写明用的哪个 Blender 版本**（245 对起始/目标场景，每对至少 3 个固定机位，指标 Photometric loss / N-CLIP / Chamfer）。`06_harness.md:240-243`【公开引用】——反例素材：**连 CVPR 的 benchmark 都不记版本**，所以复现不了是常态。

### A2.2 不适配会怎样（本机踩到的具体不兼容）

| # | 不兼容 | 具体症状 / 数字 | 出处 | 口径 |
|---|---|---|---|---|
| 1 | **渲染引擎标识符跨版本改名**：4.0 是 `BLENDER_EEVEE`，4.2+ 是 `BLENDER_EEVEE_NEXT` | 同一份 bench 脚本在两个版本上必须传不同的 engine 字符串。`bench_blender.py` 的分支写的是 `elif eng == 'BLENDER_EEVEE'`，在 4.5 上**静默不匹配** | `vc_verifier/bench_blender.py:3`、`:33`；`vc_verifier/BENCH_LOG.md:15` vs `:19` | 【本机实测】⚠️ 见附录 |
| 2 | **EEVEE Next（4.2+）官方要求 OpenGL 4.3 + `GL_ARB_shader_draw_parameters` + `GL_ARB_clip_control`**；EEVEE Legacy 不要求 | 无 GPU 环境下只能走 Mesa 的 surfaceless swrast（llvmpipe）；官方**没说 llvmpipe 能不能跑**，本机实测能跑但慢 | `06_harness.md:61-63` | 【公开引用 + 本机实测】 |
| 3 | **EEVEE Next 在 llvmpipe 上比 Legacy 慢 4~5 倍，首帧 shader 编译 13.3 s** | 8 视角 512：4.0 EEVEE Legacy **7.3 s** vs bpy 4.5 EEVEE Next **33.1 s**；首帧 3.2 s vs **13.3 s**；之后每视角 0.6 s vs **2.8 s** | `06_harness.md:337`、`:343`、`:346-348` | 【本机实测】⚠️ 采样数口径有问题，见附录 |
| 4 | **EEVEE 无头的回退路径是实测出来的，不是文档写的** | 日志实测路径：Mesa 25.2.8 → `DRI2: failed to load driver` → `Falling back to surfaceless swrast without DRM`；bpy 4.5 的日志里是 `EGL Error (0x3001): EGL_NOT_INITIALIZED` → `Managed to successfully fallback to surfaceless EGL rendering!` | `06_harness.md:64`；`vc_verifier/out/bpy45_BLENDER_EEVEE_NEXT_512.log` | 【本机实测】 |
| 5 | **Blender 自动给同名材质节点改名成 `Mix.001`** | 所以材质节点断言**必须按 `bl_idname` 比，不能按 `node.name` 比** | `10_blender_tasks.md:868` | 【本机实测】 |
| 6 | **`-E CYCLES` 只改当前场景**，.blend 里其他 EEVEE 场景照样会要显示 | 无头环境下直接失败 | `06_harness.md:66-68` | 【公开引用：devtalk 讨论帖】 |
| 7 | **bpy 是全局单例**，一个脚本把 `bpy.ops.wm.read_factory_settings` 调歪了会污染后面所有任务 | 本机做法是每个候选起一个 python 进程，**2.3 s 里约 0.5 s 是进程启动 + bpy 导入** | `10_blender_tasks.md:870-872` | 【本机实测】 |
| 8 | **Workbench 的 MATERIAL 着色取 `material.diffuse_color`（viewport 色），不是 Principled 的 Base Color** | 不同步过去**渲出来全是默认灰** | `10_blender_tasks.md:862-863` | 【本机实测】 |
| 9 | **渲染不可跨机器/跨 Mesa 复现** | 官方测试跑在固定设备上；**换 CPU / 换 Mesa 版本像素会漂**。实际做法是「自己用任务容器里那套引擎重渲一张参考图当基线」，不要直接用仓库里的 png | `10_blender_tasks.md:457-458` | 【公开引用 + 工程结论】 |
| 10 | **官方自己按设备维护 BLOCKLIST** | `cycles_render_tests.py` / `workbench_render_tests.py` 都调 `report.set_pixelated(True)`，并维护 `BLOCKLIST_GPU` / `BLOCKLIST_OPTIX` / `BLOCKLIST_METAL` / `BLOCKLIST_VULKAN` | `10_blender_tasks.md:423-424`、`:906` | 【公开引用，实查 main 分支】 |
| 11 | **采样随机源也要按库分别钉** | `trimesh.sample.sample_surface` 用自己的 RNG，`np.random.seed` 对它**无效**，必须传 `seed=`。不传则**参考解自比自的 Chamfer 是 0.00167 而不是 0**，噪声地板直接吃掉一半判别力 | `10_blender_tasks.md:866-867` | 【本机实测】 |

**「不适配会怎样」的量化后果**（可以直接当正文论据）：
- **可执行率**：公开锚点是 Objaverse-XL「能进 Blender」**5.5 M / 37 M ≈ 15%**；笔记对自己 bpy 线的估计是 **15~30%**，对 three.js 线是 **50~80%**。理由原文：**「three.js 环境统一（一个无头浏览器全搞定），比装 Python 依赖容易得多；bpy 跟 Blender 版本 + addon 强绑定。」** `13_scaling_tasks.md:1308`【公开锚点 + 本项目估】
- **端到端挖矿产出**：three.js **1~8%**，bpy **0.3~2%**（文献经验带宽 0.2%~5%）。`13_scaling_tasks.md:1310`【估】
- 笔记自己的一句话总结：**「对 three.js 这是好消息（浏览器环境统一），对 bpy 是坏消息（Blender 版本 + addon 依赖）。」** `13_scaling_tasks.md:1317`
- **GitHub 上的 bpy 脚本「开箱即跑率很低」**：大多依赖仓库里的 .blend、资产路径、add-on。`10_blender_tasks.md:374`【调研结论】
- 配套：**没有发现任何公开工作在做 bpy 脚本的批量挖掘**。`10_blender_tasks.md:372`【调研结论，空位】

### A2.3 three.js 为什么（相对）不需要版本适配

- **取证通道不依赖 three 的版本细节，也不依赖模型配合**：harness 预先定义 `window.__THREE_DEVTOOLS__ = new EventTarget()`，three 的 `Scene` 与 `WebGLRenderer` 构造函数会向它派发 `observe` 事件（three r160 源码 `three.module.js` 第 30938、31088 行）。`90_local_experiments.md:31-33`【本机实测】
- **实测：打包版页面也能抓到。** 把 three 源码整个内联进 `<script type="module">`，页面不发任何网络请求：`{"meshes":4,"renders":31,"errors":[],"ms":1025}`，**和 CDN 版结果一致（meshes 4、体素完全相同）**。`90_local_experiments.md:46-54`【本机实测】
- **笔记给这一步的保留率：约 95%「能被 `__THREE_DEVTOOLS__` 抓到 scene」，标注为【半实测】**（本机实测 CDN / importmap / 打包版都能）。`13_scaling_tasks.md:1332`
- **反面教材正是版本适配**：早期做法是把钩子打在 prototype 上，**在 r160 上捕获不到场景，因为 r160 的 render 挂在实例上，要在构造后包一层；后来换成 devtools 事件**。`vc_verifier/README.md:60`【本机实测】
  - → **这条可以正着写：three.js 的「免适配」不是天生的，是选对取证通道换来的。** 走 `prototype.render` 的路线是要版本适配的；走库自己派发的 devtools 事件就不要。
  - 公开对照：WorldCoder-Bench 走的是「本地锁版本的 three.js + harness 在页面加载前 patch `WebGLRenderer.prototype.render`」。`03_verifiable_construction.md:185`、`:193`【公开引用】——**它选了需要锁版本的那条路，所以它必须锁版本。**
- **浏览器环境统一这一条**：「three.js 环境统一（一个无头浏览器全搞定）」。`13_scaling_tasks.md:1308`、`:1317`【这是笔记的推断，不是实测】
- **本机只测了一个浏览器版本**：Chrome 148.0.7778.97。`06_harness.md:272`、`14_web_verifier.md:8`、`vc_verifier/README.md:6`

### A2.4 这个对比到底有多少实测支撑（必须在正文里交代的折扣）

**有实测支撑的部分：**
1. Blender 侧的 11 条不兼容里，第 1、3、4、5、7、8、11 条是本机实测（见 A2.2 表）。
2. 「bpy 要装两个 Python 运行时、4.0/4.1 下架、内网镜像 4.2~4.4 全 502」是本机实测。
3. 「three.js 的取证通道跨 CDN / importmap / 打包三种引入方式结果一致」是本机实测（`90_local_experiments.md:46-54`）。

**只是推断、不是实测的部分：**
1. **「three.js 50~80% 可执行 vs bpy 15~30%」这两个数都是本项目自己的【估】**，不是实测；唯一的实测锚点是 Objaverse-XL 的 15%（公开）。`13_scaling_tasks.md:1302`明说「整列都是估计」。
2. **跨 three.js 版本的确定性从没测过。** 原文：**「跨版本的确定性没有测过——公开材料里记过超越函数在不同引擎版本上会分叉，所以如果 harness 镜像升级，这条基线要重新量。」** `90_local_experiments.md:639-641`
3. **跨浏览器版本的确定性也没测过**，本机只有 Chrome 148 一个版本。
4. 相关的公开证据是**反向**的：**超越函数跨引擎版本会分叉**——ECMAScript 规范不要求 `Math.sin` 等的精度；`bounce` 物理库有现存 issue，刚体仿真在 Node（V8 11.3）与 Chrome 149（V8 14.9）下分叉、简单场景一致（报告者自测，issue 仍开着）。`15_game_verifier.md:589`、`15_game_verifier.md:51`【公开引用；`draft_domains.md:177` 注明「原 issue 链接本次实测被对方站点拒绝访问，未能复核」】

**而且笔记里记了三处 three.js 侧确实需要适配的坑**（都在取证链路而不是判据里，`90_local_experiments.md:590-617`【本机实测】）：

| 缺口 | 模型写的是什么 | 症状 |
|---|---|---|
| 只拦 ES 模块那条路径 | 经典脚本标签引入 | `THREE is not defined`、`no render within 15s`，执行门判挂 |
| 拦截规则写死了路径结构 | 从另一个 CDN 引入，路径里没有 build 这一段 | 同上 |
| 断网把 addon 一起拦了 | 用了 three 自带的几何工具 addon | 模块加载失败，执行门判挂 |

- 修法分别是：同时服务 UMD 构建、只按文件名判而不按路径判、本地有的 addon 直接服务。改完三个变异集回归仍是 13/13、16/16、18/18。`90_local_experiments.md:607-608`
- 笔记自己的定性：**「这条和前面那些盲区性质一样——都是假阳性——但来源不同：它不在判据里，在取证链路里。而且它伪装得最好：表现是『模型连页面都写不对』，很容易被当成模型能力问题记下来。」** `90_local_experiments.md:610-611`
- 验收要求原文：**「harness 的覆盖面要单独验收，至少包括：库的各种引入方式（ES 模块、经典脚本、打包内联、CDN 与本地）、常见的渲染循环写法、以及模型可能用的各种版本。验收办法就是拿真实策略的产出去跑，而不是拿自己写的参考解去跑。」** `90_local_experiments.md:613-617`

**→ 正文建议的说法**：不要写成「three.js 不需要版本适配」，写成 **「three.js 的版本适配成本可以压到接近零（一个浏览器镜像 + 库自己派发的取证事件 + 多引入方式验收），Blender 的不能（每版本一个 Python 运行时 + 引擎标识符改名 + 引擎能力要求变化 + 像素跨 Mesa 漂）」**。前半句有本机实测支撑，后半句有本机实测支撑；而「三者的产出率差 3~5 倍」只是估计。

---

## A3. 确定性（determinism）：各道闸不做会漂多少

### A3.1 时钟：这是漂移最大的一道闸，有完整的三档实测

`bench_clock.js` 的实验设计（`vc_verifier/bench_clock.js:1-4`）：同一个「用真实时钟 + `Math.random`」的 rAF 动画页，512×384、推进 1.5 s，截图取 md5。

| 方案 | 截图 md5 种类数 | 出处 |
|---|---|---|
| 不控制 | **3/3 全不同、20/20 全不同** | `06_harness.md:312-313` |
| 只调 `clock.install` | **3/3 不同**（加载耗时 113 ~ 432 ms 漏进了 `performance.now`） | `06_harness.md:314` |
| `install` + `pauseAt` + `runFor(1500)` + 种子 random | **20 次里有 2 种，11/9** | `06_harness.md:315` |
| 页面钩子 `setTime` + 直读 `canvas.toDataURL` | **3/3 逐字节一致** | `06_harness.md:14`、`06_harness.md:287` |

- 第 3 行的两种结果**推测是 rAF 帧相位差一帧，【未核实】**。`06_harness.md:317`
- 结论原文：**「clock 只能把方差压下来，压不到零。逐字节一致要靠页面钩子。」** `06_harness.md:50`、`06_harness.md:319-320`
- **对模型自由写的页面，verifier 必须用感知容差（SSIM 或 pHash），不能比 hash。** `06_harness.md:320`
- 关键实现细节（可直接引用）：**`install` 之后时钟仍按真实时间走，必须 `pauseAt` 冻结，否则页面加载耗时会漏进动画。** `vc_verifier/bench_clock.js:19`
- 配套工程坑：`WebGLRenderer` 默认 `preserveDrawingBuffer: false`，所以 `canvas.toDataURL()` **必须和 `render()` 在同一个同步任务里执行，中间不能 await**，否则会截到空白。`90_local_experiments.md:58-59`

**接管得足够彻底时，漂移为零（本项目的基线）：**
- `proto/harness.js` 接管 `requestAnimationFrame`、`performance.now`、`Date.now`、`Math.random`，**帧只在 harness 调 `__vcStep(n, dt)` 时推进**，同一页面重复探测逐字节一致。`90_local_experiments.md:34-36`
- `flaky.py`：**9 个产物各探测 3 次，判定翻面 0/9，信号值漂移 0/9（逐位相同）。** `90_local_experiments.md:629-635`
- 原文：**「这不是『噪声很小』，是这一环为零。做到零靠三件事：冻结时钟、固定随机种子、断网。」** `90_local_experiments.md:636-637`
- 图表线的独立复现：同一参考页重复渲染 5 次，**几何回读 5 次逐位完全相同，截图 md5 只有 1 种**。`17_chart_verifier.md:250-257`、`vc_verifier/chart/THRESHOLDS.md` 对应判据。
  - 笔记自己点明口径差异：**「这比 06_harness 里 three.js 动画页的结论强——那里 20 次截图有 2 种，因为那是『模型自由写的 rAF 动画』；图表库的终态是静态的，推够帧之后就稳定了。」** `17_chart_verifier.md:257-259`
  - 并且**推帧数不够会读到中间态**：harness 原先推 30 帧，改到 240 帧；文本记录原先跨 240 帧累加，**参考解报出 360 个数据标签**（真值应是数据点总数）。`vc_verifier/chart/THRESHOLDS.md:50-54`

### A3.2 固定视口 / DPR / 字体渲染

- 必加的闸（`06_harness.md:41-43`【公开引用：argos-ci 文档】）：固定 viewport、`deviceScaleFactor=1`、`--font-render-hinting=none`、`--disable-lcd-text`。
- Web/DOM 线实际注入的全套（`14_web_verifier.md:456-457`【本机实测】）：`Math.random` 定种（16807 线性同余，seed 42）、`Date` 固定到 2026-01-01、`prefers-reduced-motion: reduce`、`deviceScaleFactor: 1`、`--font-render-hinting=none` / `--disable-lcd-text` / `--force-color-profile=srgb`；**`performance.now` 保持真实（性能读数要用）**。
- **字体必须镜像内打包、禁止页面联网拉 Google Fonts；fontconfig 的细节【未核实】。** `06_harness.md:43`
- **不固定视口的量化后果（反向证据）**：Web 线的 W1 只看单视口 vs 三视口，判别力 12/22（只看 1440）或 13/22（只看 375）vs 三视口 13/22；**375 视口贡献 1 个其它层抓不到的缺陷**。`14_web_verifier.md:527-529`、`14_web_verifier.md:662`
- **没有「不固定字体会漂多少像素」的本机实测数字——这是一处证据缺口。** 笔记只给了「要固定」和出处，没给漂移量。

### A3.3 固定浏览器 / 引擎版本

- **本机做到的只是「同一台机器、同一个浏览器版本、同一个进程内的重复」**；跨版本确定性**没有测过**。`90_local_experiments.md:639-641`【本机自述的局限】
- **公开证据是跨版本会分叉**：超越函数（`Math.sin` 等）在 ECMAScript 里是 implementation-approximated，规范不规定精度；TC39 bug 记录里有 Firefox 与 Chrome 在 Windows/Mac 上通过而在 Linux 上不通过同一个 sine 测试的案例；`bounce` 物理库现存 issue：刚体仿真在 Node（V8 11.3）与 Chrome 149（V8 14.9）下分叉。`15_game_verifier.md:589`【公开引用，未能复核链接】
- **对策（公开最干净的参照）**：WorldCoder-Bench 的 **network-locked Chromium + 版本锁死的 three.js 本地归档 + 断言完全不进 prompt**。`11_hacking_defense.md:13`、`11_hacking_defense.md:92`、`11_hacking_defense.md:697`【公开引用】
- 判据侧的对策原文：**「锁死浏览器版本与镜像，verifier 与造题用同一个镜像。判据用容差不用逐位。」** `15_game_verifier.md:589`
- 另一处跨版本漂移的实测提醒：CDP `Performance.getMetrics` 的**绝对计数跨 Chrome 版本会漂，用差分比用绝对值稳**；`JSHeapUsedSize` / `Nodes` 在本机 5 次重复里逐字节一致可当强信号，但**不同 Chrome 版本之间不可比**。`14_web_verifier.md:145-146`【本机实测 + 工程结论】
- 还有一类「工具自己会漂」：**W3C Nu Checker 官方 about 页明确警告「检查器行为会变，今天 0 error 明天可能报错」，所以要确定性必须自建并 pin 版本**（本项目用 `html-validate` npm 11.16.2）。`14_web_verifier.md:159`、`14_web_verifier.md:671`【公开引用】
- **Blender 侧对应项**：换 CPU / 换 Mesa 版本像素会漂（`10_blender_tasks.md:457`）；官方按设备维护 BLOCKLIST（`10_blender_tasks.md:423-424`）。

### A3.4 随机种子

- three.js 线：`addInitScript` 注入带种子的 `Math.random`，**属常规做法，未找到官方出处**。`06_harness.md:46`【未核实出处】
- Web 线实测用的是 16807 线性同余、seed 42。`14_web_verifier.md:456`
- **不固定种子的量化后果（最硬的一个数字）**：`trimesh.sample.sample_surface` 不传 `seed=` 时，**参考解自己跟自己比 Chamfer 是 0.00167 而不是 0**，而判据的 tau 是 **0.0046 diag**——**噪声地板直接吃掉一半判别力**（0.00167 / 0.0046 ≈ 36%）。`10_blender_tasks.md:866-867`、`10_blender_tasks.md:728`【本机实测】
- Blender 侧：F2P 任务建议用 Workbench 或低 spp + **固定 `cycles.seed`**。`10_blender_tasks.md:459-460`

### A3.5 断网

- `proto/harness.js`：**除了 three 本身，所有外部请求一律拦掉，页面从内存里的 URL 加载。** `90_local_experiments.md:36`
- Web 线：三个文件从内存通过请求拦截提供，**外域一律阻断，缺文件返回真 404**。`14_web_verifier.md:445`
- 「判定为零方差」靠的三件事里断网是其中一件。`90_local_experiments.md:636-637`
- 公开侧的理由：**Gemini-3.1-Pro-Preview 在 WorldCoder-Bench 上「绕过给定素材目录，从 GitHub raw URL 拉模型，打破沙箱隔离」。** `11_hacking_defense.md:92`【公开引用】
- ⚠️ **断网本身会造成假阳性**：断网把 three 自带的 addon 一起拦了 → 模块加载失败 → 执行门判挂（见 A2.4 的第三条缺口）。`90_local_experiments.md:605-607`

### A3.6 确定性的综合基线：231 个字段里只有 4 个会变

Web/DOM 线最完整的一组确定性读数（参考页重复探测 5 次，报告拍平成键值对逐字段比）。`14_web_verifier.md:463-475`、`vc_verifier/web/BENCH_LOG.md:26-27`【本机实测】

| 项 | 结果 |
|---|---|
| 字段总数 | **231** |
| 跨 5 次有变化的字段 | **4** |
| 变的是哪些 | `ms`（4896~5018）、`loadMs`（15~21）、`framesP95`（16.7 / 16.8）、`layoutDurTotal`（0.0017~0.0019） |
| **全部参与判定的字段** | **逐字节一致**：axe 0 违例、控制台 0、404 0、列数 [1,2,3]、7 条状态机全过、键盘不可达 0、DOM 节点 852、堆 2.77 MB、LayoutCount 差分 2、RecalcStyleCount 差分 4 |

- **四个会变的全是墙钟量**；其中 `framesP95` / `layoutDurTotal` 参与判定但抖动远小于阈值余量（**p95 阈值 34 ms vs 实测 16.7~16.8 ms，约 2 倍余量**）。`14_web_verifier.md:474-475`
- 阈值 `_frozen: 2026-10-15`，**只在参考页 5 次重复上校准（看方差定余量），在任何变异体上一次都没调**。`14_web_verifier.md:479`、`vc_verifier/web/BENCH_LOG.md:11`
- **哪些量不能当硬闸**：长任务与帧 p95 依赖机器负载，阈值必须留大余量；`budget.json` 已在 Lighthouse 12.0.0（2024-04-22）被移除；帧 p95 没有官方口径，要标成自定义指标。`14_web_verifier.md:668`、`14_web_verifier.md:142`
- **「50 ms 长任务」的出处**：W3C Long Tasks API（Working Draft, 2026-03-19）「duration exceeds 50ms」，§4.1 写明小于 50 ms 直接 abort；50 ms 的来由在 RAIL。本机取 100 ms 阈值（参考页 0 个长任务），因为**无头 + 软渲染下首屏偶发长任务，阈值要高于噪声**。`14_web_verifier.md:143`【公开引用 + 本机实测】
- **「首屏 130~170 KB」这个常被引的数字出处是 Alex Russell 2017 年的个人博客，不是 web.dev**；是区间不是单值，前提是约 200 美元安卓机 / 400 Kbps / 400 ms RTT 下 TTI < 5 s。写成「170 KB JS 预算」是失真。`14_web_verifier.md:142`【出处纠偏，可直接用】

### A3.7 确定性做不到的地方（硬漏点）

- **Web Worker 里的时钟拦截不住**：PlaySuite 为此排除了 **225 个 Construct 3 游戏**，是它技术性排除里最大的一类（多于「只支持拖拽」的 72 个和「多人」的 25 个）。`draft_domains.md:177`【公开引用】
- 由此得到的硬闸：**同一份代码双跑，产物不一致就不进数据集。不确定的任务进了 RL 就是纯噪声。** `draft_domains.md:177`
- 笔记对自己成稿的红队意见：「只冻结时钟不够……20 次里仍有 2 种」，只有「接管帧调度与随机源」才能逐字节一致。`18_redteam.md:465`

---

## A4. 吞吐与成本：全部实测数字

环境口径（所有数字共用）：**KML pod，cgroup 配额 `cpu.max=4787500/100000` 约 47.9 核，384 逻辑核，无 GPU、无 `/dev/dri`、无 DISPLAY；Chrome 148.0.7778.97 headless + SwANGLE（SwiftShader 上的 ANGLE）；node v20.18.0。** `06_harness.md:270`、`vc_verifier/BENCH_LOG.md:3`、`vc_verifier/README.md:6`

### A4.1 three.js 单进程全流程（`bench_threejs.js`，1024×768，3 次）

WebGL 上下文：`ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))`，WebGL2 可用。`06_harness.md:275`

| 步骤 | 耗时 | 出处 |
|---|---|---|
| 启动 chrome | **172 ~ 191 ms** | `06_harness.md:279` |
| 加载场景直到 ready 钩子 | **401 ~ 420 ms** | `06_harness.md:280` |
| 单视角 `page.screenshot` | **64 ~ 85 ms** | `06_harness.md:281` |
| 单视角 `canvas.toDataURL` | **62 ms** | `06_harness.md:282` |
| 8 视角转台，逐张 `page.screenshot` | **477 ~ 540 ms** | `06_harness.md:283` |
| **8 视角转台，一次 evaluate 内渲染 + `toDataURL(jpeg)`** | **192 ~ 202 ms** | `06_harness.md:284` |
| 读 scene graph（13 个 mesh，含世界 bbox） | **1.8 ms** | `06_harness.md:285` |

- **一次 evaluate 内渲完 8 视角比逐张 screenshot 快 2.5 倍**（192 ms vs 477 ms）。
- 同视角渲两次 PNG 逐字节一致 3/3（页面钩子驱动，不走 rAF）。`06_harness.md:287`
- console 抓到 1 条 404（favicon），说明 console 通道是通的。`06_harness.md:288`
- 另一条口径：`proto/harness.js` 的单次探测（场景图 + 9 视角 + 48³ 体素）**约 0.8 ~ 1.0 秒，含启动浏览器**。`90_local_experiments.md:71`

### A4.2 three.js 并发（两种组织方式差 4 倍）

**每个任务独立起 chrome**（`bench_concurrency.sh`）。`06_harness.md:291-298`

| 并发 N | 总墙钟 | 吞吐 |
|---|---|---|
| 1 | 1.8 s | 0.6 任务/s |
| 8 | 2.2 s | **3.6 任务/s** |
| 32 | 8.9 s | 3.6 任务/s |
| 64 | 19.7 s | 3.2 任务/s |

→ **N≥8 就饱和，瓶颈是 chrome 启动。**

**复用 chrome**（`bench_pool.js`，每个任务 = reload + 8 视角 + scene graph）。`06_harness.md:301-308`

| 配置 | 吞吐 | p50 | p95 |
|---|---|---|---|
| 1 浏览器 × 1 页 | 2.4 任务/s | 383 ms | — |
| 1 浏览器 × 8 页 | 3.4 任务/s | — | — |
| 4 浏览器 × 8 页 | 11.6 任务/s | — | — |
| **8 浏览器 × 8 页** | **14.3 任务/s** | **4.1 s** | **4.9 s** |

- 机制判断：**每个浏览器只有一个 GPU 进程，SwiftShader 在里面串行，所以必须「多浏览器 × 多页」。** `06_harness.md:308`
- **复用把吞吐从 3.6 抬到 14.3，接近 4 倍。** `13_scaling_tasks.md:1512`
- 单页顺序跑只有 2.4 任务/s，**说明「加页」收益远小于「加浏览器」**（1×8 只到 3.4，4×8 到 11.6）。

### A4.3 Blender 单进程（`bench_blender.py`，同一张桌子 + 环面 + 太阳光，8 视角转台）

「首帧」含 shader 编译；「之后每视角」是后续视角单张耗时。`06_harness.md:333-344`

| 版本 / 引擎 | 分辨率 / 采样 | 首帧 | 之后每视角 | 8 视角合计 |
|---|---|---|---|---|
| 4.0 Workbench | 512×384 | 1.26 s | **0.10 s** | **2.0 s** |
| 4.0 Workbench | 1024×768 | 0.52 s | 0.22 s | 2.1 s |
| 4.0 EEVEE Legacy | 512, 16 spp | 3.2 s | 0.6 s | 7.3 s |
| 4.0 EEVEE Legacy | 1024, 64 spp | 1.6 s | 1.35 s | 11.2 s |
| 4.0 Cycles CPU 8 线程 | 512, 32 spp | 0.9 s | **0.78 s** | **6.3 s** |
| 4.0 Cycles CPU 48 线程 | 1024, 128 spp | 1.8 s | 1.6 s | 12.9 s |
| 4.0 Cycles CPU 8 线程 | 1024, 128 spp | 8.7 s | 8.2 s | **65.2 s** |
| bpy 4.5 Workbench | 512 | 0.85 s | **0.07 s** | **1.35 s** |
| bpy 4.5 EEVEE Next | 512, 16 spp ⚠️ | **13.3 s** | 2.8 s | **33.1 s** |
| bpy 4.5 Cycles CPU 8 线程 | 512, 32 spp | 0.96 s | 0.88 s | 7.1 s |

- **Cycles 的线程数是最大的单一旋钮**：1024/128 spp 下 48 线程 12.9 s vs 8 线程 65.2 s，**5 倍**。
- EEVEE Next 在 llvmpipe 上**能出正确图像（非黑帧，像素标准差约 45）**，但首帧 shader 编译 13 s，**适合常驻进程复用**。`06_harness.md:346-348`
- 读 scene graph（10 个物体）：**0.1 ~ 1 ms**。`06_harness.md:349`
- ⚠️ bpy 4.5 EEVEE Next 这一行的「16 spp」是**名义值**，日志显示实际渲了 64/64 samples，见附录。

### A4.4 Blender 多进程并发（512×384，8 视角，`bench_blender_conc.sh`）

`06_harness.md:352-357`

| 引擎 | N=1 | N=8 | N=32 |
|---|---|---|---|
| Workbench | 5.2 视角/s | 9.7 视角/s | **15.5 视角/s** |
| EEVEE Legacy 16 spp | 1.4 视角/s | 5.4 视角/s | **6.4 视角/s** |

- 每个进程启动和加载约 1 s。`06_harness.md:357`
- 结论（`06_harness.md:358-361`）：**「看形状」用 Workbench（每视角 0.1 s，可以塞进 RL 的每步观测）；「看材质和光照」用 Cycles CPU 低 spp + 低分辨率（约 1 s/视角，留给最终 reward）；EEVEE Next 在 CPU 上性价比最低。**

### A4.5 单条任务耗时（三条技术线横比）

| 线 | 单条任务 | 分解 | 出处 |
|---|---|---|---|
| **three.js**（复用浏览器） | **p50 383 ms / 稳态 14.3 任务/s** | reload + 8 视角 + scene graph | `06_harness.md:301-306` |
| three.js（`proto` 探针，含启浏览器） | **0.8 ~ 1.0 s** | 场景图 + 9 视角 + 48³ 体素 | `90_local_experiments.md:71` |
| **Blender**（冷启动单进程） | **2.3 s** | exec 候选脚本 0.23~0.30 s + 读状态 0.11 s + 6 万点采样 0.18 s + 10 视角 Workbench 渲染 1.15 s；其中约 0.5 s 是进程启动 + bpy 导入、0.49 s 是首帧 shader 编译 | `10_blender_tasks.md:600`、`:606`、`:609`、`:871`；`13_scaling_tasks.md:1454` |
| Blender 几何指标三项合计 | **0.25 s**（分部件版本约 120 ms） | Chamfer / F-score / 按色体素 IoU | `10_blender_tasks.md:50-51`、`:738` |
| Blender 从已有 runs/ 重算全部信号（不重跑 bpy） | **12.8 s / 22 个** | — | `10_blender_tasks.md:606` |
| **Web/DOM**（完整探针） | **4.9 s**（22 个变异平均 5.2 s，共 114~117 s） | 三视口 0.85 s（含启浏览器）+ 性能读数 1.26 s + axe 双主题 0.31 s + 键盘 40 次 Tab 0.04 s + 7 条状态机（8 次重载）2.27 s | `14_web_verifier.md:447-454`、`:635-636` |
| Web/DOM 零件成本 | 浏览器启动 181 ms、新开页+加载 61 ms、注入 axe（572 KB）72 ms、`axe.run` 首次 71 ms 之后 30~34 ms、复用浏览器开 5 个页 248 ms | — | `14_web_verifier.md:638-642` |
| **图表** | 单页全流程中位 **840 ms**，最慢 939 ms | 其中渲染（含推 240 帧）约 470 ms、**逐值回读 1~4 ms**、截图约 110 ms；17 个页面串行 14.5 s | `17_chart_verifier.md:239-243` |

**两条可以直接当正文论点的读法：**
1. **Web 的 4.9 s 里工具开销不到 0.5 s**，剩下全是自己写的固定 settle 等待和 40 帧 rAF 采样；**要吞吐可以压到 1 秒以内**。按 1 s/次估，**1024 并发 rollout 的 Web verifier 池只需要个位数核心**，对照 3D 侧的「多轮 three.js 43 核 / 多轮 Blender 365 核」，**Web 侧的 verifier 成本可以忽略**。`14_web_verifier.md:644-647`、`vc_verifier/web/BENCH_LOG.md:31`
2. **逐值回读是渲染耗时的千分之四，比截图便宜两个数量级**（1~4 ms vs 470 ms 渲染 / 110 ms 截图）。「这一条直接决定了它适合放进 RL 的每一步，而截图不适合。」`17_chart_verifier.md:241-246`

### A4.6 折算成 core-s 的单位成本

`08_rl_recipe.md:948-957`【本机实测折算；`core-s = 核配额 ÷ 吞吐`，48 核写成 47.9】

| 取证单位 | 实测吞吐 | 折算单位成本 |
|---|---|---|
| three.js 一次完整取证（reload + 8 视角转台 + scene graph） | 14.3 任务/s（8 浏览器 × 8 页） | **3.35 core-s / 次** |
| Blender Workbench 一个视角（512×384） | 15.5 视角/s（32 进程） | 3.09 core-s/视角 → **24.7 core-s / 8 视角** |
| Blender Cycles CPU 一个视角（512, 32 spp） | 0.88 s/视角（8 线程） | 7.04 core-s/视角 → **56.3 core-s / 8 视角** |

Workbench / Cycles 的数字已含每进程约 1 s 的启动与加载；常驻 worker 可以再省掉这一项，这里不扣，算保守。`08_rl_recipe.md:957`

### A4.7 跑一轮 rollout 的开销

**两种 rollout 形态的 CPU 需求**（1024 个并发 rollout 槽；假设：多轮 = 每条轨迹 40 步、其中 12 步（30%）带渲染自检、终局取证 3 次重复、轨迹墙钟 1200 s；单轮 = 1 步、终局 3 次重复、墙钟 80 s）。`08_rl_recipe.md:961-977`【估，基于实测单位成本】

| 形态 | CPU / 轨迹 | 核 / 并发槽 | 1024 并发所需 | 折 48 核机器 |
|---|---|---|---|---|
| 多轮 three.js | 50 core-s | 0.042 | **43 核** | **0.9 台** |
| 多轮 Blender（Workbench 自检 + 终局 Cycles） | 427 core-s | 0.356 | **365 核** | 7.6 台 |
| 单轮 three.js | 10 core-s | 0.126 | **129 核** | 2.7 台 |
| 单轮 Blender | 130 core-s | 1.631 | **1670 核** | **34.9 台** |

**三条结论（原文）**（`08_rl_recipe.md:979-987`）：
1. **多轮 agent 形态下渲染池几乎免费。** 轨迹墙钟被 LLM 解码占满，渲染只占百分之几。1024 并发的 three.js 自检只要 43 核——比 rollout GPU 节点的宿主 CPU 还少，不需要独立渲染农场。
2. **单轮形态下反而贵。** 墙钟从 1200 s 压到 80 s，取证成本不变，**单位成本涨 15 倍**。单轮 Blender 要 35 台机器，这时才需要独立渲染集群。
3. **贵的是 Cycles，不是 Blender。** Workbench 与 Cycles 差 **2.3 倍**（24.7 vs 56.3 core-s / 8 视角）。

**每张 rollout GPU 需要配的 CPU 核**（假设 30B-A3B MoE、vLLM/SGLang 8 卡服约 128 条并发序列，1024 并发 ≈ 64 张卡；【本机未实测，按 qwen38-vllm-fleet 量级估】）。`08_rl_recipe.md:991-999`

| 形态 | 核/卡 |
|---|---|
| 多轮 three.js | **0.7** |
| 多轮 Blender | 5.7 |
| 单轮 three.js | 2.0 |
| 单轮 Blender | **26** |

**一轮 RL 的总量**（400 步 × 64 prompt × G=8 = 204,800 条轨迹）。`08_rl_recipe.md:1207-1215`【估】

| 项 | 数量 |
|---|---|
| 轨迹数 | 204,800 |
| 输出 token | **6.55 B** |
| 输入 token（无 cache） | 约 **2.2 × 10¹¹**；按 97% cache 命中算实际预填约 7 × 10⁹ |
| 渲染 CPU（three.js 多轮） | 2,858 core-h = **2.5 机日**（48 核） |
| 渲染 CPU（Blender 多轮） | 24,301 core-h = **21 机日** |

- 注意配套的放大项：**动态采样会把「全对或全错」的组丢掉重采，通过率落在 5%~10% 这一段时，组大小 8 下实际要采的轨迹是名义值的 1.76 ~ 2.97 倍。** `ref_check.md:481-482`
- 造 10 万任务的探针开销对照（含难度带留存更正，见 B1）：**探针调用从约 160 万次涨到约 500 万次**。`90_local_experiments.md:758`
- 造题侧的机时：**1,589,000 次取证 ÷ 14.3 任务/s ≈ 31 小时墙钟；不复用浏览器（3.6 任务/s）则 123 小时、整机 5.1 机日**。`13_scaling_tasks.md:1508-1512`
- Blender 造题侧：不做进程复用（冷启动 2.3 s × 1 核）= 1,015 core-h = **21 台机小时**。`13_scaling_tasks.md:1521`

### A4.8 唯一一份公开的「渲染型 verifier 在 RL 里占多少时间」

UI2Code^N（2511.08195 表 20，RVPO 训练墙钟拆解）。`08_rl_recipe.md:1190-1203`【公开引用】

| 阶段 | 时间 (s) | 占比 |
|---|---|---|
| Generation | 130.9 | **75.4%** |
| **Rendering** | 38.8 | **22.4%** |
| Comparison（VLM 两两比较） | 3.9 | **2.2%** |

读法（原文）：
- **渲染占 22.4%**，不可忽略但不是瓶颈。这是**单轮**网页渲染口径；多轮形态下渲染占比会更低（本项目推算约 4%），单轮更高——**与推算方向一致**。
- **VLM 比较只占 2.2%**，原因是候选 rollout 只生成一次、复用做两两比较，「比较成本与昂贵的 token 生成解耦」，再用 tournament 聚合减少比较次数。**这是「组内 pairwise 能用在 RL 里」的全部理由。**

### A4.9 沙箱平台（`06_harness.md:110-124`【公开引用，多为厂商自报】）

| 平台 | GPU | 图形 / 显示 | 冷启动 | 计费 |
|---|---|---|---|---|
| E2B | 无 | Desktop 模板（Xvfb + XFCE + noVNC），有 e2b-desktop SDK | 300 ~ 500 ms（自报） | vCPU **0.000014 美元/s**；Pro 150 美元/月；会话 Pro 24 h |
| Modal | 有，T4 0.000164 ~ B300 0.001972 美元/s（H100 约 **3.95 美元/h**） | 未核实 | 未核实 | Sandbox 用 GPU 须 `runtime=gvisor`；**CPU 约为函数价 3 倍**；默认 5 min 超时，最长 24 h |
| Daytona | 有，每沙箱独占一卡，VFIO 直通 | 未核实 | 未核实 | 未核实 |
| Runloop | 无 | Browser / Computer add-on | 未核实 | **0.08 ~ 1.68 美元/h** |
| Morph Cloud | 无 | 未核实 | snapshot/branch **< 250 ms** | 0.05 美元/MCU |

**最有用的那句话（原文）**：**「目前没有一家平台写明『GPU + OpenGL/Vulkan 图形栈』。要真 GPU 光栅，得自己做 NVIDIA graphics capability 和 EGL 镜像。CPU 方案能省掉这一整套。」** `06_harness.md:124`

配套的「不必上 GPU」结论（`06_harness.md:7-10`）：
- three.js：Chrome headless + SwANGLE，本机 8 视角转台约 0.2 s；复用浏览器后 48 核配额下稳态约 14 任务/s
- Blender：apt 4.0 和 pip bpy 4.5 都能在无 GPU、无显示的环境里跑 Workbench / EEVEE / Cycles
- **「RL rollout 的视觉验证不必上 GPU 沙箱。」**
- 必加 flag（`06_harness.md:27-34`）：`--use-gl=angle --use-angle=swiftshader(-webgl) --enable-unsafe-swiftshader`；**不要加 `--disable-gpu`，它会把 SwANGLE 也关掉**；Chrome 130 起打弃用警告，**M139 起不显式 opt-in 就建不了 WebGL，本机 Chrome 148 实测不加 `--enable-unsafe-swiftshader` 就没有 WebGL**。

---

## A5. agent 在 harness 里能用的视觉工具：成本与可靠性

### A5.1 四类工具的成本（本机实测）

| 工具 | 成本 | 出处 | 口径 |
|---|---|---|---|
| **读 scene graph** | three.js **1.8 ms**（13 个 mesh，含世界 bbox）；Blender **0.1 ~ 1 ms**（10 个物体） | `06_harness.md:179`、`:285`、`:349`；`08_rl_recipe.md:1308` | 【本机实测】 |
| **读 console** | 抓到 1 条 404（favicon）即验证通道通；**「最便宜、信号最强的自检」** | `06_harness.md:180`、`:288` | 【本机实测】 |
| **单张截图** | `page.screenshot` 64 ~ 85 ms；`canvas.toDataURL` 62 ms | `06_harness.md:281-282` | 【本机实测】 |
| **多视角渲染** | 8 视角逐张 screenshot 477 ~ 540 ms；**一次 evaluate 内渲 + toDataURL(jpeg) 192 ~ 202 ms** | `06_harness.md:283-284` | 【本机实测】 |
| 多视角（Blender Workbench） | 10 视角 **1.2 s**；每视角 0.1 s | `10_blender_tasks.md:855`、`06_harness.md:359` | 【本机实测】 |
| **DOM / 可访问性树读取** | 注入 axe（572 KB）72 ms；`axe.run` 首次 71 ms、之后 30 ~ 34 ms；双主题各跑一遍取并集 307 ms | `14_web_verifier.md:451`、`:640-641` | 【本机实测】 |
| **真实键盘操作** | 40 次 Tab 记焦点序列与焦点指示 **36 ~ 40 ms** | `14_web_verifier.md:452`、`:635` | 【本机实测】 |
| **真实交互（状态机）** | 7 条断言 + 8 次页面重载 **2,267 ms**——**单项里最贵的一项，占 4.9 s 探针的 46%** | `14_web_verifier.md:453`、`:635` | 【本机实测】 |
| 逐值回读（图表线，canvas 文本/几何钩子） | **1 ~ 4 ms**，是渲染耗时的千分之四 | `17_chart_verifier.md:241-245` | 【本机实测】 |

**核心成本结论（原文）**：**「自检工具的核心不是截图。应同时给结构化观测：scene graph、console、bbox。返回 JSON 的成本是毫秒级，看图要 token。」** `06_harness.md:15-17`
而且 **「渲染型任务比 GUI 任务多一张牌：运行时状态是精确、无损、便宜的。」** `08_rl_recipe.md:1308`

### A5.2 图像 token 成本（决定工具默认分辨率）

计价公式（`06_harness.md:188-199`【公开引用，官方文档】）：
- **Claude**：`⌈w/28⌉ × ⌈h/28⌉`。标准档长边上限 1568，4.7 及之后的高分辨率档上限 2576。**超限的 tool_result 图片直接报错，不会自动缩放。**
- **OpenAI**：tile 计法（gpt-5 / 5.1 是 `70 + 140 × 512-tile 数`；gpt-4o 是 `85 + 170 × tile`）；patch 计法（GPT-5.2 及之后）`⌈w/32⌉ × ⌈h/32⌉ × 1.2`
- **Gemini**：两边都 ≤384 时 258 token，否则按 768 切块每块 258；Gemini 3 按 `media_resolution` 档位 280 / 560 / 1120 / 2240

按 Claude 公式算的几组例子（`06_harness.md:202-206`）：

| 图像 | 单张 token | 8 张合计 |
|---|---|---|
| 1024×768 | **1,036** | **8,288** |
| 512×384 | **266** | **2,128** |
| **8 视角拼成一张 1024×512 contact sheet（每格 256×256）** | **703** | — |

**→ 最有说服力的一组比：8 张 1024×768 逐张发送 8,288 token vs 拼成一张 contact sheet 703 token，差 11.8 倍。**
笔记自己的说法是「token 是逐张发送的 1/8 左右」（`06_harness.md:18`）——那是以 512×384 档（2,128 → 703，3 倍）还是 1024 档（8,288 → 703，11.8 倍）为分母没写清，**引用时建议直接给 703 / 8,288 / 2,128 三个数，让读者自己算**。
- 结论：**多视角默认用 contact sheet；局部细节再按需放大。** `06_harness.md:208`
- 在轨迹里的实际占比：3 张 1024×512 contact sheet 常驻 = 2,109 token；40 步累计图像约 84 k，**只占累计输入的 8%**。`08_rl_recipe.md:1150`、`:1154`、`:1157`
- **工程旋钮**：「图像预算写进环境：每条轨迹的视觉 token 上限，超了就强制降分辨率。**这是 RL 成本的主要旋钮。**」`06_harness.md:218`

### A5.3 可靠性：哪种工具的信号可信，哪种会翻面

**(a) 截图 + VLM 单次判定会翻面**（48 个 case × 4 judge × 2 种看图条件 × 2 次重复 = 768 次判定，temperature 0）。`90_local_experiments.md:165-176`【本机实测】

| judge | 单视角判对 | 多视角判对 | 单视角重测翻面 | 多视角重测翻面 |
|---|---|---|---|---|
| gpt-6-astra | 84/95 | 92/96 | **16.7%** | **4.2%** |
| gemini-3.8-flash | 88/96 | 92/96 | 8.3% | **0.0%** |
| doubao-seed-2.1-pro | 78/91 | 81/84 | 6.2% | 8.3% |
| claude-opus-5-5 | 76/96 | 74/93 | 16.7% | **20.8%** |
| 4 模型 8 票多数投票 | **44/48** | **46/48** | — | — |

- 分母不足 96 的是没能解析出结论的次数（模型没按格式输出）。`90_local_experiments.md:176`
- **多视角把两个最强 judge 的翻面率从 16.7% 压到 4.2%、从 8.3% 压到 0，但对 opus 没用。** `90_local_experiments.md:197`
- **逐 case 配对比较：单视角赢 11 例、多视角赢 27 例。** 当独立配对做 McNemar 得 p=0.015，但**这高估了独立性**（4 个 judge 判的是同一批 case）；逐模型单独看没有一个到显著（**p 从 0.13 到 0.61**）。能说的是「多视角不差于单视角，对强 judge 更好」，**不能说「多视角一定更好」**。`90_local_experiments.md:186-189`
- **这一节的结论推翻过一次**：最早只跑 18 个 case，看到多视角判对率不升反降，写下了「多视角对 VLM 无效」；扩到 48 例并修正一处人工标注错误后结论反过来。**「18 个样本上的方向性结论不可信。」** `90_local_experiments.md:180-184`

**(b) 截图的像素指标基本没有判别力，VLM 强得多但两者盲区互补**（29 个带标签变异）。`90_local_experiments.md:100-106`【本机实测】

| 信号 | 雪人 13 例 | 桌子 16 例 | 合计 |
|---|---|---|---|
| **页面单张截图逐像素相似度** | 5 | 7 | **12/29** |
| 几何类名多重集一致（朴素断言） | 6 | 8 | 14/29 |
| 多视角剪影 IoU | 9 | 10 | 19/29 |
| 按颜色体素 IoU | 11 | 14 | 25/29 |
| **四层组合** | **13** | **16** | **29/29** |

- 加上第三个场景（小车，18 个变异和标签**先写死再跑，阈值一个没调**）的留出测试 **18/18**，三场景累计 **47/47**，其中 18 个真正留出。`90_local_experiments.md:128-135`
- **像素指标判不出「鼻子不见了」，因为鼻子只占几十个像素。** `90_local_experiments.md:194`
- **投票也救不回全部，漏的是定量偏差**：4 模型 8 票在 48 例上单视角 44 对、多视角 46 对，而程序化信号在它自己的标注集上 47/47。漏判的都是尺寸类（桌腿缩到 70%、桌面厚度减到 1/3、屏幕卷曲、灯臂镜像）。**「VLM 擅长『有没有这个东西』，不擅长『这个东西的尺寸对不对』。」** `90_local_experiments.md:199-212`
- **定位结论（可直接当正文论点）**：**「VLM 的价值是帮你找到该加哪条程序化检查，而不是直接当 reward。」** `90_local_experiments.md:230-232`

**(c) Blender 侧的同一组对照**（22 个变异，11 该挂 / 11 不该挂）。`10_blender_tasks.md:23-33`【本机实测】

| 信号 | 总判对 | 检出（该挂） | 保真（不该挂） |
|---|---|---|---|
| **只看一张截图 view0** | 12/22 | **2/11** | 10/11 |
| 多视角剪影 IoU | 14/22 | 3/11 | 11/11 |
| 全局 Chamfer | 13/22 | 2/11 | 11/11 |
| 全局 F-score | 11/22 | **0/11** | 11/11 |
| 按色体素 IoU | 15/22 | 4/11 | 11/11 |
| **分部件 F-score** | 18/22 | 7/11 | 11/11 |
| **全量状态断言（九族全查）** | 11/22 | **11/11** | **0/11** |
| **分部件几何 + 四族断言（combo_pc）** | **21/22** | **11/11** | 10/11 |

- **「全量 bpy 断言是个陷阱」**：九族全查检出 11/11，但 11 个「语义没变」的改写**全部误杀**，判别力等于零。误杀集中在 A2 变换（`cube(size=1)+scale 1.2` 改写成 `cube(size=2)+scale 0.6`，世界形状一模一样但 `obj.scale` 变了）和 A3 网格统计（圆柱 16 段改 32 段、torus minor_segments 8 改 12）。`10_blender_tasks.md:35-37`
- **「几何信号必须分部件算，全局平均量是废的」**：杯子只占全场表面积约 2%，把它平移 30 cm，**全局 Chamfer 只从 0 动到 0.00018，分部件 Chamfer 是 0.084——差 460 倍**。`10_blender_tasks.md:38-41`
- **渲染图能抓的和断言能抓的几乎不重叠**（`10_blender_tasks.md:42-44`）：
  - 只有断言能抓：点光源 60 W → 6 W、F-curve 关键帧整条删光、倒角修改器去掉（1 cm 倒角 / 2.18 m 对角线 = 0.0046 diag，正好等于 tau）、相机焦距 50 mm → 24 mm
  - 只有渲染/几何能抓：部件朝向反了、小部件挪位、细分修改器去掉导致外形鼓了一圈

**(d) DOM 读取的真盲区（有精确实测）**
- Web 线判别力（22 变异 = 16 开发 + 6 留出，标签先写死）。`14_web_verifier.md:520-530`、`vc_verifier/web/BENCH_LOG.md:28`【本机实测】

| 信号 | 开发 16 | 留出 6 | 合计 | 检出 | 误杀 |
|---|---|---|---|---|---|
| 朴素①单张截图逐像素（1440 首屏，**阈值取最优** t=0.9999） | 10/16 | 4/6 | **14/22** | 4/11 | **1/11** |
| 朴素②DOM 标签序列一致 | 7/16 | 4/6 | 11/22 | 2/11 | **2/11** |
| 朴素③类名序列一致 | 5/16 | 3/6 | 8/22 | 0/11 | **3/11** |
| 朴素④可见文本一致 | 8/16 | 3/6 | 11/22 | 0/11 | 0/11 |
| W0 正确性（控制台/网络/未捕获） | 9/16 | 4/6 | 13/22 | 2/11 | 0/11 |
| W1 布局与响应式（三视口） | 10/16 | 3/6 | 13/22 | 2/11 | 0/11 |
| W2 可访问性（axe + 语义 + 键盘） | 11/16 | 4/6 | 15/22 | 4/11 | 0/11 |
| **五层组合** | — | — | **22/22**（第一遍 21/22） | 11/11 | 0/11 |

- 注意**单张截图逐像素那一行的阈值是「取最优」事后挑的**，还是只有 14/22 且有 1 个误杀。
- **11 条该挂的全部挂在设计时预期的那一层**（F5 多挂了一层 W3，是真的——按钮被压住后点不动）。`14_web_verifier.md:516`
- **一个很好用的对照数字**：**11 个「该挂」的变异里有 6 个的 1440 首屏像素相似度是 1.0**（F2 删 img alt、F3 button 换 div、F4 卡片写死 420px、F6 摘掉表单校验、F8 启动同步忙等 300 ms、H1 脚本尾部未定义变量、H3 主题不落存储）。而**不该挂的 P3「换配色（对比度仍达标）」像素相似度只有 0.9002**。`14_web_verifier.md:491-514`
  → **「像素相似度和『对不对』基本不相关」有了逐条证据：真缺陷像素 1.0，合法改写像素 0.90。**
- **DOM 侧确定性信号的真盲区（K4）**：`font-size:0` 真文字 + `::after` 画回屏幕。实测 axe 输出 `violations: []`、`incomplete: []`、`passes: 45`——**连 needs review 都不报**（axe issue #2680 "Pseudo elements without position:absolute not picked up by color contrast"，至今 open）。**只能靠代码闸或截图 OCR / VLM。纯 DOM 侧确定性信号在这里到顶了。** `14_web_verifier.md:608-613`、`vc_verifier/web/BENCH_LOG.md:32-35`
- **作弊测试**：7 个作弊页，第一版挡 5/7；补两条判据（axe 的 incomplete 里对比度一族也当闸；状态机断言加「前置态 + 往返」）后 **6/7**，22 变异全量回归仍 22/22、零新增误杀。`vc_verifier/web/BENCH_LOG.md:32-34`、`14_web_verifier.md:600-606`

**(e) 真实鼠标键盘操作（agent 自主探查）的成本与可靠性——公开侧最硬的一组**

WorldCoder-Bench 的四种判定方式对照（`92_number_audit.md:48-59`【已核验，逐值定位原文】）：

| 判定方式 | 通过率 | 与真值的 Kendall τ_b | 假阳率 | 相对成本 |
|---|---|---|---|---|
| 只读 DOM | 32.6 | **−0.021** | 33.7% | **1 倍** |
| 截图加 VLM | 2.7 | **−0.068** | 3.2% | **约 50 倍** |
| **八步 agent 自主探查** | 49.7 | **+0.111** | **45.6%** | **约 400 倍** |
| 隐藏运行时状态契约 | — | **1.000** | **0.0%** | **约 2 倍** |

- **八步 agent 会给 45.6% 的严重缺陷产物判过。** `92_number_audit.md:57`
- **【已更正】2.7% 是「截图加 VLM」这个判定方式自己的通过率，不是模型的能力**；模型（九个前沿模型里最好的一个）在隐藏契约上的覆盖率是 **27.8%**（严格档 19.9%）。`92_number_audit.md:57-59`、`92_number_audit.md:82`
- **→ 正文可以直接用的一句话：让 agent 真的去点鼠标，成本是读 DOM 的 400 倍，而它给将近一半的坏产物判了过；隐藏运行时契约的成本只有 2 倍，相关性是 1.000。**

**(f) 自我验证能力的上限：没有可比对象时，判别力从九成五掉到七成**（45 个带标签 case，两个 judge，`judge_noref.py`）。`90_local_experiments.md:699-706`【本机实测】

| 条件 | 总判对 | 检出（该挂的抓到多少） | 保真（该放行的放过多少） |
|---|---|---|---|
| 有参考图，单视角 | 101/107 = **94%** | 58/63 = **92%** | 43/44 = 98% |
| 有参考图，四视角 | 105/108 = **97%** | 61/64 = **95%** | 44/44 = **100%** |
| 无参考图，单视角 | 65/96 = **68%** | 35/56 = **63%** | 30/40 = 75% |
| 无参考图，四视角 | 73/96 = **76%** | 34/56 = **61%** | 39/40 = 98% |

- **检出从九成二掉到六成上下**，而四视角下的保真仍有 39/40：**没有参考的 judge 变成了一个偏宽松的放行器**。`90_local_experiments.md:710-711`
- 机制：**需求没写桌子多高、杯子多大、鼻子伸多长，于是尺寸和位置类的缺陷全都「不违反需求」。** `90_local_experiments.md:713-714`
- 生成侧与判别侧的同一结论（`90_local_experiments.md:720-723`）：

| 角色 | 没有可比对象时 | 有可比对象时 |
|---|---|---|
| 生成方（修自己的产物） | 首轮挂掉后救回 **2/37**（约 5%） | 救回 **11/31**（约 35%） |
| 判别方（判别人的产物） | 检出 **61% ~ 63%** | 检出 **92% ~ 95%** |

- **「模型缺的不是能力，是参照。」** `90_local_experiments.md:725`

**(g) 看自己的产物有没有用：四种反馈 × 两种问题描述的实验矩阵**（16 个自动生成的修复任务 × 4 模型 × 4 反馈 × 2 描述，每个最多 3 轮；基础设施故障单独剔除，283 组有效）。`90_local_experiments.md:332-350`【本机实测】

| 问题描述 | 反馈 | 首轮通过 | 末轮通过 |
|---|---|---|---|
| 纯文本 | 无 | 19/39 = 49% | 19/39 = 49% |
| 纯文本 | 页面一张图 | 20/34 = 59% | 21/34 = 62% |
| 纯文本 | 4 视角拼图 | 21/33 = 64% | 21/33 = 64% |
| 纯文本 | 场景图文本 | 22/33 = 67% | 23/33 = 70% |
| 文本加参考图 | 无 | 23/39 = 59% | 23/39 = 59% |
| 文本加参考图 | 页面一张图 | 25/37 = 68% | 29/37 = 78% |
| **文本加参考图** | **4 视角拼图** | 25/35 = 71% | **31/35 = 89%** |
| 文本加参考图 | 场景图文本 | 24/33 = 73% | 25/33 = 76% |

- **参考图把首轮通过率抬了约 8~10 个百分点**（无反馈一次成型：纯文本 49% vs 加参考图 59%）。`90_local_experiments.md:354-355`
- **首轮挂掉能不能救回来，几乎完全由「有没有参考图」决定**（`90_local_experiments.md:359-365`）：

| 问题描述 | 页面一张图 | 4 视角拼图 | 场景图文本 |
|---|---|---|---|
| 纯文本 | 1/14 | **0/12** | 1/11 |
| 文本加参考图 | 4/12 | **6/10** | 1/9 |

  纯文本三种反馈合计救回 **2/37 ≈ 5%**；给了参考图是 **11/31 ≈ 35%**。4 视角拼图这一格最极端，**从 0/12 变成 6/10**。
- **「最精确的反馈反而最没用」**：场景图文本是四种反馈里信息最精确的（全是数字），在两种描述下都是最差的一档（纯文本 1/11、加参考图 1/9）。原因：**问题描述给的是图，反馈给的是数字，模型需要先把图翻译成数字才能比对，而这一步正是它不擅长的。「反馈要和问题描述在同一个量纲上。」** `90_local_experiments.md:401-407`
- **再加一臂：只告诉它「哪一类不对」（层名），不给阈值也不给数值**（`90_local_experiments.md:377-386`）：

| 问题描述 | 反馈 | 首轮通过 | 末轮通过 | 首轮挂后救回 |
|---|---|---|---|---|
| 纯文本 | 4 视角拼图 | 6/16 | 7/16 | 1/10 |
| 纯文本 | 拼图加层名 | 40/62 | 44/62 | 5/22 |
| 文本加参考图 | 4 视角拼图 | 8/19 | 11/19 | 3/11 |
| 文本加参考图 | 拼图加层名 | 41/64 | 50/64 | 9/23 |

  两种描述下加了层名都救回得多（**10% 对 23%，27% 对 39%**）。**「模型缺的不是修改能力，是判断能力。」** `90_local_experiments.md:384-386`
- 要打的折扣（笔记自己列的，`90_local_experiments.md:397-399`、`:409-415`）：multi 那两行分母只有 10 和 11（这一轮没跑完）；更大的 multi 样本（0/12 与 6/10）来自修 bug 之前的 verifier，**不能和本表直接相减**；**能确定的是方向，不是幅度**；每格分母只有 9~14；任务全是「修复单处破坏」不是从零构建；三轮上限是人设的。
- 公开对照：**BlenderAlchemy 的拆解——视觉通道的增益里，给评估器看图占 84%，给生成器看图只占 16%**（2.5 分里 2.1 / 0.4）。`90_local_experiments.md:394`、`92_number_audit.md:45`【已核验】
  - 【已更正措辞】原稿说没有视觉时四轮分数「单调下降」，逐轮读是 **27.4 / 26.1 / 26.5**，中间有回升，已改成「一路走低，没有一轮回到起点」。`92_number_audit.md:45`

### A5.4 工具 schema 的建议（可直接抄进正文）

`06_harness.md:174-187`、`06_harness.md:381-388`
- `get_scene_graph(filter?)` → name / type / parent / material / color / 世界 bbox / 三角面数（three.js 用 `scene.traverse`，Blender 用 `bpy.data.objects`）
- `console_logs(level>=warning)` + pageerror + 404 资源
- `screenshot(url, viewport=1024x768, wait="ready_hook|ms", dpr=1)`——**wait 优先等页面的 ready 钩子，不要固定睡几秒**
- `render_views(n=8, elevation=25, radius=auto, res=512, layout="grid")`——**默认拼成一张 contact sheet，radius=auto 按场景 bbox 取景**
- `interact(actions[], record_every_ms)`——返回关键帧：前、中、后 3 帧（ArtifactsBench 的做法）
- `bash` 兜底 + **每条轨迹的视觉 token 预算**

**训练与评测工具同构（为什么重要）**：
- Anthropic 原话「performance of an agent on SWE-bench can vary significantly based on this scaffolding」，他们只用 Bash + Edit。`06_harness.md:210`【公开引用】
- **同一模型换脚手架的分差：GPT-5.5 在 OpenHands / Factory / Codex 三个脚手架上 69.85% / 67.39% / 58.19%，极差 11.7 点。** `ref_check.md:163`【公开引用】
- `92_number_audit.md:70`：**「同一个模型换脚手架能差 11.7 点，所以任何单点分数离开 harness 版本都没有意义。」**
- 另一条【二手转述，待回原表核实】：OpenSWE-32B 在 OpenHands 上 59.8%、在 SWE-agent 上 62.4%。`06_harness.md:212`
- 做法（`06_harness.md:213-218`）：工具语义层固定（同名、同参数、同返回结构）；transport 可替换（训练时进程内直调，评测/产品走 MCP）；**训练时随机化工具子集或参数默认值（分辨率、视角数）防过拟合某一个 scaffold**；保留一个 bash-only 退化通道。

### A5.5 现成产品与开源的工具面（star 数为 2026-10-15 GitHub API 实查）

`06_harness.md:128-171`【本机实查 + 公开文档】
- **Playwright MCP**（★38,140）：默认 snapshot 模式读可访问性树、按元素 ref 操作；`--caps=vision` 才开放坐标点击、拖拽、滚轮
- **Chrome DevTools MCP**（★53,531）：**59 个工具**（take_screenshot / take_snapshot / list_console_messages / evaluate_script / performance trace / lighthouse_audit / screencast_start-stop / network），有 `--slim` 精简集
- **Blender MCP**（★30,814，已改名 mcp-for-blender）：execute_blender_code、look（视口/相机/多角度自动取景/渲染图）、get_scene_info（可下钻）、generate_3d、search_assets / import_asset。**架构：插件起 socket server，JSON over TCP，监听 localhost:9876，无鉴权**；可设 `BLENDER_MCP_SAFE_MODE=1`
- **three.js MCP 生态很小**：threejs-devtools-mcp 只有 ★119
- **Godot MCP**（★6,081）、**Unity MCP**（★14,947，约 50 个工具）**README 都没写截图**
- 产品侧共性（`06_harness.md:171`）：**「产品端是『编译和 console 错误自动修 + 选择性看图』，而不是每步都截图。」** Lovable 明确「只在需要时用，默认先走更快的验证」
- **游戏引擎的硬约束**：Godot `--headless` 等于 dummy 渲染器，**读不回贴图、不能截图**（要 `xvfb-run` + `--rendering-driver opengl3`）；Unity `-batchmode -nographics` 不初始化图形设备，不能渲染或截图，且 **Personal 许可不能用 serial 激活，在大规模 RL 集群上许可合规是硬阻塞**。结论：**游戏类任务优先用 Web 引擎（three.js / Phaser / Babylon），其次 Godot，尽量不要 Unity。** `06_harness.md:86-101`
- **一个公开空位**：视觉类 benchmark 的共性是「Docker 内无头渲染 + 固定机位或固定时刻截图 + VLM 或像素指标」，**没有一家把 scene graph 当作 verifier 的一等输入**。`06_harness.md:264-266`

---

## A·量化数字清单

一行一个：数字 → 说明什么 → 出处。

### 沙箱形态 / 素材供给

| 数字 | 说明什么 | 出处 | 口径 |
|---|---|---|---|
| three.js examples 610 html ↔ 610 截图，配对率 1:1 | Web 生成类任务的参考素材天然成对 | `13_scaling_tasks.md:1236-1239`；`92_number_audit.md:12` 已独立核过 | 实测 |
| 单条 example 中位 6,137 字节（约 150~200 行），p95 13,651 | 「没有繁复代码仓库」：一道题的上下文就是一个 6 KB 单文件 | `13_scaling_tasks.md:1240` | 实测 |
| 全部 610 个 examples 总计 4.4 MB | 整个种子池比一个 SWE 实例的镜像还小 | `13_scaling_tasks.md:1241` | 实测 |
| three.js API 面 496 + 755 = 1,251 | 多样性覆盖率的现成分母 | `13_scaling_tasks.md:1242-1247` | 实测 |
| 9 个像素基线仓库：参考图约 1.9 万张、改基线 commit 3,413 个 | 「参考素材多」的总量 | `02_task_sources.md:26`、`:223` | 实测 |
| Babylon.js 975 张、Blender 2,596 张参考图 | 同上，且已独立核验 | `92_number_audit.md:13-14` | 实测+核验 |
| three.js e2e 判据：400×250、pixelThreshold=0.1、maxDifferentPixels=0.1%、54 个豁免 | 仓库自带的确定性像素闸，不用自己定 | `02_task_sources.md:30` | 公开 |
| **SWE-Gym 2,438 实例 = 2,438 个预构建镜像；OpenSWE 45,320 个 Docker 环境** | SWE 类是「每实例一个镜像」 | `06_harness.md:234-237` | 公开 |
| **SWE-smith 50,137 实例 → 环境存储 295 GB（约 6 MB/实例）** | 整仓 dockerfile 导入的存储量级 | `13_scaling_tasks.md:1262` | 公开 |
| **本项目 Web 层镜像一次性约 0.6 GB（chrome-linux64 552 MB + node_modules 65 MB）** | 一个镜像挂几百道题 | `06_harness.md:321-323`；`08_rl_recipe.md:1120-1122` | 实测 |
| bpy 4.5 site-packages 784 MB；apt blender + data 约 181 MB | 3D 层的镜像体积 | `06_harness.md:83`、`:329` | 实测 |
| nytimes/blender 约 514 MB（停更 3 年+）；linuxserver/blender 约 1.3 GB（桌面镜像，非批处理） | 现成 Blender 镜像都不合用 | `06_harness.md:76-81` | 公开 |
| three.js 单任务存储约 0.2 MB → 10 万任务约 20 GB | Web 侧任务产物便宜 | `13_scaling_tasks.md:1600-1601` | 实测折算 |
| Blender 单任务约 1 MB → 10 万任务约 100 GB | 3D 侧贵 5 倍 | `13_scaling_tasks.md:1601-1602` | 实测折算 |
| 启动 chrome 172~191 ms；加载到 ready 401~420 ms | 「启动耗时」的 Web 侧数字 | `06_harness.md:279-280` | 实测 |
| 浏览器启动 181 ms；新开页+加载 61 ms；复用开 5 页 248 ms（约 50 ms/页） | 复用后单位启动成本 | `14_web_verifier.md:638-642` | 实测 |
| Blender 进程启动 + bpy 导入约 0.5 s（占 2.3 s 的 22%） | 3D 侧必须常驻 worker | `10_blender_tasks.md:871` | 实测 |
| E2B 冷启动 300~500 ms；Morph snapshot < 250 ms | 沙箱平台的冷启动量级 | `06_harness.md:112`、`:116` | 公开（自报） |
| **本项目轨迹终局上下文约 49,000 token，累计输入约 1.06 M，累计输出 32,000** | 视觉编码任务的上下文量级 | `08_rl_recipe.md:1151-1153` | 估（基于实测单位） |
| **SWE-Master：输入 5,549.6k、输出 32.5k、平均 111.2 轮** | 对照：输出一样，输入多 5 倍 | `08_rl_recipe.md:1165` | 公开 |
| SWE-Gym SFT 轨迹平均约 19 轮 / 19,000 token | 另一个 SWE 侧锚点 | `08_rl_recipe.md:1164` | 公开 |
| 图像只占累计输入的 8% | 上下文爆炸是文本历史不是图像 | `08_rl_recipe.md:1157` | 估 |
| 输入 token ≈ 步数的平方；降 20% 轮数 ≈ 降 36% 输入 token | 控制步数比控制单步长度重要 | `08_rl_recipe.md:1171`、`:1513` | 推算 |
| SWE-Master 加 LSP：输入 −23.7%、轮数 −17.5%，分数 61.4% → 61.0% | 结构化观测工具直接省 token | `08_rl_recipe.md:1166`、`:1505-1508` | 公开 |
| SWE-bench 构造端到端保留率 2.46%（93,139 PR → 2,294） | 真实挖矿的天花板 | `13_scaling_tasks.md:1259` | 公开 |
| 本项目 three.js 真实素材线端到端约 3.2%，2,401 仓库 × 3 页 ≈ **230 个任务** | 「三位数，不是五位数」 | `13_scaling_tasks.md:1336-1341` | 估 |
| 本项目合成/变异线端到端 **88~96%** | 合成比挖矿高一到两个数量级 | `13_scaling_tasks.md:1311` | 实测 |
| 带截图的 issue 能成型**约 1,400 个**（原写「约 1 万量级」） | 【已更正】引用必须用 1,400 | `92_number_audit.md:84`（原值见 `02_task_sources.md:224`） | 已更正 |

### Blender 版本适配 / three.js 免适配

| 数字 | 说明什么 | 出处 | 口径 |
|---|---|---|---|
| bpy 版本 ↔ Python 小版本：4.0→3.10、4.1~5.0→3.11、5.1/5.2→3.13 | 「支持 N 个版本 = N 个 Python 运行时」 | `06_harness.md:71-73`；`10_blender_tasks.md:860` | 实测 |
| bpy 4.0 / 4.1 已从 PyPI 下架 | 版本可得性本身是风险 | `06_harness.md:74` | 实测 |
| 内网 pypi 镜像 bpy 4.2~4.4 下载**全部 502**；走海外代理装 121 s / 784 MB | 装一个特定版本的真实代价 | `06_harness.md:328-329`；`vc_verifier/BENCH_LOG.md:18` | 实测 |
| **引擎标识符跨版本改名：4.0 `BLENDER_EEVEE` → 4.2+ `BLENDER_EEVEE_NEXT`** | 最具体的一处 API 不兼容 | `vc_verifier/bench_blender.py:3`、`:33`；`vc_verifier/BENCH_LOG.md:15` vs `:19` | 实测 ⚠️ |
| EEVEE Next（4.2+）要求 OpenGL 4.3 + 2 个扩展；官方没说 llvmpipe 行不行 | 引擎能力要求跨版本变了 | `06_harness.md:61-63` | 公开+实测 |
| **8 视角 512：4.0 EEVEE Legacy 7.3 s vs bpy 4.5 EEVEE Next 33.1 s（约 4.5 倍）；首帧 3.2 s vs 13.3 s** | 不适配的性能后果 | `06_harness.md:337`、`:343`、`:347` | 实测 ⚠️ 采样口径见附录 |
| Blender 自动把同名材质节点改成 `Mix.001` → 断言必须按 `bl_idname` | 另一处必须适配的 API 行为 | `10_blender_tasks.md:868` | 实测 |
| bpy 是全局单例，必须每候选起一个子进程 | 版本无关但同源的隔离代价 | `10_blender_tasks.md:870-872` | 实测 |
| **换 CPU / 换 Mesa 版本像素会漂**；官方按设备维护 BLOCKLIST_GPU/OPTIX/METAL/VULKAN | 跨环境不可复现，必须自己重渲基线 | `10_blender_tasks.md:457-458`、`:423-424` | 公开+结论 |
| 官方像素判据：单像素误差 > 0.016 的像素不得超过 1%（`render_report.py:319-320`、`:149-157`） | 现成阈值，不用自己定 | `10_blender_tasks.md:411-422` | 公开（实查 main） |
| trimesh 不传 `seed=` → 参考解自比自 Chamfer 0.00167（tau 是 0.0046 diag），**噪声吃掉约 36% 判别力余量** | 随机源要按库分别钉 | `10_blender_tasks.md:866-867`、`:728` | 实测 |
| **Objaverse-XL「能进 Blender」5.5 M / 37 M ≈ 15%**；元数据 10,850,997 行 → 5.5 M | 「bpy 跟版本+addon 强绑定」唯一的公开实测锚点 | `13_scaling_tasks.md:1308`、`:1230` | 公开 |
| **可执行率估计：three.js 50~80% vs bpy 15~30%** | 核心对比的量级 | `13_scaling_tasks.md:1308` | **估（整列都是估计，`:1302`）** |
| 端到端挖矿产出估计：three.js 1~8% vs bpy 0.3~2% | 同上 | `13_scaling_tasks.md:1310` | 估 |
| bpy 脚本仓库真·可用池只有 **56 个**（`bpy language:Python stars:>10`） | 3D 侧素材供给本来就薄 | `13_scaling_tasks.md:1227` | 实测 |
| three.js 打包内联版探测结果与 CDN 版一致（meshes 4、体素完全相同） | three.js「免适配」的本机实测证据 | `90_local_experiments.md:46-54` | 实测 |
| `__THREE_DEVTOOLS__` 能抓到 scene 的保留率约 **95%** | 同上，标注为【半实测】 | `13_scaling_tasks.md:1332` | 半实测 |
| 反例：钩子打在 prototype 上在 **r160** 捕获不到场景（render 挂在实例上） | three.js 的免适配是选对通道换来的 | `vc_verifier/README.md:60` | 实测 |
| 反例：取证链路三处覆盖缺口（只拦 ES 模块 / 路径写死 / 断网拦了 addon）全部造成假阳性 | three.js 侧确实要做「引入方式」适配 | `90_local_experiments.md:590-617` | 实测 |
| **跨 three.js / 浏览器版本的确定性「没有测过」** | 这个对比最大的证据缺口 | `90_local_experiments.md:639-641` | 自述局限 |
| 反向公开证据：`bounce` 刚体仿真在 V8 11.3 与 V8 14.9 下分叉 | 跨引擎版本会漂 | `15_game_verifier.md:589` | 公开（链接未复核） |

### 确定性

| 数字 | 说明什么 | 出处 | 口径 |
|---|---|---|---|
| **不控制时钟：截图 md5 3/3、20/20 全不同** | 不做时钟闸的漂移上限 | `06_harness.md:312-313` | 实测 |
| **只调 `clock.install`：仍然 3/3 不同**（加载耗时 113~432 ms 漏进 `performance.now`） | 半做等于没做 | `06_harness.md:314`；`vc_verifier/bench_clock.js:4`、`:19` | 实测 |
| **install + pauseAt + runFor + 种子 random：20 次里 2 种（11/9）** | 做全了也压不到零 | `06_harness.md:315` | 实测 |
| **页面钩子 setTime + 直读 canvas：3/3 逐字节一致** | 唯一能逐字节复现的做法 | `06_harness.md:14`、`:287` | 实测 |
| 接管 rAF/performance.now/Date.now/Math.random + 断网：**判定翻面 0/9、信号漂移 0/9 逐位相同** | 「这一环为零」的基线 | `90_local_experiments.md:629-637` | 实测 |
| 图表线重复 5 次：几何回读逐位相同、截图 md5 只有 1 种 | 静态终态比动画好做 | `17_chart_verifier.md:250-257` | 实测 |
| 推帧 30 → 240 才读到终态；原先跨 240 帧累加让参考解报 **360 个数据标签** | 推帧数不够会读中间态 | `vc_verifier/chart/THRESHOLDS.md:50-54` | 实测 |
| 参考解自比自逐值回读最大相对误差 **0.15%**（固定偏置，非噪声），阈值 1% 有 6 倍余量 | 噪声地板与阈值余量的关系 | `17_chart_verifier.md:261-263` | 实测 |
| **Web 线 231 个字段里只有 4 个会变，全部参与判定的字段逐字节一致** | 确定性最完整的一组读数 | `14_web_verifier.md:463-475`；`vc_verifier/web/BENCH_LOG.md:26` | 实测 |
| 会变的 4 个全是墙钟量；`framesP95` 16.7/16.8 ms vs 阈值 34 ms（约 2 倍余量） | 哪些量能当硬闸 | `14_web_verifier.md:471-475` | 实测 |
| 确定性注入全套：`Math.random` 16807/seed 42、`Date` 固定 2026-01-01、reduced-motion、DPR=1、font-render-hinting=none、disable-lcd-text、force-color-profile=srgb | 闸门清单 | `14_web_verifier.md:456-457` | 实测 |
| CDP `Performance.getMetrics` 绝对计数跨 Chrome 版本会漂，**用差分比用绝对值稳** | 浏览器版本闸的具体后果 | `14_web_verifier.md:145-146` | 实测+结论 |
| W3C Nu Checker 官方警告「今天 0 error 明天可能报错」→ 必须自建并 pin（本项目用 html-validate 11.16.2） | 「工具自己会漂」 | `14_web_verifier.md:159`、`:671` | 公开 |
| 深色主题必须单独跑 axe：参考页第一版深色下 footer 链接吃了默认 `#0000ee`，在 `#12161b` 上对比度 **1.93** | 不跑第二套配置会漏 | `14_web_verifier.md:460-461` | 实测 |
| 长任务阈值取 100 ms（W3C 定义 50 ms），因为无头+软渲染下首屏偶发长任务 | 阈值要高于噪声 | `14_web_verifier.md:143` | 公开+实测 |
| 「首屏 130~170 KB」出处是 Alex Russell 2017 个人博客，不是 web.dev | 出处纠偏 | `14_web_verifier.md:142` | 出处核查 |
| Web Worker 里的时钟拦截不住 → PlaySuite 为此排除 **225 个** Construct 3 游戏（最大一类技术性排除，多于拖拽 72 / 多人 25） | 确定性的硬漏点 | `draft_domains.md:177` | 公开 |
| 硬闸：**同一份代码双跑，产物不一致就不进数据集** | 直接可抄的准入条 | `draft_domains.md:177` | 结论 |
| `preserveDrawingBuffer: false` → `toDataURL()` 必须和 `render()` 在同一同步任务里，中间不能 await | 否则截到空白 | `90_local_experiments.md:58-59` | 实测 |
| 必加 flag：`--enable-unsafe-swiftshader`（M139 起不加就建不了 WebGL）；**不要加 `--disable-gpu`** | 环境闸 | `06_harness.md:27-34` | 公开+实测 |

### 吞吐与成本

| 数字 | 说明什么 | 出处 | 口径 |
|---|---|---|---|
| **three.js 复用浏览器 8×8：14.3 任务/s，p50 4.1 s，p95 4.9 s** | 单机并发的峰值 | `06_harness.md:306` | 实测 |
| 不复用 chrome：N≥8 即饱和在 **3.6 任务/s**（N=64 反降到 3.2） | 复用是 4 倍差距 | `06_harness.md:291-298`、`13_scaling_tasks.md:1512` | 实测 |
| 1 浏览器×1 页 2.4、1×8 3.4、4×8 11.6、8×8 14.3 任务/s | 「加浏览器」远胜「加页」 | `06_harness.md:301-306` | 实测 |
| 8 视角一次 evaluate 内渲 **192~202 ms** vs 逐张 screenshot **477~540 ms** | 2.5 倍，直接省 | `06_harness.md:283-284` | 实测 |
| **渲染一帧：Workbench 0.10 s / 视角**（512×384，首帧 1.26 s） | 「看形状」的单帧成本 | `06_harness.md:335`、`:359` | 实测 |
| Cycles CPU 8 线程 0.78 s/视角（512, 32 spp） | 「看材质光照」的单帧成本 | `06_harness.md:339`、`:360` | 实测 |
| Cycles 1024/128 spp：48 线程 12.9 s vs 8 线程 **65.2 s** | 线程数是最大单一旋钮（5 倍） | `06_harness.md:340-341` | 实测 |
| EEVEE Next 首帧 shader 编译 **13.3 s** | 必须常驻进程复用 | `06_harness.md:343`、`:348` | 实测 |
| Blender 并发：Workbench N=32 **15.5 视角/s**；EEVEE Legacy 16 spp N=32 **6.4 视角/s** | 单机并发 | `06_harness.md:352-356` | 实测 |
| **单条任务：three.js p50 383 ms / Blender 2.3 s / Web-DOM 4.9 s / 图表 840 ms** | 四条线横比 | `06_harness.md:301`；`10_blender_tasks.md:600-609`；`14_web_verifier.md:454`；`17_chart_verifier.md:239` | 实测 |
| Blender 2.3 s 分解：exec 0.27 + 状态 0.11 + 采样 0.18 + 10 视角渲染 1.15 | 成本在哪 | `13_scaling_tasks.md:1454` | 实测 |
| Web 4.9 s 里工具开销不到 0.5 s，**可压到 1 s 以内** | 别把自己的 settle 等待当工具成本 | `14_web_verifier.md:644-645`；`vc_verifier/web/BENCH_LOG.md:31` | 实测+结论 |
| 读 scene graph：three.js **1.8 ms**，Blender **0.1~1 ms** | 结构化观测的成本是毫秒级 | `06_harness.md:285`、`:349` | 实测 |
| 逐值回读 **1~4 ms**，是渲染耗时的 **千分之四**，比截图便宜两个数量级 | 适合放进 RL 每一步，截图不适合 | `17_chart_verifier.md:241-245` | 实测 |
| 折算单位成本：three.js 一次取证 **3.35 core-s**；Workbench 8 视角 **24.7 core-s**；Cycles 8 视角 **56.3 core-s** | 可直接乘的单位 | `08_rl_recipe.md:950-954` | 实测折算 |
| **1024 并发 rollout 的渲染池：多轮 three.js 43 核（0.9 台 48 核机）** | 「渲染池几乎免费」 | `08_rl_recipe.md:974` | 估 |
| 多轮 Blender 365 核（7.6 台）；单轮 three.js 129 核；**单轮 Blender 1670 核（34.9 台）** | 单轮形态单位成本涨 15 倍 | `08_rl_recipe.md:975-983` | 估 |
| 每张 rollout GPU 配的 CPU：多轮 three.js **0.7 核**，单轮 Blender **26 核** | 和 GPU 的配比 | `08_rl_recipe.md:996-999` | 估（未实测） |
| **一轮 RL（400 步 × 64 prompt × G=8 = 204,800 轨迹）：输出 6.55 B token，渲染 CPU three.js 2,858 core-h = 2.5 机日；Blender 24,301 core-h = 21 机日** | 跑一轮 rollout 的开销 | `08_rl_recipe.md:1207-1215` | 估 |
| 动态采样放大项：p 落在 5%~10% 时，组大小 8 下实采轨迹是名义值的 **1.76 ~ 2.97 倍** | 容易漏掉的成本项 | `ref_check.md:481-482` | 推算 |
| 造 10 万任务的探针调用：约 160 万次 → **约 500 万次**（难度带留存更正后） | 成本模型最敏感项的后果 | `90_local_experiments.md:758` | 实测驱动 |
| 1,589,000 次取证 ÷ 14.3 任务/s ≈ **31 小时墙钟**；不复用则 123 小时 / 5.1 机日 | 造题侧机时 | `13_scaling_tasks.md:1508-1512` | 推算 |
| **UI2Code^N 实测：Generation 75.4% / Rendering 22.4% / Comparison 2.2%** | 唯一一份公开的渲染型 verifier 时间拆解 | `08_rl_recipe.md:1190-1203` | 公开 |
| E2B vCPU 0.000014 美元/s；Modal H100 约 3.95 美元/h；Runloop 0.08~1.68 美元/h | 沙箱计费量级 | `06_harness.md:110-116` | 公开（自报） |
| **没有一家沙箱平台写明「GPU + OpenGL/Vulkan 图形栈」** | CPU 方案能省掉一整套 | `06_harness.md:124` | 调研结论 |

### agent 的视觉工具

| 数字 | 说明什么 | 出处 | 口径 |
|---|---|---|---|
| 单视角 `page.screenshot` 64~85 ms；`canvas.toDataURL` 62 ms | 截图成本 | `06_harness.md:281-282` | 实测 |
| 注入 axe（572 KB）72 ms；`axe.run` 首次 71 ms、之后 30~34 ms | DOM/可访问性读取成本 | `14_web_verifier.md:640-641` | 实测 |
| 40 次 Tab 键盘遍历 **36~40 ms** | 真实键盘操作很便宜 | `14_web_verifier.md:452` | 实测 |
| **7 条状态机断言 + 8 次页面重载 2,267 ms，占 4.9 s 探针的 46%** | 真实交互是最贵的一项 | `14_web_verifier.md:453`、`:635` | 实测 |
| 图像 token：1024×768 单张 **1,036**、8 张 **8,288**；512×384 单张 266、8 张 2,128；**8 视角 contact sheet（1024×512）703** | contact sheet 比逐张发省 3~11.8 倍 | `06_harness.md:202-206` | 公开公式+推算 |
| **八步 agent 自主探查成本是读 DOM 的约 400 倍，截图+VLM 约 50 倍，隐藏运行时契约约 2 倍** | 四种观测通道的相对成本 | `92_number_audit.md:50-55` | 公开（已核验） |
| **八步 agent 给 45.6% 的严重缺陷产物判过；τ_b 只有 +0.111** | 真实鼠标键盘操作最贵且最不可靠 | `92_number_audit.md:54`、`:57` | 公开（已核验） |
| 只读 DOM τ_b **−0.021**、假阳 33.7%；截图+VLM τ_b **−0.068**、假阳 3.2%；隐藏契约 τ_b **1.000**、假阳 **0.0%** | 「看图打分信号与真值相关性」 | `92_number_audit.md:50-55` | 公开（已核验） |
| 【已更正】2.7% 是「截图+VLM」判定方式的通过率，不是模型能力；模型的隐藏契约覆盖率 **27.8%**（严格档 19.9%） | 避免语义错位 | `92_number_audit.md:57-59`、`:82` | 已更正 |
| 单张截图逐像素判对 **12/29**；多视角剪影 19/29；按色体素 25/29；四层组合 **29/29**（+留出 18/18 = 47/47） | 像素指标 vs 程序化信号 | `90_local_experiments.md:100-106`、`:135` | 实测 |
| Blender 侧：只看一张截图 12/22、检出 **2/11**；全量九族断言检出 11/11 但保真 **0/11**；combo_pc **21/22** | 单张截图的检出力极低；全量断言全是误杀 | `10_blender_tasks.md:26-35` | 实测 |
| 杯子占全场表面积约 2%，平移 30 cm：**全局 Chamfer 只动到 0.00018，分部件 0.084（差 460 倍）** | 全局平均量是废的 | `10_blender_tasks.md:40-41` | 实测 |
| VLM 单次判定翻面率：最差一档 **20.8%**（claude-opus-5-5 多视角）；多视角把最强两个 judge 从 16.7%→4.2%、8.3%→0 | 截图+VLM 的可靠性 | `90_local_experiments.md:170-173`、`:197` | 实测 |
| 4 模型 8 票投票：单视角 44/48、多视角 46/48；配对比较单视角赢 11、多视角赢 27（McNemar p=0.015，但逐模型 p=0.13~0.61 全不显著） | 多视角「不差于」而非「一定更好」 | `90_local_experiments.md:174`、`:186-189` | 实测 |
| **拿掉参考图：judge 总判对 94~97% → 68~76%，检出 92~95% → 61~63%，而保真仍 98%** | 没有参照的 judge 变成宽松放行器 | `90_local_experiments.md:703-706` | 实测 |
| 生成侧：无参考救回 **2/37（5%）**，有参考 **11/31（35%）** | 「模型缺的不是能力，是参照」 | `90_local_experiments.md:364`、`:722` | 实测 |
| 4 视角拼图这一格：纯文本 **0/12** → 加参考图 **6/10** | 最极端的一格 | `90_local_experiments.md:362-365` | 实测 |
| 加「层名」（只说哪一类不对）：救回 10%→23%、27%→39% | 「模型缺的是判断能力」 | `90_local_experiments.md:377-386` | 实测 |
| 场景图文本（最精确的反馈）救回最差：纯文本 1/11、加参考图 1/9 | 「反馈要和问题描述同量纲」 | `90_local_experiments.md:401-407` | 实测 |
| BlenderAlchemy：视觉增益 2.5 分里，给评估器看图占 2.1（84%）、给生成器看图占 0.4（16%） | 增益来自判别不来自反思 | `90_local_experiments.md:394`；`92_number_audit.md:45` | 公开（已核验） |
| Web 线 K4 盲区：`font-size:0` + `::after`，axe 输出 `violations:[] incomplete:[] passes:45`，连 needs review 都不报（issue #2680 open） | 纯 DOM 侧确定性信号的上限 | `14_web_verifier.md:608-613` | 实测 |
| 作弊集 7 个页：第一版挡 5/7，补两条判据后 **6/7**，22 变异回归仍 22/22 | 补判据不损判别力 | `vc_verifier/web/BENCH_LOG.md:32-34` | 实测 |
| 11 个「该挂」变异里 **6 个的 1440 首屏像素相似度是 1.0**；不该挂的 P3 换配色只有 **0.9002** | 像素相似度与「对不对」不相关 | `14_web_verifier.md:491-514` | 实测 |
| 让模型自己找漏洞：12 次请求 → 产出作弊页 5、**verifier 判过 0**（实际分母是 5 不是 12），全部挂在多视角剪影这一层 | 要克制地解读这个零 | `90_local_experiments.md:654-684` | 实测 |
| **同一模型换脚手架差 11.7 点**（GPT-5.5：OpenHands 69.85 / Factory 67.39 / Codex 58.19） | 训练与评测工具必须同构 | `ref_check.md:163`；`92_number_audit.md:70` | 公开 |
| Playwright MCP ★38,140（`--caps=vision` 才开坐标点击）；Chrome DevTools MCP ★53,531（59 个工具）；Blender MCP ★30,814；three.js MCP 只有 ★119 | 工具生态的厚薄 | `06_harness.md:131-149` | 实查 |
| Godot `--headless` 不能截图；Unity `-batchmode -nographics` 不能渲染；Unity Personal 许可在集群上是硬阻塞 | 游戏引擎优先 Web | `06_harness.md:86-101` | 公开 |
| 公开 benchmark 里**没有一家**把 scene graph 当 verifier 的一等输入 | 空位 | `06_harness.md:264-266` | 调研结论 |

---
---

# 主题 B：怎么挑「值得蒸馏的题目」

> 主题 B 的素材几乎全部来自公开论文（`08_rl_recipe.md` / `03_verifiable_construction.md` / `05_trajectory_repair.md` / `12_self_verification.md` / `13_scaling_tasks.md`），
> 本机实测只在两处：**变异判别力**（snowman 13 变异的四档判据）和**judge 的标签错误/豁免条款**（`12_self_verification.md` 的自评部分）。
> 这两处恰好是最关键的两处——B2 的反例和 B3 的「怎么判题目坏了」都靠它们落地。

---

## B1. 难度带筛选：p 怎么估、采几次、留存多少

### B1.1 「采 k 次估 p」各家的具体预算（这是最硬的一组横比）

| 工作 | 用谁采 | 采几次 | 保留区间 | 产出规模 | 出处 |
|---|---|---|---|---|---|
| MiniMax-M1（2506.13585） | 强推理模型 | **pass@10** | **0 < p < 0.9** | 数学约 50K、代码约 30K、逻辑约 53K | `08:625` |
| Kimi k1.5（2501.12599 §2.3） | SFT 模型 | **10 次高温采样**当难度代理 | 先剔掉过易 | — | `08:626` |
| Kimi K2（2507.20534） | SFT 模型 | pass@k | 只留「中等」 | — | `08:627` |
| SWE-Master（2602.03411 §4.2） | 待训模型 | **N ∈ [3,12]**，均值 resolve rate | **两端都砍**（分布是双峰：总是解出 / 总是失败） | 不做难度过滤 54.2% → 做了 **57.8%（+3.6）** | `08:630`、`05:179`、`05:184-186` |
| GLM-4.5（2508.06471 §3.3.1） | 待训模型 | 阶段二切到 **pass@8 = 0 且 pass@512 > 0** | 只要「极难但可解」 | 对照组停在中等难度会早早平台化 | `08:623` |
| Boundary-Aware CRL（2606.22317） | 待训模型 | **256 解码预算 × 3 个种子**，记首次正确的序号 | 分 Easy/Medium/Hard/**Frontier**/**Beyond** 五档 | 见 B1.2 | `08:563-564` |
| cadrille（2505.22914） | SFT 模型 | 3 次 | 只留均值 reward < 7.5（reward = 10×IoU，不可执行 −10） | — | `03:267` |
| WebClipper | — | **每题跑 4 次** | **0 < p < 0.5**（有上界） | — | `05:61` |
| Ling/Ring 2.6（2606.15079） | 训练中行为 | **Dynamic Pass Rating**：不用静态历史通过率 | — | — | `08:628` |
| **反例：Qwen3（2505.09388）** | **完全没有 pass@k 课程** | — | 只做 query 过滤（Qwen2.5-72B-Instruct 剔掉难验证的）+ response 过滤 | **最后只有 3,995 对 query-verifier** | `08:629` |
| KodCode | — | 自验证过不了的硬题**给到 10 次**而不是丢掉 | — | 447K triples | `03:268` |

两个可以直接写进正文的口径：

- **上界不是 1 而是 0.9（MiniMax）甚至 0.5（WebClipper）**：p 太高的题在 GRPO 里和 p=0 一样没有梯度，但代价不同——p=1 浪费 rollout，p=0 还会污染组基线。
- **SWE-Master 是唯一给了「做难度过滤 vs 不做」干净对照的**：54.2% → 57.8%，**+3.6 分**，这就是难度带筛选本身的价值上限参考值。

### B1.2 留存与分布漂移：静态课程为什么会立刻失效

Boundary-Aware CRL 表 9（Qwen2.5-7B，1,948 道题）的桶分布：

| 阶段 | Easy | Medium | Hard | Frontier | Beyond | 平均 k |
|---|---|---|---|---|---|---|
| Base | 24 | 1,343 | 354 | 166 | 61 | 12.43 |
| RL1 后 | **650** | — | — | — | — | — |
| RL2 / RL3 后 | 697 → 736 | — | — | — | — | — |

出处 `08:577-585`。两条结论：

- **第一轮 RL 就把 Easy 从 24 冲到 650（27 倍）**，之后几乎不动（650 → 697 → 736）。
  所以「重新估 p」的边际价值**绝大部分在第一遍**，静态课程失效得非常快。
- Beyond 档（256 次都没解出，必然零优势）**不是丢掉**：取最靠近 pass@32 边界的 10 道 + 最靠近 pass@256 边界的 10 道，
  **做教师轨迹的小规模 SFT 桥接，然后再 RL**（`08:565`）。这条直接通向 B2。

效果：pass@256 比 base **+9.8pp**，比 vanilla RLVR **+10.3pp**；
**538 道 base 解不出的题里有 226 道变得可解**（`08:568-573`、`08:1257`）。
⚠️ 最刺眼的一条是反向的：**vanilla RLVR 的 pass@256 平均低于 base**——
Qwen2.5-7B AIME24 **40.0 → 26.7（vanilla RLVR）→ 52.2（带课程）**；
LLaMA-3.1-8B MATH500 **73.6 → 55.4 → 88.0**。没有课程的 RL 是在**缩小**能力边界。

### B1.3 公开数据里训练前「全对/全错」的占比（这是本节要的那个数）

| 数字 | 条件 | 出处 |
|---|---|---|
| **n=4 时 35.3% 的组全对；n=256 时降到 10.2%** | Open-R1 子集 + Qwen2.5-Math-1.5B | `08:18`、`08:199` |
| 同一模型 **pass@1 = 26.5%，pass@256 = 81.3%** | 同上 | `08:199` |
| **一个 batch 里接近 50% 的组 reward 完全相同（优势为 0）** | SRPO 2504.14286 §3.3 图 8 | `08:195` |
| Reinforce-Ada 按 base pass@16 分 5,000 道题：**极难 984（19.7%）/ 难 3,082（61.7%）/ 中 870（17.4%）/ 易 63（1.3%）** | 数学域 | `08:600` |
| DAPO 图 3(b)：acc=1 的 prompt 占比持续上升 | ⚠️**只有图没有数字**，不要编数 | `08:196` |

一句可以直接引的话：**「signal collapse 是欠采样的统计假象，不是模型上限」**（`08:17`、`08:198`）——
pass@1 26.5% 对 pass@256 81.3% 就是证据：同一个模型、同一批题，采样预算决定了你看到的是「全错」还是「可学」。

### B1.4 零梯度组的概率：笔记里有一处算错，必须用更正值

- ⚠️**`08_rl_recipe.md:194` 原文写的是「组大小 8、题目通过率 p=0.1 时，全 0 的概率 `0.9^8 ≈ 19%`」——这是算术错误。**
  0.9^8 = **43.05%**；19% 对应的是 0.9^16（组大小 **16**）。`92_number_audit.md:83` 的更正是对的。
  引用归属（Reinforce-Ada 2510.04996 §2）没问题，错的只有指数/组大小。
- **同一个文件 `:201` 自己写对了**：「一个任务初期 pass 率可能只有 5%~10%，G=8 时约 **43%~66%** 的组全 0」
  （0.9^8 = 43.1%，0.95^8 = 66.3%）。**正文要引 `:201`，不要引 `:194`。**【已更正】

### B1.5 两条干净的边界：退役全对题可以，整类砍掉易档不行

- **退役全对题是对的**：ExGRPO（2510.02245）把已退役的题重新放回训练，in-dist **48.4 → 45.3（−3.1）**（`08:609-617`）。
- **但不能整类砍易档**：Reinforce-Ada 表 5——**DAPO 在 Easy 桶上比 base 低 5.70 分（0.5580 vs 0.6151）**，
  而 GRPO 是 **+7.14**、Reinforce-Ada 是 **+10.02**（`08:591-599`）。这是动态采样代价的唯一硬数字。
- ExGRPO 的分桶回放：Easy[75,100) / Medium(25,75] / Hard(0,25]，**只训 Medium 最好**；
  回放比例 ρ 消融 50%→48.3、25%→46.4、**75%→44.8（低于纯 on-policy 基线）**；
  采样 p ∝ N(Acc(q); μ=0.5, σ=1)，σ=1.5→46.2，μ=0.25 更差（`08:210`、`08:611-612`）。
- ⚠️**反例：两阶段「小预算探一下再按 1/√p̂ 分配」会崩**——难题在小预算下 p̂=0，退化成被动过滤（`08:602-603`）。
- Reinforce-Ada 的自适应组大小（采到 K_pos=K_neg=8 再下采样、按 1/p̂_i 加权）：
  **反传组只有 n=4（GRPO-n4 的成本），加权平均 47.6 > GRPO-n16 的 47.3，收敛快 2 倍**（`08:208`）。
- SRPO History Resampling（epoch 级，比在线筛便宜）：**丢全对、留全错**（天然课程）；
  AIME24 40.5→44.3，LCB 35.1→38.7，步数约为 R1-Zero 的 1/10（`08:209`）。

### B1.6 组大小是二阶的，batch 才是一阶的

ScaleRL（2510.13786）表 1，固定总 batch：

- **G = 8 / 16 / 24 / 32 → 0.585 / 0.610 / 0.590 / 0.595**（非单调，差异在噪声量级）
- **batch = 512 / 768 / 2048 → 0.605 / 0.610 / 0.645**（单调上升）

出处 `08:183-188`。结论原文写得很直：**「先把 batch 做大（prompt 多样性），G 取 8~16 就够」**。

### B1.7 难度估计的单价：为什么本机不能抄 pass@256

【本机实测 × 算术】Blender 线单视角 24.7 core-s/题（见 A4.6），
静态 pass@256 × 3 个种子 = 256 × 3 × 24.7 ≈ **5.3 核时/题**（`08:637-638`）。
3K 道题就是 **16,000 核时**，和跑一轮 RL 同量级。
所以本机只能用**在线正确率**（ExGRPO 式）或 **DPR**（训练中行为），**绝不能离线跑 pass@256**。

### B1.8 监控指标（把 B1 变成可运行的东西）

- 必须画**组内方差**与**全对组/全错组占比**（`08:1561`）。正常形态：全错组下降、全对组上升。
- **全对组冲到 80%+ 说明该换课程档位，不是该换算法。**
- 环境失败率是另一条线：正常 < 2% 且平稳，**> 5% 必须停下修基础设施**（见 B3.6）。
### B1.9 补充：采几次才够、带状过滤值多少分（`13_scaling_tasks.md` 的定量部分）

这一节是 B1 里**唯一有完整数学与阈值扫描**的素材，正文写「难度带筛选」时主要靠它。

**(a) 骨架：三件事是同一个 p(1−p)**（`13:337-351`）

```
① RL 学习信号的上界     2504.03380 Prop 3.1：策略改进下界 ∝ p(1−p)
                        2601.02648：group 内二元 reward 时 (1/N)ΣA_i² = p(1−p)
② 题目的 Fisher 信息     IRT：I_i(θ) = a_i²·P_i(1−P_i)，在 P=0.5 最大
③ 难度估计本身的方差     p̂ 的方差 = p(1−p)/n
```

**①② 说「要挑 p≈0.5 的题」，③ 说「p≈0.5 的题最难挑准」**——这个张力决定了全部工程选择（`13:349-351`）。

**(b) n=4 标难度等于没标**（`13:377-400`，本机算的 Wilson 区间表）

| p̂ | n=2 | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|---|
| **0.50（95% CI 半宽）** | 0.405 | 0.350 | 0.285 | 0.220 | 0.164 | 0.119 |

**最硬的一个数：Wald 口径下 n=4、p=0.5 时 95% CI 全宽 0.98**，几乎覆盖整个 [0,1]。
达到目标半宽所需的 n（p=0.5）：h=0.20 → 24；h=0.15 → 43；h=0.10 → 96；**h=0.05 → 385**（`13:399-404`）。

**(c) 硬边界的难度桶在数学上做不到**（`13:417-430`，本机精确枚举的三档桶误分率）

| 真 p | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|
| 0.10 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
| **0.25 / 0.75** | 26.2% | 32.1% | **37.0%** | 26.3% | **15.6%** |
| **0.35 / 0.65** | 68.9% | 45.3% | 29.1% | 26.8% | **22.5%** |
| 0.50 | 62.5% | 28.9% | 7.7% | 2.0% | 0.2% |

桶中心和桶外都能分准，但**桶边界附近的误分率在 n=64 时仍有 15%~23%，而且几乎不随 n 下降**——
真 p 恰在边界上时本来就是 50/50，这部分方差**不可能靠加 n 消除**。
⇒ **只能用软权重 / 重叠桶，不要追求稳定的连续难度分**（`13:429-432`）。

**(d) 标签复现性——「n 要多大」最直接的公开答案**（2609.40115，`13:434-451`）

| 预算 n | 难度集合的 Jaccard 复现性 |
|---|---|
| 8 | **0.632** |
| 16 | **0.727** |
| 128 | **0.876** |
| 2,111（外推） | 0.95 |

同文三条可直接引：
- **「跨训练种子的难度差异」里 81% 其实只是采样噪声**（同 checkpoint 重采两次 N=32 的 Jaccard 0.798，独立种子间 0.751）。
- **同预算下「深采一次」优于「拆块取交集」**：128 次一次性 Jaccard **0.8770**，4×32 且四块都判难才保留 **0.7906**，差 **+0.0864**。
- 原文结论句：**「low-budget difficulty labels are unreliable for classifying individual prompts」**。

**(e) 带状过滤到底值多少分——唯一有完整阈值扫描的论文**（2504.03380，Qwen2.5-3B，`13:570-614`）

| 区间 | 五个数学 benchmark 平均 |
|---|---|
| SFT 起点 | 20.2 |
| **Plain GRPO**（0 ≤ p ≤ 1） | **26.3** |
| Skewed 单边切（0.4 < p ≤ 1 / 0 ≤ p < 0.8 等） | **23.8 ~ 25.9，全部低于 plain GRPO** |
| **Balanced 0 < p < 1（= DAPO 口径）** | **27.3（+1.0）** |
| Balanced 0.1 < p < 0.9 | 28.4 |
| Balanced 0.2 < p < 0.8 | 29.8 |
| **Balanced 0.3 < p < 0.7** | **30.1（+3.8，全表最高）** |
| Balanced 0.4 < p < 0.6 | 29.9（回落） |

四条结论：
1. **只剔全对全错（DAPO 口径）只值 +1.0pp**（26.3 → 27.3）。
2. **再收紧到中段多拿 +2.8pp**（27.3 → 30.1）。
3. ⚠️**必须对称切**：单边切全部输给 plain GRPO。
4. **过紧有代价**：(0.4,0.6) 回落到 29.9，而且「can require significantly more rollouts to fill a batch」。
7B 扩展（表 2）：SFT 37.3 → plain 39.6 → (0,1) 39.9 → **(0.3,0.7) 41.8**。
在线胜过离线的机制（图 2）：**离线代理模型的难度与被训模型系统性错位**；训练中 checkpoint 感知的 batch 平均难度稳定在 0.5 附近。

**(f) ⚠️ 过滤过头反而更差（最干净的反面证据）**（`13:616-630`）

| 来源 | 做法 | 结果 |
|---|---|---|
| **Polaris 难度分布消融** | Full 40K（被 8/8 易题主导）→ 进展受阻；**去掉全部 8/8 的 26K → 最优**；只留 ≤4/8 的 19K → **变差**（「overly saturated with difficult problems」） | 最优是**只去全对**，不是激进过滤 |
| **AdaRFT 的 baseline「PPO (w/ Filter)」** | pass@40 **离线**丢 ≤10% 或 ≥90% | **六个设置无一打过 AdaRFT，且 4/6 比普通 PPO 还慢**；原文：过滤「removes a large fraction of the data, including many potentially informative examples ... must be recomputed whenever the model or the data distribution changes」 |

**(g) 训练前就有多少零梯度题（B1.3 要的那个数，最硬的一条）**（`13:553`、`13:40-50`、`13:911`）

- **Skywork-OR1 实测：开训前就有 54%（7B）/ 63%（32B）的题是 0/N 或 N/N**
  （7B = 21.4% 全错 + 32.4% 全对；32B = 20.7% + 42.0%）。
- **GRESO 实测：Qwen2.5-Math-7B 做 GRPO，有效 prompt 比例后期只剩约 20%**；
  原文「if the zero-variance prompt ratio is 80%, DS needs to perform **around five times rollouts**」。
- SRPO：**接近 50% 的组 reward 完全相同**。
- 理论上界对照（本机算）：若 pass rate 服从 U(0,1)，`P(丢弃) = 2/(G+1)`，G=16 时保留 **0.882**、过采样只要 **1.13×**。
  **G=16 的理论 1.13× 对实测 5×，正是「题库 pass rate 极度堆在两端」的量化体现**（`13:556-565`）。
- ⚠️ 由此得出的成本模型警告：漏斗里「难度带筛选留存 0.60」这条外推**很可能偏乐观，实际可能只有 0.2~0.4，候选数要再翻 1.5~3 倍**——
  **这是整个成本模型里最该先用小规模实验钉死的一项**（`13:40-50`、`13:911`）。

**(h) 固定 batch 的三种实现与代价**（`13:632-646`）

| 实现 | 机制 | 代价 |
|---|---|---|
| DAPO | over-sample + buffer | 实测约 **5×** rollout |
| Polaris 两招（Rollout Rescue / Intra-Batch Substitution） | 用 sink buffer 或组内复制替换零优势样本 | **零额外 rollout**，代价是重复样本、有效 prompt 多样性下降 |
| **GRESO** | 用历史 reward **在 rollout 前**预测零方差 prompt 并跳过 | **省 2.0~2.4× 端到端时间**，精度持平（7B 57.5 vs 57.8）；rollout 13.1M → 6.3M |
| LUFFY | 不过滤，把 off-policy 轨迹并进 group 算 advantage | on-policy RL 在 Hard 子集 reward 塌到 0，LUFFY 两子集都升；**+8.0** |

⚠️**不能静态永久剪枝**：GRESO 的时序统计——**超过 90%** 的当期零方差 prompt 在更早 epoch 也零方差，
但**约 20%** 的历史零方差 prompt 会重新变 effective ⇒ **必须留约 20% 探索概率**（`13:643-646`）。

**(i) 口径坑：题集指标 vs 单题难度不能混着论证**（`13:472-479`）

| 对象 | 方差 | 加采样的收益 |
|---|---|---|
| 题集整体指标 | `Var(μ̂|K) = Var(μ̂|K=1)×(1+2/K)/3`（Miller 2024） | **上限只有 2/3**，K=4 降一半，很快饱和 |
| 单题难度分 | `p(1−p)/n` | **一点都不饱和** |

另外：**不能用 `1 − (1 − p̂)^k` 估 pass@k**——Codex 论文原文说这是 consistent underestimate，
**n > 5k 时差距都没完全闭合**（`13:355-370`）。而且该估计量**没有闭式方差表达**，只能 bootstrap（`13:372-375`）。

**(j) 本机选型结论**（`13:481-492`）：**两段式 n=2 → n=8**，平均 4.7 次 rollout，
26.9 万候选共 **0.78M 次 LLM 调用**（n=8 一次性要 1.33M，n=64 要 10.7M）；
**只做硬闸（丢 0/N、N/N）+ 软权重三档桶**。理由就是 (c)：连续难度分在 n=64 下边界误分率仍 20% 量级。
LZE（2605.17003 附录 F）的原话最接近「n 要多少」的答案：**「N = 8 is a robust default」**（`13:467-470`）。

---


---

## B2. 「reward 越低越值得先让教师 rollout 一次再决定要不要蒸馏」——正反证据

先给结论，因为这一节的素材是**不对称的**：

> **正面证据全是间接的**（没有任何一篇给出「对低 reward 题跑教师 rollout」的成本/命中率/ROI 数字），
> **反面证据是直接且实测的**（低 reward 大量来自题坏了、verifier 坏了、重跑抖动、标签错了）。
> 所以这个命题在素材里成立的形式不是「reward 越低越该蒸馏」，而是
> **「reward 低先做归因分型，分型之后才知道该不该叫教师」**。

### B2.1 正面证据（间接，但指向很明确）

| 证据 | 内容 | 出处 |
|---|---|---|
| **GLM-5（2602.15763）的难度过滤就是这个动作** | 保留「GLM-4.7 极少答对或一贯答错，**但更强的 teacher（GPT-5.2 xhigh、Gemini 3 Pro Preview）仍可解**」的题；SFT 阶段同样只留对 GLM-4.7 有挑战的 | `08:624` |
| 推论 | **低 reward 本身不是丢弃标准，「教师也解不出」才是** | 同上 |
| GLM-4.5 | 阶段二要的是 **pass@8 = 0 且 pass@512 > 0**，这批题必须来自**有已验证答案的池子**（否则无法确认可解） | `08:623`、`08:1539` |
| Boundary-Aware | Beyond 档（256 次全败）取边界各 10 道，**做教师轨迹 SFT 桥接再 RL** | `08:565` |
| Qwen3 表 21 | **RL 17,920 GPU 小时 → AIME24 67.6；on-policy 蒸馏 1,800 小时 → 74.4**（AIME25 55.5→65.5，LCB v5 52.9→60.3）。1/10 算力、全面更好，论文还加了一句「**RL 完全没有提升 pass@64**」 | `08:1244-1249`、`92:33` |

Qwen3 那组是**「有更强教师时优先蒸馏」最硬的依据**：算力差 10 倍。
由此派生出可直接抄进正文的三分法（`08:1254-1262`、`08:1423-1427`）：

1. **有明显更强的教师 → 蒸馏，别 RL**（10 倍算力差）。
2. **没有更强教师、或教师也失败**（3D 线、WorldCoder 的 2.7%）→ **RL 是唯一选项**。
3. **想扩 pass@k → RL 必须带课程**，否则 pass@256 比 base 还低（B1.2）。

落到本项目的优先级：**前端/WebDev 先蒸馏；three.js/Blender 复刻（程序化 GT）RL 信号最干净，先做；3D 开放式设计（教师和 verifier 都弱）最后做。**

### B2.2 反例一：低 reward 是因为**题目坏了**（本节的核心反证）

| 证据 | 数字 | 出处 |
|---|---|---|
| **R2E-Gym（2504.07164 §4.2）** | **大多数任务里能区分正确/错误补丁的测试不到 20%**；被污染的测试最多到 10% | `03:71`、`03:89`、`05:174` |
| 笔记自己的推论 | 「这个低区分度问题**在视觉任务上会更严重**」 | `03:332` |
| **WorldBench（2610.10622）特征删除变异测试** | 只读代码的 judge **在 5 个被删特征里有 4 个给了满分**；换新 judge 后被删特征的保留分从 **5.44 降到 3.55**（满分 7.11） | `03:186`、`92:24` |
| 同上 | 渲染 VLM 与代码 LM 在 **32%** 的必查项上不一致，主因是「代码写了但没有一帧画出来」 | `03:168` |
| **GameDevBench（2602.11103）** | 41 道 agent 自动出的题，第一轮人工复核：**43% 没问题、50% 有小问题（物体在镜头外、断言要求指令里没提的东西）、7% 有大问题** | `03:188`、`03:275` |
| **WorldCoder-Bench 的假阳率** | 只读 DOM **33.7%**、截图+VLM **3.2%**、八步 agent **45.6%**；与真值的 τ_b 分别 **−0.021 / −0.068 / +0.111** | `03:185`、`92:50-55` |

**GameDevBench 的 7% + 50% 是「自动出题的题坏率」最直接的公开数字**，
笔记给的门禁是**大问题 ≤ 5%**（`03:337`）。

### B2.3 反例二：低 reward 是因为**verifier 坏了**（本机实测在这里）

- **单 verifier 的天花板**：R2E-Gym EB 43.7%、EF 42.8%（Best@26），而 **Pass@26 是 64.4%**
  → **约 20pp 的能力是被 verifier 的判别力吃掉的，不是模型不行**（`05:162-163`）。
- **EF verifier 会被话术骗**：patch + 完整轨迹 71.82 判别准确率 / Best@26 42.8；只给 patch 68.01 / 37.6；
  去掉思考的轨迹 68.77 / 41.4。论文自己的结论是**这类 verifier 严重依赖 agent 自己说的「我修好了」**（`05:164-172`）。
- **AgentPRM：PRM 被玩坏了而验证集看不出来**——用 10k rollout 训的 PRM，400 步后成功率从 **82% 掉到 70%**，
  **而验证集上的过程 reward 还在涨**；集成也没用（`05:570-571`、`05:1115`）。
  → 「reward 低/高」可以完全是被 hack 的 verifier 的产物，常规监控发现不了。
- **AesCoder 作者自报**：交互 agent 失败就记 0 会**系统性低估分数** → verifier 假阴性是构造的函数（`05:818`）。
- **3DCodeBench 的方法论警告**：很多「变差」的编辑**在视觉上其实更好**——全局外观指标对几何改进不敏感；
  原话是「**用什么 reward 给每步打分，决定了同一个循环看起来有效还是无效**」（`05:846-848`）。
- **NL2Repo：rubric 不是越细越好**——v1→v4 BoN 准确率 57.9% → 67.4%，Kendall τ 0.379 → 0.473；
  **v5 过度细化（穷举禁用命令、程序化护栏）全面变差**（`05:903-906`）。
- 【本机实测】**`ok_lathe` 的金标签是错的——这是整份素材里最有价值的一条反例**：
  人工标 `pass`，实际有缺陷；多视角下 4 个 judge 的 8 次判断里 **7 次判 fail**，理由高度一致（顶部有个圆洞），
  查顶视图渲染**确认了**——LatheGeometry 没有封住极点（`12:620-631`）。
  **三个「权威」判据全都漏了**：人工标 pass；页面单视角像素分 **1.000**；
  多视角剪影 IoU mv_mean **0.998** / mv_min 0.997（**结构性盲区：洞在内部，不改变外轮廓**）；
  按色体素 IoU f4f6fa 0.995 / ff7a1a 1.000（洞的体积太小）。**只有多条件 VLM judge 抓到了，7/8**（`12:632-646`）。
- 【本机实测】**而且这一个错标签直接把结论推反了**：剔掉 `ok_lathe` 后，
  单视角特异度 52/54 = **0.963**，多视角 56/56 = **1.000**（原值 0.968 / 0.891）
  → **一个坏金标签把多视角的特异度从 1.000 压到 0.891，足以得出完全相反的结论**（`12:648-656`、`12:618`）。
  由此写下的预注册规则：**「负例里出现 ≥3 个 judge 一致判 fail 的，先去复核标签，不要先下『特异度不够』的结论」**；
  以及「标负例之前先看多视角渲染」（`12:782`、`12:854`、`12:727`）。

### B2.4 反例三：低 reward 是因为**重跑抖动**（必须先减掉的基线）

| 证据 | 数字 | 出处 |
|---|---|---|
| **Repair or Resample（2608.25920）** | 54 条**原本成功**的执行各重跑 3 次 → **162 次里 85 次失败；54 条里有 39 条至少退化一次——而温度是 0** | `05:483-484`、`05:30` |
| 推论 | **「这条轨迹失败了」在 72%（39/54）的情况下只是重跑抖动** | 同上 |
| **Real-Time Repair** | 纯「回滚 + 重采样」自己就能救回 **16%**（n=55 条真失败回合、各重复 3 次、每次恢复 14.7 次调用）；带定位反馈的那一臂到 **45%** | `05:408`、`05:28` |
| 推论 | **任何「修复/蒸馏有效」的说法都要先减掉这 16% 的基线** | `05:1113` |
| **Repair or Resample 的反直觉结论** | **带反馈的方法比盲目重跑更差**：Self-Reflection 4.29、Critic-Agent 3.73、Random-Node 3.73、Last-Node 1.31，全部低于无引导整条重跑的 **6.90**；只有 Suspicious-Node（规则+语义检测、按类别给指令）到 **20.15** | `05:471-482` |
| **SymTrace：没有固定前缀连「复现同一个失败」都做不到** | Rerun → Replay：rep1 **67.97% → 80.78%**；rep3 **41.42% → 52.43%**；复用 ≥9 个前缀节点时优势 **+25.69** | `05:468-469` |
| **本机的 flaky 基线** | WorldBench 未改动的题单次重跑仍有 **7/32 翻面**；数据质量门禁定 **flaky ≤ 1%**，超了先修确定性 | `08:1563`、`03:335` |
| **噪声地板**（Verification Horizon，QwenWebBench 300 题 × 5 次，ELO σ） | 生成 σ=10.4（极差 24.4）、judge σ=8.5、Render+Judge σ=5.0；某中间 checkpoint 生成 σ=2.8 但 **judge σ=11.4 成了瓶颈**；模型档位差约 40 ELO → **任何「这轮掉了」的说法都要 > 2σ** | `08:1687-1692`、`05:880-886` |

还有一条最阴的：**Repair or Resample 的「芝加哥降雪」案例**——
整条重跑「答对了」，但它是靠常识猜了 30.00%、没拿到任何证据，被判为正确，而失败机制根本没修
（`05:485-486`）。这是**被收进训练数据的 reward 假阳性**。

### B2.5 反例四：低 reward 是因为**判据被豁免/判对了但理由错**（本机实测，最能讲故事的一组）

- 【本机实测】**`nose_back`（鼻子长在后脑勺）：单条件判定 8/8 全判 fail，但 0/8 的理由提到了朝向/背面/反向。**
  judge 一致说「候选缺少鼻子」或「鼻子贴在中间那个球上」——因为页面相机看不到后脑勺，
  「长在背面」和「不存在」在一张图里是同一件事。多条件判定只有 5/8，但**诊断 7/8 正确**（`12:604-617`、`12:850-851`）。
  → **训练数据必须按诊断正确性打标，不能按判定正确性打标，否则单条件那个 8/8 会被当成高质量样本收进去**（`12:908`）。
- 【本机实测】**豁免条款滥用**（该挂却放过）：单条件 8 例中 **4 例（50%）**明确援引了取景/相机/透视/朝向豁免；
  多条件 6 例中 **4 例（67%）**（`12:289-295`、`12:660-663`）。原话样本：
  - `head_up_0.3` claude-opus-5-5：「仅整体取景位置和缩放不同，属允许差异」
  - `head_up_0.3` doubao：「顶部遮挡属于取景带来的允许差异」
  - `body_r_+20%` doubao：「透视带来的视觉大小差异属于相机取景角度范畴，不算错误」
  - `nose_back` claude-opus-5-5：「雪人整体绕竖轴旋转约 180° 属于取景方向差异，不计入错误」
- 一句可以直接当标题的自评：**「一个把真错误解释成允许差异的模型，和一个看不见这个错误的模型，产物完全一样。」**
  漏判集中在**透视能解释掉的那两类**（几何比例、垂直位移）——**模型不是瞎，它找到了一个合法的解释**（`12:305-307`、`12:665-666`）。
- 【本机实测】**程序化判据在同样这些样本上稳定判 fail**：按色体素 IoU 对 `body_r_+20%` 读到 **0.679**、
  对 `mid_r_-20%` 读到 **0.897**，都在阈值外，**两例都正确判失败**（VLM 只有 4/7 和 8/8）
  → **凡是能被透视/取景解释掉的判据，一律不要交给 VLM**（`12:668-671`、`12:825`）。

### B2.6 反例五：低 reward 是因为**预算耗尽/基础设施挂了**（归因而不是丢弃）

SWE-Master（2602.03411 §3.4.2）的四类失败、三种处理（`08:1042-1047`、`08:66-69`、`05:189-190`）：

| 类 | 判据 | 处理 |
|---|---|---|
| A | `DONE` | 正常 reward |
| **B** | 预算耗尽（`TIMEOUT` / `MAX_STEPS` / `MAX_TOKENS`） | **强制提交 + reward × α = 0.5** |
| **C** | 环境故障（`CONTAINER_FAILED` / `SERVER_ERROR`） | **mask loss** |
| D | 模型自己的错（代码错、空白渲染、断言失败） | 0 或负，**正常回传梯度（这才是要学的信号）** |

- **B 类的硬证据**：RL 早期**约 20% 的轨迹被 token/轮数耗尽截断**，而离线复核发现**其中 24.3% 其实已经解决了问题**（图 5）。
  没有 partial credit，真实进展会被归零、训练崩（`08:524`、`08:1049-1050`）。
- ⚠️**反证**：DeepSWE 把 B 当 C 处理（reward 0 + mask loss）；SWE-Master 在自己的模型上复现这一套，
  **reward 持续下降直到训练崩溃**（§6.3 图 12）（`08:526`、`08:1052-1057`）。
- Magistral（2506.10910）：连续的「通过测试比例」reward **训练更快、少丢 3 倍数据，但最终分略低于二值**（`08:525`、`08:519`）。
- EvilGenie（2511.21654）：30% 留出测试（上限 10 条）相对 LLM judge 只有边际增益，在 Inspect 脚手架下被放弃
  → **partial credit 并不能阻止 hacking**（`08:527`）。
- ⚠️**densify reward 之前必读的反证——Spurious Rewards（2506.10947）**：Qwen2.5-Math-7B 上
  随机 reward **+21.4**、格式 reward **+13.8**、错标签 **+24.1**、1-shot RL **+26.0**、多数投票 **+27.1**，
  而真 ground-truth reward 也只有 **+29.1** → **没有空白基线的 proxy 增益不说明任何事**（`08:544`）。
- CAD-Coder 的崩溃案例（2505.19713 App. B）：只用 CD 做 reward，约 200 步后产出不可执行代码、训练中止；
  格式错给 0 还是 −1 两家分歧（SWE-RL 给 **−1**；GLM-4.5 agent RL 给 **0 并中止轨迹**），本项目建议前者（`08:1129-1137`）。

### B2.7 低 reward 必须先分型：类型决定「叫不叫教师」

- **Real-Time Repair 的失败分型**：只有 `goal_drift` 能靠重试修好（**4/5**）；
  `tool_cascade` 和 `looping` 重试只会复现同一个坏结果，必须上报升级（`05:420-421`）。
  → **「教师介入值不值」的答案按类型翻转。**
- **错误必须来自策略自己——ReTerm（2610.18484）**：base 失败 → **快照虚拟机** → 教师（DeepSeek-V4-Pro）
  **从失败状态继续**（只告诉它「上次失败了」，不给隐藏测试细节）→ 过滤成 ReTerm-10K。
  ReTerm-9B 在训练 harness 上比 Qwen3.5-9B **+14.6pp**，换到 Terminus-2 / mini-SWE-agent / OpenHands 仍 **+6.7~12.4pp**。
  作者点名原因：**手工注入的错误与 agent 自己执行时产生的错误分布不匹配**（`05:293-308`）。
  工程细节：**在尝试结束时暂停并快照虚拟机，之后再恢复跑 verifier**，免得 verifier 自己的改动污染快照（`05:296-297`）。
- **离线修正轨迹 SFT 学不出自我纠错——SCoRe**（MATH500 / Gemini 1.5 Flash）：
  base Δ(t1,t2) = **−11.2**；STaR D+ 只 +0.4；Pair-SFT +1.8；**SCoRe（on-policy 两阶段 RL）+4.4**，Δ 改善 **15.6pp**。
  HumanEval（Gemini 1.0 Pro）SCoRe Δ=**+12.2** vs base +3.0，差 9.2pp（`05:252-262`、`12:412-425`）。
  两个失败机制：**分布漂移**（学会纠 base 的错，不是自己的错）和**行为坍缩**（学会「第一轮答好、第二轮别改」，
  编辑距离分析显示第二轮常常一字未动）（`05:265-267`）。
  **Pair-SFT D_SFT+ 的 Δ / 错→对 / 对→错 = 0% / 0% / 0%**——离线纠错 SFT 的自然收敛点就是「不碰第二次」（`12:418`、`12:422`）。
- **成本侧最直接的反对意见**：CLEANER 指出 **rollout 占 RL 运行时间的 80% 以上**，
  所以 rstar2-agent 式「采 2 倍候选再挑最好」太贵（`05:291`）——这是「额外加教师 rollout」最硬的成本论据。
- SWE-Master 还会**直接丢掉 reward = 0 的轨迹**（第一道格式过滤）→ 低 reward 轨迹根本进不了 SFT 池，
  它们的价值只剩题目层面的信号「这道题有通过也有失败」（`05:181`）。

### B2.8 顺带：纯净轨迹 vs 带纠错轨迹（决定蒸馏什么，不只是蒸馏哪道题）

| 证据 | 数字 | 出处 |
|---|---|---|
| **AgentRefine 四变体消融（8,000 条，Success/Progress）——最干净的一组对照** | 完整版（错误被 mask）Alfworld 48.5/61.5、BabyAI 37.1/51.7、SciWorld 7.7/33.1、PDDL 21.7/37.4、Jericho 5.0/26.2；**纯净数据（无错误无纠正）** 49.3/65.2、30.4/43.1、5.5/21.3、**11.7**/32.5、**0.0**/13.8；错误轮也进 loss（最差）29.9/43.9、23.2/31.6、3.3/19.0、8.3/28.3、5.0/18.4 | `05:230-241` |
| 读法 | **去掉试错换来 held-in 的小涨（48.5→49.3）和 held-out 的大跌（PDDL 21.7→11.7，Jericho 5.0→0.0）** | `05:688` |
| **Agent-R 修订测试** | 只用最优轨迹 **10.84**；Agent-R **46.75**；Direct-Revision 35.67；GPT-4o 最优轨迹 8.34；ETO 13.08。只用纯净轨迹训的模型在 SciWorld / TextCraft 上接近 0 | `05:216-218`、`92:42` |
| 同上 | **早截断优于只在末尾纠错（46.75 vs 35.67）**；把「好的」（无修订）混进最优轨迹会**降分** | `05:220-222` |
| **PALADIN** | 只用成功轨迹的 ToolBench 恢复率 **32.76%** vs PALADIN **89.68%**；TSR 57.4% vs 78.38% | `05:354-364` |
| ⚠️ 但 | PALADIN 混进了推理时检索，**不是干净的数据配比消融**（去掉检索：RR 89.7→61.4，TSR 87.4→57.3） | 同上 |
| **AgentHER 反例** | 不改写目标直接喂失败轨迹是**负收益**：SFT-Random（同量失败数据直接 SFT）WebArena 14.7 / ToolBench 54.8，**低于只用成功的 18.9 / 61.2** | `05:31-33`、`05:706` |
| 负例 token 权重（Verification Horizon 扫描） | w_neg = 0.0 → **37.2%**；0.5 → **35.1%**；1.0（基线）→ **41.8%**；**0.8 → 44.4%**。整条丢掉失败轨迹再 SFT 也没有显著增益 | `05:16`、`92:41` |
| 读法 | **别删负例，也别把它们权重归零；0.8 是唯一超过基线的一档。**⚠️非单调（0.5 比 0.0 更差），论文没解释 | `05:691`、`05:1003` |
| Span-KTO | 把负例当偏好推开：SWE-bench Verified **54.2% → 59.8%** | `05:16` |
| CLEANER / SAAR | 故意保留 **30% 原样**（70% 改写 / 30% 不动）以平衡「避错」和「纠错」；AIME 约 +6%、GPQA 约 +3%、LCB 约 +5%，RL 步数只用三分之一 | `05:281-284` |
| ⚠️**配比没人系统扫过** | 公开的四个配比点各自是任意的：CLEANER 70/30、PALADIN 80/20、Verification Horizon w_neg=0.8、ReTerm 每次更新 8 组原始 + 2 组恢复。**「没有任何工作做过配比的系统扫描」**，建议从 70/30 起当超参——**这是推断** | `05:372-380`、`05:724-726` |

## B3. 判断「题目坏了」的方法：响应模式统计 vs 人工标注

### B3.0 这一节的结论句（可直接当正文论点）

> **「这题欠规约吗」的人际一致性（Krippendorff α ≈ 0.24）比「这题多难」（Fleiss κ = 0.78）低了一个量级。**
> 所以**坏题这道闸优先用响应模式统计，不要用人工标注**：
> item-total 相关 1,000 题跑 1 分钟、precision@50 最高 84%；
> 而同一份 rubric 的人工复刻花了 7 名研究者 7 周、约 882 人时，α 始终没过 0.67 的可信阈值。
> 出处 `13:802-813`、`13:855-868`、`13:900-914`。

### B3.1 先确立「坏题占比」的量级：主流 benchmark 的失败里有一半以上不是能力问题

| 证据 | 数字 | 出处 |
|---|---|---|
| **SWE-bench Verified 的人工筛查（2024-08）** | **93** 名有经验的 Python 开发者，从 2,294 条随机抽 **1,699** 条；**问题描述欠规约 38.3%**、**单测可能把正确解误判为错 61.1%**、**合计筛掉 68.3%**，最终 500 条 | `13:691-706` |
| 同上，效果 | 同一 scaffold 下 GPT-4o **16% → 33.2%（翻倍以上）** | `13:700` |
| 同上，规则 | ensemble label ≥ 2 即剔除；ensemble = 三名标注者**取最大值**（任一人判严重即剔除） | `13:702` |
| **OpenAI 停用 SWE-bench Verified（2026-02）** | 审计 500 题中 **138 条（27.6%，都是模型常失败的）**：**测试会拒掉功能正确解的至少 59.4%**，其中「强制与任务无关的实现细节」**35.5%**、「检查了题面没要求的功能」**18.8%** | `13:709-718` |
| 动机 | 近 6 个月 SOTA 只从 74.9% 走到 80.9%，需要判断**是模型到顶还是数据集到顶** | `13:717` |
| **OpenAI 又推翻对 SWE-bench Pro 的推荐（2026-07）** | 公开集 731 题；**Codex agent + 人类研究员定论 200 条（27.4%）为缺陷题**；并行 5 名资深开发者独立评审 **249 条（34.1%）**；**两条流水线一致率 74%** | `13:720-730` |
| 实例 | OpenLibrary 题面要求 1 个空格，hidden test 要求 2 个 | `13:729` |
| **SWE-Bench+（2410.06992）** | 人工复核 251 条「判通过」的补丁：**答案直接写在 issue/评论里的 82 条（32.67%）**、可疑修复合计 **160 条（63.75%）**；滤掉问题实例后 SWE-Agent+GPT-4 **12.47% → 3.97%** | `13:737-754` |
| 同上：已清洗的集子里泄题仍在 | Lite **18 条（33.33%）**、**Verified 37 条（33.04%）**；解决率 **Verified 22.4% → 10.0%** | `13:755-757` |
| **UTBoost（2506.09289）** 自动补测试反查假阳性 | **36** 条任务测试不足，揪出 **345** 个被错判为 pass 的补丁，影响 **Lite 榜条目的 40.9%、Verified 的 24.4%**，造成 18 和 11 处名次变动 | `13:757-758` |

**本机对照**（`13:732-736`）：
`90_local_experiments.md §5` 独立踩到同一个坑——
cup-wood-color 要求「有别于木色的独立颜色」而 verifier 要求恰好是 `0x3a9ad9`；
legs-centered 要求「位于四个角落附近」而 verifier 要求几乎重合。
**「OpenAI 在 500 题上栽的和我们在 9 题上栽的是同一个错误，比例也接近」（本机 2/9 = 22%，他们审计的失败题里 ≥59.4%）。**

### B3.2 最干净的分离证据：同一批模型、同一个 pipeline，「坏题归因占比」从 0% 横跨到 93%

Platinum Benchmarks（2502.03461，`13:759-788`）。**方法本身就是最低成本的坏题筛法，可直接抄**：

```
把每题发给多个前沿模型，只人工复核「至少有一个模型答错」的题
  gold 错   → 前沿模型普遍与 gold 不一致
  题本身坏  → 模型互相不一致
作者明说这给出的是下界（所有模型一致错且与 gold 一致的坏题会漏掉）
```

表 4「模型错误里有多少其实是 benchmark 的错」：

| 数据集 | 原始平均错误 | 清洗后 | **benchmark 归因占比** |
|---|---|---|---|
| SingleEq | 1.1 | 0.1 | **93%** |
| HotpotQA | 26.4 | 2.3 | **91%** |
| SingleOp | 2.5 | 0.3 | **90%** |
| MultiArith | 3.5 | 0.4 | **89%** |
| SQuAD2.0 | 56.2 | 9.9 | **82%** |
| SVAMP / DROP | 18.8 / 28.4 | 4.3 / 6.6 | 77% / 77% |
| GSM8K | 10.1 | 5.2 | 48% |
| Object Counting | 6.3 | 4.8 | 24% |
| Winograd WSC | 16.6 | 15.0 | 10% |
| MMLU HS Math | 20.5 | 19.5 | 5% |
| Navigate / Logic Ded. 3-Obj | 5.9 / 2.4 | 5.9 / 2.4 | **0%** |

**这一列从 0% 到 93% 横跨全区间——这就是「任务难」与「题/判分器坏」可以被量化分离的最直接证据。**

### B3.3 人工标注这条路的一致性数字（为什么它不可靠）

| 场景 | 指标与数值 | 出处 |
|---|---|---|
| **SWE-bench Verified 的 OpenAI 公开标注（第三方重算）** | Krippendorff **α = 0.24**（issue clarity / 欠规约判定）、**α = 0.41**（test adequacy） | SPICE 2507.09108，`13:804-805` |
| 同 rubric 的独立复刻（7 名 SE 研究者、7 周、840 实例、约 **882 人时**） | α **始终未超过 0.67** 的可信阈值，实测落在 **0.0~0.4**；OpenAI 用 moderator 裁决分歧，复刻要再加 **25%** 开销 | 同上，`13:806` |
| SQuAD 坏题三分类标注 | α = **0.344** | Rodriguez et al. ACL 2021，`13:807` |
| **对照：SWE-bench M 的难度标注** | **Fleiss κ = 0.78** | 2410.03859，`13:808` |
| **LLM 替代人工的上限（SPICE）** | SWE-V 标签上 ICA 准确率 **87.3%**、TCA **68.5%**；人工复评 ICA **93.5% 正确**、**TCA 仅 60%**。成本：1,000 实例从约 **10 万美元**人工降到 **5.10 美元** | `13:809-810` |

**SPICE 那一行是整节性价比最高的数字：约 2 万倍降本，而「题干清晰度」这一维的准确率 87.3%/93.5% 已经够用，
「测试充分性」这一维 68.5%/60% 不够用——所以 test adequacy 必须留给程序化判据（变异测试），不要交给 LLM 或人。**

其它来源的标注一致性（跨任务类型的横比，来自 `05/12`）：

| 标注对象 | 一致性 | 出处 |
|---|---|---|
| 「改写后的目标对不对」（AgentHER，3 名标注者） | **κ = 0.82**；改写精度 **97.7%（127/130）**；单 judge 复评 94.1% | `05:320` |
| 「哪一步错了」vs「哪一类错」（SymFail，536 条手标失败轨迹） | **失败节点类型 Fleiss κ = 0.81；主类别只有 0.62** → **「哪一步」比「哪一类」好标得多** | `05:467` |
| 成对选择（BlenderGym，7,950 次判断 / 50 名参与者） | **人与人 0.79**、Claude-3.5-Sonnet 0.66、随机 0.50 → **人人一致性 0.79 就是 verifier 的天花板** | `12:79`、`05:876-877` |
| ⚠️ 反向案例（AesCoder） | **GPT 与人一致 80.9%，而人与人只有 68.7%** → 这里人类基线本身就不稳 | `05:817` |
| 静态 rubric judge vs 人（Verification Horizon） | **Spearman 0.905 / Kendall 0.786**（Qwen3.6-Max）；同族内 τ=1.0，跨族 τ ≥ 0.93；prompt 严格度改变绝对分但不改排名 | `05:893-894` |
| **ArtifactsBench** | 与 WebDev Arena **排名一致 94.4%**；与人类专家**两两一致最高 90.95%**（1,825 题、自动渲染 + 三帧截图 + 源码 + 每题 10 维清单） | `12:206-210`、`92:44` |
| VAGEN（以人工评估为 GT，OSWorld-Verified） | **Acc 92.9 / F1 94.6**（ProRe 87.3/90.4，ZeroGUI 83.7/87.7） | `05:634-636` |
| CUARewardBench | 整体准确率 **81.3**（Adaptive-Group）；CUAStepBench F1 只有 **39.9** | `05:615-616` |
| HSL 自动重标注 | 准确率 **90%**（抽检 200 条） | `05:333` |
| **AgentDebug 定位准确率**（AgentErrorBench 200 条手标，GPT-4.1，三环境均值） | **All-Correct 24.3%** vs 最强 baseline 0.3%；**步级 45.0%** vs 28.0%（GAIA 58.0 vs 30.0） | `05:391-392` |
| ⚠️ 同上 | **检测器极度依赖底座**：GPT-4.1 All-Correct 32.0，**其它模型全部只有 2.0** | `05:394` |

**AgentDebug 那两行是「自动标坏题/定位坏步」的天花板读数：整条轨迹级只和人工一致 24.3%，步级 45%。**

### B3.4 响应模式统计这条路：IRT 与 point-biserial（本节推荐的主路线）

**IRT 2PL**（`13:815-880`）：

```
P(X_ij = 1 | θ_j) = σ( a_i · (θ_j − b_i) )
  θ_j : 模型 j 的潜在能力
  b_i : 题 i 的难度
  a_i : 题 i 的区分度
Fisher 信息：I_i(θ) = a_i² · P_i(1 − P_i)     ← 在 P=0.5 最大，且可加
```

**判据分工（这就是「难」与「坏」的分离）**：

| 参数 | 含义 | 判据 |
|---|---|---|
| **b_i 高** | **难** | 正常，是我们想要的 |
| **a_i ≤ 0** | **坏** | Rodriguez et al. ACL 2021 特意允许 γ<0 来抓坏题：**γ<0 ⇒ 标注错误**（能力越低反而越容易答对） |
| **4PL 的 feasibility（d）低** | **欠规约** | PSN-IRT（2505.15055）Finding 5：**低 feasibility 常源于 under-specified / 过于宽泛的题** |
| 零方差（全对或全错） | 区分度不可识别 | Vania et al. ACL 2021：**占全数据的 4%**，29 个数据集中 13 个至少含一条；**NewsQA 约 16%** 的样本被所有模型答错 |

规模参照（`13:845-853`）：
- Rodriguez et al.：SQuAD 2.0 排行榜 **161** 个 dev subjects、**11,873** items（190 万对）。
- **tinyBenchmarks（2402.14992）**：Open LLM Leaderboard **395** 个 LLM、约 29k items；
  **每 scenario 100 题即可把性能估计误差压到约 2%**：MMLU 14k → 100（**140 倍降本**）。
- **metabench（2407.12844）**：**n > 5,000** 个 LLM、**28,632** items → 压到 **858** 题（**< 原规模 3%**），
  重建总分 RMSE **0.58%**，Spearman r = **0.998**。
- PSN-IRT Finding 2：**最难题的 IRT 难度很少超过 1.0**，而 DeepSeek-V3 的能力估计 **>3.0**（benchmark 已饱和）。

**point-biserial（成本最低的一招）**（`13:855-880`）：

```
r_pb(i) = corr( X_i , S − X_i )        ← 必须用 rest-score 版，不剔自身会被系统性抬高
```

理论依据（2511.16842 Corollary 2）：**若 Rasch 模型成立，item-total 相关必为正**；
因此**低或负的 item-total 相关 = 单维假设被违反 = 该题可疑**。

实测效果（同文）：

| 项 | 数字 |
|---|---|
| 实际用的统计量 | **tetrachoric correlation**（inter-item），约 **1,000 题的 benchmark 1 分钟**跑完 |
| 送审深度 | 每个 benchmark 只 flag **50 题**给专家，报 precision@50 |
| **命中率** | 九个 benchmark 上，被 flag 的题**最高 84%** 经人工确认存在实质缺陷 |
| 新发现的第三类无效题 | **grading issues**：答案 `4.00` 但 grader 只认 `4`；`15.0` ≠ `15`；`3 PM` ≠ `15:00` |
| 增量 | **在 GSM8K 上，在 Platinum 已修订的基础上又找出 16 条此前未发现的无效题** |

阈值惯例（经典测量学，`13:870-876`）：**r_pb ≥ 0.30 区分良好；0.20~0.29 勉强可接受；< 0.20 区分差需修订；≤ 0 红旗（可能答案键写错）**。
⚠️**注意**：区分度在极易/极难题上会被天然压低（`I_i(θ) = a_i²P_i(1−P_i)`，P→0 或 1 时信息趋 0），
**不能脱离难度孤立判读 r_pb**（`13:877-878`）。

一个真用了这套阈值的 LLM benchmark（EduArt，2607.02007，`13:880-884`）：871 题、12 个模型，
**831/871 可算区分度**——剩下 **40 条被所有模型答对、方差为零，区分度无法定义**；
平均 r_pb = **0.514**；**最差题型是 True/false：83 题平均 r_pb 仅 0.245，其中 poor 24 条**
→ **题型本身就是坏题源。**

### B3.5 ceiling check：判「题干欠规约」的程序化做法与数字

（`13:790-800`，这一套是 B3 里**唯一能判「题干欠规约」而不依赖人工**的工具）

| 做法 | 公开案例与数字 |
|---|---|
| **参考解执行校验**（gold 必须让 F2P 翻转） | SWE-bench 构造：**砍掉约一半候选任务** |
| **人类 ceiling** | **BigCodeBench：32/33 = 97%**（33 条最终题面随机分给 11 名标注者）。低于此阈值的题 = 测试过严或题面欠规约 |
| **evaluator 满分可达性证明** | TheAgentCompany：每任务须有**截图证明「正确完成即满分」**；LLM judge 若「交付物正确却因中间步骤误判而 0 分」，框架会**覆盖评分给满分** |
| **oracle 信息注入** | SWE-bench 表 20：Claude 2 BM25 **2.27% → oracle 4.01%**；SWE-Llama 13b **0.70% → 4.54%**（**2~6 倍跳升**）⇒ 之前的失败很大一部分是「信息没给到」而非不会修 |
| **交互式澄清** | **Ambig-SWE（2502.13069）**：模型**分不清** well-specified 与 under-specified；但允许向用户提问后性能**最高 +74%** |
| **默认猜中率** | 2505.13360：LLM 默认能猜中未写明需求的比例 **41.1%**；欠规约 prompt 在换模型/换 prompt 时**回归概率是 2 倍** |
| **补测试反查假阳性**（verifier 太松的反向 ceiling） | UTBoost：345 个假通过补丁 |

**本机口径的 ceiling check**（`13:888`）：**把参考 9 视角渲染图加进 problem statement，重测通过率，跳升 ≥ 0.3 判为欠规约。**
`90_local_experiments.md §6` 已经把它设计成实验矩阵的独立一维（text vs text+参考图），**但还没当闸用**。

### B3.6 运行时代理指标：不用标注就能看出「题/环境坏了」

| 指标 | 阈值 | 机制与出处 |
|---|---|---|
| **环境失败率** | **正常 < 2% 且平稳；> 5% 必须停下修基础设施，绝不能继续训** | GRPO 组基线被 0 分污染 → **「剩下 5 条哪怕写得很差也会拿到正优势，等于用基础设施噪声给坏答案发奖」**（`08:1562`、`08:1675`、`08:1066`、`08:1071-1074`） |
| **flaky 率** | **≤ 1%**，超了先修确定性 | WorldBench 未改动的题单次重跑仍 **7/32 翻面**（`08:1563`、`03:335`） |
| **全对组/全错组占比** | 全错组应下降、全对组应上升；**全对组冲到 80%+ 说明该换课程档位** | `08:1561` |
| **verifier 通过率与 clean resolved 的背离** | 带轨迹级行为监控：**Hack Rate 37.76% → 1.31%，Clean Resolved 40.22 → 60.53（+20.31）**；SWE-bench Verified hack 率 51.49 → 2.13。**训练动态（图 5）：不监控时 verifier 通过率一直在涨，而 clean resolved 后期崩塌** | `08:1653-1661` |
| **噪声地板 σ** | 任何「这轮掉了」要 > 2σ | 生成 σ=10.4、judge σ=8.5、Render+Judge σ=5.0；某 checkpoint 生成 σ=2.8 而 **judge σ=11.4 成为瓶颈**；模型档位差约 40 ELO（`08:1687-1692`） |
| **重复动作序列** | ⚠️ 只是失败的标记，不是可干预的原因 | SWE-smith：**超过 25% 的轨迹含长度 ≥10 的重复动作序列**（Claude 3.7 不到 4%）；长度 10 的重复对应 **89% 的失败概率**。**但加脚手架干预压制重复并不能提高 resolve 率**（`05:149-152`） |
| ⚠️ **partial rollout 的统计偏差** | 一个 prompt 组只有最长的那条跑完才算完成 → **滞留 buffer 系统性偏向短轨迹，而视觉编码里「短」通常意味着「没自检」** | `08:1076-1081` |

### B3.7 哪些捷径必须在环境层堵（否则「通过率」本身就是假的）

- **Verification Horizon 表 2**（Qwen-Turbo，训练集 resolved 59.99% 基线）——**只有策略依赖的捷径与分数正相关**：
  解法产物检索 Freq **4.32%** / Resolved **72.34%（+12.35）** / phi +0.054；外部修复查找 7.03% / 61.69%（+1.70）。
  其余全是负的：可见测试过拟合 30.00% / **−8.37**；harness 篡改 8.25% / **−18.52**；测试 oracle 篡改 3.69% / **−12.70**
  → **要监控的是「可达的外部捷径」，不是硬编码常量**（`08:1637-1649`）。
- **模型会主动找路**：SWE-Master §6.4 记录模型自发用 `git show` / `git log` 去拿 golden patch，
  环境必须拦截并返回禁止警告；**消融显示放宽 git 限制会略微降低分数**（`08:1105`）。
  WorldCoder-Bench App. D.2 记录了模型绕过给定素材目录去 GitHub 拉模型（`08:1101`）。
- **多模态 reward hacking**（2607.09492）：只看结果最高 **48.1%** hacking；32B 仍有 **54.9%** 更差率；
  GRPO 48~53%、RLOO 67~68%、DAPO 从 2B 的 67.2% 降到 8B 的 45.5%。
  **关键一行：关键词式的「视觉证据 reward」比答案感知式 reward 更容易被 hack（高 2.2~3.4 分），只有 VLM-as-judge 的语义验证能降低 hacking**（`08:546`、`08:93`、`08:693`）。
- **ARA（2602.01750）：proxy reward 根本看不见 hacking**（真实 0.91 vs 利用 0.89，**Δ=0.02**）；GPT-4 Δ0.44；训过的 Auditor Δ0.63。
  Goodhart 起点：代码 gaming 约 **1,000 步**（4,000 步时 hacking 饱和在约 59%）、长度偏置约 3,500 步、谄媚约 4,000 步（`08:700`、`08:1612-1632`）。
- **CHERRL**：rubric-RL 的 hacking 起点步数可复现（VerInstruct 词汇 116 / 格式 301 / 自夸 478；HealthBench 语气 68 / 词汇 91 / 自夸 460）；
  起点后 100 步内捷径率上升 ≥40%；IFBench Strict **31.7 → 23.7**。
  ⚠️**警告：有些被 hack 的模型在 Arena-Hard 上不掉分（自夸 10.5 > 无偏置 8.5）→ LLM-judge 的通用榜单无法伪证 hacking**。
  标注为受控注入偏置实验，不是真实 hacking 分布（`08:1586-1608`、`08:1837`）。
- **RULER 的加法聚合 hacking 面**：加权求和把 **Aesthetic 从 4.31 推到 6.70（+55%）**，而 **CLIP −20%（0.244 → 0.196）**、
  Icon rubric 0.395 → 0.262、tokens 0.3k → 6.3k（`08:672-684`）。
  对应的正面做法（Adaptive-Group 消融）：**两个维度要相乘不要相加**——换成求和后 recall 升到 97.2 但
  **特异度塌到 53.5（≈ 全部放行）**（`05:618-623`）。
- ⚠️**hacking 不是必然的**：GLM-4.5 的指令跟随 RL 跑约 1,000 步没出现明显 hacking（§3.4 图 9）；
  UI-TARS-2 用 **F1=83.8 且假阳率偏高**的 ORM 做 GUI RL 也没出现实质 hacking（§4）。
  判据：**judge 的误差是不是可被模型主动制造的——随机误差可容忍，可被利用的系统误差不可容忍**（`08:103-105`、`08:1399-1409`、`08:1678-1681`）。

### B3.8 变异测试：本机最强的一环（判「verifier 查少了」）

- 【本机实测】snowman **13 个变异**的四档判据检出：**页面截图 5/13、多视角 9/13、按色体素 11/13、多视角+体素 13/13**；
  **按色体素 IoU 是唯一能把 6 个候选全部分开的指标**；stage-0 门禁要求 **≥ 12/13**
  （`08:1442`、`08:1322`、`08:1809-1813`）。这些数字只花几十个 token，而 8 张图要约 5,600 token。
- **WorldCoder StateProbe 的变异加固契约**：向已验证实现注入缺陷，**契约必须拒掉每一个变异体**，否则这道题改掉或丢掉（`03:270`）。
- **rubric 也要过变异测试**：用 R 生成 rubric，再让它去判 R 的变异体；**杀不掉变异体的题就是太松**（`03:170-171`）。
- **CriticGPT 的非平凡性验证（标准的反捷径做法）**：训一个「这段代码被改过吗」的判别器，
  确认**小模型做不了这个二分类**、且随规模平滑提升 → 防止插入的 bug 带上格式/风格捷径特征（`12:355`、`12:837`）。
- **CriticGPT 的对抗式难度过滤（可直接抄）**：要求插入的 bug **至少被三个 LLM critic 采样中的一个漏掉**；
  论文称这种对抗式收集「noticeably increased the subtlety」；收集期间给标注者用的 critic **被换过两次**（`12:353-354`）。
  ⚠️ 它保留了一部分未篡改样本（纯篡改会偏置分布），**但未篡改样本的标注一致性更低、训练效果更差，只能掺不能当主来源**（`12:356`）。
- ⚠️**判别-批评（DC）gap**：CriticGPT App. 7.7 训了判别器来量「模型知道多少 vs 说出多少」——
  **判别器的分数并不能预测 critic 的表现**，而在最大判别器最自信判错的那 10% 样本上 critic 仍能抓到约 **54%**
  → **「模型其实知道只是不说」这个说法没有被证实；两条能力路径是分开的，必须分开训**（`12:275-279`）。
- **测试质量的量化**：**CodeContests+（2506.05817）用 1.72M 条带标签解法测每题的 TPR/TNR → 同阈值下合格题数翻倍**；
  **HardTests（2505.24098，47,136 题）：有 oracle 程序时，合成测试的精度 +11.3 分、召回 +17.5 分，而旧式合成测试在难题上假阳率 >90%**（`03:271-272`）。
- **题面-测试对齐复核**：agentic 质量 judge 进 Docker 读代码跑命令判 instruct_clear 与 instruct_ut_align；
  **instruct_clear F1 ≈ 92~95，instruct_ut_align F1 ≈ 75~78；把 gt patch 给它能提高后者的召回**（`03:273`，Verification Horizon §2.2）。
- **人工复核的流程（GameDevBench）**：agent 出题 → 抽样复核 → **把常见错误写成清单让 agent 自纠** → 全量人工复核（`03:275`）。

### B3.9 本机两套闸的现状与最该补的一条（`13:882-914`）

| 要判的 | 判据 | 本机现状 |
|---|---|---|
| **任务难不难** | pass@8 分桶（两段式 n=2 → n=8） | **待建**（S2 阶段） |
| **题干欠规约吗** | ceiling check：参考 9 视角图进题面，**跳升 ≥ 0.3 判欠规约** | 已设计成实验矩阵一维，**还没当闸用** |
| **verifier 查多了吗** | `spec.json` 白名单 + 可见性审计（题干没钉死的字段不许进 spec） | Blender 侧有 spec.json，**three.js 侧还没有** |
| **verifier 查少了吗** | 变异集检出率（本机 47/47）+ 作弊页拦截率（本机 7/7） | **已有，是本机最强的一环** |
| **这题是坏题吗** | ① 多模型分歧三角定位（Platinum 法，只复核「至少一个模型答错」的题）② **item-total 相关 < 0.10 或 ≤ 0 送人工** ③ 零方差题单列 | **待建** |
| **verifier 在初始状态就通过了吗** | FACET 判据 ii | **缺这一条** |

**最该补、也最便宜的一条：item-total 相关 + 零方差检测。**
它不需要额外采样（难度标定的 rollout 结果直接复用），**1,000 题 1 分钟，precision@50 最高 84%**；
按 10 万任务规模，每轮 flag **1,200 条**送人工，正好对上抽检配额（`13:910-914`）。

### B3.10 三条入池硬规则（抄 SWE-bench 的逻辑，`03:84-87`）

1. **F2P 必须在 S0（空解/初始状态）上全部失败**，否则是平凡题。
2. **F2P 与 P2P 必须在 R（参考解）上全部通过，且三次重复稳定**，否则是不可解题或不稳定 verifier。
3. **断言不得依赖 R 的实现细节**（变量名/类名/函数拆分）；需要的锚点必须写进可见的题面 I。

可计算质量指标表（阈值初值为推导，`03:326-341`）：
可解率**每题 100%**；非平凡性**每题 100%**，且**空解与静态截图基线也必须失败**；
变异杀死率 **TNR ≥ 95%**；正确解通过率 **TPR ≥ 90%**（太低说明断言绑死了实现细节）；
零区分度的断言删掉或重写；外部范式假阳率在状态层应趋近 0；难度以 0<p<1 为主；
**flaky ≤ 1%**；两条规约对齐项都要通过；**人工复核的大问题 ≤ 5%**；污染 0（命中即删）。

**「判别力是最容易被忽略的一项：可解率只证明 R 能过，判别力证明错的过不了」**（`03:342`）。
而且**指标必须定期重算**——0<p<1 的题会随策略变强变成全对（Verification Horizon：没有固定的 reward 能一直有效）（`03:343`）。

---

## B4. 多样性指标、去重，以及「场景多 ≠ 数据好」的对照数字

### B4.0 这一节最该用的一句话和一组数字

> **「a generator that can create tens of thousands of levels in a matter of minutes is useless if many of those levels are effectively identical to each other.」**
> —— Smith & Whitehead, PCGames 2010（`13:166-172`，这是「组合爆炸 ≠ 有效多样性」最早最明确的出处）
>
> 【本机算术】我们自己的槽位表：**组合空间 7.0e8，可被 verifier 区分的有效等价类约 1.6 万，折损约 44,000 倍**（`13:275-297`）。

### B4.1 定量定义：Hill number 的 q=0 vs q=1（唯一干净的定量答案）

（2310.12952，`13:184-196`）

| 阶 q | 量 | 含义 |
|---|---|---|
| **q = 0** | D_0 = 支撑集大小 | **就是「组合计数」**；论文直接称它 *an uninformative measure of diversity* |
| **q = 1** | D_1 = exp(Shannon 熵) = **Vendi Score** | **有效独特元素数** |
| q → ∞ | 只由最大特征值决定 | 论文建议用它测**重复 / 记忆化** |

**所以「组合空间 / 有效多样性」的折损倍数就是 D_0 / D_1。**

Vendi Score 定义（2210.02410，`13:198-213`）：

```
给相似核 k（k(x,x)=1），K_ij = k(x_i,x_j)，取 K/n 的特征值 λ_1..λ_n
VS = exp( − Σ_i λ_i log λ_i ) = exp( − tr( (K/n) log(K/n) ) )
     即 K/n 的 von Neumann 熵的指数 = K/n 的 effective rank
```

- 互不相似时 **VS = n**（最大），全同时 **VS = 1**；模式数翻倍 VS 也翻倍。
- 成本：一般核 **O(n³)**；核是显式特征内积且 d ≪ n 时降到 **O(d²n)**（与 FID 同阶）。
- ⚠️**致命前提：VS 完全由核决定。** Inception 核量语义、像素核量亮暗颜色，**两者结论可以相反**。

### B4.2 「场景多 ≠ 数据好」的三组对照数字（本节的核心素材）

| 场景 | 「名义计数」 | **有效多样性** | 读法 | 出处 |
|---|---|---|---|---|
| **Stacked-MNIST 模式计数** | Self-cond. GAN / PresGAN / Original 的 **NoM 全是满分 1000** | **VS = 746.7 / 866.6 / 943.7** | 同一张表上把组合计数和有效多样性摆开了 | `13:206-208` |
| **MOSES 分子生成** | IntDiv（平均成对不相似度）把 **HMM 排第一（0.871）** | **VS 把 HMM 排最后（250.9，其余 475~537）** | HMM 产的是**成簇的完全重复**分子；**平均成对距离类指标对成簇重复是盲的** | `13:209-210` |
| **MS-COCO caption** | 人类 5 条 caption | **VS = 4.88**（≈5 条互不相似）；**beam search 只有 3.00**（每 5 条里只有 3 条真不同） | 直接给出「有效条数」的读法 | `13:211-212` |
| **Infinigen** | **182 个生成器、1,070 个可解释自由度** | 论文**自己在表注里把它称作 proxy** | 「组合计数不等于有效多样性」最权威的自认 | `08:…`；`92:38` |
| ⚠️ **Infinigen-Indoors 表 3 的坑** | `w/o Discrete change` 得 **86.20**，**比全系统的 80.84 更高** | 作者明说离散改动「necessary for compelling visuals, but **decrease the quantitative score**」 | **量化指标和观感会反向**——多样性指标涨了不等于数据变好，反过来也成立 | `13:330-334` |

### B4.3 覆盖度指标：三代指标与它们的超参（抄之前必须知道的）

（`13:216-243`）

| 指标 | 定义 | 特征空间与超参 | 已知失效 |
|---|---|---|---|
| PRD (α,β) | 分布分解 | Inception + mini-batch **k-means k=20**；报 (F_8, F_{1/8}) | 过于乐观；截断时反报更低 precision |
| **improved Precision / Recall** | 以每点到**第 k 近邻**的距离为半径作超球，并集 = 流形估计 | **VGG-16 第二个全连接层**（不是 Inception），**k=3**，\|Φ\|=50000 | 对**离群点敏感**，一个真实离群点就能把流形撑大；**真假分布完全相同时 P/R 也只有 0.68 / 0.67** |
| **Density / Coverage** | coverage = 邻域球建在**真实**样本上，看多少真实点被至少一个生成点覆盖 | **k=5，N=M=10000** | 需要选对嵌入 |

**Density/Coverage 是三代里唯一能「按理论选超参」的**：
Lemma 1——同分布时 **E[density] = 1**；Lemma 2——**E[coverage] = 1 − 1/2^k**，**与数据分布类型和维度无关**，
所以 k=5 给 E[coverage] ≈ 0.969（这就是 k=5 的来历）。
原文对 P&R 的 k=3 的评价是：「The exact principle behind the choices of those values for P&R is **unknown**」。
抗离群实测：按第 k 近邻距离 10:1 切出离群点后，**recall 上升 >11%（CelebA）/ >15%（LSUN bedroom），而 coverage 上升 <2%**。

**一条对本项目极重要的嵌入选择结论**（2002.09797 表 1，`13:235-243`）：
目标域与 ImageNet 统计差距大时，**随机初始化的 64 维嵌入（R64）比 ImageNet 预训练的 VGG16 fc2（T4096）更合理**：

| 域 | 指标 | T4096 → R64 |
|---|---|---|
| MNIST | **Coverage** | **0.108 → 0.714** |
| MNIST | Density | 0.047 → 0.491 |
| 音频（WaveGAN/SC09） | **Coverage** | **0.020 → 0.653** |

这和 `12_self_verification.md` 已记的「**别用 CLIP/SigLIP 当 3D 质量闸**（SigLIP 在 10 个模型上全落 0.077~0.108 窄带）」是同一件事的两面：
**程序化 3D 场景离 ImageNet 分布很远，预训练视觉特征在这个域里会把一切压成一团。**

### B4.4 平均成对距离类指标为什么不能当闸

（Directed Diversity, CHI 2021，2101.06030 表 3，`13:245-258`）

| 指标 | 定义 | **原文给的失效模式** |
|---|---|---|
| **Remote-Clique** | 平均成对距离 | 「**it is insensitive to highly clustered points**」 |
| **Chamfer Distance** | 平均最近邻距离 | 「**it is biased when points are clustered**」 |
| Entropy | Shannon-Wiener | **512 维必须先 UMAP 降到 2 维再切 5×5 网格**；不同网格尺寸结论不同 |
| Span / Sparseness / MST Dispersion | 90 分位半径 / 到 medoid 距离 / MST 边权均值 | — |

COV/MMD（1707.02392）里有一句正中本题：
「Our coverage metric can identify parts of the data distribution that are **completely missed** by the generative model,
something that **diversity metrics based on cardinality might fail to capture**.」

**质量 × 多样性一起表达：k-DPP**（1207.6083 式 92–94，`13:263-273`）

```
B_i = q_i·φ_i，‖φ_i‖=1；L_ij = q_i φ_iᵗφ_j q_j，S_ij = L_ij/√(L_ii L_jj)
P_L(Y) ∝ (Π_{i∈Y} q_i²) · det(S_Y)
         └ 质量项 ┘   └ 多样性项 ┘
```

映射到本项目：**q_i = 任务的可解性 / verifier 判别力评分，det(S_Y) = 特征空间体积**。
**一个 k-DPP 同时表达两者，不需要手调权重**——这是从 26.9 万候选里选 10 万最合适的工具。

### B4.5 本机算术：我们的槽位表差 44,000 倍（最有力的一组自有数字）

（`13:275-297`，取 `10_blender_tasks.md §2.1` 的 `SLOTS`）

| 槽位 | 离散化后档数 | **渲染后可被 verifier 分开的档数** |
|---|---|---|
| table.size（20 × 14） | 280 | 约 70 |
| table.bevel（0.005~0.03） | 26 | **约 3**（48³ 体素 + 剪影分辨率下） |
| **bulb.energy（20~200 W）** | 19 | **0 —— Workbench 下完全不可见** |
| arm.anim（两角各 41 档） | 1,681 | 约 25（5×5） |
| mug.subsurf | 3 | 3 |

```
组合空间 D_0 = 280 × 26 × 19 × 1681 × 3 ≈ 7.0e8
有效等价类 D_1 ≈ 70 × 3 × 1 × 25 × 3   = 15,750
折损倍数 ≈ 44,000 倍
```

**结论：一张看起来能出 7 亿种场景的槽位表，实际只能出约 1.6 万种可被区分的任务**；
要做到 10 万任务，**单模板不够，必须靠模板数和跨模板组合**。

**顺带得到一条验收规则**（`13:294-297`）：`bulb.energy` 这种「采样空间里有、但渲染后 verifier 看不出」的槽位
**必须禁止进 spec.json**。本机 Blender 留出集**唯一的误杀**正是「日光功率 3.0 → 3.5 被 A6 判错」——
就是因为题干没钉死它而 verifier 查了它。这就是 A 主题那条「verifier 能查的信息量必须 ≤ 题面给出的信息量」的反面案例。

### B4.6 一套可直接抄的工程化多样性仪表盘（五条，比任何单一指标都强）

来自 RST（2608.05466，把任务从 **639 个种子递归放大到 37,484 个**，`13:300-317`）：

| 维度 | 口径 | R1 → R15 实测 | 我们对应什么 |
|---|---|---|---|
| **模式均衡** | 改写族上的**熵** | **2.26~2.31 bits**（上限 log₂5 = 2.32）；**最大族占比仅 24.9%~28.9%** | 模板族熵；要求最大模板占比 **< 30%** |
| **变换机制覆盖** | 40 个改写算子的使用覆盖 | 每轮用 **31~38 个**；R15 仍有 **36/40** 在用；**最频繁算子只占 8.0%**（全程最多 12.2%）；前 12 之外的算子仍占 **31.0%** | 破坏算子表（Blender 侧已有 A2/A4/A5/A6/A7/A8/A9 七族）的覆盖率 |
| **血统集中度** | 种子覆盖率 | **98.3%（R2）→ 60.1%（R15）**；R15 保留 363 个种子中的 218 个；**单个种子贡献不超过 0.77%** | 要求单场景贡献 **< 1%** |
| **亲子新颖度** | 父子 token 级新颖度（中位） | R15：instruction **0.36**、solution **0.18**、verifier **0.33** | 题干 / 参考解 / spec 三者各自的变动率 |
| **去重** | 轮内最近邻相似度（中位 / p95） | **0.223（R1）→ 0.464（R15）**，中位仍 < 0.5；**p95 = 0.703** | 直接套用 |

**RST 还顺带证明了污染是可控的**：归一化 13-token 滑窗下**没有任何 benchmark 任务匹配任何合成轮次**，
最大 pairwise 5-gram Jaccard **< 0.009**，且 unigram JSD 从 R1 到 R15 对三个 benchmark **全部上升**
——**递归合成产出的是越来越远离 benchmark 的分布，不是向其收敛**（`13:315-317`）。

### B4.7 防塌缩的六条可执行规则（`13:319-328`）

| # | 规则 | 依据 |
|---|---|---|
| 1 | **验收用 D_1（Vendi Score）不用 D_0（组合计数）**，并同时报 D_0/D_1 的折损倍数 | 2310.12952 明确 q=0 是 uninformative；本机折损 4.4 万倍 |
| 2 | **嵌入用随机初始化低维投影或自己的几何特征，不要用 CLIP/SigLIP/ImageNet 预训练特征** | MNIST Coverage 0.108→0.714；SigLIP 窄带实测 |
| 3 | **覆盖度用 Coverage（k=5, N=M=10000）而不是 recall** | Coverage 有闭式期望 1−1/2^k 可校准；recall 被离群点撑大 >11% 而 coverage <2% |
| 4 | **平均成对距离只能当辅助不能当闸** | 对成簇重复是盲的（MOSES 上 IntDiv 把 HMM 排第一、VS 排最后） |
| 5 | **画 Expressive Range 2D 直方图，轴必须是涌现属性**（mesh 数、连通块数、开放边界边数），**不能是槽位参数本身** | Smith & Whitehead 2010 的第一条方法要求 |
| 6 | **选子集用 k-DPP**，把「可解性评分」当 q、特征体积当多样性，不手调权重 | 1207.6083 |

Smith & Whitehead 最有价值的一条自述（`13:180-183`）：他们靠 Expressive Range 分析发现生成空间严重偏向线性关卡，
真因是「**某组件被选中后再次出现的概率会略微提高**」这个**后期加进去的小实现细节**——
作者说**若不做这种分析永远发现不了**。

### B4.8 去重：十万量级是免费的，所以没有理由做得糙

（`13:918-937`）

| 项 | 依据 | 结果 |
|---|---|---|
| 视觉 embedding（10 万任务 × 9 视角 = 90 万图） | DINOv2 ViT-B 约 200 图/s | **1.25 GPU 小时** |
| pHash 90 万图 | imagededup 官方 dHash 277~426 图/s（4 vCPU 无 GPU） | **约 40 分钟** |
| 全对全余弦（10 万 × 768 维） | 一次 GEMM = 15.36 TFLOP，A100 TF32 按 70% 实效 | **0.14 秒** |
| MinHash + LSH | text-dedup 10 万文档约 11 秒 | 秒级 |
| 向量存储 | 10 万 × 768 × 4B | 307 MB（int8 后 77 MB） |

两条工程判断：
1. **十万量级完全不需要 ANN 索引**，分块暴力 GEMM + 块内 top-k 就是最优解（FAISS 官方也说 1,000~10,000 次检索直接用 Flat）。
   真正的约束不是算力，是**那 40 GB 的输出矩阵**（10 万×10 万 fp32），所以必须分块归约、永不物化全矩阵。
2. **百万级才会碰到唯一的串行墙**：datatrove 的 FineWeb 脚本里 MinHash 第三阶段（连通分量聚类）是
   **单任务、8 核、约 200 GB 内存、约 30 小时墙钟**，不可并行。

### B4.9 结构去重：单位必须是产物（场景图），不是代码

- ⚠️**一个反直觉的事实**：The Stack v1/v2、StarCoder/2、CodeGen、AlphaCode、CodeParrot、OpenCoder **全部**用
  「精确 hash + MinHash-LSH on token/字符 n-gram」，**没有一个用 AST 等价做去重**（600+ 语言无法统一解析）（`13:940-944`）。
  真的用结构哈希的只有两个：**ComPile**（LLVM StructuralHash，精确结构等价无阈值，990 GB → 853 GB，**体积 −35%**，Julia 重复率约 40%）
  和一篇解题程序去重（作者**明说不用 AST 当去重单位**）（`13:946-950`）。
  **明确未找到**：任何预训练级公开代码数据集用 AST 规范化哈希/Merkle 树 + 阈值做去重并公布比例（`13:952`）。
- 【本机证据】`10_blender_tasks.md §2.1` 的 `cube_size2`：换一条实现路径、**世界几何逐点相同**的改写，
  几何信号全部放行（分部件 F-score **0.9993**），**只有按代码比的 A2/A3 会误杀**（`13:956-960`）。
  → **同一个任务有无穷多种代码写法（AST 哈希会算成不同任务 = 假阴性），不同任务也可能有近似代码骨架（假阳性）。去重单位必须是产物。**
- 建议的三级结构指纹（全部取自本机探针已有产物，零额外成本，`13:964-975`）：
  **L-exact**（场景图规范化哈希：`sorted([(几何类型, round(顶点数), round(世界 bbox,3), 量化主色)])` + 灯光类型多重集 + 连通块数 + 开放边界边数，**哈希相同即判重，无阈值**）；
  **L-near**（上面标量拼成的 20~40 维特征向量，抓「同模板换种子」）；
  **L-spec**（`spec.json` 的**断言集合**（族 + 字段路径，不含具体数值），**Jaccard ≥ 0.9 且 L-near 近邻 → 判重**）。
- **L-spec 这一层是别人没有的，也是最该做的**（`13:973-975`）：程序化生成最容易塌缩的不是「场景长得一样」，
  而是**「考的点一样」**——10 万任务里若有 3 万都在考「某个部件缺失」就塌了。
  本机 verifier 层级分布（L1 6 / L2 8 / L3 2）就是一个**现成的粗粒度 L-spec 监控**。

### B4.10 阈值不能照抄（这是全节最容易踩的坑）

**文本/代码侧公开阈值**（`13:979-1006`，可当起点但不能照抄）：
Lee et al. NearDup 5-gram / 9000 签名 / b=20×r=450，s=0.8 → 99.4% 命中，C4 去重率 3.04%、RealNews 13.63%；
**The Stack v1 非字母数字切词 + 256 permutations，Jaccard > 0.85 → 去掉 38.6% 文件 / 53.7% 体积**；
**StarCoder2 / Stack v2 用 5-gram、Jaccard 0.7**；CodeParrot 0.85；
OpenCoder/RefineCode 5-gram / 2048 签名 / 128×16 bands，**SHA256 阶段就有约 75% 文件完全重复**；
**Allamanis 的代码判据：J(T0) ≥ 0.8 且 J(T1) ≥ 0.7**，token ≤ 20 的文件直接排除。
banding 的 S 曲线 `P(命中) = 1 − (1 − s^b)^r`，近似阈值 `t ≈ (1/r)^(1/b)`。

⚠️**num_perm 不能照抄 128**（datasketch 官方实测，`13:999-1006`）：

| 语料形态 | num_perm=128 的精度/召回 |
|---|---|
| 「少量孤立近重复」 | **P、R 在所有 num_perm 下都是 0.92~1.0** |
| **「大片高度重叠的同族」** | **P 0.69~0.77，R 0.69~0.84** |

**我们的任务集属于后者**（同模板换种子就是高度重叠的同族），所以要么上 **256~512 permutations**（开销只多 10%~35%），
要么必须加精确 Jaccard 二次复核。官方还提醒：聚类型语料上**精度不随 num_perm 单调改善**，跟着 (b,r) 的离散台阶走。

**视觉侧阈值表的关键几行**（`13:1010-1034`）：
imagededup 官方结论原文「**Hashing methods do not perform well for finding near duplicates**」；
**Prokos et al. 在 1.18M ImageNet 图上测 pHash 的 FPR：T=6 约 0.044%，T=14 飙到 73%**；
COYO-700M 实际只用 **pHash = 0**；
**DataComp 对评测集去重用 ISC 冠军 copy-detection descriptor（不是 CLIP），余弦 > 0.604169**，
而**CLIP ViT-B/32 在同 precision 下 recall 只有 0.02**；
**DINOv2 自去重用 SSCD > 0.6（1.3B → 1.1B，−15.4%），对评测集去重用 > 0.45（−32.4%）**；
**SSCD 官方推荐 > 0.75（DISC 上 90% precision）**；
**MONET（1 亿级生产集）pHash d=0 清精确 + SSCD ≥ 0.75，累计 −7.7%，并实证 pHash 不可靠：真近重复可达 d=26，而 d=1 就存在语义无关的假阳性簇**；
⚠️ **LAION-400M/5B 自身只有 URL ⊕ alt-text 的 bloom filter——没有图像内容哈希、没有 embedding 去重、没有对评测集去重**。
⚠️**明确未找到**：`pHash Hamming ≤ 5` 或 `≤ 8` 作为公开论文或库的推荐值。
**所以别说「业界通常用 pHash ≤ 5」，那是传说**（`13:1033-1034`）。

⚠️**阈值必须随库规模重标**（ISC2021 实测，`13:1036-1042`）：
**库从 100 万涨到 1,000 万，同一阈值下 recall 不变而 precision 从 0.8 跌到约 0.29。**
所以抄数字之前必做 MONET 那一步：**按 0.05 分箱人工抽检**（十万量级只要几十条样本）。

本机选型（`13:1044-1052`）：第一层对 9 视角剪影图做 **dHash d = 0**；
第二层**不用 CLIP/SigLIP**，改用 **L-near 的 20~40 维几何特征**（本机探针已产出，零额外成本，
而且它们**本来就是 verifier 的判据**，所以「去重指标」和「判别力指标」口径一致）；
第三层可选 **SSCD ≥ 0.75**；第四层 **L-spec 断言集合 Jaccard ≥ 0.9**。

### B4.11 题干去重的特殊规则：题干重复 ≠ 任务重复

（`13:1054-1067`）三层：① MinHash 5-gram，**num_perm = 256**，Jaccard ≥ 0.7（StarCoder2 口径）+ 精确 Jaccard 二次复核；
② 语义层对标 **SemDeDup：ε = 0.03（cos ≥ 0.97）判近重复**；
③ **题干 ∧ 产物联合判重**：题干近重复**且** L-near 近邻 → 判重；
**题干近重复但场景差很远 → 不判重，反而是好数据**（同一句话的多种实现）。

「桌面上放一个杯子」这句话可以对应无穷多种具体几何，**只有 spec.json 里钉死的字段才决定任务是否相同。**
顺带：**短 prompt 集精确匹配几乎没用**（3JSBench 100 条短句、Plot2Code 132 条），只能走域名/仓库级规避 + 人工抽检（`13:1160-1161`）。

### B4.12 ⚠️ 去重会过头：必须记住的反面教训

**FineWeb 实测**（2406.17557 §3.4，`13:1181-1196`）：

| 做法 | 结果规模 | 下游 |
|---|---|---|
| **全局去重**（96 个 CC 快照互相去） | 15T → **4T** token，最老快照被删掉 **90%** | **相比不去重几乎没有提升**，远落后 RefinedWeb |
| 逐快照独立去重 | **20T** token | 持平 RefinedWeb，且逐步过滤均有提升 |

作者解释：收益来自删掉「跨全部快照、动辄几十万文档的**巨型重复簇**」；
**对只有几十个副本的小簇继续去重反而有害**，被保留下来的是长尾低质数据。
对照实验：2013-48 快照「全局去重后留下的 31B token」训出来**不如**「被删掉的那 460B 单独去重后的 171B token」。
**DataComp 同向证据**：池内自去重（T_ADC 0.1/0.2/0.5）下游「与只用 CLIP filter 基本相同」——**无额外收益**。

| 该做 | 不该做 |
|---|---|
| 定位并打掉**巨型同构簇**（同模板 + 同种子族 + 同 spec 的大片任务） | 无脑拉高召回去清小簇 |
| 对公开 benchmark 去污（这一路**只有收益没有损失**） | **把「去重率」当 KPI** |
| 保留「题干近似但几何差很远」的对 | 按题干相似度一刀切 |

### B4.13 去重的收益有多大（给「不做会怎样」定价）

（`13:1206-1215`）

| 证据 | 数字 |
|---|---|
| **The Stack 代码近重复去重（最硬的一条）** | permissive 子集 HumanEval pass@100 **27.21% → 37.00%**；MBPP **44.99% → 54.69%**；all-license HumanEval 36.67 → 44.00 |
| RefinedWeb 消融（零样本均值） | OSCAR-22.01 52.7 → **55.6（+2.9）**；The Pile 53.4 → 54.5（+1.1）；**C4 只 +0.2**（本来就干净） |
| Lee et al. 记忆率 | 无 prompt 下逐字复现训练数据：C4-Original **1.93% → NearDup 0.19% → ExactSubstr 0.14%**（约 10 倍） |
| **Allamanis「代码重复的恶果」** | 不去重会让指标**虚高最多 100%**。JavaScript-150k LM Acc 55.1 → 49.1（−10.9%），**只看标识符的 Acc-ID 17.7 → 8.6（−51.4%）**；code2vec 方法命名 F1 50.98 → 44.71；JsNice 变量命名 55.04 → 34.44（−37.4%）。重复率：Concode-Java 68.7%、Java GitHub Corpus 24.8% |
| **重复数据的「双下降」** | 训练 token 中**仅 10% 是重复**，在最坏重复次数（800M 模型约 100×）下，**性能退化相当于模型缩小 2 倍**；3% 重复数据可让 copying 评测掉 3 倍 |
| **SemDeDup** | 删 37% 无损；删 50% ImageNet top-1 仅降 0.47%（68.27 vs 68.74），**训练时间减半**；保留 63% 反而超基线、预训练快 1.6 倍。**去重开销 < 训练 GPU 时的 1%** |

**最后这条是整节的理由：去重开销不到训练成本的 1%，而不去重的代价是「10% 重复 token ≈ 模型缩小 2 倍」。**

### B4.14 污染隔离：n-gram 挡不住改写（本节最硬的一组反证）

- **LMSYS（2311.04850，`13:1102-1127`）**：让 GPT-4 循环改写测试题直到 n-gram 检测不到，再微调：
  **MMLU / Llama-2-13B 54.8 → 89.9；HumanEval pass@1 / CodeLlama-13B 36.0 → 81.1（GPT-4 只有 67.0）；GSM-8K / Llama-2-13B 28.7 → 95.3。**
- 检测方法 F1（200 对）：**10-gram 重叠在原测试集上 0.816~1.0，但在改写英文/中文/Python/C 上全部是 0**；
  Emb（Multi-QA BERT, 0.5）0.805~0.985 / **0~0.179（中文）**；
  **LLM Decontaminator（top-k embedding 召回 + GPT-4 逐对判定）0.940~1.0。**
- **嵌入阈值不可统一的直接证据**：阈值 0.8 时 Abstract Algebra 能抓到但 Sociology 的改写漏掉；0.4 时 Abstract Algebra 大量假阳性。
- 真实数据集里的改写污染率（GPT-4 判定）：**The Stack 对 HumanEval 18.9%（31/164）**、StarCoder-Data 15.9%、
  CodeAlpaca 12.8%、RedPajama-1T 8.5%、**MATHInstruct 对 MATH test 15.4%（769/5000）**。
  ⚠️**注意最后两条口径：合成数据（GPT-3.5/4 生成的）也会无意污染。**
- **Llama 3 的官方承认**（`13:1092-1100`）：对 MBPP、HumanEval、MMLU、MMLU-Pro，
  **即使提高阈值，8-gram 重叠给出的污染率也高到无法得出任何可用的性能增益估计，需要换方法**
  （表 15：AGIEval 污染率 98% → 70B 增益 19.9；BBH 95% → 405B 41.0；HellaSwag 85% → 14.8；GSM8K 41% → 约 0；MATH 1% → 约 0）。
- **Dolma 的教训**：段落级 Bloom filter 只删 0.003% 数据，**但事后 WIMBD 体检发现 6 个数据集 100% 污染**
  （Winograd、SICK、GLUE-AX、SemEval-2014-T1、COPA、SuperGLUE-AXb），HumanEval/WiC/ESNLI/SNLI >90%，
  **很多污染来自 code 子集**（GitHub 上常有数据集副本）（`13:1083`）。
- **infini-gram mini**：新集子会随时间被污染——**AIME-2024 在 Pile/DCLM 上干净，在 CC-2025-21 上 40% dirty；GSM8K 在 CC-2025-21 上 74.2% dirty**（`13:1090`）。
- 时间切分的实证（`13:1129-1134`）：**LiveCodeBench** 的性能陡降**只出现在 LeetCode 题上，AtCoder 题跨月份基本平稳**；
  **SWE-bench 用 repo-disjoint（不是 instance-disjoint）**，按 2023 年切分后 oracle 检索下 **GPT-4 1.96% → 0.0%**，而 Claude 2 几乎不动。
- **两条跨集通用的坑**（`13:1155-1161`）：
  ① **多数前端/文档类集子的题目本身来自公网**（CodePen、GitHub Pages、公开 PDF），
  **只拉黑 benchmark 仓库不够，必须把源 URL / pen-id / arXiv-id 一起进黑名单**——
  **这对本项目尤其致命**，因为真实素材路线正是从 CodePen / GitHub 挖的，
  所以「素材源 → benchmark」的交集必须**在抓取阶段**就查，不是训练前查。
  ② 短 prompt 集精确匹配几乎没用。
- 黑名单可行性分级（`13:1136-1153`）：**A 类（全量可下，直接拉黑）**——3JSBench 100 条（MIT）、
  ArtifactsBench 1,825（CC-BY-NC-4.0 非商用）、**BenchCAD 17,900 条执行校验过的 CadQuery 程序**、
  PRISM 10,372、Animation2Code 1,069、Design2Code / SWE-bench / BigCodeBench / HumanEval / MBPP / ChartMimic 等；
  **B 类**——WorldCoder-Bench（论文称 2,026，仓库实际 **2,004**，**差 22 条未公开**）、ManiBench（摘要称 150~200，HF 上只有 12 条 pilot）、WebBench（5,750 中开源 2,454）；
  **C 类（做不了黑名单）**——**WebCoderBench 1,572 条真实用户需求，数据集与评测代码均不发布且把不公开当防刷分手段**；
  **WebDev Arena 活体池永不公开**（288,203 票，公开 dump 仅 10,501 行）；LiveCodeBench 设计上就该走时间切分。
- **本机的三道闸**（`13:1163-1179`）：闸 1 抓取时按素材源 URL / pen-id / repo+path 黑名单；
  闸 2 造题后三路（① 50 字符子串 stride=一词，**η < 20% 判 clean**；② embedding top-k=10 + LLM 逐对判定；
  ③ **场景图 L-exact 哈希直接比**）；闸 3 发布时按 commit / pen 创建时间做时间切分。
  **第 ③ 路是相对文本/代码数据集的结构性优势**：场景图哈希比的是**产物的几何**，改写代码、换语言、换实现路径都不影响它；
  **LMSYS 证明 10-gram 对改写的 F1 = 0，但改写不可能在保持几何不变的同时绕过场景图哈希——因为几何变了就不是同一道题了。**

### B4.15 「少而硬」优于「多而杂」的直接证据

| 证据 | 数字 | 出处 |
|---|---|---|
| **GLM-4.5「宁要少而硬，不要多而杂」** | 科学域 RL 只用专家验证过的选择题，明显优于混合质量数据（§3.3.1 图 7 右） | `08:1543` |
| **Qwen3 的极简配方** | 全流程下来**只有 3,995 对 query-verifier** → 多样性控住以后，量可以非常小 | `08:629` |
| **V-GameGym** | 先对种子代码聚类再按簇采样：**2,219 题 / 100 个簇**；质量规则是「每簇设上限、对长尾簇定向补齐」 | `03:277`、`03:339` |
| **batch 才是一阶多样性旋钮** | 固定总量下 batch 512/768/2048 → **0.605 / 0.610 / 0.645**；G = 8/16/24/32 → 0.585/0.610/0.590/0.595（二阶） | `08:185-187` |
| **BugPilot** | **1.2k FeatAdd 题在 SFT 上胜过 3k 其它 bug 两个点**；RL 后 32B 52.4% / 全量 54.6% → **无意引入的 bug 比刻意注入的更像真实分布，训练效率更高** | `03:74` |
| 多样性的另一面（输入侧） | Sketch2Code 有些页面由 **2~3 人以上**分别画以覆盖风格；BlenderGym 把视角分成模型可见与评测专用，**每个目标物体至少出现在一个输入视角里**（App. S5） | `03:101`、`03:111` |

**三条可计算的多样性轴（推导，`03:339`）**：需求文本 embedding 的簇覆盖；three.js class / bpy operator 覆盖；渲染图 embedding 覆盖。
**去重与污染隔离的三个现成技巧**（`03:276`）：**时间切分**（只用模型发布之后的任务，SWE-rebench）；
**对 benchmark 做 Jaccard + Sentence-Transformer 相似度过滤**（WebGen-Instruct）；
**隐藏契约 + 参数扰动变体**（WorldCoder-Robust 的 615 个变体）。污染阈值 **0（命中即删）**（`03:340`）。

---

## B5. 成本模型：各阶段留存率、LLM 调用量、哪个参数最敏感

### B5.0 一句话结论（可直接当正文论点）

> **这件事的瓶颈不是算力**（three.js + Blender 两条线合计约 **2,500 core-h**，一台 48 核机器两天），
> **是 LLM 调用（约 100 万次）和人工（1.5 人月）。
> 而 LLM 调用里 65% 花在难度标定上——所以「难度标定要采样多少次」是整个成本模型里唯一值得反复优化的旋钮。**
> 出处 `13:1604-1607`。

### B5.1 公开构造漏斗：真实挖矿的端到端保留率是 0.2%~5%

| 管线 | 起始 | 关键步 | **总保留率** | 最终 | 出处 |
|---|---|---|---|---|---|
| **SWE-bench** | 12 仓 / 爬 **93,139 PR** | attribute filter → 11,407（12.25%）；执行校验（≥1 条 F2P）→ 2,294（占上步 20.1%） | **2.46%** | 2,294 | `13:1257`、`03:64` |
| **SWE-bench Verified** | 2,294 | 抽 1,699 条人工标注、每条 3 名标注员；判废 **68.3%** | **21.8%** | 500 | `13:1258` |
| **SWE-bench Multimodal** | **135k PR** → 1,478 候选 | 人工核实 **83.5%** 的实例图像是必要的；**69 个实例用逐像素截图测试做功能判定** | **0.46%** | 617 | `03:69` |
| **SWE-Gym** | 358 仓 → **64,689** 条 | 只留 11 个仓 + 人工配依赖 + 执行校验 | **3.77%** | 2,438（约 200 人工小时 + **10,000 CPU core-h**，镜像 **6 TB**）⚠️ 另一处记为「约 50,000 CPU 核时」（`03:70`），两值不一致，引用时取其一并标注 | `13:1259` |
| **SWE-smith** | 128 仓 → **100,074 个 bug 候选** | 执行校验（打 patch 必须打断 ≥1 条原通过测试） | **50.1%** | 50,137（约 20 人工小时、**1,360 美元**、环境存储 **295 GB**） | `13:1260`、`08:1232` |
| **SWE-rebench** | 约 10M PR → 下载约 450,000 | match 约 5% → filter 约 33% → **install & validate 约 14%** → annotate 约 100%；**只有 31% 的仓库能装成至少一个任务** | **4.74%** | 21,336 | `13:1261` |
| **Design2Code** | C4 validation **127.9k** 页 | 三步过滤 → 14k（10.9%）→ 剥依赖换占位图 → 从 7k 由前两位作者**逐条人工检查** → 484（6.9%） | **0.38%** | 484 | `13:1284` |
| **WebCode2M** | CC 一个 segment 约 **0.5B 页** | 长度过滤 → Playwright 渲染（**占总耗时约 80%、历时约 1 个月**）→ **神经打分器 score<2 剔掉 = 52.5%，保留 47.5%**（唯一公开的单步比例）→ 截图 hash 去重 | **约 0.5%** | 2,563,905 | `13:1285` |
| **ShaderMatch / ShaderEval** | **202k 未过滤函数池** | 只留「已发布到 API + 宽松许可」 | **约 0.23%** | **467** | `13:1287` |
| **WorldCoder-Bench** | 5 位 3D 图形 PhD 手工 seed（**耗时 2 个月**） | LLM 辅助扩到 **>10,000** 候选 → 人工剔歧义/过易/欠定义/无法转成确定性 runtime check → 无头浏览器验资产接口 → 专家写 behavioral contract，执行不稳的剔除 | **≲20%** | **2,026**（+615 个 Robust 变体）；SOTA 最好 Core **27.8%**（严格 19.9%） | `13:1299`、`03:185` |
| **BlenderLLM / BlendNet** | **135 条手写 seed instruction** | self-instruct 扩到约 **50k** → GPT-4o 写 bpy → 四视角渲染 → GPT-4o 判图文一致 → 人工复核 10k 条（**与 GPT-4o 一致率 89.7%，人工池通过率只有 20%**） | **约 16%** | 8k | `13:1297` |
| **CodeContests** | 原始 hidden test **12.4 条/题** | mutation 造测试，30 份正确解输出全一致才留；每题上限 10 CPU 小时或 200 条；**6.3% 的题凑不满** | 测试 **12.4 → 203.7 条/题（16.4×）**；**假阳性 62% → 4%** | train 13,328 | `13:1262` |

**其它规模锚点**：R2E-Gym **8.1K+** 任务（32B 34.4% → 混合 verifier 51.0%）`03:71`；
SWE-rebench **3,468 仓 / 21,336 任务**（自动生成安装脚本 + 三个学习出来的质量标签）`03:73`；
OpenSWE **45,320 个 Docker 环境** `08:1494`。

### B5.2 ⚠️ SWE-smith 各合成策略的 yield 差 52 倍（最该抄走的细节）

（`13:1264-1280`、`03:72`）

| 策略 | yield |
|---|---|
| Combine(file) / Combine(module) | 97.43% / 96.16%（**但只组合已验证 patch，不产生新信息**） |
| **LM Modify（让模型「造 bug」）** | **55.98%** |
| Ctrl Invert-If / Remove Assign / Procedural Rm-Funcs | 49.44% / 48.65% / 47.09% |
| **LM Rewrite（让模型「重写函数」）** | **35.04%** |
| PR Mirroring | 33.80% |
| Op Change / Op Swap | 29.86% / 22.56% |
| Class Shuffle Funcs | **1.88%** |

→ **让模型造 bug（55.98%）比让它重写函数（35.04%）高 21 个点。**
每题成本 **0~5.53 美分**（表 1）。
【本机实测】`gen_tasks.py` 走的正是「造 bug」这一路（LLM 提语义性破坏），实测 **88%~96%**——
**比 SWE-smith 高得多，因为本机 verifier 是程序化多层的，不依赖已有单测。**

### B5.3 本机漏斗：要 10 万合格任务得造 26.9 万候选

（`13:1473-1489`，留存率里只有准入①②是实测，其余外推，逐条标注）

| 阶段 | 单阶段留存 | 性质 | 累计留存 | 进入该阶段的候选数 |
|---|---|---|---|---|
| LLM 提破坏 / 采样参数 → 候选 | 1.00 | — | 1.000 | 268,700 |
| 准入① 参考解自比自过 verifier | 0.97 | **实测 ≈1.0**，留 3% 余量 | 0.970 | 268,700 |
| 准入② 破坏版必须被判挂 | 0.90 | **实测 88%~96%**，取 90% | 0.873 | 260,600 |
| 准入③ search 片段唯一 / 脚本可执行 | 0.95 | 外推 | 0.829 | 234,500 |
| 结构 + 视觉 + 文本三路去重 | 0.85 | 外推 | 0.705 | 222,800 |
| 可解性闸（题干信息量 ≥ verifier 查的字段） | 0.88 | **半实测**：本机 9 个桌子任务里 2 个因此不可解（78%），Blender 留出集 7 个里 1 个（86%） | 0.620 | 189,400 |
| **难度带筛选（去掉 n=8 全对/全错）** | **0.60** | **外推，对标 DAPO 的 dynamic sampling** | 0.372 | 166,700 |
| **合格任务** | | | **0.372** | **100,000** |

**要造约 26.9 万个候选才能收到 10 万个合格任务。**
⚠️**这个 2.7 倍放大系数是成本模型里最敏感的一项：「难度带筛选」那条 0.60 如果实际是 0.30，候选数直接翻倍。**

### B5.4 真实素材那一路的真实量级：三位数，不是五位数

（`13:1326-1341`）

```
GitHub three.js 仓库（topic:threejs stars:>10）     2,401 个仓库   【实测】
  ↓ 抽单文件自包含页面                                约 20%    【估】
  ↓ 无头浏览器能跑起来且渲出 >=1 个 mesh（L0 执行门）  约 60%    【估，锚 Objaverse-XL 的 15%】
  ↓ 能被 __THREE_DEVTOOLS__ 抓到 scene                约 95%    【半实测】
  ↓ 冻结时钟后两次渲染逐字节一致                      约 70%    【估】
  ↓ 自动造题 + 三条准入                               约 90%    【实测 88~96%】
  ↓ 去重 + 可解性闸 + 难度带                          约 45%    【估】
                                            端到端约 3.2%
```

按每仓库平均挖出 3 个可用页面估：2,401 × 3 × 3.2% ≈ **230 个任务**。
**它的价值不在产能，在多样性注入（真实 API 用法、真实视觉风格），所以配比应该按「多样性需求」定，不按产能定。**

素材池的名义规模 vs 真·可用规模（`13:1221-1232`，全部实查）：

| 素材域 | 名义池 | 真·可用池 | 收缩 |
|---|---|---|---|
| three.js 代码仓库 | `q=three.js` **89,622** / `topic:threejs` **23,983** | `topic:threejs stars:>10` **2,401** | **约 37 倍** |
| **three.js 官方 examples** | — | **610 条，1:1 带参考截图**（中位 6,137 字节；`jsm` 496 + `src` 755 = **1,251 个 API 面**） | — |
| bpy 脚本仓库 | `q=blender addon` 6,307 / `q=bpy` 1,299 | `bpy language:Python stars:>10` **56** | **约 10~100 倍** |
| CodePen | 1,000 万 pen（2016-11 官方数字，此后无更新） | 公开 dump 约 **2.5 万**，**无列举/搜索 API** | **约 400 倍** |
| ShaderToy | >52,000 | shaders21k 的 **21,083**；官方 API 镜像已 gated 下架 | 约 2.5 倍 |
| Objaverse-XL | 元数据 **10,850,997** 行 | **只有 5.5M 能被 Blender 成功导入渲染**；商用可用 CC 约 **1.9M** | 约 5.7 倍 |

**读法：610 条是种子池的天花板，不是规模池。**
⚠️ 两个抓取硬约束（实测）：GitHub **文件级 code search 必须带 token**（未认证 401），
所以「多少个 .py 含 `import bpy`」这个数**拿不到**；ShaderToy **整站对海外出口 403**。

**三条结论**（`13:1319-1324`）：
1. **真实挖矿的天花板是 2~5%，瓶颈不在筛选而在「能不能跑起来」**（SWE-rebench 自己点名 install & validate 只有约 14%、仅 31% 的仓库能装成功）。对 three.js 是好消息（浏览器环境统一），对 bpy 是坏消息。
2. **合成/变异把 yield 抬约 20 倍（2.46% → 50.1%），而本机实测 88~96%，比 SWE-smith 再高一档。**
3. **判据强度排序（从硬到软）**：shader 逐帧像素比对 > 运行时 behavioral contract（不进 prompt）> mesh/几何分析 + 沙箱执行 > 渲染截图的 VLM 打分。
   **three.js examples 的 610 组 1:1 code+screenshot 恰好只支撑最软的那一档**——要上硬判据必须自己写 contract。

### B5.5 探针次数与 CPU 账

探针总计（`13:1491-1499`）：

```
准入阶段   268,700 候选 × 3 次探针                 =   806,000 次
难度标定   166,700 候选 × 2 次（n=2 筛）            =   333,400 次
           166,700 × 45% 存活 × 6 次（补到 n=8）    =   450,000 次
                                                    ---------
                                    探针总计       ≈ 1,589,000 次
```

| 线 | 单探针 core-s | 总 CPU | 折 48 核整机 |
|---|---|---|---|
| **three.js**（复用浏览器池 14.3 任务/s） | **3.36** | **1,480 core-h** | **31 台机小时 ≈ 1.3 机日** |
| 对照：不复用浏览器（3.6 任务/s） | — | — | **5.1 机日**（复用把吞吐抬了近 4 倍） |
| **Blender**（2 核中位） | **2.41** | **1,064 core-h** | **22 台机小时 ≈ 0.9 机日** |
| Blender 1 核 / 4 核两档 | 1.21 / 4.82 | 532 / 2,128 core-h | 0.5 / 1.8 机日 |

⚠️**一个反直觉的点：Blender 比 three.js 更便宜**——Workbench 稳态渲染 0.065 s/视角，比 SwiftShader 下的 WebGL 快；
**three.js 贵在浏览器本身**（`13:1526-1529`）。
**扩产阶段应该只渲 Workbench 剪影 + 算几何，不渲 Cycles**（「几何指标比渲染便宜 3 倍、判别力还更高」）。

### B5.6 LLM 调用账：难度标定占 65%（这是最敏感的参数）

（`13:1531-1551`）

| 用途 | 次数 | 占比 |
|---|---|---|
| 破坏 / 参数提案（每场景 1 次出 16 条） | 16,800 | 1.4% |
| 题干改写 + spec.json 导出（每候选 1 次） | 268,700 | 22% |
| **难度标定 rollout（两段式 n=2 → n=8）** | **783,000** | **65%** |
| 欠规格诊断（难桶 25% × 3 次 ceiling check） | 125,000 | 10% |
| VLM 抽检（2% 任务 × 4 judge × 2 次） | 16,000 | 1.3% |
| **合计** | **≈ 1.21 M 次** | |

两个可以省钱的点：
1. **两段式筛选省掉 0.55M 次调用**：一次性 n=8 要 1.33M 次标定调用（总计 1.76M）；先 n=2 筛掉 55% 再补 6 次只要 0.78M（总计 1.21M），**省 31%**。
2. **题干改写那 22% 可以用模板省掉**：程序化路线的题干是槽位短语拼的，不需要 LLM；只有「从真实素材反推需求」那一路必须调 LLM。程序化占 70% 时这一项降到 8 万次。

**优化后约 0.95M 次 LLM 调用**，按每次 2k 输入 + 1k 输出估 ≈ **1.9B 输入 + 0.95B 输出 token**。

**判别/评分侧的单价对照**（`08:1375`、`08:1233`）：
**Web-Shepherd 3B PRM 每 1,000 个实例 4.67 美元**（A100 按 1.19 美元/时；平均 81,287 输入 / 1,953 输出 token），
而 GPT-4o-mini **43.57**、GPT-4o **435.74**、Qwen2.5-VL-72B **53.69** → **自训小 PRM 比 GPT-4o 便宜约 93 倍**。

### B5.7 去重与人工账

**去重是免费的**（`13:1553-1565`）：视觉 embedding（90 万图，DINOv2 ViT-B 约 200 图/s）**1.25 GPU 小时**；
pHash 90 万图 15 分钟；全对全余弦 **38 秒**；向量存储 307 MB（int8 后 77 MB）；MinHash+LSH 分钟级。
**到 100 万量级也只是 12.5 GPU 小时。不要因为「怕去重贵」而跳过去重——这是整条流水线里性价比最高的一步。**

**人工抽检**（`13:1567-1587`）：抽检量与置信区间（p=0.5 最坏，95% CI 半宽）——
50 条 ±13.9%、100 条 ±9.8%、200 条 ±6.9%、**384 条 ±5.0%**、1,000 条 ±3.1%。
建议口径 **12 层 × 100 条 = 1,200 条/轮**（层内 ±9.8%，全局 ±2.8%）。

| 项 | 量 | 工时 |
|---|---|---|
| 分阶段抽检 4 轮 × 1,200 条 × 3 分钟 | 4,800 条 | **240 人时** |
| verifier 逐条一致性标定（要求 ≥92%，每层 50 条） | 600 条 × 5 分钟 | **50 人时** |
| 欠规格仲裁（难桶里 ceiling check 翻面的，估 2,000 条 × 2 分钟） | 2,000 条 | **67 人时** |
| **合计** | | **≈ 360 人时 ≈ 1.5 人月** |

**公开的人工成本锚点**：
**WebGen-Bench 647 个测试用例，全人工执行约 10.8 小时 / 377.8 美元**（WebGen-Instruct 6,667 条；32B 微调后 9.5% → 38.2%）`03:157`；
**SPICE：1,000 实例的标注从约 10 万美元人工降到 5.10 美元**（约 2 万倍）`13:809-810`；
**RaR 平均每样本 7.7 条 rubric（20,166 样本 / 154,808 条）**，显式聚合 `r = Σw_j c_j / Σw_j`，人工权重 Essential 1.0 / Important 0.7 / Optional 0.3 / Pitfall 0.9 `08:503`、`03:155`；
**Verification Horizon：671 个 WebDev 任务，平均 25.9 条 / 6 个维度**（Functional 37.7% / Content 19.0% / Visual 13.3% / Layout 12.9% / UX 9.3% / Technical 7.2%）`08:505`；
ArtifactsBench 1,825 题 / 9 个领域 / 每题 10 维清单 `03:156`；
Sketch2Code：**从 723 名申请者里选 21 名标注者**，为 484 个页面画 731 张草图 `03:101`。

### B5.8 存储与总账

（`13:1589-1602`）

| 项 | three.js 线 | Blender 线 |
|---|---|---|
| CPU | 1,480 core-h（31 台机小时） | 1,064 core-h（22 台机小时） |
| GPU | 1.25 GPU 小时（去重 embedding，两线共用） | 同 |
| LLM 调用 | ≈ 0.95 M 次（优化后） | 同 |
| LLM token | ≈ 1.9 B 输入 / 0.95 B 输出 | 同 |
| 人工 | 360 人时 | 同 |
| 存储 | 单任务约 0.2 MB（源码 5 KB + 9 视角 JPEG 约 135 KB + 体素约 50 KB）⇒ **10 万任务约 20 GB** | 单任务约 1 MB（ref.py 4 KB + state.json 30 KB + 10 视角 PNG 约 300 KB + points.npz 约 700 KB）⇒ **约 100 GB**；`.blend` 不存（由 ref.py 确定性重建） |

**环境体积的公开对照**（`08:1117-1119`）：**SWE-smith 按仓库共享环境只要 295 GB**，
而 **SWE-Gym 6 TB**、**R2E-Gym Subset 4 TB**——**20 倍压缩**。

### B5.9 训练侧的轨迹留存率（蒸馏那一端的成本）

| 证据 | 数字 | 出处 |
|---|---|---|
| **SWE-smith 轨迹留存（实测）** | 8,686 个任务、**17,906 次尝试、6,457 次成功（36%）**，每题最多留 3 条 → **最终 5,016 条**（约占原始尝试的 28%） | `08:1495`、`05:143` |
| **每题留几条（SWE-Gym 的 per-instance capping）** | 留 1 → **9.0%**；留 2 → **9.7%**；留 3 → 7.7%；不设上限 → 9.3% | `08:1496-1497` |
| 读法 | **每题取 2~3 条、优先短轨迹**；同一题内偏好更少轮数 | 同上 |
| **⚠️「难度不决定训练价值」** | SWE-smith 按难度分 4 桶各 500 条，训后 SWE-Verified **12.4 / 10.8 / 13.6 / 12.2，无单调性** → **拒绝采样阶段不要按难度挑，难度只在 S3 课程里用** | `08:1498-1499` |
| SWE-Gym 拒绝采样终点 | **491 条轨迹**（32B SFT），平均约 19 轮 / 约 19,000 token；SWE-bench Lite **3.0% → 15.3%**，Verified **7.0% → 20.6%** | `05:120`、`05:132` |
| ⚠️ SWE-Gym 在线自提升失败 | **868 条 on-policy + 491 条 off-policy 把 SWE-bench Lite 从 15.3% 拉到 8.7%** | `05:134` |
| SWE-Gym verifier 训练数据 | 只留 ≤32k token 的轨迹，**1,318 成功 + 1,318 失败 = 2,636** | `05:135` |
| R2E-Gym | 8.1K 任务 → 去污后 **4,578 题 / 10 个仓**（附录写 4,538）→ **3,321 条轨迹**（32B），Verified Pass@1 34.4% | `05:161` |
| **SWE-Master 的数据曲线** | 0 → 60K 轨迹让 resolve **6.2% → 57.8%，48K 之后趋平**；模型同时变短（平均轮数 115→94，思考 token 14.8k→12.7k） | `08:1479` |
| 本机 S2 预测（推导） | 3K~5K 任务 × N=8~16 → 留存 **10%~35%** → **5K~20K 条高质量轨迹**；**< 5% 说明太难（先加 SFT），> 60% 说明太易（没有 RL 信号）** | `08:1489` |
| 本机 S3 池（推导） | 3K~8K 题，**0 < p < 0.9** | `08:1490` |

### B5.10 一轮 RL 的开销与「蒸馏 vs RL」的算力对照

| 项 | 数字 | 出处 |
|---|---|---|
| 本机一轮 RL（推算） | **约 12,800 GPU 小时**（204,800 条轨迹；64 张 rollout 卡 + 64 张训练卡 × 100 小时） | `08:1021`、`08:1207-1218` |
| 同量级对照 | Qwen3-8B 纯 RL **17,920 GPU 小时** | `92:33` |
| 上限对照 | MiniMax-M1：**512 × H800 × 3 周 ≈ 258,000 GPU 小时 / 534,700 美元** | `08:1224` |
| ⚠️ 口径 | 本机这一条是**推算**，文件自己标为未核实（`08:1833`） | `08:1235-1238` |
| **蒸馏侧对照（最硬的一条）** | **on-policy 蒸馏 1,800 GPU 小时 → 74.4，RL 17,920 小时 → 67.6**；**1/10 算力、全面更好**，且「RL 完全没有提升 pass@64」 | `92:33`、`08:1244-1249` |
| 轻量压缩侧 | **WebClipper：抽取 + 改写在 8×H800 上一天内跑完**；输出 token −19.4%、轮数 −21%、准确率不变 | `05:57`、`05:61` |
| 上下文压缩侧 | **AgentDiet：处理过的步骤内删掉 69.2~77.4% 内容；累计输入 token −39.9~59.7%；总成本 −21.1~35.9%**，通过率还升（SWE-bench Verified + Claude 64.5 → 66.5） | `05:82-83` |
| ⚠️ 反例 | **AttnCompress：输入 token 1,118.16k → 644.66k（−42.3%），单题成本 0.1189 → 0.0949 美元，但通过率 53.17% < 未压缩 55.17%** | `05:93-95` |
| **算力该花在哪（BlenderGym VeriRatio）** | 总查询 < 30 时验证占比 **0.33** 最好；> 100 时 **0.73** 最好；**每 100 次查询约 0.45 美元** → **算力少就多生成候选，算力多就花在验证上** | `05:806-808`、`12:82` |
| 参照 | SCoRe 推理侧：每题 32 个样本时，纯并行采样 +7.4%，并行 + 一轮自我纠正 **+10.5%** | `05:269` |

### B5.11 哪个参数最敏感：三个候选与排序

| 排名 | 参数 | 为什么敏感 | 量化 |
|---|---|---|---|
| **1** | **难度标定的采样次数 n** | 它既占 LLM 调用的 **65%**，又决定难度带留存率那条 **0.60** | n=8 一次性比两段式贵 **0.55M 次调用（+31%）**；而 n=64 要 10.7M 次（**13.7 倍**）却只把边界桶误分率从 29% 降到 22.5% |
| **2** | **难度带筛选的留存率**（模型里取 0.60） | 候选总数 = 10 万 / 累计留存，这一条直接按比例放大上游**全部**成本 | **Skywork-OR1 实测开训前就有 54%（7B）/ 63%（32B）零梯度题** → 实际可能只有 **0.2~0.4**，候选数要再翻 **1.5~3 倍**（`13:40-50`、`13:911`、`13:1487-1489`） |
| **3** | **浏览器池是否复用** | 只影响 CPU（本来就不是瓶颈），但 4 倍差距 | 14.3 vs 3.6 任务/s → 1.3 机日 vs 5.1 机日 |

**所以最该先做的小规模实验是「我们的任务分布里零梯度题占多少」**——
它同时钉死 (1) 和 (2)，而且只需要几百道题 × n=8 就能测出来。
`13:40-50` 原话：**「这是整个成本模型里最该先用小规模实验钉死的一项。」**

---

## B·量化数字清单

> 一行一个数字 → 它能证明什么 → 出处（`文件:行`）。
> 口径列：实测 = 本机实测；公开 = 公开论文/榜单；推导 = 本机算术或外推；已更正 = 按 `92_number_audit.md` 改过。

### 难度带筛选：p 怎么估、采几次、留存多少

| 数字 | 能证明什么 | 出处 | 口径 |
|---|---|---|---|
| **Wald 口径下 n=4、p=0.5 时 95% CI 全宽 0.98** | **n=4 标难度等于没标** | `13_scaling_tasks.md:377-397` | 推导（本机算） |
| 达到 95% CI 半宽 0.10 需 **n=96**；半宽 0.05 需 **n=385** | 连续难度分的真实代价 | `13_scaling_tasks.md:399-404` | 推导 |
| 三档桶误分率：p=0.35/0.65 在 n=64 时仍 **22.5%**，p=0.25/0.75 仍 **15.6%**，且几乎不随 n 下降 | **硬边界难度桶在数学上做不到，只能用软权重/重叠桶** | `13_scaling_tasks.md:417-430` | 推导（精确枚举） |
| 难度集合的 Jaccard 复现性：n=8 **0.632**、n=16 **0.727**、n=128 **0.876** | 「n 要多大」最直接的公开答案 | `13_scaling_tasks.md:434-444` | 公开 |
| 「跨训练种子的难度差异」里 **81% 其实只是采样噪声**（同 checkpoint 重采 Jaccard 0.798 vs 独立种子 0.751） | 别把采样噪声当模型差异 | `13_scaling_tasks.md:446-448` | 公开 |
| 同预算下深采一次 **0.8770** vs 拆 4×32 取交集 **0.7906**（差 +0.0864） | 不要拆块取交集 | `13_scaling_tasks.md:448-449` | 公开 |
| **Skywork-OR1：开训前就有 54%（7B）/ 63%（32B）的题是全对或全错** | **「训练前全对/全错占比」最硬的公开数字** | `13_scaling_tasks.md:553` | 公开 |
| GRESO：Qwen2.5-Math-7B 做 GRPO，**有效 prompt 后期只剩约 20%**；零方差占 80% 时 DAPO 需约 **5 倍** rollout | 动态采样的真实代价 | `13_scaling_tasks.md:551` | 公开 |
| SRPO：**接近 50% 的组 reward 完全相同（优势为 0）** | 零梯度不是边缘现象 | `08_rl_recipe.md:195`；`13:552` | 公开 |
| Open-R1 子集 + Qwen2.5-Math-1.5B：**n=4 时 35.3% 的组全对，n=256 时降到 10.2%** | 全对比例是采样预算的函数 | `08_rl_recipe.md:18`、`:199` | 公开 |
| 同一模型 **pass@1 = 26.5% 而 pass@256 = 81.3%** | **「signal collapse 是欠采样的统计假象，不是模型上限」** | `08_rl_recipe.md:198-199` | 公开 |
| 理论对照：pass rate 服从 U(0,1) 时 G=16 的过采样倍数只要 **1.13×**，实测要 **5×** | **量化了「题库 pass rate 极度堆在两端」** | `13_scaling_tasks.md:556-565` | 推导 + 公开 |
| 阈值扫描：plain GRPO **26.3** → (0,1) **27.3（+1.0）** → (0.3,0.7) **30.1（+3.8）** → (0.4,0.6) 回落 **29.9** | **只剔全对全错只值 +1.0pp，收到中段多拿 +2.8pp，过紧有代价** | `13_scaling_tasks.md:586-604` | 公开 |
| 单边切（Skewed）全部 **23.8~25.9 < plain GRPO 的 26.3** | **必须对称切** | `13_scaling_tasks.md:591-596` | 公开 |
| 7B 扩展：SFT 37.3 → plain 39.6 → (0,1) 39.9 → **(0.3,0.7) 41.8** | 结论可跨尺寸 | `13_scaling_tasks.md:612` | 公开 |
| **Polaris：40K 全量受阻 → 去掉全部 8/8 的 26K 最优 → 只留 ≤4/8 的 19K 变差** | **过滤过头反而更差**（最干净的反证） | `13_scaling_tasks.md:624-630` | 公开 |
| AdaRFT 的 "PPO (w/ Filter)" 离线过滤：**六个设置无一打过 AdaRFT，4/6 比普通 PPO 还慢** | **离线难度过滤可能是负收益** | `13_scaling_tasks.md:620` | 公开 |
| SWE-Master：**不做难度过滤 54.2% → 做了 57.8%（+3.6）** | 难度带筛选本身的价值参考值 | `08_rl_recipe.md:630`；`05_trajectory_repair.md:184-186` | 公开 |
| MiniMax-M1：**pass@10 只留 0 < p < 0.9** → 数学约 50K / 代码约 30K / 逻辑约 53K | 上界不是 1 而是 0.9 | `08_rl_recipe.md:625` | 公开 |
| WebClipper：**每题跑 4 次，只留 0 < p < 0.5** | 第二个独立的双边过滤数据点，上界更低 | `05_trajectory_repair.md:61` | 公开 |
| Boundary-Aware 桶漂移：**第一轮 RL 就把 Easy 从 24 冲到 650（27 倍）**，之后 650→697→736 | **静态课程失效极快，重新估 p 的边际价值绝大部分在第一遍** | `08_rl_recipe.md:577-585` | 公开 |
| 带课程的 RL：pass@256 比 base **+9.8pp**、比 vanilla RLVR **+10.3pp**；**538 道 base 解不出的题里 226 道变可解** | 课程能扩能力边界 | `08_rl_recipe.md:568-573`、`:1257` | 公开 |
| ⚠️**vanilla RLVR 的 pass@256 平均低于 base**：AIME24 40.0 → 26.7 → 52.2；MATH500 73.6 → 55.4 → 88.0 | **没有课程的 RL 在缩小能力边界** | `08_rl_recipe.md:568-573` | 公开 |
| ExGRPO：把退役的全对题放回去，in-dist **48.4 → 45.3（−3.1）** | 退役全对题是对的 | `08_rl_recipe.md:609-617` | 公开 |
| Reinforce-Ada 表 5：**DAPO 在 Easy 桶上比 base 低 5.70 分（0.5580 vs 0.6151）**，而 GRPO +7.14、Reinforce-Ada +10.02 | **但不能整类砍掉易档**——动态采样代价的唯一硬数字 | `08_rl_recipe.md:591-599` | 公开 |
| ExGRPO 回放比例：50%→48.3、25%→46.4、**75%→44.8（低于纯 on-policy 基线）** | 回放过量会倒退 | `08_rl_recipe.md:611-612` | 公开 |
| Reinforce-Ada 自适应组：**反传组只有 n=4，加权平均 47.6 > GRPO-n16 的 47.3，收敛快 2 倍** | 自适应采样优于固定大组 | `08_rl_recipe.md:208` | 公开 |
| SRPO History Resampling：AIME24 40.5→44.3、LCB 35.1→38.7，步数约 R1-Zero 的 **1/10** | epoch 级「丢全对留全错」更便宜 | `08_rl_recipe.md:209` | 公开 |
| ScaleRL：固定总量下 **batch 512/768/2048 → 0.605/0.610/0.645**；**G=8/16/24/32 → 0.585/0.610/0.590/0.595** | **batch 是一阶旋钮，G 是二阶** | `08_rl_recipe.md:183-188` | 公开 |
| GRESO：**省 2.0~2.4× 端到端时间**，精度持平（7B 57.5 vs 57.8），rollout 13.1M → 6.3M | rollout 前预测优于过采样 | `13_scaling_tasks.md:638` | 公开 |
| GRESO 时序：**>90%** 的当期零方差 prompt 在更早 epoch 也零方差，但**约 20%** 的历史零方差会重新变 effective | **不能静态永久剪枝，必须留约 20% 探索** | `13_scaling_tasks.md:643-646` | 公开 |
| ⚠️ **`08_rl_recipe.md:194` 写「组大小 8、p=0.1 时全零概率 0.9^8 ≈ 19%」是算术错；正确是 43.05%，19% 对应组大小 16** | 引用要用 `:201` 的「G=8 时约 43%~66% 的组全 0」 | `08_rl_recipe.md:194` vs `:201`；`92_number_audit.md:83` | **已更正** |
| 本机难度估计单价：静态 pass@256 × 3 种子 = 256×3×24.7 core-s ≈ **5.3 核时/题** | **本机绝不能离线跑 pass@256**，必须用在线正确率或 DPR | `08_rl_recipe.md:637-638` | 推导（基于实测 24.7 core-s） |
| ⚠️ DAPO 四件套累加：30 → +超长过滤 **36** → +Clip-Higher 38 → +软惩罚 41 → +token 级 loss 42 → **+动态采样 50**；**样本选择占 20 分里的 14 分** | 样本选择是 RL 配方里最大的单项 | `08_rl_recipe.md:148-159`；`13:533-543` | 公开（**分项未核实**，`92:90-91`） |
| ⚠️ **DAPO 的 rollout 放大倍数不在论文里**（只有图 6 的定性说法） | **不要引用倍数** | `08_rl_recipe.md:144`、`:1829` | 未核实 |

### 「reward 低先叫教师还是先查题」：正反证据

| 数字 | 能证明什么 | 出处 | 口径 |
|---|---|---|---|
| **Qwen3 表 21：RL 17,920 GPU 小时 → AIME24 67.6；on-policy 蒸馏 1,800 小时 → 74.4**（AIME25 55.5→65.5，LCB 52.9→60.3），论文还说「RL 完全没有提升 pass@64」 | **有更强教师时优先蒸馏（算力差 10 倍）** | `08_rl_recipe.md:1244-1249`；`92_number_audit.md:33` | 公开（已核验） |
| GLM-5 难度过滤：保留「GLM-4.7 极少答对，**但 GPT-5.2 xhigh / Gemini 3 Pro 仍可解**」的题 | **低 reward 本身不是丢弃标准，「教师也解不出」才是** | `08_rl_recipe.md:624` | 公开 |
| GLM-4.5 阶段二：只要 **pass@8 = 0 且 pass@512 > 0** 的题（必须来自有已验证答案的池子） | 「极难但可解」才有价值 | `08_rl_recipe.md:623`、`:1539` | 公开 |
| Boundary-Aware：Beyond 档取边界各 10 道，**做教师轨迹 SFT 桥接再 RL** | 教师介入的具体形态 | `08_rl_recipe.md:565` | 公开 |
| ⚠️ **两份文件里没有任何「对低 reward 题跑教师 rollout」的成本/命中率/ROI 数字** | **这个命题只有间接证据，正文必须标为推断** | `08_rl_recipe.md`、`03_verifiable_construction.md` 全文 | 未找到 |
| **CLEANER：rollout 占 RL 运行时间的 80% 以上** | **「额外加教师 rollout」最硬的成本反对意见** | `05_trajectory_repair.md:291` | 公开 |
| **R2E-Gym：大多数任务里能区分正确/错误补丁的测试不到 20%**；被污染的测试最多 10% | **低 reward 可能是判别力不足** | `03_verifiable_construction.md:71`、`:89`；`05:174` | 公开 |
| **单 verifier 天花板：EB 43.7% / EF 42.8%（Best@26）vs Pass@26 64.4%** | **约 20pp 的能力被 verifier 判别力吃掉，不是模型不行** | `05_trajectory_repair.md:162-163` | 公开 |
| R2E-Gym EF 消融：patch+完整轨迹 71.82 / Best@26 42.8；只给 patch 68.01 / 37.6 | **这类 verifier 严重依赖 agent 自己说「我修好了」** | `05_trajectory_repair.md:164-172` | 公开 |
| **AgentPRM：PRM 被玩坏后成功率 82% → 70%，而验证集上的过程 reward 还在涨** | **「reward 低/高」可以完全是被 hack 的 verifier 的产物，常规监控发现不了** | `05_trajectory_repair.md:570-571` | 公开 |
| **Repair or Resample：54 条原本成功的执行各重跑 3 次 → 162 次里 85 次失败；54 条里 39 条至少退化一次——而温度是 0** | **「这条轨迹失败了」在 72%（39/54）的情况下只是重跑抖动** | `05_trajectory_repair.md:483-484` | 公开 |
| **Real-Time Repair：纯「回滚 + 重采样」自己就能救回 16%**（带定位反馈那臂 45%） | **任何「修复/蒸馏有效」都要先减掉这 16% 的基线** | `05_trajectory_repair.md:408`、`:28` | 公开 |
| Repair or Resample：Self-Reflection 4.29 / Critic-Agent 3.73 / Last-Node 1.31 **全部低于无引导整条重跑的 6.90**；只有 Suspicious-Node 到 20.15 | **带反馈的方法可能比盲目重跑更差** | `05_trajectory_repair.md:471-482` | 公开 |
| SymTrace：Rerun → Replay 让 rep1 **67.97% → 80.78%**、rep3 **41.42% → 52.43%**；复用 ≥9 个前缀节点时优势 **+25.69** | **没有固定前缀连复现同一个失败都做不到，归因无从谈起** | `05_trajectory_repair.md:468-469` | 公开 |
| Real-Time Repair 失败分型：**只有 goal_drift 能靠重试修好（4/5）**；tool_cascade 和 looping 只会复现同一个坏结果 | **低 reward 必须先分型，「教师介不介入」按类型翻转** | `05_trajectory_repair.md:420-421` | 公开 |
| **SWE-Master：RL 早期约 20% 的轨迹被预算耗尽截断，其中 24.3% 其实已经解决了问题** | **预算耗尽必须给 partial credit（reward × α=0.5），不能当失败** | `08_rl_recipe.md:524`、`:1049-1050` | 公开 |
| ⚠️ DeepSWE 把预算耗尽当环境故障（reward 0 + mask loss），SWE-Master 复现后 **reward 持续下降直到训练崩溃** | 归因错了会直接崩 | `08_rl_recipe.md:526`、`:1052-1057` | 公开 |
| **Spurious Rewards：随机 reward +21.4、格式 reward +13.8、错标签 +24.1、1-shot +26.0、多数投票 +27.1，而真 ground-truth 也只有 +29.1** | **没有空白基线的 proxy 增益不说明任何事** | `08_rl_recipe.md:544` | 公开 |
| Verification Horizon 负例权重：w_neg **0.0 → 37.2% / 0.5 → 35.1% / 1.0 → 41.8% / 0.8 → 44.4%**（非单调） | **别删负例也别归零；0.8 是唯一超基线的一档** | `05_trajectory_repair.md:16`；`92_number_audit.md:41` | 公开（已核验） |
| Span-KTO：把负例当偏好推开，SWE-bench Verified **54.2% → 59.8%** | 负例的正确用法 | `05_trajectory_repair.md:16` | 公开 |
| **Agent-R：只用最优轨迹训出的修订能力 10.84，带纠错轨迹 46.75**；Direct-Revision 35.67 | **纯净轨迹训不出恢复能力；早截断优于只在末尾纠错** | `05_trajectory_repair.md:216-222`；`92:42` | 公开（已核验） |
| AgentRefine：去掉试错后 held-in 微涨（48.5→49.3）而 **held-out 大跌（PDDL 21.7→11.7，Jericho 5.0→0.0）** | 试错数据的价值全在泛化上 | `05_trajectory_repair.md:230-241` | 公开 |
| ⚠️ AgentHER：**同量失败数据不改写目标直接 SFT，WebArena 14.7 / ToolBench 54.8，低于只用成功的 18.9 / 61.2** | **失败轨迹必须改写目标后才有正收益** | `05_trajectory_repair.md:31-33` | 公开 |
| **ReTerm：教师从失败状态继续 → ReTerm-9B 在训练 harness 上 +14.6pp，换 harness 仍 +6.7~12.4pp** | **错误必须来自策略自己**（作者点名手工注入的错误分布不匹配） | `05_trajectory_repair.md:293-308` | 公开 |
| SCoRe：base Δ(t1,t2) **−11.2**；STaR +0.4；Pair-SFT +1.8；**SCoRe +4.4（Δ 改善 15.6pp）**；HumanEval SCoRe Δ **+12.2** vs base +3.0 | **离线修正轨迹 SFT 学不出自我纠错** | `05_trajectory_repair.md:252-262`；`12:412-425` | 公开 |
| Pair-SFT D_SFT+ 的 **Δ / 错→对 / 对→错 = 0% / 0% / 0%** | 离线纠错 SFT 的自然收敛点是「不碰第二次」 | `12_self_verification.md:418-422` | 公开 |
| ⚠️ **配比没人系统扫过**：CLEANER 70/30、PALADIN 80/20、w_neg 0.8、ReTerm 8+2 各自任意 | **70/30 只能当超参起点**，正文必须标推断 | `05_trajectory_repair.md:372-380` | 推断 |

### 「题目坏了」怎么判：响应模式统计 vs 人工标注

| 数字 | 能证明什么 | 出处 | 口径 |
|---|---|---|---|
| **「这题欠规约吗」人际一致性 Krippendorff α = 0.24**（test adequacy 0.41）；**对照「这题多难」Fleiss κ = 0.78** | **判坏题的人工一致性比判难度低一个量级** | `13_scaling_tasks.md:804-808` | 公开 |
| 同 rubric 独立复刻：**7 名 SE 研究者 / 7 周 / 840 实例 / 约 882 人时，α 始终 ≤ 0.67 的可信阈值（实测 0.0~0.4）**，还要加 25% 的裁决开销 | 人工路线又贵又不收敛 | `13_scaling_tasks.md:806` | 公开 |
| **item-total（tetrachoric）相关：1,000 题的 benchmark 1 分钟跑完，每集只 flag 50 题，precision@50 最高 84%** | **响应模式统计是坏题这道闸的首选** | `13_scaling_tasks.md:855-868` | 公开 |
| 同法在 GSM8K 上，**在 Platinum 已修订的基础上又找出 16 条此前未发现的无效题** | 它和人工复核是互补的 | `13_scaling_tasks.md:867` | 公开 |
| r_pb 阈值惯例：**≥0.30 良好 / 0.20~0.29 勉强 / <0.20 需修订 / ≤0 红旗（答案键可能写错）** | 可直接抄的判据 | `13_scaling_tasks.md:870-876` | 公开 |
| ⚠️ **区分度在极易/极难题上会被天然压低**（`I = a²P(1−P)`），不能脱离难度孤立判读 r_pb | 避免误杀难题 | `13_scaling_tasks.md:877-878` | 公开 |
| EduArt：871 题 / 12 模型，**831/871 可算区分度，40 条零方差无法定义**；平均 r_pb 0.514；**True/false 题型 83 条平均只有 0.245** | **题型本身就是坏题源** | `13_scaling_tasks.md:880-884` | 公开 |
| **IRT 判据分工：b_i 高 = 难（要的）；a_i ≤ 0 = 坏（标注错误）；4PL 的 feasibility 低 = 欠规约** | **「难」与「坏」的可操作分离** | `13_scaling_tasks.md:826-843` | 公开 |
| 零方差题占全数据 **4%**，29 个数据集中 13 个至少含一条；**NewsQA 约 16%** 的样本被所有模型答错 | 零方差题的真实比例 | `13_scaling_tasks.md:842` | 公开 |
| tinyBenchmarks：**每 scenario 100 题即可把性能估计误差压到约 2%**（MMLU 14k → 100，140 倍降本） | IRT 的降本量级 | `13_scaling_tasks.md:847-849` | 公开 |
| metabench：28,632 题 → **858 题（< 3%）**，重建总分 RMSE **0.58%**，Spearman r **0.998** | 同上，更极端 | `13_scaling_tasks.md:850-851` | 公开 |
| **SPICE：LLM 替代人工，1,000 实例从约 10 万美元降到 5.10 美元（约 2 万倍）；ICA 准确率 87.3%（人工复评 93.5% 正确），TCA 68.5%（人工复评仅 60%）** | **题干清晰度可以交给 LLM，测试充分性不行** | `13_scaling_tasks.md:809-810` | 公开 |
| **Platinum 表 4：「模型错误里有多少其实是 benchmark 的错」从 0% 横跨到 93%**（SingleEq 93% / HotpotQA 91% / SQuAD2.0 82% / GSM8K 48% / MMLU HS Math 5% / Navigate 0%） | **同一批模型、同一 pipeline 下「难」与「坏」可被量化分离的最直接证据** | `13_scaling_tasks.md:775-788` | 公开 |
| Platinum 的筛法：**只人工复核「至少有一个模型答错」的题**；gold 错 → 模型普遍与 gold 不一致；题坏 → 模型互相不一致 | **最低成本的坏题筛法，可直接抄** | `13_scaling_tasks.md:763-772` | 公开 |
| **SWE-bench Verified 人工筛查：93 名开发者 / 1,699 条抽样 / 欠规约 38.3% / 单测误杀 61.1% / 合计筛掉 68.3%**；同 scaffold 下 GPT-4o **16% → 33.2%** | 坏题占比的量级 + 清洗的效果 | `13_scaling_tasks.md:691-706` | 公开 |
| **OpenAI 2026-02 停用 SWE-bench Verified：审计 138 条里「测试会拒掉功能正确解」至少 59.4%**（强制实现细节 35.5% / 检查题面没要求的 18.8%） | **连「已清洗」的集子也有一半以上是坏题** | `13_scaling_tasks.md:709-718` | 公开 |
| **OpenAI 2026-07 推翻 SWE-bench Pro：Codex+人类定论 200 条（27.4%）缺陷，5 名资深开发者独立评审 249 条（34.1%），两条流水线一致率 74%** | 两套独立流程的一致率上限 | `13_scaling_tasks.md:720-730` | 公开 |
| SWE-Bench+：251 条「判通过」补丁里 **答案直接写在 issue 的 82 条（32.67%）**、可疑修复 **160 条（63.75%）**；滤掉后 **12.47% → 3.97%** | 泄题的量级 | `13_scaling_tasks.md:741-754` | 公开 |
| 同上：**Lite 泄题 18 条（33.33%）、Verified 37 条（33.04%）**；解决率 **Verified 22.4% → 10.0%** | **「已清洗」不等于干净** | `13_scaling_tasks.md:755-757` | 公开 |
| UTBoost：**36 条任务测试不足，345 个补丁被错判为 pass，影响 Lite 榜 40.9% / Verified 24.4%**，造成 18 和 11 处名次变动 | verifier 太松的反向 ceiling | `13_scaling_tasks.md:757-758` | 公开 |
| 【本机】cup-wood-color / legs-centered 两道题因 verifier 查了题面没钉死的字段而不可解（**2/9 = 22%**） | **「OpenAI 在 500 题上栽的和我们在 9 题上栽的是同一个错误，比例也接近」** | `13_scaling_tasks.md:732-736` | 实测 |
| ceiling check 的 oracle 注入锚点：SWE-bench 表 20 **Claude 2 BM25 2.27% → oracle 4.01%**；SWE-Llama 13b **0.70% → 4.54%**（2~6 倍跳升） | **之前的失败很大一部分是「信息没给到」** | `13_scaling_tasks.md:796` | 公开 |
| Ambig-SWE：模型**分不清** well-specified 与 under-specified，但允许提问后性能**最高 +74%** | 欠规约的代价 | `13_scaling_tasks.md:798` | 公开 |
| LLM 默认能猜中未写明需求的比例 **41.1%**；欠规约 prompt 换模型/换 prompt 的**回归概率是 2 倍** | 欠规约会放大方差 | `13_scaling_tasks.md:799` | 公开 |
| 人类 ceiling：**BigCodeBench 32/33 = 97%** | 低于此阈值的题 = 测试过严或题面欠规约 | `13_scaling_tasks.md:794` | 公开 |
| 本机 ceiling check 口径：**把参考 9 视角渲染图加进题面，通过率跳升 ≥ 0.3 判为欠规约** | 可运行的闸 | `13_scaling_tasks.md:888` | 推导 |
| **GameDevBench：41 道 agent 自动出的题，43% 没问题 / 50% 有小问题 / 7% 有大问题**；门禁定「大问题 ≤ 5%」 | **自动出题的题坏率最直接的公开数字** | `03_verifiable_construction.md:188`、`:275`、`:337` | 公开 |
| **WorldBench 特征删除变异：只读代码的 judge 在 5 个被删特征里 4 个给满分**；换 judge 后被删特征保留分 **5.44 → 3.55**（满分 7.11） | 只读代码的 judge 判不出「没画出来」 | `03_verifiable_construction.md:186`；`92:24` | 公开（已核验） |
| 同上：渲染 VLM 与代码 LM 在 **32%** 的必查项上不一致，主因「代码写了但没有一帧画出来」 | 两种信号必须都要 | `03_verifiable_construction.md:168` | 公开 |
| **WorldCoder-Bench 假阳率：只读 DOM 33.7% / 截图+VLM 3.2% / 八步 agent 45.6%**；τ_b **−0.021 / −0.068 / +0.111** | **判定方式决定一切** | `92_number_audit.md:50-55` | 公开（已核验） |
| 【已更正】**2.7% 是「截图+VLM」这个判定方式的通过率，不是模型能力**；模型隐藏契约覆盖率 **27.8%**（严格 19.9%） | 数字归属比数字本身更容易错 | `92_number_audit.md:57-59`、`:82` | **已更正** |
| **AgentDebug 定位准确率：整条轨迹级 All-Correct 24.3%（最强 baseline 0.3%），步级 45.0%（vs 28.0%）** | **自动标「哪一步坏了」与人工一致性的天花板** | `05_trajectory_repair.md:391-392` | 公开 |
| ⚠️ 同上：**GPT-4.1 做检测器 All-Correct 32.0，其它模型全部只有 2.0** | 检测器极度依赖底座 | `05_trajectory_repair.md:394` | 公开 |
| SymFail：**失败节点类型 Fleiss κ = 0.81，主类别只有 0.62**（536 条手标） | **「哪一步」比「哪一类」好标得多** | `05_trajectory_repair.md:467` | 公开 |
| BlenderGym 成对选择：**人与人 0.79 / Claude-3.5-Sonnet 0.66 / 随机 0.50**（7,950 次判断 / 50 人） | **人人一致性 0.79 就是 verifier 的天花板** | `12_self_verification.md:79` | 公开 |
| ⚠️ AesCoder 反向案例：**GPT 与人一致 80.9%，而人与人只有 68.7%** | 有些任务上人类基线本身不稳 | `05_trajectory_repair.md:817` | 公开 |
| AgentHER：**κ=0.82**，改写精度 **97.7%（127/130）**；**置信度过滤把自动改写的标签噪声从 14.8% 压到 2.3%，换来 +4.1pp** | 自动标注 + 过滤的可行性 | `05_trajectory_repair.md:320-322` | 公开 |
| ArtifactsBench：**排名一致 94.4%，与人类专家两两一致最高 90.95%**；judge 只给代码 79.06 / 加图注 81.74 / 给真图 90.95 / 只给图 74.94 | **「截图 + 逐项清单」已能复现 94% 的人类偏好排名** | `12_self_verification.md:206-210`；`92:44` | 公开（已核验） |
| Verification Horizon 静态 rubric judge vs 人：**Spearman 0.905 / Kendall 0.786**；同族 τ=1.0、跨族 τ ≥ 0.93 | rubric judge 的排名可信、绝对分不可信 | `05_trajectory_repair.md:893-894` | 公开 |
| VAGEN（以人工为 GT）：**Acc 92.9 / F1 94.6**；CUARewardBench 整体 **81.3**，而 **CUAStepBench F1 只有 39.9** | 轨迹级可判，步级不可判 | `05_trajectory_repair.md:634-636`、`:615-616` | 公开 |
| 【本机实测】**`ok_lathe` 金标签错了**：人工标 pass，而多视角下 4 个 judge 的 8 次判断 **7 次判 fail**，查顶视图确认 LatheGeometry 没封极点 | **人工金标签也会错，而且错得很隐蔽** | `12_self_verification.md:620-631` | 实测 |
| 同上：**三个「权威」判据全漏了**——人工标 pass、单视角像素分 **1.000**、多视角剪影 IoU **0.998/0.997**、按色体素 **0.995/1.000** | **结构性盲区：洞在内部，不改变外轮廓** | `12_self_verification.md:632-646` | 实测 |
| 同上：剔掉它后单视角特异度 52/54 = **0.963**，多视角 56/56 = **1.000**（原值 0.968 / 0.891） | **一个坏金标签足以把结论推成完全相反** | `12_self_verification.md:648-656` | 实测 |
| 【本机实测】**`nose_back` 单条件判定 8/8 全对，但 0/8 的理由提到朝向**；多条件判定只 5/8 而**诊断 7/8 正确** | **训练数据必须按诊断正确性打标，不能按判定正确性打标** | `12_self_verification.md:604-617`、`:908` | 实测 |
| 【本机实测】**豁免条款滥用：该挂却放过的样本里，单条件 4/8（50%）、多条件 4/6（67%）明确援引取景/透视/朝向豁免** | **「一个把真错误解释成允许差异的模型，和一个看不见这个错误的模型，产物完全一样」** | `12_self_verification.md:289-307`、`:660-666` | 实测 |
| 【本机实测】程序化判据在同样样本上稳定判 fail：按色体素 IoU 对 `body_r_+20%` **0.679**、对 `mid_r_-20%` **0.897**（VLM 只 4/7 和 8/8） | **凡是能被透视/取景解释掉的判据，一律不要交给 VLM** | `12_self_verification.md:668-671` | 实测 |
| 【本机实测】snowman 13 变异检出：**页面截图 5/13 / 多视角 9/13 / 按色体素 11/13 / 组合 13/13**；stage-0 门禁 **≥12/13** | **变异测试是判「verifier 查少了」的主路线** | `08_rl_recipe.md:1442`、`:1809-1813` | 实测 |
| WorldBench 未改动的题单次重跑仍 **7/32 翻面**；门禁 **flaky ≤ 1%** | 先修确定性再谈判别力 | `08_rl_recipe.md:1563`；`03:335` | 公开 + 推导 |
| **环境失败率门禁：正常 < 2%，> 5% 必须停下修基础设施** | **组基线被 0 分污染 = 用基础设施噪声给坏答案发奖** | `08_rl_recipe.md:1562`、`:1071-1074` | 推导（机制有公开依据） |
| 行为监控：**Hack Rate 37.76% → 1.31%，Clean Resolved 40.22 → 60.53（+20.31）**；SWE-bench Verified hack 率 **51.49 → 2.13** | **不监控时 verifier 通过率一直涨而 clean resolved 后期崩塌** | `08_rl_recipe.md:1653-1661` | 公开 |
| Verification Horizon 表 2：**只有「解法产物检索」（Freq 4.32% / Resolved 72.34% / +12.35）与「外部修复查找」正相关**；可见测试过拟合 −8.37、harness 篡改 −18.52、oracle 篡改 −12.70 | **要监控可达的外部捷径，不是硬编码常量** | `08_rl_recipe.md:1637-1649` | 公开 |
| **ARA：proxy reward 根本看不见 hacking（真实 0.91 vs 利用 0.89，Δ=0.02）**；GPT-4 Δ0.44；训过的 Auditor Δ0.63 | 自带 reward 无法自证清白 | `08_rl_recipe.md:700`、`:1612-1632` | 公开 |
| 多模态 reward hacking：只看结果最高 **48.1%**；32B 仍 **54.9%** 更差率；**关键词式「视觉证据 reward」比答案感知式更易被 hack（高 2.2~3.4 分）** | 只有 VLM 语义验证能降 hacking | `08_rl_recipe.md:546`、`:693` | 公开 |
| RULER 加法聚合：**Aesthetic 4.31 → 6.70（+55%）而 CLIP −20%、Icon rubric 0.395 → 0.262、tokens 0.3k → 6.3k** | 加权求和是 hacking 面 | `08_rl_recipe.md:672-684` | 公开 |
| Adaptive-Group：改成求和后 recall 97.2 但**特异度塌到 53.5（≈全部放行）** | **两个维度要相乘不要相加** | `05_trajectory_repair.md:618-623` | 公开 |
| 噪声地板：生成 σ=10.4（极差 24.4）/ judge σ=8.5 / Render+Judge σ=5.0；某 checkpoint 生成 σ=2.8 而 **judge σ=11.4 成瓶颈**；模型档位差约 40 ELO | **任何「这轮掉了」要 > 2σ；靠单个 VLM 分差剪枝就是把噪声当信号剪** | `08_rl_recipe.md:1687-1692`；`05:880-886` | 公开 |
| 【本机实测】judge 单次判定翻面率最差一档 **20.8%**（claude-opus-5-5 多视角）；**4 模型 × 2 次 = 8 票聚合后立刻稳定**（单视角 18/18、多视角 17/18） | **单次 VLM 判定的 σ 太大，K≥4 聚合是硬要求，且多模型优于同模型多采样** | `12_self_verification.md:676-696` | 实测 |
| ⚠️ 【本机实测】但「多数正确」≠「稳定」：单视角的 18/18 建立在 **4/7 的薄弱多数**上 | 换一组 judge 可能翻 | `12_self_verification.md:697-698` | 实测 |
| 【本机实测】整体 McNemar 精确双侧 **p=0.65，仅 19/138 对不一致** | **「单看总分会得出『多视角没用』的错误结论，真正的信息全在拆解里」** | `12_self_verification.md:556-567` | 实测 |
| 【本机实测】功效表：检出 0.57→0.88 需每臂 32 次；0.70→0.85 需 121 次；配对 McNemar（不一致率 0.14）OR=2.0 需 488 次总量 | **预注册：不一致对 < 20 就标功效不足** | `12_self_verification.md:732-748`、`:775-782` | 实测 |
| **MT-Bench 位置偏置：Claude-v1 换序后默认一致率仅 23.8%（首位偏好 75.0%）**，改名后 56.2%；GPT-4 默认 65.0% → 加 few-shot 77.5% | **side-by-side 必须双序跑，只用一致的结果** | `12_self_verification.md:311-321` | 公开 |
| **CriticGPT 对抗式难度过滤：要求插入的 bug 至少被三个 critic 采样中的一个漏掉** | 可直接抄的「造难题」判据 | `12_self_verification.md:353-354` | 公开 |
| **CriticGPT 非平凡性验证：确认小模型做不了「这段代码被改过吗」这个二分类**，且随规模平滑提升 | **防止插入的 bug 带上格式/风格捷径特征** | `12_self_verification.md:355` | 公开 |
| ⚠️ **判别-批评 gap：判别器的分数不能预测 critic 表现；在最大判别器最自信判错的 10% 上 critic 仍抓到约 54%** | **「模型其实知道只是不说」未被证实，两条能力路径要分开训** | `12_self_verification.md:275-279` | 公开 |
| CodeContests+ 用 **1.72M 条带标签解法**测每题 TPR/TNR → **同阈值下合格题数翻倍** | 测试质量可量化 | `03_verifiable_construction.md:271` | 公开 |
| HardTests（47,136 题）：有 oracle 程序时合成测试**精度 +11.3 分、召回 +17.5 分**；旧式合成测试在难题上**假阳率 >90%** | 有参考解时测试质量跃升 | `03_verifiable_construction.md:272` | 公开 |
| 题面-测试对齐：**instruct_clear F1 ≈ 92~95，instruct_ut_align F1 ≈ 75~78** | 与 SPICE 的 87.3 / 68.5 同向 | `03_verifiable_construction.md:273` | 公开 |
| 入池质量阈值（推导初值）：可解率 100% / 变异杀死 TNR ≥ 95% / 正确解通过 TPR ≥ 90% / flaky ≤ 1% / 人工大问题 ≤ 5% / 污染 0 | 可直接抄的门禁表 | `03_verifiable_construction.md:326-341` | 推导 |
| **「判别力是最容易被忽略的一项：可解率只证明 R 能过，判别力证明错的过不了」** | 一句可引的话 | `03_verifiable_construction.md:342` | 推导 |

### 多样性、去重、「场景多 ≠ 数据好」

| 数字 | 能证明什么 | 出处 | 口径 |
|---|---|---|---|
| **Hill number：q=0（支撑集大小）就是组合计数，论文直接称它 *an uninformative measure of diversity*；q=1 = Vendi Score = 有效独特元素数** | **「组合空间 / 有效多样性」的折损倍数 = D_0/D_1** | `13_scaling_tasks.md:184-196` | 公开 |
| **Stacked-MNIST：三个模型的 NoM 全是满分 1000，而 VS = 746.7 / 866.6 / 943.7** | 同一张表上把组合计数和有效多样性摆开 | `13_scaling_tasks.md:206-208` | 公开 |
| **MOSES：IntDiv 把 HMM 排第一（0.871），VS 把它排最后（250.9 vs 其余 475~537）** | **平均成对距离类指标对成簇重复是盲的** | `13_scaling_tasks.md:209-210` | 公开 |
| **MS-COCO：人类 5 条 caption VS = 4.88，beam search 只有 3.00** | 「有效条数」的直观读法 | `13_scaling_tasks.md:211-212` | 公开 |
| **【本机算术】槽位表 D_0 = 7.0e8，有效等价类约 15,750，折损约 44,000 倍** | **一张看起来能出 7 亿种场景的表，实际只能出约 1.6 万种可区分任务** | `13_scaling_tasks.md:275-293` | 推导（基于实测分辨率） |
| 【本机】`bulb.energy` 19 档在 Workbench 下**可区分档数 = 0**；Blender 留出集**唯一的误杀**正是「日光功率 3.0 → 3.5 被 A6 判错」 | **渲染后看不见的槽位必须禁止进 spec.json** | `13_scaling_tasks.md:283`、`:294-297` | 实测 |
| Infinigen **182 个生成器 / 1,070 个自由度**，而**论文自己在表注里称它 proxy** | 组合计数不等于有效多样性 | `92_number_audit.md:38` | 公开（已核验） |
| ⚠️ Infinigen-Indoors 表 3：**`w/o Discrete change` 86.20 > 全系统 80.84**，作者说离散改动「necessary for compelling visuals, but decrease the quantitative score」 | **量化指标和观感会反向——多样性指标涨了不等于数据变好** | `13_scaling_tasks.md:330-334` | 公开 |
| Density/Coverage 的理论锚：同分布时 **E[density] = 1**、**E[coverage] = 1 − 1/2^k**（与分布类型和维度无关），所以 k=5 → 0.969 | **三代指标里唯一能按理论选超参的** | `13_scaling_tasks.md:228-232` | 公开 |
| 抗离群实测：切掉离群点后 **recall 上升 >11%（CelebA）/ >15%（LSUN），而 coverage 上升 <2%** | **用 coverage 不用 recall** | `13_scaling_tasks.md:233-234` | 公开 |
| **嵌入选择：MNIST Coverage 从 T4096（VGG16 fc2）的 0.108 升到 R64（随机初始化 64 维）的 0.714**；音频 0.020 → 0.653 | **目标域离 ImageNet 远时，预训练视觉特征会把一切压成一团** | `13_scaling_tasks.md:235-243` | 公开 |
| improved P/R 的失效：**真假分布完全相同时 P/R 也只有 0.68 / 0.67** | 这类指标本身有偏 | `13_scaling_tasks.md:222` | 公开 |
| RST 仪表盘五条：改写族熵 **2.26~2.31 bits（上限 2.32）**、最大族占比 **24.9~28.9%**、40 个算子每轮用 **31~38 个**、**最频繁算子只占 8.0%**、种子覆盖 98.3% → **60.1%**、**单种子贡献 ≤ 0.77%**、轮内最近邻相似度中位 0.223 → **0.464（p95 0.703）** | **五条合起来比任何单一指标都更能抓塌缩** | `13_scaling_tasks.md:300-313` | 公开 |
| RST 的污染对照：**13-token 滑窗下没有任何 benchmark 任务匹配任何合成轮次**，最大 5-gram Jaccard **< 0.009**，unigram JSD 全部上升 | **递归合成产出的是越来越远离 benchmark 的分布** | `13_scaling_tasks.md:315-317` | 公开 |
| **十万量级去重的全部成本：embedding 1.25 GPU 小时 + pHash 40 分钟 + 全对全余弦 0.14 秒 + 存储 307 MB** | **十万量级的去重是免费的，不需要 ANN 索引** | `13_scaling_tasks.md:918-932` | 推导（基于公开吞吐） |
| ⚠️ 百万级的串行墙：MinHash 第三阶段连通分量聚类是**单任务 / 8 核 / 约 200 GB 内存 / 约 30 小时墙钟**，不可并行 | 扩产规划要记住这个墙 | `13_scaling_tasks.md:935-937` | 公开 |
| **主流代码数据集没有一个用 AST 等价做去重**；真用结构哈希的只有 ComPile（StructuralHash，990 GB → 853 GB，**体积 −35%**） | 结构去重在工业界几乎没人做 | `13_scaling_tasks.md:940-952` | 公开 |
| 【本机】`cube_size2`：换实现路径、世界几何逐点相同，几何信号全部放行（**分部件 F-score 0.9993**），**只有按代码比的 A2/A3 会误杀** | **去重单位必须是产物（场景图），不是代码** | `13_scaling_tasks.md:956-960` | 实测 |
| **num_perm=128 在「大片高度重叠同族」上精度掉到 0.69~0.77 / 召回 0.69~0.84**（孤立近重复时是 0.92~1.0） | **我们的任务集属于后者，必须上 256~512 或加精确 Jaccard 复核** | `13_scaling_tasks.md:999-1006` | 公开 |
| The Stack v1：Jaccard > 0.85 去掉 **38.6% 文件 / 53.7% 体积**；StarCoder2 用 5-gram **Jaccard 0.7**；OpenCoder 的 SHA256 阶段就有约 **75% 文件完全重复** | 代码侧阈值与去重率的参照 | `13_scaling_tasks.md:985-995` | 公开 |
| **pHash 的 FPR 在 1.18M ImageNet 图上：T=6 约 0.044%，T=14 飙到 73%** | 哈希阈值一动就废 | `13_scaling_tasks.md:1021` | 公开 |
| **DataComp 对评测集去重用 copy-detection descriptor 余弦 > 0.604169；CLIP ViT-B/32 在同 precision 下 recall 只有 0.02** | **别用 CLIP 做去重** | `13_scaling_tasks.md:1025` | 公开 |
| DINOv2 自去重 **SSCD > 0.6（1.3B → 1.1B，−15.4%）**，对评测集 **> 0.45（−32.4%）**；SSCD 官方推荐 **> 0.75**（90% precision）；MONET 1 亿级生产集也用 0.75（累计 −7.7%） | 视觉去重可抄的阈值 | `13_scaling_tasks.md:1027-1031` | 公开 |
| ⚠️ MONET 实证 **pHash 不可靠：真近重复可达 d=26，而 d=1 就存在语义无关的假阳性簇** | pHash 只能用 d=0 清精确重复 | `13_scaling_tasks.md:1031` | 公开 |
| ⚠️ **明确未找到 `pHash ≤ 5` / `≤ 8` 的权威推荐值**——「业界通常用 pHash ≤ 5」是传说 | 避免写进正文 | `13_scaling_tasks.md:1033-1034` | 未找到 |
| ⚠️ **ISC2021：库从 100 万涨到 1,000 万，同一阈值下 recall 不变而 precision 从 0.8 跌到约 0.29** | **阈值必须随库规模重标** | `13_scaling_tasks.md:1036-1040` | 公开 |
| SemDeDup：**cos ≥ 0.97 判近重复；删 37% 无损，删 50% ImageNet top-1 只降 0.47%（68.27 vs 68.74），训练时间减半；去重开销 < 训练 GPU 时的 1%** | 语义去重的阈值与收益 | `13_scaling_tasks.md:1062`、`:1213` | 公开 |
| ⚠️ **FineWeb：全局去重 15T → 4T（最老快照删掉 90%）却「相比不去重几乎没有提升」；逐快照独立去重保留 20T，持平 RefinedWeb** | **去重会过头：收益只来自打掉巨型重复簇，清小簇反而有害** | `13_scaling_tasks.md:1183-1196` | 公开 |
| 同上对照实验：2013-48「全局去重后留下的 31B token」训出来**不如**「被删掉的那 460B 单独去重后的 171B token」 | 最反直觉的一条 | `13_scaling_tasks.md:1193-1196` | 公开 |
| **DataComp 池内自去重（T_ADC 0.1/0.2/0.5）下游「与只用 CLIP filter 基本相同」——无额外收益** | 同向证据 | `13_scaling_tasks.md:1198` | 公开 |
| **The Stack 去重收益：HumanEval pass@100 27.21% → 37.00%；MBPP 44.99% → 54.69%** | 去重收益最硬的一条 | `13_scaling_tasks.md:1208` | 公开 |
| **Allamanis：不去重会让指标虚高最多 100%**；JS-150k Acc 55.1 → 49.1，**只看标识符的 Acc-ID 17.7 → 8.6（−51.4%）**；JsNice 变量命名 55.04 → 34.44 | 不去重的代价 | `13_scaling_tasks.md:1211` | 公开 |
| **重复数据的「双下降」：训练 token 中仅 10% 是重复，在最坏重复次数下性能退化相当于模型缩小 2 倍** | **去重开销 < 1% 训练成本，不去重的代价是模型缩小 2 倍** | `13_scaling_tasks.md:1212-1215` | 公开 |
| **LMSYS：改写到 n-gram 测不出后微调——MMLU 54.8 → 89.9；HumanEval 36.0 → 81.1（GPT-4 只有 67.0）；GSM8K 28.7 → 95.3** | **n-gram 挡不住改写** | `13_scaling_tasks.md:1104-1112` | 公开 |
| 同上检测 F1：**10-gram 在改写英文/中文/Python/C 上全部是 0**；LLM Decontaminator **0.940~1.0** | 去污必须上 embedding + LLM 逐对判定 | `13_scaling_tasks.md:1114-1121` | 公开 |
| 真实改写污染率：**The Stack 对 HumanEval 18.9%（31/164）**、MATHInstruct 对 MATH test **15.4%（769/5000）** | **合成数据也会无意污染** | `13_scaling_tasks.md:1123-1127` | 公开 |
| Llama 3 的官方承认：对 MBPP/HumanEval/MMLU，**8-gram 给出的污染率高到无法得出任何可用的增益估计，需要换方法** | n-gram 去污在代码类 benchmark 上失效 | `13_scaling_tasks.md:1092-1100` | 公开 |
| Dolma：段落级 Bloom filter 只删 **0.003%**，事后 WIMBD 体检却发现 **6 个数据集 100% 污染** | 去污做了不等于干净 | `13_scaling_tasks.md:1083` | 公开 |
| infini-gram mini：**AIME-2024 在 Pile/DCLM 上干净，在 CC-2025-21 上 40% dirty；GSM8K 74.2% dirty** | 新集子会随时间被污染 | `13_scaling_tasks.md:1090` | 公开 |
| 本机的结构性优势：**场景图 L-exact 哈希对改写免疫**——LMSYS 证明 10-gram 对改写 F1=0，而「改写不可能在保持几何不变的同时绕过场景图哈希」 | 第三路去污是别人没有的 | `13_scaling_tasks.md:1174-1179` | 推导 |
| GLM-4.5：科学域 RL **只用专家验证过的选择题，明显优于混合质量数据** | **「宁要少而硬，不要多而杂」** | `08_rl_recipe.md:1543` | 公开 |
| Qwen3 的极简配方最后**只有 3,995 对 query-verifier** | 多样性控住以后量可以很小 | `08_rl_recipe.md:629` | 公开 |
| V-GameGym：先对种子代码聚类再按簇采样，**2,219 题 / 100 个簇** | 可抄的簇配额做法 | `03_verifiable_construction.md:277` | 公开 |
| BugPilot：**1.2k FeatAdd 题在 SFT 上胜过 3k 其它 bug 两个点**；RL 后 32B 52.4% / 全量 54.6% | **无意引入的 bug 比刻意注入的更像真实分布** | `03_verifiable_construction.md:74` | 公开 |

### 成本模型：留存率、LLM 调用量、最敏感参数

| 数字 | 能证明什么 | 出处 | 口径 |
|---|---|---|---|
| **要 10 万合格任务得造 26.9 万候选（累计留存 0.372，放大 2.7 倍）** | 本机漏斗的总账 | `13_scaling_tasks.md:1473-1489` | 推导（含两步实测） |
| 漏斗里的实测两步：**准入① 参考解自比自 ≈ 1.0（取 0.97）；准入② 破坏版被判挂 88%~96%（取 0.90）** | 本机唯一的实测留存率 | `13_scaling_tasks.md:1478-1480` | 实测 |
| **半实测的可解性闸 0.88**：本机 9 个桌子任务里 2 个不可解（78%），Blender 留出集 7 个里 1 个（86%） | 「verifier 查的超过题面给的」会吃掉约 12~22% | `13_scaling_tasks.md:1484` | 半实测 |
| ⚠️ **最敏感的一项：难度带筛选留存取 0.60，若实际是 0.30 候选数直接翻倍** | **整个成本模型里最该先用小规模实验钉死的一项** | `13_scaling_tasks.md:1487-1489`、`:40-50` | 推导 |
| 探针总计 **约 1,589,000 次**（准入 806,000 + n=2 筛 333,400 + 补到 n=8 的 450,000） | 工作量的中间量 | `13_scaling_tasks.md:1493-1499` | 推导 |
| three.js：单探针 **3.36 core-s** → **1,480 core-h = 31 台机小时 ≈ 1.3 机日**；不复用浏览器要 **5.1 机日** | **复用浏览器池把吞吐从 3.6 抬到 14.3（近 4 倍）** | `13_scaling_tasks.md:1503-1512` | 推导（基于实测吞吐） |
| Blender：2 核中位下 **2.41 core-s → 1,064 core-h = 0.9 机日**（1 核 0.5 / 4 核 1.8 机日） | 两条线同量级 | `13_scaling_tasks.md:1516-1524` | 推导 |
| ⚠️ **反直觉：Blender 比 three.js 便宜**（Workbench 0.065 s/视角 vs SwiftShader 下的 WebGL）；**three.js 贵在浏览器本身** | 扩产只渲 Workbench 剪影 + 算几何，不渲 Cycles | `13_scaling_tasks.md:1526-1529` | 推导 + 实测 |
| **LLM 调用合计约 1.21M 次，其中难度标定 783,000 次 = 65%**；题干改写 22%、欠规格诊断 10% | **难度标定是唯一值得反复优化的旋钮** | `13_scaling_tasks.md:1533-1543` | 推导 |
| **两段式（n=2 → n=8）比一次性 n=8 省 0.55M 次调用（−31%）**；优化后约 **0.95M 次 ≈ 1.9B 输入 + 0.95B 输出 token** | 可直接拿的省钱动作 | `13_scaling_tasks.md:1545-1551` | 推导 |
| n=64 要 **10.7M** 次调用（13.7 倍）却只把边界桶误分率从 29% 降到 22.5% | 为精度多花 10 倍换不到相应收益 | `13_scaling_tasks.md:481-492`、`:417-430` | 推导 |
| 人工账：**4 轮 × 1,200 条抽检 = 240 人时**，加一致性标定 50 人时 + 欠规格仲裁 67 人时 ≈ **360 人时 ≈ 1.5 人月** | 人工是第二大瓶颈 | `13_scaling_tasks.md:1569-1587` | 推导 |
| 抽检量与 CI：**384 条 ±5.0%**；建议 **12 层 × 100 条 = 1,200 条/轮**（层内 ±9.8%，全局 ±2.8%） | 抽检配额的定法 | `13_scaling_tasks.md:1569-1577` | 推导 |
| 存储：three.js 单任务约 **0.2 MB → 10 万任务 20 GB**；Blender 约 **1 MB → 100 GB**（`.blend` 不存，由 ref.py 重建） | 存储不是约束 | `13_scaling_tasks.md:1600-1602` | 推导 |
| **SWE-smith 按仓库共享环境只要 295 GB，而 SWE-Gym 6 TB、R2E-Gym Subset 4 TB（20 倍压缩）** | 环境体积可以工程掉 | `08_rl_recipe.md:1117-1119` | 公开 |
| **SWE-bench 端到端 2.46%（93,139 PR → 2,294）** | 真实挖矿的基准线 | `13_scaling_tasks.md:1257` | 公开 |
| **SWE-bench Multimodal 0.46%（135k PR → 617）**；人工核实 **83.5%** 的图像是必要的；**69 个实例用逐像素截图测试** | 多模态任务的构造更贵 | `03_verifiable_construction.md:69` | 公开 |
| **SWE-Gym 3.77%（64,689 → 2,438），约 200 人工小时 + 10,000 CPU core-h，镜像 6 TB** ⚠️（另一处记为约 50,000 核时，两值不一致） | 构造算力最硬的公开数字 | `13_scaling_tasks.md:1259`；`03:70` | 公开（口径待核） |
| **SWE-rebench 4.74%，install & validate 只有约 14%，只有 31% 的仓库能装成至少一个任务** | **真实挖矿的瓶颈在「能不能跑起来」** | `13_scaling_tasks.md:1261` | 公开 |
| **Design2Code 0.38%（127.9k → 484）**；WebCode2M **约 0.5%**（Playwright 渲染占总耗时 80%、历时约 1 个月，神经打分器保留 47.5%）；ShaderMatch **0.23%（202k → 467）** | 网页/shader 线的真实量级 | `13_scaling_tasks.md:1284-1287` | 公开 |
| **SWE-smith 50.1%（100,074 → 50,137），约 20 人工小时 + 1,360 美元 + 295 GB**；每题 **0~5.53 美分** | **合成/变异把 yield 抬约 20 倍** | `13_scaling_tasks.md:1260`；`03:72` | 公开 |
| **SWE-smith 策略 yield 差 52 倍：Combine 97.43% / LM Modify（造 bug）55.98% / LM Rewrite（重写函数）35.04% / Class Shuffle 1.88%** | **让模型造 bug 比让它重写函数高 21 个点** | `13_scaling_tasks.md:1266-1278` | 公开 |
| **【本机实测】造 bug 这一路 88%~96%，比 SWE-smith 的 55.98% 高一档** | **因为本机 verifier 是程序化多层的，不依赖已有单测** | `13_scaling_tasks.md:1280`；`90_local_experiments.md §4` | 实测 |
| **WorldCoder-Bench ≲20%（>10,000 候选 → 2,026 + 615 Robust 变体），5 位 PhD 两个月手工 seed** | 高质量 3D 任务的人力代价 | `13_scaling_tasks.md:1299`；`03:185` | 公开 |
| BlenderLLM 约 16%（135 条 seed → 约 50k → 8k）；**人工池通过率只有 20%**，人工与 GPT-4o 一致率 **89.7%** | 自动扩题的真实通过率 | `13_scaling_tasks.md:1297` | 公开 |
| CodeContests：mutation 把测试从 **12.4 条/题抬到 203.7 条（16.4×）**，**假阳性 62% → 4%**；6.3% 的题凑不满 | 补测试的收益与上限 | `13_scaling_tasks.md:1262` | 公开 |
| **【本机】真实素材路线端到端约 3.2%，2,401 仓 × 3 页 × 3.2% ≈ 230 个任务** | **真实素材的真实量级是三位数，价值在多样性注入不在产能** | `13_scaling_tasks.md:1326-1341` | 推导（含实测仓库数） |
| 素材池收缩：three.js 仓库 **89,622 → 2,401（37 倍）**；bpy **6,307 → 56（10~100 倍）**；CodePen **1,000 万 → 约 2.5 万 dump（400 倍）**；Objaverse-XL **10.85M → 只有 5.5M 能被 Blender 导入** | 名义规模都要打折 | `13_scaling_tasks.md:1223-1230` | 实查 + 公开 |
| **three.js 官方 examples：610 条 .html ↔ 610 张截图 = 1:1**，中位 6,137 字节；API 面 **jsm 496 + src 755 = 1,251** | **610 条是种子池的天花板，不是规模池** | `13_scaling_tasks.md:1234-1248` | 实查 |
| ⚠️ 抓取硬约束：GitHub 文件级 code search **未认证 401**（「多少个 .py 含 import bpy」拿不到）；ShaderToy **整站对海外出口 403** | 口径限制要写明 | `13_scaling_tasks.md:1250-1252` | 实测 |
| **判据强度排序**：shader 逐帧像素比对 > 运行时 behavioral contract > mesh/几何分析 + 沙箱执行 > 渲染截图 VLM 打分；**610 组 code+screenshot 只支撑最软的一档** | 要上硬判据必须自己写 contract | `13_scaling_tasks.md:1322-1324` | 推导 |
| **Web-Shepherd 3B PRM 每 1,000 实例 4.67 美元**，vs GPT-4o-mini 43.57、**GPT-4o 435.74**、Qwen2.5-VL-72B 53.69 | **自训小 PRM 比 GPT-4o 便宜约 93 倍** | `08_rl_recipe.md:1375`、`:1233` | 公开 |
| WebGen-Bench：**647 个测试用例全人工执行约 10.8 小时 / 377.8 美元**；32B 微调后 9.5% → 38.2% | 人工执行的单价锚点 | `03_verifiable_construction.md:157` | 公开 |
| RaR：**平均每样本 7.7 条 rubric（20,166 样本 / 154,808 条）**；Verification Horizon：**671 个 WebDev 任务平均 25.9 条 / 6 维** | rubric 的人工量级 | `08_rl_recipe.md:503`、`:505` | 公开 |
| Sketch2Code：**从 723 名申请者里选 21 名标注者**，为 484 个页面画 731 张草图 | 高质量人工标注的筛选比 | `03_verifiable_construction.md:101` | 公开 |
| **SWE-smith 轨迹留存：8,686 任务 / 17,906 次尝试 / 6,457 成功（36%）/ 每题最多 3 条 → 最终 5,016 条（约原始尝试的 28%）** | 蒸馏端的留存率 | `08_rl_recipe.md:1495` | 公开 |
| **SWE-Gym per-instance capping：留 1 → 9.0% / 留 2 → 9.7% / 留 3 → 7.7% / 不设上限 → 9.3%** | **每题取 2~3 条、优先短轨迹** | `08_rl_recipe.md:1496-1497` | 公开 |
| ⚠️ **SWE-smith 按难度分 4 桶各 500 条，训后 12.4 / 10.8 / 13.6 / 12.2，无单调性** | **「难度不决定训练价值」——拒绝采样阶段不要按难度挑** | `08_rl_recipe.md:1498-1499` | 公开 |
| **SWE-Master 数据曲线：0 → 60K 轨迹让 resolve 6.2% → 57.8%，48K 之后趋平**；平均轮数 115→94、思考 token 14.8k→12.7k | 轨迹量的边际收益拐点 | `08_rl_recipe.md:1479` | 公开 |
| ⚠️ **SWE-Gym 在线自提升失败：868 条 on-policy + 491 条 off-policy 把 SWE-bench Lite 从 15.3% 拉到 8.7%** | 自提升不是免费的 | `05_trajectory_repair.md:134` | 公开 |
| 本机一轮 RL **约 12,800 GPU 小时**（204,800 条轨迹、64+64 卡 × 100 小时）；对照 Qwen3-8B 纯 RL **17,920**、MiniMax-M1 **约 258,000 GPU 小时 / 534,700 美元** | 训练侧的量级 | `08_rl_recipe.md:1021`、`:1224` | 推导（文件自标未核实） |
| **AgentDiet：累计输入 token −39.9~59.7%、总成本 −21.1~35.9%，通过率还升（64.5 → 66.5）**；门控规则本身贡献最大（θ=500 匹配原始 65%，θ=0 → 62%，θ=2000 → 58%） | 上下文压缩的正收益 | `05_trajectory_repair.md:82-86` | 公开 |
| ⚠️ **AttnCompress：输入 token −42.3%、单题成本 0.1189 → 0.0949 美元，但通过率 53.17% < 未压缩 55.17%** | 压缩不是都免费 | `05_trajectory_repair.md:93-95` | 公开 |
| **BlenderGym VeriRatio：总查询 < 30 时验证占比 0.33 最好，> 100 时 0.73 最好；每 100 次查询约 0.45 美元** | **算力少就多生成候选，算力多就花在验证上** | `05_trajectory_repair.md:806-808` | 公开 |
| **去重的算力：embedding 1.25 GPU 小时（百万级也只 12.5）** | **「不要因为怕去重贵而跳过去重——这是整条流水线里性价比最高的一步」** | `13_scaling_tasks.md:1553-1565` | 推导 |

---

## 附：本素材库引用口径的三条自律

1. **凡 `92_number_audit.md` 更正过的，一律用更正值并标【已更正】**：
   3JSBench 695 条检查（不是 743）；WorldCoder 2.7% 是判定方式的通过率（模型能力是 27.8%）；
   组大小 8、p=0.1 的全零组概率 43.1%（19% 对应组大小 16）；3DHarnessBench 增益 9.3% 与 20.1%；
   带截图的 issue 约 1,400 个；可访问性改成「判定本身零方差但覆盖面窄」。
2. **凡只有一手引用、没有第二次核验的，引用时必须带出处性质**：
   AutoLab 脚手架消融 0.68/0.46、Vibe Code Bench 榜单分、A11yn 全部数字（`92:63-67`）；
   DAPO 的分项增量（总量已核、分项未核，`92:90-91`）；
   本机一轮 RL 的 12,800 GPU 小时（`08:1833` 自标未核实）。
3. **凡「未找到」的，不要在正文里写成已有结论**：
   「对低 reward 题跑教师 rollout」的成本/命中率/ROI；
   DAPO 的 rollout 放大倍数；`pHash ≤ 5` 的权威推荐值；
   「不交付生成器源码以防模型拟合生成器代码风格」这条原则的直接文献（`13:128-145`）；
   配比（纯净 vs 带纠错轨迹）的系统扫描。

**最后一条通用警告（两个主题共用）**：
**同一个模型换脚手架能差 11.7 点**（GPT-5.5：OpenHands 69.85 / Factory 67.39 / Codex 58.19），
所以**任何单点分数离开 harness 版本都没有意义**（`92_number_audit.md:70`）。
而审计本身的结论是：**「最容易出错的不是数字本身，是数字的归属」**——
抽查十四组撞到一处不存在的引用，**所以抽查必须做**（`92_number_audit.md:93-104`）。

