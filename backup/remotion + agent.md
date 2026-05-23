1.第一步骤是去github上面下载remotion的源码
2.观看大致操作视频https://www.youtube.com/watch?v=XB23PD8IZA0
3.https://www.youtube.com/watch?v=fB4uipaYYeU
4.别人怎么去用代码制作视频https://pathunfold.com/blog/claude-vibe-code-video

<img width="1012" height="405" alt="Image" src="https://github.com/user-attachments/assets/e0f095b8-93bd-4d1b-82d5-ec51a93b403c" />

4.里面有一些安装进程，比如选择project,就是安装到项目，global就是安装到全局。
然后它进入你的文件夹里面之后
`Copied to my-video.

Get started by running:
 cd my-video
 npm i
 npm run dev

To render a video, run:
 npx remotion render

Links to get you started:
 remotion.dev/docs
 remotion.dev/prompts
`

<img width="2278" height="1299" alt="Image" src="https://github.com/user-attachments/assets/5e9aeb97-4dae-4dec-aed2-ac20a6049d9b" />
这会让你进入remotion里面。
然后agent一段指令，它会直接做出来，例如。

> 在我的 Remotion 项目 ~/桌面/05_视频音频创作与转录/remotion/remotion/my-video 里，
创建一个30秒的教育解说视频组件，主题是「AI Agent 怎么运作」。

技术要求：
- 文件：src/AIAgent.tsx 作为主组件，在 src/Root.tsx 中注册
- 时长：30秒，30fps，共900帧，1920x1080
- 背景：#0A0F1E 深色，文字白色，重点色 #38BDF8 亮蓝色

5个场景，每场景6秒（180帧），用 <Sequence> 切换：

场景1（0-180帧）- 「感知输入」
- 标题：感知输入 Perception
- 文字：Agent 接收用户指令、网页、文件等外部信息
- 图示：从四角汇聚的箭头动画，中心是一个脑图标
- 入场：文字从下 translateY(40px) fade in

场景2（180-360帧）- 「思考规划」
- 标题：思考规划 Reasoning
- 文字：LLM 分析目标，拆解成可执行的子任务序列
- 图示：三个步骤节点从左到右依次出现，连线动画
- 重点词「LLM」用 #38BDF8 高亮

场景3（360-540帧）- 「调用工具」
- 标题：调用工具 Tool Use
- 文字：搜索网络、执行代码、读写文件、调用 API
- 图示：四个工具图标（🔍 💻 📁 🔌）依次弹出
- 每个图标有 scale 从0到1的弹性动画

场景4（540-720帧）- 「记忆存储」
- 标题：记忆存储 Memory
- 文字：短期记忆保存对话，长期记忆写入向量数据库
- 图示：两列对比，左侧闪烁的对话气泡，右侧稳定的数据库图标
- 用透明度区分短期（低）和长期（高）

场景5（720-900帧）- 「输出反馈」
- 标题：输出反馈 Output
- 文字：生成结果，评估质量，决定是否继续循环
- 图示：循环箭头动画，文字「Loop」沿路径旋转
- 结尾：所有场景缩略图同时出现，整体 fade out

动画规范：
- 所有动画用 interpolate() 和 spring() 实现
- 场景切换用 opacity interpolate(frame, [0,15], [0,1])
- 不要用任何外部图片，全部用 SVG 或 emoji + CSS 实现
- 字体用 Google Fonts Sora（标题）+ Noto Sans SC（中文）

完成后告诉我运行 npx remotion studio 预览的命令。