const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const N = 21;

const Material = {
    AIR: 0,
    STONE: 1,
    SAND: 2,
    WATER: 3
}

const COLOR = [
    [255, 255, 255],
    [50, 50, 50],
    [252, 186, 3],
    [3, 181, 252]
]

function renderMap(map) {
    const imageData = ctx.createImageData(N, N);

    for (let x = 0; x < N; x++) {
        for (let y = 0; y < N; y++) {
            const pixelIndex = ((N-1-y) * N + x) * 4;
            const color = COLOR[map[x][y]];

            imageData.data[pixelIndex] = color[0];
            imageData.data[pixelIndex + 1] = color[1];
            imageData.data[pixelIndex + 2] = color[2];
            imageData.data[pixelIndex + 3] = 255;

        }
    }

    ctx.putImageData(imageData, 0, 0);
}

function createMap() {
    const map = [];
    for (let x = 0; x < N; x++) {
        map[x] = [];
        for (let y = 0; y < N; y++) {
            map[x][y] = Material.AIR;
        }
    }
    return map;
}

function fill(material, startX, startY, width, height) {
    for (let x = startX; x < startX+width; x++) {
        for (let y = startY; y < startY+height; y++) {
            currentMap[x][y] = material;
        }
    }
}

function getTile(x, y) {
    if (x < 0 || y < 0 || x >= N || y >= N) return Material.STONE;
    else return currentMap[x][y];
}

function swap(fromX, fromY, toX, toY) {
    // const from = map[fromX][fromY];
    // map[fromX][fromY] = map[toX][toY];
    // map[toX][toY] = from;
    nextMap[fromX][fromY] = currentMap[toX][toY];
    nextMap[toX][toY] = currentMap[fromX][fromY];
}

function copy(x, y) {
    nextMap[x][y] = currentMap[x][y];
}

function updateSand(x, y) {
    // copy(x, y);
    if (getTile(x, y-1) == Material.AIR || getTile(x, y-1) == Material.WATER) {
        swap(x, y, x, y-1); 
        // console.log(nextMap);
    } else {
        const downLeft = getTile(x-1, y-1) == Material.AIR || getTile(x-1, y-1) == Material.WATER;
        const downRight = getTile(x+1, y-1) == Material.AIR || getTile(x+1, y-1) == Material.WATER;

        if (downLeft && downRight) {
            if (Math.random() < 0.5) swap(x, y, x-1, y-1);
            else swap(x, y, x+1, y-1);
        } else if (downLeft) {
            swap(x, y, x-1, y-1);
        } else if (downRight) {
            swap(x, y, x+1, y-1);
        } else {
            copy(x, y);
        }
    }
}

function updateWater(x, y) {
    if (getTile(x, y-1) == Material.AIR) {
        swap(x, y, x, y-1);
    } else {
        const downLeft = getTile(x-1, y-1) == Material.AIR;
        const downRight = getTile(x+1, y-1) == Material.AIR;

        if (downLeft && downRight) {
            if (Math.random() < 0.5) swap(x, y, x-1, y-1);
            else swap(x, y, x+1, y-1);
        } else if (downLeft) {
            swap(x, y, x-1, y-1);
        } else if (downRight) {
            swap(x, y, x+1, y-1);
        } else {

            const left = getTile(x-1, y) == Material.AIR;
            const right = getTile(x+1, y) == Material.AIR;

            if (left && right) {
                if (Math.random() < 0.5) swap(x, y, x-1, y);
                else swap(x, y, x+1, y);
            } else if (left) {
                swap(x, y, x-1, y);
            } else if (right) {
                swap(x, y, x+1, y);
            } else {
                copy(x, y);
            }
        }
    }
}

let currentMap = createMap();
let nextMap = null;

fill(Material.STONE, 9, 9, 8, 2);

let frame = 0;

function update() {
    nextMap = createMap();

    if (frame % 4 == 0) {
        
        currentMap[9][19] = (frame % 8 == 0) ? Material.WATER : Material.SAND;
    }

    for (let y = 0; y < N; y++) {
        for (let x = 0; x < N; x++) {
            switch (currentMap[x][y]) {
                case Material.SAND:
                    updateSand(x, y);
                    break;
                case Material.WATER:
                    updateWater(x, y);
                    break;
            }
        }
    }

    currentMap = nextMap;
    renderMap(currentMap);
    frame++;
}

setInterval(update, 10);