import pkgutil
import re
from string import Template
from urllib.parse import urlparse

from markupsafe import Markup, escape

# Templates are autoescaped, so every helper here that returns HTML returns
# `Markup` and escapes the values it interpolates itself.

# An attribute name that cannot end the tag or start a second attribute: no
# whitespace, quotes, `=`, `/` or `>`.
_ATTR_NAME = re.compile(r"[A-Za-z_:][\w:.-]*")


def html_attrs(attrs, prefix=""):
    """``attrs`` as ``' name="value"'`` pairs, values escaped. Pairs whose
    value is ``None`` or whose name is not a plain attribute name (e.g. a key
    like ``x onload=…``) are dropped."""
    return Markup("").join(
        Markup(' {}{}="{}"').format(prefix, name, value)
        for name, value in (attrs or {}).items()
        if value is not None and isinstance(name, str) and _ATTR_NAME.fullmatch(name)
    )


# added only for parent nodes
def extract_tag_attrs(node):
    allowed_attributes = ("id",)
    attrs = node.get("attrs") or {}
    return html_attrs({attr: attrs[attr] for attr in allowed_attributes if attr in attrs})


# A CSS colour as the editor stores it: `#rrggbb`, `rgb(…)` / `rgba(…)`, a
# colour name or a `var(--…)` reference. Anything else (quotes, semicolons,
# `url(…)`, `expression(…)`) is dropped rather than printed into the page.
_CSS_COLOR = re.compile(
    r"^(#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
    r"|[a-zA-Z]+|rgba?\([\d\s.,%]+\)|hsla?\([\d\s.,%]+\)|var\(--[\w-]+\))$"
)
_TEXT_ALIGNS = ("left", "center", "right", "justify")
_VERTICAL_ALIGNS = ("top", "middle", "bottom")


def _css_color(value):
    value = (value or "").strip() if isinstance(value, str) else ""
    return value if _CSS_COLOR.match(value) else ""


def extract_node_style(node):
    """The ``style`` attribute a block or table cell carries in the editor.

    The editor keeps its toolbar formatting as node attrs: ``textAlign``
    (TextAlign extension on paragraphs/headings), ``nodeTextAlign`` /
    ``nodeVerticalAlign`` (NodeAlignment on table cells) and
    ``backgroundColor`` (NodeBackground on blocks and cells). Returns
    ``' style="…"'`` or an empty string.

    ``left`` is the editor's default alignment and is NOT printed — the
    editor's own renderHTML omits it too — so a paragraph inside a centred
    cell keeps the cell's alignment instead of overriding it with the default.
    """
    attrs = node.get("attrs") or {}
    declarations = []
    text_align = attrs.get("nodeTextAlign") or attrs.get("textAlign")
    if text_align in _TEXT_ALIGNS and text_align != "left":
        declarations.append(f"text-align: {text_align}")
    vertical_align = attrs.get("nodeVerticalAlign")
    if vertical_align in _VERTICAL_ALIGNS:
        declarations.append(f"vertical-align: {vertical_align}")
    background = _css_color(attrs.get("backgroundColor"))
    if background:
        declarations.append(f"background-color: {background}")
    return html_attrs({"style": "; ".join(declarations)}) if declarations else Markup("")


def extract_cell_attrs(cell):
    """``colspan`` / ``rowspan`` (when they merge cells) plus the cell's style."""
    attrs = cell.get("attrs") or {}
    spans = {}
    for span in ("colspan", "rowspan"):
        value = attrs.get(span)
        if isinstance(value, int) and value > 1:
            spans[span] = value
    return html_attrs(spans) + extract_node_style(cell)


def image_src_url(src):
    """The URL of an image node's ``src``.

    The original tiptapy image node stores ``src`` as ``{"image", "fallback"}``;
    Tiptap's stock ``image`` node (what the editor's page header/footer uses
    for a logo) stores a plain URL string.
    """
    if isinstance(src, dict):
        return (src.get("fallback") or "").strip()
    if isinstance(src, str):
        return src.strip()
    return ""


def make_img_src(attrs):
    alt = (attrs.get("alt") or "").strip()
    height = attrs.get("height", "")
    width = attrs.get("width", "")
    # The stock image node carries the toolbar alignment as `textAlign`
    # (rendered as `data-align` in the editor, so the print CSS can place a
    # left/right-aligned logo the same way).
    align = (attrs.get("textAlign") or "").strip()
    fallback_url = image_src_url(attrs.get("src"))
    return Markup("img") + html_attrs(
        {
            "src": fallback_url,
            "alt": alt or None,
            "width": width or None,
            "height": height or None,
            "data-align": align or None,
        }
    )


def build_link_handler(config):
    def handle_links(attrs):
        retval = None
        if attrs:
            # A copy: the target/rel added below must not leak into the
            # caller's document JSON.
            attrs = dict(attrs)
            url = attrs.get("href", "").strip()
            link = urlparse(url)
            if not (
                link.netloc == config.DOMAIN
                or link.netloc.endswith(f".{config.DOMAIN}")
            ):
                attrs["target"] = "_blank"
                attrs["rel"] = "noopener nofollow"
            retval = html_attrs(attrs).lstrip()
        return retval

    return handle_links


def get_audio_player_block():
    audio_player_block = pkgutil.get_data(
        __name__, "templates/stack-audio-player.html"
    ).decode()
    return Markup(audio_player_block)


def get_doc_block(ext, fname, size, src):
    document_block = pkgutil.get_data(
        __name__, "templates/stack-document.html"
    ).decode()
    document = Template(document_block)
    html = document.substitute(
        fileformat=escape(ext[:4]),
        filename=escape(fname),
        filesize=escape(size),
        filesrc=escape(src),
    )
    return Markup(html)
