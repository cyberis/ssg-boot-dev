import unittest
from textnode import TextNode, TextType
from src.markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestNodes(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),            
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),            
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_delim_unmatched(self):
        node = TextNode("This is **invalid bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_extract_markdown_images_one(self):
        text = "Here is an image ![Alt Text](https://example.com/image.png) in the text."
        images = extract_markdown_images(text)
        expected = [("Alt Text", "https://example.com/image.png")]
        self.assertEqual(images, expected)
        
    def test_markdown_images_multiple(self):
        text = "Image one ![First Image](https://example.com/1.png) and image two ![Second Image](https://example.com/2.png)."
        images = extract_markdown_images(text)
        expected = [
            ("First Image", "https://example.com/1.png"),
            ("Second Image", "https://example.com/2.png"),
        ]
        self.assertEqual(images, expected)
        
    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        images = extract_markdown_images(text)
        expected = []
        self.assertEqual(images, expected)
    
    def test_extract_markdown_links_one(self):
        text = "Click [here](https://example.com) for more info."
        links = extract_markdown_links(text)
        expected = [("here", "https://example.com")]
        self.assertEqual(links, expected)
        
    def test_extract_markdown_links_multiple(self):
        text = "Visit [Google](https://google.com) or [Bing](https://bing.com) for searching."
        links = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("Bing", "https://bing.com"),
        ]
        self.assertEqual(links, expected)
        
    def test_extract_markdown_links_none(self):
        text = "No links are present in this text."
        links = extract_markdown_links(text)
        expected = []
        self.assertEqual(links, expected)
        
    def test_extract_markdown_links_and_images(self):
        text = "Here is an image ![Alt](https://example.com/img.png) and a link [Click](https://example.com)."
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        expected_images = [("Alt", "https://example.com/img.png")]
        expected_links = [("Click", "https://example.com")]
        self.assertEqual(images, expected_images)
        self.assertNotEqual(links, expected_links) # Intentional fail to show separation, images look like links
        
if __name__ == '__main__':
    unittest.main()