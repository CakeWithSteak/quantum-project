import numpy as np

from src.utils import grid_pos_to_index, make_grid_partitions


def char_to_classic(char):
    match char:
        case '0': return 's'
        case '1': return 's'
        case _: return char


def str_to_classic(string):
    return ''.join([char_to_classic(c) for c in string])


classic_rules = dict()


def add_rule(context, outcomes, rotate, flip):
    classic_context_base = str_to_classic(context)
    classic_outcome_base = str_to_classic(outcomes[0][1])

    rotations = [[0, 1, 2, 3], [2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
    flips = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]

    for r in range(len(rotations) if rotate else 1):
        for f in range(len(flips) if flip else 1):
            indices = [flips[f][i] for i in rotations[r]]
            classic_context = ''.join(classic_context_base[i] for i in indices)
            classic_outcome = ''.join(classic_outcome_base[i] for i in indices)
            classic_rules[classic_context] = classic_outcome


def get_rule(context):
    classic_context = str_to_classic(context)
    if classic_context in classic_rules:
        return classic_rules[classic_context]

    return classic_context


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

print(classic_rules)


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = ['.' for i in range(width*height)]

        partition_a = make_grid_partitions(width, height, 2, 2, 0, 0, True)
        partition_b = make_grid_partitions(width, height, 2, 2, 1, 1, True)
        self.partitions = [partition_a, partition_b]

        self.iteration = 0

    def init(self, state):
        for i in range(self.width * self.height):
            self.grid[i] = char_to_classic(state[i])

    def step(self):
        partition = self.partitions[self.iteration % len(self.partitions)]
        for chunk in partition:
            context = ''.join(self.grid[i] for i in chunk)
            result = get_rule(context)
            for i in range(len(chunk)):
                self.grid[chunk[i]] = result[i]

        self.iteration += 1

    def print(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                index = grid_pos_to_index(self.width, self.height, x, y)
                row += self.grid[index]

            print(row)
        print("")


sim = Simulation(4, 4)
sim.init("0..#"
         "...#"
         "...."
         "....")

sim.print()

for s in range(4):
    sim.step()
    sim.print()


