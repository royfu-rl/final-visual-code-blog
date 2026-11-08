#!/usr/bin/env python3
"""Web Verifier 3.3 rubric 的两本出处书：书卡画廊。

封面在 middle_processing/figure_src/book-gallery/，缩小后以 data URI 内联，组件自包含。
产物：assets/figures/book-gallery.html。正文里这样引用（build.py 会内联成 srcdoc）：
  <div class="wide-embed"><iframe src="../assets/figures/book-gallery.html" style="width:100%;height:280px;border:0"></iframe></div>
组件按宽度排版并用 kc-height 回报高度。
用法：python3 scripts/make_book_gallery.py
"""
import base64
import io
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'middle_processing/figure_src/book-gallery'
OUT = ROOT / 'assets/figures/book-gallery.html'

BOOKS = [
    {
        'cover': 'williams_en.jpg',
        'title': "The Non-Designer's Design Book",
        'href': 'https://archive.org/details/nondesignersdesi00will',
        'by': 'Robin Williams · 1994',
        'tags': ['豆瓣 13k 评分', 'Ant Design 四原则'],
    },
    {
        'cover': 'refactoring_ui_book.png',
        'title': 'Refactoring UI',
        'href': 'https://www.refactoringui.com/book',
        'by': 'Adam Wathan & Steve Schoger · 2018',
        'tags': ['HN 1,019 分', '覆盖 A1–A10'],
    },
]

PAGE = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rubric 出处书</title>
<style>
  :root{--ink:#111418;--soft:#5b636e;--line:#e4e7ec;--band:#f6f7f9}
  *{box-sizing:border-box}
  html,body{margin:0;background:transparent;color:var(--ink);
            font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,240px));gap:14px;padding:4px 2px 12px}
  .tile{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;color:inherit;text-decoration:none;
        transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease}
  .tile:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(17,20,24,.12);border-color:#cfd5dd}
  .poster{height:150px;background:var(--band);display:grid;place-items:center;border-bottom:1px solid var(--line)}
  .poster img{display:block;height:124px;width:auto;border-radius:2px;box-shadow:0 6px 14px rgba(17,20,24,.18)}
  .meta{padding:10px 12px 12px;display:flex;flex-direction:column;gap:6px}
  .name{font-size:14px;font-weight:700;line-height:1.35}
  .by{display:block;font-size:12px;font-weight:500;color:var(--soft);margin-top:2px}
  .tags{display:flex;flex-wrap:wrap;gap:6px}
  .tags span{font-size:11.5px;font-weight:600;color:var(--soft);background:var(--band);border:1px solid var(--line);padding:1px 7px;border-radius:6px}
</style>
</head>
<body>
<div class="grid">__CARDS__</div>
<script>
(function(){
  function report(){
    if (window.parent !== window) window.parent.postMessage({type: 'kc-height', h: document.querySelector('.grid').offsetHeight + 2}, '*');
  }
  window.addEventListener('resize', report);
  window.addEventListener('load', report);
  report();
})();
</script>
</body>
</html>
'''


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def data_uri(name):
    src = Image.open(SRC / name).convert('RGBA')
    im = Image.new('RGB', src.size, '#ffffff')   # 透明的圆角垫白底，否则转 JPEG 会变黑
    im.paste(src, mask=src.getchannel('A'))
    im.thumbnail((336, 480), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=84, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def card(b):
    tags = ''.join(f'<span>{esc(t)}</span>' for t in b['tags'])
    return (f'<a class="tile" href="{b["href"]}" target="_blank" rel="noopener">'
            f'<div class="poster"><img src="{data_uri(b["cover"])}" alt=""></div>'
            f'<div class="meta"><span class="name">{esc(b["title"])}<span class="by">{esc(b["by"])}</span></span>'
            f'<span class="tags">{tags}</span></div></a>')


if __name__ == '__main__':
    html = PAGE.replace('__CARDS__', ''.join(card(b) for b in BOOKS))
    assert '$' not in html, '博客页会把成对的 $ 当公式抽走'
    OUT.write_text(html, encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)}  {len(html) // 1024} KB')

