# Vibe Video 开源项目调研（README 实读）

- 采集：2026-11-04；README 取自 `raw.githubusercontent.com/<repo>/HEAD/README.md`（全部 31 个均为 README.md）
- 星标：`figure_src/vibe-video/repos.json`；echris6/motion-video-kit 不在 json 里，取自 GitHub API（同日）
- 原则：只写 README / 仓库里能看到的内容；没有的写「未提及」，拿不准的写「未核实」
- Demo 目录：`figure_src/vibe-video/repo_demos/<owner>__<repo>.<ext>`
- Used-by 口径
  - **第三方**：README 点名外部公司 / 创作者在用，并给了链接
  - **自用**：作者本人或作者所在公司在用
  - **合集**：本身是合集，条目即创作者原帖
  - **无**：README 里没有（赞助商 / Launch Partner 不算）

## 总表

| repo | 类型 | 场景 | used-by 证据 | demo 文件名 |
|---|---|---|---|---|
| remotion-dev/remotion | 框架 / 渲染器（React） | 通用；批量渲染、动画资产库、视频编辑器类应用 | 无（只有 Showcase 链接；旁证：本表 7 个项目基于它） | remotion-dev__remotion.webp |
| remotion-dev/skills | 官方 Skill | 宣传片、标题卡、地图动画、字幕 | 无（有第三方实测） | — |
| heygen-com/hyperframes | 框架 / 渲染器（HTML+GSAP）+ Skill | 产品发布、PR 讲解、数据可视化、社媒、文档转视频 | **第三方**（HeyGen、OpenAI、tldraw、TanStack 等） | heygen-com__hyperframes.png |
| hypit-ai/hypit | Skill + 工作流系统 | 爆款克隆、UGC、播客、街采、带货广告 | 无（只有 Launch Partners） | hypit-ai__hypit.gif |
| motion-canvas/motion-canvas | 框架（TS）+ 编辑器 | 信息类矢量动画 + 配音同步 | 无 | — |
| 3b1b/manim | 渲染引擎（Python） | 数学科普 | 自用（3Blue1Brown） | 3b1b__manim.jpg |
| ManimCommunity/manim | 渲染引擎（Python） | 数学科普 | 无（只提 3B1B 风格示范） | — |
| lemomo-ai/lemo-opuscar | Skill / Plugin（风格库） | 风格化短片、纪实、新闻、信息图 | 自用 + 社区贡献风格 | lemomo-ai__lemo-opuscar.jpg |
| feitangyuan/onetake | Skill | 一镜到底发布片、预告片、功能演示 | 自用 | feitangyuan__onetake.gif |
| digitalsamba/claude-code-video-toolkit | 工具包（Skill + 命令 + 模板） | Sprint review、产品 demo、release notes、竖屏科普 | 自用（Digital Samba 公司） | digitalsamba__claude-code-video-toolkit.jpg |
| echris6/motion-video-kit | Skill kit | 企业商业广告、3D 产品 spec 广告 | 无（匿名客户，未核实） | — |
| op7418/guizang-product-video-skill | Skill | 软件更新宣传片 | 自用（归藏 / CodePilot） | op7418__guizang-product-video-skill.jpg |
| alchaincyf/huashu-art-motion | Skill | 艺术风格动画、名画穿越、口播解说动画 | **第三方**（被 Open Design 收录）+ 自用 | alchaincyf__huashu-art-motion.jpg |
| Vincentwei1021/video-shotcraft | Skill（Remotion） | 产品宣传片 | 无（Showcase 页未核实；只有赞助商） | Vincentwei1021__video-shotcraft.webp |
| Vincentwei1021/anything2explainer | Skill（Remotion） | 黑底 MG 科普讲解 | 无 | Vincentwei1021__anything2explainer.jpg |
| Vincentwei1021/video-talkcraft | Skill（Remotion） | 口播 / 解说视频 | 无 | Vincentwei1021__video-talkcraft.png |
| nateherkai/herk-edit-kit | Skill kit（HyperFrames） | 口播剪辑、Reels / Shorts、showreel | 自用（YouTuber Nate Herk） | —（MP4 均超过 15 MB） |
| showlab/Code2Video | 研究框架（Manim） | 教学 / 知识点视频 | 研究机构（NUS Show Lab，ICML 2026） | showlab__Code2Video.gif |
| liyupi/ai-promo-video-maker | Skill / 规范 + 模板（Remotion） | 4K 产品宣传片 | 自用（鱼皮自家产品） | liyupi__ai-promo-video-maker.jpg |
| calesthio/OpenMontage | Agent 制作系统 | 讲解、预告、纪录蒙太奇、口播、切片、本地化 | 无（只有官方 YouTube / 社区区） | calesthio__OpenMontage.mp4 |
| nexu-io/motion-anything | 动效引擎 / 本地 App | 网页 UI 动效、发布视频 | 无 | nexu-io__motion-anything.gif |
| xiazhuo123456789/vibe-knowledge-video | Skill（Canvas） | 抖音电影感知识短片 | 无 | — |
| yihui-dev/awesome-opus5-5-videos | 作品 + prompt 合集 | MG、讲解、3D、游戏 | 合集 | yihui-dev__awesome-opus5-5-videos.webp |
| zhuyansen/awesome-claude-video-skills | Skill 合集 + 实测 | 10 类视频 skill | 合集 + 第三方实测 | zhuyansen__awesome-claude-video-skills.jpg |
| opusvideo/awesome-claude-video | 作品合集 | 广告、MG、讲解、故事、3D、MV、剪辑 | 合集（含 Higgsfield 等） | opusvideo__awesome-claude-video.jpg |
| zhuyansen/awesome-opus-5.5-video | 作品合集 | MG、产品、讲解、故事、3D、游戏、MV | 合集 | zhuyansen__awesome-opus-5.5-video.jpg |
| ismoshushi/awesome-opus-video-skills | Skill 索引 | 4 类视频 skill | 无（纯索引） | — |
| joeseesun/opus-video-prompts | Prompt + 案例合集 | 广告、MG、科普、叙事、3D、MV | 合集（含 Danny Stuart 博文等） | — |
| mexicat/pdoom-video | 作品源码（three.js） | MV / 歌词视频 | 自用（作品本身） | mexicat__pdoom-video.jpg |
| JohnHeibel/PDoomVideo | 作品源码（p5.js） | MV / 手绘叙事动画 | 自用（作品本身） | JohnHeibel__PDoomVideo.gif |
| 0xsline/OpenChatCut | 编辑器（MCP，Remotion） | 口播 / 访谈剪辑、短视频、MG | 无（只有赞助商） | 0xsline__OpenChatCut.png |

---

## remotion-dev/remotion（★70,381）

- **是什么**
  - 用 React 程序化做视频的框架 / 渲染器（"Make videos programmatically with React"）
  - 首条卖点："Make videos agentically: Turn your idea into a video using your agent."
  - 栈：React + Node.js
    - 渲染：Node.js API / Lambda / Vercel / 客户端
    - 编辑：Studio 交互编辑
- **场景**
  - README 没按题材分
  - 列了三类用途：动画资产库（"Design systems"）、批量渲染（"Render millions of videos"）、做视频编辑器类应用
  - 文档目录有 Elements / Effects / Transitions / Captions / SFX
- **Used-by**
  - README 未点名用户，只有入口：Showcase https://remotion.dev/showcase 、Experts https://remotion.dev/experts （内容未核实）
  - 旁证（本表其他 README）：shotcraft、anything2explainer、talkcraft、ai-promo-video-maker、claude-code-video-toolkit、OpenMontage、OpenChatCut 都用它渲染；HyperFrames 写 "inspired by Remotion"
- **实践**
  - 起步：`npx create-video@latest`
  - 官方 Agent Skills：https://www.remotion.dev/docs/ai/skills
  - 许可："requires obtaining a company license in some cases"
- **Demo**
  - remotion-dev__remotion.webp：README 头图 "Studio, Codex and VS Code working together"
  - 这是工具界面截图，不是成片

## remotion-dev/skills（★6,237）

- **是什么**
  - Remotion 官方 Agent Skills，"define best practices for working in Remotion projects"
  - 支持 Claude Code / Codex / Kimi Code / Cursor
  - 安装：`npx skills add remotion-dev/skills`
- **场景**（README 示例 prompt）
  - 宣传片（"Make a promo video for a record store"）、标题卡
  - 地图动画（路线、3D 地理飞越；Mapbox / CesiumJS）
  - 字幕、SaaS 化
- **Used-by**
  - README 未提及
  - 旁证：zhuyansen 实测中 4.5 分钟出片，观感 "Close to the no-skill film"；被列为 🥉 "To build your own design in Remotion"
- **实践**
  - 不确定用哪个就用 `/remotion-best-practices`（"encompasses all other skills"）
  - 写代码前先 `/remotion-docs` 查当前 API（"look up current API references ... before implementing"）
  - `/remotion-interactivity`：让代码在 Studio 里可编辑
  - `/remotion-upgrade`：同步升级 skills
- **Demo**：无（README 只有文字）

## heygen-com/hyperframes（★78,197）

- **是什么**
  - "Write HTML. Render video. Built for agents."
  - 原理：HTML/CSS + 可 seek 的动画 → headless Chrome 逐帧 seek → FFmpeg 编码，输出确定性 MP4
  - 动画适配器：GSAP / CSS / Lottie / Three.js / Anime.js / WAAPI
  - 配套：CLI、Studio、约 450 个 catalog 块、9 个 skills、AWS Lambda 渲染
  - 许可：Apache 2.0
- **场景**（"What You Can Build"）
  - 产品发布 / 功能公告
  - PR walkthrough（动画 code diff）
  - 数据可视化、chart race、地图动画
  - 社媒 kinetic 字幕
  - Docs / PDF 转视频
  - `/style-sampling` 五种风格：Collage / Finance / Science / 3D Brand / 3D True Crime Explainer
- **Used-by**（README + ADOPTERS.md https://github.com/heygen-com/hyperframes/blob/main/ADOPTERS.md ）
  - 生产在用
    - HeyGen
    - tldraw：自动生成 PR walkthrough 视频
    - OpenAI（Brent Schooley）："Edits OpenAI developer videos in the cloud ... agent review-and-revise loop"
    - reap.video、Typeframe
    - THU-MAIC：OpenMAIC 课堂一键导出 MP4
    - Mini Course Generator、PandaStudio
    - Skyflo：产品发布片
    - Nate Herk：Herk Edit Kit
  - 评估中：TanStack、OptinMonster
- **实践**
  - Agent 用 `npx hyperframes skills update` 安装（版本与 CLI 对齐；"skills add ... can lag main by hours"）
  - `/hyperframes` 标为 "Read first"
  - 生产循环："plan the video, write valid HTML, wire seekable animations, add media, lint, preview, and render"
  - `/hyperframes-registry`："Use before hand-building any named visual"
  - "Deterministic: same input, same frames, same output"
  - frame.md：把网页用的 design.md "inverts it for the frame"
- **Demo**：heygen-com__hyperframes.png，frame.md 设计模板 Biennale Yellow（1600×900）

## hypit-ai/hypit（★27,716）

- **是什么**
  - "Clone any viral video with AI agents"
  - 用 SVML 源文件描述整条视频；字幕 / B-roll / 特效 "anchored to words instead of seconds"
  - 栈：TypeScript / Node 22；headless Chromium 并发渲染（例子用 64 进程）；WhisperX 词级对齐
  - 生成模型可选：Seedance 2 Mini、GPT Image 2 等
- **场景**
  - UGC 排名榜、播客切片、街头采访
  - 付费社媒广告、TikTok Shop 带货、AI UGC 口播
  - 多语本地化
  - "Code-rendered videos"
- **Used-by**
  - 无用户案例
  - "Launch Partners"：Watcha、TokenDance、AgentSky、AutoClaw(Z.ai)、OpenAgents、Monid、HiAPI、Pollo API、BeatAPI
    - 这些是合作 / 服务商，不算用户
    - OpenAgents 有一篇 pilot user 文：https://openagents.org/blog/posts/2026-09-08-pilot-user-program-zh-hypit （未核实）
- **实践**
  - 一条工作流出 100 个变体："reuse the composition and existing material; generate the parts that change"
  - 组件可插拔："swap the host without touching the captions"
  - 生成模型不是必需的
  - 示例成本：每条 $1.07–$1.15
- **Demo**：hypit-ai__hypit.gif，"SVML source on the left ... video rendered live on the right"

## motion-canvas/motion-canvas（★19,665）

- **是什么**
  - TypeScript 库（用 generator 写动画）+ 实时预览编辑器
  - 配套：Vite 插件、2d 渲染器、player 元素
- **场景**："informative vector animations and synchronize them with voice-overs"（科普讲解）
- **Used-by**：未提及
- **实践**
  - README 只讲安装和开发，没有 agent 相关建议
  - 旁证：anything2explainer 拿它当对照（"Remotion or Motion Canvas by hand"）；HyperFrames 的 `/remotion-to-hyperframes` 也能迁移它的项目
- **Demo**：无（只有 logo）

## 3b1b/manim（★96,078）

- **是什么**
  - ManimGL："precise programmatic animations, designed for creating explanatory math videos"
  - 依赖：Python ≥3.10、FFmpeg、OpenGL、LaTeX（可选）
- **场景**：数学科普讲解
- **Used-by**
  - 3Blue1Brown（https://www.3blue1brown.com/ ）：本来就是作者给自己做视频的项目，视频源码在 https://github.com/3b1b/videos
  - 中文文档由 manim-kindergarten 维护：https://docs.manim.org.cn/
- **实践**
  - CLI 旗标：`-w` 写文件 / `-o` 写完打开 / `-s` 只看末帧 / `-n` 跳到第 n 个动画
  - `custom_config.yml` 控制输出路径和画质
- **Demo**：3b1b__manim.jpg，README 链接的 demo 视频 https://www.youtube.com/watch?v=rbu7Zu5X1zI 的缩略图

## ManimCommunity/manim（★42,205）

- **是什么**
  - 社区版 ManimCE（fork 自 3b1b/manim），Python 数学动画框架
  - 配套：Docker 镜像、Jupyter `%%manim` magic
- **场景**：数学 / 讲解视频（"as demonstrated in the videos of 3Blue1Brown"）
- **Used-by**
  - README 只拿 3Blue1Brown 当风格示范
  - 旁证：Code2Video 基于 Manim Community v0.19.0；OpenMontage 把 ManimCE 列为工具
- **实践**
  - `manim -p -ql`：预览 + 低画质快渲
  - `-s` 只看末帧，`-n` 跳动画
- **Demo**：无（只有 logo 和命令行示意图）

## lemomo-ai/lemo-opuscar（★11,609）

- **是什么**
  - Claude Code plugin：66 种影片风格，每种 = 风格 prompt + 一支全代码 demo 片
  - 栈：canvas / WebGL 逐帧渲染；用免费采样库做原创配乐；TTS 旁白（默认 Kokoro）
  - 依赖：Node 20+ / ffmpeg 7+ / Python 3.11+
- **场景**
  - 风格化短片：手绘、水墨、版画、像素、3D 材质……
  - Evidence Films：数据都有出处
  - Edit & Documentary：用真实素材做新闻 / 纪实
  - 信息图 / Keynote
- **Used-by**
  - 作者自用："Every film here was made by me, with Claude Opus 5.5"
  - 社区贡献风格：Memphis Diorama by @EianLu（https://x.com/EianLu ）
  - 代表作：OPUSCAR 98（6:31）
- **实践**
  - 模型绑定："tuned for Claude Opus 5.5; other models may not reproduce them well"
  - Agent 读三份文档：DIRECTOR.md / TECHNIQUE.md / STYLE.md，"works like a small studio"
  - 开工前一次问清：选题、素材、要不要先看 storyboard
  - 自定义风格五步
    1. 逐题规划
    2. 看改动总结
    3. 先出一帧 style frame，和原风格并排对比
    4. 出 15–30 秒 demo
    5. 确认后保存
  - 一支片约 30–60 分钟；默认 1920×1080 / 24fps
  - "No video generation, no stock footage"
- **Demo**：lemomo-ai__lemo-opuscar.jpg（docs/cover.jpg，全风格总览）

## feitangyuan/onetake（★3,679）

- **是什么**
  - Claude Agent Skill，专做一镜到底的连续镜头动效
  - 栈
    - 画面：单个 HTML + 动作库 `lib/motion.js`，Playwright 渲染
    - 验收：Python oracle（`probe.py` / `verify_promo.py`）
    - 其他：ffmpeg；旁白用 faster-whisper + Kokoro
  - 许可：PolyForm Noncommercial
- **场景**：产品发布片、预告片、功能演示、概念广告、App promo
- **Used-by**
  - 无外部用户；12 支案例都是作者做的（X @paojiaofty https://x.com/paojiaofty ）
  - 商业版：onetake Pro https://onetakemotion.com
  - 旁证：zhuyansen 榜单 🥈
- **实践**
  - 镜头交接处是设计重点："something on screen survives and visibly becomes the next beat"
  - 连贯度用 carry score 量化：v1 = 0.00 被否 → v3 = 0.75 通过
  - oracle 还会拒掉：镜头等长、没有静止段、爆音、快动作没有运动模糊、主体出画
  - 镜头长度至少相差 4 倍；出三个概念选一个
  - 真运动模糊：180° 快门多次采样，在线性光下平均
  - 草稿 1080p30，成片 4K60
  - 产品 UI 按截图用 HTML 重建，"No screen recording"
- **Demo**：feitangyuan__onetake.gif（发布片 hero.gif，5.5 MB）

## digitalsamba/claude-code-video-toolkit（★2,426）

- **是什么**
  - Claude Code 视频制作工作区：skills + 15 个 slash 命令 + 模板 + Python 工具
  - 栈
    - 合成：Remotion + moviepy
    - 开源模型（跑在 Modal / RunPod）：Qwen3-TTS、FLUX.2、ACE-Step、LTX-2、SoulX / SadTalker
    - ElevenLabs 可选
- **场景**：sprint review、产品 demo、release-notes 视频（UI 从源码重建）、9:16 科普、发布广告、视频随笔
- **Used-by**
  - Digital Samba（作者所在公司）：作者原话 "creating sprint review videos for the AI mobile development arm of Digital Samba"（https://www.digitalsamba.com/ ）
  - 成片样例：https://demos.digitalsamba.com/video/ds-release-650.mp4
  - 社区 add-on：VOICEPEAK 日语 TTS、arkiv、Upload-Post、CommentKeyword
- **实践**
  - 入口：先 `/setup`，再 `/video`
  - 流程："Script → Assets → Scene Review → Design → Audio → Preview → Render → Publish"
  - `project.json` 跟踪多 session 生命周期，每个项目自动生成 CLAUDE.md 方便接着做
  - 云 GPU 推荐 Modal
  - 成本："voiceover ~$0.01, AI video clips ~$0.23"
  - 作者格言："Be brave. Experiment."
- **Demo**：digitalsamba__claude-code-video-toolkit.jpg（ds-release-650 缩略图）

## echris6/motion-video-kit（★1,342，API 2026-11-04）

- **是什么**
  - Claude Code skill kit（business-motion-film），给真实企业做 "premium, launch-style commercials"
  - 栈：AI 素材 + HTML/GSAP 代码动效 + 选择性 Three.js
  - 渲染推荐 HyperFrames，但原则与渲染器无关
  - 脚本依赖 ffmpeg / ebur128
- **场景**：商业广告、服务宣传片、3D 设备 spec 广告、样片 reel、explainer
- **Used-by**
  - 无外部用户；三支样片是作者做的
  - 提到 "a demanding client re-shaped for seven rounds"，客户没具名（未核实）
- **实践**
  - Gauntlet 循环："builder ≠ judge, fresh critics on the actual render, item-by-item verification, and a ledger"
  - 运动语法：6 条规则 + 16 个机制，来自 28 部 SaaS 发布片
  - 可量化质检：frozen time、loudness、contrast、brand colour
  - 音乐倒推对齐："back-timing a real track so its own ending lands on the end card"
  - Three.js 场景要 "deterministic, seekable"
  - "Never present AI-generated imagery as a real customer"
- **Demo**：无（README 没有图）

## op7418/guizang-product-video-skill（★898）

- **是什么**
  - 归藏的产品宣传片 skill：复用真实产品组件和设计语言
  - 栈
    - 画面：React + esbuild + Playwright 出帧 → FFmpeg；GSAP 主时间轴
    - 背景：Three.js / canvas
    - 声音：代码合成配乐和音效
  - 也可以沿用 HyperFrames 工程；许可 AGPL-3.0
- **场景**：软件版本更新宣传片（默认 45–60 秒、横版、中文）+ 封面
- **Used-by**
  - 作者自用："我把自己做 CodePilot 宣传片时反复打磨的流程，整理成了这个 skill"
  - 示范片：CodePilot、Zed、T3 Code（是否为官方委托，未提及）
- **实践**（七步）
  1. 定范围
  2. 找真实内容，挂载真实组件
  3. 定方向：三个方向选一个；"每个视觉手法都要说得出'因为产品有什么'"；字号、界面倍数、镜头表先写成数字
  4. 逐镜头搭建，每镜出静帧对照
  5. 配声音，关键音效出现时音乐让位
  6. 审片：看联系表、每个转场、全尺寸帧
  7. 做封面
  - 同一工作区连续做片时，避开上一支用过的开场和转场
  - 音乐优先级：用户给的 → 本机能跑的生成模型 → 代码合成
- **Demo**：op7418__guizang-product-video-skill.jpg（hero「软件更新了，宣传片呢？」）

## alchaincyf/huashu-art-motion（★6,099）

- **是什么**
  - 花叔的艺术动画 skill：36 种风格配方 + 9 种解说语法
  - 栈
    - 画面：Canvas 场景 + 一条 SVG 管线；Playwright 渲染
    - 脚本（uv / Python）：`breakdown.py` 拆解、`qa.py`、`film_gate.py`、`deliver.py`
    - 配乐：纯代码合成
  - 人物：生图模型出帧，代码负责合成
- **场景**
  - 艺术风格动画、名画穿越、长卷穿越片
  - 口播解说动画段：Kurzgesagt / Vox / 白板 / 3B1B / 发布会 / 财经图表
  - 复刻参考动画
- **Used-by**
  - Open Design（nexu-io）的 motion-design skill 把它列为设计来源，并收了一份适配版
    - https://github.com/nexu-io/open-design/blob/main/skills/motion-design/SOURCES.md
    - https://github.com/nexu-io/open-design/tree/main/skills/huashu-art-motion
  - 作者接进自己的口播管线，做了《花叔穿越名画》（23 种画风，2:08）
- **实践**
  - 先拆解（量转场、拟合节拍网格、看运动热图），再按机制复刻；否掉了"一张张画之间做转场"
  - "先设计一帧，再让它动起来"
  - 交付前：先跑 `qa.py`，再"派一个没参与制作的 agent 只看成片挑问题"
  - 反 PPT 门禁："整片几乎没有镜头内快动作就红灯，不出片"
  - 积累经验："我们不只是为了复刻，我需要你积累经验"，有效做法写进 `07-正面经验.md`
- **Demo**：alchaincyf__huashu-art-motion.jpg（35 种风格总览）

## Vincentwei1021/video-shotcraft（★16,465）

- **是什么**
  - Claude Code / Codex skill，用 Remotion 做可编辑的产品宣传片
  - 镜头库：124 张配方卡 / 150 个镜头
  - 配套：Motion Workbench（CapCut 式浏览器编辑器）、剪映草稿导出、Freesound 音效检索
  - 许可：Apache-2.0
- **场景**：产品宣传片，镜头分 10 类（开场、运镜、转场、字效、UI 入场、数据、片尾等）
- **Used-by**
  - 没有具名用户
  - 社区 Showcase：https://vincentwei1021.github.io/video-shotcraft/showcase.html （未核实）
  - 赞助商 APIMart / PackyCode / AWS 不算用户
  - 配方提炼自 ClickUp、Notion、Figma 等的官方片（"none of these companies are affiliated"）
- **实践**
  - 流程："captures your real pages, picks shots ..., storyboards the film, animates it with Remotion, cuts it to the beat, adds sound design, checks every frame"
  - "It is not a video generator. Every frame is drawn by code from your own screenshots"
  - 可以按名字直接点镜头卡
  - 无头 Linux 渲染三坑
    - 加 `--concurrency=1`
    - 用 chrome-headless-shell
    - `--browser-executable` 指向本地浏览器
- **Demo**：Vincentwei1021__video-shotcraft.webp（六个 Gallery 镜头拼图）

## Vincentwei1021/anything2explainer（★3,015）

- **是什么**
  - Claude Code / Codex skill："Topic in, narrated explainer video out"
  - 栈
    - 画面：Remotion 4（React + TS）
    - 配音：中文 edge-tts、英文 kokoro-82m，也可自带
    - 制作：多 agent 并行 build
  - 许可：PolyForm Noncommercial
- **场景**：黑底动态图形科普讲解（2–8 分钟，中英双语，1280×720，只做横屏）
- **Used-by**
  - 未提及
  - 视觉语言致敬抖音 @图灵宇宙（致敬对象，不是用户）
- **实践**
  - 9 阶段
    1. 搭项目
    2. 调研（每条事实带 URL）
    3. 旁白 + TTS，生成词级时间轴
    4. 分镜
    5. overlay / 基础元素
    6. 试点一组 + 30 秒样片
    7. 并行 build（每个 agent 5–7 镜）
    8. 渲染 + 帧指标
    9. 每章一个 QC agent，修复后交付
  - 4 个人工检查点：时长和语言、旁白定稿、配音、前 30 秒
  - 旁白定稿处"is the cheapest place to intervene"；配音后文字冻结
  - "Every animation is a pure function of the frame number with seeded randomness"
  - "Every fact is sourced"
- **Demo**
  - Vincentwei1021__anything2explainer.jpg：README 链接的 `examples/rag/frames/` 里的一帧（ref_vector_space_f2990.jpg）
  - README 本身只有成片视频（https://github.com/user-attachments/assets/e2771c68-a28c-4459-ac5a-a5b685181eeb ，10 MB）

## Vincentwei1021/video-talkcraft（★2,052）

- **是什么**
  - shotcraft 的口播篇
  - 流程：口播稿 + 成品配音 → 字级对齐 → SHOTBOOK 分镜 → Remotion 成片
  - 内容：108 张动效卡 + 工作台
  - 栈
    - 时间戳：FireRedASR2 / faster-whisper
    - 人脸安全区：YuNet
    - 配音：可选 Fish Audio TTS
  - 许可：PolyForm Noncommercial
- **场景**：知识科普、产品评测、新闻解读、观点锐评（中文优先）
- **Used-by**
  - 未提及
  - 社区贡献卡来自 @scpcn01vision-oss（贡献者，不算用户）
- **实践**
  - 字级同步：偏差中位 20–40ms
  - 七层反 PPT：极缓推拉相机 + 让位 + 六式承接转场，"静止帧在结构上不可能出现"
  - 首镜先做先确认：先搭全片骨架，样板镜出有声预览
  - 三重验收：机器检测 + 逐 cue 音效能量 + 独立评审
  - 一轮审片即交付：修完 P0/P1 就交，累计不超过 3 轮
  - 效率
    - 分段并行渲染：改一镜 53 秒出新片
    - 评审用 3×4 拼图：token 从约 16 万降到约 4 万
- **Demo**：Vincentwei1021__video-talkcraft.png（108 张动效预览画廊）

## nateherkai/herk-edit-kit（★2,523）

- **是什么**
  - YouTuber Nate Herk 的剪辑 kit（原 HyperFrames Student Kit），供 Codex / Claude Code 用
  - 内容：15 个 skills、406 张 MG 卡片
  - 栈：HyperFrames + GSAP；ElevenLabs Scribe 转写（可换 Whisper）；Kie.ai 生成素材（可选）
- **场景**：口播剪辑（剪气口、错词、讲故事）、Reels / Shorts、motion showreel、广告
- **Used-by**
  - Nate Herk 本人（https://www.youtube.com/@nateherk ）：三支短视频 "edited end to end by an AI agent running the editing skills in this kit"
  - HyperFrames 的 ADOPTERS.md 也列了他
- **实践**
  - 每条剪辑意见都沉淀成规则："how every note becomes a rule in a skill"
  - 先把提议的错词剪辑点给人看
  - showreel："Pick one motif that transforms through every chapter, cut on the music's beat grid ... Show me the storyboard and beat sheet before building"
  - short-form："Build a truthful hook and payoff, preserve my meaning"；先用已有素材，再提生成
- **Demo**
  - 未下载：README 只有 4 支 MP4，都在 24–34 MB，超过 15 MB 上限
  - 例：https://github.com/user-attachments/assets/056b46e9-7379-4e71-b825-20fb9f8e9555 （15 秒 showreel，30 MB）

## showlab/Code2Video（★2,234）

- **是什么**
  - NUS Show Lab 的研究框架（ICML 2026），用可执行的 Manim 代码生成教学视频
  - 三个 agent：Planner（分镜）/ Coder（可调试代码）/ Critic（带 anchor 修版面）
  - 另发 MMMC benchmark（117 个主题）
- **场景**：教育 / 知识点讲解（3Blue1Brown 风格）
- **Used-by**
  - 研究机构作者，论文 https://arxiv.org/abs/2510.01174
  - @_akhaliq 转发 https://x.com/_akhaliq/status/1974189217304780863 （属于传播，不是使用）
- **实践**
  - 模型推荐
    - Coder："Best Manim code quality achieved with Claude-4-Opus"
    - Critic：Gemini（gemini-2.5-pro-preview-05-06）
  - 评估三维：TeachQuiz（知识传递）、AES（美学）、效率（token / 时间）
  - README 有和 Veo3 / Wan2.2 的对比
- **Demo**：showlab__Code2Video.gif（Fourier Series，1.2 MB）

## liyupi/ai-promo-video-maker（★433）

- **是什么**
  - 程序员鱼皮的产品宣传片制作器：AGENTS.md 工作规范 + Remotion 模板 + 脚本，可装成 Skill
  - 栈：Remotion 4、Playwright 4K 截图、ElevenLabs（可选）或 Mixkit 曲库、FFmpeg
  - 许可：MIT
- **场景**：App / 网站 / SaaS / 开源项目 / 课程 / AI 模型的 4K 宣传片，横竖屏都行
- **Used-by**
  - 五支成片：编程导航、面试鸭、鱼皮 AI 导航（作者自家产品）、Claude Fable 5.5 抢先看、Vibe Coding 教程
  - README 只有截图，没给产品链接
- **实践**
  - 推荐模型："Claude Opus 5.5 或者更先进的模型"；弱模型会跳过校验，或做成千篇一律的深色科技风
  - 先出 3–4 个风格方向的样帧，让产品作者挑
  - 真实产品当主角
    - 每段至少一张真实截图
    - 全片不少于 8 张
    - 还要一段 8 张以上真实作品的快速蒙太奇
  - 节奏底线
    - 快切至少停 0.65 秒，网址至少 3 秒
    - 开场 3 秒内出现痛点或亮点
    - 任何时刻往后 2 秒内必须有新信息
  - 声音校验：旁白逐句转写回文字比对，品牌名错一个字就不合格；配乐让用户亲耳试听
  - 经验沉淀：60+ 条踩坑记录，每支片子做复盘
- **Demo**
  - liyupi__ai-promo-video-maker.jpg：编程导航那支的画面（docs/images/case-codenav.jpg）
  - README 头图 showcase.gif（5.6 MB，5 支片开场合集）通过代理反复下载失败，改用这张静图

## calesthio/OpenMontage（★75,830）

- **是什么**
  - "open-source, agentic video production system"，AI 编程助手本身就是编排器
  - 规模：12 条管线、100+ 工具、60+ provider、700+ skill / 知识文件
  - 渲染：Remotion 或 HyperFrames + FFmpeg，也用 Blender
  - provider（Veo / Kling / Seedance / Piper / ElevenLabs / Suno…）都可选，零 key 也能跑
  - 许可：AGPLv3
- **场景**：讲解、MG、数字人口播、电影感预告、长视频切片、纪录蒙太奇（真实开放素材）、本地化配音、播客、录屏 demo、角色动画
- **Used-by**
  - 没有具名用户
  - 官方作品：YouTube @OpenMontage https://www.youtube.com/@OpenMontage （"every video includes the full prompt, pipeline, tools used, and cost"）
  - 社区：Show and Tell 讨论区
- **实践**
  - 固定管线："research -> proposal -> script -> scene_plan -> assets -> edit -> compose"，每阶段一个 director skill
  - 给 agent 的话："Do not improvise the production workflow"
  - 质量闸门
    - 人审强制：提案、脚本、分镜、素材、发布都要停下等确认
    - 渲染前：slideshow risk 6 维打分，防 "animated PowerPoint"
    - 渲染后：ffprobe + 4 处抽帧 + 音频电平 + 字幕检查
  - 预算：总额默认 $10，单次超过 $0.50 要确认
  - 从参考视频开始比从空白 prompt 更快
- **Demo**：calesthio__OpenMontage.mp4（"SIGNAL FROM TOMORROW" 预告，5.3 MB；Veo 镜头 + Remotion 合成）

## nexu-io/motion-anything（★1,032）

- **是什么**
  - Open Design 家族的 "agentic motion layer"：本地对话式动效引擎
  - 能做什么
    - 一句话生成动效页面 / 发布视频
    - 在运行中的页面上逐个组件改动效
  - 规模：8 个 agent 引擎 + BYOK；403 个 recipe、58 个 HyperFrames 视频模板
  - 零 npm 依赖；导出 JSON / CSS / React / Lottie / MP4 / GIF / SKILL.md
- **场景**：网页 UI 动效（kinetic text、shader 背景、交互反馈）、发布视频（WebCodecs 导出 MP4）
- **Used-by**：未提及
- **实践**
  - "taste is a feature: every recipe declares avoid_when and a restraint budget"，超出预算编辑器会警告
  - 始终尊重 prefers-reduced-motion；"GPU-safe properties only"
  - 按意图选 recipe："You never need to know a library name"
- **Demo**：nexu-io__motion-anything.gif（silk shader recipe）

## xiazhuo123456789/vibe-knowledge-video（★162）

- **是什么**
  - 复刻抖音「Vibe知识大赏」风格的知识视频 Skill（CodeBuddy / Claude Code / Codex / Cursor / Trae 都能用）
  - 栈
    - 画面：原生 JS + Canvas，页面暴露 `window.render(t)`
    - 出帧：Playwright 逐帧截图
    - 配乐：numpy 合成
    - 合成：ffmpeg
  - 许可：MIT
- **场景**：电影感知识短片——无配音、双语字幕、历史文献再现；1080p，2:00–2:45
- **Used-by**
  - 没有 skill 用户证据
  - 风格来源：@Iwanau / @Juno / 叁号暗房，README 说原片是 Opus 5.5 代码生成的（未给链接，未核实）
- **实践**
  - 七步：选题核实 → 剧本 → 分镜表 → 确认 → 代码 → 渲染 → 自检
  - "分镜表没写完不写代码"；每做两三站用 `--sheet 16` 看图
  - 第一版必有毛病，按质量门修两轮是正常流程
  - 数字纪律："先算后写"、固定种子、屏上计数是真的在数
  - 画面要一直在动：运动密度均值 3.97，静止秒少于 25%
  - 弱模型用 strict-mode 逐拍填空
- **Demo**：无（只有 badge）

## yihui-dev/awesome-opus5-5-videos（★13,397）

- **是什么**
  - Opus 5.5 写代码做的爆款视频 + 创作者原 prompt
  - 703 个 prompt，其中 418 个在 Skillry 上有 live remake
  - 技术标签：Canvas / SVG / GSAP / Three.js / GLSL
- **场景**：Motion graphics 58 / Explainers 16 / 3D 14 / Games 12
- **Used-by**（创作者原帖示例；身份未核实）
  - @anabology https://x.com/anabology/status/2103534482930491441
  - @moritzkremb https://x.com/moritzkremb/status/2103066071838466494
  - @deedydas https://x.com/deedydas/status/2102787937482252537
  - @alexalbert__ https://x.com/alexalbert__/status/2102466523164274839
  - @YouWareAI https://x.com/YouWareAI/status/2108825933608300653
  - @BThreeAgency https://x.com/BThreeAgency/status/2103739079745827092
- **实践**："Ask it to render the result as a single HTML file, then record the page if you want a video"
- **Demo**：yihui-dev__awesome-opus5-5-videos.webp（作品墙 mosaic）

## zhuyansen/awesome-claude-video-skills（★1,513）

- **是什么**
  - 能让 agent 做视频的开源 skill 合集
  - 规模：README 写 413 个 repo（repos.json 描述写 180，以 README 为准），每个都有 Agent Skills Hub 安全评级
  - 另做了 16 个 skill 的端到端实测
- **场景**：10 类——框架 72 / 宣传 77 / 讲解 73 / 剪辑 53 / 短视频 51 / 数字人 9 / 故事 25 / MG 26 / 脚本 10 / MV 17
- **Used-by**
  - 实测本身就是第三方证据
    - 设置：2026-10-11，用 Claude Code（Opus 5.5）做同一支 15 秒 promo
    - 结果：https://agentskillshub.top/best/claude-video-skills/#test-results
    - 原始数据：https://github.com/zhuyansen/agent-skills-hub/blob/main/ops/video-runs/RESULTS.md
  - "Made with Claude Opus 5.5" 一节：lemo-opuscar、PDoomVideo、ClaudeAnimationBase 等
- **实践**
  - 推荐：🥇 explainroo（2 分钟）/ 🥈 onetake / 🥉 remotion-dev/skills；hyperframes 做 15 秒 brief 用了 23.5 分钟
  - 核心结论："you may not need one for a simple promo. Claude Code with no skill made a film that passed every check in 4.4 minutes. A skill earns its place with a look, a workflow, or footage to edit."
  - 16 个全部 4/4 通过，差别在三处
    - 耗时：2.0–23.5 分钟
    - 声音：9/16 有
    - 观感：6 个接近无 skill 的默认片
- **Demo**：zhuyansen__awesome-claude-video-skills.jpg（16 个 skill + 无 skill 成片首句对比拼图）

## opusvideo/awesome-claude-video（★233）

- **是什么**：Opus 5.5 动画 / 视频合集，带原帖、prompt、工作流，另有 IMPLEMENTATION_GUIDES.md
- **场景**：产品广告、MG / UI、教育讲解、故事、艺术 / 3D、MV / 纪录 / 剪辑、模型对比
- **Used-by**（README 原帖链接）
  - Higgsfield @higgsfield_ai：Blender / After Effects 案例 https://x.com/higgsfield_ai/status/2102913101926731879
  - @deedydas：发布片 + 论文 Manim 讲解
  - @gregpr07：用 browser-use/video-use 把 13 条素材剪成发布片 https://x.com/gregpr07/status/2102984873351037161
  - @gavinpurcell：接 Runway MCP 做 5 分钟纪录片
  - @kimmonismus：用 Remotion 做 AI 史
  - @VincentWei93：shotcraft 作者
  - @other__reality：P(doom) MV
- **实践**（摘自条目）
  - 先建分镜再开始（@devteamdrew）
  - 三轮迭代：先形状 → 再纹理 → 最后交互（@SouranyPhomhome）
  - UI 循环片（@twoclipping）
    - 纯时间函数 HTML + 闭式弹簧
    - NumPy 节拍网格
    - 每帧 4 个 Playwright 子帧，用 FFmpeg 混合出运动模糊
    - 校验首尾帧能闭环
  - 单 HTML + HyperFrames + Python 配乐，"review and polish each second"（@Voxyz_ai）
- **Demo**：opusvideo__awesome-claude-video.jpg（"Mars Rover" 封面，@AndrewOnXYZ）

## zhuyansen/awesome-opus-5.5-video（★289）

- **是什么**
  - Claude 5.5 系列（Opus / Sonnet / Haiku / Fable）做的视频 / MG / 3D / 游戏合集
  - 只收原帖 ≥5,000 播放的；README 写 2,462 件，585 件带 prompt
  - 在线浏览：https://jasonzhu.ai/en/prompts/claude-opus-5-5
- **场景**：MG 325 / 产品 240 / 讲解 211 / 故事 215 / 3D 402 / 游戏 433 / 音乐剪辑 172 / 对比 464
- **Used-by**（示例；身份未核实）
  - @wesbos https://x.com/wesbos/status/2102450119975277027
  - @addyosmani https://x.com/addyosmani/status/2102436416437580159
  - @dotey：12 分钟 Transformer 讲解 https://x.com/dotey/status/2103683057689522564
  - 另有 @mattshumer_、@DotCSV、@MengTo、@magnific
- **实践**
  - 有条目标题就叫 "Motion showreel generated at xhigh effort"（@kenn）
  - "Model attribution is as stated by each creator and was not independently reproduced"
- **Demo**：zhuyansen__awesome-opus-5.5-video.jpg（"Claude Pop" MV 重制的 X 缩略图）

## ismoshushi/awesome-opus-video-skills（★30）

- **是什么**
  - 只收开源、可安装的视频 Agent Skill 的索引（133 个），只放链接
  - 每条字段：用途 / 渲染栈 / 安装 / 许可 / 是否专为 5.5
- **场景**：① 用代码出片（78）② 产品片 / 成片编辑 ③ 看视频 / 视频转 skill ④ 调外部视频模型
- **Used-by**：无（纯索引）
- **实践**
  - 定位："Opus 5.5 出片不是自己画像素，而是写渲染代码——Canvas、Remotion、p5.js、GSAP——用无头浏览器逐帧渲染，再用 ffmpeg 合成"
  - 安装约定：`npx skills add <owner>/<repo>`
- **Demo**：无（README 没有图）

## joeseesun/opus-video-prompts（★932）

- **是什么**
  - 向阳乔木整理：18 份完整提示词 + 54 个公开案例 + 9 种技术路线
  - 时间范围：2026-09-22 至 09-25（Opus 5.5 发布首周）
- **场景**
  - 擅长："动态图形、手绘/线稿/水墨动画、科普讲解、产品发布片、歌词 MV"
  - 不擅长："写实的真人镜头"
- **Used-by**（示例）
  - Deedy：一句话发布片，"1 分钟、约 2 美元"
  - Danny Stuart 博文：https://dannystuart.substack.com/p/claude-code-opus-remotion-agentic-promo-video （Remotion，先分镜后代码）
  - Higgsfield AI
  - Stefan 3D AI：Blender，约 13.3 美元
  - Linux.do《Let Me Go》MV：https://linux.do/t/topic/2943096 （effort xhigh，约 200 美元）
  - B 站 UP 主作品：https://www.bilibili.com/video/BV1Vfau6iE9Q/ 等
- **实践**（「写法经验」原文要点）
  - "先分镜，后代码"
  - "像导演一样给结构"：写清时长 / 场景数，给参考视频或参考图，用 match cut、kinetic typography 这类镜头语言
  - "列禁用清单"：粒子爆炸、RGB 分离、镜头光晕、霓虹辉光、弹跳缓动
  - "确定性渲染"：每帧只由 t 决定（seek(t)），不用 CSS transition 和计时器
  - "让它自己看片、自己返工"
  - 推理强度："effort 调到 high / xhigh"
  - 安全：`.claude/settings.json` 里加 `"deny": ["Read(./.env)"]`
  - 成本
    - 一句话短片几美元
    - 几分钟的 MV 可能到 200 美元，或占 Max 周额度的 7%–10%
    - "一次成型"多数其实跑了两轮以上
- **Demo**：无（README 没有图）

## mexicat/pdoom-video（★3,766）

- **是什么**
  - 作品源码：代码渲染的 MV，带词同步卡拉 OK 字效
  - 栈
    - 渲染：TypeScript + three.js（bun + Vite）→ headless Chrome → ffmpeg
    - 分析：Demucs 分轨 + CTC 强制对齐 + Whisper 交叉校验 + 节拍分析
- **场景**：MV / 歌词视频
- **Used-by**
  - 作者用 Claude Code（Opus 5.5）完成："concept and treatment, ... the renderer, every scene and the renders were all worked out in conversation with Claude"
  - 成片：https://www.youtube.com/watch?v=5EoO5413dBY
- **实践**
  - "Every frame is a deterministic function of song time"：预览和离线导出一模一样
  - 场景窗口锚定歌词行，并吸附节拍网格
  - 每个 plate 一个模块
  - 自适应运动模糊：按 32×32 tile 取 12 / 36 / 108 / 324 个子帧
  - 用 stills / sheet 模式出联系表检查
- **Demo**：mexicat__pdoom-video.jpg（YouTube 缩略图）

## JohnHeibel/PDoomVideo（★2,818）

- **是什么**
  - 作品源码：Opus 5.5 的 P(doom) MV（https://youtu.be/8j-hR4fJywU ）
  - 栈：p5.js + p5.brush 笔刷 → headless Chrome → ffmpeg
  - 作者另做了通用底板 ClaudeAnimationBase
- **场景**：MV / 手绘叙事动画
- **Used-by**
  - 作者用 Claude Code 生成："Everything in this repository was generated by the model. No scene ideas were specified."
  - 旁证
    - opusvideo 把原帖记在 @other__reality 名下：https://x.com/other__reality/status/2102514581684052169
    - joeseesun 记的成本："10% Max 5x 周额度"（未核实）
- **实践**
  - 人只给两条方向："use the Clawd character design"、"give each lyric interesting visuals and transitions"
  - Opus 自己写 ANIMATION_GUIDE.md，给并行的 subagent 做 brief
  - 第一代之后让 Opus 写 STORYBOARD.md，要求 "make every scene transition into the next"
  - 一章一个文件；渲帧可断点续跑
- **Demo**：JohnHeibel__PDoomVideo.gif（recursion_loop，8.2 MB）

## 0xsline/OpenChatCut（★2,886）

- **是什么**
  - 开源、本地优先的对话式 AI 视频编辑器（ChatCut 开源替代，AGPL）
  - 核心：多轨时间线 + 内置 agent + Streamable HTTP MCP（Codex / Claude Code 可以直接改真实工程）
  - 栈：React 19、Remotion 4、Electron
  - Skill：一个 router skill，按需加载 26 个专项 skill
- **场景**：口播 / 访谈的转写驱动剪辑、多素材粗剪、短视频包装、MG 模板、开发者自动化
- **Used-by**：未提及（OfoxAI 是赞助商）
- **实践**（MCP 编辑会话）
  1. `begin_edit_session`
  2. 所有读写带上 editSessionId，只改隔离草稿
  3. `review_edit_session`；manual 模式在编辑器里审批
  - 一次会话的改动 "commits ... atomically as one undo step"
  - 生成 / 导出 / 删除这类不可回滚的工具不在会话里开放（"a rejected proposal could not roll them back"）
- **Demo**：0xsline__OpenChatCut.png（编辑器总览截图）

