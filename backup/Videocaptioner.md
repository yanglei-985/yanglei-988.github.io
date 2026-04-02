现在只需要 打开一个文件夹然后shift+右键 进入powershell后 `git clone https://github.com/WEIFENG2333/VideoCaptioner.git`即可拿到文件。

安装完成之后，启动的方法跟一般的软件不太一样，

先cd进入你的文件夹，然后.\.venv\Scripts\Activate.ps1  最后videocaptioner

```
cd D:\字幕工具
.\.venv\Scripts\Activate.ps1
videocaptioner

```
还有一个卡点就是，api的设置，如何让它可以识别全部语言，我尝试了几个api站点，但是都没有办法上传储存太大的文件，以后遇到这些问题，直接去问claude（是claude，不是claude code，注意区分）。

注册地址：https://console.groq.com， 注册后生成 API Key，然后在 VideoCaptioner 里：

Base URL 填 https://api.groq.com/openai/v1
模型选 whisper-large-v3
