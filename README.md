# Bedrock Tweaks Base
 A repo containing every single tweak ported from vanillatweaks.net
Currently, it isn't exactly completed. I am currently finishing up on the JSON files required for indexing the packs. Hopefully I get that done before I start on the folders for each topic and pack.
I may need to switch this to a wiki to show how this works.
In each JSON, you have many categories
```json
{
  "topic": "Topic is the name of the category of packs.",
  "packs": [
    {
      "pack_id": "This is the pack_id, basically pack_name without spaces. The ID format could be improved, but I have not done anything related to that",
      "pack_name": "This is the pack_name, the individualized name for each packs. I have nothing more to say",
      "pack_description": "This is the pack_description. Should be under the pack_name in websites, but I plan on making a TUI with python",
      "conflict": ["This","is","a","list","containing","pack_ids","of","packs","that","conflict","with","the","current","pack"],
      "compatability": ["Same","as","conflicts","but","there","will","be","a","folder","in","the","pack","for","compatability","with","the","pack"]
    }
  ]
}
```
The folder structure should hypothetically be like this

`{topic}/{pack_id}/{compatability}`

`{topic}` is the topic from the JSON

`{pack_id}` is the pack_id from the JSON. `{pack_name}` won't be used because it has spaces in it

`{compatability}` is optional as the pack may not have compatability with other packs. This may not be the same with vanillatweaks as I can't see whether there is compatability with other packs, so I have to infer them.

That should be how the repository would be arranged.
