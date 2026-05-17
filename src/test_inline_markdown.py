import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_delimiter_bold(self):
        node = TextNode("Text with **bold content** right here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold content", TextType.BOLD),
                TextNode(" right here", TextType.TEXT),
            ]
        )

    def test_split_delimiter_italic(self):
        node = TextNode("*Italic phrase* at the start of the sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Italic phrase", TextType.ITALIC),
                TextNode(" at the start of the sentence", TextType.TEXT),
            ]
        )

    def test_split_delimiter_unclosed(self):
        # Verify that unclosed markdown elements trigger a syntax ValueError
        node = TextNode("This is broken **bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
