import os, traceback, sys, stat
from subprocess import run as sp_run
from typing import Union


class EmptySpinner:
    def __init__(self, *objects, spinner="dots"):
        self.objects = objects
        self.spinner = spinner

    def __enter__(self):
        print(*self.objects)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

emptySpinner = EmptySpinner

def sendToCF(main_args): #send vars from main to custom_functions
    global args
    args = main_args
    global spinner
    global print
    if args.dev:
        print = console.log
    else:
        print = console.print
    if args.no_spinner:
        spinner = emptySpinner
    else:
        spinner = console.status

def run(cmd: Union[str, list], quiet=False, exit_on_error=True):
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    with spinner(f"[white]> [/white][yellow]{cmd}", spinner="bouncingBall"):
        output = sp_run(cmd, shell=True, capture_output=True, text=True)
        try:
            if not args.quiet:
                if output.returncode == 0:
                    if not quiet:
                        for line in output.stdout.split("\n"):
                            print(f"  {line}")
                        return output
                else:
                    for line in output.stdout.split("\n"):
                        print(f"  [red]{line}")
                    for line in output.stderr.split("\n"):
                        print(f"  [bright_red]{line}")
                    if exit_on_error:
                        exit(1)
                    else: return output
        except UnboundLocalError or NameError:
            if output.returncode == 0:
                if not quiet:
                    for line in output.stdout.split("\n"):
                        print(f"  {line}")
                    return output
            else:
                for line in output.stdout.split("\n"):
                    print(f"  [red]{line}")
                for line in output.stderr.split("\n"):
                    print(f"  [bright_red]{line}")
                if exit_on_error:
                    exit(1)
                else:
                    return output

from rich import print
from rich.console import Console
console = Console()

from ujson import *


# For module to be easy to use and not require
# the start of the program to be cluttered
currentdir = os.getcwd()
if currentdir[-3:] == "pys":
    currentdir = currentdir[:-4]


# Yeah...
def cdir():
    return str(currentdir)


# Clears terminal screen
def clear():
    if os.name == "nt":
        # Windows
        os.system("cls")
    else:
        # Unix, like Mac and Linux
        os.system("clear")


# Simple function to load json from file
def load_json(path):
    with open(path, "r") as file:
        try:
            json_data = loads(file.read())
            if "$schema" in json_data:
                del json_data["$schema"]
            return json_data
        except JSONDecodeError:
            print(f"[red]\n{path} got a JSON Decode Error")
            print(f"[red]{traceback.format_exc()}")
            exit()


# Simple function to save json into file
def dump_json(path, dictionary):
    the_json = dumps(dictionary, indent=2)
    the_json = the_json.replace(r"\/","/")
    with open(path, "w") as file:
        file.write(the_json)

def remove_readonly(func, path, _):
    if args.dev:
        print(f"---> [bright_red]Removing readonly attribute from {os.path.relpath(path, cdir())}")
    os.chmod(path, stat.S_IWRITE)
    func(path)