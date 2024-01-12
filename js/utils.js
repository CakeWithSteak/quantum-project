// Creates a 2d array filled with AIR
function createMap() {
    const map = [];
    for (let x = 0; x < TILES_N; x++) {
        map[x] = [];
        for (let y = 0; y < TILES_N; y++) {
            map[x][y] = Material.AIR;
        }
    }
    return map;
}

// Fills an area with specific material
function fill(material, startX, startY, width, height) {
    for (let x = startX; x < startX+width; x++) {
        for (let y = startY; y < startY+height; y++) {
            currentMap[x][y] = material;
        }
    }
}

// Is coordinate inside map
function inside(x, y) {
    return x >= 0 && y >= 0 && x < TILES_N && y < TILES_N;
}

// Gets tile from the map. Return STONE if coordinate outside bounds
function getTile(x, y) {
    if (!inside(x, y)) return Material.STONE;
    else return currentMap[x][y];
}

/*
1 2 3    1 2 3
4 A 6 -> 4 A 6
7 8 9    7 8 9

Copies the 3x3 grid of tiles centered around A (fromX, fromY) to the next buffer
*/
function copy(fromX, fromY) {
    for (let x = fromX-1; x <= fromX+1; x++) {
        for (let y = fromY-1; y <= fromY+1; y++) {
            if (!inside(x, y)) continue;
            nextMap[x][y] = currentMap[x][y];
        }
    }
}

/*
1 2 3    1 2 3
4 A 6 -> 4 B 6
7 8 B    7 8 A

Copies the 3x3 grid of tiles centered around A (fromX, fromY) to the next buffer,
except A and B (toX, toY) get swapped.
*/
function swap(fromX, fromY, toX, toY) {
    copy(fromX, fromY);
    nextMap[fromX][fromY] = currentMap[toX][toY];
    nextMap[toX][toY] = currentMap[fromX][fromY];
}

/*
Copies tiles that were not considered this substep to the next buffer.

Consider substep 1 (sx=0, dy=0), tiles marked with [1] and their surrounding 8 neighbours [.] get updated:
    1.. 1.*
    ... ..*
    ... ..*

    1.. 1.*
    ... ..*
    *** ***

Notice tiles [*] are not processed, but they still need to be coppied to the next buffer.

Note: (sx, sy) are the coordinates of the tile considered within each chunk
*/
function copyEdges(sx, sy) {
    const minX = sx-1;
    const minY = sy-1;

    const maxX = (CHUNK_N-1)*3 + sx + 1;
    const maxY = (CHUNK_N-1)*3 + sy + 1;

    for (let x = 0; x < TILES_N; x++) {
        for (let y = 0; y < TILES_N; y++) {
            if (x < minX || y < minY || x > maxX || y > maxY) {
                nextMap[x][y] = currentMap[x][y];
            }
        }
    }
}
