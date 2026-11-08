# 3D 族 Showcase 来源记录（2026-11-04）

- 产出：`cards_3d.json`（3 个场景、12 张卡）；指标缓存 `impact_3d.json`
- 小红书占比：4 张以小红书为主链；另 3 张（PJ、小王子、Cozy Creek）是从小红书线索找到海外原帖，也挂了小红书链接
- 链接：卡片里所有链接都用 fetch_impact 或 curl 验过。以下几条 curl 被 Cloudflare 拦（403），没有放进卡片：openai.com/codex、TNW、tripo3d 博客

## 1 白模预演出片（greybox-previs）

- **Nexus 灰模分镜**
  - 作品：X @PJaccetturo 2112899203701547153（2026-10-21），连同整条推文串
    - 推文串原话：「each Seedance gen went wrong camera / blocking / ships changing size」，「We had Claude run Blender for us」，「Claude screenshot the blender sequences as storyboards」，片子是「@dreamina_ai Original Series, Nexus」
  - 小红书：陆三金 6ad9b245（搬运，写出了 STORYBOARD 提示词）
  - 改前每天 2000+ 美元生成费：出自首帖原文
  - doc：PJ 公开的 Blender 工作流 Google Doc（出自推文串第 6 条）
  - 没用：Genre.ai「3 亿+ 人看过」。这是 v1 记的旧说法，官网现在找不到
- **Higgsfield 白模插件**
  - 作品：X @higgsfield 2092255768770920506（2026-08-25），「Prompt the scene and build the blockout」
  - 功能：higgsfield.ai/plugins/blender，加上 2026-10-28 那篇博客
    - Scene Builder 搭可编辑白模
    - Video 页签用 Seedance 2.5 出片
    - Agent 经 Higgsfield Bridge MCP 接入
  - 年化 10 亿美元、3200 万+ 用户、近 100 万付费：Higgsfield 官方博客（2026-09-29），口径是「近 4 周 × 13」
  - B 轮 4 亿美元、估值 54 亿：TechCrunch（2026-08-17）
  - 注意：这些收入是 Higgsfield 全站的，插件没有单列
- **Codex 白模预演**：小红书 小林Kara 6aa7d98c
  - 原文：「3D 预演最大的价值，是提前控制构图、机位和复杂镜头运动……提高 AI 视频生成成功率」
  - 正文没写用的是哪个 MCP，所以只挂 Codex 和 Blender 官网
- **户型图直出白模片**：小红书 shine 6aa7e7d5
  - 内容来自 v2 extract：Codex 出三维白模和浏览器播放器 → 小云雀里用 Seedance 2/2.5 渲染
  - 评论区有人说「高质量白膜视频现货有吗，大量收」，算一个需求信号

## 2 代码造 3D 世界（code-3d-worlds）

- **《小王子》3D 游戏**
  - 作品：X @Saccc_c 2109962425512734739（2026-10-13）；可玩地址 littleprince.dev
  - 教程：X 文章 2110694725640474759
  - 小红书：陆三金 6ad0eb07（拆解）
  - 工具链出自 Kelly 6ad15b08：Fable 写 PRD → Image 2.5 → Tripo → Opus 5.5 经 Unity MCP 和 Blender 组装
  - Tripo 赞助了这个项目（作者披露），数字没写进卡片
- **果冻海岛**：小红书 Ray 6acd9d34，1.13 万赞，正文写明 #Threejs #AI编程
  - 没找到在线地址或海外原帖，只能挂 threejs.org
- **Cozy Creek 溪流**
  - 作品：X @chetanankola 2107996576228753545（2026-10-08）
  - 小红书：Process zero 6ac736fa（转述，含 3.17 亿 token 消耗清单）
  - 19.99 美元套件：3ditions 页面「Three.js Creek & Cottage Kit — Hiroshi's Island」
  - 套件和作品的关系：作者在 Threads 上说按制作成本的 1/5 出售
  - 缺口：销量未知
- **Fly 飞行模拟**
  - 作品：X @levelsio 1893350391158292550（2025-02-22，Cursor 一句话起步）
  - ARR 100 万、MRR 8.7 万、32 万玩家：@levelsio 1899596115210891751（2025-03-11）
  - 现在 0 美元/月：dev.to（2026-06），引用作者 X 简介
- **BlenderMCP**
  - 仓库：GitHub ahujasid/blender-mcp，已改名 mcp-for-blender
  - PyPI 月下载 539,997：pypistats API，2026-11-04 实测
  - 450 万+ 用户：mcp-for-blender.com 首页自报
  - Premium 10/20/60 美元每月：/premium 页面，内含 Meshy、Tripo、Hunyuan、Rodin 生成额度

## 3 代码即 CAD（cad-as-code）

- **Adam AI CAD**
  - 作品：X @zachdive 1882858765613228287（2025-01-24，首发）
  - 其他链接：YouTube EHu6Vrqo69A（用户点名）、adam.new、GitHub Adam-CAD/CADAM
  - 种子轮 410 万美元、用户生成 100 万+ 模型：adam.new/seed
  - ARR 900 万美元+：Caplight 页面的「Market signals」（2026-05-18），是第三方信号，不是公司披露
  - 没写进卡：TechCrunch（2025-10-31）里的「1000 万+ 社媒曝光、数万用户」
- **text-to-cad**
  - 作品：GitHub earthtojake/text-to-cad；X 2047072107612303692（2026-04-22）；官网 texttocad.dev
  - README 写明：agent 写 build123d 脚本 → 出 STEP/STL/3MF/GLB，带 DFM 检查，能接 SendCutSend 和 3D 打印
  - 缺口：没有下载量或采用方数字。cad-server 的 PyPI 月统计显示为 0，像是刚改名
- **AI 电路板外壳**：小红书 天桥底下一书童 6aaaa52f
  - 正文只有话题标签，「Codex × FreeCAD」来自封面
  - 没写用了哪个 FreeCAD MCP，所以没挂 freecad-mcp 仓库

## 考虑过但没用的候选

- 白模预演
  - 千叶真名「很多承接 Blender 白模的单子」（6ad89594，321 赞）：商业信号最直接，但封面是纯文字。场景 desc 用了它的结论。第一备选
  - 马里亚纳仇人 GPT6 + Blender + Seedance 2.5（6a9e999d，841 赞）：和小林Kara 重复
  - 天梦君 Blender MCP 16 机位实验（6a59768b，435 赞）：有数据（73% 切点命中），但热度低
  - Reid Hannaford（X 25 万播放）、WTR（X 12.5 万）：同一条路线，PJ 卡已经覆盖
  - 三三科技生活「一个插件打通 3D、视频」（6adae028，2.1k 赞）：正文缺失，插件名核实不了（可能就是 Higgsfield）
  - 何同学 iPhone 18 片头 × Hyper3D（6abcbf3a，1.9k 赞）：3D 用来预演实拍，不经视频模型，也不是 LLM 写代码
  - Higgsfield「Seedance 2.5 vs Blender blockout」X 帖：fxtwitter 返回 404，核实不了
  - Code Video Model、VideoCoCo：论文阶段，没有产品
  - Intangible（2025-03 种子轮 400 万美元）：3D 预演工具，没见到用白模驱动视频模型的官方功能
  - Luma Modify Video：通用视频改写，没找到白模出片的官方案例
  - Autodesk Flow Studio（原 Wonder Dynamics）：方向相反，是视频转 3D 和 CG 角色
  - Cuebric：做 LED 虚拟拍摄的 2.5D 背景，不用白模当参考
  - Kling Motion Control、Runway：参考的是动作视频或通用视频改写，没见到用 3D 白模定位的官方用法；没深查
- 3D 世界与资产
  - KurTips Blender + Tripo 荷塘（6ab1e3d9，1.76 万赞）：手工 Blender 加 Tripo 生成，没有 LLM 写代码
  - KaRmAr「100% GPT 3A 级 Blender 场景」（6aa4009e，3.3k 赞）：作者自称标题党
  - Lala罐头 梵高小岛（6ad1f470，6.8k 赞）：小王子同款思路，内容重复。第一备选
  - 祖师傅 Codex 批量做 2770 个城市资产（6aaaa452，648 赞）：资产量产这个角度好，但热度低，场景已经满 5 张
  - 星川同学 Astra 几何节点植物（6aa6779f，2.3k 赞）：个人技巧，没有产品也没有数字
  - 单依纯蛋岛 H5（6ae95741，3.3k 赞）：像粉丝自制，写着「即将上线」，没找到上线地址
  - Big喷菇 3D 房间主页（6a604b38，4.3k 赞）：属于 webdev 作品集场景，留给 web 族
  - 机械章鱼（6ae581d7）、乌头蜜森林（6ad46767）、Leon Lin 和 Meng To 的 Opus three.js 作品：同类，热度不如果冻海岛
- CAD 与打印
  - Zoo Text-to-CAD：按分钟计费，融资约 1000 万美元，没有 ARR，不如 Adam
  - Hitem3D、Rodin、Meshy 手办：走 diffusion，不是代码驱动

## 尚未补全

- Cozy Creek 套件销量
- 果冻海岛的在线地址
- text-to-cad 的下载量和采用方
- Adam 的 ARR 只有第三方口径
- Higgsfield 插件自己的使用量

