# 总页 Application 的 case 数据

总页 = `output/total.html`。Application 是 case 画廊，其余四个标签是子页的预览框。

## 流程

一条龙：`python3 scripts/make_total.py refresh`（下面 2–6 步，取数只刷新超过 1 天的）

1. 选 case：三个家族各一份 `cards_<family>.json`（webdev / 3d / video），来源记录在 `notes_<family>.md`
2. 合并：`python3 scripts/make_total.py merge` → `data/showcase.json`（只换 scenes，家族元数据不动）
3. 审稿：`python3 middle_processing/showcase/curate.py`，merge 之后必须重跑
   - 场景名对齐用户原话、统一卡片文字（core / line）
   - 补卡、删卡、换场景（`MOVE_CARDS`）、调顺序、指定封面
   - 商业数短值 `s`（进指标栏的大号数字）、营收排行、人写对照卡
4. 取数：`python3 scripts/fetch_impact.py --all` → `data/showcase_impact.json`
   - 同时覆盖 `data/framework_works.json` 里的作品
5. 抽帧、截片：`python3 scripts/make_total.py frames`、`clips`（慢，可挂后台；构建本身不联网）
   - frames：X 视频按 `poster: frame:<秒>` 抽封面
   - clips：X 视频截 6 秒无声预览，悬停播放；小红书视频笔记用爬取时的 5 帧轮播代替
6. 出页：`python3 scripts/make_total.py`（`scripts/build.py` 末尾也会自动跑）

## 卡片字段

| 字段 | 含义 |
|---|---|
| title | 作品 / 产品名 |
| core | 标签：第一个是场景类型（高亮），其余按原帖写明的填；在 `curate.py` 的 `TAGS` 里打，只能用 `data/tag_taxonomy.json` 词表里的词 |
| line | 一句话，30 字上下 |
| by | 作者或公司 |
| oss | true 开源 · false 商用 · null 个人作品 / 帖子 |
| poster | 本地路径、URL，或 `frame:<秒>`（主链接视频的那一帧）；空则取主链接缩略图 |
| links | `[{kind, url, label?}]`；`links[0]` 是作品本身 |
| biz | `[{k, v, src, s?}]`：营收、用户、融资等，必须带来源；有 `s` 的进指标栏 |
| ref | 人写的对照卡（如 3Blue1Brown），不计入汇总和排行 |
| rev | 营收排行用：`{usd, v, k, name}` |

## 卡片上的数字

- 指标栏三格，按卡片性质排
  - 商用：商业数 → GitHub star → 平台数
  - 开源：平台数 → star → 商业数（star 就是作品本身的影响力）
  - 帖子：平台数 → 商业数 → 框架 star
- 平台数：YouTube 播放 / 点赞，X 浏览 / 点赞 / 收藏，TikTok 播放 / 点赞 / 收藏，小红书 点赞 / 收藏 / 评论，B 站 播放 / 点赞 / 收藏
- 作者行带发布月份（GitHub 主链接不带）

## Application 的结构

- 三个排行：海外传播、小红书热度、营收
- 场景总表：能力 × 场景，谁在付费、变现方式、代表数据，写在 `curate.py` 的 `SCENE_TABLE`
- 三张分组大图卡：点哪张看哪组，封面由 `curate.py` 的 `FAMILY_COVER` 指定
- 每个场景的卡片数保持 3 的倍数，一行三张才整齐；排不满时第一张会放大成横版或半宽
- Vibe Video 家族下「按框架看作品」：`data/framework_works.json` 列卡片之外的代表作品，`biz` 是框架自身的商业数
- Vibe Video 四类：教学案例生成 / 产品广告与品牌营销 / 艺术创作 / 动画制作
  - 教学案例生成按讲的内容分六型，每型一张：概念科普、论文讲解、原理拆解、历史脉络、数据讲解、口播讲解

## 标签词表

- `data/tag_taxonomy.json`：五类标签，颜色即类别；`curate.py` 校验词表外的词、缺场景类型的卡、没人用的词
  - 场景类型（黄，高亮）：这是什么案例
  - Agent / 模型（紫）：谁写的代码
  - 技术方案（绿）：跑在什么框架上
  - 素材生成（蓝）：用什么模型出素材
  - 产品平台（粉）：背后是哪个产品
- 帖子没写明的不标；页面底部的词表由这个文件生成
- 彩色只留给标签：封面角标、补充说明都是中性色，指标栏的橙色只表示钱

## 目录

- `cards_*.json`、`notes_*.md`：选 case 的产物
- `impact_*.json`：选 case 时各自的取数缓存（正式缓存是 `data/showcase_impact.json`）
- `curate.py`：审稿脚本
- `posters/`：封面原图缓存（URL 哈希命名）和拼好的对照图（`*-pair.jpg`）
- `clips/`：悬停预览片缓存（URL + 起点哈希命名）

