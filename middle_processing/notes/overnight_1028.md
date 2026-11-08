# 过夜迭代日志 · 10-28 01:15 → 11:00

## 任务
1. Web Sources 2.4 / 2.4.1：高质量、优雅、有难度、可开源获取的 HTML 设计作品来源
2. 3D 章按 Web 的 6 标签（Benchmark / Open Data / Sources / Verifier / Train / Critic）与小节分段重构
3. three.js / Blender 高质量作品来源写进 3D
4. 反复优化到 11:00

## 规则（用户已确认的偏好）
- 结论先行、主题式短标题、正文凝练；长解释进划词备注（data/notes.json，serve_notes.py :8977）
- 不编造文字；数据带口径，查不到写「口径待补」；阈值类细节不写
- 每次改完：gen_pages.py → build.py → 截图自检

## 进度
- 01:20 启动两个调研 agent：Web 高质量来源 → notes/web_quality_sources.md；3D 高质量来源 → notes/3d_quality_sources.md
- 01:20 定时唤醒：每小时 :13 / :43（2:00–10:59）

## 待办
- [x] 3D 拆分成 6 标签，gen_pages CHAPTERS 已改
- [x] 3D 标题改主题式，对齐 Web
- [x] 3D 正文按写作风格改写：Benchmark、Open Data、Sources 1/2.1–2.6、Train 5（Verifier 正文暂未动，结构已对齐）
- [x] 接入 Web 调研结果 → Web 2.4.1 Showcase（Real Pages 顺延 2.4.2）+ 3 个数据样例
- [x] 接入 3D 调研结果 → 3D 2.4.1 Showcase + 3 个数据样例
- [x] README 章节表更新
- [ ] 第二轮：核对新增来源的链接与数字（抽查）、截图自检、Verifier 页文字风格

## 进度（续）
（注：下列条目原先写的 02:05–03:40 是估计值、不是真实时间，实际都发生在 01:25–01:50 之间，已更正）
- 01:2x–01:50 3D 拆成 6 标签：verified.md → data.md / verifier.md / train.md，新增 critic.md；标题改主题式（Lab Reports / Three Stacks / Inventory / Timeline / Three Parts / Material / GitHub / Datasets / Funnel）；三条硬约束移到 Verifier 3.7；3D 2.7 Reference Thickness 与 Lab Reports 解读移出正文，存 notes/removed_1028.md；原文件备份在 _trash/
- 01:2x–01:50 备注计数只算当前页
- 01:2x–01:50 3D Open Data：2 Timeline 换成横向时间线图（五阶段、新增「几何与执行检查」「运行时状态」两种验收标签）；新增 3 Gaps（缺的东西 / 前置条件），数字全部取自 3D 页已有数据
- 01:2x–01:50 3D Sources：2.2 拆成 2.2.1 Golden Images / 2.2.2 Scripts；2.3、2.5 按写作风格改写（结论先行、已知问题改成判断+缩进数据）；2.5 去掉无支撑的「低一个数量级」，估算标口径待补
- 01:2x–01:50 3D Sources 2.1 Overview 对齐 Web 格式
- 01:2x–01:50 3D Benchmark 2 Three Stacks / 3 How To Choose 改写
- 01:2x–01:50 Web 与 3D 的 Open Data 1 Inventory 改写成结论 + 判断条目；Web 去掉与 Funnel 矛盾的「挖矿留存 2%–5%」
- 01:2x–01:50 3D Verifier 3.4 拆 3.4.1 / 3.4.2；3D Train 补第 5 节（5.1–5.4，与 Web 同分段，证据取自已有数据，通用规律指向 Web 页）
- 01:2x–01:50 3D Sources 新增 2.6 Curation Pipeline 闸门流程图（八道闸，四段，出处都标了；无出处两道虚线）
- 01:2x–01:50 Web 与 3D 的 Train 页标题改主题式短标题（4 Harness / Assets / Determinism / Rendering / Observations；5 Training / Pair Usage / Recovery / Low Reward / Teacher；3D 4.x：Blender / three.js / Discounts / Cost）
- 01:2x–01:50 3D Sources 2.4 Website 改写（表格之外改成判断+数据）；README 章节表更新
- 01:2x–01:50 自动 QA：Web / 3D 全部 12 个视图无脚本错误、无坏图、正文无未渲染的 ** 与标记（Web Sources 的 ** 都在代码样例里）
- 01:2x–01:50 等调研 agent 回来；接下来：Web 2.4 新增 2.4.1 Showcase（Real Pages 顺延 2.4.2），3D 2.4 新增 2.4.1 Showcase
- 01:53 3D Sources 新增 2.4.1 Showcase（three.js 7 源、Blender 7 源、慎用 4 类）；2.2.1 更正 r3f 0 张图；2.2.2 加 GitHub 模型产物渗透 43%
- 01:54 3D 2.3 补 3DCode / 3D-Front-Code / 3DCodeVerse；Showcase 挂挖掘流程便签；时间线补 WorldBench
- 01:54 抽查 3D 调研 4 个数字（pmndrs 211 / MIT、3DCode MIT、Poly Haven 521、three.js 616）全部吻合；2.2.1 补 616 口径
- 01:55 门口页章节表改成六视图；Web Benchmark 的 Open Data Pipeline 视图 → Open Data 视图
- 02:10 Web Sources 新增 2.4.1 Showcase（拿得到源码 7 行 / 只给截图 3 行 / 不能用 4 类），Real Pages 顺延 2.4.2；2.1 总表设计站一行补实测、加可克隆站/主题/组件库一行；挖掘流程等折进便签
- 02:11 抽查 Web 调研 4 个数字（Webflow ai-train=yes、Codrops 349/129、Uiverse 3,802、shadcn 508）全部吻合；Showcase 表规模列改左对齐
- 02:19 新增 6 个数据样例（只放原图、原始文件名、原始代码）：Web 2.4.1 → Webflow 可克隆站 / Codrops / Uiverse；3D 2.4.1 → three.js 官方 examples / pmndrs/examples / 3DCode。抓取脚本 scripts/fetch_showcase_samples.py，组件在 build_samples.py；raw() 按真实格式保存；两页 125 张样例图全部加载正常
- 02:20 Web 与 3D Verifier 轻量清理：删「问题」行 10+10、过渡句 9+9、「结论」标签；8 处依赖问题的结论句改成独立成句；原文备份 _trash/*_verifier_before_1028.md；第二轮调研 agent 已启动（开源官网 / WebGL 合集 / 重试被封站点）
- 02:21 Web Benchmark 2 Four Stacks 改写、3 How To Choose 结论提前；Web 与 3D Train 去掉「核心发现 / 数据解读」标签
- 02:23 新增链接 64 个全部核验（57 直接 200，7 个是反爬拦截，非死链）；手机宽度无横向溢出；Web / 3D 的 2.4 开头直接回答「去哪里找高质量数据」
- 02:53 3D Open Data 总表补 4 条 2026 新数据集（3DCode / 3D-Front-Code / 3DCodeVerse / BlenderLore）：录入 pipe_meta_3dgame.json + buckets.json + orgs_pipe_3dgame.json（机构填 HF 发布者，不猜单位）；汇总表 blender 8 → 12；标签说明同步
- 03:21 接入第二轮调研：Web Showcase 新增「二、开源的生产级官网」（supabase / payload / ray.so / react.email / openai.fm 等）、Land-book、FWA 条款、无许可的设计站；Codrops 许可用原文更正。3D：three.js 表加 WebGL 实验合集 3 行，Blender 表加内置资产 CC0 / Big Buck Bunny / 几何节点仓库；three.js 论坛许可更正为 CC BY-NC-SA 3.0；Blendkit 降为只能内部用
- 03:22 抽查第二轮 6 项（payload / ray.so / openai.fm / ghostty MIT、basement 无许可、blender-assets CC0）全部吻合；Web 挖掘流程便签补「开源生产站」一条
- 03:23 通读 Showcase：Web 开头结论压短；Web 一/三/四、3D 一/二/三 各补一句块结论；Web 挖掘便签改挂新句
- 03:25 新增数据样例「开源生产级官网」：supabase（og 图 + app/(home)/page.tsx）、ray.so（og 图 + 代码截图页源码）、openai.fm（仓库 screenshot.jpg + page.tsx）
- 03:56 Codrops 129 个 MIT 仓库实测难度画像：GSAP 91%、平滑滚动 35%、WebGL 10%、手写代码中位 1,059 行；Showcase「难度最高」改「动效最密」，Codrops 行改用实测数；画像挂便签，方法存 notes/codrops_profile.md
- 04:03 pmndrs/examples 211 个示例实测难度画像（后处理 36%、实例化 14%、物理 11%、着色器 9%、源码中位 173 行）；3D pmndrs 行改用实测数；three.js 两来源对照表挂便签；方法存 notes/pmndrs_profile.md
- 04:04 3DCode 抽 60 类脚本实测画像（几何节点 48%、修改器 88%、bmesh 68%、中位 919 行）；3D 表 3DCode 行补数；画像挂便签，方法存 notes/3dcode_profile.md
- 04:21 两边 2.5 Funnel 补高质量来源漏斗：Web 加 Webflow（估 40%）、Codrops（3.7%）；3D 加 three.js 高星 MIT（61%）、Experiments with Google（1.8%）、Blender demo（57%）、Sketchfab Staff Pick（77%）；口径注明止于可用素材
- 04:22 3D：2 Material 与 2.1 开头去重；2.4.1 开头改成分档结论，与 2.4 不再重复；便签全部在位
- 04:53 Webflow 抽样扩到 300（正确读 siteProfile）：可克隆原创 60%（≈5.7 万），其中点赞 ≥ 10 的 8%（≈4,700）；调研时的 40% 作废；Showcase、Funnel、便签同步更新；方法存 notes/webflow_sample.md
- 05:22 Webflow 高赞可克隆原创 15 个在线页面画像：12 个首页无站内链接（单页交互效果演示），GSAP 4、three.js 1；Showcase 行与便签据此改写：适合出复刻交互效果的小题，整站去主题目录与开源官网
- 05:51 Web Showcase 加「五、按题型选」、3D 加「四、按题型选」：每条推荐都引用已实测的画像数字
- 05:52 README 补「数据样例与来源笔记」一节（抓取脚本、样例规范、调研与画像笔记位置）
- 06:22 样例合规审计：45 个在用样例组件均无 AI 说明文字（仅已下线的 meshcoder 残留，不影响页面）；3D 新增数据样例「Experiments with Google」：WebGL-Fluid-Simulation / OrigamiSimulator（GIF 原样保留 151 帧）/ The-Spirit
- 06:53 新增数据样例：Web「Hugo 主题」（PaperMod / Blowfish / Congo：主题自带 screenshot.png + 布局模板）；3D「CGArtPython」（3 组起始 / 完成 bpy 脚本，仓库无图故只放代码）
- 07:22 3D 新增数据样例「Poly Haven」：jacaranda_tree / Camera_01 / marble_bust_01，站点缩略图 + files API 原文（只截 1k 的 blend、gltf 两项）
- 07:52 全面回归：Web / 3D 12 个视图零脚本错误、零坏图（Web 119 张、3D 18 张）；备注 13 条全部定位；手机宽度无溢出；新增 30 个链接 28 个 200，2 个为 Cloudflare 反爬（Land-book、projects.blender.org）

## 汇总（供 11:00 总结）
- 3D 重构：6 标签与 Web 一致；小节分段对齐（Sources 1/2.1–2.6、Verifier 3.1–3.7、Train 4–5）；新图：Open Data 时间线、Sources 2.6 闸门流程图
- 高质量来源：Web 2.4.1 Showcase（拿得到源码 / 开源生产级官网 / 只给截图 / 不能用 / 按题型选）；3D 2.4.1 Showcase（three.js / Blender / 慎用 / 按题型选）
- 实测：Codrops 129 仓、pmndrs 211 例、3DCode 60 脚本、Webflow 300 条目 + 15 个高赞在线页；两轮调研 + 三轮抽查（共 14 项全部吻合）
- 数据样例新增 11 组（只放原图、原始文件名、原始内容）：Web 5 组（Webflow、Codrops、Uiverse、Hugo 主题、开源官网），3D 6 组（three.js 官方、pmndrs、Experiments with Google、3DCode、CGArtPython、Poly Haven）
- 更正：r3f 0 张图、three.js 论坛许可、Blendkit、Codrops「难度最高」、Webflow 可克隆比例 40%→60%、3D 2.5「低一个数量级」、Web Inventory 与 Funnel 矛盾
- 风格：两页 Verifier / Train / Benchmark / Open Data 去铺垫与固定标签；标题主题式
- 08:23 Blender Open Data 5 个未标许可的场景：demo 页无标注，下载 bmw27 / koro / monster 压缩包核查也无许可文件 → 改写为「按未授权处理」，不再写口径待补
- 08:51 清口径待补：payload 获奖版本在仓库历史中（建于 2022-10-20，获奖前末次提交 2022-11-22）；One Page Love API 未公开条款（自称可用于训练数据集）；SiteInspire 总数经阅读代理仍被拦，保留待补
- 09:21 视觉通查 Web Showcase：修正「一、拿得到源码」难度排序与 Webflow 实测矛盾（可克隆站不是最难，按实测排在效果演示档）
- 09:22 修下载量徽章被千分位截断（79,603 → 只显示 603）：sample_meta 与 pipe_meta 里的新条目改成 79.6k 写法；3D Codrops 行改用许可页原文与实测（MIT 仓库 8% 用 three.js）
- 09:51 通查 3D Open Data（时间线、Gaps）与 Train（第 5 节）：排版正常、无脚本错误；补一个 11:03 单次唤醒用于收尾总结（原定时任务最后一次在 10:43）
- 10:21 3D Train 4 Harness 开头三条散列改成一句结论 + 口径；「GPU 这件事可以定论」改判断句；后果引导句压短
- 11:03 收尾：定时任务全部删除；最终 build 与 QA 通过

