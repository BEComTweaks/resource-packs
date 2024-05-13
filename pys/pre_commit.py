import os
from json import *
import re
from shutil import get_terminal_size
import time

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *

check("clrprint")  # Check for clrprint module
from clrprint import clrprint


def pre_commit():
    stats = [0, 0]
    incomplete_packs = {"Aesthetic": [], "Colorful Slime": [], "Fixes and Consistency": [], "Fun": [],
                        "HUD and GUI": [], "Lower and Sides": [], "Menu Panoramas": [], "More Zombies": [],
                        "Parity": [], "Peace and Quiet": [], "Retro": [], "Terrain": [], "Unobtrusive": [],
                        "Utility": [], "Variation": []}
    cstats = [0, 0]
    compatibilities = {}
    conflicts = {}

    if input("Show Compatibility Progress? [y/n]\n") == "y":
        showcomp = True
    else:
        showcomp = False
    clrprint("Counting Packs and Compatibilities...", clr="yellow")
    # Counts Packs and Compatibilities
    for c in range(len(os.listdir(f'{cdir()}/jsons/packs'))):
        file = load_json(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}")
        # For compatibilities, as it doesn't have a file
        if showcomp:
            clrprint(f'= {file["topic"]}', clr="white")
        # Runs through the packs
        for i in range(len(file["packs"])):
            # Updates Incomplete Packs
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

            # Updates Pack Compatibilities
            if file["packs"][i]["compatibility"] != []:
                if showcomp:
                    clrprint(f'= \t{file["packs"][i]["pack_id"]}', clr="yellow")
            for comp in range(len(file["packs"][i]["compatibility"])):  # If it is empty, it just skips
                # Looks at compatibility folders
                try:
                    if os.listdir(
                            f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{file["packs"][i]["compatibility"][comp]}') == []:
                        if showcomp:
                            clrprint(f'- \t\t{file["packs"][i]["compatibility"][comp]}', clr="red")
                        # Adds the packid to the list of incomplete compatibilities
                        try:
                            compatibilities[file["packs"][i]["pack_id"]].append(file["packs"][i]["compatibility"][comp])
                        except KeyError:
                            compatibilities[file["packs"][i]["pack_id"]] = [file["packs"][i]["compatibility"][comp]]
                        cstats[1] += 1
                    else:
                        if showcomp:
                            clrprint(f'+ \t\t{file["packs"][i]["compatibility"][comp]}', clr="green")
                        # When the compatibility directory has something inside
                        cstats[0] += 1
                except FileNotFoundError:
                    # When the compatibility folder isn't there
                    if showcomp:
                        clrprint(f'- \t\t{file["packs"][i]["compatibility"][comp]}', clr="red")
                    # Adds the packid to the list of incomplete compatibilities
                    try:
                        compatibilities[file["packs"][i]["pack_id"]].append(file["packs"][i]["compatibility"][comp])
                    except KeyError:
                        compatibilities[file["packs"][i]["pack_id"]] = [file["packs"][i]["compatibility"][comp]]
                    cstats[1] += 1

    clrprint("Finished Counting!", clr="green")
    # Update incomplete_packs.json
    dump_json(f"{cdir()}/jsons/others/incomplete_packs.json", incomplete_packs)
    dump_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json", compatibilities)
    clrprint("Updated incomplete_packs.json and incomplete_compatibilities.json", clr="green")
    clrprint("Updating README.md...", clr="yellow")

    # Just some fancy code with regex to update README.md
    with open(f"{cdir()}/README.md", "r") as file:
        content = file.read()
    # Regex to update link
    pack_pattern = r"(https://img.shields.io/badge/Packs-)(\d+%2F\d+)(.*)"
    pack_match = re.search(pack_pattern, content)
    comp_pattern = r"(https://img.shields.io/badge/Compatibilities-)(\d+%2F\d+)(.*)"
    comp_match = re.search(comp_pattern, content)

    if pack_match and comp_match:
        # Replace the links using regex
        new_pack_url = f"{pack_match.group(1)}{stats[0]}%2F{stats[0] + stats[1]}{pack_match.group(3)}"
        updated_content = content.replace(pack_match.group(0), new_pack_url)
        new_comp_url = f"{comp_match.group(1)}{cstats[0]}%2F{cstats[0] + cstats[1]}{comp_match.group(3)}"
        updated_content = updated_content.replace(comp_match.group(0), new_comp_url)
        with open(f"{cdir()}/README.md", "w") as file:
            # Update the file
            file.write(updated_content)
    else:
        # When the regex fails if I change the link
        raise IndexError("Regex Failed")

    clrprint("Updated README.md!", clr="green")
    clrprint("Validating JSON Files...", clr="yellow")

    longest_path = 0
    # JSON files validator
    for root, _, files in os.walk(cdir()):
        for file in files:
            if file.lower().endswith('.json'):
                file_path = os.path.join(root, file)
                if longest_path < len(file_path):
                    longest_path = len(file_path)
                try:
                    file = dumps(load_json(file_path), indent=2)
                    with open(file_path, "w") as towrite:
                        towrite.write(file.replace(r"\/", "/"))
                    print(f'\r{str(file_path)[len(cdir()):]}{" " * (longest_path - len(file_path))}', end="")
                except Exception as e:
                    print(f"Error in file '{file_path}': {str(e)}")
                    exit(1)

    clrprint(f"\rJSON Files are valid!{' ' * (longest_path - 21)}", clr="green")
    clrinput("Press Enter to exit.", clr="green")
    clear()


if __name__ == "__main__":
    pre_commit()
