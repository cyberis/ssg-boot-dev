import unittest
from blocknode import BlockNode, BlockType

class TestBlockNode(unittest.TestCase):
    def test_eq(self):
        block1 = BlockNode("This is a paragraph.", BlockType.PARAGRAPH)
        block2 = BlockNode("This is a paragraph.", BlockType.PARAGRAPH)
        self.assertEqual(block1, block2)
    
    def test_neq_content(self):
        block1 = BlockNode("This is a paragraph.", BlockType.PARAGRAPH)
        block2 = BlockNode("This is a different paragraph.", BlockType.PARAGRAPH)
        self.assertNotEqual(block1, block2)
        
    def test_neq_type(self):
        block1 = BlockNode("This is a paragraph.", BlockType.PARAGRAPH)
        block2 = BlockNode("# TITLE", BlockType.HEADING)
        self.assertNotEqual(block1, block2)
        
    def test_repr(self):
        block = BlockNode("This is a heading.", BlockType.HEADING)
        self.assertEqual(repr(block), "BlockNode(content=This is a heading., type=heading, child_blocks=None, text_nodes=None, props=None)")
    
    def test_repr_with_props(self):
        block = BlockNode("This is a heading.", BlockType.HEADING, props={"level": 2})
        self.assertEqual(repr(block), "BlockNode(content=This is a heading., type=heading, child_blocks=None, text_nodes=None, props={'level': 2})")
        
    def test_repr_with_children(self):
        child_block = BlockNode("List item 1", BlockType.LIST_ITEM)
        block = BlockNode("- List item 1", BlockType.UNORDERED_LIST, child_blocks=[child_block])
        self.assertEqual(repr(block), "BlockNode(content=- List item 1, type=unordered_list, child_blocks=[BlockNode(content=List item 1, type=list_item, child_blocks=None, text_nodes=None, props=None)], text_nodes=None, props=None)")
    
    def test_repr_with_textnodes(self):
        text_node = "This is a text node."  # Simplified for this test
        block = BlockNode("This is a paragraph.", BlockType.PARAGRAPH, text_nodes=[text_node])
        self.assertEqual(repr(block), "BlockNode(content=This is a paragraph., type=paragraph, child_blocks=None, text_nodes=['This is a text node.'], props=None)")
    
if __name__ == '__main__':
    unittest.main()