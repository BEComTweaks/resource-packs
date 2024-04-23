from custom_functions import *
from json import *
import os
import re

stats = [0,0]
incomplete_packs = {}
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}","r") as js:
        try:
            file = loads(js.read())
        except JSONDecodeError:
            raise SyntaxError(f"{os.listdir(f'{cdir()}/jsons/packs')[c]} has a skill issue.\nPerhaps you are missing a comma?")
    for i in range(len(file["packs"])):
        try:
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default') == []:
                try:
                    # Adds the packid to the topic list
                    incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                except KeyError:
                    # If the topic doesn't exist in the dictionary
                    incomplete_packs[file["topic"]] = [file["packs"][i]["pack_id"]]
                stats[1] += 1
            else:
                # When the packid directory has stuff inside
                stats[0] += 1
        except FileNotFoundError:
            # If the packs have not updated with the new directory type
            stats[1] += 1
            incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])

# Just some fancy code to update README.md
with open(f"{cdir()}/README.md", "r") as file:
    content = file.read()
badge_pattern = r"(https://img.shields.io/badge/Completed_Packs-)(\d+%2F\d+)(-blue)"
badge_match = re.search(badge_pattern, content)
if badge_match:
    new_badge_url = f"{badge_match.group(1)}{stats[0]}%2F{stats[0]+stats[1]}{badge_match.group(3)}"
    updated_content = content.replace(badge_match.group(0), new_badge_url)
    with open(f"{cdir()}/README.md", "w") as file:
        file.write(updated_content)
else:
    raise IndexError("Regex Failed")

# Update incomplete_packs.json
with open(f"{cdir()}/jsons/others/incomplete_packs.json","w") as incomplete_packs_file:
    incomplete_packs_file.write(dumps(incomplete_packs,indent=2))

