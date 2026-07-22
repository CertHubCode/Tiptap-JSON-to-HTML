from .html_validator import is_valid_html
from markupsafe import Markup

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
