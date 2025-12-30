from platform import node
import unittest
from blocknode import BlockType
from blocknodes import markdown_to_blocks, block_to_block_type, markdown_to_html_node

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
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )
        self.assertEqual(html,expected_html)
        
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )
        self.assertEqual(html, expected_html)
    
    def test_lists(self):
        md = """
This is a paragraph before **the list**.

- This is a list
- with items

This is a paragraph _between_ lists.

1. First item
2. Second item
3. Third item

This is a paragraph after the lists.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><p>This is a paragraph before <b>the list</b>.</p>"
            "<ul><li>This is a list</li><li>with items</li></ul>"
            "<p>This is a paragraph <i>between</i> lists.</p>"
            "<ol><li>First item</li><li>Second item</li><li>Third item</li></ol>"
            "<p>This is a paragraph after the lists.</p></div>"
        )
        self.assertEqual(html, expected_html)
    
    def test_blockquotes(self):
        md = """
> This is a blockquote. `print("Hello")`
> Dude, I'm quoting!

Good stuff dude.    
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><blockquote>This is a blockquote. <code>print(\"Hello\")</code> Dude, I'm quoting!</blockquote><p>Good stuff dude.</p></div>"
        )
        self.assertEqual(html, expected_html)

    def test_headings(self):
        md = """
# Heading 1

Here is some text under heading 1.

## Heading 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><h1>Heading 1</h1><p>Here is some text under heading 1.</p><h2>Heading 2</h2></div>"
        )
        self.assertEqual(html, expected_html)
        
    def test_images_and_links(self):
        md = """
Here is an image: ![Alt text](https://example.com/image.png) and a [link](https://example.com).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><p>Here is an image: <img src=\"https://example.com/image.png\" alt=\"Alt text\"></img> and a <a href=\"https://example.com\">link</a>.</p></div>"
        )
        self.assertEqual(html, expected_html)
    
    def test_menu_links_in_unordered_list(self):
        md = """
- [Home](https://example.com/home)
- [About](https://example.com/about)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><ul><li><a href=\"https://example.com/home\">Home</a></li><li><a href=\"https://example.com/about\">About</a></li></ul></div>"
        )
        self.assertEqual(html, expected_html)
    
if __name__ == '__main__':
    unittest.main()