import os, shutil

def copy_dir_to_another_dir(frompath = "", topath = ""):
    if not os.path.exists(topath):
         print(f"making folder{topath}")
         os.mkdir(topath)
    items_in_frompath = os.listdir(frompath)
    for item in items_in_frompath:
        itempath = os.path.join(frompath, item)
        copypath = os.path.join(topath, item)
        if os.path.isfile(itempath):
            shutil.copy(itempath, copypath)
        if os.path.isdir(itempath):
            copy_dir_to_another_dir(itempath, copypath)