# This is an explanation to how the JSON in the jsons folder work.

In each file, you may see something like shown below

```json
{
  "topic": "Category",
  "packs": [
    {
      "pack_id": "Pack3",
      "pack_name": "Pack 3",
      "pack_description": "Test Description",
      "conflict": ["Pack4"],
      "compatability": ["Pack1"]
    }
  ]
}
```

From the example above, there is a lot going on in the json file. Even though, the objects should be self-explanatory, I will still attempt to explain them.
> How I hope the UI would look like
![Alt text](image-1.png)

From the image,

1. `Category` refers to `"topic"`
2. `Pack 3` refers to `"pack_name"`
3. `Test Description` refers to `"pack_description"`

However, other things that need mentioning
show conflicts

1. Pack ID and Pack Name are nearly the same

    VT uses a different format for Pack IDs, which make them a bit small. I wanted to finish the JSON quick, so the Pack ID is basically Pack Name without any spaces.
2. Pack 3 and Pack 4 are green when selected.

    As shown in `"conflict"`, Pack4 is there, so when both Pack 3 and Pack 4 are selected, they turn into other colors to indicate the conflict. They should prevent the download from occuring as they conflict, so unlike Vanilla Tweaks, which allows conflicting packs to be downloaded, it is best to prevent it from being downloaded.
3. Compatability modes do not appear

    I feel compatability modes would not need marking, rather let it be automatic. If they do not conflict, then why the extra colors? It may be confusing after a while.

The folder structure should hypothetically be like this

`{topic}/{pack_id}/{compatability}`

`{topic}` is the topic from the JSON

`{pack_id}` is the pack_id from the JSON. `{pack_name}` won't be used because it has spaces in it

`{compatability}` is optional as the pack may not have compatability with other packs. This may not be the same with vanillatweaks as I can't see whether there is compatability with other packs, so I have to infer them.

`{compatability}` is not 1 folder, it may contain sub folders, to show every possible version, because I am not exactly sure how to combine them. If I can, I'll try, but for now, it will have every possible mode

That should be how the repository would be arranged.

I plan on making a [Text User Interface](https://en.wikipedia.org/wiki/Text-based_user_interface), rather than jumping straight to websites. I have barely any experience with `HTML` and `Javascript`, so I feel if I make a bare-bones version as a TUI with Python, it would be easier to build on top of it.
