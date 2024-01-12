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
            const pixelIndex = (y * N + x) * 4;
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
            map[x][y] =  y == 0 ? Material.SAND : Material.AIR;
        }
    }
    return map;
}

const map = createMap();

renderMap(map);