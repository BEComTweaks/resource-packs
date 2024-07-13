# Explanation of how .py files work in pys work

Read their comments to understand more

## [custom_functions.py](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py)

Simply a housing for six functions that I use.

### [check(module)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L10-L23)

Like what it says. When this function is called, it checks whether `module` is installed. If it isn't, it
uses [pip](https://pypi.org/project/pip/) to install that specified function.

I am not using [subprocess](https://docs.python.org/3/library/subprocess.html) to run `pip install module` as subprocess
does not work when invoked in terminal, unlike pip.

pip does spawn some yellow text saying not to invoke, but if it works, it works *＼（〇*ｏ）／\_

### [cdir()](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L32-L42)

When this function is called, a string is returned, with the exact path to the repository (If it is run in
either [root](https://github.com/BEComTweaks/resource-packs/tree/main)
or [pys](https://github.com/BEComTweaks/resource-packs/tree/main/pys)).
It is just a QOL function to prevent extra code at the start of other scripts

### [expand(string)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L52-L61)

Does the opposite of `"".join(string.split())`

Takes a string, and adds spaces in front of character thsat are uppercase

### [contract(string)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L65-L66)

Only does `"".join(string.split())`. It exists for a neater code

### [clear()](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L70-L76)

Clears the terminal when the function is called

### [load_json(path)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L80-L89)

Returns JSON loaded as dictionary from file path

### [dump_json(path,dictionary)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L93-L96)

Saves JSON with indentation to path

### [prog_search(string,list_search)](https://github.com/BEComTweaks/resource-packs/blob/main/pys/custom_functions.py#L99-L132)

Checks first n letters of string with each item in list_search

- If there is more than one item that matches the first n letters of string, n is increased by 1

This continues until only one item matches the first n characters of the string, or the string runs out of characters tocheck for

## [folder_creator.py](https://github.com/BEComTweaks/resource-packs/blob/main/pys/folder_creator.py)

Creates folders based on the [json files](https://github.com/BEComTweaks/resource-packs/tree/jsons/packs).

## [pre_commit.py](https://github.com/BEComTweaks/resource-packs/blob/main/pys/pre_commit.py)

Does 3 processes

1. Counts finished packs, compatibility subpacks and pack icons
2. Updates [incomplete_packs.json](https://github.com/BEComTweaks/resource-packs/blob/main/jsons/others/incomplete_packs.json), [incomplete_compatibilities.json](https://github.com/BEComTweaks/resource-packs/blob/main/jsons/others/incomplete_compatibilities.json), [incomplete_pack_icons.json](https://github.com/BEComTweaks/resource-packs/blob/main/jsons/others/incomplete_pack_icons.json), [pack_conflicts.json](https://github.com/BEComTweaks/resource-packs/blob/main/jsons/others/pack_conflicts.json) and [index.html](https://github.com/BEComTweaks/resource-packs/blob/main/webUI/index.html)
3. Updates README.md with the numbers from above
4. Validates all text files with Prettier

## [image_utils.py](https://github.com/BEComTweaks/resource-packs/blob/main/pys/image_utils.py)

Two options:

1. Tweak Images<br>
   Takes a directory as an input.<br>
   Opens all PNG files, changes the colour by ±6 **except opacity**<br>
   Example:<br>
   - If a pixel is rgba(236,185,212,255), it can change it to rgba(237,184,214,255)
2. Compress Images
   Takes a directory as an input.<br>
   Opens all PNG files in directory **and subdirectories**, and compresses it by a number inputted

# That's it!

<sub>If you want a better explanation, there are comments in each script and have a more detailed explanation on what is
going on.</sub>

[<- Back to docs.md](https://github.com/BedrockTweaks/Bedrock-Tweaks-Base/blob/main/docs/docs.md)
