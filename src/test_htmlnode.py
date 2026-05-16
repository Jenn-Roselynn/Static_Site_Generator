import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
