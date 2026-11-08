"""合并后的人工审稿，改 data/showcase.json，可重复跑（merge 之后必须重跑）。

  一  工具函数
  二  配置：文案（导语、场景名、卡片文字、入选理由清洗）
            增删卡（补卡、排序、对照卡、补链接、封面）
            数字（商业数短值、标签改名、营收排行）
  三  执行：逐场景、逐卡套用配置，最后校验
"""
import json
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
P = HERE.parents[1] / 'data/showcase.json'
TAXONOMY = HERE.parents[1] / 'data/tag_taxonomy.json'
XHS_NOTES = HERE.parent / 'samples_src/xhs-vibe-video/notes'
V1_POSTERS = HERE.parents[1] / 'assets/market'


# ---------------------------------------------------------------------------
# 一  工具函数

def XHS(nid, tok):
    return f'https://www.xiaohongshu.com/explore/{nid}?xsec_token={tok}&xsec_source=pc_search'


def split_pair(src, out, swap=False, top=(0, .5), bottom=(.5, 1)):
    """竖版「上成片 / 下白模」封面 → 左右对照的 16:9 图（每半裁成 8:9）；top / bottom 是两块的纵向区间，用来避开中间的标题字"""
    im = Image.open(src).convert('RGB')
    halves = [im.crop((0, int(im.height * a), im.width, int(im.height * b))) for a, b in (top, bottom)]
    if swap:
        halves.reverse()
    h = min(x.height for x in halves)
    w = h * 8 // 9
    tiles = [x.crop(((x.width - w) // 2, (x.height - h) // 2, (x.width - w) // 2 + w, (x.height - h) // 2 + h)) for x in halves]
    canvas = Image.new('RGB', (w * 2 + 6, h), 'white')
    canvas.paste(tiles[0], (0, 0)); canvas.paste(tiles[1], (w + 6, 0))
    canvas.save(out, quality=88)
    return str(out)


# ---------------------------------------------------------------------------
# 二  配置

FAMILY_DESC = {
    'webdev': '写代码出产品的方向里唯一跑出规模的一条：钱来自卖给创作者的订阅，小红书上量最大的是网页复刻和作品集。',
    '3d': '代码本身就是交付物：白模给视频模型定机位，three.js / Blender 场景直接上线，CAD 脚本直接出打印件。',
    'video': '每一帧由代码算出：教学视频最先出爆款，发布片和品牌营销已经有人付钱。',
}
# 总表「代表数据」列：每个场景 1–2 张代表卡，缩略图和数字都从卡片实时取，点了跳到下方的卡
# 写成 (标题, 指标栏标签) 时取那一格的数，只写标题取第一格
SCENE_PICKS = {
    'motion-site': ['作品集泳池', 'UI UX Pro Max'],
    'html-slides': ['Claude Design', 'Genspark 幻灯片'],
    'app-mvp': ['Lovable', 'Base44'],
    'web-games': ['Astrocade', ('TapTap 双榜小游戏', '新游 AI 占比')],
    'greybox-previs': ['Higgsfield 白模插件', 'Nexus 灰模分镜'],
    'code-3d-worlds': ['《小王子》3D 游戏', 'BlenderMCP'],
    'cad-as-code': ['Adam AI CAD', ('text-to-cad', 'GitHub Star')],
    'explainer': ['Vibe知识大赏·熵增', '论文转 3B1B 讲解'],
    'launch': ['HyperFrames', 'Shotbase 发布片'],
    'mv-motion': ['Claude Pop', 'P(doom) MV'],
    'animation': ['多邻国动画复刻', '代码动画完全指南'],
}

# 场景总表（大图卡上方）：场景 key → (谁在付费, 变现方式, 代表数据)；数字是写稿时的快照
SCENE_TABLE = {
    'motion-site': ('求职者、设计师、品牌', '订阅（生成 + 托管平台）', '作品集泳池 1.1 万赞；UI UX Pro Max 14.5 万 Star；Vercel 年收入超 5 亿美元（全公司）'),
    'html-slides': ('打工人、研究生', '自付费工具 / 订阅', '单帖 6,417 赞；Claude Design 发布当天 Figma 跌约 7%；Genspark ARR 2.5 亿美元（全公司）'),
    'app-mvp': ('非程序员', '按月订阅', 'Lovable ARR 超 6 亿美元；Base44 ARR 超 2 亿美元'),
    'web-games': ('平台、广告主', '广告 + 平台分成', 'Astrocade 月活 1000 万；TapTap 上半年新游约 80% 由 AI 制作'),
    'greybox-previs': ('AI 剧集、广告制作方', '工具订阅、按项目接单', 'Higgsfield 全站年化 10 亿美元（自报，全公司）；付费订阅近 100 万'),
    'code-3d-worlds': ('流量方、买资产的开发者', '广告、卖资产包、工具付费版', '《小王子》388 万浏览；资产包 19.99 美元；BlenderMCP 3.3 万 Star'),
    'cad-as-code': ('工程师、创客', '订阅 + 打印 / 钣金下单', 'Adam ARR 900 万美元+（第三方信号）；text-to-cad 2.5 万 Star'),
    'explainer': ('知识博主、自媒体、企业培训', '工具订阅、开源 skill 引流', '熵增 4.1 万赞；论文转 3B1B 讲解 33.6 万浏览；AI 简史 20.7 万浏览'),
    'launch': ('SaaS / App 团队、品牌方', '替代外包、买断授权', 'HyperFrames 7.8 万 Star；Shotbase 20 分钟出片；onetake Pro 79 美元买断'),
    'mv-motion': ('音乐人、创作者', '未查到公开收入', 'Claude Pop 2019 万浏览；P(doom) MV 294 万浏览'),
    'animation': ('暂无明确付费方', 'skill 沉淀与开源引流', '多邻国动画复刻 5,381 赞；代码动画完全指南 3,991 赞；花叔 skill 6,110 Star'),
}
# 分组大图卡的封面：取这张卡的封面（要干净、没有烧进去的大字）
FAMILY_COVER = {'webdev': 'Astrocade', '3d': '中学投标建筑动画', 'video': 'Vibe知识大赏·熵增'}
FRAMEWORK_FAMILIES = {'video'}      # 家族标题下出「按框架看作品」

# 封面：左右对照图（白模在左、成片在右）或主链接视频的某一帧
PAIRS = {
    'Nexus 灰模分镜': (XHS_NOTES / '6ad9b245000000003103756d/images/0.jpg', 'nexus-pair.jpg',
                   dict(swap=True, top=(0, .34), bottom=(.69, 1))),
    '户型图直出白模片': (XHS_NOTES / '6aa7e7d5000000002b01dcdf/images/0.jpg', 'huxing-pair.jpg', dict(swap=True)),
}
FRAMES = {'Deedy 教学视频': 'frame:16.9', 'Shotbase 发布片': 'frame:20.4'}

# 作者开源了自己的项目（agent 当时按帖子归类成 null）
OSS = {'代码动画完全指南': True, 'Clawd 一镜到底': True}

# 挂了链接但原帖没说用了的仓库：不算进「按框架看作品」
NOT_USED = {'Deedy 教学视频': ['hyperframes']}

SCENE_CN = {'explainer': '教学案例生成', 'launch': '产品广告与品牌营销', 'mv-motion': '艺术创作', 'animation': '动画制作', 'greybox-previs': '白模参考视频生成', 'code-3d-worlds': '3D 资产',
            'cad-as-code': '参数化 CAD'}
# 场景导语里那句「谁在付钱」的出处
SCENE_SRC = {'greybox-previs': ('小红书：最近看到很多承接 Blender 白模的单子',
                                XHS('6ad89594000000003301fd48', 'ABBpZEnzBaI6sS_Swpe8pNaWZ6MV_n0qUf8_iL-1CmV-U='))}
SCENE_DESC = {'explainer': '知识博主、自媒体与企业培训买单：一个概念讲成短片，成本从几周降到几分钟',
              'animation': '动画本身就是代码：角色、动效、画风都能写出来，好的写法沉淀成可复用的 skill',
              'launch': 'SaaS、App 团队与品牌方买单：发布片和品牌动效不再外包，几十分钟出片，改文案只需重渲',
              'mv-motion': '歌词 MV、叙事短片：片子本身就是作品，画面逐帧可改',
              'greybox-previs': 'AI 剧集与广告方买单：白模先定机位比例，再让视频模型出片，少返工',
              'code-3d-worlds': '流量最大的场景：网页 3D 世界靠爆款拉流量，变现靠广告、卖资产包'}
SCENE_TAG = {'greybox-previs': 'Blender', 'code-3d-worlds': 'three.js · Blender'}

# (卡片标题, biz 的 k) → 大号短值
SHORT = {
    ('UI UX Pro Max', 'npm 月下载'): '7.8 万',
    ('v0 by Vercel', 'Vercel 年化收入'): '5 亿美元+',
    ('v0 by Vercel', 'v0 用户'): '350 万+',
    ('Genspark 幻灯片', 'ARR'): '2.5 亿美元',
    ('Genspark 幻灯片', '估值'): '26 亿美元',
    ('Lovable', 'ARR'): '6 亿美元+',
    ('Lovable', '估值'): '133 亿美元',
    ('Lovable', '平台应用月访问'): '近 10 亿',
    ('拼豆接单工作台', 'WorkBuddy 月访问'): '885 万',
    ('Astrocade', 'MAU'): '1000 万',
    ('Astrocade', '融资'): '5600 万美元',
    ('TapTap 双榜小游戏', 'TapTap 上半年新游'): '80%',
    ('Nexus 灰模分镜', '改前生成费'): '2000 美元/天',
    ('Higgsfield 白模插件', '年化收入'): '10 亿美元',
    ('Cozy Creek 溪流', '套件售价'): '19.99 美元',
    ('Fly 飞行模拟', '峰值 ARR'): '100 万美元',
    ('BlenderMCP', 'PyPI 下载'): '54 万/月',
    ('Adam AI CAD', '融资'): '410 万美元',
    ('Deedy 教学视频', '成本'): '约 2 美元',
    ('3Blue1Brown', 'YouTube 订阅'): '870 万',
    ('HyperFrames', 'HeyGen ARR'): '2 亿美元+',
    ('Clawd 一镜到底', 'onetake Pro'): '79 美元',
    ('v0 by Vercel', 'agent 触发的部署'): '28 倍',
    ('Astrocade', '月游戏局数'): '2.2 亿局',
    ('BlenderMCP', '用户'): '450 万+',
    ('HyperFrames', '登记采用方'): '12 家',
    ('测评片动效包装', '作者 B 站粉丝'): '71.8 万',
}

# 产品卡补官方视频：给出播放数据，也当封面
EXTRA_LINKS = {
    'v0 by Vercel': ({'kind': 'youtube', 'label': '发布视频', 'url': 'https://www.youtube.com/watch?v=By9wCB9IZp0'},
                     'https://i.ytimg.com/vi/By9wCB9IZp0/maxresdefault.jpg'),
    'Lovable': ({'kind': 'youtube', 'label': '2.0 发布片', 'url': 'https://www.youtube.com/watch?v=xDwR1_vrIg8'}, None),
}

# 手抄的平台数据：fetch_impact 已能自动取（TikTok），从 biz 里去掉，免得两套数字对不上
DROP_BIZ = {('Morfeo 品牌动效', 'TikTok 数据')}

# 小红书帖里作者自述的用户数，补成商业数
EXTRA_BIZ = {
    'Claude Motion': {'k': '用量', 's': '未披露', 'v': 'Anthropic 没有公开 /motion 的使用量或收入（2026-11-04 查）',
                      'src': 'https://claude.com/blog/dashboards-and-motion'},
}

# agent 排行表里的教学片：教学视频是用户点名的核心场景，名额补到 6 张（插在 Deedy 教学视频后面）
EXTRA_CARDS = {'explainer': [
    {'title': '论文转 3B1B 讲解', 'line': '任意一篇论文，自动生成 8 分钟 3Blue1Brown 风讲解片', 'by': 'Deedy Das', 'oss': None,
     'links': [{'kind': 'x', 'url': 'https://x.com/deedydas/status/2103141339651350646'}],
     'biz': [], 'poster': 'frame:150',
     'why': '排行表 #3：X 33.6 万浏览、5385 收藏；「教育类 YouTuber 被自动化」的直接证据。原帖没写 Manim，卡上不写'},
    {'title': 'AI 简史 3 分钟', 'line': '7400 行 React 代码、1 小时出片：零素材、零生图，每帧代码渲染',
     'by': 'Chubby（@kimmonismus）', 'oss': None,
     'links': [{'kind': 'x', 'url': 'https://x.com/kimmonismus/status/2102844654169575547'},
               {'kind': 'github', 'url': 'https://github.com/remotion-dev/remotion'},
               {'kind': 'site', 'url': 'https://www.remotion.dev/'}],
     'biz': [], 'poster': 'frame:60',
     'why': '排行表 #5：原帖写明 Claude Code + Remotion，SVG / Canvas 手绘、开源 TTS、Python 合成配乐，全链路代码'},
    # 小红书教学类高赞：agent 因为没有项目链接按掉了，用户原话是项目链接「最好附上」，不是硬条件
    {'title': 'Claude 自述短片', 'line': '纯 SVG + HTML 写出 168 秒电影感短片，Claude 第一人称讲自己是什么',
     'by': 'elegant', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6aba653b0000000015016a18', 'AB3XFnG7S_FsCY9rceTsgz_Ix9Ohp7khwG9kaC9Lb6erU=')}],
     'poster': str(XHS_NOTES / '6aba653b0000000015016a18/images/0.jpg'),
     'why': '小红书 Vibe Video 赞数第三（6318 赞）；讲「大模型是什么」本身就是科普'},
    {'title': '代码动画完全指南', 'line': '15 分钟讲透代码出片，片子本身就是代码动画；配套 skill 开源',
     'by': 'code秘密花园（ConardLi）', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ae88f6d000000002c01958c', 'ABxkjCkNxbDVck4bpTHc_VJIRIXzeYuXpVKs4tTmFTY9Q=')},
               {'kind': 'github', 'url': 'https://github.com/ConardLi/garden-skills'}],
     'poster': str(XHS_NOTES / '6ae88f6d000000002c01958c/images/0.jpg'),
     'why': '3991 赞 / 5385 藏，国内头部开发者博主；garden-skills 1.4 万 star'},
    {'title': '15 种科普风格', 'line': '皮影、地图、3D 拆解、3B1B 数学……15 种科普画风，每种附提示词',
     'by': 'AI产品自由', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ac50089000000001a0273a8', 'ABHQ1YUAvfry1LnqjvD77tF8WiEPSnf7yPJREdIAUyBg0=')}],
     'poster': str(XHS_NOTES / '6ac50089000000001a0273a8/images/0.jpg'),
     'why': '2579 赞 / 2590 藏；把「一种风格 = 一段提示词」讲明白了，是教学场景的方法库'},
], 'code-3d-worlds': [
    # 3D 家族小红书主链只有 4/12，补三条：普通用户照着做的网页游戏、专业建模师的程序化建模、真实投标里的建筑动画
    {'title': '梵高小岛网页游戏', 'line': '照《小王子》同款思路，Opus 5.5 + Tripo 四步做出可玩的 3D 小岛',
     'by': 'Lala罐头', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ad1f47000000000140396c9', 'ABxQV50uIXOoQGyY63JTcmnL0kySH9dNJsOY4TZIDsMZE=')},
               {'kind': 'site', 'label': 'Tripo', 'url': 'https://www.tripo3d.ai/'}],
     'poster': str(V1_POSTERS / 'xhs-6ad1f47000000000140396c9.jpg'),
     'why': '小红书 3D 方向赞数第二（6823 赞 / 7368 藏）；第一名荷塘是手工建模，不算写代码'},
    {'title': 'Blender 程序化植物', 'line': 'Astra 搭几何节点做程序化植物和动画，以前要在 Houdini 里写一两周代码',
     'by': '星川同学', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6aa6779f000000002902e885', 'ABf0NpDf4M1mXNOpdPx7b2wM8pmTMSbk5JSZRekJ0z30U=')},
               {'kind': 'site', 'label': 'Blender', 'url': 'https://www.blender.org/'}],
     'poster': str(V1_POSTERS / 'xhs-6aa6779f000000002902e885.jpg'),
     'why': '2303 赞；专业建模师（原用 Houdini）的一手对比，说明代码路线已进入专业流程'},
    {'title': '中学投标建筑动画', 'line': 'Opus 5.5 直出 3 分 42 秒投标汇报片：鸟瞰、白模生长、通风分析',
     'by': '吟游诗人阿克曼', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ad19a6a00000000180068b8', 'ABxQV50uIXOoQGyY63JTcmnO-3QtGQaZBblJ3y3cMziww=')}],
     'poster': str(XHS_NOTES / '6ad19a6a00000000180068b8/images/0.jpg'),
     'why': '947 赞 / 966 藏；用在真实的学校投标方案里，是建筑可视化外包的直接替代'},
], 'mv-motion': [
    # 小红书动效类高赞：没有衍生项目可挂，但代表国内创作者在拿代码做什么
    {'title': 'Claude 动效 Reel', 'line': '15 秒 60fps，按 120 BPM 卡 32 拍，8 段演示挤压拉伸与形变',
     'by': '新旧', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ac7a32f000000001a02693d', 'ABoZ5yD4MgUTgwqBKxVVfUJcz1wZZQR104MJGQJF9LiwI=')}],
     'poster': str(XHS_NOTES / '6ac7a32f000000001a02693d/images/0.jpg'),
     'why': '2079 赞；动效设计师视角的「Claude 最懂动态设计」，同款提示词原帖 X 231 万浏览'},
    {'title': '代码梦境短片', 'line': '69 秒梦境短片：太阳月亮、拱门花园、游鱼入心，每一帧都是代码',
     'by': '盏Sienna', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ab8e5d1000000001a024e09', 'AB2dJD-XKGEt-eneJ8rUDZ98wFMDzCm_c-FriZTdqljyQ=')}],
     'poster': str(XHS_NOTES / '6ab8e5d1000000001a024e09/images/0.jpg'),
     'why': '1410 赞；纯代码叙事短片，说明代码出片不止于信息图'},
    {'title': '15 种商用动效', 'line': '磨了三天，15 种商用级动效全由代码实时渲染，1080p 30fps',
     'by': 'Y_', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ad2a63700000000140010db', 'ABI2LFQw__JFuxRUSTvpfExxPcT9PHecgRk0Mu6T21Qus=')}],
     'poster': str(XHS_NOTES / '6ad2a63700000000140010db/images/0.jpg'),
     'why': '907 赞；作者明确按「商用级」交付标准打磨，是动效外包的替代信号'},
], 'launch': [
    {'title': 'Claude 自我宣传片', 'line': '64 秒一镜到底：Clawd 踢飞鼠标，在终端里让 Claude 给自己做片',
     'by': '墨白说', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6add72d2000000003300b7ed', 'ABppXmGidaWMkZ1G1lQkel94Di62DWV82_wB4SLrnBmGI=')}],
     'poster': str(XHS_NOTES / '6add72d2000000003300b7ed/images/0.jpg'),
     'why': '817 赞；品牌自我宣传片的完整样例，国内发布片场景的普通用户版本'},
]}
# 用户审稿：一行三张，每个场景凑到 3 的倍数，宽度才整齐
def V1_XHS(nid):
    return str(V1_POSTERS / f'xhs-{nid}.jpg')


EXTRA_CARDS['motion-site'] = [
    {'title': '作品集泳池', 'line': '作品集做成泳池：项目是漂在水上的黏土图标，留言变成云的影子',
     'by': 'Kia（纽约 ITP）', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ad4f792000000001400c800', 'ABvwejsjldc9bIaf2J9wNRhpzdm4F_gCy-OpPEWpupEeU=')},
               {'kind': 'site', 'url': 'https://kiabai.me/', 'label': '在线看'}],
     'poster': str(HERE / 'posters/kia-pool.jpg'),
     'why': '小红书作品集里赞数最高；站点在线可逛，封面是站点首屏截图'},
    {'title': 'Shopify 文艺复兴站', 'line': '一段短 skill 提取原站素材，复刻 Shopify 2026 冬季版的文艺复兴动效页',
     'by': 'Monet.AI', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6a9d696500000000260339b5', 'ABMCHDxzMf9pi4Jc1S8w8Cesb0nR00O1YuPQqFvJJ9n10=')},
               {'kind': 'site', 'url': 'https://www.shopify.com/editions/winter2026', 'label': 'Shopify 原站'}],
     'poster': V1_XHS('6a9d696500000000260339b5'),
     'why': '网页复刻的高审美样例：以前要写复杂 skill 还常丢动效，这里一段短 skill 就还原了'},
    {'title': '3D 房间个人网页', 'line': '个人网页做成可交互的 3D 房间，文科生第一次上手，已部署上线',
     'by': 'Big喷菇🍄（AI版）', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6a604b38000000001b01f92d', 'ABBAYWhe1fXH9pHXTArOAAJklX6ZmzsAAc-ddflqoY9OE=')}],
     'poster': V1_XHS('6a604b38000000001b01f92d'),
     'why': '非程序员做作品集的代表：绝大部分物件可交互；帖子没贴网址，只挂帖子链接'},
]
EXTRA_CARDS['app-mvp'] = [
    {'title': 'Base44', 'line': '用大白话做应用和网站：副业起步，被 Wix 收购后 ARR 涨到 2 亿美元',
     'by': 'Wix（创始人 Maor Shlomo）', 'oss': False,
     'links': [{'kind': 'site', 'url': 'https://base44.com/'}],
     'biz': [{'k': 'ARR', 's': '2 亿美元+', 'v': '超 2 亿美元（2026-08，创始人披露；Wix 财报披露到 5 月的 1.5 亿）',
              'src': 'https://www.calcalistech.com/ctechnews/article/syw900pvdzg'},
             {'k': '用户', 's': '1000 万+', 'v': '超 1000 万（2026-08，Wix CEO）',
              'src': 'https://x.com/Avishai_ab/status/2090434505731428571'},
             {'k': '收购价', 's': '8000 万美元', 'v': '约 8000 万美元现金，另含业绩对赌（2025-06）',
              'src': 'https://en.globes.co.il/en/article-wix-acquires-israeli-vibe-coding-co-base44-1001513267'}],
     'poster': str(HERE / 'posters/base44-site.jpg'),
     'why': 'Lovable 之外另一个有公开 ARR 的应用生成平台；营收榜是公司口径，Base44 只是 Wix 的一部分，不进榜'},
]
EXTRA_CARDS['web-games'] = [
    {'title': '蛋岛 3D 小游戏', 'line': '3 天做出单依纯「蛋岛」主题 3D 小游戏：化身小单，找每一站的彩蛋',
     'by': 'DAiKONAUT', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6ae957410000000003009114', 'ABUIkL4O4zdknKGujQbqDweqnQZ49xRasgPd9s1no4iN8=')}],
     'poster': V1_XHS('6ae957410000000003009114'),
     'why': '画面完成度最高的网页小游戏；Tripo 出资产、Codex 写交互、接 Blender 渲染。发帖时写的是即将上线'},
]
EXTRA_CARDS['greybox-previs'] = [
    {'title': '何同学一镜到底片头', 'line': '现场物体拍照生成 3D 模型搭出拍摄空间，先排多米诺和机位，4 天内发片',
     'by': 'Hyper3D.AI（官方账号）', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6abcbf3a0000000001009dc0', 'AB2SVSU9PoqkSbtEvrXeThirm4ua443FfnOPtQrzFlUhk=')},
               {'kind': 'site', 'url': 'https://hyper3d.ai/', 'label': 'Hyper3D'}],
     'poster': V1_XHS('6abcbf3a0000000001009dc0'),
     'why': '头部创作者的真实生产案例，帖子是 Hyper3D 官方发的；走实拍不走视频模型，但白模定机位的思路相同'},
    {'title': '16 机位动作片实验', 'line': 'Blender 只放参考方块和 16 台摄像机，73% 的计划切点落在 ±0.6 秒内',
     'by': '天梦君', 'oss': None, 'biz': [],
     'links': [{'kind': 'xhs', 'url': XHS('6a59768b000000001303d671', 'AB2JahK56MhqvZ1aoZQnowWGc109UqC_N3x_wm-u1n2IM=')}],
     'poster': V1_XHS('6a59768b000000001303d671'),
     'why': '少数带量化结果的实验：只传镜头位置反而让动作更自然，白模是给视频模型的构图和剪辑蓝图'},
]
EXTRA_CARDS['code-3d-worlds'].append(
    {'title': 'teardown', 'line': '一句话把任意机器做成能拆开看的 3D 模拟器，单文件 HTML 离线可跑',
     'by': 'elvarofficial', 'oss': True, 'biz': [],
     'links': [{'kind': 'github', 'url': 'https://github.com/elvarofficial/teardown'}],
     'poster': str(HERE / 'posters/teardown-cover.jpg'),
     'why': '用户点名补的；2026-10-30 才建仓。代码即 3D 资产：一个 skill 出可交互页面，还能录成 60fps 成片'})

# 去掉的卡：AI 的 4399 是选卡 agent 自己标的商业性弱；Remotion 商用生态是底座不是案例，商业数搬到 data/framework_works.json；其余是用户审稿删的。
# 卡的配置留着：想恢复只要从这里去掉
DROP_CARDS = {'AI 的 4399', '截图复刻网页', '组会文献汇报', '心理测试小程序', 'Remotion 商用生态', 'Vibe 知识视频拆解',
              'Claude 自述短片', 'Deedy 教学视频', '3Blue1Brown'}

# 成本、售价不是成绩：指标栏用中性色
PLAIN_BIZ = {('Nexus 灰模分镜', '原日均生成费'), ('Cozy Creek 溪流', '套件售价'), ('Clawd 一镜到底', 'onetake Pro'),
             ('Deedy 教学视频', '成本'),
             # 粉丝、下载、访问、采用方：是影响力，不是营收，橙色只留给钱和付费用户
             ('3Blue1Brown', 'YouTube 订阅'), ('测评片动效包装', '作者 B 站粉丝'), ('UI UX Pro Max', 'npm 月下载'),
             ('BlenderMCP', 'PyPI 下载'), ('拼豆接单工作台', '平台月访问'), ('TapTap 双榜小游戏', '新游 AI 占比'),
             ('HyperFrames', '采用方'), ('Claude Motion', '用量'), ('Base44', '用户')}

# 第三方解读 / 实测帖：保留链接，但它的播放点赞不代表这张卡
THIRD_LINKS = {'Claude Motion': ['三模型实测', '中文解读']}

# 按钮改名（同名按钮分不清）
LINK_LABEL = {('3Blue1Brown', 'https://arxiv.org/abs/2510.01174'): 'Code2Video 论文'}

# Video 四类（用户定）：教学案例生成 / 产品广告与品牌营销 / 艺术创作 / 动画制作
NEW_SCENES = {'video': ['animation']}
MOVE_CARDS = {'Claude Motion': 'explainer', 'Codex 口播包装': 'explainer', '15 种商用动效': 'launch',
              '测评片动效包装': 'animation', '多邻国动画复刻': 'animation', '花叔穿越名画': 'animation',
              'Claude 动效 Reel': 'animation', '代码动画完全指南': 'animation', '15 种科普风格': 'animation'}
# 卡片标签：第一个是场景类型（高亮），其余按原帖写明的填；词表和类别在 data/tag_taxonomy.json，这里只能用词表里的词
# 教学案例生成的场景类型按「讲的是什么内容」分，每类留最有代表性的一张
TAGS = {
    # Webdev
    '作品集泳池': ['作品集', 'Claude Code', 'three.js'],
    '个人作品集上线': ['作品集', 'Codex', 'Vercel'],
    'Shopify 文艺复兴站': ['网页复刻', 'GPT-6 Astra', 'Skill'],
    '3D 房间个人网页': ['作品集', 'Codex', 'three.js'],
    'UI UX Pro Max': ['设计规范', 'Claude Code', 'Skill'],
    'v0 by Vercel': ['网页生成', 'v0', 'React'],
    'Claude Design': ['HTML 汇报', 'Claude Design', 'HTML'],
    'Frontend Slides': ['幻灯片', 'Claude Code', 'Skill'],
    'Genspark 幻灯片': ['幻灯片', 'Genspark', 'HTML'],
    'Lovable': ['全栈应用', 'Lovable'],
    'Base44': ['全栈应用', 'Base44'],
    '拼豆接单工作台': ['全栈应用', 'WorkBuddy', '云数据库'],
    'Astrocade': ['小游戏', 'Astrocade'],
    '蛋岛 3D 小游戏': ['3D 网页游戏', 'Codex', 'Blender', 'Tripo'],
    'TapTap 双榜小游戏': ['小游戏', 'TapTap'],
    # 3D
    'Nexus 灰模分镜': ['白模分镜', 'Claude', 'Seedance'],
    'Higgsfield 白模插件': ['白模分镜', 'Higgsfield', 'Blender', 'Seedance'],
    '何同学一镜到底片头': ['拍摄预演', 'Hyper3D Rodin'],
    'Codex 白模预演': ['白模分镜', 'Codex', 'Blender MCP'],
    '16 机位动作片实验': ['动作分镜', 'Sol', 'Blender MCP'],
    '户型图直出白模片': ['户型动画', 'Codex', 'Seedance'],
    '《小王子》3D 游戏': ['3D 网页游戏', 'Opus 5.5', 'Blender', 'Tripo'],
    '果冻海岛': ['3D 微缩世界', 'three.js'],
    '梵高小岛网页游戏': ['3D 网页游戏', 'Opus 5.5', 'Tripo'],
    'Blender 程序化植物': ['程序化建模', 'GPT-6 Astra', 'Blender'],
    '中学投标建筑动画': ['建筑动画', 'Opus 5.5'],
    'Cozy Creek 溪流': ['3D 微缩世界', 'GPT-6 Astra', 'three.js', 'Blender'],
    'Fly 飞行模拟': ['3D 网页游戏', 'Cursor', 'three.js'],
    'BlenderMCP': ['Blender 自动化', 'Blender MCP'],
    'teardown': ['交互模拟器', 'Claude Code', 'three.js', 'Skill'],
    'Adam AI CAD': ['参数化零件', 'Adam', 'Fusion / Onshape'],
    'text-to-cad': ['参数化零件', 'Claude Code', 'build123d'],
    'AI 电路板外壳': ['3D 打印件', 'Codex', 'FreeCAD'],
    # Vibe Video
    'Vibe知识大赏·熵增': ['概念科普', 'Skill'],
    '论文转 3B1B 讲解': ['论文讲解', 'Opus 5.5'],
    'anatomy 原理拆解': ['原理拆解', 'Claude Code', 'Skill'],
    'AI 简史 3 分钟': ['历史脉络', 'Opus 5.5', 'Remotion'],
    'Claude Motion': ['数据讲解', 'Claude'],
    'Codex 口播包装': ['口播讲解', 'Codex', 'HyperFrames'],
    'HyperFrames': ['发布片', 'HeyGen', 'HyperFrames'],
    'Shotbase 发布片': ['发布片', 'Opus 5.5', 'HyperFrames'],
    'Clawd 一镜到底': ['发布片', 'Claude Code', 'three.js', 'Skill'],
    'Morfeo 品牌动效': ['品牌动效', 'Opus 5.5', 'HyperFrames'],
    '15 种商用动效': ['品牌动效', 'Opus 5.5'],
    'Claude 自我宣传片': ['宣传片', 'Claude Code'],
    'P(doom) MV': ['MV', 'Opus 5.5', 'p5.js'],
    'Claude Pop': ['MV', 'Opus 5.5', 'Midjourney'],
    '代码梦境短片': ['叙事短片', 'Opus 5.5'],
    '多邻国动画复刻': ['角色动画', 'Codex', 'Rive'],
    'Claude 动效 Reel': ['动效作品集', 'Opus 5.5'],
    '花叔穿越名画': ['艺术动画', 'Claude Code', 'Skill'],
    '代码动画完全指南': ['制作教程', 'Skill'],
    '15 种科普风格': ['风格库', 'Opus 5.5'],
    '测评片动效包装': ['动效包装', 'Fable 5', 'Remotion'],
}

# 补卡插在场景里哪张卡后面
INSERT_AFTER = {'explainer': 'Deedy 教学视频', 'code-3d-worlds': '果冻海岛', 'mv-motion': 'Claude Pop',
                'launch': 'Shotbase 发布片'}

# 排序：每个场景第一张 = 「精选」视角里展示的那张，放商业价值或影响力最强的；教学案例生成里熵增打头，之后国内外穿插
ORDER = {'motion-site': ['作品集泳池', '个人作品集上线', 'Shopify 文艺复兴站', '3D 房间个人网页', 'UI UX Pro Max', 'v0 by Vercel'],
         'app-mvp': ['Lovable', 'Base44', '拼豆接单工作台'],
         'web-games': ['Astrocade', '蛋岛 3D 小游戏', 'TapTap 双榜小游戏'],
         'greybox-previs': ['Nexus 灰模分镜', 'Higgsfield 白模插件', '何同学一镜到底片头', 'Codex 白模预演',
                            '16 机位动作片实验', '户型图直出白模片'],
         'code-3d-worlds': ['《小王子》3D 游戏', '果冻海岛', '梵高小岛网页游戏', 'Blender 程序化植物', '中学投标建筑动画',
                            'Cozy Creek 溪流', 'Fly 飞行模拟', 'BlenderMCP', 'teardown'],
         'explainer': ['Vibe知识大赏·熵增', '论文转 3B1B 讲解', 'anatomy 原理拆解', 'AI 简史 3 分钟', 'Claude Motion', 'Codex 口播包装'],
         'launch': ['HyperFrames', 'Shotbase 发布片', 'Clawd 一镜到底', 'Morfeo 品牌动效', '15 种商用动效', 'Claude 自我宣传片'],
         'mv-motion': ['P(doom) MV', 'Claude Pop', '代码梦境短片'],
         'animation': ['多邻国动画复刻', 'Claude 动效 Reel', '花叔穿越名画', '代码动画完全指南', '15 种科普风格', '测评片动效包装']}

# 进指标栏的 biz 标签要短，一格放得下
RENAME_K = {('Lovable', '平台应用月访问'): '应用月访问', ('拼豆接单工作台', 'WorkBuddy 月访问'): '平台月访问',
            ('TapTap 双榜小游戏', 'TapTap 上半年新游'): '新游 AI 占比', ('Genspark 幻灯片', 'ARR'): '全公司 ARR',
            ('Nexus 灰模分镜', '改前生成费'): '原日均生成费', ('v0 by Vercel', 'Vercel 年化收入'): 'Vercel 年收入',
            ('Higgsfield 白模插件', '年化收入'): '全站年化',
            ('v0 by Vercel', 'agent 触发的部署'): 'agent 部署', ('Astrocade', '月游戏局数'): '月局数',
            ('HyperFrames', '登记采用方'): '采用方'}

# 文字统一：core = 模型或工具 · 场景 · 框架（第一个上色）；line 一句话说做了什么、值在哪，30 字上下
TEXT = {
    '个人作品集上线': '设计师用 Codex 搭作品集，GitHub + Vercel 免费上线',
    'UI UX Pro Max': '给编码 agent 的设计规则库，专治页面的「AI 味」',
    'v0 by Vercel': '一句话生成 React 页面，一键部署上线',
    'Claude Design': 'AI 做 PPT 从「图片」走到可编辑、可交互的 HTML',
    'Frontend Slides': '编码 agent 的幻灯片 skill：先挑风格，再出单文件 HTML',
    'Genspark 幻灯片': 'HTML 底的幻灯片 agent：自动查资料成稿，可导出 PPTX',
    'Lovable': '一句话生成带数据库的全栈应用并上线',
    '拼豆接单工作台': '一句话做出带订单库的接单站，发布即得链接',
    'AI 的 4399': '一个网址收齐开源 AI 小游戏，人和 AI 同场玩',
    'TapTap 双榜小游戏': '两款 AI 小游戏同登 TapTap 总榜，一款广告日入千元',
    'Astrocade': '一句话生成小游戏，像刷短视频一样刷着玩',
    'Nexus 灰模分镜': 'Claude 搭灰模截成分镜喂 Seedance，镜头与比例不再跑偏',
    'Higgsfield 白模插件': 'Agent 在 Blender 搭白模定运镜，视口直出 Seedance 成片',
    'Codex 白模预演': 'Codex 经 MCP 搭白模，先锁构图机位，再交给视频模型',
    '户型图直出白模片': '户型图标好走位，零建模出 30 秒白模，再渲成动画',
    '《小王子》3D 游戏': '一人 16 天把整本书做成可漫游的网页 3D 游戏',
    '果冻海岛': '海岛装进果冻：灯塔、鲸鱼、海浪，昼夜与天气可切',
    'Cozy Creek 溪流': 'Blender 出资产、three.js 渲染，再打包成套件售卖',
    'Fly 飞行模拟': 'AI 写的多人飞行游戏，卖广告位和飞机，17 天 ARR 破百万',
    'BlenderMCP': '任意大模型经 MCP 写 bpy 驱动 Blender，截图回看再改',
    'Adam AI CAD': '一句话出可编辑参数化零件，嵌进 Fusion、Onshape',
    'text-to-cad': 'Agent 写 build123d 脚本出 STEP，直连打印与钣金下单',
    'AI 电路板外壳': 'Codex 驱动 FreeCAD 画外壳，打印出来真装上了',
    'Vibe知识大赏·熵增': '170 秒讲熵增，黑底金字粒子；原帖没写栈，同款画风已被拆成开源代码 skill',
    'Deedy 教学视频': '原帖：Opus 5.5 很会做教学类视频，示范片 1 分钟、约 2 美元',
    '论文转 3B1B 讲解': '任意论文自动生成 8 分钟 3Blue1Brown 风讲解片',
    'AI 简史 3 分钟': '7400 行 React、1 小时出片：零素材零生图，每帧代码渲染',
    'anatomy 原理拆解': '让 Claude 造台机器讲概念：机械表、布隆过滤器可拆开看',
    'HyperFrames': '写 HTML 即出片，OpenAI、tldraw 已用于生产',
    'Shotbase 发布片': '20 分钟用 HyperFrames 写出 Mac App 发布片',
    'Clawd 一镜到底': 'three.js 单文件做出一镜到底发布片，成本约 20 元',
    'Morfeo 品牌动效': '品牌规范写进 MOTION.md，卡点出整条动效',
    'P(doom) MV': '模型自定分镜、逐句配画的手绘风 MV，源码开源',
    'Claude Pop': '同一首歌，Opus 独自跑 12 小时重做纸感 MV：JS 动画 + Midjourney 素材',
    '花叔穿越名画': '复刻艺术史动画后沉淀成 skill：35 种画风、9 种解说语法',
    '多邻国动画复刻': '逆推多邻国 Rive 动画做成 skill，Codex 出新角色并对口型',
    'Claude Motion': 'Anthropic 官方：把季报、图表做成动画片，导出 MP4',
    'Codex 口播包装': '口播 → 时间戳脚本 → 分镜 → HyperFrames 渲染，教程即成品',
    '测评片动效包装': '测评片 80% 分镜动效由 Agent 写 Remotion，再进 AE',
}

# 不是模型写的代码，只作天花板对照：卡片角标标「人写 · 对照」，不进汇总和排行
REF = {'3Blue1Brown': ('人写 · 对照', '人写 Manim 的受众天花板；模型写 Manim 的研究线见 Code2Video')}

# 营收排行：年化收入（美元），标签写清口径
REVENUE = {    # 卡片标题: (美元, 显示值, 口径, 榜上显示的公司名)
    'Higgsfield 白模插件': (1e9, '10 亿美元', '全站年化', 'Higgsfield'),
    'Lovable': (6e8, '6 亿美元+', 'ARR', 'Lovable'),
    'v0 by Vercel': (5e8, '5 亿美元+', '全公司年收入', 'Vercel'),
    'Genspark 幻灯片': (2.5e8, '2.5 亿美元', '全公司 ARR', 'Genspark'),
    'HyperFrames': (2e8, '2 亿美元+', '全公司 ARR', 'HeyGen'),
}

# 入选理由上页面前去掉选卡过程里的内部用语
WHY_DROP = ('未选', '卡上不写', '也要写上', '可挂 GitHub', '只能挂', '归 3D 家族', '可换成', '按用户口径挂为框架化版本')
WHY_CLEAN = [('本组 star 第二高的讲解类 skill', '讲解类 skill 里 star 第二高'),
             ('小红书 3D 方向赞数第二（6823 赞 / 7368 藏）', '小红书「AI 游戏建模」搜索下的高赞帖（6823 赞 / 7368 藏）'),
             ('X 28 万播放', 'X 28 万浏览'),
             ('用户点名线索；', ''), ('用户点名补全：', ''), ('用户点名；', ''), ('排行表 #3：', ''), ('排行表 #5：', ''),
             ('按用户口径挂为框架化版本', '按同一路线挂为框架化版本'), ('biz 是', '商业数是')]

ORIG_K = {(t, new): (t, k) for (t, k), new in RENAME_K.items()}


# ---------------------------------------------------------------------------
# 三  执行

def curate_scene(s):
    s['cn'] = SCENE_CN.get(s['key'], s['cn'])
    s['desc'] = SCENE_DESC.get(s['key'], s['desc'])
    if s['key'] in SCENE_TAG:
        s['tag'] = SCENE_TAG[s['key']]
    if s['key'] in SCENE_SRC:
        s['src'] = dict(zip(('label', 'url'), SCENE_SRC[s['key']]))


def curate_biz(c, used):
    """去掉手抄数据 → 补短值 s（改过名的也认，脚本可重复跑）→ 标签改短 → 补作者自述的数"""
    c['biz'] = [b for b in c.get('biz') or [] if (c['title'], b['k']) not in DROP_BIZ]
    for b in c['biz']:
        key = ORIG_K.get((c['title'], b['k']), (c['title'], b['k']))
        if key in SHORT:
            b['s'] = SHORT[key]
            used.add(key)
        b['k'] = RENAME_K.get(key, b['k'])
    extra = EXTRA_BIZ.get(c['title'])
    if extra and not any(b['k'] == extra['k'] for b in c['biz']):
        c['biz'].append(extra)


def clean_why(why):
    """入选理由按「；」「。」切句，整句去掉编辑批注，再做词语替换"""
    parts = [x for x in re.split(r'(?<=[；。])', why) if x.strip() and not any(k in x for k in WHY_DROP)]
    why = ''.join(parts).rstrip('；。，')
    for a, b in WHY_CLEAN:
        why = why.replace(a, b)
    return why


def curate_card(c, used):
    t = c['title']
    curate_biz(c, used)
    for b in c['biz']:
        if (t, b['k']) in PLAIN_BIZ:
            b['plain'] = True
    for l in c['links']:
        if l.get('label') in THIRD_LINKS.get(t, []):
            l['third'] = True
        if (t, l['url']) in LINK_LABEL:
            l['label'] = LINK_LABEL[t, l['url']]
    c['by'] = (c.get('by') or '').replace('（小红书）', '')      # 平台已经在封面角标上
    if t in TEXT:
        c['line'] = TEXT[t]
    c['core'] = TAGS[t]
    if t in EXTRA_LINKS:
        link, cover = EXTRA_LINKS[t]
        if link['url'] not in {l['url'] for l in c['links']}:
            c['links'].insert(1, link)
        c['poster'] = cover or c.get('poster')
    if t in PAIRS:
        src, name, kw = PAIRS[t]
        c['poster'] = split_pair(src, HERE / 'posters' / name, **kw)
    c['poster'] = FRAMES.get(t, c.get('poster'))
    if t in OSS:
        c['oss'] = OSS[t]
    if t in NOT_USED:
        c['not_used'] = NOT_USED[t]
    if t in REF:
        c['ref'], c['line'] = REF[t]
    if t in REVENUE:
        usd, v, k, name = REVENUE[t]
        c['rev'] = {'usd': usd, 'v': v, 'k': k, 'name': name}


def insert_cards(s, have):
    if s['key'] in EXTRA_CARDS:
        at = next((i + 1 for i, c in enumerate(s['cards']) if c['title'] == INSERT_AFTER.get(s['key'])), len(s['cards']))
        s['cards'][at:at] = [c for c in EXTRA_CARDS[s['key']] if c['title'] not in have | DROP_CARDS]


def move_cards(f):
    """按 MOVE_CARDS 换场景，补上新场景，搬空的场景去掉"""
    by_key = {s['key']: s for s in f['scenes']}
    for key in NEW_SCENES.get(f['key'], []):
        if key not in by_key:
            by_key[key] = {'key': key, 'cn': SCENE_CN[key], 'desc': SCENE_DESC[key], 'cards': []}
            f['scenes'].append(by_key[key])
    for s in f['scenes']:
        for c in [c for c in s['cards'] if MOVE_CARDS.get(c['title'], s['key']) != s['key']]:
            s['cards'].remove(c)
            by_key[MOVE_CARDS[c['title']]]['cards'].append(c)
    f['scenes'] = [s for s in f['scenes'] if s['cards']]


def order_cards(s):
    if s['key'] in ORDER:
        rank = {t: i for i, t in enumerate(ORDER[s['key']])}
        s['cards'].sort(key=lambda c: rank.get(c['title'], len(rank)))


def check_tags(cards):
    """每张卡第一个标签是场景类型且只有一个；不许用词表外的词，词表里也不留没人用的词"""
    kinds = {k['key']: k['tags'] for k in json.loads(TAXONOMY.read_text())['kinds']}
    vocab = {t for tags in kinds.values() for t in tags}
    for c in cards:
        assert set(c['core']) <= vocab, f'词表外的标签：{c["title"]} {set(c["core"]) - vocab}'
        types = [t for t in c['core'] if t in kinds['type']]
        assert types == c['core'][:1], f'场景类型要放第一位且只有一个：{c["title"]} {c["core"]}'
    idle = vocab - {t for c in cards for t in c['core']}
    assert not idle, f'词表里没人用的词：{idle}'


def main():
    d = json.loads(P.read_text())
    used = set()
    for f in d['families']:
        f['desc'] = FAMILY_DESC.get(f['key'], f.get('desc', ''))
        f['cover'] = FAMILY_COVER[f['key']]
        if f['key'] in FRAMEWORK_FAMILIES:
            f['frameworks'] = True
        have = {c['title'] for s in f['scenes'] for c in s['cards']}      # 换过场景的卡不再补一遍
        for s in f['scenes']:
            s['cards'] = [c for c in s['cards'] if c['title'] not in DROP_CARDS]
            curate_scene(s)
            insert_cards(s, have)       # 先插卡再套配置，补进来的卡也走同一套，第一次跑就是终态
        move_cards(f)
        for s in f['scenes']:
            s['payer'], s['revenue'], s['proof'] = SCENE_TABLE[s['key']]
            s['picks'] = [list(x) if isinstance(x, tuple) else [x, None] for x in SCENE_PICKS[s['key']]]
            order_cards(s)
            for c in s['cards']:
                curate_card(c, used)
    cards = [c for f in d['families'] for s in f['scenes'] for c in s['cards']]
    for c in cards:                     # 补进来的卡也要洗
        c['why'] = clean_why(c.get('why') or '')

    extra_titles = {c['title'] for cs in EXTRA_CARDS.values() for c in cs}
    untexted = [c['title'] for c in cards if c['title'] not in set(TEXT) | extra_titles and not c.get('ref')]
    assert not untexted, f'没写文字：{untexted}'
    check_tags(cards)
    unused = {k for k in set(SHORT) - used if k[0] not in DROP_CARDS}
    assert not unused, f'没对上的短值：{unused}'
    P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    print('curated', len(cards), 'cards')


if __name__ == '__main__':
    main()

