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
