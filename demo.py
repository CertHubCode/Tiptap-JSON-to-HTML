import tiptapy

s = """
{
  "type": "doc",
  "content": [
    {
      "type": "dynamicTable",
      "attrs": {
        "path": [
          "root",
          "qms",
          "form",
          "records"
        ],
        "displayPath": [
          "Root",
          "QMS",
          "Form",
          "Records"
        ],
        "type": "list",
        "columns": {
          "Name": {
            "originalName": "Name",
            "alias": null,
            "visible": true,
            "order": 0,
            "width": null
          },
          "Mode of Payment": {
            "originalName": "Mode of Payment",
            "alias": "Payment",
            "visible": true,
            "order": 1,
            "width": null
          },
          "Email": {
            "originalName": "Email",
            "alias": null,
            "visible": true,
            "order": 2,
            "width": null
          },
          "Company": {
            "originalName": "Company",
            "alias": null,
            "visible": true,
            "order": 3,
            "width": null
          },
          "Date of contact": {
            "originalName": "Date of contact",
            "alias": null,
            "visible": true,
            "order": 4,
            "width": null
          },
          "Deal Status": {
            "originalName": "Deal Status",
            "alias": null,
            "visible": true,
            "order": 5,
            "width": 58
          },
          "Agreement": {
            "originalName": "Agreement",
            "alias": null,
            "visible": false,
            "order": 6,
            "width": null
          }
        },
        "content": {
          "headers": [
            "Name",
            "Email",
            "Company",
            "Date of contact",
            "Deal Status",
            "Mode of Payment",
            "Agreement"
          ],
          "rows": [
            [
              "Life Meditech",
              "l@gmail.com",
              "Life Meditech Pvt Ltd",
              "2024-11-05",
              "In progress",
              "Cash",
              "true"
            ],
            [
              "Genios",
              "genios@email.io",
              "Genio Inc. Corp",
              "2024-11-22",
              "Complete",
              "Bank Transfer",
              "false"
            ],
            [
              "Smart MediTech Device Manufacturer",
              "smart@gmail.com",
              "Smart MediTech Device Manufacturer GmbH",
              "2024-11-29",
              "On hold",
              "Bitcoin",
              "false"
            ],
            [
              "microsoft",
              "microsoft@gmail.com",
              "microsoft",
              "2024-11-06",
              "In progress",
              "Cash",
              "true"
            ],
            [
              "google",
              "google@gmail.com",
              "google",
              "2024-11-20",
              "Complete",
              "Bank Transfer",
              "true"
            ],
            [
              "MTech",
              "mtech@yahoo.com",
              "Mtech",
              "2024-11-04",
              "In progress",
              "Cash",
              "true"
            ],
            [
              "CertHub",
              "certhub@certhub.de",
              "certhub",
              "2024-11-05",
              "In progress",
              "Bank Transfer",
              "true"
            ]
          ]
        },
        "lastUpdated": 1731671604789
      }
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "text": " "
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow"
        }
      ]
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
