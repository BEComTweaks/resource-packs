import os, re, shutil, argparse
from json import *
from time import sleep

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
check("lzstring")
from lzstring import LZString

category_start = '<div class="category"><div oreui-type="button" oreui-color="dark" class="category-label" onclick="OreUI.toggleActive(this);toggleCategory(this);">topic_name</div><button class="category-label-selectall" onclick="selectAll(this)" data-allpacks="<all_packs>" data-category="topic_name"><img src="images/select-all-button/chiseled_bookshelf_empty.png" class="category-label-selectall-img"><div class="category-label-selectall-hovertext">Select All</div></button><div class="category-controlled" oreui-color="dark" oreui-type="general"><div class="tweaks">'
subcategory_start = '<div class="subcategory"><div oreui-type="button" class="category-label" oreui-color="dark" onclick="OreUI.toggleActive(this);toggleCategory(this);">topic_name</div><button class="category-label-selectall sub" onclick="selectAll(this)" data-allpacks="<all_packs>" data-category="<topic_name>"><img src="images/select-all-button/chiseled_bookshelf_empty.png" class="category-label-selectall-img"><div class="category-label-selectall-hovertext">Select All</div></button><div class="category-controlled" oreui-color="dark" oreui-type="general"><div class="subcattweaks">'
pack_start = '<div class="tweak" onclick="toggleSelection(this);" data-category="topic_name" data-name="pack_id" data-index="pack_index" oreui-type="button" oreui-color="dark" oreui-active-color="green">'
html_comp = '<div class="comp-hover-text" oreui-color="dark" oreui-type="general">Incompatible with: <incompatible></div>'
pack_mid = '<div class="tweak-info"><input type="checkbox" name="tweak"><img src="../relloctopackicon" style="width:82px; height:82px;" alt="pack_name"><br><label id="tweak" class="tweak-title">pack_name</label><div class="tweak-description">pack_description</div></div>'
html_conf = '<div class="conf-hover-text" oreui-color="dark" oreui-type="general">Conflicts with: <conflicts></div>'
pack_end = '</div>'
category_end = '</div></div></div>'
cat_end_w_subcat_no_end = '</div><div class="subcat<index>">'

html = ''
stats = [0, 0]
incomplete_packs = {}
comp_stats = [0, 0]
comps = {}
conflicts = {}
pkicstats = [0, 0]
subcats = 0
ignore = False
subcat_list = []
incomplete_pkics = {}
packs = -1
name_to_json = {}
priority = {}


with open(f"{cdir()}/jsons/others/pack_order_list.txt","r") as pol:
    cat_list = pol.read().split("\n")
    if cat_list[-1] == "":
        cat_list.pop()

parser = argparse.ArgumentParser(description='Run a massive script that updates Packs to-do, Icons to-do, Compatibilities to-do and the HTML')
parser.add_argument('--format', '-f', action='store_true', help='Include flag to format files')
parser.add_argument('--only-update-html', '-ouh', action='store_true', help='Only update the HTML')
parser.add_argument('--only-update-jsons', '-ouj', action='store_true', help='Only update the JSONs')
parser.add_argument('--build', '-b', help='Builds stuff')
parser.add_argument('--log-error', '-el', action='store_true', help='Prints out errors')
parser.add_argument('--no-stash', '-ns', action='store_true', help='Does not stash changes')
args = parser.parse_args()
if args.build == None:
    args.build = ""

if not args.no_stash:
    clrprint("Stashing changes...", clr="yellow")
    os.system('git stash --quiet --include-untracked --message "Stashed changes before pre-commit"')
    os.system('git stash apply --quiet')
    clrprint("Stashed changes!", clr="green")

# Counts Packs and Compatibilities
if not "site" in args.build or (args.build and (args.only_update_html or args.only_update_jsons or args.format)):
    clrprint("Going through Packs...", clr="yellow")
    id_to_name = {}
    for j in cat_list:
        origj = j
        if not ignore:
            file = load_json(f"{cdir()}/jsons/packs/{j}")
            name_to_json[file["topic"]] = j
            # Adds the categories automatically
            incomplete_pkics[file["topic"]] = []
            incomplete_packs[file["topic"]] = []
            html += category_start.replace("topic_name", file["topic"])
            current_category_packs = { "raw": [] }
            # Runs through the packs
            for i in range(len(file["packs"])):
                # Build if neccessary
                if "pack" in args.build:
                    try:
                        clrprint("Building", file["packs"][i]["pack_id"], "with", file["packs"][i]["build"]["with"], clr="y,b,y,b")
                        os.chdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/')
                        os.system(f'{file["packs"][i]["build"]["with"]} {file["packs"][i]["build"]["script"]}')
                    except KeyError:
                        pass # no need to build
                    # Updates Incomplete Packs
                try:
                    if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/files') == []:
                        # Adds the packid to the topic list
                        incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                        stats[1] += 1
                        if args.log_error:
                            clrprint("[packs]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,w,y")
                    else:
                        # When the packid directory has stuff inside
                        stats[0] += 1
                except FileNotFoundError:
                    # If the packs don't even exist
                    stats[1] += 1
                    if args.log_error:
                        clrprint("[packs]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,w,y")

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
                except FileNotFoundError:
                    try:
                        if os.path.exists(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                            pkicstats[0] += 1
                        else:
                            # When pack icon doesn't even exist
                            incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                            pkicstats[1] += 1
                            if args.log_error:
                                clrprint("[packs]", "[icon]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,b,w,y")
                    except KeyError:
                            incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                            pkicstats[1] += 1
                            if args.log_error:
                                clrprint("[packs]", "[icon]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,b,w,y")

                # Adds Pack Conflicts
                conflicts[file["packs"][i]["pack_id"]] = []
                try:
                    for conf in range(len(file["packs"][i]["conflict"])):
                        conflicts[file["packs"][i]["pack_id"]].append(file["packs"][i]["conflict"][conf])
                except KeyError:
                    pass # If it is empty, it just skips
                if conflicts[file["packs"][i]["pack_id"]] == []:
                    del conflicts[file["packs"][i]["pack_id"]]

                # Add priority map
                try:
                    priority[file["packs"][i]["pack_id"]] = file["packs"][i]["priority"]
                except KeyError:
                    priority[file["packs"][i]["pack_id"]] = 0

                # Adds respective HTML
                confs = ""
                if file["packs"][i]["pack_id"] not in incomplete_packs[file["topic"]]:
                    packs += 1
                    to_add_pack = pack_start
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
                        if file["packs"][i]["message"][0] == "warn":
                            desc += f'<p class="desc-warn">{file["packs"][i]["message"][1]}</p>'
                        elif file["packs"][i]["message"][0] == "error":
                            desc += f'<p class="desc-error">{file["packs"][i]["message"][1]}</p>'
                        elif file["packs"][i]["message"][0] == "info":
                            desc += f'<p class="desc-info">{file["packs"][i]["message"][1]}</p>'
                    except KeyError:
                        pass
                    to_add_pack = to_add_pack.replace("pack_description", desc)
                    to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
                    try:
                        if os.path.exists(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                            # Because I can't make the html use a missing texture thing, so
                            # it only replaces when it exists
                            to_add_pack = to_add_pack.replace("png", file["packs"][i]["icon"])
                    except KeyError:
                        pass
                    html += to_add_pack
                    current_category_packs["raw"].append(file["packs"][i]["pack_id"])
                    if not args.only_update_html:
                        listjson = []
                        for root, _, files in os.walk(f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}"):
                            for lsfile in files:
                                filepath = os.path.relpath(os.path.join(root, lsfile),f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}")
                                if len(filepath.split(os.path.sep)) == 1:
                                    continue
                                else:
                                    listjson.append("/".join(filepath.split(os.path.sep)[1:]))
                                listjson.sort()
                        dump_json(f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/list.json", listjson)
                    id_to_name[file["packs"][i]["pack_id"]] = file["packs"][i]["pack_name"]
        html = html.replace("<all_packs>", LZString.compressToEncodedURIComponent(dumps(current_category_packs)))
        # handle subcategories
        try:
            indexoforigj = cat_list.index(origj)
            if "\t" in cat_list[indexoforigj + 1] or "    " in cat_list[indexoforigj + 1]:
                html += cat_end_w_subcat_no_end
                try:
                    if not ("\t" in cat_list[indexoforigj + 2] or "    " in cat_list[indexoforigj + 2]):
                        html += category_end
                except IndexError:
                    pass
                html = html.replace("<index>", str(subcats))
                subcats += 1
                ignore = True
                if "\t" in cat_list[indexoforigj + 1]:
                    subcat_list.append(cat_list[indexoforigj + 1][1:])
                elif "    " in cat_list[indexoforigj + 1]:
                    subcat_list.append(cat_list[indexoforigj + 1][4:])
            elif not ignore:
                html += category_end
            else:
                ignore = False
        except IndexError:
            html += category_end
    
    #"""
    # Seperate loop for subcategories (I'm inefficient)
    for j in range(len(subcat_list)):
        pack_html = ""
        k = subcat_list[j]
        file = load_json(f"{cdir()}/jsons/packs/{k}")
        name_to_json[file["topic"]] = k
        # Adds the categories automatically
        incomplete_pkics[file["topic"]] = []
        incomplete_packs[file["topic"]] = []
        pack_html += subcategory_start.replace("<topic_name>", file["topic"]).replace("topic_name", f'{file["subcategory_of"]} > <b>{file["topic"]}</b>')
        current_category_packs = { "raw": [] }
        # Runs through the packs
        for i in range(len(file["packs"])):
            # Build if neccessary
            if "pack" in args.build:
                try:
                    clrprint("Building", file["packs"][i]["pack_id"], "with", file["packs"][i]["build"]["with"], clr="y,b,y,b")
                    os.chdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/')
                    os.system(f'{file["packs"][i]["build"]["with"]} {file["packs"][i]["build"]["script"]}')
                except KeyError:
                    pass # no need to build
                # Updates Incomplete Packs
            try:
                if os.listdir(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/files') == []:
                    # Adds the packid to the topic list
                    incomplete_packs[file["topic"]].append(file["packs"][i]["pack_id"])
                    stats[1] += 1
                    if args.log_error:
                        clrprint("[packs]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,w,y")
                else:
                    # When the packid directory has stuff inside
                    stats[0] += 1
            except FileNotFoundError:
                # If the packs don't even exist
                stats[1] += 1
                if args.log_error:
                    clrprint("[packs]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,w,y")

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
            except FileNotFoundError:
                try:
                    if os.path.exists(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                        pkicstats[0] += 1
                    else:
                        # When pack icon doesn't even exist
                        incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                        pkicstats[1] += 1
                        if args.log_error:
                            clrprint("[packs]", "[icon]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,b,w,y")
                except KeyError:
                        incomplete_pkics[file["topic"]].append(file["packs"][i]["pack_id"])
                        pkicstats[1] += 1
                        if args.log_error:
                            clrprint("[packs]", "[icon]", "Incomplete Pack:", file["packs"][i]["pack_id"], clr="r,b,w,y")

            # Adds Pack Conflicts
            conflicts[file["packs"][i]["pack_id"]] = []
            try:
                for conf in range(len(file["packs"][i]["conflict"])):
                    conflicts[file["packs"][i]["pack_id"]].append(file["packs"][i]["conflict"][conf])
            except KeyError:
                pass # If it is empty, it just skips
            if conflicts[file["packs"][i]["pack_id"]] == []:
                del conflicts[file["packs"][i]["pack_id"]]

            # Add priority map
            try:
                priority[file["packs"][i]["pack_id"]] = file["packs"][i]["priority"]
            except KeyError:
                priority[file["packs"][i]["pack_id"]] = 0

            # Adds respective HTML
            confs = ""
            if file["packs"][i]["pack_id"] not in incomplete_packs[file["topic"]]:
                packs += 1
                to_add_pack = pack_start
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
                    if file["packs"][i]["message"][0] == "warn":
                        desc += f'<p class="desc-warn">{file["packs"][i]["message"][1]}</p>'
                    elif file["packs"][i]["message"][0] == "error":
                        desc += f'<p class="desc-error">{file["packs"][i]["message"][1]}</p>'
                    elif file["packs"][i]["message"][0] == "info":
                        desc += f'<p class="desc-info">{file["packs"][i]["message"][1]}</p>'
                except KeyError:
                    pass
                to_add_pack = to_add_pack.replace("pack_description", desc)
                to_add_pack = to_add_pack.replace("relloctopackicon", f'packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.png')
                try:
                    if os.path.exists(f'{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                        # Because I can't make the html use a missing texture thing, so
                        # it only replaces when it exists
                        to_add_pack = to_add_pack.replace("png", file["packs"][i]["icon"])
                except KeyError:
                    pass
                pack_html += to_add_pack
                current_category_packs["raw"].append(file["packs"][i]["pack_id"])
                if not args.only_update_html:
                    listjson = []
                    for root, _, files in os.walk(f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}"):
                        for lsfile in files:
                            filepath = os.path.relpath(os.path.join(root, lsfile),f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}")
                            if len(filepath.split(os.path.sep)) == 1:
                                continue
                            else:
                                listjson.append("/".join(filepath.split(os.path.sep)[1:]))
                            listjson.sort()
                    dump_json(f"{cdir()}/packs/{file["topic"].lower()}/{file["packs"][i]["pack_id"]}/list.json", listjson)
                id_to_name[file["packs"][i]["pack_id"]] = file["packs"][i]["pack_name"]
        pack_html += category_end
        html = html.replace(f'<div class="subcat{j}"></div>',pack_html)
        html = html.replace("<all_packs>", LZString.compressToEncodedURIComponent(dumps(current_category_packs)))
    #"""
    # compatibilities
    compatibilities = load_json(f"{cdir()}/jsons/packs/compatibilities.json")
    for ways in range(compatibilities["maxway"],1,-1):
        for location in compatibilities[f"{ways}way"]["locations"]:
            listjson = []
            try:
                for root, _, files in os.walk(f"{cdir()}/packs/{location}/files"):
                    for lsfile in files:
                        filepath = os.path.relpath(os.path.join(root, lsfile),f"{cdir()}/packs/{location}")
                        if len(filepath.split(os.path.sep)) == 1:
                            continue
                        else:
                            listjson.append("/".join(filepath.split(os.path.sep)[1:]))
                        listjson.sort()
                if len(listjson) == 0:
                    raise FileNotFoundError
                dump_json(f"{cdir()}/packs/{location}/list.json", listjson)
                comp_stats[0] += 1
            except FileNotFoundError:
                if args.log_error:
                    clrprint("[compatibilities]", "Incomplete Compatibility:", location, clr="r,w,y")
                comp_stats[1] += 1
                try:
                    comps[f"{ways}way"].append(location)
                except KeyError:
                    comps[f"{ways}way"] = [location]

    clrprint("Did a lot of stuff", clr="green")

    # HTML formatting
    with open(f"{cdir()}/webUI/index.html.template", "r") as html_file:
        real_html = html_file.read()
    html = real_html.replace("<!--Packs-->",html)
    with open(f"{cdir()}/credits.md", "r") as credits:
        html = html.replace("<!--credits-->",str(markdown(credits.read())))
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify()
    html = html.replace("<br/>", "<br>")
    # Update files
    clrprint("Updating files...", clr="yellow")
    if not args.only_update_html:
        dump_json(f"{cdir()}/jsons/others/incomplete_packs.json", incomplete_packs)
        dump_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json", comps)
        dump_json(f"{cdir()}/jsons/others/incomplete_pack_icons.json", incomplete_pkics)
        dump_json(f"{cdir()}/jsons/map/name_to_json.json", name_to_json)
        dump_json(f"{cdir()}/jsons/map/id_to_name.json", id_to_name)
        dump_json(f"{cdir()}/jsons/map/priority.json", priority)
    if not args.only_update_jsons:
        with open(f"{cdir()}/webUI/index.html", "w") as html_file:
            html_file.write(html)
    if not (args.only_update_html or args.only_update_jsons):
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
            new_comp_url = f"{comp_match.group(1)}{comp_stats[0]}%2F{comp_stats[0] + comp_stats[1]}{comp_match.group(3)}"
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
        try:
            os.system('npx prettier --write "**/*.{js,ts,css,json}" --log-level silent')
        except KeyboardInterrupt:
            clrprint("You are a bit impatient...", clr="red")
        clrprint("Files are Prettier!", clr="green")
    elif not args.only_update_html:
        clrprint("Remember to format the files!", clr="y")

if "site" in args.build:
    clrprint("Make sure you built the HTML!", clr="y")
    try:
        shutil.rmtree(f"{cdir()}/build")
    except FileNotFoundError:
        pass
    try:
        shutil.copytree(f"{cdir()}/webUI", f"{cdir()}/build")
        os.remove(f"{cdir()}/build/index.html.template")
        with open(f"{cdir()}/build/index.html", "r") as file:
            content = file.read()
        with open(f"{cdir()}/build/index.html", "w") as file:
            file.write(content.replace("../", "https://raw.githubusercontent.com/BEComTweaks/resource-packs/main/"))
        clrprint("Build success!", clr="g")
    except Exception as e:
        clrprint("Build failed!", clr="r")
        clrprint(e, clr="y")
