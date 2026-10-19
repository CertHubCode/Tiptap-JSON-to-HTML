"""User-authored text renders as text, never as markup (CU-123z74bznuv).

Renderer passes this HTML to WeasyPrint with `| safe`, so anything that escapes
here becomes real markup in the PDF, e.g. an `<img>` WeasyPrint fetches.
"""
import pytest

from tiptapy import BaseDoc


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


def test_link_attrs_cannot_break_out_of_the_tag():
    mark = {"type": "link", "attrs": {"href": 'x" onmouseover="y', "a b=c": "d"}}
    html = BaseDoc(config).render(_paragraph("t", [mark]))
    assert '<a href="x&#34; onmouseover=&#34;y"' in html
    assert "b=c" not in html


def test_render_does_not_mutate_the_input():
    doc = _paragraph("t", [{"type": "link", "attrs": {"href": "https://example.com"}}])
    BaseDoc(config).render(doc)
    assert doc["content"][0]["content"][0]["marks"][0]["attrs"] == {"href": "https://example.com"}
