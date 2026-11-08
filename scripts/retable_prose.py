#!/usr/bin/env python3
"""配合 retable_artifacts.py 的正文改动：删掉指定两块、补表注、补「读表」说明。

每条都断言命中次数，对不上就整体不写盘。脚本幂等。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'parts', 'web', 'verified.md')
D3 = os.path.join(ROOT, 'parts', '3d', 'verified.md')

LEGEND = """读表：**Artifacts** 是这个渠道直接拿到的东西，**Output** 是它们能变成 RL 环境里的哪一件。

- `query`：自带能直接当题面的东西 —— 参考图、描述文本、问题文本。反向构造出来的题面不算。
- `verifier`：自带能重跑出参考状态的代码，或能逐项比对的结构 —— 布局框、无障碍树、网格、点云。
- `hint`：自带可读的参考代码或示范轨迹，用来提高 rollout 成功率。
"""


def main():
    problems, staged = [], {}

    # ---------------- parts/web/verified.md ----------------
    t = open(WEB, encoding='utf-8').read()

    # 1) 删 2.3 的「已知问题 + 数据解读」整块（表之后、2.4 之前）
    t, n = re.subn(r'\n已知问题：\n.*?\n(?=### 2\.4 Website)', '\n', t, flags=re.S)
    if n != 1 and '已知问题：' in t:
        problems.append(f'web 2.3 已知问题块：命中 {n} 次')

    # 2) 删 2.4 的「图例 + 数据解读 + 设计类站点」整块（表之后、2.4.1 之前）
    t, n = re.subn(r'\n✓ 可用　△ 有条件　✗ 不可用。desc = 正文或描述文本。† 站点对本机 403，未直连核实。\n.*?\n(?=#### 2\.4\.1 Why Real Pages Fail)',
                   '\n', t, flags=re.S)
    if n != 1 and '✓ 可用　△ 有条件　✗ 不可用。desc = 正文或描述文本。† 站点对本机 403' in t:
        problems.append(f'web 2.4 图例与数据解读块：命中 {n} 次')

    # 3) 2.2.1 表注：「— = 只有文件名」随 Reference 列一起没了
    old = 'title = 短标签，desc = 整句描述，— = 只有文件名；图:码 > 1 来自多主题（react）、多渲染后端（PixiJS）、多帧（p5）。'
    new = 'title = 短标签，desc = 整句描述；图 : 码 > 1 来自多主题（react）、多渲染后端（PixiJS）、多帧（p5）。'
    if old in t:
        t = t.replace(old, new, 1)
    elif new not in t:
        problems.append('web 2.2.1 表注：没找到')

    # 4) 2.1 读表：两段合成一段，先定义 Artifacts / Output，再给数量口径
    old = '读表：「458,596 依赖仓」是 Playwright 一家；「80 – 3.17M」「2,799 – 10M」是该类里各个数据集或站点的区间，不是合计。'
    new = LEGEND + '- 数量口径：「458,596 依赖仓」是 Playwright 一家；「80 – 3.17M」「2,799 – 10M」是该类里各个数据集或站点的区间，不是合计。'
    if old in t:
        t = t.replace(old, new, 1)
    elif LEGEND not in t:
        problems.append('web 2.1 读表段：没找到')
    staged[WEB] = t

    # ---------------- parts/3d/verified.md ----------------
    t = open(D3, encoding='utf-8').read()

    # 5) 术语写全（和 web 对齐）
    old = 'Golden Images：仓库为每份测试代码存一张标准截图，CI 每次渲染后逐像素比对，代码与截图因此天然成对。'
    new = ('Golden Images：仓库为每份测试代码存一张标准截图，持续集成（Continuous Integration）'
           '每次渲染后逐像素比对（Visual Regression Testing），代码与截图因此天然成对。\n\n' + LEGEND.rstrip())
    if old in t:
        t = t.replace(old, new, 1)
    elif LEGEND.rstrip() not in t:
        problems.append('3d 2.1 Golden Images 注：没找到')
    staged[D3] = t

    if problems:
        print('没有写盘，先解决这些：\n' + '\n'.join('  ' + p for p in problems))
        return 1
    for path, text in staged.items():
        open(path, 'w', encoding='utf-8').write(text)
    print('已改 2 个文件')
    return 0


if __name__ == '__main__':
    sys.exit(main())

