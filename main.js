const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const N = 20;

const Material = {
    AIR: 0,
    STONE: 1,
    SAND: 2
}

const COLOR = [
    [255, 255, 255],
    [50, 50, 50],
    [252, 186, 3]
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



const map = createMap();

function getTile(x, y) {
    if (x < 0 || y < 0 || x >= N || y >= N) return Material.STONE;
    else return map[x][y];
}

function swap(fromX, fromY, toX, toY) {
    const from = map[fromX][fromY];
    map[fromX][fromY] = map[toX][toY];
    map[toX][toY] = from;
}

function updateSand(x, y) {
    if (getTile(x, y-1) == Material.AIR) {
        swap(x, y, x, y-1);
    } else {
        const left = getTile(x-1, y-1) == Material.AIR;
        const right = getTile(x+1, y-1) == Material.AIR;

        if (left && right) {
            if (Math.random() < 0.5) swap(x, y, x-1, y-1);
            else swap(x, y, x+1, y-1);
        } else if (left) {
            swap(x, y, x-1, y-1);
        } else if (right) {
            swap(x, y, x+1, y-1);
        }
    }
}

let frame = 0;

function update() {
    if (frame % 4 == 0) {
        map[9][19] = Material.SAND;
    }

    for (let y = 0; y < N; y++) {
        for (let x = 0; x < N; x++) {
            switch (map[x][y]) {
                case Material.SAND:
                    updateSand(x, y);
                    break;
            }
        }
    }

    renderMap(map);
    frame++;
}

setInterval(update, 50);