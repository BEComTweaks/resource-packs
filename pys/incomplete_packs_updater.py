import os
import time
from json import *
import re

if os.getcwd() == "C:\u005CWindows\u005Csystem32":
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:/Program Files/System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
else:
    doubleclicked = False

from custom_functions import *
check("clrprint")
from clrprint import clrprint # Check for clrprint module

# The main stuff
stats = [0,0]
incomplete_packs = {}
for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
    with open(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}","r") as js:
        try:
            file = loads(js.read())
        except JSONDecodeError:
            # When it has an error
            # JSONDecodeError normally prints where I am missing a comma/bracket
            # But not the file, so this brings it up as well
            # Hence why if there is an issue with the JSON, it brings up two errors at once
            raise SyntaxError(f"{os.listdir(f'{cdir()}/jsons/packs')[c]} has a skill issue.\nPerhaps you are missing a comma?")
    for i in range(len(file["packs"])):
        try:
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default') == []:
                # Adds the packid to the topic list
                incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                stats[1] += 1
            else:
                # When the packid directory has stuff inside
                stats[0] += 1
        except FileNotFoundError:
            # If the packs have not updated with the new directory type
            stats[1] += 1
            incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
        except KeyError:
            # If the topic doesn't exist in the dictionary
            incomplete_packs[file["topic"]] = [file["packs"][i]["pack_id"]]
            stats[1] += 1

# Just some fancy code to update README.md
with open(f"{cdir()}/README.md", "r") as file:
    content = file.read()
# Regex to update link
badge_pattern = r"(https://img.shields.io/badge/Packs-)(\d+%2F\d+)(-blue)"
badge_match = re.search(badge_pattern, content)
if badge_match:
    # Replace the link using regex
    new_badge_url = f"{badge_match.group(1)}{stats[0]}%2F{stats[0]+stats[1]}{badge_match.group(3)}"
    updated_content = content.replace(badge_match.group(0), new_badge_url)
    with open(f"{cdir()}/README.md", "w") as file:
        # Update the file
        file.write(updated_content)
else:
    # When the regex fails if I change the link
    raise IndexError("Regex Failed")

# Update incomplete_packs.json
with open(f"{cdir()}/jsons/others/incomplete_packs.json","w") as incomplete_packs_file:
    incomplete_packs_file.write(dumps(incomplete_packs,indent=2))

if doubleclicked:
    clrprint("Press Enter to exit.",clr="green",end="")
    input()