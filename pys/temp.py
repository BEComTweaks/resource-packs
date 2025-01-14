from custom_functions import *
import os
import shutil
from clrprint import clrprint as print
for json in os.listdir(f'{cdir()}/jsons/packs'):
    if json == 'compatibilities.json':
        next
    else:
        x = load_json(f'{cdir()}/jsons/packs/{json}')
        for i in x["packs"]:
            try:
                shutil.rmtree(f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}/files')
            except FileNotFoundError:
                pass
            try:
                os.rename(f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}/default', f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}/files')
                print(f"~ {i["pack_id"]}", clr="y")
            except FileNotFoundError:
                print(f"! {i["pack_id"]}", clr="r")
            filders = os.listdir(f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}')
            for filder in filders:
                if filder not in ["files", "list.json"] and "pack_icon" not in filder:
                    if "." in filder:
                        os.remove(f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}/{filder}')
                        print(f"- {filder}", clr="b")
                    else:
                        shutil.rmtree(f'{cdir()}/packs/{x["topic"].lower()}/{i["pack_id"]}/{filder}')
                        print(f"- {filder}", clr="b")