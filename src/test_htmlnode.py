import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test basic conversion of a properties dictionary
        node = HTMLNode(
            tag="a",
            value="Boot.dev",
            props={"href": "https://www.boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_empty(self):
        # Test handling when props is None or empty
        node = HTMLNode(tag="p", value="Hello World")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        # Test that the __repr__ prints the properties accurately for debugging
        node = HTMLNode(tag="h1", value="Header Text")
        expected_repr = "HTMLNode(tag=h1, value=Header Text, children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        # Test basic tag rendering
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw_text(self):
        # Test rendering when tag is None (should return raw text)
        node = LeafNode(None, "Just raw text here.")
        self.assertEqual(node.to_html(), "Just raw text here.")

    def test_leaf_to_html_with_props(self):
        # Test rendering a leaf node containing attributes
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

if __name__ == "__main__":
    unittest.main()