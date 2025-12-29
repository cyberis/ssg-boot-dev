import re
from blocknode import BlockType, BlockNode
from htmlnode import ParentNode
from textnodes import block_create_textnodes
from htmlnodes import block_node_to_html_node


def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split('\n\n')
    markdown_blocks = [block.strip() for block in markdown_blocks if block.strip()]
    return markdown_blocks

def block_is_ordered_list(block):
    lines = block.splitlines()
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            return False
    return True

def block_to_block_type(block):
    if re.match(r'^#{1,6} \w+', block):
        return BlockType.HEADING
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif block_is_ordered_list(block):
        return BlockType.ORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE_BLOCK
    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.BLOCKQUOTE
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = BlockNode(block, block_type)
        block_node = block_create_textnodes(block_node)
        block_html_node = block_node_to_html_node(block_node)
        html_nodes.append(block_html_node)
    container = ParentNode("div", html_nodes)
    return container