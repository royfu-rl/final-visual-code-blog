# Codrops MIT 仓库难度画像（2026-10-28 实测）

- 样本：GitHub org codrops 全部 349 个仓库里，GitHub API 许可为 MIT 的 129 个，全部 `git clone --depth 1`
- 只统计手写源码：有 `src/` 用 `src/`，否则用根目录；排除 node_modules、dist、build、vendor、lib、`.min.` 文件
- 判定规则（正则，命中即算）：three.js（import three / "three" 依赖 / THREE.）、其他 WebGL（ogl、pixi、regl、twgl、getContext("webgl")）、着色器（.glsl/.frag/.vert 或 gl_FragColor / void main()）、GSAP（gsap / TweenMax / TimelineMax）、平滑滚动（lenis / locomotive）

| 信号 | 仓库数 | 占比 |
|---|--:|--:|
| GSAP | 117 | 91% |
| 平滑滚动 | 45 | 35% |
| ≥ 2 个 html 入口 | 45 | 35% |
| WebGL（three.js / ogl / pixi / 原生 / 着色器任一） | 13 | 10% |
| three.js | 10 | 8% |
| 自写着色器 | 7 | 5% |
| Canvas 2D | 8 | 6% |

- 手写代码行数：中位 1,059，P90 3,028，最大 89,161
- 2023 年后新建 58 个，其中 WebGL 12 个
- 星数前五（MagneticButtons 485 起）均无 WebGL，四个用 GSAP
- 原始结果：会话临时目录 profile.json（未入库）

