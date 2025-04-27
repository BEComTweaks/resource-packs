/* consoler object */
function consoler(logTag, logColour, logMessage, logMessageColour) {
  const err = new Error();
  const stack = err.stack.split("\n");
  console.log(
    `[%c${logTag}%c] %c${stack[1]}%c\n%c${logMessage}`,
    `color: ${logColour}`,
    "color: white",
    "color: #4fa1ff",
    `color: ${logMessageColour}`,
  );
  if (
    document.querySelector(".devtools-toggle-console input[type='checkbox']")
      .checked
  ) {
    const consoleElement = document.querySelector(".devtools-console-content");
    const log = document.createElement("div");
    log.className = "devtools-console-log";
    log.innerHTML = `[<span style="color: ${logColour}">${logTag}</span>] <span style="color: #4fa1ff">${stack[1]}</span><br><span style="color: ${logMessageColour}">${logMessage}</span>`;
    consoleElement.appendChild(log);
  }
}
// Handle Backgrounds
const textures = [
  { src: "images/blocks/stone.png", probability: 0.618 },
  { src: "images/blocks/copper_ore.png", probability: 0.128 },
  { src: "images/blocks/coal_ore.png", probability: 0.128 },
  { src: "images/blocks/iron_ore.png", probability: 0.064 },
  { src: "images/blocks/lapis_ore.png", probability: 0.032 },
  { src: "images/blocks/redstone_ore.png", probability: 0.016 },
  { src: "images/blocks/gold_ore.png", probability: 0.008 },
  { src: "images/blocks/emerald_ore.png", probability: 0.004 },
  { src: "images/blocks/diamond_ore.png", probability: 0.002 },
];

function selectTexture() {
  const rand = Math.random();
  let cumulativeProbability = 0;
  for (const texture of textures) {
    cumulativeProbability += texture.probability;
    if (rand < cumulativeProbability) {
      return texture.src;
    }
  }
}

function createTiles() {
  const container = document.getElementById("background-container");
  const numColumns = Math.ceil(window.innerWidth / 100) + 2;
  const numRows = Math.ceil(window.innerHeight / 100) + 2;

  for (let i = container.children.length; i < numColumns; i++) {
    const rowDiv = document.createElement("div");
    rowDiv.className = "row";
    for (let j = 0; j < numRows; j++) {
      const tile = document.createElement("div");
      tile.className = "tile";
      tile.style.backgroundImage = `url("${selectTexture()}")`;
      rowDiv.appendChild(tile);
    }
    container.appendChild(rowDiv);
  }

  // Adjust existing rows and columns
  for (let i = 0; i < container.children.length; i++) {
    const rowDiv = container.children[i];
    for (let j = rowDiv.children.length; j < numRows; j++) {
      const tile = document.createElement("div");
      tile.className = "tile";
      tile.style.backgroundImage = `url("${selectTexture()}")`;
      rowDiv.appendChild(tile);
    }
    while (rowDiv.children.length > numRows) {
      rowDiv.removeChild(rowDiv.lastChild);
    }
  }

  while (container.children.length > numColumns) {
    container.removeChild(container.lastChild);
  }
}

createTiles();

window.addEventListener("resize", createTiles);

// Handle Loading Screen
const loading_screen_element = document.querySelector(".loading-screen");
if (Math.random() <= 0.9) {
  /* From Uiverse.io by alexruix */
  loading_screen_element.innerHTML += `
  <style>
.box1 {
  width: 112px;
  height: 48px;
  margin-top: 64px;
  margin-left: 0px;
  animation: abox1 4s 1s forwards ease-in-out infinite;
}

.box2 {
  width: 48px;
  height: 48px;
  margin-top: 0px;
  margin-left: 0px;
  animation: abox2 4s 1s forwards ease-in-out infinite;
}

.box3 {
  width: 48px;
  height: 48px;
  margin-top: 0px;
  margin-left: 64px;
  animation: abox3 4s 1s forwards ease-in-out infinite;
}

@keyframes abox1 {
  0% {
    width: 112px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  12.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  25% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  37.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  50% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  62.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }

  75% {
    width: 48px;
    height: 112px;
    margin-top: 0px;
    margin-left: 0px;
  }

  87.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  100% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }
}

@keyframes abox2 {
  0% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  12.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  25% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  37.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  50% {
    width: 112px;
    height: 48px;
    margin-top: 0px;
    margin-left: 0px;
  }

  62.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }

  75% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }

  87.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }

  100% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }
}

@keyframes abox3 {
  0% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }

  12.5% {
    width: 48px;
    height: 48px;
    margin-top: 0px;
    margin-left: 64px;
  }

  25% {
    width: 48px;
    height: 112px;
    margin-top: 0px;
    margin-left: 64px;
  }

  37.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 64px;
  }

  50% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 64px;
  }

  62.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 64px;
  }

  75% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 64px;
  }

  87.5% {
    width: 48px;
    height: 48px;
    margin-top: 64px;
    margin-left: 64px;
  }

  100% {
    width: 112px;
    height: 48px;
    margin-top: 64px;
    margin-left: 0px;
  }
}
  </style>
  `;
} else {
  /* From Uiverse.io by MetaBlue2000 */
  loading_screen_element.innerHTML += `
  <style>
.box1 {
  width: 112px;
  height: 48px;
  margin-top: 64px;
  margin-left: 0px;
}

.box2 {
  width: 48px;
  height: 48px;
  margin-top: 0px;
  margin-left: 0px;
}

.box3 {
  width: 48px;
  height: 48px;
  margin-top: 0px;
  margin-left: 64px;
  animation: infinite 1.8s wink;
}

@keyframes wink {
  0% {
    width: 48px;
    height: 10px;
    rotate: -25deg;
    margin-top: 10px;
  }

  12.5% {
    width: 48px;
    height: 10px;
    rotate: -45deg;
    margin-top: 5px;
  }

  25% {
    width: 48px;
    height: 48px;
  }

  100% {
    width: 48px;
    height: 48px;
    rotate: 0deg;
  }
}
  </style>
  `;
}

/* sleep */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
/* instant */
function getTimeoutDuration() {
  // for people who want instant stuff
  const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  return mediaQuery.matches ? 0 : 1000;
}

/* devtools */
function showDevToolsPanel() {
  document.querySelector(".devtools").style.transform = "translateY(0)";
  document.querySelector(".capture-exit").setAttribute("close", ".devtools");
  document.querySelector(".capture-exit").style =
    "opacity: 1; pointer-events: all;";
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    const captureExitElement = document.querySelector(".capture-exit");
    if (captureExitElement.style !== "") {
      captureExitElement.click(); // Simulate a click on the element
    }
  }
});

function closePanel() {
  const element = document.querySelector(".capture-exit");
  document
    .querySelector(element.getAttribute("close"))
    .removeAttribute("style");
  element.removeAttribute("style");
}

document
  .querySelector(".devtools-toggle-tweak-per-column input[type='number']")
  .addEventListener("input", function () {
    const checkbox = this.parentElement.parentElement.querySelector(
      "input[type='checkbox']",
    );
    if (checkbox && checkbox.checked) {
      let styleBlock = document.querySelector("#dynamic-grid-style");

      // If the style block doesn't exist, create it
      if (!styleBlock) {
        styleBlock = document.createElement("style");
        styleBlock.id = "dynamic-grid-style";
        document.head.appendChild(styleBlock);
      }

      // Update the styles for `.tweaks` and `.subcattweaks`
      styleBlock.textContent = `
        .tweaks, .subcattweaks {
          grid-template-columns: repeat(${this.value}, 1fr) !important;
        }
      `;
      updateCategoryHeight();
    }
  });

document
  .querySelector(".devtools-toggle-tweak-per-column input[type='checkbox']")
  .addEventListener("change", function () {
    const numberInput = this.parentElement.parentElement.querySelector(
      "input[type='number']",
    );
    if (this.checked) {
      numberInput.removeAttribute("disabled");
      numberInput.dispatchEvent(new Event("input"));
      consoler(
        "tweak-per-column",
        "green",
        `Set tweaks container column width to ${numberInput.content}`,
        "white",
      );
    } else {
      numberInput.setAttribute("disabled", "true");
      const styleBlock = document.querySelector("#dynamic-grid-style");
      if (styleBlock) {
        styleBlock.remove();
      }
    }
  });
