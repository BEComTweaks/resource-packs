function toggleSelection(element) {
  element.classList.toggle("selected");
  const checkbox = element.querySelector('input[type="checkbox"]');
  checkbox.checked = !checkbox.checked;
  var selectedTweaks = [];
  const tweakElements = document.querySelectorAll(".tweak.selected");
  tweakElements.forEach((tweak) => {
    const labelElement = tweak.querySelector(".tweak-info .tweak-title");
    selectedTweaks.push("**" + tweak.dataset.category);
    selectedTweaks.push(labelElement.textContent);
  });
  selectedTweaks = [...new Set(selectedTweaks)];
  document.getElementById("selected-tweaks").innerHTML = ""; // Clear the container
  selectedTweaks.forEach((tweak) => {
    const tweakItem = document.createElement("div");
    if (tweak.includes("**")) {
      // tweakItem.className = ("tweakListCategory")
      var label = document.createElement("label");
      tweak = tweak.substring(2);
      label.textContent = tweak;
      label.className = "tweak-list-category";
      tweakItem.append(label);
    } else {
      tweakItem.className = "tweak-list-pack";
      tweakItem.textContent = tweak;
    }
    document.getElementById("selected-tweaks").appendChild(tweakItem);
  });
  console.log(selectedTweaks.length);
  if (selectedTweaks.length == 0) {
    const tweakItem = document.createElement("div");
    tweakItem.className = "tweak-list-pack";
    tweakItem.textContent = "Select some packs and see them appear here!";
    document.getElementById("selected-tweaks").appendChild(tweakItem);
  }
}

window.addEventListener("resize", () => {
  if (window.matchMedia("(max-width: 767px)").matches) {
    document.getElementById("selected-tweaks").style.display = "none";
  } else {
    document.getElementById("selected-tweaks").style.display = "block";
  }
});

function toggleSubCategory(label) {
  const tweaksContainer = label.nextElementSibling;
  tweaksContainer.style.display =
    tweaksContainer.style.display != "grid" ? "grid" : "none";
}

function toggleCategory(label) {
  const tweaksContainer = label.nextElementSibling;
  tweaksContainer.style.display =
    tweaksContainer.style.display != "block" ? "block" : "none";
}

function downloadSelectedTweaks() {
  var packName = document.getElementById("fileNameInput").value;
  if (!packName) {
    packName = `BTRP-${String(Math.floor(Math.random() * 1000000)).padStart(
      6,
      "0",
    )}`;
  }
  packName = packName.replaceAll("/", "-");
  const selectedTweaks = [];
  const tweakElements = document.querySelectorAll(".tweak.selected");
  tweakElements.forEach((tweak) => {
    selectedTweaks.push({
      category: tweak.dataset.category,
      name: tweak.dataset.name,
      index: parseInt(tweak.dataset.index),
    });
  });

  const tweaksByCategory = {
    "3D": [],
    Aesthetic: [],
    Crosshairs: [],
    "Colorful Slime": [],
    "Fixes and Consistency": [],
    Fun: [],
    GUI: [],
    "Lower and Sides": [],
    "Menu Panoramas": [],
    "More Zombies": [],
    Parity: [],
    "Peace and Quiet": [],
    Retro: [],
    Terrain: [],
    Unobtrusive: [],
    Utility: [],
    Variation: [],
    "World of Color": [],
  };

  const indicesByCategory = {
    "3D": [],
    Aesthetic: [],
    Crosshairs: [],
    "Colorful Slime": [],
    "Fixes and Consistency": [],
    Fun: [],
    GUI: [],
    "Lower and Sides": [],
    "Menu Panoramas": [],
    "More Zombies": [],
    Parity: [],
    "Peace and Quiet": [],
    Retro: [],
    Terrain: [],
    Unobtrusive: [],
    Utility: [],
    Variation: [],
    "World of Color": [],
  };

  selectedTweaks.forEach((tweak) => {
    tweaksByCategory[tweak.category].push(tweak.name);
    indicesByCategory[tweak.category].push(tweak.index);
  });

  const jsonData = {
    "3D": {
      packs: tweaksByCategory["3D"],
      index: indicesByCategory["3D"],
    },
    Aesthetic: {
      packs: tweaksByCategory["Aesthetic"],
      index: indicesByCategory["Aesthetic"],
    },
    Crosshairs: {
      packs: tweaksByCategory["Crosshairs"],
      index: indicesByCategory["Crosshairs"],
    },
    "Colorful Slime": {
      packs: tweaksByCategory["Colorful Slime"],
      index: indicesByCategory["Colorful Slime"],
    },
    "Fixes and Consistency": {
      packs: tweaksByCategory["Fixes and Consistency"],
      index: indicesByCategory["Fixes and Consistency"],
    },
    Fun: {
      packs: tweaksByCategory["Fun"],
      index: indicesByCategory["Fun"],
    },
    GUI: {
      packs: tweaksByCategory["GUI"],
      index: indicesByCategory["GUI"],
    },
    "Lower and Sides": {
      packs: tweaksByCategory["Lower and Sides"],
      index: indicesByCategory["Lower and Sides"],
    },
    "Menu Panoramas": {
      packs: tweaksByCategory["Menu Panoramas"],
      index: indicesByCategory["Menu Panoramas"],
    },
    "More Zombies": {
      packs: tweaksByCategory["More Zombies"],
      index: indicesByCategory["More Zombies"],
    },
    Parity: {
      packs: tweaksByCategory["Parity"],
      index: indicesByCategory["Parity"],
    },
    "Peace and Quiet": {
      packs: tweaksByCategory["Peace and Quiet"],
      index: indicesByCategory["Peace and Quiet"],
    },
    Retro: {
      packs: tweaksByCategory["Retro"],
      index: indicesByCategory["Retro"],
    },
    Terrain: {
      packs: tweaksByCategory["Terrain"],
      index: indicesByCategory["Terrain"],
    },
    Unobtrusive: {
      packs: tweaksByCategory["Unobtrusive"],
      index: indicesByCategory["Unobtrusive"],
    },
    Utility: {
      packs: tweaksByCategory["Utility"],
      index: indicesByCategory["Utility"],
    },
    Variation: {
      packs: tweaksByCategory["Variation"],
      index: indicesByCategory["Variation"],
    },
    "World of Color": {
      packs: tweaksByCategory["World of Color"],
      index: indicesByCategory["World of Color"],
    },
    raw: selectedTweaks.map((tweak) => tweak.name),
  };
  fetchPack("https", jsonData, packName);
}
const serverip = "localhost";

function fetchPack(protocol, jsonData, packName) {
  fetch(`${protocol}://${serverip}/exportResourcePack`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      packName: packName,
    },
    body: JSON.stringify(jsonData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = `${packName}.mcpack`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      if (protocol === "https") {
        console.error("HTTPS error, trying HTTP:", error);
        fetchPack("http", jsonData, packName); // Retry with HTTP
      } else {
        console.error("Error:", error);
      }
    });
}
