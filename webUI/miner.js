// watch for changes
document
  .querySelector(".devtools-toggle-mine-then-craft input[type='checkbox']")
  .addEventListener("change", function () {
    // handle the miner class for style changes
    if (this.checked) {
      document.querySelector("body").className = "miner";
    } else {
      document.querySelector("body").className = "";
    }
    consoler(
      "miner",
      "brown",
      `Toggle has been set to ${this.checked}`,
      "white",
    );
  });

function toggleViewAll(element) {
  consoler("startmining", "green", "The button was clicked", "white");
  console.log(document.querySelector("body").className);
  // check if active or not
  if (OreUI.getCurrentState(element) == "active") {
    // this is under the assumption that you cant disable
    // the toggle within the time it takes to show the
    // elements again
    document.querySelector("body").className = "miner";
    OreUI.becomeInactive(element);
  } else {
    document.querySelector("body").className = "miner hideall";
    OreUI.becomeActive(element);
  }
  console.log(document.querySelector("body").className);
}
