from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # If the node is already formatted, don't attempt to split it—pass it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # If the delimiter isn't present, no splitting is required
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
            
        # Split the string by the delimiter
        parts = old_node.text.split(delimiter)
        
        # A valid matching pair of delimiters always produces an odd number of parts
        # e.g., "text *bold* text" splits on "*" into ["text ", "bold", " text"] (3 parts)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: matching closing delimiter '{delimiter}' not found")
            
        for i in range(len(parts)):
            # If the string part is empty (e.g. text starts exactly with the delimiter), skip it
            if parts[i] == "":
                continue
            # Even indices are outside the delimiters (raw text)
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            # Odd indices are inside the delimiters (formatted text)
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes
