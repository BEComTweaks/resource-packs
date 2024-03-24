from custom_functions import module_checker as mc
from json import *
from os import mkdir,getcwd,listdir
mc("clrprint") #Check for clrprint module
from clrprint import clrprint
from time import sleep as wait

cdir,cdirs = "",getcwd()
for i in cdirs:
    if ord(i) == 92:
        cdir+="/"
    else:
        cdir+=i
cdir = cdir[:-4]
print("="*40, "\n")
icon = open(f'{cdir}/pack_icon.png',"r")
for i in range(len(listdir(f'{cdir}/jsons'))):
    js = open(f"{cdir}/jsons/{listdir(f'{cdir}/jsons')[i]}","r")
    file = loads(js.read())
    js.close()
    
    # Main Topic Directory
    try:
        mkdir(f'{cdir}/packs/{file["topic"].lower()}')
        clrprint('Made directory',f'{file["topic"].lower()}',clr='p,w')
    except FileExistsError:
        clrprint(f'{file["topic"].lower()}','already exists!',clr='w,r')

    for i in range(len(file["packs"])):
        print("\n")
        
        # Pack Name Directory
        try:
            mkdir(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/')
            clrprint('Made folder',f'`{file["packs"][i]["pack_id"]}`',clr='m,w')
        except FileExistsError:
            clrprint('Folder',f'`{file["packs"][i]["pack_id"]}`','already exists!',clr='r,w,r')

        # Pack Default Directory
        try:
            mkdir(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default')
            clrprint(f'|--> Made folder','`default`',clr='b,w')
        except FileExistsError:
            clrprint(f'|--> Folder','`default`','already exists!',clr='y,w,y')

        # Pack Default Directory temporary image
        x = open(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default/pack_icon.png','w')
        x.write(icon.read())
        x.close()
        clrprint('|--|--> Made','`pack_icon.png`',clr='g,w')

        for c in file["packs"][i]["compatability"]:
            # Pack Name Compatabilities Directory
            try:
                mkdir(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}')
                clrprint('|--> Made folder',f'`{c}`',clr='b,w')
            except FileExistsError:
                clrprint('|--> Folder',f'`{c}`','already exists!',clr='y,w,y')
            
            # Pack Compatabilities Directory temporary file
            x = open(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}/pack_icon.png','w')            
            x.write(icon.read())
            x.close()
            clrprint('|--|--> Made file','`pack_icon.png`',clr='g,w')
    print("\n","="*40,"\n")
