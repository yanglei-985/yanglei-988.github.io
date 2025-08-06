* 第一步——安装yt-dlp

windows

 ` 使用scoop安装（推荐）
scoop install yt-dlp`

`或使用pip安装
pip install yt-dlp`

macos

`使用brew安装
brew install yt-dlp`

`或使用pip安装
pip install yt-dlp`

注意，在安装的过程中，关闭vpn。

安装好后，我们要开始创建文件夹目录（make directory）`mkdir -p IELTS_Memory_Videos`

`mkdir：make directory 的缩写，用于创建文件夹。`

`-p：表示 “创建父目录”，如果路径中包含不存在的上级目录，也会一起创建，不会报错。`

`IELTS_Memory_Videos：要创建的文件夹名称。`
然后切换到这个目录中，我们需要把我们搜索下载的视频存放在这个文件夹当中。
`cd IELTS_Memory_Videos`
`cd：是 “change directory” 的缩写，用于切换当前工作目录。`

`IELTS_Memory_Videos：是你要进入的目标文件夹的名称。`
理解到这里之后，记住，每次我们要去下载新话题的时候，要重新打开cmd一次，然后它会自动创建新的文件夹。

<img width="1112" height="252" alt="Image" src="https://github.com/user-attachments/assets/3a3d4e08-06cd-47d4-b211-0ff0a04662f7" />

只需要输入这个指令就好
` yt-dlp "ytsearch5:IELTS speaking memory topic" `
引号是后面想要搜索的内容，search后面的数字是我们想要搜索下载的视频数量。

再来关于用yt-dlp下载x视频，其实也就是一个比较简答的指令。看图

<img width="1121" height="262" alt="Image" src="https://github.com/user-attachments/assets/bcb0dc29-09cf-46d3-99ac-50e79b2b6777" />
我们在使用引号的时候，注意使用英文的"，不要选用中文的括号和斜引号，注意，此方法不能下载涉黄和暴力视频。
