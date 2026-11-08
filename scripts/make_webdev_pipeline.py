#!/usr/bin/env python3
"""Adapt BlenderWorld's original four-column layout to temp.md's Web workflow.

The original evaluation-pipeline.drawio is the unmodified layout source. Reuse
its containers, icons, colours and editable cells, replacing Blender-specific
content and evidence. Usage: python scripts/make_webdev_pipeline.py [build|preview]
Dependencies: Pillow; preview also requires Playwright and Chromium.
"""
import base64
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'assets/figures'
SRC = ROOT / 'middle_processing/figure_src/webdev-pipeline'
NAME, TITLE = 'webdev-pipeline', 'WebDev workflow'


def build():
    tree = ET.parse(FIG / 'evaluation-pipeline.drawio')
    diagram = tree.find('diagram')
    diagram.set('id', NAME)
    diagram.set('name', TITLE)
    root = tree.find('.//mxGraphModel/root')
    cells = {c.get('id'): c for c in root.findall('mxCell')}

    def style(key, **changes):
        cell = cells[key]
        values = dict(item.split('=', 1) for item in cell.get('style', '').split(';') if '=' in item)
        values.update({k: str(v) for k, v in changes.items()})
        cell.set('style', ''.join(f'{k}={v};' for k, v in values.items()))

    def text(key, value, size=None):
        cells[key].set('value', value)
        if size:
            style(key, fontSize=size)

    def geometry(key, **changes):
        cells[key].find('mxGeometry').attrib.update({k: str(v) for k, v in changes.items()})

    def image(key, filename):
        # Fit, rather than stretch, real screenshots; embed them for offline use.
        box = cells[key].find('mxGeometry')
        size = tuple(round(float(box.get(k)) * 3) for k in ['width', 'height'])
        im = Image.open(SRC / filename).convert('RGB')
        im.thumbnail(size, Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', size, '#f8fafc')
        canvas.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
        data = io.BytesIO()
        canvas.save(data, 'PNG')
        style(key, image='data:image/png,' + base64.b64encode(data.getvalue()).decode())

    # 1. Agent capabilities: browser MCP or direct CDP scripts, plus shell.
    text('c19', 'Browser + shell', 29)
    text('c20', 'Write files / run commands', 22)
    text('c21', 'Read DOM / accessibility', 22)
    text('c22', 'Interact + read back / capture', 20)
    text('c23', 'Browser MCP / CDP scripts', 21)
    text('c25', 'Write, open, interact,<br>inspect &amp; refine<br><font size="2">* Video optional</font>', 22)
    text('c31', 'Project', 24)
    text('c33', 'Video*', 24)
    image('c29', 'shot_before.png')
    image('c30', 'shot_after.png')

    # 2. Independent evidence, not the tested agent's own screenshots.
    text('c39', 'Unpack &amp;<br>build / serve', 33)
    text('c40', 'Install deps; localize assets', 22)
    text('c41', 'Entry fails → 0 (L0)', 24)
    # One fixed viewport: render settings sit inside the box, above the captures.
    text('c44', 'Independent<br>browser render', 31)
    for key in ['c45', 'c46', 'c47', 'c48', 'c49', 'c53']:
        root.remove(cells[key])
    text('c54', 'Fixed browser + fonts<br>Freeze time / randomness<br>First screen + full page<br>DOM / styles', 20)
    geometry('c54', x=28, y=408, width=310, height=110)
    for key, x, filename in [('c50', 48, 'shot_before.png'), ('c51', 140, 'shot_after.png'), ('c52', 232, 'shot_dom.png')]:
        geometry(key, x=x, y=532, width=82, height=80)
        image(key, filename)
    geometry('c42', height=330)
    text('c57', 'Non-blank · no errors', 21)

    # 3. Preserve the original two-judge diagram, gate the Aesthetics branch.
    text('c60', 'Verifier · Functionality &amp; Aesthetics', 30)
    text('c72', 'Functionality', 34)
    for key, filename in [('c64', 'shot_desk.png'), ('c65', 'shot_dom.png'), ('c66', 'shot_after.png')]:
        image(key, filename)
    text('c67', 'Viewport shots', 22)
    text('c68', 'DOM / styles', 22)
    text('c69', 'Interaction frames', 21)
    text('c73', 'L0 → L1 → L2 → L3', 22)
    # Three judges side by side: Program (assertions / scripts), Agent (multi-step), VLM (pixels only).
    def clone(key, new_id):
        c = copy.deepcopy(cells[key])
        c.set('id', new_id)
        root.append(c)
        cells[new_id] = c
        return new_id
    for key, x in [('c74', 58), ('c79', 442)]:
        geometry(key, x=x, width=182)
    clone('c74', 'c74b'); geometry('c74b', x=250, width=182)
    gear = dict(item.split('=', 1) for item in cells['c18'].get('style').split(';') if '=' in item)['image']
    clone('c75', 'c75b'); geometry('c75b', x=256, y=350, width=36, height=30)
    style('c75', image=gear); geometry('c75', x=64, y=350, width=32, height=30)
    geometry('c80', x=448, y=350, width=36, height=28)
    for key, x, title in [('c76', 100, 'Program'), ('c81', 484, 'VLM')]:
        text(key, title, 26); geometry(key, x=x, width=140)
    clone('c76', 'c76b'); text('c76b', 'Agent', 26); geometry('c76b', x=292, width=140)
    for key, x, line in [('c77', 58, 'DOM / style asserts'), ('c78', 58, 'Scripted clicks'),
                         ('c82', 442, 'Screenshot only'), ('c83', 442, 'Describe → compare')]:
        text(key, line, 18); geometry(key, x=x, width=182)
    clone('c77', 'c77b'); text('c77b', 'Multi-step flows', 18); geometry('c77b', x=250, width=182)
    clone('c78', 'c78b'); text('c78b', 'Explore, read back', 18); geometry('c78b', x=250, width=182)
    # Bracket: left and right box centres, plus a tick from the middle box; arrow down from the middle.
    pts = cells['c117'].find('mxGeometry')
    pts.find("mxPoint[@as='sourcePoint']").attrib.update(x='1029', y='466')
    pts.find("mxPoint[@as='targetPoint']").attrib.update(x='1413', y='466')
    pts.find('Array')[0].attrib.update(x='1029', y='476')
    pts.find('Array')[1].attrib.update(x='1413', y='476')
    clone('c117', 'c117b')
    tick = cells['c117b'].find('mxGeometry')
    tick.remove(tick.find('Array'))
    tick.find("mxPoint[@as='sourcePoint']").attrib.update(x='1221', y='466')
    tick.find("mxPoint[@as='targetPoint']").attrib.update(x='1221', y='476')
    arrow = cells['c118'].find('mxGeometry')
    arrow.find("mxPoint[@as='sourcePoint']").attrib.update(x='1221', y='476')
    arrow.find("mxPoint[@as='targetPoint']").attrib.update(x='1221', y='498')
    text('c84', 'Each item: 0 / 1 · ALL pass to continue', 25)
    text('c87', 'Aesthetics · L4', 28)
    geometry('c87', width=425)
    text('c89', 'Pre-check → pairwise among passers', 23)
    geometry('c89', x=65, width=540)
    text('c90', 'Layout / colour / type / spacing / responsive*', 20)
    geometry('c90', x=65, y=667, width=540)
    text('c88', 'VLM', 23)
    # The checklist is decomposed from the task by the Critic once per task, then frozen for the whole group.
    note = ET.SubElement(root, 'mxCell', {
        'id': 'c_checklist', 'value': 'Critic → checklist · per task, frozen', 'vertex': '1', 'parent': 'c58',
        'style': 'text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;align=left;verticalAlign=middle;'
                 'fontFamily=Nunito;fontSource=https%3A%2F%2Ffonts.googleapis.com%2Fcss%3Ffamily%3DNunito;'
                 'fontSize=19;fontColor=#3D5A91;fontStyle=2;spacing=0;'})
    ET.SubElement(note, 'mxGeometry', {'x': '345', 'y': '241', 'width': '300', 'height': '40', 'as': 'geometry'})
    # The original arrow bypassed Rubric. Start it at the Rubric output instead.
    edge = cells['c116'].find('mxGeometry')
    edge.find("mxPoint[@as='sourcePoint']").attrib.update(x='1217', y='550')
    edge.find('Array')[0].attrib.update(x='897', y='550')

    # 4. All-or-nothing functionality gate times the aesthetic bonus.
    text('c93', 'Reward', 40)
    text('c96', 'Functionality gate', 28)
    text('c97', 'L0–L3 must ALL pass', 24)
    text('c98', 'g ∈ {0, 1} · fail → 0', 27)
    text('c99', '×', 36)
    text('c102', 'Aesthetics bonus', 29)
    text('c103', 'Pairwise among passers', 23)
    text('c104', '1 + λw,  w ∈ [0, 1]', 26)
    text('c106', 'Gated reward', 30)
    text('c107', 'r = g × (1 + λw)', 29)
    text('c110', 'Passers rank first', 27)
    text('c111', '0 ≤ λ ≤ 1 · suggested, unmeasured<br>* Aesthetic dimensions provisional', 18)
    geometry('c111', y=656, height=47)
    out = FIG / f'{NAME}.drawio'
    tree.write(out, encoding='utf-8', xml_declaration=True)
    print(f'build: {out} ({len(root)} editable cells)')


def preview():
    from playwright.sync_api import sync_playwright
    xml = (FIG / f'{NAME}.drawio').read_text()
    cfg = json.dumps({'xml': xml, 'toolbar': '', 'nav': False, 'resize': False, 'border': 0})
    viewer = SRC / '_viewer.html'
    viewer.write_text('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">'
                      f'<div id="g" class="mxgraph" data-mxgraph={quoteattr(cfg)}></div>'
                      '<script src="viewer-static.min.js"></script>')
    chrome = os.environ.get('CHROME_BIN')
    if not chrome:
        candidates = sorted(Path('/root/.cache/puppeteer/chrome-headless-shell').glob(
            '*/chrome-headless-shell-linux64/chrome-headless-shell'))
        chrome = str(candidates[-1]) if candidates else None
    proxy = os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY')
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chrome, args=['--no-sandbox'],
                                        proxy={'server': proxy} if proxy else None)
            page = browser.new_page(viewport={'width': 2040, 'height': 800}, device_scale_factor=1.5)
            page.goto(viewer.as_uri(), wait_until='load')
            page.wait_for_selector('#g svg', timeout=60000)
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(2000)
            png = page.locator('#g svg').first.screenshot()
            browser.close()
        im = Image.open(io.BytesIO(png)).convert('RGB')
        im.thumbnail((2800, 2800), Image.Resampling.LANCZOS)
        im.save(FIG / f'{NAME}.jpg', 'JPEG', quality=92, optimize=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/make_drawio_embed.py'), NAME, TITLE], check=True)
        print(f'preview: {FIG / (NAME + ".jpg")}')
    finally:
        viewer.unlink(missing_ok=True)


if __name__ == '__main__':
    steps = {'build': build, 'preview': preview}
    for step in sys.argv[1:] or steps:
        steps[step]()

