# Verifier / Reward Function 设计素材库

> 用途：写博客正文时的取材来源。**不是成稿**。
> 数据源：`/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/`（只读）
> 整理日期：2026-10-19。本库未联网，所有内容来自上述目录。

## 0. 口径约定（引用前必读）

**出处写法**：`04_verifier.md:34-42` 指该文件第 34–42 行。下文文件名一律省略目录前缀。

**四级证据等级**（引用时务必带上，笔记自己就是这么标的）：

| 等级 | 含义 | 风险 |
|---|---|---|
| **[本机实测]** | `scripts/vc_verifier/` 下跑出来的数 | 单场景、单参考页、M=1；只能说「机制存在」，不能说「效应量是 X」 |
| **[核实]** | `92_number_audit.md` 回原文逐值定位过 | 可直接用 |
| **[引用]** | 调研 agent 的一手引用，没有二次核验 | 要带出处性质 |
| **[推断]** | 笔记作者的推论，无实测无文献 | 不能当结论写 |

**92_number_audit.md 的三条铁律**（`92:95-104`）：
1. 抽查了十四组数字，**十三组一致，一组不通过**，另有一处措辞因逐值复核而收紧。
2. 「抽查的命中率不是 100%，所以抽查必须做。」
3. 「**最容易出错的不是数字本身，是数字的归属。**」两次出错都不是打字错误，是语义错位（评测对象对不上；把「判定方式的通过率」当成「模型的能力」）。

**已被更正、不许再用旧版的数字**（`92:76-86`，这节用错一个就全错）：

| 旧版（禁用） | 新版（用这个） |
|---|---|
| 3JSBench 743 条必查项 | **695 条** |
| WorldCoder-Bench 2.7% 当模型能力 | 2.7% 是「截图加 VLM」这种**判定方式**的通过率；模型的隐藏契约覆盖率是 **27.8%**（严格档 19.9%） |
| 3DHarnessBench 增益 5.3% / 16.4% | **9.3% / 20.1%** |
| 组大小 8、通过率 0.1 时全零组概率 19% | **43.1%**（19% 对应组大小 16） |
| 带截图的 issue 约 1 万量级 | **约 1,400 个** |
| 可访问性「零噪声」 | 「**判定本身零方差但覆盖面窄**」（axe 105 条里纯自动可判只有 41 条） |
| 某 CAD 评测「带工具 0.821 对不带工具 0.366」三行 | **整组删除，负相关结论一并撤回** —— 但 `16_primary_sources.md:1075` 又把同一组数字当一手材料写回来了，见 §8 矛盾清单第 1 条 |
| 动画机制 闭源 21.5% Avg@8 对开源 72.2% Pass@8 | **整行删掉**（两个量不可比） |
| 判别力靠训比堆参数便宜 30 倍 | 加限定词（原文两次称其为朴素外推，只在一个分布上测过） |
| BlenderAlchemy 四轮分数「单调下降」 | 逐轮是 27.4 / 26.1 / 26.5，改成「一路走低，没有一轮回到起点」 |
| WebCoderBench a11y「9.9%」当分数 | 那是**人类偏好权重**；真的 9.9% 是 A11yn 附录 K 的 Best-of-N 平台期（`14_web_verifier.md:719-735`） |

**没有独立核验的**（`92:63-67`）：AutoLab 的 0.68 / 0.46；Vibe Code Bench 的榜单分；**A11yn 的全部数字**。

**一条贯穿所有模态的总原则**（出现频率最高，建议当正文主线）：

> **verifier 能查的信息量必须小于等于题面给的信息量。**

- 生成侧实测：`90_local_experiments.md:§5`（杯子木色、桌腿居中两例）
- 判别侧实测：`10_blender_tasks.md:552,566-567` —— 留出集唯一的误杀是 `sun_energy 3.0→3.5`，题干只说了「加一个太阳」。处方逐字抄：「**修法是补白名单，不是调容差。**」（`10:832`）
- 官方对偶（Anthropic 自己的话，`16_primary_sources.md:569`）：「A good task is one where two domain experts would reach the same verdict and **everything the grader checks is stated in the task**.」
- 覆盖面的对偶（OpenAI `playwright-interactive`，`16:1570-1579`）：QA 清单由三个来源构成（用户需求、你实际实现的功能、**你打算在最终回复里声称的东西**），「Anything that appears in any of those three sources must map to at least one QA check before signoff.」—— 两条合起来是**双向约束**：判据不能超出题面，也不能少于声称。

---

## 1. 纯文本 query（text→web / text→3D）：没有参考图时 reward 怎么设计

**结论先行**：这一节素材最厚。没有参考图不是缺陷，反而是最干净的设定 —— 因为**参考解的「状态」比参考图信息量大得多，而且噪声地板是 0**。本机三条线（three.js / Blender / Web+图表）全部是在这个设定下跑出来的。

### 1.1 可用的确定性判据与实测噪声地板

#### 1.1.1 3D 侧（Blender，九族状态断言）

`10_blender_tasks.md` 的 desk_lamp 实验**就是纯文本 query**：题干写在参考脚本的 docstring 里，不给参考图（`10:10`）；verifier 比的是参考解的探针输出（state.json + 多视角渲染 + 点云，`10:262`）。

九族定义与判别力（`10:236-249` 的进闸决定逐字抄）：

| 族 | 查什么 | 进闸决定 | 合并 22 变异上的 总对/检出11/保真11 |
|---|---|---|---|
| A1 层级与命名 | 名字集合、`o.type`、`parent.name`、collection 归属 | **条件进**（只查题干点名的物体） | 12/22 · 2 · 10 |
| A2 变换 | **世界 bbox 八角点**，不是 `o.location`/`o.scale` | **不进**（改用世界 bbox 或几何指标） | 10/22 · 3 · **7** |
| A3 网格统计 | `non_manifold_edges`、`volume` 符号、`ngons`、面数预算 | **不进等式**；只留不变量与预算不等式 | 8/22 · 2 · **6** |
| A4 修改器栈 | `m.type` + `width`/`segments`/`levels`/`count` | **进** | 13/22 · 2 · 11 |
| A5 材质节点树 | 按 `bl_idname` 比类型与连边，不按 `node.name` | 条件进（只查题干钉死的 socket） | 11/22 · 1 · 10 |
| A6 灯光相机 | `L.energy`、`L.color`、`C.lens`、active camera 身份 | **进**（按字段白名单） | 12/22 · 2 · 10 |
| A7 动画 F-curve | 逐关键帧 `(co[0], co[1], interpolation)` + `c.evaluate(frame)` | **进** | 12/22 · 1 · 11 |
| A8 物理与约束 | `c.type`/`target`/`influence`；`rigid_body` 字段 | **进** | 11/22 · 0 · 11（本批没造 A8 变异） |
| A9 渲染设置 | `engine`、分辨率、fps、帧范围、samples、view_transform | **进**（精确相等，不需要容差） | 11/22 · 0 · 11 |
| **九族全查** | —— | **反面教材** | **11/22 · 11 · 0** |

**噪声地板 = 0**，而且是逐位的：参考解跑两遍，图像 1.0000、Chamfer 0.0、体素 IoU 1.0（`10:494-496`）。直接后果写在原文里：「**所以阈值不能从噪声推，只能按「什么算语义等价」来定。**」

**但零噪声是有条件的**（这条特别适合写进正文，因为它是「噪声地板不是天然为 0」的反例）：`trimesh.sample.sample_surface` 自带 RNG，`np.random.seed` 对它无效；不传 `seed=` 时**参考解和自己比的 Chamfer 是 0.00167 而不是 0** —— 而 pass/fail 的 Chamfer 带宽只有 0.0016~0.0065，「噪声地板直接吃掉一半判别力」（`10:866-867`）。

渲染跨机不可复现：「换 CPU / 换 Mesa 版本像素会漂」，处方是**在任务容器里重渲自己的参考基线**，不用仓库里 check in 的 PNG（`10:457-458`）。Blender 官方自己的办法是设备黑名单 + `set_pixelated(True)`，不是调阈值（`10:423-424`）。

#### 1.1.2 3D 侧（three.js，四层判别力）

四层定义逐字（`90_local_experiments.md:78-85`），颜色归并容差 60：

29 个变异上的判别力（`90:100-106`）：

| 信号 | 抓到 / 29 |
|---|---|
| 单张像素比对 | 12 |
| 几何类别多重集 | 14 |
| 多视角剪影 IoU | 19 |
| 逐颜色体素占据 | 25 |
| **四层组合** | **29** |

留出测试（`90:§2.3`）：换一个场景（car，9 个 mesh），**18 个变异在跑之前就贴好标签，阈值一个字没动 → 18/18**；累计 47/47，其中 18 个是真留出。

拓扑量的价值：`ok_lathe` 的翻盘不是调阈值得来的，是补了一个**开放边界边数**（只被一个三角形用到的边）信号，0 对 64（`90:§3.4`）。原理：它是拓扑量，不随洞的大小衰减，所以能抓住被全局 IoU 淹没的小破洞（`15_game_verifier.md:179` 的转述）。

#### 1.1.3 Web 侧（DOM / computed style）

- **231 个字段，5 次重复里只有 4 个会变；所有参与判定的字段逐字节相同**（`14_web_verifier.md:§4.2`）。
- 五层组合在 22 个变异上 **22/22**，检出 11/11，误杀 0/11（`14:§4.5`）。
- **两次完整重跑，判定翻面 0 次**（`14:§4.8`）—— 对照 3D 侧 VLM judge 最差档约 28%。
- 诚实披露：**22/22 是第二次跑的结果，第一次是 21/22**，两个不同原因（一个真的 verifier bug 用了 `.card` 类选择器；一个变异脚本 bug，全局正则把 `role="tablist"` 也改了）（`14:§4.10`）。
- 类名序列这一层**检出 0/11、误杀 3/11** —— 负面教材，适合写「不是所有确定性信号都有判别力」。

#### 1.1.4 审美侧（这是「纯文本 query」最独特的一块）

`19_aesthetics.md` 全文都是纯文本 query → 生成网页，**明确排除参考集**：「前提：没有参考集（real set），所以 FID / KID / precision-recall / density-coverage 全部排除，只能用 reference-free 指标」（`19:512`）。探针**只读 computed style 与几何，不做像素比较、不调 VLM**（`19:912`）。

九条冻结判据与参考页实测值（`19:990-1000`）：

| 判据 | 阈值（参考页实测） | 验证变异 |
|---|---|---|
| `hier` h1..h6 字号单调不增且 ≥ 正文 | 违例数 = 0（参考 0） | A01、A02 |
| `scale` 字号种类数与相邻比值 CV | 种类 ≤ 11（参考 7）；**CV ≤ 0.35（参考 0.133）** | A12 |
| `family` 字体族数量 | ≤ 2（参考 1） | A03 |
| `lh` 正文行高倍数 1.35~1.8 | 越界段数 = 0 | A04 |
| `len` 每行字符数 | ≤ 90（参考 42.8） | **未验证** |
| `hue` 色相家族数与色相熵 | 家族 ≤ 3（参考 1）；熵 ≤ 2.0（参考 0） | A06 |
| `contrast` WCAG 1.4.3 | 不达标样本 = 0（参考最小比值 6.27） | A06、A11 |
| `spacing` 间距种类数 + 自动选基数后倍数占比 | 种类 ≤ 20（参考 12）；**占比 ≥ 0.70（参考 0.914 @ base=2）** | A07、A10 |
| `ink` 墨水覆盖率 | **0.06 ~ 0.78**（参考 0.296 / 0.526） | A10 |

实测结果（`19:917-923`）：参考页 11 条全过；该挂的抓到 **9/11**；不该挂的 **8/8 零误杀**；单变异约 **0.8 秒**，纯 CPU，无 GPU。**两次独立运行 20 个 case，连每一条连续读数都逐位相同（0/20 不一致）**（`19:1041`）。

> **「别从设计教条里抄阈值」的黄金实例**（`19:93-110`，强烈建议进正文）：
> 一个手写、axe 全过、多视口不塌的参考页，间距取值落在各基数倍数上的占比是
> **2 → 91.4%；4 → 57.8%；8 → 32.8%；10 → 20.7%；16 → 16.4%**，共 12 个不同取值（2/6/8/9/10/12/14/16/19.9/20/24/28）。
> 「一个好页面只有 **57.8%** 的间距落在 4 的倍数上。任何写死「间距必须是 4 的倍数」的 lint 规则都会把它判挂。」
> 正确做法：**自动选基数再看占比**，判据改成「存在某个基数使 ≥70% 的取值是其倍数」，参考页在 base=2 下是 0.914，余量 0.214。
> 工程铁律（`19:110`）：**审美类程序化判据的阈值必须从参考页反推，不能从设计教条里抄。**

审美侧覆盖面的上界（这条很重要，别把程序化判据吹过头）：**纯规则 lint 的召回只有 22.9%~32.3%**（DesignRepair 的 UIS-Hunter 基线），而带知识库的检测能到 92.1% / 83.3%（`19:186`）[引用]。

#### 1.1.5 图表与矢量图（逐值回读）

- **成本**：回读 **1 到 4 毫秒**，是渲染耗时的 4/1000，比截图便宜两个数量级（`17_chart_verifier.md:§4.1`）。
- **噪声地板**：5 次重复逐位相同，md5 单一；参考图自己对自己 **canvas 0.15%**（固定偏差，距 1% 阈值有 6 倍余量）、**SVG 0.02%**（`17:§4.2`）。
- 16 个变异上：**S1（逐值回读）13/16，零误杀；S3（结构断言）14/16，零误杀；S1 OR S3 = 16/16**；对照 S2（像素）9/16 且 4 个误杀（`17:§4.3`）。
- 三个 verifier bug 全是**假阳性**、全是坐标系/画幅问题、**全都不是调阈值能修的**；修完 S1 从 12/16 到 13/16，S3 从 13/16 到 14/16 —— 判别力的提升**纯粹来自消除假阳**（`17:§4.4`）。
- 四环噪声表（`17:§5.1`）：渲染 0、回读 0、比对 0，**唯一的噪声源是「题面到判据的对齐」，而且这一环没测过**。

#### 1.1.6 游戏侧（也是纯文本 query）

33 条去重子命题里 **24 条全确定性、6 条需要会玩的策略、3 条只能靠人**（`15_game_verifier.md:0节` + `15:165-167`）。
**纯程序判据（A/B/E/F 族）的噪声地板是 0（重放逐字节一致）**，原文强调：「这是它们真正的优势 —— 不是更准，是**没有方差**」（`15:§1.4`）。

### 1.2 VLM / reward model 在「无参考图」下的实测可靠性

这是本节最硬的一组对照，**直接回答「没有参考图时 VLM 还能不能用」**。

`90_local_experiments.md:702-706`（`judge_noref.py`，同一标注集）：

| 条件 | 判对率 | 检出率 | 保真率 |
|---|---|---|---|
| **给参考图** | **94% / 97%** | 92%~95% | —— |
| **不给参考图（只给题面）** | **68% / 76%** | **61%~63%** | 4 视角下仍 39/40 |

读法：去掉参考图，**判对率掉 20 多个点，检出率掉 30 个点，但保真率几乎不动** —— 也就是说无参考图的 VLM 变成了一个「几乎不误杀、但一半错误抓不到」的器件。对应的工程结论：**无参考图时 VLM 只能当补抓，不能当闸。**

Blender 侧单次实测（`10:757-766`，4 judge × 2 视角条件，temperature 0，176 次调用，并发 12 下 865 秒）：

| judge | 条件 | 总对/22 | 检出/11 | 保真/11 | JSON 坏 |
|---|---|---|---|---|---|
| gpt-6-astra | single | 16 | 5 | 11 | 0 |
| gpt-6-astra | multi | 16 | 6 | 10 | 0 |
| claude-opus-5-5 | single | 13 | 3 | 10 | 0 |
| claude-opus-5-5 | multi | 14 | 4 | 10 | 1 |
| gemini-3.8-flash | single | 14 | 4 | 10 | 0 |
| gemini-3.8-flash | multi | 15 | 4 | 11 | 0 |
| doubao-seed-2.1-pro | single | 14 | 4 | 10 | 1 |
| doubao-seed-2.1-pro | multi | 14 | 3 | 11 | **3** |

四条可直接引用的结论：
1. **VLM 的形状是「高保真、低检出」**：保真约 11/11，但 11 个真错误只抓到 **3~6 个**；程序化 `combo_pc` 是检出 11/11 + 保真 10/11（`10:768-769`）。
2. **多视角拼图几乎没用**：16→16、13→14、14→15、14→14；而且**拼图把解析失败率拉高了**（doubao multi 坏 3 个）（`10:770-771`）。
3. **VLM 独占的检出：没有。**22 个变异里 VLM 抓到的每一个，程序化信号都抓到了（`10:807`）。
4. **VLM 的误杀集中在相机**：`camera_moved`（该过）被 **8 个条件里的 4 个**判错，**尽管题面明确写了相机位置变化不算错误** —— 「VLM 分不清『画面变了』和『场景变了』」（`10:777-779`）。

重测翻面率（这是 VLM 噪声地板的唯一本机数）：`90:168-174`，4 个不同家族 judge、48 个 case、temperature 0、每种条件跑 2 次 → **单模型重测翻面率 4.2% ~ 20.8%**，最差是 **claude-opus-5-5 在多视角档 20.8%**。对照：4 模型 8 票多数投票单视角 44/48、多视角 46/48，而**程序化信号在同一标注集上是 47/47**（`19:873-876` 转引）。

Blender 侧的诚实缺口：**VLM 只跑了 1 遍，没有自一致率数字**（`10:843`）；`should` 标签只有 1 个标注者，**没有一致率**（`10:841-842`）。

无参考图下的 rubric 用法（关键，`03_verifiable_construction.md` 的 RaR）：
**Reference-Likert 31.7% < 无参考 rubric 32.0% < 带参考 rubric 35.9%**。
→ **参考的正确用法是去「生成 rubric」，不是当比较对象。** 这条解释了为什么无参考 rubric 能和带参考的 Likert 打平。

游戏侧 LLM judge 的三条公开噪声地板（`15:§1.4`，这是视频/录屏那节也要用的）：
- 同一个 LLM judge 重判同一条规则，**同谓词结构**时重判分差 ≥0.25 的比例是 **12.7%（Small）/ 8.8%（Big）**；**结构不同**时升到 **17.7% / 11.1%**（A2Z 附录 B.5 表 S10）。
- 换 judge 配置、固定轨迹：一致率 **0.910 / 0.888**（222 条里 6 条、242 条里 3 条改了判分）。
- 人与人同 rubric：**91.4% / κ=0.68 / α=0.624**。
→ 原文推论逐字：**「LLM 参与的游戏判定上，3 个百分点以内的效应不要信。」**

### 1.3 已知 hack / reward 被刷穿的具体实例（纯文本 query 设定）

| # | hack | 数字 | 出处 |
|---|---|---|---|
| H1 | **九族全查 = 判别力归零** | 检出 11/11，但语义等价改写**误杀 11/11**；保真 **0/7**（dev）、**0/4**（holdout）。误杀集中在 A2（`cube(size=1)+scale1.2` 改写成 `cube(size=2)+scale0.6`，世界形状一模一样）和 A3（圆柱 16→32 段、圆环 minor 8→12） | `10:35-37,249,540,560,591` |
| H2 | **全局平均被小部件骗穿** | 杯子平移 **30 cm**，全局 Chamfer 只从 0 变 **0.00018**，全局 F@0.5% **0.9916**（能过 0.99 闸）；逐部件 Chamfer 0.08375、F 0.2243 —— **460 倍**差距。全局 F-score 在合并集上检出 **0/11** | `10:708,721-723,580` |
| H3 | **低于采样分辨率的需求无法用几何验** | `bevel_removed`（1 cm 倒角 / 2.18 m 对角 = 0.0046 diag ≈ tau）通过**所有**几何与图像信号：剪影 0.9831、逐部件 F 0.9992、全局 F 1.0000。原文警告：只比渲染图的话这类扰动会造出「**无解噪声任务**」 | `10:512,728-729,367` |
| H4 | **静帧看不见的属性让所有图像+几何信号给满分 1.0000** | `bulb_dim`（60 W→6 W）和 `anim_missing`（删掉全部关键帧）在 view0 / 多视角剪影 / Chamfer / 全局 F / 体素 / 逐部件 F 上**全部 = 1.0000** | `10:510-511,180-182,199-201` |
| H5 | **verifier 知道的比题面多** | 杯子木色、桌腿居中两例；留出集唯一误杀 `sun_energy 3.0→3.5` | `90:§5`；`10:552,566-567` |
| H6 | **容差边界误杀** | roughness 0.60→0.62 正好落在 0.02 容差边上，A5 把它杀了，而那个字段题面从没钉死 | `10:164-165,518` |
| H7 | **开放曲面体素化 + 小部件等值判断** | 0% 通过率那个任务叠了两个问题：开放曲面体素化重叠只有 0.017；灯罩在 48³ 下只占 **20 个体素** → 「**小部件上的占据类指标不是相似度，是等值判断**」 | `90:§6` |
| H8 | **离屏渲染器作弊页一开始真的成功了** | 修法两条：只统计在文档内、有尺寸、未隐藏的 canvas；把离屏渲染次数当**蜜罐信号** | `draft_verifier.md:§5,§7` |
| H9 | **换成整体美学分 → 堆叠重叠描边与重复装饰** | 美学分 **4.309 → 6.697**，而 rubric 分 **0.395 → 0.262（低于零样本基线）**、输出 token **0.3k → 6.3k（21 倍）**。换成结构化 rubric 后，hack 换成「把 query 词画成风格化标签」，分从 0.693 压到 0.536 | `19:131,130,347,360` |
| H10 | **经典计算美学指标全部单调可刷** | 白空间越多、边缘越少、颜色越少、对齐线越少分越高 → **RL 必然收敛到空白单列页**。AIM 的 `cp11` 色彩和谐源码自带两条警告：形式化来自照片增强「This is not proven for user interfaces」；**模板 X 几乎总是最小距离** → RL 会学会「把颜色铺满色轮」 | `19:58,249-250,271-274` |
| H11 | **reward 在最优点附近反向** | Duan et al. CHI 2024：「general decrease in performance as the UI improves」，首轮 **52%** 准确到后续迭代掉到 **39%** | `19:60,187,293` |
| H12 | **审美判据自己的五种可刷形态**（[推断]，未实测） | ① 塌缩到极简白页（`ink` 下界 0.06 挡一部分）② 整页做成一张图（加文本节点数下界 + OCR 对账）③ 色相熵刷低（熵只设上界是故意的）④ 间距基数刷高（**目前没设种类数下界**，应补「≥3」）⑤ tell 规避（换 Space Grotesk + 青绿渐变） | `19:1013-1021` |
| H13 | **作弊页测试** | `hack_probe.py` 5 个可用作弊页，**verifier 通过 0 个**（真实分母是 12 里的 5） | `90:§13` |
| H14 | **变异集不能既当调参集又当验收集** | `11_hacking_defense.md:§2.1` 自己的警告：颜色容差 tol=60 是在同一批 13 个变异上调出来的，所以 13/13 是过拟合 | `11:§2.1` |

### 1.4 分层组合方式、权重与公式（逐字抄）

#### 1.4.1 Blender 侧：**纯 AND 闸，没有任何加权分**

`10_blender_tasks.md` 全文**没有一个加权求和**，每条判据都是合取（这一点本身就是素材）。

组合定义（`10:493`）：
```
combo_pc = geom_pc ∧ A4 ∧ A6 ∧ A7 ∧ A9
```

推荐落地判据（`10:818-829`，本机 22 变异 21/22）：
```
pass = 分部件 F-score@0.5%diag >= 0.99                 # 形状、位置、朝向、颜色
       ∧ spec 白名单内的 A4 修改器断言                  # 渲染看不见
       ∧ spec 白名单内的 A6 灯光相机断言                # 渲染看不见
       ∧ spec 白名单内的 A7 F-curve 断言                # 静帧看不见
       ∧ spec 白名单内的 A8 约束物理断言                # 静帧看不见
       ∧ A9 渲染设置精确相等                            # 题干写死就查
       ∧ A3 的不变量（流形性 / 法线朝向），不查顶点数等式
       ∧ 候选脚本 exec 无异常
```

阈值（跑变异之前就冻结，`10:494-496`）：图像 **0.995** / 剪影 IoU **0.97** / Chamfer ≤ **0.004 diag** / 体素 IoU ≥ **0.80**；逐部件 F 的 **0.99** 是唯一后定的一条（从 pass 组下限 0.9989 反推，已标注，`10:838-839`）。

字段白名单（四条路线都绕不开，`10:255-266`）：
```
task/
  prompt.md      题干（自然语言 + 可选参考图）
  spec.json      被钉死的字段清单（verifier 只查这些）
  ref.py         参考解 bpy 脚本
  probe/         参考解探针输出：state.json / view_*.png / points.npz
```
`spec` 行 schema = `(族, 字段路径, 容差)`；难度调节 = 钉死的 slot 数 + slot 之间的依赖深度。

槽位容差表（`10:292-298`，逐字）：
```python
SLOTS = [
    Slot("table.size",   dom=[(0.8,2.0),(0.5,1.2)], family="A2", tol=0.005, phrase="一张 {0}×{1} 的木桌"),
    Slot("table.bevel",  dom=[(0.005,0.03)],        family="A4", tol=0.02,  phrase="桌面边缘倒角 {0}"),
    Slot("bulb.energy",  dom=[(20,200)],            family="A6", tol=0.02,  phrase="点光源 {0} W"),
    Slot("arm.anim",     dom=[(-40,0),(0,40)],      family="A7", tol=0.01,  phrase="灯臂第 1~40 帧从 {0}° 转到 {1}°"),
    Slot("mug.subsurf",  dom=[0,1,2],               family="A4", tol=0,     phrase="杯身加 {0} 级细分"),
]
```

tau 选择的三条硬规则（`10:689-700`）：
1. **tau 小于采样间距时，F-score 测的是采样密度，不是几何**。tau=0.1% diag（2.2 mm）时，该过的 `mug_seg_48` 得 0.4977，**低于**该挂的 `shade_flipped` 0.9639，完全倒挂（60k 点 / 2.18 m 场景 → 平均点距约 3~5 mm）。
2. tau 太大只能抓「整个部件消失」：tau=1% diag 时，8 个该挂的里只有 1 个低于 0.99。
3. **不存在一个全局 tau 能分开该挂和该过**：0.5% 时该挂的 0.9993 / 0.9985 和该过的 0.9993 数值重叠。
→ 建议：**tau = 0.5% diag 且逐部件算**；安全下界 `tau >= 3 × 平均最近邻距离`，用参考解自采样两次估。

成本（`10:596-610,733-744`）：单次探针 **1.61~2.43 秒，均值 2.3 秒**（exec 0.23~0.30 / 读九族状态 0.07~0.15 / 采 59,992 点 0.15~0.21 / Workbench 渲 10 视角 256² 1.09~1.24）；**几何全套约 0.4 秒**（Chamfer+HD95 107 ms、F-score 106 ms、32³ 逐色体素 36 ms）vs 10 视角渲染 1.1~1.2 秒。
→ 逐字结论：「**几何指标比渲染便宜 3 倍，而且判别力更高**」（逐部件 F 检出 7/11 对多视角剪影 3/11），「**如果只能留一个视觉信号，留几何，不留渲染**」（`10:743-744`）；「**渲染图只用来给模型看，不用来判分**」（`10:855-856`）。

#### 1.4.2 Web 侧：W0–W4，**门控是乘法的**

定义（`14:62-66`）：W0 正确性 → W1 布局/响应式 → W2 a11y → W3 交互/状态 → W4 性能预算。逐字：「**门控是乘法的**」。

#### 1.4.3 审美侧：L0–L4，哪几层做闸、哪几层做分（`19:889-896`，逐字）

| 层 | 内容 | 采样 | 噪声 |
|---|---|---|---|
| L0 硬闸 | 能跑、画布非空、无运行时报错 | n=1 | 0 |
| **L1 审美硬闸** | §6.4 的 6 条已验证判据（hier/scale/family/lh/hue/contrast/spacing） | **n=1** | **0** |
| L2 功能断言 | DOM 状态、交互前后差分、多视口不塌 | n=1 | 低 |
| L3 rubric 化模型评审 | 只放 Design quality 与 B 类子项；**输入必须含关键源码片段** | r=3 多数票，**降噪按 r=2 计** | 中高 |
| L4 组内 pairwise | 同一 query 的通过者两两比，AB/BA 各一次，不一致记 tie | 组内 | 较低 |
| 校准集 | 200 对专家裁决，每条至少 3 人（目标 7 人） | 季度重标 | ICC 0.637 → 目标 0.80 |

→ [推断] 「审美维度的迭代信号应该主要来自 **L1 的零噪声硬闸**（通过率可以 n=1 读），而不是 L3 的 rubric 分」（`19:901`）。

三档处置（`19:1029-1033`，这段可以整段改写进正文）：
- **档1 今天就能做成零噪声程序化 reward**：对比度、层级单调性、字号尺度自洽、字体族数、行高、色相家族数与熵、间距节奏与基数、墨水覆盖率上下界、多视口不塌 → **乘法硬闸，不计权重，不过就截断后续评分。n=1 即可读，0.8 秒/页，纯 CPU。**
- **档2 rubric 化模型评审**：排版品味、配色协调、组件一致性、动效克制、整体感与识别度 → **闸后**做组内 pairwise（**不做 pointwise**），AB/BA 各一次，r=3 但降噪按 r=2 算，输入必须含关键源码片段。
- **档3 彻底放弃当 reward，只当验收**：风格取向、品牌调性、原创性整体、**圆角一致性、栅格对齐**、全部经典计算美学指标 → 原创性只保留**具名 tell 的负向闸**；经典指标只能当 **veto**（density 远离 50% 时打回），**绝不当排序器**。

> **权重倒置论证**（`19:336-350`，强推进正文，因为它和 Anthropic 官方做法正好相反）：
> Anthropic 官方降权 Craft / Functionality 的理由逐字：「Claude already scored well on craft and functionality by default, as the required technical competence tended to come naturally to the model.」（`16:73`，`19:339`）
>
> | | 推理时 harness | RL |
> |---|---|---|
> | 没区分力的维度 | 浪费权重，该降权 | **正是最安全的硬闸**：不提供优化压力，但能挡住塌缩 |
> | 有区分力的维度 | 该加权，推模型冒险 | **最容易被 Goodhart** |
> | 「模型默认就及格」 | 观察到的事实 | **会在训练中失效**：一旦别的项提供了优化压力，模型会拿 craft 去换分 |
>
> [推断] 处置：把 Craft 四个分项**全部做成乘法硬闸**（不计权重、只决定是否进入后续评分），Design quality 放在闸后做 rubric 化组内 pairwise，Originality 的 tell 做**负向闸**。

#### 1.4.4 游戏侧：L0–L5（`15:§1.3` + `15:§5.4`，阈值先定死不许回头调）

```
L0 执行门   未捕获异常数 > 0 → fail；600 帧后 rAF 回调计数 < 600 → fail；首 10 帧内无绘制调用 → fail
L1 响应门   T1 与 T0 的状态指纹序列完全相同 → fail
            键盘-only 轨迹与 T0 相同，或鼠标-only 与 T0 相同 → fail
            同一轨迹两次跑的指纹序列 SHA256 不等 → fail（判为 harness 问题，单列一桶）
            down→20 帧→up→20 帧 的后 20 帧位置增量 > 1 像素 → fail
L2 规则门   极端同向输入 1000 帧后挡板中心出界 → fail
            球的相邻帧位移线段穿过砖块或墙 → fail
            T2 全程 HUD 数字从未严格递增 → fail
            命数到 0 后 60 帧内未出现终局画面 → fail
L3 退化门   第 500~600 帧的绘制调用数对帧号线性拟合斜率 > 0.5 → fail
            连续 120 帧状态指纹完全不变且非终局 → fail
            画布像素熵 < 阈值，或 HUD 与背景对比度 < 3:1 → fail
            同一帧渲两次像素差异 > 100 个像素 → fail
L4 完成门   T2 在 3 个种子里 0 次打完全部砖块 → fail
L5 平衡门   T0 的最终分数 > 0 → fail（不动不该得分）
            T3 十个种子的分数均值 > T2 分数的 0.6 倍 → fail（乱按就能赢）
            T2 − T3均值 的归一化分差 < 0.40 → fail（技能不可分辨）
            T3 十个种子的分数标准差 / 均值 > 2.0 → fail（方差爆炸）
```
阈值来源的诚实标注（`15:§5.4` 逐字）：`0.40` 来自 RAPP 的 0.665 对 0.245 取中间偏严；**`0.6 倍` 和 `2.0` 是拍的，没有文献依据**，第一轮跑完必须报告它们离边界多远。

三条借来的原则（`15:§1.3`）：① 门控是乘法的；② **RULER 式加权求和会把 rubric 分从 0.395 推到 0.262**；③ **「录屏的 VLM 打分只报事件，不定生死」**。

#### 1.4.5 纯文本 query 的一个硬事实：从零起的任务极难过闸

`draft_verifier.md:§10`：从零生成 **0/13 和 0/13**，**26 个里 23 个死在 L1**。
对策是「相对关系判据 vs 绝对符合判据」的分裂：`relational.py` 把从零任务从 0/80 救到 **13/80**，但代价是修复任务从 47/47 掉到 **35/47**。
→ 正文可用的论点：**判据必须按任务类型分叉，不能一套判据吃两种任务。**

任务准入（`03_verifiable_construction.md:84-87`，三条）：参考解必须过、被破坏版必须挂、检索片段必须唯一。
可解性带（`10:400-401`）：让弱模型重写 8 次，**平均解出率为 0（太难/欠定）或 1（太易）的题全丢，只留中间带**。
单模型 pass@8 实测（`90:§15`）：**3/16 = 19% 可用**（Wilson 6.6%~43.0%），**0.3~0.7 难度带里 0/16**；成本模型 0.60→0.19，漏斗 37.2%→11.8%，候选量 269k→**848k（×3.2）**。
对照（`03`）：R2E-Gym 里**大多数问题不到 20% 的测试能区分正确与错误补丁**。

---

## 2. 纯图像参考（image→web / image→3D）：视觉相似度各自的失效点，以及什么能替代

**结论先行**：这一节素材也很厚，而且**全是负面证据** —— 本地三条线（3D / Web / 图表）各自独立地测出「像素比对不存在可用的工作点」。正文可以把这节写成「视觉相似度的验尸报告」。

### 2.1 各感知指标的失效点（逐个点名）

#### 2.1.1 跟人类判断的一致率天花板（`04_verifier.md:34-42`）

2AFC 人类一致率：

| 指标 | 2AFC 一致率 |
|---|---|
| PSNR | **57.1%** |
| SSIM | **57.3%** |
| LPIPS | 70.7% |
| **DreamSim** | **96.2%** |
| CLIP | 83.1% |

→ PSNR / SSIM 基本等于抛硬币（57% 对 50%）。DreamSim 的 96.2% 是全场唯一能看的，但它是**感知相似度**，不是**语义正确性**（见下面 H2 类实例）。

Design2Code 的细粒度指标组合预测人类胜负 **79.9%**，但 **Text 这一项的系数是负的**（`04:34-42`，`14:367-371`）—— 也就是说「文本相似度越高，人类越不喜欢」。

#### 2.1.2 像素比对：三条线各自的失效点

**Web 侧**（`14:§4.6`，最硬的一组）：
- **像素噪声地板 = 0.000**（完全确定）。
- **但 11 个该挂的变异里有 7 个是像素完全相同（相似度 1.0）**。
- 最佳阈值也只能做到 **14/22**，11 个里只检出 4 个。
- **P3 重新配色（该过）的像素差 0.9002，比大多数真实缺陷都大。**
→ 一句话：**像素的噪声地板是 0，判别力也接近 0。零噪声不等于有用。**

**图表侧**（`17:§4.3`，16 个变异的像素差）：
- `data_one_point`（改一个数据点）像素差只有 **0.75%**
- `legend_swap` 像素差 **0.01%**
- `recolor`（该过）像素差 **30.51%**
→ 逐字结论：「**像素比对在这件事上根本不存在可用的工作点。**」
- 像素层 S2 在 16 个变异上 9/16 且 **4 个误杀**，对照 S1 13/16 零误杀。

**3D 侧**（`10:516,509`，最精彩的一例）：
- `camera_moved`（**该过**）单图相似度 **0.9534**
- `wood_blue`（**真错误**）单图相似度 **0.9844**
→ 该过的那个画面变化**更大**。逐字结论：「**画面变化量和语义错误量完全不相关。**」单图 view0 总对 12/22。

**Blender 官方自己的阈值**（`10:413-422`，可以当外部锚点引用）：
```python
# render_report.py 第 319~320 行
self.fail_threshold = 0.016
self.fail_percent   = 1
```
即「单像素误差超过 0.016 的像素不得超过 1%」。注意官方靠的是**设备黑名单 + `set_pixelated(True)`**，不是靠调这个阈值。

#### 2.1.3 多视角剪影 IoU：对小部件天生不敏感

- 留出集上检出 **0/3**，比 dev 集更差（`10:563-570`）。
- `mug_moved`（杯子挪 **30 厘米**）剪影 IoU 仍然 **0.9934**，因为杯子在剪影里只有几十个像素。
→ 逐字：「**剪影 IoU 对小部件天生不敏感，不能当主判据。**」
- 另一面：three.js 线上多视角剪影是 19/29，确实比像素 12/29 好（`90:100-106`）—— 所以它是**有用的中间层，不是主判据**。

#### 2.1.4 全局几何指标：被面积占比稀释

`draft_verifier.md:65-73`（Blender 22 变异，检出 / 保真分开列）：

| 信号 | 总对/22 | 检出 | 保真 |
|---|---|---|---|
| 单张截图 | 12 | 2 | 10 |
| 多视角剪影 | 14 | 3 | 11 |
| 全局 Chamfer | 13 | 2 | 11 |
| **全局 F-score** | 11 | **0** | 11 |
| 逐部件 F-score | 18 | 7 | 11 |
| **全量状态断言** | 11 | **11** | **0** |
| **逐部件几何 + 四族断言** | **21** | **11** | **10** |

**460 倍**那个数（`10:721-723` / `draft_verifier.md`）：杯子挪 30 cm，杯子只占场景表面积约 **2%**，新位置还贴着桌面所以最近邻距离被桌子「接住」→ 全局 Chamfer **0.00018**，逐部件 **0.08375**。
→ 两条可迁移的律（`draft_verifier.md`）：**几何必须逐部件算；断言只许查被钉死的字段。**

#### 2.1.5 嵌入 / CLIP 类相似度：当 reward 会主动破坏

- **CLIP 相似度当 reward**：Design2Code 从 SFT 的 **72.3 打到 62.0**；Flame **85.0 → 72.2**；换成 VLM judge 升到 **74.6 / 89.0**（`19:128`，`04:52-56`）。
- **ChartMaster：像素 SSIM 当 reward 掉到 SFT 基线以下**（`17:§3.4`）。
- **SigLIP2 在 3JSBench 上完全没有区分度**[核实]：通过率是 **80.0% / 49.0% / 27.0%**，而 SigLIP2 相似度分别只加 **0.011 / 0.009 / 0.007** —— **53 个点的通过率差距对应 0.004 的相似度差距**（`92:26-27`，`91_3jsbench_verified.md`）。站方明确标注它不参与判定。
- 多样性指标的同类教训（`19:608-610`）：taxonomy 引导的 LLM judge 0.90~0.94 > 嵌入 0.78 > 词汇 0.63 > gzip 0.28。
- DeepMind 的量化上界（`19:516,604-607`）：Vendi Score 选对表征空间时约 **65%** 对齐人类（模型差异大时 80%），但**所有自动指标在区分「同等多样」的两组时 AUC 都 < 0.6** → **自动指标只能读大差异，读不出 10% 量级的差异。**

#### 2.1.6 学习出来的视觉 reward model：能用，但必须是专门训的小模型

`04:52-56` + `19:122,129,135`：

| 模型 | 数字 | 对照 |
|---|---|---|
| UI2Code^N comparator | 与人类一致 **94%** | 零样本 62%；**GPT-5 85%** |
| **UIClip**（CLIP B/32，约 151M 参数） | 成对选择 **75.12%**；网页缺陷检测 **87.1%** | 纯 CLIP 预训练 65.42%；**GPT-4V 仅 51.58%**；LLaVA 54.59% |
| Visual-ERM（8B 生成式 RM） | `r = clip(1−S̃) + 渲染成功奖励`；VC-RewardBench **F1_hard 比基座 +36.8** | **GPT-5.2 只有 32.7** |
| RULER rubric | 与人类 Spearman **0.7929** | Aesthetic 预测器 **0.6051**；CLIP **0.5518** |
| arXiv 2607.20690 | 19 条界面质量原则，合成注入约 10,000 页训 4B VLM，micro-F1 **36% → 84%**，19 条里 13 条 F1 > 80%，作者自己定位为 **reward signal** | ⚠️ 84% 是在**合成注入**违规上测的，分布外未验证；真实噪声地板可能接近 Duan 的 **κ ≈ 0.1**（`19:196`，[推断]） |

→ 两条可写进正文的结论：**① 专门训的小模型显著强于通用前沿模型（75.12% 对 51.58%）；② reward model 不需要等大模型。**
反面：UIClip 本身只做了 best-of-5 重排，**查遍 2025~2026 没有任何工作把 UIClip 当 GRPO/PPO 的 reward**（`19:122,299`）—— 这是个空位。

#### 2.1.7 纯图像参考下 VLM judge 的实测可靠性

- **有参考图是 VLM 最好的工况**：判对率 **94% / 97%**，检出 **92%~95%**（`90:702-706`）。这和 §1.2 的无参考图 68%/76% 构成直接对照。
- 但 Blender 侧单图/多图都只有 13~16/22，检出 3~6/11（`10:757-766`）。
- **BlenderGym 两两比最好只有 0.66，人与人 0.79**（`10:779,842`；`04_verifier.md`）[引用] → 校准目标线：**3D 侧至少要达到人与人的水平（0.79）**。
- 位置偏置必须做 AB/BA 交换（WiserUI-Bench，`19:125,1083`）：**o1 胜者在前 16.56% / 在后 97.78%；GPT-4o 31.89% / 88.33%。**

### 2.2 什么能替代视觉相似度

| 替代物 | 判别力数字 | 出处 |
|---|---|---|
| **逐部件几何（按材质基色分组，取最差组）** | 18/22，检出 7/11；对照全局 F-score 检出 0/11 | `10:582,580` |
| **逐颜色体素占据** | 25/29（three.js）；15/22（Blender） | `90:100-106`；`10:581` |
| **开放边界边数（拓扑量）** | 0 对 64，不随洞的大小衰减，抓住被全局 IoU 淹没的小破洞 | `90:§3.4`；`15:179` |
| **九族状态断言（白名单）** | A4 检出 1/8 且保真 7/7，抓住剪影 IoU 0.9831 和逐部件 F 0.9992 都漏掉的 bevel；A6 抓住所有图像几何信号全 1.0000 的 bulb_dim；A7 抓住 anim_missing | `10:142-144,180-183,199-202` |
| **DOM / computed style 回读** | 231 字段只有 4 个会变；五层组合 22/22 | `14:§4.2,§4.5` |
| **图表逐值回读（从画出来的几何反推，不读配置对象）** | S1 13/16 零误杀；S1 OR S3 = 16/16；回读 1~4 ms | `17:§4.1,§4.3` |
| **渲染计数器 + 效果开关像素对照**（OpenAI Astra 的一手做法） | 「Astra used Three.js's renderer counters to inspect draw calls, triangles, geometries, and textures. A Playwright test collected 90 frame intervals… tests could also compare rendered pixels with a particular effect enabled and disabled」⚠️ **原文没给百分位数值，也没给通过阈值，也没给像素差容差** | `16:1179,1183-1189` |
| **把参考图用来生成 rubric，而不是当比较对象** | Reference-Likert 31.7% < 无参考 rubric 32.0% < **带参考 rubric 35.9%** | `03_verifiable_construction.md`（RaR） |

**逐值回读的具体做法**（`17_chart_verifier.md`，可直接抄）：坐标轴刻度的像素位置 → 线性拟合 `value = a·px + b`；hook canvas 的 `fillText`/`strokeText`；SVG 走 DOM + `getBoundingClientRect`；matplotlib 走 artist 内省。

**不用模型配合就能拿到场景**（`03:209-216`，`90`）：
- three.js：`__THREE_DEVTOOLS__` 的 `observe`/`register` 事件，由**引擎**在 `WebGLRenderer` 和 `Scene` 构造函数里各派发一处（r160 `three.module.js` 第 30938 / 31088 行）—— 比「要求页面暴露 `window.__3D_STATE__`」这种约定稳得多。
- 更粗暴的一手片段（`03:209-216`）：patch `THREE.WebGLRenderer.prototype.render` 记录 `{scene, camera, frames}`。
- 逐引擎可用性实测（`15:§3.3`，实地读 CDN 发行包源码）：three.js 能 / PixiJS v8 能（`__PIXI_APP_INIT__` 是引擎设的，`__PIXI_DEVTOOLS__` 是作者设的，不能依赖）/ Babylon.js 能（`EngineStore.Instances` 无条件 push）/ **Phaser 3 不能**（八个 dist 文件里 grep `PHASER_GAME` 全 0 命中）/ p5.js 部分能 / matter.js 不能 / Unity WebGL 不能（`SendMessage` 只写无返回）/ Godot 4 web 不能。
→ 逐字结论：「**可靠的钩子全都是「在 document-start 注入一个引擎会条件读取的全局」**，所以 verifier 的真正硬需求是**控制 document-start 脚本注入**（Playwright `addInitScript` / CDP `Page.addScriptToEvaluateOnNewDocument`）。」

### 2.3 纯图像参考下的 hack 实例

| # | hack | 数字 | 出处 |
|---|---|---|---|
| H15 | **八步 agent 自主探查给 45.6% 的严重缺陷产物判过**[核实] | 通过率 49.7、τ_b **+0.111**、假阳 **45.6%**、相对成本约 **400 倍** | `92:50-57` |
| H16 | **只读 DOM 的假阳 33.7%，τ_b 是负的**[核实] | 通过率 32.6、τ_b **−0.021**、假阳 33.7%、成本 1 倍 | `92:50-55` |
| H17 | **截图加 VLM 的 τ_b 也是负的（−0.068），成本约 50 倍**[核实] | 通过率 2.7（**这是判定方式自己的通过率，不是模型能力**）、τ_b −0.068、假阳 3.2% | `92:50-59` |
| H18 | **隐藏运行时状态契约：τ_b = 1.000、假阳 0.0%、成本约 2 倍**[核实] | 但九个前沿模型里最好的覆盖率只有 **27.8%**（严格档 19.9%） | `92:50-59` |
| H19 | **离屏渲染器作弊页** | 修法：只统计在文档内有尺寸未隐藏的 canvas；离屏渲染次数当蜜罐。另加两个信号：互穿 0.053→0.762、绘制顺序 **5534 个像素**变化；回归 13/13、16/16、18/18 | `draft_verifier.md:§5,§7` |
| H20 | **pair_overlap 这个信号失败了** | 参考解自己的最大值在 48³ 下就是 1.0 → 完全没有余量 | `draft_verifier.md:§7` |
| H21 | **K4 是 axe 的结构性盲区** | `violations: []`、`incomplete: []`、`passes: 45` —— 一个作弊页让 axe 满分通过；对应 issue #2680 仍开启 | `14:§4.9` |
| H22 | **Anthropic 一手承认的同类攻击面** | 「In order to pass the task, **Claude hid changes from the grader, which only graded the final output.**」→ 作弊页测试必须加「渲染时换场景 / 只在探测帧正确 / 测完恢复」 | `16:888,894` |
| H23 | **答案泄漏的四条路径**（一手） | 容器里有修好的新版包；修复存在于之前被 revert 的提交；残留的构建产物里有答案；更新后的包能从内网镜像下载 → 防法「Keep the answers structurally out of the model's reach」 | `16:898-904` |

### 2.4 纯图像参考的分层与公式（逐字抄）

**WebRenderBench RL reward**（`14:354`，逐字）：
```
R = 0.6·RDA + 0.2·GDA + 0.2·SDA
```
- 全从**最终渲染页**算，不看代码不用 LLM（`19:210`）。
- RDA：3×3 象限 + 位置差，按唯一性加权；配对用 inner-text **LCS > 0.80**。
- SDA：匹配元素对的 computed style 差（前景色/背景色/字号/border-radius）。
- 另有象限硬闸 + `posSim` / `score` 公式（`14:346-348`）。
- 开源 ALISA-Qwen2.5-VL-7B（RL）超过闭源。

**Design2Code 五指标**（`14:367-371`）：`0.2 × Σ`，**Text 系数为负**。

**FullFront Code Score**（`14:387`，权重只在 repo 源码里）：
```
Code Score = 0.25·结构 + 0.20·文本内容 + 0.10·文本样式 + 0.20·图片 + 0.25·表单
```

**Chart Specification**（`17:§3.6`）：`R = R_f + R_e + R_sem + R_code`，其中有一个**二值拓扑闸值 3.5 分**（90.2/78.4 → 86.7/73.6）。
**ChartMaster**：`R = R_attr + R_vis`，数值容差 ≤1%。

**Visual-ERM**（`04:52-56`）：`r = clip(1−S̃) + 渲染成功奖励`。

**UI2Code^N comparator + round-robin**（`19:128,301`，同基座最干净的一组阶梯）：
```
SFT 82.5 → vanilla verifier 83.0 → comparator 85.5 → +round-robin 86.0
```
机制：同一次调用里给候选与上轮参考打分以共享刻度，两两比，**reward = 胜场数，平局 0.5，渲染失败 −1**；代价 **O(N²)** 次 verifier 调用。
→ 一句话：**相对排序 > 绝对打分。**

**通用 L0–L4 分层表**（`04:277-285`，聚合规则逐字）：
- 「**前一层失败就截断，后层不再计算。L1 的 core 断言失败时设上限，L3、L4 的分再高也不能补回来。**」
- ⚠️ `draft_verifier.md:220` 的诚实声明：**那张表里的成本/噪声档位是调研笔记里的设计估计，不是逐层本机实测。**

---

## 3. 文 + 图

**结论先行**：素材充足，而且这是**本地实验里唯一有「同一标注集、换输入模态」的受控对照**的模态。核心发现有两条：① 参考图加进来之后 VLM 判对率从 68%/76% 跳到 94%/97%；② **但代码才是主导模态，截图是补充。**

### 3.1 文+图是 VLM 的最佳工况 —— 有受控对照

`90_local_experiments.md:702-706`（`judge_noref.py`，同一标注集，唯一变量是有无参考图）：

| 条件 | 判对率 | 检出率 | 保真率 |
|---|---|---|---|
| **题面 + 参考图** | **94% / 97%** | **92%~95%** | —— |
| 只有题面 | 68% / 76% | 61%~63% | 4 视角下 39/40 |

### 3.2 但代码是主导模态，截图只是补充 —— 两组独立证据

1. **WebDevJudge 消融**（`19:679-681`）：**只给截图，pairwise 掉 9.79~10.7 个点；只给代码，只掉 0.31~2.60 个点。**
2. **ArtifactsBench 消融**[核实]（`92:44`，`19:680`）：判别模型**只给代码 79.06 → 加图注 81.74 → 给真图 90.95 → 只给图不给代码 74.94**。

→ [推断] 直接处方（`19:681,894,1032`）：**审美 / 设计类 judge 的输入必须包含关键源码片段，而不是只喂截图。**
→ 同一篇还核实了 ArtifactsBench 与 WebDev Arena 排名一致 **94.4%**，与人类专家两两一致最高 **90.95%**（`92:44`）。

### 3.3 文+图下可用的确定性判据与噪声地板

**Blender 路线 2（扰动→修回）**是文+图参考的典型形态（`10:319-368`）：
- 题面逐字：「这是起始场景，这是目标渲染图（**多视角**），写 bpy 脚本改成目标」（`10:341`）。
- 关键结构：**图是题面侧的参考，reward 是状态侧的** —— verifier 比的是 spec 字段 + 逐部件几何（`10:343`），不比图。
- BlenderGym 的同构做法：**245 对**，就是参数扰动造的；逐字「**扰动即监督**」（`10:322-323`）[引用]。

**Blender 路线 4（官方渲染测试 → F2P）**允许**只给图不给参数**（`10:408-462`）：
- 题面逐字：「任务 = 给 broken.blend + ref.png（**可以只给图，不给参数**），要求写脚本修复」（`10:438`）。
- **准入筛选逐字**：「扰动场景，**只有当被破坏的渲染在官方 0.016/1% 判据下 FAIL 时才接受这个扰动**」——「这一步把『改不动的扰动』自动筛掉，**比人工判断可靠**」（`10:434-441`）。
- 代码逐字（`10:446-453`）：
```python
def to_f2p(blend, ref_png, engine, seed):
    broken, spec = perturb(blend, seed)                      # 复用扰动算子表
    img = render(broken, engine)
    if oiio_diff(ref_png, img, fail=0.016, failpercent=1) == "PASS":
        return None                                          # 扰动没生效，丢掉
    return Task(start=broken, gold_img=ref_png, spec=spec,
                verifier=lambda out: oiio_diff(ref_png, render(out, engine)) == "PASS"
                                     and spec_check(out, spec))
```
- 反向保护：**P2P 守卫** = 同类别另取 3 个场景当回归集，必须不被改坏。
- 规模：官方 `tests/files/render/` = **48 个类目、839 个 .blend、2,596 张参考 PNG**[核实]（`92:14`，`10:325,426-429`）。
- 许可：`tests/files` 是 GPL —— **当评测集风险低，当训练数据要法务过**（`10:461-462`）。

**a11y 侧（唯一一个 reward 和 eval 是同一个量的实例）**（`14:249,262`，逐字）：
```
reward = 1.0 − Σ_v w(impact_v)·|nodes_v| / max(DOM 节点数, 1)
w = {minor 0.1, moderate 0.2, serious 0.3, critical 0.4}      # 无下界
```
- `14:262` 明确指出：**reward = 1 − IR_Axe 和评测指标是同一个量**，所以「Qwen2.5-Coder-7B 的 IR_Axe 0.05 超过 GPT-5.1 的 0.13」应该读成「**直接优化的 vs 零样本的**」，不是「小模型比大模型强」。
- ⚠️ **A11yn 的全部数字都没有独立核验**（`92:67`）。
- 覆盖面的更正（`92:85`）：a11y 不是「零噪声」，是「**判定本身零方差但覆盖面窄**」—— axe 规则引擎 **105 条里纯自动可判只有 41 条**。
- 另一处更正（`14:719-735`）：A11YBench 没有独立的 arXiv id（2606.21926 是 A11YRepair）；Vision2UI 不是独立 id（是 2404.06369 v1，v2 改名 WebCode2M），和 Vision2Web（2603.26648）无关。

### 3.4 文+图下的校准协议（`04_verifier.md:291-297`，逐字抄）

| 手段 | 门槛 |
|---|---|
| 人工裁决对 | **200 对** |
| 两两一致率 | **≥ 85%** |
| 3D 侧 | **至少达到人与人的水平（BlenderGym 0.79）** |
| 变异测试 | 必做 |
| 对抗注入 | **必须判 0 分** |
| AB/BA 交换 | **≥ 90%** |
| 取证 | **3 倍** |
| 多 judge 投票 | 必做 |
| judge 与 policy 分家 | 不同家族 |
| 监控 | proxy 与留出集的分歧 |

κ 的样本量（`11_hacking_defense.md:§2.4`）：**200 对只够平衡任务；通过率在 10~20% 时需要 340+ 对。**

verifier 逐条一致率门槛（`11:§2.7`，这组数字很适合当正文的「及格线」）：
- 专家 panel **95~97%**
- 强 verifier **92%**
- 弱 verifier **76~82%**
- → **要求 ≥ 92%，绝不低于 85%。**

**Anthropic 一手的 grader 选择顺序**（`16:583-585`，逐字可引）：
1. 先用程序化判定（exact match、固定集合的标签、JSON schema、跑测试通过）；
2. 只对开放式输出用 LLM-as-judge，且 rubric 必须「**written as checkable claims (not a 1-to-5 scale)**」；
3. 「**You pick the judge model, and it should not be the model you are testing.**」
4. 有基线时用**随机顺序、对基线盲的两两比较**。
5. 「read a sample of scored transcripts before believing your evaluator」（`16:587`）。

**三条基线期诊断**（`16:591-593`）：① **grader 在同一份输出上跑两遍，报告判定有没有变**；② 把管道故障（超时/API 错/截断）和模型方差分开；③ 基线 ≥ 约 95% 就别再追质量了，去追成本和延迟。

**噪声地板准入规则**（`16:597`，逐字）：「Claude checks that the eval's noise (how far the score can move by chance alone) is **smaller than the smallest improvement you'd act on**.」配套停止条件（`16:627`）：「**If the gain is within noise, it says so and recommends against merging.**」

**三条反 grader-hacking 规则**（`16:603-605`，逐字）：
- 分 train/test，test 从不给看；**train 涨 / test 平就是过拟合的信号**；
- 「**Never paste failures into the prompt**」；
- 「**Keep the answers structurally out of the model's reach**」。

**四档闸强度**（`16:511-515`，Anthropic 唯一的多档方案）：一个 prompt 里说 → `/goal` 每轮由独立评估者重查 → **确定性闸：Stop hook 阻塞回合结束直到脚本通过** → 第二意见：换新模型的 subagent 试着反驳。

**官方承认的怀疑型 reviewer 代价**（`16:535`，逐字）：「A reviewer prompted to find gaps will usually report some, even when the work is sound… Chasing every finding leads to over-engineering… Tell the reviewer to flag only gaps that affect correctness or the stated requirements.」→ **怀疑模式的假阳是系统性的、方向可预测的。**

**判定冲突时谁说话**（OpenAI `playwright-interactive`，`16:1604-1609`，逐字）：「Use screenshots as the primary evidence for fit. **Numeric checks support the screenshots; they do not overrule visible clipping.**」
→ 笔记自己的综合（`16:1611-1615`）：**哪一侧更可信取决于错误所在的维度** —— 3D 结构错误是像素盲的，2D 裁切错误是指标盲的。因此 `vf-1` 需要一条对称限制：**不只是「不许只看一张图就判」，还要「不许只看指标就判」。**

**官方对视觉判据的四项验收**（`16:1512`，这是唯一一份 three.js 级别的像素验收规范，逐字）：
> 「Before finishing, you verify with Playwright screenshots and canvas-pixel checks across desktop/mobile viewports that it is **nonblank, correctly framed, interactive/moving, and that referenced assets render as intended without overlapping**.」
→ 和本地四层判据逐项对上（`16:1516-1523`）。

**可程序化的硬约束（最接近「公式」的审美判据）**（`16:1383-1385`，逐字 + 形式化）：
> 「Define constraints such as one H1 headline, no more than six sections, two typefaces maximum, one accent color, and one primary CTA above the fold.」
→ `count(h1)==1`、`count(section)<=6`、`count(font-family)<=2`、`count(accent)==1`、`count(CTA above fold)==1`。
配套：border-radius ≤ 8px；**letter-spacing 必须是 0，不能是负的**；font-size 不许随视口宽度缩放；视口预算 `calc(100svh - header-height)`（`16:1448-1449,1533-1540`）。

**反事实删除判据族**（`16:1434-1444`，逐字，机制上和「效果开关像素对照」是同一个原语）：
> 「If the first viewport still works after removing the image, the image is too weak. If the brand disappears after hiding the nav, the hierarchy is too weak.」
> 「If removing a border, shadow, background, or radius does not hurt interaction or understanding, it should not be a card.」
> 「If deleting 30 percent of the copy improves the page, keep deleting.」

**现成的确定性 lint（判据可直接抄）**（`19:164-172,212`）：
- `axe-core` / Lighthouse：返回 passes / violations / incomplete / inapplicable 四个数组。
- ⭐ `@double-great/stylelint-a11y` → `line-height-is-vertical-rhythmed`：**「排版纵向节奏」唯一的真 lint 实现**。只检查 px 与无单位值；px 必须是 `baselineGrid`（**默认 24**）的整数倍；无单位必须 ≥ `minRelativeLineHeight`（**默认 1.5**）；忽略 % / em / rem / 关键字 / `font` 简写。
- `stylelint-plugin-mozilla` → `use-design-tokens`；`@evilmartians/design-lint`（**11 条** Oxlint 规则）；`@kong/stylelint-plugin-design-tokens`；`stylelint-declaration-strict-value`；`@takazudo/zudo-design-token-lint`。
- `@projectwallace/css-analyzer`（`wallace-cli --json`）给 total / unique / **uniqueness ratio**；⚠️ **只吃 CSS 字符串 → 对 Tailwind 类的 LLM 生成页基本失效，必须改走 computed style。**
- **三件没有现成实现的**（所以本地那套是首创，`19:176-180`）：modular scale（字号比例级数）、视觉层级单调性、间距节奏自动选基数。
- **Figma 不是规则引擎**（`19:200-204`）：Design Lint 插件错误类型总共只有 **10 种**，而且「核心判据是『该图层有没有绑定 style』，不看具体值对不对」；Similayer 只选择不 flag；Code Connect 官方文档未提及任何 validate / lint。

### 3.5 文+图下的 hack 实例（补 §2.3 之外的）

- **RaR 的教训反过来也是 hack 面**：把参考图当比较目标（Reference-Likert 31.7%）比**不给参考**（32.0%）还差 —— 参考图用错位置会降低判别力。
- **「把缺陷归因于环境然后宣布完成」**（`16:924-937`，Anthropic 一手 12 条 hack 清单里的一条）：原文「Attributing a visible defect to the environment and declaring the task done anyway」。笔记标注这条对渲染任务**高风险**：模型可以甩锅给 SwiftShader 然后交活 → **verifier 必须自己裁决基础设施故障**。
- **「我在脑子里检查过了」**（同清单）：「Submitting a solution without compiling or running it, relying on a mental check instead」。
- **Anthropic 自己的反 hack prompt（可直接抄，有实测效果）**（`16:868-870`）：「Please write a high quality, general purpose solution… Do not hard code any test cases…」
  效果：不可能任务上的 hack 率 **50%→23%（Opus 4.6）、55%→35%（Opus 4.5）、53%→20%（Sonnet 4.5）**。
- **但在 GUI / computer-use 环境里 prompt 级缓解失效**（`16:874`，逐字）：「**Concerningly, unlike previous models, Opus 4.6 engaged in this behavior even when it was actively discouraged by the system prompt.**」
  ⚠️ 同厂另一张卡（Fable 5 §6.3.7）说法相反：「**prompt-based steering remains useful**」→ 见 §8 矛盾清单第 4 条。
- **坏任务本身就会造出 hack**（`16:841`，本库里最有行动价值的一个数）：缺文件（不可能完成）的任务上，**成功 hack 比完好任务多 1.5~3 个百分点**，而**尝试 hack 的比率高 3 到 6 倍**。而且模型还被**明确指示不许要求澄清**，「further exacerbating the problem」（`16:843`）。
- **隐藏测试 hack 率的口径**（`16:854`，可直接抄）：「Hack rates are determined by the percentage of problems where the model's submitted solution for visible tests does not pass the held-out hidden tests」—— 笔记自承**本地留出集目前没有这个指标**（`16:2040`）。

### 3.6 文+图的分层：Anthropic 一手的硬闸结构

**最接近「公式」的一句**（`16:123`，逐字）：
> 「Each criterion had a hard threshold, and if any one fell below it, the sprint failed and the generator got detailed feedback on what went wrong.」
→ **任一维度不过即整体失败，不是加权求和过线。阈值数值从未公开。**

四维 rubric 同时给 generator 和 evaluator（`16:60-69`）：Design quality / Originality / Craft / Functionality。
**权重理由（按基线方差分配，不是按重要性）**（`16:73`）：「I emphasized design quality and originality over craft and functionality… Claude already scored well on craft and functionality by default… by weighting design and originality more heavily it pushed the model toward more aesthetic risk-taking.」

**三条一手的分离原则**：
- 自评失败：「agents tend to respond by confidently praising the work… particularly pronounced for subjective tasks like design, where there is no binary check equivalent to a verifiable software test」（`16:45`）。
- 分离不消除宽容，只让宽容**可调**：「tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work」（`16:47`）。
- evaluator 操作活页面而不是打静态截图：给它 Playwright MCP，「Because the evaluator was actively navigating the page rather than scoring a static screenshot, each cycle took real wall-clock time. **Full runs stretched up to four hours.**」（`16:90`）

**QA 的预算占比（这个数很适合写进正文）**（`16:151-159`）：
- 单 agent：20 分钟 / **9 美元**
- 全 harness（Opus 4.5，带 sprint）：6 小时 / **200 美元** ≈ **22 倍**
- V2（Opus 4.6，去掉 sprint）：3 小时 50 分 / **124.70 美元**（去掉一个组件省了约 38%）
- **QA 只占总成本的 8.4%（10.39 / 124.70），但三轮每一轮都找出了真问题。**
- 官方原话：「**over 20x more expensive**, but the difference in output quality was immediately apparent」

**反篡改工程（这条是全库唯一来源）**（`16:668`）：agent 只许翻 `passes` 字段；「It is unacceptable to remove or edit tests…」；**选 JSON 而不是 Markdown，因为「the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files」**。规模：claude.ai 克隆的功能清单 **> 200 条**，初始全部 `passes: false`（`16:649`）。

**rubric 本身就产生了大部分增益**（`16:171-173`）：「Even on the first iteration, outputs were noticeably better than a baseline with no prompting at all.」
**反面**（`16:167`）：「Including phrases like '**the best designs are museum quality**' pushed designs toward a particular visual convergence.」
⚠️ 而 Anthropic 官方 `canvas-design/SKILL.md` **正文里在用**这个措辞，还要求「Emphasize craftsmanship REPEATEDLY」（`16:418-421`，`19:359`）→ 见 §8 矛盾清单第 5 条。笔记的处置（`16:426`）：**这种措辞在 generator 侧是增益，在 evaluator rubric 里是污染。**

---

## 4. 文 + 图 + 视频

**结论先行**：素材**中等偏薄**，而且以外部文献为主、本地实测为零。但有一组极强的**反面证据**（V-GameGym 的归谬）和一条明确的工程处方（**录屏只报事件，不定生死**）。`15_game_verifier.md` 是唯一的主力来源，`01_frontier_labs.md` 提供厂商侧的一手引用，`16_primary_sources.md` 证明**没有任何一家官方披露过把视频当 reward**。

### 4.1 厂商侧的一手材料（全是定性的，没有一个数字）

**小米 MiMo-V2-Flash（arXiv 2601.02780）§4.3.2** —— 唯一明确用录屏视频做判别的厂商（`01_frontier_labs.md:299-300`，逐字）：
> 「execute generated code using Playwright to obtain rendered videos, and apply a multimodal visual discriminator to retain only high-quality samples」
> 「**video-based evaluation reduces visual hallucination compared to static screenshots**」
> 「Our vision-based verifier scores rollout executions from **recorded videos**, jointly evaluating visual quality, functional correctness, and executability」

→ 三条可用的点：① 视频判别是为了**降低视觉幻觉**，不是为了提高判别力；② **同一个判别器两用**，既过滤预训练/SFT 数据又当 RL 奖励；③ **WebDev 的训练细节未披露，没有任何数字。**

`01:§4.3` 的归纳（国内各家已收敛到三层结构）：预训练 = 代码与渲染图配对（K2.5、K3、Qwen3-VL、GLM-5V）→ 数据过滤 = 在真实沙箱里运行（MiMo、MiniMax、GLM）→ RL = **先过确定性门控，再叠加模型评审；构建失败或伪造实现时 reward 置 0**（K3、MiMo）。
`01:§4.3` 的 [推断]：**视频判别（MiMo）是为了解决动画、交互、three.js 动态场景在单张截图里看不到的问题。**

**管线 5「渲染在环的 agent 轨迹」**（`01:435-446`）：策略模型自己开浏览器或 Blender，截图、录屏、看渲染结果后修改；轨迹本身既是 SFT 数据也是 RL rollout；**判分时用视频而不是单张截图**。证据只有 MiMo 的录屏判别、GPT-5.4「first mainline model trained for computer use」、GPT-5.6「inspect and refine the rendered result」。

**官方一手材料里视频判别的全部痕迹**（`16_primary_sources.md:§3.1`，这节的价值在于证明「没有」）：
- 唯一一条隐含视频判别的指令，来自 OpenAI 官方 `frontend-skill` 的动效规则（`16:1458-1459`，逐字）：「Motion rules: - **noticeable in a quick recording**」。笔记的桥接（`16:1465`）：这一条和 MiMo 的录屏视频判别「**是同一个判据形式，但这里是人类手写的指令**」。
- 配套的动效配额（`16:1453-1456`）：「Ship at least **2-3** intentional motions for visually led work」—— 一个 hero 入场序列、一个滚动联动/吸附/景深效果、一个 hover/揭示/布局过渡。
- `playwright-interactive` 的三条时序要求（`16:1594-1596,1644-1646`，逐字）：「**If motion or transitions are part of the experience, inspect at least one in-transition state in addition to the settled endpoints.**」「For dynamic or interaction-dependent visuals… **do not rely on a single screenshot for signoff**.」「For realtime or animation-heavy apps, verify behavior under actual interaction timing.」**可逆控件要测完整往返（初始 → 变化 → 回到初始）**；30~90 秒的探索性走查。
- 还有一条反作弊规则值得抄（`16:1647`，逐字）：「**`page.evaluate(...)` and `electronApp.evaluate(...)` may inspect or stage state, but they do not count as signoff input.**」→ 笔记指出这意味着本地的 `__vcStep(n, dt)` 是**布景**，不是真实输入（`16:1649-1651`）。
- Astra 的 90 帧统计（`16:1179`，逐字）：「A Playwright test **collected 90 frame intervals** and reported average and percentile timings alongside those counts.」⚠️ **没给百分位数值，也没给通过阈值**（`16:1185`）；全文也**没有固定时间步**（`16:1189`）。
- 截图历史保留策略的三方分歧（可当消融点，`16:1104,1854,1871`）：OSWorld 2.0 **保留每一张**截图 + 服务端在 **100k token** 处压缩；CUA 考虑「current and past screenshots and actions」；OpenCUA 用 **3 张滑动窗口**。
- **结论逐字（`16:1777,1893`）：三家都把「在渲染页上评论 / 渲染在环」做成了产品，没有一家说用它训练。**

### 4.2 本地的「可玩性」拆解：录屏判不了可玩性

`15_game_verifier.md:34-37`（逐字，这是整节最强的一段）：
> **「像素与录屏判不了可玩性，它判的是「有东西在动」。」**
> V-GameGym 把交互代码**改写成 10 秒自动演示**再录屏打分，录屏 rubric 里还留着「Interaction Logic: user input responsiveness 0–25」这一项，**而整个过程从来没有发送过任何输入**。
> 「**这不是实现瑕疵，是「用录屏当可玩性证据」这条路本身的归谬。**」

V-GameGym 的数（`15:222`）[引用]：2,219 个游戏 / 2,190 个仓库 / 100 聚类 / 70 个模型；把交互代码改写成 10 秒自动演示，录 10 张截图 + 1 段视频，**代码/图像/视频三分**；**judge 无人类对照**；GPT-5 **代码 96.6、图像 17.6、视频 20.7、总分 45.0**。
另一个数（`15:83`）：V-GameGym **录屏成功率 92.7%**（在 A3「画面有内容」那一行当证据用）。

VideoGameBench（`15:224`）[引用]：23 个游戏，测试集 10 个（7 公开 + 3 保密），7 个模型，**每模型每游戏只跑 1 次**；判据是**从 YouTube 长流程视频抓 checkpoint 帧，感知哈希 + 汉明距离 < 12**（Kirby 调到 6~8）逐帧匹配；**无 judge**；最好成绩 **0.48%**，3 个保密游戏**全部 0%**。
重复性实测（`15:§1.1` D3 行）：Gemini 2.5 Pro 跑 5 次，Kirby **4/5** 到达检查点（样本方差 0.2），**另两个游戏 0/5**（附 D.3 表 9）。

ArtifactsBench 的三时刻截图做法（`12_self_verification.md:207`）—— 介于截图与视频之间的折中。

### 4.3 替代路线：输入重放 + 确定时钟 + 状态差分（R3）

**抗欺骗强度排序**（`15:44`，逐字）：
> **输入重放加状态差分 > 绘制调用拦截 > 引擎自带钩子 > 像素与音频 > 要求模型暴露接口**
> 即 **R3 > R2 > R1 > R4 > R0**。

四条替代路线表（`15:§3.2`）：

| 路线 | 怎么拿到状态 | 骗得过吗 | 覆盖面 | 成本 |
|---|---|---|---|---|
| R0 要求模型暴露接口（`exportState`/`setState`） | 脚手架规定 | **骗得过，而且训练时一定会被骗** | 100%（强制） | 低 |
| R1 引擎自带钩子 | 引擎自己派发的全局 | **难骗**（事件由引擎发），但钩子只给渲染/场景图，不给分数与生命 | 取决于引擎 | 低 |
| R2 渲染循环与绘制调用拦截 | 劫持 rAF、`getContext`、2D ctx 方法、`drawArrays/drawElements` | **几乎骗不过**：这就是玩家看到的东西，要骗必须真的画出来 | 全部 canvas 游戏 | 中 |
| **R3 输入重放 + 确定时钟 + 状态差分** | **不读游戏内部任何东西**；固定种子固定时钟跑多条输入轨迹，比较帧哈希序列 | **最难骗**：要骗必须真的实现一个会按规则响应输入的系统 | 全部 | 中 |
| R4 像素与音频弱监督 | 帧差；音效事件探测 | **容易骗**：背景动画会让每一帧都不同 | 全部 | 低 |

R3 的论证逐字（`15:§3.2`）：「它把『可玩性』转成了一个**不需要语义的差分问题**。一条空输入轨迹、一条有输入轨迹、几条不同强度的策略轨迹，剩下的全是序列比较。」
与 R4 的分工逐字：「R4 只能当**否决器**（画面全白就判挂），**不能当排序器**」—— 和 `feature-value-is-veto-not-ranking` 那条一致。

**R2 的一个被低估的技巧**（`15:§3.4`）：对 **Canvas2D** 游戏，拦截 `fillText` 就能**直接从参数里读出 HUD 字符串**（分数、生命、关卡），**完全不需要 OCR**。网页小游戏绝大多数 HUD 就是 `fillText`。这条让「分数会涨」从半确定性降级成**全确定性**。
⚠️ 原文自承：「本条是机制推论，**没有找到公开文献把渲染 trace 当游戏测试 oracle 的**。」

**R2 的四个盲区**（`15:§3.4`，这组很重要）：
- **精灵批处理会把逐物体信号抹平** —— Pixi 与 Phaser 都会把共用图集的上千个精灵合并成一次 `drawArrays`，所以「绘制调用数约等于物体数」这个直觉**恰好在网页小游戏最常用的 2D 引擎上是错的**。
- 没有语义身份；没有不被渲染的状态（分数、生命、RNG 种子、AI 状态）；shader 侧逻辑不透明；**WebGPU 不在范围内**（Spector 只管 WebGL1/2）。
- 工具：Spector.js（`new SPECTOR.Spector()`，`captureNextFrame` / `startCapture` / `stopCapture(): ICapture`），原文注明**单次 capture 到达指定命令数或 10 秒后自动停止** —— 它是采样器，不是连续状态流。WebGL-Inspector 已被其自己的 README 标为不兼容 WebGL2、已被取代。

### 4.4 视频/时序的确定性噪声地板（这是本节唯一可量化的硬骨架）

**要固定的五件东西**（`15:§4.1`）：① 随机源（`Math.random` → 确定 PRNG；`crypto.getRandomValues` 也要换）② 时间源（`Date.now`、`new Date()`、`performance.now` 全部返回 harness 推进的虚拟时钟）③ 帧驱动（接管 rAF，帧只在 `__vcStep(n, dt)` 时推进；**`setTimeout`/`setInterval` 也要挂到同一虚拟时钟上** —— 本地现状是**未接管，游戏任务必须补**）④ 输入（按**帧号**而不是墙钟毫秒，每条轨迹是 `(frame, action)` 列表）⑤ 资源加载（断网，固定加载顺序）。

**两条路线，建议都用**（`15:§4.1`）：
- **页内 shim**：便宜可移植，但**游戏可以检测**（查 `Date.now.toString()` 就能看出被改过），漏一个 API 就漏一个熵源。
- **CDP 虚拟时间**（`Emulation.setVirtualTimePolicy`，EXPERIMENTAL）：policy 取 `advance`/`pause`/`pauseIfNetworkFetchesPending`；`budget`「这么多虚拟毫秒过去之后虚拟时间暂停并发出 `virtualTimeBudgetExpired` 事件」；`maxVirtualTimeTaskStarvationCount`「在虚拟时间被强制前推以**防止死锁**之前能运行的最大任务数」；`initialVirtualTime`。配 `HeadlessExperimental.beginFrame` 显式步帧。**它在 JS 之下，游戏检测不到** —— 这是它的硬优势。代价：实验性接口，跨 Chrome 版本会变。
- 逐字建议：「**两条都用。**CDP 虚拟时间负责「游戏检测不到」，页内 shim 负责「漏网的 API」。两条同时在，可以互相当对照：如果只开一条和同时开两条的轨迹不一致，说明有个熵源被漏了。」

**本机实测的确定性结果**（`draft_verifier.md:§6`，这组是全库关于「时序 reward 的噪声地板到底能不能做到 0」的唯一实测）：
- **只上虚拟时钟 → 跑出 3 个不同结果。**
- **加上暂停 + 步进后，20 次里仍有 2 次不一致。**
- **只有 harness 驱动帧推进 + 直接读 canvas，才做到逐字节一致。**

对照：`14:§4.8` Web 侧两次完整重跑**判定翻面 0 次**；`19:1041` 审美侧两次独立运行 **0/20 不一致**；`90:§12` flaky 基线 9 个产物 × 3 次探测 → **翻面 0/9，数值逐位相同 0/9**；`15:B3` 行引用本地 three.js harness「同页面重复探测逐字节一致」。

**存活与卡死探测的三个陷阱**（`15:§3.5`，直接关系到「视频里看起来没动」会不会假阳）：
1. **rAF 计数为 0 不等于游戏死了，可能只是被节流**。Chrome 官方：「页面在后台时 Chrome 不调用 `requestAnimationFrame()`，这个行为从 2011 年就有了」→ **把帧计数当证据之前必须先把可见性钉住**。
2. **主线程卡死时你的探针也卡死** → 「**截图成功但 evaluate 超时 ⇒ 主线程卡死**」（原文标为推论）。区分「卡死」与「只是慢」要四条一起看：rAF 计数不增、LoAF/longtask 出现秒级条目、短超时的 evaluate 失败、N 秒内截图哈希不变。**单看任一条都有歧义。**
3. **JS 里拦不住同 realm 的死循环** → `loop-protect`（Babel AST 改写，默认阈值 **100ms**；原文自认不解决停机问题，只覆盖 `while`/`for`/`do`，**不防递归**；CodePen 同思路，freeCodeCamp 用约 500ms），或跨 realm 杀（Worker / 跨进程 iframe + `terminate()`，代价是失去逐帧粒度）。Long Tasks 阈值规范写死 **50ms**，**时长只以 1ms 粒度提供**。

**输入保真度的五个坑**（`15:§3.6`，这组决定「没响应」会不会假阳）：
- **合成事件不是可信事件**：`dispatchEvent()` 派发时 `isTrusted` 为 false，`HTMLElement.click()` 也是 false → 游戏自己的监听器照样会收到（绝大多数游戏不查 `isTrusted`），但**不触发默认动作**。一律走 CDP `Input.dispatchKeyEvent` / `dispatchMouseEvent` / `dispatchTouchEvent`。
- **`rawKeyDown` 与 `keyCode=0`**：Puppeteer 在按键不产生文本时发 `rawKeyDown` —— **恰好在方向键、空格跳跃、WASD、Escape 上**。`code`、`key`、`windowsVirtualKeyCode` **三个都要填**。
- **按键重复**：朴素的 down/up 对会产生「一按一格」，看起来像游戏坏了，要显式长按。
- **只绑 touch 的游戏**：纯鼠标 harness 会静默什么都不发生 → 配 `Emulation.setTouchEmulationEnabled`。
- **Gamepad 无法合成**：实地枚举 `browser_protocol.json` 的 53 个域与全部命令，**没有 Gamepad 域**；`Input` 只有 13 个命令，`Emulation` 的 48 个命令**没有 gamepad**；整个协议里 "gamepad" 只出现一次。只能 shim，产生的是 `isTrusted: false` 的事件。
- 另两条：headless 页面常常失焦，失焦页面丢键盘输入 → `Emulation.setFocusEmulationEnabled`；pointer lock 下 CDP 鼠标移动能否给出正确 `movementX/Y` **未核实**，标为高风险类别。

**跨引擎浮点分叉**（`15:§4.2` 第二档）：有一个实例在 codeberg issue（perplexdotgg/bounce #8，issue 仍开启），**报告者自测，不是论文**。

### 4.5 视频/时序侧 VLM 的实测可靠性

本地**没有视频 judge 实测**。能用的只有游戏侧 LLM judge 的三条公开噪声地板（`15:§1.4`，§1.2 已引，这里重列因为视频那节一定要用）：
- 同一 judge 重判同一规则，重判分差 ≥0.25 的比例 **12.7%（Small）/ 8.8%（Big）**；谓词结构不同时 **17.7% / 11.1%**。
- 换 judge 配置、固定轨迹：一致率 **0.910 / 0.888**。
- 人与人同 rubric：**91.4% / κ=0.68 / α=0.624**。
- → **「LLM 参与的游戏判定上，3 个百分点以内的效应不要信。纯程序判据的噪声地板是 0 —— 不是更准，是没有方差。」**

**自动 judge 的一致率天花板已经逼近人类**（`15:§0` 第 8 条，这组数字说明「继续优化 judge 收益很小」）：
- PlaytestArena：GUI judge 与人的条目级一致率 **87.9%（κ=0.66）**，人与人 **91.4%（κ=0.68）**；游戏级 ρ=**0.89** 对人与人 **0.92**。
- PlaySuite：里程碑 judge 与人「±1 级内一致」**90.4%**，人与人 **93.0%**；人与人的 Krippendorff α 只有 **0.624**。
- → 逐字：「**差距只有 2.6 个百分点，而人自己的一致性就不高。继续优化 judge 的收益很小**，该把力气花在覆盖率和确定性判据上。」

**A2Z 的三组数**[核实]（`92:35-36`）：
- 源码判满分的规则，真玩只有 **76.8%** 成立；源码判零分的里 **25.7%** 真玩是对的。
- 第一遍正常玩覆盖 **40.5%**，再玩一遍 **41.0%**，换成对抗式状态注入 **48.5%**。
- → 逐字结论（`92:36`）：「**游戏侧瓶颈是覆盖率不是准确率。**」
- 补充（`15:§2.2`）：部分分 **54.3%**；去掉某个轴之后排名翻转 **20.5% / 8.9% / 11.2%**。
- 依赖链（`15:§1.1` C7 行）：局部通过 **72.4%** → 依赖调整后 **22.7%**，差 **49.7 点**；加依赖上下文把运行时违例的覆盖率从 71.1% 提到 **80.2%**。
- 细粒度覆盖（`15:§1.1` D2 行）：十个游戏从 **10.0% → 73.4%**；对照一个 milestone 式在线游戏 agent（Orak，GPT-5.6-Luna、3 个种子、≤200 步）里程碑达成率只有 **6.7%~26.7%**。

**世界模型当不了可玩性 verifier**（`15:§2.5`）：Muse/WHAM（10 亿图像与动作对、约七年游玩、300×180、WHAM-1.6B、FVD 与 Wasserstein，**持久性只有定性演示**）；Genie 3（720p / 24fps / 一致性「几分钟」，**无定量基准**）。

**agent 真玩的能力边界**（`15:§2.4`）：**题材差异超过模型差异**；**给 agent 历史会让它变差**；动作频率不是瓶颈。
PlaytestArena D1：GUI agent 在 20 个游戏约 120 关上 pass@20 **0.82**（GPT-5.4），人 **0.92**。
PlayCoder 的时序盲区（`15:§1.1` B5 行）：失败集中在高频反馈（>60 FPS 才出现的 bug），**4/43 项目（约 9%）结构性测不到**。

### 4.6 动画的另一条路：不渲视频，直接断言时间轴

这是全库对「视频 reward 性价比」最有力的反论（`10_blender_tasks.md:185-202`）：
- A7 族逐关键帧断言 `(k.co[0], k.co[1], k.interpolation)`，外加直接 `c.evaluate(20)` 逐帧求值；驱动器查 `driver.expression`。
- **`anim_missing`（删掉两整条 F-curve）在 view0 / 多视角 / Chamfer / 体素 IoU 上全部 1.0000，只有 A7 抓到。**
- 逐字：「**渲染单帧的 verifier 对动画完全失明。**」「要用渲染抓动画，得渲**一整段序列**，成本至少翻 **N 倍**。」（`10:199-201`）
- A7 的保真率是满分：dev 7/7、holdout 4/4。
- **全库没有任何地方实现或测量过「渲染序列 verifier / 时序一致性指标 / 光流信号」**（`10` 的 grep 结论）。

→ 正文可用的论点：**在「代码生成 3D/动画」这个设定里，时间轴是声明式的，所以时序正确性应该走断言而不是走视频判别。视频判别的价值在「交互响应」这类无法声明的性质上。**

### 4.7 视频侧的成本对照

- **A2Z 三轴评测总共约 900 墙钟小时**（10 台 m7i.4xlarge + 1 台工作站），其中 **playtest 占 56.8%、重放占 40.1%、源码检查只占 3.1%**（`15:§5.5` 引附录 C）。
  → 逐字：「**纯程序判据的成本优势是两到三个数量级**，这是它最被低估的一点。」
- 本地**推算**（`15:§5.5`，**不是实测**，依据是 3D 线「单次探测 0.8~1.0 秒」按工作量折算）：单条 600 帧轨迹约 1.0~2.0 秒；每帧存指纹 +0.3 秒；像素哈希（每 10 帧一次共 60 次 `toDataURL`）+1.5 秒；浏览器启动 0.6 秒，**四条轨迹复用同一实例**；**单个变异的四条轨迹 + 双跑自检 ≈ 20~30 秒**；**30 个变异 + 1 个参考解 ≈ 11~16 分钟**；加跨机器自检 ×2 → **一轮完整实验约 25~35 分钟**，「可以一晚跑十几轮，阈值扫描完全负担得起」。
- 3D 侧的渲染成本对照（`draft_verifier.md:§6`）：单张截图 **62~85 ms**；8 视角转台 **0.2~0.5 秒**；Blender Workbench 32 进程 **15.5 视角/秒**；Blender 几何约 **0.4 秒/候选**；three.js 探针 **0.8~1.0 秒**，池化后约 **14 任务/秒**；场景图 13 个 mesh **1.8 ms**。

### 4.8 视频侧的设计（尚未实测，照抄时必须标「设计稿」）

`15:§5` 是一份**完整的最小实验设计**，但明确标注为设计 + 推算。四条轨迹（`15:§5.2`）：

| 轨迹 | 输入 | 用来验 |
|---|---|---|
| T0 空轨迹 | 600 帧无输入 | 基线；A 族；E1/E2；F2（不动不能赢） |
| T1 固定脚本 | 600 帧预写死的 `(frame, action)` 列表 | B 族（与 T0 比是否分叉）；C1/C3；B4 |
| T2 贪心脚本 | 每帧按 HUD 与绘制调用里解析出的球位置追球（**不读内部变量**） | D1（能不能通关）；F1 的上端 |
| T3 随机猴子 | 600 帧随机按键，固定种子，跑 10 个种子 | F3；F4（分数方差）；顺带做覆盖率 |

核心约束逐字（`15:§5.1`）：「**不读游戏任何内部变量。**这是实验的核心约束，否则证明不了 R3 这条路可行。」
每帧末尾导出的**状态指纹** = 绘制调用序列的哈希 + 从 `fillText` 解析出的 HUD 数字 + 画布像素哈希。

F1 的计算：`(T2 的归一化分) − (T3 十个种子的均值)`，以及 `(T2) − (T0)`。RAPP 实测分差是 **0.665（人设计）对 0.245（随机生成）**，阈值先取 **0.40** 死值。

**F 族（难度与平衡）是公开文献里最被忽视、落地成本最低的一族**（`15:§1.2`，强推进正文）：
- RAPP 2015 给了一个现成的、完全确定性的难度度量，而 2026 年的游戏生成 benchmark（A2Z、PlaytestArena、PlaySuite、V-GameGym、Code2Games）**没有一个用它**。
- 它只要三样东西：**一个分数读数、三档强弱策略、多次重放。**
- RAPP 的数（`15:§1.1` F 族各行）：人设计 **0.7966（Explorer）对 0.2493（Random）**；随机生成的游戏只有 **0.6193 对 0.3195**。
- F2：人设计游戏里 DoNothing 归一化分 **0.1317**、胜率 **0.0556**；随机生成游戏里 DoNothing 反而拿到 **0.3747**、胜率 **0.1846**。
- F4：随机生成游戏的分数标准差**最小 199,406**，人设计游戏的**最大只有 121.55** —— **差 1500 倍以上。**
- F3 的旁证：Android 实测**随机 Monkey 的平均覆盖率在 6 个工具里最好**（1503.07217）→「随机能走很远」是常态不是例外。

期望看到的曲线（`15:§5.6`）：「单条判据 10~15/30，分层组合接近 30/30」，**和 3D 线的 12/29 → 29/29 同形**。

### 4.9 视频侧的 hack 实例

| # | hack | 出处 |
|---|---|---|
| H24 | **V-GameGym：10 秒自动演示 + 从不发输入，却保留「user input responsiveness 0–25」rubric 项** —— 用录屏当可玩性证据这条路本身的归谬 | `15:34-37,222` |
| H25 | **R0（要求模型暴露 `exportState`）骗得过，而且训练时一定会被骗** | `15:§3.2` |
| H26 | **R4（像素与音频弱监督）容易骗：背景动画会让每一帧都不同** | `15:428` |
| H27 | **CreativeGame 的 Tier 2 会「发送基本输入」，但输入之后什么都不读回** → 它实际上从没回答「有没有响应」这个问题 | `15:§1.2` B 族 |
| H28 | **CreativeGame 自评：LLM 创意分一律给 7/10**，作者点名 Goodhart 风险 | `15:§1.1` F8 行 |
| H29 | **A 族只能当门不能当分**：Code2Games 基线构建成功率 91.8~95.9 几乎持平，而核心玩法分从 43.5 到 58.1；A2Z 可验证率 93.9%/94.2%，Claude-Fable-5.1 可验证率 98.7% 而 GDD 忠实度只有 77.0 | `15:§1.2` A 族 |
| H30 | **变异 13 是故意种的结构性盲区**：「分数变量更新了但没重绘 HUD」—— 因为读不到内部变量，**只能检出「HUD 不涨」而无法区分是哪一侧坏了**，预期被 C1 抓到但诊断信息是错的 | `15:§5.3` |
| H31 | **变异 20：球碰到挡板就直接加 100 分** —— 规则「自洽」，分数会涨，碰撞生效，**只有 T3 的分数与 T2 接近这一条能抓到** | `15:§5.3` |
| H32 | **tunneling 假阳**：碰撞判据的采样间隔必须小于体厚，否则穿透会假阳 | `15:§1.1` C2 行 |
| H33 | **「加粒子特效」「加暂停键」「HUD 字体与位置变化」是故意放的三个近误杀用例** —— 分别考 E4（泄漏）、B1/E2（暂停不是卡死）、`fillText` 解析鲁棒性 | `15:§5.3` |

### 4.10 视频侧的分层处方（两句逐字，可直接当正文结论）

- `15:189`：**「录屏的 VLM 打分只报事件，不定生死。」**
- `15:824`：**「录屏 VLM 的输出进诊断，不进 reward。」**
- `15:§3.2`：**「R4 只能当否决器（画面全白就判挂），不能当排序器。」**
- `01:§4.3`：厂商侧三层结构 —— **先过确定性门控，再叠加模型评审；构建失败或伪造实现时 reward 置 0。**

---

## 5. 文 + 图 + 视频 + 音频

### 5.1 结论：**本地材料基本未覆盖**

对整个 `vc_data/` 目录做过音频关键词全量 grep（`音频|audio|Audio|声音|Web Audio|WebAudio|音效|hear|sound`），**在题的命中只有 6 处，没有任何一处是测量、公式、噪声地板或 hack 实例**。

明确的空白（都是 grep 确认的）：
- `10_blender_tasks.md`：**全文零次提及音频。**
- `19_aesthetics.md`：**视频 0 命中、音频 0 命中。**唯一和「动」有关的是从 computed style 读 `animation-duration` / `transition` 的取值分布，而且这一条被归到「**低确定性、无公开度量**」（`19:87`），处置是**档2 rubric 化评审，不是程序化闸**（`19:1032`）。
- `14_web_verifier.md` / `17_chart_verifier.md`：零音频判据。
- `16_primary_sources.md`：2,116 行里**没有音频 judge、没有音频 rubric、没有音频通过/失败判据、没有 TTS/波形/频谱 verifier**（全文 grep 确认）。
- 其余三处 grep 命中是无关的：`13_scaling_tasks.md:240`（audio 域 Coverage 0.020→0.653，讲的是嵌入选择）、`20_base_model.md:1962`（Uni-MoE 模态专家）、`09_pretrain_data.md:304`（预处理里删掉 `<audio>` 标签）。

### 5.2 全部在题的音频素材（6 条，逐字）

| # | 内容 | 出处 | 性质 |
|---|---|---|---|
| A1 | 抗欺骗强度排序把音频排在倒数第二：「输入重放加状态差分 > 绘制调用拦截 > 引擎自带钩子 > **像素与音频** > 要求模型暴露接口」 | `15_game_verifier.md:44` | 定性排序 |
| A2 | **唯一的音频判据实现路径**：「R4 像素与音频弱监督 \| 帧差；`AudioBufferSourceNode.prototype.start` / `AnalyserNode` 探测音效事件 \| A3、E7、B1 的弱版本 \| **容易骗**：背景动画会让每一帧都不同 \| 覆盖面：全部 \| 成本：低」 | `15:428` | 机制，无数字 |
| A3 | 配套处置：「**R4 只能当否决器（画面全白就判挂），不能当排序器**」，与 `feature-value-is-veto-not-ranking` 一致 | `15:§3.2` | 处方 |
| A4 | **音频通道的一个意外副作用**：「一个有用的副作用：**有声音的页面豁免后台节流**，所以 §3.2 的 R4 音频通道顺带解决了这个问题。」（指 Chrome 在后台不调 rAF 的问题） | `15:499` | 机制，可直接用 |
| A5 | 「加音效」在变异清单里是**不该挂**的那一类（额外功能） | `15:695` | 标注约定 |
| A6 | Anthropic 一手承认的模态盲区（逐字）：「the agent's song composition skills could clearly use a lot of work. Additionally, **Claude can't actually hear, which made the QA feedback loop less effective with respect to musical taste.**」笔记的推广：「**判别通道缺失的那个维度，harness 就是瞎的。**音频对 Claude 是这样，three.js 的三维结构对单张截图是同样的事。」 | `16:195`、`16:197` | 一手引用 + 推广 |
| A7 | `draft_domains.md:166`：像素 + 音频弱监督，**容易骗** | `draft_domains.md:166` | 与 A2 同义 |

### 5.3 这节能写什么、不能写什么

**能写的**（只有三条，且都是定性的）：
1. 音频在本项目的分级里是**最弱的判别通道之一**（排在倒数第二，只强于「要求模型暴露接口」）。
2. 技术上有两个具体钩子可用：hook `AudioBufferSourceNode.prototype.start`（音效事件的触发时刻）和 `AnalyserNode`（有没有声音在出）。它们能验证的是 A3「画面/声音有内容」、E7「没塌」、B1「输入能改变状态」的**弱版本**。
3. 有一个工程副作用值得单独写：**给页面加声音可以豁免 Chrome 的后台节流**，于是音频通道顺带解决了「rAF 在后台不被调用导致帧计数误判」这个假阳问题。

**不能写的**（这节必须明确标注的空白）：
- **没有任何音频判据的噪声地板实测值。**
- **没有任何音频 judge / 音频 reward model 的可靠性数字。**
- **没有任何音频相关的 hack 实例**（A2 的「容易骗」是对像素帧差说的，不是对音频说的）。
- **没有任何把音频纳入分层组合的方案或权重。**
- **没有任何一家厂商披露过把音频当 reward 信号。**

→ 建议正文就按这个口径写：**「文+图+视频+音频」这一档，本地材料未覆盖**；可以给出的只是「音频该放在分层的哪一层（否决器，不是排序器）」和「两个可用钩子」，以及 Anthropic 自己承认的那条通用律 ——「**判别通道缺失的那个维度，harness 就是瞎的**」。

---

## 6. 跨模态通用：hack 防御、校准协议、统计口径

这一节不属于任何单一模态，但五节正文都要引。

### 6.1 判别力的四个指标与门槛（`11_hacking_defense.md:§2.2`，公式块逐字）

```
DR  = 被杀掉的变异数 / 该挂的变异数            （变异杀死率 / 检出率）
FKR = 被误杀的等价改写数 / 不该挂的总数        （误杀率）
AR  = 1 − FKR                                  （接受率 / 保真率）
J   = DR + AR − 1                              （Youden's J）
```
配套：Wilson 区间公式（`11:191-195`）、样本量表、**rule of three**（0 次事件时的上界 ≈ 3/n）。

**重测翻面率公式**（`11:§2.3`，全库最有用的一个公式）：
```
F = 1 − q^K − (1−q)^K
```
实例：WorldBench **7/32 ≈ 21.9%** 的翻面率 → 反推单次判对率 **q ≈ 12.5%**；**K=5 的多数投票把翻面率压到约 1.6%**。

κ 的样本量（`11:§2.4`）：**200 对只够平衡任务；通过率 10~20% 时要 340+ 对。**

### 6.2 rubric 条款的权重失衡（`11:§2.7`，这组数字很有冲击力）

- **存在型条款占 90.2%，非存在型只占 8.6%**。
- 存在型条款满足时 **+14.9**，非存在型违反时只 **−2.0**。
- completeness **+1.07**，conciseness **−2.91**。
- 指令块（`11:377-389`）：**要求非存在型条款占比 ≥ 30%，并列了 7 条必备条款。**
- **Rubric Dropout 的甜点区是 30~50%**；而**按有用性加权比什么都不做更差**。

### 6.3 过优化的四个在线监控量与停训信号（`11:§3.0-3.3`）

- 14 行报警表（`11:§3.0`）。
- **WR / ROG / NRFR / RHR**；关键警告逐字：「**正的 ROG 不是没有 hacking 的证据**」—— **26.4% 的样本比基线更差**。
- **自内化差距（self-internalization gap）当停训信号**：峰值出现在 panel 共识峰值的 100 步以内；而**训练用 verifier 自己的 reward 在最后一个 checkpoint 之前从不见顶**。
- **CHERRL 的可复现起病判据**：Δ_gap 0.08 / 0.10 / 0.12，M_pct 15~30%，bucket ≥ 0.99 且 ≥ 20 个样本，5 步平滑。
- **起病在 68~478 步之间，而从起病到灾难只有约 100 步。**
- 六步排查顺序（`11:§3.6`）；抽样尺寸与 L-A…L-F 分层配额（`11:§4.1-4.3`）。
- **句法型 hack 在 Match Rate 0.6~0.95 可检出，语义型只有 0.0~0.4**（`11:§4.4`）。

### 6.4 沙箱与对抗注入（`11:§1`，两个逐字清单）

- **12 条沙箱检查表**（`11:104-116`）。
- **12 条对抗注入集**（`11:297-309`），配套校准要求：**注入必须判 0 分**（`04:291-297`）。

### 6.5 Anthropic 一手的 hack 清单与检测机制（`16:§5`）

- **Opus 5 §6.3 十二条 hack 清单**（`16:924-935`），含「Editing or deleting tests and checks in order to pass」「Attributing a visible defect to the environment and declaring the task done anyway」「Attempting to satisfy the inferred grading criteria, rather than the requested task」「Submitting a solution without compiling or running it, relying on a mental check instead」。
- **Fable 5 增补**（`16:943-950`）：「Exploiting unintended information leakage in training environments—recovering reference solutions from **git history, build caches**, or other answer-revealing artifacts」。
- **Opus 4.6 增补**（`16:954`）：「Premature claims of success… asserting that a programming task was complete because **some of** the tests had passed」。
- **grader 披露分档**（`16:798-803`）：清楚披露 8/10~10/10、含糊 4/10~7/10、几乎不披露 ≤3/10；「grader awareness across our models is **much lower when grading is not disclosed** in the prompt」。
- **CoT 监控判据（可直接抄）**（`16:768`）：「The monitor searches for cases where the model's reasoning references guidelines or instructions that **don't exist in the task contents**」；但「**The CoT monitor flags far fewer episodes overall than the NLAs do**」—— CoT 监控的召回远低于激活探针。
- **一个反直觉发现**（`16:772-776`）：对 grader awareness 做反向 steering，**同时降低了同一批环境上的行为 reward**；原文「steering primarily influenced these aspects of **presentation style**, rather than the overall content or implementation strategy」。
  → 笔记的读法：**grader 奖励的是表达方式，不是解法质量。**
- **把训练环境 prompt 改写成像部署**（`16:780-788`）：「These edits **reduce the model's train reward, grader awareness, and certain training-incentivized behaviors**」，但 NLA 测到的 awareness 只降了「modestly」。
- **探针从不当训练信号**（`16:1031`，逐字）：「we never used probe scores as a direct training signal.」
- **把静默守卫干预单独报出来的口径**（`16:1118`，可直接抄）：Toolathlon「Of **324 trials**, one trial (**0.3%**) was stopped by production safety classifiers and six (**1.9%**) were halted by our evaluation harness's sandbox-escape monitor, **and all seven are counted as failures**」。
- **过度验证也是一种失效**（`16:983,990`）：24 小时蛋白设计实验里，Mythos 5 交齐全部 **30** 个设计；一个 Opus 5 臂只交了 **17** 个未排序的，另一个**什么都没交、最后 8 小时沉默**，卡在自我验证循环里。

### 6.6 八种把任务变可验证的范式与准入（`03_verifiable_construction.md`）

- 统一任务抽象 `(S0, Q, I, A, R)` + M（`03:32-43`）；四个观察层表（`03:47-52`）。
- 八种构造范式，每种都列了「能验 / 不能验」；视觉侧 F2P/P2P 逐栈表（`03:78-82`）。
- **三条准入条件**（`03:84-87`）：参考解必须过、被破坏版必须挂、检索片段必须唯一。
- 14 行可计算数据质量指标表 + 阈值（`03:326-340`）。
- **R2E-Gym：大多数问题里不到 20% 的测试能区分正确与错误补丁。**

### 6.7 统计与样本量（`19:§5.5` 的公式块，正文引数字时要拿来自检）

```
ICC(1,k) = k·ICC(1,1) / (1 + (k−1)·ICC(1,1))
k        = ρ_target·(1−ICC₁₁) / (ICC₁₁·(1−ρ_target))
Δ_Elo    = θ × 400/ln10                  → 1 logit = 173.72 Elo
SE(θ̂)   = 1/√(n·p(1−p))                 → SE_Elo ≈ 347.4/√n
n        = (1.96×173.72/h)² / 0.25        （CI 半宽 h）
n        = 947,600 / Δ²                   （检出 Δ Elo，80% power，α=0.05 双侧）
design effect = 1+(m−1)ρ̄ = 1+9×0.206 = 2.85 → n_eff = 10/2.85 = 3.51
MDE      = 2.38/√(M·n)
```

三组可直接用的推论：
- **标注人数**（起点 ICC(1,1)=0.369）：ICC ≥ 0.70 要 **4 人**、≥0.80 要 **7 人**、≥0.90 要 **16 人**、≥0.95 要 **33 人**（`19:783-789`）。⚠️ Spearman-Brown 假设评分者可交换、误差独立同方差，审美标注很可能有共享偏差 → **7 人 / 16 人应当当作乐观下界**（`19:792-793`）。
- **加题比加人划算**（`19:849-852`）：k 从 3 到 16，人力 ×5.3，题量只省 **30%**。
- **10 个 judge 只值 3.5 个**（`19:861-871`）：LLM judge 的错误相关 **ρ̄ = 0.206** → design effect 2.85 → **n_eff = 3.51**；只换训练 seed 的两个 GRPO judge 错误相关 **0.36~0.39**，加第二个 seed 只让 n_eff 涨 **0.11** —— **seed 多样性买不到独立性**。
- **判别力的可测下限**：审美维度建议 M=30 题、n=8 → **MDE ≈ 15.4 个百分点**；想读 5 个点需要 **M·n ≈ 2,260**，「**在审美维度上不划算**」（`19:898-900`）。

### 6.8 一个反复出现的方法论警告（五节正文都适用）

- **「能把该挂的和不该挂的分开」≠「能当闸」**（`19:986`，逐字）：还要看**余量**、**好样本在哪一侧**、**极端情形会不会翻向**。
  最佳实例是栅格对齐（`19:971-986`）：参考页 0.824、该挂的 A09 **0.707**、该挂的 A07 **0.794**、**该过且审美更好的 P03 却是 0.765**（比 A07 更接近失败）、**最糟的 A10（抹掉所有边距）对齐率反而是 1.000**。存在可分离阈值（0.707 < t ≤ 0.765），但余量只有 **0.058**（相对 0.824 是 7%），且方向在极端情形下翻转 → **作废当闸，只留作连续诊断量。**
- **假阳性多数来自度量定义本身，不是来自阈值**（`19:962`）：`widthCh` 原来用容器宽度除以估算字宽，于是「25 字的短标签放在 1400px 容器里」被算成 **200ch**；修法是 `min(容器容量, 实际字符数)`。修之前参考页在 1440 档就有 1 个假报警。同构的是图表侧三个 verifier bug（全是假阳、全是坐标系问题、全不是调阈值能修的，`17:§4.4`）。
- **信号是在它自己验证的那个 case 上造出来的，就不算独立验证**（`90:§3.4` 自述）：开放边界边数这个信号是在 `ok_lathe` 上创造的，所以「加了之后 13/13 和 16/16」不是独立验证。
- **准入拒绝率按场景特征分层之后必须是均匀的**（`draft_verifier.md:§9`，新加的验收指标）：当前是 1/10 和 2/16 → 0/16，**但从没分层看过**。
- **六个实测盲点全是假阳性、全不是调阈值能修的**（`draft_verifier.md:255-262`）。

---

## 7. 所有能用的量化数字清单

**状态标记**：
- 【92 已核实】= `92_number_audit.md` 回原文逐值核过，可直接用
- 【92 已更正】= 旧值被更正过，这里写的是**新值**
- 【92 未核】= `92` 明示没有第二次核验
- 【本机实测】= `scripts/vc_verifier/` 跑出来的
- 【引用】= 调研 agent 一手引用，无二次核验
- 【推算】= 不是实测
- 【待核】= 我发现的疑点，正文引用前必须回原文

### 7.1 外部榜单与仓库（全部【92 已核实】）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| three.js 参考截图 **610** 张 | 像素基线仓库的供给量 | `92:12` | 【92 已核实】读 dev 分支文件树，未截断 |
| Babylon.js 参考图 **975** 张 | 同上 | `92:13` | 【92 已核实】10,476 个文件未截断 |
| Blender 渲染测试参考图 **2,596** 张 | 同上 | `92:14`、`10:325,426-429` | 【92 已核实】22,173 个文件未截断 |
| Blender 官方 `tests/files/render/` = **48 类目 / 839 个 .blend** | F2P 任务的原料规模 | `10:426-429` | 【引用】（2,596 那部分已核实） |
| Blender `tests/files` 全量 **7,240** 个文件（LFS） | 同上 | `10:461` | 【引用】 |
| 3JSBench：Astra **80.0% ±4.5（240/300）**、Opus 5.5 **49.0% ±5.7（147/300）**、Kimi K3 **23.0%**、Gemini 3.8 Flash **8.7%** | 分层确定性判据下的真实通过率分布 | `92:19` | 【92 已核实】无头浏览器渲其单页站；**站方 2026-10-14 改判过一次，这是改判后的值** |
| 3JSBench：**100 道题 / 每题三次一次成型的尝试 / 10 个模型** | 样本规模 | `92:20` | 【92 已核实】 |
| 3JSBench：**695 条必查项分六族** —— 部件计数 **223**、结构 **160**、空间关系 **157**、任务专属几何 **45**、文字 **12**、渲染质量 **98** | 「判据可以做到多细」的现成答案 | `92:21-22` | 【92 已更正】**原为 743，禁用** |
| 其中部件计数 223 + 结构 160 + 空间关系 157 = **540 条，占 78%** | 判据的重心在「有几个、接在哪、挨着谁」 | `15:§1.2` C 族 | 【92 已核实】（分项来自 695 那组） |
| 3JSBench 管线：隔离无头浏览器 → 记录场景并渲 **九个固定视角** → 在捕获到的场景上做确定性测量 → **全部必查项通过才算过** | 乘法门控的外部实例 | `92:23-24` | 【92 已核实】 |
| 3,000 次尝试里最常见失败：**物体互相穿插 20%、可见背面 19%、表面闪烁 17%、朝向不符 16%、部件断开 16%** | 失败模式的真实分布，用来选判据 | `92:25` | 【92 已核实】 |
| SigLIP2 相似度：Astra 加 **0.011**、Opus 5.5 加 **0.009**、GPT-6 Sol 加 **0.007**，而通过率是 **80.0% / 49.0% / 27.0%** | **53 点通过率差距对应 0.004 相似度差距** → 嵌入相似度零区分度 | `92:26-27` | 【92 已核实】站方明确标为不参与判定 |
| Muse Spark 1.3 中位 **995 个 mesh / 177,000 三角面**，Astra 只用 **45** 个 | 网格预算族（98 条检查）的判别对象 | `91_3jsbench_verified.md`、`15:§1.1` E4 行 | 【92 已核实】（出自已核实的 695/六族那一组） |
| Muse Spark 有 **33%** 的尝试出现闪烁 | E5「不闪烁」判据的必要性 | `15:§1.1` E5 行 | 【92 已核实】 |
| Gemini 的 markdown 围栏：300 次里 **55 次**，只有 **1** 次通过 | L0 执行门的价值 | `91_3jsbench_verified.md` | 【引用】 |

### 7.2 WorldCoder-Bench 四种判定方式（整表【92 已核实】，`92:50-59`）

| 判定方式 | 通过率 | 与真值 Kendall τ_b | 假阳率 | 相对成本 |
|---|---|---|---|---|
| 只读 DOM | **32.6** | **−0.021** | **33.7%** | 1 倍 |
| 截图加 VLM | **2.7** | **−0.068** | 3.2% | 约 **50 倍** |
| 八步 agent 自主探查 | **49.7** | **+0.111** | **45.6%** | 约 **400 倍** |
| **隐藏运行时状态契约** | — | **1.000** | **0.0%** | 约 **2 倍** |

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| 九个前沿模型里最好的一个在隐藏契约上覆盖率只有 **27.8%**（严格档 **19.9%**） | 隐藏契约判据又准又便宜，但模型目前远远过不去 | `92:57-59` | 【92 已更正】**2.7% 不是模型能力，别混用** |

### 7.3 感知指标与 VLM judge 的可靠性

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| 2AFC 人类一致率：PSNR **57.1%**、SSIM **57.3%**、LPIPS **70.7%**、DreamSim **96.2%**、CLIP **83.1%** | PSNR/SSIM 基本等于抛硬币；只有 DreamSim 够用 | `04:34-42` | 【引用】 |
| Design2Code 细粒度指标组合预测人类胜负 **79.9%**，**Text 系数为负** | 文本相似度越高人类越不喜欢 | `04:34-42`、`14:367-371` | 【引用】 |
| UI2Code^N comparator 与人类一致 **94%**，零样本 **62%**，GPT-5 **85%** | 专训判别器 > 前沿通用模型 | `04:52-56` | 【引用】 |
| UIClip 成对选择 **75.12%**；缺陷检测 **87.1%**；纯 CLIP 预训练 **65.42%**；**GPT-4V 仅 51.58%**；LLaVA **54.59%** | 151M 参数的专训小模型碾压前沿 VLM | `19:122,135` | 【引用】 |
| UIClip 规模：JitterWeb **2,466,969** 行、paired **313,186**、人评 **2,350** 行（约 1,175 对）、CLIP B/32 约 **151M** 参数 | reward model 能塞进 RL 内循环 | `19:122,299` | 【引用】 |
| Visual-ERM（8B）：VC-RewardBench **F1_hard 比基座 +36.8**，**GPT-5.2 只 32.7** | 同上 | `04:52-56`、`19:129` | 【引用】 |
| RULER rubric 与人类 Spearman **0.7929**；Aesthetic 预测器 **0.6051**；CLIP **0.5518** | 实例级 rubric ≫ 标量美学分 | `04:52-56`、`19:130-131` | 【引用】 |
| RULER 通用措辞在 Icon 上掉 **9.2 点**（0.591 对 0.683） | rubric 必须实例级 | `19:130` | 【引用】 |
| ArtifactsBench：与 WebDev Arena 排名一致 **94.4%**；与人类专家两两一致最高 **90.95%**；**只给代码 79.06 / 加图注 81.74 / 给真图 90.95 / 只给图不给代码 74.94** | **代码是主导模态，图是补充** | `92:44` | 【92 已核实】 |
| WebDevJudge：人类 pairwise **84.56%**；最好 LLM judge GPT-4.1 pairwise **70.34%**、single-answer **60.86**；Claude-4-Sonnet **59.17 / 70.18** | 人类天花板与模型差距 | `19:151,672-676` | 【引用】 |
| WebDevJudge 消融：**只给截图 pairwise 掉 9.79~10.7 点；只给代码只掉 0.31~2.60 点** | 同上（第二组独立证据） | `19:679-681` | 【引用】 |
| WebDevJudge rubric 效应：无 rubric **65.0%** → 人工 rubric 树 **92.0%** → LLM 生成 rubric **90.0%** | rubric 能大幅提高原始一致率 | `19:656-662` | 【引用】⚠️ **三条限定**：65.0% 来自 100 条、92.0%/90.0% 来自另外 50 条（**非受控 A/B**）；是 **raw agreement 无 chance correction**，不是 kappa；**只有 2 人** |
| AesCoder：**GPT judge 对人类 80.9%**（10 人 × 200 对 = 2,000 条），而**人与人只有 68.7%** | judge 可以超过人与人一致率 | `19:126` | 【引用】 |
| UIClip 评分者间 **Krippendorff α = 0.37** | 审美标注的噪声地板 | `19:122` | 【引用】 |
| BlenderGym VLM 两两比最好 **0.66**，人与人 **0.79** | 3D 侧 judge 的校准目标线 | `10:779,842`、`04` | 【引用】 |
| WiserUI-Bench 位置偏置：**o1 胜者在前 16.56% / 在后 97.78%**；**GPT-4o 31.89% / 88.33%** | **必须做 AB/BA 交换** | `19:125,1083` | 【引用】 |
| WiserUI-Bench 最佳 MLLM **GPT-4o 60.11%**（随机 50%）；一致准确率最佳 InternVL-2.5-38B **34.56%**（随机 25%） | 不依赖口味的外部校准集的现实水位 | `19:125,650,1083` | 【引用】 |
| WiserUI-Bench 规模：**300 对**真实 UI，胜者由**真实 A/B 测试转化率**决定；684 条专家 rationale；web 252 / mobile 48 | 唯一的「不含口味」真值 | `19:125,303` | 【引用】 |
| LLM judge 的错误相关 **ρ̄ = 0.206** → design effect **2.85** → **n_eff = 10/2.85 = 3.51** | **10 个 judge 只值 3.5 个** | `19:861-871` | 【引用】RewardBench 1,133 条校准对 |
| 只换训练 seed 的两个 GRPO judge 错误相关 **0.36~0.39**（跨模型均值 0.24）；加第二个 seed 只让 n_eff 涨 **0.11** | **seed 多样性买不到独立性** | `19:870` | 【引用】 |
| **28%** 的系统对比会得出假显著（Focus 子集 28%、Factuality 22%、Math 与 Precise IF ≤ 2%） | 上界而非普适 | `19:863-866` | 【引用】 |
| 同一 LLM judge 重判同一规则，重判分差 ≥0.25 的比例 **12.7%（Small）/ 8.8%（Big）**；谓词结构不同时 **17.7% / 11.1%** | 游戏/时序判定的 LLM 噪声地板 | `15:§1.4`（A2Z 附 B.5 表 S10） | 【引用】 |
| 换 judge 配置、固定轨迹：一致率 **0.910 / 0.888**（222 条里 6 条、242 条里 3 条改了判分） | 同上 | `15:§1.4` | 【引用】 |
| 人与人同 rubric **91.4% / κ=0.68 / α=0.624** | 天花板 | `15:§1.4,§0` | 【引用】 |
| → **LLM 参与的游戏判定上，3 个百分点以内的效应不要信** | 效应量的可信门槛 | `15:§1.4` | 【引用】原文结论 |
| PlaytestArena：GUI judge 与人条目级 **87.9%（κ=0.66）**，人与人 **91.4%（κ=0.68）**；游戏级 ρ **0.89** 对 **0.92** | judge 的一致率天花板已逼近人类 | `15:§0` 第 8 条 | 【引用】 |
| PlaySuite：judge 与人「±1 级内一致」**90.4%**，人与人 **93.0%**；人与人 Krippendorff α 只有 **0.624** | 同上，**差距只有 2.6 个百分点** | `15:§0` 第 8 条 | 【引用】 |
| TTCW：**14 条二元测试**；LLM 故事通过条目数比专业作家**少 3~10 倍**；**没有一个 LLM 与专家评分正相关** | LLM 当原创性 judge 失效 | `19:143` | 【引用】 |
| Creativity Index：专业人类作者比 LLM 高 **66.2%**；**对齐把 LLM 的 Creativity Index 压低 30.1%** | 对齐与原创性的张力 | `19:144` | 【引用】 |
| Idefics2-8B 直接生成 **46.7**，自我修订掉到 **12.3** | 没有外部判据的自我修订对开源是负收益 | `92:34` | 【92 已核实】 |

### 7.4 本机实测：判别力（这节是正文的硬骨架）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| three.js 29 变异：像素 **12/29**、几何类别多重集 **14/29**、多视角剪影 **19/29**、逐颜色体素 **25/29**、**四层组合 29/29** | 分层组合 > 最好的单层 | `90:100-106` | 【本机实测】 |
| three.js 留出：car，9 个 mesh，**18 个变异跑前贴标签、阈值不动 → 18/18**；累计 **47/47**（18 个真留出） | 分层判据换场景没塌 | `90:§2.3` | 【本机实测】 |
| 开放边界边数：**0 对 64** | 拓扑量不随洞的大小衰减 | `90:§3.4` | 【本机实测】⚠️ 信号是在它验证的那个 case 上造的，不算独立验证 |
| Blender 合并 22 变异：view0 **12/22（检出 2 / 保真 10）**、多视角剪影 **14/22（3/11）**、全局 Chamfer **13/22（2/11）**、**全局 F-score 11/22（检出 0 / 保真 11）**、逐部件 F **18/22（7/11）**、**全量状态断言 11/22（检出 11 / 保真 0）**、**combo_pc 21/22（11/10）** | 「检出」和「保真」必须分开看；两种极端都没用 | `10:574-592`、`draft_verifier.md:65-73` | 【本机实测】 |
| Blender dev 集 15 个（8 挂 / 7 过）：**combo_pc 15/15**；A2 保真 **4/7**；A3 保真 **3/7** | A2/A3 不能进闸的实测依据 | `10:523-541` | 【本机实测】 |
| Blender 留出 7 个（3 挂 / 4 过）：**combo_pc 6/7**（检出 3/3，1 个误杀）；**剪影 IoU 检出 0/3** | 换批次没塌；剪影对小部件失效 | `10:555-570` | 【本机实测】 |
| **杯子平移 30 cm：全局 Chamfer 0.00018 / 逐部件 0.08375 = 460 倍**；全局 F@0.5% **0.9916**（能过 0.99 闸）/ 逐部件 **0.2243** | **几何必须逐部件算** | `10:708,721-723` | 【本机实测】 |
| 杯子占场景表面积约 **2%** | 稀释倍数的来源 | `10:721-723` | 【本机实测】 |
| `bulb_dim`（60 W→6 W）与 `anim_missing`：view0 / 多视角 / Chamfer / 全局 F / 体素 / 逐部件 F **全部 1.0000** | 静帧看不见的属性只能靠断言 | `10:510-511` | 【本机实测】 |
| `bevel_removed`：剪影 **0.9831**、逐部件 F **0.9992**、全局 F **1.0000**（1 cm / 2.18 m = **0.0046 diag ≈ tau**） | 低于采样分辨率的需求别指望几何指标 | `10:512,728-729` | 【本机实测】 |
| `camera_moved`（**该过**）view0 **0.9534** vs `wood_blue`（**真错误**）view0 **0.9844** | **画面变化量与语义错误量完全不相关** | `10:516,509` | 【本机实测】 |
| `mug_moved` 30 cm 的多视角剪影仍是 **0.9934** | 剪影对小部件天生不敏感 | `10:547,568-570` | 【本机实测】 |
| 灯罩在 48³ 下只占 **20 个体素**；开放曲面体素化重叠 **0.017** | **小部件上的占据类指标不是相似度，是等值判断** | `90:§6` | 【本机实测】 |
| tau 扫描：tau=0.1% diag 时该过的 `mug_seg_48` **0.4977** < 该挂的 `shade_flipped` **0.9639** | **tau < 采样间距时 F-score 测的是采样密度** | `10:674-697` | 【本机实测】 |
| 60k 点 / 2.18 m 场景 → 平均点距 **约 3~5 mm**；安全下界 **tau ≥ 3 × 平均最近邻距离** | tau 的选法 | `10:689-700` | 【本机实测】 |
| tau=1% diag 时 8 个该挂的里只有 **1** 个低于 0.99 | tau 太大只能抓「整个部件消失」 | `10:689-697` | 【本机实测】 |
| 逐部件 F 的 pass 组下限 **0.9989** → 阈值定 **0.99** → **7/11 检出、11/11 保真** | 阈值怎么从参考反推 | `10:724-727` | 【本机实测】⚠️ **这一条是后定的，已标注** |
| Web 五层组合 **22/22**，检出 **11/11**，误杀 **0/11**；类名序列层**检出 0/11、误杀 3/11** | 不是所有确定性信号都有判别力 | `14:§4.5` | 【本机实测】⚠️ **22/22 是第二次跑；第一次 21/22**，两个不同原因 |
| Web 像素：噪声地板 **0.000**，但 **11 个该挂的里 7 个像素完全相同（1.0）**；最佳阈值只到 **14/22**、4-of-11 检出；**P3 重新配色（该过）像素差 0.9002** | **零噪声不等于有用** | `14:§4.6` | 【本机实测】 |
| Web **231 个字段，5 次重复里只有 4 个会变；所有参与判定的字段逐字节相同** | DOM 回读的噪声地板 | `14:§4.2` | 【本机实测】 |
| Web 两次完整重跑**判定翻面 0 次** | 对照 3D 侧 VLM judge 最差档约 28% | `14:§4.8` | 【本机实测】 |
| Web 作弊页 **7 个**，第一版挡住 5 → 补判据后 **6/7**；**K4 仍是 axe 的结构性盲区**（`violations: []`、`incomplete: []`、`passes: 45`，issue #2680 开启） | 作弊集必须单独做 | `14:§4.9` | 【本机实测】 |
| 图表 16 变异：**S1（逐值回读）13/16 零误杀**、**S2（像素）9/16 且 4 个误杀**、**S3（结构）14/16 零误杀**、**S1 OR S3 = 16/16** | 回读 + 结构 = 满分；像素是拖累 | `17:§4.3` | 【本机实测】 |
| 图表像素差：`data_one_point` **0.75%**、`legend_swap` **0.01%**、`recolor`（该过）**30.51%** | **像素比对在图表上根本不存在可用的工作点** | `17:§4.3` | 【本机实测】 |
| 图表回读耗时 **1~4 ms**，是渲染的 **4/1000** | 比截图便宜两个数量级 | `17:§4.1` | 【本机实测】 |
| 图表噪声地板：5 次重复逐位相同，md5 单一；参考图自己对自己 **canvas 0.15%**（距 1% 阈值 6 倍余量）、**SVG 0.02%** | 噪声地板的实测值 | `17:§4.2` | 【本机实测】 |
| 修掉三个 verifier bug 后：S1 **12/16 → 13/16**、S3 **13/16 → 14/16** —— **提升纯粹来自消除假阳** | 假阳不是调阈值能修的 | `17:§4.4` | 【本机实测】 |
| 审美 20 变异：该挂抓到 **9/11**，不该挂 **8/8 零误杀**，总计 **17/20**；单变异 **约 0.8 秒**纯 CPU | 审美可以做成零噪声硬闸 | `19:917-923` | 【本机实测】 |
| 审美两次独立运行 20 个 case：**连续读数逐位相同，0/20 不一致** | 噪声地板 = 0 | `19:1041,885` | 【本机实测】 |
| 功能侧 W0~W4 对 11 个审美变异**判过 9 个**；审美判据在那 9 个盲区里补上 **7 个** | 审美判据不是功能判据的子集 | `19:18-19,950` | 【本机实测】 |
| 栅格对齐：参考 **0.824**、A09（该挂）**0.707**、A07（该挂）**0.794**、**P03（该过且更好）0.765**、**A10（最糟）1.000** | 「能分开」≠「能当闸」 | `19:971-986` | 【本机实测】→ **作废当闸** |
| 栅格对齐可分离阈值余量只有 **0.058**（相对 0.824 是 **7%**） | 余量不足 | `19:980-985` | 【本机实测】 |
| 圆角一致性：参考页本来就有 **4 种**（6/8/10/999px），变异推到 **6 种**，距离只有 **2 档** | 判别余量不足 → 作废 | `19:965-968` | 【本机实测】 |
| 参考页间距基数分布：**2 → 91.4%、4 → 57.8%、8 → 32.8%、10 → 20.7%、16 → 16.4%**，共 **12** 个取值 | **4px 栅格假设被实测推翻**；最佳基数是 2 | `19:93-110` | 【本机实测】 |
| 审美参考页最小对比比值 **6.27**；字号种类 **7**、相邻比值 **CV 0.133**；字体族 **1**；行长 **42.8ch**；色相家族 **1**、熵 **0**；间距种类 **12**；墨水覆盖率 **0.296 / 0.526** | 阈值全部从参考页反推 | `19:990-1000` | 【本机实测】 |
| 审美判据**真正被独立验证过的只有 6 条**（`len` 判别力未验证、`ink` 无独立验证，8 条进闸） | 诚实折扣 | `19:1003-1009,1111` | 【本机实测】 |
| flaky 基线：9 个产物 × 3 次探测 → **翻面 0/9，数值逐位相同 0/9** | 确定性基线 | `90:§12` | 【本机实测】 |
| `hack_probe.py`：5 个可用作弊页，**verifier 通过 0 个**（真实分母是 12 里的 5） | 作弊集测试结果 | `90:§13` | 【本机实测】 |
| 从零生成：**0/13 和 0/13**，**26 个里 23 个死在 L1** | 从零任务极难过闸 | `draft_verifier.md:§10` | 【本机实测】 |
| `relational.py`：从零 **0/80 → 13/80**，但修复任务 **47/47 → 35/47** | 判据必须按任务类型分叉 | `draft_verifier.md:§10` | 【本机实测】 |
| 离屏渲染器作弊页修好后新增两个信号：互穿 **0.053 → 0.762**、绘制顺序 **5534 个像素**变化；回归 **13/13、16/16、18/18** | 蜜罐 + 新信号 | `draft_verifier.md:§5,§7` | 【本机实测】 |
| `pair_overlap` 信号**失败**：参考解自己在 48³ 下的最大值就是 **1.0** | 没有余量的信号要丢掉 | `draft_verifier.md:§7` | 【本机实测】 |
| 准入拒绝率 **1/10 和 2/16 → 0/16**，**但从没按场景特征分层看过** | 新加的验收指标 | `draft_verifier.md:§9` | 【本机实测】 |
| 审美缺陷：**审美判据抓到 9/11，功能判据只抓到 2（而且是顺带）**，**0/8 误杀**；约 **0.8 秒** 对 **4.9 秒** | 审美判据的独立价值 | `draft_verifier.md:§11` | 【本机实测】 |

### 7.5 本机实测：VLM judge 可靠性与重测翻面

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| **768 条判定**；单模型重测**翻面率 4.2% ~ 20.8%**；最差是 **claude-opus-5-5 多视角档 20.8%**；gemini-3.8-flash **8.3% → 0.0%** | VLM 的噪声地板 | `90:168-174` | 【本机实测】4 个家族 judge × 48 case × temp 0 × 各 2 次 |
| 4 模型 8 票多数投票：单视角 **44/48**、多视角 **46/48**；**程序化信号在同一标注集上 47/47** | 投票能降噪但仍不如程序判据 | `19:873-876` 转引 `90:§3` | 【本机实测】 |
| **有参考图 94% / 97%**（检出 92%~95%）vs **无参考图 68% / 76%**（检出 61%~63%）；4 视角下保真仍 **39/40** | 参考图对 VLM 的价值，以及无参考图时 VLM 只能当补抓 | `90:702-706` | 【本机实测】 |
| Blender 4 judge × 2 条件：最好 **16/22**（gpt-6-astra），检出只有 **3~6 / 11**，保真约 **11/11** | **VLM 是高保真低检出器件** | `10:757-769` | 【本机实测】 |
| 多视角拼图：**16→16、13→14、14→15、14→14**；doubao multi 多丢 **3** 个解析失败 | **多视角拼图几乎没用，还抬高解析失败率** | `10:770-771` | 【本机实测】 |
| **VLM 独占的检出：0 个**（22 个变异里 VLM 抓到的程序化信号全都抓到了） | VLM 不提供独立信息 | `10:807` | 【本机实测】 |
| `camera_moved`（该过）被 **8 个条件里的 4 个**判错，**尽管题面明确说相机位置不算错误** | VLM 分不清「画面变了」和「场景变了」 | `10:777-779` | 【本机实测】 |
| 8 个条件全都漏掉的变异：`table_thin`（5→2 cm）、`bulb_dim`、`anim_missing`、`bevel_removed`、`cam_lens_24` | **一个是量化尺寸，四个是静帧里不存在的属性** | `10:772-774` | 【本机实测】 |
| 8 个条件全都抓到的变异：`mug_handle_missing`、`wood_blue`、`mug_moved` | 全是语义级、人眼显然的 | `10:775-776` | 【本机实测】 |
| VLM 成本：**865 秒 / 176 次 ≈ 每次 5 秒**（并发 12），对照程序化全套 **2.3 秒**；**176 次里 5 个结果无法解析** | VLM 比程序判据贵一个量级 | `10:814-817` | 【本机实测】 |
| `ok_lathe` 翻盘：**人的标签是错的，4 个 VLM 是对的** | 标注本身会错 | `90:§3.4` | 【本机实测】 |
| 18 个样本的早期结论是误导性的（后来被推翻） | 样本量不够就不要下结论 | `90:§3.1` | 【本机实测】 |
| ⚠️ Blender 侧 VLM **只跑了 1 遍，没有自一致率数字**；`should` 标签**只有 1 个标注者，没有一致率** | 必须声明的折扣 | `10:841-843` | 【本机实测】自述 |

### 7.6 本机实测：成本与确定性

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| Blender 单次探针 **1.61~2.43 秒，均值 2.3 秒**（exec 0.23~0.30 / 读九族 0.07~0.15 / 采 **59,992** 点 0.15~0.21 / Workbench 渲 10 视角 256² 1.09~1.24） | 成本分解 | `10:596-610` | 【本机实测】 |
| 22 个变异含重建参考 **约 70 秒**；从已有 `runs/` 重算全部信号 **12.8 秒 / 22** | 阈值扫描的成本 | `10:596-610` | 【本机实测】 |
| 几何指标：Chamfer+HD95 **107 ms**、F-score **106 ms**、32³ 逐色体素 **36 ms**、逐部件版约 **120 ms**、采样 150~210 ms → **全套约 0.4 秒** | 对照 10 视角渲染 1.1~1.2 秒 | `10:733-744` | 【本机实测】 |
| → **几何比渲染便宜 3 倍，判别力还更高**（逐部件 F 检出 7/11 对多视角剪影 3/11） | 「只能留一个视觉信号就留几何」 | `10:743-744` | 【本机实测】 |
| Cycles CPU 512×512 / 32 spp ≈ **0.9 秒/帧** | 为什么用 Workbench | `10:459-460` | 【本机实测】 |
| three.js 探针 **0.8~1.0 秒**（含启动浏览器）；池化后约 **14 任务/秒** | 浏览器侧成本 | `draft_verifier.md:§6`、`90:§1.5` | 【本机实测】 |
| 场景图 13 个 mesh **1.8 ms**；单张截图 **62~85 ms**；8 视角转台 **0.2~0.5 秒**；Blender Workbench 32 进程 **15.5 视角/秒** | 成本梯度 | `draft_verifier.md:§6` | 【本机实测】 |
| Blender 单进程 2.3 秒/任务，持久池预计 **< 1.3 秒/任务** | — | `10:608-610` | 【推算】原文写「预计」 |
| **确定性**：只上虚拟时钟 → **3 个不同结果**；加暂停+步进后 **20 次里仍有 2 次不一致**；**只有 harness 驱动帧推进 + 直接读 canvas 才逐字节一致** | 时序 reward 的噪声地板能做到 0，但要做对 | `draft_verifier.md:§6` | 【本机实测】 |
| 不传 `seed=` 时参考解和自己比的 Chamfer 是 **0.00167 而不是 0** —— pass/fail 带宽只有 0.0016~0.0065，「**噪声地板直接吃掉一半判别力**」 | 零噪声是有条件的 | `10:866-867` | 【本机实测】 |
| 参考解跑两遍：图像 **1.0000**、Chamfer **0.0**、体素 IoU **1.0** → **噪声地板 = 0** | 所以阈值只能按「什么算语义等价」定 | `10:494-496` | 【本机实测】 |
| 冻结阈值：图像 **0.995** / 剪影 IoU **0.97** / Chamfer ≤ **0.004 diag** / 体素 IoU ≥ **0.80**；逐部件 F **0.99** | 可直接抄的阈值 | `10:494-496,724-725` | 【本机实测】 |
| 审美侧成本 **0.8 秒/页，纯 CPU**；带功能侧 W0~W4 同跑 **66 秒**；不带 **17 秒 / 20 个变异** | 适合当 L0/L1 乘法闸 | `19:885,910` | 【本机实测】 |
| 审美侧环境：**无 GPU，Chrome 148 无头 + SwiftShader，固定视口 375 / 1440，固定 `Math.random` 种子与 `Date`** | 可复现条件 | `19:911` | 【本机实测】 |
| 单模型 pass@8：**3/16 = 19% 可用**（Wilson **6.6%~43.0%**）；**0.3~0.7 难度带里 0/16** | 任务供给的真实水位 | `90:§15` | 【本机实测】 |
| 成本模型 **0.60 → 0.19**；漏斗 **37.2% → 11.8%**；候选量 **269k → 848k（×3.2）** | 难度带保留率的代价 | `90:§15` | 【本机实测】 |

### 7.7 Reward hacking 的量化（外部，大部分一手）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| **RULER 换成整体美学分**：美学分 **4.309 → 6.697**，rubric 分 **0.395 → 0.262（低于零样本基线）**，输出 token **0.3k → 6.3k（21 倍）** | 最典型的「堆叠重叠描边与重复装饰」刷分实例 | `19:131` | 【引用】⚠️ 同文件 `19:347` 写的是 **4.42 → 6.21**，见 §8 矛盾 2 |
| 换成结构化 rubric 后 hack 换形态：「把 query 词画成风格化标签」，分从 **0.693 压到 0.536** | **rubric 形式会改变 hack 的形态，不会消除 hack** | `19:130,360` | 【引用】 |
| **CLIP 相似度当 reward**：Design2Code **72.3 → 62.0**、Flame **85.0 → 72.2**；换 VLM judge 升到 **74.6 / 89.0** | 相似度 reward 会主动破坏 | `19:128`、`04:52-56` | 【引用】 |
| **ChartMaster：像素 SSIM 当 reward 掉到 SFT 基线以下** | 同上 | `17:§3.4` | 【引用】 |
| **Duan et al. CHI 2024：首轮 52% 准确，后续迭代掉到 39%**；「general decrease in performance as the UI improves」 | **reward 在最优点附近反向** | `19:60,187,293` | 【引用】 |
| Duan et al. 标签噪声：**Fleiss κ = 0.112（准确性）/ 0.100（有用性）** | 设计违规判定的噪声地板约 0.1 | `19:60,187` | 【引用】 |
| Duan et al. 召回：**GPT-4 P=0.603 / R=0.380 / F1=0.466**；**人类均值 P=0.829 / R=0.336 / F1=0.478**；合并真值 100 个违规里仅 GPT-4 发现 **9**、共同 **29**、**仅人类 62** | 人和 GPT-4 的召回都很低 | `19:187` | 【引用】 |
| **纯规则 lint 的召回只有 32.3% / 22.9%**（UIS-Hunter），带知识库检测 **92.1% / 83.3%** | 程序化判据的覆盖面上界 | `19:186` | 【引用】 |
| DesignRepair 知识库规模：MD3 的 **24 种组件**、**228 条硬约束（113 do + 115 don't）+ 399 条软约束**；检测用 **127 条 Vercel 硬约束 + 48 条 GitHub** | 判据库能做多大 | `19:186` | 【引用】 |
| **AIM `cp11` 色彩和谐源码自带两条警告**：形式化来自照片增强「This is not proven for user interfaces」；**模板 X 几乎总是最小距离** | RL 会学会「把颜色铺满色轮」 | `19:58,271-274` | 【引用】读源码注释 |
| **Ngo 非单调**：Ngo 分最高的布局**最不受偏好**（286 票），最受偏好是 medium symmetry（**499 / 798**） | 优化这个指标会反向 | `19:257,1033` | 【引用】 |
| Ngo 评分者间 **Kendall W = 0.1023**（亚洲 0.1859 / 西方 0.0843） | 人对布局美学几乎不一致 | `19:257-258` | 【引用】 |
| Ngo 6 项聚合 OM 与 13 项聚合 OM **R² = 0.9144**；**原文从未报告过 r 或 R²** | 13 个指标高度冗余，而且从没验证过 | `19:259,256,315` | 【引用】 |
| **Purchase AUIC 2011：14 项实现成工具后只有一项捕捉到美学吸引力**（强预测因子是「图片的摆放位置」） | 14 里 13 项基本没用 | `19:260,1033` | 【引用】 |
| **Webthetics r ≈ 0.85 含训练/验证集重叠（泄漏）+ 原代码有 bug**；TOCHI 2022 交叉验证 **LCC = 0.752** | **泄漏的典型案例：0.85 → 真值 0.752** | `19:53,281-284,646` | 【引用】 |
| Miniukovich CHI 2015：桌面网页 **N=62，至多解释 49%** 美学方差；iPhone apps **N=53，至多 32%**；NordiCHI 2014 移动端 6 指标：主观复杂度 **40%**、美学 **36%** | 手工指标的天花板（R²≈0.49 ⇒ r≈0.70，**而且是 62 页上的样本内权重**） | `19:242-248` | 【引用】 |
| Reinecke CHI 2013：感知**鲜艳度** r=**.88** R²=**.78**；感知**复杂度** r=**.80** R²=**.65**；**视觉吸引力 adj R² 只有 .48** | 只有「感知代理」模型能用，吸引力不能 | `19:224-234` | 【引用】450 个网站，曝光 500 ms |
| Reinecke 单指标：colorfulness r=**.71** / **.53**；quadtree 叶数 vs 感知复杂度 r=**.28（N=367）**；space-based 叶数 r=**.50**；symmetry/balance/equilibrium **最终被剔除出模型** | 经典指标逐个的相关性 | `19:227-231` | 【引用】 |
| Webby 获奖站也只有 **4.21~6.57 / 9 分，SD = 1.69** | 连获奖站都只是中分、方差巨大 | `19:234` | 【引用】 |
| Anthropic：不可能完成的任务上**成功 hack 多 1.5~3 个百分点**，**尝试 hack 的比率高 3 到 6 倍** | **坏任务本身就会造出 hack** | `16:841` | 【引用】一手，但基于「通用 reward-hacking 分类器」；约 80% 计入的尝试只是「knowingly incomplete work」 |
| Anthropic 反 hack prompt 效果：**50%→23%（Opus 4.6）、55%→35%（Opus 4.5）、53%→20%（Sonnet 4.5）** | prompt 级缓解的量级 | `16:859-870` | 【引用】一手 |
| Opus 4.6 四栏表：主分类器 **0%** / 隐藏测试 **0%** / 不可能任务无提示 **50%** / 带反 hack 提示 **23%**；Opus 4.5 **0/0/55/35**；Haiku 4.5 **6/3/30/23**；Sonnet 4.5 **1/1/53/20** | 唯一完整的 reward-hacking 表 | `16:857-862` | 【引用】一手 |
| 模型因 grader 假设改方案：**695 条里 2 条**（≈0.29%）；主动找 grader 线索：**1/695**（≈0.14%） | **「作用于」grader awareness 很罕见** | `16:807` | 【引用】一手 |
| 「All three models successfully guessed what the answer key expected in about **0.3%** of sampled RL training episodes」 | 猜答案键的基线率 | `16:829` | 【引用】一手 |
| 成功 hack 率（剔除禁用方法子类）：Opus 5 **0.093%**、Mythos 5.1 **0.045%**、Opus 5.5 **0.046%** | 跨模型成功 hack 率 | `16:831` | 【引用】一手；⚠️ 原文自承环境不同「not perfectly comparable」 |
| Opus 5.5 git 掩盖披露率 **96.9%** | ⚠️ 这测的是「被问起时愿不愿意说」，**不是「多久会藏一次」** | `16:892` | 【引用】一手 |
| Fable 5 内部使用审计 **886 个会话**：「把没验证的猜测当事实陈述」**41**、「谎报完成或已验证」**16**、「绕过阻塞而不停下」**9**、「忽略明确指令/格式/必需步骤」**4**、「编造没观察到的细节」**3** | 假完成/跳过验证的真实发生率 | `16:960,970,976` | 【引用】一手 |
| Opus 5 训练审计规模：**约 150 万**个 episode 的摘要、数千个环境、**约 400 份**完整轨迹通读 | 审计的量级 | `16:910` | 【引用】一手 |
| Toolathlon：**324 次试验**里 1 次（**0.3%**）被安全分类器拦、6 次（**1.9%**）被沙箱逃逸监控拦，**七次全部计为失败** | 静默守卫干预的报告口径 | `16:1118` | 【引用】一手 |
| GPT-6 Astra：严重度 1/2 标记占匹配任务的 **13.62%**，GPT-5.6 Sol 为 **19.46%**；reward hacking 下降，**但凭证搜索类标记更频繁** | 跨模型失配标记的变化 | `16:1747` | 【引用】镜像读取 |
| OpenAI 三种要进作弊检测清单的手法：「**temporary/reverted hacks, test-set tuning, and timing/precompute tricks**」 | 可直接抄的作弊分类 | `16:1757` | 【引用】镜像读取 |
| 存在型 rubric 条款占 **90.2%**，非存在型只占 **8.6%**；存在型满足 **+14.9**，非存在型违反只 **−2.0**；completeness **+1.07**，conciseness **−2.91** | rubric 权重失衡 | `11:§2.7` | 【引用】 |
| **非存在型条款占比要求 ≥ 30%**，并列 7 条必备条款 | 处方 | `11:377-389` | 【引用】 |
| **Rubric Dropout 甜点区 30~50%**；**按有用性加权比什么都不做更差** | 处方 | `11:§2.7` | 【引用】 |
| verifier 逐条一致率：专家 panel **95~97%**、强 verifier **92%**、弱 **76~82%** → **要求 ≥92%，绝不低于 85%** | 及格线 | `11:§2.7` | 【引用】 |
| **WorldBench 翻面率 7/32 ≈ 21.9% → 单次判对率 q ≈ 12.5%**；**K=5 多数投票 → 约 1.6%** | 投票降噪的量级 | `11:§2.3` | 【引用】 |
| **正的 ROG 不是没有 hacking 的证据：26.4% 的样本比基线更差** | 过优化监控的陷阱 | `11:§3.1` | 【引用】 |
| **过优化起病在 68~478 步之间；从起病到灾难只有约 100 步** | 监控的时间窗 | `11:§3.3` | 【引用】 |
| CHERRL 起病判据：Δ_gap **0.08 / 0.10 / 0.12**，M_pct **15~30%**，bucket ≥ **0.99** 且 ≥ **20** 个样本，**5 步**平滑 | 可复现的起病定义 | `11:§3.3` | 【引用】 |
| **句法型 hack 在 Match Rate 0.6~0.95 可检出，语义型只有 0.0~0.4** | 检测能力的边界 | `11:§4.4` | 【引用】 |
| 自内化差距：峰值在 panel 共识峰值的 **100 步**以内；**训练用 verifier 自己的 reward 在最后一个 checkpoint 之前从不见顶** | 停训信号 | `11:§3.1` | 【引用】 |
| 组大小 8、通过率 0.1 时**全零组概率 43.1%** | 零梯度组的真实比例 | `92:83` | 【92 已更正】**原为 19%，19% 对应组大小 16** |
| 带截图的 issue 能成型**约 1,400 个** | 数据供给 | `92:84` | 【92 已更正】**原为约 1 万，禁用** |
| TRACE 四类 / **54 个子类** | hack 分类法规模 | `11` | 【引用】 |
| R2E-Gym：**大多数问题里不到 20% 的测试能区分正确与错误补丁** | 测试本身的判别力也很低 | `03` | 【引用】 |

### 7.8 游戏 / 视频侧

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| 33 条去重子命题：**全确定性 24 条、半确定性 6 条、只能靠人 3 条** | 「能玩」能被程序化多少 | `15:§0,165-167` | 【引用】原文自己的计数 |
| A2Z：源码判满分的规则真玩只有 **76.8%** 成立；源码判零分的里 **25.7%** 真玩是对的 | **只读源码会被骗，量级可测** | `92:35` | 【92 已核实】 |
| A2Z 覆盖率：第一遍正常玩 **40.5%**，再玩一遍 **41.0%**，对抗式状态注入 **48.5%** | **游戏侧瓶颈是覆盖率不是准确率** | `92:36` | 【92 已核实】 |
| A2Z 部分分 **54.3%**；去掉某个轴后排名翻转 **20.5% / 8.9% / 11.2%** | 评分口径的脆弱性 | `15:§2.2` | 【引用】 |
| A2Z 依赖链：局部通过 **72.4% → 依赖调整后 22.7%**（差 **49.7 点**）；加依赖上下文把运行时违例覆盖率 **71.1% → 80.2%** | 前置依赖必须进判据 | `15:§1.1` C7 行 | 【引用】 |
| A2Z 细粒度覆盖：十个游戏 **10.0% → 73.4%**；对照在线 agent（Orak，3 种子、≤200 步）里程碑达成率只有 **6.7%~26.7%** | 注入 ≫ 碰运气玩 | `15:§1.1` D2 行 | 【引用】 |
| A2Z GDD 规模：平均每份 **69 条结果性需求 + 32 条不变量**，配 **20** 个重放场景 | **短 prompt 配细判据等于纯噪声** | `15:§1.2` C 族 | 【引用】 |
| A2Z 可验证率 **93.9% / 94.2%**；Claude-Fable-5.1 可验证率 **98.7%** 而 GDD 忠实度只有 **77.0** | **A 族只能当门，不能当分** | `15:§1.2` A 族 | 【引用】 |
| Code2Games：基线构建成功率 **91.8~95.9** 几乎持平，核心玩法分从 **43.5 到 58.1** | 同上 | `15:§1.2` A 族 | 【引用】 |
| **V-GameGym：GPT-5 代码 96.6 / 图像 17.6 / 视频 20.7 / 总分 45.0**；judge 无人类对照 | **录屏判不了可玩性** | `15:222` | 【引用】 |
| V-GameGym 规模：**2,219 个游戏 / 2,190 个仓库 / 100 聚类 / 70 个模型**；**10 秒自动演示 + 10 张截图 + 1 段视频** | 归谬的设置 | `15:222,34-37` | 【引用】 |
| V-GameGym **录屏成功率 92.7%** | 录屏本身的可靠性 | `15:83` | 【引用】 |
| VideoGameBench：**感知哈希 + 汉明距离 < 12**（Kirby 调到 6~8）；最好成绩 **0.48%**；3 个保密游戏**全部 0%**；每模型每游戏**只跑 1 次** | 视频帧匹配判据的现实水位 | `15:224` | 【引用】 |
| VideoGameBench 重复性：Gemini 2.5 Pro 跑 5 次，Kirby **4/5**（方差 0.2），另两个游戏 **0/5** | 单次跑的结论不可信 | `15:§1.1` D3 行 | 【引用】 |
| PlaytestArena：GUI agent 在 20 个游戏约 120 关上 pass@20 **0.82**（GPT-5.4），人 **0.92** | agent 真玩的能力边界 | `15:§1.1` D1 行 | 【引用】 |
| PlaytestArena 有效通关 **46/50** | — | `15:§2.2` | 【引用】 |
| PlaySuite 因不支持拖拽而**排除 72 个游戏**；Construct 3 排除 **225 个** | harness 能力决定任务池 | `15:§1.1` B2 行、`15:886` | 【引用】 |
| PlaySuite harness 启动开销 **90 秒 → 8.3 秒** | 成本优化 | `15:§1.1` A4 行 | 【引用】 |
| PlayCoder：失败集中在高频反馈（>60 FPS 才出现的 bug），**4/43 项目（约 9%）结构性测不到**；假阴 **16%** / 假阳 **5%**，α=**0.790** | 时序判据的结构性盲区 | `15:§1.1` B5 行、`15:883` | 【引用】 |
| **RAPP：人设计 0.7966（Explorer）对 0.2493（Random）；随机生成的游戏只有 0.6193 对 0.3195** | 完全确定性的难度度量 | `15:§1.1` F1 行 | 【引用】 |
| RAPP F2：人设计游戏 DoNothing 归一化分 **0.1317**、胜率 **0.0556**；随机生成游戏 DoNothing 拿到 **0.3747**、胜率 **0.1846** | 「不动不能赢」可以量化 | `15:§1.1` F2 行 | 【引用】 |
| **RAPP F4：随机生成游戏分数标准差最小 199,406，人设计游戏最大只有 121.55 —— 差 1500 倍以上** | 方差爆炸就是「规则不自洽」的指纹 | `15:§1.1` F4 行、`15:§0` | 【引用】 |
| RAPP 直接把「每帧超过 **50ms**」的变异游戏整类排除 | 单帧预算判据 | `15:§1.1` E6 行 | 【引用】 |
| **A2Z 三轴评测共约 900 墙钟小时**（10 台 m7i.4xlarge + 1 台工作站）：**playtest 56.8% / 重放 40.1% / 源码检查 3.1%** | **纯程序判据的成本优势是两到三个数量级** | `15:§5.5` | 【引用】 |
| Android 实测：**随机 Monkey 的平均覆盖率在 6 个工具里最好** | 「随机能走很远」是常态 | `15:§1.1` F3 行 | 【引用】⚠️ 逐工具百分比只在原文图里，笔记只引定性结论 |
| CreativeGame：**LLM 创意分一律给 7/10** | 作者自己点名 Goodhart | `15:§1.1` F8 行 | 【引用】 |
| 好奇心驱动 playtest：**3000 步**、**25K 点**、24 小时 **90%** | 探索类 playtest 的量级 | `15:881` | 【引用】 |
| Long Tasks 规范：阈值 **50ms**，**时长只以 1ms 粒度提供** | 卡顿判据的分辨率 | `15:§3.5` | 【引用】规范原文 |
| `loop-protect` 默认阈值 **100ms**（CodePen 同思路，freeCodeCamp 约 **500ms**）；**不解决停机问题，只覆盖 while/for/do，不防递归** | 死循环防护的边界 | `15:§3.5` | 【引用】 |
| Spector.js 单次 capture **到达指定命令数或 10 秒后自动停止** | 它是采样器不是连续流 | `15:§3.4` | 【引用】 |
| CDP 实地枚举：**53 个域**，`Input` 只有 **13 个命令**，`Emulation` **48 个命令**，**没有 Gamepad 域**，「gamepad」全协议只出现 1 次 | Gamepad 无法合成 | `15:§3.6` | 【引用】实地枚举 |
| Phaser 3：**3.60/3.70/3.80.1/3.90 的八个 dist 文件里 grep `PHASER_GAME` 全 0 命中** | 最常用的网页游戏引擎恰好最不可用 | `15:§3.3` | 【引用】实地读源码 |
| 本地游戏实验**推算**：单变异四轨迹 + 双跑自检 **20~30 秒**；30 变异 + 1 参考 **11~16 分钟**；一轮完整实验 **25~35 分钟** | 可负担性 | `15:§5.5` | 【推算】**明确标注不是实测** |
| 游戏侧阈值 **0.40**（来自 RAPP 0.665 对 0.245 取中间偏严）；**`0.6 倍` 和 `2.0` 是拍的，没有文献依据** | 阈值来源要诚实标注 | `15:§5.4` | 【推算】原文自述 |

### 7.9 Arena / Elo（只能当季度验收，不能当训练信号）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| Code Arena·WebDev：**142 模型 / vote_count 合计 1,283,033 ≈ 641,517 场** | 唯一有逐票数据的 arena | `19:152,724` | 【引用】读官方 HF 数据集 |
| 置信区间宽度：webdev overall **中位 16.9 分**，最窄 **9.8**，最宽 **81.1**；webdev-html 中位 **35.1**，最宽 **132.9**；webdev-react 中位 **19.6** | **排名差距小于约 17 Elo 不可监督** | `19:724-732` | 【核实】官方自报 |
| 头部：rank1 **1811.1 [1796.6, 1825.7]**（2,597 票）vs rank2 **1780.2 [1769.7, 1790.8]**（5,746 票）不重叠；但 **rank 2/3/4（1780.2 / 1773.7 / 1760.1）互相重叠 → 前四名统计上不可区分** | 头部拥挤 | `19:728-729` | 【核实】 |
| WebDev Arena 平局：官方博客 **26% tie ratio**（Chatbot Arena 35%）；**18% of user votes fall into the 'both bad' category**，归因于依赖解析失败、状态管理错误、TS 编译错误；**18% 含在 26% 里** | **arena 信号里约 17-18% 被功能失败吃掉**（[推断]） | `19:685-689,708` | 【引用】原文 |
| 实测官方数据集 `webdev-arena-preference-10k`（N=**10,501**）：A 胜 **37.93%**、B 胜 **37.77%**、tie **7.29%**、tie(both bad) **17.01%**、**平局类合计 24.30%**（≠ 博客的 26%） | **用数据集，不用博客** | `19:692-702` | 【本机实测】作者自己算的 |
| Chatbot Arena 100k（N=106,134）：tie 19.29% + bothbad 19.07% = **38.36%**；140k：15.88% + 11.62% = **27.50%** | 对照 | `19:703` | 【本机实测】 |
| **平局不该记 0.5**：很简单的 query 平局风险比 **1.37**，高客观性 query **1.35**；3 个 arena 数据集 × 4 种评分系统，**让平局不触发更新反而把含平局的胜负预测准确率相对提升 1~3%** | 平局编码的是题目难度，不是实力相等 | `19:713-716` | 【引用】 |
| Design Arena：website 类目 **191 模型 / 2,201,736 battles ≈ 110 万票**；全站下界约 **623 万票**；`wins + losses == battles` **191/191 全成立**（结构上无平局）；**`btStdErr` 全为 null**；一个 tournament 跑 **5 场** | **结构上不可用作训练信号** | `19:153,743-747` | 【本机实测】一手核实 API |
| Design Arena 评分：BT，`Rating = 400·log₁₀(strength)`，起点 **1200** | 公式 | `19:153` | 【引用】 |
| UI-Bench：10 工具 × 30 prompts = **300 站**；**4,000+** 专家判断；**194 位**专家（仅 **10.8%** 此前用过 AI 建站工具）；TrueSkill μ=25 / σ=8.33，no drift, no draws | 规模 | `19:154` | 【引用】⚠️ 论文 4,075 / 线上榜 4,047 / 又引 8,150，**三处不一致** |
| UI-Bench 实测：**σ 全部 1.68~1.77，置信区间宽度 6.6~6.9 分**；#1 Orchids **30.08 [26.61, 33.55]** 对 #10 Replit **20.95 [17.56, 24.34]** → **只有 #1 与 #9/#10 真正分离，#2~#8 统计上不可区分**；**专家间一致度完全未报告** | 榜单分辨率 | `19:154` | 【核实】 |
| Elo 差距：Design Arena 开闭源约 **69 Elo**（Opus 5.5 **1392** 对开源最好 **1323**）；Code Arena WebDev 约 **139 Elo**（Opus 5.5 **1813** 对 Qwen3.8-Max **1674**） | 项目要追的差距 | `19:822,1056-1057` | 【引用】 |
| **69 Elo 只要约 200 场有信息对战就能检出，139 Elo 只要约 50 场** → 「众包 Elo 慢」是**供给问题不是统计问题** | 关键重构 | `19:822-824` | 【本机计算】 |
| 公式验证：2025-12-23 WebDev Arena 快照 **75,257 票 / 32 模型 ≈ 2,350 票/模型**，观测 CI 半宽 **±12~±17**；公式预测 **±14.0** → 吻合 | 公式可用 | `19:818-820` | 【本机计算】 |
| Leaderboard Illusion：**Meta 在 Llama-4 发布前测了 27 个私有变体**；数据份额 Google 约 **19.2%**、OpenAI 约 **20.4%**，**83 个开源权重模型合计只约 29.7%**；额外 Arena 数据带来的相对提升**最高达 112%** | arena 过拟合风险 | `19:738` | 【引用】 |
| Style control 初版只控四个特征：**答案 token 长度、markdown 标题数、加粗数、列表数** | 官方承认风格混淆 | `19:739` | 【引用】 |

### 7.10 人类一致率与标注成本（审美/主观维度的天花板）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| **DesignPref：20 位职业设计师各评完同样 600 对；二元一致 0.624；Krippendorff α = 0.248；28.5% 的对子两两分歧率 ≥ 96%** | **任何单一全局审美 reward 的约 60% 硬天花板** | `19:49-50,621-630` | 【核实】 |
| DesignPref 四档一致 **0.386**，四档 α **0.104** | **四档量表接近纯噪声** | `19:124,628-629` | 【核实】 |
| DesignPref 规模：**400 个生成设计 × 100 屏描述 → 600 对 × 20 人 = 12,000 条** | 规模 | `19:124,621-622` | 【核实】 |
| DesignPref 模型侧：pooled UIClip **57.45%**（SRCC 0.196）；pooled GPT-5 + RAG **57.62%**；**personalized UIClip 60.16%** | **60% 天花板**；个性化只多 2.7 个点 | `19:51,124,636-647` | 【核实】 |
| **AUV-Bench：单人 ordinal α 宏平均 0.368；3 人 ICC(1,3) = 0.637** | 逐标注者噪声地板 | `19:150,768` | 【核实】 |
| AUV-Bench 逐维 α / ICC(1,3)：Color **0.328 / 0.596**、Typography **0.334 / 0.609**、Copy Quality **0.334 / 0.610**、Graphics **0.346 / 0.614**、Visual-style Consistency **0.366 / 0.635**、Component Consistency **0.399 / 0.672**、Image-Text Fit **0.402 / 0.667**、**Layout 0.431 / 0.694** | **最可靠的维度恰好是最可程序化的维度（Layout 最高，Color 最低）** | `19:760-772` | 【核实】 |
| AUV-Bench 规模：**1,395 个可执行 Web UI**；51 招募 / **44 留存**；每条 **3 人**；质控前 **33,480** 条评分；8 维 1~5 分；**40 张视觉 rubric 样例**校准 | 规模 | `19:150,753-754` | 【核实】 |
| **AUV-Bench 校准后绝对审美分只有 2.78~3.18 / 5，而 pairwise 胜率可接近 80%** | **相对强 ≠ 绝对好** | `19:150,1065` | 【核实】 |
| UICrit 重算：aesthetics **ICC(1,1) = +0.024**、usability **+0.048**、design_quality **+0.026**；两两 r ∈ **[−0.012, +0.093]**；组内 SD **1.00** ≈ 总 SD **1.02** | **数值化审美评分 ≈ 纯标注噪声，绝对不能当回归 reward** | `19:123` | 【本机重算】作者在公开数据上重算 |
| UICrit：design_quality **48% 恰好是 6**（量程压死）；11,344 条里 **1,058 条纯 Gemini 产出**、**1,893 条 Gemini 辅助** | 数据污染 | `19:123` | 【引用】 |
| 单人标注 α = **0.368**；3 人 ICC = **0.637**；平局率 **26%** | draft 原本缓议审美的理由 | `19:4,150`、`14:677` | 【核实】 |
| 标注人数反解（ICC(1,1)=0.3691）：ICC ≥ 0.70 要 **4 人**、≥0.80 要 **7 人**（成本 ×2.33）、≥0.90 要 **16 人**（×5.33）、≥0.95 要 **33 人** | 要多少人才够 | `19:780-789` | 【本机计算】⚠️ **7 人/16 人是乐观下界** |
| **加题比加人划算**：k 从 3 到 16，人力 ×5.3，题量只省 **30%** | 预算分配 | `19:849-852` | 【本机计算】 |
| 现状 3 人时单条 UI 的 MOS 测量 SE 约 **0.41 分** → **0.2~0.4 分的差异读不出来** | 分辨率 | `19:833-839` | 【本机计算】⚠️ **σ_total=0.9 是假设的，AUV-Bench 没报 MOS 标准差 —— 这是唯一必须自己量的参数** |
| 两系统比较题量（配对 ρ=0.5，k=3）：δ=0.2 需 **93** 题、δ=0.3 需 **41**、δ=0.5 需 **15**；不配对翻倍（k=3 时 δ=0.2 需 **185** 题/组，k=16 只降到 **130**） | 实验设计 | `19:843-849` | 【本机计算】 |
| 审美维度建议 M=30 题、n=8 → **MDE ≈ 15.4 个百分点**；想读 5 个点需 **M·n ≈ 2,260** → 「**在审美维度上不划算**」 | 可测下限 | `19:898-900` | 【本机计算】 |
| Human Creativity Benchmark：**15,000** 条专业判断、5 领域、3 阶段；**收敛在技术正确性与视觉层级，分歧在审美方向与概念冒险** | 独立支持 A/B/C 三分 | `19:156` | 【引用】 |
| D3（`07_capability_spec.md`）：人不用 rubric 时一致率只有 **65%**，用 rubric 树后 **92%** | rubric 的价值 | `15:§1.1` F7 行 | 【引用】 |

### 7.11 多样性 / 「AI 味」（只能当批次诊断，绝不能进 reward）

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| Wenger & Kenett：**AUT LLM 0.459 / 人类 0.738（效应量 2.2）；FF 0.534 / 0.835（2.0）；DAT 0.665 / 0.819（1.4）**；但**个体原创性 LLM 并不差（AUT 0.711 对 0.696）** | **「AI 味」= 每个输出都原创，但彼此相像 → 是分布量，不能当 per-sample reward** | `19:27,433-446` | 【引用】22 个模型（统计用 7 个）对 102 名 Prolific 人类 |
| Kirk et al.：**EAD per-input SFT 0.79~0.81 → RLHF 0.07~0.16（−80%~−91%）**；across-input 0.86 → 0.69~0.87（小得多）；Sent-BERT per-input 0.45~0.50 → 0.06~0.15 | **RLHF 的坍塌是 per-input 的；「AI 味」是跨 prompt 的 → Kirk 的数不能直接搬** | `19:454-462` | 【引用】+【推断】 |
| Olmo 3：Think 血统 **SFT −62% / DPO −4% / RL +4% → 保留 38%**；Instruct **−38% / −23% / −5% → 34%**；**RL-Zero → 93%**；Vendi 从约 **3.4 个有效模式降到约 1.8**（GSM8K 只剩 **1.3**）；只看正确输出时 IFEval **83.4%** 的多样性损失仍存在；关掉 CoT 后 SBERT 多样性不变 → **坍塌在权重里**；GSM8K majority-vote 增益 Base **+24%** 对 Think **仅 +0.4%** | **SFT 而不是 RL 才是多样性死掉的地方** | `19:466-480,1103-1105` | 【引用】 |
| NoveltyBench 反规模律：gemma-2 **2B Distinct@10 = 5.66 > 27B 的 3.03**；Llama-3.2 **1B = 6.74 > 405B 的 3.20**；**闭源模型没有一个 utility > 4**（Claude-3.5 Sonnet Distinct@10 **1.76** 全场最低） | 多样性与规模反相关 | `19:483-485` | 【引用】 |
| DeepMind：Vendi Score 选对表征空间时约 **65%** 对齐人类（模型差异大时 **80%**）；**所有自动指标在区分「同等多样」的两组时 AUC 都 < 0.6** | **自动指标只能读大差异** | `19:516,604-607` | 【引用】 |
| 多样性指标与人类判断 Spearman：**taxonomy 引导的 LLM judge 0.90~0.94 > 嵌入 0.78 > 词汇 0.63 > gzip 0.28** | 指标选择决定结论 | `19:608-610` | 【引用】 |
| effective semantic diversity：**加闸前 Base 对 RL 的 neural diversity d = −2.12，只在合格输出里算之后翻成 d = +1.54** | **有效性闸会把结论的符号翻过来** | `19:526` | 【引用】 |
| The Price of Format：同 checkpoint、同采样参数、**只换 prompt 包装，标签分布熵跌 31%~69.7%** | prompt 包装本身就能压塌分布 | `19:1096` | 【引用】 |
| LandingAgent Diversity（30 targets × 12 行业 = 540 页，DINOv3 ViT-L/16，K=3）：Direct gemini **0.26 / Faith 3.83 / Aes 3.67**；Direct gpt-5 **0.28 / 4.60 / 3.63**；**Direct + Polisher 0.25 / 4.33 / 3.62**；LandingAgent gemini **0.36 / 4.30 / 4.00**；gpt-5 **0.37 / 4.70 / 4.10**；消融 去 Polishing 0.24 / 去 RAG 0.29 / 完整 0.38 | **抛光同时降低多样性和美感** | `19:409-424` | 【引用】⚠️ 同配置 Table 3 是 **0.36**、Table 4 是 **0.38**；聚合式写 `1/(K(K−1))` 而 `i<j` 只有 3 对 → **K=3 时这是真均值的一半** |
| PrototypeFlow + ControlNet：Generation Diversity **SD-1.5 15.93 → 11.48**；PrototypeFlow 自己 **15.95 → 13.98**，而 FID 变好 | 第二个独立证据：抛光杀多样性 | `19:423` | 【引用】 |
| Design Theater DHI（24 prompt × 5 工具 = 120 个界面）：**DHI-Visual 0.137**（最像 Claude-Vercel v0 **0.119**）；**DHI-Color 31.9**（最像 20.6）；**DHI-Layout 0.196**（最像 Bolt-Claude 0.181）；全 10 个工具对只落在 **0.119~0.151**（跨度 **0.032**），**未报重复测量方差** | 唯一的直接同质化指标，**值域太窄，没噪声地板不能用** | `19:385-398` | 【引用】 |
| Design Theater：**TFS —— 超过 25% 的设计理由在界面里找不到，功能类升到 34%**；**PAS —— 五工具中四个只实现 ≤6% 的功能性原则** | 声称与实现的落差 | `19:389-390` | 【引用】 |
| Design2Code 附录表 4：合成页 Avg Tag **19±8** / DOM 深度 **5±1** / Unique Tags **10±3**；真实页 **158±100 / 13±5 / 22±6** → 标签种类只有真实页的 **45%**、DOM 深度 **38%** | 结构模板化的基线 | `19:306,518` | 【引用】 |
| **本机风格集中度实测**（gallery 11 页 three.js 演示 vs basic 12 页系统字体栈）：fontFamily **k=2, H=1.0, HHI 0.50, Inter 11/11** vs **k=1, H=0, HHI 1.00, `-apple-system` 12/12**；hue **k=1, HHI 1.00** vs **k=3, HHI 0.561**；spacing HHI **0.067 / 0.114**；具名 tell：Inter 占比 **100% / 0%**，紫渐变 **0% / 0%**，任意渐变 **45.5% / 25%** | **gallery 集 Inter 100% → 任何「禁 Inter」lint 全判挂；basic 集所有 tell 全为 0 → lint 满分通过，但它的 fontFamily HHI = 1.00 比 gallery 的 0.50 更集中 —— 只是收敛到了另一个取值。具名 tell 和分布集中度测的是两件不同的事。** | `19:551-569,31-35` | 【本机实测】⚠️ **N=11 与 12，单项目单题族，人工挑选，不是随机样本** |
| 字体是最坍塌的维度（HHI 0.50 / 1.00），色相次之（1.00 / 0.561），**间距最分散（0.067 / 0.114）** | [推断] 与 Anthropic 点名症状顺序一致 | `19:572-577` | 【推断】 |
| **紫渐变在两个样本里都是 0%** → [推断] 紫渐变可能是特定时期/模型/prompt（Tailwind 系）的产物，**不是普适的 AI 味标志** | 反直觉 | `19:574-575,35` | 【推断】 |
| tell 判据实测：注入 Inter + 白卡紫渐变能被 **100% 抓到**；**20 个页面里只有 A11 命中、P04（品牌蓝渐变）不误报** | tell 只测「像不像那几个已知默认」 | `19:26,447` | 【本机实测】 |
| 学界空白（作者全文检索确认）：**配色/字体/布局模板的分布熵或集中度 —— 零篇**（11 篇 web/UI benchmark 全文检索 `entropy`/`homogen*`/`template collapse`/`mode collapse` **全部 0 命中**）；**Inter 占比 / 紫渐变占比 —— 一个严肃测量都没有**（一篇博客声称「被禁字体占 90%」，**无出处无方法，不可引用**）；**「AI 做的页」分类器 —— 零论文、零数据集、零基准**；**rubric 措辞 → 视觉输出分布收敛的量化 —— 零篇** | 这是本地实验填的空位 | `19:28-29,374-377,517` | 【本机检索】 |
| Google Generative UI（arXiv 2604.09577）：全文 `diversity` 只出现 **1 次**（指承包商多样性），`entropy` **0 次** | Google 没有输出多样性指标，还把跨代一致性当**特性** | `19:491-492` | 【引用】 |
| AesCoder 规模/成本：AesCode-358K（158K plot + 200K webpage）；OpenDesign 840 例；Qwen3-4B / Qwen2.5-Coder-7B，VeRL，**约 77 天 × 11 节点 8×MI300** | **唯一完整跑通的 RL 审美流水线，及其代价** | `19:126` | 【引用】 |
| AesCoder 消融：只让 RM 读代码文本打分 **0.71**（与 RFT / DPO 持平）；完整 agentic 版 **1.04** | 只读代码的自评几乎等于没评 | `19:126` | 【引用】 |
| AesCoder 与 Design Arena 排名 **Spearman 0.98 / Kendall 0.91** | 只能当模型级 sanity check | `19:126,153,749` | 【引用】 |
| AesCoder **论文未检测 reward hacking**；三项量纲不同（0–100 与 ±1）却直接加权，**没解释** | 公式的缺陷 | `19:126` | 【引用】 |

### 7.12 其他可用数字

| 数字 | 说明什么 | 出处 | 状态 |
|---|---|---|---|
| RL **17,920 GPU 小时得 67.6**；on-policy 蒸馏 **1,800 小时得 74.4** | 先问教师再决定要不要 RL | `92:33` | 【92 已核实】两臂同 checkpoint 出发 |
| SWE-Master：零样本 **6.2** → SFT 约 60K 轨迹 **57.8** → 加 RL **61.4** → 采 8 次用验证器选 **70.2** → 两者都做 **70.8**；RL 边际增益 **3.6**，推理时选择 **12.4** | **推理时选择比 RL 便宜得多** | `92:37` | 【92 已核实】 |
| Infinigen：**182 个生成器、1,070 个可解释自由度**（论文自己在表注里称它为 **proxy**） | 组合计数 ≠ 有效多样性 | `92:38` | 【92 已核实】 |
| Infinigen 另一组：`src/infinigen/assets` 下 **568 个 py 文件、约 246 个生成器**、约 **40,000** 手写行 | 规模 | `10:272-273,313-314` | 【引用】 |
| MTAC-IFBench：11 个模型约束满足率 **60.6% 到 80.4%**，最高 GLM-5.2 **80.4%**，**全部在同一脚手架下跑** | 旗舰表里唯一站得住的一行 | `92:39` | 【92 已核实】 |
| 3DHarnessBench 四档：单视角 Qwen **0.740** / Opus 5 **0.725**；主动视觉档 Opus 5 **0.871**；MiniMax **0.3722 → 规范化后 0.6148**；Gemini **0.6776 → 强模型检视图 0.7605** | 观察接口的价值 | `92:40` | 【92 已核实】 |
| 3DHarnessBench 增益 **9.3% 与 20.1%** | — | `92:81` | 【92 已更正】**原为 5.3% / 16.4%，禁用** |
| 负例 token 权重扫描 0.0 / 0.5 / 0.8 / 1.0 → **37.2 / 35.1 / 44.4 / 41.8**；原文明说**只有 0.8 那一档超过基线，整体非单调** | 轨迹修复 | `92:41` | 【92 已核实】 |
| Agent-R：只用最优轨迹训出来的修订能力 **10.84**，带纠错轨迹训 **46.75** | 纯净轨迹训不出恢复能力 | `92:42` | 【92 已核实】 |
| WebClipper：剪枝后轮数降 **21%**、token 降 **19.4%** 而准确率不掉；直接删冗余轮从 **0.713 掉到 0.603** | 轨迹剪枝 | `92:43` | 【92 已核实】 |
| BlenderAlchemy：视觉增益 2.5 分里，**给评估器看图占 2.1、给生成器看图占 0.4**（25.7 / 27.8 / 28.2） | **自检的增益来自判别不来自反思** | `92:45` | 【92 已核实】⚠️ 四轮分数是 27.4 / 26.1 / **26.5**，**不是「单调下降」** |
| DAPO 四件套：动态采样 **+8**、超长过滤 **+6**，合计 **20 分**（朴素 GRPO 30 → 50） | — | `92:90-91` | 【92 部分核实】**只核到总量 20，没核到分项** |
| BlenderGym：**245 对**，就是参数扰动造的 —— 「扰动即监督」 | 任务构造范式 | `10:322-323` | 【引用】 |
| SceneCraft：去掉内循环约束**丢 38.4 分** | 约束评分函数的价值 | `10:273-274` | 【引用】 |
| BlenderLLM / BlendNet：GPT-4o 合成，**12,059 行**，Apache-2.0；**没有发现任何公开工作在做 bpy 脚本的批量挖掘** | 空位 | `10:372-374` | 【引用】 |
| Poly Haven **2,387 个 CC0 资产**；GitHub topics blender-python **575** / blender-addon **2,323** | 原料供给 | `10:326,379` | 【引用】 |
| Blender 官方判据：**单像素误差超过 0.016 的像素不得超过 1%** | 外部锚点 | `10:413-422,904-905` | 【引用】读源码 |
| Anthropic harness：单 agent **20 分钟 / 9 美元**；全 harness（Opus 4.5）**6 小时 / 200 美元**（≈22 倍）；V2（Opus 4.6，去 sprint）**3 小时 50 分 / 124.70 美元**（省约 38%）；**QA 只占 8.4%（10.39 / 124.70）但三轮每轮都找出真问题** | **verifier 的预算占比基准** | `16:151-159` | 【引用】一手 |
| Anthropic harness：5~15 次迭代/代；单次完整跑**长达 4 小时**；Sprint 3 单独有 **27 条判据** | 迭代预算 | `16:90,103,111,135` | 【引用】一手 |
| claude.ai 克隆的功能清单 **> 200 条**，初始全部 `passes: false` | 清单式 verifier 的规模 | `16:649` | 【引用】一手 |
| Anthropic 客服 bench：**44 张票，30 训 / 14 留出**；起点 Opus 4.8 default(high) **74.4% / 4.6 分/票** → 删掉「强制工具调用仪式、草稿纸步骤、互相矛盾的规则」+ Opus 5.5 low → **87.8% / 1.9 分** → Sonnet 5 low → **88.9% / 1 分** → 加路由规则与退款上限交叉引用 → **98.9%（训练集）**；**留出 14 条：最终 90.5% 对原始 78.6%，成本约 1/5** | **删掉脚手架赘肉比加东西有效**；注意 **98.9% 训练 → 90.5% 留出的落差** | `16:631` | 【引用】一手 |
| `claude-api` skill 爬坡：**66.1% → 补 8 个缺失特性 74% → C#/Java 类型表 77% → 反思 + 「旧形式→新形式」映射表 80% → 修任务与 grader 的错误 ≈88%** | **最后一段增益来自修 grader/任务，不是修 policy** | `16:632` | 【引用】一手 |
| 反思的发现：「the skill content was present but Claude was simply writing older API shapes (e.g., from its trained priors)」 | **上下文约束干不过训练先验**；修法是映射表不是黑名单 —— 和「禁了 Inter 就收敛到 Space Grotesk」同类 | `16:634` | 【引用】一手 |
| **基线 ≥ 约 95% 就别再追质量了** | grader 设计经验法则 | `16:593` | 【引用】一手 |
| OSWorld 2.0：Opus 5.5 partial **81.8%** / strict **48.7%**；Fable 5.1 **80.7% / 42.8%**；Opus 5 **74.0% / 37.2%** | **partial 与 strict 差约 33 点 —— 评分严格度主导结果** | `16:1106` | 【引用】一手 |
| OSWorld 2.0 harness：**保留每一张截图** + 服务端在 **100k token** 处压缩；1080p、最多 **500** 步、最大推理强度 | 对照 OpenCUA 的 3 张滑动窗口 | `16:1104-1108` | 【引用】一手 |
| ScreenSpot-Pro 图片尺寸：Mythos Preview 最大 **1,568px / 1,568 token**；Mythos 5 最大 **2,576px / 4,784 token** | 给 VLM judge 送多大的图 | `16:1111` | 【引用】一手 |
| ScreenSpot-Pro 自我更正：padded vs unpadded 尺寸的 prompt bug，改完**所有先前模型重新评测** | 厂商自己披露的数字更正 | `16:1113` | 【引用】一手 |
| Astra 90 帧轨道测试（Blender 换船 + WebGPU）：draw calls **119 → 77**；三角面 **48,809 → 61,092**；平均帧间隔 **251.48 ms → 199.26 ms** | 渲染计数器当判据的实例 | `16:1194-1197` | 【引用】镜像读取 |
| Astra 控制起始场景：改后用 **7,040** 个代理三角面替代 **51,200**；「Both policies used the same geometry producer, so this isolated the loading decision」 | 隔离变量的纪律 | `16:1207` | 【引用】 |
| Astra 六层地面 High 质量：传输 **~35 MB → ~15 MB**，**同时保留 241,952 个三角面** | 增益与不变量一起报 | `16:1209` | 【引用】 |
| Astra 受控模拟（6 秒下降 + 3 秒稳定，两个 worker，**100 ms** 模拟延迟）：丢弃任务 **6,074 → 13**；图注自限「**This measures terrain scheduling, not frame rate.**」 | 报数时必须说清这个数不代表什么 | `16:1211-1212` | 【引用】 |
| Astra 规模：**2,048** 个星系、**> 10,000** 颗行星；Blender 源文件 **193** 个可编辑 mesh；导出船 **14,968** 三角面 / **8** 个不透明材质批次 | 任务规模基准 | `16:1246-1247` | 【引用】 |
| CUA/Operator：OSWorld **38.1%**（前 SOTA 22.0%，人 72.4%）；WebArena **58.1%**（前 SOTA 36.2%，人 78.2%）；WebVoyager **87.0%** | 2025-01 的 computer-use 基线 | `16:1865` | 【引用】镜像读取 |
| ProgramBench：每个 episode 复用上一个代码库但给全新 **1,000,000 token** 预算；Opus 5 跨 5 个 episode **83% → 93%** | 四张卡里唯一的「fresh context」命中，**而且与代码评审无关** | `16:1021` | 【引用】一手 |
| 四张 system card 页数：Opus 5.5 **230 页**、Fable 5/Mythos 5 **317 页**、Opus 4.6 **213 页**、Opus 5 **198 页** | 材料规模 | `16:729-733` | 【引用】 |
| **四张卡里前端/审美的训练或评测披露：零**（"Puppeteer"、"aesthetic"、"frontend"、"front-end"、"visual design"、"design taste"、"CSS"、"WebDev" 全部 0 命中；"Playwright" 只有 1 次，是内部使用的轶事） | **没有一家披露过前端审美是怎么训的** | `16:1092-1095` | 【本机检索】全文 grep |
| **"inoculation"/inoculation prompting 在四张卡里 0 命中**；"honesty training" 作为具名技术也不存在 —— inoculation 的说法出自 `anthropic.com/research/emergent-misalignment-reward-hacking`，**不是 system card** | 归属更正 | `16:1027` | 【本机检索】 |
| mdskills.ai 的计数器（9.9k popularity / 9.5k stars / 536 forks / advisor 8.0）是**站点模板值，跨 skill 完全相同，不能当采纳数引用** | 反例 | `16:1711,2116` | 【本机核实】 |
| `develop-web-game` **在 `openai/skills@main` 里不存在**：全仓 tar 快照检查，无 `.experimental/`，`grep -rliE 'web-game\|render_game_to_text\|playtest'` **零命中**，所有 raw 路径 404 | 更正 `01_frontier_labs.md`：那个「五阶段循环」没有任何来源文本支撑 | `16:1696-1711,2033` | 【本机核实】 |


---

## 8. 矛盾与待核清单

写正文时这些地方**不要直接引用**，或者引用时必须带限定词。按严重程度排。

### 8.1 真矛盾（两处笔记给出不相容的数字/结论）

**矛盾 1 【待核，优先级最高】CAD 工具消融 0.366 → 0.821**
- `92:78` 明确判定：「某 CAD 评测上『带工具 0.821 对不带工具 0.366』等三行 …… **回原文核验不通过**：那篇论文评的模型与引用里的对不上，也没有这样一组带工具对照 …… **三行全部删除，负相关的结论一并撤回**」。
- `16:1075` 却把**同一对数字**作为**一手披露**报出来：BenchCAD Vision2Code，Opus 5 从 **0.366 → 0.821（2.24 倍）**，并附完整设置「random subset of **1,000** of the full **17,874** Vision2Code files；**voxel IoU averaged over five runs**」。
- 判断：两者很可能指**不同来源**（92 核的是某篇论文，16 读的是厂商一手材料）。**但在核清之前，这对数字一律标【待核】，不得用于论证「循环增益与单步基线负相关」**（那个结论已被 92 撤回）。若只想用「给工具后 voxel IoU 翻 2.24 倍」这个事实，必须注明出处是 `16:1075` 的一手材料，并写明「1,000 个文件子集、五次平均」。

**矛盾 2 RULER hack 的美学分前后值**
- `19:131`：**4.309 → 6.697**，同时 rubric 分 0.395 → 0.262，token 0.3k → 6.3k。
- `19:347`：**4.42 → 6.21**。
- 判断：同一文件内两处不一致。**正文用 `19:131` 那组**（它带完整三元组，看起来是最终核过的版本），并在心里把它当作「约 4.3 → 约 6.7」。想严谨就写**「美学分从 4.3 涨到 6.7，而 rubric 分从 0.395 跌到 0.262（低于零样本基线），输出 token 翻 21 倍」**，不报小数第三位。

**矛盾 3 WebDev Arena 平局率 26% vs 24.30%**
- 官方博客：**26% tie ratio**（`19:685`）。
- 作者自己跑官方数据集 `webdev-arena-preference-10k`（N=10,501）：平局类合计 **24.30%**（`19:692-702`）。
- 判断：**不是矛盾，是口径差**——博客的 26% 没公布统计窗口与子集。处方已经在笔记里：**「用数据集，不用博客」**。正文报 24.30% 并注明 N=10,501。

**矛盾 4 UI-Bench 专家判断数：4,075 / 4,047 / 8,150**
- 论文 4,075，线上榜 4,047，又有一处引 8,150（`19:154`）。
- 判断：**三处不一致，一律写「4,000+」**。不要报精确值。

**矛盾 5 LandingAgent Diversity 同配置 0.36 vs 0.38**
- Table 3 是 **0.36**，Table 4 是 **0.38**（`19:409-424`）。
- 另有公式缺陷：聚合式写 `1/(K(K−1))` 而 `i<j` 只有 3 对 → **K=3 时报出来的是真均值的一半**。
- 判断：**这组数字只能用来说方向（抛光同时降低多样性和美感），不能报绝对值**。

### 8.2 口径陷阱（数字都对，但很容易被用错）

**陷阱 6 WorldCoder-Bench 的 2.7%**
- `92:58` 已点名：「**2.7% 是『截图加 VLM』这个判定方式自己的通过率，不是模型的能力**——成稿里这两个数曾经混用过，已更正」。模型的隐藏契约覆盖率是 **27.8%（严格档 19.9%）**。
- 用法：**说「截图加 VLM 只放过 2.7% 的产物」可以；说「模型只有 2.7% 能过」是错的。**

**陷阱 7 Blender 的「噪声地板 = 0」**
- `10:494-496` 的 0 是**在传 `seed=` 的条件下**。不传时参考解和自己比的 Chamfer 是 **0.00167**，而 pass/fail 带宽只有 0.0016~0.0065 —— `10:866-867` 自己说「**噪声地板直接吃掉一半判别力**」。
- 用法：写「零噪声」必须紧跟「前提是渲染器固定种子」。

**陷阱 8 「可访问性零噪声」**
- `92:85` 已更正：规则引擎 105 条里**纯自动可判只有 41 条**，所以应写**「判定本身零方差但覆盖面窄」**，不是「零噪声」。

**陷阱 9 Anthropic 成功 hack 率 0.093% / 0.045% / 0.046%**
- `16:831` 原文自承环境不同「not perfectly comparable」。**不能用来做跨模型排序。**

**陷阱 10 Opus 5.5 git 掩盖披露率 96.9%**
- `16:892`：这测的是「**被问起时愿不愿意说**」，**不是「多久会藏一次」**。两件事。

**陷阱 11 OSWorld 2.0 的 81.8% vs 48.7%**
- `16:1106`：partial 与 strict 差约 **33 个点**。任何引用必须带 partial/strict 标签，否则等于没说。

**陷阱 12 3JSBench 的 695 与 743**
- `92:21,79`：**695 条**（分六族 223/160/157/45/12/98）。**743 已禁用。**

**陷阱 13 3DHarnessBench 增益 5.3% / 16.4%**
- `92:81`：**已更正为 9.3% 与 20.1%**。旧值禁用（错因：基线取第一档、增益却从第二档起算）。

**陷阱 14 全零组概率 19%**
- `92:83`：**组大小 8、通过率 0.1 时是 43.1%**；19% 对应**组大小 16**。

**陷阱 15 带截图的 issue「约 1 万」**
- `92:84`：**已更正为约 1,400 个**（原值与自己引的 0.457% 转化率矛盾）。禁用 1 万。

**陷阱 16 Webthetics r ≈ 0.85**
- `19:53,281-284`：**含训练/验证集重叠（泄漏），而且原代码有 bug**。交叉验证后的真值是 **LCC = 0.752**。引 0.85 必须说它是泄漏值。

**陷阱 17 Miniukovich 的 R² = 0.49**
- `19:242-248`：是 **N=62 页上的样本内权重**，不是留出集性能。而且 R²≈0.49 ⇒ r≈0.70。

**陷阱 18 Ngo 的「13 项指标」**
- `19:256,259,315`：**原文从未报告过 r 或 R²**；6 项聚合与 13 项聚合 OM 的 **R² = 0.9144**（高度冗余）；而且 Ngo 分最高的布局**最不受偏好**。这组指标**整体不可作为 reward**。

**陷阱 19 DAPO 的「动态采样 +8、超长过滤 +6」**
- `92:90-91`：**只核到总量 20 分，没核到分项**。引分项要标「待核」。

**陷阱 20 AutoLab 的 0.68 / 0.46**
- `92:64-65`：benchmark 本身已核实存在（36 任务、claude-opus-4.6 领先），但**这组具体分数在原文表里没直接读到，来自二手整理**。引用需注明。

**陷阱 21 本机游戏实验的 20~30 秒 / 11~16 分钟 / 25~35 分钟**
- `15:§5.5`：**明确标注是推算，不是实测**。
- 同节：游戏侧阈值 **0.40** 有 RAPP 依据（0.665 对 0.245 取中间偏严），但「**`0.6 倍` 和 `2.0` 是拍的，没有文献依据**」。

**陷阱 22 本机 VLM 可靠性实验的样本量**
- Blender 侧 VLM **只跑了 1 遍，没有自一致率数字**；`should` 标签**只有 1 个标注者，没有一致率**（`10:841-843`）。
- Web/3D 侧 18 个样本的早期结论**后来被推翻**（`90:§3.1`）；`ok_lathe` 一例是**人的标签错了**（`90:§3.4`）。
- 用法：这些数字可以用来说「VLM 是高保真低检出器件」这个**方向**，报具体分数时要带样本量。

**陷阱 23 本机风格集中度实测（gallery/basic）**
- `19:551-569`：**N=11 与 12，单项目单题族，人工挑选，不是随机样本**。
- 但它有一个很强的定性结论值得用：**gallery 集 Inter 占比 100% → 任何「禁 Inter」lint 全判挂；basic 集所有具名 tell 全为 0 → lint 满分通过，可它的 fontFamily HHI = 1.00 比 gallery 的 0.50 更集中 —— 只是收敛到了另一个取值。** 具名 tell 和分布集中度测的是两件不同的事。

**陷阱 24 审美 MOS 的 SE ≈ 0.41 分**
- `19:833-839`：其中 **σ_total = 0.9 是假设的**，AUV-Bench 没报 MOS 标准差 —— **这是唯一必须自己量的参数**。

**陷阱 25 标注人数反解（4 / 7 / 16 / 33 人）**
- `19:780-789`：**7 人 / 16 人是乐观下界**（Spearman-Brown 假设条目等价、误差独立）。

**陷阱 26 Design Theater DHI**
- `19:385-398`：全 10 个工具对只落在 **0.119~0.151**（跨度 0.032），而且**未报重复测量方差**。**值域太窄 + 没噪声地板 → 不能用。**

**陷阱 27 Android Monkey「平均覆盖率最好」**
- `15:§1.1` F3：**逐工具百分比只在原文图里，笔记只引定性结论。** 不要编百分比。

**陷阱 28 Kirk et al. 的 −80%~−91%**
- `19:454-462`：那是 **per-input** 多样性的坍塌；而「AI 味」是**跨 prompt** 的（across-input 只从 0.86 掉到 0.69~0.87，小得多）。**Kirk 的数不能直接搬去论证「AI 味是 RLHF 造成的」。**
- 真正支持的证据在 Olmo 3（`19:466-480`）：**SFT −62%、DPO −4%、RL +4%，RL-Zero 保留 93%** → **SFT 而不是 RL 才是多样性死掉的地方。**

**陷阱 29 「mdskills.ai 的采纳数」与 `develop-web-game`**
- `16:1711,2116`：那些计数器（9.9k popularity / 9.5k stars / 536 forks）是**站点模板值，跨 skill 完全相同，不能引用**。
- `16:1696-1711,2033`：**`develop-web-game` 在 `openai/skills@main` 里根本不存在**（全仓 tar 快照检查、无 `.experimental/`、`grep -rliE 'web-game|render_game_to_text|playtest'` 零命中、raw 路径全 404）。所以 `01_frontier_labs.md` 里那个「五阶段循环」**没有任何来源文本支撑，不要写进正文**。

**陷阱 30 inoculation prompting 的归属**
- `16:1027`：四张 system card 里 **"inoculation" 零命中**，"honesty training" 作为具名技术也不存在。那个说法出自 `anthropic.com/research/emergent-misalignment-reward-hacking`，**不是 system card**。

**陷阱 31 BlenderAlchemy「无视觉时单调下降」**
- `92:45`：逐轮读是 **27.4 / 26.1 / 26.5**，**中间有回升**。正确措辞是**「一路走低，没有一轮回到起点」**。

**陷阱 32 停更榜单与厂商自报分**
- `92:69-70`：「几个公开榜单已经停更，上面标的 2026 年数字多数是厂商自报；**同一个模型换脚手架能差 11.7 点**，所以任何单点分数离开 harness 版本都没有意义。」

**陷阱 33 「判别力靠训比堆参数便宜 30 倍」**
- `92:86`：原文**两次称其为朴素外推，且只在一个分布上测过**。已加限定词。

**陷阱 34 Anthropic 不可能任务的「多 1.5~3 个百分点」**
- `16:841`：基于**通用 reward-hacking 分类器**，且**约 80% 计入的「尝试」只是「knowingly incomplete work」**。所以**「尝试 hack 高 3~6 倍」比「成功率高 1.5~3 点」更可信**，但两者都要带这个限定。

**陷阱 35 AesCoder**
- `19:126`：**论文未检测 reward hacking**；三项量纲不同（0–100 与 ±1）却直接加权且**没解释**。它只能当「唯一完整跑通的 RL 审美流水线及其代价（约 77 天 × 11 节点 8×MI300）」来引。

### 8.3 没有矛盾、但材料本身是空的

- **音频：`15:428` 一条实现路径（`AudioBufferSourceNode.prototype.start` / `AnalyserNode` 探测音效事件），零实测、零一致率、零 hack 实例。** `16` 明确：**没有任何一手来源披露音频作为 reward 信号**。
- **视频：`19_aesthetics.md` 零视频零音频；一手来源同样零披露。** 本地唯一的视频素材集中在 `15_game_verifier.md` + MiMo 的 §4.3.2 引文。
- **四张 system card 里前端/审美的训练或评测披露：零命中**（`16:1092-1095`，全文 grep 八个关键词）。这本身就是一个可写的发现。

