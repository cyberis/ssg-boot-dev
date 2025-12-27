import unittest
from blocknode import BlockType
from blocknodes import markdown_to_blocks, block_to_block_type

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
        
    def test_block_type_detection_heading(self):
        block1 = "# This is a heading"
        block_type1 = block_to_block_type(block1)
        self.assertEqual(block_type1, BlockType.HEADING)
        block2 = "## Subheading"
        block_type2 = block_to_block_type(block2)
        self.assertEqual(block_type2, BlockType.HEADING)
        block3 = "###### Smallest heading"
        block_type3 = block_to_block_type(block3)
        self.assertEqual(block_type3, BlockType.HEADING)
        
    def test_block_type_detection_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_type_detection_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_block_type_detection_code_block(self):
        block = "```\ndef example():\n    return True\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE_BLOCK)
        
    def test_block_type_detection_blockquote(self):
        block = "> This is a quote.\n> It spans multiple lines."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.BLOCKQUOTE)
        
    def test_block_type_detection_paragraph(self):
        block = "This is a regular paragraph without any special formatting."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_type_detection_malformed_heading(self):
        block = "####### Too many hashes for a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_type_detection_malformed_unordered_list(self):
        block = "- This is a valid unordered list item\n* but this is not"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_type_detection_malformed_ordered_list(self):
        block = "10. This is not a valid ordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_type_detection_incomplete_code_block(self):
        block = "```\ndef example():\n    return True"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_type_detection_incomplete_blockquote(self):
        block = "> This is a quote.\nThis line is not part of the quote."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()