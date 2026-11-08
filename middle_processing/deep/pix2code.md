- **定位**：最早的截图转代码工作，第一次公开发布「GUI 截图 ↔ 代码」合成配对数据（iOS / Android / Web 三个平台）

<figure class="paper-fig"><div class="flow"><div class="step"><b>DSL</b>人工设计布局 / 组件 DSL</div><span class="arr">→</span><div class="step"><b>Stochastic UI generator</b>按语法随机组合 GUI</div><span class="arr">→</span><div class="step"><b>DSL compiler</b>编译成 iOS / Android / HTML</div><span class="arr">→</span><div class="step"><b>渲染截图</b>各平台渲染得到截图</div><span class="arr">→</span><div class="step"><b>滑窗切样本</b>48 token 窗口配整张截图</div></div><figcaption>pix2code · 自绘流程图（论文无数据管线图，依据正文描述）</figcaption></figure>

- **自动化合成流程**（对照上面的自绘图）
  1. **DSL 设计**：人工设计一套轻量的类标记语言 DSL，只描述布局、组件和层级，不管标签里的文字，所以词表很小
  2. **Stochastic user interface generator**：随机生成器按 DSL 语法随机组合出 GUI 描述（纯程序，不用模型）
  3. **DSL compiler**：编译器把 DSL 编译成目标平台代码（iOS Storyboard、Android XML、HTML/CSS），标签文字随机填
  4. **渲染截图**：在对应平台渲染编译出的代码并截图，得到（截图，代码）对
  5. **滑窗切样本**：DSL 按 48 个 token 的滑窗切开，每个窗口和整张截图配成一个训练样本
- **质量控制**
  - 数据由语法和编译器生成，天然保证正确，论文没有另设过滤或去重步骤
- **关键数字**
  - 生成器可产出的不同配置数：iOS 26×10⁵、Android 21×10⁶、Web 31×10⁴
  - 实际使用：每个平台 1,500 对训练、250 对测试；训练样本（图-序列对）分别为 93,672 / 85,756 / 143,850
  - 效果：greedy 解码的 token 错误率 iOS 22.73%、Android 22.34%、Web 12.14%；模型约 109×10⁶ 参数
- **局限**
  - DSL 只表达布局，不管真实文本，离真实代码很远
  - 生成器组合空间有限，数据量很小，界面风格单一
  - 输入统一缩放到 256×256，不保长宽比
- **可借鉴**
  - 先定义「DSL + 编译器」，再用随机文法采样造数据：配对天然正确、零标注成本，而且同一份 DSL 可以编译到多个平台
  - 训练目标用中间 DSL 而不是原始代码，能缩小词表和搜索空间

