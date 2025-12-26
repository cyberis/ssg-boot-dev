import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:  #We are only splitting text nodes
            new_nodes.append(node)
            continue
        delimiter_count = node.text.count(delimiter)
        if delimiter_count % 2 != 0:
            raise ValueError(f'Invalid Markdown - Missing delimiter "{delimiter}"')
        elif delimiter_count == 0:  # The delimiter wasn't found in the text so just resturn it as is
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:
                    new_node = TextNode(part, TextType.TEXT)
                else:
                    new_node = TextNode(part, text_type)
                new_nodes.append(new_node)
    return new_nodes       

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches
    images = []
    for alt_text, url in matches:
        images.append(TextNode(alt_text, TextType.IMAGE, url))
    return images

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches
    links = []
    for link_text, url in matches:
        links.append(TextNode(link_text, TextType.LINK, url))
    return links