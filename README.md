# final-visual-code-blog

Visual Coding 博客的最终版，今后只改这里。

- Webdev / 3D / Video / 画廊：来自 `../visual-coder-blog-v2`
- Market：来自 `../visual-coder-blog`
- 两个老项目原样保留，不再更新

## 页面

```
output/
  total.html           总页：Hero + Application 画廊 + 四个子页预览框
  webdev.html          Webdev (2D)
  3d.html              3D 原版（保留对比）
  3d-v2.html           3D 改写版，照 webdev.html 的表达、表格、标题和结构重写
  video.html           Video
  market.html          Market
  deep-research.html   Deep Research 正文，各页的 Deep Research 按钮指这里
  assets/              所有页面共用的图、封面、预览片
```

深链

- 子页：`webdev.html#verifier`、`3d.html#data`、`video.html#vibe`、`market.html#webdev`
- 总页：`total.html#web`、`total.html#web/verifier`、`total.html#market/webdev`

总页的预览框

- 壳是 `scripts/doc_preview.html`，改自 critic-blog 的 `charts/doc-preview.html`
- 打开标签才加载子页；子页不知道自己被嵌入，单独打开和预览里是同一个页面
- 3D 标签并排放原版和 v2，一边切视图另一边跟着切；窄屏上下叠

## 目录

```
pages/      一章一个 md，build.py 的输入
              web.md 3d.md video.md   由 parts/ 装配，别手改
              market.md overview.md   手写
parts/      Web / 3D / 3D v2 / Video 的正文，一个视图一个文件，改这里（parts/3d 保持原样，3D 的新改动写 parts/3d-v2）
data/       benchmark 与管线元数据、showcase 案例、划词备注
assets/     源图：logo、figures、samples、market（Market 封面）、js、css
scripts/    构建与生成脚本、两个页面模板
middle_processing/   调研原文、爬取结果、样例、缓存
output/     产物，别手改
```

## 重建

```bash
python3 scripts/gen_pages.py   # 改了 parts/ 或 data/ 之后：parts + data → pages/{web,3d,3d-v2,video}.md
python3 scripts/build.py       # pages/*.md → output/ 全部页面（末尾自动跑 make_total.py）
python3 scripts/make_total.py  # 只改了总页或 showcase 数据时用
```

`gen_pages.py` 跑完会自查覆盖率：映射表和元数据两边对不上的名字会打 warn。
`build.py` 里 `引用了不存在的文件` 的 warn 基本来自样例网页的源码字符串，不是页面要加载的资源。

## 改什么动哪里

- 章节正文：`parts/<章>/<视图>.md`
  - Web (2D)、3D、3D v2：`bench` `opendata` `data` `verifier` `train`
  - Video：`vibe` `from-web` `from-blender`
- 表格：正文里写标记，数据改 `data/*.json`，分类改 `data/buckets.json`
  - `<!--BENCH:html,webdev,ppt,manim-->`
  - `<!--PIPE:blender,3js,cad-->`
- 总页开头的 benchmark 图（Webdev 2 / 3D 3 / Video 1）：数据只改 `data/header_bench.json`
  - `python3 scripts/make_bench_charts.py && python3 scripts/make_total.py`
  - 每个面板自带坐标范围和小数位；Kling-Keye 没分数时画「待补」，有了就在 `scores` 里加 `"keye"`
  - 分数来源与核对记录：`middle_processing/notes/header-bench/{webdev,3d,video}.md`
- Application 画廊：`data/showcase.json`，流程见 `middle_processing/showcase/README.md`
  - 卡片标签：词表 `data/tag_taxonomy.json`，打标在 `middle_processing/showcase/curate.py` 的 `TAGS`
  - 一条龙：`python3 scripts/make_total.py refresh`
- Market：`pages/market.md`；卡片区由脚本写进标记之间，别手改
  - `scripts/market_demos.py`：`<!--DEMOS:tab-->`，数据 `middle_processing/market/demos_*.json`
  - `scripts/market_bestpractice.py`：`<!--BP:route-->`，数据 `middle_processing/market/best_practice.json`
  - `scripts/market_xhs_gallery.py`：`<!--XG:route-->`，数据 `middle_processing/market/xhs/gallery.json`
- 页面骨架：子页 `scripts/page_template.html`，总页 `scripts/total_template.html`

## 素材生成

- 数据样例（规范见 `middle_processing/SAMPLES.md`）
  - `scripts/fetch_showcase_samples.py`：原始文件 → `middle_processing/samples_src/<slug>/`
  - `scripts/build_samples.py`：样例组件 → `middle_processing/samples/<slug>.html`
- draw.io 图：`assets/figures/<name>.drawio` → `scripts/make_drawio_embed.py` → `<name>.html`
  - Web Verifier 图 3.1：`scripts/make_webdev_pipeline.py`
- 审美对比：`middle_processing/figure_src/aesthetic-pairs/` → `scripts/make_aesthetic_pairs.py`
  - 缩略图先跑 `python3 scripts/make_aesthetic_pairs.py shots`（需 Playwright）
- 书卡：`scripts/make_book_gallery.py`，内容写在脚本的 `BOOKS` 里
- Vibe Video 页
  - 爬取：`scripts/xhs_vibe_crawl.py search|fetch|frames|sheets`（带登录 Cookie，Cookie 文件不进项目）
  - 手写配置：`middle_processing/figure_src/vibe-video/{scenes,projects}.json`
  - 生成：`scripts/make_vibe_video.py build`，重写 `parts/video/vibe.md` 的两段表格
- 来源笔记：`middle_processing/notes/`

## 划词备注

正文只放结论，长解释挂在备注里：划词 → 「＋ 备注」→ 存进 `data/notes.json`。

```bash
nohup setsid python3 scripts/serve_notes.py --port 8977 > /dev/null 2>&1 &
# 访问 <网关>/proxy/8977/output/webdev.html —— 可增删改
```

其他方式打开是只读，看到的是 build 时嵌进页面的那份。这时控制台里 `api/notes` 的 404 是正常的。

