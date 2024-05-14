import os
from uuid import uuid4
from random import randint
import shutil

if str(os.getcwd()).endswith("system32") or __name__ != "__main__":
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
from custom_functions import *

check("PIL", "pillow")  # Check for Python Image Library
from PIL import Image
from selector import val_command



def lsdir(directory: str):
    folder_list = []

    # Go through the directory structure
    for dirpath, dirnames, filenames in os.walk(directory):
        # Normalize the directory path
        r_dirpath = os.path.relpath(dirpath, directory)
        # Convert backslashes to forward slashes for non-Windows
        r_dirpath = r_dirpath.replace(os.path.sep, "/")

        # Add a trailing slash if it's a directory
        if not r_dirpath.endswith("/"):
            r_dirpath += "/"

        folder_list.append(r_dirpath)

        # Add the relative paths of all files in the directory
        for filename in filenames:
            relative_filepath = os.path.relpath(os.path.join(dirpath, filename), directory)
            # Convert backslashes to forward slashes for non-Windows
            relative_filepath = relative_filepath.replace(os.path.sep, "/")
            folder_list.append(relative_filepath)

    return folder_list


def manifestgenerator():
    global mf
    mf = load_json(f"{cdir()}/jsons/others/manifest.json")
    # Pack Name
    pk_name = input("Enter your pack name\nLeave empty for a template name\n")
    if pk_name == "":
        mf["header"]["name"] = f"BTRP-{randint(0, 999999)}"
    else:
        mf["header"]["name"] = pk_name
    selected_packs = load_json(f"{cdir()}/jsons/others/selected_packs.json")
    description = ""
    for i in selected_packs:
        if i != "raw":
            description += f"\n{i}"
            for p in selected_packs[i]["packs"]:
                description += f'\n\t{p}'
    mf["header"]["description"] = description[1:]
    mf["header"]["uuid"] = str(uuid4())
    mf["modules"][0]["uuid"] = str(uuid4())
    try:
        os.mkdir(f'{cdir()}/{mf["header"]["name"]}')
    except FileExistsError:
        pass
    # Dumps JSON with formatting
    dump_json(f'{cdir()}/{mf["header"]["name"]}/manifest.json', mf)
    # It is not supposed to be the template,
    # but there isn't any icons for the pack
    # so this is temprary
    with Image.open(f'{cdir()}/pack_icons/template.png') as img:
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
                # Honestly can't be bothered to comment this hunk
                # it just works lol
                if not compatible:
                    for k in ctopic["packs"][selpacks[category]["index"][index]]["compatibility"]:
                        try:
                            if k in selpacks["raw"]:
                                from_dir.append(f"{cdir()}/packs/{category.lower()}/{selpacks[category]['packs'][index]}/{k}")
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
    from_list_dir = lsdir(from_dir)
    to_dir = f"{cdir()}/{mf['header']['name']}"
    to_list_dir = lsdir(to_dir)
    for i in from_list_dir:
        print(
            f'\r{from_dir.split("/")[-2]} {from_list_dir.index(i) + 1}/{len(from_list_dir)}{" " * (shutil.get_terminal_size().columns - len(from_dir.split("/")[-2]) - len(str(from_list_dir.index(i) + 1)) - len(str(len(from_list_dir))) - 2)}',
            end="")
        if i == "./":
            # Root directory
            pass
        elif i.endswith("/"):
            # Folder
            try:
                os.mkdir(f'{to_dir}/{i}')
            except FileExistsError:
                pass
        else:
            # File
            if i in to_list_dir:
                # If the file already exists, it attempts to merge
                if i.endswith(".json"):
                    # Merges the dictionaries
                    to_json = load_json(f'{to_dir}/{i}')
                    from_json = load_json(f'{from_dir}/{i}')
                    to_json = to_json | from_json
                    dump_json(f'{to_dir}/{i}', to_json)
                elif i.endswith(".lang"):
                    # Merges lang files
                    with open(f'{from_dir}/{i}', 'r') as from_lang_file:
                        from_lang = from_lang_file.read()
                    with open(f'{to_dir}/{i}', 'a') as to_lang_file:
                        to_lang_file.write(f'\n{from_lang}')
                else:
                    # Shouldn't happen, but it is just here
                    # For PNGs, TGAs and non-text files
                    raise FileExistsError(f'{from_dir}/{i} cannot be copied to {to_dir}/{i} as it is cannot be merged')
            else:
                # Copies over the file since it doesn't exist
                shutil.copy(f'{from_dir}/{i}', f'{to_dir}/{i}')


def export():
    manifestgenerator()
    from_dir = list_of_from_directories()
    clrprint(f"Exporting at {cdir()}{os.path.sep}{mf['header']['name']}...", clr="y")
    for i in from_dir:
        main_copyfile(i)
    # Keeps selected packs for easy changes
    print(f"\rselected_packs.json 1/1{' ' * (shutil.get_terminal_size().columns - 23)}",end="")
    shutil.copy(f"{cdir()}/jsons/others/selected_packs.json", f"{cdir()}/{mf['header']['name']}")
    # Makes mcpack
    print(f"\r{mf['header']['name']}.zip 1/2{' ' * (shutil.get_terminal_size().columns - len(mf['header']['name']) - 9)}",end="")
    shutil.make_archive(f"{cdir()}/{mf['header']['name']}", 'zip', f"{cdir()}/{mf['header']['name']}")

    print(f"\r{mf['header']['name']}.mcpack 2/2{' ' * (shutil.get_terminal_size().columns - len(mf['header']['name']) - 12)}",end="")
    shutil.move(f"{cdir()}/{mf['header']['name']}.zip", f"{cdir()}/{mf['header']['name']}.mcpack")
    # Remove folder
    shutil.rmtree(f"{cdir()}/{mf['header']['name']}")
    clrprint(f"\rFinished exporting the pack!{' ' * (shutil.get_terminal_size().columns - 29)}", clr="g")
    clrprint("It is now available at",f"{os.path.sep}{mf['header']['name']}.mcpack",clr="d,g")
    if clrinput("Clear Selected Packs? [y/n]", clr="y") == "y":
        val_command("selected_packs", "clear selected packs")
    clrinput("Press Enter to exit.", clr="g")


if __name__ == "__main__":
    export()
