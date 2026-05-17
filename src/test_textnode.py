import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is an apple", TextType.TEXT)
        node2 = TextNode("This is an orange", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("Same text content", TextType.BOLD)
        node2 = TextNode("Same text content", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # --- Conversion Function Tests ---

    def test_text_node_to_html_text(self):
        # Verify basic raw text conversion has no tag wrapper
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_link(self):
        # Verify links map the anchor content to value and url to props
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_text_node_to_html_image(self):
        # Verify images use empty string values and extract source/alt tags
        node = TextNode("Cute cat picture", TextType.IMAGE, "https://www.cats.com/pic.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.cats.com/pic.png", "alt": "Cute cat picture"}
        )

if __name__ == "__main__":
    unittest.main()
