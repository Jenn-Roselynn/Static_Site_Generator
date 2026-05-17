from enum import Enum

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
        cleaned_block = block.strip()
        if cleaned_block != "":
            filtered_blocks.append(cleaned_block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    # 1. Heading Validation (1-6 '#' followed strictly by a space)
    if block.startswith("#"):
        for i in range(1, 7):
            if block.startswith("#" * i + " "):
                return BlockType.HEADING

    # 2. Code Block Validation (Must start with ```\n and end with ```)
    if block.startswith("```") and block.endswith("```"):
        # Explicit check for the markdown block specification constraint
        if len(lines) > 1 and lines[0].startswith("```"):
            return BlockType.CODE

    # 3. Blockquote Validation (Every line must start with '>')
    if block.startswith(">"):
        all_quoted = True
        for line in lines:
            if not line.startswith(">"):
                all_quoted = False
                break
        if all_quoted:
            return BlockType.QUOTE

    # 4. Unordered List Validation (Every line must start strictly with '- ' or '* ')
    if block.startswith("- ") or block.startswith("* "):
        all_unordered = True
        delim = "- " if block.startswith("- ") else "* "
        for line in lines:
            if not line.startswith(delim):
                all_unordered = False
                break
        if all_unordered:
            return BlockType.UNORDERED_LIST

    # 5. Ordered List Validation (Every line must be sequential starting at 1. )
    if block.startswith("1. "):
        all_ordered = True
        expected_number = 1
        for line in lines:
            prefix = f"{expected_number}. "
            if not line.startswith(prefix):
                all_ordered = False
                break
            expected_number += 1
        if all_ordered:
            return BlockType.ORDERED_LIST

    # 6. Fallback Default
    return BlockType.PARAGRAPH
