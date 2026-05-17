import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Reads a markdown file, converts it to HTML, extracts the title,
    injects it into an HTML template, and writes the output to a destination file.
    Swaps out absolute root paths with a configurable basepath.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    page_title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", page_title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # REPLACEMENT LOGIC FOR GITHUB PAGES SUBDIRECTORIES
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Crawls every entry in the content directory recursively, passing down
    the basepath configuration to the single page builder.
    """
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(from_path):
            if entry.endswith(".md"):
                html_filename = entry[:-3] + ".html"
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                # Pass basepath down
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            next_dest_dir = os.path.join(dest_dir_path, entry)
            # Pass basepath into the nested recursive frames
            generate_pages_recursive(from_path, template_path, next_dest_dir, basepath)