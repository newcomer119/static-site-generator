import unittest
from textnode import TextNode, TextType

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter_code(self):
        # 1. Test basic code delimiter splitting
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_bold(self):
        # 2. Test bold markdown tags
        node = TextNode("Hello **world** how are you", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("world", TextType.BOLD),
            TextNode(" how are you", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_italic(self):
        # 3. Test multi-character or italic syntax matching
        node = TextNode("_Italic text_ at the beginning", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Italic text", TextType.ITALIC),
            TextNode(" at the beginning", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_mismatched_delimiter(self):
        # 4. Test that unclosed markdown formatting throws errors gracefully
        node = TextNode("This is **broken bold formatting", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        # 1. Test image extraction with multiple images
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(matches, expected)

    def test_extract_markdown_links(self):
        # 2. Test normal hyperlink text extraction
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(matches, expected)

    def test_extract_links_ignores_images(self):
        # 3. Critical test: Link extractor should ignore images!
        text = "Here is a [link](https://boot.dev) and an image ![alt](https://boot.dev/pic.png)"
        matches = extract_markdown_links(text)
        expected = [("link", "https://boot.dev")]
        self.assertListEqual(matches, expected)

    def test_split_images(self):
        # 1. Test standard multi-image text parsing
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links(self):
        # 2. Test standard multi-link text parsing
        node = TextNode(
            "Text [link1](url1) mid text [link2](url2) tail",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" mid text ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" tail", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)


    def test_text_to_textnodes(self):
        # Test full parsing pipeline containing bold, italic, code, image, and link tokens
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()