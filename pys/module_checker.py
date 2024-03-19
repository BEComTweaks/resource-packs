import importlib
import subprocess
def module_checker(module):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        subprocess.check_call(["pip", "install", module])
