"""User-authored text renders as text, never as markup (CU-123z74bznuv).

Renderer passes this HTML to WeasyPrint with `| safe`, so anything that escapes
here becomes real markup in the PDF, e.g. an `<img>` WeasyPrint fetches.
"""
import base64

import pytest

from tiptapy import BaseDoc

_SVG_FETCHING_FILE = base64.b64encode(
    b'<svg xmlns="http://www.w3.org/2000/svg"><image href="file:///etc/passwd"/></svg>'
).decode()


class config:
    DOMAIN = "python.org"


def _paragraph(text, marks=None):
    node = {"type": "text", "text": text}
    if marks:
        node["marks"] = marks
    return {"type": "doc", "content": [{"type": "paragraph", "content": [node]}]}


@pytest.mark.parametrize(
    "payload",
    [
        "<img src=x onerror=alert(1)>",
        "<link rel=attachment href=file:///etc/passwd>",
        # Passes the HTML validator, so it used to be emitted raw.
        '<img src="file:///etc/passwd">',
    ],
)
def test_html_in_text_renders_as_text(payload):
    html = BaseDoc(config).render(_paragraph(payload))
    assert "<img" not in html and "<link" not in html
    assert "&lt;" in html


@pytest.mark.parametrize(
    "payload",
    [
        '<img src="file:///etc/passwd">',
        "<img src=http://169.254.169.254/latest/meta-data/>",
        "<a rel=attachment href=file:///etc/passwd>x</a>",
        '<svg><use href="file:///etc/passwd#x"></use></svg>',
        '<span style="background: url(file:///etc/passwd)">x</span>',
        # An inline SVG fetches its own `<image href>`, and WeasyPrint parses any
        # image Pillow can't open as SVG, so the declared type proves nothing.
        f'<img src="data:image/svg+xml;base64,{_SVG_FETCHING_FILE}">',
        f'<img src="data:image/png;base64,{_SVG_FETCHING_FILE}">',
        '<img src="data:image/png,%89PNG">',
    ],
)
def test_dynamic_table_cell_html_cannot_make_weasyprint_fetch(payload):
    """Cells go through `safe_html`, which emits HTML the validator accepts as-is."""
    doc = {
        "type": "doc",
        "content": [
            {"type": "dynamicTable", "attrs": {"content": {"headers": ["c"], "rows": [[payload]]}}}
        ],
    }
    html = BaseDoc(config).render(doc)
    assert payload not in html
    assert "&lt;" in html


@pytest.mark.parametrize("image", ["data:image/png;base64,iVBORw0KGgo=", "data:image/jpeg;base64,/9j/4AAQ"])
def test_dynamic_table_cell_keeps_renderer_inline_images_and_anchors(image):
    cell = f'<img src="{image}" alt="f.png"><a href="#embedded-file-1-appendix">f.pdf</a>'
    doc = {
        "type": "doc",
        "content": [{"type": "dynamicTable", "attrs": {"content": {"headers": ["c"], "rows": [[cell]]}}}],
    }
    assert cell in BaseDoc(config).render(doc)


def test_link_attrs_cannot_break_out_of_the_tag():
    mark = {"type": "link", "attrs": {"href": 'x" onmouseover="y', "a b=c": "d"}}
    html = BaseDoc(config).render(_paragraph("t", [mark]))
    assert '<a href="x&#34; onmouseover=&#34;y"' in html
    assert "b=c" not in html


def test_render_does_not_mutate_the_input():
    doc = _paragraph("t", [{"type": "link", "attrs": {"href": "https://example.com"}}])
    BaseDoc(config).render(doc)
    assert doc["content"][0]["content"][0]["marks"][0]["attrs"] == {"href": "https://example.com"}
