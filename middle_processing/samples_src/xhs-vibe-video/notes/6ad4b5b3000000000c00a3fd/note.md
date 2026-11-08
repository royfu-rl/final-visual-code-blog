# 用 Opus 5.5 搭了条短视频产线

- 作者：John Wayne　类型：normal　赞 219 / 藏 248 / 评 7
- 链接：https://www.xiaohongshu.com/explore/6ad4b5b3000000000c00a3fd?xsec_token=ABvwejsjldc9bIaf2J9wNRhuaMxywcFxceXebeRD3J9q8=&xsec_source=pc_search
- 命中关键词：Claude Code 做视频、Claude 口播视频、HyperFrames

这两天用 Claude Code 搭了一条短视频产线，模型是 Opus 5.5[哇R]
	
起因是我们的 App 要在 TikTok 每天出片，工作量超级大
一开始让 Claude 去操作剪映，MCP 和 computer use 支持很有限[暗中观察R]
很多数据是加密的，opus 5.5 看不到全局，又慢又容易出错，质量也不行
	
后来我们直接绕开了剪辑软件，口播、画面、标题、贴纸、转场、音效都写在一条时间线上自己实现[偷笑R][偷笑R]
	
几个关键点
	
1. 渲染用 HyperFrames，HeyGen 开源的
画面就是 HTML，动画用 GSAP，无头 Chrome 逐帧截图，FFmpeg 编码
	
2. 剪辑点挂在口播的词上
ElevenLabs 配音的接口会返回每个字的起止时间，说到哪个词，就在那一刻切镜头、弹贴纸、放音效
改了口播重新配音，画面自己跟着走，不用手动对轨
	
3. 审片也交给 Claude
渲染完自动出三张拼图，Opus 5.5 自己看图，七项打分，每项 8 分以上才交给我
	
4. 踩过的坑都让它写进 README
HDR 素材、关键帧太稀、动画不能用随机数，同一个坑不踩第二次
	
我现在只做三件事：提需求、看成片、反馈修改意见，剪辑软件一次都不用开
	
完整教程整理成了 PDF 放在附件里，直接下载就好[害羞R][害羞R]
#野生极客体验howto[话题]# #野生体验家howto[话题]# #vibecoding[话题]# #AI新手村[话题]# #AI教程[话题]#

## 图片
- images/0.jpg
- images/1.jpg
- images/2.jpg
- images/3.jpg
- images/4.jpg
- images/5.jpg

## 评论首屏
- monkey（赞 0）：严肃学习
- 湖新路程序员（赞 1）：让 Opus 给自己做的片打分，分数容易偏松，隔几条人眼抽查一下更稳
- 一只瑗瑗（赞 0）：大好人！！
- Exciting（赞 0）：产线搭起来好看，收尾的人呢
- momo（赞 0）：剪映官宣和codex合作集成了[doge]
- CoCo-PPT版本（赞 0）：👍

