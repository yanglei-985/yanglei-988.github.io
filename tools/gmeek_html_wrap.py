#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gmeek_html_wrap.py — 把"整页/复杂 HTML"转换成可粘贴进 GitHub Issue 的
Gmeek-html 安全片段。

背景
----
Gmeek 用 GitHub 官方 Markdown API(mode=gfm)渲染正文,会净化/转义裸 HTML 里的
<style>/<script>/<title> 等标签,导致公众号式排版变成纯文本。Gmeek 内置的
`Gmeek-html` 开关可以绕过:把 HTML 放进以 `Gmeek-html` 开头的代码块里,Gmeek
会反转义还原成真实 HTML 注入页面(代码块内容只转义不删除,所以 <style>/<script>
都能保留)。

本脚本自动完成清理与防冲突:
  1. 去掉 <!DOCTYPE>/<html>/<head>/<body>/<title>/<meta> 外壳;
  2. 把所有 <style> 里的 CSS 选择器收敛到一个 .wrapper 作用域(body/html -> .wrapper),
     避免污染整页(背景/字体)与类名冲突;
  3. 追加一条中和规则,消除 Gmeek-html 反转义后残留的 <pre> 灰底等宽外壳;
  4. 用 fenced 代码块 + `Gmeek-html` 包裹输出(保留换行,JS 里的 // 注释与 < 运算符安全)。

用法
----
  python3 tools/gmeek_html_wrap.py 输入.html               # 结果打印到 stdout
  python3 tools/gmeek_html_wrap.py 输入.html -o 输出.md      # 写入文件
  python3 tools/gmeek_html_wrap.py 输入.html --wrapper my-post

随后把输出内容(整段,含首尾的 ```)粘贴进对应 GitHub Issue 的正文并保存,
Gmeek 重建后即生效。注意:Gmeek 的内容源头是 Issue,改仓库文件不会驱动线上更新。

限制
----
  * <script> 不做作用域处理(JS 本身无法自动 scope),原样保留;
  * @keyframes 动画名为全局,若多篇文章用同名动画可能互相影响,建议起独特名字;
  * 复杂选择器(如 `html body .x`)按"替换前导 html/body"的规则近似处理。
"""
import argparse
import re
import sys


# ----------------------------- CSS 作用域处理 ----------------------------- #
def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def _read_block(css: str, open_idx: int):
    """从 '{' 处读取,返回 (内部内容, 匹配 '}' 之后的下标)。"""
    depth = 0
    i = open_idx
    n = len(css)
    while i < n:
        c = css[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return css[open_idx + 1:i], i + 1
        i += 1
    return css[open_idx + 1:], n


def _split_top_level(s: str, sep: str):
    """在括号深度 0 处按 sep 切分(用于切分逗号分隔的选择器列表)。"""
    parts, depth, cur = [], 0, ""
    for c in s:
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        if c == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += c
    parts.append(cur)
    return parts


def _prefix_selector(sel: str, scope: str) -> str:
    sel = sel.strip()
    if not sel:
        return sel
    if sel in ("html", "body", ":root"):
        return scope
    # 前导 html/body 改写为 wrapper,例如 body.dark -> .wrapper.dark
    m = re.match(r"^(html|body)(?=[\s.#:\[>+~]|$)", sel)
    if m:
        rest = sel[m.end():]
        return (scope + rest).strip()
    return scope + " " + sel


# 进入并递归处理的条件 at-rule(其内部仍是普通规则)
_NESTED_AT = ("@media", "@supports", "@container", "@document")
# 内部不做选择器处理、原样保留的 at-rule
_RAW_AT = ("@keyframes", "@-webkit-keyframes", "@font-face", "@page",
           "@font-feature-values", "@property")


def scope_css(css: str, scope: str) -> str:
    css = _strip_comments(css)
    out = []
    i, n, prelude = 0, len(css), ""
    while i < n:
        c = css[i]
        if c == "{":
            body, j = _read_block(css, i)
            sel = prelude.strip()
            low = sel.lower()
            if low.startswith(_NESTED_AT):
                out.append("%s {\n%s\n}" % (sel, scope_css(body, scope)))
            elif low.startswith(_RAW_AT):
                out.append("%s {%s}" % (sel, body))
            elif sel.startswith("@"):
                out.append("%s {%s}" % (sel, body))
            else:
                selectors = [_prefix_selector(s, scope)
                             for s in _split_top_level(sel, ",") if s.strip()]
                out.append("%s {%s}" % (", ".join(selectors), body))
            prelude = ""
            i = j
        elif c == ";" and prelude.strip().startswith("@"):
            out.append(prelude.strip() + ";")  # @import / @charset 等
            prelude = ""
            i += 1
        else:
            prelude += c
            i += 1
    return "\n".join(out)


# ------------------------------- 主流程 --------------------------------- #
def extract_styles_and_body(html: str):
    styles = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.DOTALL | re.IGNORECASE)
    css = "\n".join(styles)

    m_body = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.DOTALL | re.IGNORECASE)
    if m_body:
        body = m_body.group(1)
    else:
        # 片段:去掉文档级外壳后作为 body
        body = html
        body = re.sub(r"<!DOCTYPE[^>]*>", "", body, flags=re.IGNORECASE)
        body = re.sub(r"</?html[^>]*>", "", body, flags=re.IGNORECASE)
        body = re.sub(r"<head[^>]*>.*?</head>", "", body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r"<title[^>]*>.*?</title>", "", body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r"<meta[^>]*>", "", body, flags=re.IGNORECASE)

    # body 内若仍混入 <style>(已被上面收集),移除它们以免重复
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
    return css, body.strip()


NEUTRALIZE_TMPL = (
    "/* fix: Gmeek-html 反转义后会残留一层 <pre>,这里中和它的灰底/等宽/空白保留 */\n"
    "#postBody pre.notranslate{background:transparent!important;border:0!important;"
    "padding:0!important;margin:0!important;white-space:normal!important;"
    "font-family:inherit!important;line-height:inherit!important;overflow:visible!important;}\n"
    "{scope},{scope} *{{box-sizing:border-box;}}"
)


def build_snippet(html: str, wrapper: str) -> str:
    scope = "." + wrapper
    css, body = extract_styles_and_body(html)
    scoped = scope_css(css, scope) if css.strip() else ""
    neutralize = NEUTRALIZE_TMPL.replace("{scope}", scope)
    style_block = "<style>\n%s\n%s\n</style>\n" % (scoped, neutralize)
    app = '<div class="%s">\n%s%s\n</div>' % (wrapper, style_block, body)
    return "```\nGmeek-html" + app + "\n```\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="把整页 HTML 转成 Gmeek-html 安全片段")
    p.add_argument("input", help="输入 HTML 文件路径")
    p.add_argument("-o", "--output", help="输出文件(默认打印到 stdout)")
    p.add_argument("--wrapper", default="gmeek-embed",
                   help="包裹容器的 class 名(作用域),默认 gmeek-embed")
    args = p.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as f:
        html = f.read()

    snippet = build_snippet(html, args.wrapper)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(snippet)
        sys.stderr.write("已写入 %s(%d 字符)\n" % (args.output, len(snippet)))
    else:
        sys.stdout.write(snippet)


if __name__ == "__main__":
    main()
