import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_standard_h1(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_h1_with_whitespace(self):
        md = "   #    Tolkien Fan Club   "
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_multiple_lines_with_h1(self):
        md = "\n\n# Main Title\nSome content text.\n## Subtitle"
        self.assertEqual(extract_title(md), "Main Title")

    def test_no_h1_raises_exception(self):
        md = "## Subheading only\nNo matching h1 elements here."
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
