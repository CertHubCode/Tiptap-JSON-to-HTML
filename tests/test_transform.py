import os
from copy import deepcopy

import pytest

import tiptapy

tags_to_test = (
    "simple",
    "blockquote",
    "bulletlist",
    # "mark_tags",
    "ordered_list",
    "paragraph",
    "paragraph-is_renderable",
    "paragraph-codemark",
    # "paragraph-escape",
    # "image",
    "image-is_renderable",
    "image-missing_caption",
    "image-no_caption",
    "image-mime_type",
    "image-height_width",
    "image-plain_src",
    "image-plain_src-blank",
    "custom_image",
    "custom_image-no_caption",
    "featuredimage",
    "featuredimage-is_renderable",
    "featuredimage-missing_caption",
    "featuredimage-no_caption",
    "featuredimage-mime_type",
    "featuredimage-height_width",
    "horizontal_rule",
    "embed",
    "embed-missing_caption",
    "embed-no_caption",
    "embed-null_caption",
    "heading",
    "heading-align",
    "is_renderable",
    "code_block",
    "code_block-is_renderable",
    "audio",
    "audio-no_caption",
    "audio-is_renderable",
    "document-pdf",
    "document-is_renderable",
    "document-sketch",
    "camel-case",
    # "data_attributes",
    # "xss",
    "dynamic_table",
    "dynamic_table_dup_labels",
    "risk_matrix",
    "traceability_matrix",
    "traceability_matrix_empty",
    "traceability_matrix_grouped",
    "table",
    "date",
    "dynamic_text_content",
    "checklist",
    "textField",
    "checkbox",
    "numberField",
    "dateField",
    "selectField",
    "radioField",
    "checkboxGroup",
    "details",
    "page_break",
    "math",
    "note_references",
    "ordered_list_type",
    "table_of_contents",
)

class config:
    """
    Config class to store constans which are used by the othe nodes.
    """

    DOMAIN = "python.org"


def build_test_data(rebuild_html=False):
    """
    Scan data directories and return test data

    :param rebuild_html: If True, rebuild the html files
    """
    store = {"json": {}, "html": {}}
    for data_type in store:
        dir_path = os.path.abspath(f"tests/data/{data_type}/")
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            with open(file_path) as f:
                data = f.read()
                store[data_type][file.split(f".{data_type}")[0]] = data

            # Use this to (re)generate the html files
            if rebuild_html and data_type == "json":
                with open(file_path.replace("json", "html"), "w") as f:
                    f.write(tiptapy.BaseDoc(config).render(data))

    return store["json"], store["html"]


json_data, html_data = build_test_data()


@pytest.mark.parametrize("tag", tags_to_test)
def test_html_tag(tag):
    """
    Test expected json input with the expected html.
    """
    tag_data = json_data[tag]
    tag_data_copy = deepcopy(tag_data)

    expected_html = html_data[tag].strip()
    print(expected_html)
    renderer = tiptapy.BaseDoc(config)
    rendered_html = renderer.render(tag_data).strip()
    print(rendered_html)
    assert rendered_html == expected_html
    assert tag_data == tag_data_copy  # Test pass by value


def test_dynamic_table_caption_is_generic_and_escaped():
    """`content.caption` renders under any dynamicTable (not only traceability ones),
    after the rows, and is HTML-escaped like cell text."""
    data = {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {
                    "columns": {},
                    "gridState": {},
                    "content": {
                        "headers": ["A"],
                        "rows": [["a1"]],
                        "caption": "<script>alert(1)</script> note",
                    },
                },
            }
        ],
    }
    rendered_html = tiptapy.BaseDoc(config).render(data)
    assert ">a1</td>" in rendered_html
    assert "</table><p class=\"dynamic-table-caption\">" in rendered_html
    assert "<script>" not in rendered_html
    assert "&lt;script&gt;alert(1)&lt;/script&gt; note</p>" in rendered_html


def test_dynamic_table_without_rows_or_caption_still_reports_no_content():
    data = {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {"columns": {}, "gridState": {}, "content": {"headers": ["A"], "rows": []}},
            }
        ],
    }
    rendered_html = tiptapy.BaseDoc(config).render(data)
    assert "No content found" in rendered_html
    assert "dynamic-table-caption" not in rendered_html


def _render_fixture(name):
    return tiptapy.BaseDoc(config).render(json_data[name])


def test_traceability_grouped_blanks_continuations_and_stripes_odd_groups():
    """The spec sample: one row per user -> system requirement link; only the user
    requirement (and validation, which follows it) is grouped."""
    rendered_html = _render_fixture("traceability_matrix_grouped")
    assert '<table class="dynamic-table dynamic-table--traceability"' in rendered_html
    tbody = rendered_html.split("<tbody>", 1)[1]
    rows = tbody.split("</tr>")[:-1]
    assert len(rows) == 3
    # Header row is never touched by grouping.
    thead = rendered_html.split("<tbody>", 1)[0]
    assert "dynamic-table-row--group-odd" not in thead
    assert "dynamic-table-cell--continuation" not in thead
    # groupIndexes [0, 0, 1]: only the odd group is striped.
    assert ["dynamic-table-row--group-odd" in r for r in rows] == [False, False, True]
    # Continuation cells render blank with the shared class; others keep their text.
    continuation_td = '<td class="dynamic-table-cell--continuation" style="font-size: 12px"></td>'
    assert [r.count(continuation_td) for r in rows] == [0, 2, 0]
    cell = lambda text: f'<td style="font-size: 12px; white-space: pre-line">{text}</td>'
    assert cell("SR-1") in rows[0] and cell("V-1\nV-2") in rows[0]
    # SR and verification never continue: SR-2 and its verifications sit in their own row.
    assert cell("SR-2") in rows[1] and cell("V-3\nV-4") in rows[1]
    assert cell("SR-3") in rows[2] and cell("—") in rows[2]


def test_traceability_ungrouped_fixture_is_unchanged():
    rendered_html = _render_fixture("traceability_matrix")
    assert rendered_html == html_data["traceability_matrix"]
    assert "dynamic-table-cell--continuation" not in rendered_html
    assert "dynamic-table-row--group-odd" not in rendered_html
    assert "<tr class=" not in rendered_html


def _grouped_table(content, grid_state=None):
    return {
        "type": "doc",
        "content": [
            {
                "type": "dynamicTable",
                "attrs": {"columns": {}, "gridState": grid_state or {}, "content": content},
            }
        ],
    }


def test_continuation_flag_follows_cell_index_not_visible_position():
    """Columns may be reordered (orderedFields) or hidden: the continuation flag must be
    read at the column's own `cell_index`, like the cell value itself."""
    data = _grouped_table(
        {
            "headers": ["A", "B", "C"],
            "rows": [["a1", "b1", "c1"], ["a1", "b2", "c2"]],
            "continuations": [[False, False, False], [True, False, False]],
            "groupIndexes": [0, 0],
        },
        grid_state={
            "columns": {
                "orderedFields": ["C", "B", "A"],
                "columnVisibilityModel": {"B": False},
            }
        },
    )
    rendered_html = tiptapy.BaseDoc(config).render(data)
    second_row = rendered_html.split("</tr>")[-2]
    assert ">c2</td>" in second_row
    assert second_row.rstrip().endswith('<td class="dynamic-table-cell--continuation" style="font-size: 12px"></td>')
    assert "a1" not in second_row


def test_misaligned_continuations_are_ignored():
    content = {
        "headers": ["A"],
        "rows": [["a1"], ["a1"]],
        "continuations": [[False]],  # one entry for two rows -> not aligned
        "groupIndexes": [0, 1],
    }
    rendered_html = tiptapy.BaseDoc(config).render(_grouped_table(content))
    assert rendered_html.count(">a1</td>") == 2
    assert "dynamic-table-cell--continuation" not in rendered_html
    assert "dynamic-table-row--group-odd" not in rendered_html
