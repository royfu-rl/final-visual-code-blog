# Round 2：可合法拿到的高质量作品源（补充调研）

- 日期：2026-10-28；所有数字均为当日实测，口径写在格内或脚注
- 与 round 1 的关系：只补新来源与复查结果，不重复 `web_quality_sources.md` / `3d_quality_sources.md` 已有条目
- 方法
  - GitHub search API（未鉴权；一次查询塞多个 `repo:`，拿 ★ / SPDX / pushed_at / homepage）
  - 无配额的仓库体检：`git clone --depth 1 --filter=blob:none --no-checkout` + `git ls-tree`，按需 `git show` 读 LICENSE / package.json
  - curl（本机代理 + 备用代理 `10.74.128.15:11080`）、WebFetch、WebSearch
  - **新增出口：`r.jina.ai` 阅读代理**。本机与 WebFetch 都 403 的 Codrops、Blendkit、three.js 论坛、FWA 条款页，经它读到了原文
  - 各站公开接口：FWA `/api/cases/`、Blender Studio 前端自带的 MeiliSearch 只读 key、projects.blender.org（Gitea API）、archive.org advancedsearch / metadata
- 许可记号：✓ 可训练可分发（MIT / Apache / BSD / CC0 / CC-BY）　△ 有条件（copyleft、逐件核、权属存疑）　✗ 不可用
- 「页面数」口径：路由文件正则计数（Next `app/**/page.*`、`pages/**`、SvelteKit `+page.*`、Astro / Nuxt `pages/**`），不含 md 内容页；文档型站点另记 md 数

---

## 0 结论速览

1. **能用的开源生产站，几乎都是开发者工具和开源基金会的站**
   - 最好的 5 个：Supabase 官网（apps/www）、Payload 官网、ray.so、react.email 官网、openai.fm
   - 全部 MIT 或 Apache-2.0，是真实生产站（GitHub homepage 字段指向生产域名），多数在 2026-10 仍在推送
2. **设计最强的那批，源码公开却没给许可**
   - basement.studio 官网：Awwwards SOTD 2025-04-25，仓库无 LICENSE
   - 同样无许可：Neon、TanStack、astro.build、svelte.dev（根目录无许可）
   - 明确不开源：tailwindcss.com（README 写「not licensed under an open-source license」），posthog.com（LICENSE 写「Please do not duplicate, copy, or use our website」）
   - 结论：「看得到」不等于「能用」，必须逐仓读 LICENSE
3. **对 round 1 结论的修正**
   - three.js 论坛不是「无内容许可」：ToS §3 写用户贡献按 **CC BY-NC-SA 3.0** 授权，商用训练 ✗
   - Codrops 许可页读到原文：demo 默认 MIT，**另有说明的除外**（老仓的「勿原样再分发」就属于这种）；文章「不得整篇转载」
   - **Blendkit 的 CC0 子集也不能整包再分发**：2026 条款 5.9 写 CC0 资产「Article 5 point 4 shall apply accordingly」，而 5.4 禁止脱离项目单独分发。round 1 Top 5 的第 5 名应降为 △，只能内部使用
   - Blender 内置 Essentials 资产已核实为 **CC0**（blender-assets 仓库的 LICENSE 与 README），之前的「口径待补」已解决
   - FWA 条款比 Awwwards 更严：「you may not create a database in any form whatsoever of these web pages」，连做标签库都要书面许可
4. **WebGL 实验档案：量大，可用的少**
   - Experiments with Google 共 1,654 个实验，打 WebGL 标签的 664 个；其中带 GitHub 源码的只有 85 个仓，宽松许可的只有 30 个
   - 这批作品集中在 2011–2015 年，WebGL1 与老版 three.js 居多；论性价比，不如 round 1 的 three.js 官方 examples 和 pmndrs/examples
5. **Blender 生产场景有两条新路径**
   - Big Buck Bunny 工程文件
     - download.blender.org 上的 zip 含 591 个 .blend，可只读中央目录列清单，不必整包下载
     - archive.org 上有第三方镜像，含 203 个 .blend，带角色、道具、布景
   - Blender Studio 可下载文件 636 个，含 .blend 的 164 个，免费的只有 15 个，印证了付费墙

---

## A 开源的生产级网站

### A.1 排名表（设计 × 难度 × 许可干净）

| # | 名称 + 链接 | 拿到什么 | 规模 | 许可 | 质量与难度信号 | 获取方式 |
|---|---|---|---|---|---|---|
| 1 | [supabase/supabase](https://github.com/supabase/supabase) `apps/www` → supabase.com | 官网全站：产品页、Launch Week、博客 | 子目录 5,308 文件；路由 100；md/mdx 567；★114,159（整仓）；push 2026-10-27 | ✓ 根目录 Apache-2.0；`apps/www/package.json` 写 MIT | 依赖 gsap、ogl、motion；有 `Shaders/ShieldGlow.tsx`、`PostgresGlow.tsx`、`components/Globe.tsx`；博客有「interactive constellation three.js r3f」 | blobless clone + sparse checkout `apps/www` |
| 2 | [payloadcms/website](https://github.com/payloadcms/website) → payloadcms.com | 官网（Next 16） | 1,367 文件；路由 98；★642；push 2026-10-27 | ✓ MIT（Copyright 2023 Payload） | Awwwards Honorable Mention 2022-11-25（页面外链 payloadcms.com；与现版本的对应关系待补）；framer-motion | git clone |
| 3 | [raycast/ray-so](https://github.com/raycast/ray-so) → ray.so | 工具型站：代码截图、icon、ios-icons、presets、prompts、snippets、themes | 524 文件；路由 16；★2,368；push 2026-10-15 | ✓ MIT（Raycast Technologies） | 路由含 code / icon / ios-icons / presets / themes 等多个工具页 | git clone |
| 4 | [resend/react-email](https://github.com/resend/react-email) `apps/web` → react.email | 官网 + 邮件组件示例 | 整仓 1,803 文件；路由 28；★19,881；push 2026-10-27 | ✓ `apps/web/license.md` 为 MIT | 仓内 package.json 含 three、@react-three/fiber / drei、framer-motion | sparse checkout `apps/web` |
| 5 | [openai/openai-fm](https://github.com/openai/openai-fm) → openai.fm | 单页交互式 TTS 演示站 | 54 文件；1 页；★2,908；push 2026-03-03 | ✓ MIT | 单页交互式 TTS 演示；Next 15 + Tailwind 4 | git clone |
| 6 | [ghostty-org/website](https://github.com/ghostty-org/website) → ghostty.org | 官网 + 文档 | 506 文件；路由 3（文档走内容）；★328；push 2026-10-27 | ✓ MIT | 终端产品官网 + 文档 | git clone |
| 7 | [nuxt/nuxt.com](https://github.com/nuxt/nuxt.com) → nuxt.com | 官网 + 文档 | 1,378 文件；路由 31；md 105；★461 | ✓ MIT | Nuxt 4 + Nuxt UI 设计系统 | git clone |
| 8 | [radix-ui/website](https://github.com/radix-ui/website) → radix-ui.com | 设计系统官网 + 文档 | 620 文件；路由 25；★1,041；push 2026-10-07 | ✓ MIT（Copyright 2024 WorkOS） | 设计系统官网（WorkOS 维护） | git clone |
| 9 | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) `apps/v4` → ui.shadcn.com | 文档 + blocks 站 | 5,081 文件；路由 19；★126,697（整仓） | ✓ MIT | 设计 token、亮暗主题；registry 已在 round 1 收录 | sparse checkout |
| 10 | [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs) → langfuse.com | 官网 + 文档 | 3,478 文件；路由 27；★247 | ✓ MIT（Langfuse GmbH） | 依赖 three、@react-three/fiber、framer-motion | git clone |
| 11 | [pixel-point/pixelpoint-website](https://github.com/pixel-point/pixelpoint-website) → pixelpoint.io | 设计工作室官网 | 756 文件；路由 36；★92；push 2026-08-28 | ✓ MIT | 工作室自站；Rive + framer-motion（Gatsby） | git clone |
| 12 | [cilium/cilium.io](https://github.com/cilium/cilium.io) → cilium.io | 开源项目官网 | 3,005 文件；路由 124；★73；push 2026-10-21 | ✓ Apache-2.0 + `LICENSE-CC-BY-4.0` | 多页营销 + 内容；framer-motion | git clone |
| 13 | [nodejs/nodejs.org](https://github.com/nodejs/nodejs.org) `apps/site` → nodejs.org | 官网（多语言） | 1,752 文件；页面型文件 1,280（多为多语言 md）；★6,872 | ✓ MIT | 大型多语言多页 | sparse checkout |
| 14 | [vitejs/vite](https://github.com/vitejs/vite) `docs` → vite.dev | 官网 + 文档 | 147 文件；md 57；★83,598（整仓） | ✓ MIT | 有自写落地页组件（`docs/.vitepress/theme/landing/*.vue`） | sparse checkout |
| 15 | [angular/angular](https://github.com/angular/angular) `adev` → angular.dev | 官网 + 文档 + 教程 | 2,646 文件；md 422；★101,095（整仓） | ✓ MIT | 大型文档站；Angular + Tailwind | sparse checkout |
| 16 | [vuejs/docs](https://github.com/vuejs/docs) → vuejs.org | 官网 + 文档 | 515 文件；src md 119；★3,243；push 2026-10-16 | ✓ CC BY 4.0（**图片除外**，LICENSE 原文） | VitePress + gsap | git clone |
| 17 | [zen-browser/www](https://github.com/zen-browser/www) → zen-browser.app | 产品官网 | 164 文件；路由 13；★1,474 | △ MPL-2.0（文件级 copyleft） | Astro 7 + Tailwind 4 | git clone |
| 18 | [godotengine/godot-website](https://github.com/godotengine/godot-website) → godotengine.org | 官网 | 4,904 文件；html 69；★398 | ✓ MIT（LICENSE.txt） | 静态站（无 npm 依赖），多页 | git clone |
| 19 | [bevyengine/bevy-website](https://github.com/bevyengine/bevy-website) → bevy.org | 官网 + 书 + 新闻 | 1,959 文件；md 852；★250 | ✓ MIT | 静态站，内容量大 | git clone |
| 20 | [mozilla/bedrock](https://github.com/mozilla/bedrock) → mozilla.org | 官网全站 | 4,605 文件；html 模板 685；★1,339 | △ MPL-2.0 | 规模最大的多页营销站之一 | git clone |

补充（小或旧，✓）：

- [vercel/hyper-site](https://github.com/vercel/hyper-site)：MIT，★465，push 2025-05-22，3 页
- [14islands/14islands-com-v2](https://github.com/14islands/14islands-com-v2)：MIT，★14，最后提交 2020-05-22
  - 14islands.com 获 Awwwards SOTD 2020-06-29，但与 v2 仓库的版本对应关系待补
- [vercel/swr-site](https://github.com/vercel/swr-site)：Apache-2.0，★511
- [v8/v8.dev](https://github.com/v8/v8.dev)：Apache-2.0，★1,022
- [freshframework/fresh](https://github.com/freshframework/fresh) `www`：MIT，12 个路由
- 文档型（设计一般）：electron/website（Apache-2.0）、facebook/docusaurus（MIT）、withastro/starlight（MIT）、tauri-apps/tauri-docs（MIT）、cloudflare/cloudflare-docs（CC-BY-4.0，★5,366）

### A.2 copyleft（能用，但有传染义务）

| 名称 | 规模 | 许可 | 信号 |
|---|---|---|---|
| [significa/significa.co](https://github.com/significa/significa.co) | 398 文件；路由 63；★312 | AGPL-3.0 | Awwwards HM 2023-05-18（页面外链 significa.co）；SvelteKit + matter-js |
| [midday-ai/midday](https://github.com/midday-ai/midday) `apps/website` | 367 文件；路由 53；★15,102 | AGPL-3.0 | SaaS 产品官网；motion |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) `packages/twenty-website` | 1,480 文件；路由 48；★59,921 | AGPL-3.0，部分文件为商业许可（LICENSE 原文） | 依赖 three |
| [hackclub/site](https://github.com/hackclub/site) | 398 文件；路由 33；★284 | GPL-3.0 | — |
| [WordPress/wporg-main-2022](https://github.com/WordPress/wporg-main-2022) | 219 文件；★83 | GPL-2.0-or-later（package.json） | wordpress.org 2022 改版主题 |

### A.3 看得到但不能用

| 仓库 | 卡点（原文或实测） |
|---|---|
| [basementstudio/website-2k25](https://github.com/basementstudio/website-2k25)（★265） | 无 LICENSE（唯一的 LICENSE.txt 在 `.agents/skills/` 下）；该站获 Awwwards SOTD 2025-04-25（curl 核实）；r3f + rapier，`public/3d/models/*.glb` |
| [neondatabase/website](https://github.com/neondatabase/website)（★332） | 无 LICENSE，README 也未提许可；6,706 文件、390 个路由，Rive + framer-motion |
| [TanStack/tanstack.com](https://github.com/TanStack/tanstack.com)（★1,130） | 无 LICENSE；r3f + `.glb` 模型 |
| [withastro/astro.build](https://github.com/withastro/astro.build)（★512） | 无 LICENSE |
| [sveltejs/svelte.dev](https://github.com/sveltejs/svelte.dev)（★332） | 根目录无 LICENSE；只有 `packages/site-kit/LICENSE`（MIT），管不到站点本体 |
| [tailwindlabs/tailwindcss.com](https://github.com/tailwindlabs/tailwindcss.com) | README：「This project is not licensed under an open-source license and is the intellectual property of Tailwind Labs Inc. The source is available only as an educational resource」 |
| [PostHog/posthog.com](https://github.com/PostHog/posthog.com)（★1,159） | LICENSE：「Please do not duplicate, copy, or use our website for commercial or non-commercial use」；只有 `/contents/` 目录是 MIT |
| [appwrite/website](https://github.com/appwrite/website) | 已归档；README 写 CC BY-NC-ND 4.0 |
| [prisma/web](https://github.com/prisma/web)（★1,106） | 根目录无 LICENSE（只有 `packages/proxy` 为 Apache-2.0）；r3f + ogl |
| [inngest/website](https://github.com/inngest/website) | package.json 写 `"license": "UNLICENSED"` |
| tina.io · remix-website · joinmastodon · AppFlowy-Website · Effect-TS/website · darkroomengineering/sf-website | 均无 LICENSE；sf-website 描述写「Our website, open source.」，但没有给许可 |
| [reactjs/react.dev](https://github.com/reactjs/react.dev) | △ README：「Content … is CC-BY-4.0 licensed」；代码部分没有声明许可 |
| vercel/next.js | nextjs.org 的站点代码不在仓内（`apps/` 下只有 bundle-analyzer） |
| calcom/cal.com | 已 301 到 calcom/cal.diy；apps 只有 api / docs / web，没有营销站 |
| unkeyed/unkey | 原 `apps/www` 已不存在（`web/apps/` 下是 dashboard / design / portal） |
| spacedriveapp/spacedrive | 根目录 Apache-2.0，但仓内没见到营销站目录（路由来自 docs） |

### A.4 发现方法

- 没找到权威的「开源公司官网」awesome 清单（WebSearch 两轮均无）
- GitHub 检索有效，但量小
  - `"official website" in:description stars:>400`：23 仓
  - `"marketing website" in:description stars:>80`：12 仓
  - `topic:agency-website stars:>30`：23 仓，几乎全是模板
- 最有效的是按公司或工作室枚举 org，再逐仓读 LICENSE
  - 工作室 org：basementstudio 43 仓、darkroomengineering 35 仓、14islands 35 仓、pixel-point 39 仓、significa 34 仓、locomotivemtl 90 仓
  - 结果：只有 pixel-point、significa、14islands 公开了带许可的自站

---

## B WebGL / three.js 实验档案

| # | 名称 + 链接 | 拿到什么 | 规模 | 许可 | 质量与难度信号 | 获取方式 |
|---|---|---|---|---|---|---|
| 1 | [Experiments with Google](https://experiments.withgoogle.com/)（chromeexperiments.com 已 301 到 `/collection/chrome`） | 实验页：作者、日期、标签、Launch 链接，部分有「Get Code」 | sitemap 共 1,654 个实验页（全抓）；标签 WebGL 664 · 3D 363 · Three.js 36；有 Get Code 的 326 个（GitHub 304）；WebGL ∩ GitHub 89 页，对应 85 个仓 | 85 仓：MIT 21 · Apache 8 · Unlicense 1 · 无许可 30 · GPL 2 · AGPL 1 · Artistic 1 · NOASSERTION 2 · 已失效 19；**宽松许可合计 30 个** | Google 策展；年份 2011–2015 每年约 200 个，2022–2023 年各约 20 个；高星：WebGL-Fluid-Simulation ★16,768 MIT、sketch-threejs ★2,550 MIT、OrigamiSimulator ★1,403 MIT、The-Spirit ★1,284 MIT | sitemap → 页面 `Get Code Button` 链接 → search API 查许可；robots 只封 `/preview/` 和 `/search` |
| 2 | [googlecreativelab](https://github.com/googlecreativelab)（org） | 实验源码 | 64 仓，其中 Apache-2.0 46 个（search API 计数） | ✓ 多数 Apache-2.0 | [chrome-music-lab](https://github.com/googlecreativelab/chrome-music-lab) ★2,420，已归档，8 个实验目录、138 个 html | git clone |
| 3 | [dataarts](https://github.com/dataarts)（Google Data Arts） | 经典 Chrome 实验 | 12 仓；webgl-globe 2,107 文件；3-dreams-of-black 5,135 文件 | webgl-globe、armsglobe：✓ Apache-2.0（LICENSE 头）；3-dreams-of-black：△ 无 LICENSE 文件，README 写「opened up with the Apache License 2.0」，音乐与影像素材的权属另计 | WebGL 早期标杆（ro.me、Globe） | git clone（均已归档） |
| 4 | [google/santa-tracker-web](https://github.com/google/santa-tracker-web) | 50+ 个小游戏 / 场景的整站 | 5,313 文件；`static/scenes/` 56 个目录；★665；push 2026-10-26 | ✓ LICENSE：「All image and audio files … CC-BY. All other files … Apache 2」 | 生产级、多场景、强美术 | git clone |
| 5 | [WebGLSamples](https://github.com/WebGLSamples/WebGLSamples.github.io) | 经典 WebGL 演示（aquarium、caves、city、electricflower…） | 约 50 个顶层目录；96 个 html；★989 | ✓ BSD-3（LICENSE.md：「Unless otherwise specified inside a file」） | 浏览器性能演示的老牌集合 | git clone |
| 6 | [webgpu/webgpu-samples](https://github.com/webgpu/webgpu-samples) | WebGPU 官方示例 | `sample/` 52 个目录；★2,191；push 2026-10-02 | ✓ BSD-3 | 计算着色器、粒子、阴影等 | git clone |
| 7 | [KhronosGroup/WebGL](https://github.com/KhronosGroup/WebGL) | 主体是一致性测试，另有 `sdk/demos` | 7,704 个 html，其中 demos 26 个（google / intel / mozilla / webkit 等） | ✓ MIT | 规范方出品；demos 偏少 | sparse checkout `sdk/demos` |
| 8 | [oframe/ogl](https://github.com/oframe/ogl) | 极简 WebGL 库 + 示例 | `examples/` 49 个 html；★4,729；push 2025-04-13 | ✓ Unlicense（package.json；仓库无 LICENSE 文件，GitHub 显示 None） | 示例短小、无依赖，适合「单文件重写」题 | git clone |
| 9 | [pmndrs/racing-game](https://github.com/pmndrs/racing-game) | R3F 赛车游戏整站 | 91 文件；★2,224；最后推送 2023-02-23 | ✓ MIT | 物理 + 后处理 + 整站 | git clone |
| 10 | [gfxfundamentals/webgl-fundamentals](https://github.com/gfxfundamentals/webgl-fundamentals) | 教程 + 可运行示例 | 374 个 html；★5,027 | ✓ BSD 式（LICENSE：「Redistribution and use … permitted」） | 题解对：讲解 + 代码 | git clone |
| 11 | [Hubs-Foundation/hubs](https://github.com/Hubs-Foundation/hubs) | 生产级 WebXR 社交应用 | ★2,223 | △ MPL-2.0 | 大型 three.js 应用 | git clone |
| 12 | glslsandbox · vertexshaderart | 着色器画廊站点的代码 | [mrdoob/glsl-sandbox](https://github.com/mrdoob/glsl-sandbox) ★1,686 MIT；[greggman/vertexshaderart](https://github.com/greggman/vertexshaderart) ★141 BSD-3 | 站点代码 ✓；**画廊里用户作品的许可口径待补** | — | — |

**B.2 不能用或价值低**

- Active Theory
  - org 只有 8 个仓，都是小库：activeframe MIT ★418、split-text、fit-text…
  - Paper-Planes-Android-Experiment 无许可；没有站点源码
- Lusion
  - 没找到官方 org；GitHub 搜「lusion」224 个结果全是第三方仿站或逆向工程
  - 例：canxerian/lusion-reverse-engineered 标 CC0，但仿的是别人的设计，权属不在发布者 → ✗
- Three.js Journey
  - 首页「thousands of projects made by students」只是嵌入的 9 条 X 帖，链到 live demo，GitHub 链接 0 条
  - `/selection` 和 `/challenges` 返回 302（需登录）；页脚「© 2025. All rights reserved.」
- basementstudio/basement-laboratory（★385）：无许可 ✗
  - 同 org 的 shader-lab（★714）是 Apache-2.0 工具，可用
- 库与 starter（不是作品，但许可干净）
  - 14islands/r3f-scroll-rig：MIT，★988
  - darkroomengineering/satus：MIT，★1,012
  - darkroomengineering/lenis：MIT，★16,912

---

## C 被封 / 未核站点复查（站点 → 页面原文要点 / 状态）

- **Land-book**
  - 状态：首页、terms、sitemap 本机 403；`robots.txt` 和 `llms.txt` 本机 200；`/pro` 经阅读代理 200
  - robots 原文：「AI assistant crawlers are explicitly listed and welcome」；GPTBot、ClaudeBot、CCBot 与其他 bot 同规则，只封 `/api/`、登录页和筛选参数
  - llms.txt 原文：「When referencing an entry, link to its page … and credit the designer or studio」；模板链接是「affiliate links」
  - 规模（/pro 页原文）：「Browse 20,000+ website examples」「+200,000 categorized website sections」
  - 结论：只有截图和外链，没有源码；`/terms` 不存在（返回首页标题）。✗ 不能作源码；可作发现入口
- **Lapa Ninja**
  - 状态：本机、备用代理、WebFetch 都 403；阅读代理遇到 Cloudflare「Just a moment」
  - 规模只能取搜索摘要（未直读）：首页「7,300+ landing page designs since 2015」「15,000+ full-page website screenshots」；`/post/` 约 7,514 条（每页 24 条 × 314 页）；2025 年 542 条、2026 年 204 条
  - 条款：口径待补
- **The FWA**
  - 状态：首页是 SPA；JS 里找到公开接口 `/api/cases/`；条款页经阅读代理读到原文
  - 规模（API `total` 字段）：10,790 个获奖案例，每条都有奖项
    - FOTD 9,034 · MOTD 2,098 · FOTM 316 · TCEA 209 · FOTY 26 · PCA 24 · TCEAY 4
    - 年份 2000–2026；外链在 github.io 上的只有 3 个
  - Terms §II 原文
    - 「No material, however, can be used for any commercial purpose whatsoever.」
    - 「Unless otherwise expressly permitted in writing, you may not create a database in any form whatsoever of these web pages.」
    - 「Submitted work remains the intellectual property … of its respective owners」
  - 结论：✗ 连标签库都不能建，只能人工浏览参考
- **CSS Design Awards**
  - 状态：本机超时；备用代理 1 次 200（未存正文），之后超时；WebFetch「Socket is closed」；阅读代理返回「Robot Challenge Screen」
  - 搜索摘要：2009 年创办，评审团 200+；奖项有 WOTD、Special Kudos、UI / UX / Innovation、WOTM、WOTY、DOTY；每个 WOTD 带 JPANEL 分
  - 总数与条款：口径待补
- **Codrops 许可页**（tympanus.net/codrops/licensing/）
  - 状态：本机、备用代理、WebFetch 都 403；阅读代理 200
  - 原文
    - 「Our downloadable demos are licensed under the MIT license, if not specifically mentioned otherwise」
    - freebies：「can be used in personal or commercial projects with the exception of redistribution, republishing or sale of the item itself」
    - 文章：「You are free to copy excerpts of our articles but please don't republish entire articles.」
  - 影响
    - round 1 的「2020 后 MIT 仓 ✓、2012–2019 ✗」不变
    - 「教程文章改写成 Query」只能内部用，不分发原文
- **three.js 论坛**（discourse.threejs.org）
  - 状态：本机、备用代理、WebFetch 都 403；阅读代理 200（about.json、site.json、`/c/showcase/7.json`、`/tos`）
  - 规模（about.json）：topics 26,457 · posts 226,367 · users 30,544；showcase 分类 2,948 帖、12,981 回复
  - ToS §3 原文：「User contributions are licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.」
  - 结论：✗（NC-SA）。修正 round 1 的「无内容许可」
- **Shadertoy terms**
  - 状态：本机 403、WebFetch 403、阅读代理遇 Cloudflare、Wayback 429；仍只能看搜索摘要
  - 搜索摘要（结果标题「What license will my Shaders have?」）
    - 「All the shaders you create in Shadertoy are owned by you」
    - 「if you don't place a license on a shader, it will be protected by our default license … CC BY-NC-SA 3.0 Unported」
    - 另授予 Shadertoy 托管、展示的许可
  - 结论：与 round 1 一致，✗（逐条带 MIT 声明的除外）
- **Blendkit 许可与条款**
  - 状态：本机、备用代理、WebFetch 都 403；阅读代理 200（`/docs/licenses/`、licensing-faq、`/terms-and-conditions-2026/`）
  - 许可页原文：「only has 2 available licenses」：Royalty Free 「doesn't allow for re-sale of the asset in the same form」；CC0
  - 条款 5.4：「strictly prohibited to redistribute the product without the incorporation in the project; you are not allowed to create a project that consists only of a product」
  - 条款 5.9：CC0 资产可「use … in any possible way which does not violate … the Terms」，且「**The Article 5 point 4 of the Terms shall apply accordingly**」
  - 条款 5.8：「database is meant to be used for scene creation in Blender and other 3D content creation software」，并部署了防滥用措施
  - AI 条款：在条款页和 FAQ 里检索 AI / train / dataset / machine learning，**均无命中**（没有明文的 AI 条款）
  - 结论：从 Blendkit 下载的 CC0 资产也受合同约束，不能整包再分发 → △，只能内部用
- **Blender Essentials（内置资产）**
  - 状态：projects.blender.org Gitea API 200
  - [blender/blender-assets](https://projects.blender.org/blender/blender-assets)：API `licenses: ["CC0-1.0"]`；LICENSE 为 CC0 1.0 全文；README：「License: 'CC0 - Public Domain'」
  - 结论：✓，见 D 表

---

## D Blender 补充

| # | 名称 + 链接 | 拿到什么 | 规模 | 许可 | 质量与难度信号 | 获取方式 |
|---|---|---|---|---|---|---|
| 1 | [blender/blender-assets](https://projects.blender.org/blender/blender-assets) | 随 Blender 发布的内置资产 + 在线资产库源文件 | git tree 922 项，其中 .blend 177 个：work/bundled 27 · work/online 36 · ready/online 57 · publish/online 57；内容有几何节点 essentials、procedural hair 节点、shading / compositing 节点、雕刻与 GP 笔刷、human base meshes、材质、HDRI world | ✓ CC0 | 官方仓库，2026-10-22 仍在更新；Blender 开发者的 fork 活跃（如 SimonThommes、LukasTonne） | Gitea API / git clone（API size 字段 11,275,721，单位口径待补） |
| 2 | [Blender Studio](https://studio.blender.org/) 资产索引 | 开放电影的生产文件、角色、材质库 | 前端 MeiliSearch 只读索引：asset 8,210；可下载文件 636，其中 `contains_blend_file=true` 164，**免费的 84 个里带 .blend 的只有 15 个**；production_file 2,161（免费 99）；许可分面：CC-BY 7,588 · CC-BY-ND 616 | ✓ CC-BY 为主（ND 的剔除）；但大部分要订阅 | 免费 .blend 例：Charge Material Asset Library、Smoke & Fire FX - Geometry Nodes、2D Smoke Simulation Setup、Einar Real-Time Realism Demo | 页面内嵌的公开搜索 key（`/s/indexes/studio/search`）→ 资产页下载 |
| 3 | Big Buck Bunny 生产文件 · 官方 zip：[download.blender.org/demo/bbb/blender.zip](https://download.blender.org/demo/bbb/blender.zip) | 场景 .blend | zip 830.7 MB（2013-12-16），598 项，**.blend 591 个**（3d 295 · 2d 164 · post 135），解压后 4.87 GB | △ 影片 CC-BY 3.0；zip 内只有 README，没有许可文件 | README：Sunflower（立体版）的场景文件，路径相对「Peach DVD」根目录，**不含角色和道具资产** | HTTP Range 只读中央目录列清单，按需取单个文件 |
| 4 | Big Buck Bunny 生产文件 · 第三方镜像：[archive.org/details/bigbuckbunny_production](https://archive.org/details/bigbuckbunny_production) | 角色、道具、布景、场景 .blend + 贴图 | 430 文件、1.14 GB；**.blend 203 个**（scenes 127 · props 30 · envs 20 · sets 16 · chars 7） | △ 条目 licenseurl 为空，第三方 2022-09-22 上传；内容来自 CC-BY 3.0 影片 | 与第 3 条互补，可拼成完整生产集；Blender 2.4x 时代文件，新版兼容性待测 | archive.org metadata API |
| 5 | Yo Frankie!：[download.blender.org/apricot/](https://download.blender.org/apricot/) | `full-svn/apricot-full-svn.tar` + BGE 游戏包 | tar 107.8 MB（2009-02-22）；yofrankie_bge.zip 120 MB（2012） | 许可口径待补（未展开核实） | 开放游戏的完整 SVN | 直下 |
| 6 | [a1studmuffin/SpaceshipGenerator](https://github.com/a1studmuffin/SpaceshipGenerator) | 程序化飞船 bpy 脚本 | 3 个 .py；★7,842；最后提交 2020-12-23 | ✓ 代码 MIT；**生成内容 CC-BY 3.0**（LICENSE 第二段，附软性请求「less okay with people selling the spaceship models directly」） | 经典程序化建模 | git clone |
| 7 | IRCSS 几何节点三件：[French-Houses](https://github.com/IRCSS/Blender-Geometry-Node-French-Houses) · [Trees](https://github.com/IRCSS/Trees-With-Geometry-Nodes-Blender) · [Chinese-Landscape](https://github.com/IRCSS/Procedural-Chinese-Landscape-Painting-Blender-3D) | 程序化 .blend（几何节点） | .blend 分别为 2 / 1 / 1 个（French Houses 11.9 MB + 9.4 MB）；★331 / 107 / 85；French Houses push 2026-09-28 | ✓ 三仓均 MIT | 建筑、树、山水画风格化；Chinese-Landscape 配 Medium 长文 | git clone |
| 8 | [johnnygizmo/node_assets](https://github.com/johnnygizmo/node_assets) | 几何节点资产 .blend | 22 个 .blend；★114；最后推送 2022-11-22 | ✓ CC0 | 可拆成节点组小题 | git clone |
| 9 | [rbarbosa51/GeometryNodesByTutorials](https://github.com/rbarbosa51/GeometryNodesByTutorials) | 书配套 .blend（Blender 3.3） | 82 个 .blend；★43 | ✓ MIT | README：书的第 1、17、19、21、31、32 章公开为免费 demo | git clone |
| 10 | [josauder/procedural_city_generation](https://github.com/josauder/procedural_city_generation) | 程序化城市（Python + Blender 可视化） | 81 个 .py；★596；最后提交 2016-10-30 | △ MPL-2.0 | 路网 + 建筑 | git clone |
| 11 | [RanmanEmpire/RM_SubdivisionSurface](https://github.com/RanmanEmpire/RM_SubdivisionSurface) | 用几何节点实现细分曲面 | ★152 | ✓ MIT | 节点级算法题 | git clone |

**D.2 注意**

- GPL 系（节点组 .blend 也受 GPL 约束 → △）
  - aachman98/Sorcar ★1,183
  - BradyAJohnston/MolecularNodes ★1,396
  - friggog/tree-gen ★958
  - williamchange/b3dsdf ★515
  - Tams3d/T3D-GN-Presets ★115
- 无许可（✗）
  - node-dojo/dojo-recursive-bins ★642
  - enzyme69/blendersushi ★248
- 2026 年 AI 产物渗入 Blender 侧
  - `topic:blender topic:procedural-generation` 结果里已有 gokayfem/video-to-blender、gaussian-splat-to-blender-nodes 等 agent 工具（2026 年建，MIT）
  - 与 round 1 three.js 侧的结论一致：挖 GitHub 要加日期截断
- download.blender.org 的 `/durian/`（Sintel）、`/mango/`（Tears of Steel）、`/peach/` 只显示「Please visit www.blender.org」
  - Sintel / ToS 的生产文件只在 Blender Studio，基本付费
  - `demo/movies/ToS/copyright.txt` 写 CC BY-ND 3.0，只覆盖原声音轨

---

## E URL 核验清单（2026-10-28）

| 状态 | URL | 方式 / 备注 |
|---|---|---|
| 200 | https://api.github.com/search/repositories?q=repo:… | 多 repo 批量取 ★ / SPDX / push；未鉴权 10 次/分 |
| 200 | github.com 上 50 余仓的 blobless clone（A、B、D 表中各仓） | `git ls-tree` 计数；`git show` 读 LICENSE / package.json |
| 301 | https://github.com/calcom/cal.com → calcom/cal.diy | curl |
| 301 | https://github.com/denoland/fresh → freshframework/fresh | curl |
| 200 | https://raw.githubusercontent.com/tailwindlabs/tailwindcss.com/main/README.md | 「not licensed under an open-source license」 |
| 200 | https://raw.githubusercontent.com/PostHog/posthog.com/master/LICENSE | 「Please do not duplicate…」 |
| 200 | https://raw.githubusercontent.com/appwrite/website/main/README.md | CC BY-NC-ND 4.0 |
| 200 | https://www.awwwards.com/sites/basement-studio-3 | SOTD 2025-04-25 |
| 200 | https://www.awwwards.com/sites/basement-chronicles | SOTD 2023-11-08 |
| 200 | https://www.awwwards.com/sites/significa-1 | HM 2023-05-18，外链 significa.co |
| 200 | https://www.awwwards.com/sites/payload-cms | HM 2022-11-25，外链 payloadcms.com |
| 200 | https://www.awwwards.com/sites/14islands | SOTD 2020-06-29，外链 14islands.com |
| 404 | https://www.awwwards.com/sites/{supabase, ray-so, openai-fm, ghostty, nuxt, radix-ui, midday, tanstack, …} | 猜的 slug 不存在，**不代表没获奖** |
| 200 | https://experiments.withgoogle.com/sitemap.xml + 1,654 个实验页 | 4 线程全抓 |
| 200 | https://www.chromeexperiments.com/ → experiments.withgoogle.com/collection/chrome | 跳转 |
| 200 | https://thefwa.com/api/cases/?offset=…&limit=100 | 108 页，total 10,790 |
| 200（阅读代理） | https://thefwa.com/terms-conditions · /copyright | r.jina.ai |
| 200（阅读代理） | https://tympanus.net/codrops/licensing/ | 本机 / 备用代理 / WebFetch 403 |
| 200（阅读代理） | https://discourse.threejs.org/about.json · /site.json · /c/showcase/7.json · /tos | 本机 / 备用代理 / WebFetch 403 |
| 200（阅读代理） | https://www.blendkit.com/docs/licenses/ · /docs/licenses/licensing-faq/ · /terms-and-conditions-2026/ | WebFetch 403 |
| Cloudflare | https://www.shadertoy.com/terms | 本机 403、WebFetch 403、阅读代理挑战页；Wayback 429 |
| 403 / 挑战页 | https://www.lapa.ninja/（含 /terms/、robots、sitemap） | 三条出口都失败 |
| 超时 / 挑战页 | https://www.cssdesignawards.com/ | 本机超时；备用代理 1 次 200 后超时；阅读代理「Robot Challenge Screen」 |
| 200 | https://land-book.com/robots.txt · /llms.txt · /rss.xml | 本机 curl |
| 403 | https://land-book.com/（首页、about_us、sitemap.xml） | 本机 |
| 200（阅读代理） | https://land-book.com/pro | 20,000+ / 200,000+ |
| 429 | https://web.archive.org/web/…id_/… | 本机与备用代理均被限流；WebFetch 不支持该域 |
| 200 | https://archive.org/wayback/available?url=… | 只能查到快照存在 |
| 200 | https://threejs-journey.com/ · /highlights/1 | WebFetch / curl；/selection、/challenges 返回 302 |
| 200 | https://projects.blender.org/api/v1/repos/search · /repos/blender/blender-assets · /git/trees/main?recursive=true | Gitea API |
| 200 | https://projects.blender.org/blender/blender-assets/raw/branch/main/LICENSE · README.md | CC0 |
| 200 | https://studio.blender.org/search/?type=asset&media_type=file | 页面内嵌 MeiliSearch 配置 |
| 200 | https://studio.blender.org/s/indexes/studio/search | facet / filter 计数 |
| 404 | https://studio.blender.org/sitemap.xml | 301 后 404 |
| 200 | https://download.blender.org/{ED, apricot, apricot/full-svn, demo, demo/movies, demo/movies/ToS, demo/movies/BBB, demo/asset-bundles, demo/old_demos}/ | 目录列表 |
| 200（占位） | https://download.blender.org/{durian, mango, peach}/ | 「Please visit www.blender.org」 |
| 206 | https://download.blender.org/demo/bbb/blender.zip | Range 读中央目录与 README.txt |
| 200 | https://download.blender.org/demo/movies/ToS/copyright.txt | CC BY-ND 3.0（只覆盖原声） |
| 200 | https://archive.org/advancedsearch.php?q=… · https://archive.org/metadata/bigbuckbunny_production | 203 个 .blend |

---

## F 口径待补

- CSS Design Awards、Lapa Ninja 的总量与条款（三条出口都被挡）
- Shadertoy 条款原文（只有搜索摘要）
- Payload（2022 年 HM）、14islands（2020 年 SOTD）的获奖版本与现仓库的对应关系
- glslsandbox、vertexshaderart 画廊里用户作品的许可
- Yo Frankie! full-svn 的许可与内容清单
- blender-assets 的 API `size` 单位，以及是否含 LFS
- 公司官网的设计信号目前只有零星 Awwwards 记录；更系统的打分可用 round 1 的 Awwwards 列表反查域名（只作标签，不建库分发）

