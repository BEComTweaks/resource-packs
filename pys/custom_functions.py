def module_checker(module):
    import importlib
    import subprocess
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        subprocess.check_call(["pip", "install", module])
