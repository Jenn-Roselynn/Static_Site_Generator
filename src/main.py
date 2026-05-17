import os
import shutil
import sys  # Added to read arguments
from generate_page import generate_pages_recursive

def clear_and_copy_static(src, dst):
    if os.path.exists(dst):
        print(f"Cleaning target directory: {dst}...")
        shutil.rmtree(dst)
        
    print(f"Creating target directory: {dst}...")
    os.mkdir(dst)
    
    copy_recursive(src, dst)

def copy_recursive(src, dst):
    if not os.path.exists(src):
        raise ValueError(f"Source directory does not exist: {src}")

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)

def main():
    # 1. Grab command line argument for basepath if provided, else default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    source_dir = "./static"
    # 2. Update output target from "./public" to "./docs"
    dest_dir = "./docs"
    
    print(f"Starting static site generation with basepath: '{basepath}'...")
    clear_and_copy_static(source_dir, dest_dir)
    
    # 3. Pass the basepath variable to the recursive generator
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path=dest_dir,
        basepath=basepath
    )
    
    print("Static site generation complete.")

if __name__ == "__main__":
    main()