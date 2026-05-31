# tools / 博客辅助脚本

> 说明:仓库根目录的 `README.md` 由 Gmeek 在每次构建时**自动覆盖生成**(里面是文章数、字数等统计),所以工具文档放在这里(`tools/README.md`),不会被冲掉。

## gmeek_html_wrap.py

把"整页 / 复杂 HTML"(公众号导出、AI 生成的带 `<style>`/`<script>`/卡片排版的页面)
转换成可直接粘贴进 GitHub Issue 的 **`Gmeek-html` 安全片段**,从而在 Gmeek 博客里
还原出完整排版。

### 为什么需要它

Gmeek 用 GitHub 官方 Markdown API(`mode=gfm`)渲染正文,会**净化 / 转义**裸 HTML 里的
`<style>`、`<script>`、行内 `style=` 等内容,导致排版变成纯文本。Gmeek 自带的 `Gmeek-html`
开关可以绕过:把 HTML 放进以 `Gmeek-html` 开头的代码块里,Gmeek 会反转义还原成真实 HTML。
本脚本自动完成"去外壳 + CSS 作用域化 + 中和残留 `<pre>` + 包进代码块"。

### 用法

```bash
# 结果打印到 stdout
python3 tools/gmeek_html_wrap.py 你的整页.html

# 写入文件,并自定义容器 class(作用域名)
python3 tools/gmeek_html_wrap.py 你的整页.html -o out.md --wrapper my-post
```

脚本做了什么:

1. 去掉 `<!DOCTYPE>` / `<html>` / `<head>` / `<body>` / `<title>` / `<meta>` 外壳;
2. 把 `<style>` 里的选择器收敛到唯一容器作用域(`body`/`html` → `.wrapper`,其余选择器加前缀),
   避免污染整页背景/字体或与博客模板类名冲突;
3. 追加中和规则,消除 `Gmeek-html` 反转义后残留的 `<pre>` 灰底等宽外壳;
4. 用 fenced 代码块 + `Gmeek-html` 包裹输出(保留换行,JS 里的 `//` 注释与 `<` 运算符安全)。

> 纯行内样式的公众号 `<section>` 内容无需额外作用域处理,脚本同样适用。

### 发布一篇复杂 HTML 文章的 5 步

1. **新建 issue**,填标题(标题 = 文章标题 + 网址拼音)。
2. 跑脚本得到成品 `out.md`,**全选复制**。
3. 在正文 **Write 标签**粘贴(别用 Preview 判断效果——那里只显示成代码块,属正常)。
4. **至少加 1 个 Label**。⚠️ Gmeek 会忽略没有标签的 issue,这是最常见的失败原因。
5. **Submit** → 仓库 Actions 等 "build Gmeek" 出绿勾(约 1~2 分钟)→ 刷新发布页查看。

### 重要前提

- 内容源头是 **GitHub Issue**,不是仓库文件。改 `backup/` 或 `docs/` 不会驱动线上更新,
  且会被下次构建覆盖。**要改文章,改对应 Issue 正文。**
- HTML 内不要出现连续三个反引号(会提前结束代码块)。

更详细的约定见 `.kiro/steering/gmeek-html-posts.md`。
