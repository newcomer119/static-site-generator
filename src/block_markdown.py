from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped != "":
            filtered_blocks.append(stripped)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
        
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
        
    if block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
            
    if block.startswith("- "):
        is_ul = True
        for line in lines:
            if not line.startswith("- "):
                is_ul = False
                break
        if is_ul:
            return BlockType.UNORDERED_LIST
            
    if block.startswith("1. "):
        is_ol = True
        current_num = 1
        for line in lines:
            if not line.startswith(f"{current_num}. "):
                is_ol = False
                break
            current_num += 1
        if is_ol:
            return BlockType.ORDERED_LIST
            
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def extract_title(markdown):
    """Finds the first h1 (# ) in a document and returns its stripped content."""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Invalid Markdown: Missing an h1 header tag.")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            content = block[level + 1:]
            block_nodes.append(ParentNode(f"h{level}", text_to_children(content)))
            
        elif block_type == BlockType.CODE:
            content = block.strip("`").strip("\n")
            code_leaf = LeafNode("code", content)
            block_nodes.append(ParentNode("pre", [code_leaf]))
            
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                if line.startswith("> "):
                    cleaned_lines.append(line[2:])
                else:
                    cleaned_lines.append(line[1:])
            content = " ".join(cleaned_lines)
            block_nodes.append(ParentNode("blockquote", text_to_children(content)))
            
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                content = line[2:]
                li_nodes.append(ParentNode("li", text_to_children(content)))
            block_nodes.append(ParentNode("ul", li_nodes))
            
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                dot_index = line.find(". ")
                content = line[dot_index + 2:]
                li_nodes.append(ParentNode("li", text_to_children(content)))
            block_nodes.append(ParentNode("ol", li_nodes))
            
        else:
            content = " ".join(block.split("\n"))
            block_nodes.append(ParentNode("p", text_to_children(content)))
            
    return ParentNode("div", block_nodes)