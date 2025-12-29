from enum import Enum

# Define our BlockTypes
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    LIST_ITEM = "list_item"
    CODE_BLOCK = "code_block"
    BLOCKQUOTE = "blockquote"
    
class BlockNode():
    def __init__(self, content, block_type, child_blocks=None, text_nodes=None, props=None):
        self.content = content
        self.block_type = block_type
        self.child_blocks = child_blocks
        self.text_nodes = text_nodes
        self.props = props
        
    def __eq__(self, other):
        return (self.content == other.content and 
                self.block_type == other.block_type and 
                self.child_blocks == other.child_blocks and
                self.text_nodes == other.text_nodes and
                self.props == other.props)
    
    def __repr__(self):
        return f"BlockNode(content={self.content}, type={self.block_type.value}, child_blocks={self.child_blocks}, text_nodes={self.text_nodes}, props={self.props})"