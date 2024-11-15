import tiptapy

s = """

{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "marks": [
            {
              "type": "bold"
            }
          ],
          "text": "Bold "
        },
        {
          "type": "hardBreak"
        },
        {
          "type": "text",
          "marks": [
            {
              "type": "strike"
            }
          ],
          "text": "Strike"
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "marks": [
            {
              "type": "underline"
            }
          ],
          "text": "Underline"
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "marks": [
            {
              "type": "italic"
            }
          ],
          "text": "Italic"
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "marks": [
            {
              "type": "highlight",
              "attrs": {
                "color": "#ffd699"
              }
            }
          ],
          "text": "Highlight"
        },
        {
          "type": "hardBreak"
        }
      ]
    },
    {
      "type": "orderedList",
      "attrs": {
        "start": 1
      },
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "one"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "two"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "three"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      }
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "one"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "two"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "three"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      }
    },
    {
      "type": "taskList",
      "content": [
        {
          "type": "taskItem",
          "attrs": {
            "checked": true
          },
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "hello"
                }
              ]
            }
          ]
        },
        {
          "type": "taskItem",
          "attrs": {
            "checked": false
          },
          "content": [
            {
              "type": "paragraph",
              "attrs": {
                "textAlign": "left"
              },
              "content": [
                {
                  "type": "text",
                  "text": "hi"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      }
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "right"
      },
      "content": [
        {
          "type": "text",
          "text": "Last updated on "
        },
        {
          "type": "date",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "last_updated_at"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Last Updated At"
            ],
            "type": "date",
            "format": "YYYY-MM-DD",
            "content": "2024-11-12",
            "lastUpdated": 1731668527558
          }
        },
        {
          "type": "text",
          "text": " by "
        },
        {
          "type": "dynamic-text-content",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "last_updated_by"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Last Updated By"
            ],
            "type": "plain",
            "content": "Saud Chougle",
            "lastUpdated": 1731668527559
          }
        },
        {
          "type": "text",
          "text": " "
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {
        "textAlign": "left",
        "level": 1
      },
      "content": [
        {
          "type": "dynamic-text-content",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "name"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Name"
            ],
            "type": "plain",
            "content": "Process 1",
            "lastUpdated": 1731668508787
          }
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "text",
          "marks": [
            {
              "type": "underline"
            }
          ],
          "text": "Abbreviation:"
        },
        {
          "type": "text",
          "text": " "
        },
        {
          "type": "dynamic-text-content",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "abbreviation"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Abbreviation"
            ],
            "type": "plain",
            "content": "p1",
            "lastUpdated": 1731668508788
          }
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            },
            {
              "type": "tableHeader",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "text": "Name"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableHeader",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "text": "Date & Signature"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "marks": [
                        {
                          "type": "bold"
                        }
                      ],
                      "text": "Author"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "dynamic-text-content",
                      "attrs": {
                        "path": [
                          "root",
                          "qms",
                          "sop",
                          "author"
                        ],
                        "displayPath": [
                          "Root",
                          "QMS",
                          "SOP",
                          "Author"
                        ],
                        "type": "plain",
                        "content": "Saud Chougle",
                        "lastUpdated": 1731668508785
                      }
                    },
                    {
                      "type": "text",
                      "text": "  "
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "marks": [
                        {
                          "type": "bold"
                        }
                      ],
                      "text": "Process Owner"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "dynamic-text-content",
                      "attrs": {
                        "path": [
                          "root",
                          "qms",
                          "sop",
                          "owner"
                        ],
                        "displayPath": [
                          "Root",
                          "QMS",
                          "SOP",
                          "Owner"
                        ],
                        "type": "plain",
                        "content": "Nicolas Gehring",
                        "lastUpdated": 1731668508787
                      }
                    },
                    {
                      "type": "text",
                      "text": "  "
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "marks": [
                        {
                          "type": "bold"
                        }
                      ],
                      "text": "Reviewer"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "dynamic-text-content",
                      "attrs": {
                        "path": [
                          "root",
                          "qms",
                          "sop",
                          "reviewers"
                        ],
                        "displayPath": [
                          "Root",
                          "QMS",
                          "SOP",
                          "Reviewers"
                        ],
                        "type": "plain",
                        "content": "Leon Kobinger, Julia Sommer, ClinicalEvaluator",
                        "lastUpdated": 1731668508787
                      }
                    },
                    {
                      "type": "text",
                      "text": "  "
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "marks": [
                        {
                          "type": "bold"
                        }
                      ],
                      "text": "Formal Reviewer"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "dynamic-text-content",
                      "attrs": {
                        "path": [
                          "root",
                          "qms",
                          "sop",
                          "formal_reviewer"
                        ],
                        "displayPath": [
                          "Root",
                          "QMS",
                          "SOP",
                          "Formal Reviewer"
                        ],
                        "type": "plain",
                        "content": "Jonas Bayer",
                        "lastUpdated": 1731668508786
                      }
                    },
                    {
                      "type": "text",
                      "text": "  "
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 3,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "text": "*) Signatures not necessary for draft version"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "text",
                      "marks": [
                        {
                          "type": "bold"
                        }
                      ],
                      "text": "Version"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 2,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  },
                  "content": [
                    {
                      "type": "dynamic-text-content",
                      "attrs": {
                        "path": [
                          "root",
                          "qms",
                          "sop",
                          "version"
                        ],
                        "displayPath": [
                          "Root",
                          "QMS",
                          "SOP",
                          "Version"
                        ],
                        "type": "plain",
                        "content": "1.0",
                        "lastUpdated": 1731668508787
                      }
                    },
                    {
                      "type": "text",
                      "text": "  "
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            },
            {
              "type": "tableCell",
              "attrs": {
                "colspan": 1,
                "rowspan": 1,
                "colwidth": null
              },
              "content": [
                {
                  "type": "paragraph",
                  "attrs": {
                    "textAlign": "left"
                  }
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {
        "textAlign": "left",
        "level": 2
      },
      "content": [
        {
          "type": "text",
          "text": "Goal"
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "dynamic-text-content",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "goal"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Goal"
            ],
            "type": "plain",
            "content": "Process Goal",
            "lastUpdated": 1731668508787
          }
        },
        {
          "type": "text",
          "text": "  "
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {
        "textAlign": "left",
        "level": 2
      },
      "content": [
        {
          "type": "text",
          "text": "Scope"
        }
      ]
    },
    {
      "type": "paragraph",
      "attrs": {
        "textAlign": "left"
      },
      "content": [
        {
          "type": "dynamic-text-content",
          "attrs": {
            "path": [
              "root",
              "qms",
              "sop",
              "scope"
            ],
            "displayPath": [
              "Root",
              "QMS",
              "SOP",
              "Scope"
            ],
            "type": "plain",
            "content": "Process Scope",
            "lastUpdated": 1731668508788
          }
        },
        {
          "type": "text",
          "text": "  "
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {
        "textAlign": "left",
        "level": 2
      },
      "content": [
        {
          "type": "text",
          "text": "Background Information"
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
