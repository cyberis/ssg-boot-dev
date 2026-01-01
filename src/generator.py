import os
from pathlib import Path
from shutil import copy2
from blocknodes import markdown_to_html_node
from htmlnode import ParentNode, LeafNode

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    
    from_path = Path(from_path)
    dest_path = Path(dest_path)
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    dest_dir_path = dest_path.parent
    if not dest_dir_path.exists():
        os.makedirs(dest_dir_path, exist_ok=True)
    
    html_content = (template.replace("{{ Title }}", title)
                    .replace("{{ Content }}", content.to_html())
                    .replace("href=\"/", f"href=\"{basepath}")
                    .replace("src=\"/", f"src=\"{basepath}"))
    
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
def generate_pages_recursively(basepath, dir_path_content, template_path, dest_dir):
    dir_path_content = Path(dir_path_content)
    dest_dir = Path(dest_dir)
    
    for root, dirs, files in os.walk(dir_path_content):
        relative_root = Path(root).relative_to(dir_path_content)
        target_root = dest_dir / relative_root
        
        for file in files:
            if file.endswith('.md'):
                from_path = Path(root) / file
                dest_file_name = file[:-3] + '.html'
                dest_path = target_root / dest_file_name
                
                generate_page(basepath, from_path, template_path, dest_path)