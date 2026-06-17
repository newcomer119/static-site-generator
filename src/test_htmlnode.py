import unittest
from htmlnode import HTMLNode, LeafNode , ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_values(self):
        # 1. Test normal props formatting with leading spaces
        node = HTMLNode(
            "a", 
            "Boot.dev", 
            props={"href": "https://www.boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_empty_or_none(self):
        # 2. Test that None or empty props return an empty string safely
        node_none = HTMLNode("p", "Hello World", props=None)
        node_empty = HTMLNode("p", "Hello World", props={})
        
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr_output(self):
        # 3. Test that our __repr__ prints values clearly for debugging
        node = HTMLNode("h1", "Title Text")
        expected_repr = "HTMLNode(h1, Title Text, children: None, None)"
        self.assertEqual(repr(node), expected_repr)


    def test_leaf_to_html_p(self):
        # 1. Test basic paragraph tag rendering
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        # 2. Test rendering with attributes (props)
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        # 3. Test rendering raw text when tag is None
        node = LeafNode(None, "Just some plain text content.")
        self.assertEqual(node.to_html(), "Just some plain text content.")


    def test_to_html_with_children(self):
        # 1. Basic test with a leaf child node
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        # 2. Deep recursion check with a grandchild node
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        # 3. Test mixing parent nodes, leaf nodes, and plain text
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i></p>"
        )
    
if __name__ == "__main__":
    unittest.main()