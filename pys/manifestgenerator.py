import json
from custom_functions import cdir
from uuid import uuid4
from random import randint
from os import mkdir
with open(f"{cdir()}/jsons/others/manifest.json","r") as manifest:
    mf = json.loads(manifest.read())
mf["header"]["name"] = f"BTRP-{randint(0,999999)}"
with open(f"{cdir()}/jsons/others/selected_packs.json","r") as selectedpacks:
    sp = selectedpacks.read()
    sps = ""
    for i in sp:
        if i == '"':
            sps += "'"
        else:
            sps += i
    mf["header"]["description"] = sps
mf["header"]["uuid"] = str(uuid4())
mf["modules"][0]["uuid"] =str(uuid4())
try:
    mkdir(f"{cdir()}/generated")
except:
    pass
with open(f"{cdir()}/generated/manifest.json","w") as manifest:
    manifest.write(json.dumps(mf,indent="  "))
