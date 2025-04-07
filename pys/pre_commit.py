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
from custom_functions import console
from markdown import markdown
from bs4 import BeautifulSoup
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
comp_stats = [0, 0]
pkicstats = [0, 0]
subcats = 0
ignore = False
subcat_list = []
packs = -1
name_to_json = {}
priority = {}


with open(f"{cdir()}/jsons/pack_order_list.txt","r") as pol:
    cat_list = pol.read().split("\n")
    if cat_list[-1] == "":
        cat_list.pop()

parser = argparse.ArgumentParser(description='Run a massive script that updates Packs to-do, Icons to-do, Compatibilities to-do and the HTML')
parser.add_argument('--format', '-f', action='store_true', help='Include flag to format files')
parser.add_argument('--only-update-html', '-html', action='store_true', help='Only update the HTML')
parser.add_argument('--only-update-jsons', '-json', action='store_true', help='Only update the JSONs')
parser.add_argument('--build', '-b', help='Builds stuff based on specification. Can be "pack", "site", "both" or "server"')
# parser.add_argument('--update-theme', '-u', action='store_true', help='Pulls the theme used for the website from the resource-packs repository')
parser.add_argument('--no-stash', '-ns', action='store_true', help='Does not stash changes')
parser.add_argument('--quiet', '-q', action='store_true', help='Quieten outputs of run statements (the commands will still be shown)')
parser.add_argument('--dev', '-d', action='store_true', help='Show time and lines of each print statement')
parser.add_argument('--no-spinner', action='store_true', help='Disables the spinner from rich')
args = parser.parse_args()

if args.build == "both":
    args.build = "packsite"
elif args.build == "server":
    args.build = "packsite server"
elif args.build == None:
    args.build = ""

if args.dev:
    print = console.log
else:
    print = console.print

sendToCF(args)

if args.no_spinner:
    spinner = emptySpinner
else:
    spinner = console.status

if not args.no_stash:
    print("[bold yellow]Stashing changes...")
    run('git stash --include-untracked --message "Stashed changes before pre-commit"', quiet=True)
    run('git stash apply', quiet=True)
    print(f"[green]Stashed changes!")

# Counts Packs and Compatibilities
if "site" not in args.build or ("site" in args.build and (args.only_update_html or args.only_update_jsons or args.format or "pack" in args.build)):
    print(f"[yellow]Going through packs...")
    id_to_name = {}
    for j in cat_list:
        origj = j
        if not ignore:
            file = load_json(f"{cdir()}/jsons/packs/{j}")
            name_to_json[file["topic"]] = j
            try:
                category_loc = f'{cdir()}/packs/{file["location"]}'
            except KeyError:
                category_loc = f'{cdir()}/packs/{file["topic"].lower()}'
            # Adds the categories automatically
            html += category_start.replace("topic_name", file["topic"])
            current_category_packs = { "raw": [] }
            # Runs through the packs
            for i in range(len(file["packs"])):
                # Build first
                if "regolith" in file["packs"][i] and "pack" in args.build:
                    print(f"-> [cyan]Building {file['packs'][i]['pack_id']}")
                    os.chdir(f'{category_loc}/{file["packs"][i]["pack_id"]}')
                    print(f"--> [bright_yellow]Checking the config file...")
                    regolith_config = load_json(f'{category_loc}/{file["packs"][i]["pack_id"]}/config.json')
                    if regolith_config["regolith"]["profiles"]["build"]["export"]["readOnly"] == True:
                        regolith_config["regolith"]["profiles"]["build"]["export"]["readOnly"] = False
                    dump_json(f'{category_loc}/{file["packs"][i]["pack_id"]}/config.json', regolith_config)
                    # install filters
                    run("regolith install-all", quiet=True)
                    # check for previous builds
                    if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/files'):
                        print(f"--> [yellow]Purging previous build...")
                        shutil.rmtree(f'{category_loc}/{file["packs"][i]["pack_id"]}/files', onerror=remove_readonly)
                    if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/build'):
                        print(f"--> [yellow]Purging previous incomplete build...")
                        shutil.rmtree(f'{category_loc}/{file["packs"][i]["pack_id"]}/build', onerror=remove_readonly)
                    run(f"regolith run build {"--experiments size_time_check" if "server" in args.build else ""}", quiet=True)
                    # Check for .gitkeep and fix folder naming
                    if os.path.exists("build"):
                        print(f"--> [yellow]Fixing build folder...")
                        build_dir = f"{category_loc}/{file["packs"][i]["pack_id"]}"
                        try:
                            os.mkdir(f"{build_dir}/files")
                        except FileExistsError:
                            print(f"--> [yellow]Why does {os.path.relpath(build_dir, cdir())}/files exist?")
                        for folder in os.listdir("build"):
                            if folder.endswith("bp"):
                                if ".gitkeep" in os.listdir(f"build/{folder}"):
                                    shutil.rmtree(f"build/{folder}", onerror=remove_readonly)
                                else:
                                    os.rename(f"{build_dir}/build/{folder}", f"{build_dir}/files/bp")
                            elif folder.endswith("rp"):
                                if ".gitkeep" in os.listdir(f"build/{folder}"):
                                    shutil.rmtree(f"build/{folder}", onerror=remove_readonly)
                                else:
                                    os.rename(f"{build_dir}/build/{folder}", f"{build_dir}/files/rp")
                            else:
                                print(f"[red]Unknown folder found in {os.path.relpath(os.getcwd(), cdir())}/build/: [yellow]{folder}")
                        # now move to proper folder
                    os.chdir(cdir())
                # Updates Incomplete Packs
                pack_exists = False
                try:
                    if "regolith" in file["packs"][i] or os.listdir(f'{category_loc}/{file["packs"][i]["pack_id"]}/files') != []:
                        # When the packid directory has stuff inside or is regolith
                        stats[0] += 1
                        pack_exists = True
                    else:
                        # screw it go to filenotfounderror
                        raise FileNotFoundError
                except FileNotFoundError:
                    stats[1] += 1
                    print(f"[red]Incomplete Pack: [yellow]{file['packs'][i]['pack_id']}")

                # Updates Incomplete pack_icon.png
                try:
                    if not pack_exists:
                        pass
                    elif os.path.getsize(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.png') == os.path.getsize(f'{cdir()}/pack_icons/missing_texture.png'):
                        raise FileNotFoundError
                    else:
                        # When pack icon is complete
                        pkicstats[0] += 1
                except FileNotFoundError:
                    try:
                        if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                            pkicstats[0] += 1
                        else:
                            # When pack icon doesn't even exist
                            raise KeyError # who cares
                    except KeyError:
                            pkicstats[1] += 1
                            print(f"[red]Incomplete Pack Icon: [yellow]{file['packs'][i]['pack_id']}")

                # Adds Pack Conflicts
                conflicts = []
                try:
                    for conf in range(len(file["packs"][i]["conflict"])):
                        conflicts.append(file["packs"][i]["conflict"][conf])
                except KeyError:
                    pass # If it is empty, it just skips

                # Add priority map
                try:
                    priority[file["packs"][i]["pack_id"]] = file["packs"][i]["priority"]
                except KeyError:
                    priority[file["packs"][i]["pack_id"]] = 0

                # Adds respective HTML
                confs = ""
                if pack_exists:
                    packs += 1
                    to_add_pack = pack_start
                    to_add_pack += pack_mid
                    if conflicts != []:
                        for c in conflicts:
                            confs += f"{c}, "
                        to_add_pack += html_conf.replace('<conflicts>',confs[:-2])
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
                    to_add_pack = to_add_pack.replace("relloctopackicon", f"{os.path.relpath(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.png', start=cdir())}".replace("\\","/"))
                    try:
                        if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                            # Because I can't make the html use a missing texture thing, so
                            # it only replaces when it exists
                            to_add_pack = to_add_pack.replace("png", file["packs"][i]["icon"])
                    except KeyError:
                        pass
                    html += to_add_pack
                    current_category_packs["raw"].append(file["packs"][i]["pack_id"])
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
    # Seperate loop for subcategories (I'm inefficient)
    for j in range(len(subcat_list)):
        pack_html = ""
        k = subcat_list[j]
        file = load_json(f"{cdir()}/jsons/packs/{k}")
        name_to_json[file["topic"]] = k
        try:
            category_loc = f'{cdir()}/packs/{file["location"]}'
        except KeyError:
            category_loc = f'{cdir()}/packs/{file["topic"].lower()}'
        # Adds the categories automatically
        pack_html += subcategory_start.replace("<topic_name>",file["topic"]).replace("topic_name", f'{file["subcategory_of"]} > <b>{file["topic"]}</b>')
        current_category_packs = { "raw": [] }
        # Runs through the packs
        for i in range(len(file["packs"])):
            if "regolith" in file["packs"][i] and "pack" in args.build:
                print(f"-> [cyan]Building {file['packs'][i]['pack_id']}")
                os.chdir(f'{category_loc}/{file["packs"][i]["pack_id"]}')
                print(f"--> [bright_yellow]Checking the config file...")
                regolith_config = load_json(f'{category_loc}/{file["packs"][i]["pack_id"]}/config.json')
                if regolith_config["regolith"]["profiles"]["build"]["export"]["readOnly"] == True:
                    regolith_config["regolith"]["profiles"]["build"]["export"]["readOnly"] = False
                dump_json(f'{category_loc}/{file["packs"][i]["pack_id"]}/config.json', regolith_config)
                # install filters
                run("regolith install-all", quiet=True)
                # check for previous builds
                if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/files'):
                    print(f"--> [yellow]Purging previous build...")
                    shutil.rmtree(f'{category_loc}/{file["packs"][i]["pack_id"]}/files', onerror=remove_readonly)
                if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/build'):
                    print(f"--> [yellow]Purging previous incomplete build...")
                    shutil.rmtree(f'{category_loc}/{file["packs"][i]["pack_id"]}/build', onerror=remove_readonly)
                run(f"regolith run build {"--experiments size_time_check" if "server" in args.build else ""}", quiet=True)
                # Check for .gitkeep and fix folder naming
                if os.path.exists("build"):
                    print(f"--> [yellow]Fixing build folder...")
                    build_dir = f"{category_loc}/{file["packs"][i]["pack_id"]}"
                    for folder in os.listdir("build"):
                        if folder.endswith("bp"):
                            if ".gitkeep" in os.listdir(f"build/{folder}"):
                                shutil.rmtree(f"build/{folder}", onerror=remove_readonly)
                            else:
                                os.rename(f"{build_dir}/build/{folder}", f"{build_dir}/files/bp")
                        elif folder.endswith("rp"):
                            if ".gitkeep" in os.listdir(f"build/{folder}"):
                                shutil.rmtree(f"build/{folder}", onerror=remove_readonly)
                            else:
                                os.rename(f"{build_dir}/build/{folder}", f"{build_dir}/files/rp")
                        else:
                            print(f"[red]Unknown folder found in {os.path.relpath(os.getcwd(), cdir())}/build/: [yellow]{folder}")
                    # now move to proper folder
                os.chdir(cdir())
            # Updates Incomplete Packs
            pack_exists = False
            try:
                if "regolith" in file["packs"][i] or os.listdir(f'{category_loc}/{file["packs"][i]["pack_id"]}/files') != []:
                    # When the packid directory has stuff inside or is regolith
                    stats[0] += 1
                    pack_exists = True
                else:
                    # screw it go to filenotfounderror
                    raise FileNotFoundError
            except FileNotFoundError:
                stats[1] += 1
                print(f"[red]Incomplete Pack: [yellow]{file['packs'][i]['pack_id']}")

            # Updates Incomplete pack_icon.png
            try:
                if not pack_exists:
                    pass
                elif os.path.getsize(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.png') == os.path.getsize(f'{cdir()}/pack_icons/missing_texture.png'):
                    # Adds packid to topic list
                    raise FileNotFoundError
                else:
                    # When pack icon is complete
                    pkicstats[0] += 1
            except FileNotFoundError:
                try:
                    if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                        pkicstats[0] += 1
                    else:
                        # When pack icon doesn't even exist
                        raise KeyError # who cares
                except KeyError:
                        pkicstats[1] += 1
                        print(f"[red]Incomplete Pack Icon: [yellow]{file['packs'][i]['pack_id']}")

            # Adds Pack Conflicts
            conflicts = []
            try:
                for conf in range(len(file["packs"][i]["conflict"])):
                    conflicts.append(file["packs"][i]["conflict"][conf])
            except KeyError:
                pass # If it is empty, it just skips

            # Add priority map
            try:
                priority[file["packs"][i]["pack_id"]] = file["packs"][i]["priority"]
            except KeyError:
                priority[file["packs"][i]["pack_id"]] = 0

            # Adds respective HTML
            confs = ""
            if pack_exists:
                packs += 1
                to_add_pack = pack_start
                to_add_pack += pack_mid
                if conflicts != []:
                    for c in conflicts:
                        confs += f"{c}, "
                    to_add_pack += html_conf.replace('<conflicts>',confs[:-2])
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
                to_add_pack = to_add_pack.replace("relloctopackicon", f"{os.path.relpath(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.png', start=cdir())}".replace("\\","/"))
                try:
                    if os.path.exists(f'{category_loc}/{file["packs"][i]["pack_id"]}/pack_icon.{file["packs"][i]["icon"]}'):
                        # Because I can't make the html use a missing texture thing, so
                        # it only replaces when it exists
                        to_add_pack = to_add_pack.replace("png", file["packs"][i]["icon"])
                except KeyError:
                    pass
                pack_html += to_add_pack
                current_category_packs["raw"].append(file["packs"][i]["pack_id"])
                id_to_name[file["packs"][i]["pack_id"]] = file["packs"][i]["pack_name"]
        pack_html += category_end
        html = html.replace(f'<div class="subcat{j}"></div>',pack_html)
        html = html.replace("<all_packs>", LZString.compressToEncodedURIComponent(dumps(current_category_packs)))
    # compatibilities
    compatibilities = load_json(f"{cdir()}/jsons/packs/compatibilities.json")
    compat_map = {}
    for ways in range(compatibilities["max_simultaneous"],1,-1):
        compat_map[f"{ways}way"] = []
        for compatibility in compatibilities[f"{ways}way"]:
            if len(compatibility["merge"]) != ways:
                print(f"[red]Incorrect Compatibility format: [yellow]{compatibility['location']}")
                comp_stats[1] += 1
            elif os.path.exists(f"{cdir()}/packs/{compatibility["location"]}"):
                comp_stats[0] += 1
                compat_map[f"{ways}way"].append(compatibility["merge"])
            else:
                print(f"[red]Incomplete Compatibility: [yellow]{compatibility['location']}")
                comp_stats[1] += 1
    print(f"[green]Done!")

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
    print(f"[yellow]Updating files...")
    if not args.only_update_html:
        try:
            os.mkdir(f"{cdir()}/jsons/map")
        except FileExistsError:
            pass
        dump_json(f"{cdir()}/jsons/map/name_to_json.json", name_to_json)
        dump_json(f"{cdir()}/jsons/map/id_to_name.json", id_to_name)
        dump_json(f"{cdir()}/jsons/map/priority.json", priority)
        dump_json(f"{cdir()}/jsons/map/compatibility.json", compat_map)
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
    print("[green]Updated!")
    # Used only for CTs and BPs because RP is main
    """
    try:
      if args.update_theme:
        print(f"[yellow]Updating theme.css...")
        import requests
        response = requests.get("https://becomtweaks.github.io/resource-packs/theme.css")
        if response.status_code == 200:
          with open(f"{cdir()}/webUI/theme.css","w") as theme:
            theme.write(response.text)
          print(f"[green]Updated theme.css!")
    except requests.exceptions.ConnectionError:
      print(f"[red]Get a working internet connection before rerunning with `-ut`/`--update-theme`")
    """
    print(f"[yellow]Updated files!")


    if args.format:
        print(f"[yellow]Making files Prettier\u2122")
        os.chdir(cdir())
        try:
            run('pnpm exec prettier --write "**/*.{js,ts,css,json}"', quiet=True)
        except KeyboardInterrupt:
            print(f"---> [red]You are a bit impatient...")
        print(f"[green]Files are Prettier!")
    elif not args.only_update_html:
        print(f"[yellow]Remember to format the files!")

if "site" in args.build:
    if not (args.only_update_html or args.only_update_jsons or args.format):
        print(f"[bright_cyan]Make sure you built the HTML!")
    try:
        shutil.rmtree(f"{cdir()}/build", onerror=remove_readonly)
    except FileNotFoundError:
        pass
    try:
        shutil.copytree(f"{cdir()}/webUI", f"{cdir()}/build")
        os.remove(f"{cdir()}/build/index.html.template")
        with open(f"{cdir()}/build/index.html", "r") as file:
            content = file.read()
        with open(f"{cdir()}/build/index.html", "w") as file:
            file.write(content.replace("../", "https://raw.githubusercontent.com/BEComTweaks/resource-packs/main/"))
        print(f"[bright_cyan]Website build success!")
    except Exception as e:
        print(f"---> [red]Website build failed!")
        print(e)
