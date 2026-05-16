import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Baseline Test: Two entirely identical nodes must match perfectly
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        # Edge Case 1: Matching URLs should register as strictly equal
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        # Edge Case 2: Mismatched text content must fail the equality check
        node = TextNode("This is an apple", TextType.NORMAL)
        node2 = TextNode("This is an orange", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        # Edge Case 3: Mismatched formatting styles must fail the equality check
        node = TextNode("Same text content", TextType.BOLD)
        node2 = TextNode("Same text content", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
