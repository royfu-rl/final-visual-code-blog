# 数据样例组件规范

给 2.2–2.4 里举例的来源做「数据样例」卡片：抓 2–6 条真实样本（2.4 Website 的来源统一 6 条），展示数据长什么样。
**抓不到样本的来源不做卡片**（未发布的、要申请的、只以几十 GB 分片发布的）——
表里的 Permitted 列已经写了原因，再渲染一张「取不到」的空卡没有信息。**不要编造样本。**

## 1. 取样本

- HuggingFace：`datasets-server` 的 rows 接口 2026-10-22 起全线 503，改走文件树
  - `https://huggingface.co/api/datasets/<id>/tree/main[/<子目录>]` 列文件
  - `https://huggingface.co/datasets/<id>/resolve/main/<path>` 下载，**必须带 `-L`**，否则拿到的是
    132 字节的 LFS 指针文件
- GitHub：`https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>`
- 网络：`export https_proxy=http://oversea-squid2.ko.txyun:11080`
- 样本挑「有代表性、画面完整」的；按文件大小取中位数附近那几个，别总拿第一条
- **不要下载整个数据集**

原始文件落 `middle_processing/samples_src/<slug>/`，不进 git 以外的地方。

## 2. 图片

- **原图放**：`assets/samples/<slug>/<原始文件名>`，长边 > 900px 等比缩小；不转格式、不裁剪、不铺底色（builder 里用 `raw()`）
- 3D 数据（网格 / 点云）不要放原始文件，放数据集自带的渲染图或缩略图；没有就只展示文本字段
- **不写任何说明文字**：卡片只放原图、原始文件名（`ds-meta`）、原始内容（`ds-code`，标题写文件名或字段名）；
  标题栏只放数据集链接。`strip()` 会把手写组件里的说明一并去掉

## 3. 组件

`scripts/build_samples.py` 里按数据集写一个 builder，产出
`middle_processing/samples/<slug>.html`。硬性要求：

1. **整个组件一行**，文件里不能有换行（markdown 遇空行会截断 HTML 块）
2. `<pre>` 内容按 `esc()` 转义：`& < >` 转实体、换行转 `&#10;`、`$`→`&#36;`、
   `~`→`&#126;`、`|`→`&#124;`，超过 60 行截断并注明原文行数
3. 图片路径写 `../assets/samples/<slug>/<n>.jpg`（相对 `web/`、`3d/` 等章节目录）
4. 纯文本 / 代码的数据集去掉 `<img>`，卡片只放 `ds-meta` + `ds-code`
5. 取不到样本的直接不写 builder、不写标记

## 4. 挂到正文

在 `parts/<chapter>/<view>.md` 里写标记，`scripts/gen_pages.py` 的 `fill_samples()` 会把连着的几条合成一面画廊：每条一个方块（封面 + logo、名称、机构、徽章、样例条数），点开弹出样例本体：

```
<!--SAMPLE:design2code|Design2Code-->
```

按表格里的行序排，抓不到的跳过；标记之间隔了正文就分成两面墙。

## 5. 自检

```bash
python3 scripts/build_samples.py          # 自带断言：组件不能有换行
python3 scripts/gen_pages.py              # 缺组件会打 [warn]
node --experimental-websocket scripts/shot.mjs '#web/verified' 'Design2Code · 数据样例' /tmp/x.png 1500 open
```

最后一条截图的是旧的折叠块，换成画廊后要先点开方块再截弹层（`.sg-body.open`），交付前必须看一眼。

