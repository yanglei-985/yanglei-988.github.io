1.做任何事情之前，需要一个良好的网络，这里使用V2rayN,下载地址——https://v2rayn.info/  推荐版本为7.19.5 然后自由配置就好。
相关的教程——https://v2rayn.me/   如果没有一个合适的访问途径，只能通过其他社交软件分享zip压缩包。
https://www.wenshushu.cn/ 文叔叔传文件非常舒服

其他重点，1.运行的时候需要以管理员的身份运行，然后环境配置不要太乱，以默认的环境配置进行网络配置，不要改变系统代理，V4即可。注意windows版本，多数情况要打开tun模式。

2.Obsidian的下载地址——https://obsidian.md/
在此之前，我们优先选择使用chrome浏览器——https://www.google.cn/chrome/。

为使用这台电脑的任何人安装（所有用户）

装在 C:\Program Files\ 这需要管理员权限，所有用户账户都能用，其他程序调用时不会有权限隔离问题。

仅为我安装，装在 C:\Users\xx，不需要管理员权限，只有当前用户能用，但这会导致其他程序访问文件的时候，无法获取权限。

所以建议选所有用户，和 Program Files 装 codex 是同一个道理，权限更高、更稳定。

<img width="472" height="87" alt="Image" src="https://github.com/user-attachments/assets/59d5fa11-373e-4788-94fa-932b6ef2ea73" />
而你的仓库就可以随便创建了，放到桌面也可以。

https://github.com/YishenTu/claudian
下载releases里面的前三个文件，然后创建claudian插件。

https://github.com/kepano/obsidian-skills 五个skill,用claude就导入到.claude文件，codex则是.codex文件里。

3.node和npm的安装，对于在安装过程中，会遇到一些无法识别npm命令的情况，这时使用
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

这个过程之后，node和npm就已经下载好了。

