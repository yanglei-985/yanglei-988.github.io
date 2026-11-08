"""SVG illustrations for the grammar page (content/grammar.md).

Each figure is plain inline SVG styled by CSS classes defined in
build_grammar.py, so it follows the site's light/dark theme:
  n = 名词性 (green)   a = 形容词性 (gold)   d = 副词性 (blue)
  v = 动词 / 连接 (terracotta)   neu = neutral   hl = accent outline

FIGURES maps an exact line of the article to the figure inserted after it.
The article text itself is never modified.
"""
from html import escape

FS = 15  # base font size inside the 680-wide viewBox


def tw(s, fs=FS):
    """Rough text width: CJK ~1em, ASCII ~0.56em."""
    w = 0.0
    for ch in s:
        w += fs * (1.0 if ord(ch) > 0x2E80 else 0.56)
    return w


def T(x, y, s, cls="", anchor="start", fs=None):
    st = ' style="font-size:%spx"' % fs if fs else ""
    return '<text x="%.1f" y="%.1f" class="%s" text-anchor="%s"%s>%s</text>' % (x, y, cls, anchor, st, escape(s))


def R(x, y, w, h, cls, rx=10, extra=""):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" class="box %s"%s/>' % (x, y, w, h, rx, cls, extra)


def box(x, y, w, h, cls, title, sub=None, tcls=None):
    out = [R(x, y, w, h, cls)]
    cx = x + w / 2
    if sub:
        out.append(T(cx, y + h / 2 - 3, title, "tb " + (tcls or "t" + cls.split()[0]), "middle"))
        out.append(T(cx, y + h / 2 + 17, sub, "ts", "middle"))
    else:
        out.append(T(cx, y + h / 2 + 5, title, "tb " + (tcls or "t" + cls.split()[0]), "middle"))
    return "".join(out)


def chip_w(text, fs=FS):
    return tw(text, fs) + 22


def chips(x, y, items, gap=8, h=32, fs=FS):
    """items: (text, cls, role, attr). Returns svg, list of (x, w) per chip."""
    out, pos = [], []
    for it in items:
        text, cls = it[0], it[1]
        w = chip_w(text, fs)
        out.append(R(x, y, w, h, cls, rx=7))
        out.append(T(x + w / 2, y + h / 2 + 5, text, "ten", "middle", fs))
        if len(it) > 2 and it[2]:
            out.append(T(x + w / 2, y + h + 18, it[2], "tb t" + cls.split()[0], "middle", 13))
        if len(it) > 3 and it[3]:
            out.append(T(x + w / 2, y + h + 34, it[3], "ts", "middle", 12))
        pos.append((x, w))
        x += w + gap
    return "".join(out), pos


def arrow(x1, y1, x2, y2, mid=None, cls="ln"):
    if mid:
        d = "M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x1, y1, mid[0], mid[1], x2, y2)
    else:
        d = "M%.1f,%.1f L%.1f,%.1f" % (x1, y1, x2, y2)
    return '<path d="%s" class="%s" marker-end="url(#ah)"/>' % (d, cls)


def svg(h, body, label):
    defs = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" class="ahead"/></marker></defs>')
    return ('<svg viewBox="0 0 680 %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s%s</svg>'
            % (h, escape(label), defs, body))


# ---------------------------------------------------------------- figures

def fig_four_parts():
    b = []
    b.append(T(40, 44, "① 形容词性成分 修饰 名词性成分", "tk"))
    b.append(box(40, 60, 240, 76, "a", "形容词性成分", "形容词·定语从句·分词·介词短语"))
    b.append(arrow(286, 98, 394, 98))
    b.append(T(340, 88, "修饰", "ts", "middle"))
    b.append(box(400, 60, 240, 76, "n", "名词性成分", "名词·代词·名词性从句·不定式·动名词"))
    b.append(T(40, 186, "② 副词性成分 修饰 动词、形容词、其他副词", "tk"))
    b.append(box(40, 202, 240, 76, "d", "副词性成分", "副词·状语从句·不定式·介词短语"))
    for i, (cls, name) in enumerate([("v", "动词（谓语）"), ("a", "形容词性成分"), ("d", "其他副词性成分")]):
        y = 196 + i * 46
        b.append(box(400, y, 240, 36, cls, name))
        b.append(arrow(286, 240, 394, y + 18, mid=(340, y + 18 if i != 1 else 240)))
    b.append(T(340, 362, "其余一切——从句、非谓语动词——都只是这几类成分的变形", "ts", "middle"))
    return svg(378, "".join(b), "四类成分与两条修饰关系")


def fig_prep():
    b = []
    b.append(box(20, 30, 150, 66, "neu", "介词", "at · on · with · for …", tcls="tink"))
    b.append(T(186, 70, "+", "tbig", "middle"))
    b.append(box(202, 30, 200, 66, "n", "名词性成分", "名词 · 动名词 · 名词性从句"))
    b.append(T(418, 70, "=", "tbig", "middle"))
    b.append(box(434, 30, 226, 66, "hl", "介词短语", "整体当作一个成分来用", tcls="tacc"))
    b.append(arrow(547, 96, 205, 160, mid=(470, 150)))
    b.append(arrow(547, 96, 515, 160))
    b.append(box(40, 160, 330, 70, "a", "形容词属性 → 后置定语", "The book on the shelf is great."))
    b.append(box(390, 160, 270, 70, "d", "副词属性 → 状语", "We went to a movie after dinner."))
    return svg(244, "".join(b), "介词短语的两种属性")


def fig_components():
    b = []
    b.append(T(50, 24, "例 1 · 主谓宾 + 层层叠加的状语", "tk"))
    s, pos = chips(50, 40, [("I", "n", "主语", "名词性"), ("will meet", "v", "谓语", "动词"), ("you", "n", "宾语", "名词性"),
                            ("at the park", "d", "状语", "副词性"), ("tomorrow", "d", "状语", "副词性"),
                            ("if it doesn't rain", "d", "状语", "副词性从句")])
    b.append(s)
    x0, x1 = pos[3][0], pos[5][0] + pos[5][1]
    b.append('<path d="M%.1f,124 v8 h%.1f v-8 M%.1f,132 v8" class="ln"/>' % (x0, x1 - x0, (x0 + x1) / 2))
    b.append(T((x0 + x1) / 2, 158, "三个副词性成分，都在修饰谓语 will meet", "ts", "middle"))
    b.append(T(50, 196, "例 2 · 补语：宾语和补语之间藏着「A is B」", "tk"))
    s, pos = chips(50, 236, [("We", "n", "主语", ""), ("consider", "v", "谓语", ""), ("him", "n", "宾语", ""), ("a fool", "a", "宾语补语", "")])
    b.append(s)
    hx = pos[2][0] + pos[2][1] / 2
    fx = pos[3][0] + pos[3][1] / 2
    b.append('<path d="M%.1f,234 C%.1f,206 %.1f,206 %.1f,234" class="ln dash"/>' % (hx, hx, fx, fx))
    b.append(T((hx + fx) / 2, 214, "=", "tb tacc", "middle"))
    b.append(T(372, 250, "还原：he is a fool", "ten tacc"))
    b.append(T(372, 274, "能还原出系动词关系的，就是补语", "ts"))
    return svg(300, "".join(b), "句子成分与词性属性的对应")


def fig_five_patterns():
    rows = [
        ("SV", "主谓", [("He", "n", "主语"), ("came", "v", "谓语")]),
        ("SVP", "主系表", [("She", "n", "主语"), ("is", "v", "系动词"), ("happy", "a", "表语")]),
        ("SVO", "主谓宾", [("We", "n", "主语"), ("learn", "v", "谓语"), ("English", "n", "宾语")]),
        ("SVOO", "主谓双宾", [("I", "n", "主语"), ("gave", "v", "谓语"), ("him", "n", "间接宾语"), ("a book", "n", "直接宾语")]),
        ("SVOC", "主谓宾补", [("I", "n", "主语"), ("painted", "v", "谓语"), ("the old wall", "n", "宾语"), ("black", "a", "宾语补语")]),
    ]
    b = []
    for i, (code, name, items) in enumerate(rows):
        y = 18 + i * 66
        b.append(T(24, y + 20, code, "tcode"))
        b.append(T(24, y + 40, name, "ts"))
        s, _ = chips(130, y, items, gap=10)
        b.append(s)
        if i:
            b.append('<line x1="24" y1="%d" x2="656" y2="%d" class="sep"/>' % (y - 8, y - 8))
    return svg(352, "".join(b), "简单句的五种基本句型")


def fig_conj():
    b = []
    b.append(T(24, 32, "✗", "tb tv"))
    b.append(T(48, 32, "I love you you love me.", "ten"))
    b.append(T(360, 32, "Run-on 连缀句", "ts"))
    b.append(T(24, 62, "✗", "tb tv"))
    b.append(T(48, 62, "I love you, you love me.", "ten"))
    b.append(T(360, 62, "Comma splice 逗号粘连", "ts"))
    b.append('<line x1="24" y1="84" x2="656" y2="84" class="sep"/>')
    b.append(T(24, 140, "并列", "tb tink"))
    s, _ = chips(100, 118, [("She enjoys painting,", "neu"), ("and", "v"), ("he loves playing the guitar", "neu")])
    b.append(s)
    b.append(T(24, 202, "主从", "tb tink"))
    s, pos = chips(100, 180, [("He believes", "neu"), ("that", "v"), ("honesty is the best policy", "neu")])
    b.append(s)
    x0, x1 = pos[1][0], pos[2][0] + pos[2][1]
    b.append('<path d="M%.1f,218 v8 h%.1f v-8 M%.1f,226 v8" class="ln"/>' % (x0, x1 - x0, (x0 + x1) / 2))
    b.append(T((x0 + x1) / 2, 254, "从句 = 连词 + 简单句（这里整体作宾语）", "ts", "middle"))
    return svg(268, "".join(b), "两个简单句必须用连词连接")


def fig_to_clause():
    b = []
    b.append(box(20, 36, 150, 64, "neu", "Is he a doctor?", "一般疑问句", tcls="ten tink"))
    b.append(arrow(172, 68, 236, 68))
    b.append(T(204, 56, "① 调语序", "ts", "middle"))
    b.append(box(240, 36, 150, 64, "neu", "he is a doctor", "陈述语序", tcls="ten tink"))
    b.append(arrow(392, 68, 456, 68))
    b.append(T(424, 56, "② 加连词", "ts", "middle"))
    b.append(box(460, 36, 200, 64, "n", "whether he is a doctor", "连词放句首", tcls="ten tink"))
    b.append(arrow(560, 102, 560, 146))
    b.append(T(552, 130, "③ 放进主句", "ts", "end"))
    b.append(box(250, 150, 410, 52, "hl", "Whether he is a doctor doesn't matter.", tcls="ten tacc"))
    b.append(T(24, 166, "选哪个连词？", "tb tink", fs=13))
    b.append(T(24, 188, "陈述句 → that", "ts"))
    b.append(T(24, 206, "一般疑问句 → whether", "ts"))
    b.append(T(24, 224, "特殊疑问句 → 原疑问词", "ts"))
    return svg(240, "".join(b), "独立句子变名词性从句的三步")


def fig_antecedent():
    b = []
    b.append(T(24, 30, "两个简单句，缺连词：", "ts"))
    s, pos = chips(24, 42, [("Sally is a teacher.", "neu"), ("Sally is warm-hearted.", "neu")], gap=12)
    b.append(s)
    b.append(T(pos[1][0] + pos[1][1] + 14, 63, "✗ 不能直接拼在一起", "tb tv", fs=13))
    b.append('<line x1="24" y1="98" x2="656" y2="98" class="sep"/>')
    s, pos = chips(24, 160, [("Sally is a", "neu"), ("teacher", "n"), ("who", "v"), ("is warm-hearted.", "neu")])
    b.append(s)
    tx = pos[1][0] + pos[1][1] / 2
    wx = pos[2][0] + pos[2][1] / 2
    b.append('<path d="M%.1f,158 C%.1f,124 %.1f,124 %.1f,160" class="ln" marker-end="url(#ah)"/>' % (wx, wx, tx, tx))
    b.append(T((tx + wx) / 2, 126, "① 指代先行词 teacher", "tb tn", "middle", 13))
    b.append(T(wx, 212, "② 充当连词", "tb tv", "middle", 13))
    x0, x1 = pos[2][0], pos[3][0] + pos[3][1]
    b.append('<path d="M%.1f,222 v8 h%.1f v-8" class="ln"/>' % (x0, x1 - x0))
    b.append(T(x1 + 14, 186, "✓", "tb tn"))
    b.append(T((x0 + x1) / 2, 250, "形容词性从句 · 跟在先行词后面修饰它", "ts", "middle"))
    return svg(264, "".join(b), "关系词的两大作用")


def fig_relatives():
    rows = [
        ("n", "主语关系代词", "who · which · that"),
        ("n", "宾语关系代词（动词宾语）", "who · whom · which · that"),
        ("n", "宾语关系代词（介词宾语）", "who · whom · which"),
        ("d", "状语关系副词", "when · where · why"),
        ("a", "定语关系限定词", "whose · which"),
        ("a", "补语关系代词", "which · that"),
    ]
    b = [box(20, 128, 170, 56, "hl", "关系词", "在从句里充当什么成分？", tcls="tacc")]
    for i, (cls, name, words) in enumerate(rows):
        y = 14 + i * 48
        b.append('<path d="M190,156 C215,156 215,%d 240,%d" class="ln"/>' % (y + 19, y + 19))
        b.append(R(240, y, 420, 38, cls, rx=8))
        b.append(T(256, y + 24, name, "tb t" + cls, fs=14))
        b.append(T(646, y + 24, words, "ten", "end", 14))
    return svg(306, "".join(b), "形容词性从句的关系词框架")


def fig_restrictive():
    b = []
    b.append(T(24, 22, "限制性 · 没有逗号", "tk"))
    s, pos = chips(24, 66, [("I don't wear", "neu"), ("clothes", "n"), ("which make me different from other people.", "a")])
    b.append(s)
    cx = pos[1][0] + pos[1][1] / 2
    ax = pos[2][0] + 40
    b.append('<path d="M%.1f,64 C%.1f,40 %.1f,40 %.1f,64" class="ln" marker-end="url(#ah)"/>' % (ax, ax, cx, cx))
    b.append(T(ax + 12, 48, "只修饰 clothes：某一类衣服", "tb ta", fs=13))
    b.append(T(24, 124, "我不穿那些让我看起来和别人不同的衣服。", "ts"))
    b.append('<line x1="24" y1="142" x2="656" y2="142" class="sep"/>')
    b.append(T(24, 166, "非限制性 · 有逗号", "tk"))
    s, pos = chips(24, 210, [("I don't wear clothes", "hl"), (", which makes me different from other people.", "a")])
    b.append(s)
    cx = pos[0][0] + pos[0][1] / 2
    ax = pos[1][0] + 50
    b.append('<path d="M%.1f,208 C%.1f,184 %.1f,184 %.1f,208" class="ln" marker-end="url(#ah)"/>' % (ax, ax, cx, cx))
    b.append(T(ax + 12, 192, "指代整个主句：「不穿衣服」这件事", "tb tacc", fs=13))
    b.append(T(24, 268, "我不穿衣服，这让我与众不同。", "ts"))
    return svg(284, "".join(b), "限制性与非限制性定语从句")


def fig_adverbial():
    kinds = [("时间", "when · while · before · until"), ("地点", "where · wherever"), ("原因", "because · for · as · since"),
             ("目的", "so that · in case"), ("结果", "so … that · such … that"), ("条件", "if · unless"),
             ("让步", "though · although · as"), ("比较", "than · as … as"), ("方式", "as · as if")]
    b = [box(170, 14, 340, 58, "hl", "主句（谓语 / 表语）", "副词性从句 = 一个副词性成分，修饰主句", tcls="tacc")]
    for i, (k, words) in enumerate(kinds):
        x = 20 + (i % 3) * 216
        y = 112 + (i // 3) * 62
        b.append(R(x, y, 208, 52, "d", rx=8))
        b.append(T(x + 14, y + 22, k, "tb td", fs=14))
        b.append(T(x + 14, y + 42, words, "ten tsm", fs=12.5))
    b.append(arrow(340, 108, 340, 76))
    return svg(310, "".join(b), "副词性从句的九大分类")


def fig_nonfinite():
    left = [("不定式", "to do"), ("动名词", "doing"), ("分词", "doing / done")]
    right = [("n", "名词性", "主语 · 宾语 · 表语 · 补语"), ("a", "形容词性", "定语 · 表语 · 补语"), ("d", "副词性", "状语")]
    b = []
    for i, (name, form) in enumerate(left):
        b.append(box(40, 16 + i * 70, 190, 54, "v", name, form))
    for i, (cls, name, roles) in enumerate(right):
        b.append(box(450, 16 + i * 70, 200, 54, cls, name, roles))
    links = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1), (2, 2)]
    for l, r in links:
        y1 = 43 + l * 70
        y2 = 43 + r * 70
        b.append(arrow(232, y1, 446, y2, mid=(340, (y1 + y2) / 2 + (8 if l != r else 0))))
    b.append(R(40, 232, 610, 40, "neu", rx=8))
    b.append(T(345, 257, "铁律：一句话只有一个谓语动词，其余动词一律用非谓语形式", "tb tink", "middle", 14))
    return svg(286, "".join(b), "非谓语动词对应的词性")


def fig_participle():
    b = [box(20, 14, 315, 40, "v", "现在分词 doing"), box(345, 14, 315, 40, "v", "过去分词 done")]
    cells = [
        (20, 64, "主动 · 正在进行", "a sinking ship", "= a ship that is sinking"),
        (20, 158, "主动 · 一般特质", "a puzzling problem", "= a problem that puzzles people"),
        (345, 64, "及物动词：被动", "a broken cup", "= a cup that has been broken"),
        (345, 158, "不及物动词：主动 · 已完成", "fallen leaves", "= leaves that have fallen"),
    ]
    for x, y, title, ex, eq in cells:
        b.append(R(x, y, 315, 84, "a", rx=8))
        b.append(T(x + 16, y + 26, title, "tb ta", fs=14))
        b.append(T(x + 16, y + 52, ex, "ten tb"))
        b.append(T(x + 16, y + 72, eq, "ten tsm", fs=13))
    return svg(256, "".join(b), "分词的四种意义")


def fig_convert():
    rows = [
        ("n", "名词性从句", "名词 · 动名词 · 不定式", "What you decide will…", "Your decision will…"),
        ("a", "形容词性从句", "形容词 · 介词短语 · 分词", "the flowers that are on the table", "the flowers on the table"),
        ("d", "副词性从句", "不定式 · 介词短语 · 分词", "If you heat water, you can…", "Heating water, you can…"),
    ]
    b = []
    for i, (cls, src, dst, ex1, ex2) in enumerate(rows):
        y = 14 + i * 78
        b.append(box(20, y, 132, 56, cls, src))
        b.append(arrow(154, y + 28, 186, y + 28))
        b.append(box(190, y, 210, 56, "neu", dst, tcls="tink"))
        b.append(T(420, y + 24, ex1, "ten tsm", fs=13))
        b.append(T(420, y + 46, "→ " + ex2, "ten tb t" + cls, fs=13))
    b.append(T(340, 262, "非谓语更简练，但表意要靠上下文「脑补」——混用才是王道", "ts", "middle"))
    return svg(276, "".join(b), "从句与非谓语动词的相互转换")


def fig_framework():
    cols = [
        ("① 词性即成分", ["名词性成分", "形容词性成分", "副词性成分", "动词（谓语）", "两条修饰关系"]),
        ("② 简单句", ["SV 主谓", "SVP 主系表", "SVO 主谓宾", "SVOO 双宾", "SVOC 宾补"]),
        ("③ 从句", ["连词 + 简单句", "名词性从句", "形容词性从句", "副词性从句", "限制 / 非限制"]),
        ("④ 非谓语动词", ["= 从句的简化", "不定式 名/形/副", "动名词 名", "分词 形/副", "与从句互换"]),
    ]
    b = []
    for i, (title, lines) in enumerate(cols):
        x = 12 + i * 168
        b.append(R(x, 12, 150, 214, "neu", rx=10))
        b.append('<path d="M%d,22 a10,10 0 0 1 10,-10 h130 a10,10 0 0 1 10,10 v22 h-150 z" class="hdr"/>' % x)
        b.append(T(x + 75, 36, title, "tb thdr", "middle", 14))
        for j, line in enumerate(lines):
            b.append(T(x + 75, 72 + j * 32, line, "tsm", "middle", 13.5))
        if i < 3:
            b.append(arrow(x + 152, 119, x + 166, 119))
    b.append(R(12, 242, 654, 40, "hl", rx=8))
    b.append(T(339, 267, "两条铁律：一句只有一个谓语动词 · 其余动词必须用非谓语形式", "tb tacc", "middle", 14))
    return svg(296, "".join(b), "全书知识框架")


# exact article line -> (caption, svg function)
FIGURES = [
    ("2. **副词修饰形容词、动词、其他副词**。", "四类成分与两条修饰关系", fig_four_parts),
    ("**介词只有一种用法：介词 + 名词性成分 = 介词短语。**", "介词短语：要么当形容词用，要么当副词用", fig_prep),
    ("| 补语 (Complement) | 补充说明的额外成分 | 名词/形容词属性 |", "句子成分 = 词性属性的具体落位", fig_components),
    ("| SVOC | 主谓宾补 | 主语 + 谓语动词 + 宾语 + 宾语补语 |", "简单句的五种基本句型（颜色 = 词性属性）", fig_five_patterns),
    ("**连词 + 简单句 = 并列结构 or 主从结构**", "简单句 + 简单句，中间必须有连词", fig_conj),
    ("- 步骤三：把连词置于从句的句首。", "独立句子变名词性从句：调语序 → 加连词 → 放进主句", fig_to_clause),
    ("Sally is a teacher who is warm-hearted. (√)（who 既指代 teacher 又起连词作用）", "关系词的两大作用：指代先行词 + 充当连词", fig_antecedent),
    ("- 补语关系代词：which、that", "形容词性从句的关系词框架", fig_relatives),
    ("- I don't wear clothes, **which** makes me different from other people.（我不穿衣服，这让我与众不同。）", "一个逗号，天壤之别", fig_restrictive),
    ("| 方式 | The cat jumped out **as** a tiger jumped at prey. |", "副词性从句的九大分类", fig_adverbial),
    ("| 分词 | × | × | 形容词 / 副词 | 同上 |", "非谓语动词 = 失去谓语身份、保留动词特征的名词 / 形容词 / 副词", fig_nonfinite),
    ("- *returned* students = students who have returned", "分词的四种意义", fig_participle),
    ("- 副词性从句 → 不定式、介词短语、分词……", "从句 ⇄ 非谓语动词", fig_convert),
    ("## 全书知识框架总结", "全书知识框架一览", fig_framework),
]
