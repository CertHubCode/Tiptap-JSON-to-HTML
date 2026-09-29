import pkgutil
from string import Template
from urllib.parse import urlparse


# added only for parent nodes
def extract_tag_attrs(node):
    allowed_attributes = ("id",)
    attrs = node.get("attrs")
    return (
        "".join(
            f' {attr}="{attrs[attr]}"' for attr in allowed_attributes if attr in attrs
        )
        if attrs
        else ""
    )


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
    img = f'img src="{fallback_url}"'
    if alt:
        img += f' alt="{alt}"'
    if width:
        img += f' width="{width}"'
    if height:
        img += f' height="{height}"'
    if align:
        img += f' data-align="{align}"'

    return img


def build_link_handler(config):
    def handle_links(attrs):
        retval = None
        if attrs:
            url = attrs.get("href", "").strip()
            link = urlparse(url)
            if not (
                link.netloc == config.DOMAIN
                or link.netloc.endswith(f".{config.DOMAIN}")
            ):
                attrs["target"] = "_blank"
                attrs["rel"] = "noopener nofollow"
            retval = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v is not None)
        return retval

    return handle_links


def get_audio_player_block():
    audio_player_block = pkgutil.get_data(
        __name__, "templates/stack-audio-player.html"
    ).decode()
    return audio_player_block


def get_doc_block(ext, fname, size, src):
    document_block = pkgutil.get_data(
        __name__, "templates/stack-document.html"
    ).decode()
    document = Template(document_block)
    html = document.substitute(
        fileformat=ext[:4], filename=fname, filesize=size, filesrc=src
    )
    return html
