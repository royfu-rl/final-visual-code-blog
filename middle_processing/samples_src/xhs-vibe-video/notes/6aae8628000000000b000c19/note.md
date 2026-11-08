# VideoGen 大基本功之 Forcing

- 作者：Leo　类型：normal　赞 319 / 藏 504 / 评 22
- 链接：https://www.xiaohongshu.com/explore/6aae8628000000000b000c19?xsec_token=AB6_WBKkec9zc6O0CZoLDvozP-Suh5AsDbcRHfmTNUJsg=&xsec_source=pc_search
- 命中关键词：vibe video、视频 skill

整理了一篇视频生成技术笔记，串起 Diffusion Forcing、CausVid、Self Forcing、Rolling Forcing 和 Causal Forcing，看看扩散模型如何走向实时流式生成。尝试讲清少步蒸馏、分布对齐、滚动去噪与因果初始化分别解决什么问题，以及为什么“生成更快”不等于“长视频更稳”。
#视频生成[话题]# #计算机视觉[话题]# #从入门到精通[话题]#

## 图片
- images/0.jpg
- images/1.jpg
- images/2.jpg
- images/3.jpg
- images/4.jpg
- images/5.jpg
- images/6.jpg
- images/7.jpg

## 评论首屏
- 鸡排教教主（赞 0）：用什么写的呢
- Stream（赞 1）：有无pdf 分享谢谢[微笑R]
- Vincent教你学AI（赞 4）：Rolling diffusion 是第一篇，diffusion forcing 没 cite 他
- 门腔（赞 0）：最近出的CMD怎么样[doge]
- 好困（赞 0）：基本功
- 土豆🥔（赞 0）：大佬，forcing下一步的发展方向是什么？
- PaulLee（赞 0）：
- Junos.Z（赞 3）：可以看看我们最近的Self Gradient Forcing Plus:
Decoupling Gradient Flows for Autoregressive Video Generation，无需额外loss或者数据，无需长rollout训练，5s训练窗口即可产生24h流式视频生成[派对R]
- 北辰（赞 0）：关于将训练时限制注意力窗口，将最后的chunk看不到第一个chunk的方式纳入到训练中。请问这个思想是哪篇文章有提过呀。
- S-66🐰（赞 0）：nervous[微笑R] good luck to me

