const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function renderMap(map) {
    const imageData = ctx.createImageData(TILES_N, TILES_N);

    for (let x = 0; x < TILES_N; x++) {
        for (let y = 0; y < TILES_N; y++) {
            const pixelIndex = ((TILES_N-1-y) * TILES_N + x) * 4;
            const color = COLOR[map[x][y]];

            imageData.data[pixelIndex] = color[0];
            imageData.data[pixelIndex + 1] = color[1];
            imageData.data[pixelIndex + 2] = color[2];
            imageData.data[pixelIndex + 3] = 255;

        }
    }

    ctx.putImageData(imageData, 0, 0);
}