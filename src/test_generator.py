import unittest
from generator import extract_title

class TestGenerator(unittest.TestCase):
    def test_extract_title_found(self):
        markdown = """
# My Title
This is some content.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")
        
    def test_extract_title_not_found(self):
        markdown = """
This is some content without a title.
"""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")
        
    def test_extract_title_multiple_lines(self):
        markdown = """
Some intro text.
# Another Title
More content here.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Another Title")
        
    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")
        
    def test_extract_title_h2(self):
        markdown = """
## Subtitle Here
Content follows.
"""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")
        
if __name__ == '__main__':
    unittest.main()