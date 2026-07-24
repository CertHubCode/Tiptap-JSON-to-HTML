import pytest

from tiptapy.jinja_filters import markdown_filter


@pytest.mark.parametrize(
    "source, expected",
    [
        # Plain text stays inline, no <p> wrapper.
        ("text field value", "text field value"),
        ("**bold**", "<strong>bold</strong>"),
        ("_italic_", "<em>italic</em>"),
        ("`code`", "<code>code</code>"),
        ("~~gone~~", "<s>gone</s>"),
        (
            "[link](https://example.com)",
            '<a href="https://example.com">link</a>',
        ),
        # Block level markdown keeps its own tags.
        ("- one\n- two", "<ul>\n<li>one</li>\n<li>two</li>\n</ul>"),
        ("# Heading\n\npara", "<h1>Heading</h1>\n<p>para</p>"),
    ],
)
def test_markdown_is_rendered(source, expected):
    assert markdown_filter(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        # Values reaching the filter are already HTML escaped upstream; the
        # entities must survive the markdown round trip.
        ("a &amp; b", "a &amp; b"),
        (
            "&lt;script&gt;alert(1)&lt;/script&gt;",
            "&lt;script&gt;alert(1)&lt;/script&gt;",
        ),
        # Raw HTML is never trusted, `html: False` escapes it.
        ("<b>raw</b>", "&lt;b&gt;raw&lt;/b&gt;"),
        # markdown-it refuses these hrefs, so the link stays literal text.
        ("[x](javascript:alert(1))", "[x](javascript:alert(1))"),
    ],
)
def test_html_stays_escaped(source, expected):
    assert markdown_filter(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        # `>` arrives as `&gt;`, so blockquotes only parse after unescaping.
        ("&gt; quoted", "<blockquote>\n<p>quoted</p>\n</blockquote>"),
        # `"` arrives as `&quot;`, so link titles only parse after unescaping.
        (
            "[t](http://example.com &quot;title text&quot;)",
            '<a href="http://example.com" title="title text">t</a>',
        ),
    ],
)
def test_upstream_escaping_does_not_break_syntax(source, expected):
    assert markdown_filter(source) == expected


def test_bare_urls_are_linkified():
    pytest.importorskip("linkify_it")
    assert markdown_filter("see https://example.com now") == (
        'see <a href="https://example.com">https://example.com</a> now'
    )


def test_footnotes_render_a_footnote_section():
    pytest.importorskip("mdit_py_plugins")
    rendered = markdown_filter("text[^a]\n\n[^a]: the note")
    assert 'class="footnote-ref"' in rendered
    assert 'class="footnotes"' in rendered
    assert "the note" in rendered


@pytest.mark.parametrize("value", ["", "   ", None, 123])
def test_non_markdown_values_pass_through(value):
    assert markdown_filter(value) == value
