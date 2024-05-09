import os
from uuid import uuid4
from random import randint
from pathlib import Path
import shutil

if str(os.getcwd()).endswith("system32") or __name__ != "__main__":
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
from custom_functions import *

check("clrprint")  # Check for clrprint module
from clrprint import clrprint

check("PIL", "pillow")  # Check for Python Image Library
from PIL import Image


def merge(dict1: dict, dict2: dict):
    return dict1 | dict2


def lsdir(directory: str):
    folder_list = []

    # Traverse the directory structure recursively
    for dirpath, dirnames, filenames in os.walk(directory):
        # Normalize the directory path
        r_dirpath = os.path.relpath(dirpath, directory)
        # Convert backslashes to forward slashes for platform consistency
        r_dirpath = r_dirpath.replace(os.path.sep, "/")

        # Add a trailing slash if it's a directory
        if not r_dirpath.endswith("/"):
            r_dirpath += "/"

        folder_list.append(r_dirpath)

        # Add the relative paths of all files in the directory
        for filename in filenames:
            relative_filepath = os.path.relpath(os.path.join(dirpath, filename), directory)
            # Normalize the file path
            relative_filepath = relative_filepath.replace(os.path.sep, "/")
            folder_list.append(relative_filepath)

    return folder_list


def manifestgenerator():
    global mf
    mf = load_json(f"{cdir()}/jsons/others/manifest.json")
    # Pack Name
    mf["header"]["name"] = f"BTRP-{randint(0, 999999)}"
    with open(f"{cdir()}/jsons/others/selected_packs.json", "r") as selectedpacks:
        # Puts Selected Packs into Description
        # This part is just temporary, I have
        # not finished it yet, since the selection
        # process in incomplete
        sp = selectedpacks.read()
        sps = ""
        for i in sp:
            if i == '"':
                sps += "'"
            else:
                sps += i
        mf["header"]["description"] = sps
    mf["header"]["uuid"] = str(uuid4())
    mf["modules"][0]["uuid"] = str(uuid4())
    try:
        os.mkdir(f'{cdir()}/{mf["header"]["name"]}')
    except:
        pass
    # Dumps JSON with formatting
    dump_json(f'{cdir()}/{mf["header"]["name"]}/manifest.json', mf)

    with Image.open(f'{cdir()}/pack_icon.png') as img:
        # Adds a pack icon for good measure
        img.save(f'{cdir()}/{mf["header"]["name"]}/pack_icon.png')


def list_of_from_directories():
    selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")
    added_packs = []
    from_dir = []
    for category in selpacks:
        if category != "raw":
            # Pack JSON
            ctopic = load_json(f"{cdir()}/jsons/packs/{category.replace(' ', '_').lower()}.json")

            for index in range(len(selpacks[category]["packs"])):
                compatible = False
                # Removes compatible packs since they are accounted
                # for in compatiblity
                if ctopic["packs"][selpacks[category]["index"][index]]["pack_id"] in added_packs:
                    compatible = True

                if not compatible:
                    for k in ctopic["packs"][selpacks[category]["index"][index]]["compatibility"]:
                        try:
                            if k in selpacks["raw"]:
                                from_dir.append(
                                    f"{cdir()}/packs/{category.lower()}/{selpacks[category]['packs'][index]}/{k}")
                                added_packs.append(selpacks[category]['packs'][index])
                                added_packs.append(k)
                                compatible = True
                                break
                        except KeyError:
                            pass
                if not compatible:
                    from_dir.append(f"{cdir()}/packs/{category.lower()}/{selpacks[category]['packs'][index]}/default")
                    added_packs.append(selpacks[category]['packs'][index])
    return from_dir


def main_copyfile(from_dir):
    print(from_dir.split("/")[-2])
    from_list_dir = lsdir(from_dir)
    to_dir = f"{cdir()}/{mf["header"]["name"]}"
    to_list_dir = lsdir(to_dir)
    for i in from_list_dir:
        if i == "./":
            pass
        elif i.endswith("/"):
            try:
                os.mkdir(f'{to_dir}/{i}')
            except FileExistsError:
                pass
        else:
            if i in to_list_dir:
                if i.endswith(".json"):
                    to_json = load_json(f'{to_dir}/{i}')
                    from_json = load_json(f'{from_dir}/{i}')
                    to_json = to_json | from_json
                    dump_json(f'{to_dir}/{i}', to_json)
                elif i.endswith(".lang"):
                    with open(f'{from_dir}/{i}','r') as from_lang_file:
                        from_lang = from_lang_file.read()
                    with open(f'{to_dir}/{i}','a') as to_lang_file:
                        to_lang_file.write(f'\n{from_lang}')
                else:
                    raise FileExistsError(
                        f'{from_dir}/{i} cannot be copied to {to_dir}/{i} as it is cannot be merged')
            else:
                shutil.copy(f'{from_dir}/{i}',f'{to_dir}/{i}')


def extractor():
    manifestgenerator()
    from_dir = list_of_from_directories()
    for i in from_dir:
        main_copyfile(i)
    shutil.copy(f"{cdir()}/jsons/others/selected_packs.json",f"{cdir()}/{mf["header"]["name"]}")
    clrinput("Press Enter to exit.", clr="green")


if __name__ == "__main__":
    extractor()
