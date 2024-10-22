import os
from shutil import copy as copyfile

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *

def folder_creator():
    for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
        pack_json = load_json(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs/')[c]}")
        # Main Topic Directory
        try:
            # Makes the topic folder
            os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}')
        except FileExistsError:
            pass

        for i in range(len(pack_json["packs"])):
            # Pack Name Directory
            try:
                # Makes the PackID Directory in Topic
                os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/')
            except FileExistsError:
                pass

            # Pack Default Directory
            try:
                # Makes the default directory in PackID
                os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/default')
            except FileExistsError:
                pass

            # Pack Directory pack_icon.png
            try:
                if pack_json["packs"][i]["icon"] != "png":
                    pass
                else:
                    raise KeyError
            except KeyError:
                with open(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png','a') as _:
                    # The main purpose of doing this is to
                    # 1. Create a pack_icon.png as  \packs\topic\packid\
                    # 2. Make no changes to \packs\topic\packid\pack_icon.png if it is already made/modified
                    pass
                if os.path.getsize(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png') == 0:
                    # Basically checks whether pack_icon.png is empty, and
                    # if so, it copies the pack_icon.png to \packs\topic\packid
                    copyfile(f'{cdir()}/pack_icons/missing_texture.png',
                             f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png')
            try:
                for comp in pack_json["packs"][i]["compatibility"]:
                    # Pack Name Compatibilities Directory
                    try:
                        # Creates compatability directory
                        os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/{comp}')
                    except FileExistsError:pass
            except KeyError:
                pass # If there is no compatibility, it will just pass


if __name__ == "__main__":
    folder_creator()
