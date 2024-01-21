from enum import Enum

import numpy as np

from src.utils import grid_pos_to_index


def add_rule(context, outcomes, rotate, flip):
    pass


add_rule("0...", [(1, "...0")], True, False)
add_rule("1...", [(1, "...1")], True, False)

add_rule("##0.", [(1, "##.0")], True, True)
add_rule("##1.", [(1, "##.1")], True, True)

add_rule("#.0.", [(1, "#0..")], True, True)
add_rule("#.1.", [(1, "#1..")], True, True)

add_rule("#.0#", [(1 / np.sqrt(2), "#0.#"), (1 / np.sqrt(2), "#1.#")], True, False)
add_rule("#.1#", [(1 / np.sqrt(2), "#0.#"), (-1 / np.sqrt(2), "#1.#")], True, False)

add_rule("1.1.", [(np.exp(1j * np.pi / 4), ".1.1")], True, False)
add_rule("1.0.", [(1, "0.1.")], True, False)
add_rule("0.1.", [(1, "1.0.")], True, False)
add_rule("0.0.", [(1, "0.0.")], True, False)


class Tile(Enum):
    AIR = 0
    BLOCK = 1
    SIGNAL = 2


def char_to_tile(char):
    match char:
        case '.': return Tile.AIR
        case '#': return Tile.BLOCK
        case '0': return Tile.SIGNAL
        case '1': return Tile.SIGNAL


def tile_to_char(tile):
    match tile:
        case Tile.AIR:
            return '.'
        case Tile.BLOCK:
            return '#'
        case Tile.SIGNAL:
            return 's'


def init_2d_array(width, height, value):
    grid = []
    for x in range(width):
        grid.append([])
        for y in range(height):
            grid[x].append(value)

    return grid


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = init_2d_array(width, height, Tile.AIR)

    def init(self, state):
        for x in range(self.width):
            for y in range(self.height):
                char = state[grid_pos_to_index(self.width, self.height, x, y, False)]
                self.grid[x][y] = char_to_tile(char)

    def print(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += tile_to_char(self.grid[x][y])

            print(row)


sim = Simulation(4, 4)
sim.init("0..#"
         "...#"
         "...."
         "....")

sim.print()