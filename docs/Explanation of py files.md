# Explanation of how .py files work in pys work

Currently, it has 6 Python Scripts inside.

[main.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/main.py) will not have a section here as there is too much going on there. I will recommend reading the comments in the code to know what is going on.

## [custom_functions.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py)

Simply a housing for two functions that I use.

### [check(module)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L8-L21)

Like what it says. When this function is called, it checks whether `module` is installed. If it is, it uses [pip](https://pypi.org/project/pip/) to install that specified function.

I am not using [subprocess](https://docs.python.org/3/library/subprocess.html) to run `pip install module` as subprocess does not work when invoked in terminal, unlike pip.

pip does spawn some yellow text saying not to invoke, but if it works, it works _＼（〇_ｏ）／_

### [cdir()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L34-L34)

When this function is called, a string is returned, with the exact path to the repository (If it is run in either [root](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main) or [pys](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main/pys)).
It is just a QOL function to prevent extra code at the start of other scripts

### [clear()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L43-L49)

Clears the terminal when the function is called

### [load_json(path)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L52-L54)

Returns JSON loaded as dictionary from file path

### [dump_json(path,dictionary)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L57-L59)

Saves JSON with indentation to path

### [prog_search(string,list_search)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L62-L95)

Checks first n letters of string with each item in list_search
- If there is more than one item that matches the first n letters of string, n is increased by 1

This continues until only one item matches the first n characters of the string, or the string runs out of characters to check for

## [folder_creator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/folder_creator.py)

Creates folders based on the [json files](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/jsons/packs).

## [manifestgenerator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/manifestgenerator.py)

Generates a `manifest.json` file in a random directory in the following template `BTRP-xxxxxx`

Uses [jsons/others/manifest.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/jsons/others/manifest.json) as the template to create the manifest.json. Description is not ready yet, as I need to set up the selection of packs for the description to work.

## [pre_commit.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py)

Does 3 processes

1. Counts finished packs, and compatibility subpacks [Lines 35-75](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L35-L75)
2. Updates [incomplete_packs.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/jsons/others/incomplete_packs.json) with the incomplete packs [Lines 77-78](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L77-L78)
3. Updates README.md with the numbers from above [Lines 79-103](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L79-L103)
4. Validates JSON files [Lines 104-125](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L104-L125)
   - Uses JSON5 instead of JSON as Minecraft allows comments in JSON Files, while normal JSON doesn't

## [tweakimage.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/tweakimage.py)

Takes a directory as an input.

Opens all PNG files, changes the colour by ±6 **except opacity**

Example:
- If a pixel is rgba(236,185,212,255), it can change it to rgba(237,184,214,255)

# That's it!

<sub>If you want a better explanation, there are comments in each script and have a more detailed explanation on what is going on.</sub>
