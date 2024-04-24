from custom_functions import *
from json import *
import os
check("clrprint") #Check for clrprint module
check("shutil") #Check for shtil module (not sure if it is pre-installed, so just in case)
from clrprint import *
from shutil import copy as copyfile

showerror = int(input("Print process?\n0 = Don't show anything\n1 = Don't show errors\n2 = Show everything\n"))
if showerror != 0:
    print("="*40, "\n")
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs/')[c]}","r") as js:
        try:
            pack_json = loads(js.read())
        except JSONDecodeError:
            raise SyntaxError(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs/')[c]} has a skill issue.\nPerhaps you are missing a comma?")
    if showerror != 0:
        print(pack_json["topic"].lower())
    # Main Topic Directory
    try:
        os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}')
        if showerror != 0:
            clrprint('Made directory',f'{pack_json["topic"].lower()}',clr='p,w')
    except FileExistsError:
        if showerror == 2:
            clrprint(f'{pack_json["topic"].lower()}','already exists!',clr='w,r')
        else:
            pass

    for i in range(len(pack_json["packs"])):
        # Pack Name Directory
        if showerror != 0:
            clrprint(f'|--> {pack_json["packs"][i]["pack_id"]}')
        try:
            os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/')
            if showerror != 0:
                clrprint('|----> Made folder',clr='m')
        except FileExistsError:
            if showerror == 2:
                clrprint('|----> Folder already exists!',clr='r')
            else:
                pass

        # Pack Default Directory
        try:
            os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/default')
            if showerror != 0:
                clrprint(f'|-------> Made folder','`default`',clr='b,w')
        except FileExistsError:
            if showerror == 2:
                clrprint(f'|-------> Folder','`default`','already exists!',clr='y,w,y')
            else:
                pass

        # Pack Directory pack_icon.png
        r =  open(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png','a')
        r.close()        
        if len(os.listdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}')) == 2 and os.path.getsize(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png') == 0:
            copyfile(f'{cdir()}/pack_icon.png',f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png')
            if showerror != 0:
                clrprint('|----------> Made','`pack_icon.png`',clr='g,w')
        elif os.path.getsize(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/pack_icon.png') != 0 and showerror == 2:
            clrprint('|---------->','`pack_icon.png`','has been modified!',clr='m,w,m')
        
        for c in pack_json["packs"][i]["compatability"]:
            # Pack Name Compatabilities Directory
            try:
                os.mkdir(f'{cdir()}/packs/{pack_json["topic"].lower()}/{pack_json["packs"][i]["pack_id"]}/{c}')
                if showerror != 0:
                    clrprint('|-------> Made folder',f'`{c}`',clr='b,w')
            except FileExistsError:
                if showerror == 2:
                    clrprint('|-------> Folder',f'`{c}`','already exists!',clr='y,w,y')
                else:
                    pass
    if showerror != 0:
        print("\n","="*40,"\n")
