#!/usr/bin/env python3
"""把 2.1–2.4 的来源表统一成「Artifacts → Output」两列结构。

Artifacts = 这个渠道直接拿到的东西（彩色标签：图 / 文本 / 代码 / 可跑的产物 / 资产 / 结构化字段）
Output    = 这些 Artifacts 能变成 RL 环境里的哪一件（query / verifier / hint）

第一列（带链接的名字）和 Datasize 原样搬，不重打，链接不会丢。
Reference 列和旧 Output 列的信息全部折进 Artifacts 标签。
脚本幂等：已经改过就跳过。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 标签家族 -> CSS 类
FAM = {'img': 'a-img', 'txt': 'a-txt', 'code': 'a-code', 'run': 'a-run', 'asset': 'a-asset', 'meta': 'a-meta'}
USE = {'q': ('u-q', 'query'), 'v': ('u-v', 'verifier'), 'h': ('u-h', 'hint')}


def arts(items):
    if not items:
        return '—'
    return ''.join(f'<span class="art {FAM[f]}">{t}</span>' for f, t in items)


def uses(keys):
    if not keys:
        return '—'
    return ''.join(f'<span class="use {USE[k][0]}">{USE[k][1]}</span>' for k in keys)


# ---------------------------------------------------------------------------
# 每张表：表头正则、新表头、新分隔行、以及逐行的 (Artifacts, Output)
#   keep = 旧表里要原样保留的列下标（第一列固定保留，这里写其余的）
# ---------------------------------------------------------------------------

I, T, C, R, A, M = 'img', 'txt', 'code', 'run', 'asset', 'meta'

TABLES = [
    # ---------------- web / 2.1 Overview ----------------
    dict(file='parts/web/verified.md',
         head='| Source | Type | Datasize | Example | Output | 详见 |',
         new_head='| Source | Type | Datasize | Example | Artifacts | Output | 详见 |',
         new_sep='|---|---|--:|---|---|---|:-:|',
         keep=[1, 2, 3], tail=[5],        # Type / Datasize / Example 原样；详见 放最后
         rows=[
             ([(I, 'image'), (C, '.tsx'), (C, '.js'), (C, '.json')], 'qvh'),
             ([(I, '截图断言'), (C, '组件代码')], 'qvh'),
             ([(T, '问题描述'), (I, 'image'), (C, 'patch')], 'qvh'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (T, 'title'), (R, '.html'), (C, '代码片段')], 'qvh'),
             ([(R, '线上 .html'), (I, '渲染结果')], 'qvh'),
             ([(I, '设计稿'), (I, 'image')], 'q'),
         ]),
    # ---------------- web / 2.2.1 Repo ----------------
    dict(file='parts/web/verified.md',
         head='| Repo | Reference（image +） | Datasize（图 / 码） | Output | Permitted |',
         new_head='| Repo | Datasize（图 / 码） | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|---|',
         keep=[2], tail=[4],
         rows=[
             ([(I, 'image'), (T, 'title'), (C, '.tsx')], 'qvh'),
             ([(I, 'image'), (T, 'desc 9%'), (C, '.json')], 'qvh'),
             ([(I, 'image'), (T, 'desc'), (C, '.ts')], 'qvh'),
             ([(I, 'image'), (C, '.json')], 'qvh'),
             ([(I, 'image'), (C, '.js')], 'qvh'),
             ([(I, 'image'), (T, 'desc'), (C, '.js')], 'qvh'),
             ([(I, 'image'), (C, '.ts')], 'qvh'),
             ([(I, 'image'), (C, '.js')], 'qvh'),
             (None, None),                # 合计行：两列留空
         ]),
    # ---------------- web / 2.3 Huggingface ----------------
    dict(file='parts/web/verified.md',
         head='| Dataset | Reference | Datasize | Output | Permitted |',
         new_head='| Dataset | Datasize | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|---|',
         keep=[2], tail=[4],
         rows=[
             ([(I, 'image'), (M, '简化 HTML 解析')], 'qv'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (T, '问题'), (T, '文字答案'), (M, '包围盒')], 'qv'),
             ([(I, 'image'), (R, '.html'), (M, '布局框')], 'qvh'),
             ([(I, 'image'), (T, 'desc'), (R, '.html Tailwind')], 'qvh'),
             ([(I, 'image'), (T, '指令'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (M, '无障碍树'), (M, '包围盒'), (M, '样式')], 'qv'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (R, '.html')], 'qvh'),
             ([(I, '手绘草图'), (R, '.html')], 'qvh'),
             ([(I, 'image'), (C, 'DSL')], 'qvh'),
         ]),
    # ---------------- web / 2.4 Website ----------------
    dict(file='parts/web/verified.md',
         head='| Website | Reference | Datasize | Output | Permitted |',
         new_head='| Website | Datasize | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|:-:|',
         keep=[2], tail=[4],
         rows=[
             ([(I, 'image'), (T, 'title'), (R, '单文件 .html ≤ 13 KB')], 'qvh'),
             ([(T, 'title'), (T, 'desc'), (R, '多文件静态站')], 'qvh'),
             ([(I, 'image'), (T, 'title'), (C, 'html / css / js 三段')], 'qvh'),
             ([(I, 'image'), (T, 'title'), (T, 'desc'), (C, 'p5 草图 .js')], 'qvh'),
             ([(I, '设计稿'), (T, 'desc'), (R, '多文件前端工程')], 'qvh'),
             ([(I, 'image'), (T, 'title'), (C, 'GLSL 片段着色器')], 'qvh'),
             ([(T, 'title'), (T, 'desc'), (C, '笔记本')], 'qh'),
             ([(T, 'title'), (C, 'html / css / js 三段')], 'qvh'),
         ]),
    # ---------------- 3d / 2.1 Overview ----------------
    dict(file='parts/3d/verified.md',
         head='| Source | Type | Datasize | Example | 详见 |',
         new_head='| Source | Type | Datasize | Example | Artifacts | Output | 详见 |',
         new_sep='|---|---|--:|---|---|---|:-:|',
         keep=[1, 2, 3], tail=[4],
         rows=[
             ([(I, 'image'), (R, '.blend'), (C, '.ts'), (R, '.html')], 'qvh'),
             ([(C, '.py'), (R, '.html')], 'vh'),
             ([(R, 'Blender 场景'), (A, 'OBJ / USD')], 'v'),
             ([(T, 'text'), (A, '点云'), (I, 'image'), (C, 'bpy .py'), (C, 'CadQuery .py')], 'qvh'),
             ([(A, '网格文件'), (M, '元数据')], 'v'),
             ([(T, 'title'), (T, 'desc'), (C, '脚本片段')], 'qh'),
             ([(I, 'image'), (T, 'title'), (A, '模型'), (A, 'HDRI')], 'qv'),
         ]),
    # ---------------- 3d / 2.2 Github Repo ----------------
    dict(file='parts/3d/verified.md',
         head='| Repo | Reference | Datasize | Output | Permitted |',
         new_head='| Repo | Datasize | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|---|',
         keep=[2], tail=[4],
         rows=[
             ([(I, 'image'), (R, '.blend')], 'qv'),
             ([(I, 'image'), (T, 'title'), (C, '.ts¹')], 'qvh'),
             ([(I, 'image'), (T, 'title'), (R, '.html')], 'qvh'),
             ([(C, 'bpy .py')], 'vh'),
             ([(R, '.html'), (C, '.js')], 'vh'),
             ([(C, '插件 .py')], 'vh'),
             ([(R, 'Blender 场景'), (A, 'OBJ / USD')], 'v'),
         ]),
    # ---------------- 3d / 2.3 Huggingface ----------------
    dict(file='parts/3d/verified.md',
         head='| Dataset | Reference | Datasize | Output | Permitted |',
         new_head='| Dataset | Datasize | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|---|',
         keep=[2], tail=[4],
         rows=[
             ([(T, 'text'), (C, 'bpy .py')], 'qvh'),
             ([(A, '点云'), (C, '分部件 bpy .py')], 'qvh'),
             ([(I, '多视角图'), (C, '起始脚本'), (C, '编辑后 bpy .py')], 'qvh'),
             ([(T, 'text'), (A, 'GLB 资产'), (R, 'three.js .html')], 'qvh'),
             ([(A, '点云'), (C, 'CadQuery 代码')], 'qvh'),
             ([(T, 'text'), (I, '多视角图'), (A, '点云'), (C, 'CAD 命令序列')], 'qvh'),
             ([(C, 'CAD 构造序列')], 'vh'),
             ([(T, 'text 多级'), (C, 'CAD 命令序列')], 'qvh'),
             ([(I, 'image'), (T, '固定指令'), (C, 'CadQuery 代码')], 'qvh'),
             ([(I, '4 视角图'), (C, '原代码'), (T, '编辑指令'), (C, 'CadQuery 代码')], 'qvh'),
             ([(A, '网格文件'), (M, '元数据')], 'v'),
         ]),
    # ---------------- 3d / 2.4 Website ----------------
    dict(file='parts/3d/verified.md',
         head='| Website | Reference | Datasize | Output | Permitted |',
         new_head='| Website | Datasize | Artifacts | Output | Permitted |',
         new_sep='|---|--:|---|---|:-:|',
         keep=[2], tail=[4],
         rows=[
             ([(I, 'image'), (T, 'title'), (A, 'HDRI'), (A, '贴图'), (A, '模型')], 'qv'),
             ([(I, 'image'), (T, 'title'), (A, '3D 模型')], 'qv'),
             ([(T, 'title'), (T, 'desc'), (C, '脚本片段')], 'qh'),
             ([(T, 'title'), (T, 'desc'), (C, '代码片段')], 'qh'),
             ([(I, 'image'), (T, 'title'), (T, 'desc'), (R, '少量 .blend')], 'qh'),
             ([(T, 'title'), (T, 'desc'), (C, '片段链接')], 'qh'),
         ]),
]


def cells(line):
    """'| a | b |' -> ['a', 'b']，保持单元格内文本逐字不动"""
    return [c.strip() for c in line.strip().strip('|').split('|')]


def rewrite(text, spec, where):
    if spec['new_head'] in text:
        return text, 'skip'
    i = text.find(spec['head'])
    if i < 0:
        raise SystemExit(f'{where}: 找不到表头 {spec["head"]}')
    lines = text[i:].split('\n')
    body = []
    for ln in lines[2:]:                       # 跳过表头与分隔行
        if not ln.startswith('|'):
            break
        body.append(ln)
    if len(body) != len(spec['rows']):
        raise SystemExit(f'{where}: 表有 {len(body)} 行，映射写了 {len(spec["rows"])} 行')

    out = [spec['new_head'], spec['new_sep']]
    for ln, (a, u) in zip(body, spec['rows']):
        c = cells(ln)
        new = [c[0]] + [c[k] for k in spec['keep']]
        new += ['', ''] if a is None else [arts(a), uses(u)]
        new += [c[k] for k in spec['tail']]
        out.append('| ' + ' | '.join(new) + ' |')

    old_block = '\n'.join(lines[:2 + len(body)])
    return text.replace(old_block, '\n'.join(out), 1), 'done'


def main():
    log = []
    for spec in TABLES:
        path = os.path.join(ROOT, spec['file'])
        text = open(path, encoding='utf-8').read()
        text, st = rewrite(text, spec, spec['file'] + ' / ' + spec['head'][:22])
        open(path, 'w', encoding='utf-8').write(text)
        log.append(f'  {st:4}  {spec["file"]}  {spec["new_head"][:40]}…')
    print('\n'.join(log))
    return 0


if __name__ == '__main__':
    sys.exit(main())

