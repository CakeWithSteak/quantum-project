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

function inside(x, y) {
    return x >= 0 && y >= 0 && x < N && y < N;
}

function getTile(x, y) {
    if (!inside(x, y)) return Material.STONE;
    else return currentMap[x][y];
}

function swap(fromX, fromY, toX, toY) {
    copy(fromX, fromY);
    nextMap[fromX][fromY] = currentMap[toX][toY];
    nextMap[toX][toY] = currentMap[fromX][fromY];
}

function copy(fromX, fromY) {
    for (let x = fromX-1; x <= fromX+1; x++) {
        for (let y = fromY-1; y <= fromY+1; y++) {
            if (!inside(x, y)) continue;
            nextMap[x][y] = currentMap[x][y];
        }
    }
}

function updateSand(x, y) {
    if (getTile(x, y-1) == Material.AIR || getTile(x, y-1) == Material.WATER) {
        swap(x, y, x, y-1); 
    } 
    else {
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

function updateIdentity(x, y) {
    copy(x, y);
}

function copyEdges(sx, sy) {
    let minX = sx-1;
    let minY = sy-1;

    let maxX = N-3 + sx + 1;
    let maxY = N-3 + sy + 1;

    for (let x = 0; x < N; x++) {
        for (let y = 0; y < N; y++) {
            if (x < minX || y < minY || x > maxX || y > maxY) {
                nextMap[x][y] = currentMap[x][y];
            }
        }
    }
}

let currentMap = createMap();
let nextMap = null;

fill(Material.STONE, 9, 9, 8, 2);
// fill(Material.SAND, 9, 19, 1, 1);
// fill(Material.STONE, 0, 0, 2, 2);


let frame = 0;

function update() {
    nextMap = createMap();

    if (frame % 4 == 0) {
        
        currentMap[9][19] = (frame % 8 == 0) ? Material.WATER : Material.SAND;
    }

    const chunks = N/3;

    const substep = frame % 9;
    let sx = substep % 3;
    let sy = (substep - sx) / 3;

    for (let chunkY = 0; chunkY < chunks; chunkY++) {
        for (let chunkX = 0; chunkX < chunks; chunkX++) {
            const x = chunkX * 3 + sx;
            const y = chunkY * 3 + sy;

            switch (currentMap[x][y]) {
                case Material.SAND:
                    updateSand(x, y);
                    break;
                case Material.WATER:
                    updateWater(x, y);
                    break;
                case Material.STONE:
                case Material.AIR:
                    updateIdentity(x, y);
                    break;
            }
        }
    }

    copyEdges(sx, sy);
    

    currentMap = nextMap;
    renderMap(currentMap);
    frame++;
}

setInterval(update, 10);