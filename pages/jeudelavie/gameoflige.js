const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const rows = 25;
const cols = 50;
const cellSize = 20;
canvas.width = cols * cellSize;
canvas.height = rows * cellSize;

let grid = Array.from({ length: rows }, () => Array(cols).fill(0));
let running = false;

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            ctx.fillStyle = grid[i][j] ? "black" : "white";
            ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);
            ctx.strokeRect(j * cellSize, i * cellSize, cellSize, cellSize);
        }
    }
}

canvas.addEventListener("click", (event) => {
    const x = Math.floor(event.offsetX / cellSize);
    const y = Math.floor(event.offsetY / cellSize);
    grid[y][x] = 1 - grid[y][x];  // Active ou désactive la cellule
    drawGrid();
});

function getNeighbors(x, y) {
    let neighbors = 0;
    for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
            if (dx === 0 && dy === 0) continue;
            const nx = x + dx, ny = y + dy;
            if (nx >= 0 && nx < cols && ny >= 0 && ny < rows) {
                neighbors += grid[ny][nx];
            }
        }
    }
    return neighbors;
}

function updateGrid() {
    let newGrid = grid.map(row => [...row]);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            let neighbors = getNeighbors(j, i);
            if (grid[i][j] === 1) {
                newGrid[i][j] = (neighbors === 2 || neighbors === 3) ? 1 : 0;
            } else {
                newGrid[i][j] = (neighbors === 3) ? 1 : 0;
            }
        }
    }
    grid = newGrid;
    drawGrid();
}

let interval;
document.getElementById("start").addEventListener("click", () => {
    if (running) {
        clearInterval(interval);
        document.getElementById("start").textContent = "Démarrer";
    } else {
        interval = setInterval(updateGrid, 500);
        document.getElementById("start").textContent = "Arrêter";
    }
    running = !running;
});


drawGrid();
