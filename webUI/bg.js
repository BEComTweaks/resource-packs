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
