#!/usr/bin/env python3
"""审美 rubric 的 pairwise 示例：同一 query、同一份内容，只在一条规则上不同的两张网页。

源：middle_processing/figure_src/aesthetic-pairs/
  - <slug>.html：一张网页，<body class="{{V}}">。A 版 V=good、B 版 V=bad；
    B 版的差异全部写在 .bad 选择器和 .only-bad 元素里，保证两版只差这一条规则
  - pairs.json：每对的规则编号、名字、query、两侧一句话说明
产物：assets/figures/aesthetic-pairs/<slug>.html。正文里这样引用（build.py 会内联成 srcdoc）：
  <div class="wide-embed"><iframe src="../assets/figures/aesthetic-pairs/<slug>.html" style="height:560px;border:0"></iframe></div>
组件按宽度排版并用 kc-height 回报高度；「放大对比」走 template.html 的 kc-expand 协议。
另出一份 <slug>-thumb.html：rubric 表里那一格只放 A / B 两张缩略图，点开走 kc-expand 全屏，
  并排或单张（空格切换）看两张真网页。缩略图由 shots 子命令用 Playwright 截好，存在 figure_src/aesthetic-pairs/thumbs/。
用法：python3 scripts/make_aesthetic_pairs.py [shots] [slug ...]
"""
import base64
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'middle_processing/figure_src/aesthetic-pairs'
OUT = ROOT / 'assets/figures/aesthetic-pairs'
THUMBS = SRC / 'thumbs'

VIEWER = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{--ink:#111418;--soft:#5b636e;--line:#e4e7ec;--band:#f6f7f9;--ok:#0b7a4b;--ok-bg:#e6f5ed;--bad:#b42318;--bad-bg:#fdecea;
        --mono:"SF Mono",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace}
  *{box-sizing:border-box}
  html,body{margin:0;background:transparent;color:var(--ink);
            font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
  .card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
  .top{display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--band);border-bottom:1px solid var(--line)}
  .tag{font:600 10.5px/1 var(--mono);letter-spacing:.08em;color:var(--soft);text-transform:uppercase}
  .query{flex:1;min-width:0;font-size:13.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .rule{font-size:12px;color:var(--soft);white-space:nowrap}
  button{font:inherit;font-size:12px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:999px;padding:4px 11px;cursor:pointer}
  button:hover{border-color:#c5cad3}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:14px}
  .head{display:flex;align-items:center;gap:8px;margin-bottom:8px;min-height:24px}
  .side{font:700 12px/1 var(--mono);width:22px;height:22px;border-radius:6px;display:grid;place-items:center;background:var(--ink);color:#fff;flex:none}
  .pill{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:999px;flex:none}
  .ok .pill{color:var(--ok);background:var(--ok-bg)} .bad .pill{color:var(--bad);background:var(--bad-bg)}
  .say{flex:1;min-width:0;color:var(--soft);font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .open{border:0;background:none;color:#2f6bff;padding:0 2px}
  .stage{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:10px;background:#eef0f3}
  .stage iframe{position:absolute;top:0;left:0;width:1280px;height:800px;border:0;transform-origin:0 0;background:#fff}
  @media (max-width:720px){.grid{grid-template-columns:1fr}.say,.query{white-space:normal}.rule{display:none}}
  /* 放大态：父页把本 iframe 铺满视口，这里画成居中的大卡片，点卡片外收起 */
  body.full{height:100vh;display:flex;align-items:center;justify-content:center;padding:28px}
  body.full .card{width:min(100%,2400px);box-shadow:0 24px 80px rgba(0,0,0,.35)}
  /* 放大态只放一张、尽量大，A / B 原地切换（空格或方向键），差别最容易看出来 */
  .flip{display:none;gap:2px;background:#e9ecf1;border-radius:999px;padding:3px}
  .flip button{border:0;background:none;padding:4px 12px}
  .flip button.on{background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.12)}
  body.full .flip{display:inline-flex}
  body.full .grid{grid-template-columns:1fr}
  body.full .grid > div{display:none}
  body.full .grid > div.sel{display:block}
</style>
</head>
<body>
<div class="card">
  <div class="top"><span class="tag">Query</span><span class="query">__QUERY__</span><span class="rule">__RULE__</span><span class="flip" title="空格或方向键切换"><button class="on">A 符合</button><button>B 违反</button></span><button id="zoom">放大对比</button></div>
  <div class="grid">
    <div class="ok sel"><div class="head"><span class="side">A</span><span class="pill">符合</span><span class="say">__A__</span><button class="open" data-v="good">新标签打开</button></div><div class="stage"><iframe title="A" data-v="good"></iframe></div></div>
    <div class="bad"><div class="head"><span class="side">B</span><span class="pill">违反</span><span class="say">__B__</span><button class="open" data-v="bad">新标签打开</button></div><div class="stage"><iframe title="B" data-v="bad"></iframe></div></div>
  </div>
</div>
<script>
(function(){
  var PAGE = __PAGE__;
  var W = 1280, H = 800;
  var full = false, embedded = window.parent !== window;
  function doc(v){ return PAGE.replace('{{V}}', v); }
  var frames = [].slice.call(document.querySelectorAll('.stage iframe'));
  // 一页正文里有十来个对比组件：滚到附近才把两张网页放进去，免得一开页就渲染二十张
  function load(){ frames.forEach(function(f){ if (!f.srcdoc) f.srcdoc = doc(f.dataset.v); }); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      if (es.some(function(e){ return e.isIntersecting; })) { load(); io.disconnect(); }
    }, {rootMargin: '800px 0px'});
    io.observe(document.querySelector('.card'));
  } else load();

  function layout(){
    var room = full ? window.innerHeight - 56 - 120 : Infinity;   // 放大态按视口高度封顶
    frames.forEach(function(f){
      var st = f.parentNode, w = st.clientWidth;
      var s = Math.min(w / W, room / H);
      st.style.height = Math.round(H * s) + 'px';
      f.style.transform = 'translate(' + Math.max(0, (w - W * s) / 2) + 'px,0) scale(' + s + ')';
    });
    if (embedded && !full) window.parent.postMessage({type: 'kc-height', h: document.querySelector('.card').offsetHeight + 2}, '*');
  }
  window.addEventListener('resize', layout);
  layout();

  [].slice.call(document.querySelectorAll('.open')).forEach(function(b){
    b.onclick = function(){
      var url = URL.createObjectURL(new Blob([doc(b.dataset.v)], {type: 'text/html'}));
      window.open(url, '_blank');
      setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
    };
  });

  var panels = [].slice.call(document.querySelectorAll('.grid > div'));
  var flips = [].slice.call(document.querySelectorAll('.flip button'));
  var sel = 0;
  function pick(i){
    sel = i;
    panels.forEach(function(p, k){ p.classList.toggle('sel', k === i); });
    flips.forEach(function(b, k){ b.classList.toggle('on', k === i); });
    layout();
  }
  flips.forEach(function(b, k){ b.onclick = function(){ pick(k); }; });

  var zoom = document.getElementById('zoom');
  function setFull(on){
    full = on;
    document.body.classList.toggle('full', on);
    zoom.textContent = on ? '收起' : '放大对比';
    layout();
  }
  zoom.onclick = function(){
    if (!embedded) { setFull(!full); return; }
    window.parent.postMessage({type: full ? 'kc-collapse' : 'kc-expand'}, '*');
  };
  document.body.addEventListener('click', function(e){
    if (full && e.target === document.body) window.parent.postMessage({type: 'kc-collapse'}, '*');
  });
  window.addEventListener('keydown', function(e){
    if (!full) return;
    if (e.key === 'Escape') window.parent.postMessage({type: 'kc-collapse'}, '*');
    if (e.key === ' ' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); pick(1 - sel); }
  });
  // 父页放大 / 还原好 iframe 后回 ack，这边排好版再回话，父页才显影
  window.addEventListener('message', function(e){
    if (e.source !== window.parent || !e.data || typeof e.data !== 'object') return;
    if (e.data.type === 'kc-expand-ack')   { setFull(true);  window.parent.postMessage({type: 'kc-modal-ready'}, '*'); }
    if (e.data.type === 'kc-collapse-ack') { setFull(false); window.parent.postMessage({type: 'kc-revealed'}, '*'); }
  });
})();
</script>
</body>
</html>
'''

THUMB = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{--ink:#111418;--soft:#5b636e;--line:#e4e7ec;--band:#f6f7f9;--ok:#0b7a4b;--ok-bg:#e6f5ed;--bad:#b42318;--bad-bg:#fdecea;
        --mono:"SF Mono",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace}
  *{box-sizing:border-box}
  html,body{margin:0;background:transparent;color:var(--ink);
            font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
  /* 表格里那一格：两张缩略图，整块可点 */
  .thumbs{display:flex;gap:6px;padding:2px;cursor:zoom-in;outline:none;width:max-content}
  .thumbs figure{position:relative;margin:0;width:72px;height:45px;border-radius:6px;overflow:hidden;border:1px solid var(--line);
                 transition:transform .15s ease,box-shadow .15s ease}
  .thumbs:hover figure,.thumbs:focus-visible figure{box-shadow:0 6px 14px rgba(17,20,24,.16);transform:translateY(-1px)}
  .thumbs img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
  .thumbs i{position:absolute;left:3px;bottom:3px;font:700 9px/1 var(--mono);font-style:normal;color:#fff;padding:2px 4px;border-radius:3px}
  .thumbs .ok i{background:var(--ok)} .thumbs .bad i{background:var(--bad)}
  /* 放大态：父页把本 iframe 铺满视口，这里画成居中的大卡片 */
  .modal{display:none}
  body.full{height:100vh;display:flex;align-items:center;justify-content:center;padding:28px}
  body.full .thumbs{display:none}
  body.full .modal{display:block;width:min(100%,2400px)}
  .card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,.35)}
  .top{display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--band);border-bottom:1px solid var(--line)}
  .tag{font:600 10.5px/1 var(--mono);letter-spacing:.08em;color:var(--soft);text-transform:uppercase}
  .query{flex:1;min-width:0;font-size:13.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .rule{font-size:12px;color:var(--soft);white-space:nowrap}
  button{font:inherit;font-size:12px;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:999px;padding:4px 11px;cursor:pointer}
  .seg{display:inline-flex;gap:2px;background:#e9ecf1;border-radius:999px;padding:3px}
  .seg button{border:0;background:none;padding:4px 12px}
  .seg button.on{background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.12)}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:14px}
  body.single .grid{grid-template-columns:1fr}
  body.single .grid > div{display:none}
  body.single .grid > div.sel{display:block}
  .head{display:flex;align-items:center;gap:8px;margin-bottom:8px}
  .side{font:700 12px/1 var(--mono);width:22px;height:22px;border-radius:6px;display:grid;place-items:center;background:var(--ink);color:#fff;flex:none}
  .pill{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:999px;flex:none}
  .ok .pill{color:var(--ok);background:var(--ok-bg)} .bad .pill{color:var(--bad);background:var(--bad-bg)}
  .say{flex:1;min-width:0;color:var(--soft);font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .stage{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:10px;background:#eef0f3}
  .stage{background-size:cover;background-position:top center}
  .stage iframe{position:absolute;top:0;left:0;width:1280px;height:800px;border:0;transform-origin:0 0;background:#fff;opacity:0;transition:opacity .25s ease}
  .stage iframe.ready{opacity:1}
  @media (max-width:720px){.grid{grid-template-columns:1fr}.rule{display:none}}
</style>
</head>
<body>
<div class="thumbs" role="button" tabindex="0" title="点击放大">
  <figure class="ok"><img src="__TA__" alt="A 符合"><i>A</i></figure>
  <figure class="bad"><img src="__TB__" alt="B 违反"><i>B</i></figure>
</div>
<div class="modal"><div class="card">
  <div class="top"><span class="tag">Query</span><span class="query">__QUERY__</span><span class="rule">__RULE__</span>
    <span class="seg" title="空格或方向键在 A、B 之间切换"><button class="on" data-m="2">并排</button><button data-m="0">A 符合</button><button data-m="1">B 违反</button></span>
    <button id="close">收起</button></div>
  <div class="grid">
    <div class="ok sel"><div class="head"><span class="side">A</span><span class="pill">符合</span><span class="say">__A__</span></div><div class="stage" style="background-image:url(__TA__)"><iframe title="A" data-v="good"></iframe></div></div>
    <div class="bad"><div class="head"><span class="side">B</span><span class="pill">违反</span><span class="say">__B__</span></div><div class="stage" style="background-image:url(__TB__)"><iframe title="B" data-v="bad"></iframe></div></div>
  </div>
</div></div>
<script>
(function(){
  var PAGE = __PAGE__;
  var W = 1280, H = 800;
  var full = false, mode = 2, embedded = window.parent !== window;
  var frames = [].slice.call(document.querySelectorAll('.stage iframe'));
  var panels = [].slice.call(document.querySelectorAll('.grid > div'));
  var segs = [].slice.call(document.querySelectorAll('.seg button'));
  var thumbs = document.querySelector('.thumbs');

  function report(){
    if (embedded && !full) window.parent.postMessage({type: 'kc-height', h: thumbs.offsetHeight + 4}, '*');
  }
  function layout(){
    if (!full) { report(); return; }
    var room = window.innerHeight - 56 - 120;
    frames.forEach(function(f){
      var st = f.parentNode, w = st.clientWidth;
      if (!w) return;
      var s = Math.min(w / W, room / H);
      st.style.height = Math.round(H * s) + 'px';
      f.style.transform = 'translate(' + Math.max(0, (w - W * s) / 2) + 'px,0) scale(' + s + ')';
    });
  }
  function setMode(m){
    mode = m;
    document.body.classList.toggle('single', m !== 2);
    panels.forEach(function(p, k){ p.classList.toggle('sel', m === 2 ? k === 0 : k === m); });
    segs.forEach(function(b){ b.classList.toggle('on', +b.dataset.m === m); });
    layout();
  }
  function setFull(on){
    full = on;
    document.body.classList.toggle('full', on);
    // 真网页加载前先露缩略图（图框背景），加载完再淡入，点开不会先白一下
    if (on) frames.forEach(function(f){
      if (f.srcdoc) return;
      f.onload = function(){ f.classList.add('ready'); };
      f.srcdoc = PAGE.replace('{{V}}', f.dataset.v);
    });
    layout();
    if (!on) report();
  }
  function open(){ if (embedded) window.parent.postMessage({type: 'kc-expand'}, '*'); else setFull(true); }
  function close(){ if (embedded) window.parent.postMessage({type: 'kc-collapse'}, '*'); else setFull(false); }

  thumbs.addEventListener('click', open);
  thumbs.addEventListener('keydown', function(e){ if (e.key === 'Enter') open(); });
  document.getElementById('close').onclick = close;
  segs.forEach(function(b){ b.onclick = function(){ setMode(+b.dataset.m); }; });
  document.body.addEventListener('click', function(e){ if (full && e.target === document.body) close(); });
  window.addEventListener('keydown', function(e){
    if (!full) return;
    if (e.key === 'Escape') close();
    if ([' ', 'ArrowLeft', 'ArrowRight'].indexOf(e.key) >= 0) { e.preventDefault(); setMode(mode === 0 ? 1 : 0); }
  });
  window.addEventListener('resize', layout);
  // 父页放大 / 还原好 iframe 后回 ack，这边排好版再回话，父页才显影
  window.addEventListener('message', function(e){
    if (e.source !== window.parent) return;
    if (!e.data) return;
    if (e.data.type === 'kc-expand-ack')   { setFull(true);  window.parent.postMessage({type: 'kc-modal-ready'}, '*'); }
    if (e.data.type === 'kc-collapse-ack') { setFull(false); window.parent.postMessage({type: 'kc-revealed'}, '*'); }
  });
  report();
})();
</script>
</body>
</html>
'''


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def load_page(slug):
    page = (SRC / f"{slug}.html").read_text(encoding='utf-8')
    assert page.count('{{V}}') == 1, f"{slug}: body 里要有且只有一个 {{{{V}}}}"
    # 博客页渲染 markdown 前会把一行里成对的 $…$ 当公式抽走，内联进 srcdoc 的「$249 … $412」也会被误伤；
    # 页面里的 $ 只出现在正文文字里，写成实体即可（<style> 里不解码实体，所以样式里不许出现 $）
    assert '$' not in ''.join(page.split('<style>')[1].split('</style>')[:1]), f"{slug}: <style> 里有 $"
    return page.replace('$', '&#36;')


def fill(template, pair, page):
    html = template
    for key, value in [('__TITLE__', f"{pair['id']} {pair['name']}"), ('__QUERY__', pair['query']),
                       ('__RULE__', f"{pair['id']} · {pair['name']}"), ('__A__', pair['a']), ('__B__', pair['b'])]:
        html = html.replace(key, esc(value))
    return html.replace('__PAGE__', json.dumps(page, ensure_ascii=False).replace('</', '<\\/'))


def write(name, html):
    out = OUT / name
    out.write_text(html, encoding='utf-8')
    print(f"{out.relative_to(ROOT)}  {len(html) // 1024} KB")


def build(pair):
    page = load_page(pair['slug'])
    write(f"{pair['slug']}.html", fill(VIEWER, pair, page))
    # 缩略图组件放在 markdown 表格的单元格里：内联后的 srcdoc 若含 | 会把表格切开
    thumbs = {v: 'data:image/jpeg;base64,' + base64.b64encode((THUMBS / f"{pair['slug']}-{v}.jpg").read_bytes()).decode()
              for v in ['good', 'bad']}
    html = fill(THUMB, pair, page).replace('__TA__', thumbs['good']).replace('__TB__', thumbs['bad'])
    assert '|' not in html, f"{pair['slug']}-thumb: 含 |，会切开 markdown 表格"
    write(f"{pair['slug']}-thumb.html", html)


def shots(pairs):
    """把每张网页的 A / B 版截成 1280×800 首屏，缩成 288×180 的缩略图。需要 Playwright + Chromium。"""
    from io import BytesIO
    from PIL import Image
    from playwright.sync_api import sync_playwright
    THUMBS.mkdir(parents=True, exist_ok=True)
    proxy = os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY')   # 页面要拉 Google Fonts
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={'server': proxy} if proxy else None)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        for pair in pairs:
            src = (SRC / f"{pair['slug']}.html").read_text(encoding='utf-8')
            for v in ['good', 'bad']:
                page.set_content(src.replace('{{V}}', v), wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(300)
                im = Image.open(BytesIO(page.screenshot())).convert('RGB').resize((288, 180), Image.Resampling.LANCZOS)
                im.save(THUMBS / f"{pair['slug']}-{v}.jpg", 'JPEG', quality=82, optimize=True)
            print(f"shots: {pair['slug']}")
        browser.close()


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = json.loads((SRC / 'pairs.json').read_text(encoding='utf-8'))
    args = sys.argv[1:]
    take_shots = 'shots' in args
    wanted = set(args) - {'shots'}
    pairs = [x for x in pairs if not wanted or x['slug'] in wanted]
    if take_shots:
        shots(pairs)
    for pair in pairs:
        build(pair)

