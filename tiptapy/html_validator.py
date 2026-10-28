from bs4 import BeautifulSoup
import base64
import binascii
import re
from typing import Tuple, List


class HTMLValidator:
    STANDARD_HTML_TAGS = {
        'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside',
        'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote',
        'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code',
        'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn',
        'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset',
        'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html',
        'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label',
        'legend', 'li', 'link', 'main', 'map', 'mark', 'menu', 'menuitem',
        'meta', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol',
        'optgroup', 'option', 'output', 'p', 'param', 'picture', 'plaintext',
        'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script',
        'section', 'select', 'small', 'source', 'span', 'strike', 'strong',
        'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'template',
        'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
        'tt', 'u', 'ul', 'var', 'video', 'wbr', 'xmp',
        # Additional common tags
        'c', 'abbr', 'acronym', 'big', 'center', 'dir', 'font', 'isindex',
        'listing', 'plaintext', 'strike', 'tt', 'xmp',
        # SVG elements
        'svg', 'circle', 'rect', 'line', 'polyline', 'polygon', 'path', 'text',
        'g', 'defs', 'clipPath', 'mask', 'filter', 'feGaussianBlur', 'feOffset',
        'feMerge', 'feMergeNode', 'feComposite', 'feBlend', 'feColorMatrix',
        'feComponentTransfer', 'feFuncR', 'feFuncG', 'feFuncB', 'feFuncA',
        'feFlood', 'feImage', 'feMorphology', 'feTile', 'feTurbulence',
        'animate', 'animateMotion', 'animateTransform', 'set', 'use',
        # MathML elements
        'math', 'mrow', 'mi', 'mo', 'mn', 'msup', 'msub', 'msubsup', 'mfrac',
        'msqrt', 'mroot', 'mtable', 'mtr', 'mtd', 'mtext', 'mspace', 'mpadded',
        'mphantom', 'menclose', 'merror', 'mprescripts', 'none', 'maligngroup',
        'malignmark', 'mover', 'munder', 'munderover', 'mstyle', 'semantics',
        'annotation', 'annotation-xml'
    }

    DANGEROUS_TAGS = {
        'script', 'iframe', 'object', 'embed', 'applet', 'basefont', 'bgsound',
        'link', 'meta', 'title', 'style', 'xmp', 'listing', 'plaintext'
    }

    DANGEROUS_ATTRIBUTES = {
        'onerror', 'onclick', 'onload', 'onmouseover', 'onfocus', 'onblur',
        'onchange', 'onsubmit', 'onreset', 'onkeydown', 'onkeyup', 'onkeypress',
        'onmouseout', 'onmouseenter', 'onmouseleave', 'onmousedown', 'onmouseup',
        'oncontextmenu', 'oninput', 'oninvalid', 'onselect', 'onabort',
        'onbeforeunload', 'onerror', 'onhashchange', 'onmessage', 'onoffline',
        'ononline', 'onpagehide', 'onpageshow', 'onpopstate', 'onresize',
        'onstorage', 'onunload'
    }

    DANGEROUS_PROTOCOLS = {
        'javascript:', 'vbscript:', 'data:text/html', 'data:application/x-javascript',
        'data:application/javascript', 'data:application/ecmascript'
    }

    # Attributes WeasyPrint fetches a resource from (as does `href` on any tag but
    # `<a>`, e.g. svg `<use>`/`<feImage>`). The Renderer's url_fetcher follows
    # file:// and internal http(s) URLs, so these may only carry an inline PNG/JPEG
    # or an in-document anchor, which is what the Renderer itself writes into table
    # cells (CU-123z74bznuv).
    RESOURCE_ATTRIBUTES = {
        'src', 'srcset', 'data', 'poster', 'background', 'dynsrc', 'lowsrc', 'xlink:href'
    }
    # An inline image is checked by its bytes, not its declared type: WeasyPrint
    # parses anything Pillow can't open as SVG, whatever the type says, and an SVG
    # fetches its own `<image href>`. Bytes that start with a PNG/JPEG signature
    # never parse as XML.
    INLINE_IMAGE = re.compile(r'data:image/(?:png|jpeg);base64,(.*)', re.IGNORECASE | re.DOTALL)
    RASTER_SIGNATURES = (b'\x89PNG\r\n\x1a\n', b'\xff\xd8\xff')
    # `url(` fetches from CSS; a backslash can spell it as a CSS escape.
    FETCHING_STYLE = re.compile(r'\\|url\s*\(|image(?:-set)?\s*\(', re.IGNORECASE)

    def is_valid_html(self, content: str) -> Tuple[bool, str]:
        """
        Validate HTML content for safety and well-formedness.

        Args:
            content: String content to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if '<' not in content or '>' not in content:
            return False, "No HTML tags found"

        if self._has_dangerous_content(content):
            return False, "Contains dangerous content"

        try:
            soup = BeautifulSoup(content, 'html.parser')
            if not soup.find():  # Handle empty tags like <>
                return False, "Not well-formed HTML (no tags found)"
            if not self._is_well_formed_html(soup, content):
                return False, "Not well-formed HTML"
            if not self._has_only_standard_tags(soup):
                return False, "Contains non-standard HTML tags"
            if not self._has_only_safe_attributes(soup):
                return False, "Contains dangerous attributes"
            return True, "Valid HTML"
        except Exception as e:
            return False, f"HTML parsing failed: {str(e)}"

    def _has_dangerous_content(self, content: str) -> bool:
        """Check for dangerous strings in content."""
        content_lower = content.lower()
        for protocol in self.DANGEROUS_PROTOCOLS:
            if protocol in content_lower:
                return True
        return False

    def _is_well_formed_html(self, soup: BeautifulSoup, original_content: str) -> bool:
        """Check if HTML is well-formed with balanced tags."""
        # Strip whitespace before checking structure — real-world HTML from rich
        # text editors commonly has leading/trailing newlines or spaces.
        stripped = original_content.strip()
        if not stripped.startswith('<'):
            return False
        if not (stripped.endswith('>') or stripped.endswith('/>')):
            return False
        return True

    def _has_only_standard_tags(self, soup: BeautifulSoup) -> bool:
        """Check if all tags are standard HTML tags and not dangerous."""
        for tag in soup.find_all():
            tag_name = tag.name.lower() if tag.name else ""
            if tag_name in self.DANGEROUS_TAGS:
                return False
            if tag_name not in self.STANDARD_HTML_TAGS:
                return False
        return True

    def _has_only_safe_attributes(self, soup: BeautifulSoup) -> bool:
        """Check if all attributes are safe."""
        for tag in soup.find_all():
            for attr_name, attr_value in tag.attrs.items():
                if isinstance(attr_name, str):
                    attr_name_lower = attr_name.lower()
                    if attr_name_lower in self.DANGEROUS_ATTRIBUTES:
                        return False
                    if not self._is_safe_resource_attribute(tag, attr_name_lower, attr_value):
                        return False

                    # Check attribute values for dangerous protocols
                    if isinstance(attr_value, str):
                        attr_value_lower = attr_value.lower()
                        for protocol in self.DANGEROUS_PROTOCOLS:
                            if protocol in attr_value_lower:
                                return False
                    elif isinstance(attr_value, list):
                        for value in attr_value:
                            if isinstance(value, str):
                                value_lower = value.lower()
                                for protocol in self.DANGEROUS_PROTOCOLS:
                                    if protocol in value_lower:
                                        return False
        return True

    def _is_safe_resource_attribute(self, tag, attr_name: str, attr_value) -> bool:
        """False for an attribute that would make WeasyPrint load an external resource."""
        values = attr_value if isinstance(attr_value, list) else [attr_value]
        # Not lowercased: base64 is case-sensitive.
        values = [v.strip() for v in values if isinstance(v, str)]
        # `<a rel=attachment href=...>` embeds whatever `href` points at in the PDF.
        if attr_name == 'rel':
            return not any('attachment' in v.lower() for v in values)
        if attr_name == 'style':
            return not any(self.FETCHING_STYLE.search(v) for v in values)
        if attr_name in self.RESOURCE_ATTRIBUTES or (attr_name == 'href' and tag.name.lower() != 'a'):
            return all(v.startswith('#') or self._is_inline_raster_image(v) for v in values)
        return True

    def _is_inline_raster_image(self, value: str) -> bool:
        """True for a base64 `data:` URL whose bytes are a PNG or JPEG."""
        match = self.INLINE_IMAGE.fullmatch(value)
        if not match:
            return False
        try:
            data = base64.b64decode(match.group(1), validate=True)
        except binascii.Error:
            return False
        return data.startswith(self.RASTER_SIGNATURES)


# Global instance
html_validator = HTMLValidator()


def is_valid_html(content: str) -> bool:
    """Convenience function to check if content is valid HTML."""
    is_valid, _ = html_validator.is_valid_html(content)
    return is_valid
