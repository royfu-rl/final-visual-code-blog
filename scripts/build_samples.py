#!/usr/bin/env python3
"""middle_processing/samples_src/** -> middle_processing/samples/<slug>.html

「数据样例」卡片：每个来源 2–6 条真实样本，只放数据源自带的原图、原始文件名与原始内容，不写说明文字。抓不到样本的来源
不做卡片（表里的 Permitted 列已经写了原因）。规范见
middle_processing/SAMPLES.md。组件必须是单行（markdown 遇空行会截断 HTML 块），
<pre> 里的内容要按下面 esc() 的规则转义。

用法：python3 scripts/build_samples.py [slug ...]   不带参数就全建
"""
import html
import json
import os
import re
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'middle_processing', 'samples_src')
OUT = os.path.join(ROOT, 'middle_processing', 'samples')
MAXLINES = 60
MAXCOLS = 400
MAXSIDE = 900


def esc(text):
    """转义成能塞进单行 <pre> 的内容：$ 会被当公式，~ 和 | 会被生成器/表格吃掉"""
    lines = text.split('\n')
    body = [l if len(l) <= MAXCOLS else l[:MAXCOLS] + f'…（本行共 {len(l)} 字符）' for l in lines[:MAXLINES]]
    if len(lines) > MAXLINES:
        body.append(f'…（截断，原文共 {len(lines)} 行）')
    s = html.escape('\n'.join(body), quote=False)
    return s.replace('\n', '&#10;').replace('$', '&#36;').replace('~', '&#126;').replace('|', '&#124;')


def code(label, text):
    n = text.count('\n') + 1
    shown = f'，展示前 {MAXLINES} 行' if n > MAXLINES else ''
    return (f'<details class="ds-code"><summary>{label}（共 {n} 行{shown}）</summary>'
            f'<pre>{esc(text)}</pre></details>')


def card(img, name, blocks=()):
    """卡片只放数据源自带的东西：原图、原始文件名、原始内容。不写任何说明文字"""
    im = f'<img class="ds-img" src="../assets/samples/{img}" alt="">' if img else ''
    return f'<div class="ds-card">{im}<div class="ds-meta"><b>{name}</b></div>{"".join(blocks)}</div>'


def demo(head, cards):
    return f'<div class="ds-demo"><div class="ds-head">{head}</div><div class="ds-grid">{"".join(cards)}</div></div>'


def read(rel):
    return open(os.path.join(SRC, rel), encoding='utf-8').read()


def raw(slug, name):
    """原图拷进 assets：长边超过 MAXSIDE 就等比缩小，保持原格式与透明背景，不裁剪、不铺底色"""
    dst = os.path.join(ROOT, 'assets', 'samples', slug, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(os.path.join(SRC, slug, name))
    fmt = im.format                      # 按真实格式存：有的原图扩展名与内容不符（.jpg 里装的是 PNG）
    if max(im.size) > MAXSIDE:
        im.thumbnail((MAXSIDE, MAXSIDE), Image.LANCZOS)
        im.save(dst, format=fmt, optimize=True)
    else:
        shutil.copyfile(os.path.join(SRC, slug, name), dst)
    return f'{slug}/{name}'


def head(link, dsid):
    return f'<b>数据样例</b> · <a href="{link}">{dsid}</a>'


def strip(text):
    """手写的组件同样只留原始字段：标题栏只留数据集链接，卡片只留原始文件名，代码块标题只留文件名或字段名"""
    text = re.sub(r'(<div class="ds-head"><b>数据样例</b> · <a [^>]*>[^<]*</a>).*?(</div><div class="ds-grid">)',
                  r'\1\2', text)

    def meta(m):
        b = re.match(r'\s*<b>([^<]*)</b>', m.group(1)) or re.search(r'（([\w./-]+\.\w+)）', m.group(1))
        return f'<div class="ds-meta"><b>{b.group(1)}</b></div>' if b else ''

    def summary(m):
        name = re.split(r'[（：]', m.group(1))[0].strip()
        n = re.search(r'共 [\d,]+ 行[^）]*', m.group(1))
        return f'<summary>{name}（{n.group(0)}）</summary>' if n else f'<summary>{name}</summary>'

    text = re.sub(r'<div class="ds-meta">(.*?)</div>', meta, text)
    text = re.sub(r'<summary>(.*?)</summary>', summary, text)
    return re.sub(r' alt="[^"]*"', ' alt=""', text)


# ---------------------------------------------------------------------------
# 各数据集
# ---------------------------------------------------------------------------

def design2code():
    h = head('https://huggingface.co/datasets/SALT-NLP/Design2Code', 'SALT-NLP/Design2Code')
    return demo(h, [card(raw('design2code', f'{i}.png'), f'{i}.png',
                         [code(f'{i}.html', read(f'design2code/{i}.html'))])
                    for i in ('5485', '13004', '10564')])


def design2code_hard():
    h = head('https://huggingface.co/datasets/SALT-NLP/Design2Code-HARD', 'SALT-NLP/Design2Code-HARD')
    return demo(h, [card(raw('design2code-hard', f'{i}.png'), f'{i}.png',
                         [code(f'{i}.html', read(f'design2code-hard/{i}.html'))])
                    for i in ('g4', 'g2', 'g44')])


def sketch2code():
    h = head('https://huggingface.co/datasets/SALT-NLP/Sketch2Code', 'SALT-NLP/Sketch2Code')
    return demo(h, [card(raw('sketch2code', f'{i}_0.png'), f'{i}_0.png',
                         [code(f'{i}.html', read(f'sketch2code/{i}.html'))])
                    for i in ('5485', '13004', '10564')])


def web2code():
    """图在 HF 上 29.6 GB 的 Web2Code_image.zip 里，由 scripts/fetch_web2code_images.py 按 Range 取出"""
    d = json.load(open(os.path.join(SRC, 'web2code', 'samples.json'), encoding='utf-8'))
    h = head('https://huggingface.co/datasets/MBZUAI/Web2Code', 'MBZUAI/Web2Code')
    return demo(h, [card(raw('web2code', os.path.basename(rec['image'])), rec['image'],
                         [code('conversations[0]', rec['conversations'][0]['value']),
                          code('conversations[1]', rec['conversations'][1]['value'])])
                    for rec in (d[0], d[3], d[7])])


def chartjs():
    h = head('https://github.com/chartjs/Chart.js/tree/master/test/fixtures', 'chartjs/Chart.js')
    return demo(h, [card(raw('chartjs', f'{i}.png'), f'{i}.png', [code(f'{i}.js', read(f'chartjs/{i}.js'))])
                    for i in ('bar-animation-hide-show', 'bar-base-value', 'aligned-pixels')])


def openlayers():
    h = head('https://github.com/openlayers/openlayers/tree/main/test/rendering/cases', 'openlayers/openlayers')
    return demo(h, [card(raw('openlayers', f'{i}.png'), f'{i}/expected.png',
                         [code(f'{i}/main.js', read(f'openlayers/{i}.js'))])
                    for i in ('circle-style', 'layer-vector-polygon', 'icon-sprite')])


def primer_react():
    h = head('https://github.com/primer/react/tree/main/.playwright/snapshots', 'primer/react')
    return demo(h, [card(raw('primer-react', f'{i}.png'), f'{i}-Default-light-linux.png',
                         [code(f'{i}.test.ts', read(f'primer-react/{i}.test.ts'))])
                    for i in ('Avatar', 'ActionList', 'Dialog')])


def js13kgames():
    h = head('https://js13kgames.com/2024/games', 'js13kgames.com')
    items = [('1.jpg', '6174'), ('3.jpg', 'economy-of-motion'), ('7.jpg', 'monster-steps'), ('6.jpg', 'emojiphobia'),
             ('2.jpg', 'great-plumber-65'), ('5.jpg', 'bounty-islands'), ('4.jpg', 'cooler'), ('8.jpg', 'ghosted')]
    return demo(h, [card(f'js13kgames/{im}', f'{i}/index.html', [code('index.html', read(f'js13kgames/{i}.html'))])
                    for im, i in items])


def hf_spaces():
    h = head('https://huggingface.co/spaces', 'HuggingFace Spaces')
    items = [('hf-spaces/1.jpg', 'victor/deepsite-gallery', 'victor_deepsite-gallery'),
             ('hf-spaces/3.jpg', 'CompVis/stable-diffusion-license', 'CompVis_stable-diffusion-license'),
             (None, 'Xenova/whisper-web', 'Xenova_whisper-web')]
    return demo(h, [card(im, name, [code('index.html', read(f'hf-spaces/{f}.html'))]) for im, name, f in items])


def from_cards(slug):
    """通用 builder：新来源只交 samples_src/<slug>/cards.json + 原始文件，不再单写函数。
    {"link": 数据集链接, "id": 标题栏显示名,            （多个仓库时改用 "links": [[显示名, 链接], ...]）
     "cards": [{"img": 原图文件名或 null, "name": 原始文件名, "code": [[字段名或文件名, 原始内容文件], ...]}]}
    """
    m = json.loads(read(f'{slug}/cards.json'))
    links = m.get('links') or [[m['id'], m['link']]]
    return demo('<b>数据样例</b> · ' + ' · '.join(f'<a href="{u}">{t}</a>' for t, u in links),
                [card(c.get('img') and raw(slug, c['img']), c['name'],
                      [code(label, read(f'{slug}/{f}')) for label, f in c.get('code', [])])
                 for c in m['cards']])


BUILDERS = {
    'js13kgames': js13kgames,
    'hf-spaces': hf_spaces,
    'chartjs': chartjs,
    'openlayers': openlayers,
    'primer-react': primer_react,
    'design2code': design2code,
    'design2code-hard': design2code_hard,
    'sketch2code': sketch2code,
    'web2code': web2code,
}
BUILDERS.update({s: (lambda s=s: from_cards(s)) for s in sorted(os.listdir(SRC))
                 if s not in BUILDERS and os.path.isfile(os.path.join(SRC, s, 'cards.json'))})


def main():
    want = sys.argv[1:] or sorted(BUILDERS)
    os.makedirs(OUT, exist_ok=True)
    for slug in want:
        text = BUILDERS[slug]()
        assert '\n' not in text, f'{slug}: 组件里有换行'
        p = os.path.join(OUT, f'{slug}.html')
        open(p, 'w', encoding='utf-8').write(text)
        print(f'  {slug:18} {len(text) / 1024:6.1f} KB  {text.count("ds-card")} 卡')
    if sys.argv[1:]:
        return
    for f in sorted(os.listdir(OUT)):
        if not f.endswith('.html') or f[:-5] in BUILDERS:
            continue
        p = os.path.join(OUT, f)
        text = open(p, encoding='utf-8').read()
        if strip(text) != text:
            open(p, 'w', encoding='utf-8').write(strip(text))
            print(f'  {f[:-5]:18} 去掉说明文字（手写组件）')


if __name__ == '__main__':
    main()

