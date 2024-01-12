let currentMap = createMap();
let nextMap = null;

fill(Material.STONE, 9, 9, 8, 2);

let frame = 0;

function update() {
    // Creates the next buffer where all results will be stored
    nextMap = createMap();

    // Adds sand / water sometimes
    if (frame % 4 == 0) {
        currentMap[9][19] = (frame % 8 == 0) ? Material.WATER : Material.SAND;
    }

    /* 
        Gets current substep (0 to 8) and computes the relative coordinates in each chunk of the tile to be simulated

        0 1 2   0 1 2
        3 4 5   3 4 5
        6 7 8   6 7 8

        0 1 2   0 1 2
        3 4 5   3 4 5
        6 7 8   6 7 8

        For example at substep 3:
            sx = 0, sy = 1
        
        Only 3x3 grids around tiles marked [3] will be considered
    */
    const substep = frame % 9;
    let sx = substep % 3;
    let sy = (substep - sx) / 3;

    // Go through each chunk and simulate tile (sx, sy)
    for (let chunkY = 0; chunkY < CHUNK_N; chunkY++) {
        for (let chunkX = 0; chunkX < CHUNK_N; chunkX++) {
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

    // Copies tiles that were not considered this substep. (Read method comment for more info)
    copyEdges(sx, sy);
    
    // Swap buffers and draw
    currentMap = nextMap;
    renderMap(currentMap);
    frame++;
}

// Loop the update function
setInterval(update, 0);