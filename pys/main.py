import os
import shutil

if str(os.getcwd()).endswith("system32"):
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
else:
    doubleclicked = False
try:
    from custom_functions import *
except:
    print(f"main.py is at {os.path.realpath(__file__)} but it is executing at {os.getcwd}!")
    print("You are likely using a non-Windows device!")
    print("Send the path where the code is executing at to https://discord.com/channels/567364180857061437/1053415910343462923/threads/1231970599799226388 along with your current device!")
    exit(1)

check("clrprint")
from clrprint import clrprint

check("ujson")
from ujson import *

# Updates Terminal Size for flexible list
# placements
def update_size():
    global clm, lins, min_clm, clms, pclms
    clm = shutil.get_terminal_size().columns
    lins = shutil.get_terminal_size().lines
    min_clm = 42
    clms = clm // min_clm
    pclms = -1
update_size()

# Counts the number of columns and adds a
# new line if it exceeds the columns available
def clmthing():
    global pclms, clms
    pclms += 1
    if pclms == clms:
        pclms = 0
        print("\n")


# Menu Up and Down stuff
down = {
    "main_menu": ["pack_select", "selected_packs"],
    "pack_select": ["select_pack"]
}
up = {
    "select_pack": "pack_select",
    "pack_select": "main_menu",
    "selected_packs": "main_menu"
}


# Command validation for functions
def val_command(menu, command):
    if type(command) == list:
        if command[0] == "back":
            # Heading back to packs if user doesn't
            # select/unselect pack
            return ["pack_select", command[1]]
        elif menu == "pack_select":
            # Heading into pack_select if user wants
            # to select/unselect a pack
            return ["select_pack", command[0], command[1], command[2]]
        elif menu == "select_pack" and command[0] == "select":
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            topic = packjson["topic"]

            # Adds pack to selected packs
            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")
            selpackjson[topic].append("".join(command[2].split()))
            selpackjson[topic].sort()
            selpackjson["raw"].append("".join(command[2].split()))
            selpackjson["raw"].sort()

            # Dumps dictionary
            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)

            # It shows up for like 10ms lol
            clrprint(f"{command[2]} has been added to Selected Packs!", clr="green")

            return [up[menu], f'{"".join(topic.replace(" ", "_").lower().split())}.json']
        elif menu == "select_pack" and command[0] == "unselect":
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")
            topic = packjson["topic"]

            # Checks each item in the list for the pack
            # to be unselected
            for i in range(len(selpackjson[topic])):
                if selpackjson[topic][i] == "".join(command[2].split()):
                    selpackjson[topic].pop(i)
                    break
            for i in range(len(selpackjson["raw"])):
                if selpackjson["raw"][i] == "".join(command[2].split()):
                    selpackjson["raw"].pop(i)
                    break

            # Dumps Dictionary
            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)

            # It shows up for like 10ms
            clrprint(f"{command[2]} has been removed from Selected Packs!", clr="green")

            return [up[menu], f'{"".join(topic.replace(" ", "_").lower().split())}.json']
    elif type(command) == str:
        if command == "back":
            # Goes up the 'directory'
            return [up[menu]]
        elif menu == "main_menu" and command not in ["exit", "show selected packs"]:
            # Enters Pack Selection page
            return ["pack_select", command]
        elif menu == "main_menu" and command == "show selected packs":
            # Enters Selected Packs page
            return ["selected_packs"]
        elif command == "exit":
            # Exits program
            clrprint("Exited program.", clr="yellow")
            exit(0)
        else:
            raise ValueError(f"{command} is not a valid command!")


# Menu Screen showing categories
def main_menu():
    choice = None
    while choice is None:
        # Terminal Init
        update_size()
        clear()
        # Navigation Bar
        clrprint("Main Menu", clr="default")

        clrprint("\nCategories", clr="purple")
        menu_commands = [""]

        # Sort the list of files before iterating over them
        pack_files = sorted(os.listdir(f"{cdir()}/jsons/packs"))
        for i, filename in enumerate(pack_files):
            clmthing()
            loadpackjson = load_json(f'{cdir()}/jsons/packs/{filename}')
            print(f'{i + 1}. {loadpackjson["topic"]}', end="")
            print(" " * (min_clm - len(f'{i + 1}. {loadpackjson["topic"]}')), end="")
            menu_commands.append(filename.lower())
        clrprint("\n\nOthers", clr="purple")

        print(f"{len(pack_files) + 1}. Show Selected Packs", end="")
        print(" " * (min_clm - 23), end="")
        menu_commands.append("show selected packs")
        clmthing()

        print(f"{len(pack_files) + 2}. Exit Program")
        menu_commands.append("exit")

        choice = input("\nEnter your choice.\n").lower()
        progged = prog_search(choice, menu_commands)
        # Validates the input/choice
        if choice in ["back", "exit"]:
            pass
        elif choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
        if choice == "":
            choice = None
    return choice


def pack_select(topic):
    choice = None
    while choice is None:
        # Terminal Init
        update_size()
        clear()
        # Loading JSON files
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")
        incpacks = load_json(f"{cdir()}/jsons/others/incomplete_packs.json")
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")
        # Navigation Bar
        clrprint(f'Main Menu -> {packs["topic"]}\n', clr="default")
        # Notices
        clrprint("Red", "means this pack has not been finished and cannot be selected", clr="r,y")
        clrprint("Green", "means this pack has been selected", clr="g,y")
        clrprint("Blue", "means this pack conflicts with another pack and cannot be selected\n", clr="b,y")

        clrprint("Packs", clr="purple")
        menu_commands = [""]

        for i in range(len(packs["packs"])):
            clmthing()
            if packs["packs"][i]["pack_id"] in incpacks[packs["topic"]]:
                # Pack is not finished
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="red")
                menu_commands.append("")
            elif packs["packs"][i]["pack_id"] in selpacks[packs["topic"]]:
                # Pack is already selected
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="green")
                menu_commands.append(packs["packs"][i]["pack_name"])
            else:
                conflict = False
                for c in packs["packs"][i]["conflict"]:
                    if c in selpacks["raw"]:
                        # Pack conflicts with another pack
                        clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="blue")
                        conflict = True
                        break
                if not conflict:
                    # Pack is finished, not selected and has no conflicts
                    clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="white")
                menu_commands.append(packs["packs"][i]["pack_name"])
            print(" " * (min_clm - len(f'{i + 1}. {packs["packs"][i]["pack_name"]}')), end="")

        clrprint("\n\nOthers", clr="purple")

        print(f'{i + 2}. Go Back (back)', end="")
        print(" " * (min_clm - len(f'{i + 2}. Go Back (back)')), end="")
        menu_commands.append("back")
        clmthing()

        print(f'{i + 3}. Exit Program')
        menu_commands.append("exit")

        choice = input("Enter your choice.\n")
        progged = prog_search(choice, menu_commands)
        # Validates input/choice
        if choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif choice in ["back", "exit"]:
            pass
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
        if choice == "":
            choice = None
    if choice.lower() in ["exit", "back"]:
        # Returns only choice
        return choice
    else:
        # Returns category, pack name and index of pack_name
        # in JSON file
        return [topic, choice, menu_commands.index(choice)]


def selected_packs():
    choice = None
    while choice is None:
        # Terminal Init
        update_size()
        clear()
        # Loading JSON File
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")
        # Navigation Bar
        clrprint("Main Menu -> Selected Packs\n", clr="default")
        menu_commands = [""]

        hasitem = False
        for key, value in selpacks.items():
            # Passes through the if statement only
            # if the list has something inside, and
            # its name isn't "raw"
            if value != [] and key != "raw":
                hasitem = True
                sortedsel = sorted(value)
                clrprint(key, clr="green")
                for item in sortedsel:
                    print(f"\t- {item}")
        # Just a small easter egg
        if not hasitem:
            clrprint("What is Bedrock Tweaks without any tweaks selected? ._.\nMaybe head back and select some packs!", clr="yellow")

        clrprint("\nOptions", clr="purple")

        print(f"1. Go Back (back)")
        menu_commands.append("back")

        print("\n2. Exit Program (exit)")
        menu_commands.append("exit")

        choice = input("Enter your choice.\n")
        # Validates input/choice
        # There is like only two choices lol
        # not sure what im validating
        if choice in ["back", "exit"]:
            pass
        elif choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        else:
            choice = None
        if choice == "":
            choice = None
    return choice


def select_pack(topic, pack, index):
    choice = None
    while choice == None:
        # Terminal Init
        update_size()
        clear()
        # Loading JSON Files
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")
        # Navigation Bar
        clrprint(f'Main Menu -> {packs["topic"]} -> {pack}\n', clr="default")
        # Pack Description
        print(packs["packs"][int(index) - 1]["pack_description"])

        menu_commands = [""]
        conflict = False
        for i in packs["packs"][index - 1]["conflict"]:
            if i in selpacks["raw"]:
                # When the current pack has a selected conflict
                clrprint(f"{pack} has a conflict with {i}!", clr="b")
                clrprint(f"Unselect {i} to select {pack}!", clr="b")
                conflict = True
                break
        uns = "S"
        if "".join(pack.split()) in selpacks[packs["topic"]]:
            # When the current pack is already selected
            clrprint(f"{pack} has already been selected!", clr="green")
            uns = "Uns"
        if uns == "Uns" and conflict:
            # Another meme, taking inspiration from
            # `from __future__ import braces`
            clrprint(f"Both {pack} and {i} are selected...", clr="red")
            raise SyntaxError("not a chance")
        if conflict:
            # Prevents selection of pack
            clrprint(f"\n1. {uns}elect {pack} ({uns.lower()}elect)", clr="red")
            menu_commands.append("")
        else:
            # (un)selects the pack
            print(f"\n1. {uns}elect {pack} ({uns.lower()}elect)")
            menu_commands.append(f"{uns.lower()}elect")

        print("\n2. Go Back (back)")
        menu_commands.append("back")

        print(f"\n3. Exit Program (exit)")
        menu_commands.append("exit")

        choice = input("\nEnter your choice.\n").lower()
        progged = prog_search(choice, menu_commands)
        # Validates input/choice
        # There is like only three choices lol
        if choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif choice in ["back", "exit"]:
            pass
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
        if choice == "":
            choice = None
    if choice == "back":
        return ["back", f'{topic.replace(" ", "_").lower()}']
    elif choice == "exit":
        return "exit"
    else:
        return [choice, f'{topic.replace(" ", "_").lower()}', pack]


command = ["main_menu"]
# Main Loop
try:
    while True:
        if command[0] == "main_menu":
            # Main Menu
            command = main_menu()
            command = val_command("main_menu", command)
        elif command[0] == "pack_select":
            # Pack Selection
            command = pack_select(command[1])
            command = val_command("pack_select", command)
        elif command[0] == "select_pack":
            # More info on pack and if to
            # (un)select or not
            command = select_pack(command[1], command[2], command[3])
            command = val_command("select_pack", command)
        elif command[0] == "selected_packs":
            # Show Selected Packs
            command = selected_packs()
            command = val_command("selected_packs", command)
        # Shows up for like 10ms, to show my suffering
        clrprint("If you can see this, I suffered about 11 hours in total for this", clr="purple")
        clrprint("Please send help by putting a star on the repo!", clr="purple")
except KeyboardInterrupt:
    # I don't like seeing massive errors when
    # I stop the program with Ctrl+C, so neat
    # exit instead of spam
    val_command("keyboard_interrupt", "exit")