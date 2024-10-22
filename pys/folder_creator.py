import os
from shutil import copy as copyfile

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *

check("clrprint")  # Check for clrprint module
from clrprint import *


def folder_creator():
    try:
        showerror = int(input("Print process?\n0 = Don't show anything\n1 = Don't show errors\n2 = Show everything\n"))
    except ValueError:
        return

    if showerror != 0:
        # Seperator
        print("=" * 40, "\n")
    for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
        pack_json = load_json(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs/')[c]}")

        if showerror != 0:
            print(pack_json["topic"].lower())
        # Main Topic Directory
        try:
            # Makes the topic folder
            os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}')
            if showerror != 0:
                clrprint('+ Made directory', f'{pack_json["topic"].lower()}', clr='p,w')
        except FileExistsError:
            if showerror == 2:
                clrprint(f'- {pack_json["topic"].lower()}', 'already exists!', clr='w,r')
            else:
                pass

        for i in range(len(pack_json["packs"])):
            # Pack Name Directory
            if showerror != 0:
                clrprint(f'= |--> {pack_json["packs"][i]["pack_id"]}')
            try:
                # Makes the PackID Directory in Topic
                os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/')
                if showerror != 0:
                    clrprint('+ |----> Made folder', clr='m')
            except FileExistsError:
                if showerror == 2:
                    clrprint('- |----> Folder already exists!', clr='r')
                else:
                    pass

            # Pack Default Directory
            try:
                # Makes the default directory in PackID
                os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/default')
                if showerror != 0:
                    clrprint('+ |-------> Made folder', '`default`', clr='b,w')
            except FileExistsError:
                if showerror == 2:
                    clrprint('- |-------> Folder', '`default`', 'already exists!', clr='y,w,y')
                else:
                    pass

            # Pack Directory pack_icon.png
            try:
                if pack_json["packs"][i]["details"]["icon"] != "png":
                    pass
            except:
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
                    if showerror != 0:
                        clrprint('+ |----------> Made', '`pack_icon.png`', clr='g,w')
                elif showerror == 2:
                    # When length of pack_icon.png is larger than 0
                    clrprint('- |---------->', '`pack_icon.png`', 'has been modified!', clr='m,w,m')
            try:
                for comp in pack_json["packs"][i]["compatibility"]:
                    # Pack Name Compatibilities Directory
                    try:
                        # Creates compatability directory
                        os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/{comp}')
                        if showerror != 0:
                            clrprint('+ |-------> Made folder', f'`{comp}`', clr='b,w')
                    except FileExistsError:
                        if showerror == 2:
                            clrprint('- |-------> Folder', f'`{comp}`', 'already exists!', clr='y,w,y')
                        else:
                            pass
            except KeyError:
                pass # If there is no compatibility, it will just pass
        if showerror != 0:
            # Seperator
            print("\n", "=" * 40, "\n")


if __name__ == "__main__":
    folder_creator()
