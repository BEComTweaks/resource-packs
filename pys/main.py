contributor = False  # Tools for contributors
con_clr = "w"
import os
import shutil

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from custom_functions import *
    from selector import selected_packs, val_command, selector
    from folder_creator import folder_creator
    from pre_commit import pre_commit
    from image_utils import image_utils
    from exporter import export
except ModuleNotFoundError:
    print(f"main.py is at {os.path.realpath(__file__)} but it is executing at {os.getcwd()}!")
    print("You are likely using a non-Windows device!")
    print(
        "Send the path where the code is executing at to https://discord.com/channels/567364180857061437/1053415910343462923/threads/1231970599799226388 along with your current device!")
    exit(1)

check("clrprint")
from clrprint import clrprint

try:
    while True:
        if shutil.get_terminal_size().columns < 47:
            print("The minimum terminal width recommended is 47.")
            print("Make sure the bar below is in a single line.")
            print(f"[{'=' * 45}]")
            while shutil.get_terminal_size().columns < 47:
                pass
            clrprint("Success!", clr="g")
            time.sleep(1)
        clear()
        if shutil.get_terminal_size().columns > 100:
            clrprint(r"    _____              __                        __  ", end="   ", clr=con_clr)
            clrprint(r"  ______                             __         ", clr=con_clr)
            clrprint(r"   / __ /  ___    ____/ / _____  ____    _____  / /__", end="   ", clr=con_clr)
            clrprint(r" /_  __/ _      __  ___    ____ _   / /__  _____", clr=con_clr)
            clrprint(r"  / __  | / _ \  / __  / / ___/ / __ \  / ___/ / //_/", end="   ", clr=con_clr)
            clrprint(r"  / /   | | /| / / / _ \  / __  /  / //_/ / ___/", clr=con_clr)
            clrprint(r" / /_/ / /  __/ / /_/ / / /    / /_/ / / /__  / / |  ", end="   ", clr=con_clr)
            clrprint(r" / /    | |/ |/ / /  __/ / /_/ /  / / |  /__  / ", clr=con_clr)
            clrprint(r"/_____/  \___/  \____/ /_/     \____/  \___/ /_/|_|  ", end="   ", clr=con_clr)
            clrprint(r"/_/     |__/|__/  \___/  \____/\ /_/|_| /____/  ", clr=con_clr)
        else:
            clrprint(r"    _____            __                    __  ", clr=con_clr)
            clrprint(r"   / __ / ___   ____/ /_____ ____   _____ / /__", clr=con_clr)
            clrprint(r"  / __  |/ _ \ / __  // ___// __ \ / ___// //_/", clr=con_clr)
            clrprint(r" / /_/ //  __// /_/ // /   / /_/ // /__ / / |  ", clr=con_clr)
            clrprint(r"/_____/ \___/ \____//_/    \____/ \___//_/|_|  ", clr=con_clr)
            clrprint(r"  ______                         __        ", clr=con_clr)
            clrprint(r" /_  __/_      __ ___   ____ _  / /__ _____", clr=con_clr)
            clrprint(r"  / /  | | /| / // _ \ / __  / / //_// ___/", clr=con_clr)
            clrprint(r" / /   | |/ |/ //  __// /_/ / / / | /__  / ", clr=con_clr)
            clrprint(r"/_/    |__/|__/ \___/ \____/\/_/|_|/____/  ", clr=con_clr)
        clrprint("\n\nOptions:", clr="p")
        menu_commands = [""]

        i = 1
        print(f"{i}. Start Pack Selection")
        menu_commands.append("start pack selection")
        i += 1
        print(f"{i}. View Selected Packs")
        menu_commands.append("view selected packs")
        i += 1
        print(f"{i}. Export Pack")
        menu_commands.append("export pack")
        if contributor:
            i += 1
            clrprint(f"{i}. Create Folders", clr="b")
            menu_commands.append("create folders")
            i += 1
            clrprint(f"{i}. Launch Image Utilities", clr="b")
            menu_commands.append("launch image utilities")
            i += 1
            clrprint(f"{i}. Pre Commit Checks", clr="b")
            menu_commands.append("pre commit")
        i += 1
        print(f"{i}. Credits")
        menu_commands.append("credits")
        i += 1
        print(f"{i}. Exit Program")
        menu_commands.append("exit")

        menu_commands.append("contributor")
        choice = clrinput("Enter your choice:", clr="yellow")
        progged = prog_search(choice, menu_commands)
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
        if choice != None:
            if choice == "exit":
                raise KeyboardInterrupt
            elif choice == "start pack selection":
                selector()
            elif choice == "view selected packs":
                opt = selected_packs()
                if opt == "clear selected packs":
                    val_command("selected_packs", opt)
            elif choice == "export pack":
                export()
            elif choice == "create folders":
                folder_creator()
            elif choice == "launch image utilities":
                image_utils()
            elif choice == "pre commit":
                pre_commit()
            elif choice == "credits":
                clear()
                with open(f"{cdir()}/credits.md", "r") as credits:
                    credit = credits.read()
                    credit = credit.replace("[","")
                    credit = credit.replace("]("," - ")
                    credit = credit.replace(")","")
                    credit = credit.replace("#","")
                    credit = credit.replace("<br>","")
                    print(credit)
                    clrinput("Press Enter to go back", clr="g")
            elif choice == "contributor":
                contributor = not (contributor)
                con_clr = ["b", "w"][["b", "w"].index(con_clr) - 1]
except KeyboardInterrupt:
    val_command("KeyboardInterrupt", "exit")
