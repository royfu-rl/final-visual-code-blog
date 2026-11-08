#!/usr/bin/env python3
"""2.4 Website 的数据样例原始文件 -> middle_processing/samples_src/<slug>/

只下载数据源自带的东西（原图、原始代码、原始元数据），不做任何改写。
每个来源从候选里按顺序取前 6 条能抓到的，写成 cards.json，交给 build_samples.py 的 from_cards 生成卡片。
科研用途：非商用许可（如 Shadertoy 默认 CC BY-NC-SA）也收，许可以数据自带的字段为准。
不调 GitHub API（匿名额度 60 次/小时），只走 raw.githubusercontent.com。

用法：python3 scripts/fetch_showcase_samples.py [slug ...]   不带参数就全抓
"""
import io
import json
import os
import re
import subprocess
import sys
import tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'middle_processing', 'samples_src')
GH = 'https://raw.githubusercontent.com'
N = 6


def get(url, dst=None, rng=None):
    """curl -L；dst 为空时返回字节"""
    cmd = ['curl', '-sfgL', '-m', '180', url] + (['-r', rng] if rng else [])
    if dst:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        subprocess.run(cmd + ['-o', dst], check=True)
        return dst
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def text(url):
    return get(url).decode('utf-8', 'ignore')


def ext(url):
    return os.path.splitext(url.split('?')[0])[1] or '.png'


def take(cands, fn):
    """按顺序试候选，失败的跳过，凑满 N 条为止"""
    out = []
    for c in cands:
        if len(out) == N:
            break
        try:
            item = fn(c)
        except (subprocess.CalledProcessError, KeyError, AttributeError, IndexError, ValueError) as e:
            print(f'    skip {str(c)[:80]}: {type(e).__name__}')
            continue
        if item:
            out.append(item)
    return out


def first(repo, paths):
    """仓库里第一个存在的文件 -> (分支, 路径)"""
    for br in ('main', 'master', 'dev'):
        for p in paths:
            if subprocess.run(['curl', '-sfgIL', '-m', '30', f'{GH}/{repo}/{br}/{p}'], capture_output=True).returncode == 0:
                return br, p
    raise ValueError(repo)


def save(slug, links, cards):
    """links: [[显示名, 链接], ...]；cards: [{"img", "name", "code": [[标签, 文件], ...]}]"""
    json.dump({'links': links, 'cards': cards}, open(f'{SRC}/{slug}/cards.json', 'w'), ensure_ascii=False, indent=1)
    return len(cards)


def gh_links(repos):
    return [[r, f'https://github.com/{r}'] for r in repos]


# ---------------------------------------------------------------- Web ----

def webflow_cloneable():
    def one(n):
        page = text(f'https://webflow.com/made-in-webflow/website/{n}')
        img = re.search(r'name="twitter:image" content="([^"]+)"', page).group(1)
        live = re.search(r'https://[a-z0-9-]+\.webflow\.io', page).group(0)
        get(img, f'{SRC}/webflow-cloneable/{n}{ext(img)}')
        get(live + '/', f'{SRC}/webflow-cloneable/{n}.html')
        return {'img': f'{n}{ext(img)}', 'name': live.replace('https://', ''), 'code': [['index.html', f'{n}.html']]}
    cards = take(['gsap-flip-layout', 'horizontal-scrolling-gsap', 'video-scrub-on-scroll',
                  'gsap-text-scroll-reveal', 'sticky-sections-gsap', 'oma-gsap-hero'], one)
    return save('webflow-cloneable', [['Made in Webflow', 'https://webflow.com/made-in-webflow']], cards)


def codrops():
    def one(repo):
        br, src = first(f'codrops/{repo}', ['src/index.html', 'index.html'])    # 新仓库手写源码在 src/，老仓库在根目录
        get(f'{GH}/codrops/{repo}/{br}/{src}', f'{SRC}/codrops/{repo}.html')
        m = re.search(r'!\[[^\]]*\]\(([^)\s]+)\)', text(f'{GH}/codrops/{repo}/{br}/README.md'))
        img = None
        if m:
            u = m.group(1) if m.group(1).startswith('http') else f'{GH}/codrops/{repo}/{br}/{m.group(1).lstrip("./")}'
            img = f'{repo}{ext(u)}'
            get(u, f'{SRC}/codrops/{img}')
        return {'img': img, 'name': f'codrops/{repo}', 'code': [[src, f'{repo}.html']]}
    cards = take(['OnScrollTypographyAnimations', 'TypeShuffleAnimation', 'ScrollBasedLayoutAnimations',
                  'MagneticButtons', 'ImageGridMotionEffect', 'SlideshowAnimations', 'LineHoverStyles'], one)
    return save('codrops', [['codrops', 'https://github.com/codrops']], cards)


def uiverse():
    def one(p):
        f = p.replace('/', '__')
        get(f'{GH}/uiverse-io/galaxy/main/{p}', f'{SRC}/uiverse/{f}')
        return {'img': None, 'name': p, 'code': [[p.split('/')[-1], f]]}
    cards = take(['Buttons/ChanduOffl_itchy-vampirebat-74.html', 'Cards/05akalan57_thin-sloth-31.html',
                  'loaders/0xnihilism_brown-puma-30.html', 'Checkboxes/010binary_empty-falcon-21.html',
                  'Toggle-switches/3bdel3ziz-T_honest-deer-30.html', 'Inputs/0xnihilism_calm-baboon-55.html',
                  'Forms/3bdel3ziz-T_helpless-wasp-32.html'], one)        # 后几类各取目录里的第一个文件
    return save('uiverse', [['uiverse-io/galaxy', 'https://github.com/uiverse-io/galaxy']], cards)


HUGO = ['adityatelange/hugo-PaperMod', 'nunocoracao/blowfish', 'jpanther/congo', 'luizdepra/hugo-coder',
        'hugo-sid/hugo-blog-awesome', 'zhaohuabing/hugo-theme-cleanwhite']


def hugo_themes():
    def one(repo):                     # Hugo 主题库要求每个主题自带 images/screenshot.png
        key = repo.replace('/', '__')
        br, lay = first(repo, ['layouts/index.html', 'layouts/_default/baseof.html', 'layouts/baseof.html'])
        get(f'{GH}/{repo}/{br}/images/screenshot.png', f'{SRC}/hugo-themes/{key}.png')
        get(f'{GH}/{repo}/{br}/{lay}', f'{SRC}/hugo-themes/{key}.html')
        return {'img': f'{key}.png', 'name': f'{repo} · images/screenshot.png', 'code': [[lay, f'{key}.html']]}
    return save('hugo-themes', gh_links(HUGO), take(HUGO, one))


OSS = [  # (仓库, 首页源码, 图片：URL 或 live:<线上地址> 表示取线上页面的 og:image)
    ('supabase/supabase', 'apps/www/app/(home)/page.tsx', 'https://supabase.com/images/og/supabase-og.png'),
    ('raycast/ray-so', 'app/(navigation)/(code)/page.tsx', 'live:https://ray.so'),
    ('openai/openai-fm', 'src/app/page.tsx', f'{GH}/openai/openai-fm/main/public/screenshot.jpg'),
    ('resend/react-email', 'apps/web/src/app/page.tsx', 'live:https://react.email'),
    ('payloadcms/website', 'src/app/(frontend)/(pages)/page.tsx', 'live:https://payloadcms.com'),
    ('nuxt/nuxt.com', 'app/pages/index.vue', 'live:https://nuxt.com'),
]


def oss_sites():
    def one(site):
        repo, src, img = site
        key = repo.replace('/', '__')
        if img.startswith('live:'):
            img = re.search(r'<meta[^>]+(?:property|name)="(?:og|twitter):image"[^>]*content="([^"]+)"', text(img[5:])).group(1)
        br, _ = first(repo, [src])
        get(img, f'{SRC}/oss-sites/{key}{ext(img)}')
        get(f'{GH}/{repo}/{br}/{src}', f'{SRC}/oss-sites/{key}{ext(src)}')
        return {'img': f'{key}{ext(img)}', 'name': f'{repo} · {img.split("/")[-1].split("?")[0]}',
                'code': [[src, f'{key}{ext(src)}']]}
    cards = take(OSS, one)
    return save('oss-sites', gh_links([c['name'].split(' · ')[0] for c in cards]), cards)


def shadcn_blocks():
    def one(name):
        d = json.loads(text(f'https://ui.shadcn.com/r/styles/new-york-v4/{name}.json'))
        code = []
        for i, f in enumerate(d['files'][:3]):
            fn = f'{name}__{i}.tsx'
            os.makedirs(f'{SRC}/shadcn-blocks', exist_ok=True)
            open(f'{SRC}/shadcn-blocks/{fn}', 'w').write(f['content'])
            code.append([f['path'], fn])
        return {'img': None, 'name': f'r/styles/new-york-v4/{name}.json', 'code': code}
    cards = take(['login-03', 'signup-03', 'dashboard-01', 'sidebar-07', 'login-04', 'calendar-21', 'sidebar-15'], one)
    return save('shadcn-blocks', [['shadcn/ui blocks', 'https://ui.shadcn.com/blocks']], cards)


def onepagelove():
    """RSS 里最新收录的单页站：OPL 截的首屏图 + 站点线上首页的 HTML"""
    slugs = re.findall(r'<link>https://onepagelove\.com/([a-z0-9-]+)</link>', text('https://onepagelove.com/feed'))

    def one(s):
        page = text(f'https://onepagelove.com/{s}')
        img = re.search(r'<meta property="og:image" content="([^"]+)"', page).group(1)
        live = re.search(r'<a href="([^"]+)"[^>]*title="Visit [^"]*Website"', page).group(1).split('?')[0]
        get(img, f'{SRC}/onepagelove/{s}.jpg')
        get(live, f'{SRC}/onepagelove/{s}.html')
        return {'img': f'{s}.jpg', 'name': f'onepagelove.com/{s} · {img.split("/")[-1]}',
                'code': [[live, f'{s}.html']]}
    return save('onepagelove', [['One Page Love', 'https://onepagelove.com/']], take(slugs, one))


def codepen():
    """CodePen 博客《2026 年上半年趋势》里点名的 pen；截图接口不对外，只取 debug 视图的整页 HTML"""
    def one(pen):
        user, pid = pen.split('/')
        get(f'https://cdpn.io/{user}/debug/{pid}', f'{SRC}/codepen/{pid}.html')
        return {'img': None, 'name': f'{user}/pen/{pid}', 'code': [[f'pen/debug/{pid}', f'{pid}.html']]}
    cards = take(['thebabydino/dPXVyqN', 't_afif/PwGPJOB', 'una/bNeLmoZ', 'cbolson/MYebgqj', 'una/ogzRBWV',
                  't_afif/JoKYwXO'], one)
    return save('codepen', [['codepen.io', 'https://blog.codepen.io/2026/07/03/432-trends-of-2026-so-far/']], cards)


def observable():
    """D3 官方 gallery 的 notebook：文档 API 给缩略图与版本号，再按版本号取导出的 JS"""
    def one(slug):
        d = json.loads(text(f'https://api.observablehq.com/document/@d3/{slug}'))
        js = f'{d["id"]}@{d["version"]}.js'
        get(f'https://static.observableusercontent.com/thumbnail/{d["thumbnail"]}.jpg', f'{SRC}/observable/{d["thumbnail"]}.jpg')
        get(f'https://api.observablehq.com/@d3/{slug}@{d["version"]}.js?v=3', f'{SRC}/observable/{js}')
        return {'img': f'{d["thumbnail"]}.jpg', 'name': f'@d3/{slug}', 'code': [[js, js]]}
    cards = take(['zoomable-sunburst', 'collapsible-tree', 'tree-of-life', 'bar-chart-race', 'zoomable-circle-packing',
                  'hierarchical-edge-bundling', 'force-directed-graph'], one)
    return save('observable', [['observablehq.com', 'https://observablehq.com/@d3/gallery']], cards)


def shadertoy():
    """3DCodeVerse 的 Shadertoy 子集是 webdataset 分片（每片约 300MB），只读几片的开头，按点赞数取前 6"""
    base = 'https://huggingface.co/datasets/ilabai/3dcodeverse/resolve/main/shadertoy'
    pool = {}
    for p in ('33', '3X', '4c', 'Xs', 'ls', 'Md'):
        try:
            data = get(f'{base}/{p}/{p}-00000.tar', rng='0-12000000')
        except subprocess.CalledProcessError:
            continue
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode='r|') as tf:
                for m in tf:
                    sid, _, fn = m.name.partition('/')
                    if m.isfile() and not fn.endswith('.mp4'):
                        pool.setdefault(sid, {})[fn] = tf.extractfile(m).read()
        except (tarfile.ReadError, EOFError):
            pass                                       # 只读了开头，读到截断处为止
    full = {k: v for k, v in pool.items() if {'code.glsl', 'meta.json', 'shader.json'} <= set(v)
            and any(f.startswith('renders/grid') for f in v)}
    likes = lambda v: json.loads(v['shader.json'])['info'].get('likes', 0)
    cards = []
    for sid, v in sorted(full.items(), key=lambda kv: -likes(kv[1]))[:N]:
        grid = max((f for f in v if f.startswith('renders/grid')), key=lambda f: len(v[f]))   # 取信息量最大的一帧
        for name, data in ((f'{sid}.png', v[grid]), (f'{sid}.glsl', v['code.glsl']), (f'{sid}.meta.json', v['meta.json'])):
            os.makedirs(f'{SRC}/shadertoy', exist_ok=True)
            open(f'{SRC}/shadertoy/{name}', 'wb').write(data)
        cards.append({'img': f'{sid}.png', 'name': f'shadertoy/{sid[:2]}/{sid}/{grid}',
                      'code': [['code.glsl', f'{sid}.glsl'], ['meta.json', f'{sid}.meta.json']]})
    return save('shadertoy', [['ilabai/3dcodeverse · shadertoy', 'https://huggingface.co/datasets/ilabai/3dcodeverse']], cards)


# ----------------------------------------------------------------- 3D ----

def threejs_examples():
    def one(n):
        get(f'{GH}/mrdoob/three.js/dev/examples/screenshots/{n}.jpg', f'{SRC}/threejs-examples/{n}.jpg')
        get(f'{GH}/mrdoob/three.js/dev/examples/{n}.html', f'{SRC}/threejs-examples/{n}.html')
        return {'img': f'{n}.jpg', 'name': f'examples/screenshots/{n}.jpg', 'code': [[f'examples/{n}.html', f'{n}.html']]}
    cards = take(['webgpu_compute_cloth', 'webgpu_tsl_vfx_linkedparticles', 'webgpu_tsl_procedural_terrain',
                  'webgpu_tsl_galaxy', 'webgpu_tsl_raging_sea', 'webgl_shaders_ocean', 'webgpu_volume_cloud',
                  'webgl_gpgpu_birds'], one)
    return save('threejs-examples', [['mrdoob/three.js', 'https://github.com/mrdoob/three.js/tree/dev/examples']], cards)


def pmndrs_examples():
    def one(n):
        b = f'{GH}/pmndrs/examples/main/examples/{n}'
        get(f'{b}/thumbnail.webp', f'{SRC}/pmndrs-examples/{n}.webp')
        get(f'{b}/src/App.tsx', f'{SRC}/pmndrs-examples/{n}.App.tsx')
        return {'img': f'{n}.webp', 'name': f'examples/{n}/thumbnail.webp',
                'code': [[f'examples/{n}/src/App.tsx', f'{n}.App.tsx']]}
    cards = take(['caustics', 'aquarium', 'instanced-vertex-colors', 'diamond-refraction', 'portal-shapes',
                  'the-three-graces', 'racing-game', 'water-shader'], one)
    return save('pmndrs-examples', [['pmndrs/examples', 'https://github.com/pmndrs/examples']], cards)


def threedcode():
    base = 'https://huggingface.co/datasets/YipengGao/3DCode/resolve/main/3DCodeData'

    def one(n):
        get(f'{base}/{n}/renders/Image_005.webp', f'{SRC}/3dcode/{n}.webp')
        get(f'{base}/{n}/{n}.py', f'{SRC}/3dcode/{n}.py')
        get(f'{base}/{n}/captions/caption_object.txt', f'{SRC}/3dcode/{n}.caption_object.txt')
        return {'img': f'{n}.webp', 'name': f'3DCodeData/{n}/renders/Image_005.webp',
                'code': [[f'{n}.py', f'{n}.py'], ['captions/caption_object.txt', f'{n}.caption_object.txt']]}
    cards = take(['ArmChair_000', 'Bathtub_000', 'Beetle_000', 'FallenTree_000', 'KitchenIsland_000',
                  'CantileverStaircase_000'], one)
    return save('3dcode', [['YipengGao/3DCode', 'https://huggingface.co/datasets/YipengGao/3DCode']], cards)


WEBGL = [  # Experiments with Google / Chrome Experiments 里宽松许可的仓库：(仓库, 图片候选, 代码候选)
    ('PavelDoGreat/WebGL-Fluid-Simulation', ['screenshot.jpg'], ['script.js']),
    ('amandaghassaei/OrigamiSimulator', ['assets/doc/crane.gif'], ['js/dynamic/dynamicSolver.js']),
    ('edankwan/The-Spirit', ['app/images/screenshot.jpg'], ['src/3d/particles.js']),
    ('edankwan/hyper-mix', ['app/images/screenshot.jpg'], ['src/3d/particles.js', 'src/3d/simulator.js', 'src/3d/floor.js']),
    ('amandaghassaei/VortexShedding', ['README'], ['js/main.js', 'main.js']),
]   # evanw/webgl-water、jwagner/terrain 没有许可证，不收


def webgl_experiments():
    def one(item):
        repo, imgs, codes = item
        key = repo.replace('/', '__')
        br, cp = first(repo, codes)
        if imgs == ['README']:                         # 没有固定截图的仓库，取 README 里的第一张图
            readme = text(f'{GH}/{repo}/{br}/README.md')
            u = re.search(r'!\[[^\]]*\]\(([^)\s]+)\)|<img[^>]+src="([^"]+)"', readme)
            u = u.group(1) or u.group(2)
            ip, u = u, (u if u.startswith('http') else f'{GH}/{repo}/{br}/{u.lstrip("./")}')
        else:
            _, ip = first(repo, imgs)
            u = f'{GH}/{repo}/{br}/{ip}'
        get(u, f'{SRC}/webgl-experiments/{key}{ext(u)}')
        get(f'{GH}/{repo}/{br}/{cp}', f'{SRC}/webgl-experiments/{key}.js')
        return {'img': f'{key}{ext(u)}', 'name': f'{repo} · {ip.split("/")[-1]}', 'code': [[cp, f'{key}.js']]}
    cards = take(WEBGL, one)
    return save('webgl-experiments', gh_links([c['name'].split(' · ')[0] for c in cards]), cards)


def cgart():
    def one(st):
        key = st.replace('/', '__')
        for t in ('start', 'done'):
            get(f'{GH}/CGArtPython/blender_plus_python/main/{st}_{t}.py', f'{SRC}/cgart/{key}_{t}.py')
        b = os.path.basename(st)
        return {'img': None, 'name': os.path.dirname(st) + '/',
                'code': [[f'{b}_start.py', f'{key}_start.py'], [f'{b}_done.py', f'{key}_done.py']]}
    cards = take(['art_projects/truchet_tiles/truchet_tiles', 'loop_of_rings/loop_of_rings',
                  'geo_nodes/subdivided_triangulated_cube/subdivided_triangulated_cube_part_1',
                  'hex_delay/hex_delay', 'stack_spin/stack_spin', 'weave/weave'], one)
    return save('cgart', [['CGArtPython/blender_plus_python', 'https://github.com/CGArtPython/blender_plus_python']], cards)


def polyhaven():
    """按下载量取前 6 个模型"""
    assets = json.loads(text('https://api.polyhaven.com/assets?t=models'))
    top = sorted(assets, key=lambda a: -assets[a].get('download_count', 0))

    def one(a):
        get(f'https://cdn.polyhaven.com/asset_img/thumbs/{a}.png?width=512&height=512', f'{SRC}/polyhaven/{a}.png')
        files = json.loads(text(f'https://api.polyhaven.com/files/{a}'))
        keep = {k: {'1k': files[k]['1k']} for k in ('blend', 'gltf') if '1k' in files.get(k, {})}
        json.dump(keep, open(f'{SRC}/polyhaven/{a}.files.json', 'w'), indent=1)   # 只截取 1k 的 blend / gltf，字段原样
        return {'img': f'{a}.png', 'name': f'asset_img/thumbs/{a}.png',
                'code': [[f'api.polyhaven.com/files/{a}', f'{a}.files.json']]}
    return save('polyhaven', [['Poly Haven', 'https://polyhaven.com/models']], take(top, one))


def gltf_samples():
    base = f'{GH}/KhronosGroup/glTF-Sample-Assets/main/Models'
    idx = json.loads(text(f'{base}/model-index.json'))
    show = [m for m in idx if 'showcase' in m.get('tags', []) and m.get('screenshot') and 'glTF' in m.get('variants', {})]

    def one(m):
        n, shot, g = m['name'], m['screenshot'], m['variants']['glTF']
        get(f'{base}/{n}/{shot}', f'{SRC}/gltf-samples/{n}{ext(shot)}')
        get(f'{base}/{n}/glTF/{g}', f'{SRC}/gltf-samples/{n}.gltf')
        return {'img': f'{n}{ext(shot)}', 'name': f'Models/{n}/{shot}', 'code': [[f'glTF/{g}', f'{n}.gltf']]}
    return save('gltf-samples', [['KhronosGroup/glTF-Sample-Assets', 'https://github.com/KhronosGroup/glTF-Sample-Assets']],
                take(show, one))


def sketchfab():
    """精选 + 可下载 + CC BY，按点赞排；带 NoAI 标签的不用"""
    res = json.loads(text('https://api.sketchfab.com/v3/search?type=models&staffpicked=true&downloadable=true'
                          '&license=by&sort_by=-likeCount&count=24'))['results']
    keys = ('name', 'uid', 'viewerUrl', 'license', 'faceCount', 'vertexCount', 'animationCount', 'likeCount',
            'viewCount', 'publishedAt', 'staffpickedAt', 'archives')

    def one(r):
        if 'noai' in {t['name'].lower() for t in r.get('tags', [])}:
            return None
        thumb = max((i for i in r['thumbnails']['images'] if i['width'] <= 1024), key=lambda i: i['width'])['url']
        get(thumb, f'{SRC}/sketchfab/{r["uid"]}.jpg')
        keep = {k: r.get(k) for k in keys}
        keep.update(user=r['user']['username'], tags=[t['name'] for t in r['tags']], categories=[c['name'] for c in r['categories']])
        json.dump(keep, open(f'{SRC}/sketchfab/{r["uid"]}.json', 'w'), ensure_ascii=False, indent=1)
        return {'img': f'{r["uid"]}.jpg', 'name': r['name'],     # viewerUrl 里的 slug 是 none，用记录自带的 name
                'code': [['api.sketchfab.com/v3/search', f'{r["uid"]}.json']]}
    return save('sketchfab', [['Sketchfab Staff Picks', 'https://sketchfab.com/3d-models/popular']], take(res, one))


FETCHERS = {'codepen': codepen, 'observable': observable, 'webflow-cloneable': webflow_cloneable, 'codrops': codrops, 'uiverse': uiverse, 'hugo-themes': hugo_themes,
            'oss-sites': oss_sites, 'shadcn-blocks': shadcn_blocks, 'onepagelove': onepagelove, 'shadertoy': shadertoy,
            'threejs-examples': threejs_examples, 'pmndrs-examples': pmndrs_examples, '3dcode': threedcode,
            'webgl-experiments': webgl_experiments, 'cgart': cgart, 'polyhaven': polyhaven,
            'gltf-samples': gltf_samples, 'sketchfab': sketchfab}

if __name__ == '__main__':
    for slug in sys.argv[1:] or FETCHERS:
        os.makedirs(f'{SRC}/{slug}', exist_ok=True)
        try:
            print(f'  {slug:18} {FETCHERS[slug]()} 条')
        except (subprocess.CalledProcessError, KeyError, AttributeError, ValueError) as e:
            print(f'  {slug:18} 失败：{type(e).__name__} {e}')

