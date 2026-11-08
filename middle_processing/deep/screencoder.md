- **定位**：模块化多 agent 的截图转 HTML 框架，同时当作数据引擎，产出 Screen-10K，用于 SFT + RL 两阶段后训练

<figure class="paper-fig"><img src="../assets/papers/screencoder-fig3.png" alt="ScreenCoder overview"><figcaption>ScreenCoder · Fig. 3：Grounding 标出组件区域，Planning 建布局树，Generation 写带占位符的 HTML，最后用原图素材回填占位</figcaption></figure>

- **自动化合成流程**（对照上图，从左往右读）
  1. **Input (Screenshots, Design Sketches)**：网页截图或设计草图；做数据时的输入是爬到的 5 万个网页
  2. **Grounding Agent**：用 MLLM 按文字提问定位 Sidebar / Header / Navbar / Content，返回框和标签。后处理全靠规则：类内 NMS 去重；漏检时按空间先验兜底（顶部又宽又矮的框视为 header）；把不与任何组件重叠的最大矩形推断为主内容区
  3. **Planning Agent**：一个确定性算法（Visual-to-Structural Tree Mapping），把框转成 DOM 式布局树。像素坐标换成百分比并用绝对定位；带子区域的节点设为 CSS Grid 容器。整个过程不调用模型
  4. **Generation Agent**：遍历布局树，每个节点用一个自适应 prompt（包含语义标签、树上下文和可选的用户指令）让 LLM 写代码，再按树结构拼成 **Initial Generated HTML**，图片先放占位符
  5. **Placeholder Mapping**：用 UIED 检测原图里的图标和图片，按规划得到的区域分组；以负 CIoU 作代价、Hungarian 算法一对一匹配占位框，然后从原图裁图回填
  6. **Output Webpage & Code**：得到最终页面和代码
  - （图外）**Screen-10K**：爬取 5 万个网页，经过自动过滤留下 1 万对高质量图-码对；其中 9K 用于 SFT，1K 用于 RL
  - （图外）**RL 奖励**：把生成的代码渲染出来，和原图算 −MSE，用 GRPO 优化
- **质量控制**
  - 50K → 10K，只保留 20%；论文只说是「严格的自动化过滤」，没有公开过滤标准
  - grounding 阶段有规则后处理（NMS、兜底、主内容推断）
  - RL 阶段用像素级渲染对比当奖励，相当于在线的执行校验
- **关键数字**
  - 规模：Screen-10K 共 10,000 对；ScreenBench 有 1,000 个网页
  - 训练：基座 Qwen2.5-VL-32B，LLaMA-Factory，16 张 A100
  - 后训练收益（ScreenBench）：Block 0.723 → SFT 0.741 → RL 0.758；Position 0.613 → 0.705 → 0.742；CLIP 0.762 → 0.784 → 0.791
  - 人评：与 GPT-4o 两两对比，ScreenCoder 胜 65%、负 11%、平 24%
- **局限**
  - 过滤规则、数据引擎用的具体 MLLM 都没在正文写明（prompt 只以图片形式放在附录）
  - 规划器输出的是百分比 + 绝对定位的代码，响应式能力和代码风格都被锁死（推断）
  - v1 和 v2 口径不一致：v1 写的是 5 万对数据集、3,000 对评测集、「块 + 文本 + 位置」组合奖励；v2 改成 1 万对、1,000 对、−MSE
- **可借鉴**
  - 把感知、规划、生成拆开：规划用确定性算法，结构不会跑偏，数据更干净
  - 图片占位加上「检测 + Hungarian 匹配 + 裁原图回填」，截图里的真实素材就能进到代码里
  - 渲染 −MSE 奖励最简单，拿同一批数据接着做 RL 就行

