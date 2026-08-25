from tiptapy import BaseDoc


def _cell(node_type, text, colspan=1, colwidth=None):
    return {
        "type": node_type,
        "attrs": {"colspan": colspan, "rowspan": 1, "colwidth": colwidth},
        "content": [
            {
                "type": "paragraph",
                "attrs": {"textAlign": "left"},
                "content": [{"type": "text", "text": text}],
            }
        ],
    }


def _table_doc(header_cells, body_cells):
    return {
        "type": "doc",
        "content": [
            {
                "type": "table",
                "content": [
                    {"type": "tableRow", "content": header_cells},
                    {"type": "tableRow", "content": body_cells},
                ],
            }
        ],
    }


class TestTableColumnWidths:
    """Regression tests: plain tables must honor per-column widths set in the editor."""

    def setup_method(self):
        self.doc = BaseDoc({"base_url": "https://example.com"})

    def test_all_columns_defined_and_fits_uses_exact_px_widths(self):
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "A", colwidth=[100]),
                _cell("tableHeader", "B", colwidth=[200]),
            ],
            body_cells=[_cell("tableCell", "a1"), _cell("tableCell", "b1")],
        )

        rendered_html = self.doc.render(data)

        assert '<colgroup><col style="width: 100px"><col style="width: 200px"></colgroup>' in rendered_html
        assert 'width: 300px' in rendered_html
        assert 'table-layout: fixed' in rendered_html

    def test_mixed_defined_and_undefined_columns_keeps_defined_widths(self):
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "Name", colwidth=None),
                _cell("tableHeader", "Email", colwidth=[136]),
            ],
            body_cells=[_cell("tableCell", "Ann"), _cell("tableCell", "ann@example.com")],
        )

        rendered_html = self.doc.render(data)

        assert '<colgroup><col><col style="width: 136px"></colgroup>' in rendered_html
        assert 'width: 100%' in rendered_html
        assert 'table-layout: fixed' in rendered_html

    def test_all_defined_but_overflowing_converts_to_percentages(self):
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "A", colwidth=[500]),
                _cell("tableHeader", "B", colwidth=[500]),
            ],
            body_cells=[_cell("tableCell", "a1"), _cell("tableCell", "b1")],
        )

        rendered_html = self.doc.render(data)

        assert '<col style="width: 50.0%">' in rendered_html
        assert rendered_html.count('<col style="width: 50.0%">') == 2

    def test_colspan_header_expands_colwidth_array_across_columns(self):
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "AB", colspan=2, colwidth=[100, 150]),
                _cell("tableHeader", "C", colwidth=[80]),
            ],
            body_cells=[
                _cell("tableCell", "a1"),
                _cell("tableCell", "b1"),
                _cell("tableCell", "c1"),
            ],
        )

        rendered_html = self.doc.render(data)

        assert '<colgroup><col style="width: 100px"><col style="width: 150px"><col style="width: 80px"></colgroup>' in rendered_html
        assert '<th colspan="2">' in rendered_html

    def test_table_with_no_header_row_content_does_not_crash(self):
        data = {
            "type": "doc",
            "content": [{"type": "table", "content": []}],
        }

        rendered_html = self.doc.render(data)

        assert "<table" in rendered_html

    def test_outer_table_with_nested_table_cell_skips_width_enforcement(self):
        """A cell that itself contains a nested <table> must not have its outer
        table's column pinned to a rigid pixel width: the nested content's real
        size is unpredictable, and forcing table-layout:fixed on the outer table
        crushes it (e.g. a narrow user-drawn column that later gets a large
        nested table dropped into it renders as unreadable single-letter-per-line
        text). See: real production doc "Test nested tables"."""
        inner_table = {
            "type": "table",
            "content": [
                {
                    "type": "tableRow",
                    "content": [
                        _cell("tableHeader", "Inner A", colwidth=[50]),
                        _cell("tableHeader", "Inner B", colwidth=[50]),
                    ],
                },
            ],
        }
        outer_cell_with_nested = {
            "type": "tableCell",
            "attrs": {"colspan": 1, "rowspan": 1, "colwidth": [100]},
            "content": [inner_table],
        }
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "table",
                    "content": [
                        {
                            "type": "tableRow",
                            "content": [
                                _cell("tableHeader", "A", colwidth=[100]),
                                _cell("tableHeader", "B", colwidth=[100]),
                            ],
                        },
                        {
                            "type": "tableRow",
                            "content": [_cell("tableCell", "x", colwidth=[100]), outer_cell_with_nested],
                        },
                    ],
                }
            ],
        }

        rendered_html = self.doc.render(data)

        outer_table_open = rendered_html.split("<table", 1)[1]
        assert outer_table_open.startswith(' class="basic-table">'), (
            "Outer table with a nested-table cell must render without a forced width/table-layout style"
        )
        assert rendered_html.count("<colgroup>") == 1, "Only the inner (nested) table should get a colgroup"

    def test_outer_table_with_nested_dynamic_table_cell_skips_width_enforcement(self):
        nested_dynamic_table = {
            "type": "dynamicTable",
            "attrs": {
                "columns": {"col1": {"visible": True, "order": 0, "width": None}},
                "content": {"headers": ["col1"], "rows": [["value"]]},
            },
        }
        outer_cell_with_nested = {
            "type": "tableCell",
            "attrs": {"colspan": 1, "rowspan": 1, "colwidth": [100]},
            "content": [nested_dynamic_table],
        }
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "A", colwidth=[100]),
                _cell("tableHeader", "B", colwidth=[100]),
            ],
            body_cells=[_cell("tableCell", "x", colwidth=[100]), outer_cell_with_nested],
        )

        rendered_html = self.doc.render(data)

        outer_table_open = rendered_html.split("<table", 1)[1]
        assert outer_table_open.startswith(' class="basic-table">'), (
            "Outer table with a nested dynamicTable cell must render without a forced width/table-layout style"
        )

    def test_header_cell_missing_attrs_key_does_not_crash(self):
        """A cell dict that omits "attrs" entirely (not attrs: {}) must not
        blow up the header-row width-derivation pass in table.html."""
        header_cell_no_attrs = {
            "type": "tableHeader",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "A"}]}],
        }
        data = _table_doc(
            header_cells=[header_cell_no_attrs, _cell("tableHeader", "B", colwidth=[100])],
            body_cells=[_cell("tableCell", "a1"), _cell("tableCell", "b1")],
        )

        rendered_html = self.doc.render(data)

        assert "<table" in rendered_html
        assert "A" in rendered_html and "B" in rendered_html

    def test_body_cell_missing_attrs_key_does_not_crash(self):
        """A body-row cell without "attrs" hits the separate colspan
        rendering call site (table.html <td>), not just the header-row
        width calculation."""
        body_cell_no_attrs = {
            "type": "tableCell",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "b1"}]}],
        }
        data = _table_doc(
            header_cells=[
                _cell("tableHeader", "A", colwidth=[100]),
                _cell("tableHeader", "B", colwidth=[100]),
            ],
            body_cells=[_cell("tableCell", "a1"), body_cell_no_attrs],
        )

        rendered_html = self.doc.render(data)

        assert "<table" in rendered_html
        assert "b1" in rendered_html

    def test_dynamic_table_missing_attrs_key_does_not_crash(self):
        """A dynamicTable node with no "attrs" key at all must fall back
        gracefully instead of raising in dynamicTable.html."""
        data = {
            "type": "doc",
            "content": [{"type": "dynamicTable"}],
        }

        rendered_html = self.doc.render(data)

        assert "No content found" in rendered_html
