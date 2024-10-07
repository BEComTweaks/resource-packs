// I sleep now
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function enableSelection(element, checkbox) {
  element.classList.add("selected");
  checkbox.checked = true;
}

function disableSelection(element, checkbox) {
  element.classList.remove("selected");
  checkbox.checked = false;
}

function toggleSelection(element) {
  const checkbox = element.querySelector('input[type="checkbox"]');
  // logging
  if (checkbox.checked) {
    disableSelection(element, checkbox);
    console.log(`Unselected ${element.dataset.name}`);
  } else {
    enableSelection(element, checkbox);
    console.log(`Selected ${element.dataset.name}`);
  }
  updateSelectedTweaks();
  /*var selectedTweaks = getSelectedTweaks();
  var dataCategory = element.dataset.category;
  const selectAllElement =
    element.parentElement.parentElement.parentElement.querySelector(
      ".category-label-selectall",
    );
  if (selectedTweaks[dataCategory]["packs"].length == 0) {
    unselectAll("", selectAllElement);
  } else if (
    selectedTweaks[dataCategory]["packs"].length ==
    element.parentElement.querySelectorAll(".tweak").length
  ) {
    selectAll("", selectAllElement);
  } else {
    partialSelected(selectAllElement);
  }
  updateURL(getSelectedTweaks());*/
}

function updateSelectedTweaks() {
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
  // if selected tweaks is empty
  if (selectedTweaks.length == 0) {
    const tweakItem = document.createElement("div");
    tweakItem.className = "tweak-list-pack";
    tweakItem.textContent = "Select some packs and see them appear here!";
    document.getElementById("selected-tweaks").appendChild(tweakItem);
  }
}
// query params function
function updateURL(st) {
  for (var key in st) {
    try {
      if (st[key].packs) {
        // remove categories
        delete st[key];
      }
    } catch (e) {
      // keep raw
    }
  }
  const params = new URLSearchParams(window.location.search);
  let newUrl;
  // remove st raw if empty
  if (st["raw"].length == 0) {
    params.delete("st_raw");
    newUrl = `${window.location.pathname}`;
  } else {
    const stcomp = LZString.compressToEncodedURIComponent(JSON.stringify(st));
    params.set("st_raw", stcomp);
    newUrl = `${window.location.pathname}?${params.toString()}`;
  }
  // update url
  window.history.replaceState({}, "", newUrl);
}
// if query params already exists
const loadedparams = new URLSearchParams(window.location.search);
if (loadedparams.has("st_raw")) {
  const st = JSON.parse(
    LZString.decompressFromEncodedURIComponent(loadedparams.get("st_raw")),
  );
  processJsonData(st, "select");
}
// for people who want instant stuff
const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

function getTimeoutDuration() {
  return mediaQuery.matches ? 0 : 487.5;
}
// toggle category
function toggleCategory(label) {
  const tweaksContainer = label.parentElement.querySelector(
    ".category-controlled",
  );
  const timeoutDuration = getTimeoutDuration();
  const selectallbutton = label.nextElementSibling;
  if (tweaksContainer.style.maxHeight) {
    // close category
    tweaksContainer.style.maxHeight = null;
    selectallbutton.style.opacity = 0;
    setTimeout(() => {
      tweaksContainer.style.display = "none";
      tweaksContainer.style.paddingTop = null;
      tweaksContainer.style.paddingBottom = null;
      label.classList.remove("open");
      selectallbutton.style.display = "none";
    }, timeoutDuration); // Matches the transition duration
  } else {
    // open category
    tweaksContainer.style.display = "block";
    tweaksContainer.style.paddingTop = "7.5px";
    tweaksContainer.style.paddingBottom = "7.5px";
    label.classList.add("open");
    tweaksContainer.style.maxHeight = tweaksContainer.scrollHeight + "px";
    const outerCatLabel =
      label.parentElement.parentElement.parentElement.querySelector(
        ".category-label",
      );
    const outerCatContainer =
      label.parentElement.parentElement.parentElement.querySelector(
        ".category-controlled",
      );
    if (outerCatLabel) {
      outerCatContainer.style.maxHeight =
        outerCatContainer.scrollHeight + tweaksContainer.scrollHeight + "px";
    }
    selectallbutton.style.display = "block";
    selectallbutton.style.opacity = 1;
  }
}
// i wonder what this is for
function downloadSelectedTweaks() {
  // set min_engine_version
  var mcVersion = document.getElementById("mev").value;
  console.log(`Minimum Engine Version is set to ${mcVersion}`);
  // set pack name
  var packName = document.getElementById("fileNameInput").value;
  if (!packName) {
    packName = `BTRP-${String(Math.floor(Math.random() * 1000000)).padStart(
      6,
      "0",
    )}`;
  }
  packName = packName.replaceAll("/", "-");
  console.log(`Pack Name is set to ${packName}`);
  // get selected tweaks
  jsonData = getSelectedTweaks();
  // fetch
  fetchPack("https", jsonData, packName, mcVersion);
}
const serverip = "localhost";

function fetchPack(protocol, jsonData, packName, mcVersion) {
  // get download button
  var downloadbutton = document.getElementsByClassName(
    "download-selected-button",
  )[0];
  // For people that spam the download button
  downloadbutton.onclick = null;
  // Change between border animations
  if (protocol === "http") {
    // when attempting through http
    downloadbutton.classList.remove("s");
    downloadbutton.innerText = "Retrying with HTTP...";
  } else {
    // when attempting through https
    downloadbutton.classList.add("http");
    downloadbutton.classList.add("s");
    downloadbutton.innerText = "Fetching Pack...";
  }

  console.log("Fetching pack...");
  // fetch
  fetch(`${protocol}://${serverip}/exportResourcePack`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      packName: packName,
      mcVersion: mcVersion,
    },
    body: JSON.stringify(jsonData),
  })
    .then((response) => {
      // when the response doesnt feel good
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then(async (blob) => {
      // pack received
      console.log("Received pack!");
      downloadbutton.innerText = "Obtained pack!";
      downloadbutton.classList.remove("http");
      // When using https, remove the s class
      if (downloadbutton.classList.contains("s")) {
        downloadbutton.classList.remove("s");
      }
      // Download the file
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = `${packName}.mcpack`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      // reset button text
      await sleep(1000);
      downloadbutton.innerText = "Download Selected Tweaks";
      downloadbutton.onclick = downloadSelectedTweaks;
    })
    .catch(async (error) => {
      // when the response doesnt send
      if (protocol === "https") {
        console.error("HTTPS error, trying HTTP:", error);
        fetchPack("http", jsonData, packName, mcVersion); // Retry with HTTP
      } else {
        console.error("Error:", error);
        downloadbutton.classList.remove("http");
        downloadbutton.innerText =
          "Couldn't fetch pack. Check console for error log.";
        downloadbutton.classList.add("error");
        await sleep(3000);
        downloadbutton.classList.remove("error");
        downloadbutton.innerText = "Download Selected Tweaks";
        downloadbutton.onclick = downloadSelectedTweaks;
      }
    });
}

// process json data from url/json
function processJsonData(jsonData, dowhat) {
  const rawPacks = jsonData.raw;

  if (Array.isArray(rawPacks)) {
    rawPacks.forEach(function (pack) {
      const div = document.querySelector(`div.tweak[data-name="${pack}"]`);
      if (div) {
        if (dowhat == "select") {
          enableSelection(div, div.querySelector('input[type="checkbox"]'));
          console.log(`Selected ${pack}`);
        } else if (dowhat == "unselect") {
          disableSelection(div, div.querySelector('input[type="checkbox"]'));
          console.log(`Unselected ${pack}`);
        }
      } else {
        console.error(`Div with data-name="${pack}" not found.`);
      }
    });
  } else {
    console.error("The 'raw' field in selected_packs.json is not an array.");
  }
  updateSelectedTweaks();
}
// get selected tweaks
function getSelectedTweaks() {
  const selectedTweaks = [];
  const tweakElements = document.querySelectorAll(".tweak.selected");
  tweakElements.forEach((tweak) => {
    selectedTweaks.push({
      category: tweak.dataset.category,
      name: tweak.dataset.name,
      index: parseInt(tweak.dataset.index),
    });
  });
  // yza should explain this
  const tweaksByCategory = {
    Aesthetic: [],
    "More Zombies": [],
    Terrain: [],
    "Lower and Sides": [],
    Variation: [],
    "Peace and Quiet": [],
    Mobs: [],
    Utility: [],
    Directional: [],
    "Growth Stages": [],
    Unobtrusive: [],
    "3D": [],
    GUI: [],
    Crosshairs: [],
    Hearts: [],
    "LGBTQ+ Pride": [],
    "Hunger Bars": [],
    "Hotbar Selector": [],
    "Menu Panoramas": [],
    "Xisuma's Hermitcraft Bases": [],
    Retro: [],
    Fun: [],
    "World of Color": [],
    "Colorful Slime": [],
    Elytra: [],
    Parity: [],
    "Fixes and Consistency": [],
  };

  const indicesByCategory = {
    Aesthetic: [],
    "More Zombies": [],
    Terrain: [],
    "Lower and Sides": [],
    Variation: [],
    "Peace and Quiet": [],
    Mobs: [],
    Utility: [],
    Directional: [],
    "Growth Stages": [],
    Unobtrusive: [],
    "3D": [],
    GUI: [],
    Crosshairs: [],
    Hearts: [],
    "LGBTQ+ Pride": [],
    "Hunger Bars": [],
    "Hotbar Selector": [],
    "Menu Panoramas": [],
    "Xisuma's Hermitcraft Bases": [],
    Retro: [],
    Fun: [],
    "World of Color": [],
    "Colorful Slime": [],
    Elytra: [],
    Parity: [],
    "Fixes and Consistency": [],
  };
  console.log("Obtaining selected tweaks...");
  selectedTweaks.forEach((tweak) => {
    tweaksByCategory[tweak.category].push(tweak.name);
    indicesByCategory[tweak.category].push(tweak.index);
  });
  console.log("Obtained!");
  const jsonData = {
    Aesthetic: {
      packs: tweaksByCategory["Aesthetic"],
      index: indicesByCategory["Aesthetic"],
    },
    "More Zombies": {
      packs: tweaksByCategory["More Zombies"],
      index: indicesByCategory["More Zombies"],
    },
    Terrain: {
      packs: tweaksByCategory["Terrain"],
      index: indicesByCategory["Terrain"],
    },
    "Lower and Sides": {
      packs: tweaksByCategory["Lower and Sides"],
      index: indicesByCategory["Lower and Sides"],
    },
    Variation: {
      packs: tweaksByCategory["Variation"],
      index: indicesByCategory["Variation"],
    },
    "Peace and Quiet": {
      packs: tweaksByCategory["Peace and Quiet"],
      index: indicesByCategory["Peace and Quiet"],
    },
    Mobs: {
      packs: tweaksByCategory["Mobs"],
      index: indicesByCategory["Mobs"],
    },
    Utility: {
      packs: tweaksByCategory["Utility"],
      index: indicesByCategory["Utility"],
    },
    Directional: {
      packs: tweaksByCategory["Directional"],
      index: indicesByCategory["Directional"],
    },
    "Growth Stages": {
      packs: tweaksByCategory["Growth Stages"],
      index: indicesByCategory["Growth Stages"],
    },
    Unobtrusive: {
      packs: tweaksByCategory["Unobtrusive"],
      index: indicesByCategory["Unobtrusive"],
    },
    "3D": {
      packs: tweaksByCategory["3D"],
      index: indicesByCategory["3D"],
    },
    GUI: {
      packs: tweaksByCategory["GUI"],
      index: indicesByCategory["GUI"],
    },
    Crosshairs: {
      packs: tweaksByCategory["Crosshairs"],
      index: indicesByCategory["Crosshairs"],
    },
    Hearts: {
      packs: tweaksByCategory["Hearts"],
      index: indicesByCategory["Hearts"],
    },
    "LGBTQ+ Pride": {
      packs: tweaksByCategory["LGBTQ+ Pride"],
      index: indicesByCategory["LGBTQ+ Pride"],
    },
    "Hunger Bars": {
      packs: tweaksByCategory["Hunger Bars"],
      index: indicesByCategory["Hunger Bars"],
    },
    "Hotbar Selector": {
      packs: tweaksByCategory["Hotbar Selector"],
      index: indicesByCategory["Hotbar Selector"],
    },
    "Menu Panoramas": {
      packs: tweaksByCategory["Menu Panoramas"],
      index: indicesByCategory["Menu Panoramas"],
    },
    "Xisuma's Hermitcraft Bases": {
      packs: tweaksByCategory["Xisuma's Hermitcraft Bases"],
      index: indicesByCategory["Xisuma's Hermitcraft Bases"],
    },
    Retro: {
      packs: tweaksByCategory["Retro"],
      index: indicesByCategory["Retro"],
    },
    Fun: {
      packs: tweaksByCategory["Fun"],
      index: indicesByCategory["Fun"],
    },
    "World of Color": {
      packs: tweaksByCategory["World of Color"],
      index: indicesByCategory["World of Color"],
    },
    "Colorful Slime": {
      packs: tweaksByCategory["Colorful Slime"],
      index: indicesByCategory["Colorful Slime"],
    },
    Elytra: {
      packs: tweaksByCategory["Elytra"],
      index: indicesByCategory["Elytra"],
    },
    Parity: {
      packs: tweaksByCategory["Parity"],
      index: indicesByCategory["Parity"],
    },
    "Fixes and Consistency": {
      packs: tweaksByCategory["Fixes and Consistency"],
      index: indicesByCategory["Fixes and Consistency"],
    },
    raw: selectedTweaks.map((tweak) => tweak.name),
  };
  return jsonData;
}
// Extra code to trigger file input
document
  .querySelector(".zipinputcontainer")
  .addEventListener("click", function () {
    document.getElementById("zipInput").click();
  });
// upload pack
document
  .getElementById("zipInput")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        JSZip.loadAsync(e.target.result)
          .then(function (zip) {
            let fileFound = false;

            zip.forEach(function (relativePath, zipEntry) {
              if (relativePath.endsWith("selected_packs.json")) {
                fileFound = true;
                zipEntry
                  .async("string")
                  .then(function (content) {
                    try {
                      const jsonData = JSON.parse(content);
                      processJsonData(jsonData, "select");
                    } catch (error) {
                      console.error("Error parsing JSON:", error);
                    }
                  })
                  .catch(function (error) {
                    console.error(
                      "Error extracting selected_packs.json:",
                      error,
                    );
                  });
              }
            });

            if (!fileFound) {
              console.error(
                "selected_packs.json not found in any folder within the ZIP file.",
              );
            }
          })
          .catch(function (error) {
            console.error("Error reading the ZIP file:", error);
          });
      };
      reader.readAsArrayBuffer(file);
    } else {
      console.error("No file selected.");
    }
  });

// select all tweaks
function selectAll(compressedstring, element) {
  if (compressedstring != "") {
    const st = JSON.parse(
      LZString.decompressFromEncodedURIComponent(compressedstring),
    );
    processJsonData(st, "select");
    updateURL(st);
    element.onclick = function () {
      unselectAll(compressedstring, element);
    };
  }
  element.innerHTML =
    '<img src="images/select-all-button/chiseled_bookshelf_occupied.png" class="category-label-selectall-img"><div class="category-label-selectall-hovertext">Unselect All</div>';
}

function partialSelected(element) {
  element.innerHTML =
    '<img src="images/select-all-button/chiseled_bookshelf_has_selected.png" class="category-label-selectall-img"><div class="category-label-selectall-hovertext">Select All</div>';
  const compressedstring = element.onclick.toString().split("'")[1];
  element.onclick = function () {
    selectAll(compressedstring, element);
  };
}

function unselectAll(compressedstring, element) {
  if (compressedstring != "") {
    const st = JSON.parse(
      LZString.decompressFromEncodedURIComponent(compressedstring),
    );
    processJsonData(st, "unselect");
    updateURL(st);
    element.onclick = function () {
      selectAll(compressedstring, element);
    };
  }
  element.innerHTML =
    '<img src="images/select-all-button/chiseled_bookshelf_empty.png" class="category-label-selectall-img"><div class="category-label-selectall-hovertext">Select All</div>';
}
