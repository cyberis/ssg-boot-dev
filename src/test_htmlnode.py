import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", None, None, {"class": "container"})
        node2 = HTMLNode("div", None, None, {"class": "container"})
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = HTMLNode("div", None, None, {"class": "container"})
        node2 = HTMLNode("p", "Hello world", None, {"class": "info"})
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = HTMLNode("span", "Red Text", None, {"style": "color:red;"})
        self.assertEqual(repr(node), "HTMLNode(tag=span, value=Red Text, children=None, props={'style': 'color:red;'})")

    def test_different_tags(self):
        div_node = HTMLNode("div", None, None, {"class": "container"})
        span_node = HTMLNode("span", "Content", None, {"class": "special"})
        self.assertNotEqual(div_node, span_node)
        
    def test_props_to_html(self):
        node = HTMLNode("a", "Link", None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
        
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
            
    def test_leaf_with_children(self):
        with self.assertRaises((TypeError, ValueError)):
            LeafNode("p", "Hello", props={"class": "text"}, children=[HTMLNode("span", "Child")])
            
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_doc_fragment(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        child3 = LeafNode("p", "Paragraph 3")
        child4 = LeafNode("p", "Paragraph 4")
        parent1 = ParentNode("div", [child1, child2], props={"class": "section"})
        parent2 = ParentNode("div", [child3, child4], props={"class": "section"})
        grandparent = ParentNode("div", [parent1, parent2], props={"id": "about-us"})
        doc_fragment = ParentNode("div", [grandparent], props={"id": "doc-fragment"})
        self.assertEqual(
            doc_fragment.to_html(),
            '<div id="doc-fragment"><div id="about-us"><div class="section"><p>Paragraph 1</p><p>Paragraph 2</p></div><div class="section"><p>Paragraph 3</p><p>Paragraph 4</p></div></div></div>',
        )