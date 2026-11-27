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


def _reference(content):
    node = {"type": "dynamic-text-content", "attrs": {"type": "rich", "content": content, "entity_type": "SOP"}}
    return {"type": "doc", "content": [{"type": "paragraph", "content": [node]}]}


def test_rich_reference_prints_its_source_html_as_formatting():
    """A reference carries its source's stored HTML (CU-123z74ccj33): the PDF printed it as text."""
    content = '<h2>Purpose</h2><p><span style="font-size: 14px">Instruments are disinfected.</span></p>'
    html = BaseDoc(config).render(_reference(content))
    assert '<h2>Purpose</h2><p><span style="font-size:14px">Instruments are disinfected.</span></p>' in html
    assert "&lt;" not in html


def test_paragraph_holding_a_rich_reference_is_not_a_p():
    """An HTML parser closes a <p> at the reference's first <h2> or <p>, which moves the
    reference content out of its span, so the PDF's reference styles miss it."""
    html = BaseDoc(config).render(_reference("<h2>Purpose</h2>"))
    assert html.startswith("<div>") and html.endswith("</div>")
    plain = {"type": "dynamic-text-content", "attrs": {"type": "plain", "content": "Purpose"}}
    html = BaseDoc(config).render({"type": "doc", "content": [{"type": "paragraph", "content": [plain]}]})
    assert html.startswith("<p>")


def test_rich_reference_keeps_its_images():
    """One image used to fail the whole-content check, so the reference printed as raw tags."""
    content = '<h2>Purpose</h2><p>Flow: <img src="https://assets.certhub.de/flow.png" alt="flow"></p>'
    html = BaseDoc(config).render(_reference(content))
    assert "<h2>Purpose</h2>" in html
    assert 'src="https://assets.certhub.de/flow.png"' in html


def test_marks_wrap_the_reference_so_its_size_mark_survives():
    """Renderer makes everything inside the reference inherit the sentence's size; a size mark
    set on the reference itself sits outside it, as in the editor."""
    node = {"type": "dynamic-text-content", "attrs": {"type": "plain", "content": "Purpose"},
            "marks": [{"type": "textStyle", "attrs": {"fontSize": "18px"}}]}
    html = BaseDoc(config).render({"type": "doc", "content": [{"type": "paragraph", "content": [node]}]})
    assert '<span style="font-size: 18px"><span class="dynamic-text-content">Purpose</span></span>' in html


def test_a_linked_reference_drops_the_links_inside_it():
    """A link inside a link: the HTML parser closes the outer one and moves the content out of
    the reference, so Renderer's reference styles miss it. The inner link keeps its text."""
    content = '<p><a href="https://certhub.de/plan">See the plan</a> now</p>'
    node = {"type": "dynamic-text-content", "attrs": {"type": "rich", "content": content},
            "marks": [{"type": "link", "attrs": {"href": "https://certhub.de/sop"}}]}
    html = BaseDoc(config).render({"type": "doc", "content": [{"type": "paragraph", "content": [node]}]})
    assert html.count("<a ") == 1
    assert '<span class="dynamic-text-content"><p>See the plan now</p></span>' in html
    assert '<a href="https://certhub.de/plan">See the plan</a>' in BaseDoc(config).render(_reference(content))


@pytest.mark.parametrize(
    "payload",
    [
        '<img src="file:///etc/passwd">',
        "<img src=http://169.254.169.254/latest/meta-data/>",
        f'<img src="data:image/svg+xml;base64,{_SVG_FETCHING_FILE}">',
        "<script>alert(1)</script>",
        "<a rel=attachment href=file:///etc/passwd>x</a>",
        '<span style="background: url(file:///etc/passwd)">x</span>',
        # Hide a tag from a different HTML parser than WeasyPrint's.
        '<p>x<!--><a rel="attachment" href="file:///etc/passwd">y</a>--></p>',
        '<p>x<![CDATA[><a rel="attachment" href="file:///etc/passwd">y</a>]]></p>',
    ],
)
def test_rich_reference_html_cannot_make_weasyprint_fetch(payload):
    """Unsafe parts are removed, the rest prints (CU-123z74bznuv)."""
    html = BaseDoc(config).render(_reference(payload))
    for unsafe in ("file:", "169.254", "data:image/svg", "<script", "alert(1)"):
        assert unsafe not in html


def test_link_attrs_cannot_break_out_of_the_tag():
    mark = {"type": "link", "attrs": {"href": 'x" onmouseover="y', "a b=c": "d"}}
    html = BaseDoc(config).render(_paragraph("t", [mark]))
    assert '<a href="x&#34; onmouseover=&#34;y"' in html
    assert "b=c" not in html


def test_render_does_not_mutate_the_input():
    doc = _paragraph("t", [{"type": "link", "attrs": {"href": "https://example.com"}}])
    BaseDoc(config).render(doc)
    assert doc["content"][0]["content"][0]["marks"][0]["attrs"] == {"href": "https://example.com"}
