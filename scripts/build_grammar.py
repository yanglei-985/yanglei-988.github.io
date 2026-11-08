#!/usr/bin/env python3
"""Build the grammar feature page: content/grammar.md -> static/grammar/index.html

The article text is rendered exactly as written; this script only adds the
page shell around it: illustrations (scripts/grammar_figures.py), a sticky
table of contents, in-page search with keyword chips, and an "ask AI" panel
that hands the question to Gemini / Google AI Mode / DeepSeek.

Gmeek copies static/ into docs/, so the page is served at <site>/grammar/.
Re-run after editing the article or the figures:

    pip install markdown
    python3 scripts/build_grammar.py
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grammar_figures import FIGURES  # noqa: E402

SRC = ROOT / "content" / "grammar.md"
OUT = ROOT / "static" / "grammar" / "index.html"
THEME = ROOT / "templates" / "theme.css"
CONFIG = ROOT / "config.json"

# Terms offered as one-click searches; each must appear in the article.
KEYWORDS = [
    "名词性成分", "形容词性成分", "副词性成分", "修饰关系", "介词短语", "主谓宾定状补", "补语", "系动词",
    "五种基本句型", "连词", "名词性从句", "同位语从句", "形式主语", "先行词", "关系代词", "关系副词",
    "whose", "限制性", "非限制性", "状语从句", "让步", "不定式", "动名词", "分词", "逻辑主语",
    "悬垂分词", "独立主格", "句末重心", "非谓语动词",
]


def insert_figures(lines):
    """Return article lines with <figure> blocks after their anchor lines."""
    hits = []
    for anchor, caption, fn in FIGURES:
        idx = [i for i, line in enumerate(lines) if line == anchor]
        if len(idx) != 1:
            raise SystemExit("figure anchor must match exactly one line: %r (found %d)" % (anchor, len(idx)))
        hits.append((idx[0], caption, fn))
    hits.sort(key=lambda h: h[0])
    after = {}
    for num, (i, caption, fn) in enumerate(hits, 1):
        after[i] = (
            '<figure class="gm-fig" id="fig-%d"><div class="gm-fig-scroll">%s</div>'
            '<figcaption><span>图 %d</span>%s</figcaption></figure>' % (num, fn(), num, html.escape(caption))
        )
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if i in after:
            out.extend(["", after[i], ""])
    return out, len(hits)


def build():
    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")
    title = lines[0].lstrip("# ").strip()
    body_lines, fig_count = insert_figures(lines[1:])

    md = markdown.Markdown(
        extensions=["tables", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "1-3"}},
    )
    article = md.convert("\n".join(body_lines))
    article = re.sub(r"<table>", '<div class="gm-table"><table>', article)
    article = article.replace("</table>", "</table></div>")

    # TOC from the article's own headings (skip the article's in-text 课程目录 list heading)
    toc_items = []
    for tok in md.toc_tokens:
        stack = [tok]
        while stack:
            t = stack.pop(0)
            if t["name"] != "课程目录":
                toc_items.append((t["level"], t["id"], html.unescape(t["name"])))
            stack[0:0] = t["children"]
    chapters = sum(1 for lv, _, _ in toc_items if lv == 1)
    sections = sum(1 for lv, _, n in toc_items if lv == 2 and re.match(r"\d+\.\d+", n))
    toc_html = []
    for level, hid, name in toc_items:
        toc_html.append('<li class="lv%d"><a href="#%s" data-id="%s">%s</a></li>' % (level, hid, hid, html.escape(name)))

    plain = re.sub(r"[#>*`|\-\s]", "", text)
    words = len(plain)
    missing = [k for k in KEYWORDS if k not in text]
    if missing:
        raise SystemExit("keywords not found in article: %s" % missing)

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    theme_css = THEME.read_text(encoding="utf-8")

    page = (TEMPLATE
            .replace("%%TITLE%%", html.escape(title))
            .replace("%%SITE%%", html.escape(config.get("title", "")))
            .replace("%%SUB%%", html.escape(config.get("subTitle", "")))
            .replace("%%AVATAR%%", html.escape(config.get("avatarUrl", "")))
            .replace("%%THEME_CSS%%", theme_css)
            .replace("%%TOC%%", "\n".join(toc_html))
            .replace("%%KEYWORDS%%", "".join('<button type="button" class="gm-kw">%s</button>' % html.escape(k) for k in KEYWORDS))
            .replace("%%STATS%%", "约 %.1f 万字 · %d 章 %d 节 · %d 张图解" % (words / 10000.0, chapters, sections, fig_count))
            .replace("%%ARTICLE%%", article))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print("wrote %s (%d figures, %d toc entries, %d chars)" % (OUT.relative_to(ROOT), fig_count, len(toc_items), words))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" data-color-mode="light" data-light-theme="light" data-dark-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>%%TITLE%% · %%SITE%%</title>
<meta name="description" content="核心专题：%%TITLE%%。词性即成分、简单句、从句、非谓语动词，配图解、目录、搜索与 AI 问答。">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:type" content="article">
<link rel="icon" href="%%AVATAR%%">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,700;1,9..144,500&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+SC:wght@600;700;900&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<script>
  (function(){var t="light";try{t=localStorage.getItem("meek_theme")||"light";}catch(e){}document.documentElement.setAttribute("data-color-mode",t);})();
</script>
<style>
%%THEME_CSS%%

/* ===================== grammar feature page ===================== */
html[data-color-mode][data-light-theme] {
  --g-n: #2f6b55; --g-n-bg: #dfeae3;
  --g-a: #96701c; --g-a-bg: #f3e8c8;
  --g-d: #3b5b84; --g-d-bg: #dde6f1;
  --g-v: #a4482b; --g-v-bg: #f4e0d7;
}
html[data-color-mode="dark"][data-dark-theme] {
  --g-n: #8cc4ad; --g-n-bg: #1d3029;
  --g-a: #dcb862; --g-a-bg: #352b18;
  --g-d: #9fbbe0; --g-d-bg: #1d2836;
  --g-v: #e59a80; --g-v-bg: #3a241c;
}
@media (prefers-color-scheme: dark) {
  html[data-color-mode="auto"][data-dark-theme] {
    --g-n: #8cc4ad; --g-n-bg: #1d3029;
    --g-a: #dcb862; --g-a-bg: #352b18;
    --g-d: #9fbbe0; --g-d-bg: #1d2836;
    --g-v: #e59a80; --g-v-bg: #3a241c;
  }
}
html { scroll-behavior: smooth; scroll-padding-top: 84px; }
.gm-progress { position: fixed; top: 0; left: 0; height: 3px; width: 0; background: var(--accent); z-index: 40; }

.gm-hero { border-bottom: 1px solid var(--line); }
.gm-hero .wrap { max-width: 1240px; padding-top: 64px; padding-bottom: 44px; }
.gm-hero h1 { margin: 16px 0 0; font-family: var(--font-serif); font-weight: 900; font-size: clamp(34px, 5.6vw, 64px); line-height: 1.12; color: var(--ink); max-width: 15em; }
.gm-hero h1 .mark { padding: 0 .04em; }
.gm-hero-meta { display: flex; flex-wrap: wrap; gap: 8px 22px; margin-top: 22px; font-family: var(--font-mono); font-size: 12.5px; color: var(--muted); }
.gm-legend { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 22px; }
.gm-legend span { display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 12px; border-radius: 999px; font-size: 13px; border: 1px solid; }
.lg-n { color: var(--g-n); background: var(--g-n-bg); border-color: var(--g-n); }
.lg-a { color: var(--g-a); background: var(--g-a-bg); border-color: var(--g-a); }
.lg-d { color: var(--g-d); background: var(--g-d-bg); border-color: var(--g-d); }
.lg-v { color: var(--g-v); background: var(--g-v-bg); border-color: var(--g-v); }

.gm-shell { max-width: 1240px; margin: 0 auto; padding: 40px 32px 0; display: grid; grid-template-columns: 270px minmax(0, 1fr); gap: 56px; }
.gm-side { position: sticky; top: 84px; align-self: start; max-height: calc(100vh - 100px); overflow: auto; padding-bottom: 24px; scrollbar-width: thin; }
.gm-side-title { font-family: var(--font-mono); font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin: 22px 0 10px; }
.gm-search { display: flex; align-items: center; border: 1px solid var(--line-2); border-radius: 4px; background: var(--paper-2); }
.gm-search:focus-within { border-color: var(--accent); }
.gm-search svg { width: 15px; height: 15px; margin-left: 10px; flex: none; fill: none; stroke: var(--muted); stroke-width: 1.6; }
.gm-search input { flex: 1; min-width: 0; height: 40px; padding: 0 8px; border: 0; outline: 0; background: transparent; color: var(--ink); font-size: 14.5px; }
.gm-search-bar { display: none; align-items: center; justify-content: space-between; margin-top: 8px; font-family: var(--font-mono); font-size: 12px; color: var(--muted); }
.gm-search-bar.on { display: flex; }
.gm-search-bar button { height: 26px; min-width: 30px; padding: 0 8px; border: 1px solid var(--line-2); border-radius: 3px; background: transparent; color: var(--ink); cursor: pointer; }
.gm-search-bar button:hover { border-color: var(--accent); color: var(--accent); }
.gm-results { list-style: none; margin: 8px 0 0; padding: 0; max-height: 260px; overflow: auto; border-top: 1px solid var(--line); }
.gm-results li button { display: block; width: 100%; text-align: left; padding: 8px 2px; border: 0; border-bottom: 1px solid var(--line); background: transparent; color: var(--ink-2); font-size: 13px; line-height: 1.5; cursor: pointer; }
.gm-results li button small { display: block; font-family: var(--font-mono); font-size: 10.5px; color: var(--muted); letter-spacing: .04em; }
.gm-results li button:hover { color: var(--accent); }
.gm-results mark { background: var(--marker); color: inherit; padding: 0 1px; }
.gm-kws { display: flex; flex-wrap: wrap; gap: 6px; }
.gm-kw { height: 28px; padding: 0 10px; border: 1px solid var(--line-2); border-radius: 999px; background: transparent; color: var(--ink-2); font-size: 12.5px; cursor: pointer; }
.gm-kw:hover, .gm-kw.on { border-color: var(--accent); color: var(--accent); }
.gm-toc { list-style: none; margin: 0; padding: 0; border-left: 1px solid var(--line); }
.gm-toc a { display: block; padding: 4px 0 4px 14px; margin-left: -1px; border-left: 2px solid transparent; color: var(--ink-2); font-size: 13.5px; line-height: 1.45; }
.gm-toc .lv1 a { margin-top: 10px; font-family: var(--font-serif); font-weight: 700; font-size: 14.5px; color: var(--ink); }
.gm-toc .lv3 { display: none; }
.gm-toc .lv3 a { padding-left: 28px; font-size: 12.5px; color: var(--muted); }
.gm-toc .lv3.show { display: block; }
.gm-toc a:hover { color: var(--accent); }
.gm-toc a.active { color: var(--accent); border-left-color: var(--accent); }

.gm-article { min-width: 0; max-width: 760px; font-size: 16.5px; line-height: 1.9; color: var(--ink); }
.gm-article h1, .gm-article h2, .gm-article h3 { font-family: var(--font-serif); color: var(--ink); line-height: 1.35; scroll-margin-top: 84px; }
.gm-article h1 { font-size: 32px; font-weight: 900; margin: 2.4em 0 .6em; padding-top: .8em; border-top: 1px solid var(--ink); }
.gm-article h2 { font-size: 24px; font-weight: 800; margin: 2em 0 .6em; padding-bottom: .3em; border-bottom: 1px solid var(--line); }
.gm-article h3 { font-size: 19px; font-weight: 700; margin: 1.8em 0 .5em; }
.gm-article p { margin: .8em 0; }
.gm-article ul, .gm-article ol { padding-left: 1.5em; margin: .7em 0; }
.gm-article li { margin: .25em 0; }
.gm-article li > ul, .gm-article li > ol { margin: .2em 0; }
.gm-article strong { color: var(--ink); }
.gm-article em { color: var(--accent); font-style: normal; border-bottom: 1px dotted color-mix(in srgb, var(--accent) 50%, transparent); }
.gm-article blockquote { margin: 1.2em 0; padding: .8em 1.2em; border-left: 3px solid var(--accent); background: var(--paper-2); color: var(--ink-2); border-radius: 0 4px 4px 0; }
.gm-article blockquote p { margin: .3em 0; }
.gm-article hr { border: 0; height: 1px; background: var(--line); margin: 3em 0; }
.gm-article code { font-family: var(--font-mono); font-size: .86em; background: var(--paper-3); padding: .1em .35em; border-radius: 3px; }
.gm-table { overflow-x: auto; margin: 1.2em 0; border: 1px solid var(--line); border-radius: 4px; }
.gm-article table { width: 100%; border-collapse: collapse; font-size: 14.5px; line-height: 1.6; }
.gm-article th, .gm-article td { padding: 9px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.gm-article th { background: var(--paper-3); font-weight: 700; white-space: nowrap; }
.gm-article tr:last-child td { border-bottom: 0; }
.gm-article tbody tr:nth-child(2n) { background: var(--paper-2); }
mark.gm-hit { background: var(--marker); color: inherit; border-radius: 2px; }
mark.gm-hit.cur { background: var(--gold); color: var(--paper); }

/* figures */
.gm-fig { margin: 2em 0; padding: 18px 18px 12px; background: var(--paper-2); border: 1px solid var(--line); border-radius: 6px; }
.gm-fig-scroll { overflow-x: auto; }
.gm-fig svg { display: block; width: 100%; height: auto; min-width: 540px; }
.gm-fig figcaption { margin-top: 12px; font-size: 13px; color: var(--muted); }
.gm-fig figcaption span { font-family: var(--font-mono); font-size: 11.5px; letter-spacing: .1em; color: var(--accent); margin-right: 10px; }
.gm-fig text { font-family: var(--font-sans); font-size: 15px; fill: var(--ink); }
.gm-fig .ten { font-family: "Fraunces", Georgia, "Times New Roman", serif; }
.gm-fig .tb { font-weight: 700; }
.gm-fig .ts { font-size: 12.5px; fill: var(--muted); }
.gm-fig .tsm { fill: var(--ink-2); }
.gm-fig .tk { font-family: var(--font-mono); font-size: 12px; letter-spacing: .08em; fill: var(--accent); }
.gm-fig .tcode { font-family: var(--font-mono); font-size: 16px; font-weight: 700; fill: var(--ink); }
.gm-fig .tbig { font-size: 26px; fill: var(--muted); }
.gm-fig .box { stroke-width: 1.4; }
.gm-fig .n { fill: var(--g-n-bg); stroke: var(--g-n); } .gm-fig .tn { fill: var(--g-n); }
.gm-fig .a { fill: var(--g-a-bg); stroke: var(--g-a); } .gm-fig .ta { fill: var(--g-a); }
.gm-fig .d { fill: var(--g-d-bg); stroke: var(--g-d); } .gm-fig .td { fill: var(--g-d); }
.gm-fig .v { fill: var(--g-v-bg); stroke: var(--g-v); } .gm-fig .tv { fill: var(--g-v); }
.gm-fig .neu { fill: var(--paper); stroke: var(--line-2); } .gm-fig .tneu, .gm-fig .tink { fill: var(--ink); }
.gm-fig .hl { fill: var(--paper); stroke: var(--accent); stroke-width: 2; } .gm-fig .thl, .gm-fig .tacc { fill: var(--accent); }
.gm-fig .hdr { fill: var(--accent); } .gm-fig .thdr { fill: var(--accent-ink); }
.gm-fig .ln { fill: none; stroke: var(--muted); stroke-width: 1.4; }
.gm-fig .dash { stroke-dasharray: 4 4; stroke: var(--accent); }
.gm-fig .ahead { fill: var(--muted); }
.gm-fig .sep { stroke: var(--line); stroke-width: 1; }

/* ask AI */
.gm-ask-fab { position: fixed; right: 24px; bottom: 24px; z-index: 30; display: inline-flex; align-items: center; gap: 8px; height: 48px; padding: 0 20px; border: 0; border-radius: 999px; background: var(--accent); color: var(--accent-ink); font-size: 15px; font-weight: 700; box-shadow: 0 10px 28px -12px rgba(0,0,0,.45); cursor: pointer; }
.gm-ask-fab:hover { background: var(--accent-2); }
.gm-sel-btn { position: absolute; z-index: 35; display: none; height: 32px; padding: 0 12px; border: 0; border-radius: 4px; background: var(--ink); color: var(--paper); font-size: 13px; cursor: pointer; box-shadow: var(--shadow); }
.gm-scrim { position: fixed; inset: 0; z-index: 45; background: rgba(0,0,0,.28); opacity: 0; pointer-events: none; transition: opacity .2s ease; }
.gm-scrim.on { opacity: 1; pointer-events: auto; }
.gm-drawer { position: fixed; top: 0; bottom: 0; z-index: 50; width: min(420px, 100vw); background: var(--paper); border-color: var(--line); box-shadow: var(--shadow); transition: transform .25s ease; overflow: auto; }
.gm-ask { right: 0; border-left: 1px solid var(--line); transform: translateX(105%); }
.gm-ask.on { transform: none; }
.gm-drawer-head { position: sticky; top: 0; z-index: 2; display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; background: var(--paper); border-bottom: 1px solid var(--line); }
.gm-drawer-head b { font-family: var(--font-serif); font-size: 19px; }
.gm-x { width: 34px; height: 34px; border: 0; border-radius: 50%; background: transparent; color: var(--ink-2); font-size: 20px; cursor: pointer; }
.gm-x:hover { background: var(--paper-3); }
.gm-ask-body { padding: 18px 20px 28px; }
.gm-ask-ctx { padding: 12px 14px; background: var(--paper-2); border: 1px solid var(--line); border-radius: 4px; font-size: 13px; color: var(--ink-2); }
.gm-ask-ctx .lbl { font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .12em; color: var(--muted); text-transform: uppercase; }
.gm-ask-ctx .val { margin-top: 4px; font-weight: 700; color: var(--ink); }
.gm-ask-ctx .quote { margin-top: 6px; max-height: 84px; overflow: hidden; color: var(--muted); font-size: 12.5px; line-height: 1.6; }
.gm-ask-ctx label { display: flex; align-items: center; gap: 6px; margin-top: 8px; font-size: 12.5px; color: var(--muted); cursor: pointer; }
.gm-quick { display: flex; flex-wrap: wrap; gap: 6px; margin: 16px 0 10px; }
.gm-quick button { height: 30px; padding: 0 11px; border: 1px solid var(--line-2); border-radius: 999px; background: transparent; color: var(--ink-2); font-size: 12.5px; cursor: pointer; }
.gm-quick button:hover { border-color: var(--accent); color: var(--accent); }
.gm-ask textarea { width: 100%; min-height: 110px; padding: 12px; border: 1px solid var(--line-2); border-radius: 4px; background: var(--paper-2); color: var(--ink); font: inherit; font-size: 15px; line-height: 1.6; resize: vertical; outline: 0; }
.gm-ask textarea:focus { border-color: var(--accent); }
.gm-prov { display: grid; gap: 8px; margin-top: 14px; }
.gm-prov button { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 2px 10px; padding: 12px 14px; border: 1px solid var(--line-2); border-radius: 4px; background: var(--paper); color: var(--ink); text-align: left; cursor: pointer; }
.gm-prov button b { font-size: 15px; }
.gm-prov button small { grid-column: 1 / -1; font-size: 12px; color: var(--muted); line-height: 1.5; }
.gm-prov button em { font-style: normal; font-family: var(--font-mono); font-size: 10.5px; color: var(--accent); border: 1px solid var(--accent); border-radius: 999px; padding: 1px 8px; }
.gm-prov button:hover { border-color: var(--accent); }
.gm-prov button.primary { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 8%, var(--paper)); }
.gm-ask-note { margin-top: 14px; font-size: 12px; line-height: 1.7; color: var(--muted); }
.gm-ask details { margin-top: 12px; font-size: 12.5px; color: var(--muted); }
.gm-ask details pre { white-space: pre-wrap; max-height: 220px; overflow: auto; padding: 10px; background: var(--paper-2); border: 1px solid var(--line); border-radius: 4px; font-family: var(--font-mono); font-size: 11.5px; color: var(--ink-2); }
.gm-toast { position: fixed; left: 50%; bottom: 90px; z-index: 60; transform: translate(-50%, 20px); opacity: 0; padding: 10px 16px; border-radius: 4px; background: var(--ink); color: var(--paper); font-size: 14px; transition: all .2s ease; pointer-events: none; max-width: calc(100vw - 32px); }
.gm-toast.on { opacity: 1; transform: translate(-50%, 0); }

.gm-mbar { display: none; }

@media (max-width: 1000px) {
  .gm-shell { grid-template-columns: minmax(0, 1fr); padding: 24px 16px 0; gap: 0; }
  .gm-hero .wrap { padding-top: 40px; padding-bottom: 32px; }
  .gm-side { position: fixed; top: 0; bottom: 0; left: 0; z-index: 50; width: min(340px, 88vw); max-height: none; padding: 16px 18px 90px; background: var(--paper); border-right: 1px solid var(--line); box-shadow: var(--shadow); transform: translateX(-105%); transition: transform .25s ease; }
  .gm-side.on { transform: none; }
  .gm-ask-fab { display: none; }
  .gm-mbar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 30; display: grid; grid-template-columns: repeat(3, 1fr); background: var(--paper); border-top: 1px solid var(--line); padding-bottom: env(safe-area-inset-bottom); }
  .gm-mbar button { height: 54px; border: 0; background: transparent; color: var(--ink); font-size: 14px; cursor: pointer; }
  .gm-mbar button.ai { color: var(--accent); font-weight: 700; }
  .site-foot { padding-bottom: 60px; }
  .gm-article { font-size: 16px; }
  .gm-article h1 { font-size: 26px; }
  .gm-article h2 { font-size: 21px; }
  .gm-fig { padding: 12px 10px 10px; margin-left: -4px; margin-right: -4px; }
}
@media (min-width: 1001px) { .gm-side-close { display: none; } }
</style>
</head>
<body>
<div class="gm-progress" id="gmProgress"></div>
<header class="site-bar">
  <div class="wrap">
    <a class="brand" href="../">
      <img src="%%AVATAR%%" alt="avatar">
      <span class="brand-text"><span class="brand-name">%%SITE%%</span><span class="brand-sub">%%SUB%%</span></span>
    </a>
    <nav class="site-nav">
      <a href="../"><span class="nav-text">首页</span></a>
      <a href="../tag.html#All"><span class="nav-text">标签</span></a>
      <button class="icon-btn" type="button" id="themeBtn" title="切换主题" aria-label="切换主题">
        <svg viewBox="0 0 16 16" class="stroke"><g id="themeIcon"></g></svg>
      </button>
    </nav>
  </div>
</header>

<section class="gm-hero">
  <div class="wrap">
    <div class="kicker">核心专题 · English Grammar System</div>
    <h1>%%TITLE%%</h1>
    <div class="gm-hero-meta"><span>%%STATS%%</span><span>选中任意文字即可问 AI</span></div>
    <div class="gm-legend" aria-label="图解配色">
      <span class="lg-n">名词性</span><span class="lg-a">形容词性</span><span class="lg-d">副词性</span><span class="lg-v">动词 / 连接</span>
    </div>
  </div>
</section>

<div class="gm-shell">
  <aside class="gm-side" id="gmSide" aria-label="目录与搜索">
    <div class="gm-drawer-head gm-side-close" style="padding:0 0 12px;margin-bottom:4px;"><b>目录 · 搜索</b><button class="gm-x" type="button" data-close="side" aria-label="关闭">×</button></div>
    <form class="gm-search" id="gmSearchForm" role="search">
      <svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="4.6"/><path d="M10.4 10.4 14 14"/></svg>
      <input id="gmQ" type="search" placeholder="搜索全文：定语从句、whose…" autocomplete="off" aria-label="搜索全文">
    </form>
    <div class="gm-search-bar" id="gmBar"><span id="gmCount"></span><span><button type="button" id="gmPrev" aria-label="上一个">↑</button> <button type="button" id="gmNext" aria-label="下一个">↓</button> <button type="button" id="gmClear">清除</button></span></div>
    <ul class="gm-results" id="gmResults"></ul>
    <div class="gm-side-title">关键词条</div>
    <div class="gm-kws" id="gmKws">%%KEYWORDS%%</div>
    <div class="gm-side-title">目录</div>
    <ul class="gm-toc" id="gmToc">
%%TOC%%
    </ul>
  </aside>

  <article class="gm-article" id="gmArticle">
%%ARTICLE%%
  </article>
</div>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-brand"><b>%%SITE%%</b><span>%%SUB%%</span></div>
    <div class="foot-meta"><div><a href="../">← 返回首页</a> · <a href="#">回到顶部 ↑</a></div><div>核心专题 · 英语语法体系</div></div>
  </div>
</footer>

<button class="gm-ask-fab" type="button" id="gmFab"><span aria-hidden="true">✦</span> 问 AI</button>
<button class="gm-sel-btn" type="button" id="gmSelBtn">✦ 问 AI 这段</button>
<div class="gm-mbar"><button type="button" data-open="side">☰ 目录</button><button type="button" data-open="search">⌕ 搜索</button><button type="button" class="ai" data-open="ask">✦ 问 AI</button></div>
<div class="gm-scrim" id="gmScrim"></div>

<aside class="gm-drawer gm-ask" id="gmAsk" aria-label="问 AI">
  <div class="gm-drawer-head"><b>问 AI · 不懂就问</b><button class="gm-x" type="button" data-close="ask" aria-label="关闭">×</button></div>
  <div class="gm-ask-body">
    <div class="gm-ask-ctx">
      <div class="lbl" id="gmCtxLbl">当前章节</div>
      <div class="val" id="gmCtxVal">—</div>
      <div class="quote" id="gmCtxQuote" hidden></div>
      <label><input type="checkbox" id="gmCtxOn" checked> 把这部分内容一起发给 AI 作背景</label>
    </div>
    <div class="gm-quick" id="gmQuick">
      <button type="button" data-q="用大白话给我讲一遍这部分，再用一个比喻帮我记住。">大白话讲一遍</button>
      <button type="button" data-q="针对这部分出 5 道练习题（选择或改错），最后再给出答案和解析。">出 5 道练习题</button>
      <button type="button" data-q="再给我 5 个地道例句，并按「名词性 / 形容词性 / 副词性成分」逐句分析。">再来 5 个例句</button>
      <button type="button" data-q="中国学生在这部分最容易犯哪些错误？各举一个错句并改正。">常见错误</button>
    </div>
    <textarea id="gmQuestion" placeholder="写下你的问题，例如：which 和 that 到底什么时候不能互换？"></textarea>
    <div class="gm-prov">
      <button type="button" class="primary" data-ai="gemini"><b>Gemini</b><em>推荐</em><small>登录 Google 账号即可免费用。问题会自动复制，打开后按 Ctrl/⌘ + V 粘贴发送。</small></button>
      <button type="button" data-ai="aimode"><b>Google AI 模式</b><em>自动带入</em><small>由 Gemini 驱动的 Google 搜索 AI 模式，问题会直接填好。</small></button>
      <button type="button" data-ai="deepseek"><b>DeepSeek</b><em>国内直连</em><small>免费，国内网络可直接打开。问题已复制，粘贴即可。</small></button>
    </div>
    <details><summary>查看 / 复制将要发送的完整提示词</summary><pre id="gmPromptPreview"></pre><button type="button" class="btn-line" id="gmCopyPrompt" style="height:34px;font-size:13px;margin-top:6px;">复制提示词</button></details>
    <p class="gm-ask-note">提示：Gemini 与 Google AI 模式需要能访问 Google；DeepSeek 在国内可直接使用。本页不会收集你的问题，所有内容只在你的浏览器里生成。</p>
  </div>
</aside>
<div class="gm-toast" id="gmToast" role="status"></div>

<script>
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var article = $("gmArticle");
  var TITLE = document.querySelector(".gm-hero h1").textContent;

  /* ---------- theme (shares the blog's meek_theme setting) ---------- */
  var ICONS = {
    light: '<circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.6M8 12.9v1.6M1.5 8h1.6M12.9 8h1.6M3.4 3.4l1.1 1.1M11.5 11.5l1.1 1.1M3.4 12.6l1.1-1.1M11.5 4.5l1.1-1.1"/>',
    dark: '<path d="M13.5 9.6A5.6 5.6 0 0 1 6.4 2.5a5.6 5.6 0 1 0 7.1 7.1z"/>',
    auto: '<circle cx="8" cy="8" r="5.5"/><path d="M8 2.5v11" /><path d="M8 2.5a5.5 5.5 0 0 1 0 11z" fill="currentColor"/>'
  };
  function setTheme(m) {
    document.documentElement.setAttribute("data-color-mode", m);
    $("themeIcon").innerHTML = ICONS[m] || ICONS.light;
  }
  setTheme(document.documentElement.getAttribute("data-color-mode"));
  $("themeBtn").addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-color-mode");
    var next = cur === "light" ? "dark" : cur === "dark" ? "auto" : "light";
    try { localStorage.setItem("meek_theme", next); } catch (e) {}
    setTheme(next);
  });

  /* ---------- drawers ---------- */
  var side = $("gmSide"), ask = $("gmAsk"), scrim = $("gmScrim");
  function closeAll() { side.classList.remove("on"); ask.classList.remove("on"); scrim.classList.remove("on"); }
  function open(which) {
    closeAll();
    if (which === "ask") { openAsk(); return; }
    side.classList.add("on"); scrim.classList.add("on");
    if (which === "search") setTimeout(function () { $("gmQ").focus(); }, 260);
  }
  document.querySelectorAll("[data-open]").forEach(function (b) { b.addEventListener("click", function () { open(b.dataset.open); }); });
  document.querySelectorAll("[data-close]").forEach(function (b) { b.addEventListener("click", closeAll); });
  scrim.addEventListener("click", closeAll);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });
  var isMobile = function () { return window.matchMedia("(max-width: 1000px)").matches; };
  $("gmToc").addEventListener("click", function (e) { if (e.target.closest("a") && isMobile()) closeAll(); });

  /* ---------- TOC scrollspy + progress ---------- */
  var heads = Array.prototype.slice.call(article.querySelectorAll("h1[id], h2[id], h3[id]"));
  var tocLinks = {};
  document.querySelectorAll("#gmToc a").forEach(function (a) { tocLinks[a.dataset.id] = a; });
  var current = { h2: null, h1: null };
  function onScroll() {
    var y = window.scrollY + 100, active = null, h2 = null, h1 = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].offsetTop > y) break;
      active = heads[i];
      if (heads[i].tagName === "H2") h2 = heads[i];
      if (heads[i].tagName === "H1") { h1 = heads[i]; h2 = null; }
    }
    current.h2 = h2; current.h1 = h1;
    document.querySelectorAll("#gmToc a.active").forEach(function (a) { a.classList.remove("active"); });
    document.querySelectorAll("#gmToc .lv3.show").forEach(function (li) { li.classList.remove("show"); });
    if (active && tocLinks[active.id]) {
      tocLinks[active.id].classList.add("active");
      var sec = h2 || active;
      var li = tocLinks[sec.id] && tocLinks[sec.id].parentElement;
      for (var n = li && li.nextElementSibling; n && n.classList.contains("lv3"); n = n.nextElementSibling) n.classList.add("show");
    }
    var doc = document.documentElement;
    var p = window.scrollY / Math.max(1, doc.scrollHeight - window.innerHeight);
    $("gmProgress").style.width = (Math.min(1, p) * 100).toFixed(2) + "%";
  }
  var ticking = false;
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; onScroll(); }); } }, { passive: true });
  onScroll();

  /* ---------- search ---------- */
  var hits = [], cur = -1;
  function sectionOf(node) {
    var name = "";
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING) { if (heads[i].tagName !== "H3") name = heads[i].textContent; }
      else break;
    }
    return name;
  }
  function clearHits() {
    article.querySelectorAll("mark.gm-hit").forEach(function (m) {
      var p = m.parentNode; p.replaceChild(document.createTextNode(m.textContent), m); p.normalize();
    });
    hits = []; cur = -1;
    $("gmResults").innerHTML = ""; $("gmBar").classList.remove("on");
    document.querySelectorAll(".gm-kw.on").forEach(function (k) { k.classList.remove("on"); });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function search(q) {
    clearHits();
    q = q.trim();
    if (!q) return;
    var lower = q.toLowerCase();
    var walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return n.parentNode.closest("svg") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; }
    });
    var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var text = node.nodeValue, low = text.toLowerCase(), idx = low.indexOf(lower);
      if (idx < 0) return;
      var frag = document.createDocumentFragment(), last = 0;
      while (idx >= 0) {
        frag.appendChild(document.createTextNode(text.slice(last, idx)));
        var m = document.createElement("mark"); m.className = "gm-hit"; m.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(m); hits.push(m);
        last = idx + q.length; idx = low.indexOf(lower, last);
      }
      frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
    $("gmBar").classList.add("on");
    if (!hits.length) { $("gmCount").textContent = "没有找到「" + q + "」"; return; }
    var list = $("gmResults"), html = "";
    hits.slice(0, 60).forEach(function (m, i) {
      var block = m.closest("p, li, td, th, h1, h2, h3, blockquote, figcaption") || m.parentNode;
      var t = block.textContent, at = t.toLowerCase().indexOf(lower);
      var s = Math.max(0, at - 18), snip = (s ? "…" : "") + esc(t.slice(s, at)) + "<mark>" + esc(t.slice(at, at + q.length)) + "</mark>" + esc(t.slice(at + q.length, at + q.length + 30)) + "…";
      html += '<li><button type="button" data-i="' + i + '"><small>' + esc(sectionOf(m)) + "</small>" + snip + "</button></li>";
    });
    list.innerHTML = html;
    go(0);
  }
  function go(i) {
    if (!hits.length) return;
    if (cur >= 0) hits[cur].classList.remove("cur");
    cur = (i + hits.length) % hits.length;
    hits[cur].classList.add("cur");
    $("gmCount").textContent = "共 " + hits.length + " 处 · 第 " + (cur + 1) + " 处";
    hits[cur].scrollIntoView({ behavior: "smooth", block: "center" });
  }
  var timer;
  $("gmQ").addEventListener("input", function () { clearTimeout(timer); var v = this.value; timer = setTimeout(function () { search(v); }, 250); });
  $("gmSearchForm").addEventListener("submit", function (e) {
    e.preventDefault();
    if (hits.length) go(cur + 1); else search($("gmQ").value);
    if (isMobile()) closeAll();
  });
  $("gmNext").addEventListener("click", function () { go(cur + 1); });
  $("gmPrev").addEventListener("click", function () { go(cur - 1); });
  $("gmClear").addEventListener("click", function () { $("gmQ").value = ""; clearHits(); });
  $("gmResults").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return; go(+b.dataset.i); if (isMobile()) closeAll();
  });
  $("gmKws").addEventListener("click", function (e) {
    var b = e.target.closest(".gm-kw"); if (!b) return;
    $("gmQ").value = b.textContent; search(b.textContent); b.classList.add("on");
  });

  /* ---------- ask AI ---------- */
  var selected = "", frozen = null;
  function sectionText(h) {
    if (!h) return "";
    var out = [], n = h.nextElementSibling;
    while (n && !/^H[12]$/.test(n.tagName)) { if (!n.matches("figure")) out.push(n.innerText); n = n.nextElementSibling; }
    return out.join("\n").replace(/\n{3,}/g, "\n\n").trim();
  }
  function ctx() {
    var h = current.h2 || current.h1;
    var name = h ? h.textContent.trim() : "全文概览";
    if (selected) return { label: "你选中的内容", name: name, text: selected };
    var t = h ? sectionText(h) : (article.querySelector("blockquote") || article).innerText;
    return { label: "当前章节", name: name, text: t };
  }
  function buildPrompt(limit) {
    var c = frozen || ctx(), q = $("gmQuestion").value.trim() || "请讲解这部分内容，并帮我理清其中的重点和难点。";
    var parts = ["你是一位耐心的英语语法老师。我正在学习《" + TITLE + "》，它的核心方法是：一切英语成分只分名词性、形容词性、副词性（外加动词）四类；简单句是积木，从句 = 连词 + 简单句，非谓语动词和从句是一回事。"];
    parts.push("【所在章节】" + c.name);
    if ($("gmCtxOn").checked && c.text) {
      var t = c.text.length > limit ? c.text.slice(0, limit) + "……（节选）" : c.text;
      parts.push("【" + (selected ? "我选中的原文" : "本节原文") + "】\n" + t);
    }
    parts.push("【我的问题】\n" + q);
    parts.push("请用中文讲解，英文例句保留英文，并尽量沿用上面「名词性 / 形容词性 / 副词性成分」的分析框架。");
    return parts.join("\n\n");
  }
  function refreshCtx() {
    var c = frozen || ctx();
    $("gmCtxLbl").textContent = c.label;
    $("gmCtxVal").textContent = c.name;
    var qd = $("gmCtxQuote");
    if (selected) { qd.hidden = false; qd.textContent = "“" + selected + "”"; } else { qd.hidden = true; }
    $("gmPromptPreview").textContent = buildPrompt(1800);
  }
  function openAsk() {
    closeAll();
    frozen = null; frozen = ctx();
    refreshCtx();
    ask.classList.add("on"); scrim.classList.add("on");
    setTimeout(function () { $("gmQuestion").focus(); }, 260);
  }
  $("gmFab").addEventListener("click", function () { selected = ""; openAsk(); });
  $("gmQuestion").addEventListener("input", function () { $("gmPromptPreview").textContent = buildPrompt(1800); });
  $("gmCtxOn").addEventListener("change", refreshCtx);
  $("gmQuick").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    $("gmQuestion").value = b.dataset.q; refreshCtx(); $("gmQuestion").focus();
  });

  function toast(msg) {
    var t = $("gmToast"); t.textContent = msg; t.classList.add("on");
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("on"); }, 3200);
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return fallback(); });
    }
    return Promise.resolve(fallback());
    function fallback() {
      var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select(); var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); return ok;
    }
  }
  var PROVIDERS = {
    gemini: { url: function () { return "https://gemini.google.com/app"; }, copy: true, name: "Gemini" },
    aimode: { url: function () { return "https://www.google.com/search?udm=50&q=" + encodeURIComponent(buildPrompt(700)); }, copy: true, name: "Google AI 模式" },
    deepseek: { url: function () { return "https://chat.deepseek.com/"; }, copy: true, name: "DeepSeek" }
  };
  document.querySelectorAll("[data-ai]").forEach(function (b) {
    b.addEventListener("click", function () {
      var p = PROVIDERS[b.dataset.ai], prompt = buildPrompt(1800);
      var win = window.open(p.url(), "_blank", "noopener");
      copy(prompt).then(function (ok) {
        if (b.dataset.ai === "aimode") toast(ok ? "已打开 Google AI 模式（完整问题也已复制）" : "已打开 Google AI 模式");
        else toast(ok ? "问题已复制 ✓ 在 " + p.name + " 里按 Ctrl/⌘ + V 粘贴发送" : "复制失败，请展开下方「完整提示词」手动复制");
      });
      if (!win) toast("浏览器拦截了新窗口，请允许弹出窗口后重试");
    });
  });
  $("gmCopyPrompt").addEventListener("click", function () {
    copy(buildPrompt(1800)).then(function (ok) { toast(ok ? "提示词已复制 ✓" : "复制失败，请手动选择文本复制"); });
  });

  /* selection → ask */
  var selBtn = $("gmSelBtn");
  function hideSel() { selBtn.style.display = "none"; }
  document.addEventListener("selectionchange", function () {
    var s = window.getSelection();
    if (!s || s.isCollapsed || !article.contains(s.anchorNode)) { setTimeout(function () { if (window.getSelection().isCollapsed) hideSel(); }, 150); return; }
  });
  article.addEventListener("mouseup", showSel);
  article.addEventListener("touchend", function () { setTimeout(showSel, 300); });
  function showSel() {
    var s = window.getSelection(), text = s ? s.toString().trim() : "";
    if (!text || text.length < 2 || !article.contains(s.anchorNode)) { hideSel(); return; }
    var r = s.getRangeAt(0).getBoundingClientRect();
    selBtn.style.display = "block";
    var left = Math.min(window.scrollX + r.left + r.width / 2 - selBtn.offsetWidth / 2, window.scrollX + document.documentElement.clientWidth - selBtn.offsetWidth - 8);
    selBtn.style.left = Math.max(8, left) + "px";
    selBtn.style.top = (window.scrollY + r.top - 42) + "px";
    selBtn.dataset.text = text.slice(0, 1500);
  }
  selBtn.addEventListener("mousedown", function (e) { e.preventDefault(); });
  selBtn.addEventListener("click", function () {
    selected = selBtn.dataset.text || ""; hideSel();
    $("gmQuestion").value = "";
    openAsk();
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
