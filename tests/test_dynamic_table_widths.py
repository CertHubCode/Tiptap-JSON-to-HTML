import re

from tiptapy import BaseDoc


def _dynamic_table_doc(headers, dimensions=None):
    return {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {
                    "type": "list",
                    "content": {"headers": headers, "rows": [[f"{h} value" for h in headers]]},
                    "columns": {},
                    "gridState": {"columns": {"dimensions": dimensions}} if dimensions else None,
                },
            }
        ],
    }


class TestDynamicTableColumnWidths:
    """The PDF sizes columns like the editor grid, scaled down to the page when wider."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_table_that_fits_keeps_the_editors_widths(self):
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions={"A": {"width": 250}}))
        assert 'style="width: 450px;' in html
        # Unsized columns take the DataGrid's default 100px.
        assert re.findall(r'<col\s+style="width: (\d+)px">', html) == ["250", "100", "100"]

    def test_overflowing_table_scales_to_the_page_width(self):
        dimensions = {"A": {"width": 400}, "B": {"width": 400}}
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions=dimensions))
        assert 'style="width: 100%;' in html
        # 400 + 400 + 100 = 900 > 670 (portrait), kept in proportion.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["44.4444", "44.4444", "11.1111"]

    def test_column_is_never_narrower_than_the_editors_minimum(self):
        html = self.doc.render(_dynamic_table_doc(["A", "B"], dimensions={"A": {"width": 30}}))
        assert re.findall(r'<col\s+style="width: (\d+)px">', html) == ["50", "100"]

    def test_scaled_column_is_held_at_the_minimum_and_the_rest_shrink(self):
        dimensions = {"A": {"width": 600}, "B": {"width": 50}, "C": {"width": 50}}
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions=dimensions))
        # Plain scaling would make B and C 47.9px; they stay 50 of 670 and A takes the other 570.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["85.0746", "7.4627", "7.4627"]

    def test_too_many_columns_for_the_minimum_share_the_page_equally(self):
        headers = [f"C{i}" for i in range(15)]  # 15 x 50 > 670 (portrait)
        html = self.doc.render(_dynamic_table_doc(headers))
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["6.6667"] * 15
