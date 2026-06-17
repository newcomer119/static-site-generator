import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # 1. Tests that two identical nodes are equal (with default URL=None)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        # 2. Tests that two nodes with identical URLs are equal
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_type(self):
        # 3. Tests that different TextTypes make the nodes unequal
        node = TextNode("This is text", TextType.NORMAL)
        node2 = TextNode("This is text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text(self):
        # 4. Tests that different text content makes the nodes unequal
        node = TextNode("Apple", TextType.CODE)
        node2 = TextNode("Banana", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        # 5. Tests that one node having a URL and the other having None makes them unequal
        node = TextNode("Image node", TextType.IMAGE, "https://boot.dev/logo.png")
        node2 = TextNode("Image node", TextType.IMAGE)
        self.assertNotEqual(node, node2)


    def test_text_node_to_html_node_text(self):
        # 1. Test normal/plain text node conversion
        node = TextNode("This is a text node", TextType.NORMAL) # Adjust to .TEXT if applicable
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_link(self):
        # 2. Test hyperlink conversion with href attribute mapping
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_text_node_to_html_node_image(self):
        # 3. Test image conversion where text acts as alt tags
        node = TextNode("An cute puppy", TextType.IMAGE, "https://boot.dev/puppy.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/puppy.png", "alt": "An cute puppy"})

if __name__ == "__main__":
    unittest.main()