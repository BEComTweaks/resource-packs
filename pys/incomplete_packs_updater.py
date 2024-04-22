from custom_functions import *
from json import *
import os
incomplete_packs = {}
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}","r") as js:
        file = loads(js.read())
    for i in range(len(file["packs"])):
        try:
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default') == []:
                try:
                    incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                except KeyError:
                    incomplete_packs[file["topic"]] = [file["packs"][i]["pack_id"]]
        except FileNotFoundError:
            # The packs have not updated with the new directory type
            incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
incomplete_packs_file = open(f"{cdir()}/jsons/others/incomplete_packs.json","w")
incomplete_packs_file.write(dumps(incomplete_packs,indent=2))
incomplete_packs_file.close()
