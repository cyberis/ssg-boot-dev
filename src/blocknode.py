from enum import Enum

# Define our BlockTypes
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE_BLOCK = "code_block"
    BLOCKQUOTE = "blockquote"
    
class BlockNode():
    def __init__(self, content, block_type):
        self.content = content
        self.block_type = block_type
        
    def __eq__(self, other):
        return self.content == other.content and self.block_type == other.block_type
    
    def __repr__(self):
        return f"BlockNode({self.content}, {self.block_type.value})"