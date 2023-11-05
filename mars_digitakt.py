import sys
import os
import re
import zipfile

def argsParse(args):
    if len(args) == 1:
        print("enter path to folder")
        sys.exit()
    print(args[1])
    return args[1]

def is_wav(filename):
    f = filename.split(".")
    if f[-1].lower() == "wav":
        return True
    return False

def is_c_or_non_pitched(filename):
    f = filename.split(" ")[-1].split(".")[0]
    pitched = re.search("[ABCDEFGabcdefg]#?-?[0-9]", f)
    if "c" in f.lower() and "#" not in f.lower():
        return True
    if not pitched:
        return True
    return False

    
def get_path_list(path):
    to_zip = []
    res = os.walk(path)
    for root, dirs, files in res:
        if len(files) > 0:
            for i in files:
                if is_wav(i) and is_c_or_non_pitched(i):

                    to_zip.append(os.path.join(root, i))
    return to_zip

def create_zip(files, trim):
    with zipfile.ZipFile(f"{sys.argv[1].split('/')[-1]}.zip", 'w') as zipped:
        for f in files:
            zipped.write(f, arcname=(f"{f.replace(trim, '')}"),compress_type=zipfile.ZIP_DEFLATED)

path = argsParse(sys.argv)
if os.path.isdir(path):
    res = get_path_list(path)
    create_zip(res,path)
else:
    print("not a directory")
    sys.exit()