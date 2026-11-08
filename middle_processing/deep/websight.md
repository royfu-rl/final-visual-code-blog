- **定位**：第一个百万级、完全合成的「截图 → HTML + Tailwind」配对数据，被 Design2Code 等后续工作当作训练集基线

<figure class="paper-fig"><div class="flow"><div class="step"><b>Website concepts</b>Mistral-7B 批量出网站概念</div><span class="arr">→</span><div class="step"><b>Tailwind only</b>规定只用 Tailwind，HTML 自包含</div><span class="arr">→</span><div class="step"><b>Code LLM</b>Deepseek-Coder-33B 写整页 HTML</div><span class="arr">→</span><div class="step"><b>Filtering</b>去掉空泛 / 配图不符的页面</div><span class="arr">→</span><div class="step"><b>Screenshot</b>Playwright 渲染整页截图</div></div><figcaption>WebSight · 自绘流程图（论文无管线图，依据正文描述）</figcaption></figure>

- **自动化合成流程**（对照上面的自绘图）
  1. **Generating diverse website concepts**：Mistral-7B-Instruct 用一条固定 prompt 批量生成网站概念，每次 10 个，要求公司领域、配色、布局位置各不相同，累计几百万条
  2. **Opting for Tailwind CSS**：规定只用 Tailwind 工具类，让 HTML 自包含、不需要外部样式文件，代码更短、更好学
  3. **Using a code specialized LLM to generate the HTML codes**：Deepseek-Coder-33b-instruct 把概念写成完整页面。prompt 禁止出现 Lorem ipsum；图片一律写成 `source.unsplash.com/random/WxH/?keyword`，按关键词动态取图
  4. **Filtering**：丢掉文字太少、内容空泛、配图与主题不符的页面，剩下 200 万
  5. **Screenshot capture process**：Playwright 渲染并截取整页，所以截图分辨率不固定
- **质量控制**
  - 只有第 4 步这一道过滤，标准如上；论文没给过滤掉多少
  - 训练时发现验证 loss 不能反映真实效果，改为人工看生成样例来选 checkpoint
- **关键数字**
  - 规模：v0.1 有 823K 对（HTML + 传统 CSS，图片是色块占位）；v0.2 有 200 万对，是 v0.1 的 2.5 倍，换成真实图片和 Tailwind
  - 训练：自家 8B VLM（Mistral-7B + SigLIP-SO400M）用 DoRA（rank 64）微调，每步 2016 个样本，共 1100 步，不到 1 个 epoch，得到 Sightseer
  - 下游：论文只做了定性评测，没有给量化指标
- **局限**
  - 页面结构简单，复杂布局、长文本、和训练分布差异大的设计都复现不好（论文自述）
  - Tailwind 在基座预训练语料里出现得少，模型偶尔写出错误语法，或者文字和背景同色
  - 图片 URL 是随机取图，同一段代码再渲染一次，得到的图可能不同（推断）
- **可借鉴**
  - 两段式生成：小模型负责发散主题，大的代码模型负责落地，多样性和代码质量分开控制
  - 选输出格式时优先考虑「单文件自包含」，这样训练目标更干净
  - 用带关键词的图库 URL 当图片占位，既省掉生图步骤，又让截图里有和主题相关的真实图片

