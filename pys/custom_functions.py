import importlib
import pip
from pip import main
def module_checker(module):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        pip.main(["install",module])