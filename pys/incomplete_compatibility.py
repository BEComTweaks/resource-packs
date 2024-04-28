import os
from json import *
import re

if str(os.getcwd()).endswith("system32"):
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:/Windows/System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
else:
    doubleclicked = False

from custom_functions import *
check("clrprint") # Check for clrprint module
from clrprint import clrprint

cstats = [0,0]
compatibilities = []
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
    clrprint(f'= {file["topic"]}',clr="white")
    for i in range(len(file["packs"])):
        if file["packs"][i]["compatibility"] != []:
            clrprint(f'= \t{file["packs"][i]["pack_id"]}',clr="yellow")
        for comp in range(len(file["packs"][i]["compatibility"])):
            if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{file["packs"][i]["compatibility"][comp]}') == []:
                clrprint(f'- \t\t{file["packs"][i]["compatibility"][comp]}',clr="red")
                # Adds the packid to the list of incomplete compatibilities
                compatibilities.append(file["packs"][i]["compatibility"])
                cstats[1] += 1
            else:
                clrprint(f'+ \t\t{file["packs"][i]["compatibility"][comp]}',clr="green")
                # When the compatibility Directory has something inside
                cstats[0] += 1

# Just some fancy code to update README.md
with open(f"{cdir()}/README.md", "r") as file:
    content = file.read()
# Regex to update link
badge_pattern = r"(https://img.shields.io/badge/Compatibilities-)(\d+%2F\d+)(.*)"
badge_match = re.search(badge_pattern, content)
if badge_match:
    # Replace the link using regex
    new_badge_url = f"{badge_match.group(1)}{cstats[0]}%2F{cstats[0]+cstats[1]}{badge_match.group(3)}"
    updated_content = content.replace(badge_match.group(0), new_badge_url)
    with open(f"{cdir()}/README.md", "w") as file:
        # Update the file
        file.write(updated_content)
else:
    # When the regex fails if I change the link
    raise IndexError("Regex Failed")

if doubleclicked:
    clrprint("Updated README.md",clr="green")
    clrprint("Press Enter to exit.",clr="green",end="")
    input()