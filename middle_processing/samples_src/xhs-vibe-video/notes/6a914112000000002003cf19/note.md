# Code-as-World：从一段视频逆推物理世界

- 作者：MirroS　类型：normal　赞 887 / 藏 635 / 评 7
- 链接：https://www.xiaohongshu.com/explore/6a914112000000002003cf19?xsec_token=ABRDFdkUaW6BKKbGXwCgBF444cggUps2b-b8Q0U3GLgD8=&xsec_source=pc_search
- 命中关键词：Motion Canvas

用 Code-as-World 探索 Physical RSI 的世界表征
	
视频生成模型越来越强。
但像素只是物理世界在某个时刻、某个视角下的投影。它告诉模型“看起来是什么样”，却没有直接说明：
世界里有什么、它们如何变化，以及变化为什么发生。
画面看起来合理，不等于背后的世界真的合理。
一个视频可以足够逼真，同时丢失物体身份、改变几何关系，甚至违背因果。
所以我们开始思考：
如果 Agent 要真正理解并推演物理世界，它需要的究竟是更多像素，还是一个能够执行、检验和修正的内部世界？
	
MirroS 的第一步，是 Code-as-World。
我们让 Agent 用代码描述三个问题：世界由什么构成、世界如何演化、这个世界如何被观测
代码写下的不是一段视觉描述，而是一个可以运行的世界。
Agent 先根据图像或视频提出假设，把假设写成程序；再执行模拟、渲染结果，与真实观测比较，并根据误差不断修改。
表征不是一次预测出来的，而是在 discovery loop 中被反复发现和验证的。
	
建立在这套表征之上，物理智能的 scaling 才刚刚开始：
物理推理，是对世界状态的构建与推演；
视频生成，是状态演化之后的视觉渲染；
具身交互，是在内部世界中模拟未来并选择行动。
真正需要积累的，或许不是更多彼此割裂的像素，而是能够被理解、执行和复用的结构化物理经验。
丰富描述世界的概念，修正推演世界的规律；
让已经理解的世界，成为探索下一个未知世界的起点。
	
#CodingAgent[话题]# #PhysicalAI[话题]# #WorldModel[话题]# #AGI[话题]# #RSI[话题]# #大模型[话题]# #世界模型[话题]# #物理AI[话题]#

## 图片
- images/0.jpg
- images/1.jpg
- images/2.jpg
- images/3.jpg
- images/4.jpg
- images/5.jpg
- images/6.jpg

## 评论首屏
- MirroS（赞 4）：项目主页：mirros-lab.github.io/code-as-world
论文：mirros.ai/report/code-as-world.pdf
代码：github.com/mirros-lab/code-as-world
全文 Blog : mirros.ai/blog/representing-physical-world
- 莫下河（赞 12）：composition：3D建模
Evolution：物理引擎
Appearance：rendering
本质还是渲染管线…
- 小红薯736890631（赞 1）：模拟器场景代码构建流程有计划开源吗？目前好像只有一个例子
- hooolly（赞 0）：猫猫那块，做个手机壳会很美
- 你找哪只unicorn（赞 0）：封面好美
- 小天狼星（赞 1）：[心心眼R][心心眼R][心心眼R]
- 皇上（赞 0）：）

