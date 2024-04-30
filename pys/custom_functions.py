import os
import importlib
import pip
from pip import main
import time

# If I need a module that isn't installed
def check(module,module_name=""):
    if module_name == "":
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            print(f"{module} is not installed!")
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install",module])
            time.sleep(1)
    else:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            print(f"{module} is not installed!")
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install",module_name])
            time.sleep(1)

check("ujson","ujson")
from ujson import *
check("clrprint")
from clrprint import clrprint

# For module to be easy to use and not require
# the start of the program to be cluttered
currentdir = os.getcwd()
if currentdir[-4:] == "\\pys":
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