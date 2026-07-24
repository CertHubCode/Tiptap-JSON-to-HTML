import re
from html import unescape

from markdown_it import MarkdownIt
from markupsafe import Markup

from .html_validator import is_valid_html

# Matches the feature set the Tiptap editor previews markdown with, so a field
# renders the same in the PDF as it did while the author was typing it:
# CommonMark, plus tables, strikethrough, linkified bare URLs and footnotes.
# `html: False` keeps any raw HTML in the field value escaped.
#
# Linkified bare URLs need linkify-it-py and footnotes need mdit-py-plugins.
# Both are pinned in requirements.txt, but they are picked up optionally so an
# environment that has not installed them yet still boots the renderer with
# those two features off, rather than failing at import time.
_md_options = {"html": False, "breaks": True}

try:
    import linkify_it  # noqa: F401
except ModuleNotFoundError:
    _linkify_available = False
else:
    _linkify_available = True
    _md_options["linkify"] = True

_md = MarkdownIt("commonmark", _md_options).enable(["table", "strikethrough"])

if _linkify_available:
    _md.enable("linkify")

try:
    from mdit_py_plugins.footnote import footnote_plugin
except ModuleNotFoundError:
    pass
else:
    _md.use(footnote_plugin)

# Matches output that is a single top level paragraph, so inline fields can drop
# the <p> wrapper and keep flowing with the surrounding text.
_single_paragraph_re = re.compile(r"^<p>(.*)</p>$", re.DOTALL)

# Keep in sync with Frontend linkedEntityDisplayLabels.ts and
# app/utils/linked_entity_display_labels.py
_LINKED_TO_TRACED_DISPLAY_LABELS: dict[str, str] = {
    "Linked SOPs": "Traced SOPs",
    "Linked Work Instructions": "Traced Work Instructions",
    "Linked Products": "Traced Products",
    "Linked Documents": "Traced Documents",
    "Linked Global Element Entries": "Traced Global Element Entries",
    "Linked Files": "Traced Files",
    "Linked Forms Details": "Traced Forms Details",
    "Linked Background Information": "Traced Background Information",
}


def to_traced_display_label_filter(label: str) -> str:
    if not isinstance(label, str):
        return label
    return _LINKED_TO_TRACED_DISPLAY_LABELS.get(label, label)


def validate_html_filter(content):
    """Filter to check if content is valid HTML."""
    if not isinstance(content, str):
        return False
    return is_valid_html(content)


def safe_html_filter(content):
    """Filter to safely render HTML content."""
    if not isinstance(content, str):
        return content
    if is_valid_html(content):
        return Markup(content)
    else:
        return content


def markdown_filter(content):
    """Render markdown source as HTML.

    `escape_values_recursive` has already HTML escaped the value by the time it
    reaches this filter, which destroys markdown syntax: `>` becomes `&gt;` so
    blockquotes never parse, and `"` becomes `&quot;` so link and image titles
    never parse. Undo that escaping and let markdown-it produce the output
    instead. That is safe because `_md` is built with `html: False`, so every
    piece of text is re-escaped on the way out and no raw HTML from the source
    survives, and markdown-it rejects `javascript:`/`vbscript:`/`file:`/`data:`
    hrefs in links.
    """
    if not isinstance(content, str) or not content.strip():
        return content

    rendered = _md.render(unescape(content)).strip()
    if rendered.count("<p>") == 1:
        match = _single_paragraph_re.match(rendered)
        if match:
            rendered = match.group(1)
    return Markup(rendered)
