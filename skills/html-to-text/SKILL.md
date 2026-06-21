---
name: html-to-text
description: "Strip HTML to clean plain text with the standard library only (no BeautifulSoup/lxml): drops script/style, turns block tags into line breaks, and collapses whitespace. Use when the user wants readable text from an HTML page/email, to clean scraped HTML before sending it to an LLM, or to build a text index from web content."
version: "1.0.0"
---

# HTML to Text

Use this skill when you have HTML - a scraped page, a newsletter body, a feed entry's content - and you want clean, readable plain text without adding `beautifulsoup4` or `lxml`. A small `HTMLParser` subclass removes `<script>`/`<style>`, converts block elements into newlines, and collapses whitespace, which is exactly the shape you want before sending content to an LLM (fewer tokens) or into a search index.

## When to invoke

- User says: "get the text out of this HTML", "clean this scraped page", "strip tags before summarizing", "convert this email HTML to text".
- HTML is about to be fed to a model or a digest and the markup is just noise.

## When NOT to invoke

- You need to keep structure (tables, links as Markdown) - use a real HTML-to-Markdown converter.
- The page is rendered by JavaScript - fetch it with a headless browser first, then convert.

## Concrete example

User input:

```text
Turn this article HTML into plain text so I can summarize it with fewer tokens.
```

Output:

```python
# Copy assets/htmltext.py into your project, then:
from htmltext import html_to_text

text = html_to_text(article_html)
summary = call_llm(f"Summarize:\n{text}")
```

`<script>` and `<style>` blocks are dropped entirely, block tags become line breaks, and runs of spaces/blank lines are collapsed, so the output reads like prose.

## Pattern to apply

1. Subclass `html.parser.HTMLParser` with `convert_charrefs=True` so entities decode automatically.
2. Track a skip-depth for `script`/`style`/`head` so their text never leaks into the output.
3. Emit newlines around block tags, then collapse intra-line whitespace and multi-blank runs.
4. Keep it pure (string in, string out) so it is trivial to unit test.

Reference: `assets/htmltext.py`.

## Source

Distilled from the author's scraping and digest pipelines. v1.0.0.
See also: [[rss-feed-reader]], [[gemini-cost-tracker]], [[pipeline-orchestrator]].

→ Build the full runnable bot with Trawlkit.
