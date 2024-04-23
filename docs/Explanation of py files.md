# Explanation of how .py files work in pys work

Currently, it has 4 Python Scripts inside.

## [custom_functions.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py)

Simply a housing for two functions that I use.

### [check(module)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/0bbad992d41ccb1ab7cbf3af0d20987d7af463dd/pys/custom_functions.py#L7-L15)

Like what it says. When this function is called, it checks whether `module` is installed. If it is, it uses [pip](https://pypi.org/project/pip/) to install that specified function.

I am not using [subprocess](https://docs.python.org/3/library/subprocess.html) to run `pip install module` as subprocess does not work when invoked in terminal, unlike pip. It does spawn some yellow text saying not to invoke, but if it works, it works _＼（〇_ｏ）／_

### [cdir()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/0bbad992d41ccb1ab7cbf3af0d20987d7af463dd/pys/custom_functions.py#L19-L29)

When this function is called, a string is returned, with the exact path to the repository (If it is run in either [root](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main) or [pys](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main/pys)).
It is just a QOL function to prevent extra code at the start of other scripts

## [folder_creator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/folder_creator.py)

Creates folders based on the [json files](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/jsons/packs).

What it does upon execution:

1. It asks for mode.

    - Mode = 0:
        
        - Executes without printing anything
        - Fastest Execution
        - Least Debuggable
    - Mode = 1:

        - Prints each pack
            
            - If the pack already exists in `packs/{category}/{packid}`, it does not print any more statements for it
            - If the directory does not exist/is empty, it prints extra statements, like creation of pack_icon.png and sub-directories
        - Moderately Fast Execution
        - Moderately Debuggable
    - Mode = 2:
        
        - Prints each pack
            
            - Prints errors, like directories not being empty, in red and yellow
            - Prints successes, like creation of directories, in blue and magenta
        - Relatively Slow Execution
        - Pretty Debuggable

## [incomplete_packs_updater.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/incomplete_packs_updater.py)

Updates [jsons/others/incomplete_packs.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/jsons/others/incomplete_packs.json) with the addition/removal of packs.

Updates [README.md](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/README.md) [Line 4](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/README.md?plain=1#L4) with progress on packs completed

## [manifestgenerator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/manifestgenerator.py)

Generates a `manifest.json` file in a random directory in the following template `BTRP-xxxxxx`

Uses [jsons/others/manifest.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/jsons/others/manifest.json) as the template to create the manifest.json. Description is not ready yet, as I need to set up the selection of packs for the description to work.

# That's it!