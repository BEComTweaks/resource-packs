function toggleSelection(element) {
    element.classList.toggle('selected');
    const checkbox = element.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
}

function toggleCategory(label) {
    const tweaksContainer = label.nextElementSibling;
    tweaksContainer.style.display = tweaksContainer.style.display != 'grid' ? 'grid' : 'none';
}

function downloadSelectedTweaks() {
    const selectedTweaks = [];
    const tweakElements = document.querySelectorAll('.tweak.selected');
    tweakElements.forEach(tweak => {
        selectedTweaks.push({
            category: tweak.dataset.category,
            name: tweak.dataset.name,
            index: parseInt(tweak.dataset.index)
        });
    });
    
    const tweaksByCategory = {
        "Aesthetic": [],
        "Colorful Slime": [],
        "Fixes and Consistency": [],
        "Fun": [],
        "HUD and GUI": [],
        "Lower and Sides": [],
        "Menu Panoramas": [],
        "More Zombies": [],
        "Parity": [],
        "Peace and Quiet": [],
        "Retro": [],
        "Terrain": [],
        "Unobtrusive": [],
        "Utility": [],
        "Variation": []
    };

    const indicesByCategory = {
        "Aesthetic": [],
        "Colorful Slime": [],
        "Fixes and Consistency": [],
        "Fun": [],
        "HUD and GUI": [],
        "Lower and Sides": [],
        "Menu Panoramas": [],
        "More Zombies": [],
        "Parity": [],
        "Peace and Quiet": [],
        "Retro": [],
        "Terrain": [],
        "Unobtrusive": [],
        "Utility": [],
        "Variation": []
    };

    selectedTweaks.forEach(tweak => {
        tweaksByCategory[tweak.category].push(tweak.name);
        indicesByCategory[tweak.category].push(tweak.index);
    });

    const jsonData = {
        "Aesthetic": {
            "packs": tweaksByCategory["Aesthetic"],
            "index": indicesByCategory["Aesthetic"]
        },
        "Colorful Slime": {
            "packs": tweaksByCategory["Colorful Slime"],
            "index": indicesByCategory["Colorful Slime"]
        },
        "Fixes and Consistency": {
            "packs": tweaksByCategory["Fixes and Consistency"],
            "index": indicesByCategory["Fixes and Consistency"]
        },
        "Fun": {
            "packs": tweaksByCategory["Fun"],
            "index": indicesByCategory["Fun"]
        },
        "HUD and GUI": {
            "packs": tweaksByCategory["HUD and GUI"],
            "index": indicesByCategory["HUD and GUI"]
        },
        "Lower and Sides": {
            "packs": tweaksByCategory["Lower and Sides"],
            "index": indicesByCategory["Lower and Sides"]
        },
        "Menu Panoramas": {
            "packs": tweaksByCategory["Menu Panoramas"],
            "index": indicesByCategory["Menu Panoramas"]
        },
        "More Zombies": {
            "packs": tweaksByCategory["More Zombies"],
            "index": indicesByCategory["More Zombies"]
        },
        "Parity": {
            "packs": tweaksByCategory["Parity"],
            "index": indicesByCategory["Parity"]
        },
        "Peace and Quiet": {
            "packs": tweaksByCategory["Peace and Quiet"],
            "index": indicesByCategory["Peace and Quiet"]
        },
        "Retro": {
            "packs": tweaksByCategory["Retro"],
            "index": indicesByCategory["Retro"]
        },
        "Terrain": {
            "packs": tweaksByCategory["Terrain"],
            "index": indicesByCategory["Terrain"]
        },
        "Unobtrusive": {
            "packs": tweaksByCategory["Unobtrusive"],
            "index": indicesByCategory["Unobtrusive"]
        },
        "Utility": {
            "packs": tweaksByCategory["Utility"],
            "index": indicesByCategory["Utility"]
        },
        "Variation": {
            "packs": tweaksByCategory["Variation"],
            "index": indicesByCategory["Variation"]
        },
        "raw": selectedTweaks.map(tweak => tweak.name)
    };

    const jsonFile = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(jsonFile);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'selected_tweaks.json');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function downloadSelectedTweaks1() {
    const selectedTweaks = [];
    const tweakElements = document.querySelectorAll('.tweak.selected');
    tweakElements.forEach(tweak => {
        selectedTweaks.push({
            category: tweak.dataset.category,
            name: tweak.dataset.name,
            index: parseInt(tweak.dataset.index)
        });
    });
    
    const tweaksByCategory = {
        "Aesthetic": [],
        "Colorful Slime": [],
        "Fixes and Consistency": [],
        "Fun": [],
        "HUD and GUI": [],
        "Lower and Sides": [],
        "Menu Panoramas": [],
        "More Zombies": [],
        "Parity": [],
        "Peace and Quiet": [],
        "Retro": [],
        "Terrain": [],
        "Unobtrusive": [],
        "Utility":[],
        "Variation": []
    };

    selectedTweaks.forEach(tweak => {
        tweaksByCategory[tweak.category].push(tweak.name);
    });

    const jsonData = {
        "Aesthetic": {
            "packs": tweaksByCategory["Aesthetic"],
            "index": tweaksByCategory["Aesthetic"].map((_, i) => i)
        },
        "Colorful Slime": {
            "packs": tweaksByCategory["Colorful Slime"],
            "index": tweaksByCategory["Colorful Slime"].map((_, i) => i)
        },
        "Fixes and Consistency": {
            "packs": tweaksByCategory["Fixes and Consistency"],
            "index": tweaksByCategory["Fixes and Consistency"].map((_, i) => i)
        },
        "Fun": {
            "packs": tweaksByCategory["Fun"],
            "index": tweaksByCategory["Fun"].map((_, i) => i)
        },
        "HUD and GUI": {
            "packs": tweaksByCategory["HUD and GUI"],
            "index": tweaksByCategory["HUD and GUI"].map((_, i) => i)
        },
        "Lower and Sides": {
            "packs": tweaksByCategory["Lower and Sides"],
            "index": tweaksByCategory["Lower and Sides"].map((_, i) => i)
        },
        "Menu Panoramas": {
            "packs": tweaksByCategory["Menu Panoramas"],
            "index": tweaksByCategory["Menu Panoramas"].map((_, i) => i)
        },
        "More Zombies": {
            "packs": tweaksByCategory["More Zombies"],
            "index": tweaksByCategory["More Zombies"].map((_, i) => i)
        },
        "Parity": {
            "packs": tweaksByCategory["Parity"],
            "index": tweaksByCategory["Parity"].map((_, i) => i)
        },
        "Peace and Quiet": {
            "packs": tweaksByCategory["Peace and Quiet"],
            "index": tweaksByCategory["Peace and Quiet"].map((_, i) => i)
        },
        "Retro": {
            "packs": tweaksByCategory["Retro"],
            "index": tweaksByCategory["Retro"].map((_, i) => i)
        },
        "Terrain": {
            "packs": tweaksByCategory["Terrain"],
            "index": tweaksByCategory["Terrain"].map((_, i) => i)
        },
        "Unobtrusive": {
            "packs": tweaksByCategory["Unobtrusive"],
            "index": tweaksByCategory["Unobtrusive"].map((_, i) => i)
        },
        "Utility": {
            "packs": tweaksByCategory["Utility"],
            "index": tweaksByCategory["Utility"].map((_, i) => i)
        },
        "Variation": {
            "packs": tweaksByCategory["Variation"],
            "index": tweaksByCategory["Variation"].map((_, i) => i)
        },
        "raw": selectedTweaks.map(tweak => tweak.name)
    };

    const jsonFile = new Blob([JSON.stringify(jsonData, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(jsonFile);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'selected_tweaks.json');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}