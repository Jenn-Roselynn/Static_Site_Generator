def extract_title(markdown):
    """
    Scans a markdown string line by line to locate the primary H1 header.
    Returns the inner text context with leading/trailing whitespaces stripped.
    Raises a ValueError if no explicit H1 row exists.
    """
    for line in markdown.splitlines():
        # Clean trailing or leading structural alignment gaps
        stripped = line.strip()
        if stripped.startswith("# "):
            # Slice off the token identifier and return the raw headline text
            return stripped[2:].strip()
        elif stripped == "#":
            # Corner case: An empty H1 header tag sequence
            return ""
            
    raise ValueError("Invalid Markdown: Document lacks an explicit H1 target header line.")
