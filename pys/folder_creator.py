from custom_functions import *
from json import *
import os
check("clrprint") #Check for clrprint module
check("shutil") #Check for shtil module (not sure if it is pre-installed, so just in case)
from clrprint import *
from shutil import copy as copyfile

print("="*40, "\n")
showerror = bool(int(input("Show error?\n(0 = No, 1 = Yes)\n")))
for c in range(len(os.listdir(f'{cdir()}/jsons'))):
    js = open(f"{cdir()}/jsons/{os.listdir(f'{cdir()}/jsons')[c]}","r")
    file = loads(js.read())
    js.close()
    
    print(file["topic"].lower())
    # Main Topic Directory
    try:
        os.mkdir(f'{cdir()}/packs/{file["topic"].lower()}')
        clrprint('Made directory',f'{file["topic"].lower()}',clr='p,w')
    except FileExistsError:
        if showerror:
            clrprint(f'{file["topic"].lower()}','already exists!',clr='w,r')
        else:
            pass

    for i in range(len(file["packs"])):
        # Pack Name Directory
        clrprint(f'|--> {file["packs"][i]["pack_id"]}')
        try:
            os.mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/')
            clrprint('|----> Made folder',clr='m')
        except FileExistsError:
            if showerror:
                clrprint('|----> Folder already exists!',clr='r')
            else:
                pass

        # Pack Default Directory
        try:
            os.mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default')
            clrprint(f'|-------> Made folder','`default`',clr='b,w')
        except FileExistsError:
            if showerror:
                clrprint(f'|-------> Folder','`default`','already exists!',clr='y,w,y')
            else:
                pass

        # Pack Directory pack_icon.png
        r =  open(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png','a')
        r.close()        
        if len(os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}')) == 2 and os.path.getsize(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png') == 0:
            copyfile(f'{cdir()}/pack_icon.png',f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
            clrprint('|----------> Made','`pack_icon.png`',clr='g,w')
        elif os.path.getsize(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png') != 0 and showerror:
            clrprint('|---------->','`pack_icon.png`','has been modified!',clr='m,w,m')
        
        for c in file["packs"][i]["compatability"]:
            # Pack Name Compatabilities Directory
            try:
                os.mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}')
                clrprint('|-------> Made folder',f'`{c}`',clr='b,w')
            except FileExistsError:
                if showerror:
                    clrprint('|-------> Folder',f'`{c}`','already exists!',clr='y,w,y')
                else:
                    pass
    print("\n","="*40,"\n")