import re
from textnode import TextNode, TextType
from blocknode import BlockNode, BlockType

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

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

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
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def block_create_textnodes(block_node):
    if not isinstance(block_node, BlockNode):
        raise ValueError("Input must be a BlockNode")
    child_text_nodes = []
    block_type = block_node.block_type
    match block_type:
        case BlockType.HEADING:
            level = len(re.match(r'^(#+)', block_node.content).group(1))
            block_node.props['level'] = level
            text = re.sub(r'^#{1,6} ', '', block_node.content)
            text_node = TextNode(text, TextType.TEXT)
            child_text_nodes.append(text_node)
        case BlockType.PARAGRAPH:
            # Combine all lines into a single paragraph text
            text = ""
            for line in block_node.content.splitlines():
                text += line.strip() + " "
            text_nodes = text_to_textnodes(text.strip())
            child_text_nodes.extend(text_nodes)
        case BlockType.UNORDERED_LIST:
            lines = block_node.content.splitlines()
            if not block_node.child_blocks:
                block_node.child_blocks = []
            for line in lines:
                text = re.sub(r'^- ', '', line)
                child_block = BlockNode(text, BlockType.LIST_ITEM)
                child_block = block_create_textnodes(child_block)
                block_node.child_blocks.append(child_block)
        case BlockType.ORDERED_LIST:
            lines = block_node.content.splitlines()
            if not block_node.child_blocks:
                block_node.child_blocks = []
            for line in lines:
                text = re.sub(r'^\d+\. ', '', line)
                child_block = BlockNode(text, BlockType.LIST_ITEM)
                child_block = block_create_textnodes(child_block)
                block_node.child_blocks.append(child_block)
        case BlockType.LIST_ITEM:
            text_nodes = text_to_textnodes(block_node.content)
            child_text_nodes.extend(text_nodes)
        case BlockType.CODE_BLOCK:
            text = re.sub(r'^```', '', block_node.content)
            text = re.sub(r'```$', '', text)
            # Remove leading newline if present due to markdown code block formatting
            if text.startswith('\n'):
                text = text[1:]
            text_node = TextNode(text, TextType.TEXT)
            child_text_nodes.append(text_node)
        case BlockType.BLOCKQUOTE:
            lines = block_node.content.splitlines()
            quote_text = '\n'.join([re.sub(r'^> ?', '', line) for line in lines])
            text_node = TextNode(quote_text, TextType.TEXT)
            child_text_nodes.append(text_node)
    
    block_node.text_nodes = child_text_nodes
    return block_node