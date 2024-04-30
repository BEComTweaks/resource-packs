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

# Fancy thing to get the value
def indexreturn(filename:str, keyone:str, keytwo:int=-1, keythree:str=""):
    if not isinstance(filename,str):
        raise TypeError(f"Expected 'str' for 'filename' but got {type(filename).__name__}")
    elif not isinstance(keyone,str):
        raise TypeError(f"Expected 'str' for 'keyone' but got {type(keyone).__name__}")
    elif not isinstance(keytwo,int):
        raise TypeError(f"Expected 'int' for 'keytwo' but got {type(keytwo).__name__}")
    elif not isinstance(keythree,str):
        raise TypeError(f"Expected 'str' for 'keythree' but got {type(keythree).__name__}")
    if "." in filename:
        with open(f"{cdir()}/jsons/packs/{filename}","r") as file:
            try:
                filejson = loads(file.read())
            except JSONDecodeError as error_message:
                print(f"Error in `{filename}`: {error_message}")
    else:
        with open(f"{cdir()}/jsons/packs/{filename}.json","r") as file:
            try:
                filejson = loads(file.read())
            except JSONDecodeError as error_message:
                print(f"Error in `{filename}`: {error_message}")
    k = filejson[keyone]
    if keytwo != -1:
        k = k[keytwo]
        if keythree != "":
            k = k[keythree]
    return k

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