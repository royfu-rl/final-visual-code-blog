Task = Query + Verifier + Harness，三件都从同一批素材里切出来；本页只讲素材。

- 素材：可公开获取的原始物件，如截图、源码、测试断言；同一份素材可拆成 Query、Verifier 的参考答案或 Hint（训练时给模型的部分答案信息，评测时不给）
- 其余两页：Verifier 给轨迹打 reward；Train 讲 Harness 与三件的组合用法

## 1 Three Parts

缺任何一件，素材只是数据，不是可验证任务。

| 件 | Web 上的形态 | 缺了会怎样 |
|---|---|---|
| Query（全称 Omni Reference Query） | 需求描述，加零到四层参考：参考图、参考页面、参考录屏、参考音频 | 只有源码时只能做无监督训练 |
| Verifier | 把采集到的证据判成通过或不通过的规则 | 没有 reward，只能人工评审 |
| Harness | 无头浏览器、冻结时钟、固定视口、运行时状态读取、多视口截图 | 产物跑不起来，Verifier 无法执行 |

## 2 Material

供给上限由来源决定：三类来源里只有 Golden Images（测试用的标准答案截图）自带图码配对。

### 2.1 Overview

可挖来源分 GitHub、HuggingFace、Website 三类，自带图码配对的只有 Golden Images，8 个仓库共 14,522 张截图。

- 图码配对：一张截图与生成它的源码
- Golden Images：前端仓库为每份测试代码存的标准答案截图；每次改代码后重新渲染、与它逐像素比对，这种测试叫视觉回归测试（Visual Regression Testing，VRT），因此代码与截图天然成对

**Artifacts 词表**：全书来源表共用六类标签，颜色即类别。

<!--ARTIFACTS-->

1. 一个标签只写一个物件。
2. 同义词归一：渲染结果、GUI 截图都写「截图」。
3. 限定语写进括号，如 `bpy .py（分部件）`；文件类型直接写扩展名。

| Source | Type | Datasize | Example | Artifacts |
| --- | --- | --: | --- | --- |
| **GitHub** | Golden Images（VRT 基线） | 8 仓 · 14,522 图 | [primer/react](https://github.com/primer/react) · [MapLibre](https://github.com/maplibre/maplibre-gl-js) · [Chart.js](https://github.com/chartjs/Chart.js) | <span class="art a-img">截图</span><span class="art a-code">.tsx</span><span class="art a-code">.js</span><span class="art a-code">.json</span> |
|  | VRT 下游仓库（未挖） | 458,596 依赖仓（Playwright 一家） | [Playwright](https://github.com/microsoft/playwright) · Storybook · BackstopJS | <span class="art a-img">截图</span><span class="art a-code">断言</span><span class="art a-code">源码</span> |
|  | Issue + 截图 + Pull Request | ≈ 1,400 条 | [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) · OmniGIRL | <span class="art a-txt">问题描述</span><span class="art a-img">截图</span><span class="art a-code">补丁</span> |
| **HuggingFace** | 图码配对集 | 80 – 3.17M | [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m) · [WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) · [Design2Code](https://arxiv.org/abs/2403.03163) | <span class="art a-img">截图</span><span class="art a-run">.html</span> |
| **Website** | 社区站 / 问答站 | 2,799 – 10M | [CodePen](https://codepen.io/) · [Shadertoy](https://www.shadertoy.com/) · [js13kGames](https://js13kgames.com/) | <span class="art a-img">截图</span><span class="art a-txt">标题</span><span class="art a-run">.html</span><span class="art a-code">代码片段</span> |
|  | 真实门户页 | 45.1k 页 | [WebRenderBench](https://arxiv.org/abs/2510.04097) | <span class="art a-run">.html</span><span class="art a-img">截图</span> |
|  | 设计站与获奖画廊 | 3,116 – 62 万 | [Awwwards](https://www.awwwards.com/) · [One Page Love](https://onepagelove.com/) · [Mobbin](https://mobbin.com/) | <span class="art a-img">截图</span><span class="art a-txt">评分</span><span class="art a-txt">标签</span> |
|  | 可克隆站 / 主题 / 组件库 | 560 – 95,246 | [Webflow](https://webflow.com/made-in-webflow) · [Codrops](https://github.com/codrops) · [Astro 主题](https://astro.build/themes/) | <span class="art a-run">.html</span><span class="art a-code">源码</span><span class="art a-img">截图</span> |

- Artifacts 列：该渠道直接拿到的物件
- 数量口径：「458,596 依赖仓」只计 Playwright 一家；「80 – 3.17M」「2,799 – 10M」是该类各数据集或站点的区间，不是合计

### 2.2 GitHub

GitHub 上有三类来源，成熟度各不相同：

- **Golden Images**（测试用的标准答案截图）：截图和代码天然配对，但只能检查「像不像」，且一部分拿不到
- **VRT 下游仓库**：用了 VRT（视觉回归测试：改完代码重新截图，与标准截图比对）工具、自己写了截图测试的项目；潜在数量大，目前只有规模估算，还没挖
- **带图 issue**：不是图码配对，用途是「看图修 bug」，能用的约 1,400 条

#### 2.2.1 Golden Images

Golden Images 是测试里存的「标准答案截图」。前端仓库常为每份测试代码配一张页面截图，每次改代码后重新渲染，再与这张截图逐像素比对，查界面有没有被意外改坏；这种测试叫视觉回归测试（Visual Regression Testing，VRT）。所以这类仓库里，代码和截图天然一一配对。

8 个仓库共 14,522 张截图、约 5,799 份代码，严格一图一码的只有 Chart.js 与 OpenLayers。

<!--REPO:web-->

这类配对只够做最弱一档 Verifier：把生成的代码渲染成截图，再让模型打分。

另一个来源是 VRT 下游仓库，即用了 Playwright 等 VRT 工具、自己写了截图测试的项目，估计有几千个仓库、几万个 PR（口径待补），还没挖。先实扫两个最典型的：

<!--REPO:web-vrt-->

- 口径：2026-11-07 读 GitHub trees API。图 = 基线目录（`*-snapshots/`、`__image_snapshots__/`）下的 .png；码 = 同目录产出这些基线的测试文件
- 这两个仓库本身没进上面的 8 个，上面那张表是已经扫完入库的，这两个只是下游这一档的样子

#### 2.2.2 Issues

带截图的 issue 不是图码配对，而是三件套：问题描述 + bug 截图 + 修复补丁，可用来训练「看图修 bug」；能用的约 1,400 条。

1. 这类题必须看图。
   - [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859)：论文正文 619 道题、17 个 JavaScript 库（摘要写 617）；含图的 557 道中，人工确认 83.5% 不看图做不出来
   - 公开数据集行数与论文不一致：HF 旧版（princeton-nlp）612 行；官方现行版（SWE-bench）580 行、16 个库
2. 这类题很难。
   - [OmniGIRL](https://arxiv.org/abs/2505.04606)：959 道题中含图 19 道；Claude-3.5-Sonnet 直接看图只解决 3.5%，用 agent 方法为 0%
   - 10.5% 是最好成绩：直接给出要改的文件，且先把图片内容改写成文字
3. 量少：检索能命中几十万条，能整理成三件套的只有约 1,400 条。
   - 按 issue 里的图片地址检索：新版地址命中 TypeScript 192,818、JavaScript 51,136、CSS 3,488；旧版地址另有 TypeScript 76,009、JavaScript 40,801
   - 1,400 = 约 30 万条候选 × 0.457% 转化率；转化率出处口径待补

<!--REPO:web-issue-->

- 口径：题数 2026-11-07 读自 HF datasets-server，与论文口径不一致的在「特性」里标了出处
- 标记：✓ 宽松许可，△ 有条件，？未声明

### 2.3 Datasets

公开网页配对数据共 37 条，35 条集中在单文件「截图 → 代码」，多文件 Web App 只有 2 条。

<!--PIPE:html,webdev-->

### 2.4 Website

高质量网页作品按能拿到什么分档：Webflow 可克隆站规模最大，Codrops 的 MIT 仓库动效最密，开源官网是真实的多页生产站，获奖画廊只给截图与评分；社区站多是单文件或片段。

<!--SITE:web-->

## 3 Funnel

素材从名义规模走到可训任务，要依次过可用性、执行校验、人工复核几道关。真实挖矿最后多只剩 0.2%–5%，损耗主要在执行这一步，因此真实素材只作评测集与分布锚点，不作 RL 题库主体。

- 两次收缩：名义规模（自报或检索数）→ 可用素材，差一到两个数量级；可用素材 → 可训任务（带执行校验），再差两个数量级
- 口径：留存率 = 终点 ÷ 起点；Webflow 与 Codrops 两行止于许可干净的可用素材，不产出任务；SWE 系列与 WebCode2M 的终点经过执行或渲染校验；检索计数随时间漂移，引用须注明查询条件

| Source | Name | Unit | Filter | Funnel | Retention |
|---|---|:-:|---|--:|--:|
| **GitHub** | [SWE-bench](https://arxiv.org/abs/2310.06770) | PR | 12 个热门 Python 仓的 PR → 属性过滤 → 执行校验 | 93k → 11k → **2.3k** | 2.5% |
| | [SWE-Gym](https://arxiv.org/abs/2412.21139) | 条 | 358 个 Python 仓的 PR → 选 11 仓 → 执行校验 | 65k → **2.4k** | 3.8% |
| | [SWE-rebench](https://arxiv.org/abs/2505.20411) | PR | GitHub 公开 PR → 下载 → 安装与校验 | 10M → 450k → **21k** | 0.21% |
| | [SWE-smith](https://arxiv.org/abs/2504.21798)（合成） | bug | 128 个 Python 仓合成 bug → 执行校验 | 100k → **50k** | 50.1% |
| **HuggingFace** | [Design2Code](https://arxiv.org/abs/2403.03163) | 页 | [C4](https://huggingface.co/datasets/allenai/c4) 验证集网页 → 长度去重 → 抽 7k 人工检查 | 128k → 14k → **484** | 0.38% |
| | [WebCode2M](https://huggingface.co/datasets/xcodemind/webcode2m) | 页 | [Common Crawl](https://commoncrawl.org/) 抽样 → 长度 → 渲染 → 打分器 → 截图去重 | 500M → **2.56M** | 0.51% |
| | [The Stack v2](https://arxiv.org/abs/2402.19173)（html） | GB | [Software Heritage](https://www.softwareheritage.org/) 源码存档 → 许可 → 近似去重 → 质量 | 2.4T → **99G** | 4.1% |
| **Website** | [CodePen](https://blog.codepen.io/2016/11/25/10000000/) | 作品 | [CodePen](https://codepen.io/) 官方自报作品数 → 无列举接口 → 只剩公开镜像 | 10M → **25k** | 0.25% |
| | [shaders21k](https://arxiv.org/abs/2211.16412) | 作品 | [Shadertoy](https://www.shadertoy.com/) 公开作品 → 可编译 → 去重 → 去静态画面 | 52k → **21k** | 40.5% |
| | [ShaderMatch](https://huggingface.co/spaces/Vipitis/shadermatch) | 函数 | [shaders21k](https://arxiv.org/abs/2211.16412) + [Shadertoy](https://www.shadertoy.com/) 接口的函数 → 执行确认 | 202k → **467** | 0.23% |
| | [Webflow 可克隆站](https://webflow.com/made-in-webflow)（估） | 条目 | sitemap 条目 → 可克隆原创 → 点赞 ≥ 10（抽样 300 外推） | 95k → ≈57k → **≈4.7k** | 5% |
| | [Codrops](https://github.com/codrops) | 仓 | 全部仓库 → MIT → 含 WebGL | 349 → 129 → **13** | 3.7% |

**一、真实挖矿**

损耗集中在执行校验与人工复核两步。

1. 执行校验是最大的损耗环节。
   - [SWE-rebench](https://arxiv.org/abs/2505.20411)：安装与校验约 14% 通过；31% 的仓库能产出至少一个任务
2. 留存率只在同一终点之间可比。
   - shaders21k 的 40.5% 止于可用素材（只过编译与去重）；同一批作品做成任务（ShaderMatch）后为 0.23%
3. 人工复核再剔除大部分，本步留存 6.9%–31.7%。
   - Design2Code：人工检查 7k 页，留 484 页，留存 6.9%
   - SWE-bench Verified：从 2,294 条抽 1,699 条人工复核，判废 68.3%；题面欠规约 38.3%、测试误杀正确解 61.1%（两类重叠，分母均为 1,699）

**二、合成扩产**

合成能把产能提高一个数量级以上，但留存率由合成策略决定。

1. 少量种子即可扩出大量已验证任务。
   - RST：639 个种子任务经 15 轮扩展得到 37,484 个已验证任务（约 59 倍）；每个通过任务约 0.05 美元，人工对照每题数百到数千美元，出处口径待补
2. 策略之间留存率相差 52 倍。
   - [SWE-smith](https://arxiv.org/abs/2504.21798)：组合类 97.43% / 96.16% > 模型造 bug 55.98% > 重写函数 35.04% > 打乱类内方法 1.88%
   - 组合类只拼接已验证补丁，不产生新信息，因此高留存不等于高产出

## 4 Curation Pipeline

真实网页有四个问题：归档渲染不出来，八成质量低，平均长度 31.2k token，约为可训长度 5k 的 6 倍，原文文字进提示词反而降低效果。所以原始网页要过十道闸才能进训练集，按渲染前、渲染、渲染后三段排开。顺序比闸本身更要紧：渲染最贵，长度与结构闸必须排在它前面。

<div class="wide"><div class="gp-wrap"><div class="gp gf">
<div class="gp-grp" style="grid-column:2/3;--g:var(--brand)">渲染前 · 源码</div>
<div class="gp-grp" style="grid-column:3/4;--g:#e8913a">渲染</div>
<div class="gp-grp" style="grid-column:4/5;--g:#6a4fd6">渲染后 · 截图</div>
<div class="gp-grp" style="grid-column:5/6;--g:#d6455d">入库前 · 全库比对与许可</div>
<div class="gp-end gp-in arr">原始<br>源码</div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">01</span><b>长度粗筛</b></div><div class="gf-r">渲染最贵，不先挡掉空页与超长页就白烧；31.2k 是 Design2Code 484 页均值（±23.9k），5k 是唯一经实验验证的可训长度</div><div class="gf-src"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a> · <a href="https://arxiv.org/abs/2403.03163">Design2Code</a> · <a href="https://arxiv.org/abs/2412.04626">BigDocs</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">02</span><b>资产本地化</b></div><div class="gf-r">外链离线超时，测到的是网络不是设计；归档页缺图片与样式表，须重爬</div><div class="gf-src"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a> · <a href="https://arxiv.org/abs/2403.03346">S4</a> · <a href="https://arxiv.org/abs/2403.03163">Design2Code</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">03</span><b>图片占位</b></div><div class="gf-r">图床会失效，<a href="https://huggingface.co/datasets/HuggingFaceM4/WebSight">WebSight</a> 192 万条因此不可复现</div><div class="gf-src"><a href="https://arxiv.org/abs/2403.03163">Design2Code</a> · <a href="https://arxiv.org/abs/2412.04626">BigDocs</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">04</span><b>不可见剪枝</b></div><div class="gf-r">看不见的元素让图码对不齐，<a href="https://arxiv.org/abs/2201.04100">CLAY</a> 37.4% 屏含无效元素</div><div class="gf-src"><a href="https://arxiv.org/abs/2403.03346">S4</a> · <a href="https://arxiv.org/abs/2404.06369">WebCode2M</a></div></div>
<div class="gf-gate no-src"><div class="gf-h"><span class="gp-step">05</span><b>去编译产物</b><span class="gf-tag warn">无出处</span></div><div class="gf-r">打包代码不是人写的，仅推论</div></div>
</div>
<div class="gp-g gp-hot arr"><div class="gp-step">成本瓶颈</div><div class="gp-name">渲染</div><div class="gp-big">80%<small>总耗时</small></div><div class="gp-row"><span>耗时占比</span><b>80%</b><span class="gp-bar"><i style="width:80%;background:#e8913a"></i></span></div><div class="gp-cap"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a> 实测，全程约一个月；本项目估算：2,000 万页约需 2,000 CPU-day</div></div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">06</span><b>审美过滤</b></div><div class="gf-r">80% 真实页只有 0–1 分（6 名标注员打 1 万个分，五分制）</div><div class="gf-src"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">07</span><b>内容安全</b></div><div class="gf-r">去色情脏话</div><div class="gf-src"><a href="https://arxiv.org/abs/2404.06369">WebCode2M</a></div></div>
</div>
<div class="gf-col arr">
<div class="gf-gate"><div class="gf-h"><span class="gp-step">08</span><b>去重</b></div><div class="gf-r">重复让指标虚高一倍（<a href="https://arxiv.org/abs/1812.06469">Allamanis</a>），10% 重复 ≈ 模型小两倍（<a href="https://arxiv.org/abs/2205.10487">Hernandez</a>）</div><div class="gf-src"><a href="https://arxiv.org/abs/2211.15533">The Stack</a> · <a href="https://arxiv.org/abs/2402.19173">StarCoder2</a> · <a href="https://arxiv.org/abs/2303.09540">SemDeDup</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">09</span><b>去污染</b></div><div class="gf-r">评测集与训练集同源 C4 / CC，n 元组挡不住改写；剔除答案泄漏的题后，解决率 12.47% → 3.97%（<span class="warn">Python 修复任务，Web 口径待补</span>）</div><div class="gf-src"><a href="https://arxiv.org/abs/2410.13824">MultiUI</a> · <a href="https://arxiv.org/abs/2304.14108">DataComp</a> · <a href="https://arxiv.org/abs/2410.06992">SWE-Bench+</a></div></div>
<div class="gf-gate"><div class="gf-h"><span class="gp-step">10</span><b>许可核对</b></div><div class="gf-r">截图端看仓库许可，代码端还要看上游库许可，两端分别核对；聚合站点无列举接口，逐件许可无法批量读取</div><div class="gf-src"><a href="https://arxiv.org/abs/2211.15533">The Stack</a> · <a href="https://arxiv.org/abs/2402.19173">StarCoder2</a></div></div>
</div>
<div class="gp-end gp-out">可用<br>素材</div>
<div class="gp-lock">顺序锁定：长度与结构闸排在渲染之前</div>
</div></div></div>

**数据清洗心得**

1. 审美分不能拿来排序，也不能直接当 reward，只能用来卡住两头。
   - 「双侧区间」指太丑的不要，太「极简」的也不要；「否决闸」指只用来一票否决
   - 原因一：传统审美指标能被刷。留白越多、颜色越少分越高，拿它当 reward，模型会学出一张空白页
   - 原因二：好看本身没有共识。[DesignPref](https://arxiv.org/abs/2511.20513) 里 20 位专业设计师判同样 600 对页面，只有 62.4% 意见一致；在这份数据上训的模型准确率 57.45%
   - 推论：谁说自己的审美 reward 准确率远高于 60%，先怀疑是不是测试数据泄漏了
2. CLIP 这类通用图文模型不能当质量闸，也不能用来查重复。
   - 它找相似图的能力太弱：同一精度下只能找回 2% 的重复（[DataComp](https://arxiv.org/abs/2304.14108)）。查重复要用专门做图片拷贝检测的模型
3. 去重会过头。
   - [FineWeb](https://arxiv.org/abs/2406.17557) 把所有快照放在一起全局去重，15T 压到 4T，训练效果反而和不去重差不多；每个快照各自去重，留下 20T，效果更好
   - 真正有用的是去掉几十万篇规模的巨型重复簇；只有几十份副本的小簇，再去重反而有害

