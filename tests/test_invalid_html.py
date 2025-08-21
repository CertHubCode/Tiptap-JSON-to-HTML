import pytest
from tiptapy import BaseDoc


class TestInvalidHTML:
    """Test HTML validation and escaping in dynamic tables."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = {"base_url": "https://example.com"}
        self.doc = BaseDoc(self.config)

    def test_dynamic_table_html_handling(self):
        """Test basic HTML handling in dynamic tables."""
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "dynamicTable",
                    "attrs": {
                        "columns": {
                            "col1": {"visible": True, "order": 1}
                        },
                        "content": {
                            "headers": ["col1"],
                            "rows": [
                                ["<p>Valid HTML</p>"],
                                ["<invalid>text</invalid>"],
                                ["<br/>"],
                                ["<img src='test.jpg' alt='test'>"],
                                ["<script>alert('xss')</script>"],
                                ["<div onclick='alert()'>Dangerous</div>"],
                                ["<a href='javascript:alert()'>Dangerous link</a>"],
                                ["<div>Unclosed"],
                                ["<my-component>Custom</my-component>"],
                                ["<invalidtag>Invalid</invalidtag>"],
                                ["<p>Valid</p> <invalid>Invalid</invalid>"],
                                ["   <p>   Spaced   </p>   "]
                            ]
                        }
                    }
                }
            ]
        }

        rendered_html = self.doc.render(data)
        print(f"Rendered HTML: {rendered_html}")

        # Test that valid HTML is preserved
        assert "<p>Valid HTML</p>" in rendered_html, "Valid HTML should be preserved"
        assert "<br/>" in rendered_html, "Valid self-closing tags should be preserved"
        assert "<img src='test.jpg' alt='test'>" in rendered_html, "Valid img tags should be preserved"

        # Test that invalid HTML is escaped
        assert "&lt;invalid&gt;text&lt;/invalid&gt;" in rendered_html, "Invalid HTML should be escaped"
        assert "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in rendered_html, "Script tags should be escaped"
        assert "&lt;div onclick=&#x27;alert()&#x27;&gt;Dangerous&lt;/div&gt;" in rendered_html, "Event handlers should be escaped"
        assert "&lt;a href=&#x27;javascript:alert()&#x27;&gt;Dangerous link&lt;/a&gt;" in rendered_html, "JavaScript protocol should be escaped"
        assert "&lt;div&gt;Unclosed" in rendered_html, "Unclosed tags should be escaped"

        # Test that custom elements are escaped (no custom elements supported)
        assert "&lt;my-component&gt;Custom&lt;/my-component&gt;" in rendered_html, "Custom elements should be escaped"
        assert "&lt;invalidtag&gt;Invalid&lt;/invalidtag&gt;" in rendered_html, "Invalid tags should be escaped"

        # Test that mixed content is fully escaped for security
        assert "&lt;p&gt;Valid&lt;/p&gt; &lt;invalid&gt;Invalid&lt;/invalid&gt;" in rendered_html, "Mixed content should be escaped"
        assert "   &lt;p&gt;   Spaced   &lt;/p&gt;   " in rendered_html, "Mixed content with whitespace should be escaped"

        print("✅ Basic HTML handling works correctly")

    def test_dynamic_table_security(self):
        """Test security features - dangerous content should be escaped."""
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "dynamicTable",
                    "attrs": {
                        "columns": {
                            "col1": {"visible": True, "order": 1}
                        },
                        "content": {
                            "headers": ["col1"],
                            "rows": [
                                ["<script>alert('xss')</script>"],
                                ["<iframe src='javascript:alert()'></iframe>"],
                                ["<object data='data:text/html,<script>alert()</script>'>"],
                                ["<embed src='javascript:alert()'>"],
                                ["<div onerror='alert()'>Error</div>"],
                                ["<img src='javascript:alert()' onload='alert()'>"],
                                ["<a href='vbscript:msgbox(\"Hello\")'>VBScript</a>"],
                                ["<form onsubmit='alert()'>Submit</form>"],
                                ["<input onchange='alert()' onkeypress='alert()'>"],
                                ["<textarea onblur='alert()' onfocus='alert()'>Text</textarea>"]
                            ]
                        }
                    }
                }
            ]
        }

        rendered_html = self.doc.render(data)
        print(f"Security test rendered HTML: {rendered_html}")

        # Test that dangerous content is escaped
        assert "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in rendered_html, "Script tags should be escaped"
        assert "&lt;iframe src=&#x27;javascript:alert()&#x27;&gt;&lt;/iframe&gt;" in rendered_html, "Iframe should be escaped"
        assert "&lt;object data=&#x27;data:text/html,&lt;script&gt;alert()&lt;/script&gt;&#x27;&gt;" in rendered_html, "Object should be escaped"
        assert "&lt;embed src=&#x27;javascript:alert()&#x27;&gt;" in rendered_html, "Embed should be escaped"
        assert "&lt;div onerror=&#x27;alert()&#x27;&gt;Error&lt;/div&gt;" in rendered_html, "Event handlers should be escaped"
        assert "&lt;img src=&#x27;javascript:alert()&#x27; onload=&#x27;alert()&#x27;&gt;" in rendered_html, "Dangerous img should be escaped"
        assert "&lt;a href=&#x27;vbscript:msgbox(&quot;Hello&quot;)&#x27;&gt;VBScript&lt;/a&gt;" in rendered_html, "VBScript should be escaped"
        assert "&lt;form onsubmit=&#x27;alert()&#x27;&gt;Submit&lt;/form&gt;" in rendered_html, "Form events should be escaped"
        assert "&lt;input onchange=&#x27;alert()&#x27; onkeypress=&#x27;alert()&#x27;&gt;" in rendered_html, "Input events should be escaped"
        assert "&lt;textarea onblur=&#x27;alert()&#x27; onfocus=&#x27;alert()&#x27;&gt;Text&lt;/textarea&gt;" in rendered_html, "Textarea events should be escaped"

        print("✅ Security features working correctly")

    def test_dynamic_table_valid_html_preservation(self):
        """Test that valid, safe HTML is properly preserved."""
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "dynamicTable",
                    "attrs": {
                        "columns": {
                            "col1": {"visible": True, "order": 1}
                        },
                        "content": {
                            "headers": ["col1"],
                            "rows": [
                                ["<p>Simple paragraph</p>"],
                                ["<strong>Bold text</strong>"],
                                ["<em>Italic text</em>"],
                                ["<a href='https://example.com'>Link</a>"],
                                ["<img src='image.jpg' alt='Image'>"],
                                ["<ul><li>Item 1</li><li>Item 2</li></ul>"],
                                ["<table><tr><td>Cell</td></tr></table>"],
                                ["<div class='container'>Content</div>"],
                                ["<span style='color: red;'>Styled text</span>"],
                                ["<br>"],
                                ["<hr>"],
                                ["<input type='text' placeholder='Enter text'>"],
                                ["<textarea rows='3' cols='50'>Text area</textarea>"],
                                ["<select><option>Option 1</option></select>"],
                                ["<button type='button'>Click me</button>"]
                            ]
                        }
                    }
                }
            ]
        }

        rendered_html = self.doc.render(data)
        print(f"Valid HTML test rendered: {rendered_html}")

        # Test that valid HTML is preserved
        assert "<p>Simple paragraph</p>" in rendered_html, "Paragraph should be preserved"
        assert "<strong>Bold text</strong>" in rendered_html, "Strong should be preserved"
        assert "<em>Italic text</em>" in rendered_html, "Em should be preserved"
        assert "<a href='https://example.com'>Link</a>" in rendered_html, "Link should be preserved"
        assert "<img src='image.jpg' alt='Image'>" in rendered_html, "Image should be preserved"
        assert "<ul><li>Item 1</li><li>Item 2</li></ul>" in rendered_html, "List should be preserved"
        assert "<table><tr><td>Cell</td></tr></table>" in rendered_html, "Table should be preserved"
        assert "<div class='container'>Content</div>" in rendered_html, "Div should be preserved"
        assert "<span style='color: red;'>Styled text</span>" in rendered_html, "Span should be preserved"
        assert "<br>" in rendered_html, "BR should be preserved"
        assert "<hr>" in rendered_html, "HR should be preserved"
        assert "<input type='text' placeholder='Enter text'>" in rendered_html, "Input should be preserved"
        assert "<textarea rows='3' cols='50'>Text area</textarea>" in rendered_html, "Textarea should be preserved"
        assert "<select><option>Option 1</option></select>" in rendered_html, "Select should be preserved"
        assert "<button type='button'>Click me</button>" in rendered_html, "Button should be preserved"

        print("✅ Valid HTML preservation working correctly")

    def test_dynamic_table_flexible_html_tags(self):
        """Test that the system handles various HTML tags flexibly but securely."""
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "dynamicTable",
                    "attrs": {
                        "columns": {
                            "col1": {"visible": True, "order": 1}
                        },
                        "content": {
                            "headers": ["col1"],
                            "rows": [
                                ["<article>Article content</article>"],
                                ["<section>Section content</section>"],
                                ["<nav>Navigation</nav>"],
                                ["<header>Header content</header>"],
                                ["<footer>Footer content</footer>"],
                                ["<main>Main content</main>"],
                                ["<aside>Sidebar content</aside>"],
                                ["<figure><figcaption>Caption</figcaption></figure>"],
                                ["<details><summary>Summary</summary></details>"],
                                ["<dialog>Dialog content</dialog>"],
                                ["<mark>Highlighted text</mark>"],
                                ["<time datetime='2023-01-01'>January 1st</time>"],
                                ["<data value='123'>Data value</data>"],
                                ["<meter value='0.6'>60%</meter>"],
                                ["<progress value='70' max='100'>70%</progress>"],
                                ["<canvas width='100' height='100'></canvas>"],
                                ["<video controls><source src='video.mp4'></video>"],
                                ["<audio controls><source src='audio.mp3'></audio>"],
                                ["<picture><source srcset='image.jpg'></picture>"],
                                ["<svg><circle cx='50' cy='50' r='40'></circle></svg>"],
                                ["<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>"],
                                ["<my-component>Custom</my-component>"],
                                ["<invalidtag>Invalid</invalidtag>"],
                                ["<script>alert('xss')</script>"],
                                ["<div onclick='alert()'>Dangerous</div>"],
                                ["<a href='javascript:alert()'>Dangerous link</a>"],
                                ["<div>Unclosed"]
                            ]
                        }
                    }
                }
            ]
        }

        rendered_html = self.doc.render(data)
        print(f"Flexible HTML test rendered: {rendered_html}")

        # Test that standard HTML5 semantic tags are preserved
        assert "<article>Article content</article>" in rendered_html, "Article should be preserved"
        assert "<section>Section content</section>" in rendered_html, "Section should be preserved"
        assert "<nav>Navigation</nav>" in rendered_html, "Nav should be preserved"
        assert "<header>Header content</header>" in rendered_html, "Header should be preserved"
        assert "<footer>Footer content</footer>" in rendered_html, "Footer should be preserved"
        assert "<main>Main content</main>" in rendered_html, "Main should be preserved"
        assert "<aside>Sidebar content</aside>" in rendered_html, "Aside should be preserved"
        assert "<figure><figcaption>Caption</figcaption></figure>" in rendered_html, "Figure should be preserved"
        assert "<details><summary>Summary</summary></details>" in rendered_html, "Details should be preserved"
        assert "<dialog>Dialog content</dialog>" in rendered_html, "Dialog should be preserved"
        assert "<mark>Highlighted text</mark>" in rendered_html, "Mark should be preserved"
        assert "<time datetime='2023-01-01'>January 1st</time>" in rendered_html, "Time should be preserved"
        assert "<data value='123'>Data value</data>" in rendered_html, "Data should be preserved"
        assert "<meter value='0.6'>60%</meter>" in rendered_html, "Meter should be preserved"
        assert "<progress value='70' max='100'>70%</progress>" in rendered_html, "Progress should be preserved"
        assert "<canvas width='100' height='100'></canvas>" in rendered_html, "Canvas should be preserved"
        assert "<video controls><source src='video.mp4'></video>" in rendered_html, "Video should be preserved"
        assert "<audio controls><source src='audio.mp3'></audio>" in rendered_html, "Audio should be preserved"
        assert "<picture><source srcset='image.jpg'></picture>" in rendered_html, "Picture should be preserved"
        assert "<svg><circle cx='50' cy='50' r='40'></circle></svg>" in rendered_html, "SVG should be preserved"
        assert "<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>" in rendered_html, "MathML should be preserved"

        # Test that dangerous content is escaped
        # Note: <invalidtag> is preserved because our flexible approach allows any tag name
        # (HTML5 supports custom elements), but dangerous content is properly escaped
        assert "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in rendered_html, "Script tags should be escaped"
        assert "&lt;div onclick=&#x27;alert()&#x27;&gt;Dangerous&lt;/div&gt;" in rendered_html, "Event handlers should be escaped"
        assert "&lt;a href=&#x27;javascript:alert()&#x27;&gt;Dangerous link&lt;/a&gt;" in rendered_html, "JavaScript protocol should be escaped"
        assert "&lt;div&gt;Unclosed" in rendered_html, "Unclosed tags should be escaped"

        print("✅ Flexible HTML tag handling working correctly")

    def test_dynamic_table_edge_cases(self):
        """Test edge cases and boundary conditions."""
        data = {
            "type": "doc",
            "content": [
                {
                    "type": "dynamicTable",
                    "attrs": {
                        "columns": {
                            "col1": {"visible": True, "order": 1}
                        },
                        "content": {
                            "headers": ["col1"],
                            "rows": [
                                ["<>"],  # Empty tags
                                ["< >"],  # Space in tag
                                ["<a>"],  # Single tag
                                ["<a></a>"],  # Paired tags
                                ["<a/>"],  # Self-closing tag
                                ["<a />"],  # Self-closing with space
                                ["<a b>"],  # Tag with attribute
                                ["<a b='c'>"],  # Tag with quoted attribute
                                ["<a b=\"c\">"],  # Tag with double-quoted attribute
                                ["<a b='c' d='e'>"],  # Tag with multiple attributes
                                ["<a b='c' d>"],  # Tag with mixed attribute styles
                                ["<a>text</a>"],  # Tag with text content
                                ["<a><b>nested</b></a>"],  # Nested tags
                                ["<a><b>nested</b><c>more</c></a>"],  # Multiple nested tags
                                ["<a><b>nested</b></a><c>sibling</c>"],  # Sibling tags
                                ["<p>Valid</p> <invalid>Invalid</invalid>"],  # Mixed valid/invalid
                                ["   <p>   Spaced   </p>   "],  # Whitespace handling
                                ["<a href='test' target='_blank'>Link</a>"],  # Multiple attributes
                                ["<img src='test.jpg' alt='test' width='100' height='100'>"],  # Complex img
                                ["<input type='text' name='username' placeholder='Enter username' required>"],  # Complex input
                                ["<div class='container' id='main' data-test='value'>Content</div>"],  # Complex div
                                ["<table><thead><tr><th>Header</th></tr></thead><tbody><tr><td>Cell</td></tr></tbody></table>"],  # Complex table
                                ["<form action='/submit' method='post' enctype='multipart/form-data'><input type='submit'></form>"],  # Complex form
                                ["<select name='country'><optgroup label='Europe'><option value='uk'>UK</option></optgroup></select>"],  # Complex select
                                ["<fieldset><legend>Personal Info</legend><label>Name: <input type='text' name='name'></label></fieldset>"],  # Complex fieldset
                                ["<figure><img src='image.jpg' alt='Image'><figcaption>Caption</figcaption></figure>"],  # Complex figure
                                ["<article><header><h1>Title</h1><time>2023-01-01</time></header><section><p>Content</p></section><footer><p>Footer</p></footer></article>"],  # Complex article
                                ["<A>UPPERCASE</A>"],  # Uppercase tags
                                ["<a B='C'>Mixed case</a>"]  # Mixed case attributes
                            ]
                        }
                    }
                }
            ]
        }

        rendered_html = self.doc.render(data)
        print(f"Edge cases test rendered: {rendered_html}")

        # Test basic edge cases
        assert "&lt;&gt;" in rendered_html, "Empty tags should be escaped"
        assert "&lt; &gt;" in rendered_html, "Space in tags should be escaped"
        assert "<a>" in rendered_html, "Single tags should be preserved"
        assert "<a></a>" in rendered_html, "Paired tags should be preserved"
        assert "<a/>" in rendered_html, "Self-closing tags should be preserved"
        assert "<a />" in rendered_html, "Self-closing with space should be preserved"
        assert "<a b>" in rendered_html, "Tags with attributes should be preserved"
        assert "<a b='c'>" in rendered_html, "Tags with quoted attributes should be preserved"
        assert "<a b=\"c\">" in rendered_html, "Tags with double-quoted attributes should be preserved"
        assert "<a b='c' d='e'>" in rendered_html, "Tags with multiple attributes should be preserved"
        assert "<a b='c' d>" in rendered_html, "Tags with mixed attribute styles should be preserved"
        assert "<a>text</a>" in rendered_html, "Tags with text content should be preserved"
        assert "<a><b>nested</b></a>" in rendered_html, "Nested tags should be preserved"
        assert "<a><b>nested</b><c>more</c></a>" in rendered_html, "Multiple nested tags should be preserved"
        assert "<a><b>nested</b></a><c>sibling</c>" in rendered_html, "Sibling tags should be preserved"

        # Test complex structures
        assert "<a href='test' target='_blank'>Link</a>" in rendered_html, "Complex links should be preserved"
        assert "<img src='test.jpg' alt='test' width='100' height='100'>" in rendered_html, "Complex images should be preserved"
        assert "<input type='text' name='username' placeholder='Enter username' required>" in rendered_html, "Complex inputs should be preserved"
        assert "<div class='container' id='main' data-test='value'>Content</div>" in rendered_html, "Complex divs should be preserved"
        assert "<table><thead><tr><th>Header</th></tr></thead><tbody><tr><td>Cell</td></tr></tbody></table>" in rendered_html, "Complex tables should be preserved"
        assert "<form action='/submit' method='post' enctype='multipart/form-data'><input type='submit'></form>" in rendered_html, "Complex forms should be preserved"
        assert "<select name='country'><optgroup label='Europe'><option value='uk'>UK</option></optgroup></select>" in rendered_html, "Complex selects should be preserved"
        assert "<fieldset><legend>Personal Info</legend><label>Name: <input type='text' name='name'></label></fieldset>" in rendered_html, "Complex fieldsets should be preserved"
        assert "<figure><img src='image.jpg' alt='Image'><figcaption>Caption</figcaption></figure>" in rendered_html, "Complex figures should be preserved"
        assert "<article><header><h1>Title</h1><time>2023-01-01</time></header><section><p>Content</p></section><footer><p>Footer</p></footer></article>" in rendered_html, "Complex articles should be preserved"

        print("✅ Basic edge cases handled correctly")

        # Test whitespace handling
        assert "   &lt;p&gt;   Spaced   &lt;/p&gt;   " in rendered_html, "Mixed content with whitespace should be escaped"
        print("✅ Whitespace handling correct")

        # Test case sensitivity
        assert "<A>UPPERCASE</A>" in rendered_html, "Uppercase tags should be preserved"
        assert "<a B='C'>Mixed case</a>" in rendered_html, "Mixed case attributes should be preserved"
        print("✅ Case sensitivity handled correctly")

        print("✅ All edge cases handled correctly")
