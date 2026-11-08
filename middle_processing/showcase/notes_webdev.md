# Webdev（2D）选卡记录

- 日期：2026-11-04
- 结果：4 个场景 14 张卡，其中小红书 8 张、海外开源 2 张、商用产品 4 张
- 自动取数缓存：`impact_webdev.json`，卡片上的赞、藏、star 和播放都没有手抄
- 封面：
  - 有 v1 本地图的直接用（`visual-coder-blog/market/posters/`）
  - 小红书签名图会过期，`uupm.cc/share.png` 下载慢，这 3 张已按 URL 哈希预存进 `posters/`
    - `da56996e88ab2f65.img`：陆78
    - `cc4a8b15acb72ff5.img`：李叔
    - `2583c5b148acb10b.img`：uupm

## 1 场景怎么选

| 场景 | 小红书热度 | 商业证据 | 结论 |
|---|---|---|---|
| 动效官网与作品集 | 全站最高赞 1.9 万；作品集是量最大的一类 | Vercel 年化收入 5 亿美元以上 | 选；作品集并进来 |
| HTML 汇报与 PPT | 收藏常高于点赞（1.06 万藏） | Genspark ARR 2.5 亿美元 | 选 |
| 应用与小程序 | 中（4 千赞） | Lovable ARR 6 亿美元以上，收入最大 | 选 |
| 网页小游戏 | 中（4 千赞） | Astrocade 月活 1000 万；TapTap 有 AI 小游戏日入千元 | 选 |
| 运营活动页与 H5 | 5 千赞 | 热帖多是即梦或 GPT 生图，不是写代码 | 不选 |
| 数据大屏与内部工具 | 1 千赞 | 有 B 端价值，但小红书没热度 | 不选 |
| 交互科普与课件 | 7.5 千赞 | 最热的人体拆解是 three.js 3D | 不选，归 3D 家族 |
| 3D 交互小世界 | — | — | 按要求排除 |

## 2 每张卡的出处

### 动效官网与作品集

- **截图复刻网页**（赛文乔伊）
  - 帖子：「只需丢给 AI 一张截图和一段视频，像素级复刻」，封面写 K2.5，发帖时间 2026-01-27
  - 链接：kimi.com，返回 200；GitHub `MoonshotAI/Kimi-K2.5`
- **个人作品集上线**（陆78）
  - 正文给了六步：Codex / Claude Code / Cursor → GitHub → Vercel → 绑域名
  - 正文没贴作品集网址，所以只挂了工具链接
- **UI UX Pro Max**
  - star 数来自 fetch_impact，14.5 万
  - npm 月下载 78,443：取自 `api.npmjs.org/downloads/point/last-month/ui-ux-pro-max-cli`，统计窗口 2026-10-04 到 11-02
  - README 徽章写「79 种 UI 风格」，官网封面写 57 种，所以 line 里没写数字
- **v0 by Vercel**
  - 年化收入 5 亿美元以上：Vercel 2026-08-06 新闻稿，说 7 月初越过
    - BusinessWire 拦脚本（403），原文从 financialcontent 转载核对
  - agent 触发的部署一年涨 28 倍：Vercel 官方博客《Ship 2026 recap》，2026-10-15
  - v0 用户 350 万以上：Series F 新闻稿，2025-09-30
    - 这一条只从搜索摘要看到，没打开原文
    - Sacra 估 2026-02 超过 400 万，属二手，没用
  - v0 单独的收入没有披露

### HTML 汇报与 PPT

- **Claude Design**（大师的AI小灶）
  - 产品：Anthropic 官方页 2026-04-17 发布，可导出 PPTX、PDF、Canva 和独立 HTML
  - 官方页没写「幻灯片就是 HTML」。「HTML 底」的说法来自帖子和二手报道（computingforgeeks）
  - Figma 发布当天跌约 7%：Motley Fool 2026-05-03
    - Reuters 盘中数字是 6.4%
- **组会文献汇报**（山山而川）
  - 四步话术都在正文里，第四步是「html 转 ppt 友好的 svg」
- **Frontend Slides**
  - star 数来自 fetch_impact，3.2 万
  - YouTube 教程是作者本人 Zara Zhang 发的，8.2 万播放
- **Genspark 幻灯片**
  - ARR 2.5 亿美元（12 个月从零做到）、估值 26 亿美元：BusinessWire 2026-06-17，原文从 01net 转载核对
  - 「全球首个基于 HTML 的 AI Slides」：CEO Eric Jing 在 X 上的说法，经二手转述，属公司自称
  - ARR 是全公司口径，没有单拆 Slides
  - Creative 模式用 Nano Banana 生图，不是代码，只有 Professional 模式是 HTML

### 应用与小程序

- **Lovable**
  - 来源：TechCrunch 2026-09-24，联合创始人 Fabian Hedin 在 HumanX 上说的
    - 年化收入超过 6 亿美元，6 月时约 5 亿
    - 估值 133 亿美元，2026-08 融资 4 亿美元
    - 平台上的应用每月访问近 10 亿次
  - 封面用 v1 的 `bp-webdev-00.jpg`，是第三方视频的缩略图，比较通用；lovable.dev 拦脚本，拿不到 og 图
- **拼豆接单工作台**（李叔聊AI）
  - 帖子：WorkBuddy「代码开发 → 网站开发」，自动建订单表和项目表
  - 月访问 885 万、同类第一：格隆汇 7-07 转述花旗研报，花旗又引易观 2026-03 的数据
  - 「月活 2000 万、日活 1300 万」只在二手转述里出现，腾讯财报只说按日活是国内第一，没给数字，所以没用
  - 9 月起能一句话生成并上线微信小程序：IT 之家 2026-09-24（同花顺转载）
- **心理测试小程序**（莫名其妙）
  - 正文：上线一周多累计一万多名用户，作者还在想怎么变现
  - 话题标签写的是 codex

### 网页小游戏

- **AI 的 4399**（南山君）
  - 合集站 toy.cedarstar.org 返回 200，标题 CEDAR TOY
  - 这些是给「小机」（用户的 AI 伴侣）通过 MCP 玩的开源小游戏，人用浏览器同一个网址看
- **TapTap 双榜小游戏**（明月桥investor）
  - 正文：「奖来」带来千元级的广告日收入，「荒野钓鱼」只有几十元
  - 新游 5002 款、约 80% 由 AI 做：InvenGlobal 2026-07-27，转述 CEO 黄一孟在 TDW 上的话
  - TapTap 制造半年做了近 5000 款、累计玩家 1100 万以上：新浪财经（星游际）
  - 这两条都是平台口径，帖子没说用的是不是 TapTap 制造
- **Astrocade**
  - 月活 1000 万（4 个月翻倍）、每月 2.2 亿局：GamesBeat 2026-10-07，CEO 采访
  - 融资 5600 万美元：Fortune 2026-05-05，A 轮 Sea 领投，B 轮红杉领投
  - 还没开始赚钱，CEO 说「明年开始重视收入」
  - 引擎和技术栈没有披露

## 3 链接核验

- 小红书、GitHub、YouTube 的 13 条链接都用 fetch_impact 拉到了数
- 站点链接 curl 返回 200 的：kimi.com、developers.openai.com/codex、vercel.com、v0.app、uupm.cc、anthropic.com 新闻页、codebuddy.cn/work、toy.cedarstar.org、taptap.cn、astrocade.com
- **lovable.dev、genspark.ai 首页对脚本返回 403**，是防爬，不是死链：同域 robots.txt 返回 200
- biz 来源：BusinessWire 三条对脚本返回 403，其余都是 200；BusinessWire 原文从转载站核对

## 4 考虑过、没选的

- 小艾不迟到「In full bloom」动效网页（1.6 万赞）：没说用什么工具，core 写不出来
- 是朝朝「网页滚动术语 6 个」（1.7 万赞）：是给 AI 写提示词的知识帖，不是作品；转载自 X，原帖没找到
- Kia 泳池作品集（1.1 万赞）、Big喷菇 3D 房间：three.js 3D，归 3D 家族
- 西陆1004「疼痛位置小程序」（8 千赞）：人体是 Blender 3D 模型，小程序也没链接
- 快跑啊小卢 HTML 汇报（7.4 千赞）：TapNow 软广
- Save Note 作品集 agent（7.2 千赞）：Mcode 产品软文，信息少
- 辣味章鱼 Codex 作品集（7 千赞）：和陆78 重复，陆78 流程更全
- 红发魔女Amber 3D 爱丽丝游戏、DAiKONAUT 蛋岛：3D
- 浙大猫学长「vibe 一款网络游戏」（3.8 千赞）：正文只有话题标签，没有产品链接；要是嫌「AI 的 4399」偏小众，可以换它
- 逸蒙「4 天 4.69 万美元」、熠辉「月入 1.2 万美元」：标题党，正文没细节
- Caroline「狗狗肖像月入 30 万美元」：转述 Lovable 访谈，赞 783，数字查不到原始出处
- Fly（levelsio）：three.js 3D，2026 年中收入已经归零
- Gamma：是自家卡片格式，不是 LLM 写代码
- Kimi PPT：走模板
- Manus：被收购后幻灯片路线不明，没再查
- Replit：ARR 只有 Sacra 估算（2026-04 约 5.25 亿），一手只有融资信息；和 Lovable 重复
- Bolt.new：没查到 2026 年的一手数字
- TapTap 制造单独成卡：会到 15 张，所以并进明月桥那张卡的 biz

## 5 缺口

- v0 用户数是 2025-09 的官方口径，没有更新的一手数字
- Genspark 和 Lovable 的数字都是公司自报，没有经过审计
- WorkBuddy 没有官方用户数
- 「AI 的 4399」商业性弱，见上面的替换建议

