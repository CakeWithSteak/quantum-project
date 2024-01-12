// Updates a 3x3 grid center around a sand tile (x, y). Output is written to the next buffer
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

// Updates a 3x3 grid center around a water tile (x, y). Output is written to the next buffer
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

// Updates a 3x3 grid center around a static tile (stone, air, etc) (x, y). Output is written to the next buffer
function updateIdentity(x, y) {
    copy(x, y);
}