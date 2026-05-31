# context.md — 在 Gmeek 博客发布"公众号/Obsidian 风格 HTML 文章"的完整上下文

> 用途:把这份文档交给任意 AI,它就能在没有前情的情况下,帮我把"带排版的 HTML 文章"正确发布到我的 Gmeek 博客上。

---

## 1. 我的博客是什么

- 框架 **Gmeek**:在 **GitHub Issues 里写正文** → GitHub Action 跑 `Gmeek.py` → 生成 `docs/*.html` → GitHub Pages。
- 仓库 `yanglei-985/yanglei-988.github.io`;线上 `https://www.ylletter.fun`。
- 构建触发:`issues`(新建/编辑)、每天定时、手动 dispatch。**git push 不触发构建。**

## 2. 目标

把 AI 生成的"宝玉风格/公众号风格"HTML(`<section>` + 行内 `style=` 卡片)发布到博客,排版要和 Obsidian 一致。

## 3. 核心约束

1. **内容源头是 GitHub Issue 正文**,不是仓库文件;改仓库文件会被下次构建覆盖。改文章 = 改 Issue。
2. **Gmeek 用 GitHub GFM API 渲染,会"清洗"裸 HTML**(删 `style=`/`<style>`/`<script>`/`<section>` 样式)→ 直接粘 HTML 会塌成乱码。
3. **每篇 Issue 必须 ≥1 个 Label**,否则不生成文章。
4. **Issue 的 Preview 标签 ≠ 最终效果**(显示成代码块属正常),只认发布后的页面。

## 4. 解决方法:`Gmeek-html` 代码块

把 HTML 放进以 `Gmeek-html` 开头的 fenced 代码块,Gmeek 会反转义还原成真实 HTML。公众号行内样式内容的标准套法(Issue 正文整体):

```
Gmeek-html<style>#postBody pre.notranslate{background:transparent!important;border:0!important;padding:0!important;margin:0!important;white-space:normal!important;font-family:inherit!important;line-height:inherit!important;overflow:visible!important;}</style><把你完整的 HTML 压缩成单行后放这里，不要有换行或缩进>
```

- 那行 `<style>` 必须有(中和 Gmeek-html 残留的 `<pre>` 外壳)。
- 用三反引号 fenced,别用单行内联反引号。
- **HTML 必须压缩成单行**:标签之间不要保留任何换行或缩进。

### ⚠️ 关键:为什么必须压缩 HTML

Gmeek-html 还原后,内容仍被套在一层 `<pre>` 里。`<pre>` 会**把空白字符(空格、缩进、空行)原样保留并渲染成可见字符**。如果你的 HTML 有多行缩进写法(尤其是嵌套 `<section>` 的段落),`<pre>` 会把那些缩进空格照单全收,页面后半段就开始出现数字、乱位、错行。`white-space:normal` 那条中和规则能减轻,但**最彻底、最保险的做法是把 HTML 压成单行**,根本不给 `<pre>` 留任何空白。

**压缩用一行 Python 即可**(去掉所有标签间空白):

```
python3 -c "import re;open('out.html','w',encoding='utf-8').write(re.sub(r'>\s+<','><',open('in.html',encoding='utf-8').read()))"
```

**压缩后,整个 Issue 正文应该是这样的 3 行结构**(开头 ```、中间 `Gmeek-html<style>…</style>` + 全部 HTML 挤成一行、结尾 ```):

```
Gmeek-html<style>…中和规则…</style><section …><h2>…</h2><p>…</p></section><section …>…</section>……全部在同一行……
```

> 仓库里的 `tools/gmeek_html_wrap.py` 已内置这步压缩,直接用它产出的成品就是压缩好的。

### 如果是"整页 HTML"(带 `<html><head><style>` 的完整文档)

需要额外:① 去掉 `<!DOCTYPE>/<html>/<head>/<body>/<title>/<meta>` 外壳;② 把 `<style>` 里的 `body{}` 改成 `.wrapper{}`、给选择器加 `.wrapper` 前缀、重命名会和模板冲突的类名(如 `.main-container`),整体包进一个 `<div class="wrapper">`。`tools/gmeek_html_wrap.py` 会自动做这些(并自动压缩)。

## 5. 最容易踩的坑(按踩坑概率排序)

1. **HTML 没压缩(最易忽略!)** → 残留 `<pre>` 把缩进/空行渲染成可见字符,页面后半段出现数字、乱位、错行。发布前务必把 HTML 压成单行。
2. **`<section>` 标签没闭合** → 线上出现"嵌套空框/套娃"。Obsidian 会自动补全缺失的 `</section>` 所以看着正常;但浏览器/Gmeek 不补,缺失的闭合会让卡片层层相互嵌套,变成一串空盒子。发布前务必校验 `<section>` 开/闭数量相等。
3. 漏写结尾的 ` ``` `(代码块没闭合)。
4. 忘了给 Issue 加 Label。
5. 只看了 Preview 标签就以为失败。

## 6. 发布前自检清单

1. **HTML 是否已压缩成单行**(标签间无换行/缩进)?
2. `<section>` 开标签数是否 == `</section>` 闭标签数?
3. (可选)用 GitHub markdown API(`POST https://api.github.com/markdown`,`mode=gfm`)渲染后,把 `<code class="notranslate">Gmeek-html(.*?)</code>` 用 `html.unescape` 还原,确认结果里是真实 `<section style=...>` 而不是 `&lt;section`,且整页标签平衡。

## 7. 仓库里已有的工具与文件(在分支 `fix/jichang-gmeek-html-render` / PR #50)

- `tools/gmeek_html_wrap.py`:把整页/复杂 HTML 一键转成 Gmeek-html 安全片段(去外壳 + CSS 作用域 + 中和 `<pre>` + **压缩单行** + 包代码块)。用法:`python3 tools/gmeek_html_wrap.py 输入.html -o out.md --wrapper 容器名`。
- `tools/README.md`:脚本说明。
- `.kiro/steering/gmeek-html-posts.md`:仓库写作规约。
- `drafts/*.src.html` 原始稿 / `drafts/*.gmeek.md` 已转换+压缩+校验过的成品。

## 8. 当前进度与待办

- **机场(Issue #6)**:已做好修复版,尚未粘回 Issue。
- **S31 = 「AI的黄金内容」= Issue #52**:之前发布版有未闭合 `<section>` + 未压缩,导致后半段乱。修复:用 `drafts/s31.gmeek.md`(已压缩、标签平衡)替换 Issue #52 正文。
- **会议整理 = 「AI是最好的杠杆」= Issue #51**:已正常发布。
- 短视频IP商业定位:成品在 `drafts/duan-shi-pin-ip-ding-wei.gmeek.md`,待发布。

## 9. 可直接发给下一个 AI 的提示词

> 我用 Gmeek(GitHub Issues→Pages)写博客,要发布公众号风格 `<section>`+行内 style 的 HTML 并保持排版。已知 Gmeek 走 GFM 会清洗裸 HTML,必须把 HTML 包进以 `Gmeek-html` 开头的 fenced 代码块(并加中和 `#postBody pre.notranslate` 的 `<style>`);内容写进 Issue 正文且至少加 1 个 Label;Preview 标签不代表最终效果。请按顺序:① 校验 `<section>` 开/闭是否相等(不等就补 `</section>`);② **把 HTML 压缩成单行**(去掉所有标签间的换行和缩进,如 `re.sub(r'>\s+<','><',html)`);③ 按上法包好并输出我可直接粘进 Issue 的整段内容。**特别注意:HTML 一定要压缩成单行,否则残留的 `<pre>` 会把缩进空白渲染成可见字符,导致文章后半段错乱——这是最容易被忽略的坑。**
