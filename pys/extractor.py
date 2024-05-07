import os
import json
from uuid import uuid4
from random import randint

if str(os.getcwd()).endswith("system32") or __name__ != "__main__":
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *
check("clrprint") # Check for clrprint module
import clrprint
check("PIL","pillow") # Check for Python Image Library
from PIL import Image

def manifestgenerator():
    mf = load_json(f"{cdir()}/jsons/others/manifest.json")
    # Pack Name
    mf["header"]["name"] = f"BTRP-{randint(0,999999)}"
    with open(f"{cdir()}/jsons/others/selected_packs.json","r") as selectedpacks:
        # Puts Selected Packs into Description
        # This part is just temporary, I have
        # not finished it yet, since the selection
        # process in incomplete
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
        os.mkdir(f'{cdir()}/{mf["header"]["name"]}')
    except:
        pass
    # Dumps JSON with formatting
    dump_json(f'{cdir()}/{mf["header"]["name"]}/manifest.json',mf)

    with Image.open(f'{cdir()}/pack_icon.png') as img:
        # Adds a pack icon for good measure
        img.save(f'{cdir()}/{mf["header"]["name"]}/pack_icon.png')

    clrinput("Press Enter to exit.",clr="green")

def extractor():
    manifestgenerator()
if __name__ == "__main__":
    extractor()