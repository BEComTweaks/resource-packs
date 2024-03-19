from module_checker import module_checker as mc
from json import *
from os import mkdir,getcwd
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

icon = open(f'{cdir}/pack_icon.png',"r")
while True:
    js = open(f"{cdir}/jsons/{input('Enter the JSON you want to open: ')}.json","r")
    file = loads(js.read())
    js.close()
    
    try:
        mkdir(f'{cdir}/packs/{file["topic"].lower()}')
        clrprint(f'Made Directory {file["topic"].lower()}',clr='purple')
    except FileExistsError:
        clrprint(f'{file["topic"].lower()} already exists!',clr='red')

    for i in range(len(file["packs"])):
        print("\n")
        wait(0.25)
        try:
            mkdir(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}')
            clrprint(f'Made Sub-Directory {file["packs"][i]["pack_id"]}',clr='magenta')
            x = open(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png','w')
            x.write(icon.read())
            x.close()
            clrprint(f'Made `pack_icon.png` at {cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/',clr='green')
        except FileExistsError:
            clrprint(f'{file["packs"][i]["pack_id"]} already exists!',clr='red')
        

        for c in file["packs"][i]["compatability"]:
            wait(0.25)
            try:
                mkdir(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}')
                clrprint(f'|--> Made Sub-Sub-Directory {c}',clr='blue')
                x = open(f'{cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}/pack_icon.png','w')
                x.write(icon.read())
                x.close()
                clrprint(f'|--> Made `pack_icon.png` at {cdir}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{c}/',clr='green')
            except FileExistsError:
                clrprint(f'|--> Conflict {c} already exists!',clr='yellow')
