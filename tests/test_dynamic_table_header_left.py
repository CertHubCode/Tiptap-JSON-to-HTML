import re

import pytest
from bs4 import BeautifulSoup

from tiptapy import BaseDoc

HEADERS = ["Number", "Title", "Id"]
ROWS = [
    ["EN 455-3", "Medical gloves", "1"],
    ["EN ISO 17664-2", "Processing", "2"],
    ["EN ISO 10993-9", "Biological evaluation", "3"],
]
COLUMNS = {
    "Number": {"originalName": "Number", "alias": "Standard number", "visible": True, "order": 1, "width": 300},
    "Title": {"originalName": "Title", "alias": None, "visible": True, "order": 0, "width": None},
    "Id": {"originalName": "Id", "alias": None, "visible": False, "order": 2, "width": None},
}


def _doc(table_settings=None, content=None, columns=None):
    attrs = {
        "type": "list",
        "content": content or {"headers": HEADERS, "rows": ROWS},
        "columns": COLUMNS if columns is None else columns,
        "gridState": {},
    }
    if table_settings is not None:
        attrs["tableSettings"] = table_settings
    return {"type": "doc", "content": [{"type": "dynamicTable", "attrs": attrs}]}


def _left(**extra):
    return {"columnFontSize": "10px", "rowFontSize": "9px", "headerPosition": "left", **extra}


def _cells(html):
    table = BeautifulSoup(html, "html.parser").find("table")
    return [[cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])] for tr in table.find_all("tr")]


class TestDynamicTableHeaderLeft:
    """tableSettings.headerPosition == 'left' prints the headers as the first column and
    each record as a column, like the editor's TransposedTable."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_headers_form_the_first_column_and_records_the_others(self):
        html = self.doc.render(_doc(_left()))
        soup = BeautifulSoup(html, "html.parser")

        assert soup.find("table")["class"] == ["dynamic-table", "dynamic-table--header-left"]
        assert soup.find("thead") is None
        # Column order and aliases as in the editor; the hidden Id column is left out.
        assert _cells(html) == [
            ["Title", "Medical gloves", "Processing", "Biological evaluation"],
            ["Standard number", "EN 455-3", "EN ISO 17664-2", "EN ISO 10993-9"],
        ]
        assert [th["scope"] for th in soup.select("tbody th")] == ["row", "row"]

    def test_header_column_takes_a_quarter_and_records_share_the_rest(self):
        html = self.doc.render(_doc(_left()))
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["25", "25.0", "25.0", "25.0"]

    def test_more_than_six_records_wrap_into_a_block_repeating_the_header_column(self):
        rows = [[f"N{i}", f"T{i}", str(i)] for i in range(8)]
        html = self.doc.render(_doc(_left(), content={"headers": HEADERS, "rows": rows}))
        soup = BeautifulSoup(html, "html.parser")

        # Columns sized for six records, so the blocks line up and none gets narrower.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["25"] + ["12.5"] * 6
        blocks = [
            [[cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])] for tr in tbody.find_all("tr")]
            for tbody in soup.find_all("tbody")
        ]
        assert blocks == [
            [
                ["Title", "T0", "T1", "T2", "T3", "T4", "T5"],
                ["Standard number", "N0", "N1", "N2", "N3", "N4", "N5"],
            ],
            [
                ["Title", "T6", "T7", "", "", "", ""],
                ["Standard number", "N6", "N7", "", "", "", ""],
            ],
        ]

    def test_font_sizes_apply_to_headers_and_cells(self):
        soup = BeautifulSoup(self.doc.render(_doc(_left())), "html.parser")
        assert {th["style"] for th in soup.select("th")} == {"font-size: 10px"}
        assert {td["style"] for td in soup.select("td")} == {"font-size: 9px"}

    def test_duplicate_label_column_prints_its_label(self):
        content = {
            "headers": ["temp_core", "Title"],
            "rows": [["37", "Probe"]],
            "columns": [{"key": "temp_core", "label": "Temperature"}, {"key": "Title", "label": "Title"}],
        }
        html = self.doc.render(_doc(_left(), content=content, columns={}))
        assert _cells(html) == [["Temperature", "37"], ["Title", "Probe"]]

    def test_rich_text_cells_keep_their_markup(self):
        content = {"headers": ["Notes"], "rows": [["<p><strong>bold</strong> note</p>"]]}
        html = self.doc.render(_doc(_left(), content=content, columns={}))
        assert "<strong>bold</strong>" in BeautifulSoup(html, "html.parser").find("td").decode_contents()

    def test_no_record_keeps_the_headers_on_top(self):
        content = {"headers": HEADERS, "rows": [], "caption": "No records"}
        html = self.doc.render(_doc(_left(), content=content))
        assert "dynamic-table--header-left" not in html
        assert _cells(html) == [["Title", "Standard number"]]

    def test_caption_is_still_printed(self):
        content = {"headers": HEADERS, "rows": ROWS, "caption": "Filtered view"}
        html = self.doc.render(_doc(_left(), content=content))
        assert '<p class="dynamic-table-caption">Filtered view</p>' in html

    @pytest.mark.parametrize(
        "content",
        [
            {"headers": HEADERS, "rows": ROWS, "kind": "traceability"},
            {"headers": HEADERS, "rows": ROWS, "kind": "riskAnalysis"},
            {"headers": ["Minor", "Major"], "rows": [["1", "2"]], "rowLabels": ["Likely"]},
            {"headers": ["Minor", "Major"], "rows": [[{"value": 1, "color": "#a5d6a7"}, "2"]]},
        ],
        ids=["traceability", "risk-analysis", "row-labels", "matrix-cells"],
    )
    def test_locked_content_keeps_headers_on_top(self, content):
        html = self.doc.render(_doc(_left(), content=content, columns={}))
        assert "dynamic-table--header-left" not in html
        assert "<thead>" in html


class TestDynamicTableHeaderTopUnchanged:
    """Tables without the setting, or set to 'top', print exactly as before."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    @pytest.mark.parametrize("table_settings", [{"headerPosition": "top"}, {"headerPosition": None}, {}])
    def test_top_or_unset_renders_the_same_as_no_setting(self, table_settings):
        legacy = self.doc.render(_doc({"columnFontSize": "10px", "rowFontSize": "9px"}))
        html = self.doc.render(_doc({"columnFontSize": "10px", "rowFontSize": "9px", **table_settings}))
        assert html == legacy
        assert "dynamic-table--header-left" not in html

    def test_no_table_settings_at_all_renders_headers_on_top(self):
        html = self.doc.render(_doc(None))
        assert _cells(html)[0] == ["Title", "Standard number"]
