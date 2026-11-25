#!/usr/bin/env python3
"""Build the prompt library page: content/prompts.md -> static/prompts/index.html

Every prompt is a card (illustration + title) on one framed board. Clicking a
card opens the full prompt with one-click copy and "copy & open" buttons for
ChatGPT / Gemini / Claude / DeepSeek. Each card also has its own link
(<site>/prompts/#<id>).

Gmeek copies static/ into docs/, so the page is served at <site>/prompts/.
Edit content/prompts.md (format is described at its top), then re-run:

    python3 scripts/build_prompts.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt_art import art  # noqa: E402

SRC = ROOT / "content" / "prompts.md"
OUT = ROOT / "static" / "prompts" / "index.html"
THEME = ROOT / "templates" / "theme.css"
CONFIG = ROOT / "config.json"

# Category -> colour class (colours are defined in the page CSS).
CATS = [("学习", "n"), ("调研", "d"), ("英语", "a"), ("法语", "v"), ("写作", "a"), ("效率", "e")]
CAT_CLASS = dict(CATS)


def parse(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    items = []
    for block in re.split(r"^=== ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n---\n")
        lines = head.strip().splitlines()
        item = {"id": lines[0].strip()}
        for ln in lines[1:]:
            k, _, v = ln.partition(":")
            item[k.strip()] = v.strip()
        item["prompt"] = body.strip()
        for key in ("title", "cat", "desc", "art"):
            if not item.get(key):
                raise SystemExit("prompt %s is missing '%s'" % (item["id"], key))
        if item["cat"] not in CAT_CLASS:
            raise SystemExit("prompt %s has unknown cat %s" % (item["id"], item["cat"]))
        items.append(item)
    return items


def build():
    items = parse(SRC.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    theme_css = THEME.read_text(encoding="utf-8")

    cards = []
    for i, it in enumerate(items, 1):
        cards.append(
            '<button type="button" class="pb-card c-%s" data-id="%s" data-cat="%s" data-search="%s">'
            '<span class="pb-media">%s</span>'
            '<span class="pb-body"><span class="pb-no">%02d · %s</span><span class="pb-title">%s</span></span>'
            '</button>' % (
                CAT_CLASS[it["cat"]], html.escape(it["id"]), html.escape(it["cat"]),
                html.escape((it["title"] + " " + it["desc"] + " " + it["cat"] + " " + it["prompt"]).lower()),
                art(it["art"]), i, html.escape(it["cat"]), html.escape(it["title"])))

    used = [c for c, _ in CATS if any(it["cat"] == c for it in items)]
    chips = ['<button type="button" class="pb-chip on" data-cat="">全部 <i>%d</i></button>' % len(items)]
    for c in used:
        chips.append('<button type="button" class="pb-chip" data-cat="%s">%s <i>%d</i></button>'
                     % (html.escape(c), html.escape(c), sum(1 for it in items if it["cat"] == c)))

    data = [{"id": it["id"], "title": it["title"], "cat": it["cat"], "cls": CAT_CLASS[it["cat"]],
             "desc": it["desc"], "prompt": it["prompt"]} for it in items]

    page = (TEMPLATE
            .replace("%%SITE%%", html.escape(config.get("title", "")))
            .replace("%%SUB%%", html.escape(config.get("subTitle", "")))
            .replace("%%AVATAR%%", html.escape(config.get("avatarUrl", "")))
            .replace("%%THEME_CSS%%", theme_css)
            .replace("%%COUNT%%", str(len(items)))
            .replace("%%CATCOUNT%%", str(len(used)))
            .replace("%%CHIPS%%", "".join(chips))
            .replace("%%CARDS%%", "\n".join(cards))
            .replace("%%DATA%%", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print("wrote %s (%d prompts)" % (OUT.relative_to(ROOT), len(items)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" data-color-mode="light" data-light-theme="light" data-dark-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>常用 Prompt 武器库 · %%SITE%%</title>
<meta name="description" content="核心专题：常用 Prompt 武器库。学新东西、做调研、学单词、写文章、排查报错……把每次和 AI 打交道的开场白写好，随取随用。">
<meta property="og:title" content="常用 Prompt 武器库">
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

/* ===================== prompt library page ===================== */
html[data-color-mode][data-light-theme] {
  --g-n: #2f6b55; --g-n-bg: #dfeae3;
  --g-a: #96701c; --g-a-bg: #f3e8c8;
  --g-d: #3b5b84; --g-d-bg: #dde6f1;
  --g-v: #a4482b; --g-v-bg: #f4e0d7;
  --g-e: #5b5f57; --g-e-bg: #e6e3da;
}
html[data-color-mode="dark"][data-dark-theme] {
  --g-n: #8cc4ad; --g-n-bg: #1d3029;
  --g-a: #dcb862; --g-a-bg: #352b18;
  --g-d: #9fbbe0; --g-d-bg: #1d2836;
  --g-v: #e59a80; --g-v-bg: #3a241c;
  --g-e: #b9bcb2; --g-e-bg: #262b27;
}
@media (prefers-color-scheme: dark) {
  html[data-color-mode="auto"][data-dark-theme] {
    --g-n: #8cc4ad; --g-n-bg: #1d3029;
    --g-a: #dcb862; --g-a-bg: #352b18;
    --g-d: #9fbbe0; --g-d-bg: #1d2836;
    --g-v: #e59a80; --g-v-bg: #3a241c;
    --g-e: #b9bcb2; --g-e-bg: #262b27;
  }
}
.site-nav a.on .nav-text { color: var(--accent); }

.pb-hero { border-bottom: 1px solid var(--line); }
.pb-hero .wrap { max-width: 1240px; padding-top: 64px; padding-bottom: 44px; }
.pb-hero h1 { margin: 16px 0 0; font-family: var(--font-serif); font-weight: 900; font-size: clamp(34px, 5.6vw, 64px); line-height: 1.12; color: var(--ink); }
.pb-hero h1 .mark { padding: 0 .04em; }
.pb-intro { max-width: 40em; margin: 22px 0 0; color: var(--ink-2); font-size: 16.5px; line-height: 1.9; }
.pb-hero-meta { display: flex; flex-wrap: wrap; gap: 8px 22px; margin-top: 22px; font-family: var(--font-mono); font-size: 12.5px; color: var(--muted); }

/* the framed board */
.pb-stage { max-width: 1240px; margin: 0 auto; padding: 48px 32px 24px; }
.pb-frame { position: relative; border: 1.5px solid var(--ink); border-radius: 22px; background: var(--paper-2); padding: 34px 40px 44px; box-shadow: 6px 6px 0 var(--paper-3); }
.pb-frame::before { content: "PROMPT · LIBRARY"; position: absolute; top: -10px; left: 34px; padding: 0 10px; background: var(--paper); font-family: var(--font-mono); font-size: 11px; letter-spacing: .18em; color: var(--accent); }
.pb-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px 24px; padding-bottom: 18px; border-bottom: 1.5px solid var(--ink); }
.pb-head h2 { margin: 0; border: 0; padding: 0; font-family: var(--font-serif); font-weight: 900; font-size: 26px; line-height: 1.2; color: var(--ink); }
.pb-head h2 small { margin-left: 10px; font-family: var(--font-mono); font-size: 12px; font-weight: 400; letter-spacing: .1em; color: var(--muted); }
.pb-tools { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.pb-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pb-chip { height: 30px; padding: 0 12px; border: 1px solid var(--line-2); border-radius: 999px; background: transparent; color: var(--ink-2); font-size: 13px; cursor: pointer; }
.pb-chip i { font-style: normal; font-family: var(--font-mono); font-size: 11px; color: var(--muted); margin-left: 2px; }
.pb-chip:hover, .pb-chip.on { border-color: var(--accent); color: var(--accent); }
.pb-chip.on { background: var(--accent); color: var(--accent-ink); }
.pb-chip.on i { color: inherit; opacity: .75; }
.pb-search { display: flex; align-items: center; width: 220px; border: 1px solid var(--line-2); border-radius: 999px; background: var(--paper); }
.pb-search:focus-within { border-color: var(--accent); }
.pb-search svg { width: 14px; height: 14px; margin-left: 12px; flex: none; fill: none; stroke: var(--muted); stroke-width: 1.6; }
.pb-search input { flex: 1; min-width: 0; height: 32px; padding: 0 10px 0 8px; border: 0; outline: 0; background: transparent; color: var(--ink); font-size: 13.5px; }

.pb-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 22px 20px; margin-top: 28px; }
.pb-card { display: flex; flex-direction: column; padding: 0; text-align: left; border: 1.5px solid var(--ink); border-radius: 12px; background: var(--paper); color: var(--ink); overflow: hidden; cursor: pointer; transition: transform .18s ease, box-shadow .18s ease; font: inherit; }
.pb-card:nth-child(4n+1) { border-radius: 12px 16px 12px 14px; }
.pb-card:nth-child(4n+3) { border-radius: 16px 12px 14px 12px; }
.pb-card:hover, .pb-card:focus-visible { transform: translate(-2px, -3px); box-shadow: 4px 5px 0 var(--cc); outline: none; }
.pb-card[hidden] { display: none; }
.pb-media { display: block; aspect-ratio: 16 / 10; background: var(--cbg); border-bottom: 1.5px solid var(--ink); }
.pb-media svg { display: block; width: 100%; height: 100%; }
.pb-body { display: block; padding: 12px 14px 15px; }
.pb-no { display: block; font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .12em; color: var(--cc); }
.pb-title { display: block; margin-top: 5px; font-family: var(--font-serif); font-weight: 700; font-size: 16px; line-height: 1.35; color: var(--ink); }
.pb-empty { display: none; padding: 40px 0 10px; text-align: center; color: var(--muted); }
.pb-empty.on { display: block; }

.c-n { --cc: var(--g-n); --cbg: var(--g-n-bg); }
.c-a { --cc: var(--g-a); --cbg: var(--g-a-bg); }
.c-d { --cc: var(--g-d); --cbg: var(--g-d-bg); }
.c-v { --cc: var(--g-v); --cbg: var(--g-v-bg); }
.c-e { --cc: var(--g-e); --cbg: var(--g-e-bg); }

/* illustration strokes */
.pb-media .o { stroke: var(--ink); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.pb-media path.o:not(.c):not(.g):not(.p), .pb-media circle.o:not(.c):not(.g):not(.p) { fill: none; }
.pb-media .p { fill: var(--paper); }
.pb-media .c { fill: color-mix(in srgb, var(--cc) 30%, var(--paper)); }
.pb-media .g { fill: var(--marker); }
.pb-media .k { fill: none; stroke: var(--cc); stroke-width: 2.2; stroke-linecap: round; }
.pb-media .thick { stroke-width: 5; }
.pb-media .dash { stroke-dasharray: 3 5; }
.pb-media .gr { fill: none; stroke: var(--ink); stroke-width: 1.2; opacity: .25; stroke-dasharray: 2 6; }
.pb-media .dot { fill: var(--cc); opacity: .55; }
.pb-media .t { font-family: var(--font-mono); font-size: 12px; font-weight: 500; fill: var(--ink); }
.pb-media .tw { font-family: "Fraunces", Georgia, serif; font-style: italic; font-size: 17px; fill: var(--ink); }

/* how to use strip */
.pb-how { max-width: 1240px; margin: 0 auto; padding: 18px 32px 64px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.pb-how div { border-top: 1px solid var(--line-2); padding-top: 14px; font-size: 14px; color: var(--ink-2); line-height: 1.75; }
.pb-how b { display: block; font-family: var(--font-mono); font-size: 11px; letter-spacing: .14em; color: var(--accent); margin-bottom: 4px; font-weight: 500; }
.pb-how em { font-style: normal; background: var(--marker); padding: 0 .2em; }

/* detail dialog */
.pb-scrim { position: fixed; inset: 0; z-index: 45; background: rgba(0,0,0,.32); opacity: 0; pointer-events: none; transition: opacity .2s ease; }
.pb-scrim.on { opacity: 1; pointer-events: auto; }
.pb-dlg { position: fixed; z-index: 50; left: 50%; top: 50%; width: min(760px, calc(100vw - 32px)); max-height: calc(100vh - 48px); display: flex; flex-direction: column; transform: translate(-50%, -46%); opacity: 0; pointer-events: none; transition: all .22s ease; background: var(--paper); border: 1.5px solid var(--ink); border-radius: 18px; box-shadow: 8px 8px 0 var(--cc, var(--accent)); }
.pb-dlg.on { opacity: 1; transform: translate(-50%, -50%); pointer-events: auto; }
.pb-dlg-head { display: grid; grid-template-columns: 120px 1fr auto; gap: 18px; align-items: center; padding: 20px 22px 16px; border-bottom: 1px solid var(--line); }
.pb-dlg-art { border: 1.5px solid var(--ink); border-radius: 10px; overflow: hidden; }
.pb-dlg-art .pb-media { border-bottom: 0; }
.pb-dlg-kicker { font-family: var(--font-mono); font-size: 11px; letter-spacing: .14em; color: var(--cc); }
.pb-dlg h3 { margin: 4px 0 0; font-family: var(--font-serif); font-weight: 900; font-size: 24px; line-height: 1.25; border: 0; padding: 0; }
.pb-dlg-desc { margin: 6px 0 0; color: var(--ink-2); font-size: 14px; line-height: 1.6; }
.pb-x { align-self: start; width: 34px; height: 34px; border: 1px solid var(--line-2); border-radius: 50%; background: transparent; color: var(--ink); font-size: 18px; line-height: 1; cursor: pointer; }
.pb-x:hover { border-color: var(--accent); color: var(--accent); }
.pb-dlg-body { flex: 1; min-height: 0; overflow: auto; padding: 18px 22px; }
.pb-hint { margin: 0 0 10px; font-size: 12.5px; color: var(--muted); }
.pb-hint mark { background: var(--marker); color: var(--ink); padding: 0 .25em; border-radius: 2px; }
.pb-prompt { margin: 0; padding: 18px 20px; border: 1px dashed var(--line-2); border-radius: 10px; background: var(--paper-2); white-space: pre-wrap; word-break: break-word; font-family: var(--font-sans); font-size: 14.5px; line-height: 1.85; color: var(--ink); }
.pb-prompt mark { background: var(--marker); color: var(--ink); padding: 0 .2em; border-radius: 2px; font-weight: 600; }
.pb-dlg-foot { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 14px 22px 18px; border-top: 1px solid var(--line); }
.pb-btn { height: 38px; padding: 0 16px; border: 1px solid var(--line-2); border-radius: 999px; background: transparent; color: var(--ink); font-size: 14px; cursor: pointer; }
.pb-btn:hover { border-color: var(--accent); color: var(--accent); }
.pb-btn.main { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); font-weight: 700; }
.pb-btn.main:hover { background: var(--accent-2); color: var(--accent-ink); }
.pb-foot-sp { flex: 1; }
.pb-nav { width: 38px; padding: 0; }
.pb-toast { position: fixed; left: 50%; bottom: 40px; z-index: 60; transform: translate(-50%, 20px); opacity: 0; padding: 10px 16px; border-radius: 4px; background: var(--ink); color: var(--paper); font-size: 14px; transition: all .2s ease; pointer-events: none; max-width: calc(100vw - 32px); }
.pb-toast.on { opacity: 1; transform: translate(-50%, 0); }
body.pb-lock { overflow: hidden; }

@media (max-width: 1180px) { .pb-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
@media (max-width: 920px)  { .pb-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } .pb-frame { padding: 28px 22px 32px; } .pb-how { grid-template-columns: 1fr; } }
@media (max-width: 640px) {
  .pb-stage { padding: 32px 14px 16px; }
  .pb-frame { padding: 24px 14px 24px; border-radius: 16px; box-shadow: 4px 4px 0 var(--paper-3); }
  .pb-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 12px; }
  .pb-search { width: 100%; }
  .pb-tools { width: 100%; }
  .pb-title { font-size: 14.5px; }
  .pb-dlg { top: auto; bottom: 0; left: 0; width: 100vw; max-height: 88vh; transform: translateY(100%); border-radius: 18px 18px 0 0; box-shadow: none; }
  .pb-dlg.on { transform: none; }
  .pb-dlg-head { grid-template-columns: 1fr auto; }
  .pb-dlg-art { display: none; }
  .pb-how { padding: 10px 16px 48px; }
}
</style>
</head>
<body>
<header class="site-bar">
  <div class="wrap">
    <a class="brand" href="../">
      <img src="%%AVATAR%%" alt="avatar">
      <span class="brand-text"><span class="brand-name">%%SITE%%</span><span class="brand-sub">%%SUB%%</span></span>
    </a>
    <nav class="site-nav">
      <a href="../"><span class="nav-text">首页</span></a>
      <a href="../tag.html#All"><span class="nav-text">标签</span></a>
      <a href="../grammar/"><span class="nav-text">语法体系</span></a>
      <a class="on" href="./"><span class="nav-text">常用 Prompt</span></a>
      <button class="icon-btn" type="button" id="themeBtn" title="切换主题" aria-label="切换主题">
        <svg viewBox="0 0 16 16" class="stroke"><g id="themeIcon"></g></svg>
      </button>
    </nav>
  </div>
</header>

<section class="pb-hero">
  <div class="wrap">
    <div class="kicker">核心专题 · Prompt Library</div>
    <h1>常用 Prompt <span class="mark">武器库</span></h1>
    <p class="pb-intro">每次和 AI 打交道，不用从零想开场白。学一个新东西、调研一件事、记一个单词、打磨一篇文章、排查一个报错——把好用的提示词写好一次，以后直接调用，越用越顺手。</p>
    <div class="pb-hero-meta"><span>%%COUNT%% 个 Prompt</span><span>%%CATCOUNT%% 个场景</span><span>点卡片 · 一键复制</span><span>直达 ChatGPT / Gemini / Claude / DeepSeek</span></div>
  </div>
</section>

<main class="pb-stage">
  <div class="pb-frame">
    <div class="pb-head">
      <h2>我的提示词<small>%%COUNT%% PROMPTS</small></h2>
      <div class="pb-tools">
        <div class="pb-chips" id="pbChips">%%CHIPS%%</div>
        <label class="pb-search"><svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.6"/><path d="M10.4 10.4 14 14"/></svg><input id="pbQ" type="search" placeholder="搜索 Prompt…" aria-label="搜索 Prompt"></label>
      </div>
    </div>
    <div class="pb-grid" id="pbGrid">
%%CARDS%%
    </div>
    <div class="pb-empty" id="pbEmpty">没有找到匹配的 Prompt，换个关键词试试。</div>
  </div>
</main>

<section class="pb-how">
  <div><b>01 · 选</b>按场景筛选或直接搜索，点开卡片看完整的提示词。</div>
  <div><b>02 · 填</b>把<em>【高亮的部分】</em>换成你自己的内容：主题、单词、原文、报错……</div>
  <div><b>03 · 用</b>一键复制，或者直接打开常用的 AI，粘贴发送；每张卡片都有自己的链接，方便收藏。</div>
</section>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-brand"><b>%%SITE%%</b><span>%%SUB%%</span></div>
    <div class="foot-meta"><div><a href="../">← 返回首页</a> · <a href="#">回到顶部 ↑</a></div><div>核心专题 · 常用 Prompt 武器库</div></div>
  </div>
</footer>

<div class="pb-scrim" id="pbScrim"></div>
<div class="pb-dlg" id="pbDlg" role="dialog" aria-modal="true" aria-labelledby="pbDlgTitle">
  <div class="pb-dlg-head">
    <div class="pb-dlg-art" id="pbDlgArt"></div>
    <div>
      <div class="pb-dlg-kicker" id="pbDlgKicker"></div>
      <h3 id="pbDlgTitle"></h3>
      <p class="pb-dlg-desc" id="pbDlgDesc"></p>
    </div>
    <button class="pb-x" type="button" id="pbClose" aria-label="关闭">×</button>
  </div>
  <div class="pb-dlg-body">
    <p class="pb-hint" id="pbHint">使用前把 <mark>【高亮部分】</mark> 换成你自己的内容。</p>
    <pre class="pb-prompt" id="pbPrompt"></pre>
  </div>
  <div class="pb-dlg-foot">
    <button class="pb-btn main" type="button" id="pbCopy">复制 Prompt</button>
    <button class="pb-btn" type="button" data-ai="chatgpt">ChatGPT</button>
    <button class="pb-btn" type="button" data-ai="gemini">Gemini</button>
    <button class="pb-btn" type="button" data-ai="claude">Claude</button>
    <button class="pb-btn" type="button" data-ai="deepseek">DeepSeek</button>
    <span class="pb-foot-sp"></span>
    <button class="pb-btn pb-nav" type="button" id="pbPrev" aria-label="上一个">←</button>
    <button class="pb-btn pb-nav" type="button" id="pbNext" aria-label="下一个">→</button>
  </div>
</div>
<div class="pb-toast" id="pbToast" role="status"></div>

<script>
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var DATA = %%DATA%%;
  var byId = {}; DATA.forEach(function (d, i) { d.i = i; byId[d.id] = d; });

  /* ---------- theme (shares the blog's meek_theme setting) ---------- */
  var ICONS = {
    light: '<circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.6M8 12.9v1.6M1.5 8h1.6M12.9 8h1.6M3.4 3.4l1.1 1.1M11.5 11.5l1.1 1.1M3.4 12.6l1.1-1.1M11.5 4.5l1.1-1.1"/>',
    dark: '<path d="M13.5 9.6A5.6 5.6 0 0 1 6.4 2.5a5.6 5.6 0 1 0 7.1 7.1z"/>',
    auto: '<circle cx="8" cy="8" r="5.5"/><path d="M8 2.5v11" /><path d="M8 2.5a5.5 5.5 0 0 1 0 11z" fill="currentColor"/>'
  };
  function setTheme(m) { document.documentElement.setAttribute("data-color-mode", m); $("themeIcon").innerHTML = ICONS[m] || ICONS.light; }
  setTheme(document.documentElement.getAttribute("data-color-mode"));
  $("themeBtn").addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-color-mode");
    var next = cur === "light" ? "dark" : cur === "dark" ? "auto" : "light";
    try { localStorage.setItem("meek_theme", next); } catch (e) {}
    setTheme(next);
  });

  /* ---------- filter + search ---------- */
  var cards = [].slice.call(document.querySelectorAll(".pb-card"));
  var cat = "", q = "";
  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (!cat || c.dataset.cat === cat) && (!q || c.dataset.search.indexOf(q) !== -1);
      c.hidden = !ok; if (ok) shown++;
    });
    $("pbEmpty").classList.toggle("on", shown === 0);
  }
  $("pbChips").addEventListener("click", function (e) {
    var b = e.target.closest(".pb-chip"); if (!b) return;
    document.querySelectorAll(".pb-chip").forEach(function (x) { x.classList.toggle("on", x === b); });
    cat = b.dataset.cat; apply();
  });
  $("pbQ").addEventListener("input", function () { q = this.value.trim().toLowerCase(); apply(); });

  /* ---------- dialog ---------- */
  var dlg = $("pbDlg"), scrim = $("pbScrim"), cur = null, lastFocus = null;
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function visibleList() { return cards.filter(function (c) { return !c.hidden; }).map(function (c) { return byId[c.dataset.id]; }); }
  function open(id, push) {
    var d = byId[id]; if (!d) return;
    cur = d;
    if (!dlg.classList.contains("on")) lastFocus = document.activeElement;
    dlg.className = "pb-dlg on c-" + d.cls;
    var card = document.querySelector('.pb-card[data-id="' + id + '"]');
    $("pbDlgArt").innerHTML = card ? card.querySelector(".pb-media").outerHTML : "";
    $("pbDlgKicker").textContent = String(d.i + 1).padStart(2, "0") + " · " + d.cat;
    $("pbDlgTitle").textContent = d.title;
    $("pbDlgDesc").textContent = d.desc;
    $("pbPrompt").innerHTML = esc(d.prompt).replace(/【[^】\n]*】/g, function (m) { return "<mark>" + m + "</mark>"; });
    $("pbHint").hidden = d.prompt.indexOf("【") === -1;
    $("pbPrompt").parentNode.scrollTop = 0;
    scrim.classList.add("on"); document.body.classList.add("pb-lock");
    if (push !== false && location.hash !== "#" + id) history.replaceState(null, "", "#" + id);
    setTimeout(function () { $("pbCopy").focus(); }, 60);
  }
  function close() {
    dlg.classList.remove("on"); scrim.classList.remove("on"); document.body.classList.remove("pb-lock");
    cur = null;
    if (location.hash) history.replaceState(null, "", location.pathname + location.search);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function step(n) {
    var list = visibleList(); if (!cur || !list.length) return;
    var k = list.indexOf(cur); if (k === -1) k = 0;
    open(list[(k + n + list.length) % list.length].id);
  }
  $("pbGrid").addEventListener("click", function (e) { var c = e.target.closest(".pb-card"); if (c) open(c.dataset.id); });
  $("pbClose").addEventListener("click", close);
  scrim.addEventListener("click", close);
  $("pbPrev").addEventListener("click", function () { step(-1); });
  $("pbNext").addEventListener("click", function () { step(1); });
  document.addEventListener("keydown", function (e) {
    if (!dlg.classList.contains("on")) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowRight" && e.target.tagName !== "INPUT") step(1);
    else if (e.key === "ArrowLeft" && e.target.tagName !== "INPUT") step(-1);
  });
  if (location.hash && byId[location.hash.slice(1)]) open(location.hash.slice(1), false);

  /* ---------- copy + open AI ---------- */
  function toast(msg) {
    var t = $("pbToast"); t.textContent = msg; t.classList.add("on");
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("on"); }, 3000);
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
  $("pbCopy").addEventListener("click", function () {
    if (!cur) return;
    copy(cur.prompt).then(function (ok) { toast(ok ? "已复制 ✓ 记得替换【高亮部分】" : "复制失败，请手动选择文本复制"); });
  });
  var AI = {
    chatgpt: ["https://chatgpt.com/", "ChatGPT"],
    gemini: ["https://gemini.google.com/app", "Gemini"],
    claude: ["https://claude.ai/new", "Claude"],
    deepseek: ["https://chat.deepseek.com/", "DeepSeek"]
  };
  document.querySelectorAll("[data-ai]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!cur) return;
      var a = AI[b.dataset.ai], win = window.open(a[0], "_blank", "noopener");
      copy(cur.prompt).then(function (ok) { toast(ok ? "已复制 ✓ 在 " + a[1] + " 里按 Ctrl/⌘ + V 粘贴" : "复制失败，请手动复制"); });
      if (!win) toast("浏览器拦截了新窗口，请允许弹出窗口后重试");
    });
  });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
