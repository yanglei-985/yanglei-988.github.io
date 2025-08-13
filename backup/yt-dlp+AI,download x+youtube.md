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

但是有的时候，我们会遇到无法下载youtube的情况，例如。

<img width="1319" height="87" alt="Image" src="https://github.com/user-attachments/assets/689a7c0a-07aa-4a52-8640-78202b9c9c3e" />
也就是youtube要验证我们是否为机器人，所以我们就需要给cookies给它，这个时候可以选择使用新的代码进行解析：

1. 完全退出 Chrome（包括后台进程）
   - 右下角任务栏 → 找到 Chrome 图标 → 右键 → 退出
   - 或者在任务管理器里结束所有 `chrome.exe` 进程。

2. 再运行：

   ```bash
   yt-dlp --cookies-from-browser chrome "https://www.youtube.com/watch?v=9BnUUtlQbFU（示例）"
   ```

3. 缺点：执行期间不能用 Chrome 看视频。

理解了上面的基础，我们继续进阶，关于批量下载视频。
1.在足够空间的地方创建一个文件夹，以及一个txt文件，文件的每一行是你需要的youtube链接，可以高达40多个（我的记录），批量下载，直接到你的文件夹里面。
`yt-dlp -a "D:\bruce\bruce.txt" --cookies-from-browser chrome`
例如我这个文件，引号就是txt文件的位置，然后再获取chrome关于youtube的cookie，yt-dlp就可以直接读取你的txt文件中
所包含的youtube链接了。


随着你使用的次数越多，你就会遇到更多的问题，而今天我遇到的问题就是，当你下载的次数过多了，会出现
` [youtube:tab] PLB043E64B8BE05FB7: Playlists that require authentication may not extract correctly without a successful webpage download. If you are not downloading private content, or your cookies are only for the first account and channel, pass "--extractor-args youtubetab:skip=authcheck" to skip this check`

`WARNING: [youtube] Unable to download webpage: HTTP Error 429: Too Many Requests (caused by <HTTPError 429: Too Many Requests>)`

前者是验证问题，后者是下载次数过多的问题，如何解决？我直接解决的方法就是问一下AI，然后结合yt-dlp的资料，它就给了我解答方法。

`yt-dlp -a "D:\bruce\bruce.txt" --cookies-from-browser chrome --extractor-args youtubetab:skip=authcheck`
这里多加了一个--extractor-args youtubetab:skip=authcheck

然后`yt-dlp -a "D:\bruce\bruce.txt" --cookies-from-browser chrome --extractor-args youtubetab:skip=authcheck --sleep-interval 5`
这个意在你每次下载完一个视频的时候，出现5秒的间隔，这个时间可以调整。以及可以通过切换ip地址来防止下载过量。
