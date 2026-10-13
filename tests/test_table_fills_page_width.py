import re

import pytest

from tiptapy import BaseDoc

# Mirrors table.html: the page's printable width in editor px, and the narrowest column.
PAGE_WIDTH = {"portrait": 670, "landscape": 970}
MIN_COL_WIDTH = 35


def _header(colwidth, colspan=1):
    return {
        "type": "tableHeader",
        "attrs": {"colspan": colspan, "rowspan": 1, "colwidth": colwidth},
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Header"}]}],
    }


def _body(column_count):
    return [
        {
            "type": "tableCell",
            "attrs": {"colspan": 1, "rowspan": 1, "colwidth": None},
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Cell"}]}],
        }
        for _ in range(column_count)
    ]


def _render_table(widths, page_orientation="portrait"):
    """Render a plain table whose header row has one sized column per entry of `widths`."""
    data = {
        "type": "doc",
        "content": [
            {
                "type": "table",
                "content": [
                    {"type": "tableRow", "content": [_header([w]) for w in widths]},
                    {"type": "tableRow", "content": _body(len(widths))},
                ],
            }
        ],
    }
    return BaseDoc({"base_url": "https://example.com"}).render(data, page_orientation=page_orientation)


def _table_style(rendered_html):
    return re.search(r'<table class="basic-table" style="([^"]*)"', rendered_html).group(1)


def _col_percentages(rendered_html):
    colgroup = re.search(r"<colgroup>(.*?)</colgroup>", rendered_html).group(1)
    cols = re.findall(r"<col[^>]*>", colgroup)
    percentages = [re.fullmatch(r'<col style="width: ([\d.]+)%">', col) for col in cols]
    assert all(percentages), f"Every column must carry a percentage width: {cols}"
    return [float(match.group(1)) for match in percentages]


SIZED_TABLES = {
    "one tiny column": [50],
    "two small columns": [100, 200],
    "two narrow columns": [60, 60],
    "three medium columns": [150, 150, 150],
    "columns below the editor minimum": [10, 20, 300],
    "exactly the portrait page": [335, 335],
    "just over the portrait page": [400, 400],
    "many tiny columns that fit": [40] * 15,
    "many wide columns that overflow": [300] * 10,
    "one huge column": [2000],
    "huge and tiny columns mixed": [1500, 40, 40],
}


@pytest.mark.parametrize("page_orientation", ["portrait", "landscape"])
@pytest.mark.parametrize("widths", SIZED_TABLES.values(), ids=SIZED_TABLES.keys())
class TestSizedTablesFillPageWidth:
    """Whatever the editor widths add up to, a table with every column sized spans the
    full page width: small tables stretch up to it, big ones scale down to it."""

    def test_table_spans_full_width(self, widths, page_orientation):
        style = _table_style(_render_table(widths, page_orientation))

        assert "width: 100%;" in style
        assert "table-layout: fixed" in style

    def test_column_percentages_add_up_to_full_width(self, widths, page_orientation):
        percentages = _col_percentages(_render_table(widths, page_orientation))

        assert len(percentages) == len(widths)
        assert sum(percentages) == pytest.approx(100, abs=0.01)

    def test_wider_editor_columns_stay_wider(self, widths, page_orientation):
        percentages = _col_percentages(_render_table(widths, page_orientation))

        by_editor_width = [pct for _, pct in sorted(zip(widths, percentages), key=lambda pair: pair[0])]
        assert by_editor_width == sorted(by_editor_width)

    def test_no_column_narrower_than_minimum_when_it_fits(self, widths, page_orientation):
        page_width = PAGE_WIDTH[page_orientation]
        if MIN_COL_WIDTH * len(widths) > page_width:
            pytest.skip("The minimum cannot fit every column on this page")

        percentages = _col_percentages(_render_table(widths, page_orientation))

        for pct in percentages:
            assert pct / 100 * page_width >= MIN_COL_WIDTH - 0.01


@pytest.mark.parametrize(
    "widths, expected",
    [
        # (670 - 300) / 2 = 185 spare per column.
        ([100, 200], [42.5373, 57.4627]),
        # Equal columns stay equal.
        ([60, 60], [50.0, 50.0]),
        # A single column takes the whole page.
        ([50], [100.0]),
    ],
)
def test_small_table_shares_spare_width_equally(widths, expected):
    assert _col_percentages(_render_table(widths)) == expected


def test_landscape_stretches_to_the_wider_page():
    # (970 - 300) / 2 = 335 spare per column.
    assert _col_percentages(_render_table([100, 200], "landscape")) == [44.8454, 55.1546]


def test_colspan_header_columns_fill_page_width():
    data = {
        "type": "doc",
        "content": [
            {
                "type": "table",
                "content": [
                    {"type": "tableRow", "content": [_header([100, 150], colspan=2), _header([80])]},
                    {"type": "tableRow", "content": _body(3)},
                ],
            }
        ],
    }

    rendered_html = BaseDoc({"base_url": "https://example.com"}).render(data)
    percentages = _col_percentages(rendered_html)

    assert len(percentages) == 3
    assert sum(percentages) == pytest.approx(100, abs=0.01)


def test_table_with_unsized_column_spans_full_width():
    """An unsized column is left as a bare <col>, which takes whatever the sized ones
    leave of the 100% table, so the table still fills the page."""
    data = {
        "type": "doc",
        "content": [
            {
                "type": "table",
                "content": [
                    {"type": "tableRow", "content": [_header(None), _header([136])]},
                    {"type": "tableRow", "content": _body(2)},
                ],
            }
        ],
    }

    rendered_html = BaseDoc({"base_url": "https://example.com"}).render(data)

    assert "width: 100%;" in _table_style(rendered_html)
    assert '<colgroup><col><col style="width: 136px"></colgroup>' in rendered_html
