const stoneColors = ["black-stone", "white-stone"];
let stoneCounter = 0;

function placeStone(position) {
  const intersection = document.getElementById(position);
  intersection.classList.add(stoneColors[stoneCounter % stoneColors.length]);
  stoneCounter++;
}

export { placeStone };