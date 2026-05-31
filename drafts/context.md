# context.md — 在 Gmeek 博客发布"公众号/Obsidian 风格 HTML 文章"的完整上下文

> 用途:把这份文档交给任意 AI,它就能在没有前情的情况下,帮我把"带排版的 HTML 文章"正确发布到我的 Gmeek 博客上。

---

## 1. 我的博客是什么

- 框架:**Gmeek**(开源,Meekdai/Gmeek)。写作方式是"**在 GitHub Issues 里写正文**"。
- 流程:GitHub Issue →(GitHub Action 跑 `Gmeek.py`)→ 生成 `docs/*.html` → GitHub Pages 部署。
- 仓库:`yanglei-985/yanglei-988.github.io`;线上域名:`https://www.ylletter.fun`(= GitHub Pages)。
- 触发构建的事件:`issues`(新建/编辑 issue)、每天定时 `schedule`、手动 `workflow_dispatch`。**`git push` 不触发构建**。

## 2. 我的目标

我用 AI 生成"**宝玉风格 / 公众号风格**"的 HTML(`<section>` + 大量**行内 `style=`** 的卡片排版),在 Obsidian 里预览很漂亮。我希望**发布到 Gmeek 博客后,排版和 Obsidian 一模一样**。

## 3. 核心机制与硬约束(务必理解)

1. **内容源头是 GitHub Issue 正文,不是仓库文件。** 每次构建都会从 Issue 重新生成页面;改 `backup/`、`docs/` 里的文件会被下次构建覆盖。**要改文章 = 改对应 Issue 的正文。**
2. **Gmeek 用 GitHub 官方 Markdown API(GFM)渲染正文,会"清洗"裸 HTML**:删掉 `style=`、`<style>`、`<script>`、`<section>` 的样式等。所以**直接把 HTML 粘进 Issue,排版会塌成纯文本/乱码**。
3. **每篇 Issue 必须至少有 1 个 Label**,否则 Gmeek 直接跳过、根本不生成文章。
4. **Issue 编辑器里的 "Preview" 标签 ≠ 最终效果**。Preview 用的是 GitHub 自带渲染,看 Gmeek-html 会显示成"代码块",这是正常的。**只有发布后的页面(ylletter.fun 上)才是真实效果。**

## 4. 解决方法:Gmeek 自带的 `Gmeek-html` 转义开关

把 HTML 放进一个**以 `Gmeek-html` 开头的 fenced 代码块**里。代码块内的内容 GFM 只转义不删除,Gmeek 在构建时会把它**反转义还原成真实 HTML** 注入页面,从而绕过清洗。

### 对"公众号行内样式 `<section>` 内容"的标准套法(最常用)

Issue 正文 = 下面这个整体(第一行 ```、最后一行 ``` 必须保留):

~~~text
```
Gmeek-html<style>#postBody pre.notranslate{background:transparent!important;border:0!important;padding:0!important;margin:0!important;white-space:normal!important;font-family:inherit!important;line-height:inherit!important;overflow:visible!important;}</style>
<这里粘贴你完整的 <section ...> ... </section> HTML，原样，不要改>
```
~~~

- 那行 `<style>…pre.notranslate…</style>` 是**必须的**:Gmeek-html 还原后会残留一层 `<pre>` 外壳(灰底、等宽、保留空白),这条规则把它中和掉。
- **用 fenced 代码块(三反引号),不要用单行内联反引号**:因为内联会把内容压成一行,破坏 JS 的 `//` 注释和 `<` 运算符。
- 行内样式内容**不需要**额外做 CSS 作用域处理。

### 如果是"整页 HTML"(带 `<html><head><style>` 的完整文档)

需要额外:① 去掉 `<!DOCTYPE>/<html>/<head>/<body>/<title>/<meta>` 外壳;② 把 `<style>` 里的 `body{}` 改成 `.wrapper{}`、给选择器加 `.wrapper` 前缀、重命名会和模板冲突的类名(如 `.main-container`),整体包进一个 `<div class="wrapper">`。仓库里有脚本自动做这些:`tools/gmeek_html_wrap.py`。

## 5. 最容易踩的坑(踩过)

- **`<section>` 标签没闭合 → 线上出现"嵌套空框/套娃"**。Obsidian 会自动补全缺失的 `</section>` 所以看着正常;但浏览器/Gmeek 不补,缺失的闭合会让卡片层层相互嵌套,变成一串空盒子。**发布前务必校验 `<section>` 开/闭数量相等。**
- 漏写结尾的 ` ``` `(代码块没闭合)。
- 忘了给 Issue 加 Label。
- 只看了 Preview 标签就以为失败。

## 6. 校验方法(发布前自检)

把"包好的整段"做这两项检查:
1. `<section>` 开标签数 == `</section>` 闭标签数(必须相等,差值=0)。
2. 可选:用 GitHub markdown API(`POST https://api.github.com/markdown`,`mode=gfm`)渲染后,把 `<code class="notranslate">Gmeek-html(.*?)</code>` 用 `html.unescape` 还原,确认结果里是真实 `<section style=...>` 而不是 `&lt;section`,且整页标签平衡。

## 7. 仓库里已有的工具与文件(在分支 `fix/jichang-gmeek-html-render` / PR #50)

- `tools/gmeek_html_wrap.py`:把整页/复杂 HTML 一键转成 Gmeek-html 安全片段(去外壳 + CSS 作用域 + 中和 `<pre>` + 包代码块)。用法:`python3 tools/gmeek_html_wrap.py 输入.html -o out.md --wrapper 容器名`。
- `tools/README.md`:脚本说明。
- `.kiro/steering/gmeek-html-posts.md`:仓库写作规约(原理+流程)。
- `drafts/*.src.html` 原始稿 / `drafts/*.gmeek.md` 已转换并校验过的成品。

## 8. 当前进度与待办

- **机场(Issue #6)**:已做好修复版 `backup/机场.md`,但**尚未粘回 Issue #6**(粘回并保存后才会上线)。
- **S31(标题「AI的黄金内容」= Issue #52,线上 `post/AI-de-huang-jin-nei-rong.html`)**:已发布,但**这一版有 17 个 `<section>` 没闭合(开 47 / 闭 30)**,导致结尾出现嵌套空框。修复:用平衡版 `drafts/s31.gmeek.md`(开/闭各 38,已校验)替换 Issue #52 的正文并保存。两版文字内容一致。
- 已正常发布、排版正确的:**Issue #51「AI是最好的杠杆」**(= 会议整理,29 section,渲染无误)。

## 9. 可直接发给下一个 AI 的提示词

> 我在用 Gmeek(GitHub Issues → GitHub Pages)写博客。我要把"公众号风格的 `<section>` + 行内 style HTML"发布上去并保持排版。已知:Gmeek 用 GitHub GFM API 渲染,会清洗裸 HTML,必须把 HTML 包进以 `Gmeek-html` 开头的 fenced 代码块(并加一条中和 `#postBody pre.notranslate` 的 `<style>`)才能还原成真实 HTML;内容必须写进 Issue 正文且至少加 1 个 Label;Issue 的 Preview 标签不代表最终效果。请:① 检查我给你的 HTML 的 `<section>` 开/闭标签是否相等(不等就补全 `</section>`,Obsidian 看着正常不代表平衡);② 按上面的套法把它包好;③ 输出我可直接粘进 Issue 的整段内容。
