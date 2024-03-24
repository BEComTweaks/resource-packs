import importlib
import subprocess
import pip
from pip import main
from time import sleep as wait
def module_checker(module):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        print(f"{module} is not installed!")
        wait(0.25)
        print("Installing with subprocess...")
        try:
            subprocess.check_call(["pip", "install", module])
            print(f"{module} has been installed!")
            print("Exiting to main program...")
            wait(1)
        except ModuleNotFoundError and FileNotFoundError:
            # Invoked from CMD
            print("")
            print("Subprocess failed!")
            wait(0.25)
            print("Installing with pip...")
            try:
                pip.main(["install",module])
                print(f"{module} has been installed!")
                print("Exiting to main program...")
                wait(1)

            except:
                raise Exception("Installation failed!")