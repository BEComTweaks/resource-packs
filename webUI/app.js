/************\
| OreUI HTML |
\************/

const OreUI = {
  becomeActive: function (element) {
    element.setAttribute("oreui-state", "active");
  },
  becomeInactive: function (element) {
    element.setAttribute("oreui-state", "inactive");
  },
  toggleActive: function (element) {
    if (element.getAttribute("oreui-state") === "active") {
      element.setAttribute("oreui-state", "inactive");
    } else {
      element.setAttribute("oreui-state", "active");
    }
  },
  becomeDisabled: function (element) {
    element.setAttribute("disabled", true);
  },
  becomeEnabled: function (element) {
    element.removeAttribute("disabled");
  },
  toggleDisabled: function (element) {
    if (element.hasAttribute("disabled")) {
      element.removeAttribute("disabled");
    } else {
      element.setAttribute("disabled", true);
    }
  },
  getCurrentState: function (element) {
    if (element.hasAttribute("disabled")) {
      return "disabled";
    } else if (element.hasAttribute("oreui-state")) {
      return element.getAttribute("oreui-state");
    } else {
      return "inactive";
    }
  },
  isActive: function (element) {
    if (element.hasAttribute("oreui-state")) {
      return element.getAttribute("oreui-state") === "active";
    } else {
      return false;
    }
  },
  isDisabled: function (element) {
    if (element.hasAttribute("disabled")) {
      return element.getAttribute("disabled") === "true";
    } else {
      return false;
    }
  },
  getColor: function (element) {
    return element.getAttribute("oreui-color");
  },
  getActiveColor: function (element) {
    if (element.hasAttribute("oreui-active-color")) {
      return element.getAttribute("oreui-active-color");
    } else {
      return element.getAttribute("oreui-color");
    }
  },
  getDisabledColor: function (element) {
    if (element.hasAttribute("oreui-disabled-color")) {
      return element.getAttribute("oreui-disabled-color");
    } else {
      return "dark";
    }
  },
  setColor: function (element, color) {
    element.setAttribute("oreui-color", color);
  },
  setActiveColor: function (element, color) {
    element.setAttribute("oreui-active-color", color);
  },
  setDisabledColor: function (element, color) {
    element.setAttribute("oreui-disabled-color", color);
  },
};

window.OreUI = OreUI;

/************\
| Search Bar |
\************/

document.addEventListener("click", filterPacks);
function filterPacks() {
  const query = document.getElementById("searchBar").value.toLowerCase().trim();
  const resultsDiv = document.getElementById("searchResults");

  if (query === "") {
    if (resultsDiv.hasAttribute("hasMatches")) {
      resultsDiv.removeAttribute("hasMatches");
    }
    resultsDiv.innerHTML = "";
    return;
  }

  const packs = document.querySelectorAll(".tweak");
  let matches = [];

  packs.forEach((pack, index) => {
    const title = pack.querySelector(".tweak-title").textContent;
    const description = pack.querySelector(".tweak-description").textContent;
    const icon = pack.querySelector("img").src;
    const isSelected = pack.querySelector("input[type='checkbox']").checked; // Check selection state

    if (
      title.toLowerCase().includes(query) ||
      description.toLowerCase().includes(query)
    ) {
      matches.push({
        title,
        description,
        icon,
        isSelected, // Track selection state
        packIndex: index, // Keep track of the original pack's index
      });
    }
  });

  if (matches.length === 0) {
    if (resultsDiv.hasAttribute("hasMatches")) {
      resultsDiv.removeAttribute("hasMatches");
    }
    resultsDiv.innerHTML = "";
  } else {
    if (matches.length > 5) matches = matches.slice(0, 5);
    resultsDiv.setAttribute("hasMatches", true);
    resultsDiv.innerHTML = matches
      .map(
        (match) => `
      <div
        ${match.isSelected ? 'oreui-state="active"' : ""}
        class="search-result-item"
        onclick="triggerPackClick(${match.packIndex})"
        style="cursor: pointer;"
        oreui-type="button"
        oreui-color="dark"
        oreui-active-color="green"
      >
        <img src="${match.icon}" alt="${match.title.trim()}" style="width: 48px; height: 48px;" />
        <div>
          <strong>${match.title}</strong>
          <p>${match.description}</p>
        </div>
      </div>
    `,
      )
      .join("");
  }
}

function triggerPackClick(index) {
  // Simulate a click on the corresponding pack
  const packs = document.querySelectorAll(".tweak");
  if (packs[index]) {
    packs[index].click();
  }
}

/******************\
| Custom functions |
\******************/
const lodash = _.noConflict();

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function enableSelection(element, checkbox) {
  OreUI.becomeActive(element);
  checkbox.checked = true;
}

function disableSelection(element, checkbox) {
  OreUI.becomeInactive(element);
  checkbox.checked = false;
}

function toggleSelection(element) {
  const checkbox = element.querySelector('input[type="checkbox"]');
  if (checkbox.checked) {
    disableSelection(element, checkbox);
    console.log(
      `[%cselection%c]\nUnselected ${element.dataset.name}`,
      "color: green",
      "color: initial",
    );
  } else {
    enableSelection(element, checkbox);
    console.log(
      `[%cselection%c]\nSelected ${element.dataset.name}`,
      "color: green",
      "color: initial",
    );
  }
  updateSelectedTweaks();
  var selectedTweaks = getSelectedTweaks();
  updateSelectAllButton(selectedTweaks);
  updateURL(selectedTweaks);
  updateDownloadButton(selectedTweaks);
}

function updateDownloadButton(st) {
  const downloadButton = document.querySelector(".download-selected-button");
  if (st["raw"].length == 0) {
    downloadButton.disabled = true;
  } else {
    downloadButton.disabled = false;
  }
}

function updateSelectAllButton(st) {
  document
    .querySelectorAll(".category-label-selectall")
    .forEach((selectallbutton) => {
      const imgElement = selectallbutton.querySelector(
        ".category-label-selectall-img",
      );
      const hoverTextElement = selectallbutton.querySelector(
        ".category-label-selectall-hovertext",
      );
      const category = selectallbutton.dataset.category;
      if (st[category].length == 0) {
        imgElement.src =
          "images/select-all-button/chiseled_bookshelf_empty.png";
        hoverTextElement.textContent = "Select All";
        selectallbutton.onclick = new Function(`selectAll(this);`);
      } else if (
        st[category].length ==
        selectallbutton.parentElement.querySelectorAll(".tweak").length
      ) {
        imgElement.src =
          "images/select-all-button/chiseled_bookshelf_occupied.png";
        hoverTextElement.textContent = "Unselect All";
        selectallbutton.onclick = new Function(`unselectAll(this);`);
      } else {
        imgElement.src =
          "images/select-all-button/chiseled_bookshelf_has_selected.png";
        hoverTextElement.textContent = "Select All";
        selectallbutton.onclick = new Function(`selectAll(this);`);
      }
    });
}

function updateSelectedTweaks() {
  var selectedTweaks = [];
  const tweakElements = document.querySelectorAll(
    ".tweak[oreui-state='active']",
  );
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
      if (key !== "raw") {
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
  updateDownloadButton(st);
  const preselectAlerter = document.getElementsByClassName("preselected")[0];
  sleep(500).then(() => {
    // slow down before showing the alert
    preselectAlerter.style.top = "20vh";
  });
  sleep(5000).then(() => {
    preselectAlerter.style.top = "-20vh";
  });
}

function getTimeoutDuration() {
  // for people who want instant stuff
  const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
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
      selectallbutton.style.display = "none";
    }, timeoutDuration); // Matches the transition duration
  } else {
    // open category
    tweaksContainer.style.display = "block";
    tweaksContainer.style.maxHeight = tweaksContainer.scrollHeight + "px";
    selectallbutton.style.display = "block";
    selectallbutton.style.opacity = 1;
    // change height to match outer categories
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
  }
}

/* test */
function downloadSelectedTweaks() {
  // set min_engine_version
  var mcVersion = document.getElementById("mev").value;
  console.log(
    `[%cdownload%c]\nMinimum Engine Version is set to ${mcVersion}`,
    "color: cyan",
    "color: initial",
  );
  // set pack name
  var packName = document.getElementById("fileNameInput").value;
  if (!packName) {
    packName = `BTRP-${String(Math.floor(Math.random() * 1000000)).padStart(
      6,
      "0",
    )}`;
  }
  packName = packName.replaceAll("/", "-");
  console.log(
    `[%cdownload%c]\nPack Name is set to ${packName}`,
    "color: cyan",
    "color: initial",
  );
  // get selected tweaks
  jsonData = getSelectedTweaks();
  // fetch
  fetchPack(jsonData, packName, mcVersion);
}

const root_url = "..";
const listofcategories = [
  "Aesthetic",
  "Terrain",
  "Variation",
  "Peace and Quiet",
  "Utility",
  "Unobtrusive",
  "3D",
  "GUI",
  "Menu Panoramas",
  "Retro",
  "Fun",
  "World of Color",
  "Parity",
  "Fixes and Consistency",
  "More Zombies",
  "Lower and Sides",
  "Mobs",
  "Directional",
  "Growth Stages",
  "Crosshairs",
  "Hearts",
  "LGBTQ+ Pride",
  "Hunger Bars",
  "Hotbar Selector",
  "Xisuma's Hermitcraft Bases",
  "Colorful Slime",
  "Elytra",
  "Enchantment Glints",
];

async function fetchPack(jsonData, packName, mcVersion) {
  console.log("[%cfetch%c]\nMaking pack...", "color: blue", "color: initial");
  const downloadbutton = document.getElementsByClassName(
    "download-selected-button",
  )[0];
  downloadbutton.onclick = null;
  downloadbutton.innerText = "Fetching Pack...";
  OreUI.becomeActive(downloadbutton);
  const zip = new JSZip();
  const files = [];
  const file_content = [];
  const filePriorities = [];
  const rploc = {};
  let rpmf = {};

  try {
    const idToNameResponse = await fetch(
      `${root_url}/jsons/map/id_to_name.json`,
    );
    if (!idToNameResponse.ok) {
      throw new Error("Failed to fetch id_to_name.json");
    }
    const idToName = await idToNameResponse.json();
    console.log(
      "[%cfetch%c] Fetched id_to_name.json",
      "color: blue",
      "color: initial",
    );

    const manifestResponse = await fetch(
      `${root_url}/jsons/others/manifest.json`,
    );
    if (!manifestResponse.ok) {
      throw new Error("Failed to fetch manifest.json");
    }
    var manifest = await manifestResponse.json();
    manifest.header.name = packName;
    manifest.header.min_engine_version = mcVersion.split(".").map(Number);
    manifest.header.uuid = uuid.v4();
    let description = "Selected Packs:\n";
    listofcategories.forEach((category) => {
      if (jsonData[category] && jsonData[category].length > 0) {
        description += ` - ${category}\n`;
        jsonData[category].forEach((pack) => {
          description += `\t - ${idToName[pack]}\n`;
        });
      }
    });
    manifest.header.description = description.trim();
    files.push("manifest.json");
    file_content.push(JSON.stringify(manifest, null, 2));
    filePriorities.push(999);
    console.log(
      "[%cfetch%c] Fetched manifest.json",
      "color: blue",
      "color: initial",
    );
    downloadbutton.innerText = "manifest.json";
    rpmf = manifest;
    rpmf.modules[0].type = "resources";
    rpmf.modules[0].uuid = uuid.v4();
    rpmf.header.uuid = uuid.v4();

    const packIconResponse = await fetch(
      `${root_url}/pack_icons/pack_icon.png`,
    );
    if (!packIconResponse.ok) {
      throw new Error("Failed to fetch pack_icon.png");
    }
    const packIconBlob = await packIconResponse.blob();
    zip.file("pack_icon.png", packIconBlob);
    files.push("pack_icon.png");
    file_content.push(undefined);
    filePriorities.push(999);
    rploc["pack_icon"] = file_content.indexOf(packIconBlob);
    console.log(
      "[%cfetch%c] Fetched pack_icon.png",
      "color: blue",
      "color: initial",
    );
    downloadbutton.innerText = "pack_icon.png";

    files.push("selected_packs.json");
    file_content.push(JSON.stringify(jsonData, null, 2));
    rploc["selected_packs"] = files.indexOf("selected_packs.json");
    filePriorities.push(999);
    downloadbutton.innerText = "selected_packs.json";

    const compatibilitiesResponse = await fetch(
      `${root_url}/jsons/packs/compatibilities.json`,
    );
    if (!compatibilitiesResponse.ok) {
      throw new Error("Failed to fetch compatibilities.json");
    }
    const compatibilities = await compatibilitiesResponse.json();
    const incompleteCompatibilitiesResponse = await fetch(
      `${root_url}/jsons/others/incomplete_compatibilities.json`,
    );
    if (!incompleteCompatibilitiesResponse.ok) {
      throw new Error("Failed to fetch incomplete_compatibilities.json");
    }
    const inComp = await incompleteCompatibilitiesResponse.json();
    const compatloc = [];
    let i = compatibilities.maxway + 1;
    while (i > 2) {
      i = i - 1;
      compatibilities[`${i}way`].compatibilities.forEach(
        (listofcompatibilities, index) => {
          let doesnthave = false;
          listofcompatibilities.forEach((pack) => {
            if (jsonData["raw"].indexOf(pack) == -1) {
              doesnthave = true;
            }
          });
          const location = compatibilities[`${i}way`].locations[index];
          console.log(location);
          if (inComp[`${i}way`] !== undefined) {
            console.log("inside by one");
            if (!doesnthave && inComp[`${i}way`].indexOf(location) == -1) {
              compatloc.push(location);
              listofcompatibilities.forEach((pack) => {
                jsonData["raw"].splice(jsonData["raw"].indexOf(pack), 1);
              });
              console.log(
                `[%cfetch%c]\nAdded ${i}way compatibility for ${listofcompatibilities}`,
                "color: blue",
                "color: initial",
              );
            }
          } else if (!doesnthave) {
            compatloc.push(location);
            listofcompatibilities.forEach((pack) => {
              jsonData["raw"].splice(jsonData["raw"].indexOf(pack), 1);
            });
            console.log(
              `[%cfetch%c]\nAdded ${i}way compatibility for ${listofcompatibilities}`,
              "color: blue",
              "color: initial",
            );
          }
        },
      );
    }
    const priorityResponse = await fetch(`${root_url}/jsons/map/priority.json`);
    if (!priorityResponse.ok) {
      throw new Error("Failed to fetch priority.json");
    }
    const priorityMap = await priorityResponse.json();

    for (const cats of listofcategories) {
      for (const pack of jsonData[cats]) {
        if (jsonData["raw"].indexOf(pack) !== -1) {
          for (const pack of jsonData[cats]) {
            if (jsonData["raw"].indexOf(pack) !== -1) {
              console.log(
                `${root_url}/packs/${cats.toLowerCase()}/${pack}/list.json`,
              );
              const listResponse = await fetch(
                `${root_url}/packs/${cats.toLowerCase()}/${pack}/list.json`,
              );
              if (!listResponse.ok) {
                throw new Error("Failed to fetch list.json");
              }
              const listJson = await listResponse.json();
              for (const fileloc of listJson) {
                const fileResponse = await fetch(
                  `${root_url}/packs/${cats.toLowerCase()}/${pack}/files/${fileloc}`,
                );
                if (!fileResponse.ok) {
                  throw new Error(`Failed to fetch file: ${fileloc}`);
                }
                console.log(
                  `[%cfetch%c]\n${fileloc}`,
                  "color: blue",
                  "color: initial",
                );
                downloadbutton.innerText = fileloc.split("/").pop();
                console.log(fileResponse.headers.get("content-type"));
                if (
                  fileResponse.headers
                    .get("content-type")
                    .includes("application") ||
                  fileResponse.headers.get("content-type").includes("text")
                ) {
                  const text = await fileResponse.text();
                  files.push(fileloc);
                  file_content.push(text);
                  filePriorities.push(priorityMap[pack]);
                } else if (files.indexOf(fileloc) === -1) {
                  files.push(fileloc);
                  zip.file(fileloc, await fileResponse.blob());
                  file_content.push(undefined);
                  filePriorities.push(priorityMap[pack]);
                } else if (
                  priorityMap[pack] > filePriorities[files.indexOf(fileloc)]
                ) {
                  zip.remove(fileloc);
                  zip.file(fileloc, await fileResponse.blob());
                  filePriorities[files.indexOf(fileloc)] = priorityMap[pack];
                  console.log(
                    `Priority of ${fileloc} updated to ${priorityMap[pack]}`,
                  );
                }
              }
            }
          }
        }
      }
    }
    var compatFetchPromises = [];
    for (const loc of compatloc) {
      compatFetchPromises.push(
        (async () => {
          const listResponse = await fetch(
            `${root_url}/packs/${loc}/list.json`,
          );
          if (!listResponse.ok) {
            throw new Error("Failed to fetch list.json");
          }
          const listJson = await listResponse.json();
          const fileFetchPromises = listJson.map(async (fileloc) => {
            const fileResponse = await fetch(
              `${root_url}/packs/${loc}/files/${fileloc}`,
            );
            if (!fileResponse.ok) {
              throw new Error(`Failed to fetch file: ${fileloc}`);
            }
            console.log(
              `[%cfetch%c]\n${fileloc}`,
              "color: blue",
              "color: initial",
            );
            downloadbutton.innerText = fileloc.split("/").pop();
            if (
              fileResponse.headers
                .get("content-type")
                .includes("application") ||
              fileResponse.headers.get("content-type").includes("text")
            ) {
              const text = await fileResponse.text();
              files.push(fileloc);
              file_content.push(text);
              filePriorities.push(priorityMap[loc]);
            } else {
              zip.file(fileloc, await fileResponse.blob());
              if (files.indexOf(fileloc) == -1) {
                files.push(fileloc);
                file_content.push(undefined);
                filePriorities.push(999); // its compatibilities anyways, so highest priority
              } else {
                filePriorities[files.indexOf(fileloc)] = 999;
              }
            }
          });
          await Promise.all(fileFetchPromises);
        })(),
      );
    }
    await Promise.all(compatFetchPromises);

    console.log(files);
    downloadbutton.innerText = "Zipping Up";
    var completedFiles = [];
    var completedFilesContent = [];
    let manifestfromfiles = {};
    /* duplicate checker */
    files.forEach((file, index) => {
      console.log(file);
      console.log(file_content[index]);
      if (file_content[index] === undefined) {
        console.log("nah not today");
        return; // its added already wdym
      } else if (completedFiles.indexOf(file) === -1) {
        completedFiles.push(file);
        completedFilesContent.push(file_content[index]);
      } else if (file.endsWith(".json")) {
        const addedFileIndex = completedFiles.indexOf(file);
        const addedJSON = JSON.parse(completedFilesContent[addedFileIndex]);
        const toAddJSON = JSON.parse(file_content[index]);
        const mergedJSON = lodash.merge(addedJSON, toAddJSON);
        completedFilesContent[addedFileIndex] = JSON.stringify(
          mergedJSON,
          null,
          2,
        );
      } else if (
        file.includes(".mc") ||
        file.endsWith(".js") ||
        file.endsWith(".bak") ||
        file.endsWith(".txt") ||
        file.endsWith(".lang")
      ) {
        const addedFileIndex = completedFiles.indexOf(file);
        completedFilesContent[addedFileIndex] += "\n" + file_content[index];
      }
    });
    console.log(completedFiles);
    /* add the files to zip now */
    completedFiles.forEach((file, index) => {
      if (file === "manifest.json") {
        manifestfromfiles = JSON.parse(completedFilesContent[index]);
      }
      zip.file(file, completedFilesContent[index]);
    });
    manifest = lodash.merge(manifest, manifestfromfiles);
    manifest.modules.forEach((module) => {
      module.uuid = uuid.v4();
    });
    zip.file("manifest.json", JSON.stringify(manifest, null, 2));
    const blob = await zip.generateAsync({ type: "blob" });
    console.log(
      "[%cfetch%c]\nFinished fetches",
      "color: blue",
      "color: initial",
    );
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = `${packName}.zip`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    downloadbutton.innerText = "Download Selected Tweaks";
    downloadbutton.onclick = downloadSelectedTweaks;
    OreUI.becomeInactive(downloadbutton);
  } catch (error) {
    console.error("Error during fetch or processing:", error);
  }
}

// process json data from url/json
function processJsonData(jsonData, dowhat) {
  const rawPacks = jsonData.raw;

  if (Array.isArray(rawPacks)) {
    rawPacks.forEach(function (pack) {
      const div = document.querySelector(`div.tweak[data-name="${pack}"]`);
      if (div) {
        if (dowhat == "select") {
          if (!div.querySelector('input[type="checkbox"]').checked) {
            enableSelection(div, div.querySelector('input[type="checkbox"]'));
            console.log(
              `[%cmass%c]\nSelected ${pack}`,
              "color: green",
              "color: initial",
            );
          }
        } else if (dowhat == "unselect") {
          if (div.querySelector('input[type="checkbox"]').checked) {
            disableSelection(div, div.querySelector('input[type="checkbox"]'));
            console.log(
              `[%cmass%c]\nUnselected ${pack}`,
              "color: green",
              "color: initial",
            );
          }
        }
      } else {
        console.log(
          `[%cerror%c]\nDiv with data-name="${pack}" not found.`,
          "color: red",
          "color: initial",
        );
      }
    });
  } else {
    console.log(
      "[%cerror%c]\n%cThe 'raw' field in selected_packs.json is not an array.",
      "color: red",
      "color: initial",
    );
  }
  updateSelectedTweaks();
  const st = getSelectedTweaks();
  updateSelectAllButton(st);
  updateURL(st);
  updateDownloadButton(st);
}
// get selected tweaks
function getSelectedTweaks() {
  const selectedTweaks = [];
  const tweakElements = document.querySelectorAll(
    ".tweak[oreui-state='active']",
  );
  tweakElements.forEach((tweak) => {
    selectedTweaks.push({
      category: tweak.dataset.category,
      name: tweak.dataset.name,
      index: parseInt(tweak.dataset.index),
    });
  });
  const jsonData = {
    Aesthetic: [],
    Terrain: [],
    Variation: [],
    "Peace and Quiet": [],
    Utility: [],
    Unobtrusive: [],
    "3D": [],
    GUI: [],
    "Menu Panoramas": [],
    Retro: [],
    Fun: [],
    "World of Color": [],
    Parity: [],
    "Fixes and Consistency": [],
    "More Zombies": [],
    "Lower and Sides": [],
    Mobs: [],
    Directional: [],
    "Growth Stages": [],
    Crosshairs: [],
    Hearts: [],
    "LGBTQ+ Pride": [],
    "Hunger Bars": [],
    "Hotbar Selector": [],
    "Xisuma's Hermitcraft Bases": [],
    "Colorful Slime": [],
    Elytra: [],
    "Enchantment Glints": [],
  };
  selectedTweaks.forEach((tweak) => {
    jsonData[tweak.category].push(tweak.name);
  });
  jsonData.raw = selectedTweaks.map((tweak) => tweak.name);
  console.log(
    "[%cget%c]\nObtained selected tweaks!",
    "color: purple",
    "color: initial",
  );
  return jsonData;
}
// Extra code to trigger file input
document
  .querySelector(".zipinputcontainer")
  .addEventListener("click", function () {
    document.getElementById("zipInput").click();
  });
// upload pack
const zipInput = document.getElementById("zipInput");
const selectedFile = document.querySelector(".selectedFile");
zipInput.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (zipInput.files.length > 0) {
    selectedFile.innerText = zipInput.files[0].name;
  }
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
                    document.querySelector(
                      ".download-selected-button",
                    ).disabled = false;
                  } catch (error) {
                    console.log(
                      `[%cerror%c]\nError parsing JSON: %c${error}`,
                      "color: red",
                      "color: initial",
                      "color: red",
                    );
                    selectedFile.innerText = "Invalid JSON in pack";
                    sleep(3000).then(() => {
                      selectedFile.innerText = "Upload pack";
                    });
                  }
                })
                .catch(function (error) {
                  console.log(
                    `[%cerror%c]\nError extracting selected_packs.json: %c${error}`,
                    "color: red",
                    "color: initial",
                    "color: red",
                  );
                  selectedFile.innerText = "Invalid pack";
                  sleep(3000).then(() => {
                    selectedFile.innerText = "Upload pack";
                  });
                });
            }
          });

          if (!fileFound) {
            console.log(
              `[%cerror%c]\nselected_packs.json not found in any folder within the ZIP file.`,
              "color: red",
              "color: initial",
            );
            selectedFile.innerText = "Invalid pack";
            sleep(3000).then(() => {
              selectedFile.innerText = "Upload pack";
            });
          }
        })
        .catch(function (error) {
          console.log(
            `[%cerror%c]\nError reading ZIP file: %c${error}`,
            "color: red",
            "color: initial",
            "color: red",
          );
          selectedFile.innerText = "Invalid file";
          sleep(3000).then(() => {
            selectedFile.innerText = "Upload pack";
          });
        });
    };
    reader.readAsArrayBuffer(file);
  } else {
    console.log(
      `[%cerror%c]\nNo file selected.`,
      "color: red",
      "color: initial",
    );
  }
});

function selectAll(element) {
  const st = JSON.parse(
    LZString.decompressFromEncodedURIComponent(element.dataset.allpacks),
  );
  processJsonData(st, "select");
  updateSelectAllButton(getSelectedTweaks());
}

function unselectAll(element) {
  const st = JSON.parse(
    LZString.decompressFromEncodedURIComponent(element.dataset.allpacks),
  );
  processJsonData(st, "unselect");
  updateSelectAllButton(getSelectedTweaks());
}

function updateCategoryHeight() {
  const categoryControlled = document.querySelectorAll(".category-controlled");
  categoryControlled.forEach((element) => {
    if (element.style.maxHeight) {
      element.style.maxHeight = element.scrollHeight + "px";
    }
  });
}

window.addEventListener("resize", updateCategoryHeight);
