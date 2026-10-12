"""The editor keeps its cell menu / toolbar formatting as node attrs
(``backgroundColor``, ``nodeTextAlign``, ``nodeVerticalAlign``, ``textAlign``);
``extract_node_style`` / ``extract_cell_attrs`` print them as inline CSS."""

import pytest

from tiptapy.macros import extract_cell_attrs, extract_node_style


def _node(**attrs):
    return {"type": "tableCell", "attrs": attrs}


class TestExtractNodeStyle:
    def test_no_attrs_prints_nothing(self):
        assert extract_node_style({"type": "paragraph"}) == ""
        assert extract_node_style(_node()) == ""

    def test_prints_the_cell_background(self):
        assert extract_node_style(_node(backgroundColor="#000080")) == ' style="background-color: #000080"'

    @pytest.mark.parametrize(
        "color",
        ["rgb(0, 0, 128)", "rgba(0,0,128,0.5)", "hsl(240, 100%, 25%)", "navy", "var(--docx-accent1-color)", "#abc"],
    )
    def test_accepts_the_colour_forms_the_editor_stores(self, color):
        assert extract_node_style(_node(backgroundColor=color)) == f' style="background-color: {color}"'

    @pytest.mark.parametrize(
        "value",
        [
            "url(https://evil.example/x.png)",
            "red; background-image: url(x)",
            'red" onload="alert(1)',
            "expression(alert(1))",
            "#00008",  # not a hex colour (5 digits)
            "",
            None,
            12,
        ],
    )
    def test_drops_anything_that_is_not_a_colour(self, value):
        assert extract_node_style(_node(backgroundColor=value)) == ""

    def test_cell_menu_alignment_wins_over_toolbar_alignment(self):
        assert extract_node_style(_node(nodeTextAlign="center", textAlign="right")) == ' style="text-align: center"'

    def test_toolbar_alignment_prints_on_blocks(self):
        assert extract_node_style({"type": "paragraph", "attrs": {"textAlign": "justify"}}) == ' style="text-align: justify"'

    def test_left_is_the_editor_default_and_is_not_printed(self):
        # The editor's own renderHTML omits it, and printing it would override
        # the alignment of the cell the paragraph sits in.
        assert extract_node_style({"type": "paragraph", "attrs": {"textAlign": "left"}}) == ""
        assert extract_node_style(_node(nodeTextAlign="left")) == ""

    @pytest.mark.parametrize("value", ["middle", "top", "bottom"])
    def test_prints_vertical_alignment(self, value):
        assert extract_node_style(_node(nodeVerticalAlign=value)) == f' style="vertical-align: {value}"'

    def test_rejects_unknown_alignments(self):
        assert extract_node_style(_node(nodeTextAlign="start; color: red", nodeVerticalAlign="baseline")) == ""

    def test_joins_every_declaration(self):
        style = extract_node_style(_node(nodeTextAlign="right", nodeVerticalAlign="bottom", backgroundColor="#FFF2CC"))
        assert style == ' style="text-align: right; vertical-align: bottom; background-color: #FFF2CC"'


class TestExtractCellAttrs:
    def test_single_cell_prints_only_its_style(self):
        assert extract_cell_attrs(_node(colspan=1, rowspan=1, colwidth=None)) == ""
        assert extract_cell_attrs(_node(colspan=1, rowspan=1, backgroundColor="#000080")) == (
            ' style="background-color: #000080"'
        )

    def test_merged_cells_keep_their_spans(self):
        assert extract_cell_attrs(_node(colspan=2, rowspan=1)) == ' colspan="2"'
        assert extract_cell_attrs(_node(colspan=1, rowspan=3)) == ' rowspan="3"'
        assert extract_cell_attrs(_node(colspan=2, rowspan=2, nodeVerticalAlign="middle")) == (
            ' colspan="2" rowspan="2" style="vertical-align: middle"'
        )

    def test_ignores_spans_that_are_not_counts(self):
        assert extract_cell_attrs(_node(colspan="2", rowspan=None)) == ""
