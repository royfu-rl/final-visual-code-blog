#!/usr/bin/env python3
"""parts/<chapter>/*.md + data/*.json -> <chapter>/<chapter>.md

V2 的章节结构和 V1 不同：按产物技术栈切分，不按「场景」切分。
  Web(2D)  html / webdev / ppt / manim
  3D       blender / 3js / cad
  Video    video_web / video_blender

每章一个页面，章内小节用 template.html 的 .env-view 做视图切换；小节里的总表按
bucket 分组，用 .tbl-tabs 做组内切换。正文写在 parts/<chapter>/<view>.md，表格靠
标记插入，生成的章节 md 不要手改。

标记：
  <!--BENCH:html,webdev-->   按这些 bucket 各出一张 benchmark 表，带切换按钮
  <!--PIPE:html,webdev-->    同上，出数据管线表
  单个 bucket 也走同一套（只有一个 pane，按钮条仍然渲染，给出条数）
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PARTS = os.path.join(ROOT, "parts")
MID = os.path.join(ROOT, "middle_processing")
LOGOS = os.path.join(ROOT, "assets", "logos")

# ---------------------------------------------------------------------------
# 章节与视图
# ---------------------------------------------------------------------------

# (chapter_dir, 页面主标题, [(view_key, 按钮名)])
CHAPTERS = [
    ("web", "Web (2D)", [
        ("bench",    "Benchmark",
         "各家模型在 Web 公开基准上的成绩，厂商自报与榜单排名并列。"),
        ("opendata", "Open Data",
         "按产物技术栈盘点公开的数据管线与 benchmark：35 条管线压在截图转代码这一格，多文件工程只有 2 条。"),
        ("data",     "Sources",
         "素材从哪来、怎么筛；同一份资产可拆成 Query、Verifier 参考答案或 Hint。"),
        ("verifier", "Verifier",
         "给轨迹打 reward 的那一半：功能性按 L0–L3 逐条判，审美性照带示例的专家 rubric 两两比较。"),
        ("train",    "Train",
         "Agent Data = ⟨Query, Multi-Turn Trajectory⟩。运行环境怎么搭，一对配对数据的四种花法，选题与蒸馏。"),
    ]),
    ("3d", "3D", [
        ("bench",    "Benchmark",
         "按真值来源分三类读公开基准：blender 与 3js 是主力，cad 辅助。"),
        ("opendata", "Open Data",
         "别人做过的数据管线：blender 12 条、cad 8 条，3js 一条都没有。"),
        ("data",     "Sources",
         "素材从哪来、怎么筛；3D 资产多、代码少，题目主力靠合成。"),
        ("verifier", "Verifier",
         "给轨迹打 reward 的那一半：读场景图，不读渲染图。"),
        ("train",    "Train",
         "运行环境怎么搭：Blender 按版本分叉，three.js 不必。"),
    ]),
    # 3D 的改写版：照 Web (2D) 的表达、表格、标题与结构重写，和 3d 并存，方便对比
    ("3d-v2", "3D", [
        ("bench",    "Benchmark",
         "各家模型在 3D 公开基准上的成绩，厂商自报与榜单排名并列。"),
        ("opendata", "Open Data",
         "按产物技术栈盘点公开的数据管线与 benchmark：blender 12 条、cad 8 条，3js 一条都没有。"),
        ("data",     "Sources",
         "素材从哪来、怎么筛；3D 资产多、代码少，题目主力靠合成。"),
        ("verifier", "Verifier",
         "给轨迹打 reward 的那一半：功能性按 L0–L3 读场景状态逐条判，审美性只在通过者之间两两比较。"),
        ("train",    "Train",
         "Agent Data = ⟨Query, Multi-Turn Trajectory⟩。运行环境怎么搭，配对数据怎么用，低 reward 怎么归因。"),
    ]),
    ("video", "Video", [
        ("vibe",         "Vibe Video",
         "社区怎么让 agent 写代码出片：9 类场景的做法与成片，加 24 个开源项目。"),
        ("from-web",     "From Web",
         "每一帧是帧号与代码的纯函数，所以这条线能写硬判据。"),
        ("from-blender", "From Blender",
         "公开素材是空的；判据只能从活状态里读，不能从渲染帧里读。"),
    ]),
]

# bucket → (按钮名, 一句说明)
BUCKETS = {
    "html":    ("HTML", "单文件产物：截图 / 设计稿 / 草图转 HTML、SVG、React 组件、图表绘图代码。渲染一次就能比对，判据最成熟。"),
    "webdev":  ("WebDev", "多文件 Web App：从规格或多轮对话生成可运行应用，由浏览器 agent 实测功能与跨页状态。"),
    "ppt":     ("PPT", "幻灯片 / 海报 / 演讲视频代码：python-pptx、Beamer、SlidesLib，产物是版面对象树，可逐对象回读。"),
    "manim":   ("Manim", "代码驱动的讲解动画：Manim 及同类引擎，产物是视频，判据要落在渲染成功、时长与关键帧上。"),
    "blender": ("Blender", "写 Blender Python 建模与编辑场景，产物是场景图，可直接读几何与材质状态。"),
    "3js":     ("Three.js", "浏览器端 3D 代码：three.js 场景、参数化 3D，渲染与几何检查都在无头浏览器里完成。"),
    "cad":     ("CAD", "写 CadQuery 等参数化 CAD 代码，按尺寸、约束、可制造性验收，确定性最高。"),
    "video_web":     ("From Web", "用 Web 技术栈产出动画与视频：Canvas / WebGL / SVG / CSS / Lottie / Remotion / Motion Canvas。"),
    "video_blender": ("From Blender", "用 Blender 与 bpy 产出动画与视频，产物是渲染序列。"),
}

# ---------------------------------------------------------------------------
# 元数据
# ---------------------------------------------------------------------------


def _load_list(*files):
    out = {}
    for f in files:
        p = os.path.join(DATA, f)
        if os.path.isfile(p):
            out.update({m["name"]: m for m in json.load(open(p, encoding="utf-8"))})
    return out


def load_bench_meta():
    meta = _load_list("bench_meta_web.json", "bench_meta_3dgame.json", "bench_meta_video.json")
    lang = {}
    p = os.path.join(DATA, "bench_lang.json")
    if os.path.isfile(p):
        lang.update(json.load(open(p, encoding="utf-8")))
    p = os.path.join(DATA, "bench_lang_verified.json")
    if os.path.isfile(p):
        lang.update({m["name"]: m["lang"] for m in json.load(open(p, encoding="utf-8")) if m.get("lang")})
    for name, l in lang.items():
        if name in meta:
            meta[name]["lang"] = l
    return meta


def load_pipe_meta():
    return _load_list("pipe_meta_web.json", "pipe_meta_3dgame.json", "pipe_meta_video.json")


def load_repo_meta():
    """2.2 的仓库表：自带参考截图的开源仓库，字段与 pipe_meta 同构，多一个 permitted"""
    return _load_list("repo_meta_web.json", "repo_meta_3d.json")


def load_site_meta():
    """2.4 的站点表：和仓库表同构，没有建库日期与 star"""
    return _load_list("site_meta_web.json", "site_meta_3d.json")


def load_buckets():
    p = os.path.join(DATA, "buckets.json")
    if not os.path.isfile(p):
        raise SystemExit("缺 data/buckets.json —— 分类映射还没生成")
    return json.load(open(p, encoding="utf-8"))


def load_urls():
    """name → 原文链接。元数据 json 里没有这一列，从调研原始表的表格行里取。"""
    urls = {}
    for f in ("benchmarks.md", "pipelines.md"):
        p = os.path.join(MID, f)
        if not os.path.isfile(p):
            continue
        for line in open(p, encoding="utf-8"):
            if not line.startswith("|"):
                continue
            for name, url in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", line):
                urls.setdefault(name.strip(), url)
    # 原始表里没有的条目（后补的 benchmark）在这里给规范链接，优先级最高
    p = os.path.join(DATA, "urls_extra.json")
    if os.path.isfile(p):
        urls.update(json.load(open(p, encoding="utf-8")))
    return urls


def load_orgs():
    orgs = {}
    for f in ("orgs_bench_web.json", "orgs_bench_3dgame.json",
              "orgs_pipe_web.json", "orgs_pipe_3dgame.json", "sample_meta_web.json"):
        p = os.path.join(DATA, f)
        if os.path.isfile(p):
            for m in json.load(open(p, encoding="utf-8")):
                orgs[m["name"]] = [o for o in (m.get("industry"), m.get("academic")) if o and o.get("org")]
    return orgs


def load_sample_meta():
    """只做数据样例、不进任何表的条目：机构（同 orgs_*.json 结构）、影响力、链接，供折叠头用"""
    p = os.path.join(DATA, "sample_meta_web.json")
    return {m["name"]: m for m in json.load(open(p, encoding="utf-8"))} if os.path.isfile(p) else {}


ORGS = load_orgs()
URLS = load_urls()
SAMPLE_META = load_sample_meta()

# ---------------------------------------------------------------------------
# 渲染（徽章 / logo 的样式沿用 V1，换页面不换观感）
# ---------------------------------------------------------------------------


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def date_key(d):
    return tuple(int(x) for x in re.findall(r"\d+", d or "")[:3]) + (0, 0)


def link(label, url):
    return f"[{label}]({url})" if url and label else "—"


_HF_DL = ('<svg class="hf-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v11"/><path d="M8 11l4 4 4-4"/>'
          '<path d="M4 20h16"/></svg>')
_HF_LK = ('<svg class="hf-i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21C7 17.5 3 14 3 9.5 3 7 5 5 '
          '7.5 5 9.2 5 10.7 6 12 7.6 13.3 6 14.8 5 16.5 5 19 5 21 7 21 9.5 21 14 17 17.5 12 21z"/></svg>')
_HF_ST = ('<svg class="hf-i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6 6.6.6-5 4.3 1.5 '
          '6.5L12 16.9 6 20.9l1.5-6.5-5-4.3 6.6-.6z"/></svg>')
_HF_ICON = {"dl": _HF_DL, "lk": _HF_LK, "st": _HF_ST}
_HF_TITLE = {"dl": "downloads", "lk": "likes", "st": "GitHub stars"}


def impact_badges(text, url=None):
    if not text:
        return ""
    parts = []
    for key, pat in (("dl", r"([\d.]+\s*[kKmM]?)\s*下载"),
                     ("lk", r"([\d.]+\s*[kKmM]?)\s*likes?"),
                     ("st", r"([\d.]+\s*[kKmM]?)\s*stars?")):
        m = re.search(pat, text)
        if m:
            parts.append((key, m.group(1).replace(" ", "")))
    if parts:
        inner = "".join(f'<span class="hf-b hf-{k}" title="{_HF_TITLE[k]}">{_HF_ICON[k]}{v}</span>'
                        for k, v in parts)
    else:
        inner = f'<span class="hf-b">{text}</span>'
    return f'<a class="hf" href="{url}">{inner}</a>' if url else f'<span class="hf">{inner}</span>'


def org_mark(m, name):
    """工业机构在前、学术在后，各一个 logo；没有 favicon 的用首字母方块。"""
    orgs = ORGS.get(name) or ([{"org": m["org"]}] if (m or {}).get("org") else [])
    if not orgs:
        return "", ' <span class="org">独立作者</span>'
    marks = ""
    for o in orgs:
        f = os.path.join(LOGOS, slug(o["org"]) + ".png")
        if os.path.isfile(f):
            marks += (f'<img height="14" src="../assets/logos/{slug(o["org"])}.png" align="center" '
                      f'alt="" title="{o["org"]}"> ')
        else:
            marks += f'<span class="org-mark" title="{o["org"]}">{o["org"][0].upper()}</span> '
    return marks, ' <span class="org">' + " · ".join(o["org"] for o in orgs) + "</span>"


def _name_cell(name, meta):
    mark, org = org_mark(meta, name)
    url = URLS.get(name)
    label = f"[{name}]({url})" if url else name
    return f"{mark}{label}{org}"


def bench_table(names, meta):
    out = ["| 发布日期 | Benchmark | Download | 任务形态 | 编程语言 | 题目数量 | 影响力 | 考察能力 | Example |",
           "|---|---|---|---|---|---|---|---|---|"]
    rows = []
    for name in names:
        m = meta.get(name, {})
        date = m.get("date", "")
        cells = [date, _name_cell(name, m),
                 link(m.get("download_label"), m.get("download_url")),
                 m.get("task_form") or "—",
                 m.get("lang") or "—",
                 m.get("size") or "—",
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 m.get("capability") or "—",
                 example_cell(name, m)]
        rows.append((date_key(date), "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |"))
    return out + [r for _, r in sorted(rows, key=lambda x: x[0])]


def art_chips(items):
    """artifacts: ["img:image", "run:.html"] -> 彩色标签。家族见 template.html 的 .a-* """
    if not items:
        return "—"
    out = []
    for it in items:
        fam, _, label = it.partition(":")
        out.append(f'<span class="art a-{fam}">{label}</span>')
    return "".join(out)


def pipe_table(names, meta):
    out = ["| 发布日期 | 数据集 / 工作 | Download | Artifacts | Datasize | 影响力 | 特性 / 训练用途 | Example |",
           "|---|---|---|---|--:|---|---|---|"]
    rows = []
    for name in names:
        m = meta.get(name, {})
        date = m.get("date", "")
        cells = [date, _name_cell(name, m),
                 link(m.get("download_label"), m.get("download_url")),
                 art_chips(m.get("artifacts")), m.get("size") or "—",
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 m.get("feature") or m.get("typ") or "—",
                 example_cell(name, m)]
        rows.append((date_key(date), "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |"))
    return out + [r for _, r in sorted(rows, key=lambda x: x[0])]


REPO_HEAD = {    # <!--REPO:<组>--> 的列名改写；没登记的组用仓库表默认列名
    "web-issue": {"建库": "发布", "仓库": "数据集", "Datasize（图 / 码）": "Datasize（题 / 图）"},
}


def repo_table(meta, head=None):
    """2.2 的仓库表：和 2.3 的管线表同一套列，末尾多一列许可。按 star 从多到少。"""
    cols = ["建库", "仓库", "Download", "Artifacts", "Datasize（图 / 码）",
            "影响力", "特性", "Permitted", "Example"]
    cols = [(head or {}).get(c, c) for c in cols]
    out = ["| " + " | ".join(cols) + " |",
           "|---|---|---|---|--:|---|---|---|---|"]
    rows = []
    for name, m in meta.items():
        cells = [m.get("date", ""), _name_cell(name, m),
                 link(m.get("download_label"), m.get("download_url")),
                 art_chips(m.get("artifacts")), m.get("size") or "—",
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 m.get("feature") or "—", m.get("permitted") or "—",
                 example_cell(name, m)]
        rows.append((_to_star(m.get("impact")), "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |"))
    return out + [r for _, r in sorted(rows, key=lambda x: -x[0])]


SITE_GROUPS = {   # 2.4 站点表按类型分组的顺序；没写 group 的条目归第一组
    "web": ["社区站", "可克隆站与教程 demo", "主题、模板与组件库", "开源生产级官网", "获奖画廊"],
    "3d": ["资产站与问答站", "three.js 作品", "WebGL 实验", "Blender 作品与资产"],
}


def site_table(meta):
    """2.4 的站点表：一张表按类型分组，组内按规模从大到小。"""
    chapter = next(iter(meta.values())).get("chapter", "web")
    order = SITE_GROUPS.get(chapter, [])
    out = ["| 类型 | 站点 | 获取方式 | Artifacts | Datasize | 特性 | Permitted | Example |",
           "|---|---|---|---|--:|---|---|---|"]
    groups = {}
    for name, m in meta.items():
        mark, _ = org_mark(m, name)            # 站点的机构名就是站名，只留图标不重复写一遍
        url = URLS.get(name) or m.get("site_url") or m.get("download_url")
        dl = m.get("download_url")
        how = f"[{m.get('download_label')}]({dl})" if dl and dl != url and m.get("download_label") else "—"
        cells = [f"{mark}[{name}]({url})" if url else f"{mark}{name}", how,
                 art_chips(m.get("artifacts")), m.get("size") or "—",
                 m.get("feature") or "—", m.get("permitted") or "—",
                 example_cell(name, m)]
        g = m.get("group") or (order[0] if order else "")
        groups.setdefault(g, []).append((_to_star(m.get("size")), [str(c).replace("|", "/") for c in cells]))
    for g in order + [g for g in groups if g not in order]:
        for i, (_, cells) in enumerate(sorted(groups.get(g, []), key=lambda x: -x[0])):
            out.append("| " + " | ".join([f"**{g}**" if i == 0 else ""] + cells) + " |")
    return out


def _to_star(text):
    m = re.search(r"([\d.]+)\s*([kKmM万]?)", (text or "").replace(",", ""))
    if not m:
        return 0.0
    return float(m.group(1)) * {"k": 1e3, "m": 1e6, "万": 1e4}.get(m.group(2).lower(), 1)


def all_table(bnames, bmeta, pnames, pmeta):
    """benchmark 与数据管线合成一张表：加一列「类型」，按发布日期混排。"""
    out = ["| 发布日期 | 名称 | 类型 | Download | 形态 | 规模 / 题量 | 影响力 | 说明 | Example |",
           "|---|---|---|---|---|---|---|---|---|"]
    rows = []
    for name, m, typ in ([(n, bmeta.get(n, {}), "Benchmark") for n in bnames]
                         + [(n, pmeta.get(n, {}), "数据集") for n in pnames]):
        date = m.get("date", "")
        if typ == "Benchmark":
            form = m.get("task_form") or "—"
            if m.get("lang"):
                form = f'{form}（{m["lang"]}）'
            note = m.get("capability") or "—"
        else:
            form = m.get("form") or m.get("lang") or "—"
            note = m.get("feature") or m.get("typ") or "—"
        cells = [date, _name_cell(name, m), typ,
                 link(m.get("download_label"), m.get("download_url")),
                 form, m.get("size") or "—",
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 note, example_cell(name, m)]
        rows.append((date_key(date), "| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |"))
    return out + [r for _, r in sorted(rows, key=lambda x: x[0])]


def grouped_all(bucket_keys, buckets, bmeta, pmeta):
    """一个 bucket 一张合表（benchmark + 数据管线），外面套 .tbl-tabs 的按钮条。"""
    out = ['<div class="tbl-tabs">', ""]
    for b in bucket_keys:
        bn = sorted([n for n, v in buckets["bench"].items() if v.get("bucket") == b],
                    key=lambda n: date_key(bmeta.get(n, {}).get("date", "")))
        pn = sorted([n for n, v in buckets["pipe"].items() if v.get("bucket") == b],
                    key=lambda n: date_key(pmeta.get(n, {}).get("date", "")))
        label, desc = BUCKETS.get(b, (b, ""))
        out += [f'<div class="tbl-pane" data-label="{label}" data-count="{len(bn) + len(pn)}">', "",
                f'<p class="tbl-desc">{desc}'
                f' 本组 {len(bn)} 条 benchmark、{len(pn)} 条数据管线，按发布日期混排。</p>', ""] \
               + all_table(bn, bmeta, pn, pmeta) + ["", "</div>", ""]
    return out + ["</div>"]


def grouped(kind, bucket_keys, bmap, meta):
    """一个 bucket 一张表，外面套 .tbl-tabs 的按钮条；管线表列多，挂 .wide 突破正文栏。"""
    table = bench_table if kind == "bench" else pipe_table
    out = ['<div class="tbl-tabs">' if kind == "bench" else '<div class="tbl-tabs wide">', ""]
    for b in bucket_keys:
        names = sorted([n for n, v in bmap.items() if v.get("bucket") == b],
                       key=lambda n: date_key(meta.get(n, {}).get("date", "")))
        label, desc = BUCKETS.get(b, (b, ""))
        out += [f'<div class="tbl-pane" data-label="{label}" data-count="{len(names)}">', "",
                f'<p class="tbl-desc">{desc}</p>', ""] + table(names, meta) + ["", "</div>", ""]
    return out + ["</div>"]

# ---------------------------------------------------------------------------
# 装配
# ---------------------------------------------------------------------------

# Artifacts 词表：六个类别（颜色见 template.html 的 .a-*）。标签不在这里写死，
# 由 <!--ARTIFACTS--> 现场从 data/*.json 与各 parts/*.md 里收，收来的就是全书真在用的。
ART_FAMILY = [
    ("img",   "图像",       "已经渲染出来的画面"),
    ("txt",   "文本",       "人写或模型写的自然语言"),
    ("code",  "代码",       "要再经一道工具才出画面的源码与中间表示"),
    ("run",   "可运行件",   "跑一次就出画面的整件"),
    ("asset", "资产",       "几何与贴图，不含代码"),
    ("meta",  "结构化字段", "机器可读、能逐项比对的字段"),
]
_ART_RE = re.compile(r"<!--\s*ARTIFACTS\s*-->")


def _artifact_inventory():
    """全书在用的标签：data/*.json 的 artifacts 字段 + parts 里手写的 <span class="art ...">"""
    import collections
    fam = collections.defaultdict(collections.Counter)
    for f in sorted(os.listdir(DATA)):
        if not f.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        except Exception:
            continue
        for r in d if isinstance(d, list) else []:
            for it in (r or {}).get("artifacts") or []:
                k, _, v = it.partition(":")
                fam[k][v] += 1
    for sub in os.listdir(PARTS):
        d = os.path.join(PARTS, sub)
        # 3d-v2 是 3d 的改写版，表格重复，算进来会打乱词表排序
        if not os.path.isdir(d) or sub.startswith("_") or sub == "3d-v2":
            continue
        for f in os.listdir(d):
            if f.endswith(".md"):
                for k, v in re.findall(r'class="art a-(\w+)">([^<]*)<',
                                       open(os.path.join(d, f), encoding="utf-8").read()):
                    fam[k][v] += 1
    return fam


def fill_artifacts(body):
    """<!--ARTIFACTS--> → Artifacts 词表（既是色标图例，也是规范）"""
    if not _ART_RE.search(body):
        return body
    fam = _artifact_inventory()
    out = ["| 类别 | 含义 | 标签（共 {} 个） |".format(sum(len(v) for v in fam.values())),
           "|---|---|---|"]
    for key, cn, desc in ART_FAMILY:
        tags = [v for v, _ in fam.get(key, {}).most_common()]
        chips = "".join(f'<span class="art a-{key}">{v}</span>' for v in tags) or "—"
        out.append(f"| **{cn}** | {desc} | {chips} |")
    return _ART_RE.sub(lambda _: "\n".join(out), body)


_MARK_RE = re.compile(r"<!--\s*(BENCH|PIPE|ALL)\s*:\s*([\w,\s]+?)\s*-->")
_REPO_RE = re.compile(r"<!--\s*(REPO|SITE)\s*:\s*([\w-]+)\s*-->")


def fill_repos(body, rmeta, smeta):
    """<!--REPO:web--> → 仓库表，<!--SITE:web--> → 站点表；两张都与管线表同列，一样挂 .wide"""
    def repl(m):
        kind, chapter = m.group(1), m.group(2)
        src, fn = (rmeta, repo_table) if kind == "REPO" else (smeta, site_table)
        sel = {n: v for n, v in src.items() if v.get("chapter") == chapter}
        if not sel:
            print(f"  [warn] 没有 chapter={chapter} 的 {kind} 条目，标记留空")
            return ""
        rows = fn(sel, REPO_HEAD.get(chapter)) if kind == "REPO" else fn(sel)
        return "\n".join(['<div class="wide">', ""] + rows + ["", "</div>"])
    return _REPO_RE.sub(repl, body)
_FRONT_RE = re.compile(r"<!--\s*FRONTIER\s*-->")


def fill_tables(body, buckets, bmeta, pmeta):
    def repl(m):
        kind = m.group(1).lower()
        keys = [k.strip() for k in m.group(2).split(",") if k.strip()]
        if kind == "all":
            return "\n".join(grouped_all(keys, buckets, bmeta, pmeta))
        bmap = buckets["bench"] if kind == "bench" else buckets["pipe"]
        meta = bmeta if kind == "bench" else pmeta
        return "\n".join(grouped(kind, keys, bmap, meta))
    return _MARK_RE.sub(repl, body)


_SAMPLE_RE = re.compile(r"<!--\s*SAMPLE:([a-z0-9._-]+)\s*\|\s*([^>]+?)\s*-->")


# ── Example 列 ────────────────────────────────────────────────────────────
# 表里每行挂一个样例缩略图，点开复用 fill_samples 那套弹层（同一个 sg-<slug> 面板）。
# 行名能直接 slug 化对上样例文件的不用登记（Design2Code → design2code）；
# 对不上的在这里补。
SAMPLE_ALIAS = {
    "WebRenderBench / ALISA": "webrenderbench",
    "plotly.js": "plotlyjs",
    "Chart.js": "chartjs",
    "p5.js": "p5js",
    "deck.gl": "deckgl",
    "MapLibre GL JS": "maplibre",
    "Ionic Framework": "ionic",
    "One Page Love": "onepagelove",
    "Poly Haven": "polyhaven",
    "three.js 官方 examples": "threejs-examples",
    "Hugging Face 静态空间": "hf-spaces",
    "主题目录：Astro / Hugo / Jamstack": "hugo-themes",
    "开源的获奖个人站": "oss-sites",
    "Webflow 可克隆站": "webflow-cloneable",
    "shadcn/ui 与 registry": "shadcn-blocks",
    "Uiverse · HyperUI": "uiverse",
    "Khronos glTF-Sample-Assets": "gltf-samples",
    "Experiments with Google": "webgl-experiments",
    "CGArtPython": "cgart",
    "vercel/satori": "satori",
    "SWE-bench Multimodal": "swe-bench-m",
    "Objaverse-XL": "objaverse",
}

_EX_WANT = {}      # slug -> 行名：本视图里 Example 列引用到的样例，视图开头清空


def sample_slug(name):
    """行名 -> 样例 slug；没有对应样例返回 None。"""
    slug = SAMPLE_ALIAS.get(name) or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if (os.path.isfile(os.path.join(MID, "samples", f"{slug}.html"))
            or os.path.isfile(os.path.join(MID, "deep", f"{slug}.md"))):
        return slug
    return None


def _sample_src(slug):
    demo_p = os.path.join(MID, "samples", f"{slug}.html")
    deep_p = os.path.join(MID, "deep", f"{slug}.md")
    demo = open(demo_p, encoding="utf-8").read().strip() if os.path.isfile(demo_p) else ""
    deep = open(deep_p, encoding="utf-8").read().strip() if os.path.isfile(deep_p) else ""
    return demo, deep


def _sample_tile(slug, name, mm, sid, cls="sg-tile", tag="div"):
    """样例方块：封面 + 名称 / 机构 / 影响力 / 样例条数。画廊和 Example 列共用一套。

    Example 列用 span 而不是 div —— 方块要塞进 markdown 表格的单元格里。
    """
    demo, deep = _sample_src(slug)
    marks, org = org_mark(mm, name)
    # .doc img 的 height:auto 会盖掉 height="14"，标题里必须挂 h-logo 才不会撑成原图大小
    marks = (marks.replace('<img height="14" ', '<img class="h-logo" height="20" ')
                  .replace('<span class="org-mark"', '<span class="org-mark h-logo"'))
    flat = lambda t: re.sub(r"[^0-9a-z一-鿿]+", "", t.lower())
    if org and (flat(org) in flat(name) or flat(name) in flat(org)):
        org = ""                       # 机构名和条目名是同一个（站点类），不重复写
    n = demo.count('class="ds-card"')
    poster = _poster(demo, deep) or f'<span class="sg-mono">{name[:1].upper()}</span>'
    return (f'<{tag} class="{cls}" role="button" tabindex="0" data-sg="{sid}">'
            f'<{tag} class="sg-poster">{poster}</{tag}>'
            f'<{tag} class="sg-meta"><span class="deep-title sg-name">{marks}{name}{org}</span>'
            f'<span class="sg-sub">{impact_badges(mm.get("impact"))}'
            f'{f"<span class=sg-n>{n} 条样例</span>" if n else ""}</span></{tag}></{tag}>')


def example_cell(name, mm=None):
    """Example 列的格子：和画廊方块同样的信息，缩到单元格大小。没有样例就是「—」。"""
    slug = sample_slug(name)
    if not slug:
        return "—"
    _EX_WANT[slug] = name
    # sg-tile 让现有的弹层 JS 直接生效，ex-tile 负责缩小
    return _sample_tile(slug, name, mm or {}, f"sg-{slug}",
                        cls="sg-tile ex-tile", tag="span")


_EX_RE = re.compile(r"<!--\s*EX:\s*([^>]+?)\s*-->")


def fill_example_cells(body, meta):
    """<!--EX:<行名>--> → Example 格子，给手写的表格用；弹层照样由 example_panels 补。"""
    return _EX_RE.sub(lambda m: example_cell(m.group(1), meta.get(m.group(1))), body)


def example_panels(body, meta, view):
    """给 Example 列补弹层。

    弹层必须落在**引用它的那个视图里**：.env-view 不激活时是 display:none，
    指向别的视图的 id 打不开；而同一个样例可能在 A 视图进了画廊、又在 B 视图的表里被引用，
    两边都叫 sg-<slug> 就会出现重复 id，getElementById 只取第一个。
    所以：本视图已有画廊弹层的，直接复用；没有的，改挂视图内唯一的 sg-<slug>--<view>。
    """
    out, panels = body, []
    for slug, name in sorted(_EX_WANT.items()):
        if f'id="sg-{slug}"' in body:
            continue                                   # 本视图的画廊已经有了，直接指过去
        sid = f"sg-{slug}--{view}"
        out = out.replace(f'data-sg="sg-{slug}"', f'data-sg="{sid}"')
        panel = _sample_panel(slug, name, meta)
        if panel:
            panels.append(panel.replace(f'id="sg-{slug}"', f'id="{sid}"', 1))
    return out + ("\n\n" + "\n\n".join(panels) + "\n" if panels else "")


def _poster(demo, deep):
    """方块的封面：样例里的第一张原图；没有图就用第一段代码的开头；都没有返回空"""
    m = re.search(r'<img[^>]*?\ssrc="([^"]+)"', demo + deep)
    if m:
        return f'<img loading="lazy" src="{m.group(1)}" alt="">'
    m = re.search(r"<pre>(.*?)</pre>", demo)
    if m:
        return '<pre class="sg-code">' + "&#10;".join(m.group(1).split("&#10;")[:18]) + "</pre>"
    return ""


def _sample_panel(slug, name, meta):
    """样例弹层本体。fill_samples 的方块和 Example 列的小格子都指向它，一个 slug 只出一份。"""
    demo, deep = _sample_src(slug)
    if not (demo or deep):
        return ""
    mm = meta.get(name, {})
    marks, org = org_mark(mm, name)
    marks = (marks.replace('<img height="14" ', '<img class="h-logo" height="20" ')
                  .replace('<span class="org-mark"', '<span class="org-mark h-logo"'))
    flat = lambda t: re.sub(r"[^0-9a-z一-鿿]+", "", t.lower())
    if org and (flat(org) in flat(name) or flat(name) in flat(org)):
        org = ""
    url = URLS.get(name) or mm.get("download_url")
    label = f'<a href="{url}">{name}</a>' if url else name
    demo = demo.replace("<img ", '<img loading="lazy" ')      # 弹层没打开时不加载
    deep = deep.replace("<img ", '<img loading="lazy" ')
    panel = [f'<div class="sg-body" id="sg-{slug}"><div class="sg-bar">'
             f'<span class="deep-title">{marks}{label}{org} '
             f'{impact_badges(mm.get("impact"), mm.get("impact_url"))}</span>'
             '<span class="sg-nav"><button type="button" class="sg-prev" title="上一个（←）">‹</button>'
             '<span class="sg-pos"></span><button type="button" class="sg-next" title="下一个（→）">›</button>'
             '<button type="button" class="sg-x" title="关闭（Esc）">✕</button></span></div><div class="sg-stage">', ""]
    for part in (demo, deep):
        if part:
            panel += [part, ""]
    return "\n".join(panel + ["</div></div>"])


def fill_samples(body, meta):
    """连着的 <!--SAMPLE:<slug>|<条目名>--> 合成一面画廊：每条一个方块，点开弹出样例

    方块：封面（第一张原图，没有就用代码开头）+ 机构 logo、条目名、机构、下载量 / star 徽章（取自
    bench/pipe/repo/site 四份元数据）+ 样例条数。弹层：同一套标题（名称带链接）+ 样例本体：
      middle_processing/samples/<slug>.html —— 实抓样本（单行组件）
      middle_processing/deep/<slug>.md  —— 定位、数据管线图、合成流程、关键数字
    两者缺一个就只出另一个；都没有就打 warn 并跳过这一格。弹层逻辑见 template.html 的 sg-*。
    """
    def one(slug, name):
        demo_p = os.path.join(MID, "samples", f"{slug}.html")
        deep_p = os.path.join(MID, "deep", f"{slug}.md")
        if not (os.path.isfile(demo_p) or os.path.isfile(deep_p)):
            print(f"  [warn] 缺 samples/{slug}.html 与 deep/{slug}.md，跳过")
            return "", ""
        demo = open(demo_p, encoding="utf-8").read().strip() if os.path.isfile(demo_p) else ""
        deep = open(deep_p, encoding="utf-8").read().strip() if os.path.isfile(deep_p) else ""
        mm = meta.get(name, {})
        tile = _sample_tile(slug, name, mm, f"sg-{slug}")
        return tile, _sample_panel(slug, name, meta)

    def repl(m):
        tiles, panels = zip(*(one(s, n) for s, n in _SAMPLE_RE.findall(m.group(0))))
        return "\n\n".join([f'<div class="sg-grid">{"".join(tiles)}</div>'] + [p for p in panels if p]) + "\n\n"

    return re.sub(rf"(?:{_SAMPLE_RE.pattern}\s*)+", repl, body)


def fill_frontier(body, chapter):
    """<!--FRONTIER--> → data/frontier_<chapter>.html（厂商自报分数表，整表直接注入）"""
    if not _FRONT_RE.search(body):
        return body
    p = os.path.join(DATA, f"frontier_{chapter.split('-')[0]}.html")      # 3d-v2 和 3d 共用一份
    if not os.path.isfile(p):
        print(f"  [warn] 缺 data/frontier_{chapter}.html，<!--FRONTIER--> 留空")
        return _FRONT_RE.sub("", body)
    tbl = open(p, encoding="utf-8").read().strip()
    return _FRONT_RE.sub(lambda _: tbl, body)


def toc(body, prefix):
    """视图内目录：收 `## <序号> <标题>` 三级。"""
    items = []
    for m in re.finditer(r"^(#{2,4})\s+(\d+(?:\.\d+){0,2})\s+(.+)$", body, re.M):
        lvl = f"l{len(m.group(1))}"
        num = m.group(2)
        items.append(f'<li class="{lvl}"><a href="#{prefix}-{num.replace(".", "-")}">'
                     f'<span class="num">{num}</span> {m.group(3).strip()}</a></li>')
    if not items:
        return ""
    return '<nav class="toc view-toc"><h2>In This Section</h2><ul>' + "".join(items) + "</ul></nav>"


def anchorize(body, prefix):
    """给 `## 1 Foo` 加上 `<a id="bench-1">`，让视图内目录能跳。"""
    def repl(m):
        hashes, num, title = m.group(1), m.group(2), m.group(3)
        return f'{hashes} <a id="{prefix}-{num.replace(".", "-")}"></a>{num} {title}'
    return re.sub(r"^(#{2,4})\s+(\d+(?:\.\d+){0,2})\s+(.+)$", repl, body, flags=re.M)


HEAD = """# {title}

<style>
/* 窄屏：表格独立滚动，否则宽表会被截掉 */
@media (max-width:720px){{
  .doc table{{display:block;overflow-x:auto}}
}}
</style>

<div class="view-switch"></div>
"""


def build_chapter(chapter, title, views, buckets, bmeta, pmeta, rmeta, smeta):
    parts = [HEAD.format(title=title)]
    written = 0
    for key, label, desc in views:
        src = os.path.join(PARTS, chapter, f"{key}.md")
        if not os.path.isfile(src):
            print(f"  [skip] {chapter}/{key}.md 还没写")
            continue
        body = open(src, encoding="utf-8").read().strip()
        _EX_WANT.clear()                 # Example 列的引用按视图统计
        body = fill_tables(body, buckets, bmeta, pmeta)
        body = fill_repos(body, rmeta, smeta)
        body = fill_artifacts(body)
        body = fill_samples(body, {**SAMPLE_META, **bmeta, **pmeta, **rmeta, **smeta})
        body = fill_frontier(body, chapter)
        body = fill_example_cells(body, {**SAMPLE_META, **bmeta, **pmeta, **rmeta, **smeta})
        # Example 列指向的样例，若本视图里还没有弹层（没进画廊），在末尾补一份
        body = example_panels(body, {**SAMPLE_META, **bmeta, **pmeta, **rmeta, **smeta}, key)
        # 目录要在 anchorize 之前收，否则标题前多了锚点就匹配不上序号
        nav = toc(body, key)
        body = anchorize(body, key)
        parts.append(f'<div class="env-view" data-view="{key}" data-label="{label}"'
                     f' data-desc="{desc}">\n\n'
                     + nav + "\n\n" + body + "\n\n</div>\n")
        written += 1
        print(f"  [ok]   {chapter}/{key}.md  {len(body)} 字符")
    if not written:
        return
    out = os.path.join(ROOT, "pages", f"{chapter}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  写出 {os.path.relpath(out, ROOT)} ({os.path.getsize(out)} 字节)\n")


def main():
    buckets = load_buckets()
    bmeta, pmeta = load_bench_meta(), load_pipe_meta()
    rmeta, smeta = load_repo_meta(), load_site_meta()
    for chapter, title, views in CHAPTERS:
        print(f"== {title}")
        build_chapter(chapter, title, views, buckets, bmeta, pmeta, rmeta, smeta)

    # 覆盖率自查：映射表里引用了元数据里没有的名字，或反过来，都要报出来
    for kind, meta in (("bench", bmeta), ("pipe", pmeta)):
        bmap = buckets[kind]
        miss = [n for n in bmap if n not in meta]
        extra = [n for n in meta if n not in bmap]
        if miss:
            print(f"  [warn] {kind}: 映射表有、元数据无 —— {miss}")
        if extra:
            print(f"  [warn] {kind}: 元数据有、映射表无 —— {extra}")
        used = sorted({v.get("bucket") for v in bmap.values()})
        print(f"  {kind}: {len(bmap)} 条，bucket = {used}")


if __name__ == "__main__":
    main()

