import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
            
        parts = old_node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: matching closing delimiter '{delimiter}' not found")
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            image_alt, image_link = image
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown syntax: image section split failed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            link_text, link_url = link
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown syntax: link section split failed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    # 1. Split bold (** remains the standard for bold)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # 2. Split italic using asterisks
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    
    # 3. Split italic using underscores
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # 4. Split inline code (Fixed to point to TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # 5. Split markdown images into image text nodes
    nodes = split_nodes_image(nodes)
    
    # 6. Split markdown links into link text nodes
    nodes = split_nodes_link(nodes)
    
    return nodes