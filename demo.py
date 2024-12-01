import tiptapy

s = """
{
  "type": "doc",
  "content": [
    {
      "type": "checklist",
      "attrs": {
        "path": [
          "root",
          "product",
          "A",
          "Single Record multi values fields",
          "checklist_bk3z5"
        ],
        "displayPath": [
          "Root",
          "Product",
          "A",
          "Single Record multi values fields",
          "Multiple Checkboxs"
        ],
        "content": [
          {
            "label": "EU",
            "value": "EU",
            "checked": true
          },
          {
            "label": "AUS",
            "value": "AUS",
            "checked": true
          },
          {
            "label": "CAN",
            "value": "CAN",
            "checked": true
          },
          {
            "label": "US",
            "value": "US",
            "checked": true
          }
        ],
        "type": "checklist"
      }
    }
  ]
}
"""


class config:
    """
    Config class to store constants used by the other nodes.
    """
    DOMAIN = "python.org"


renderer = tiptapy.BaseDoc(config)
out = renderer.render(s)
print(out)
