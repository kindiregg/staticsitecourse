from textnode import TextNode, TextType
import os
import shutil
from static_to_public import copy_static_to_public
from generate_page import generate_page

template_path = "./template.html"
from_path = "./content/index.md"
dest_path = "./public/index.html"

def main():
    if os.path.exists("./public"):
        print("Deleting public directory...")
        shutil.rmtree("./public")

    print("Copying static files to public directory...")
    copy_static_to_public()

    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()