import re

from tiptapy import BaseDoc


def _dynamic_table_doc(headers, dimensions=None, sized_by_user=False):
    grid_columns = {"dimensions": dimensions, **({"sizedByUser": True} if sized_by_user else {})}
    return {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {
                    "type": "list",
                    "content": {"headers": headers, "rows": [[f"{h} value" for h in headers]]},
                    "columns": {},
                    "gridState": {"columns": grid_columns} if dimensions else None,
                },
            }
        ],
    }


class TestDynamicTableColumnWidths:
    """The PDF sizes columns like the editor grid. A table the user resized (`sizedByUser`)
    gives the spare width to the columns without a saved width, or stays narrow when every
    column has one; any other table prints as it always did, the spare width shared equally
    by all columns. A wider one is scaled down to the page."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_unmarked_table_shares_the_spare_width_between_all_columns(self):
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions={"A": {"width": 250}}))
        assert 'style="width: 100%;' in html
        # Unsized columns count as 100px; each column gets a third of the spare 670 - 450 = 220px.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["48.2587", "25.8706", "25.8706"]

    def test_unmarked_table_with_every_column_sized_still_fills_the_page(self):
        dimensions = {"A": {"width": 200}, "B": {"width": 100}}
        html = self.doc.render(_dynamic_table_doc(["A", "B"], dimensions=dimensions))
        assert 'style="width: 100%;' in html
        # Each column gets half the spare 670 - 300 = 370px: 385 and 285 of 670.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["57.4627", "42.5373"]

    def test_table_that_fits_shares_the_spare_width_between_unsized_columns(self):
        html = self.doc.render(
            _dynamic_table_doc(["A", "B", "C"], dimensions={"A": {"width": 250}}, sized_by_user=True)
        )
        assert 'style="width: 100%;' in html
        # A keeps its 250px; unsized B and C start at 50px and each take half the spare
        # 670 - 350 = 320px (portrait): 250, 210 and 210 of 670.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["37.3134", "31.3433", "31.3433"]

    def test_wide_sized_column_leaves_the_unsized_columns_what_is_left_of_the_page(self):
        html = self.doc.render(
            _dynamic_table_doc(["A", "B", "C"], dimensions={"A": {"width": 500}}, sized_by_user=True)
        )
        # 500 + 50 + 50 fits, so A is not scaled: B and C share the other 170px of 670.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["74.6269", "12.6866", "12.6866"]

    def test_table_with_every_column_sized_stays_narrower_than_the_page(self):
        dimensions = {"A": {"width": 200}, "B": {"width": 100}}
        html = self.doc.render(_dynamic_table_doc(["A", "B"], dimensions=dimensions, sized_by_user=True))
        assert 'style="width: 300px;' in html
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["66.6667", "33.3333"]

    def test_overflowing_table_scales_to_the_page_width(self):
        dimensions = {"A": {"width": 400}, "B": {"width": 400}}
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions=dimensions, sized_by_user=True))
        assert 'style="width: 100%;' in html
        # 400 + 400 + 50 = 850 > 670 (portrait): unsized C is held at 50, A and B share the rest.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["46.2687", "46.2687", "7.4627"]

    def test_column_is_never_narrower_than_the_editors_minimum(self):
        html = self.doc.render(_dynamic_table_doc(["A", "B"], dimensions={"A": {"width": 30}}, sized_by_user=True))
        # A is raised to 50; unsized B takes the spare 670 - 100 = 570px: 50 and 620 of 670.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["7.4627", "92.5373"]

    def test_scaled_column_is_held_at_the_minimum_and_the_rest_shrink(self):
        dimensions = {"A": {"width": 600}, "B": {"width": 50}, "C": {"width": 50}}
        html = self.doc.render(_dynamic_table_doc(["A", "B", "C"], dimensions=dimensions))
        # Plain scaling would make B and C 47.9px; they stay 50 of 670 and A takes the other 570.
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["85.0746", "7.4627", "7.4627"]

    def test_too_many_columns_for_the_minimum_share_the_page_equally(self):
        headers = [f"C{i}" for i in range(15)]  # 15 x 50 > 670 (portrait)
        html = self.doc.render(_dynamic_table_doc(headers))
        assert re.findall(r'<col\s+style="width: ([\d.]+)%">', html) == ["6.6667"] * 15
