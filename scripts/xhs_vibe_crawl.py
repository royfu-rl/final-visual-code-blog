#!/usr/bin/env python3
"""Video 章 Vibe Video：从小红书爬「用 Claude / Agent 写代码出片」的笔记。

三步：
  search  带登录 Cookie 开桌面版搜索页，截获 search/notes 接口的返回（标题、作者、点赞、xsec_token）
  fetch   按热度挑笔记，带 Cookie 开桌面版详情页取正文，图片用 xhs-fetcher skill 的函数下载
  frames  视频笔记抽几帧当示例图
  sheets  每条笔记拼一张总览图，读笔记时一条看一张

产物默认在 middle_processing/samples_src/xhs-vibe-video/（环境变量 XHS_VIBE_OUT 可改）：
  search/<关键词>.json   每个关键词的原始搜索结果
  index.json             去重合并，带命中关键词与点赞数
  notes/<note_id>/       note.json、note.md、images/、frames/（视频笔记抽帧）

用法（Cookie 只从文件读，不进项目目录）：
  python3 scripts/xhs_vibe_crawl.py search --cookie <cookie 文件>
  python3 scripts/xhs_vibe_crawl.py fetch  --cookie <cookie 文件> --top 150 [--min-likes 50]
  python3 scripts/xhs_vibe_crawl.py frames --cookie <cookie 文件> <note_id> ...
"""
import argparse
import asyncio
import importlib.util
import json
import os
import random
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('XHS_VIBE_OUT') or ROOT / 'middle_processing/samples_src/xhs-vibe-video')
SKILL = Path('/mmu_mllm_hdd_4/infra/skills/xhs-fetcher/scripts/xhs_fetch.py')
PROXY = 'http://10.68.24.18:11080'
DESKTOP_UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')

KEYWORDS = [
    # 总称
    'Opus5.5 做视频', 'Claude 做视频', 'Claude Code 做视频', 'vibe video', '纯代码视频', '代码生成视频',
    'AI 写代码做动画', 'Codex 做视频',
    # 工具与项目
    'Remotion', 'HyperFrames', 'Hypit 视频', 'Motion Canvas', 'opuscar', '视频 skill', 'Higgsfield Claude',
    # 场景
    'Claude 产品宣传片', 'Claude MV', 'Claude 科普动画', 'manim AI 动画', 'Claude 3D 动画',
    'Claude 数据可视化动画', 'Claude 片头动画', 'Claude 口播视频', 'Claude 动效设计', 'Claude Blender 动画',
]

NOTE_JS = """() => {
  const m = (((window.__INITIAL_STATE__ || {}).note || {}).noteDetailMap) || {};
  for (const k in m) if (m[k].note && m[k].note.noteId) return JSON.parse(JSON.stringify(m[k].note));
  return null;
}"""


def likes(v):
    """'1.2万' / '999' / '' → int"""
    m = re.match(r'([\d.]+)\s*([万wW]?)', str(v or '0').strip())
    return int(float(m.group(1)) * (10000 if m.group(2) else 1)) if m else 0


def video_urls(note):
    """stream 下的分组名会变（h264/h265 → EF4/EF5…），不认名字，全收；按分辨率从小到大，抽帧只要够看"""
    streams = [it for x in (((note.get('video') or {}).get('media') or {}).get('stream') or {}).values() for it in x or []]
    streams.sort(key=lambda it: int(it.get('height') or 0))
    return [u for it in streams for u in [it.get('masterUrl'), *(it.get('backupUrls') or [])] if u]


def load_cookies(path):
    out = []
    for kv in Path(path).read_text().strip().split(';'):
        k, _, v = kv.partition('=')
        if k.strip():
            out.append({'name': k.strip(), 'value': v.strip(), 'domain': '.xiaohongshu.com', 'path': '/'})
    return out


def load_skill():
    spec = importlib.util.spec_from_file_location('xhs_fetch', SKILL)
    xf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(xf)
    get = xf.get
    xf.get = lambda op, url, timeout=60: get(op, url, min(timeout, 30))   # skill 下载默认等 300 秒，单张卡住会拖住整批
    return xf


async def browser(p, cookie_file):
    b = await p.chromium.launch(proxy={'server': PROXY})
    ctx = await b.new_context(viewport={'width': 1400, 'height': 1000}, locale='zh-CN', user_agent=DESKTOP_UA)
    await ctx.add_cookies(load_cookies(cookie_file))
    return b, ctx


async def search(cookie_file, pages):
    from playwright.async_api import async_playwright
    (OUT / 'search').mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b, ctx = await browser(p, cookie_file)
        for kw in KEYWORDS:
            dst = OUT / 'search' / f'{kw}.json'
            if dst.exists():
                continue
            pg = await ctx.new_page()
            got = []

            async def on_resp(r):
                if 'search/notes' in r.url:
                    try:
                        got.append(await r.json())
                    except Exception:
                        pass
            pg.on('response', on_resp)
            await pg.goto(f'https://www.xiaohongshu.com/search_result?keyword={quote(kw)}&source=web_explore_feed&type=51',
                          timeout=60000)
            await pg.wait_for_timeout(4000)
            for _ in range(pages - 1):            # 滚到底触发下一页
                await pg.mouse.wheel(0, 20000)
                await pg.wait_for_timeout(3000 + random.randint(0, 2000))
            items = [it for g in got for it in (g.get('data') or {}).get('items') or [] if it.get('model_type') == 'note']
            dst.write_text(json.dumps(items, ensure_ascii=False, indent=1))
            print(f'{kw:<20} {len(items)} 条')
            await pg.close()
            await asyncio.sleep(3 + random.random() * 3)
        await b.close()

    index = {}
    for f in sorted((OUT / 'search').glob('*.json')):
        for it in json.loads(f.read_text()):
            nc = it.get('note_card') or {}
            rec = index.setdefault(it['id'], {
                'id': it['id'], 'xsec_token': it.get('xsec_token'), 'title': nc.get('display_title'),
                'author': (nc.get('user') or {}).get('nickname'), 'type': nc.get('type'),
                'likes': likes((nc.get('interact_info') or {}).get('liked_count')), 'keywords': []})
            rec['keywords'].append(f.stem)
    rows = sorted(index.values(), key=lambda r: -r['likes'])
    (OUT / 'index.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f'去重后 {len(rows)} 条 → {OUT / "index.json"}')


async def fetch(cookie_file, top, min_likes, ids):
    """手机 UA 免登录抓几条就会落登录墙，所以带 Cookie 开桌面版详情页，从 __INITIAL_STATE__ 取笔记。"""
    from playwright.async_api import async_playwright
    xf = load_skill()
    op = xf.opener(PROXY)
    rows = json.loads((OUT / 'index.json').read_text())
    rows = [r for r in rows if r['id'] in ids] if ids else [r for r in rows if r['likes'] >= min_likes][:top]
    async with async_playwright() as p:
        b, ctx = await browser(p, cookie_file)
        pg = await ctx.new_page()
        comments = []

        async def on_resp(r):
            if 'comment/page' in r.url:
                try:
                    comments.extend(((await r.json()).get('data') or {}).get('comments') or [])
                except Exception:
                    pass
        pg.on('response', on_resp)
        for i, r in enumerate(rows):
            d = OUT / 'notes' / r['id']
            if (d / 'note.json').exists():
                continue
            url = f'https://www.xiaohongshu.com/explore/{r["id"]}?xsec_token={r["xsec_token"]}&xsec_source=pc_search'
            comments.clear()
            try:
                await pg.goto(url, timeout=60000)
                await pg.wait_for_timeout(2500)
                note = await pg.evaluate(NOTE_JS)
            except Exception as e:
                note = None
                print(f'[{i}] {r["id"]} 打开失败 {e}')
            if not note:
                print(f'[{i}] {r["id"]} 没取到笔记（风控 / 已删）')
                continue
            info = note.get('interactInfo') or {}
            images = [im.get('urlDefault') or im.get('url') for im in note.get('imageList') or []][:12]
            rec = {
                'note_id': r['id'], 'url': url, 'type': note.get('type'), 'title': note.get('title'),
                'desc': note.get('desc'), 'tags': [t.get('name') for t in note.get('tagList') or []],
                'author': (note.get('user') or {}).get('nickname'), 'user_id': (note.get('user') or {}).get('userId'),
                'time': note.get('time'), 'ip_location': note.get('ipLocation'),
                'likes': info.get('likedCount'), 'collects': info.get('collectedCount'),
                'comments_count': info.get('commentCount'), 'keywords': r['keywords'],
                'duration': ((note.get('video') or {}).get('capa') or {}).get('duration'),
                'images': images,
                'comments': [{'user': (c.get('user_info') or {}).get('nickname'), 'content': c.get('content'),
                              'likes': c.get('like_count')} for c in comments[:15]],
            }
            (d / 'images').mkdir(parents=True, exist_ok=True)
            rec['image_files'] = []
            for j, u in enumerate(images):
                f = d / 'images' / f'{j}.jpg'
                ok, _ = xf.download(op, xf.image_candidates(u), str(f), xf.is_image)
                rec['image_files'].append(f'images/{j}.jpg' if ok else None)
            (d / 'note.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            md = [f'# {rec["title"]}', '',
                  f'- 作者：{rec["author"]}　类型：{rec["type"]}　赞 {rec["likes"]} / 藏 {rec["collects"]} / 评 {rec["comments_count"]}'
                  + (f'　时长 {rec["duration"]}s' if rec['duration'] else ''),
                  f'- 链接：{url}', f'- 命中关键词：{"、".join(r["keywords"])}', '', rec['desc'] or '', '',
                  '## 图片', *[f'- {f}' for f in rec['image_files'] if f], '', '## 评论首屏',
                  *[f'- {c["user"]}（赞 {c["likes"]}）：{c["content"]}' for c in rec['comments']]]
            (d / 'note.md').write_text('\n'.join(md) + '\n')
            print(f'[{i}] {r["id"]} 赞 {r["likes"]} 图 {sum(1 for f in rec["image_files"] if f)}/{len(images)} {rec["title"]}',
                  flush=True)
            await asyncio.sleep(2 + random.random() * 3)
        await b.close()


async def frames(cookie_file, ids, n=5):
    """视频笔记抽 n 帧当示例图：重新打开详情页拿新签名的视频地址，ffmpeg 按时间点只读需要的那几段，n 帧并行抽。"""
    from playwright.async_api import async_playwright

    def grab(t, u, dst):
        return subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-http_proxy', PROXY,
                                 '-headers', 'Referer: https://www.xiaohongshu.com/\r\n', '-ss', f'{t:.2f}', '-i', u,
                                 '-frames:v', '1', '-vf', 'scale=960:-2', '-q:v', '3', str(dst)])
    async with async_playwright() as p:
        b, ctx = await browser(p, cookie_file)
        pg = await ctx.new_page()
        for nid in ids:
            d = OUT / 'notes' / nid
            rec = json.loads((d / 'note.json').read_text())
            if rec['type'] != 'video' or len(list(d.glob('frames/*.jpg'))) >= n - 1:
                continue
            await pg.goto(rec['url'], timeout=60000)
            await pg.wait_for_timeout(2500)
            urls = video_urls(await pg.evaluate(NOTE_JS) or {})
            dur = rec.get('duration') or 30
            (d / 'frames').mkdir(exist_ok=True)
            todo = list(range(n))
            for u in urls[:3]:                    # 主地址失败的帧换备用地址再抽
                jobs = {k: grab(dur * (0.12 + 0.76 * k / max(1, n - 1)), u, d / 'frames' / f'{k}.jpg') for k in todo}
                todo = [k for k, j in jobs.items() if j.wait(timeout=120) != 0]
                if not todo:
                    break
            print(f'{nid} 帧 {n - len(todo)}/{n} {rec["title"]}', flush=True)
            await asyncio.sleep(1 + random.random() * 2)
        await b.close()


def sheets(w=480):
    """每条笔记拼一张总览图 sheet.jpg（图文笔记取前 6 张图，视频笔记取封面 + 抽帧），读笔记时一条只看一张"""
    from PIL import Image
    for d in sorted((OUT / 'notes').iterdir()):
        files = sorted(d.glob('images/*.jpg'), key=lambda f: int(f.stem))
        files = (files[:1] + sorted(d.glob('frames/*.jpg'))) if (d / 'frames').exists() else files[:6]
        ims = []
        for f in files[:6]:
            try:
                im = Image.open(f).convert('RGB')
            except Exception:
                continue
            im.thumbnail((w, w * 2))
            ims.append(im)
        if not ims:
            continue
        cols = min(3, len(ims))
        rows = [ims[k:k + cols] for k in range(0, len(ims), cols)]
        hs = [max(im.height for im in r) for r in rows]
        sheet = Image.new('RGB', (cols * w + (cols - 1) * 6, sum(hs) + (len(rows) - 1) * 6), '#ffffff')
        y = 0
        for r, h in zip(rows, hs):
            for k, im in enumerate(r):
                sheet.paste(im, (k * (w + 6), y))
            y += h + 6
        sheet.save(d / 'sheet.jpg', quality=80)
    print('sheet.jpg 已更新')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('search')
    s.add_argument('--cookie', required=True)
    s.add_argument('--pages', type=int, default=2)
    f = sub.add_parser('fetch')
    f.add_argument('--cookie', required=True)
    f.add_argument('--top', type=int, default=150)
    f.add_argument('--min-likes', type=int, default=30)
    f.add_argument('--ids', nargs='*')
    v = sub.add_parser('frames')
    v.add_argument('--cookie', required=True)
    v.add_argument('ids', nargs='+')
    sub.add_parser('sheets')
    a = ap.parse_args()
    if a.cmd == 'search':
        asyncio.run(search(a.cookie, a.pages))
    elif a.cmd == 'fetch':
        asyncio.run(fetch(a.cookie, a.top, a.min_likes, set(a.ids or [])))
    elif a.cmd == 'frames':
        asyncio.run(frames(a.cookie, a.ids))
    else:
        sheets()

