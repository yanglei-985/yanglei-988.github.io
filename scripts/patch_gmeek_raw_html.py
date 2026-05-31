#!/usr/bin/env python3
"""Patch Gmeek to preserve Obsidian-style raw HTML tag attributes in Markdown.

Gmeek renders Markdown through GitHub's /markdown API. That API keeps many raw
HTML tags but sanitizes attributes such as style/data-*, so rich Markdown
exported from Obsidian or WeChat-style editors loses its layout.

This patch wraps Gmeek.markdown2html so raw block-level HTML tag lines are
replaced with placeholders before calling GitHub, then restored afterward. Only
the tag lines are protected, so Markdown between tags is still rendered by
GitHub GFM.
"""
from pathlib import Path
import sys

TARGET = Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/Gmeek/Gmeek.py")
text = TARGET.read_text(encoding="utf-8")

if "def _extract_raw_html_tags" in text:
    print("Gmeek raw HTML tag patch already applied")
    raise SystemExit(0)

old = '''    def markdown2html(self, mdstr):\n        payload = {"text": mdstr, "mode": "gfm"}\n        headers = {"Authorization": "token {}".format(self.options.github_token)}\n        try:\n            response = requests.post("https://api.github.com/markdown", json=payload, headers=headers)\n            response.raise_for_status()  # Raises an exception if status code is not 200\n            return response.text\n        except requests.RequestException as e:\n            raise Exception("markdown2html error: {}".format(e))\n'''
new = '''    def _extract_raw_html_tags(self, mdstr):\n        # Preserve common block-level HTML tag lines whose attributes are\n        # normally stripped by GitHub's Markdown API. Only tag lines are\n        # replaced, so Markdown between opening/closing tags is still rendered.\n        preserve_tags = {\n            "section", "div", "article", "aside", "main", "header", "footer",\n            "nav", "figure", "figcaption", "details", "summary", "table",\n            "thead", "tbody", "tfoot", "tr", "td", "th", "blockquote",\n            "p", "span"\n        }\n        attr_markers = (" style=", " data-", " class=", " id=", " label=")\n        tags = []\n        out = []\n\n        # Match a line that is just one raw HTML opening/self-closing/closing tag.\n        # This covers Obsidian-style layout wrappers like:\n        # <section data-role="outer" style="...">\n        tag_line_re = re.compile(r'^(\\s*)<(/?)([A-Za-z][A-Za-z0-9-]*)([^<>]*)>(\\s*)$')\n\n        for line in mdstr.splitlines(keepends=True):\n            line_body = line[:-1] if line.endswith('\\n') else line\n            newline = '\\n' if line.endswith('\\n') else ''\n            match = tag_line_re.match(line_body)\n            if match:\n                tag_name = match.group(3).lower()\n                lower_line = line_body.lower()\n                has_preserved_attr = any(marker in lower_line for marker in attr_markers)\n                is_closing_tag = match.group(2) == '/'\n                if tag_name in preserve_tags and (has_preserved_attr or is_closing_tag):\n                    token = "GMEK_RAW_HTML_TAG_%d" % len(tags)\n                    tags.append((token, line_body.strip()))\n                    out.append("\\n\\n" + token + "\\n\\n" + newline)\n                    continue\n            out.append(line)\n        return ''.join(out), tags\n\n    def _restore_raw_html_tags(self, htmlstr, tags):\n        for token, raw_tag in tags:\n            htmlstr = re.sub(r'<p>\\s*' + re.escape(token) + r'\\s*</p>', raw_tag, htmlstr)\n            htmlstr = htmlstr.replace(token, raw_tag)\n        return htmlstr\n\n    def markdown2html(self, mdstr):\n        mdstr, raw_html_tags = self._extract_raw_html_tags(mdstr)\n        payload = {"text": mdstr, "mode": "gfm"}\n        headers = {"Authorization": "token {}".format(self.options.github_token)}\n        try:\n            response = requests.post("https://api.github.com/markdown", json=payload, headers=headers)\n            response.raise_for_status()  # Raises an exception if status code is not 200\n            return self._restore_raw_html_tags(response.text, raw_html_tags)\n        except requests.RequestException as e:\n            raise Exception("markdown2html error: {}".format(e))\n'''
if old not in text:
    raise SystemExit("Cannot find original markdown2html block in Gmeek.py; upstream may have changed")
text = text.replace(old, new, 1)
TARGET.write_text(text, encoding="utf-8")
print("Applied Gmeek raw HTML tag preservation patch to", TARGET)
