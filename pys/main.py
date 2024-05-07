contributor = True # Tools for contributors
import os
import shutil
import time
import traceback

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
    from tweakimage import tweakimage
except ModuleNotFoundError:
    print(f"main.py is at {os.path.realpath(__file__)} but it is executing at {os.getcwd()}!")
    print("You are likely using a non-Windows device!")
    print("Send the path where the code is executing at to https://discord.com/channels/567364180857061437/1053415910343462923/threads/1231970599799226388 along with your current device!")
    exit(1)

check("clrprint")
from clrprint import clrprint

try:
    while True:
        if shutil.get_terminal_size().columns < 47:
            print("The minimum terminal width recommended is 47.")
            print("Make sure the bar below is in a single line.")
            print(f"[{'='*45}]")
            while shutil.get_terminal_size().columns < 47:
                pass
            clrprint("Success!",clr="g")
            time.sleep(1)
        clear()
        if shutil.get_terminal_size().columns > 100:
            print("    _____              __                        __  ",end="   ")
            print("  ______                             __         ")
            print("   / __ /  ___    ____/ / _____  ____    _____  / /__",end="   ")
            print(" /_  __/ _      __  ___    ____ _   / /__  _____")
            print("  / __  | / _ \  / __  / / ___/ / __ \  / ___/ / //_/",end="   ")
            print("  / /   | | /| / / / _ \  / __  /  / //_/ / ___/")
            print(" / /_/ / /  __/ / /_/ / / /    / /_/ / / /__  / / |  ",end="   ")
            print(" / /    | |/ |/ / /  __/ / /_/ /  / / |  /__  / ")
            print("/_____/  \___/  \____/ /_/     \____/  \___/ /_/|_|  ",end="   ")
            print("/_/     |__/|__/  \___/  \__,_/\ /_/|_| /____/  ")
        else:
            print("    _____            __                    __  ")
            print("   / __ / ___   ____/ /_____ ____   _____ / /__")
            print("  / __  |/ _ \ / __  // ___// __ \ / ___// //_/")
            print(" / /_/ //  __// /_/ // /   / /_/ // /__ / / |  ")
            print("/_____/ \___/ \____//_/    \____/ \___//_/|_|  ")
            print("  ______                         __        ")
            print(" /_  __/_      __ ___   ____ _  / /__ _____")
            print("  / /  | | /| / // _ \ / __  / / //_// ___/")
            print(" / /   | |/ |/ //  __// /_/ / / / | /__  / ")
            print("/_/    |__/|__/ \___/ \__,_/\/_/|_|/____/  ")
        clrprint("\n\nOptions:",clr="p")
        menu_commands = [""]

        i = 1
        print(f"{i}. Start Pack Selection")
        menu_commands.append("start pack selection")
        i += 1
        print(f"{i}. View Selected Packs")
        menu_commands.append("view selected packs")
        i += 1
        clrprint(f"{i}. Export Pack",clr="r")
        #menu_commands.append("export pack")
        menu_commands.append("")
        if contributor:
            i += 1
            print(f"{i}. Create Folders")
            menu_commands.append("create folders")
            i += 1
            print(f"{i}. Tweak Image Pixels")
            menu_commands.append("tweak image")
            i += 1
            print(f"{i}. Pre Commit Checks")
            menu_commands.append("pre commit")
        i += 1
        print(f"{i}. Credits")
        menu_commands.append("credits")
        i += 1
        print(f"{i}. Exit Program")
        menu_commands.append("exit")

        choice = clrinput("Enter your choice:",clr="yellow")
        progged = prog_search(choice,menu_commands)
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
                selected_packs()
            elif choice == "export":
                pass
            elif choice == "create folders":
                folder_creator()
            elif choice == "tweak image":
                tweakimage()
            elif choice == "pre commit":
                pre_commit()
            elif choice == "credits":
                clear()
                with open(f"{cdir()}/credits.txt","r") as credits:
                    print(credits.read())
                    clrinput("Press Enter to go back",clr="g")
except KeyboardInterrupt:
    val_command("KeyboardInterrupt","exit")