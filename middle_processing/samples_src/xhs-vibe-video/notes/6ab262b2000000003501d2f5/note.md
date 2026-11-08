# GAE：一个 Latent，同时生成视频与三维世界

- 作者：勇气号　类型：video　赞 128 / 藏 140 / 评 19　时长 92s
- 链接：https://www.xiaohongshu.com/explore/6ab262b2000000003501d2f5?xsec_token=AB0RCbAlT6e4Pnw6RLByXzFyF7HjOJ8Li-7mX5Y8iZ1I0=&xsec_source=pc_search
- 命中关键词：manim AI 动画

最近，我们和团队一起探索了在 representation space 中构建 VAE 的新可能，并基于这一思路，从零开始训练了一个 1B 参数模型，发布新工作：GAE（Geometry-Native Autoencoder）。
	
不同于以往基于 DINOv2 等单图语义编码器进行压缩，我们尝试利用预训练的 3D foundation model 构建 latent space，使其天然支持 RGB 与 geometry 的联合表达，为 world model 提供更具空间结构的生成基础。
	
GAE 的核心想法是：让生成模型直接在 geometry-native latent space中生成，再从同一个 latent state 中同时解码出 RGB 视频与三维几何，进而得到与画面对应的点云。
	
我们改变的不是模型最终输出什么，而是生成模型工作的内部表示：这个表示不仅包含外观信息，也天然承载空间与几何结构。视频中每组并排展示的 RGB 画面与点云，都来自同一个生成状态。
	
我们希望 GAE 能为“生成看得见的画面”与“生成具有空间结构的世界”提供一个共同的 foundation，让 world model 在生成视觉内容的同时，也能够生成可被理解和利用的三维世界。
	
- Code: [https://github.com/TencentARC/GAE](https://github.com/TencentARC/GAE)
- Project Page: [https://jiah-cloud.github.io/GAE.github.io/](https://jiah-cloud.github.io/GAE.github.io/)
- Paper: [https://arxiv.org/pdf/2609.24981](https://arxiv.org/pdf/2609.24981)
	
This is not 3D reconstruction—it is 3D-native generation: generating your video and your 3D world simultaneously.
#视频生成[话题]# #世界模型[话题]# #三维重建[话题]# #游戏ai[话题]# #世界生成[话题]#

## 图片
- images/0.jpg

## 评论首屏
- Chaos（赞 1）：和之前的gen3r区别是？
- 卷积神经网络（赞 0）：和之前oneworld的区别是？
- Leon-Redfield（赞 0）：这个工作做的好漂亮啊，有两个小问题，这个工作和VGGT类的工作有什么关系呢？另外就是我看视频里面动态的东西的点云都会保留，所以说这个工作是不是没有考虑时序表征对吗？
- Alex（赞 0）：这是你们的工作？
- Alex（赞 1）：我只能说有相同想法的真多呀[捂脸R]
- IMU炼丹侠（赞 0）：太优雅了
- 長青（赞 0）：如果只比重建能比过vggt omega吗
- 花花（赞 0）：能同时编码mesh或者voxel吗
- 小红领巾（赞 0）：带生成的VGGT
- U+vV（赞 0）：感觉是不是不好scale呀，而且是不是上限会被重建模型卡死，没法scale呀

