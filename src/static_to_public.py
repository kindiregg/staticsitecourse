import os
import shutil

project_root = os.path.dirname(os.path.dirname(__file__))
static_dir = os.path.join(project_root, "static")
# static_contents = os.listdir(static_dir)

def collect_paths(base_path):
    file_list = []
    contents = os.listdir(base_path)
    
    for content in contents:
        content_path = os.path.join(base_path, content)

        if os.path.isdir(content_path):
            file_list.extend(collect_paths(content_path))
        else:
            file_list.append(content_path)
            public_path = content_path.replace("/static/", "/public/", 1)
            print(f"{content_path} -> {public_path}")

    return file_list

def copy_to_public(file_paths):
    for file_path in file_paths:
        public_path = file_path.replace("/static/", "/public/", 1)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        shutil.copy(file_path, public_path)

def copy_static_to_public():
    files = collect_paths(static_dir)
    copy_to_public(files)