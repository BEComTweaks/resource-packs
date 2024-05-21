import os
import shutil

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *

check("clrprint")
from clrprint import clrprint


# Updates Terminal Size for flexible list
# placements
def update_size():
    global clm, min_clm, clms, pclms
    clm = shutil.get_terminal_size().columns
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

quick_select = False


# Command validation for functions
def val_command(menu, command):
    global quick_select
    if type(command) is list:
        if command[0] == "back":
            # Heading back to packs if user doesn't
            # select/unselect pack
            return ["pack_select", command[1]]
        elif menu == "pack_select" and not quick_select:
            # Heading into pack_select if user wants
            # to select/unselect a pack
            return ["select_pack", command[0], command[1], command[2], command[3]]
        elif menu == "select_pack" and command[0] == "select":
            # Loads JSON
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            topic = packjson["topic"]

            # Adds pack to selected packs
            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")
            selpackjson[topic]["packs"].append(contract(command[2]))
            selpackjson[topic]["index"].append(command[3])
            selpackjson["raw"].append(contract(command[2]))

            # Dumps dictionary
            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)

            # It shows up for like 10ms lol
            clrprint(f"{command[2]} has been added to Selected Packs!", clr="green")

            return [up[menu], f'{contract(topic.replace(" ", "_").lower())}.json']
        elif menu == "select_pack" and command[0] == "unselect":
            # Loads JSONs
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")
            topic = packjson["topic"]

            # Checks each item in the list for the pack
            # to be unselected
            # yes i can change it to index, but im lazy
            for i in range(len(selpackjson[topic])):
                if selpackjson[topic]["packs"][i] == contract(command[2]):
                    selpackjson[topic]["packs"].pop(i)
                    selpackjson[topic]["index"].pop(i)
                    break
            for i in range(len(selpackjson["raw"])):
                if selpackjson["raw"][i] == contract(command[2]):
                    selpackjson["raw"].pop(i)
                    break

            # Dumps Dictionary
            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)

            # It shows up for like 10ms
            clrprint(f"{command[2]} has been removed from Selected Packs!", clr="green")

            return [up[menu], f'{contract(topic.replace(" ", "_").lower())}.json']
        else:
            raise ValueError(f"{command} is not a valid command format!")
    elif type(command) is str:
        if command == "back":
            # Goes up the 'directory'
            return [up[menu]]
        elif menu == "main_menu" and command.endswith("quick select"):
            if command[0] == "e":
                quick_select = True
            elif command[0] == "d":
                quick_select = False
            else:
                raise ValueError(f"{command} is not a valid command!")
            return ["main_menu"]
        elif menu == "main_menu" and command not in ["exit", "show selected packs"]:
            # Enters Pack Selection page
            return ["pack_select", command]
        elif menu == "main_menu" and command == "show selected packs":
            # Enters Selected Packs page
            return ["selected_packs"]
        elif menu == "selected_packs" and command == "clear selected packs":
            # Loads JSON
            selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")

            for key, _ in selpacks.items():
                if key == "raw":
                    selpacks["raw"] = []
                else:
                    selpacks[key]["packs"] = []
                    selpacks[key]["index"] = []

            # Dumps JSON
            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpacks)

            clrprint("Selected Packs have been cleared!")
            return [up[menu]]
        elif command == "exit":
            # Exits program
            global loop
            loop = False
            clrprint("Exited program.", clr="yellow")
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

        update_size()
        print(f"{len(pack_files) + 1}. Show Selected Packs", end="")
        print(" " * (min_clm - 23), end="")
        menu_commands.append("show selected packs")
        clmthing()

        if quick_select:
            clrprint(f"{len(pack_files) + 2}. Disable Quick Select", clr="g", end="")
            print(" " * (min_clm - 24), end="")
            menu_commands.append("disable quick select")
        else:
            clrprint(f"{len(pack_files) + 2}. Enable Quick Select", clr="r", end="")
            print(" " * (min_clm - 23), end="")
            menu_commands.append("enable quick select")

        # I need two for some reason
        clmthing()
        clmthing()

        print(f"{len(pack_files) + 3}. Exit Program", end="")
        menu_commands.append("exit")
        clmthing()

        choice = input("\nEnter your choice.\n").lower()
        progged = prog_search(choice, menu_commands)
        # Validates the input/choice
        if choice.isnumeric():
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


# Pack Select Screen showing packs available
def pack_select(topic):
    choice = None
    while choice is None:
        # Terminal Init
        update_size()
        clear()
        # Loading JSON files
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")
        incpacks = load_json(f"{cdir()}/jsons/others/incomplete_packs.json")
        inccomp = load_json(f"{cdir()}/jsons/others/incomplete_compatibilities.json")
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")
        # Navigation Bar
        clrprint(f'Main Menu -> {packs["topic"]}\n', clr="default")
        # Notices
        clrprint("Red", "-> Pack is incomplete", clr="r,w")
        clrprint("Green", "-> Pack is already selected", clr="g,w")
        if quick_select:
            clrprint("Quick Select is enabled! You can't view the packs for more info!")
        clrprint("Yellow", "-> Compatibility with another pack is not completed", clr="y,w")
        clrprint("Blue", "-> Conflicts with another pack\n", clr="b,w")

        clrprint("Packs", clr="purple")
        menu_commands = [""]
        issue = [""]

        for i in range(len(packs["packs"])):
            clmthing()
            if packs["packs"][i]["pack_id"] in incpacks[packs["topic"]]:
                # Pack is not finished
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="red")
                issue.append("incomplete")
            elif packs["packs"][i]["pack_id"] in selpacks[packs["topic"]]["packs"]:
                # Pack is already selected
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="green")
                issue.append("selected")
            else:
                conflict = False
                compatible = True
                for c in packs["packs"][i]["conflict"]:
                    if c in selpacks["raw"]:
                        # Pack conflicts with another pack
                        clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="blue")
                        issue.append(["conflict", c])
                        conflict = True
                        break
                for c in packs["packs"][i]["compatibility"]:
                    try:
                        if c in selpacks["raw"] and c in inccomp[packs["packs"][i]["pack_id"]]:
                            clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="yellow")
                            issue.append(["incompatible", c])
                            compatible = False
                            break
                    except KeyError:
                        # It is complete i guess
                        pass
                if not conflict and compatible:
                    # Pack is finished, not selected and has no conflicts
                    clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="white")
                    issue.append("")
            menu_commands.append(packs["packs"][i]["pack_name"])
            print(" " * (min_clm - len(f'{i + 1}. {packs["packs"][i]["pack_name"]}')), end="")

        clrprint("\n\nOthers", clr="purple")

        print(f'{i + 2}. Go Back (back)', end="")
        print(" " * (min_clm - len(f'{i + 2}. Go Back (back)')), end="")
        menu_commands.append("back")
        issue.append("")
        clmthing()

        print(f'{i + 3}. Exit Program')
        menu_commands.append("exit")
        issue.append("")

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
        if choice is not None:
            progged = menu_commands.index(choice)
            if issue[progged] == "incomplete":
                choice = None
            try:
                if issue[progged][0] in ["conflict", "incompatible"] and quick_select:
                    choice = None
            except IndexError:
                pass
    if choice.lower() in ["exit", "back"]:
        # Returns only choice
        return choice
    elif not quick_select:
        # Returns category, pack name and index of pack_name
        # in JSON file
        progged = menu_commands.index(choice)
        return [topic, choice, progged, issue[progged]]
    elif quick_select:
        # Instantly selects pack unless issue
        progged = menu_commands.index(choice)
        if issue[progged] == "selected":
            select = "unselect"
        else:
            select = "select"
        return [select, f'{topic.replace(" ", "_").lower()}', choice, progged - 1]


# Selected Packs Screen showing Selected Packs
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
        for key, _ in selpacks.items():
            if key != "raw" and selpacks[key]["packs"] != []:
                # Passes through the if statement only
                # if the list has something inside, and
                # its name isn't "raw"
                hasitem = True
                sortedsel = sorted(selpacks[key]["packs"])
                clrprint(key, clr="green")
                for item in sortedsel:
                    print(f"\t- {item}")
        # Just a small easter egg
        if not hasitem:
            clrprint("What is Bedrock Tweaks without any tweaks selected? ._.\nMaybe head back and select some packs!",
                     clr="yellow")

        clrprint("\nOptions", clr="purple")

        if hasitem:
            print(f"1. Clear Selected Packs")
            menu_commands.append("clear selected packs")
        else:
            clrprint(f"1. Clear Selected Packs", clr="r")
            menu_commands.append("")

        print(f"\n2. Go Back (back)")
        menu_commands.append("back")
        if __name__ == "__main__":
            print("\n3. Exit Program (exit)")
            menu_commands.append("exit")

        choice = input("Enter your choice.\n")
        progged = prog_search(choice, menu_commands)
        # Validates input/choice
        if choice in menu_commands:
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


# More info about pack and (un)select pack
def select_pack(topic, pack, index, issue):
    choice = None
    while choice == None:
        # Terminal Init
        update_size()
        clear()
        # Loading JSON Files
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")  # Navigation Bar
        clrprint(f'Main Menu -> {packs["topic"]} -> {pack}\n', clr="default")
        # Pack Description
        print(packs["packs"][int(index) - 1]["pack_description"])

        menu_commands = [""]
        uns = "S"
        conflict, compatible = False, True
        if type(issue) == list:
            if issue[0] == "conflict":
                # When the current pack has a selected conflict
                clrprint(f"{expand(pack)} has a conflict with {issue[1]}!", clr="b")
                clrprint(f"Unselect {issue[1]} to select {expand(pack)}!", clr="b")
                conflict = True
            elif issue[0] == "incompatible":
                clrprint(f"{expand(pack)} is not compatible with {issue[1]} yet!", clr="y")
                clrprint(f"Unselect {issue[1]} to select {expand(pack)}!", clr="y")
                compatible = False
        elif issue == "selected":
            # When the current pack is already selected
            clrprint(f"{pack} has already been selected!", clr="green")
            uns = "Uns"
        clrprint("\nOptions", clr="purple")
        if conflict or not compatible:
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
        return [choice, f'{topic.replace(" ", "_").lower()}', pack, int(index) - 1]


def selector():
    command = ["main_menu"]
    loop = True
    # Main Loop
    try:
        while loop:
            if command[0] == "main_menu":
                # Main Menu
                command = main_menu()
                # I really did not know how to fix TypeError
                # so this exists I guess
                if command == "exit":
                    raise KeyboardInterrupt
                command = val_command("main_menu", command)
            elif command[0] == "pack_select":
                # Pack Selection
                command = pack_select(command[1])
                if command == "exit":
                    raise KeyboardInterrupt
                if quick_select and command not in ["exit", "back"]:
                    command = val_command("select_pack", command)
                else:
                    command = val_command("pack_select", command)
            elif command[0] == "select_pack":
                # More info on pack and if to
                # (un)select or not
                command = select_pack(command[1], command[2], command[3], command[4])
                if command == "exit":
                    raise KeyboardInterrupt
                command = val_command("select_pack", command)
            elif command[0] == "selected_packs":
                # Show Selected Packs
                command = selected_packs()
                if command == "exit":
                    raise KeyboardInterrupt
                command = val_command("selected_packs", command)
            # Shows up for like 10ms, to show my suffering
            clrprint("If you can see this, I suffered about 11 hours in total for this", clr="purple")
            clrprint("Please send help by putting a star on the repo!", clr="purple")
    except KeyboardInterrupt:
        # I don't like seeing massive errors when
        # I stop the program with Ctrl+C, so neat
        # exit instead of spam
        val_command("keyboard_interrupt", "exit")


if __name__ == "__main__":
    selector()
