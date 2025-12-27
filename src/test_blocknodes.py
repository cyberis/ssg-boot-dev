import unittest
from blocknodes import markdown_to_blocks

class TestBlockNodes(unittest.TestCase):
    def test_markdown_to_blocks_complex(self):
        markdown = """
# Title

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here

This is the same paragraph on a new line with no inline formatting.

- This is a list
- with items

``` 
def example():
    print("Hello, World!")
```

1. First item
2. Second item 
3. Third item

Here is an image: ![Alt text](https://example.com/image.png) and a [link](https://example.com).

> This is a blockquote.
> Programming is hard but fun!
"""
        blocks = markdown_to_blocks(markdown)
        expected_blocks = [
            "# Title",
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here",
            "This is the same paragraph on a new line with no inline formatting.",
            "- This is a list\n- with items",
            "``` \ndef example():\n    print(\"Hello, World!\")\n```",
            "1. First item\n2. Second item \n3. Third item",
            "Here is an image: ![Alt text](https://example.com/image.png) and a [link](https://example.com).",
            "> This is a blockquote.\n> Programming is hard but fun!"
        ]
        self.assertEqual(blocks, expected_blocks)
    
    def test_markdown_to_blocks_simple(self):
        markdown = "This is a simple paragraph."
        blocks = markdown_to_blocks(markdown)
        expected_blocks = ["This is a simple paragraph."]
        self.assertEqual(blocks, expected_blocks)
        
    def test_markdown_to_blocks_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        expected_blocks = []
        self.assertEqual(blocks, expected_blocks)
        
    def test_markdown_to_blocks_only_newlines(self):
        markdown = "\n\n\n"
        blocks = markdown_to_blocks(markdown)
        expected_blocks = []
        self.assertEqual(blocks, expected_blocks)  
        
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        markdown = "\n\nThis is a paragraph with leading and trailing newlines.\n\n"
        blocks = markdown_to_blocks(markdown)
        expected_blocks = ["This is a paragraph with leading and trailing newlines."]
        self.assertEqual(blocks, expected_blocks)
        
    def test_markdown_to_blocks_multiple_consecutive_newlines(self):
        markdown = "Paragraph one.\n\n\n\nParagraph two.\n\n\nParagraph three."
        blocks = markdown_to_blocks(markdown)
        expected_blocks = [
            "Paragraph one.",
            "Paragraph two.",
            "Paragraph three."
        ]
        self.assertEqual(blocks, expected_blocks)
        
    def test_markdown_to_blocks_no_double_newlines(self):
        markdown = "This is a single paragraph with no double newlines."
        blocks = markdown_to_blocks(markdown)
        expected_blocks = ["This is a single paragraph with no double newlines."]
        self.assertEqual(blocks, expected_blocks)
        
    def test_markdown_to_blocks_varied_spacing(self):
        markdown = "  \nThis is a paragraph with leading spaces.\n\nThis is another paragraph.\n   \n"
        blocks = markdown_to_blocks(markdown)
        expected_blocks = [
            "This is a paragraph with leading spaces.",
            "This is another paragraph."
        ]
        self.assertEqual(blocks, expected_blocks)
        

if __name__ == '__main__':
    unittest.main()