- **定位**：用纯文本 LLM 写渲染代码来批量造「富文本图 + 指令」，一套框架覆盖图表、文档、表格、图示、乐谱、电路、化学结构等 9 类

<figure class="paper-fig"><img src="../assets/papers/cosyn-fig2.png" alt="CoSyn system overview"><figcaption>CoSyn-400K · Fig. 2：一句查询选中渲染管线，persona 驱动主题，LLM 依次写数据和代码，渲染出图，再以代码为上下文生成问答</figcaption></figure>

- **自动化合成流程**（对照上图，从左往右读）
  1. **20 Pipelines / 11 Tools**：根据用户查询（如 "book covers"）选一条管线。11 种渲染工具包括 Matplotlib、Plotly、Vega-Lite、LaTeX、HTML、Mermaid、Graphviz、SVG、Asymptote、LilyPond、RDKit；每种工具都有对应的执行函数
  2. **Selected Persona**：从 Ge et al. 发布的 20 万个 persona 里采样一个，塞进 prompt，用来打散 LLM 的输出分布
  3. **Topic Generation**：LLM 以 persona 为条件，一次生成若干个不重叠的主题
  4. **Data Generation**：Claude-3.5-Sonnet 按主题生成 JSON 格式的具体内容，prompt 要求用真实实体名，禁止 xxA、[Name] 这类占位
  5. **Code**：Claude-3.5-Sonnet 把数据硬编码进单文件渲染代码，prompt 要求单页、不重叠、不引用外部文件
  6. **Render**：执行代码，得到图片
  7. **Textual Instruction**（Context for LLM）：只把数据和代码给 GPT-4o-mini（不给图），让它生成「问题 | 解释 | 短答案」三元组，每张图 5–10 条，天然带 CoT
  - （图外）**Pointing 数据**：让 LLM 读源码，提一个指点类问题，并改代码在答案位置画上指定颜色的点；再从像素里读出 (x, y)，归一化到 0–100
- **质量控制**
  - 论文没有单独的过滤、去重或打分环节，也没给丢弃比例；质量主要靠三点：代码必须能执行出图、prompt 约束、选用强代码模型
  - 生成模型对比：各造 10 万张图表后，用 Claude-3.5-Sonnet 数据训出的模型 ChartQA 77.2，用 GPT-4o 的只有 72.4；GPT-4o 在冷门库上的代码失败率更高
  - 多样性量化：图像用 CLIP、文本用 Sentence-BERT 算平均两两余弦距离；图表子集的图像多样性 0.596，ChartQA 是 0.340
- **关键数字**
  - 规模：40 万张图、270 万条指令、9 类图像；文档一类就用了 100 多个查询
  - 成本：40 万张图约 8,000 美元
  - 下游：7B 模型（CLIP ViT-L/14 + Mistral-7B，沿用 Molmo 训练流程）在 7 个富文本基准上平均 80.9，比 Llama 3.2 11B 高 3.9；不看任何评测集训练数据的 zero-shot 版本也有 74.7
  - 工具多样性：同样 45K 张图，只用 Matplotlib 时 ChartQA 73.9，换成 5 种工具混合后 75.2
  - 新任务：只合成 7K 张营养成分表样本，就在 NutritionQA 上超过大多数开源 VLM
  - Pointing：65K 张合成图的效果接近 155K 张人工标注图（ScreenSpot 68.0 vs 68.5）；两者合并 74.9，超过用 130 万张截图训练的 UGround（73.3）
  - 去偏：ChartQA 上人写问题与机器生成问题之间的分差，从 21.8 降到 14.2
- **局限**
  - 效果高度依赖 prompt 和渲染管线的设计；小众领域要单独做 prompt 工程（论文自述）
  - 只有英文
  - 缺少显式质检，渲染成功但画面有瑕疵（比如文字重叠）的样本可能混进来（推断）
- **可借鉴**
  - 把代码当图文之间的桥：问答只看源码生成，答案可以做到精确，不依赖 VLM 去读图
  - persona 条件采样是低成本的多样性开关
  - 同一类图用多种渲染工具生成，本身就是有效的增强
  - 改源码画点来造 grounding 数据，坐标可以从像素里读出来，不用人标

