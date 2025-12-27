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
        self.assertEqual(repr(block), "BlockNode(This is a heading., heading)")
        
if __name__ == '__main__':
    unittest.main()