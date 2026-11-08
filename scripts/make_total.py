#!/usr/bin/env python3
"""总页 output/total.html：Hero + Application（case 画廊）+ 四个预览标签（Webdev / 3D / Video / Market）。

四个子页都放在 doc-preview 壳里（scripts/doc_preview.html），打开标签才加载。build.py 末尾会自动跑本脚本。

  python3 scripts/make_total.py refresh   # 下面六步一次跑完（取数只刷新超过 1 天的）

  python3 scripts/make_total.py merge     # middle_processing/showcase/cards_*.json → data/showcase.json（只换 scenes，保留家族元数据）
  python3 middle_processing/showcase/curate.py   # 审稿：文字、补卡、商业数短值、排行口径（merge 之后必须重跑）
  python3 scripts/fetch_impact.py --all  # 刷新卡片链接的播放、点赞、star
  python3 scripts/make_total.py frames    # 预抽视频帧当封面（慢，可挂后台；构建本身不联网抽帧）
  python3 scripts/make_total.py clips     # 截 6 秒悬停预览片（同上，构建只读缓存）
  python3 scripts/make_total.py           # data/showcase.json + data/showcase_impact.json → output/total.html

数据：
  data/showcase.json          三个能力家族 → 场景 → 卡片（字段见 middle_processing/showcase/README.md）
  data/showcase_impact.json   fetch_impact.py 的缓存，按链接取数
  data/framework_works.json   「按框架看作品」里卡片之外的代表作品
  data/tag_taxonomy.json      卡片标签词表，五类，颜色即类别
产物：
  output/total.html           模板 scripts/total_template.html
  output/assets/showcase/     卡片封面（640 宽 JPEG；原图缓存在 middle_processing/showcase/posters/）
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/showcase.json'
IMPACT = ROOT / 'data/showcase_impact.json'
TAXONOMY = ROOT / 'data/tag_taxonomy.json'         # 卡片标签词表，颜色即类别
FRAMEWORKS = ROOT / 'data/framework_works.json'    # Vibe Video「按框架看作品」：卡片之外的代表作品
CARDS = ROOT / 'middle_processing/showcase'
TEMPLATE = ROOT / 'scripts/total_template.html'
SHELL = ROOT / 'scripts/doc_preview.html'
OUT = ROOT / 'output'
POSTERS = OUT / 'assets/showcase'
POSTER_CACHE = CARDS / 'posters'
CN_PROXY = 'http://10.68.24.18:11080'
CN_HOSTS = ('xhscdn.com', 'rednotecdn.com', 'hdslb.com', 'xiaohongshu.com')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'

esc = html.escape

# ---------------------------------------------------------------------------
# 图标与平台

ICON = {
    'youtube': '<svg viewBox="0 0 24 24"><path fill="#ff0033" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-4.8.5-4.8s0-3.2-.5-4.8z"/><path fill="#fff" d="M9.75 15.02 15.5 12 9.75 8.98z"/></svg>',
    'x': '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
    'github': '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.2-3.1-.1-.4-.5-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17 4.6 18 4.9 18 4.9c.6 1.6.2 2.8.1 3.2.8.8 1.2 1.9 1.2 3.1 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>',
    'xhs': '<svg viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#ff2442"/><text x="12" y="16.6" font-size="12" font-weight="800" text-anchor="middle" fill="#fff" font-family="sans-serif">书</text></svg>',
    'tiktok': '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.8 5.8 0 1 0 5 5.7V9a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.3-1.5"/></svg>',
    'bilibili': '<svg viewBox="0 0 24 24"><path fill="#00a1d6" d="M17.8 4.6h-1.3l1.7-1.7a1 1 0 0 0-1.4-1.4L13.7 4.6h-3.4L7.2 1.5a1 1 0 0 0-1.4 1.4l1.7 1.7H6.2A4.2 4.2 0 0 0 2 8.8v7.6a4.2 4.2 0 0 0 4.2 4.2h11.6a4.2 4.2 0 0 0 4.2-4.2V8.8a4.2 4.2 0 0 0-4.2-4.2M8.5 13.9a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6m7 0a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6"/></svg>',
    'site': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.6 2.8 3.8 6 3.8 9.5s-1.2 6.7-3.8 9.5c-2.6-2.8-3.8-6-3.8-9.5S9.4 5.3 12 2.5"/></svg>',
    'paper': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5M8.5 13h7M8.5 17h5"/></svg>',
    'hf': '<svg viewBox="0 0 24 24"><text x="12" y="18" font-size="17" text-anchor="middle">🤗</text></svg>',
}
ICON['doc'] = ICON['paper']
LABEL = {'youtube': 'YouTube', 'x': 'X', 'xhs': '小红书', 'tiktok': 'TikTok', 'bilibili': 'B 站', 'github': 'GitHub',
         'site': '官网', 'paper': '论文', 'hf': 'Hugging Face', 'doc': '文档'}
# 主链接（作品本身）上取哪几项数：(字段, 标签)
STATS = {
    'youtube': [('views', '播放'), ('likes', '点赞')],
    'x': [('views', '浏览'), ('likes', '点赞'), ('bookmarks', '收藏')],
    'xhs': [('likes', '点赞'), ('collects', '收藏'), ('comments', '评论')],
    'bilibili': [('views', '播放'), ('likes', '点赞'), ('favorites', '收藏')],
    'tiktok': [('views', '播放'), ('likes', '点赞'), ('collects', '收藏')],
    'github': [('stars', 'Star'), ('forks', 'Fork')],
}


def fmt(n):
    """数字 → 中文读法：3.5 亿 / 35.3 万 / 3,256"""
    if n >= 1e8:
        return f'{n / 1e8:.1f}'.rstrip('0').rstrip('.') + ' 亿'
    if n >= 1e7:
        return f'{round(n / 1e4)} 万'
    if n >= 1e4:
        return f'{n / 1e4:.1f}'.rstrip('0').rstrip('.') + ' 万'
    return f'{n:,}'


# ---------------------------------------------------------------------------
# 封面

def fetch_bytes(url):
    proxy = CN_PROXY if any(h in url for h in CN_HOSTS) else None
    handlers = [urllib.request.ProxyHandler({'http': proxy, 'https': proxy})] if proxy else []
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://www.xiaohongshu.com/' if proxy else ''})
    with urllib.request.build_opener(*handlers).open(req, timeout=40) as r:
        return r.read()


def video_frame(url, sec, fetch=False):
    """视频第 sec 秒的一帧（X 的视频封面多是片头白屏或标题卡）。

    构建时只读缓存，不联网：代理下远程 seek 一帧可能要几分钟。缓存由 `make_home.py frames` 预先抽好，
    没抽到就返回 None，卡片退回平台缩略图。
    """
    POSTER_CACHE.mkdir(parents=True, exist_ok=True)
    out = POSTER_CACHE / (hashlib.sha1(f'{url}@{sec}'.encode()).hexdigest()[:16] + '.jpg')
    if out.exists() or not fetch:
        return str(out) if out.exists() else None
    try:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(sec), '-i', url, '-frames:v', '1', '-q:v', '3', str(out)],
                       capture_output=True, timeout=900)
    except subprocess.TimeoutExpired:
        pass
    return str(out) if out.exists() else None


def frame_at(card, impact):
    """卡片要不要从视频抽帧：poster 写 'frame:12' 取第 12 秒；X 视频没给封面时默认取 35% 处"""
    links = card.get('links') or []
    m = (impact.get(links[0]['url']) or {}) if links else {}
    src = card.get('poster')
    if not m.get('video'):
        return None, None
    if src and src.startswith('frame:'):
        return m['video'], float(src[6:])
    if not src:
        return m['video'], round((m.get('duration') or 0) * .35, 1)
    return None, None


CLIP_CACHE = CARDS / 'clips'
CLIP_SEC = 6


def clip_src(card, impact):
    """悬停预览的片源：主链接有视频（目前是 X）就截，起点和封面帧一致"""
    m = impact.get(card['links'][0]['url']) or {}
    if not m.get('video'):
        return None, None
    src = card.get('poster') or ''
    start = float(src[6:]) if src.startswith('frame:') else round((m.get('duration') or 0) * .35, 1)
    start = max(0, min(start, (m.get('duration') or 0) - CLIP_SEC))
    return m['video'], start


def clip_path(url, start):
    return CLIP_CACHE / (hashlib.sha1(f'{url}@{start}'.encode()).hexdigest()[:16] + '.mp4')


def clips():
    """截悬停预览：6 秒、无声、640 宽、faststart（慢，可挂后台；构建只读缓存）"""
    data = json.loads(DATA.read_text())
    impact = json.loads(IMPACT.read_text()) if IMPACT.exists() else {}
    CLIP_CACHE.mkdir(parents=True, exist_ok=True)
    for f in data['families']:
        for s in f['scenes']:
            for c in s['cards']:
                url, start = clip_src(c, impact)
                if not url or clip_path(url, start).exists():
                    continue
                t, out = time.time(), clip_path(url, start)
                try:
                    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(start), '-i', url, '-t', str(CLIP_SEC), '-an',
                                    '-vf', 'scale=640:-2', '-c:v', 'libx264', '-crf', '28', '-preset', 'veryfast',
                                    '-movflags', '+faststart', str(out)], capture_output=True, timeout=900)
                except subprocess.TimeoutExpired:
                    out.unlink(missing_ok=True)
                ok = out.exists() and out.stat().st_size > 10000
                if not ok:
                    out.unlink(missing_ok=True)
                print(f'{"ok  " if ok else "FAIL"} {c["title"]:<16} @{start}s  {time.time() - t:.0f}s', flush=True)


XHS_FRAMES = ROOT / 'middle_processing/samples_src/xhs-vibe-video/notes'


def card_reel(card, slug):
    """小红书视频笔记拿不到视频，用爬取时抽的 5 帧在悬停时轮播，当作动态预览"""
    m = re.search(r'explore/([0-9a-f]{24})', card['links'][0]['url'])
    src = sorted((XHS_FRAMES / m.group(1) / 'frames').glob('*.jpg')) if m else []
    if card['links'][0]['kind'] != 'xhs' or not src:
        return ''
    from PIL import Image
    names = []
    for i, f in enumerate(src):
        dst = POSTERS / 'frames' / f'{slug}-{i}.jpg'
        dst.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(f).convert('RGB')
        if im.width > 640:
            im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        im.save(dst, 'JPEG', quality=78, optimize=True)
        names.append(f'assets/showcase/frames/{dst.name}')
    return f'<span class="reel" data-frames="{"|".join(names)}"></span><span class="badge badge-play">▶ 悬停预览</span>'


def card_clip(card, impact, slug):
    """有缓存的预览片拷进 output/assets/showcase/clips/，返回 <video>；没有就空"""
    url, start = clip_src(card, impact)
    if not url or not clip_path(url, start).exists():
        return ''
    dst = POSTERS / 'clips' / f'{slug}.mp4'
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(clip_path(url, start), dst)
    return f'<video muted loop playsinline preload="none" data-src="assets/showcase/clips/{slug}.mp4"></video><span class="badge badge-play">▶ 悬停预览</span>'


def frames():
    """预抽所有卡片要用的视频帧（慢，适合挂后台）"""
    data = json.loads(DATA.read_text())
    impact = json.loads(IMPACT.read_text()) if IMPACT.exists() else {}
    for f in data['families']:
        for s in f['scenes']:
            for c in s['cards']:
                url, sec = frame_at(c, impact)
                if url:
                    t = time.time()
                    ok = video_frame(url, sec, fetch=True)
                    print(f'{"ok  " if ok else "FAIL"} {c["title"]:<16} @{sec}s  {time.time() - t:.0f}s', flush=True)


def poster(src, slug):
    """本地路径或 URL → output/assets/showcase/<slug>.jpg；拿不到返回 None（卡片用渐变占位）"""
    if not src:
        return None
    from PIL import Image
    if re.match(r'https?://', src):
        POSTER_CACHE.mkdir(parents=True, exist_ok=True)
        raw = POSTER_CACHE / (hashlib.sha1(src.encode()).hexdigest()[:16] + '.img')
        if not raw.exists():
            # YouTube 老视频没有 maxres 图，退到 4:3 的 hqdefault（16:9 裁切正好去掉黑边）
            for u in dict.fromkeys([src, src.replace('maxresdefault', 'hqdefault')]):
                try:
                    raw.write_bytes(fetch_bytes(u))
                    break
                except Exception as e:
                    err = e
            else:
                print(f'  [poster] 下载失败 {slug}: {err}')
                return None
    else:
        raw = Path(src)
        if not raw.exists():
            print(f'  [poster] 不存在 {src}')
            return None
    try:
        im = Image.open(raw)
        if getattr(im, 'n_frames', 1) > 1:          # 动图取中间一帧
            im.seek(im.n_frames // 2)
        im = im.convert('RGB')
        if im.width > 640:
            im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        dst = POSTERS / f'{slug}.jpg'
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)
        return f'assets/showcase/{slug}.jpg'
    except Exception as e:
        print(f'  [poster] 读图失败 {slug}: {e}')
        return None


# ---------------------------------------------------------------------------
# 卡片

def stat_items(card, impact):
    """指标栏三格：内容平台的数（第一条有数的链接）打底，附带仓库的 star、biz 里带短值 s 的商业数排在后面"""
    links = card.get('links') or []
    plat = []
    for l in links:
        m = impact.get(l['url']) or {}
        if l.get('third'):                   # 第三方解读 / 实测帖，不代表这张卡自己的传播
            continue
        if l['kind'] != 'github' and any(m.get(k) for k, _ in STATS.get(l['kind'], [])):
            plat = [(fmt(m[k]), lab, l['kind'], '') for k, lab in STATS[l['kind']] if m.get(k)]
            break
    star = []
    gh = None if card.get('oss') is None else next((l for l in links if l['kind'] == 'github' and (impact.get(l['url']) or {}).get('stars')), None)
    if gh:
        name = repo_name(gh['url'])          # 指标栏一格放不下长仓库名，链接按钮上有全名
        own = name.lower() == card['title'].lower()      # 卡片就是这个仓库，不用再写一遍名字
        star.append((fmt(impact[gh['url']]['stars']), f'{name} Star' if len(name) <= 9 and not own else 'GitHub Star', 'github', ''))
    biz = [(b['s'], b['k'], 'biz', b.get('src', '')) for b in card.get('biz') or [] if b.get('s')]
    if card.get('oss') is False:            # 商用产品：营收、估值、用户先上，播放量垫后
        return (biz + star + plat)[:3]
    # 开源项目的 star 就是作品本身的影响力；帖子挂的仓库多是所用框架，不进指标栏（链接按钮上有 ★）
    extra = star + biz if card.get('oss') else biz + star
    if not plat:                            # 主链接取不到数：开源看 star，帖子（如 TikTok）的数在 biz 里
        items = star + biz if card.get('oss') else biz + star
        forks = (impact.get(gh['url']) or {}).get('forks') if gh and len(items) == 1 else None    # 只有一格太空，补 Fork
        return (items + ([(fmt(forks), 'Fork', 'github', '')] if forks else []))[:3]
    # 平台数至少留两格，不够三格时平台数补满
    return (plat[:max(2, 3 - len(extra))] + extra)[:3]


def month_of(m):
    """发布月份 YYYY-MM：X / 小红书存的是 2026-09-23，YouTube 是 Sep 22, 2026"""
    d = m.get('date') or ''
    if re.match(r'\d{4}-\d{2}', d):
        return d[:7]
    try:
        return time.strftime('%Y-%m', time.strptime(d, '%b %d, %Y'))
    except ValueError:
        return ''


def repo_name(url):
    return re.search(r'github\.com/[\w.-]+/([\w.-]+)', url).group(1)


def used_repos(card):
    """卡片用到的仓库（小写名）；not_used 里的是只作参考挂上的，原帖没说用了它"""
    skip = {n.lower() for n in card.get('not_used') or []}
    return {repo_name(l['url']).lower() for l in card.get('links') or [] if l['kind'] == 'github'} - skip


DOMESTIC = ('xhs', 'bilibili', 'douyin')


def tags_of(card):
    """筛选条用的标签：来源（小红书 / 海外）× 性质（开源 / 商用）"""
    links = card.get('links') or [{'kind': 'site'}]
    t = ['xhs' if links[0]['kind'] in DOMESTIC else 'intl']
    t += {True: ['oss'], False: ['biz']}.get(card.get('oss'), [])
    return ' '.join(t)


POSTER_OF = {}        # slug → 封面相对路径，排行榜复用


def card_poster(card, impact, slug):
    """封面：指定的图 / 视频帧，退到主链接缩略图，再退到渐变占位"""
    main = card['links'][0]
    src = card.get('poster')
    url, sec = frame_at(card, impact)
    if url or (src and src.startswith('frame:')):
        src = video_frame(url, sec) if url else None
    img = POSTER_OF[slug] = poster(src or (impact.get(main['url']) or {}).get('thumb'), slug)
    return f'<img src="{img}" alt="" loading="lazy">' if img else f'<span class="ph">{esc(card["title"])}</span>'


def card_badges(card):
    main = card['links'][0]
    src = f'<span class="badge badge-src">{ICON.get(main["kind"], "")}{esc(main.get("label") or LABEL.get(main["kind"], ""))}</span>'
    if card.get('ref'):
        return src + f'<span class="badge badge-kind ref">{esc(card["ref"])}</span>'
    kind = {True: '<span class="badge badge-kind oss">开源</span>', False: '<span class="badge badge-kind biz">商用</span>'}
    return src + kind.get(card.get('oss'), '')


def card_stats(card, tiles):
    """指标栏：平台数带图标；商业数橙色，标签点开是来源，悬停看口径"""
    full = {b['k']: b['v'] for b in card.get('biz') or []}
    plain = {b['k'] for b in card.get('biz') or [] if b.get('plain')}
    out = []
    for v, lab, k, src in tiles:
        # 字号三档：带中文单位的商业数比纯数字宽
        long = ' xlong' if len(v) > 7 else ' long' if len(v) > 6 or (k == 'biz' and len(v) > 4) else ''
        if k == 'biz':
            tag = f'<a href="{esc(src)}" target="_blank" rel="noopener">{esc(lab)} ↗</a>' if src else esc(lab)
            tone = ' plain' if lab in plain else ''      # 成本、售价不是成绩，不用橙色
            out.append(f'<div class="stat biz{long}{tone}" title="{esc(full.get(lab, ""))}"><b>{esc(v)}</b><span>{tag}</span></div>')
        else:
            out.append(f'<div class="stat{long}"><b>{v}</b><span>{ICON.get(k, "")}{esc(lab)}</span></div>')
    return f'<div class="stats">{"".join(out)}</div>' if out else ''


def card_bizs(card, tiles):
    """商业明细：进了指标栏的不重复，其余逐条列出，带来源"""
    shown = {lab for _, lab, k, _ in tiles if k == 'biz'}
    cls = 'bz os' if card.get('oss') else 'bz'
    rows = [f'<div class="{cls}"><i>{esc(b["k"])}</i><span>{esc(b["v"])}'
            + (f' <a href="{esc(b["src"])}" target="_blank" rel="noopener" title="来源">↗</a>' if b.get('src') else '')
            + '</span></div>' for b in card.get('biz') or [] if b['k'] not in shown]
    return f'<div class="bizs">{"".join(rows)}</div>' if rows else ''


def link_metric(l, m):
    """链接按钮上的数：GitHub 写 star，视频平台写播放，X 写浏览，小红书写赞"""
    if l['kind'] == 'github':
        return f'★ {fmt(m["stars"])}' if m.get('stars') else ''
    if l['kind'] in ('youtube', 'bilibili', 'tiktok') and m.get('views'):
        return f'{fmt(m["views"])}播放' + (f' · {fmt(m["likes"])} 赞' if m.get('likes') else '')
    if l['kind'] == 'x' and m.get('views'):
        return f'{fmt(m["views"])}浏览'
    if l['kind'] == 'xhs' and m.get('likes'):
        return f'{fmt(m["likes"])} 赞'
    return ''


def card_links(card, impact, tiles):
    links = card['links']
    # 指标栏已经用了哪条链接的平台数，那条按钮上就不重复标
    used = None
    if any(k not in ('biz', 'github') for _, _, k, _ in tiles):
        used = next((l['url'] for l in links if l['kind'] != 'github' and not l.get('third')
                     and any((impact.get(l['url']) or {}).get(k) for k, _ in STATS.get(l['kind'], []))), None)
    out = []
    for l in links:
        m = impact.get(l['url']) or {}
        num = link_metric(l, m) if l['url'] != used or l['kind'] == 'github' else ''
        label = l.get('label') or (repo_name(l['url']) if l['kind'] == 'github' else LABEL.get(l['kind'], l['kind']))
        out.append(f'<a class="lk" href="{esc(l["url"])}" target="_blank" rel="noopener">{ICON.get(l["kind"], "")}'
                   f'{esc(label)}{f"<em>{num}</em>" if num else ""}</a>')
    return f'<div class="links">{"".join(out)}</div>'


TAG_KINDS = {t: k['key'] for k in json.loads(TAXONOMY.read_text())['kinds'] for t in k['tags']}


def tag(t):
    return f'<span class="tg tg-{TAG_KINDS[t]}">{esc(t)}</span>'


def render_taxonomy():
    """页面底部的标签词表：既是色标图例，也是规范"""
    kinds = json.loads(TAXONOMY.read_text())['kinds']
    rows = ''.join(f'<tr><th>{esc(k["label"])}</th><td>{esc(k["desc"])}</td><td class="tax-tags">{"".join(tag(t) for t in k["tags"])}</td></tr>' for k in kinds)
    return f'''  <section class="tax">
    <p><b>标签词表</b>：Application 的卡片共用 {len(kinds)} 类标签，颜色即类别。</p>
    <table class="tbl"><thead><tr><th>类别</th><th>含义</th><th>标签（共 {len(TAG_KINDS)} 个）</th></tr></thead><tbody>{rows}</tbody></table>
  </section>'''


def render_card(card, impact, slug, size='', top=''):
    main = card['links'][0]
    tiles = stat_items(card, impact)
    # 作者 · 发布月份（GitHub 只有建仓日期，不算发布时间）
    month = month_of(impact.get(main['url']) or {}) if main['kind'] != 'github' else ''
    by = ' · '.join(x for x in [esc(card.get('by') or ''), month] if x)
    repos = ' '.join(sorted(used_repos(card)))
    if card.get('ref') or card.get('oss') is False or main['kind'] == 'github':
        repos = ''                  # 和「按框架看作品」清单一致：人写对照、产品、框架自己都不算作品
    return f'''<article class="card{size}" id="c-{slug}" data-f="{tags_of(card)}{' top' if top else ''}"{f' data-top="{top}"' if top else ''} data-repo="{esc(repos)}">
  <a class="poster" href="{esc(main['url'])}" target="_blank" rel="noopener">{card_poster(card, impact, slug)}{card_clip(card, impact, slug) or card_reel(card, slug)}{card_badges(card)}</a>
  <div class="body">
    <h5 class="title">{esc(card['title'])}{f'<span class="by">{by}</span>' if by else ''}</h5>
    <div class="core">{''.join(tag(c) for c in card['core'])}</div>
    <p class="line">{esc(card.get('line') or '')}</p>
    {f'<p class="why"><b>入选理由</b>{esc(card["why"])}</p>' if card.get('why') else ''}
    {card_stats(card, tiles)}
    {card_bizs(card, tiles)}
    {card_links(card, impact, tiles)}
  </div>
</article>'''


def reach_of(card, impact):
    """传播量：第一条有播放 / 浏览数的链接"""
    for l in card.get('links') or []:
        v = (impact.get(l['url']) or {}).get('views')
        if v:
            return v, f'{LABEL[l["kind"]]} {"浏览" if l["kind"] == "x" else "播放"}'
    return 0, ''


def board(title, sub, rows, rev=False):
    """rows: (数值, 显示值, 口径, 卡片, slug, 家族)"""
    top = max(r[0] for r in rows)
    lis = ''.join(
        f'<li><a href="#c-{slug}" data-jump="c-{slug}" style="--fc:{fam["color"]};--w:{v / top * 100:.0f}%">'
        f'<span class="rk">{i}</span>'
        + (f'<img src="{POSTER_OF[slug]}" alt="" loading="lazy">' if POSTER_OF.get(slug) else '<i class="noimg"></i>')
        + f'<span class="bt"><b>{esc((c.get("rev") or {}).get("name") if rev else c["title"])}</b>'
          f'<small>{esc(fam["en"])} · {esc(c["title"] if rev else c.get("by", ""))}</small></span>'
        f'<span class="bv"><b>{esc(shown)}</b><small>{esc(note)}</small></span></a></li>'
        for i, (v, shown, note, c, slug, fam) in enumerate(rows, 1))
    return f'<section class="board"><h3>{title}<small>{sub}</small></h3><ol>{lis}</ol></section>'


def render_boards(data, impact):
    cards = [(c, f'{f["key"]}-{s["key"]}-{i}', f) for f in data['families'] for s in f['scenes'] for i, c in enumerate(s['cards'])]
    reach = sorted(((*reach_of(c, impact), c, slug, f) for c, slug, f in cards if not c.get('ref')), key=lambda r: -r[0])[:5]
    reach = [(v, fmt(v), note, c, slug, f) for v, note, c, slug, f in reach]
    rev = sorted(((c['rev']['usd'], c['rev']['v'], c['rev']['k'], c, slug, f) for c, slug, f in cards if c.get('rev')),
                 key=lambda r: -r[0])[:5]
    # 小红书热度：主链接是小红书的帖子按点赞排，收藏写在口径里
    xhs = []
    for c, slug, f in cards:
        m = impact.get(c['links'][0]['url']) or {}
        if c['links'][0]['kind'] == 'xhs' and m.get('likes') and not c.get('ref'):
            xhs.append((m['likes'], fmt(m['likes']), f'赞 · 藏 {fmt(m.get("collects") or 0)}', c, slug, f))
    xhs.sort(key=lambda r: -r[0])
    return ('<div class="boards">' + board('海外传播 Top 5', '作品或官方视频的播放 / 浏览', reach)
            + board('小红书 Top 5', '国内普通用户的点赞', xhs[:5])
            + (board('公司营收 Top 5', '案例背后公司的整体年化收入', rev, rev=True) if rev else '') + '</div>')


FILTERS = [('top', '精选'), ('all', '全部'), ('xhs', '小红书'), ('intl', '海外'), ('oss', '开源'), ('biz', '商用')]


def reach_key(m):
    """作品清单排序：有播放 / 浏览的一组排前面，只有赞的（小红书）一组排后面，组内各按自己的数"""
    return (1, m['views']) if m.get('views') else (0, m.get('likes') or 0)


def work_row(url, title, by, impact, stat=None, jump=None):
    m = impact.get(url) or {}
    if not stat and not (m.get('views') or m.get('likes')):
        stat = {'v': '—', 'k': ''}
    kind = next((k for pat, k in [('youtube', 'youtube'), ('x.com', 'x'), ('xiaohongshu', 'xhs'), ('tiktok', 'tiktok')] if pat in url), 'site')
    if stat:
        v, k = stat['v'], stat['k']
    elif m.get('views'):
        v, k = fmt(m['views']), '浏览' if kind == 'x' else '播放'
    else:
        v, k = fmt(m.get('likes') or 0), '赞'
    go = f'<a class="fw-jump" href="#{jump}" data-jump="{jump}">卡片 ↓</a>' if jump else ''
    row = (f'<li>{ICON.get(kind, "")}<span class="fw-t"><b>{esc(title)}</b><small>{esc(by)}</small></span>'
           f'<span class="fw-v"><b>{v}</b><small>{k}</small></span>{go}'
           f'<a class="fw-out" href="{esc(url)}" target="_blank" rel="noopener">↗</a></li>')
    return reach_key(m), row


def framework_bar(fam, impact):
    """按框架看作品：每个框架一个按钮（star · N 件），点开是作品清单，卡片里的作品同时高亮"""
    fws = json.loads(FRAMEWORKS.read_text())['frameworks']
    pills, panels = [], []
    for fw in fws:
        rows = []
        for s in fam['scenes']:
            for i, c in enumerate(s['cards']):
                repos = used_repos(c)
                main = c['links'][0]
                if (main['kind'] == 'github' and repo_name(main['url']).lower() in fw['match']) or c.get('ref') or c.get('oss') is False:
                    continue                # 框架自己那张卡、人写对照卡、产品卡都不算「作品」
                if repos & set(fw['match']):
                    biz = next(({'v': b['s'], 'k': b['k']} for b in c.get('biz') or [] if b.get('s')), None)
                    m = impact.get(main['url']) or {}
                    rows.append(work_row(main['url'], c['title'], c.get('by', ''), impact,
                                         stat=None if (m.get('views') or m.get('likes')) else biz,
                                         jump=f'c-{fam["key"]}-{s["key"]}-{i}'))
        rows += [work_row(w['url'], w['title'], w['by'], impact, stat=w.get('stat')) for w in fw['works']]
        rows.sort(key=lambda r: r[0], reverse=True)
        key = fw['match'][0]
        star = (impact.get(fw['repo']) or {}).get('stars') or 0
        pills.append(f'<button data-fw="{esc(" ".join(fw["match"]))}" data-fwp="{esc(key)}">{ICON["github"]}{esc(fw["name"])}'
                     f'<em>★ {fmt(star)}</em><i>{len(rows)} 件</i></button>')
        biz = ''.join(f'<a class="fw-biz" href="{esc(b["src"])}" target="_blank" rel="noopener"><b>{esc(b["s"])}</b>{esc(b["k"])} ↗</a>' for b in fw.get('biz') or [])
        panels.append(f'<div class="fw-panel" data-fwp="{esc(key)}" hidden><ol>{"".join(r for _, r in rows)}</ol>'
                      f'<div class="fw-foot"><a class="fw-repo" href="{esc(fw["repo"])}" target="_blank" rel="noopener">{ICON["github"]}{esc(repo_name(fw["repo"]))} ↗</a>{biz}</div></div>')
    return f'<div class="fw-bar"><span>按框架看作品</span>{"".join(pills)}</div>{"".join(panels)}'


def top_picks(cards, impact):
    """精选视角：编辑首选（场景第一张），再配另一来源（小红书 / 海外）里数据最好的一张"""
    origin = lambda c: c['links'][0]['kind'] in DOMESTIC
    def score(c):                   # 小红书看赞，海外看播放 / 浏览
        m = impact.get(c['links'][0]['url']) or {}
        return m.get('likes') if origin(c) else m.get('views') or 0
    others = [i for i, c in enumerate(cards) if origin(c) != origin(cards[0]) and not c.get('ref')]
    return [0] + ([max(others, key=lambda i: score(cards[i]) or 0)] if others else [])


def proof_tile(f, s, title, label, impact):
    """代表数据的一格：缩略图 + 标题 + 数字，点了跳到下方那张卡"""
    i, card = next((i, c) for i, c in enumerate(s['cards']) if c['title'] == title)
    slug = f'{f["key"]}-{s["key"]}-{i}'
    tiles = stat_items(card, impact)
    v, lab, kind, _ = next((t for t in tiles if t[1] == label), tiles[0])
    note = f'{LABEL[kind]} {lab}' if kind in STATS and kind != 'github' else lab
    return (f'<a class="pf" href="#c-{slug}" data-jump="c-{slug}" style="--fc:{f["color"]}"><img src="{POSTER_OF[slug]}" alt="" loading="lazy">'
            f'<span><b>{esc(title)}</b><small><em>{esc(v)}</em> {esc(note)}</small></span></a>')


def render_summary(fams, impact):
    """场景总表：三类能力合成一张，第一列合并单元格，放在大图卡上方"""
    rows = []
    for f in fams:
        for i, s in enumerate(f['scenes']):
            fam = (f'<th rowspan="{len(f["scenes"])}"><a href="#fam-{f["key"]}" data-go="overview/fam-{f["key"]}" style="color:{f["color"]}">{esc(f["en"])}</a></th>'
                   if i == 0 else '')
            go = f'sc-{f["key"]}-{s["key"]}'
            rows.append(f'<tr>{fam}<td class="sum-sc"><a href="#{go}" data-go="overview/{go}">{esc(s["cn"])}</a><i>{len(s["cards"])}</i></td>'
                        f'<td>{esc(s["payer"])}</td><td>{esc(s["revenue"])}</td>'
                        f'<td class="sum-proof" title="{esc(s["proof"])}"><div class="pf-row">'
                        + ''.join(proof_tile(f, s, t, lab, impact) for t, lab in s['picks']) + '</div></td></tr>')
    return ('<div class="sum-wrap"><table class="tbl sum-tbl"><thead><tr><th>能力</th><th>场景</th><th>谁在付费</th><th>变现方式</th><th>代表数据</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def render_picks(fams):
    """分组大图卡：图就是入口，点哪张看哪组。封面取 cover 指向的那张卡，小字取 desc 冒号前的结论"""
    out = []
    for f in fams:
        slug = next(f'{f["key"]}-{s["key"]}-{i}' for s in f['scenes'] for i, c in enumerate(s['cards']) if c['title'] == f['cover'])
        out.append(f'<button class="pick" data-fam="{f["key"]}" style="--fc:{f["color"]}"><img src="{POSTER_OF[slug]}" alt="">'
                   f'<span><b>{esc(f["en"])}</b><small>{esc(f["desc"].partition("：")[0])}</small></span></button>')
    return f'<div class="picks">{"".join(out)}</div>'


def render_overview(data, impact):
    fams = data['families']
    tip = {'top': ' title="每个场景：编辑首选一张，再配另一来源（小红书 / 海外）里数据最好的一张"'}
    filt = ''.join(f'<button data-filter="{k}"{" class=on" if k == "all" else ""}{tip.get(k, "")}>{v}</button>' for k, v in FILTERS)
    out = []
    for f in fams:
        out.append(f'''  <section class="fam" id="fam-{f['key']}" style="--fc:{f['color']}">
    {framework_bar(f, impact) if f.get('frameworks') else ''}''')
        for s in f['scenes']:
            lead = len(s['cards']) % 3          # 三列网格排不满的那几张放大到最前面，不留孤卡
            size = {1: [' wide'], 2: [' half', ' half']}.get(lead, [])
            tops = top_picks(s['cards'], impact)
            cards = '\n'.join(render_card(c, impact, f'{f["key"]}-{s["key"]}-{i}', size[i] if i < len(size) else '',
                                           top=('solo' if len(tops) == 1 else 'pair') if i in tops else '')
                              for i, c in enumerate(s['cards']))
            out.append(f'''    <div class="scene" id="sc-{f['key']}-{s['key']}">
      <div class="scene-head"><h4>{esc(s['cn'])}{f'<em>{esc(s["tag"])}</em>' if s.get('tag') else ''}<i>{len(s['cards'])}</i></h4><p>{esc(s.get('desc', ''))}{f' <a class="scene-src" href="{esc(s["src"]["url"])}" target="_blank" rel="noopener">{esc(s["src"]["label"])} ↗</a>' if s.get('src') else ''}</p></div>
      <div class="grid">
{cards}
      </div>
    </div>''')
        out.append('  </section>')
    out.append(render_taxonomy())
    out.append('</div>')
    head = f'''<div class="ov">
  <h2 class="ov-title">Application</h2>
  {render_boards(data, impact)}
  {render_summary(fams, impact)}
  {render_picks(fams)}
  <div class="filters"><span>筛选</span>{filt}<button class="why-toggle" aria-pressed="false" title="理由里的数字是选卡时记录的，以卡片上的实时数为准">显示入选理由</button></div>'''
    return '\n'.join([head] + out)


# ---------------------------------------------------------------------------

def merge():
    data = json.loads(DATA.read_text())
    for f in data['families']:
        src = CARDS / f'cards_{f["key"]}.json'
        if src.exists():
            f['scenes'] = json.loads(src.read_text())['scenes']
            print(f'{f["key"]:<8} {len(f["scenes"])} 个场景 {sum(len(s["cards"]) for s in f["scenes"])} 张卡')
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1))


def build():
    data = json.loads(DATA.read_text())
    impact = json.loads(IMPACT.read_text()) if IMPACT.exists() else {}
    shutil.rmtree(POSTERS, ignore_errors=True)
    fetched = sorted({m.get('fetched') for m in impact.values() if m.get('fetched')})
    date = fetched[-1] if fetched else time.strftime('%Y-%m-%d')
    page = (TEMPLATE.read_text()
            .replace('__OVERVIEW__', render_overview(data, impact))
            .replace('__BENCH__', html.escape((ROOT / 'assets/figures/header-bench.html').read_text(), quote=True))   # 开头 benchmark 图，见 make_bench_charts.py
            .replace('__UPDATED_DATE__', date)
            .replace('__UPDATED__', f'Snapshot {date}')
            .replace('__SHELL__', json.dumps(SHELL.read_text(), ensure_ascii=False).replace('</', r'<\/')))
    n = sum(len(s['cards']) for f in data['families'] for s in f['scenes'])
    (OUT / 'total.html').write_text(page)
    print(f'[write] output/total.html  {n} 张卡  {len(page) // 1024} KB')


def refresh():
    """一条龙：合并 → 审稿 → 取数（只刷新超过 1 天的）→ 抽帧 → 截片 → 出页"""
    py = sys.executable
    merge()
    subprocess.run([py, str(CARDS / 'curate.py')], check=True)
    subprocess.run([py, str(ROOT / 'scripts/fetch_impact.py'), '--all', '--stale', '1'], check=True)
    frames()
    clips()
    build()


if __name__ == '__main__':
    {'merge': merge, 'frames': frames, 'clips': clips, 'refresh': refresh}.get(sys.argv[1] if sys.argv[1:] else '', build)()

