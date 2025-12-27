import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from htmlnodes import text_node_to_html_node

class TestHtmlNodes(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Just some text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode(None, "Just some text")
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("b", "Bold text")
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("i", "Italic text")
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("code", "Code snippet")
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("a", "Click here", props={"href": "https://example.com"})
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        expected_node = LeafNode("img", "", props={"src": "https://example.com/image.png", "alt": "An image"})
        self.assertEqual(html_node, expected_node)
        
    def test_text_node_to_html_node_unsupported_type(self):
        class FakeTextType:
            UNKNOWN = 99
            
        text_node = TextNode("Unknown type", FakeTextType.UNKNOWN)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
            
if __name__ == '__main__':
    unittest.main()