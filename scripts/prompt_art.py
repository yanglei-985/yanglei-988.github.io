"""Line-art illustrations for the prompt library page (content/prompts.md).

Each drawing is inline SVG on a 240x150 canvas, styled only by CSS classes
defined in build_prompts.py, so it follows the site's light/dark theme and the
card's category colour:
  o  = ink outline          c  = category colour fill (soft)
  k  = category colour line  p  = paper fill
  g  = gold accent fill      t  = small mono label text
"""

# A faint ground line + a few dots so every drawing sits on the same "desk".
_GROUND = '<path class="gr" d="M28 128H212"/><circle class="dot" cx="36" cy="22" r="2"/><circle class="dot" cx="206" cy="30" r="2"/><circle class="dot" cx="196" cy="112" r="1.6"/>'

ART = {
    "compass": """
<circle class="c" cx="120" cy="72" r="44"/>
<circle class="o p" cx="120" cy="72" r="34"/>
<path class="o" d="M120 32v8M120 104v8M80 72h8M152 72h8"/>
<path class="g o" d="M120 72l9-25-9 4-9-4z" transform="rotate(35 120 72)"/>
<path class="o p" d="M120 72l9 25-9-4-9 4z" transform="rotate(35 120 72)"/>
<circle class="o p" cx="120" cy="72" r="3.5"/>
<text class="t" x="120" y="26" text-anchor="middle">N</text>
<path class="k" d="M168 104c10-6 20-6 28 2"/>
<path class="k" d="M44 50c8-8 18-10 26-4"/>
""",
    "magnifier": """
<rect class="o p" x="56" y="36" width="78" height="92" rx="6"/>
<path class="k" d="M68 54h40M68 66h52M68 78h30M68 90h46M68 102h26"/>
<circle class="c o" cx="146" cy="78" r="26"/>
<circle class="o" cx="146" cy="78" r="18" fill="none"/>
<path class="o thick" d="M165 97l22 22"/>
<path class="g o" d="M181 113l8-8 9 9-8 8z"/>
<path class="k" d="M138 70a10 10 0 0 1 10-6"/>
""",
    "play": """
<rect class="o p" x="48" y="34" width="144" height="88" rx="10"/>
<rect class="c" x="56" y="42" width="128" height="62" rx="5"/>
<path class="g o" d="M110 60v26l22-13z"/>
<path class="o" d="M56 112h128"/>
<circle class="o p" cx="98" cy="112" r="4"/>
<path class="k" d="M56 112h42"/>
<path class="o" d="M150 26l-12 8M90 26l12 8"/>
""",
    "card": """
<rect class="c o" x="70" y="40" width="112" height="76" rx="8" transform="rotate(6 126 78)"/>
<rect class="o p" x="58" y="34" width="112" height="76" rx="8"/>
<text class="tw" x="114" y="70" text-anchor="middle">word</text>
<path class="k" d="M84 84h60"/>
<path class="o" d="M90 96h48"/>
<path class="g o" d="M176 30l4 10 10 1-8 6 3 10-9-6-9 6 3-10-8-6 10-1z"/>
""",
    "beret": """
<path class="c o" d="M72 70c0-22 26-34 52-32 30 2 46 18 44 32-2 8-18 12-48 12-30 0-48-4-48-12z"/>
<path class="o" d="M124 38c0-6 4-10 8-10"/>
<path class="o p" d="M80 78c14 6 66 6 82 0v8c-16 6-68 6-82 0z"/>
<path class="k" d="M98 106h10M114 106h10M130 106h10"/>
<rect class="o" x="98" y="100" width="44" height="14" rx="2" fill="none"/>
<path class="g" d="M98 100h15v14H98z"/>
<path class="c" d="M127 100h15v14h-15z"/>
""",
    "tree": """
<rect class="g o" x="102" y="28" width="36" height="20" rx="4"/>
<path class="o" d="M120 48v12M76 60h88M76 60v12M120 60v12M164 60v12"/>
<rect class="c o" x="58" y="72" width="36" height="18" rx="4"/>
<rect class="o p" x="102" y="72" width="36" height="18" rx="4"/>
<rect class="c o" x="146" y="72" width="36" height="18" rx="4"/>
<path class="o" d="M120 90v10M104 100h32M104 100v8M136 100v8"/>
<rect class="o p" x="92" y="108" width="24" height="14" rx="3"/>
<rect class="o p" x="124" y="108" width="24" height="14" rx="3"/>
""",
    "columns": """
<rect class="o p" x="44" y="34" width="152" height="90" rx="6"/>
<path class="o" d="M120 34v90"/>
<rect class="c" x="52" y="44" width="60" height="12" rx="3"/>
<rect class="c" x="52" y="64" width="44" height="12" rx="3"/>
<rect class="c" x="52" y="84" width="54" height="12" rx="3"/>
<rect class="c" x="52" y="104" width="36" height="12" rx="3"/>
<path class="k" d="M130 50h52M130 70h40M130 90h48M130 110h30"/>
<path class="g o" d="M114 66l8 4-8 4z"/>
""",
    "boxes": """
<rect class="c o" x="46" y="80" width="46" height="40" rx="4"/>
<rect class="o p" x="98" y="80" width="46" height="40" rx="4"/>
<rect class="g o" x="150" y="80" width="46" height="40" rx="4"/>
<path class="o" d="M46 92h46M98 92h46M150 92h46"/>
<rect class="o p" x="60" y="44" width="22" height="14" rx="2" transform="rotate(-12 71 51)"/>
<rect class="o p" x="108" y="34" width="22" height="14" rx="2" transform="rotate(8 119 41)"/>
<rect class="o p" x="158" y="48" width="22" height="14" rx="2" transform="rotate(-6 169 55)"/>
<path class="k dash" d="M71 60l-2 18M119 50l1 28M169 64l3 14"/>
""",
    "book": """
<path class="o p" d="M120 50c-18-10-40-12-62-8v76c22-4 44-2 62 8z"/>
<path class="c o" d="M120 50c18-10 40-12 62-8v76c-22-4-44-2-62 8z"/>
<path class="o" d="M120 50v76"/>
<path class="k" d="M70 62c12-2 26-1 38 4M70 76c12-2 26-1 38 4M70 90c12-2 26-1 38 4"/>
<path class="g o" d="M150 26c6 0 8 6 4 10s-12 2-12-4 4-6 8-6z"/>
<path class="o" d="M160 30l8-4M142 26l-6-4"/>
<circle class="o p" cx="152" cy="80" r="10"/>
<path class="o" d="M146 92l-4 14M158 92l4 14"/>
""",
    "glasses": """
<rect class="o p" x="52" y="30" width="136" height="72" rx="4"/>
<text class="tw" x="74" y="58">avidement</text>
<path class="k" d="M74 70h70M74 82h50"/>
<circle class="c o" cx="96" cy="112" r="15"/>
<circle class="c o" cx="144" cy="112" r="15"/>
<path class="o" d="M111 110c4-4 14-4 18 0M81 108l-16-6M159 108l16-6"/>
<path class="g" d="M170 36h12v12h-12z"/>
""",
    "bulb": """
<path class="g o" d="M120 30c-22 0-36 16-36 34 0 14 8 22 14 30 4 5 4 10 4 14h36c0-4 0-9 4-14 6-8 14-16 14-30 0-18-14-34-36-34z"/>
<path class="o" d="M106 116h28M108 124h24"/>
<path class="o" d="M112 108c0-14 2-22 8-30 6 8 8 16 8 30"/>
<path class="k" d="M64 46l-12-6M60 72H46M176 46l12-6M180 72h14M120 18V8"/>
<path class="c o" d="M168 96c0-8 10-12 16-6s-2 14-8 14l-6 6v-6c-2 0-2-4-2-8z"/>
""",
    "paper": """
<path class="o p" d="M70 28h72l26 26v72H70z"/>
<path class="o c" d="M142 28v26h26z"/>
<path class="k" d="M84 50h40M84 64h70M84 76h70M84 88h50"/>
<rect class="g" x="82" y="98" width="56" height="10" rx="2"/>
<path class="o" d="M84 116h40"/>
<path class="o thick" d="M178 70l-30 44"/>
<path class="o p" d="M176 66l8 6-4 6-8-6z"/>
""",
    "pen": """
<path class="o p" d="M52 118c40-4 70-22 92-56"/>
<path class="k" d="M52 118c24-2 42-8 56-18"/>
<path class="c o" d="M150 36l30 30-48 48-36 6 6-36z"/>
<path class="o" d="M102 120l20-20M150 36l30 30"/>
<path class="g o" d="M158 28l8-8 30 30-8 8z"/>
<circle class="o p" cx="118" cy="104" r="4"/>
""",
    "wrench": """
<path class="c o" d="M150 34a26 26 0 0 0-26 34L70 122l14 14 54-54a26 26 0 0 0 34-26l-14 14-14-4-4-14z" transform="translate(-6 -10)"/>
<circle class="o p" cx="74" cy="118" r="4" transform="translate(-6 -10)"/>
<path class="o p" d="M150 92l26 26-10 10-26-26z"/>
<path class="g o" d="M134 76l16 16-8 8-16-16z"/>
<path class="k" d="M52 40l10 6M50 60h12M176 36l-6 10"/>
""",
    "scale": """
<path class="o" d="M120 32v84M90 124h60M66 48h108"/>
<circle class="g o" cx="120" cy="40" r="7"/>
<path class="o" d="M66 48l-18 36M66 48l18 36M174 48l-18 30M174 48l18 30"/>
<path class="c o" d="M44 84h44c0 12-10 18-22 18s-22-6-22-18z"/>
<path class="o p" d="M152 78h44c0 12-10 18-22 18s-22-6-22-18z"/>
<text class="t" x="66" y="76" text-anchor="middle">A</text>
<text class="t" x="174" y="70" text-anchor="middle">B</text>
""",
}


def art(name):
    body = ART.get(name, ART["compass"])
    return ('<svg viewBox="0 0 240 150" aria-hidden="true" focusable="false">'
            + _GROUND + body.strip() + '</svg>')
