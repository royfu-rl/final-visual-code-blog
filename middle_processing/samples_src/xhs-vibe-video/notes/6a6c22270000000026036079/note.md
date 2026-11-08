# VideoCoCo：用代码让视频生成懂物理

- 作者：momo　类型：normal　赞 92 / 藏 97 / 评 8
- 链接：https://www.xiaohongshu.com/explore/6a6c22270000000026036079?xsec_token=ABs1L1dAbddN8-xmwO7DT7k3h2SgDDS9qMoWYBHb41T5w=&xsec_source=pc_search
- 命中关键词：Motion Canvas、代码生成视频

现在的视频生成模型，画面已经越来越逼真，但仔细一看，经常还是一种 “视觉高分，物理不及格” 的状态：
球可能反物理地滚动，物体碰撞后没有合理反馈，羽毛甚至比石头下落得更快。
原因在于，现有模型擅长模仿世界的“样子”，却不一定理解世界运行的“道理”。它学会了视觉模式，却没有真正掌握物体关系、运动规律和物理因果。
为了解决这个问题，我们提出了 VideoCoCo：把可执行的 Blender 代码作为视频生成过程中的 Code-as-CoT。
整个系统由两个 Agent 协作完成：
🧠 Coding Agent 负责理解 prompt、拆解场景和规划运动过程，并生成可执行的 Blender 代码；
🎬 Rendering Agent 负责执行和检查代码，先搭建一个符合物理规律的 3D 动态世界，再将它渲染成最终视频。
简单来说，模型不再直接“凭感觉画视频”，而是先通过代码把物体怎么运动、怎么碰撞、事件如何发展规划清楚，再进行视觉生成。因此，视频在物理一致性、可控性和时空连贯性上都能得到明显提升。
做这个系统时，我们得到的一个重要 insight 是：
可以把 reasoning、planning 和 memory 的压力交给 Agentic LLM，让 generation model 更专注地做好 pixel-to-pixel rendering。
最惊喜的是，即使完全不微调，只加入一份代码草稿，指标也能明显上涨。
这说明提升并不只是来自堆数据、堆模型或者堆训练，而是真正来自这条 “可执行的思维链”：它不只是告诉模型“应该怎么做”，还可以被运行、检查和纠错。
也许视频生成的下一步，不只是让画面看起来更真实，而是让模型先真正理解：这个世界应该如何运行。
📄 论文：VideoCoCo: Code-as-CoT for Physically-Consistent Video Generation via an Agentic Dual-Engine System
#视频生成[话题]# #AIGC[话题]# #Agent[话题]# #多模态[话题]# #生成式AI[话题]# #论文分享[话题]# #Blender[话题]#

## 图片
- images/0.jpg
- images/1.jpg
- images/2.jpg
- images/3.jpg
- images/4.jpg
- images/5.jpg

## 评论首屏
- 林风（赞 0）：这是挂了多少人[捂脸R]
- redflash（赞 0）：太强了
- 小梦AI大模型打卡（赞 0）：这里的图4（文章中Figure3）都是错的[笑哭R]
- None（赞 0）：[赞R][赞R]

