# Explanation of how .py files work in pys work

Currently, it has 4 Python Scripts inside.

## [custom_functions.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py)

Simply a housing for two functions that I use.

### [check(module)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/0bbad992d41ccb1ab7cbf3af0d20987d7af463dd/pys/custom_functions.py#L7-L15)

Like what it says. When this function is called, it checks whether `module` is installed. If it is, it uses [pip](https://pypi.org/project/pip/) to install that specified function.

I am not using [subprocess](https://docs.python.org/3/library/subprocess.html) to run `pip install module` as subprocess does not work when invoked in terminal, unlike pip.

pip does spawn some yellow text saying not to invoke, but if it works, it works _＼（〇_ｏ）／_

### [cdir()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/0bbad992d41ccb1ab7cbf3af0d20987d7af463dd/pys/custom_functions.py#L19-L29)

When this function is called, a string is returned, with the exact path to the repository (If it is run in either [root](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main) or [pys](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main/pys)).
It is just a QOL function to prevent extra code at the start of other scripts

## [folder_creator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/folder_creator.py)

Creates folders based on the [json files](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/jsons/packs).

## [pre_commit.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py)

Does 3 processes

1. Counts finished packs, and compatibility subpacks [Lines 35-93](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L35-L93)
2. Updates README.md with the numbers from above [Lines 94-118](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L94-L118)
3. Validates JSON files [Lines 119-138](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L119-L138)
   - Uses JSON5 instead of JSON as Minecraft allows comments in JSON Files, while normal JSON doesn't

## [manifestgenerator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/manifestgenerator.py)

Generates a `manifest.json` file in a random directory in the following template `BTRP-xxxxxx`

Uses [jsons/others/manifest.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/jsons/others/manifest.json) as the template to create the manifest.json. Description is not ready yet, as I need to set up the selection of packs for the description to work.

## [tweakimage.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/tweakimage.py)

Takes a directory as an input.

Opens all PNG files, changes the colour by ±6 **except opacity**

Example:
- If a pixel is rgba(236,185,212,255), it can change it to rgba(237,184,214,255)

# That's it!
