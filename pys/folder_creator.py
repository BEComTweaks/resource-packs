from custom_functions import *
from json import *
from os import mkdir,getcwd,listdir
check("clrprint") #Check for clrprint module
check("shutil") #Check for shtil module (not sure if it is pre-installed, so just in case)
from clrprint import *
from shutil import copy as copyfile

print("="*40, "\n")
icon = open(f'{cdir()}/pack_icon.png',"r")
for c in range(len(listdir(f'{cdir()}/jsons'))):
    js = open(f"{cdir()}/jsons/{listdir(f'{cdir()}/jsons')[c]}","r")
    file = loads(js.read())
    js.close()
    
    # Main Topic Directory
    try:
        mkdir(f'{cdir()}/packs/{file["topic"].lower()}')
        clrprint('Made directory',f'{file["topic"].lower()}',clr='p,w')
    except FileExistsError:
        clrprint(f'{file["topic"].lower()}','already exists!',clr='w,r')

    for i in range(len(file["packs"])):
        # Pack Name Directory
        try:
            mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/')
            clrprint('|----> Made folder',f'`{file["packs"][i]["pack_id"]}`',clr='m,w')
        except FileExistsError:
            clrprint('|----> Folder',f'`{file["packs"][i]["pack_id"]}`','already exists!',clr='r,w,r')

        # Pack Default Directory
        try:
            mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default')
            clrprint(f'|---------> Made folder','`default`',clr='b,w')
        except FileExistsError:
            clrprint(f'|---------> Folder','`default`','already exists!',clr='y,w,y')

        # Pack Directory pack_icon.png
        r =  open(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png','r')
        if len(listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}')) == 2 and len(r.read()) == 0:
            r.close()
            copyfile(f'{cdir()}/pack_icon.png',f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
            clrprint('|--------------> Made','`pack_icon.png`',clr='g,w')
            input(listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}'))
        elif len(r.read()) != 0:
            r.close()
            clrprint('|-------------->','`pack_icon.png`','has been modified!',clr='m,w,m')
        
        for c in file["packs"][i]["compatability"]:
            # Pack Name Compatabilities Directory
            try:
                mkdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}')
                clrprint('|---------> Made folder',f'`{c}`',clr='b,w')
            except FileExistsError:
                clrprint('|---------> Folder',f'`{c}`','already exists!',clr='y,w,y')
    print("\n","="*40,"\n")
icon.close()
