import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excess_newlines(self):
        # Test handling multiple trailing or excessive spacing variations safely
        md = """
# This is a heading



This is a paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph.",
            ]
        )

    def test_block_to_block_types(self):
        # 1. Test happy paths for various block types
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> quote\n> line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Just a regular paragraph."), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        # 2. Test that broken number increments fall back to a standard paragraph
        block = "1. First item\n3. Wrong sequence number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        # 3. Test that mixed blocks fall back to paragraph
        block = "- Item 1\n This line has no dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")
        self.assertEqual(extract_title("#   Spaced Heading  "), "Spaced Heading")
        with self.assertRaises(Exception):
            extract_title("## No h1 header")
if __name__ == "__main__":
    unittest.main()