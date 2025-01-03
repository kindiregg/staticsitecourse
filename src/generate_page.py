from block_markdown import markdown_to_html_node, extract_title
import os

template_path = "./template.html"
from_path = "./content/index.md"
dest_path = "./public/index.html"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_contents = markdown_file.read()
    markdown_file.close()

    page_title = extract_title(markdown_contents)
    html_nodes = markdown_to_html_node(markdown_contents)
    html_string = html_nodes.to_html()

    template_file = open(template_path)
    template_contents = template_file.read()
    template_file.close()
    
    page_contents = template_contents.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    output_file = open(dest_path, "w")
    output_file.write(page_contents)
    output_file.close()
    print(f"PAGE CONTENTS: {page_contents}")

if __name__ == "__main__":
    generate_page(from_path, template_path, dest_path)