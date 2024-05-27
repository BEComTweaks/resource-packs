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
from exporter import lsdir
check("clrprint")  # Check for clrprint module
from clrprint import clrprint
check("markdown")#  Check for markdown module
from markdown import markdown

category_start = '\n        <div class="category">\n            <div class="category-label" onclick="toggleCategory(this)">topic_name</div>\n            <div class="tweaks">'
pack = '\n                <div class="tweak" onclick="toggleSelection(this)" data-category="topic_name"\n                    data-name="pack_id" data-index="pack_index">\n                    <div class="tweak-info">\n                        <input type="checkbox" id="tweaknumber" name="tweak" value="tweaknumber">\n                        <img src="https://raw.githubusercontent.com/BedrockTweaks/Bedrock-Tweaks-Base/main/relloctopackicon"\n                            style="width:82px; height:82px;" alt="pack_name"><br>\n                        <label for="tweaknumber" class="tweak-title">pack_name</label>\n                        <div class="tweak-description">pack_description\n                        </div>\n                    </div>\n                </div>'
category_end = '\n            </div>\n        </div>'
with open(f"{cdir()}/credits.md","r") as credits:
    html_end = f'\n        <button class="download-selected-button" onclick="downloadSelectedTweaks()">Download Selected Tweaks</button>\n    </div>\n    <script src="resource-pack-page.js"></script>\n</body>\n<footer style="auto" class="container">\n    <div class="credits-footer">\n{markdown(credits.read())}\n    </div>\n</footer>\n<footer align="center">\n    <a href="https://github.com/BedrockTweaks/Bedrock-Tweaks-Base">GitHub</a>\n</footer>\n</html>'


def pre_commit():
    html = '<!DOCTYPE html>\n<html lang="en">\n\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Bedrock Tweaks</title>\n    <link rel="stylesheet" href="resource-pack-page.css">\n</head>\n\n<body>\n    <header>\n    <h1>Bedrock Tweaks</h1>\n    </header>\n\n    <div class="container">\n        <!-- Categories -->'
    stats = [0, 0]
    incomplete_packs = {"Aesthetic": [], "Colorful Slime": [], "Fixes and Consistency": [], "Fun": [],
                        "HUD and GUI": [], "Lower and Sides": [], "Menu Panoramas": [], "More Zombies": [],
                        "Parity": [], "Peace and Quiet": [], "Retro": [], "Terrain": [], "Unobtrusive": [],
                        "Utility": [], "Variation": []}
    cstats = [0, 0]
    compatibilities = {}
    pkicstats = [0, 0]
    incomplete_pkics = {"Aesthetic": [], "Colorful Slime": [], "Fixes and Consistency": [], "Fun": [],
                        "HUD and GUI": [], "Lower and Sides": [], "Menu Panoramas": [], "More Zombies": [],
                        "Parity": [], "Peace and Quiet": [], "Retro": [], "Terrain": [], "Unobtrusive": [],
                        "Utility": [], "Variation": []}
    packs = -1
    clrprint("Going through Packs...", clr="yellow")
    # Counts Packs and Compatibilities
    pack_jsons = sorted(os.listdir(f'{cdir()}/jsons/packs'))
    for c, _ in enumerate(pack_jsons):
        file = load_json(f"{cdir()}/jsons/packs/{os.listdir(f'{cdir()}/jsons/packs')[c]}")
        html += category_start.replace("topic_name", file["topic"])
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

            # Updates Incomplete pack_icon.png
            if os.path.getsize(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png') == os.path.getsize(f'{cdir()}/pack_icons/missing_texture.png'):
                # Adds packid to topic list
                incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                pkicstats[1] += 1
            else:
                # When pack icon is complete
                pkicstats[0] += 1

            # Updates Pack Compatibilities
            for comp in range(len(file["packs"][i]["compatibility"])):  # If it is empty, it just skips
                # Looks at compatibility folders
                try:
                    if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{file["packs"][i]["compatibility"][comp]}') == []:
                        # Adds the packid to the list of incomplete compatibilities
                        try:
                            compatibilities[file["packs"][i]["pack_id"]].append(file["packs"][i]["compatibility"][comp])
                        except KeyError:
                            compatibilities[file["packs"][i]["pack_id"]] = [file["packs"][i]["compatibility"][comp]]
                        cstats[1] += 1
                    else:
                        # When the compatibility directory has something inside
                        cstats[0] += 1
                except FileNotFoundError:
                    # When the compatibility folder isn't there
                    # Adds the packid to the list of incomplete compatibilities
                    try:
                        compatibilities[file["packs"][i]["pack_id"]].append(file["packs"][i]["compatibility"][comp])
                    except KeyError:
                        compatibilities[file["packs"][i]["pack_id"]] = [file["packs"][i]["compatibility"][comp]]
                    cstats[1] += 1
            
            # Adds respective HTML
            if file["packs"][i]["pack_id"] not in incomplete_packs[file["topic"]]:
                packs += 1
                to_add_pack = pack.replace("topic_name", file["topic"])
                to_add_pack = to_add_pack.replace("pack_index", str(i))
                to_add_pack = to_add_pack.replace("pack_id", file["packs"][i]["pack_id"])
                to_add_pack = to_add_pack.replace("pack_name", file["packs"][i]["pack_name"])
                to_add_pack = to_add_pack.replace("pack_description", file["packs"][i]["pack_description"])
                to_add_pack = to_add_pack.replace("tweaknumber", f"tweak{packs}")
                to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
                html += to_add_pack
            
            # Adds list of items in pack
            dump_json(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default.json',
            lsdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/default'))
            for comp in file["packs"][i]["compatibility"]:
                dump_json(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{comp}.json',
                lsdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/{comp}'))
        html += category_end
    html += html_end
    clrprint("Finished Counting!", clr="green")
    # Update files
    clrprint("Updating files...", clr="yellow")
    dump_json(f"{cdir()}/jsons/others/incomplete_packs.json", incomplete_packs)
    dump_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json", compatibilities)
    dump_json(f"{cdir()}/jsons/others/incomplete_pack_icons.json", incomplete_pkics)
    with open(f"{cdir()}/webUI/main.html", "w") as html_file:
        html_file.write(html)

    # Just some fancy code with regex to update README.md
    with open(f"{cdir()}/README.md", "r") as file:
        content = file.read()
    # Regex to update link
    pack_pattern = r"(https://img.shields.io/badge/Packs-)(\d+%2F\d+)(.*)"
    pack_match = re.search(pack_pattern, content)
    comp_pattern = r"(https://img.shields.io/badge/Compatibilities-)(\d+%2F\d+)(.*)"
    comp_match = re.search(comp_pattern, content)
    pkic_pattern = r"(https://img.shields.io/badge/Pack%20Icons-)(\d+%2F\d+)(.*)"
    pkic_match = re.search(pkic_pattern, content)

    if pack_match and comp_match and pkic_match:
        # Replace the links using regex
        new_pack_url = f"{pack_match.group(1)}{stats[0]}%2F{stats[0] + stats[1]}{pack_match.group(3)}"
        updated_content = content.replace(pack_match.group(0), new_pack_url)
        new_comp_url = f"{comp_match.group(1)}{int(cstats[0] / 2)}%2F{int(cstats[0] / 2 + cstats[1] / 2)}{comp_match.group(3)}"
        updated_content = updated_content.replace(comp_match.group(0), new_comp_url)
        new_pkic_url = f"{pkic_match.group(1)}{pkicstats[0]}%2F{pkicstats[0] + pkicstats[1]}{pkic_match.group(3)}"
        updated_content = updated_content.replace(pkic_match.group(0), new_pkic_url)
        with open(f"{cdir()}/README.md", "w") as file:
            # Update the file
            file.write(updated_content)
    else:
        # When the regex fails if I change the link
        raise IndexError("Regex Failed")

    clrprint("Updated a lot of files", clr="green")
    clrprint("Validating JSON Files...", clr="yellow")
    # JSON files validator
    for root, _, files in os.walk(cdir()):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.json') and 'node_modules' not in str(file_path):
                dump_json(file_path,load_json(file_path))
    clrprint(f"JSON Files are valid!", clr="green")
    clrinput("Press Enter to exit.", clr="green")


if __name__ == "__main__":
    pre_commit()