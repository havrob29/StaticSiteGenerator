import os, shutil
from copydir import copy_dir_to_another_dir
from generatepage import generate_page_recursive
path_to_static = "./static"
path_to_public = "./public"


def main():
    print("removing public folder..")
    if os.path.exists(path_to_public):
            shutil.rmtree(path_to_public)
    
    copy_dir_to_another_dir(path_to_static, path_to_public)

    generate_page_recursive("./content", "template.html", "./public")

main()