# pmndrs/examples 难度画像（2026-10-28 实测）

- 样本：pmndrs/examples 的 `examples/` 下 211 个示例；`git clone --depth 1 --filter=blob:limit=300k`
- 统计每个示例 `src/` 下的 .tsx/.ts/.jsx/.js/.glsl 与 package.json
- 判定规则（正则）：物理（@react-three/rapier、cannon）、后处理（@react-three/postprocessing、EffectComposer）、着色器（shaderMaterial、ShaderMaterial、gl_FragColor、void main()、.glsl）、实例化（Instanced、<Instances）、glTF（useGLTF、GLTFLoader、.glb）

| 信号 | 示例数 | 占比 |
|---|--:|--:|
| 后处理 | 76 | 36% |
| 加载 glTF 模型 | 120 | 57% |
| 实例化 | 30 | 14% |
| 物理 | 24 | 11% |
| 自写着色器 | 20 | 9% |
| WebXR | 0 | 0% |

- 不加载 glTF 的纯代码示例 91 个（43%）
- 源码行数：中位 173，P90 525，最大 14,130

