#!/usr/bin/env python3
"""首页 Showcase 卡片的影响力指标：按链接拉播放、点赞、star，缓存进 data/showcase_impact.json。

  python3 scripts/fetch_impact.py <url> ...     # 抓这几条，打印结果并写缓存
  python3 scripts/fetch_impact.py --all         # 刷新 data/showcase.json 里所有卡片的链接
  python3 scripts/fetch_impact.py --all --stale 7   # 只刷新 7 天前抓的

各平台的取法（都不用登录）：
  YouTube   youtubei/v1/player 取播放量与标题，youtubei/v1/next 取点赞数与日期
  X         api.fxtwitter.com 取点赞、浏览、转发、收藏
  TikTok    视频页 HTML 内嵌的 __UNIVERSAL_DATA_FOR_REHYDRATION__ 取播放、点赞、收藏
  GitHub    api.github.com/repos（有 GITHUB_TOKEN 就带上，没有每小时 60 次）
  B 站      api.bilibili.com/x/web-interface/view
  小红书    不联网，读已爬好的笔记：v1 的 market/xhs/notes、v2 的 samples_src/xhs-vibe-video/notes
"""
import fcntl
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get('IMPACT_CACHE') or ROOT / 'data/showcase_impact.json')   # 并行跑时各写各的
SHOWCASE = ROOT / 'data/showcase.json'
V1_XHS = ROOT / 'middle_processing/market/xhs'
XHS_DIRS = [
    V1_XHS / 'notes',                                                          # <id>.json
    ROOT / 'middle_processing/samples_src/xhs-vibe-video/notes',              # <id>/note.json
]
CN_PROXY = 'http://10.68.24.18:11080'      # 国内站（B 站）走国内代理，海外出口会被 412
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
YT_CLIENT = {'client': {'clientName': 'WEB', 'clientVersion': '2.20251001.00.00', 'hl': 'en'}}


def http(url, data=None, headers=None, timeout=40, proxy=None):
    h = {'User-Agent': UA, **(headers or {})}
    if data is not None:
        data = json.dumps(data).encode()
        h['Content-Type'] = 'application/json'
    opener = urllib.request.build_opener(*([urllib.request.ProxyHandler({'http': proxy, 'https': proxy})] if proxy else []))
    with opener.open(urllib.request.Request(url, data=data, headers=h), timeout=timeout) as r:
        return r.read().decode('utf-8', 'ignore')


def num(v):
    """'1.2万' / '11.1K' / '6,302' / 407 → int"""
    m = re.match(r'([\d.,]+)\s*([万wWkKmM]?)', str(v or '0').strip())
    if not m:
        return 0
    n = float(m.group(1).replace(',', ''))
    return int(n * {'万': 1e4, 'w': 1e4, 'W': 1e4, 'k': 1e3, 'K': 1e3, 'm': 1e6, 'M': 1e6}.get(m.group(2), 1))


# ---------------------------------------------------------------------------
# 各平台

def youtube(url):
    vid = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})', url).group(1)
    body = {'videoId': vid, 'context': YT_CLIENT}
    p = json.loads(http('https://www.youtube.com/youtubei/v1/player?prettyPrint=false', body)).get('videoDetails', {})
    nxt = http('https://www.youtube.com/youtubei/v1/next?prettyPrint=false', body)
    likes = re.search(r'like this video along with ([\d,]+) other', nxt)
    date = re.search(r'"dateText":\{"simpleText":"([^"]+)"', nxt)
    return {'platform': 'youtube', 'title': p.get('title'), 'author': p.get('author'),
            'views': int(p.get('viewCount') or 0), 'likes': num(likes.group(1)) if likes else None,
            'date': date.group(1) if date else None,
            'thumb': f'https://i.ytimg.com/vi/{vid}/maxresdefault.jpg'}


def x(url):
    m = re.search(r'(?:x|twitter)\.com/(\w+)/status/(\d+)', url)
    t = json.loads(http(f'https://api.fxtwitter.com/{m.group(1)}/status/{m.group(2)}'))['tweet']
    media = (t.get('media') or {}).get('all') or [{}]
    video = ((t.get('media') or {}).get('videos') or [{}])[0]
    # 只拿来抽封面：取码率 ≥ 0.8 Mbps 里最小的一档（约 852 宽），原画质动辄十几 MB，代理下载很慢
    mp4s = sorted((f for f in video.get('formats') or [] if f.get('container') == 'mp4'), key=lambda f: f.get('bitrate') or 0)
    video['url'] = next((f['url'] for f in mp4s if (f.get('bitrate') or 0) >= 800000), video.get('url'))
    return {'platform': 'x', 'title': (t.get('text') or '')[:140], 'author': t['author']['screen_name'],
            'video': video.get('url'), 'duration': video.get('duration'),
            'followers': t['author'].get('followers'), 'views': t.get('views'), 'likes': t.get('likes'),
            'reposts': t.get('retweets'), 'bookmarks': t.get('bookmarks'),
            'date': time.strftime('%Y-%m-%d', time.strptime(t['created_at'], '%a %b %d %H:%M:%S %z %Y')),
            'thumb': media[0].get('thumbnail_url') or media[0].get('url')}


def github(url):
    repo = re.search(r'github\.com/([\w.-]+/[\w.-]+)', url).group(1).removesuffix('.git')
    tok = os.environ.get('GITHUB_TOKEN')
    d = json.loads(http(f'https://api.github.com/repos/{repo}', headers={'Authorization': f'Bearer {tok}'} if tok else None))
    return {'platform': 'github', 'title': d['full_name'], 'author': d['owner']['login'],
            'stars': d['stargazers_count'], 'forks': d['forks_count'], 'desc': d.get('description'),
            'homepage': d.get('homepage'), 'license': (d.get('license') or {}).get('spdx_id'),
            'date': d['created_at'][:10], 'thumb': f'https://opengraph.githubassets.com/1/{repo}'}


def tiktok(url):
    """视频页 HTML 里内嵌的 __UNIVERSAL_DATA_FOR_REHYDRATION__ 带全量统计，不用登录"""
    html = http(url, headers={'Accept-Language': 'en-US,en;q=0.9'}, timeout=60)
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    item = json.loads(m.group(1))['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']
    st = item['stats']
    return {'platform': 'tiktok', 'title': (item.get('desc') or '')[:140], 'author': item['author']['uniqueId'],
            'views': num(st.get('playCount')), 'likes': num(st.get('diggCount')),
            'collects': num(st.get('collectCount')), 'comments': num(st.get('commentCount')),
            'date': time.strftime('%Y-%m-%d', time.localtime(int(item['createTime']))),
            'thumb': (item.get('video') or {}).get('cover')}


def bilibili(url):
    bv = re.search(r'(BV\w{10})', url).group(1)
    d = json.loads(http(f'https://api.bilibili.com/x/web-interface/view?bvid={bv}',
                        headers={'Referer': 'https://www.bilibili.com/'}, proxy=CN_PROXY))['data']
    return {'platform': 'bilibili', 'title': d['title'], 'author': d['owner']['name'],
            'views': d['stat']['view'], 'likes': d['stat']['like'], 'favorites': d['stat']['favorite'],
            'date': time.strftime('%Y-%m-%d', time.localtime(d['pubdate'])), 'thumb': d['pic']}


def xhs(url):
    nid = re.search(r'(?:explore|discovery/item|item)/([0-9a-f]{24})', url).group(1)
    for d in XHS_DIRS:
        for f in (d / f'{nid}.json', d / nid / 'note.json'):
            if f.exists():
                n = json.loads(f.read_text())
                imgs = sorted((f.parent / 'images').glob('*.jpg')) if f.name == 'note.json' else []
                v1_cover = ROOT / f'assets/market/xhs-{nid}.jpg'
                cover = str(imgs[0]) if imgs else (str(v1_cover) if v1_cover.exists() else None)
                c = n.get('comments_count', n.get('comments'))      # v2 存评论列表 + 计数，v1 只存计数
                return {'platform': 'xhs', 'title': n.get('title'), 'author': n.get('author'),
                        'likes': num(n.get('likes')), 'collects': num(n.get('collects')),
                        'comments': len(c) if isinstance(c, list) else num(c),
                        'date': time.strftime('%Y-%m-%d', time.localtime(n['time'] / 1000)) if n.get('time') else None,
                        'thumb': cover}
    # 没抓详情的笔记，退到搜索结果里的赞藏数（v1 notes.tsv、v2 index.json）
    for line in (V1_XHS / 'notes.tsv').read_text().splitlines()[1:]:
        f = line.split('\t')
        if f[2] == nid:
            return {'platform': 'xhs', 'title': f[8], 'author': f[7], 'likes': num(f[4]),
                    'collects': num(f[5]), 'comments': num(f[6]), 'date': None, 'thumb': None}
    for n in json.loads((XHS_DIRS[1].parent / 'index.json').read_text()):
        if n['id'] == nid:
            return {'platform': 'xhs', 'title': n['title'], 'author': n['author'], 'likes': n['likes'],
                    'collects': None, 'comments': None, 'date': None, 'thumb': None}
    raise LookupError(f'小红书笔记 {nid} 不在本地爬取数据里')


HANDLERS = [
    (r'youtube\.com/(watch|shorts)|youtu\.be/', youtube),
    (r'(x|twitter)\.com/\w+/status/', x),
    (r'github\.com/[\w.-]+/[\w.-]+', github),
    (r'bilibili\.com/video/BV', bilibili),
    (r'tiktok\.com/@[\w.]+/video/\d+', tiktok),
    (r'xiaohongshu\.com/', xhs),
]


def fetch(url, tries=3):
    for pat, fn in HANDLERS:
        if re.search(pat, url):
            for i in range(tries):            # 代理偶发超时，退避重试
                try:
                    return fn(url)
                except (TimeoutError, OSError) as e:
                    if i == tries - 1 or getattr(e, 'code', None) in (403, 404):
                        raise
                    time.sleep(3 * (i + 1))
    return None


# ---------------------------------------------------------------------------

def card_urls():
    data = json.loads(SHOWCASE.read_text())
    urls = [l['url'] for fam in data['families'] for sc in fam['scenes'] for c in sc['cards'] for l in c.get('links', [])]
    fws = ROOT / 'data/framework_works.json'
    if fws.exists():
        urls += [u for fw in json.loads(fws.read_text())['frameworks'] for u in [fw['repo']] + [w['url'] for w in fw['works']]]
    return urls


def main(argv):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    stale = float(argv[argv.index('--stale') + 1]) if '--stale' in argv else 0
    urls = card_urls() if '--all' in argv else [a for a in argv if a.startswith('http')]
    for url in dict.fromkeys(urls):
        old = cache.get(url)
        if old and stale and time.time() - old.get('ts', 0) < stale * 86400:
            continue
        try:
            r = fetch(url)
        except Exception as e:
            print(f'[fail] {url}  {type(e).__name__}: {e}')
            continue
        if r is None:
            continue
        r.update(fetched=time.strftime('%Y-%m-%d'), ts=int(time.time()))
        cache[url] = r
        print(json.dumps({'url': url, **{k: v for k, v in r.items() if k not in ('thumb', 'ts', 'video')}}, ensure_ascii=False))
        save(url, r)


def save(url, r):
    """加锁后重读、合并、原子替换：几个进程同时写同一份缓存也不会互相冲掉"""
    with open(CACHE.parent / f'.{CACHE.name}.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        cur = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        cur[url] = r
        tmp = CACHE.with_suffix('.tmp')
        tmp.write_text(json.dumps(cur, ensure_ascii=False, indent=1))
        os.replace(tmp, CACHE)


if __name__ == '__main__':
    main(sys.argv[1:])

