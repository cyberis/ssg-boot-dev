import unittest
from textnode import TextNode, TextType
from textnodes import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes,
)

class TestTextNodes(unittest.TestCase):
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
        
    def test_split_images_one(self):
        node = TextNode("Text before image ![Alt Text](https://example.com/image.png) text after image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("Text before image ", TextType.TEXT),
            TextNode("Alt Text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" text after image.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_images_multiple(self):
        node = TextNode("Image one ![First Image](https://example.com/1.png) and image two ![Second Image](https://example.com/2.png).", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("Image one ", TextType.TEXT),
            TextNode("First Image", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" and image two ", TextType.TEXT),
            TextNode("Second Image", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_images_none(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [TextNode("This text has no images.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_links_one(self):
        node = TextNode("Click [here](https://example.com) for more info.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" for more info.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_links_multiple(self):
        node = TextNode("Visit [Google](https://google.com) or [Bing](https://bing.com) for searching.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
            TextNode(" for searching.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_links_none(self):
        node = TextNode("No links are present in this text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [TextNode("No links are present in this text.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
        
    # Test Case 1 - All Elements Included
    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes) 
    
    # Test Case 2 - No Special Formatting
    def test_text_to_textnodes_2(self):
        text = "Just some plain text without any special formatting."
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Just some plain text without any special formatting.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    # Test Case 3 - Malformed Markdown
    def test_text_to_textnodes_3(self):
        text = "This is **bold text with no ending and an _italic_ word"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)
            
    # Test Case 4 - Nested Formatting (should not be supported)
    def test_text_to_textnodes_4(self):
        text = "This is _italic and **bold** text_"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)
            
    # Test Case 5 - Link at the Start
    def test_text_to_textnodes_5(self):
        text = "[Start Link](https://start.com) followed by text."
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Start Link", TextType.LINK, "https://start.com"),
            TextNode(" followed by text.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    #Test Caste 6 - Image at the End
    def test_text_to_textnodes_6(self):
        text = "Text before image ![End Image](https://end.com/image.png)"
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Text before image ", TextType.TEXT),
            TextNode("End Image", TextType.IMAGE, "https://end.com/image.png"),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
if __name__ == '__main__':
    unittest.main()