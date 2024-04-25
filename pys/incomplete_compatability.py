from custom_functions import cdir
from json import *
import os
import re
cstats = [0,0]
compatabilities = []
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}","r") as js:
        try:
            file = loads(js.read())
        except JSONDecodeError:
            raise SyntaxError(f"{os.listdir(f'{cdir()}/jsons/packs')[c]} has a skill issue.\nPerhaps you are missing a comma?")
    for i in range(len(file["packs"])):
        for comp in range(len(file["packs"][i]["compatability"])):
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{file["packs"][i]["compatability"][comp]}') == []:
                # Adds the packid to the list of incomplete compatabilities
                compatabilities.append(file["packs"][i]["compatability"])
                cstats[1] += 1
            else:
                # When the Compatability Directory has something inside
                print(f'+\t{file["topic"]}\t{file["packs"][i]["pack_id"]}\t{file["packs"][i]["compatability"][comp]}')
                cstats[0] += 1
print(cstats)

# Just some fancy code to update README.md
with open(f"{cdir()}/README.md", "r") as file:
    content = file.read()
badge_pattern = r"(https://img.shields.io/badge/Compatabilities-)(\d+%2F\d+)(-blue)"
badge_match = re.search(badge_pattern, content)
if badge_match:
    new_badge_url = f"{badge_match.group(1)}{cstats[0]}%2F{cstats[0]+cstats[1]}{badge_match.group(3)}"
    updated_content = content.replace(badge_match.group(0), new_badge_url)
    with open(f"{cdir()}/README.md", "w") as file:
        file.write(updated_content)
else:
    raise IndexError("Regex Failed")