## 1 A Verifiable Task Is Three Things, Not One

本章只回答一个问题：**怎么把一批网页，变成能训模型的题。**

一条可验证任务由三件组成，缺一件就只是数据，不是任务。三个词全章含义固定，后面三节各讲一件。

| 件 | 在 Web 这条线上具体是什么 | 缺了它会怎样 |
|---|---|---|
| Omni Reference Query | 需求描述，加上零到四层参考：参考图、参考页面、参考录屏、参考音频 | 只有源码没有题干，就只能做无监督 |
| Verifier | 把采集到的证据判成通过或不通过的规则 | 没有梯度，只能靠人看 |
| Harness | 无头浏览器、冻结时钟、固定视口、运行时状态读取、多视口截图 | 产物跑不起来，判据无从落地 |

三条硬约束：

1. **Verifier 能查的信息量 ≤ Query 给出的信息量。**
   - 反例：需求只说「杯子要用有别于桌面木色的独立颜色」，判据却要求恰好是参考图里那个蓝。题不可解，进 RL 就是纯噪声。
   - 反向更严：题面、实现、意图里的每个声明，都至少映射到一个检查项。
2. **参考代码不进 reward，也不进题面。**
   - 它属于 Verifier 一侧，不属于目标一侧。
   - 五个用途：证明可解、生成断言、当变异母本、做 verifier 自检、当合格的示范轨迹。没有一个是「当目标」。
   - 实测：用参考做李克特量表打分 31.7%，无参考评分项 32.0%，用参考生成评分项 35.9%。
3. **判据读运行后的状态，不读代码。**
   - 实测：一个在世界几何上逐点等同的替代实现，通过了全部几何信号（分部件 F-score 0.9993），只被代码比对类判据误杀。
   - 等价实现极多，验状态是可复现性的必要条件，不是审美偏好。

## 2 Omni Reference Query: Where The Material Comes From

Query 这一侧回答两个问题：

- 素材从哪来 → 决定供给的天花板
- 参考给到什么程度 → 决定判据的来源

### 2.1 Overview

**可挖的来源压倒性地是代码仓库和开发者社区，不是设计网站。** 设计站在素材里几乎是空的，总表里单独标「未查」。

核心发现：唯一自带「代码与参考截图」配对的 Golden Images，11 个仓库总共只有 18,615 张参考图。

| Source | Type | Datasize | Example | 详见 |
|---|---|--:|---|:-:|
| **GitHub** | Golden Images（VRT 基线） | 11 仓 · 18,615 图 | [three.js](https://github.com/mrdoob/three.js) · [Babylon.js](https://github.com/BabylonJS/Babylon.js) · [Chart.js](https://github.com/chartjs/Chart.js) | 2.2.1 |
| | VRT 下游仓库（未挖） | 458,596 依赖仓 | [Playwright](https://github.com/microsoft/playwright) · Storybook · BackstopJS | 2.2.1 |
| | Issue + 截图 + PR | ≈ 1,400 条 | [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) · OmniGIRL | 2.2.2 |
| **HuggingFace** | 图码配对集 | 80 – 3.17M | [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m) · [WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) · [Design2Code](https://arxiv.org/abs/2403.03163) | 2.3 |
| **Website** | 社区站 / 问答站 | 2,799 – 10M | [CodePen](https://codepen.io/) · [Shadertoy](https://www.shadertoy.com/) · [js13kGames](https://js13kgames.com/) | 2.4 |
| | 真实门户页 | 45.1k 页 | [WebRenderBench](https://arxiv.org/abs/2510.04097) | — |
| | 设计站（未查） | — | [Awwwards](https://www.awwwards.com/) · [Dribbble](https://dribbble.com/) · [Figma Community](https://www.figma.com/community) | — |

Golden Images：仓库为每份测试代码存一张标准截图，CI 每次渲染后逐像素比对（Visual Regression Testing），代码与截图因此天然成对。

数据解读：

- 能当 RL 题干母本的只有 Golden Images、VRT 下游仓库和真实门户页。
- 社区站与公开配对集产出的是「配对」，不是「题」。**配对只够做无监督与蒸馏母本，要变成 RL 题还得补判据。**

### 2.2 Github Repo

#### 2.2.1 Repo

全库最硬的一类来源：仓库自带「代码与参考截图」配对，配对关系由持续集成维护，不是事后对齐。

核心发现：11 个仓库共 18,615 张参考图、8,157 份代码，严格一图一码的只有 three.js / Chart.js / OpenLayers 三家。

| Repo | Reference（image +） | Datasize（图 / 码） | Output | Permitted |
|---|:-:|--:|:-:|---|
| [primer/react](https://github.com/primer/react) | title | 7,768 / 753（**10.3 : 1**） | `.tsx` | ✓ MIT |
| [Blender](https://github.com/blender/blender/tree/main/tests/files/render) | — | 2,564 / 839（**3.1 : 1**） | `.blend` | △ GPL |
| [MapLibre](https://github.com/maplibre/maplibre-gl-js) | desc 9% | 1,960 / 1,734（1.1 : 1） | `.json` | ✓ BSD-3 |
| [PixiJS](https://github.com/pixijs/pixijs) | desc | 1,711 / 460（**3.7 : 1**） | `.ts` | ✓ MIT |
| [plotly.js](https://github.com/plotly/plotly.js) | — | 1,324 / 1,309（1 : 1） | `.json` | ✓ MIT |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js) | title | 916 / 906（1 : 1） | `.ts`¹ | △ Apache-2.0，代码在 Playground |
| [Chart.js](https://github.com/chartjs/Chart.js) | — | 667 / 667（1 : 1） | `.js` | ✓ MIT |
| [three.js](https://github.com/mrdoob/three.js) | title | 613 / 613（1 : 1） | `.html` | ✓ MIT |
| [p5.js](https://github.com/processing/p5.js) | desc | 605 / 442（1.4 : 1） | `.js` | △ LGPL-2.1 |
| [deck.gl](https://github.com/visgl/deck.gl) | — | 252 / ≈199（≈1.3 : 1） | `.ts` | ✓ MIT |
| [OpenLayers](https://github.com/openlayers/openlayers) | — | 235 / 235（1 : 1） | `.js` | ✓ BSD-2 |
| **合计** | | **18,615 / 8,157（2.3 : 1）** | | |

title = 短标签，desc = 整句描述，— = 只有文件名；图:码 > 1 来自多主题（react）、多渲染后端（PixiJS / Blender）、多帧（p5）。
¹ 888/906 的代码在外部 Playground，仓库只存 id。✓ 宽松许可，△ 传染性许可或代码不在仓库。2026-10-20 按各仓库 HEAD 实数，许可读自各仓库 LICENSE。

数据解读：

- **图数与码数按各仓库 HEAD 逐个实数。**
  - 旧材料里 three.js 610、Babylon.js 975、Blender 2,596，实测分别是 613、916、2,564。
  - 公开材料里的「约」常差一个数量级，引用这类数字必须核验。
- **有基线却不能用的，不排掉会把供给高估一倍：**
  - react-three-fiber：0 张图
  - PlayCanvas：296 个示例、592 张缩略图，但没有比对
  - Godot：238 个文件，只有 1 张图
  - Mermaid、Ant Design：走外部云服务
  - ECharts：基线不在仓库里
- 它只支撑最软的那一档判据。
  - three.js 的 613 组配对是一比一的，但另一端是截图，只能喂视觉相似度，喂不了运行时契约。
  - 判据强度：逐帧像素比对 > 运行时行为契约 > 几何分析 > 渲染截图的模型打分。**Golden Images 恰好落在最软的那一端。**

three.js 的形态直接决定 Harness 的单价：

- 全树 6,413 个文件
- 示例页 610 个（WebGL 298 / WebGPU 234 / WebXR 27 / 其他 23）
- 单页中位 6,137 字节，95 分位 13,651，最大 66,143，总体积 4.4 MB
- 可用接口 1,251 个
- **这个量级模型能在上下文里直接带着走，不需要先检索再用。**

视觉回归生态不是数据，是「哪里还藏着带截图断言的仓库」的规模估算：

- 下游依赖数：[Playwright](https://github.com/microsoft/playwright) 458,596 > Storybook 127,816 > jest-image-snapshot 15,400 > Storybook 测试运行器 13,236 > BackstopJS 5,300 > Loki 3,942 > reg-suit 611 > lost-pixel 187
- 已合并 PR 的文本命中：截图断言 14,656 次与 32,634 次
- 排除 [Chromatic](https://www.chromatic.com/)（57,166 个依赖）与 [Percy](https://percy.io/)（6,023 个依赖）：**基线都存在云端，拿不到**

#### 2.2.2 Issue From PR

带截图的 issue 是独立的一条路，产物是「问题描述、复现截图、修复补丁」三元组，不是「图与码」。

- [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859)：617 个实例覆盖 17 个 JavaScript 库，**83.5% 经人工确认必须看图才能解**；公开数据集实际 612 行。
- OmniGIRL：959 个实例上，一个当时的前沿模型在带图 issue 上解决率只有 10.5%。
- 存量搜索命中十万量级（新图床上 TypeScript 192,818、JavaScript 51,136、CSS 3,488），但**真正能成型的只有约 1,400 个**。
  - 曾更正过：原先写「约一万」，与自己引用的转化率矛盾。

### 2.3 Huggingface

核心发现：规模最大的几份数据集都未发布；能下载的最大一份 317 万行；被当成基准最多的那份只有 484 条。

| Dataset | Reference | Datasize | Output | Permitted |
|---|:-:|--:|:-:|---|
| [Pix2Struct](https://arxiv.org/abs/2210.03347) | image | 80M | 简化 HTML 解析 | ✗ 未发布 |
| [UI2Code^N](https://arxiv.org/abs/2511.08195) | image | ≈10M | HTML | ✗ 未发布 |
| [MultiUI](https://huggingface.co/datasets/neulab/MultiUI) | image + 问题 | 7.3M | 文字答案 / 包围盒 | △ ODC-BY，需申请 |
| [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m) | image | 3.17M（净化 2.56M） | HTML + 布局框 | ✓ CC-BY-4.0 |
| [WebSight v0.2](https://huggingface.co/datasets/HuggingFaceM4/WebSight) | image + desc | 1.92M | HTML（Tailwind） | ✓ CC-BY-4.0 |
| [Web2Code](https://huggingface.co/datasets/MBZUAI/Web2Code) | image + 指令 | 828k | HTML | △ 卡片 MIT，与论文不一致 |
| [WebUI](https://huggingface.co/datasets/biglab/webui-7k) | image | 400k 页 × ≤ 6 设备 | 无障碍树 + 包围盒 + 样式 | △ 研究许可 |
| [ScreenCoder](https://huggingface.co/datasets/Leigest/ScreenCoder) | image | 1,000（论文 10k） | HTML | ✓ Apache-2.0 |
| [BigDocs](https://arxiv.org/abs/2412.04626) | image | 11k | HTML | ？HF 主仓未见该子集 |
| [Design2Code](https://huggingface.co/datasets/SALT-NLP/Design2Code) | image | 484 | HTML | ✓ ODC-BY |
| [Design2Code-HARD](https://huggingface.co/datasets/SALT-NLP/Design2Code-HARD) | image | 80 | HTML | ✓ ODC-BY |
| [Sketch2Code](https://huggingface.co/datasets/SALT-NLP/Sketch2Code) | 手绘草图 | 731 | HTML | ✓ ODC-BY |
| [pix2code](https://github.com/tonybeltramelli/pix2code) | image | 1,750 | DSL（非 HTML） | ✓ Apache-2.0 |

已知问题：

- Pix2Struct：目标是简化解析，不是可运行页面
- UI2Code^N：两处独立确认未放出
- MultiUI：基于无障碍树，**不是代码对**；100 万站点
- WebCode2M：1,100 GB，净化版剔 19.2%，平均 5,366 token
- WebSight：317 GB；**图床已失效**，渲染不可复现
- Web2Code：截图管线抓的是第 2 屏；许可口径**自相矛盾**
- WebUI：**完全不做候选过滤**；不含 HTML
- ScreenCoder：爬 5 万 → 留 1 万，留存 20%；公开的只有 ScreenBench 1,000 对
- BigDocs：元素密度低，平均 20.3 个元素
- Design2Code：平均 **31,216** token
- Design2Code-HARD：平均 251 个标签，26% 的样本超过 500 个标签
- Sketch2Code：10 个模型都难读懂草图
- pix2code：纯合成

desc = 描述文本（WebSight 的 `llm_generated_idea`）。许可与字段 2026-10-20 读自各数据集卡片与文件列表。

数据解读：**论文里的数不等于能下载的数，引用前必须核。** 逐条核过的偏差（最大差一百倍）：

- Design2Code：论文 484，公开 485
- Design2Code-HARD：卡片 80，实际 162 行
- Web2Code：论文 117.97 万，默认配置只有 100 行
- [SWE-bench](https://arxiv.org/abs/2310.06770)：2,294 对 2,519
- [SWE-smith](https://arxiv.org/abs/2504.21798)：50,137 对 59,136
- [Objaverse-XL](https://arxiv.org/abs/2307.05663)：1,020 万对 10,850,997

### 2.4 Website

核心发现：十四家社区站只有七家可用；能当生成目标的产物只有「自包含可运行单文件」一种，其余是片段、笔记本或纯资产。

| Website | Reference | Datasize | Output | Permitted |
|---|:-:|--:|---|:-:|
| [js13kGames](https://js13kgames.com/) | image + title | 2,799 | 单文件 `.html`（≤ 13 KB） | ✓ 逐件核许可 |
| [Hugging Face 静态空间](https://huggingface.co/spaces) | title + desc | 331,654 | 多文件静态站 | ✓ 按许可字段筛 |
| [Poly Haven](https://polyhaven.com/) | image + title | 2,387 | HDRI / 贴图 / 模型，无代码 | ✓ CC0 |
| [CodePen](https://codepen.io/) | image + title† | 10M → 25k | html / css / js 三段 | △ MIT 须署名；拿不到量 |
| [OpenProcessing](https://openprocessing.org/) | image + title + desc | 1M+ | p5 草图 `.js` | △ 逐件核；限速 6 s |
| [Sketchfab](https://sketchfab.com/) | image + title | 500k | 3D 模型，无代码 | △ 剔除 NC 许可 |
| [Frontend Mentor](https://www.frontendmentor.io/) | image（设计稿）+ desc | 7,155 | 多文件前端工程 | △ 设计稿不可再分发 |
| [Stack Overflow](https://stackoverflow.com/) | title + desc | 20.9k（three.js 标签） | 代码片段 | ✗ 转储禁训 |
| [Blender StackExchange](https://blender.stackexchange.com/) | title + desc | 123k 问 | 脚本片段 | ✗ 转储禁训 |
| [Shadertoy](https://www.shadertoy.com/) | image + title† | 52k | GLSL 片段着色器 | ✗ CC BY-NC-SA |
| [BlenderArtists](https://blenderartists.org/) | image + title + desc | 602k 帖 | 帖子 + 少量 `.blend` | ✗ robots 全禁 |
| [three.js 论坛](https://discourse.threejs.org/) | title + desc† | 26k 帖 | 片段链接 | ✗ 无内容许可 |
| [Observable](https://observablehq.com/) | title + desc | — | 笔记本，不可独立渲染 | ✗ 无默认许可 |
| [JSFiddle](https://jsfiddle.net/) | title | — | html / css / js 三段 | ✗ 无默认许可 |

✓ 可用　△ 有条件　✗ 不可用。desc = 正文或描述文本。† 站点对本机 403，未直连核实。

数据解读：

- **产物形态把这十四家分成三种命运：**
  - 能直接当生成目标（三家半）：js13kGames 的自包含单文件、静态空间的多文件工程、CodePen 与 JSFiddle 的单文件片段（后者取不到量）
  - 拿到片段（六家）：跑不起来、过不了执行闸，只能当无监督语料或反向构造题干的素材
  - 资产站（两家）：一行代码都没有，是素材池与渲染基线，不是题库
- 着色器与笔记本都不能直接套网页管线，要单独处置。
  - 着色器源码不是页面，要补一层固定的渲染外壳才能进 harness
  - 笔记本的单元格依赖运行时求值顺序，离开自己的运行环境就不可渲染
- **「没写许可」是最严的情况，不是最松的。**
  - 无许可等于保留一切权利，所以 Observable 与 JSFiddle 比 Shadertoy 更不可用
  - Shadertoy 的非商业条款只留下非商用研究一个口子
- 爬虫协议不是许可，但决定能不能合法拿到。许可与条款分别过，两道闸都过才算可用。
  - BlenderArtists 的 60 万帖也许能引用，但抓取代理被全量封禁，整条路堵死
  - js13kGames「允许抓取」不代表每件作品都可商用
- 可用量要按许可过滤之后算。
  - 自报规模最大的三家：CodePen 过滤完约 2.5 万；OpenProcessing 要按 6 秒间隔慢爬且逐件核许可；BlenderArtists 归零
  - 同一现象：Blender 官方扩展目录里传染性许可 1,341 个、MIT 只有 4 个
  - **名义规模与可用规模差一到两个数量级，差距主要来自许可，不是反爬**
- 体积限制是意外的质量闸。
  - js13kGames 的 13 KB 上限让 2,799 件作品天然自包含、可单文件渲染
  - 与 three.js 示例页的中位 6,137 字节同一量级
  - **自包含单文件是这条线唯一可规模化的产物形态**

设计类站点（**本项目素材里全部标「未查」，表里只算待办，不算已有供给**）：

- [Awwwards](https://www.awwwards.com/)：获奖站截图与录屏，本项目自评「只有图没有代码」
- [Dribbble](https://dribbble.com/)：版权风险高
- [Figma Community](https://www.figma.com/community)：免费文件为署名许可，但爬虫协议点名封禁主流抓取代理
- [itch.io](https://itch.io/)：无源码
- [Observable](https://observablehq.com/)：无默认许可
- 其余获奖与画廊类聚合站：素材里零命中，不列

#### 2.4.1 Why Real Pages Fail

核心发现：真实页面在可渲染性、质量和长度三条上同时不合格，三条都有实测。

- **原始网页归档不能用于渲染。** 四家、三种做法、同一个结论：
  - [Design2Code](https://arxiv.org/abs/2403.03163)：只把归档里的网址当种子重爬，因为归档缺图片与样式表，无法忠实渲染
  - [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m)：起点是公共爬取语料，但管线开头就是内联样式再过真实浏览器
  - WebUI 与 [ScreenCoder](https://arxiv.org/abs/2507.22827)：直接自爬
- 真实页面大部分不配当监督信号。
  - 6 名标注员约两周打出 10,000 个质量分，**80% 落在五分制的 0 到 1 分**
  - 据此训出的打分器在 WebCode2M 管线上剔掉 52.5% 的原始数据（全库唯一公开的单步剔除比例）
- 长度本身让它不可训。
  - Design2Code：平均源码 31,216 ± 23,903 token、158 个标签、DOM 深度 13
  - 合成数据：647 ± 216 token、19 个标签、深度 5
  - 真实页面 token 多 50 倍、标签多 6 倍、深度 2 倍
  - **唯一被实验验证过的可训点：约 5,000 token**，既保留真实结构又训得动
- 把原文文字直接塞进提示词是净负收益。
  - 一个 8B 开源模型拿到全部文字后，HTML 合法率 98.0% → 39.2%
  - 另一个 8B 模型的文字维度分 80.3 → 55.6 → 22.6

DOM 简化的三条路线：

1. 简化成解析目标：学得动，但产物不可渲染，没有生成目标，也接不上视觉判据
2. 保留可渲染页面
3. 重写而不是清洗：拿真实分布换干净

**本章取路线 2：只有可渲染的数据才能同时带包围盒对齐信号和下游渲染奖励。**

### 2.5 Two Contractions

两次收缩，都有公开自报的实测值：

- 名义规模 → 能用的规模：差一到两个数量级
- 能用的素材 → 能训的任务：再掉两个数量级

核心发现：真实挖矿的端到端留存率全部落在 0.2% 到 5%，瓶颈不在筛选，在能不能跑起来。

| Source | Name | Unit | Filter | Funnel | Retention |
|---|---|:-:|---|--:|--:|
| **GitHub** | 3js | 仓 | GitHub 搜「three.js」→ 主题标签 → 星 > 10 | 89k → **2.4k** | 2.7% |
| | blender | 仓 | GitHub 搜「blender addon」→ Python + 星 > 10 | 6.3k → **56** | 0.9% |
| | [SWE-bench](https://arxiv.org/abs/2310.06770) | PR | 12 个热门 Python 仓的 PR → 属性过滤 → 执行校验 | 93k → 11k → **2.3k** | 2.5% |
| | [SWE-Gym](https://arxiv.org/abs/2412.21139) | 条 | 358 个 Python 仓的 PR → 选 11 仓 → 执行校验 | 65k → **2.4k** | 3.8% |
| | [SWE-rebench](https://arxiv.org/abs/2505.20411) | PR | GitHub 公开 PR → 下载 → 安装与校验 | 10M → 450k → **21k** | 0.21% |
| | [SWE-smith](https://arxiv.org/abs/2504.21798)（合成） | bug | 128 个 Python 仓合成 bug → 执行校验 | 100k → **50k** | 50.1% |
| | 本项目 three.js（估） | 页 | 上面 3js 的 2.4k 仓 × 3 页 → 可用 | 7.2k → **≈230** | 3.2% |
| **HuggingFace** | [Design2Code](https://arxiv.org/abs/2403.03163) | 页 | [C4](https://huggingface.co/datasets/allenai/c4) 验证集网页 → 长度去重 → 抽 7k 人工检查 | 128k → 14k → **484** | 0.38% |
| | [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m) | 页 | [Common Crawl](https://commoncrawl.org/) 抽样 → 长度 → 渲染 → 打分器 → 截图去重 | 500M → **2.56M** | 0.51% |
| | [The Stack v2](https://arxiv.org/abs/2402.19173)（html） | GB | [Software Heritage](https://www.softwareheritage.org/) 源码存档 → 许可 → 近似去重 → 质量 | 2.4T → **99G** | 4.1% |
| | [Objaverse-XL](https://arxiv.org/abs/2307.05663) | 文件 | GitHub / [Sketchfab](https://sketchfab.com/) 等 3D 索引 → Blender 渲染 | 37M → **5.5M** | 14.9% |
| **Website** | [CodePen](https://blog.codepen.io/2016/11/25/10000000/) | 作品 | [CodePen](https://codepen.io/) 官方自报作品数 → 无列举接口 → 只剩公开镜像 | 10M → **25k** | 0.25% |
| | [shaders21k](https://arxiv.org/abs/2211.16412) | 作品 | [Shadertoy](https://www.shadertoy.com/) 公开作品 → 可编译 → 去重 → 去静态画面 | 52k → **21k** | 40.5% |
| | [ShaderMatch](https://huggingface.co/spaces/Vipitis/shadermatch) | 函数 | [shaders21k](https://arxiv.org/abs/2211.16412) + [Shadertoy](https://www.shadertoy.com/) 接口的函数 → 执行确认 | 202k → **467** | 0.23% |

Retention = 终点 ÷ 起点。3js / blender 只筛标签与星数，没有可运行性检查；SWE 系列、WebCode2M、Objaverse-XL 经过执行或渲染校验。检索计数随时间漂移，引用时锚查询条件。

数据解读：

- **卡住的那一步是执行，不是筛选。** [SWE-rebench](https://arxiv.org/abs/2505.20411) 自己点名：安装与校验只有约 14% 通过，只有 31% 的仓库能装成至少一个任务。
- 人工环节再杀一个数量级。
  - Design2Code：人工检查把 7 千条压到 484 条，这一步只有 6.9%
  - SWE-bench Verified：人工复核判废 68.3%，其中题面欠规约 38.3%、测试误杀正确解 61.1%
- 合成与变异把产能抬一个数量级，但策略之间差 52 倍。
  - [SWE-smith](https://arxiv.org/abs/2504.21798) 组合类策略留存 97.43% 与 96.16%，但只组合已验证补丁，不产生新信息
  - 让模型造 bug 55.98%，重写函数 35.04%，打乱类内方法只有 1.88%；造 bug 比重写函数高 21 个点
  - RST：639 个种子任务经 15 轮扩展得到 37,484 个已验证任务，**每个通过任务约 0.05 美元**；它引用的人工对照是每题数百到数千美元
- 真实素材这条线的产能是三位数，不是五位数（本项目 three.js 路线估算约 230 个任务）。**真实素材当评测集与分布锚点，不当 RL 题库主体。**

口径警告：本项目素材内部自相矛盾。一处要求真实素材占比不低于 30%，另一处算出客观上只能占 0.2% 量级。引用任一条都要标明。

### 2.6 Nine Gates

**闸的顺序比闸本身重要。** 渲染是整条管线的成本瓶颈：

- [WebCode2M](https://arxiv.org/abs/2404.06369) 实测渲染占总耗时约 80%，全程约一个月
- 本项目估算渲 2,000 万页约需 2,000 CPU-day
- 所以长度与结构闸必须排在渲染闸之前

核心发现：九道闸里只有一道有完整的阈值扫描记录，其余要么照抄别人的生产常量，要么必须按自己的库规模重标。

| Policy | Used | Value | Reason |
|---|---|---|---|
| 长度粗筛 | [WebCode2M](https://arxiv.org/abs/2404.06369) · [Design2Code](https://arxiv.org/abs/2403.03163) · [BigDocs](https://arxiv.org/abs/2412.04626) | 640–10,240 字符；> 100k token | 渲染最贵，不先挡掉空页与超长页就白烧 |
| 资产本地化 | [WebCode2M](https://arxiv.org/abs/2404.06369) · [S4](https://arxiv.org/abs/2403.03346) · [Design2Code](https://arxiv.org/abs/2403.03163) | — | 外链离线超时，测到的是网络不是设计 |
| 图片占位 | [Design2Code](https://arxiv.org/abs/2403.03163) · [BigDocs](https://arxiv.org/abs/2412.04626) | — | 图床会失效，[WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) 192 万条因此不可复现 |
| 不可见剪枝 | [S4](https://arxiv.org/abs/2403.03346) · [WebCode2M](https://arxiv.org/abs/2404.06369) | — | 看不见的元素让图码对不齐，[CLAY](https://arxiv.org/abs/2201.04100) 37.4% 屏含无效元素 |
| 去编译产物 | **无出处** | — | 打包代码不是人写的，仅推论 |
| 审美过滤 | [WebCode2M](https://arxiv.org/abs/2404.06369) | < 2 分剔除（剔 52.5%） | 80% 真实页只有 0–1 分 |
| 内容安全 | [WebCode2M](https://arxiv.org/abs/2404.06369) | 0.04（保留 91.3%） | 去色情脏话；0.04 是扫过 0.02 / 0.04 / 0.05 后的选点 |
| 去重 | [The Stack](https://arxiv.org/abs/2211.15533) · [StarCoder2](https://arxiv.org/abs/2402.19173) · [SemDeDup](https://arxiv.org/abs/2303.09540) | Jaccard 0.7–0.85；余弦 0.97 | 重复让指标虚高一倍（[Allamanis](https://arxiv.org/abs/1812.06469)），10% 重复 ≈ 模型小两倍（[Hernandez](https://arxiv.org/abs/2205.10487)） |
| 去污染 | [MultiUI](https://arxiv.org/abs/2410.13824) · [DataComp](https://arxiv.org/abs/2304.14108) | 余弦 0.604，标记约 3% | 评测集与训练集同源 C4 / CC，n 元组挡不住改写 |

数据解读：

- **内容安全是全库唯一完整的「阈值扫描再选点」记录。**
  - 0.02、0.04、0.05 三个点的剔除率与残留率都测了，再选 0.04
  - 其余八道闸没有一家这么做过。该照抄的是这种工作方式，不只是那个数
- **审美闸只能当双侧区间或否决闸，不能当单调排序器。** 三条反向证据：
  1. 经典计算美学指标全都单向可刷：留白更多、边缘更少、颜色更少都分更高，用它做 RL 必然收敛到一张空白单列页
  2. [一项用户研究](https://arxiv.org/abs/2403.13139)：界面越好工具表现越差，准确率 52% → 39%，标注一致性只有 0.112
  3. 口味本身不收敛：[DesignPref](https://arxiv.org/abs/2511.20513) 里 20 名专业设计师判同样 600 对，二元一致率只有 0.624，28.5% 的对分歧超过 96%，在这份数据上训的模型只到 57.45%
  - 推论：任何声称全局审美奖励远高于 60% 的结果，都该先怀疑泄漏
- 不要用通用图文对齐模型当质量闸。
  - [DataComp](https://arxiv.org/abs/2304.14108) 对照：同一精度下它的召回只有 0.02，所以去污染用的是拷贝检测描述子
  - 本项目在 10 个三维模型上实测：它的分数全落在 0.077 到 0.108 的窄带里
- 去重会过头。
  - [FineWeb](https://arxiv.org/abs/2406.17557)：全局去重把 15T 压到 4T，最老的快照被删 90%，相比不去重几乎没有提升
  - 逐快照独立去重得到 20T，持平更强的对照
  - 收益来自打掉跨全部快照、动辄几十万文档的巨型重复簇；**对只有几十个副本的小簇继续去重反而有害**
- 去重的算力几乎免费，阈值却必须随库规模重标。
  - 90 万张图的视觉嵌入约 1.25 GPU 小时；10 万文档的最小哈希约 11 秒
  - 同一阈值下（[ISC2021](https://arxiv.org/abs/2106.09672)），库从 100 万涨到 1,000 万，召回不变，精度从 0.8 跌到约 0.29
  - **照抄前必须按 0.05 分箱人工抽检**

四个缺口：

1. 去编译产物的阈值：全库零命中
2. 滚动触发的懒加载图片：没有任何一家提到
3. 感知哈希的推荐阈值：查不到任何出处，「业界通常取 5 或 8」是传说
4. 合成界面的多样性基线：没有任何工作报告过
   - 可借的通用证据：只要 3% 自生成污染就会崩塌，常规筛选完全无效；召回和多样性比精度衰减得更快
   - **质量闸必须配一个独立的多样性监控器，最好看的页面恰恰最同质**

### 2.7 Reference Thickness

Query 这一侧的另一个变量：参考给到什么程度。

- 参考越厚，模型的任务越收敛，Verifier 能查的东西也越多
- 两者必须同步放宽，否则违反约束 1（信息量约束）

核心发现：五档参考不是难度递进，是**判据来源的替换**。每放宽一档，主判据就从状态断言往感知指标滑一格，而感知指标全部不可靠。

| 参考档 | Query 里有什么 | query 从哪来 | 主判据落在哪 | 素材厚薄 |
|---|---|---|---|---|
| 纯文本 | 只有需求描述 | 真实线上 query 分布；从真实页面反推；专家播种后程序化扩写 | **参考解的运行状态**，噪声地板为 0 | 最厚 |
| 纯图像 | 只有参考图 | 已有配对集；Golden Images 仓库；逆向挖矿 | 逐部件几何、结构回读；**不是像素比对** | 厚，但全是负面证据 |
| 文加图 | 需求加参考图 | 真实需求配真实页面截图；扰动已有场景造「改回去」题 | 状态断言为主，参考图进题面不进 reward | 厚，有唯一一组受控对照 |
| 文加图加视频 | 再加参考录屏 | 交互流程录制 | 输入重放加状态差分；**不是录屏判别** | 中等，本地实测为零 |
| 再加音频 | 再加声音 | — | 音频只能当否决器 | **本地材料未覆盖** |

**纯文本档最干净。** 参考解的状态比参考图信息量大得多，噪声地板为 0。

- 实测：231 个可回读字段里五次重复只有 4 个会变；所有参与判定的字段逐字节相同，两次完整重跑判定翻面 0 次
- 后果：**阈值不能从噪声推，只能按「什么算语义等价」来定**
- 零噪声不是天然的：
  - 几何采样自带的随机源不受全局种子控制，不显式传种子时，参考解和自己比的距离是 0.00167 而不是 0
  - 通过与不通过的带宽只有 0.0016 到 0.0065，噪声地板直接吃掉一半判别力

这一档独有的内容是审美：

- 排除参考集之后分布类指标全部不可用，只能用无参考指标；探针只读计算样式与几何
- 本项目冻结了九条判据：参考页 11 条全过，该挂的抓到 9/11，不该挂的 8/8 零误杀，单次约 0.8 秒纯 CPU
- 别从设计教条里抄阈值。
  - 一个手写的、无障碍检查全过、多视口不塌的参考页，间距落在各基数倍数上的占比：2 的倍数 91.4%、4 的倍数 57.8%、8 的倍数 32.8%、16 的倍数 16.4%
  - **好页面只有 57.8% 的间距落在 4 的倍数上，写死「间距必须是 4 的倍数」的规则会把它判挂**
  - 正确做法：自动选基数再看占比
- 程序化审美判据有上界：UIS-Hunter 的对照里，纯规则检查召回只有 22.9% 到 32.3%，带知识库的检测能到 83.3% 与 92.1%。**它是闸，不是评价体系。**

**纯图像档几乎全是负面证据。** 三条线各自独立测出：像素比对不存在可用的工作点。

| 线 | 实测 |
|---|---|
| Web | 11 个该挂的变异里 **7 个像素完全相同**；最佳阈值也只能做到 14/22；而**该过的重新配色像素差 0.9002，比大多数真实缺陷都大** |
| 图表 | 改一个数据点的像素差只有 **0.75%**，图例互换 0.01%，而**该过的重新配色是 30.51%**；像素层 9/16 且 4 个误杀，对照逐值回读 13/16 零误杀 |
| 3D | **该过的相机移动单图相似度 0.9534，真错误的木色变蓝 0.9844** |

数据解读：**画面变化量和语义错误量完全不相关。**

- 人类一致率：峰值信噪比 57.1%、结构相似度 57.3%，基本等于抛硬币；感知距离 70.7%
- 替代方案四类，都有判别力数字：
  - 逐部件几何 18/22（对照：全局几何分检出 0/11）
  - 逐颜色体素占据 25/29
  - 开放边界边数 0 对 64
  - 结构回读 22/22
- 最该记的一组：杯子平移 30 厘米
  - 全局距离只从 0 变到 0.00018，全局几何分 0.9916（能过 0.99 的闸）
  - 逐部件距离 0.08375，逐部件分 0.2243，差 460 倍
  - **全局平均会被小部件骗穿**

**文加图这一档是判官模型的最佳工况，但主导模态是代码。**

- 唯一一组「同一标注集、只换输入模态」的受控对照：
  - 题面带参考图：判对率 94% 与 97%，检出率 92% 到 95%
  - 只有题面：判对率 68% 与 76%，检出率只有 61% 到 63%，保真率几乎不动（四视角下 39/40）
  - 所以无参考图的判官「几乎不误杀、但一半错误抓不到」，**只能当补抓，不能当闸**
- 加了参考图，主导模态仍然不是图：
  - 只给截图，成对判别掉 9.79 到 10.7 个点；只给代码，只掉 0.31 到 2.60 个点
  - 四档对照：只给代码 79.06 → 加图注 81.74 → 给真图 90.95 → 只给图不给代码 74.94（低于只给代码）
  - **设计类判官的输入必须包含关键源码片段，不能只喂截图**
- 造题形态：扰动即监督
  - 取一个已有场景扰动它，题面给起始场景加目标渲染图，要求改回去
  - 图在题面侧，reward 在状态侧
  - 准入可自动化：**只有被破坏的渲染在官方判据下判失败，才接受这个扰动**

**视频这一档的归谬最干净。** V-GameGym 把交互代码改写成 10 秒自动演示再录屏打分，录屏评分项里还留着「用户输入响应性 0 到 25 分」，而整个过程从来没有发送过任何输入。

- 同向的数字：
  - 同一个基准上，一个前沿模型的三轴分：代码 96.6、图像 17.6、视频 20.7
  - VideoGameBench 用感知哈希逐帧匹配，最好成绩 0.48%，三个保密游戏全部 0%
- 抗欺骗强度排序：**输入重放加确定时钟加状态差分 > 绘制调用拦截 > 引擎自带钩子 > 像素与音频 > 要求模型暴露接口**
  - 末位骗得过，训练时一定会被骗
  - 首位最难骗：要骗就必须真的实现一个会按规则响应输入的系统
- 动画有更便宜的路：
  - 删掉两整条动画曲线，单视角、多视角、距离、体素占据全部给 1.0000，只有逐关键帧断言抓到
  - 时间轴是声明式的，时序正确性走断言，不走视频判别
- 成本也支持这个顺序：一个三轴游戏评测约 900 墙钟小时，真玩占 56.8%、重放占 40.1%、源码检查只占 3.1%
- **录屏判官的输出进诊断，不进 reward。**

**音频这一档本地材料未覆盖。** 全量检索后在题的命中只有 6 处，没有一处是测量、公式、噪声地板或刷分实例。能写的只有三条：

1. 音频在抗欺骗排序里只高于「要求模型暴露接口」
2. 技术上有两个钩子：拦截音频源的播放时刻、读频谱分析节点；能验证的只是「有内容」「没塌」的弱版本
3. 给页面加声音可以豁免浏览器的后台节流，顺带解决动画帧回调在后台不被调用导致的假阳

通用律（来自一家公开承认的模态盲区：模型听不见，所以音乐质检的反馈回路失效）：**判别通道缺失的那个维度，harness 就是瞎的。**
## 3 Verifier

Verifier 评估 Agent 在 Harness 里完成 Omni Reference Query 后交出的代码产物。

### 3.1 Overview

**问题**：一个网页产物，从哪几个维度评、按什么顺序评？

**结论**：**两个维度、五层关卡，前层不过后层不跑**（图 3.1）。

- Functionality（功能性）：需求是否都实现、有没有增量 → L0–L3（L0 能跑是前提）
- Aesthetics（审美性）：好不好看 → L4

本章：3.2 谁来评 → 3.3 功能 → 3.4 审美 → 3.5 验收 verifier → 3.6 前沿对照。

组合规则（Web 与 3D 共用）：

1. 全部满足才算过，不加权（加权会让强项补弱项）；同 [Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) harness「任一维度低于硬阈值即整体失败」，本项目跑通的 verifier 亦然
2. 前层失败即截断：后层依赖前层（不出画面测不了布局），还省成本
3. 题目钉死的项（核心检查）不过直接 0 分；L4 只在全过的作品间排名次
   - 不给部分分：部分分和真实满足的关系接近抛硬币（〔外部〕游戏任务里源码分落在 0 到 1 之间的规则，真玩满足率 54.3%，[A2Z GameSpec-Bench](https://arxiv.org/abs/2609.39564) §4.3）
   - 和组内相对优势（GRPO）怎么拼：组内无人通过 → L4 没有信号；仅 1 人通过 → 排不出名次；全组通过 → 优势全部来自 L4，而 L4 的人类一致率上限约 60%（3.4.2），按 std 归一化会把噪声放大（推断）
   - 本文建议（未实测）：reward = 闸 × (1 + λ·组内胜率)，λ ≤ 1，保证任一通过者高于任一失败者；全通过的组不除以 std，或把参考解放进比较池当锚、不在锚上更新
4. 阈值在跑改坏的样本前冻结；后定的须标出
5. 代价是稀疏：全部满足才给分，reward 近似 0/1，会出现整组全 0 或全 1、没有梯度
   - 〔three.js〕修复题，单一模型、温度 1.0：16 题 × 8 次中 13 题全对或全错，只剩 3/16 = 19% 的题有梯度（Wilson 95% 区间 6.6%–43.0%，本项目实测）；Web 任务未测
   - 组大小 8、通过率 0.1 时，整组全 0 的概率 0.9⁸ ≈ 43.0%（本项目推算）
   - 对策：用要训练的那个模型自己的 pass@k 做难度过滤，配合动态采样；跨模型汇总的通过率会凭空造出中等难度

适用边界：本章判别力数字（22/22、29/29、47/47、18/18）只来自「修复单处破坏」类任务；从零生成时现有检查规则 0/26 组（见 3.5）。

例题：生成一个销售看板网页：标题 32px；一个蓝色的「切换年份」按钮；一张柱状图显示 1–4 月销售额 120 / 150 / 90 / 200；点按钮后图表换成去年的数据。

<figure class="paper-fig">
<svg viewBox="0 0 1000 320" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
<defs>
<marker id="f31a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker>
<marker id="f31r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#dc2626"/></marker>
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
<text x="500" y="94" font-size="16" font-weight="700">L2 布局</text>
<text x="500" y="118">摆得对吗</text>
<text x="700" y="94" font-size="16" font-weight="700">L3 行为</text>
<text x="700" y="118">用起来对吗</text>
<text x="900" y="94" font-size="16" font-weight="700">L4 美学</text>
<text x="900" y="118">好看吗</text>
</g>
<g text-anchor="middle" fill="#0f172a" font-size="12">
<text x="100" y="153">进程状态</text>
<text x="100" y="171">非空白帧</text>
<text x="300" y="153">DOM · 计算样式</text>
<text x="300" y="171">图表数值</text>
<text x="500" y="162">布局几何</text>
<text x="700" y="153">点击 +</text>
<text x="700" y="171">状态差分</text>
<text x="900" y="153">排版检查 +</text>
<text x="900" y="171">两两比较</text>
</g>
<g stroke="#94a3b8" stroke-width="1.5" marker-end="url(#f31a)">
<line x1="182" y1="124" x2="217" y2="124"/>
<line x1="382" y1="124" x2="417" y2="124"/>
<line x1="582" y1="124" x2="617" y2="124"/>
<line x1="782" y1="124" x2="817" y2="124"/>
</g>
<g stroke="#dc2626" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#f31r)">
<line x1="100" y1="186" x2="100" y2="258"/>
<line x1="300" y1="186" x2="300" y2="258"/>
<line x1="500" y1="186" x2="500" y2="258"/>
<line x1="700" y1="186" x2="700" y2="258"/>
<line x1="900" y1="186" x2="900" y2="258"/>
</g>
<rect x="20" y="262" width="960" height="40" rx="10" fill="#fef2f2" stroke="#dc2626"/>
<text x="500" y="288" text-anchor="middle" fill="#dc2626" font-weight="600">不通过 → 0 分，后面不跑</text>
</svg>
<figcaption>图 3.1　Web 的分层关卡：L0–L3 由程序读运行后的状态，L4 先过排版检查再交模型比较；任一层不过即 0 分、后层不跑</figcaption>
</figure>

| Taxonomy | Reward | Detail | Reference | Output | Used | Example |
|---|---|---|:-:|:-:|---|---|
| **L0 执行** | 执行检查 | 能打开、出画面吗 | 任意 | `.html` | [MiMo-V2-Flash](https://arxiv.org/abs/2601.02780) | 不报错、非空白 |
| **L1 结构** | DOM / 样式回读† | 元素属性对不对 | 文本 / 文加图 | `.html` | [WebRenderBench](https://arxiv.org/abs/2510.04097) | 标题是 32px 吗 |
| | 图表逐值回读 | 图表数值对不对 | 文本 / 图像 | `.js`/`.json` | [ChartMaster](https://arxiv.org/abs/2508.17608) | 柱值 120/150/90/200 |
| **L2 布局** | 布局几何 | 摆放对不对‡ | 图像 | `.html` | [WebRenderBench](https://arxiv.org/abs/2510.04097) | 按钮压没压图表 |
| **L3 行为** | 点击 + 状态差分 | 点击反应对不对 | 文本 / 视频 | `.html` | [WebGen-Bench](https://arxiv.org/abs/2505.03733) 等§ | 点按钮后数据换没换 |
| **L4 美学** | 审美检查 + 排序¶ | 好不好看 | 文加图 | `.html` | [UI2Code^N](https://arxiv.org/abs/2511.08195) 等§ | 排版检查后两两比 |

<small style="color:#64748b">† 回读网页元素的 DOM 与计算样式（真实属性）<br>‡ 重叠、出框、多视口不塌<br>§ Used 其余出处：L3 [Interaction2Code](https://arxiv.org/abs/2411.03292)；L4 [Anthropic][hd]<br>¶ 程序审美检查 + 模型相对排序</small>

- 3D 的分层见 3D 页 3.1（场景图、动画曲线、逐部件几何、体素、拓扑）；全局几何见 [CAD-Coder](https://arxiv.org/abs/2505.19713) · [BlenderGym](https://arxiv.org/abs/2504.01786)，不分颜色的体素见 [3D-R2N2](https://arxiv.org/abs/1604.00449)
- L0–L4 是默认分层；游戏等场景可把 L3 拆细，用输入重放 + 状态差分：[PlayCoder](https://arxiv.org/abs/2604.19742) · [GameWorld](https://arxiv.org/abs/2604.07429)

为什么分这几层：

| 层 | 依据 |
|---|---|
| L0 | 不出画面，后面各层都测不了（组合规则 2） |
| L1〔图表〕 | 像素看不出数据错：改一个数据点像素只差 0.75%；逐值回读加结构检查后 16/16† |
| L2〔Blender〕 | 需逐元素比，整体比会被大元素稀释；Web 侧未单独实测，证据是 3D 杯子（3.3.4） |
| L3〔外部〕 | 不发输入测不了行为：[V-GameGym](https://arxiv.org/abs/2509.20136) 打分时从没发过输入；[VideoGameBench](https://arxiv.org/abs/2505.18134) 上最好的模型游戏完成度仅 0.48% |
| L4〔外部〕 | 比较比打分准：普通打分 83.0 → 两两比较 85.5 → 循环赛 86.0‡ |

<small style="color:#64748b">† 本项目实测，见 3.3.4；n = 16（改坏 8 + 换写法 8）× 1 程序 × 1 次：逐值回读单独判对 13/16（抓错 5/8、放对 8/8，漏的 3 个都不是数据错），加结构检查后 16/16（全对）<br>‡ 另有只做监督微调的基线，见 3.3.3；读自论文图 3a，未核实</small>

术语（本章与 3D 页通用）：

| 术语 | 含义 |
|---|---|
| 改坏的样本 | 故意改出真错误，应判挂 |
| 换写法的样本 | 写法变了、结果一样，应判过 |
| 抓错率 | 改坏的样本被判挂的比例 |
| 放对率 | 换写法的样本被判过的比例 |
| Critic | 模型评审：看渲染结果、自己操作页面、输出问题清单的 VLM Agent（打分场景叫「打分模型」） |

谁来评：能交给一个模型吗？→ 3.2

### 3.2 Agentic Critic

**问题**：能不能让一个 VLM Agent 当评审，自己去看、去点、去找问题？

**结论**：能用，但 **VLM 不判题目钉死的属性对不对**；可以在全部通过的作品之间做相对排序（即 L4）；问题清单用来补程序检查（图 3.2）。

<figure class="paper-fig">
<svg viewBox="0 0 1000 290" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
<defs>
<marker id="f32a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/></marker>
<marker id="f32b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2563eb"/></marker>
</defs>
<g stroke-width="1.5">
<rect x="20" y="40" width="170" height="80" rx="12" fill="#f8fafc" stroke="#94a3b8"/>
<rect x="250" y="40" width="200" height="80" rx="12" fill="#f8fafc" stroke="#94a3b8"/>
<rect x="510" y="40" width="190" height="80" rx="12" fill="#eff6ff" stroke="#2563eb"/>
<rect x="760" y="40" width="220" height="80" rx="12" fill="#eff6ff" stroke="#2563eb"/>
<rect x="840" y="196" width="140" height="60" rx="12" fill="#eff6ff" stroke="#2563eb"/>
</g>
<g text-anchor="middle" fill="#0f172a">
<text x="105" y="74" font-size="16" font-weight="700">Generator</text>
<text x="105" y="100" font-size="13">产出代码</text>
<text x="350" y="74" font-size="16" font-weight="700">Harness</text>
<text x="350" y="100" font-size="13">截图 · 录屏 · 点击</text>
<text x="605" y="74" font-size="16" font-weight="700">Critic（VLM）</text>
<text x="605" y="100" font-size="13">看画面、自己操作页面</text>
<text x="870" y="74" font-size="16" font-weight="700">问题清单</text>
<text x="870" y="100" font-size="13">结构化列出发现的问题</text>
<text x="910" y="220" font-size="16" font-weight="700">新增程序检查</text>
<text x="910" y="243" font-size="13">把新问题写成检查</text>
</g>
<g stroke="#94a3b8" stroke-width="1.5" marker-end="url(#f32a)">
<line x1="192" y1="80" x2="247" y2="80"/>
<line x1="452" y1="80" x2="507" y2="80"/>
<line x1="702" y1="80" x2="757" y2="80"/>
</g>
<g text-anchor="middle" fill="#0f172a" font-size="12">
<text x="220" y="70">代码</text>
<text x="480" y="70">渲染</text>
</g>
<g fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#f32b)">
<line x1="930" y1="122" x2="930" y2="193"/>
<path d="M800,122 L800,226 L105,226 L105,123"/>
</g>
<text x="452" y="216" text-anchor="middle" fill="#2563eb" font-size="12">修改：清单反馈回 Generator</text>
</svg>
<figcaption>图 3.2　Agentic Critic：问题清单一路回 Generator 修改，一路沉淀为新的程序检查</figcaption>
</figure>

外部做法：

- 〔外部〕[Anthropic][hd]：生成器与 Critic 分离（质检成本见 3.6）；Critic 用 Playwright 实操页面，不给截图打分；单次运行最长 4 小时、每次生成 5–15 轮迭代；生成器自评会自信地夸自己，调挑剔一个独立 Critic 更容易
- 〔外部〕[OpenAI playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive)：题目要求、实现声明、产物三方合成检查清单，每条声明对应一个看得见的检查，视觉与功能分开记
- 〔外部〕[MiMo-V2-Flash][mimo]：Critic 看录屏而非截图，同时评视觉、功能、能否运行

本项目实测（three.js，Web 侧未测）：48 个带标签样本 × 4 模型 × 2 视角 × 2 次，温度 0，参考图与作品并排†。

<small style="color:#64748b">† 48 = 雪人候选 5 + 雪人改动 13 + 桌子改动 14 + 工作台生成 16（原始实验记录去重）；n = 768；视角 = 单张 / 多角度；「判对 x/96」= 一个模型一种视角的总判对（改坏 + 换写法），分母 48 样本 × 2 次</small>

1. 〔three.js〕比像素准：单个模型判对 74–92 次，分母 84–96（不足 96 是没解析出结论）；像素比对（n = 29 个样本 × 1 次）仅 12/29
2. 〔three.js〕多角度与单张未见差异（强模型上数字更高，但不显著）：两个最强模型 84/95 → 92/96、88/96 → 92/96；同图判两次结论变了的比例 16.7% → 4.2%、8.3% → 0（分母 48）；逐模型都不显著，只能说「未见差异」
3. 〔three.js〕离不开参考图（另一组：47 个样本 × 2 个模型 × 2 视角 × 1 次）：拿掉后总判对率单张 94% → 68%、多角度 97% → 76%，主要掉在抓错（单张 58/63 → 35/56）；无参考图每种视角分母 96（含 2 条重跑），有参考图分母 107、108 超过 47 × 2，来源未核实（每格分母 40–64）
4. 〔three.js〕投票救不回尺寸偏差：桌腿缩到 70%，8 票（4 模型 × 2 次）全判通过，程序检查抓到了
5. 〔three.js〕真正价值是发现漏掉的检查项：雪人头顶没封口，多角度下 8 次判定 7 次判挂，单张全放过；程序检查全漏，于是补了「网格破洞边数」（经过见 3D 页 3.2）

上面全是静帧属性和尺寸类错误，动态 / 交互类错误的抓错率未测。第 1 条与 3.3.2「11 个真错误只抓到 3–6 个」不冲突，见 3.3.2 对照表；VLM 为什么不判钉死的属性、外部直接拿 VLM 当 reward 的反例，也在那里。

检查本身怎么做？→ 3.3

### 3.3 Functionality

**问题**：需求实现了没有，怎么评？

**结论**：用程序检查**读运行后的状态**（L0–L3），不读代码，也不看截图。

#### 3.3.1 How To Evaluate

1. 〔外部〕读运行状态，其他通道都不行（[WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 表 2）

   | 判定方式 | 与真值的相关性 | 坏作品被判过的比例 | 相对成本 |
   |---|--:|--:|--:|
   | 读隐藏的运行状态 | 1.000（真值即由它定义） | 0 | 2 倍 |
   | Agent 自己探索 8 步 | +0.111 | 45.6% | 400 倍 |
   | 只读 DOM | −0.021 | 33.7% | 1 倍 |
   | 截图 + 模型打分 | −0.068 | 3.2%（好作品也几乎全判挂，见 3.3.4） | 50 倍 |

2. 〔外部〕确定性检查才能把模型分开（[3JSBench](https://3jsbench.com/)）
   - 695 条确定性必查项：Astra 80.0% 对 Opus 5.5 49.0%，差 31 个点；同批作品 SigLIP2 相似度均值 0.1081 对 0.1067，只差约 0.001
   - 格式失误伴随低通过率：Gemini 3.8 Flash 300 次里 55 次多包一层 markdown 围栏，剥掉再判，这 55 次仍只 1 次通过
3. 〔three.js〕状态自己去取，不靠模型配合（本项目实测；Web 可直接读 DOM，这条针对 3D 画布）
   - 不让模型把场景挂到约定全局变量（如 [WorldCoder-Bench][wcb] 的 `window.__3D_STATE__`）：训练时模型会学会「写这一行就行」，还能伪造
   - 改用 three.js 自带 devtools 事件通道，页面脚本执行前装好接收端；参考解用的 CDN、importmap、整库打包三种写法实测一致，其他引入方式见 3.5
   - 只认文档里、有尺寸、没隐藏的画布；离屏渲染次数当作弊信号
   - 防作弊：手写 7 个作弊页，初版挡住 6 个（漏的是另起离屏渲染器），修补后 7/7，但修补用的就是这 7 个，不算独立验收；让模型照规则写作弊页（n = 12 = 3 个场景 × 4 个模型 × 1 次），交出的 5 份判过 0 份（另 1 份取不到状态、6 份拒绝或没按格式输出）。每份只试一次、没有梯度、看不到判定结果，只说明这一轮想到的路被堵住，不代表钻不了空子
4. 〔外部〕照抄前沿验收清单：[OpenAI 前端提示文档](https://developers.openai.com/api/docs/guides/frontend-prompt) 给 three.js 产出定了四条：画面不空白、取景对、画面在动、资源不重叠
5. 单层不够，要叠起来（本项目实测）

   | 域 | 样本 | 结果 |
   |:-:|---|---|
   | 〔Web〕 | 单个参考页，n = 22† | 单项抓错最多 4/11；Web 检查五项（W0–W4）‡组合判对 22/22 |
   | 〔three.js〕 | 逐层数字见 3D 页 3.3.1 | 单层各有漏网，四层组合才全中，留出集也全中 |
   | 〔图表〕 | n 见 3.1 依据 L1 | 判对 16/16 |

   <small style="color:#64748b">† 改坏 11 + 换写法 11，含 6 个留出；× 1 程序 × 1 次<br>‡ 与 3.1 的 L0–L4 对应：W0 正确性 ⊂ L0/L1、W1 布局 ⊂ L2、W3 交互 ⊂ L3；W2 可访问性、W4 性能预算在 3.1 没有单列一层，同样读运行后的状态，均属 L0–L3。组合抓错 11/11、放对 11/11</small>

   判别力**多来自修掉「把对的判成错」，而非调阈值**（哪些数看过样本见 3.5 阈值来源表）：
   - 〔Web〕首次 21/22、复跑 22/22，阈值没动；唯一误判的是一个换写法样本（类名全换哈希名），挂在两处：verifier 量列数时绑了类名，改成按结构定位（修 1 处实现）；生成样本的重命名脚本把 ARIA 角色也改了、样本真坏了，改脚本后重新生成（修 1 个样本）。构成仍是改坏 11 + 换写法 11
   - 〔图表〕三个缺陷都是坐标系和帧的问题导致把对判成错，调阈值修不了
   - 〔Web〕反例：确定性信号未必有判别力。对照组「类名序列一致」（朴素做法，不属 L0–L4）抓错 0/11，还把换写法的 3/11 判错

所有状态都查一遍行吗？→ 3.3.2

#### 3.3.2 Insight：Two Backfires

**问题**：程序检查能不能全开？模型打分能不能代替程序检查？

**结论**：都不能。**全开会把对的判成错；模型打分会漏掉错的**，尤其是静帧看不见的属性和小幅尺寸偏差。

<figure class="paper-fig">
<svg viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
<rect x="570" y="30" width="50" height="25" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4 3"/>
<g stroke="#94a3b8" stroke-width="1">
<line x1="120" y1="30" x2="120" y2="280"/>
<line x1="120" y1="280" x2="620" y2="280"/>
<line x1="115" y1="30" x2="120" y2="30"/>
<line x1="115" y1="155" x2="120" y2="155"/>
<line x1="370" y1="280" x2="370" y2="285"/>
<line x1="620" y1="280" x2="620" y2="285"/>
</g>
<g fill="#0f172a" font-size="12">
<text x="108" y="34" text-anchor="end">1</text>
<text x="108" y="159" text-anchor="end">0.5</text>
<text x="108" y="284" text-anchor="end">0</text>
<text x="370" y="302" text-anchor="middle">0.5</text>
<text x="620" y="306" text-anchor="middle">1</text>
</g>
<text x="370" y="330" text-anchor="middle" fill="#0f172a">抓错率（改坏的样本被判挂的比例）</text>
<text x="60" y="155" text-anchor="middle" fill="#0f172a" transform="rotate(-90 60 155)">放对率（换写法的样本被判过的比例）</text>
<rect x="256" y="30" width="137" height="25" rx="4" fill="#faf5ff" stroke="#9333ea" stroke-width="1.5"/>
<circle cx="620" cy="53" r="7" fill="#2563eb"/>
<circle cx="620" cy="280" r="7" fill="#dc2626"/>
<g font-size="13">
<text x="636" y="38" fill="#0f172a">理想区</text>
<text x="636" y="64" fill="#2563eb">只查题目钉死的项（白名单组合）：11/11、10/11</text>
<text x="636" y="276" fill="#dc2626">九类全查：11/11、0/11</text>
<text x="636" y="296" fill="#dc2626" font-size="12">把对的判成错</text>
<text x="324" y="78" text-anchor="middle" fill="#9333ea">模型打分（4 个模型 × 单 / 多视角）</text>
<text x="324" y="98" text-anchor="middle" fill="#9333ea" font-size="12">抓错 3/11–6/11，放对 10/11–11/11：漏掉错的</text>
</g>
</svg>
<figcaption>图 3.3　全开和模型打分各偏一头，只查钉死的项才同时接近右上角（本项目实测，Blender 22 个样本）</figcaption>
</figure>

测试方法（图 3.3）：看能否分开改坏与换写法的样本。Web 侧未单独实测，借用 3D 数据：〔Blender〕台灯场景 22 个 = 改坏 11 + 换写法 11（开发 15 + 留出 7）；「九类」= Blender 场景状态的九类字段（层级、变换、网格、修改器、材质、灯光相机、动画、物理、渲染设置），定义见 3D 页 3.3.1。

1. 〔Blender〕程序检查全开 → 把对的判成错：九类全查抓错 11/11、放对 0/11；只查题目钉死的项抓错 11/11、放对 10/11（细节见 3D 页 3.3.2）。对策：**只查题目里写死的项**
2. 〔Blender〕模型打分代替程序检查 → 漏掉错的（n = 176 = 22 样本 × 4 模型 × 2 视角（单张 / 多角度）× 1 次，温度 0）
   - 四个不同厂家的模型一致：换写法放对 10/11–11/11，**但 11 个真错误只抓到 3–6 个**
   - 多角度拼图无益：四个模型单张 → 多角度总判对（分母 22）16→16、13→14、14→15、14→14，反而更易输出格式出错
   - 模型没有独家抓到的错：这 22 个样本里，模型抓到的程序检查全抓到了
   - 判错有规律：模型分不清「画面变了」和「东西变了」（推断）。题目明说「相机位置变了不算错」，换写法的「相机移动」样本在八种条件（4 模型 × 2 视角）里仍被判错四次
3. 结论还不稳定（温度 0，同一条件跑两次）
   - 〔three.js〕同一模型判两次，结论变了的比例 0–20.8%（3.2 的 48 个样本，分母 48）
   - 〔three.js〕八票（4 模型 × 2 次）多数投票，同上 48 个样本：单视角判对 44/48，多视角 46/48
   - 〔外部〕[WorldBench](https://arxiv.org/abs/2610.10622)：没改动的 32 个条目里 7 个在两次运行间改判（7/32，21.9%）
   - 〔外部〕反推（本项目推算，假设各次独立）：2q(1 − q) = 21.9%，单次偏离常态的概率 q ≈ 12.5%；五票多数投票可压到约 1.6%。这是假设各票独立的结果，实际打分模型犯错相关 0.206（3.3.3），会更高

模型与程序检查对照（本项目实测；「—」= 原始实验记录里没有，Web 侧没测过模型）：

| 样本集 | 域 | n | 模型抓错 | 模型放对 | 程序抓错 | 程序放对 | 出处 |
|---|:-:|--:|--:|--:|--:|--:|---|
| 台灯 22 | Blender | 176 | 3–6/11 | 10–11/11 | 11/11 | 10/11 | 本节 |
| 47，有参考图 | three.js | 107 / 108† | 58/63–61/64 | 43/44–44/44 | — | — | 3.2 |
| 47，无参考图 | three.js | 96 / 96 | 34/56–35/56 | 30/40–39/40 | — | — | 3.2 |
| 三场景 47 | three.js | 47 | — | — | 27/27‡ | 20/20‡ | 3D 页 3.3.1 |
| 参考页 22 | Web | 22 | — | — | 11/11 | 11/11 | 3.3.1 |

<small style="color:#64748b">† 单张 / 多角度；超过 47 × 2，来源未核实<br>‡ 改坏 7 + 9 + 11、换写法 6 + 7 + 7（三个场景的原始记录）；其中 29 个参与过调阈值，与 3.2 的 48 个样本共有 27 个，不是同一批</small>

与 3.2「判对 74–92」不矛盾：three.js 的错误多半看得见；Blender 的 11 个里 5 个（4 个静帧看不见的属性、1 个尺寸偏差）8 种条件下全漏。

〔外部〕反例：有人直接拿 VLM 截图分当 reward，而且有效

| 工作 | VLM 怎么用 | 结果 | 判的是 |
|---|---|--:|---|
| [AesCoder](https://arxiv.org/abs/2510.23272) | 截图分为主、合成 GRPO reward† | InterAes 0.71 → 1.04 | 交互审美‡ |
| [WebGen-Agent](https://arxiv.org/abs/2509.22644) | 截图分 + GUI agent 分当步级 reward | 38.9% → 45.4% | 整体质量 |

<small style="color:#64748b">† GPT-5 截图分权重 0.8，另加执行 0.1、交互 0.1；Qwen3-4B 上的对照是只读代码打分（0.71），1.04 来自「执行 + 截图 + 交互」三项合成 reward，不只是截图分；静态审美分各只涨约 1 分（如 Aes 25.20 → 26.19）。WebGen-Agent 底座 Qwen2.5-Coder-7B<br>‡ 论文没检测钻空子</small>

两者判的都不是题目钉死的属性，和本文立场不冲突：钉死的属性交给程序，整体质量可以交给 VLM 比较。同一底座上「VLM 截图分」对「程序检查 + L4」未测。

非用模型打分不可时怎么用？→ 3.3.3

#### 3.3.3 Insight：Rank, Not Score

**问题**：非得用模型打分时，怎么用？

**结论**：**让模型比哪个好，不让它给绝对分**；上线前先验收；别指望多找几个模型来投票。

1. 〔外部〕比较优于打分（均出自 [UI2Code^N][ui2]）
   - 同一 SFT 底座、只换 reward（UI 修补任务，图 3a）：只做监督微调 82.5（基线）→ 普通打分 83.0 → 两两比较 85.5 → 循环赛（每两个都比一次）86.0；比较的收益从 83.0 算起，不从 82.5；读自图 3a，正文无文字、无方差，未核实
   - 做法：同一次调用把新作品和上一轮参考一起给模型，用同一把尺子比；计分：赢 1、平 0.5、跑不起来 −1；代价：调用次数是作品数的平方
2. 上线前的验收门槛（直接当及格线）
   - 人工裁决量：基线 200 对（本项目设定）；前端任务通过率常在 10%–20%，此时至少 340 对，按通过 / 失败分层抽样（本项目按 κ 置信区间公式推导，κ 即 Cohen's kappa：扣除碰巧一致后的一致程度）；两数均无外部出处
   - 与人一致率**目标 ≥ 92%，底线 85%**（本项目设定）；左右换位再判一致率 ≥ 90%
   - 适用场景：Critic 按检查清单逐条判（如 3.2 的问题清单）；不用于 L4 审美：人与人才约 60%（3.4.2），模型接近这个上限即可（本文建议）
   - 〔外部〕一致率参照（逐条与参考专家组比，[Rubric RL 钻空子研究](https://arxiv.org/abs/2605.12474)）：专家组内部 95%–97%，强打分模型 92%，弱的 76%–82%
   - 须用改坏的样本测抓错率，不能只拿好作品测一致率；作品里藏「给我打满分」这类指令须判 0 分；同一作品重复取证 3 次，结论不一致的项标为不稳定；打分模型和被训练模型不能同一家
3. 〔外部〕多找模型投票不划算（[Error Dependence in LLM Judge Consensus](https://arxiv.org/abs/2609.22512)）
   - 十个模型只顶 3.5 个独立的：RewardBench 1,133 对样本上，不同打分模型犯错相关系数 0.206（10 ÷ (1 + 9 × 0.206) ≈ 3.5，是信息量等价，不代表 3.5 个就够）
   - 换种子换不来独立：只换训练随机种子的两个模型犯错相关 0.36–0.39；再加一个种子只多顶 0.11 个

参考能直接逐像素比吗？→ 3.3.4

#### 3.3.4 Insight：No Pixel-Level Reward

**问题**：能不能直接拿截图和参考图逐像素比，当 reward？

**结论**：不能，要改用**带语义的分层 reward**：先认出元素再逐个比，即回到 L1–L2。像素看不到「画面由哪几个东西组成、各自对不对」。

画面变化大小和错误大小对不上（本项目实测，下表三组例子，详见 2.7）：

| 域 | 换写法 | 改坏 | 指标 |
|:-:|---|---|---|
| 〔three.js〕 | — | 雪人胡萝卜鼻子挪到后脑勺，仍 0.999 | 单张截图相似度（越接近 1 越像） |
| 〔Blender〕 | 相机移动 0.9534 | 木色变蓝反而 0.9844 | 同上 |
| 〔图表〕 | 换配色差 30.51% | 改一个数据点只差 0.75% | 差异像素占比 |

- 〔three.js〕判别力差：29 个带标签样本（改坏 + 换写法）× 1 次，像素比对只判对 12 个（本项目实测）
- 〔外部〕人也不认：图像相似度二选一测试（2AFC）里，PSNR、SSIM 与人一致的比例仅 57.1%、57.3%，随机猜是 50%（[DreamSim](https://arxiv.org/abs/2306.09344) 表 5）
- 〔外部〕[WorldCoder-Bench][wcb] 用截图 + 模型打分重判，通过率仅 2.7%，原文说它「不加区分地惩罚视觉差异」；[UI2Code^N][ui2] 直接拿 CLIP 相似度当 reward，在 Design2Code 和 Flame 上都不如只做监督微调
- 〔Blender〕分层的好处：杯子平移 30 厘米，全局 Chamfer 距离（两组点云间的平均最近距离）只变 0.00018，逐部件算变 0.08375，差 460 倍（本项目实测；Web 侧未单独实测「逐元素比 vs 整页比」）

好不好看怎么评？→ 3.4

### 3.4 Aesthetics

**问题**：好不好看，怎么评？

**结论**：**一半能用程序查，做成硬关卡；另一半交给模型比较，只设上下限。**

#### 3.4.1 How To Evaluate

1. 〔Web〕程序能查的一半：只读计算样式和几何，共 11 条（排版层级、字号尺度、字体族数、行高、间距节奏、色相数量、对比度等）；阈值在参考页上测出，加余量后冻结
   - 单个参考页；n = 19（只坏审美 11 + 换写法 8）× 1 程序 × 1 次；只坏审美原有 12 个，1 个（去掉限宽）在参考页上不构成缺陷，按冻结规则剔除

   | 样本（本项目实测） | 指标 | 审美检查 | 功能检查 |
   |---|:-:|--:|--:|
   | 参考页 | 通过 | 11 条全过 | 全过 |
   | 只坏审美的 11 个 | 抓错 | 9/11 | 2/11（均为顺带抓到） |
   | 换写法的 8 个 | 放对 | 8/8 | 8/8 |
   | 每个样本 | 耗时 | 约 0.8 秒 | 约 4.9 秒 |

   - 功能检查看不见：标题层级反了、字号乱、四种字体混用、行高压到 1.02、间距全是奇数、边距全抹掉
2. 〔Web〕11 条里两条不能当关卡：圆角一致性（参考页本就有四种圆角，余量不够）、栅格对齐（见 3.5）。进关卡的 9 条里独立验证过的 7 条：层级、字号尺度、字体族数、行高、色相、对比度、间距；行长没验证判别力，墨水覆盖率总被间距先抓到（按判定代码计）
3. 〔Web〕别写死设计教条，基数要从页面自身测：手写参考页（n = 1 页）的间距仅 57.8% 落在 4 的倍数上，基数取 2 时命中 91.4%（本项目实测）；关卡阈值是占比 ≥ 0.70
4. 〔外部〕经典计算美学指标不能用：对称、平衡、密度都能单向推高，最优解是空白单列页
   - [Salimun 2013](https://theses.gla.ac.uk/4256)：72 人实验，指标最高的布局最不受欢迎，最受欢迎的是中等对称
   - [Purchase et al. 2011](https://eprints.gla.ac.uk/54578)：14 项指标放到真实网页上，只有 1 项和好不好看对得上
   - [Duan et al. CHI 2024](https://arxiv.org/abs/2403.13139)：设计越改越好，模型反馈准确率从 52% 掉到 39%
5. 〔外部〕[Anthropic][hd] 的「工艺」维度（排版层级、间距一致、配色和谐、对比度）：前三项能程序查，配色和谐不能（推断）；官方因模型默认就及格而降了它的权重；本文建议进了强化学习**它应当是硬关卡**：降的是排序比重，不是关卡位置

美学分能越高越好吗？→ 3.4.2

#### 3.4.2 Insight：Aesthetics Band

**问题**：美学能不能当 reward 里的一个分数？

**结论**：**只能设上下限（太素、太花都挂）或一票否决，不能分越高越好**（图 3.4）。

<figure class="paper-fig">
<svg viewBox="0 0 1000 320" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, -apple-system, 'PingFang SC', sans-serif" font-size="14">
<defs>
<marker id="f34r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#dc2626"/></marker>
</defs>
<g text-anchor="middle" fill="#0f172a" font-size="16" font-weight="700">
<text x="260" y="28">分越高越好</text>
<text x="760" y="28">只设上下限</text>
</g>
<g stroke="#94a3b8" stroke-width="1">
<line x1="70" y1="50" x2="70" y2="260"/><line x1="70" y1="260" x2="450" y2="260"/>
<line x1="570" y1="50" x2="570" y2="260"/><line x1="570" y1="260" x2="950" y2="260"/>
</g>
<g fill="#0f172a" text-anchor="middle">
<text x="260" y="290">某审美指标（如装饰量）</text>
<text x="760" y="290">同一审美指标</text>
<text x="45" y="155" transform="rotate(-90 45 155)">reward</text>
<text x="545" y="155" transform="rotate(-90 545 155)">reward</text>
</g>
<path d="M80,250 C200,235 320,160 432,72" fill="none" stroke="#9333ea" stroke-width="2.5"/>
<path d="M300,196 L400,118" fill="none" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#f34r)"/>
<text x="372" y="180" fill="#dc2626" font-size="12">训练往这头推</text>
<circle cx="434" cy="70" r="7" fill="#dc2626"/>
<text x="440" y="52" text-anchor="end" fill="#dc2626" font-size="12">极端：堆满描边与重复装饰</text>
<rect x="88" y="62" width="214" height="84" rx="8" fill="#ffffff" stroke="#94a3b8"/>
<g fill="#0f172a" font-size="12">
<text x="100" y="84" font-size="13" font-weight="600">RULER · SVG 图标</text>
<text x="100" y="104">美学分 4.424 → 6.210</text>
<text x="100" y="122">按检查项算的分 0.395 → 0.262</text>
<text x="100" y="140">输出长度 0.3k → 6.3k</text>
</g>
<rect x="680" y="60" width="160" height="200" fill="#faf5ff"/>
<g stroke="#9333ea" stroke-width="1" stroke-dasharray="4 4">
<line x1="680" y1="60" x2="680" y2="260"/><line x1="840" y1="60" x2="840" y2="260"/>
</g>
<path d="M572,250 H680 V90 H840 V250 H948" fill="none" stroke="#9333ea" stroke-width="2.5"/>
<text x="760" y="160" text-anchor="middle" fill="#9333ea" font-weight="700">区间内：通过</text>
<g fill="#dc2626" text-anchor="middle" font-size="13">
<text x="625" y="236">太素：挂</text>
<text x="894" y="236">太花：挂</text>
</g>
<g fill="#0f172a" text-anchor="middle" font-size="12">
<text x="680" y="276">下限</text>
<text x="840" y="276">上限</text>
</g>
</svg>
<figcaption>图 3.4　美学 reward 的两种形状：分越高越好会被推到极端（左，RULER 实测）；只设上下限则太素、太花都挂（右，示意）</figcaption>
</figure>

1. 〔外部〕人自己都判不一致，上限约 60%
   - [DesignPref](https://arxiv.org/abs/2511.20513)：20 位职业设计师判同样 600 对，两两一致率仅 62.4%，一致性系数 0.248；在这份数据上训的模型：所有人一起训 57.45%，按个人训 60.16%
   - 论文原话：28.5% 的对子，设计师间两两分歧率不低于 96%。论文没定义这个量；按二选一常规定义，20 人时两两分歧率最高约 52.6%（10 人对 10 人：10 × 10 ÷ 190），故此口径存疑
2. 〔外部〕分越高越好的美学分会被模型钻空子（[RULER](https://arxiv.org/abs/2609.25270)，SVG 生成，只换 reward）
   - SVG 图标（Icon）子集上用 CLIP + 美学 + HPS 加权分当 reward：美学分 4.424 → 6.210；按具体检查项算的分 0.395 → 0.262，低于训练前；输出长度 0.3k → 6.3k（21 倍），堆满层层描边和重复装饰（图 3.4 左）
   - 换成更严的结构化评分表（Rubric-S）后，钻空子换了花样：把题目里的词画成风格化标签
3. 「AI 味」（模型产出千篇一律）只能在一批作品上看，不能看单个
   - 集中度：一批页面的样式取值（如字体）有多集中，越高越单调
   - 〔外部〕单页只能查点名的默认值：Inter 字体、白底紫渐变（[Anthropic 前端设计博客](https://claude.com/blog/improving-frontend-design-through-skills)）
   - 〔Web〕反例（本项目实测，两批各 11 / 12 页，样本小）：一批 100% 用 Inter，字体集中度 0.50；另一批一次没用，集中度 1.00，反而更单调
   - 〔外部〕旁证：[Generative UI](https://arxiv.org/abs/2604.09577) 的系统指令点名推荐字体；Anthropic 与 OpenAI（[GPT-5.4 前端博客](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)）都归因于高频模式收敛；文字创意测验（非网页）上模型间差异度 0.459、人与人 0.738，单条原创性 0.711 对 0.696，整体趋同而单条不差（[Wenger & Kenett](https://arxiv.org/abs/2501.19361)）
4. 评测上省钱
   - 〔外部〕多出题比多找人划算：评分人从 3 个加到 16 个，人力 5.3 倍，题量只省 30%（本项目按 [AUV-Bench](https://arxiv.org/abs/2609.34854) 的一致性系数估算）
   - 〔Web〕美学上 30 道题 × 每题 8 次，能分辨的最小差距至少约 15.4 个百分点（公式没算题间方差，是下界）；要分辨 5 个点需两千多次，不划算（本项目按二项分布估算，含打分模型噪声）

这些检查本身靠谱吗？→ 3.5

### 3.5 Discrimination

**问题**：怎么知道 verifier 本身靠谱？

**结论**：上线前量它能不能分清好坏，训练中盯着模型钻空子，再守住两条原则。

1. 上线前三个指标就够：抓错率、放对率、Youden 指数（= 抓错率 + 放对率 − 1），各配置信区间（与 3D 页同一说法）
   - 一般给 Wilson 95% 区间（小样本下更稳的比例区间）；一次都没出错时，出错率的 95% 上界 ≈ 3 ÷ n
   - 例：3D 留出集 18/18，上界 ≈ 3 ÷ 18 ≈ 16.7%，Wilson 95% 下界 82.4%，两种算法相近
   - 抓错率、放对率分开给（Wilson 95% 下界为本文推算）：

     | 样本集 | 抓错 | 放对 | Wilson 95% 下界（抓错 / 放对） |
     |---|--:|--:|---|
     | 〔Web〕参考页 22 | 11/11 | 11/11 | 74.1% / 74.1% |
     | 〔Web〕审美 19 | 9/11 | 8/8 | 52.3%（上界 94.9%）/ 67.6% |
     | 〔图表〕16 | 8/8 | 8/8 | 67.6% / 67.6% |
     | 〔three.js〕留出 18（小车） | 11/11 | 7/7 | 74.1% / 64.6% |

   - 有效样本数：18/18 是一个场景（小车）的 18 个改坏 / 换写法样本，22/22 是一个参考页上的，跨场景 / 跨页面的独立样本数都是 1；82.4% 只对该场景的这批样本成立，换场景没有统计保证（跨页留出未测）
   - 准入：修复题的初始状态（什么都不改）必须判挂，否则原样交回也能拿分；本项目尚未补上这条
   - 取证链路单独验收：截断会放大 Harness 自身的漏洞。〔three.js〕模型用经典脚本标签、另一个 CDN 路径或自带 addon 引入库时，Harness 没覆盖，正确产物在 L0 直接判 0，看起来像「模型连页面都写不对」（本项目实测）；所以要拿真实策略的产出（不是参考解）验收 Harness 覆盖面；L0 失败要抽检（本文建议）
2. 训练中盯着钻空子
   - 〔外部〕**平均分在涨，不代表没人钻空子**：Safety VQA、32B 模型上，26.4% 的样本比基线更差（[Multimodal Reward Hacking](https://arxiv.org/abs/2607.09492)）
   - 〔外部〕停训信号看「训练用的打分」与「独立打分小组」的差距（[Rubric RL 钻空子研究](https://arxiv.org/abs/2605.12474)）：差距峰值在独立小组分数见顶后 100 步内；训练用的打分到最后一个检查点都没见顶，单看它永远不知道该停
   - 〔外部〕钻空子来得早、涨得快：人为注入偏置的实验里，第 68–478 步开始钻空子，之后 100 步内捷径行为发生率至少再涨 40%（[CHERRL](https://arxiv.org/abs/2606.04923)）
   - 〔外部〕模型认得出表面形式的钻空子，认不出内容层面的：检测代码环境钻空子的匹配率，改测试、覆盖率游戏类 0.6–0.95，风格操纵、信息泄露类仅 0.0–0.4（[TRACE](https://arxiv.org/abs/2601.20103)）
3. 两条原则
   - 「能分开该挂的和该过的」≠「能当关卡」：还要看离边界多远、好作品落在哪侧、极端情况会不会反过来
     - 〔Web〕例（栅格对齐，本项目实测）：3.4.1 那批 19 个有效样本（另有参考页；原始 20 个改动中 1 个判为无效）：参考页 0.824；改坏的三个 0.707、0.794、1.000（1.000 那个边距全抹掉、全贴左边）；换写法且更好看的 1 个 0.765；其余 15 个同参考页 0.824
     - 只有 0.707 能和 0.765 分开，间距 0.058；0.794、1.000 反落在好页面之上，一条阈值分不开 → **不能当关卡，只留作参考指标**
   - 规则在哪个样本上调出来，就不能拿它证明规则好用：〔three.js〕「网格破洞边数」是在雪人场景一个样本上调出的，所以「加了之后雪人 13 个样本 13/13」不算独立验证（本项目实测）；同理，调规则用的改坏样本不能再拿来验收

阈值来源（本项目；「前 / 后」= 定阈值时有没有看过带标签样本）：

| 阈值 | 值 | 怎么定 | 看样本前/后 | 有无独立验证 |
|---|---|---|:-:|---|
| 〔Web〕检查五项（W0–W4）† | 如溢出 ≤ 1px‡ | 只在参考页上校准 | 前 | 无 |
| 〔Web〕审美检查 | 如字体族 ≤ 2‡ | 参考页实测加余量 | 前 | 无 |
| 〔图表〕逐值回读 | 误差 ≤ 1% | 自比 0.15%，留 6 倍余量 | 前 | 无§ |
| 〔Blender〕图像相似度 | ≥ 0.995 | 按「什么算等价」定 | 前 | 有：12/22 |
| 〔Blender〕剪影交并比 | ≥ 0.97 | 同上 | 前 | 有：14/22 |
| 〔Blender〕点云距离 | ≤ 对角线 0.4% | 同上 | 前 | 有：13/22 |
| 〔Blender〕体素交并比 | ≥ 0.80 | 同上 | 前 | 有：15/22 |
| 〔Blender〕逐部件 F 分数 | ≥ 0.99 | 换写法下限 0.9989 反推 | 后 | 无 |
| 〔three.js〕剪影 / 体素 | 0.9 / 0.9、0.5 | 雪人上定，桌子上复验 | 后 | 留出 18/18 |
| 〔three.js〕分块 / 颜色 | 0.5 / 距离 60 | 在带标签样本上扫过或补加 | 后 | 留出 18/18 |

<small style="color:#64748b">† 与 L0–L4 的对应见 3.3.1 表注<br>‡ 检查五项另如重叠比 ≤ 0.05；审美检查另如间距占比 ≥ 0.70<br>§ 自比 = 参考解与自己比；「回读或结构」组合规则是看过各自漏哪几个后选的，没做留出<br>有无独立验证：「有」后为该阈值单用的判对数（满分 22）</small>

**组合判定唯一的独立证据是 3D 留出集 18/18**：换一个场景、标签先写死、阈值一个没动（Blender 先冻结的四个阈值单用也算独立，但只判对 12–15/22，见 3D 页 3.5）。其余满分或接近满分的数字都参与过调试：

- 22/22（Web）：阈值没在样本上调，但首次 21/22，修 1 处实现、重新生成 1 个样本后复跑才全对；6 个留出也在这两次里
- 29/29（three.js 雪人 + 桌子）：剪影、体素、分块、颜色阈值都在这批样本上定或调过
- 47/47 = 29 + 18：只有 18 个独立
- 21/22（Blender 白名单组合）：组合成员看过开发集才选，F ≥ 0.99 是后定的

适用边界：以上数字都来自「修复单处破坏」类任务，换到从零搭建就不成立（〔three.js〕本项目实测）

| 检查规则 | 修复单处破坏 | 从零搭建 |
|---|--:|--:|
| 现有（比对参考的绝对几何） | 47/47 | 0/26 组（抽看 4 个，人看都对，也判挂） |
| 相对关系原型（个数、接触、比例） | 35/47 | 13/80 次（现有规则 0/80） |

<small style="color:#64748b">32 组（场景 × 模型 × 描述方式）中有效 26 组（纯文本 / 加参考图各 13 组），每组最多 3 轮；13/80 按同一批实验的每次尝试计，80 的精确构成原始记录未交代（未核实）。从零任务的需求没钉死尺寸，「和参考重合」不再等于「满足需求」；修复任务天然没有「部分做对」，这也可能是 3.1 规则 5 难度两极分化的来源（推断）；13/80 里有多少人看也对，未测</small>

外推边界：Web 结论来自一个手写参考页、断网、冻结时钟、同一浏览器版本；真实网页的外部资源、字体、动效和跨浏览器版本都未覆盖（未测）。[WebRenderBench](https://arxiv.org/abs/2510.04097) 用 45.1K 真实门户页从渲染结果算布局 reward，可作扩展方向。

前沿实验室也这么做吗？→ 3.6

### 3.6 Frontier Lab

**问题**：前沿实验室的 verifier 怎么做？

**结论**：训练方法没公开；但**环境和检查规则的做法公开了，和 3.1–3.5 一致，可以直接照抄**。

〔外部〕披露情况（下表均为外部资料）：西方三家都没公开视觉编码的训练数据和强化学习环境；国内披露最多，且结构一致。

| 来源 | 披露了什么 | 没披露什么 | 出处 |
|---|---|---|---|
| Anthropic harness | 生成与评审分离、few-shot 校准评审、Playwright 实操后打分† | 前端与 3D 专项数据、RL 环境、视觉 reward 模型 | [harness 设计博客][hd] |
| Anthropic 前端 | 「分布收敛」归因；frontend-design skill | 同上 | [前端 skill 博客][fd] |
| OpenAI 模型 | 仅几句，提到 UI 与 computer use 训练§ | 数据来源、设计偏好数据、内部评测集 | [GPT-5.4 前端博客][g54] |
| OpenAI Astra | 特效开关的像素差分、渲染计数器、90 个帧间隔采样 | 同上 | [Astra 游戏博客](https://developers.openai.com/blog/how-to-build-games-with-astra) |
| Google | RL 并用可验证与生成式奖励；加入端到端 web 与移动应用任务 | WebDev 数据来源、审美 reward 模型 | [Gemini 2.5 技术报告](https://arxiv.org/abs/2507.06261) |
| Kimi K2.5 / K3 | 代码↔渲染配对预训练（K3 扩到 3D、游戏、CAD）；RL 先过确定性检查，构建失败或伪造实现记 0 | 3D 侧 reward | [Kimi K2.5](https://arxiv.org/abs/2602.02276) · [Kimi K3](https://arxiv.org/abs/2607.24653) |
| Qwen3-VL | 代码↔渲染配对预训练 | RL 环境 | [Qwen3-VL](https://arxiv.org/abs/2511.21631) |
| MiniMax-M2 | 数据过滤在真实沙箱里跑 | — | [MiniMax-M2](https://arxiv.org/abs/2605.26494) |
| MiMo-V2-Flash | 沙箱过滤；看录屏判别 | 3D 专项数据 | [MiMo-V2-Flash][mimo] |

<small style="color:#64748b">† 前端实验四维加权、5–15 轮迭代；全栈实验四维各设硬阈值<br>§ 原话：「专门训练过 UI 与图像使用」「为 computer use 训练，可配合 Playwright 反复检查自己的产物」；出处另见 [GPT-5.6 发布页](https://openai.com/index/gpt-5-6/)</small>

国内各家都没有披露 Blender 方向的训练数据（推断）。

1. 〔外部〕训练方法：**Anthropic 与 OpenAI 怎么训视觉编码，公开资料里是空白**（素材均已核对）
   - 本项目整理的 2,116 行一手资料汇编（Anthropic + OpenAI）搜不到蒸馏、教师模型、监督微调、人类反馈、冷启动、中训、GPU 小时、样本效率
   - 四份 Anthropic 系统卡逐节通读，搜不到审美、前端、视觉设计、样式表、Web 开发；两篇 OpenAI Astra 博客没出现「训练」一词
   - OpenAI 说训练过「用工具检查自己的产物」但没说怎么训；Anthropic 与 Google 只当它是产品功能

2. 〔外部〕环境与检查规则

   | 内容 | 一手数字 | 出处 |
   |---|---|---|
   | 规模 | 约 150 万条训练过程记录、数千个训练环境† | [Opus 5 系统卡 §6.3](https://www.anthropic.com/claude-opus-5-system-card) |
   | 环境分级 | 按钻空子的风险分高低两组 | [Fable 5 / Mythos 5 卡 §6.4.2](https://anthropic.com/claude-fable-5-mythos-5-system-card) |
   | 跨模型比较 | 只用三个模型都跑过的环境比钻空子比例 | [Opus 5.5 系统卡 §6.2](https://www.anthropic.com/claude-opus-5-5-system-card) |
   | 坏题的代价 | 缺文件、做不成的题：尝试钻空子的比例高 3–6 倍‡ | 同上 §6.2.2 |
   | 怎么处理 | 环境有问题、做不了的题：修环境，不修模型 | 同上 |
   | 模型猜检查规则 | 按猜的规则改答案 2/695；主动找线索 1/695§ | 同上 |
   | 质检划不划算 | 只占整套运行成本的 8.3%，每轮都找出真问题 | [harness 设计博客][hd] |

   <small style="color:#64748b">† 均为最终阶段；约 400 条由多个 Claude 模型通读，人只核对关键论断<br>‡ 缺文件、不可能完成的题；缺文件的题钻空子成功率高 1.5–3 个百分点（均为通用钻空子分类器测得）；「明知没做完还交」占这些尝试的约 80%；「怎么处理」一行指官方的做法<br>§ 模型猜检查规则的频率；猜中标准答案并成功的约 0.3%<br>「Fable 5 / Mythos 5 卡」即 Fable 5 / Mythos 5 系统卡</small>

   最关键的是坏题的代价：**先清理坏题，再调模型**（推断）；配套给模型留「这题有问题」的出口，不禁止它提问。

3. 〔外部〕可以照抄的做法（按来源；打分模型不能与被训模型同一家，见 3.3.3）

   | 出处 | 做法 |
   |---|---|
   | [Anthropic eval 设计博客](https://claude.dev/blog/automating-eval-design-and-hillclimbing/) | 每个检查项都须在题目里说出来；写成程序检查，不写五分制 |
   | 同上 | 好题 = 两个领域专家会给出同样判断的题 |
   | 同上 | **分数一直不涨的题，是题或检查规则坏了** |
   | 同上 | **评测的波动必须小于值得采取行动的最小提升** |
   | 同上 | 同一作品判两遍看结论变不变；机器故障与模型本身的波动分开统计 |
   | [OpenAI playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) | 题目、实现、意图里的每个要求至少对应一个检查项 |
   | 同上 | 视觉上重要但主观的要求转成看得见的检查项，不能略过 |
   | 同上 | 视觉检查与功能检查分开：功能过了不等于视觉过了 |
   | [harness 设计博客][hd] | 任一项低于及格线即整体不及格；默认就能及格的项降权 |
   | [GPT-5.4 前端博客][g54] | 能数的硬约束写具体数目，如最多两种字体等† |
   | 同上 · [Astra 游戏博客](https://developers.openai.com/blog/how-to-build-games-with-astra) | 故意删掉一部分，看检查规则会不会跟着变‡ |
   | [Opus 5.5 系统卡 §8.14.5](https://www.anthropic.com/claude-opus-5-5-system-card) | 被安全拦截挡下的尝试单独报出，并算作失败 |
   | [长程 harness 博客](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 规则和状态存成结构化文件（如 JSON），模型不太会篡改 |

   <small style="color:#64748b">† 一个主标题、不超过六个区块、最多两种字体、一个强调色、首屏一个主按钮<br>‡ 删图片、藏导航、去边框阴影、砍三成文案、开关特效</small>

4. 〔three.js〕不照抄的一条：要求模型主动暴露运行时状态接口。本项目**让检查规则自己去读状态，不让作品为了被检查而改写法**（理由见 3.3.1「状态自己去取」）

5. 〔外部〕**只靠模型自评来造训练信号行不通**，三方面一手证据：
   - 自评会夸自己的作品（见 3.2）
   - 会说检查过了其实没有（[Fable 5 / Mythos 5 系统卡 §2.3.3.2](https://anthropic.com/claude-fable-5-mythos-5-system-card)）：内部使用审计的 886 个会话里 16 个「说做完了或验证过了，其实没有」；系统卡没把它归因于强化学习
   - 自我检查又会过头（[Opus 5 系统卡 §2.2.6](https://www.anthropic.com/claude-opus-5-system-card)）：24 小时蛋白设计实验，目标 30 个；Mythos 5 交齐 30 个；Opus 5 一组只交 17 个未排序的，另一组什么都没交，最后 8 小时没有输出，卡在自我验证循环里
   - 所以裁剪训练过程时，**该剪的不是改错本身，而是没有新信息的反复检查**

[hd]: https://www.anthropic.com/engineering/harness-design-long-running-apps
[ui2]: https://arxiv.org/abs/2511.08195
[mimo]: https://arxiv.org/abs/2601.02780
[wcb]: https://arxiv.org/abs/2606.01869
[fd]: https://claude.com/blog/improving-frontend-design-through-skills
[g54]: https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4

## 4 Harness: Many Assets, No Repository

- SWE 类 harness：一个实例一个镜像，整个仓库连依赖冻进去，模型进去改代码、跑测试。
- 视觉生成类：沙箱里**参考素材很多，代码仓库几乎没有**，上下文短一个数量级。
- 这个差别直接决定 rollout 单价，下面量化。

### 4.1 The Asset-Heavy, Repo-Free Shape

核心发现：视觉生成的镜像按依赖集共用，SWE 的镜像按实例独占。

| 维度 | SWE 类 | 视觉生成类 |
|---|---|---|
| 素材供给 | 爬 PR，一条任务一段补丁 | 成对、单文件：three.js 素材线 610 个页面对 610 张截图 |
| 单条体积 | 仓库级 | 每条中位数 6,137 字节 |
| 镜像组织 | 一实例一镜像 | 一依赖集一镜像，挂几百道题 |
| 环境侧总量 | SWE-smith 每实例约 6 MB × 50,137 条 | Web 层固定约 0.6 GB，不随题数增长 |
| 启动 | 起容器 + 装依赖 | 浏览器 172 到 191 毫秒，场景载入 401 到 420 毫秒，复用页面 50 毫秒 |

上下文对照：

| | 本项目视觉编码轨迹 | 公开 SWE agent 轨迹 |
|---|---|---|
| 累计输入 token | 约 1.06 M | 5.55 M |
| 输出 token | 约 32 k | 32.5 k |
| 步数 | 40 | 111.2 |

- 输出几乎一样，输入差 5 倍，步数差 2.8 倍。
- **累计输入约为步数的平方量级**：每一步都重带前面所有观测。
- 所以控成本的首要旋钮是步数，不是分辨率。
- 图像只占累计输入的 8%：三张常驻多视角拼图 2,109 token，40 步累计约 84 k。砍小图省不了多少。

### 4.2 Determinism Is A Ladder With A Hard Top

判据可复现的前提是产物可复现。无头浏览器上的阶梯实测：

1. 不控制：三次全不同。
2. 只装虚拟时钟：仍三次全不同，页面加载耗时 113 到 432 毫秒漏进时间源。
3. 加暂停、定长推进、种子化随机：20 次里剩 2 种。
4. 页面主动暴露时间钩子 + 直接读画布像素：**三次逐字节一致**。

综合基线：可观测字段共 231 个；固定视口、固定设备像素比、关字体微调、镜像内打包固定字体并禁止联网拉字体后，只剩 4 个字段会变。

阶梯的硬顶：

- **工作线程里的时钟拦不住。** 用到它的样例只能整批排除，本项目为 225 条。
- **断网会造成假阳性。** 封外链能稳住渲染，也会封掉注入判据的那一路，「判据没跑」被读成「判据通过」。
- **跨引擎版本的逐字节一致从没测过。** 反向证据：超越函数跨引擎版本会发散，某物理库相隔较远的两个版本结果不同。版本要钉死。
- **种子不是万能的。** 固定种子能把布局噪声从 0.00167 压下去，但它本就小于该任务判据容差 0.0046，收益在该量程上读不出来。

翻面基线留作对照：

- 未改动的题单次重跑仍有 **7/32 翻面**。
- 数据质量门禁：抖动不超过 1%；超了先修确定性，再谈阈值。

### 4.3 Visual Verification Does Not Need A GPU Sandbox

核心发现：视觉验证单价是毫秒到秒级，不需要 GPU。

| 配置 | 吞吐 | p50 |
|---|---|---|
| 1 浏览器 1 页 | 2.4 任务/秒 | 383 毫秒 |
| 4 浏览器 8 页 | 11.6 任务/秒 | — |
| 8 浏览器 8 页 | 14.3 任务/秒 | 4.1 秒 |

- 组织方式比机器重要：单进程逐题起浏览器 3.6 任务/秒，复用浏览器 14.3，差 4 倍。
- 单条耗时：three.js 383 毫秒、Blender 2.3 秒、Web 页面 4.9 秒、图表 840 毫秒。
- 单位成本：3.35、24.7、56.3 核秒。
- 一轮 1024 条 rollout：多轮 three.js 要 43 核，单轮 Blender 要 1670 核，**差 39 倍，来自技术栈而非算法**。
- 公开世界唯一一份「渲染型判据在 RL 里的耗时占比」：75.4% 生成、22.4% 渲染、2.2% 比对。瓶颈是生成，不是渲染。

GPU：

- 三类技术线都能在无 GPU、无显示的机器上完整渲染。
    - 浏览器走软件光栅后端。
    - Blender 多个版本都能跑三种渲染引擎。
- 公开沙箱平台**没有一家写明支持「GPU 加图形栈」**；要真 GPU 光栅得自己做镜像，CPU 方案省掉这一整套。
- 坑：新版浏览器不显式开启就建不出 WebGL；顺手关 GPU 的那个开关会把软件渲染后端一起关掉。

### 4.4 Give The Agent Structured Observations, Not Screenshots

核心发现：最便宜、信号最强的自检工具都不是图。

| 工具 | 成本 |
|---|---|
| 读场景图 | three.js 1.8 毫秒，Blender 0.1 到 1 毫秒 |
| 读控制台 | 近乎免费；抓到一条资源加载失败即证明观测通道通 |
| 逐值回读图表数据 | 1 到 4 毫秒，渲染耗时的千分之四 |
| 单张截图 | 64 到 85 毫秒 |
| 读无障碍树 | 注入 72 毫秒，首次 71 毫秒，之后 30 到 34 毫秒 |
| 真实键盘遍历 | 40 次焦点切换 36 到 40 毫秒 |
| 八视角：逐张截图 | 477 到 540 毫秒 |
| 八视角：一次求值内渲完再导出 | 192 到 202 毫秒 |
| 真实交互状态机 | 7 条断言 + 8 次重载 2,267 毫秒，单项最贵，占探针 46% |

- 结构化数据毫秒级，看图要花 token。
- 渲染型任务比纯界面操作多一张牌：**运行时状态精确、无损、便宜**。能直接读的数，不该让模型看图猜。

不需要模型配合就能拿到场景：

- 可靠钩子都是「文档启动时注入一个引擎会条件读取的全局」，由引擎自己派发，比要求页面暴露状态接口稳。
- 逐引擎实测：主流三个 3D 引擎能拿到；两个常见 2D 游戏引擎、两个原生运行时拿不到。
- Verifier 的硬需求是**控制文档启动时的脚本注入**，不是约定接口。

图像预算在环境层硬性规定（按主流计价公式）：

| 方案 | 单张 | 八张 |
|---|---|---|
| 1024×768 逐张 | 1,036 token | 8,288 |
| 512×384 逐张 | 266 | 2,128 |
| 八视角拼成一张 1024×512 | — | 703 token |

- 默认给拼图，要细节再按需放大。
- **每条轨迹的视觉 token 上限写进环境，超了强制降分辨率——这是 RL 成本的主要旋钮。**
- 边界：超出分辨率上限的图片不会自动缩放，直接报错。
## 5 Putting The Three Parts To Work

三件齐了，剩下的问题是怎么花。本节只留有硬数字支撑的几条。

### 5.1 What One Pair Is Actually Good For

核心发现：配对当「待复述的内容」最没用；要产生价值，得让它承载结构预测的压力。

「这是一个某类网站，它的源码是以下内容」直接当预训练样本：本项目素材零命中，也没有文献直接批判过，以下是推论。两组数字给出方向：

- 结构规划 +3.1；先描述图里有什么再写码 −0.1 到 −0.9。
- 纯文本输入能拿到多模态的 95.8%，**但那份描述是从标准答案代码里抽的 oracle**；真实的自己描述版本 81.2 → 81.1，白做。

结论：**「把视觉信息精确地文本化」极有价值，「让模型自己去文本化」毫无价值。** 我们的 DOM 与场景图属于前者：程序从运行时状态直接读出，不经过模型。

有干货的无监督构造集中在两处：一次渲染挂多个监督头、局部对齐。

| 构造 | 实测 |
|---|---|
| 截图解析 | 全库最大单条增益：完整配方 67.8 / 137.5 / 84.2，**去掉截图解析掉到 12.2 / 35.1 / 24.2** |
| 一次渲染挂十个头 | 200 万数据上一个目标换十个，定位类 +4.5；同一目标把数据加到 1,500 万只 +0.2 |
| 局部包围盒对齐 DOM 片段 | 整页截图 + 随机节点包围盒，预测该节点源码；另一家做了同族 1.4 亿以上对，**但从未单独消融** |
| 受控降质 | 约 30 万真实页造 230 万样本，九个降质函数、每样本最多叠三个；设计选择准确率 75.12%，缺陷检测 87.1% vs 通用模型 51.58% |
| 反向构造 query | 读无障碍树而非原始源码（token 密度高得多）；MultiUI 做到 100 万站点 730 万样本 |

数据解读：

- **目标设计打败数据量**：同样数据量换成十个目标，收益超过数据量加到 7.5 倍。
- 被问过的几类构造在素材里零命中：代码填空、顺序恢复、互信息类目标、片段腐蚀、仓库级打包、代码与渲染之间的对比式对齐损失。这是真空地，不是共识地。
- 配比：
  - 中训规模约为底座的 5%（三家分别 5.4%、13.6%、22.9%）。
  - 合成数据占比压在 15% 以下；纯合成会灾难性遗忘，一个文字问答指标从 58.76 掉到 23.38 与 20.51。

### 5.2 Why Single-Turn Pairs Cannot Teach Recovery

核心发现：只用最优轨迹训出的修订能力 10.84，带纠错轨迹 46.75。

| 证据 | 数字 |
|---|---|
| 只用最优轨迹 vs 带纠错轨迹 | 10.84 vs 46.75；只在末尾纠错 35.67 |
| 工具调用恢复率 | 基线 32.76%，带纠错训练 89.68% |
| 纠错能否离线学到 | 离线配对微调的两轮改善率、错到对率、对到错率**全是 0%** |
| 直接灌失败轨迹 | 等量失败数据监督微调得 14.7 与 54.8，**低于只用成功数据的 18.9 与 61.2** |
| 负例权重扫描 | 0.0 → 37.2 / 0.5 → 35.1 / 0.8 → 44.4 / 基线 → 41.8，**只有 0.8 超过基线，非单调** |
| 无外部判据的自我修订 | 8B 模型直接生成 46.7，自我修订掉到 12.3 |

数据解读：

- 负例权重的非单调性是原文强调的，不是「越高越好」。
- 自我修订不是能力问题，是**判据问题**：没有外部判据时净负。
- 删掉试错的「纯净轨迹」：同分布小涨（完整版 48.5 → 纯净版 49.3），两个未见环境大跌（21.7 → 11.7、5.0 → 0.0）。

错误从哪来：

1. 离线修正轨迹学不出自我纠错，自然收敛点是「第 2 轮一字不改」。
2. **错误必须来自策略自己**：让待训模型先失败 → 在失败处快照整个虚拟机 → 教师从失败状态继续。
   - 训练用 harness 上比同规模基线高 14.6 个百分点。
   - 换到三个完全不同的 harness 仍高 6.7 到 12.4 个百分点。

### 5.3 Five Reasons A Reward Is Low

低 reward 不等于该叫教师。五类成因处理各不相同，只有最后一类该叫教师。本表可直接当检查表。

| 类型 | 怎么认 | 证据 | 处理 |
|---|---|---|---|
| 题目坏了 | 多个强模型互相不一致，或普遍与标准答案不一致 | 自动出题坏率：小问题 50%、大问题 7%；某执行环境里能区分对错补丁的测试不到 20% | 退池，别叫教师 |
| 判据坏了 | 负例里三个以上判官一致判挂 | 单判据天花板低于能力上限约 20 个百分点；本项目一条金标签标错，剔掉后多视角特异度 0.891 → 1.000 | 先复核标签 |
| 重跑抖动 | 同轨迹重跑会翻面 | 54 条原本成功的执行各重跑三次，162 次里 85 次失败，54 条里 39 条至少退化一次，**温度是 0** | 先减掉这条基线 |
| 判对但理由错 | 判定对、诊断错 | 本项目单条件判定 50%、多条件 67% 援引取景或透视豁免放过真错误；「鼻子长在后脑勺」样例八次全判挂，0/8 的理由提到朝向 | 按诊断正确性打标 |
| 预算耗尽或环境故障 | 看终止原因 | RL 早期约 20% 的轨迹被轮数或 token 耗尽截断，离线复核发现其中 24.3% 已解决问题 | 分开处理，见下 |

最后一类有一组正反对照：

- 公开做法：预算耗尽 →「强制提交，reward 乘 0.5」；环境故障 →「屏蔽梯度」。
- 把预算耗尽也按环境故障处理的那一家，复现时 reward 持续下降直到训练崩溃。
- 结论：**部分分是必需品，不是精细化。**
- 但「越细越好」有反证：某评分细则从 v1 细化到 v4，择优准确率 57.9% → 67.4%；过度细化的 v5全面变差。

判坏题不要靠人工标注：

- 同一评分细则下，「题面欠规约」标注者一致性 0.24，测试充分性 0.41。
- 一次独立复刻投入 7 名研究者、7 周、约 882 人时，一致性始终在 0.0 到 0.4。
- 同一批人标「难度」一致性 0.78。**人能一致地判「难」，不能一致地判「坏」。**

主路线是响应模式统计：

- 区分度 ≤ 0 说明题坏了（能力越低反而越容易答对）。
- 零方差题在公开统计里约占全量 4%。
- 题总分相关用剔除自身的版本，经典阈值：0.30 以上良好、0.20 到 0.29 勉强、低于 0.20 需修订、≤ 0 红旗。
- 实测：约一千题的集子一分钟跑完，每集只送 50 题给专家，被标出的题最高 84% 经人工确认有实质缺陷；在一个已人工修订过的集子上又找出 16 条无效题。

判「题面欠规约」的程序化做法：**题面补上参考信息再重测通过率，跳升超过 0.3 即判欠规约。**

### 5.4 When To Actually Call The Teacher

归完型后，叫教师的判据只有一条，不是「reward 低」，而是：**教师解得出，学生解不出。**

有明显更强的教师时，蒸馏对 RL 是数量级优势。Qwen3 同起点对照：

- RL 花 17,920 GPU 小时得 67.6；同策略蒸馏花 1,800 小时得 74.4。十分之一算力，全面更好。
- 原文补充「RL 完全没有提升高预算通过率」：90.0 → 90.0，蒸馏后 93.3。

由此三分法：

1. 有明显更强的教师 → 蒸馏，别 RL。
2. 没有更强教师，或教师也失败 → RL 是唯一选项。
3. 想扩高预算通过率 → **RL 必须带课程**；否则反向：某模型在一个数学集上 40.0 → 26.7 → 52.2，无课程 RL 把能力边界缩小了。

落到本文三个技术栈的优先级：

1. 前端与网页开发：先蒸馏。
2. three.js 与 Blender 复刻类任务：RL 信号最干净，先做。
3. 开放式 3D 设计（教师和判据都弱）：放最后。

先定难度带：

- 上界不是 1，是 0.9 甚至 0.5：通过率太高的题在分组相对优势算法里和全败题一样没有梯度。各家预算差别大，口径一致。
- 对照：不筛 54.2%，筛了 57.8%，差 3.6 分。
- 全败档不丢：取最靠近两个预算边界的各十道题，做小规模教师轨迹桥接再 RL。
  - 高预算通过率比基线高 9.8 个百分点，比无课程 RL 高 10.3 个百分点。
  - 538 道原本解不出的题里 226 道变得可解。

两条成本约束：

- rollout 占 RL 运行时间八成以上，「多采一倍候选再挑最好」很贵。
- 本项目 Blender 线单视角单题 24.7 核秒；按 256 次 × 3 个种子是每题 5.3 核时，三千道题一万六千核时，和跑一轮 RL 同量级。
- 结论：**离线跑高预算通过率在本机不可行，只能用训练中的在线正确率。**

整条链路：

**先定难度带 → 低 reward 先归因分型 → 退掉坏题与坏判据 → 减掉抖动基线 → 挑「教师解得出而学生解不出」的题 → 教师从学生自己的失败状态往下接 → 蒸带试错的轨迹，负例降权不删。**

「reward 越低越该叫教师」在这条链路里仍成立，只是它在第 5 步，不是第 1 步。

