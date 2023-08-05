"""PQI
Usage:
  pqi add <name>
  pqi (-h | --help)
  pqi (-v | --version)
Options:
  -h --help        Show this screen.
  -v --version     Show version.
"""
import json
import shutil

"""
     _ __      _,.---._      .=-.-.
  .-`." ,`.  ,-." - ,  `.   /==/_ /
 /==/, -   \/==/ ,    -  \ |==|, |
|==| _ .=. |==| - .=.  ,  ||==|  |
|==| , "=",|==|  : ;=:  - ||==|- |
|==|-  ".."|==|,  "="  ,  ||==| ,|
|==|,  |    \==\ _   -    ;|==|- |
/==/ - |     ".=".  ,  ; -\/==/. /
`--`---"       `--`--"" `--`--`-`
                ---- A Terminal Tools For Python
"""

import os
import re
import sys
import pickle
import platform
from docopt import docopt

APP_DESC = """
         TPL ---- PyQt5 template
         @author qq 625781186  (https://github.com/625781186/pygui_cli) 
"""

FILE_NAME = "~\\pip\\tpl.json" if ("Windows" in platform.system()) else "~/.pip/tpl.json"
FILE_PATH = os.path.expanduser(FILE_NAME)
dir_path = os.path.dirname(FILE_PATH)
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
if not os.path.exists(FILE_PATH):
    source_path = None
    print("Sorry, can't find {} , please install tpl".format(FILE_PATH))
else:
    with open(FILE_PATH, "r") as f:
        raw_data = f.read()

        data = json.loads(raw_data, encoding='utf-8')
        source_path = data["source_path"]
print("read template :%s" % source_path)

# FILE_NAME = "~\\pip\\pip.ini" if ("Windows" in platform.system()) else "~/.pip/pip.conf"
# FILE_PATH = os.path.expanduser(FILE_NAME)
# dir_path = os.path.dirname(FILE_PATH)
# if not os.path.exists(dir_path):
#     os.mkdir(dir_path)
# SOURCES_NAME = os.path.join(dir_path, "sources.dict")
# SOURCES = dict()

# if not os.path.exists(SOURCES_NAME):
#     with open(SOURCES_NAME, "wb") as fp:
#         pickle.dump({
#             "pypi": "https://pypi.python.org/simple/",
#             "tuna": "https://pypi.tuna.tsinghua.edu.cn/simple",
#             "douban": "https://pypi.doubanio.com/simple/",
#             "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
#             "ustc": "https://mirrors.ustc.edu.cn/pypi/web/simple"
#         }, fp)
# with open(SOURCES_NAME, "rb") as fp:
#     SOURCES = pickle.load(fp)

# def list_all_source():
#     print('\n')
#     for key in SOURCES.keys():
#         print(key, '\t', SOURCES[key])
#     print('\n')
#
# def write_file(source_name):
#     with open(FILE_PATH, 'w') as fp:
#         str_ = "[global]\nindex-url = {0}\n[install]\ntrusted-host = {1}".format(
#             SOURCES[source_name], SOURCES[source_name].split('/')[2])
#         fp.write(str_)
#
# def select_source_name(source_name):
#     if source_name not in SOURCES.keys():
#         print("\n{} is not in the Source list.\n".format(source_name))
#     else:
#         write_file(source_name)
#         print("\nSource is changed to {}({}).\n".format(source_name, SOURCES[source_name]))
#
# def show_current_source():
#     if not os.path.exists(FILE_PATH):
#         print("\nCurrent source is pypi.\n")
#         return
#     config = configparser.ConfigParser()
#     config.read(FILE_PATH)
#     index_url = config.get("global", "index-url")
#     for key in SOURCES.keys():
#         if index_url == SOURCES[key]:
#             print("\nCurrent source is {}({}).\n".format(key, index_url))
#             break
#     else:
#          print("\nCurrent source is {}.\n".format(index_url))
#
# def check_url(url):
#     p = re.compile("^https?://.+?/simple/?$")
#     if p.match(url) == None:
#         return False
#     return True
#
# def add_source(source_name, source_url):
#     if not check_url(source_url):
#         print("\nURL({}) does not conform to the rules.\n".format(source_url))
#         return
#     SOURCES[source_name] = source_url
#     with open(SOURCES_NAME, "wb") as fp:
#         pickle.dump(SOURCES, fp)
#     print("\n{}({}) is add to Source list.\n".format(source_name, source_url))

# def remove_source(source_name):
#     if source_name not in SOURCES.keys():
#         print("\n{} is not in the Source list.\n".format(source_name))
#     else:
#         source_url = SOURCES.pop(source_name)
#         with open(SOURCES_NAME, "wb") as fp:
#             pickle.dump(SOURCES, fp)
#         print("\n{}({}) is remove to Source list.\n".format(source_name, source_url))

FILE_NAME = "~\\pip\\tpl.json" if ("Windows" in platform.system()) else "~/.pip/tpl.json"
FILE_PATH = os.path.expanduser(FILE_NAME)
dir_path = os.path.dirname(FILE_PATH)
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
if not os.path.exists(FILE_PATH):
    print("Sorry, can't find {} , please install tpl".format(FILE_PATH))

else:
    with open(FILE_PATH, "r") as f:
        raw_data = f.read()

        data = json.loads(raw_data, encoding='utf-8')
        source_path = data["source_path"]


def copy_folder(to_folder: str):
    print(to_folder)
    if to_folder == ".":
        print(sys.argv)
    if os.path.exists(source_path):
        if os.path.exists(to_folder):
            print(to_folder)
            to_folder = os.path.abspath(".")
            shutil.copytree(source_path, to_folder)
        else:
            print("%s is not exists, please create it" % to_folder)
            sys.exit(0)
    else:
        print("%s is not exists, please install tpl" % source_path)
        sys.exit(0)


def main():
    arguments = docopt(__doc__, version="0.0.1")

    if arguments["add"]:
        print(arguments["<name>"])
        copy_folder(arguments["<name>"])
    else:
        print("input error!")


if __name__ == "__main__":
    print(APP_DESC)
    main()
