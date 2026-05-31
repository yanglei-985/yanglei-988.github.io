---
inclusion: always
---

# 在 Gmeek 博客里发布"复杂 HTML 排版"文章(公众号式)

本仓库是 **Gmeek** 驱动的博客:正文写在 **GitHub Issues** 里,GitHub Action
(`.github/workflows/Gmeek.yml`)调用 `Gmeek.py` 把 issue 正文转成 `docs/` 下的
静态 HTML,再由 GitHub Pages 部署。

## 核心约束(务必牢记)

1. **内容源头是 GitHub Issue,不是仓库文件。**
   每次构建都会从 issue 重新抓取正文 → 覆盖 `backup/<标题>.md` → 重新生成 `docs/`。
   定时构建(每天)还会先删空 `backup/` 与 `docs/` 再全量重建。
   **因此:直接改 `backup/*.md` 或 `docs/*.html` 不会持久,会被下次构建还原。
   真正要改的是对应的 Issue 正文。** 改仓库文件只适合做"可粘贴源 / 预览"。

2. **Gmeek 用 GitHub Markdown API(`mode=gfm`)渲染,会净化裸 HTML。**
   `<style>`、`<script>`、`<title>`、`<head>`、`<body>` 等标签会被转义成纯文本,
   所以直接把整页 HTML 贴进 issue,排版会失效(显示成 `&lt;style&gt;` 之类的代码文本)。

## 正确写法:`Gmeek-html` 代码块

Gmeek 内置一个转义开关(见 `Gmeek.py` 的 `createPostHtml`):凡是以 `Gmeek-html`
开头的代码块,Gmeek 会把其内容**反转义还原成真实 HTML** 注入页面。代码块内的内容
只会被转义、不会被删除,所以 `<style>` / `<script>` 都能完整保留。

在 issue 正文里这样写(注意 ` ``` ` 三引号代码块):

    ```
    Gmeek-html<div class="my-post">
      <style> .my-post h2{color:#07c160} </style>
      <h2>标题</h2>
      <p>正文……</p>
    </div>
    ```

### 必须遵守的几条规则

- **用 fenced 代码块(三引号),不要用单行内联反引号。**
  因为内联写法要求全部压成一行,会让 JS 里的 `//` 注释吞掉后续代码、并破坏 `<` 运算符。
  fenced 保留换行,JS / CSS 原样安全。
- **去掉文档外壳。** 不要包含 `<!DOCTYPE>`、`<html>`、`<head>`、`<body>`、`<title>`、
  `<meta>`;只保留"片段"。把内容整体包进一个**唯一的容器** `<div class="xxx">`。
- **CSS 必须收敛到容器作用域,避免污染整页:**
  - 把 `body { … }` 改成 `.xxx { … }`(否则会改写整站的背景/字体)。
  - 给所有选择器加上 `.xxx ` 前缀(或至少把会与模板冲突的类名,如 `.main-container`,
    作用域化 / 改名)。Gmeek 模板自身用到 `#header`/`#content`/`#postBody`/`.main-container`
    等,裸类名/裸标签选择器会互相干扰。
- **中和残留的 `<pre>`。** fenced + Gmeek-html 反转义后,会残留一层
  `<pre class="notranslate">` 包裹(灰底、等宽字体、保留空白)。在 `<style>` 里加:

      #postBody pre.notranslate{background:transparent!important;border:0!important;
      padding:0!important;margin:0!important;white-space:normal!important;
      font-family:inherit!important;line-height:inherit!important;overflow:visible!important;}

- `@keyframes` 动画名是**全局**的,多篇文章用同名动画会相互影响,建议起独特名字。

## 推荐:用脚本自动转换

仓库提供了 `tools/gmeek_html_wrap.py`,自动完成"去外壳 + CSS 作用域化 + 中和 `<pre>`
+ 包进 Gmeek-html 代码块":

    # 结果打印到 stdout
    python3 tools/gmeek_html_wrap.py 你的整页.html

    # 写入文件,并自定义容器 class(作用域)
    python3 tools/gmeek_html_wrap.py 你的整页.html -o out.md --wrapper my-post

然后把 `out.md` 的**全部内容**(含首尾的 ` ``` `)粘贴进对应 GitHub Issue 正文并保存。

## 发布 / 修复一篇复杂 HTML 文章的标准流程

1. 准备好整页 HTML(公众号导出、AI 生成等)。
2. 跑 `tools/gmeek_html_wrap.py` 得到安全片段。
3. 打开对应 GitHub Issue,**用片段替换原正文,保存**(新建文章则新开一个 issue)。
4. 保存会触发 Action 重建,等 1~2 分钟,线上页面即生效。
5. (可选)本地 / 分支预览:可用 `https://htmlpreview.github.io/?<raw 文件 URL>`
   直接渲染 `docs/post/*.html` 查看效果,但**这一步不改变线上**——线上只认 issue。

## 替代方案:整页独立 HTML 直接放 docs/

若是不需要进文章列表的完整独立页(纯静态展示页),也可以把 `.html` 直接放进
`docs/`(或子目录),GitHub Pages 会原样提供、零净化。缺点是不进 Gmeek 的文章管理,
需手动加链接,且同样要注意会被定时全量重建影响(放在 `static/` 目录可被 Gmeek 复制保留)。
