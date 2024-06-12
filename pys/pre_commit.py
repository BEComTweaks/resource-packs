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
check("markdown")#  Check for markdown module
from markdown import markdown

category_start = '\n            <div class="category">\n                <div class="category-label" onclick="toggleCategory(this)">topic_name</div>\n                <div class="tweaks">'
pack_start = '\n                    <div class="tweak" onclick="toggleSelection(this)" data-category="topic_name"\n                        data-name="pack_id" data-index="pack_index">'
html_comp = '\n                        <div class="comp-hover-text">Incompatible with: <incompatible></div>'
pack_mid = '\n                        <div class="tweak-info">\n                            <input type="checkbox" id="tweaknumber" name="tweak" value="tweaknumber">\n                            <img src="https://raw.githubusercontent.com/BedrockTweaks/resource-packs/main/relloctopackicon"\n                                style="width:82px; height:82px;" alt="pack_name"><br>\n                            <label for="tweak" class="tweak-title">pack_name</label>\n                            <div class="tweak-description">pack_description</div>\n                        </div>'
html_conf = '\n                        <div class="conf-hover-text">Conflicts with: <conflicts></div>'
pack_end = '\n                    </div>'

category_end = '\n                </div>\n            </div>'
with open(f"{cdir()}/credits.md","r") as credits:
    cred = str(markdown(credits.read()))
    indented = ""
    for i in cred:
        indented += i
        if i == "\n":
            indented += "            "
    html_end = f'\n            <div class="download-container">\n                <div class="file-download">\n                    <input type="text" id="fileNameInput" placeholder="Enter Pack name">\n                </div>\n                <button class="download-selected-button" onclick="downloadSelectedTweaks()">Download Selected Tweaks</button>\n                <div id="loading-circle"></div>\n            </div>\n       </div>\n        <script src="resource-pack-page.js"></script>\n    </body>\n    <footer style="auto" class="footer-container">\n        <div class="credits-footer">\n            {indented}\n			<p><a href="https://github.com/BedrockTweaks/Bedrock-Tweaks-Base">GitHub</a></p>\n        </div>\n    </footer>\n</html>'

def pre_commit():
    html = '<!DOCTYPE html>\n<html lang="en">\n    <head>\n        <meta charset="UTF-8">\n        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n        <title>Bedrock Tweaks/resource-packs</title>\n        <link rel="stylesheet" href="resource-pack-page.css">\n    </head>\n    <body>\n        <br>\n        <div class="image-container">\n            <a href="https://bedrocktweaks.github.io"><img id="title" alt="Resource Packs" src="images/title.png"></a>\n        </div>\n        <div id="background-container"></div>\n        <script>\n            // Array of textures with their corresponding probabilities\n            const textures = [\n                { src: "images/blocks/stone.png", probability: 0.618 },\n                { src: "images/blocks/copper_ore.png", probability: 0.128 },\n                { src: "images/blocks/coal_ore.png", probability: 0.128 },\n                { src: "images/blocks/iron_ore.png", probability: 0.064 },\n                { src: "images/blocks/lapis_ore.png", probability: 0.032 },\n                { src: "images/blocks/redstone_ore.png", probability: 0.016 },\n                { src: "images/blocks/gold_ore.png", probability: 0.008 },\n                { src: "images/blocks/emerald_ore.png", probability: 0.004 },\n                { src: "images/blocks/diamond_ore.png", probability: 0.002 }\n            ];\n            \n            // Function to select a texture based on the defined probabilities\n            function selectTexture() {\n                const rand = Math.random();\n                let cumulativeProbability = 0;\n            \n                for (const texture of textures) {\n                    cumulativeProbability += texture.probability;\n                    if (rand < cumulativeProbability) {\n                        return texture.src;\n                    }\n                }\n            }\n            \n            // Function to create tiles with random background images\n            function createTiles() {\n                const container = document.getElementById("background-container");\n                const numColumns = Math.ceil(window.innerWidth / 100) + 2;\n                const numRows = Math.ceil(window.innerHeight / 100) + 2;\n            \n                container.innerHTML = "";\n            \n                for (let i = 0; i < numColumns; i++) {\n                    const rowDiv = document.createElement("div");\n                    rowDiv.className = "row"; // Add a class for styling purposes if needed\n            \n                    for (let j = 0; j < numRows; j++) {\n                        const tile = document.createElement("div");\n                        tile.className = "tile";\n                        tile.style.backgroundImage = `url("${selectTexture()}")`;\n                        rowDiv.appendChild(tile);\n                    }\n            \n                    container.appendChild(rowDiv);\n                }\n            }\n            // Call the function to create tiles\n            createTiles();\n            \n            // Redraw tiles on window resize to maintain the grid\n            window.addEventListener("resize", () => {\n                document.getElementById("background-container").innerHTML = "";\n                createTiles();\n            });\n        </script>\n        <div class="container">\n            <!-- Categories -->'
    stats = [0, 0]
    incomplete_packs = {"Aesthetic": [], "Colorful Slime": [], "Fixes and Consistency": [], "Fun": [],
                        "HUD and GUI": [], "Lower and Sides": [], "Menu Panoramas": [], "More Zombies": [],
                        "Parity": [], "Peace and Quiet": [], "Retro": [], "Terrain": [], "Unobtrusive": [],
                        "Utility": [], "Variation": []}
    cstats = [0, 0]
    compatibilities = {}
    conflicts = {}
    pkicstats = [0, 0]
    incomplete_pkics = {"Aesthetic": [], "Colorful Slime": [], "Fixes and Consistency": [], "Fun": [],
                        "HUD and GUI": [], "Lower and Sides": [], "Menu Panoramas": [], "More Zombies": [],
                        "Parity": [], "Peace and Quiet": [], "Retro": [], "Terrain": [], "Unobtrusive": [],
                        "Utility": [], "Variation": []}
    packs = -1
    clrprint("Going through Packs...", clr="yellow")
    # Counts Packs and Compatibilities
    pack_jsons = sorted(os.listdir(f'{cdir()}/jsons/packs'))
    for _, j in enumerate(pack_jsons):
        file = load_json(f"{cdir()}/jsons/packs/{j}")
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
            
            # Updates Incomplete Pack Compatibilities
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
            
            # Updates Pack Conflicts
            conflicts[file["packs"][i]["pack_id"]] = []
            for conf in range(len(file["packs"][i]["conflict"])):  # If it is empty, it just skips
                conflicts[file["packs"][i]["pack_id"]].append(file["packs"][i]["conflict"][conf])
            if conflicts[file["packs"][i]["pack_id"]] == []:
                del conflicts[file["packs"][i]["pack_id"]]
            
            # Adds respective HTML
            compats = ""
            confs = ""
            if file["packs"][i]["pack_id"] not in incomplete_packs[file["topic"]]:
                packs += 1
                to_add_pack = pack_start
                try:
                    c = ""
                    for c in compatibilities[file["packs"][i]["pack_id"]]:
                        compats += c
                        compats += ", "
                    to_add_pack += html_comp.replace('<incompatible>',compats[:-2])
                except KeyError:
                    pass
                to_add_pack += pack_mid
                try:
                    c = ""
                    for c in conflicts[file["packs"][i]["pack_id"]]:
                        confs += c
                        confs += ", "
                    to_add_pack += html_conf.replace('<conflicts>',confs[:-2])
                except KeyError:
                    pass
                to_add_pack += pack_end
                # Replace vars
                to_add_pack = to_add_pack.replace("topic_name", file["topic"])
                to_add_pack = to_add_pack.replace("pack_index", str(i))
                to_add_pack = to_add_pack.replace("pack_id", file["packs"][i]["pack_id"])
                to_add_pack = to_add_pack.replace("pack_name", file["packs"][i]["pack_name"])
                to_add_pack = to_add_pack.replace("pack_description", file["packs"][i]["pack_description"])
                to_add_pack = to_add_pack.replace("tweaknumber", f"tweak{packs}")
                to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
                #to_add_pack = to_add_pack.replace("https://raw.githubusercontent.com/BedrockTweaks/resource-packs/main/","../")
                html += to_add_pack
        html += category_end
    html += html_end
    clrprint("Finished Counting!", clr="green")
    # Update files
    clrprint("Updating files...", clr="yellow")
    dump_json(f"{cdir()}/jsons/others/incomplete_packs.json", incomplete_packs)
    dump_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json", compatibilities)
    dump_json(f"{cdir()}/jsons/others/incomplete_pack_icons.json", incomplete_pkics)
    dump_json(f"{cdir()}/jsons/others/pack_conflicts.json", conflicts)
    with open(f"{cdir()}/webUI/index.html", "w") as html_file:
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