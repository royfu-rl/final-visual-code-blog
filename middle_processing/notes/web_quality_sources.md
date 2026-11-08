# 高质量 · 高难度网页作品：开放来源调研

- 日期：2026-10-28；所有数字均为当日实测，口径写在格内
- 目的
  - 补 `parts/web/data.md` §2.1 表中「设计站（未查）」一行
  - 往「高审美 / 高难度」方向扩，CodePen、Shadertoy、js13k、HF Spaces、Frontend Mentor、WebSight 等已有条目不重复
- 方法
  - curl（本机代理；被封的站再试备用代理 `10.74.128.15:11080`）、WebFetch、GitHub API（未登录）、HF API、arXiv API
  - 查不到的数一律写「口径待补」
- 勘误：旧笔记（`sources_and_uses.md` §1.5）写「Figma 免费文件 CC BY 4.0」，与现行条款不符，见 §3

## 0 结论速览

1. 同时满足「源码 + 渲染结果 + 明确许可 + 质量信号」且有万级规模的来源只有一个：Webflow 可克隆站
   - 但多数条目 likes 只有 0–1，要按社区信号过滤后才算高审美
   - Webflow 官方词汇表说可克隆站是 CC0；webflow.com 的 robots 写 `ai-train=yes`
2. 获奖画廊（Awwwards / One Page Love / SiteInspire / Httpster）只给截图、评分、标签和外链
   - 用作质量标签、发现入口和评测锚点，不能当可分发的训练源码
3. 难度最高、许可最干净的「小而精」来源：Codrops 2020 年后的 MIT 仓库（129 个，README 多数链到对应的教程文章）
4. 能成规模拿到多文件、多页面整站的，只有主题目录（Astro / Hugo / Jamstack Themes），许可可以机器筛
5. 意外发现
   - One Page Love 的 API 页直接写「Powers apps, training datasets」；Webflow 主动放行 AI 训练
   - 2026 年「给 agent 的审美」类仓库爆火：taste-skill 103,561★（2026-02 创建），awesome-design-md 123,985★（2026-03 创建）。它们是规则和设计 token，不是作品
   - Design Creativity Bench（2610.11539）测得：人类设计的创意跨度 0.902，模型只有 0.581。这说明人类高审美作品仍然稀缺、值得挖
   - 已有数据集 ronantakizawa/webui 把 Awwwards / LapaNinja / SiteInspire 的页面收进来，整体标 MIT；这类页面的代码归原站所有，并没有 MIT 授权

## 1 来源排名总表

排序依据：源码可得 > 许可清楚 > 质量信号 > 难度 > 规模。✓ 可训练可分发，△ 需逐件核或只可内部用，✗ 不可用。

| # | 名称 + 链接 | 拿到什么 | 规模（日期 · 口径） | 许可 | 质量信号 | 难度信号 | 获取方式 | 示例条目 |
|---|---|---|---|---|---|---|---|---|
| 1 | [Webflow Made in Webflow](https://webflow.com/made-in-webflow)（可克隆站） | live 页的 HTML + CSS + webflow.js（含 GSAP）；可渲染；views / likes / 克隆数 | 95,246 条（2026-10-28，sitemap 计数）；抽 60 条，24 条可克隆（40%），粗估 2.6–5.0 万（95% 区间） | ✓ 可克隆站 CC0（[词汇表](https://webflow.com/glossary/cloneable-site)原文）；robots `ai-train=yes`；字体、图片另有版权 | numLikes、timesCloned、numViews；抽样里 likes ≥ 10 的仅 7/60 | GSAP / Flip / SplitText、滚动交互、CMS、多页；分类有 3D、Parallax | 2 个 sitemap → 条目页 `__NEXT_DATA__`（`cloneable` 字段）→ 直抓 `<slug>.webflow.io` | [gsap-flip-layout](https://webflow.com/made-in-webflow/website/gsap-flip-layout)（克隆 308）· [live](https://gsap-flip-layout.webflow.io/) |
| 2 | [Codrops](https://github.com/codrops)（GitHub 组织） | src（手写 HTML/CSS/JS）+ dist（构建产物）+ 在线 demo + 教程文章 | 349 仓（users API）；其中 MIT 129 个，2020 年后基本全是 MIT | ✓ 2020 年后 MIT；✗ 2012–2019 无 LICENSE，README 写「Don't republish, redistribute or sell 'as-is'」 | 编辑精选，配教程文章；星数最高 2,316 | WebGL、着色器、GSAP、滚动排版、页面转场；一仓多个 demo 入口 | GitHub API + clone；tympanus.net 的 demo 与文章：本机和 WebFetch 都 403 | [OnScrollTypographyAnimations](https://github.com/codrops/OnScrollTypographyAnimations)（350★ MIT） |
| 3 | 主题目录：[Astro](https://astro.build/themes/) · [Hugo](https://themes.gohugo.io/) · [Jamstack Themes](https://jamstackthemes.dev/) | 完整多文件工程 + demo 站 + 缩略图 | Astro 1,348 个（付费 781 / 免费 567）；Hugo 638 个；Jamstack 1,200 个 | Hugo ✓（收录门槛是 OSI 许可；抽 54 仓：MIT 41 / GPL 系 5 / NOASSERTION 7 / 无 1）；Astro △（2026-09 新增的免费主题 37 个，查到 35 仓：MIT 23 / Apache 1 / NOASSERTION 9 / 无 2）；Jamstack △（抽 60 条，查到 49 仓：MIT 36 / 其他宽松 3 / GPL 2 / NOASSERTION 4 / 无 4；11 条 search 未命中（失效、改名或 fork），6 仓已归档） | GitHub 星：Hugo 抽样中 ≥ 100★ 18/54；`topic:hugo-theme` ≥ 100★ 193 仓；`topic:jekyll-theme` ≥ 100★ 179 仓 | 多页、响应式、暗色模式、内容集合；需构建 | Astro portal API（monthly 接口带 repoUrl / demoUrl）；Hugo `themes.txt`；Jamstack 的 md front matter 里有 github + demo | [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod) · [11ty-Serene](https://jamstackthemes.dev/theme/11ty-serene/) |
| 4 | shadcn registry 生态：[shadcn/ui](https://ui.shadcn.com/blocks) · [registry 目录](https://ui.shadcn.com/r/registries.json) · [Magic UI](https://magicui.design/docs/components) | 组件与区块源码（.tsx，内嵌在 JSON 里）+ 依赖声明；要套固定外壳才能渲染 | shadcn/ui new-york-v4 共 471 项（block 97）；第三方 registry 508 家（healthy 408），itemCount 合计 124,231；Magic UI 250 项 | shadcn/ui ✓ MIT；Magic UI ✓ MIT；第三方逐家核（大头是图标库） | 官方 health score 与 ranking；星数：shadcn 126,693、Magic UI 22,909 | 设计系统一致性（token、亮暗主题）、Motion 动画、可访问性 | `registries.json` → `<registry>/r/{name}.json`，schema 统一 | [login-03.json](https://ui.shadcn.com/r/styles/new-york-v4/login-03.json) · [marquee.json](https://magicui.design/r/marquee.json) |
| 5 | 单文件元素：[Uiverse galaxy](https://github.com/uiverse-io/galaxy) · [HyperUI](https://github.com/markmead/hyperui) | Uiverse：单文件 HTML + `<style>`，注释里带作者与标签；HyperUI：Tailwind HTML，含暗色变体 | Uiverse 3,802 个（Buttons 1,231 / Cards 726 / loaders 718 …）；HyperUI 560 个（application 295 / marketing 177 / neobrutalism 74） | ✓ 两仓都是 MIT；hyperui.dev 站点 robots 写 `ai-train=no`，只管爬站，不管仓库 | 社区精选；14,047★ / 12,274★ | 低到中：微交互、CSS 动画，无多页 | git clone；uiverse.io 站点 403；Uiverse 仓库最后推送 2024-09-02，站上的新作没有同步 | [Uiverse 按钮](https://raw.githubusercontent.com/uiverse-io/galaxy/main/Buttons/ChanduOffl_itchy-vampirebat-74.html) · [HyperUI announcements](https://github.com/markmead/hyperui/tree/main/public/examples/marketing/announcements) |
| 6 | [One Page Love](https://onepagelove.com/) | 全长截图 + 评语 + 标签 + live 外链；代码就是第三方的 live 站 | 9,402 站；模板 322 个（免费 118）；站方自称存档 20,000+ | △ 截图和评语归 OPL，站点代码归原作者；API 条款口径待补 | 人工策展，只收「Real live websites」 | Tech 标签：Tailwind 383、GSAP 142、Three.js 51；Style 标签：Scroll Effects 1,346、3D 238 | API（Private Beta，需申请）；sitemap；robots 不封 GPTBot / ClaudeBot | [hedroom](https://onepagelove.com/hedroom) |
| 7 | [Awwwards](https://www.awwwards.com/websites/sites_of_the_day/)（SOTD + Dev Award） | 评分（Dev Award 含 6 项分）+ 技术标签 + live 外链；无源码 | SOTD 约 6.1k（分页估算：204 页 × 每页约 30 条，2009-06-01 → 2026-10-27） | ✗ 站内素材「unauthorized use or reproduction is strictly prohibited」；作品版权归作者 | 评审分，如 a24：SOTD 7.65、Dev 7.41 | Technology 过滤含 WebGL / Three.js / GSAP；Dev 分项有 Animations、Responsive、Accessibility | 列表分页可抓（robots 封 `/websites/?`，不封 `/websites/sites_of_the_day/?page=`）；sitemap 404 | [a24](https://www.awwwards.com/sites/a24) |
| 8 | 开源的获奖个人站（GitHub） | 完整工程，多为 Three.js / GSAP | 几十个：README 含「site of the day」且 ≥ 20★ 的 18 仓；含「FWA of the day」的 28 仓；`topic:awwwards` ≥ 10★ 的 51 仓，多为课程或仿站 | 混杂：brunosimon/folio-2019 MIT（4,750★）、folio-2025 MIT；andrewwoan 系列 MIT；bizarro/bruno-arizio 无许可 | 获奖记录（README 自述） | 最高：WebGL 场景、物理、自定义着色器、转场 | GitHub 检索 + 逐仓核许可 | [folio-2019](https://github.com/brunosimon/folio-2019) · [mr-pandas](https://github.com/andrewwoan/mr-pandas-psychologically-safe-portfolio) |
| 9 | [HTML5 UP](https://html5up.net/) · [Start Bootstrap](https://startbootstrap.com/themes) | zip 包（HTML/CSS/JS）+ demo | HTML5 UP 44 个；Start Bootstrap 50 仓（43 个 MIT） | HTML5 UP 用 CC BY 3.0（须署名）；Start Bootstrap 用 MIT | 成熟模板，风格偏老 | 低到中：响应式单页 | 直接下载 | [forty](https://html5up.net/forty)（`/download` 返回 2.2 MB zip） |
| 10 | [Vercel Templates](https://vercel.com/templates) | 模板页 + GitHub 仓库 + 部署 demo | 528 个模板页（Next.js 344；sitemap 计数） | 逐仓核；vercel/examples 是 MIT | 官方收录 | 中：Next.js 全栈，偏功能 starter | sitemap → 模板页 → GitHub | [nextjs-portfolio](https://vercel.com/templates/next.js/nextjs-portfolio) |
| 11 | [FreeFrontend](https://freefrontend.com/) | 聚合 CodePen / Uiverse 作者的示例：预览、代码、zip | 首页 feed 显示 52 条；总量口径待补 | △ 页面无许可声明；许可跟原件走（CodePen 公开 pen 默认 MIT） | 编辑挑选 | 低到中：CSS / GSAP 特效 | robots 允许（只封带 query 的 URL 和 404 页）；有 sitemap | 首页 |
| 12 | DESIGN.md 集：[awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | 品牌设计系统的 YAML token（颜色、字体、间距），不是页面 | 仓库 85 个 DESIGN.md；getdesign.md 页面自称 550+ | ✓ MIT（123,985★）；规范见 google-labs-code/design.md（Apache-2.0） | 星数 | 无，用作 Query 的「风格条件」 | git clone | [stripe/DESIGN.md](https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/stripe/DESIGN.md) |
| 13 | 纯画廊：[Httpster](https://httpster.net/) · [SiteInspire](https://www.siteinspire.com/) | 截图 + 外链 + 作者 | Httpster 3,116 站；SiteInspire 无总数（如 Agencies 2,407 / Typographic 2,105） | △ 只能当发现入口 | 人工策展 | 口径待补 | 爬页面；SiteInspire 的 curl 返回 429，WebFetch 可读 | [makingsoftware](https://httpster.net/website/makingsoftware/) |

**GitHub topic 作为发现入口**（`github.com/topics/<t>` 页面计数，2026-10-28；星级过滤用 search API 的 total_count）

| topic | 仓库数 | 星级过滤后 |
|---|--:|--:|
| portfolio | 94,894 | ≥ 100★：474 |
| portfolio-website | 30,283 | ≥ 100★：223 |
| landing-page | 21,152 | ≥ 100★：138 |
| threejs | 26,882 | ≥ 100★：655 |
| webgl | 16,486 | ≥ 100★：798 |
| gsap | 9,619 | ≥ 100★：95 |
| creative-coding | 6,587 | ≥ 100★：179 |
| lenis / locomotive-scroll | 809 / 441 | ≥ 20★：22 / 21 |
| awwwards | 233 | ≥ 10★：51 |
| shadcn-ui / framer-motion | 21,570 / 17,594 | — |

- 名义数与可用数差两个数量级：portfolio 9.5 万 → ≥ 100★ 只剩 474

### 1.1 2025–2026 与高审美相关的数据集

结论：目前没有「获奖级人类作品 + 有许可的源码」且成规模的公开集；最接近的 webui 里画廊站页面只有几百条。

| 名称 | 内容 | 规模 | 许可 | 对我们的用处 |
|---|---|---|---|---|
| [ronantakizawa/webui](https://huggingface.co/datasets/ronantakizawa/webui)（博客已收） | 40 个来源的截图 + HTML/CSS/JS + 包围盒 | train 行数：github 13,041 / codepen 9,384 / lapaninja 372 / siteinspire 84（每样本 3 视口）；awwwards 在 validation，onepagelove 在 test，行数口径待补 | 标 MIT，但卡片写「aggregates code under various open-source licenses」 | 说明画廊站页面在现有数据里占比很小 |
| [Auroraventures/cipher-awwwards-sft25](https://huggingface.co/datasets/Auroraventures/cipher-awwwards-sft25) | 96 条 Awwwards SOTD 结构化记录 + 741 条真实代码（three.js examples 578 / motion 148 / GSAP 示例 63） | 1K–10K | ✗ CC BY-NC 4.0 | 只能参考做法 |
| [datapointai/vibe-landing-page-arena](https://huggingface.co/datasets/datapointai/vibe-landing-page-arena) | AI 生成落地页的两两人工偏好 | 36,000 次判断 / 3,492 名标注者 / 100 个提示 | ✓ CC BY 4.0（自动门控） | 审美 reward 的校准数据 |
| [datapointai/vibe-design-arena](https://huggingface.co/datasets/datapointai/vibe-design-arena) | 60 个 vibe-coded 应用全配对 | 1,770 对 × 每对 30 票 | ✓ CC BY 4.0（门控） | 同上 |
| [Kombai/design-creativity-bench](https://huggingface.co/datasets/Kombai/design-creativity-bench)（[2610.11539](https://arxiv.org/abs/2610.11539)） | 15 个模型 × 20 个提示的自包含 HTML | 300 页 | ✓ MIT | 量化「模型设计趋同」；人类创意跨度 0.902，模型 0.581 |
| [obaydata/design-repo](https://huggingface.co/datasets/obaydata/design-repo-web-design-benchmark) | 数据商样例：提示 + 设计图 + 仓库 + 录屏 | 自称每周产能 300 条 | ✗ CC BY-NC 4.0 | 可外采的形态参考 |
| [LandingAgent / LandingBench](https://arxiv.org/abs/2608.27902) | 真实落地页的结构画像 | — | 原始数据未随仓库发布（README 原文） | 只能参考方法 |
| [TaoD2C-Bench](https://arxiv.org/abs/2610.10374) | 17 个商业平台的生产设计稿 + 97,652 条专家标注 | 2,861 稿 | 发布情况口径待补 | 工业 D2C，审美不是重点 |

## 2 Top 5 推荐与挖矿管线

### 2.1 推荐

1. **Webflow 可克隆站**：唯一同时有 CC0、渲染即得、社区信号和万级规模的来源
2. **Codrops MIT 仓库**：难度最高，教程文章可以直接改写成 Query
3. **主题目录（Astro / Hugo / Jamstack）**：唯一成规模的多文件、多页面整站，许可能机器筛
4. **shadcn registry 生态**：schema 统一、源码内嵌在 JSON 里，设计系统级一致
5. **Uiverse + HyperUI**：MIT、单文件、免构建，可以直接进 harness

另外，One Page Love 与 Awwwards 只作「标签 + 评测锚点」，不进训练源码。

### 2.2 通用管线

发现 → 抓取 → 渲染 → 过滤 → 切任务（Query / Verifier / Harness）

- 渲染统一走现有 harness：无头浏览器、冻结时钟、三视口、滚动录屏
- 过滤沿用 data.md §2.6 的九道闸，下面只写各来源特有的步骤

### 2.3 各来源特有步骤

1. Webflow 可克隆站
   - 发现：两个 showcase sitemap → 95,246 个条目 URL
   - 抓取：条目页 `__NEXT_DATA__` 取 `cloneable / numLikes / timesCloned / cloneOf`
     - 只留 `cloneable=True` 且 `cloneOf=False` 的条目，去掉克隆副本
   - 渲染：抓 `<slug>.webflow.io` 全站（HTML + 共享 CSS + webflow.js + GSAP），资产本地化，滚动录屏
   - 过滤：按 likes / 克隆数设阈值（抽样中 likes ≥ 10 约 12%）；剔除教程 demo 页和空页；字体、图片换占位
   - 注意：交互编译在 webflow.js 运行时里，HTML 也是生成器产物（类名 `w-*`），不是手写代码
2. Codrops MIT 仓库
   - 发现：GitHub API 列出 349 仓 → 留下 MIT 的 129 个
   - 抓取：clone；`dist/` 直接渲染，`src/` 当参考答案
   - 渲染：多入口（`index*.html`）分别截图、录屏
   - 过滤：剔除纯库和无 demo 的仓
   - 注意：文章正文在 tympanus.net，需要换网络出口才能抓（本机 403）
3. 主题目录
   - 发现：Astro portal API（monthly 接口带 repoUrl / demoUrl）+ Hugo `themes.txt` + Jamstack md 的 front matter
   - 抓取：GitHub API 取 `license.spdx_id` 与星数，只留 OSI 许可
   - 渲染：优先渲 demo 站（免构建）；站内链接爬两层，得到多页任务
   - 过滤：设星数阈值；剔除付费主题（Astro 付费 781 个）；同作者的多个变体去重
4. shadcn registry
   - 发现：`registries.json` 共 508 家 → 只留 healthy 且许可为 MIT / Apache 的
   - 抓取：`/r/{name}.json`，代码在 `files[].content` 里
   - 渲染：固定的 Next.js + Tailwind v4 外壳，亮暗两套主题各截一次
   - 过滤：剔除图标库（itemCount 大头是图标，如 keyline 12,984）；去近重复
5. Uiverse + HyperUI
   - 发现：clone 两个仓库
   - 渲染：单文件直接渲，额外截悬停、点击状态
   - 过滤：去近重复（同模板改色）；按标签分层采样
6. 补充：OPL 与 Awwwards 的用法
   - live URL 只渲进评测集，不分发
   - 用标签（GSAP / Three.js / Scroll Effects）给难度分层
   - 用 Dev Award 分项分校准审美 reward

## 3 看着诱人但用不了

| 来源 | 卡点 | 证据 |
|---|---|---|
| [Dribbble](https://dribbble.com/terms) | 条款禁止复制和未授权使用；本机返回 202 挑战页 | §7「Copying, distributing, or disclosing any part of the Website」；§11「Use of the Dribbble Content for any purpose not expressly permitted ... is strictly prohibited」 |
| [Behance](https://www.behance.net/) | 返回 403；robots 对 CCbot / ClaudeBot / GPTBot 写 `Disallow: /` | robots |
| [Mobbin](https://mobbin.com/terms) | 有 621,500 张界面截图，但条款明文禁止用于 AI | 「will not use ... to train, test, index, benchmark, or improve any generative AI ... model」 |
| [Figma Community](https://www.figma.com/legal/community-free-resource-license/) | 免费资源用自定义许可：只能在 Figma 平台内使用，禁止衍生作品；robots 封 GPTBot / ClaudeBot / CCBot | 「solely in connection with your authorized use of the Figma Platform」「modify, translate, or create derivative works」 |
| [Framer Marketplace](https://www.framer.com/marketplace/) | 无源码导出；免费模板也逐个禁止再分发（标签 Limited / Single-Use） | sitemap 计数：模板 13,661、组件 10,790 |
| Godly → [recent.design](https://recent.design/?ref=godly) | godly.website 301 跳到 recent.design；robots 写 `ai-train=no`，并封 AI bot | robots |
| [21st.dev](https://21st.dev/) | robots 写 `ai-train=no` | 注释原文「bulk training on the catalog is not: ask first」 |
| Awwwards（当源码用） | 只有外链；站内素材禁止复制 | terms 原文 |
| Land-book · Lapa Ninja | curl 和 WebFetch 都返回 403 | — |
| CSS Design Awards | curl 超时，WebFetch 报「Socket is closed」 | — |
| The FWA | 单页应用，HTML 里没有条目；sitemap 返回 500 | — |
| [Landingfolio](https://www.landingfolio.com/) | 961 站、4,652 个分区截图，但代码在会员 Library 里 | 许可文本未取到 |
| Tailwind Plus | 付费；许可页 302 跳到登录页 | — |
| Codrops 2012–2019 | 禁止原样再分发 | README 原文 |
| React Bits · Aceternity · Preline | 可用于做项目，但禁止再分发组件或做竞品，分发数据集有风险 | Commons Clause / 自定义许可 / Fair Use |
| Glitch | glitch.com 已 307 跳转到博客 | 2025-05-22「Important changes are coming to Glitch」，2025-07-23「Until we meet again」 |
| CodePen Picked | 返回 403，无法枚举（公开 pen 默认 MIT 已核实） | — |

## 4 已核验 URL

- 日期均为 2026-10-28；「状态」是 HTTP 码（`curl -L` 的最终码）或 WebFetch 结果
- 「本机代理 + 备用代理同结果」表示两条出口都试过

| 状态 | URL | 备注 |
|---|---|---|
| 200 | https://www.awwwards.com/ | |
| 000 / WebFetch 失败(Socket is closed) | https://www.cssdesignawards.com/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 200 / WebFetch 仅标题(SPA) | https://thefwa.com/ | |
| 301 → 200 | https://godly.website/ | 跳转 recent.design/?ref=godly |
| 429 / WebFetch OK | https://www.siteinspire.com/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 403 / WebFetch 403 | https://land-book.com/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 403 / WebFetch 403 | https://www.lapa.ninja/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 200 | https://onepagelove.com/ | |
| 200 / WebFetch OK | https://httpster.net/ | |
| 200 | https://webflow.com/made-in-webflow | |
| 200 / WebFetch OK | https://www.framer.com/marketplace/ | 跳转→https://www.framer.com/marketplace/templates/ |
| 200 | https://readymag.com/ | |
| 200 | https://html5up.net/ | (44 个 /download 链接) |
| 200 | https://cruip.com/ | |
| 200 | https://astro.build/themes/ | |
| 200 | https://themes.gohugo.io/ | |
| 200 | https://jamstackthemes.dev/ | |
| 200 | https://vercel.com/templates | |
| 200 | https://ui.shadcn.com/ | |
| 200 | https://magicui.design/ | |
| 200 | https://ui.aceternity.com/ | |
| 403 / WebFetch 403 | https://uiverse.io/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 200 | https://www.hyperui.dev/ | |
| 200 | https://preline.co/ | |
| 200 | https://flowbite.com/ | |
| 200 | https://daisyui.com/ | |
| 200 | https://tailblocks.cc/ | |
| 403 | https://tympanus.net/codrops/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 200 | https://21st.dev/ | |
| 403 | https://codepen.io/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 202 | https://dribbble.com/ | 本机代理 + 备用代理 10.74.128.15 同结果 |
| 200 | https://www.figma.com/community | |
| 200 | https://www.awwwards.com/robots.txt | |
| 200 | https://thefwa.com/robots.txt | |
| 200 | https://recent.design/robots.txt | |
| 200 | https://onepagelove.com/robots.txt | |
| 404 | https://httpster.net/robots.txt | |
| 200 | https://webflow.com/robots.txt | (Content-Signal: ai-train=yes) |
| 200 | https://www.framer.com/robots.txt | |
| 200 | https://readymag.com/robots.txt | |
| 200 | https://html5up.net/robots.txt | |
| 200 | https://astro.build/robots.txt | |
| 404 | https://themes.gohugo.io/robots.txt | |
| 200 | https://ui.shadcn.com/robots.txt | |
| 200 | https://21st.dev/robots.txt | |
| 200 | https://www.figma.com/robots.txt | |
| 200 | https://ui.aceternity.com/robots.txt | |
| 200 | https://magicui.design/robots.txt | |
| 200 | https://www.hyperui.dev/robots.txt | |
| 200 / WebFetch OK | https://www.awwwards.com/websites/sites_of_the_day/ | |
| 200 | https://www.awwwards.com/websites/honorable/ | |
| 200 | https://www.awwwards.com/websites/developer/ | |
| 200 | https://www.awwwards.com/websites/ | |
| 404 | https://www.awwwards.com/sitemap.xml | |
| 200/404 | https://www.awwwards.com/websites/sites_of_the_day/?page=N | (N=1..204 有内容, 205+ 404) |
| 200 | https://www.awwwards.com/terms/ | |
| 200 | https://onepagelove.com/llms.txt | |
| 200 | https://onepagelove.com/api | |
| 200 | https://d3e54v103j8qbb.cloudfront.net/growth-seo/live/showcase_projects_sitemap0.xml | |
| 200 | https://d3e54v103j8qbb.cloudfront.net/growth-seo/live/showcase_projects_sitemap1.xml | |
| 200 | https://webflow.com/made-in-webflow/website/gsap-flip-layout | |
| 200 | https://webflow.com/glossary/cloneable-site | |
| 200 | https://webflow.com/templates/template-licenses | |
| 200 | https://www.framer.com/marketplace/sitemap.xml | |
| 200 | https://www.framer.com/marketplace/sitemap/resources-templates.xml | |
| 200 | https://www.framer.com/marketplace/sitemap/resources-components.xml | |
| 200 | https://raw.githubusercontent.com/gohugoio/hugoThemesSiteBuilder/main/themes.txt | |
| 200 | https://raw.githubusercontent.com/withastro/astro.build/main/src/content/themes/themes.json | |
| 200 | https://portal.astro.build/api/themes/monthly?month=2026-09-01T00:00:00.000Z | |
| 200 | https://html5up.net/license | |
| 200 | https://ui.shadcn.com/r/index.json | |
| 200 | https://ui.shadcn.com/r/registries.json | |
| 200 | https://ui.shadcn.com/r/styles/new-york-v4/registry.json | |
| 404 | https://ui.shadcn.com/registry.json | |
| 200 | https://magicui.design/r/registry.json | |
| 200 | https://ui.aceternity.com/registry.json | |
| 200 | https://ui.aceternity.com/api/components | |
| 200 | https://ui.aceternity.com/llms.txt | |
| 200 | https://ui.aceternity.com/llms-full.txt | |
| 200 | https://github.com/uiverse-io/galaxy | (tree 3,813 blobs) |
| 200 | https://github.com/topics/portfolio | (94,894 repos) |
| 200 | https://github.com/topics/portfolio-website | (30,283 repos) |
| 200 | https://github.com/topics/landing-page | (21,152 repos) |
| 200 | https://github.com/topics/awwwards | (233 repos) |
| 200 | https://github.com/topics/creative-coding | (6,587 repos) |
| 200 | https://github.com/topics/webgl | (16,486 repos) |
| 200 | https://github.com/topics/threejs | (26,882 repos) |
| 200 | https://github.com/topics/gsap | (9,619 repos) |
| 200 | https://github.com/topics/locomotive-scroll | (441 repos) |
| 200 | https://github.com/topics/tailwindcss-template | (42 repos) |
| 200 | https://github.com/topics/astro-theme | (274 repos) |
| 200 | https://github.com/topics/hugo-theme | (1,908 repos) |
| 200 | https://github.com/topics/jekyll-theme | (1,979 repos) |
| 200 | https://github.com/topics/nextjs-template | (1,014 repos) |
| 200 | https://github.com/topics/html-template | (1,328 repos) |
| 200 | https://github.com/topics/css-animation | (656 repos) |
| 200 | https://github.com/topics/threejs-portfolio | (12 repos) |
| 200 | https://github.com/topics/lenis | (809 repos) |
| 200 | https://github.com/topics/barba-js | 页面无计数 |
| 200 | https://github.com/topics/shadcn-ui | (21,570 repos) |
| 200 | https://github.com/topics/webflow | (395 repos) |
| 200 | https://github.com/topics/framer-motion | (17,594 repos) |
| 200 / WebFetch OK | https://www.figma.com/legal/community-free-resource-license/ | |
| 200 | https://www.figma.com/legal/community-terms/ | |
| 200 | https://huggingface.co/datasets/Auroraventures/cipher-awwwards-sft25 | |
| 401 / 200 | https://huggingface.co/datasets/datapointai/vibe-landing-page-arena | README 门控 401，页面 200 |
| 401 | https://huggingface.co/datasets/datapointai/vibe-design-arena | README 门控（auto） |
| 200 | https://huggingface.co/datasets/obaydata/design-repo-web-design-benchmark | |
| 200 | https://huggingface.co/datasets/TheBaldDudeCo/website-gallery | |
| 200 | https://huggingface.co/datasets/JoshPurtell/web-design-screenshots | |
| 200 | https://huggingface.co/datasets/Kukedlc/web-design-diamond | |
| 404 | https://huggingface.co/datasets/smirki/Codepen-Sites-v1 | |
| 200 | https://huggingface.co/datasets/KalnRangelov/landing-page-training-data | |
| 401 | https://huggingface.co/datasets/Karmane/framer-saas-templates-pricing-and-traction | README 门控（manual）；描述取自 API |
| 200 | https://arxiv.org/abs/2608.27902 | |
| 200 | https://arxiv.org/abs/2603.13036 | |
| 200 | https://arxiv.org/abs/2610.10374 | |
| 200 | https://huggingface.co/datasets/ronantakizawa/webui | |
| 200 | https://huggingface.co/datasets/Kombai/design-creativity-bench | |
| 200 | https://huggingface.co/datasets/MiniMaxAI/VIBE | |
| 200 | https://gsap-flip-layout.webflow.io/ | |
| 200 | https://vercel.com/sitemap.xml | |
| 200 | https://github.com/stackbit/jamstackthemes | (content/theme 1,200 个 md) |
| 200 / WebFetch OK | https://freefrontend.com/ | |
| 404 | https://freefrontend.com/gsap-examples/ | |
| 200 | https://aura.build/ | 跳转→https://www.aura.build/ |
| 200 | https://mobbin.com/ | |
| 403 | https://www.behance.net/ | |
| 200 / WebFetch OK | https://www.landingfolio.com/ | |
| 200 | https://startbootstrap.com/themes | |
| 200 / WebFetch OK | https://getdesign.md/ | |
| 200 / WebFetch OK | https://www.awwwards.com/sites/a24 | |
| 307 → 200 | https://glitch.com/ | 跳转 blog.glitch.com |
| 200 | https://datasets-server.huggingface.co/statistics?dataset=ronantakizawa/webui&config=default&split=* | |
| 200 / WebFetch 302->login | https://tailwindcss.com/plus/license | 跳转→https://tailwindcss.com/plus/login |
| 200 / WebFetch 403 / curl 200 | https://mobbin.com/terms | |
| 200 | https://onepagelove.com/hedroom | |
| 200 | https://onepagelove.com/tech/three-js | |
| 200 | https://portal.astro.build/api/themes?limit=5000 | |
| 200 | https://gsap.com/standard-license | |
| 200 | https://arxiv.org/abs/2610.11539 | |
| 200 | https://arxiv.org/abs/2604.15309 | |
| 200 | https://arxiv.org/abs/2510.23272 | |
| 200 | https://arxiv.org/abs/2604.20398 | |
| 200 | https://html5up.net/forty | |
| 200 | https://github.com/adityatelange/hugo-PaperMod | |
| 200 | https://themes.gohugo.io/themes/hugo-papermod/ | |
| 200 | https://github.com/shadcnstudio/shadcn-astro-zolt-landing-page-free | |
| 429 | https://github.com/uiverse-io/galaxy/blob/main/Buttons/ChanduOffl_itchy-vampirebat-74.html | |
| 200 | https://github.com/codrops/OnScrollTypographyAnimations | |
| 200 | https://httpster.net/website/makingsoftware/ | |
| 200 | https://jamstackthemes.dev/theme/11ty-serene/ | |
| 200 | https://github.com/CLCK0622/11ty-Serene | |
| 200 | https://vercel.com/templates/next.js/nextjs-portfolio | |
| 200 | https://github.com/brunosimon/folio-2019 | |
| 200 | https://github.com/andrewwoan/mr-pandas-psychologically-safe-portfolio | |
| 200 | https://github.com/markmead/hyperui/blob/main/public/examples/marketing/announcements | 跳转→https://github.com/markmead/hyperui/tree/main/public/examples/marketing/announcements |
| 200 | https://github.com/magicuidesign/magicui | |
| 200 | https://www.framer.com/marketplace/templates/launchdeck-3d/ | |
| 200 | https://github.com/VoltAgent/awesome-design-md | |
| 200 | https://github.com/DavidHDev/react-bits | |
| 200 | https://ui.aceternity.com/components | |
| 200 | https://magicui.design/docs/components | |
| 200 | https://ui.shadcn.com/blocks | |
| 200(raw) | https://raw.githubusercontent.com/uiverse-io/galaxy/main/Buttons/ChanduOffl_itchy-vampirebat-74.html | |
| WebFetch 403 | https://tympanus.net/codrops/licensing/ | |
| WebFetch 失败(Socket is closed) | https://www.cssdesignawards.com/wotd-award-winners | |
| WebFetch OK | https://recent.design/?ref=godly | |
| WebFetch OK | https://blog.codepen.io/documentation/licensing/ | |
| WebFetch 403 | https://codepen.io/picked/pens | |
| WebFetch OK | https://dribbble.com/terms | |
| WebFetch 仅标题 | https://www.aura.build/ | |
| 200 | https://html5up.net/forty/download | (zip) |
| 200 | https://ui.shadcn.com/r/styles/new-york-v4/login-03.json | 条目 JSON 内嵌源码 |
| 200 | https://magicui.design/r/marquee.json | 条目 JSON 内嵌源码 |
| 200 | https://reactbits.dev/r/registry.json | 1,274 项 |
| 200 | https://raw.githubusercontent.com/gohugoio/hugoThemesSiteBuilder/main/README.md | 收录要求 OSI 许可 |
| 200 | https://raw.githubusercontent.com/withastro/astro.build/main/scripts/update-themes.mjs | 指向 portal.astro.build API |
| 200 | https://raw.githubusercontent.com/stackbit/jamstackthemes/master/content/theme/11ty-Serene.md | front matter 含 github + demo |
| 200 | https://raw.githubusercontent.com/cruip/tailwind-landing-page-template/main/README.md | GPL + 请勿再分发 |
| 200 | https://raw.githubusercontent.com/DavidHDev/react-bits/main/LICENSE.md | MIT + Commons Clause |
| 200 | https://raw.githubusercontent.com/htmlstreamofficial/preline/main/LICENSE | MIT + Fair Use |
| 404 | https://raw.githubusercontent.com/aceternity/ui/main/LICENSE | 仓库不可见 |
| 200 | https://raw.githubusercontent.com/codrops/RainEffect/master/README.md | 旧仓"勿原样再分发" |
| 200 | https://raw.githubusercontent.com/codrops/OnScrollTypographyAnimations/main/README.md | src + dist 结构 |
| 200 | https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/stripe/DESIGN.md | YAML token |
| 200 | https://raw.githubusercontent.com/IAURAI/LandingAgent/main/README.md | 原始数据未发布 |
| 200 | https://api.github.com/users/codrops | public_repos 349 |
| 200 | https://api.github.com/repos/{withastro/astro.build, uiverse-io/galaxy, stackbit/jamstackthemes, markmead/hyperui, mertJF/tailblocks, VoltAgent/awesome-design-md, codrops/OnScrollTypographyAnimations}/git/trees/... | 文件计数 |
| 200 | https://api.github.com/search/repositories?q=... | 星数 / 许可 / topic 星级过滤 / "site of the day" 等检索；未登录配额 10 次/分 |
| 200 | https://huggingface.co/api/datasets?search=... | 关键词：awwwards / dribbble / webflow / framer / landing page / tailwind / shadcn / codepen / webgl / threejs / web design / figma / frontend 等 |
| 200 | https://export.arxiv.org/api/query?search_query=... | awwwards / dribbble / web design aesthetic / landing page / UI design code generation 等 |
| 200（部分） | https://codeload.github.com/stackbit/jamstackthemes/tar.gz/refs/heads/master | 58 MB 截断，已解出 1,199 个主题 md |

## 5 口径待补

- Land-book、Lapa Ninja、CSS Design Awards、The FWA 的规模与条款（被封或单页应用）
- uiverse.io 站点总数（403）；Codrops 许可页原文（403）
- Webflow 可克隆率只来自 60 个样本；Made in Webflow 的 JSON API 路径未摸清
- One Page Love 的 API 条款（Private Beta）
- Awwwards Honorable / Developer 的单独计数（筛选靠 JS，未计）
- Tailwind Plus 许可原文（需登录）
- ronantakizawa/webui 的 validation / test 按来源行数

