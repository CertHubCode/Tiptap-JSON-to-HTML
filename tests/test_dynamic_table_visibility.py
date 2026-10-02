import re

from tiptapy import BaseDoc


def _dynamic_table_doc(headers, columns=None, visibility_model=None, dimensions=None):
    grid_columns = {}
    if visibility_model is not None:
        grid_columns["columnVisibilityModel"] = visibility_model
    if dimensions is not None:
        grid_columns["dimensions"] = dimensions
    return {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {
                    "type": "list",
                    "content": {"headers": headers, "rows": [[f"{h} value" for h in headers]]},
                    "columns": columns or {},
                    "gridState": {"columns": grid_columns} if grid_columns else None,
                },
            }
        ],
    }


def _rendered_headers(html):
    return re.findall(r"<th[^>]*>(.*?)</th>", html)


class TestDynamicTableColumnVisibility:
    """The PDF must show the same columns as the editor grid (DynamicTableRenderer.tsx)."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_linked_columns_hidden_by_default_even_if_columns_say_visible(self):
        headers = ["Name", "Id", "Linked Files", "Linked Documents", "Linked Global Element Entries"]
        columns = {h: {"originalName": h, "visible": True} for h in headers}
        html = self.doc.render(_dynamic_table_doc(headers, columns=columns, visibility_model={}))
        assert _rendered_headers(html) == ["Name"]

    def test_visibility_model_can_reveal_a_linked_column(self):
        headers = ["Name", "Linked Files"]
        html = self.doc.render(_dynamic_table_doc(headers, visibility_model={"Linked Files": True}))
        assert _rendered_headers(html) == ["Name", "Traced Files"]

    def test_visibility_model_wins_over_columns_visible(self):
        headers = ["Name", "Status"]
        columns = {h: {"originalName": h, "visible": True} for h in headers}
        html = self.doc.render(_dynamic_table_doc(headers, columns=columns, visibility_model={"Status": False}))
        assert _rendered_headers(html) == ["Name"]

    def test_created_at_shows_only_when_explicitly_visible(self):
        headers = ["Name", "Created At"]
        hidden = self.doc.render(_dynamic_table_doc(headers))
        assert _rendered_headers(hidden) == ["Name"]

        columns = {"Created At": {"originalName": "Created At", "visible": True}}
        shown = self.doc.render(_dynamic_table_doc(headers, columns=columns))
        assert _rendered_headers(shown) == ["Name", "Created At"]

    def test_created_at_follows_columns_visible_not_a_model_reveal(self):
        headers = ["Name", "Created At"]
        revealed_by_model_only = self.doc.render(
            _dynamic_table_doc(headers, visibility_model={"Created At": True})
        )
        assert _rendered_headers(revealed_by_model_only) == ["Name"]

        columns = {"Created At": {"originalName": "Created At", "visible": True}}
        hidden_by_model = self.doc.render(
            _dynamic_table_doc(headers, columns=columns, visibility_model={"Created At": False})
        )
        assert _rendered_headers(hidden_by_model) == ["Name"]

    def test_dead_linked_global_elements_column_never_renders_on_global_element_tables(self):
        headers = ["Name", "Linked Global Elements"]
        doc = _dynamic_table_doc(headers, visibility_model={"Linked Global Elements": True})
        doc["content"][0]["attrs"]["entity_type"] = "GlobalElement"
        assert _rendered_headers(self.doc.render(doc)) == ["Name"]

        doc["content"][0]["attrs"]["entity_type"] = "KnowledgeTopic"
        assert _rendered_headers(self.doc.render(doc)) == ["Name", "Linked Global Elements"]

    def test_columns_visible_false_still_hides_without_model_entry(self):
        headers = ["Name", "Status"]
        columns = {"Status": {"originalName": "Status", "visible": False}}
        html = self.doc.render(_dynamic_table_doc(headers, columns=columns))
        assert _rendered_headers(html) == ["Name"]


class TestDynamicTableUnsizedColumnWidth:
    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_unsized_column_weighs_like_the_editors_default_width_on_overflow(self):
        headers = ["A", "B", "C"]
        dimensions = {"A": {"width": 400}, "B": {"width": 400}}
        html = self.doc.render(_dynamic_table_doc(headers, dimensions=dimensions))
        widths = re.findall(r'<col\s+style="width: ([\d.]+)%">', html)
        # 400 + 400 + 100 (DataGrid default) = 900
        assert widths == ["44.4444", "44.4444", "11.1111"]
