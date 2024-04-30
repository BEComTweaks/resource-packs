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
check("clrprint")
from clrprint import clrprint
check("ujson")
from ujson import *

clm = shutil.get_terminal_size().columns
lins = shutil.get_terminal_size().lines

# Menu Up and Down stuff
down = {
            "main_menu": ["pack_select","selected_packs"],
            "pack_select": ["select_pack"]
            }
up = {
            "select_pack": ["pack_select"],
            "pack_select": ["main_menu"],
            "selected_packs": ["main_menu"]
            }
# Command validation for below
def val_command(menu,command):
    if command == "back":
        return ["page",up[menu]]
    elif menu == "main_menu"  and command not in ["exit","show selected packs"]:
        return ["page","pack_select",command]
    elif menu == "main_menu" and command == "show selected packs":
        return ["page","selected_packs"]
    elif menu == "pack_select" and command != "exit":
        print(command)
        input("pack_select completed")
        
    elif command == "exit":
        clrprint("Exited program.",clr="yellow")
        exit(0)
    
# Menu Screen showing categories
def main_menu():
    choice = None
    while choice == None:
        clear()
        print("Main Menu:")
        clrprint("Categories",clr="blue")
        menu_commands = [""]
        for i in range(len(os.listdir(f"{cdir()}/jsons/packs"))):
            print(f'{i+1}.', end=" ")
            with open(f'{cdir()}/jsons/packs/{os.listdir(f"{cdir()}/jsons/packs")[i]}',"r") as packjson:
                print(loads(packjson.read())["topic"])
                menu_commands.append(os.listdir(f"{cdir()}/jsons/packs")[i].lower())
        clrprint("Others",clr="purple")
        print(f"{i+2}. Show Selected Packs")
        menu_commands.append("show selected packs")
        print(f"{i+3}. Exit Program (exit)")
        menu_commands.append("exit")
        choice = input("Enter your choice.\n").lower()
        if choice in menu_commands:
            if " " in choice:
                choice = choice.replace(" ","_")
        elif choice not in menu_commands and choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif choice not in menu_commands:
            choice = None
    return choice

def pack_select(topic):
    choice = None
    while choice == None:
        with open(f"{cdir()}/jsons/packs/{topic}","r") as packjson:
            packs = loads(packjson.read())
        with open(f"{cdir()}/jsons/others/incomplete_packs.json","r") as incjson:
            incpacks = loads(incjson.read())
        with open(f"{cdir()}/jsons/others/selected_packs.json","r") as seljson:
            selpacks = loads(seljson.read())
        clear()
        print(packs["topic"])
        clrprint("Green","means this pack has been selected",clr="g,w")
        clrprint("Red","means this pack has not been finished and cannot be selected\n",clr="r,w")
        clrprint("Packs",clr="blue")
        menu_commands = [""]
        for i in range(0,len(packs["packs"]),2):
            if packs["packs"][i]["pack_id"] in incpacks[packs["topic"]]:
                clrprint(f'{i+1}. {packs["packs"][i]["pack_name"]}',end="",clr="red")
                menu_commands.append("")
            elif packs["packs"][i]["pack_id"] in selpacks[packs["topic"]]:
                clrprint(f'{i+1}. {packs["packs"][i]["pack_name"]}',end="",clr="green")
                menu_commands.append(packs["packs"][i]["pack_name"].lower())
            else:
                clrprint(f'{i+1}. {packs["packs"][i]["pack_name"]}',end="",clr="white")
                menu_commands.append(packs["packs"][i]["pack_name"].lower())
            print(" "*((int(clm)//2)-len(f'{i+1}. {packs["packs"][i]["pack_name"]}')),end="")
            if i + 1 < len(packs["packs"]):
                i += 1
                if packs["packs"][i]["pack_id"] in incpacks[packs["topic"]]:
                    clrprint(f'{i+1}. {packs["packs"][i]["pack_name"]}',clr="red")
                    menu_commands.append("")
                elif packs["packs"][i]["pack_id"] in selpacks[packs["topic"]]:
                    clrprint(f'{i+1}. {packs["packs"][1]["pack_name"]}',clr="green")
                    menu_commands.append(packs["packs"][i]["pack_name"].lower())
                else:
                    clrprint(f'{i+1}. {packs["packs"][i]["pack_name"]}',clr="white")
                    menu_commands.append(packs["packs"][i]["pack_name"].lower())
        clrprint("\nOthers",clr="purple")
        print(f'{i+2}. Go Back (back)',end="")
        print(" "*((int(clm)//2)-len(f'{i+2}. Go Back (back)')),end="")
        menu_commands.append("back")
        print(f'{i+3}. Exit Program (exit)')
        menu_commands.append("exit")
        choice = input("Enter your choice.\n").lower()
        if choice in menu_commands:
            pass
        elif choice not in menu_commands and choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif choice not in menu_commands:
            choice = None
    return choice
    

while True:
    mainmenu = main_menu()
    command = val_command("main_menu",mainmenu)
    if command[0] == "page" and command[1] == "pack_select":
        packselect = pack_select(command[2])
        command = val_command("pack_select",packselect)