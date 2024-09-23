import os
from json import *
import re
from time import sleep
import argparse

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *
check("clrprint")
from clrprint import clrprint
check("markdown")
from markdown import markdown
check("bs4","beautifulsoup4")
from bs4 import BeautifulSoup

category_start = '<div class="category"><div class="category-label" onclick="toggleCategory(this)">topic_name</div><div class="category-controlled"><div class="tweaks">'
subcategory_start = '<div class="subcategory"><div class="category-label" onclick="toggleCategory(this)">topic_name</div><div class="category-controlled"><div class="subcattweaks">'
pack_start = '<div class="tweak" onclick="toggleSelection(this)" data-category="topic_name" data-name="pack_id" data-index="pack_index">'
html_comp = '<div class="comp-hover-text">Incompatible with: <incompatible></div>'
pack_mid = '<div class="tweak-info"><input type="checkbox" id="tweaknumber" name="tweak" value="tweaknumber"><img src="https://raw.githubusercontent.com/BEComTweaks/resource-packs/main/relloctopackicon"style="width:82px; height:82px;" alt="pack_name"><br><label id="tweak" class="tweak-title">pack_name</label><div class="tweak-description">pack_description</div></div>'
html_conf = '<div class="conf-hover-text">Conflicts with: <conflicts></div>'
pack_end = '</div>'
category_end = '</div></div></div>'
cat_end_w_subcat_no_end = '</div><div class="subcat<index>">'

with open(f"{cdir()}/credits.md","r") as credits:
    html_end = f'</div><div class="download-container"><div class="file-download"><input type="text" id="fileNameInput" placeholder="Enter Pack name"><br><select name="mev" id="mev"><option value="1.21.0">1.21</option><option value="1.20.0">1.20</option><option value="1.19.0">1.19</option><option value="1.18.0">1.18</option><option value="1.17.0">1.17</option><option value="1.16.0">1.16</option></select></div><div class="zipinputcontainer"><input type="file" id="zipInput"/></div><button class="download-selected-button" onclick="downloadSelectedTweaks()">Download Selected Tweaks</button><div id="selected-tweaks"><div class="tweak-list-pack">Select some packs and see them appear here!</div></div></div><script src="app.js"></script></div></body><footer class="footer-container"><div class="half-dark"><div class="credits-footer">{str(markdown(credits.read()))}<p><a href="https://github.com/BEComTweaks/resource-packs">GitHub</a></p></div></div></footer></html>'

html = '<!DOCTYPE html><html lang="en"><head><meta content="Bedrock Edition Community Tweaks Resource Packs" name="author"><meta content="Resource Pack tweak selector. Unofficially updated by BEComTweaks on GitHub" name="description"><meta charset="utf-8"><meta content="width=device-width, initial-scale=1.0" name="viewport"><title>Resource Packs</title><link href="theme.css" rel="stylesheet"><link href="images/icon.png" rel="icon" type="image/x-icon"></meta></meta></head><body><div id="background-container"></div><script src="bg.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.7.1/jszip.min.js"></script><div class="half-dark"><br><br><div class="image-container"><img alt="Resource Packs" id="title" src="images/title.png"></div><ul class="large-nav"><li><a class="nav-link" href="https://becomtweaks.github.io">Home</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/crafting-tweaks">Crafting Tweaks</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/behaviour-packs">Behaviour Packs</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/resource-packs">Resource Packs</a></li></ul><ul class="small-nav"><li><a class="nav-link" href="https://becomtweaks.github.io">Home</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/crafting-tweaks">CTs</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/behaviour-packs">BPs</a></li><li style="float:right"><a class="nav-link" href="https://becomtweaks.github.io/resource-packs">RPs</a></li></ul><div class="container"><!-- Categories -->'
stats = [0, 0]
incomplete_packs = {}
cstats = [0, 0]
compatibilities = {}
conflicts = {}
pkicstats = [0, 0]
subcats = 0
ignore = False
subcat_list = []
incomplete_pkics = {}
packs = -1
pack_list = []
name_to_json = {}
clrprint("Going through Packs...", clr="yellow")
with open(f"{cdir()}/jsons/others/pack_order_list.txt","r") as pol:
    for i in pol:
        pack_list.append(i)

parser = argparse.ArgumentParser(description='Run a massive script that updates Packs to-do, Icons to-do, Compatibilities to-do and the HTML')
parser.add_argument('--format', action='store_true', help='Include flag to format files')
parser.add_argument('--use-relative-location', action='store_true', help='Use relative location')
args = parser.parse_args()

# Counts Packs and Compatibilities
for j in pack_list:
    origj = j
    if not ignore:
        if j.endswith("\n"):
            j = j[:-1]
        file = load_json(f"{cdir()}/jsons/packs/{j}")
        name_to_json[file["topic"]] = j
        incomplete_packs[file["topic"]] = []
        incomplete_pkics[file["topic"]] = []
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
            try:
                if file["packs"][i]["pack_id"] in incomplete_packs[file["topic"]]:
                    pass
                elif os.path.getsize(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png') == os.path.getsize(f'{cdir()}/pack_icons/missing_texture.png'):
                    # Adds packid to topic list
                    incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                    pkicstats[1] += 1
                else:
                    # When pack icon is complete
                    pkicstats[0] += 1
            except:
                if file["packs"][i]["details"]["icon"] != "png": # Assuming pack icon is done
                    pkicstats[0] += 1
                else:
                    # When pack icon doesn't even exist
                    incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                    pkicstats[1] += 1
            
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
                desc = file["packs"][i]["pack_description"]
                try:
                    if file["packs"][i]["details"]["message"][0] == "warn":
                        desc += f'<p class="desc-warn">{file["packs"][i]["details"]["message"][1]}</p>'
                    elif file["packs"][i]["details"]["message"][0] == "error":
                        desc += f'<p class="desc-error">{file["packs"][i]["details"]["message"][1]}</p>'
                    elif file["packs"][i]["details"]["message"][0] == "info":
                        desc += f'<p class="desc-info">{file["packs"][i]["details"]["message"][1]}</p>'
                except KeyError:
                    pass
                to_add_pack = to_add_pack.replace("pack_description", desc)
                to_add_pack = to_add_pack.replace("tweaknumber", f"tweak{packs}")
                to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
                try:
                    to_add_pack = to_add_pack.replace("png", file["packs"][i]["details"]["icon"])
                except KeyError:
                    pass
                # Uses relative location
                if args.use_relative_location:
                    to_add_pack = to_add_pack.replace("https://raw.githubusercontent.com/BEComTweaks/resource-packs/main/","../")
                html += to_add_pack
    try:
        if pack_list[pack_list.index(origj) + 1].startswith("\t"):
            html += cat_end_w_subcat_no_end
            try:
                if not pack_list[pack_list.index(origj) + 2].startswith("\t"):
                    html += category_end
            except IndexError:
                pass
            html = html.replace("<index>", str(subcats))
            subcats += 1
            ignore = True
            subcat_list.append(pack_list[pack_list.index(origj) + 1][1:])
        elif not ignore:
            html += category_end
        else:
            ignore = False
    except IndexError:
        html += category_end
for j in range(len(subcat_list)):
    pack_html = ""
    k = subcat_list[j]
    if k.endswith("\n"):
        k = k[:-1]
    if k.startswith("\t"):
        k = k[1:]
    file = load_json(f"{cdir()}/jsons/packs/{k}")
    name_to_json[file["topic"]] = k
    incomplete_packs[file["topic"]] = []
    incomplete_pkics[file["topic"]] = []
    pack_html += subcategory_start.replace("topic_name", f'{file["subcategory_of"]} > <b>{file["topic"]}</b>')
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
        try:
            if file["packs"][i]["pack_id"] in incomplete_packs[file["topic"]]:
                pass
            elif os.path.getsize(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png') == os.path.getsize(f'{cdir()}/pack_icons/missing_texture.png'):
                # Adds packid to topic list
                incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                pkicstats[1] += 1
            else:
                # When pack icon is complete
                pkicstats[0] += 1
        except:
            if file["packs"][i]["details"]["icon"] != "png": # Assuming pack_icon is done
                pkicstats[0] += 1
            else:
                # When pack icon doesn't even exist
                incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                pkicstats[1] += 1
        
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
            desc = file["packs"][i]["pack_description"]
            try:
                if file["packs"][i]["details"]["message"][0] == "warn":
                    desc += f'<p class="desc-warn">{file["packs"][i]["details"]["message"][1]}</p>'
                elif file["packs"][i]["details"]["message"][0] == "error":
                    desc += f'<p class="desc-error">{file["packs"][i]["details"]["message"][1]}</p>'
                elif file["packs"][i]["details"]["message"][0] == "info":
                    desc += f'<p class="desc-info">{file["packs"][i]["details"]["message"][1]}</p>'
            except KeyError:
                pass
            to_add_pack = to_add_pack.replace("pack_description", desc)
            to_add_pack = to_add_pack.replace("tweaknumber", f"tweak{packs}")
            to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
            try:
                to_add_pack = to_add_pack.replace("png", file["packs"][i]["details"]["icon"])
            except KeyError:
                pass
            if args.use_relative_location:
                to_add_pack = to_add_pack.replace("https://raw.githubusercontent.com/BEComTweaks/resource-packs/main/","../")
            pack_html += to_add_pack
    pack_html += category_end
    html = html.replace(f'<div class="subcat{j}"></div>',pack_html)
clrprint("Finished Counting!", clr="green")

# HTML formatting
html += html_end
soup = BeautifulSoup(html, 'html.parser')
html = soup.prettify()
html = html.replace("<br/>", "<br>")
# Update files
clrprint("Updating files...", clr="yellow")
dump_json(f"{cdir()}/jsons/others/incomplete_packs.json", incomplete_packs)
dump_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json", compatibilities)
dump_json(f"{cdir()}/jsons/others/incomplete_pack_icons.json", incomplete_pkics)
dump_json(f"{cdir()}/jsons/others/name_to_json.json", name_to_json)
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
clrprint("Updated a lot of files!", clr="green")

if args.format:
    clrprint("Making files Prettier", clr="yellow")
    os.system(f"cd {cdir()}")
    os.system('npx prettier --write "**/*.{js,ts,css,json}" --log-level silent')
    clrprint("Files are Prettier!", clr="green")
