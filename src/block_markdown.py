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
    # 1. Heading Validation (1-6 '#' followed strictly by a space)
    if block.startswith("#"):
        lines = block.split("\n")
        if len(lines) == 1:  # Headings must be a single line
            for i in range(1, 7):
                if block.startswith("#" * i + " "):
                    return BlockType.HEADING

    # 2. Code Block Validation (Must start and end with triple backticks)
    if block.startswith("```") and block.endswith("```"):
        if len(block) >= 6:  # Minimum valid empty code block structure
            return BlockType.CODE

    # 3. Blockquote Validation (Every line must start with '>')
    lines = block.split("\n")
    if block.startswith(">"):
        all_quoted = True
        for line in lines:
            if not line.startswith(">"):
                all_quoted = False
                break
        if all_quoted:
            return BlockType.QUOTE

    # 4. Unordered List Validation (Every line must start with '- ' or '* ')
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