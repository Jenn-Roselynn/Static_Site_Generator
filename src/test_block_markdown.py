import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excess_newlines(self):
        md = """
# This is a heading



This is a paragraph with way too many newlines surrounding it.


- Item 1
- Item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph with way too many newlines surrounding it.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_block_to_block_types(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> quote\n> more quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- list\n- item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("just a normal paragraph text"), BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_lists(self):
        malformed_unordered = "- item 1\naccidental regular paragraph line"
        self.assertEqual(block_to_block_type(malformed_unordered), BlockType.PARAGRAPH)
        
        bad_order = "2. item 1\n3. item 2"
        self.assertEqual(block_to_block_type(bad_order), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
print("Hello, World!")
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print(\"Hello, World!\")\n</code></pre></div>",
        )

    def test_codeblock_multiline(self):
        md = """```
line 1
line 2
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>line 1\nline 2\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a heading

## This is a subheading

### This is a sub-subheading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a subheading</h2><h3>This is a sub-subheading</h3></div>",
        )

    def test_quotes(self):
        md = """
> This is a quote
> with multiple lines
> and some **bold** text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and some <b>bold</b> text.</blockquote></div>",
        )

    def test_unordered_lists(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_unordered_lists_nested(self):
        md = """
+ Item 1
+ Item 2
+ Nested item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Nested item</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_full_markdown_to_html_with_code_block(self):
        # Fixed: Outer spacing handles block identification; inner spacing is kept tight
        md = """
# Welcome to my blog

This is a paragraph of text.

- This is a list item
- This is another list item

```
print("Hello, World!")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>Welcome to my blog</h1><p>This is a paragraph of text.</p><ul><li>This is a list item</li><li>This is another list item</li></ul><pre><code>print(\"Hello, World!\")\n</code></pre></div>"
        self.assertEqual(html, expected_html)
if __name__ == "__main__":
    unittest.main()