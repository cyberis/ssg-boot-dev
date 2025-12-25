import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a different test node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a test node", TextType.ITALIC)
        self.assertEqual(repr(node), "TextNode(This is a test node, italic, None)")
        
    def test_link_node(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
        self.assertEqual(repr(node), "TextNode(Click here, link, https://example.com)")
    
    def test_diff_types(self):
        text_node = TextNode("Some text", TextType.TEXT)
        bold_node = TextNode("Some text", TextType.BOLD)
        italic_node = TextNode("Italic text", TextType.ITALIC)
        code_node = TextNode("Code snippet", TextType.CODE)
        self.assertNotEqual(text_node, bold_node)
        self.assertNotEqual(bold_node, italic_node)
        self.assertNotEqual(italic_node, code_node)
        
if __name__ == '__main__':
    unittest.main()