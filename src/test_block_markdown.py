import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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
        # A list item where line 2 does not have the bullet token
        malformed_unordered = "- item 1\naccidental regular paragraph line"
        self.assertEqual(block_to_block_type(malformed_unordered), BlockType.PARAGRAPH)
        
        # An ordered list that does not start with 1
        bad_order = "2. item 1\n3. item 2"
        self.assertEqual(block_to_block_type(bad_order), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()