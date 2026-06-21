"""Convert HTML to clean plain text using the standard library only.

No BeautifulSoup, no lxml: a small ``HTMLParser`` subclass drops ``<script>`` and
``<style>`` content, turns block elements into line breaks, and collapses runs of
whitespace - enough to feed an LLM, a digest, or a search index.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

_BLOCK_TAGS = {
    "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "header", "footer", "ul", "ol", "table", "blockquote",
}
_DROP_TAGS = {"script", "style", "head", "noscript"}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: object) -> None:
        if tag in _DROP_TAGS:
            self._skip_depth += 1
        elif tag in _BLOCK_TAGS:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _DROP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        elif tag in _BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            self._parts.append(data)

    def text(self) -> str:
        return "".join(self._parts)


def html_to_text(html: str) -> str:
    """Return readable plain text extracted from an HTML string."""
    parser = _TextExtractor()
    parser.feed(html)
    raw = parser.text()
    # Collapse intra-line whitespace, then trim blank-line runs to at most one.
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
    out: list[str] = []
    blank = False
    for line in lines:
        if line:
            out.append(line)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip()


if __name__ == "__main__":  # pragma: no cover
    import sys

    print(html_to_text(sys.stdin.read()))
