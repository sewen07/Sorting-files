import os 
import json
import shutil
import sys

PATTERN = "essay" #write here what files do you want to sort (it will elliminate it from the file name aswell)

def find_myfiles_paths(source):
    myfiles = []
    
    for root, dirs, files in os.walk(source):
        for file in files:
            if PATTERN in file.lower():
                path = os.path.join(source, file)
                myfiles.append(path)
        break

    return myfiles

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, dest):
    shutil.copyfile(source, dest)

def make_json_metadata_file(path, files):
    data = {
        "FileNames":files,
        "NumberOfFiles":len(files)
    }
    with open(path, "w") as f:
        json.dump(data, f)

def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    myfiles = find_myfiles_paths(source_path)
    new_files = get_name_from_paths(myfiles, "essay")

    create_dir(target_path)

    for src, dest in zip(myfiles, new_files):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)

        
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_files)
  
    print("Everything is done.")
if __name__ == "__main__":
    args = sys.argv
    if (len(args)) != 3:
        raise Exception("You have to write a source and a target directory.")
    
    source, target = args[1:]
    main(source, target)


