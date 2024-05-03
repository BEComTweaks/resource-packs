import os
import importlib
import pip
from pip import main
import time

# If I need a module that isn't installed
def check(module,module_name=""):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        print(f"{module} is not installed!")
        if module_name == "":
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install",module])
        else:
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install",module_name])
        time.sleep(1)

check("clrprint")
from clrprint import clrprint
check("ujson")
from ujson import *
# For module to be easy to use and not require
# the start of the program to be cluttered
currentdir = os.getcwd()
if currentdir[-3:] == "pys":
    currentdir = currentdir[:-4]
# Yeah...
def cdir():
    return currentdir

# clrinput doesn't work in IDLE, so if someone
# does run it in IDLE, it would work
def clrinput(message,clr:str="white"):
    clrprint(f"{message} ",clr=clr,end="")
    return input()

def clear():
    if os.name == "nt":
        # Windows
        os.system("cls")
    else:
        # Unix, like Mac and Linux
        os.system("clear")

# Simple function to load json from file
def load_json(path):
    with open(path,"r") as file:
        return loads(file.read())

# Simple function to save json into file
def dump_json(path,dictionary):
    with open(path,"w") as file:
        file.write(dumps(dictionary,indent=1))

def prog_search(string:str,list_search:list):
    string = string.lower()
    temp_list = []
    for i in list_search:
        temp_list.append(i.lower())
    list_search = temp_list
    i=0
    found = 0
    found_at = 0
    for i in range(1,len(string)):
        found = 0
        found_at = 0
        for s in range(0,len(list_search)):
            try:
                if list_search[s][:i] == string[:i]:
                    found += 1
                    if found == 1:
                        found_at = s
                if found == 2:
                    break
            except IndexError:
                pass
        if found == 1:
            return found_at
    if found == 0:
        return None