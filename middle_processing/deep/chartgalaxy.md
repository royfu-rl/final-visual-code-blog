- **定位**：百万级「信息图表 + 数据表 + D3.js 代码」数据，给 VLM 补上「设计感强的图表」这一块的理解与 chart-to-code 能力

<figure class="paper-fig"><img src="../assets/papers/chartgalaxy-fig2.png" alt="ChartGalaxy dataset construction pipeline"><figcaption>ChartGalaxy · Fig. 2：上半部收集真实信息图并抽表，下半部用归纳出的图型、变体和布局模板程序化合成</figcaption></figure>

- **自动化合成流程**（对照上图，先上排再下排，从左往右读）
  1. **Data collection**：从 18 个允许研究使用的图表网站（Visual Capitalist、Statista 等）爬取，再用 Google / Bing 图片搜索补充，只保留 CC 许可的图；爬虫加平台许可过滤器完成
  2. **Duplicate removal**：用感知哈希加 CLIP 相似度去重（程序）
  3. **Data table extraction**：Gemini-2.0-Flash 和 GPT-4o-mini 并行抽表，两者一致就直接收；不一致时由 GPT-4o 第三票裁决，还不一致才交人工。产出 61,833 张带表的真实图
  4. **75 chart types & 440 variations**：人工参照 Data Viz Project、Datylon 两套分类，归纳出 75 类图型、440 种视觉变体，全部用 D3.js 实现成可参数化的渲染程序
  5. **Text** / **Image**
     - 文字：先检索后生成。Sentence-BERT 按主题和数据事实检索 3 张最相关的真实图作为 in-context 示例，再让 Gemini-2.0-Flash 写标题和副标题
     - 图片：从 Icon645、Noun Project 等来源建图标库，先用启发式规则去掉墨水比低、分辨率差、长宽比极端的图，再由 Gemini-2.0-Flash 给每张图写关键词和描述，剔除过于写实或杂乱的，最后得到 681,459 张。检索时拿 Sentence-BERT 比对关键词和标题
  6. **68 layout templates**：人在环路里扩展模板。3 位作者先在 1,500 张真实图上标框，归纳出 55 个模板 → 用这些模板合成 12 万张带框图，训练 InternImage + DINO 检测器 → 在未标注真实图上检测元素（文字用 PP-OCRv4）→ LTSim 相似度低的布局作为候选 → k-means 聚类后人工看中心，新增 13 个模板，共 68 个
  7. **Synthetic infographic chart**：数据表先按规则映射出候选图型，候选有多个时由 Gemini-2.0-Flash 挑；变体用 adaptive sampling 抽，偏向出现少的变体；配色取自真实图的调色板。布局求解时先滤掉与元素冲突的模板，再对剩下的做网格搜索式紧凑排布（约束问题），选墨水比最高的那个
  - （图外）**数据表来源**：真实表 200,085 张（VizNet、UN data、Our World in Data、Papers with Code），另有 Gemini-2.0-Flash 合成的 98,483 张；每张表都由 Gemini-2.0-Flash 补一个主题和若干数据事实
- **质量控制**
  - 真实图抽表：43.6% 在双模型一致时直接接受；剩下 56.4% 里，GPT-4o 解决了 76.2%。合计 86.6% 全自动完成，13.4% 由人工校正。抽查 200 条完全一致的样本，全部正确
  - 一致性判据：数据点数相同、列名和类别值相同、数值偏差 ≤ 5%
  - 敏感话题：用 Gemini-2.0-Flash 过滤宗教冲突、可识别个人的医疗记录等内容
  - 合成图的配套框标注来自程序本身，不需要人工
- **关键数字**
  - 规模：1,701,356 张合成图 + 61,833 张真实图；75 类图型 / 440 种变体 / 68 个模板
  - 指令集：从 70,248 张图生成 443,455 条 QA
  - 下游：InternVL3-8B 在 InfographicVQA 上 +3.80、ChartQAPro 上 +5.98；Qwen2.5-VL-7B 分别 +4.44、+3.59；在自建评测集上整体 +26.87 / +23.85
  - 消融（InternVL3-8B，自建评测集）：只训真实图 55.74，只训合成图 76.08，两者都训 80.07
  - 代码基准：500 张合成图，测 D3.js 复现；Gemini-2.5-Pro 最高，总分 85.21
- **局限**
  - 只有单图信息图，没有多图叙事（论文自述）
  - 真实图只发布 URL，不发原图
  - 合成图的收益主要体现在自建集上；InternVL3 在 ChartQAPro 上只训真实图（42.58）反而略高于只训合成图（41.76）
  - 模板扩展和抽表的兜底环节仍依赖人工
- **可借鉴**
  - 「归纳 → 程序化」闭环：先从真实数据里抽图型、变体、模板，再用合成数据训检测器反过来挖掘新模板
  - 双模型交叉抽取、第三模型仲裁、最后才人工兜底：把人工比例压到 13.4%
  - 用墨水比加最小间距约束做自动排版，美观度指标可以直接算出来

