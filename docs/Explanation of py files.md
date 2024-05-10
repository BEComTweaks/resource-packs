# Explanation of how .py files work in pys work

Currently, it has 7 Python Scripts inside, 3 of which are still not complete.

## [custom_functions.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py)

Simply a housing for six functions that I use.

### [check(module)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L10-L23)

Like what it says. When this function is called, it checks whether `module` is installed. If it isn't, it uses [pip](https://pypi.org/project/pip/) to install that specified function.

I am not using [subprocess](https://docs.python.org/3/library/subprocess.html) to run `pip install module` as subprocess does not work when invoked in terminal, unlike pip.

pip does spawn some yellow text saying not to invoke, but if it works, it works _＼（〇_ｏ）／_

### [cdir()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L32-L42)

When this function is called, a string is returned, with the exact path to the repository (If it is run in either [root](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main) or [pys](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/main/pys)).
It is just a QOL function to prevent extra code at the start of other scripts

### [expand(string)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L52-L61)

Does the opposite of `"".join(string.split())`

Takes a string, and adds spaces in front of character thsat are uppercase

### [contract(string)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L65-L66)

Only does `"".join(string.split())`. It exists for a neater code

### [clear()](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L70-L76)

Clears the terminal when the function is called

### [load_json(path)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L80-L87)

Returns JSON loaded as dictionary from file path

### [dump_json(path,dictionary)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L91-L94)

Saves JSON with indentation to path

### [prog_search(string,list_search)](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/custom_functions.py#L97-L130)

Checks first n letters of string with each item in list_search
- If there is more than one item that matches the first n letters of string, n is increased by 1

This continues until only one item matches the first n characters of the string, or the string runs out of characters to check for

## [folder_creator.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/folder_creator.py)

Creates folders based on the [json files](https://github.com/NSPC911/Bedrock-Tweaks-Base/tree/jsons/packs).

## [pre_commit.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py)

Does 3 processes

1. Counts finished packs, and compatibility subpacks [Lines 32-86](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L32-L86)
2. Updates [incomplete_packs.json](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/jsons/others/incomplete_packs.json) with the incomplete packs [Lines 89-92](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L89-L92)
3. Updates README.md with the numbers from above [Lines 98-117](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L98-L117)
4. Validates JSON files [Lines 121-136](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/pre_commit.py#L121-L136)
   - Uses JSON5 instead of JSON as Minecraft allows comments in JSON Files, while normal JSON doesn't

## [tweakimage.py](https://github.com/NSPC911/Bedrock-Tweaks-Base/blob/main/pys/tweakimage.py)

Takes a directory as an input.

Opens all PNG files, changes the colour by ±6 **except opacity**

Example:
- If a pixel is rgba(236,185,212,255), it can change it to rgba(237,184,214,255)

# That's it!

<sub>If you want a better explanation, there are comments in each script and have a more detailed explanation on what is going on.</sub>
