#!/usr/bin/env python3
"""pages/*.md → output/ 下平铺的页面（webdev / 3d / video / market / deep-research），末尾跑 make_total.py 出 total.html。

Usage:  python3 scripts/build.py

Editing workflow: edit any markdown file listed in DOCS_SPEC below, then re-run.

Reference handling (automatic):
  * A markdown link whose href resolves to a LOCAL .md file (relative path,
    absolute filesystem path, or a directory containing README/index/SKILL.md)
    is pulled into the page as a loadable sub-doc and the link is rewritten to
    an in-page `#doc:<id>` switch — clicking it renders that markdown inline,
    no full-page navigation, no dead links. Discovery is transitive (BFS): a
    referenced doc's own local .md links are included too.
  * Out-of-tree docs are VENDORED: their .md source and every local image they
    use are copied into code/vendor/<id>/, and image paths are rewritten to the
    copies. After a build, code/ has no dependency on files outside it — the
    whole folder can be zipped and moved. (Rebuilt fresh each run.)
  * External links (http/https/mailto) are left untouched; the template opens
    them in a new tab.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections import deque
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, "vendor")   # copies of out-of-tree docs + their images
OUT = os.path.join(ROOT, "output")

# Each entry: (id, label, markdown-path relative to ROOT, is_tab, parent-id)
#   is_tab=True  -> shown in the top tab bar
#   is_tab=False -> loadable sub-doc, reachable only via in-page links; `parent`
#                   keeps that tab highlighted and adds a "← back" breadcrumb.
DOCS_SPEC: list[tuple[str, str, str, bool, str | None]] = [
    ("overview", "Overview", "pages/overview.md", True, None),
    ("web",      "Web (2D)", "pages/web.md",      True, None),
    ("3d",       "3D",       "pages/3d.md",       True, None),
    ("3d-v2",    "3D",       "pages/3d-v2.md",    True, None),
    ("video",    "Video",    "pages/video.md",    True, None),
    ("market",   "Market",   "pages/market.md",   True, None),
]

# output/ 下的页面，平铺在一层，共用一份 output/assets/。
#
# 子页的顶部标签栏放的是**本章自己的视图**（Benchmark / Data / Verifier …），
# 不放别的章 —— 一页只讲一章。跨章的入口在 total.html 和 deep-research.html 上。
#
#   (文件名, 这一页带的章, 标签栏里是否留指向其他页的链接)
PAGES: list[tuple[str, list[str], bool]] = [
    ("deep-research.html", ["overview"], True),   # Deep Research 正文，total.html 的 Hero 按钮指这里
    ("webdev.html",        ["web"],      False),
    ("3d.html",            ["3d"],       False),
    ("3d-v2.html",         ["3d-v2"],    False),  # 3D 改写版，和 3d.html 在总页并排对比
    ("video.html",         ["video"],    False),
    ("market.html",        ["market"],   False),
]
# 每一章对应的页面（deep-research.html 标签栏跳这里）
ENTRY = {"web": "webdev.html", "3d": "3d.html", "video": "video.html", "market": "market.html"}

DEEP_RESEARCH = "deep-research.html"
TITLE     = "Visual Coding"
SUBTITLE  = "Web · 3D · Video — Verified Environments for Visual Code"

# 每个子站的头部，按它带的那一章取：(标题, logo 字母, eyebrow, subtitle, hero 按钮)
#
# 标题是**本章自己**的名字，不是 "Visual Coding" —— 子页各自成立，总页才叫 Visual Coding。
# 浏览器标签仍是「<标题> · Visual Coding」，保留出身。
# hero 按钮也按章给：只放这一章正文真正引用过的外链，别让 webdev 页挂着 BlenderGym。
SITE_HEAD = {
    "overview": ("Visual Coding", "V", "Web Dev · Blender × 3D · Vibe Gaming",
                 SUBTITLE,
                 [("Vibe Code Bench ↗", "https://www.vals.ai/benchmarks/vibe-code"),
                  ("3JSBench ↗", "https://3jsbench.com/")]),
    "web":      ("Webdev", "W", "HTML · WebDev · PPT · Manim",
                 "Web (2D) — Task = Query + Verifier + Harness：公开基准、公开数据、自建可验证环境",
                 [("Vibe Code Bench ↗", "https://www.vals.ai/benchmarks/vibe-code")]),
    "3d":       ("3D", "3", "Blender · Three.js · CAD",
                 "3D — 判据读场景图，不读渲染图：公开基准、公开数据、自建可验证环境",
                 [("3JSBench ↗", "https://3jsbench.com/")]),
    "3d-v2":    ("3D", "3", "Blender · Three.js · CAD",
                 "3D — Task = Query + Verifier + Harness：公开基准、公开数据、自建可验证环境",
                 [("3JSBench ↗", "https://3jsbench.com/")]),
    "video":    ("Video", "V", "Vibe Video · From Web · From Blender",
                 "Video — 每一帧是帧号与代码的纯函数：两条路线，分界在确定性从哪里来",
                 []),          # 这一章正文没引用过 benchmark，就不放按钮
    "market":   ("Market", "M", "3D Assets · Game & World · Ad Creative · Web 3D · Industrial 3D",
                 "Market — 钱跟着分发走，不跟着模型走：五条赛道、三个阶段、各技术路线在哪里赚钱",
                 []),
}

MAX_AUTO_DOCS = 60  # safety cap on transitively-included external docs

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# (?<![-\w]) 防止把 data-src / xlink:src 之类的属性也当成 src 改写 —— 没有这个
# 前视，data-src="../x/y.html" 里的 src=" 会被匹配到，路径按 md 所在目录重写一遍，
# 结果指到不存在的位置（实测 eval 页签的 Open Source 预览因此 404）。
_SRC_RE    = re.compile(r'(?<![-\w])(src\s*=\s*)"([^"]+)"')
_MDIMG_RE  = re.compile(r'(!\[[^\]]*\]\()([^)\s]+)(\))')
# markdown link [text](href) — but NOT an image ![text](href)
_LINK_RE  = re.compile(r'(?<!\!)\[([^\]]*)\]\(([^)\s]+)\)')
# <iframe ...attrs... src="..." ...attrs...> — captures attrs-before, the src
# value, and attrs-after so inline_iframes can swap src="" for srcdoc="".
_IFRAME_RE = re.compile(r'<iframe\b([^>]*?)\ssrc\s*=\s*"([^"]+)"([^>]*)>', re.IGNORECASE)

_HREF_RE   = re.compile(r'(?<![-\w])href\s*=\s*"([^"]+)"')

_DIR_INDEX_NAMES = ("README.md", "index.md", "index.zh.md", "SKILL.md")

MAX_ANCESTOR_DEPTH = 50     # 子文档往上找 tab 的防环上限，与 template.html 里同名常量一致

# ---------------------------------------------------------------------------
# Image path helpers
# ---------------------------------------------------------------------------

def _copy_into(src_abs: str, dest_abs: str) -> bool:
    """Copy src_abs → dest_abs, creating parent dirs as needed. Returns True on success."""
    if not os.path.isfile(src_abs):
        return False
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(src_abs, dest_abs)
    return True


def _rewrite_img(path_val: str, md_dir: str, vendor_rel: str | None) -> str:
    """Rewrite one image path to a ROOT-relative path that resolves offline.

    In-tree docs: return a path relative to ROOT (http/abs left as-is).
    Vendored docs (out-of-tree): copy the image into vendor/<id>/ and point at
    the copy, so the code/ folder has no external dependency after a build.
    """
    if re.match(r'^(https?:|data:|#)', path_val):
        return path_val
    raw = unquote(path_val)
    if os.path.isabs(raw):
        src_abs  = os.path.normpath(raw)
        subpath  = os.path.basename(raw)
    else:
        src_abs  = os.path.normpath(os.path.join(md_dir, raw))
        subpath  = raw

    if vendor_rel is None:          # in-tree doc
        if path_val.startswith('/'):
            return path_val
        # Always emit forward slashes: this path goes into an HTML/URL context,
        # and os.path.relpath yields backslashes on Windows, which browsers
        # won't resolve as path separators.
        return os.path.relpath(src_abs, ROOT).replace(os.sep, '/')

    # vendored doc: copy the asset under vendor/<id>/ so code/ is self-contained
    subpath  = subpath.lstrip('./').replace('../', '')
    dest_abs = os.path.join(ROOT, vendor_rel, subpath)
    if _copy_into(src_abs, dest_abs):
        return os.path.relpath(dest_abs, ROOT).replace(os.sep, '/')
    return path_val     # missing source: leave untouched


def rewrite_images(md: str, md_dir: str, vendor_rel: str | None = None) -> str:
    """Rewrite all image src/href references in `md` to ROOT-relative paths."""
    md = _SRC_RE.sub(
        lambda m: f'{m.group(1)}"{_rewrite_img(m.group(2), md_dir, vendor_rel)}"', md
    )
    md = _MDIMG_RE.sub(
        lambda m: f'{m.group(1)}{_rewrite_img(m.group(2), md_dir, vendor_rel)}{m.group(3)}', md
    )
    return md


def inline_iframes(md: str, md_dir: str) -> str:
    """Inline any <iframe src="local.html"> as srcdoc so the page needs no 2nd fetch.

    The SPA ships as a single self-contained index.html; an iframe pointing at a
    separate local .html would be the one remaining HTTP request, which breaks
    under file:// and is fragile behind caching proxies (AutoDL). We read the
    referenced file and embed its full HTML in a srcdoc="" attribute, HTML-escaping
    &, ", < and > so the value can't prematurely close the attribute or the outer
    <script> block, and collapsing newlines to &#10;/&#13; so the whole <iframe>
    stays on ONE physical line (marked re-parses this md and would otherwise
    terminate the HTML block at the first blank line inside the inlined document,
    shattering the chart). The browser decodes the entities and renders the iframe
    from the inlined document — JS inside it still executes normally.

    External (http/https) and missing local files are left untouched.
    """
    def _repl(m: re.Match) -> str:
        pre, src, post = m.group(1), m.group(2), m.group(3)
        if re.match(r'^(https?:|data:|//)', src):
            return m.group(0)                       # external: leave as-is
        target = src.split("#")[0].split("?")[0]
        abs_path = target if os.path.isabs(target) else os.path.join(md_dir, target)
        abs_path = os.path.normpath(abs_path)
        if not (abs_path.endswith(".html") and os.path.isfile(abs_path)):
            return m.group(0)                       # not a local .html file: leave
        with open(abs_path, encoding="utf-8") as f:
            content = f.read()
        esc = (content.replace("&", "&amp;").replace('"', "&quot;")
                      .replace("<", "&lt;").replace(">", "&gt;"))
        # Collapse newlines to numeric entities so the whole <iframe> stays on a
        # SINGLE physical line in the emitted markdown. The SPA re-parses this md
        # with marked in the browser, and CommonMark treats a block-level tag like
        # the wrapping <div>/<iframe> as an HTML block that TERMINATES at the first
        # blank line. The inlined document contains blank lines (e.g. inside its
        # <style>), so a literal newline here would cut the HTML block short,
        # leave srcdoc="" unclosed, and shatter the chart. The browser decodes
        # &#10;/&#13; back to real newlines inside srcdoc, so JS line comments
        # inside the inlined document keep working.
        esc = esc.replace("\r", "&#13;").replace("\n", "&#10;")
        return f'<iframe{pre}{post} srcdoc="{esc}">'

    return _IFRAME_RE.sub(_repl, md)

# ---------------------------------------------------------------------------
# Local-path resolution helpers
# ---------------------------------------------------------------------------

def _is_external(href: str) -> bool:
    return bool(re.match(r'^(https?:|mailto:|tel:|data:)', href))


def _pick_md_from_dir(directory: str) -> str | None:
    """Return the best index .md file inside a directory, or None."""
    for name in _DIR_INDEX_NAMES:
        candidate = os.path.join(directory, name)
        if os.path.isfile(candidate):
            return candidate
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".md"):
            return os.path.join(directory, filename)
    return None


def _resolve_local_md(href: str, base_dir: str) -> str | None:
    """Resolve a local href to an existing .md path, or return None.

    Handles relative paths, absolute filesystem paths, %20-encoded spaces,
    a trailing #fragment, and directories (→ README/index/SKILL.md inside).
    """
    path_part = unquote(href.split("#")[0])
    if not path_part:
        return None
    abs_path = path_part if os.path.isabs(path_part) else os.path.join(base_dir, path_part)
    abs_path = os.path.normpath(abs_path)
    if os.path.isdir(abs_path):
        return _pick_md_from_dir(abs_path)
    if abs_path.endswith(".md") and os.path.isfile(abs_path):
        return abs_path
    return None


def _slug(text: str, fallback: str) -> str:
    """Turn arbitrary text into a URL-safe lowercase slug."""
    s = re.sub(r'[^a-z0-9]+', '-', (text or "").lower()).strip('-')
    return s or fallback


def _rewrite_local_asset(href: str, base_dir: str) -> str | None:
    """Rewrite a local NON-md link (source file / dir / .mdx) to a ROOT-relative path.

    Doc links resolve relative to the .md they live in, but the SPA loads every
    doc into a single index.html at ROOT, so a browser resolves all relative
    hrefs against ROOT — dropping the doc's own subdir prefix and breaking the
    link. We rewrite such links to a ROOT-relative path (forward slashes) so
    they resolve correctly when the site is served over HTTP.

    Preserves a trailing #fragment (e.g. #L157 line anchors). Returns None when
    the target doesn't exist inside ROOT (external/missing → caller leaves it).
    """
    path_part, _, frag = href.partition("#")
    path_part = unquote(path_part)
    if not path_part:
        return None
    abs_path = path_part if os.path.isabs(path_part) else os.path.join(base_dir, path_part)
    abs_path = os.path.normpath(abs_path)
    # Must live inside ROOT and actually exist (file or directory).
    if not abs_path.startswith(ROOT + os.sep) or not os.path.exists(abs_path):
        return None
    rel = os.path.relpath(abs_path, ROOT).replace(os.sep, '/')
    if os.path.isdir(abs_path) and not rel.endswith('/'):
        rel += '/'
    return rel + (('#' + frag) if frag else '')

# ---------------------------------------------------------------------------
# Asset loading
# ---------------------------------------------------------------------------

def _load_assets() -> dict[str, str]:
    """Read all bundled JS/CSS assets from the assets/ directory.

    Raises FileNotFoundError with a clear message if any asset is missing.
    """
    asset_dir = os.path.join(ROOT, "assets")
    asset_files = {
        "marked_js":          "js/marked.min.js",
        "katex_js":           "js/katex.min.js",
        "katex_autorender_js": "js/katex-auto-render.min.js",
        "katex_css":          "css/katex.selfcontained.css",
    }
    assets: dict[str, str] = {}
    for key, filename in asset_files.items():
        path = os.path.join(asset_dir, filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Missing asset: {path}")
        with open(path, encoding="utf-8") as f:
            assets[key] = f.read()
    return assets

# ---------------------------------------------------------------------------
# Doc-graph construction (BFS)
# ---------------------------------------------------------------------------

def _collect_docs() -> list[dict]:
    """Seed the doc list from DOCS_SPEC, then BFS-expand local .md links.

    Returns an ordered list of doc dicts ready for image-rewriting in the next
    phase. Each dict has the fields:
        id, label, tab, parent, abs, dir, vendor_rel, raw, md (None until phase 3)
    """
    docs: list[dict]      = []
    by_abs: dict[str, dict] = {}
    used_ids: set[str]    = set()

    def _uniq_id(base: str) -> str:
        base = base or "doc"
        candidate, n = base, 1
        while candidate in used_ids:
            n += 1
            candidate = f"{base}-{n}"
        used_ids.add(candidate)
        return candidate

    def _add_doc(
        abs_md: str, doc_id: str, label: str, is_tab: bool, parent: str | None
    ) -> dict:
        with open(abs_md, encoding="utf-8") as f:
            raw = f.read()
        in_tree    = os.path.normpath(abs_md).startswith(ROOT + os.sep)
        vendor_rel = None if in_tree else os.path.join("vendor", doc_id)
        if vendor_rel:      # archive a readable copy of the source for portability
            _copy_into(abs_md, os.path.join(ROOT, vendor_rel, os.path.basename(abs_md)))
        doc = {
            "id": doc_id, "label": label, "tab": is_tab, "parent": parent,
            "abs": abs_md, "dir": os.path.dirname(abs_md), "vendor_rel": vendor_rel,
            "raw": raw, "md": None,
        }
        docs.append(doc)
        by_abs[abs_md] = doc
        return doc

    # Phase 1 — seed from the explicit tab/sub-doc spec
    queue: deque[dict] = deque()
    for doc_id, label, rel, is_tab, parent in DOCS_SPEC:
        full = os.path.normpath(os.path.join(ROOT, rel))
        if not os.path.isfile(full):
            print(f"  [skip] {rel} (missing)")
            continue
        used_ids.add(doc_id)
        queue.append(_add_doc(full, doc_id, label, is_tab, parent))

    # Phase 2 — BFS: rewrite local .md links to #doc:<id>, pulling new docs in
    auto_count = 0

    def _make_link_rewriter(doc: dict):
        """Return a regex replacement function bound to `doc`."""
        nonlocal auto_count

        def _repl(m: re.Match) -> str:
            nonlocal auto_count
            text, href = m.group(1), m.group(2)
            if _is_external(href) or href.startswith("#"):
                return m.group(0)                       # external / plain anchor: leave
            target = _resolve_local_md(href, doc["dir"])
            if not target:
                # Not a local .md: if it points at a real in-tree source file or
                # dir, rewrite to a ROOT-relative path so it resolves in the SPA.
                asset = _rewrite_local_asset(href, doc["dir"])
                if asset and asset != href:
                    return f'[{text}]({asset})'
                return m.group(0)                       # external / missing: leave
            existing = by_abs.get(target)
            if existing:
                return f'[{text}](#doc:{existing["id"]})'
            if auto_count >= MAX_AUTO_DOCS:
                print(f"  [warn] MAX_AUTO_DOCS reached, skipping {target}")
                return m.group(0)
            auto_count += 1
            new_id = _uniq_id(_slug(text, os.path.splitext(os.path.basename(target))[0]))
            # keep the nearest tab ancestor highlighted; add breadcrumb → this doc
            new_doc = _add_doc(
                target, new_id,
                (text or os.path.basename(target)).strip(),
                False, doc["id"],
            )
            queue.append(new_doc)
            print(f"  [ref]  {os.path.relpath(target, ROOT):48s} -> #{new_id}  (from {doc['id']})")
            return f'[{text}](#doc:{new_id})'

        return _repl

    while queue:
        doc = queue.popleft()
        doc["raw"] = _LINK_RE.sub(_make_link_rewriter(doc), doc["raw"])

    return docs, auto_count

# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

def _render_html(
    template: str,
    assets: dict[str, str],
    payload: list[dict],
    head: tuple[str, str] = SITE_HEAD["overview"],
) -> str:
    """Fill the template with assets and doc payload, return the final HTML.

    The payload is embedded as JSON inside a <script type="application/json">
    block (injected by build.py via __DOCS__) to avoid the '</script>' XSS
    hazard that arises from direct string-substitution into a <script> block.
    JSON-encodes ensure_ascii=False for compact CJK output.
    """
    # Escape any literal </script> that might appear in markdown content so
    # the browser's HTML parser never sees a premature end-of-script tag.
    docs_json = json.dumps(payload, ensure_ascii=False).replace("</script>", r"<\/script>")
    # 划词备注：嵌一份进页面，换别的静态服务打开也能只读看到（可写要走 scripts/serve_notes.py）
    notes_path = os.path.join(ROOT, "data", "notes.json")
    notes = json.load(open(notes_path, encoding="utf-8"))["notes"] if os.path.isfile(notes_path) else []
    notes_json = json.dumps(notes, ensure_ascii=False).replace("</", r"<\/")

    return (
        template
        .replace("/*__MARKED__*/",   assets["marked_js"])
        .replace("/*__KATEX_JS__*/", assets["katex_js"] + "\n" + assets["katex_autorender_js"])
        .replace("/*__KATEX_CSS__*/", assets["katex_css"])
        .replace("__DOCS__",    docs_json)
        .replace("/*__NOTES__*/[]", notes_json)
        .replace("__ARXIV__",   DEEP_RESEARCH)
        .replace("__TITLE__",   head[0])
        .replace("__MARK__",    head[1])
        .replace("__EYEBROW__", head[2])
        .replace("__SUBTITLE__", head[3])
        .replace("__LINKS__", "\n".join(
            f'      <a class="btn" href="{url}" target="_blank" rel="noopener">{label}</a>'
            for label, url in head[4]))
    )

# ---------------------------------------------------------------------------
# 把一个项目真正用到的资源拷进它自己的目录
# ---------------------------------------------------------------------------

# (正则, 取第几个捕获组)。md 里的路径此时已经被 rewrite_images 改成「相对 ROOT」。
_URL_RE = re.compile(r"""url\(['"]?(assets/[^'")]+)""")   # market 卡片的封面写在背景图里
_REF_PATTERNS = [(_SRC_RE, 2), (_MDIMG_RE, 2), (_LINK_RE, 2), (_HREF_RE, 1), (_URL_RE, 1)]


def _copy_referenced_assets(payload: list[dict]) -> tuple[int, float, list[str]]:
    """把 payload 引用到的本地文件按同样的相对路径拷进 output/。

    拷完 output/ 就不依赖 ROOT 下的任何东西了：html 自带 js/css（build 时内联），
    图片与 iframe 素材在这里有一份自己的副本，整个目录可以直接打包搬走。
    """
    wanted: set[str] = set()
    missing: set[str] = set()
    for doc in payload:
        md = doc.get("md") or ""
        for pat, grp in _REF_PATTERNS:
            for m in pat.finditer(md):
                raw = unquote(m.group(grp).split("#")[0].split("?")[0])
                if not raw or re.match(r'^(https?:|mailto:|tel:|data:|/)', raw):
                    continue
                abs_src = os.path.normpath(os.path.join(ROOT, raw))
                if not abs_src.startswith(ROOT + os.sep):
                    continue
                rel = os.path.relpath(abs_src, ROOT).replace(os.sep, "/")
                if rel.startswith("output/"):
                    continue
                if os.path.isfile(abs_src):
                    wanted.add(rel)
                elif "/" in rel:
                    # 不带目录的裸文件名基本都是样例正文里的字符串（SMILES、被转义的
                    # 网页源码里的 href="placeholder.png"），不是本页要加载的资源。
                    missing.add(rel)

    total = 0
    for rel in sorted(wanted):
        src = os.path.join(ROOT, rel)
        shutil.copy2(src, _mkparent(os.path.join(OUT, rel)))
        total += os.path.getsize(src)
    return len(wanted), total / 1048576, sorted(missing)


def _mkparent(path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    # Rebuild vendor dir from scratch each run so stale copies never linger.
    if os.path.isdir(VENDOR):
        shutil.rmtree(VENDOR)

    # 1) Collect all docs via BFS link-expansion
    docs, auto_count = _collect_docs()

    # 2) Finalize: rewrite image paths (done after BFS so final markdown is stable).
    #    For vendored (out-of-tree) docs this also copies their images into vendor/.
    vendored = 0
    for doc in docs:
        # Inline local <iframe src="*.html"> as srcdoc BEFORE image rewriting:
        # rewrite_images would otherwise resolve the iframe src relative to the
        # doc's own dir and double the path (eval/ -> eval/eval/), 404-ing it.
        doc["md"] = inline_iframes(doc["raw"], doc["dir"])
        doc["md"] = rewrite_images(doc["md"], doc["dir"], doc["vendor_rel"])
        kind = "tab" if doc["tab"] else f"sub of {doc['parent']}"
        if doc["vendor_rel"] is None:
            print(f"  [ok]   {os.path.relpath(doc['abs'], ROOT):48s} -> #{doc['id']}  ({kind})")
        else:
            vendored += 1
            print(f"  [vendor] {doc['vendor_rel']:46s} <- {doc['abs']}")

    # 3) Load assets and template once
    assets   = _load_assets()
    with open(os.path.join(ROOT, "scripts", "page_template.html"), encoding="utf-8") as f:
        template = f.read()

    # 4) 每篇文档归到哪个 tab 名下（子文档跟着 parent 一路往上找）
    by_id   = {d["id"]: d for d in docs}
    tab_of  = {}
    for doc in docs:
        cur, depth = doc, 0
        while cur and not cur["tab"] and cur["parent"] and depth < MAX_ANCESTOR_DEPTH:
            cur, depth = by_id.get(cur["parent"]), depth + 1
        tab_of[doc["id"]] = (cur or doc)["id"]

    print()
    shutil.rmtree(os.path.join(OUT, "assets"), ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    for name, ids, cross in PAGES:
        payload = []
        for doc in docs:
            if tab_of[doc["id"]] in ids:
                payload.append({k: doc[k] for k in ("id", "label", "tab", "parent", "md")})
            elif cross and doc["tab"] and doc["id"] in ENTRY:
                # 别的页里的章：只留一个标签，点了就跳过去
                payload.append({"id": doc["id"], "label": doc["label"], "tab": True,
                                "parent": None, "md": "", "href": ENTRY[doc["id"]]})

        html = _render_html(template, assets, payload, SITE_HEAD.get(ids[0], SITE_HEAD["overview"]))
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(html)
        n_asset, mb, missing = _copy_referenced_assets(payload)

        own = sum(1 for d in payload if not d.get("href"))
        print(f"  [write] output/{name:22s} {own} 篇正文 + {len(payload) - own} 个跨页标签"
              f"  ({len(html) // 1024} KB + {n_asset} 个资源 {mb:.1f} MB)")
        for m in missing:
            print(f"            [warn] 引用了不存在的文件: {m}")

    print(f"\n  {len(docs)} docs ({auto_count} auto-included, {vendored} vendored into vendor/)"
          f" — 写出 {len(PAGES)} 个页面")

    # 总页 output/total.html
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "make_total.py")], check=True)


if __name__ == "__main__":
    main()

