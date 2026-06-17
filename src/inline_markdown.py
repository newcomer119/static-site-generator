from textnode import TextNode, TextType
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # We only look to split raw text/normal type nodes
        if old_node.text_type != TextType.NORMAL: # or TextType.TEXT depending on your enum key
            new_nodes.append(old_node)
            continue
            
        # Split the string by the delimiter
        parts = old_node.text.split(delimiter)
        
        # An even number of parts means a closing delimiter is missing
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: closing delimiter '{delimiter}' not found.")
            
        for i in range(len(parts)):
            # Skip empty strings (e.g., if delimiter is at the start or end)
            if parts[i] == "":
                continue
                
            # Even indices are raw text, odd indices are the text inside delimiters
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes


def extract_markdown_images(text):
    # Matches ![alt text](url)
    # Group 1 captures anything inside [], Group 2 captures everything inside ()
    pattern = r"!\[([^\[\]]*)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Matches [anchor text](url) while avoiding preceding exclamation marks
    pattern = r"(?<!!)\[([^\[\]]*)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        images = extract_markdown_images(current_text)
        
        # If no images found, keep the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
            
        for alt_text, url in images:
            # Reconstruct the raw markdown pattern to find where to split
            markdown_pattern = f"![{alt_text}]({url})"
            sections = current_text.split(markdown_pattern, 1)
            
            # If there's content before the image, make it a text node
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                
            # Append the actual Image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # The remainder of the string becomes our focus for the next iteration
            current_text = sections[1]
            
        # Don't forget any trailing text after the final image!
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        links = extract_markdown_links(current_text)
        
        if not links:
            new_nodes.append(old_node)
            continue
            
        for anchor_text, url in links:
            markdown_pattern = f"[{anchor_text}]({url})"
            sections = current_text.split(markdown_pattern, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes


def text_to_textnodes(text):
    # Start with a single raw plain text node
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Run it sequentially through each of your splitting functions
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes