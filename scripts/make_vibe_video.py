#!/usr/bin/env python3
"""Video 章 Vibe Video 的组件：场景画廊 + 项目表的示例图与 logo。

素材：
  middle_processing/samples_src/xhs-vibe-video/notes/     小红书笔记（scripts/xhs_vibe_crawl.py 爬的）
  middle_processing/samples_src/xhs-vibe-video/extract/   逐条笔记的结构化抽取（batch_*.jsonl）
  middle_processing/figure_src/vibe-video/scenes.json     场景 taxonomy：定义、最佳实践、示例帧（手写）
  middle_processing/figure_src/vibe-video/projects.json   项目表的示例图来源（手写）
  middle_processing/figure_src/vibe-video/repos.json      GitHub 元数据缓存（repos 子命令拉）
  middle_processing/figure_src/vibe-video/logos/          owner 头像
  middle_processing/figure_src/vibe-video/repo_demos/     README 里的效果图

产物：
  assets/figures/vibe-video/scenes.html   场景画廊，图片内联，正文这样引用（build.py 会内联成 srcdoc）：
    <div class="wide-embed"><iframe src="../assets/figures/vibe-video/scenes.html" style="width:100%;height:900px;border:0"></iframe></div>
  assets/figures/vibe-video/ex/<slug>.jpg     项目表 Example 列的图（正文 <img> 直接引用，点开走 template 的 zoomImg）
  assets/figures/vibe-video/logos/<owner>.png 项目表 Project 列的 logo
  parts/video/vibe.md 里 <!--VIBE-SHARED-->、<!--VIBE-PROJECTS--> 两段表格（标记之间整段重写）

用法：
  python3 scripts/make_vibe_video.py repos owner/name ...   # 拉 star、简介、头像，合并进缓存
  python3 scripts/make_vibe_video.py stats                  # 抽取结果按场景汇总（写 scenes.json 前看）
  python3 scripts/make_vibe_video.py build                  # 出画廊、项目表、示例图、logo
"""
import base64
import collections
import io
import json
import re
import shutil
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'middle_processing/figure_src/vibe-video'
XHS = ROOT / 'middle_processing/samples_src/xhs-vibe-video'
OUT = ROOT / 'assets/figures/vibe-video'


# ---------------------------------------------------------------------------
# GitHub 元数据

def gh(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'visual-coder-blog', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def repos(names):
    cache_file = SRC / 'repos.json'
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    (SRC / 'logos').mkdir(parents=True, exist_ok=True)
    for name in names:
        if name in cache:
            continue
        try:
            d = json.loads(gh(f'https://api.github.com/repos/{name}'))
        except Exception as e:
            print(f'{name:<45} 失败 {e}')
            continue
        owner = d['owner']['login']
        cache[name] = {
            'full_name': d['full_name'], 'stars': d['stargazers_count'], 'forks': d['forks_count'],
            'description': d['description'], 'homepage': d['homepage'], 'license': (d.get('license') or {}).get('spdx_id'),
            'created': d['created_at'][:10], 'pushed': d['pushed_at'][:10], 'topics': d.get('topics') or [],
            'owner': owner, 'owner_type': d['owner']['type'], 'checked': time.strftime('%Y-%m-%d'),
        }
        cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
        logo = SRC / 'logos' / f'{owner}.png'
        try:
            if not logo.exists():
                logo.write_bytes(gh(d['owner']['avatar_url'] + ('&' if '?' in d['owner']['avatar_url'] else '?') + 's=96'))
        except Exception as e:
            print(f'  头像失败 {e}')
        print(f'{d["full_name"]:<45} {d["stargazers_count"]:>7}  {(d["description"] or "")[:60]}')


# ---------------------------------------------------------------------------
# 笔记与抽取结果

def num(v):
    """'1.2万' / '999' → int"""
    m = re.match(r'([\d.]+)\s*(万?)', str(v or '0'))
    return int(float(m.group(1)) * (10000 if m.group(2) else 1)) if m else 0


def wan(n):
    return f'{n / 10000:.1f} 万' if n >= 10000 else f'{n:,}'


def extracts():
    rows = {}
    for f in sorted((XHS / 'extract').glob('batch_*.jsonl')):
        for line in f.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r['id']] = r
    return rows


_IDS = None


def full_id(prefix):
    """scenes.json 里笔记 id 只写前 8 位，这里补全（前缀必须唯一）"""
    global _IDS
    _IDS = _IDS or [d.name for d in (XHS / 'notes').iterdir()]
    hit = [i for i in _IDS if i.startswith(prefix)]
    assert len(hit) == 1, f'笔记前缀 {prefix} 匹配到 {len(hit)} 条'
    return hit[0]


def note(nid):
    return json.loads((XHS / 'notes' / full_id(nid) / 'note.json').read_text())


def stats():
    rows = extracts()
    rel = collections.Counter(r.get('relevant') for r in rows.values())
    print(f'抽取 {len(rows)} 条：{dict(rel)}')
    by = collections.defaultdict(list)
    for r in rows.values():
        if r.get('relevant') in ('core', 'adjacent'):
            by[r.get('scene')].append(r)
    for k, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        likes = sum(num(note(r['id'])['likes']) for r in rs)
        print(f'\n## {k}  {len(rs)} 条  赞 {wan(likes)}')
        for r in sorted(rs, key=lambda r: -num(note(r['id'])['likes']))[:40]:
            print(f'  {r["id"]} 赞{note(r["id"])["likes"]:>6} q{r.get("quality")} {r["title"][:30]}  demo={(r.get("demo") or {}).get("file")}')


# ---------------------------------------------------------------------------
# 图片

def jpeg(path, width, quality=80):
    from PIL import Image
    im = Image.open(path)
    if getattr(im, 'n_frames', 1) > 1:      # GIF / 动图 WebP 取中间一帧，首帧常是空白或片头
        im.seek(im.n_frames // 2)
    im = im.convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return buf.getvalue()


def data_uri(path, width, quality=72):
    """画廊的图内联成 WebP（比 JPEG 小约三成），整页才不至于太重"""
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=quality, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def esc(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# ---------------------------------------------------------------------------
# 场景画廊

GALLERY = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vibe Video 场景画廊</title>
<style>
  :root{--ink:#111418;--soft:#5b636e;--faint:#8a929d;--line:#e4e7ec;--band:#f6f7f9;--brand:#2563eb}
  *{box-sizing:border-box}
  html,body{margin:0;background:transparent;color:var(--ink);
            font:13px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
  a{color:inherit}
  /* 行内态：场景卡片墙 */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;padding:4px 2px 14px}
  .fam{grid-column:1/-1;display:flex;align-items:baseline;gap:9px;margin:10px 0 -4px;padding-bottom:7px;border-bottom:1px solid var(--line);font-weight:400}
  .fam:first-child{margin-top:0}
  .fam b{font-size:15px;font-weight:700}
  .fam span{font-size:12px;color:var(--faint);letter-spacing:.06em;text-transform:uppercase}
  .fam i{margin-left:auto;font-style:normal;font-size:12px;color:var(--soft)}
  .card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;cursor:pointer;outline:none;
        transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease}
  .card:hover,.card:focus-visible{transform:translateY(-3px);box-shadow:0 14px 32px rgba(17,20,24,.13);border-color:#d3d8df}
  .poster{position:relative;display:grid;grid-template-columns:2fr 1fr;grid-template-rows:repeat(2,minmax(0,1fr));gap:2px;aspect-ratio:16/8.4;overflow:hidden;background:#0f1115}
  .poster img{width:100%;height:100%;min-height:0;object-fit:cover;display:block}
  .poster img:first-child{grid-row:1/3}
  .poster img:only-child{grid-column:1/3}
  .poster .k{position:absolute;left:10px;top:10px;font:700 10.5px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;
             color:#fff;background:var(--c);padding:5px 8px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
  .meta{padding:12px 14px 13px;display:flex;flex-direction:column;gap:7px;flex:1}
  .ttl{display:flex;align-items:baseline;gap:8px}
  .ttl b{font-size:15.5px;font-weight:700}
  .ttl span{font-size:12px;color:var(--faint)}
  .cnt{margin-left:auto;font-size:11.5px;color:var(--soft);white-space:nowrap}
  .def{margin:0;color:var(--soft);font-size:12.5px}
  .bp{margin:0;padding:0;list-style:none;counter-reset:bp;display:flex;flex-direction:column;gap:5px}
  .bp li{counter-increment:bp;position:relative;padding-left:22px;font-size:12.5px;line-height:1.5}
  .bp li::before{content:counter(bp);position:absolute;left:0;top:1px;width:16px;height:16px;border-radius:5px;background:var(--c);color:#fff;
                 font:700 10px/16px ui-monospace,Menlo,monospace;text-align:center}
  .more{margin-top:auto;padding-top:4px;font-size:12px;font-weight:600;color:var(--c)}
  /* 放大态：父页把 iframe 铺满视口，这里画成居中的大面板 */
  .modal{display:none}
  body.full{height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
  body.full .grid{display:none}
  body.full .modal{display:flex;flex-direction:column;width:min(1320px,100%);height:min(860px,100%);background:#fff;border-radius:16px;overflow:hidden;
                   box-shadow:0 26px 90px rgba(0,0,0,.4)}
  .bar{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid var(--line);background:var(--band)}
  .bar .dot{width:10px;height:10px;border-radius:3px;background:var(--c);flex:none}
  .bar b{font-size:16px;white-space:nowrap}
  .bar .en{font-size:12.5px;color:var(--faint);white-space:nowrap}
  .bar .d{flex:1;min-width:0;color:var(--soft);font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  button{font:inherit;font-size:12px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:999px;padding:4px 12px;cursor:pointer;white-space:nowrap}
  button:hover{border-color:#c9ced6}
  .body{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr)}
  .viewer{display:flex;flex-direction:column;min-height:0;background:#0f1115}
  .stage{flex:1;min-height:0;display:grid;place-items:center;position:relative}
  .stage img{max-width:100%;max-height:100%;object-fit:contain;display:block}
  .stage .nav{position:absolute;top:50%;transform:translateY(-50%);width:34px;height:34px;padding:0;border-radius:50%;background:rgba(255,255,255,.12);
              border:1px solid rgba(255,255,255,.2);color:#fff;font-size:16px}
  .stage .nav:hover{background:rgba(255,255,255,.24)}
  .stage .prev{left:12px} .stage .next{right:12px}
  .cap{padding:9px 14px;color:#c9d0da;font-size:12.5px;border-top:1px solid rgba(255,255,255,.08);display:flex;gap:10px;align-items:baseline}
  .cap .w{color:#fff;font-weight:600;white-space:nowrap}
  .cap .t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .cap a{color:#9ec1ff;text-decoration:none;white-space:nowrap}
  .strip{display:flex;gap:6px;padding:8px 10px 10px;overflow-x:auto;background:#0b0d10}
  .strip img{height:52px;width:auto;border-radius:5px;opacity:.55;cursor:pointer;border:2px solid transparent;flex:none}
  .strip img.on{opacity:1;border-color:#fff}
  .side{overflow:auto;padding:16px 18px 22px;display:flex;flex-direction:column;gap:16px}
  .side h4{margin:0 0 7px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:700}
  .side .bp li{font-size:13px;line-height:1.6}
  .side .bp li + li{margin-top:3px}
  .srcs{display:inline-flex;flex-wrap:wrap;gap:4px;margin-left:4px;vertical-align:1px}
  .srcs a{font-size:10.5px;font-weight:600;color:var(--soft);text-decoration:none;border:1px solid var(--line);border-radius:5px;padding:0 5px;white-space:nowrap}
  .srcs a:hover{color:var(--brand);border-color:var(--brand)}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chips span,.chips a{font-size:12px;border:1px solid var(--line);background:var(--band);border-radius:6px;padding:1px 8px;text-decoration:none}
  .chips a:hover{border-color:var(--brand);color:var(--brand)}
  .pit{margin:0;padding-left:18px;color:var(--soft);font-size:12.5px}
  @media (max-width:820px){
    body.full{padding:0}
    body.full .modal{height:100%;border-radius:0}
    .body{grid-template-columns:1fr;grid-template-rows:auto 1fr}
    .stage{height:46vh;flex:none}
    .bar .d,.bar .en{display:none}
  }
</style>
</head>
<body>
<div class="grid">__CARDS__</div>
<div class="modal" role="dialog" aria-modal="true">
  <div class="bar"><span class="dot"></span><b id="m-cn"></b><span class="en" id="m-en"></span><span class="d" id="m-def"></span>
    <button id="m-prev" title="上一类">‹ 上一类</button><button id="m-next" title="下一类">下一类 ›</button><button id="m-close">收起</button></div>
  <div class="body">
    <div class="viewer">
      <div class="stage"><img id="m-img" alt=""><button class="nav prev" id="i-prev" aria-label="上一张">‹</button><button class="nav next" id="i-next" aria-label="下一张">›</button></div>
      <div class="cap"><span class="w" id="m-who"></span><span class="t" id="m-t"></span><a id="m-link" target="_blank" rel="noopener">看原帖 ↗</a></div>
      <div class="strip" id="m-strip"></div>
    </div>
    <div class="side">
      <section><h4>最佳实践</h4><ol class="bp" id="m-bp"></ol></section>
      <section><h4>常用栈</h4><div class="chips" id="m-stack"></div></section>
      <section><h4>代表项目</h4><div class="chips" id="m-proj"></div></section>
      <section id="m-pit-s"><h4>踩坑</h4><ul class="pit" id="m-pit"></ul></section>
    </div>
  </div>
</div>
<script>
(function(){
  var S = __DATA__;
  var embedded = window.parent !== window, full = false, cur = 0, img = 0;
  var grid = document.querySelector('.grid'), modal = document.querySelector('.modal');
  function byId(id){ return document.getElementById(id); }
  function report(){ if (embedded && !full) window.parent.postMessage({type: 'kc-height', h: grid.offsetHeight + 4}, '*'); }
  function el(tag, attrs, text){
    var e = document.createElement(tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }
  function showImg(k){
    var s = S[cur], d = s.demos[k]; img = k;
    byId('m-img').src = d.src;
    byId('m-who').textContent = '@' + d.who + ' · 赞 ' + d.likes;
    byId('m-t').textContent = d.title;
    byId('m-link').href = d.url;
    [].forEach.call(byId('m-strip').children, function(t, j){ t.classList.toggle('on', j === k); });
  }
  function fill(i){
    cur = (i + S.length) % S.length;
    var s = S[cur];
    modal.style.setProperty('--c', s.color);
    byId('m-cn').textContent = s.cn; byId('m-en').textContent = s.en; byId('m-def').textContent = s.def;
    var bp = byId('m-bp'); bp.innerHTML = '';
    s.practices.forEach(function(p){
      var li = el('li', {}, p.t + ' ');
      if (p.src.length){
        var box = el('span', {'class': 'srcs'});
        p.src.forEach(function(r){ box.appendChild(el('a', {href: r.url, target: '_blank', rel: 'noopener', title: r.title}, '@' + r.who)); });
        li.appendChild(box);
      }
      bp.appendChild(li);
    });
    var st = byId('m-stack'); st.innerHTML = '';
    s.stack.forEach(function(x){ st.appendChild(el('span', {}, x)); });
    var pj = byId('m-proj'); pj.innerHTML = '';
    s.projects.forEach(function(p){ pj.appendChild(el('a', {href: p.url, target: '_blank', rel: 'noopener'}, p.name)); });
    byId('m-pit-s').style.display = s.pitfalls.length ? '' : 'none';
    var pt = byId('m-pit'); pt.innerHTML = '';
    s.pitfalls.forEach(function(x){ pt.appendChild(el('li', {}, x)); });
    var strip = byId('m-strip'); strip.innerHTML = '';
    s.demos.forEach(function(d, k){
      var t = el('img', {src: d.src, alt: d.title, title: d.title});
      t.onclick = function(){ showImg(k); };
      strip.appendChild(t);
    });
    var one = s.demos.length < 2;
    byId('i-prev').style.display = byId('i-next').style.display = one ? 'none' : '';
    showImg(0);
  }
  function setFull(on){
    full = on;
    document.body.classList.toggle('full', on);
    if (!on) report();
  }
  function open(i){
    fill(i);
    if (embedded) window.parent.postMessage({type: 'kc-expand'}, '*'); else setFull(true);
  }
  function close(){ if (embedded) window.parent.postMessage({type: 'kc-collapse'}, '*'); else setFull(false); }

  [].forEach.call(document.querySelectorAll('.card'), function(c){
    var i = +c.dataset.i;
    [].forEach.call(c.querySelectorAll('.poster img'), function(im){ im.src = S[i].demos[+im.dataset.d].src; });
    c.addEventListener('click', function(e){ if (!e.target.closest('a')) open(i); });
    c.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
  });
  byId('m-close').onclick = close;
  byId('m-prev').onclick = function(){ fill(cur - 1); };
  byId('m-next').onclick = function(){ fill(cur + 1); };
  byId('i-prev').onclick = function(){ showImg((img - 1 + S[cur].demos.length) % S[cur].demos.length); };
  byId('i-next').onclick = function(){ showImg((img + 1) % S[cur].demos.length); };
  document.body.addEventListener('click', function(e){ if (full && e.target === document.body) close(); });
  window.addEventListener('keydown', function(e){
    if (!full) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') byId('i-prev').click();
    if (e.key === 'ArrowRight') byId('i-next').click();
  });
  window.addEventListener('resize', report);
  window.addEventListener('load', report);
  // 父页放大 / 还原好 iframe 后回 ack，这边排好版再回话，父页才显影
  window.addEventListener('message', function(e){
    if (e.source !== window.parent || !e.data) return;
    if (e.data.type === 'kc-expand-ack')   { setFull(true);  window.parent.postMessage({type: 'kc-modal-ready'}, '*'); }
    if (e.data.type === 'kc-collapse-ack') { setFull(false); window.parent.postMessage({type: 'kc-revealed'}, '*'); }
  });
  report();
})();
</script>
</body>
</html>
'''


def note_ref(nid):
    n = note(nid)
    return {'who': n['author'], 'likes': n['likes'], 'title': n['title'] or '', 'url': n['url']}


def scene_members(cfg):
    """每类的笔记：core + adjacent，按主场景归类（alias 里的小类并进大类）"""
    out = collections.defaultdict(list)
    for r in extracts().values():
        if r.get('relevant') in ('core', 'adjacent'):
            out[cfg.get('alias', {}).get(r.get('scene'), r.get('scene'))].append(r)
    return out


def build_gallery(cfg, repo_meta):
    by = scene_members(cfg)
    data, cards = [], []
    for fam in cfg['families']:
        n = sum(len(by[k]) for k in fam['scenes'])
        cards.append(f'<h3 class="fam"><b>{esc(fam["cn"])}</b><span>{esc(fam["en"])}</span>'
                     f'<i>{len(fam["scenes"])} 类 · {n} 条笔记</i></h3>')
        for key in fam['scenes']:
            cards.append(scene_card(key, cfg['scenes'][key], by[key], repo_meta, data))
    # 博客页会把成对的 $ 当公式抽走：正文里写成实体，JS 字符串里写成 \u0024
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/').replace('$', '\\u0024')
    html = GALLERY.replace('__CARDS__', ''.join(cards).replace('$', '&#36;')).replace('__DATA__', blob)
    assert '$' not in html
    (OUT / 'scenes.html').write_text(html, encoding='utf-8')
    print(f'scenes.html  {len(html) // 1024} KB  {len(data)} 类')


def scene_card(key, s, members, repo_meta, data):
    likes = sum(num(note(r['id'])['likes']) for r in members)
    demos = []
    for d in s['demos']:
        path = XHS / 'notes' / full_id(d['note']) / d['file']
        ref = note_ref(d['note'])
        ref['src'] = data_uri(path, 720)
        demos.append(ref)
    projects = [{'name': repo_meta[p]['full_name'].split('/')[1], 'url': f'https://github.com/{repo_meta[p]["full_name"]}'}
                for p in s.get('projects', []) if p in repo_meta]
    data.append({
        'key': key, 'cn': s['cn'], 'en': s['en'], 'color': s['color'], 'def': s['def'],
        'practices': [{'t': p['t'], 'src': [note_ref(n) for n in p.get('src', [])]} for p in s['practices']],
        'stack': s['stack'], 'projects': projects, 'pitfalls': s.get('pitfalls', []),
        'demos': demos,
    })
    # 封面图不重复内联，由脚本从数据里取同一份 src 填上
    poster = ''.join(f'<img data-d="{k}" alt="">' for k in range(min(3, len(demos))))
    top = ''.join(f'<li>{esc(p["t"])}</li>' for p in s['practices'][:3])
    return (f'<article class="card" tabindex="0" data-i="{len(data) - 1}" style="--c:{s["color"]}">'
            f'<div class="poster">{poster}<span class="k">{esc(s["en"])}</span></div>'
            f'<div class="meta"><div class="ttl"><b>{esc(s["cn"])}</b><span>{esc(s["en"])}</span>'
            f'<span class="cnt">{len(members)} 条 · 赞 {wan(likes)}</span></div>'
            f'<p class="def">{esc(s["def"])}</p><ol class="bp">{top}</ol>'
            f'<span class="more">全部 {len(s["practices"])} 条做法、{len(demos)} 张成片 →</span></div></article>')


# ---------------------------------------------------------------------------
# 项目表：表格写进 parts/video/vibe.md 的标记之间，示例图与 logo 拷进 assets

PAGE = ROOT / 'parts/video/vibe.md'
ASSET = '../assets/figures/vibe-video'


def write_block(name, rows):
    """把表格写进 vibe.md 里 <!--NAME--> 与 <!--/NAME--> 之间（整段重写）"""
    md = PAGE.read_text()
    a = md.index(f'<!--{name}-->') + len(f'<!--{name}-->')
    b = md.index(f'<!--/{name}-->')
    PAGE.write_text(md[:a] + '\n' + '\n'.join(rows).replace('$', '&#36;') + '\n' + md[b:])
    print(f'{name} {len(rows) - 2} 行 → {PAGE.relative_to(ROOT)}')


def build_shared(shared):
    rows = ['| Practice | Detail | Source |', '|---|---|---|']
    for x in shared:
        src = [used_line({'t': '@' + note(n)['author'], 'note': n}) for n in x.get('src', [])]
        src += [used_line(u) for u in x.get('u', [])]
        rows.append(f'| {esc(x["p"])} | {esc(x["d"])} | {"、".join(src)} |')
    write_block('VIBE-SHARED', rows)


def tag(key, scenes):
    if key == 'all':
        return '<span class="scn" style="--c:#64748b">全场景</span>'
    s = scenes[key]
    return f'<span class="scn" style="--c:{s["color"]}">{s["cn"]}</span>'


def used_line(u):
    href = note(u['note'])['url'] if 'note' in u else u['u']
    return f'<a href="{esc(href)}">{esc(u["t"])}</a>'


def build_projects(cfg, scenes, repo_meta):
    (OUT / 'ex').mkdir(parents=True, exist_ok=True)
    (OUT / 'logos').mkdir(parents=True, exist_ok=True)
    rows = ['| Type | Project | Field | Used | Example |', '|---|---|---|---|---|']
    for t in cfg['types']:
        items = sorted(t['items'], key=lambda p: -repo_meta[p['repo']]['stars'])
        for k, p in enumerate(items):
            meta = repo_meta[p['repo']]
            full, owner = meta['full_name'], meta['owner']
            slug = full.replace('/', '__')
            shutil.copy(SRC / 'logos' / f'{owner}.png', OUT / 'logos' / f'{owner}.png')
            ex = p['example']
            src = XHS / 'notes' / full_id(ex['note']) / ex['file'] if 'note' in ex else SRC / 'repo_demos' / ex['repo_file']
            (OUT / 'ex' / f'{slug}.jpg').write_bytes(jpeg(src, 1280, 82))
            href = note(ex['note'])['url'] if 'note' in ex else f'https://github.com/{full}'
            cells = [
                f'{t["cn"]}<br><span class="pstar">{t["en"]}</span>' if k == 0 else '',
                f'<img class="plogo" src="{ASSET}/logos/{owner}.png" alt=""><a href="https://github.com/{full}">{full.split("/")[1]}</a>'
                f'<span class="pstar">★ {wan(meta["stars"])}</span>',
                ' '.join(tag(f, scenes) for f in p['field']),
                '<br>'.join(used_line(u) for u in p['used']),
                f'<img class="ex-thumb" src="{ASSET}/ex/{slug}.jpg" alt="" loading="lazy" onclick="zoomImg(this)" '
                f'data-cap="{esc(ex["cap"])}" data-href="{esc(href)}">',
            ]
            assert not any('|' in c for c in cells), f'{full} 的单元格里有 |，会把 md 表格切断'
            rows.append('| ' + ' | '.join(cells) + ' |')
    write_block('VIBE-PROJECTS', rows)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    repo_meta = json.loads((SRC / 'repos.json').read_text())
    scenes = json.loads((SRC / 'scenes.json').read_text())
    build_gallery(scenes, repo_meta)
    build_shared(scenes['shared'])
    build_projects(json.loads((SRC / 'projects.json').read_text()), scenes['scenes'], repo_meta)


if __name__ == '__main__':
    cmd = sys.argv[1:2]
    if cmd == ['repos']:
        repos(sys.argv[2:])
    elif cmd == ['stats']:
        stats()
    elif cmd == ['build']:
        build()
    else:
        sys.exit(__doc__)

