import os
from blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line
    raise Exception("no h1 header in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if os.path.isfile(from_path):
        markdownfile = open(from_path, "r")
        markdown = markdownfile.read()
        markdownfile.close()
    else:
        raise Exception(f"{from_path} is not a valid file to read")
    
    if os.path.isfile(template_path):
        templatefile = open(template_path, "r")
        template = templatefile.read()
        templatefile.close()
    else:
        raise Exception(f"{template_path} is not a valid file to read")
    
    html = markdown_to_html_node(markdown)
    html = html.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    if os.path.exists(os.path.dirname(dest_path)) == False:
        os.makedirs(os.path.dirname(dest_path))
    
    f = open(dest_path, "w")
    f.write(template)
    f.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.exists(dest_dir_path):
        print(f"making folder {dest_dir_path}")
        os.mkdir(dest_dir_path)

    dir_items = os.listdir(dir_path_content)
    for item in dir_items:
        itempath = os.path.join(dir_path_content, item)
        destpath = os.path.join(dest_dir_path, item)
        if os.path.isfile(itempath) and item.endswith(".md"):
            generate_page(itempath, template_path, destpath[:-3] + ".html")
        if os.path.isdir(itempath):
            generate_page_recursive(itempath, template_path, destpath)

