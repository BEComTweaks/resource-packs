// watch for changes
document
  .querySelector(".devtools-toggle-mine-then-craft input[type='checkbox']")
  .addEventListener("change", function () {
    // handle the miner class for style changes
    const numberElement = document.querySelector(
      "#mineThenCraftPoints > .number",
    );
    if (this.checked) {
      document.querySelector("body").className = "miner";
      updateDownloadButton(getSelectedTweaks());
    } else {
      document.querySelector("body").className = "";
      document.querySelector(".download-selected-button").disabled = false;
    }
    consoler(
      "miner",
      "brown",
      `Toggle has been set to ${this.checked}`,
      "white",
    );
  });

function toggleViewAll(element) {
  // check if active or not
  if (OreUI.getCurrentState(element) == "active") {
    // this is under the assumption that you cant disable
    // the toggle within the time it takes to show the
    // elements again
    document.querySelector("body").className = "miner";
    OreUI.becomeInactive(element);
    element.innerText = "Start Mining";
  } else {
    document.querySelector("body").className = "miner hideall";
    OreUI.becomeActive(element);
    element.innerText = "Stop Mining";
  }
  console.log(document.querySelector("body").className);
}

document.querySelectorAll("#background-container .tile").forEach((element) => {
  element.addEventListener("click", function () {
    if (
      document.querySelector(
        ".devtools-toggle-mine-then-craft input[type='checkbox']",
      ).checked
    ) {
      // update points
      const numberElement = document.querySelector(
        "#mineThenCraftPoints > .number",
      );
      switch (element.dataset.type) {
        case "stone.png":
          numberElement.textContent = Number(numberElement.textContent) + 1;
          break;
        case "copper_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 2;
          break;
        case "coal_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 2;
          break;
        case "iron_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 4;
          break;
        case "lapis_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 6;
          break;
        case "redstone_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 6;
          break;
        case "gold_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 8;
          break;
        case "emerald_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 8;
          break;
        case "diamond_ore.png":
          numberElement.textContent = Number(numberElement.textContent) + 10;
          break;
      }
      // change the block
      updateTile(element);
      // update download container
      if (
        Number(numberElement.textContent) <
        getSelectedTweaks()["raw"].length * 20
      ) {
        document.querySelector(".download-selected-button").disabled = true;
      } else {
        document.querySelector(".download-selected-button").disabled = false;
      }
    }
  });
});
