import os
import shutil
from icecream import ic

if str(os.getcwd()).endswith("system32"):
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
else:
    doubleclicked = False
from custom_functions import *

# Default size is 120x30, so I am building based on that
if shutil.get_terminal_size().columns != 120 and shutil.get_terminal_size().lines != 30:
    clrprint(f"\rThe terminal's current size is ({shutil.get_terminal_size().columns}, {shutil.get_terminal_size().lines}) but the recommended size is (120, 30).",clr="r")
    clrprint("Continuing means there may be visual issues.",clr="r")
    clrprint("Make sure you have double-clicked the file instead of running through CMD",clr="r")
    try:
        clrinput("If you are fine with this, press Enter. If not, press Ctrl+C",clr="y")
    except KeyboardInterrupt:
        exit(1)
clear()

# Menu Screen showing categories
def main_menu():
    print("Menu:")
    menu_commands = [""]
    for i in range(len(os.listdir(f"{cdir()}/packs"))):
        print(f'{i+1}.', end=" ")
        print(os.listdir(f"{cdir()}\\packs")[i])
        menu_commands.append(os.listdir(f"{cdir()}\\packs")[i].lower())
    print(f"{i+2}. Show Selected Packs")
    menu_commands.append("show selected packs")
    print(f"{i+3}. Exit")
    menu_commands.append("exit")
    choice = input("Enter your command.\n").lower()
    if choice not in os.listdir(f"{cdir()}\\packs") and choice.isnumeric():
        try:
            choice = menu_commands[int(choice)]
        except IndexError:
            choice = None
    elif choice not in os.listdir(f"{cdir()}\\packs"):
        choice = None
    return choice
