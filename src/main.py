import os
import sys
import shutil
from block_markdown import markdown_to_html_node, extract_title

def copy_directory_recursive(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
        
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_directory_recursive(src_path, dst_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} with basepath: {basepath}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    
    # Replace content tokens
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    # Replace root paths to align with GitHub subdirectories
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_html_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def main():
    # 1. Capture basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # 2. Shift build output location from 'public' to 'docs'
    src_dir = "static"
    dst_dir = "docs" 
    content_dir = "content"
    template_file = "template.html"
    
    print("Cleaning up old deployment builds...")
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        
    print("Syncing static assets...")
    copy_directory_recursive(src_dir, dst_dir)
    
    print("Recursively compiling markdown content pages...")
    generate_pages_recursive(content_dir, template_file, dst_dir, basepath)
    print("Static site compilation complete!")

if __name__ == "__main__":
    main()