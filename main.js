import { placeStone } from './board.js';

const indent = 2.0;
const board = document.getElementById("board");
const alphabet = "ABCDEFGHIJKLMNOPQRS";

for (let row = 0; row < 19; row++) {
  for (let col = 0; col < 19; col++) {
    const intersection = document.createElement("div");
    intersection.classList.add("intersection");
    intersection.setAttribute("id", alphabet[col] + (row + 1));
    intersection.addEventListener("click", () => placeStone(alphabet[col] + (row + 1)));
    intersection.style.top = `${row * 2.0 + indent}em`;
    intersection.style.left = `${col * 2.0 + indent}em`;
    board.appendChild(intersection);
  }
}