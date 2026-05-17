# block\_markdown.py
from enum import Enum
from html import escape
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    if markdown is None:
        return []
    
    lines = markdown.splitlines()
    blocks = []
    current_block_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        
        # Handle blank lines
        if stripped == "":
            if in_code_block:
                current_block_lines.append(line)
            elif current_block_lines:
                blocks.append("\n".join(current_block_lines).strip("\n"))
                current_block_lines = []
            continue

        # Check for entering/exiting a code block fence
        if stripped.startswith("```"):
            if not in_code_block:
                # If we were building another block, save it first
                if current_block_lines:
                    blocks.append("\n".join(current_block_lines).strip("\n"))
                    current_block_lines = []
                in_code_block = True
                current_block_lines.append(line)
            else:
                in_code_block = False
                current_block_lines.append(line)
                blocks.append("\n".join(current_block_lines).strip("\n"))
                current_block_lines = []
            continue

        if in_code_block:
            current_block_lines.append(line)
            continue

        # ---- STRUCTURAL BREAK DETECTION ----
        # If we aren't in a code block, check if this line signals a change in structure
        is_heading = stripped.startswith("#")
        is_list_item = stripped.startswith("- ") or stripped.startswith("+ ") or stripped.startswith("* ")
        import re
        is_ordered_item = bool(re.match(r'^\d+\.\s+', stripped))
        is_quote = stripped.startswith(">")

        if current_block_lines:
            prev_line = current_block_lines[-1].strip()
            was_list_item = prev_line.startswith("- ") or prev_line.startswith("+ ") or prev_line.startswith("* ")
            was_ordered_item = bool(re.match(r'^\d+\.\s+', prev_line))
            was_quote = prev_line.startswith(">")
            was_heading = prev_line.startswith("#")

            # If a structural change occurs between back-to-back rows, split immediately
            if (is_heading or 
                (is_list_item and not was_list_item) or 
                (not is_list_item and was_list_item) or
                (is_ordered_item and not was_ordered_item) or
                (not is_ordered_item and was_ordered_item) or
                (is_quote and not was_quote) or
                (not is_quote and was_quote)):
                
                blocks.append("\n".join(current_block_lines).strip("\n"))
                current_block_lines = []

        current_block_lines.append(line)

    # Clean up any leftover active tracks
    if current_block_lines:
        blocks.append("\n".join(current_block_lines).strip("\n"))

    return [b for b in blocks if b.strip() != ""]

def block_to_block_type(block):
    if block is None:
        return BlockType.PARAGRAPH
    s = block.strip()
    lines = block.splitlines()
    # 1. Code block (fenced)
    if s.startswith("```"):
        return BlockType.CODE
    # 2. Heading
    if s.startswith("#"):
        import re
        m = re.match(r'^(#{1,6})\s+', s)
        if m:
            return BlockType.HEADING
    # 3. Quote: every non-empty line starts with '>'
    nonempty = [l for l in lines if l.strip() != ""]
    if nonempty and all(l.lstrip().startswith(">") for l in nonempty):
        return BlockType.QUOTE
    # 4. Unordered list: consistent marker (-, +, or *) on every non-empty line
    import re
    m = re.match(r'^\s*([\-+\*])\s+(.+)$', nonempty[0]) if nonempty else None
    if m:
        marker = m.group(1)
        ok = True
        for l in nonempty:
            mm = re.match(r'^\s*([\-+\*])\s+(.+)$', l)
            if not mm or mm.group(1) != marker:
                ok = False
                break
        if ok:
            return BlockType.UNORDERED_LIST
    # 5. Ordered list: require first item to start with "1." and subsequent lines match \d+.
    if nonempty:
        m = re.match(r'^\s*(\d+)\.\s+(.+)$', nonempty[0])
        if m:
            first_num = int(m.group(1))
            if first_num != 1:
                return BlockType.PARAGRAPH
            ok = True
            for l in nonempty:
                mm = re.match(r'^\s*(\d+)\.\s+(.+)$', l)
                if not mm:
                    ok = False
                    break
            if ok:
                return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# adapter to reuse your inline_markdown.text_to_textnodes -> returns TextNode objects
def _text_to_children_from_text(text):
    # text_to_textnodes returns TextNode-like objects (from your inline_markdown).
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for tn in text_nodes:
        html_nodes.append(text_node_to_html_node(tn))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        btype = block_to_block_type(block)
        if btype == BlockType.PARAGRAPH:
            children.append(_paragraph_to_node(block))
        elif btype == BlockType.HEADING:
            children.append(_heading_to_node(block))
        elif btype == BlockType.CODE:
            children.append(_code_to_node(block))
        elif btype == BlockType.QUOTE:
            children.append(_quote_to_node(block))
        elif btype == BlockType.UNORDERED_LIST:
            children.append(_unordered_to_node(block))
        elif btype == BlockType.ORDERED_LIST:
            children.append(_ordered_to_node(block))
    return ParentNode("div", children)

def _paragraph_to_node(block):
    lines = block.split("\n")
    paragraph_text = " ".join([line.strip() for line in lines if line.strip() != ""])
    return ParentNode("p", _text_to_children_from_text(paragraph_text))

def _heading_to_node(block):
    # first non-empty line determines heading level
    first = next((l for l in block.split("\n") if l.strip() != ""), "")
    level = 0
    for ch in first:
        if ch == "#":
            level += 1
        else:
            break
    text = first[level:].lstrip()
    return ParentNode(f"h{max(1, min(level,6))}", _text_to_children_from_text(text))

def _code_to_node(block):
    lines = block.split("\n")
    # remove leading fence and trailing fence if present
    start = 1 if lines and lines[0].strip().startswith("```") else 0
    end = len(lines)
    if len(lines) >= 2 and lines[-1].strip().startswith("```"):
        end = len(lines) - 1
    code_lines = lines[start:end]
    code_text = "\n".join(code_lines)
    # ensure a trailing newline inside <code> as tests expect
    code_text += "\n"
    # create a raw text node (no inline parsing): use your TextNode/TextType
    raw_node = TextNode(code_text, TextType.TEXT)
    code_html = text_node_to_html_node(raw_node)
    return ParentNode("pre", [ParentNode("code", [code_html])])

def _quote_to_node(block):
    lines = block.split("\n")
    cleaned = []
    for l in lines:
        if l.strip() == "":
            continue
        s = l.lstrip()
        if s.startswith("> "):
            cleaned.append(s[2:])
        elif s.startswith(">"):
            cleaned.append(s[1:].lstrip())
        else:
            cleaned.append(s)
    quote_text = " ".join(cleaned)
    return ParentNode("blockquote", _text_to_children_from_text(quote_text))

def _unordered_to_node(block):
    lines = [l for l in block.split("\n") if l.strip() != ""]
    items = []
    for l in lines:
        import re
        m = re.match(r'^\s*([\-+\*])\s+(.+)$', l)
        if m:
            items.append(ParentNode("li", _text_to_children_from_text(m.group(2).strip())))
    return ParentNode("ul", items)

def _ordered_to_node(block):
    lines = [l for l in block.split("\n") if l.strip() != ""]
    items = []
    for l in lines:
        import re
        m = re.match(r'^\s*(\d+)\.\s+(.+)$', l)
        if m:
            items.append(ParentNode("li", _text_to_children_from_text(m.group(2).strip())))
    return ParentNode("ol", items)
