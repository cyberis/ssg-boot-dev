from textnode import TextType
from htmlnode import LeafNode, ParentNode
from blocknode import BlockNode, BlockType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", value=text_node.text)
        case TextType.CODE:
            return LeafNode("code", value=text_node.text)
        case TextType.LINK:
            return LeafNode("a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def block_node_to_html_node(block_node):
    match block_node.block_type:
        case BlockType.PARAGRAPH:
            children = [text_node_to_html_node(tn) for tn in block_node.text_nodes]
            return ParentNode("p", children)
        case BlockType.HEADING:
            level = block_node.props.get("level", 1)
            tag = f"h{level}"
            children = [text_node_to_html_node(tn) for tn in block_node.text_nodes]
            return ParentNode(tag, children)
        case BlockType.UNORDERED_LIST:
            children = []
            for child_block in block_node.child_blocks:
                child_html_node = block_node_to_html_node(child_block)
                children.append(child_html_node)
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = []
            for child_block in block_node.child_blocks:
                child_html_node = block_node_to_html_node(child_block)
                children.append(child_html_node)
            return ParentNode("ol", children)
        case BlockType.LIST_ITEM:
            children = [text_node_to_html_node(tn) for tn in block_node.text_nodes]
            return ParentNode("li", children)
        case BlockType.CODE_BLOCK:
            children = [text_node_to_html_node(tn) for tn in block_node.text_nodes]
            return ParentNode("pre", [ParentNode("code", children)])
        case BlockType.BLOCKQUOTE:
            children = [text_node_to_html_node(tn) for tn in block_node.text_nodes]
            return ParentNode("blockquote", children)
        case _:
            raise ValueError(f"Unsupported BlockType: {block_node.block_type}")
                
        