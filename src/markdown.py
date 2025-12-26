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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        parts = re.split(pattern, node.text)
        i = 0
        while i < len(parts):
            text_part = parts[i]
            if text_part:
                new_nodes.append(TextNode(text_part, TextType.TEXT))
            if i + 2 < len(parts):
                alt_text = parts[i + 1]
                url = parts[i + 2]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                i += 3
            else:
                break
        #if i == len(parts) - 1 and parts[i]:
        #    new_nodes.append(TextNode(parts[i], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        parts = re.split(pattern, node.text)
        i = 0
        while i < len(parts):
            text_part = parts[i]
            if text_part:
                new_nodes.append(TextNode(text_part, TextType.TEXT))
            if i + 2 < len(parts):
                link_text = parts[i + 1]
                url = parts[i + 2]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                i += 3
            else:
                break
        #if i == len(parts) - 1 and parts[i]:
        #    new_nodes.append(TextNode(parts[i], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes