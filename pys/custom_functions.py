from os import getcwd
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

# For module to be easy to use and not require
# the start of the program to be cluttered
currentdir = getcwd()
if currentdir[-4:] == "\\pys":
    currentdir = currentdir[:-4]
# Yeah...
def cdir():
    return currentdir
