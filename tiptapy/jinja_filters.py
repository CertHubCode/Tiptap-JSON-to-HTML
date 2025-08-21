from .html_validator import is_valid_html
from markupsafe import Markup


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
