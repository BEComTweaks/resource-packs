from custom_functions import *
from json import *
check("clrprint") #Check for clrprint module
from clrprint import *
import os
incomplete_packs = {}
for c in range(len(os.listdir(f'{cdir()}/jsons'))):
    if os.listdir(f'{cdir()}/jsons')[c] != "incomplete_packs.json":
        js = open(f"{cdir()}/jsons/{os.listdir(f'{cdir()}/jsons')[c]}","r")
        file = loads(js.read())
        js.close()
        for i in range(len(file["packs"])):
            try:
                if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default') == []:
                    incomplete_packs[f'{file["packs"][i]["pack_id"]}'] = f'{file["topic"]}'
            except FileNotFoundError:
                # The packs have not updated with the new directory type
                incomplete_packs[f'{file["packs"][i]["pack_id"]}'] = f'{file["topic"]}'
incomplete_packs_file = open(f"{cdir()}/jsons/incomplete_packs.json","w")
incomplete_packs_file.write(dumps(incomplete_packs,indent=2))
incomplete_packs_file.close()
