import numpy as np
from qiskit import QuantumCircuit

from src.utils.simulate import simulate
from src.utils.utils import make_grid_partitions, char_to_classic, grid_pos_to_index, niceify_shots
from src.utils.visualize import signal_color


class SignalSimulation:
    def __init__(self, width, height, rule_set):
        self.width = width
        self.height = height
        self.grid = ['.' for i in range(width*height)]
        self.rule_set = rule_set

        partition_a = make_grid_partitions(width, height, 2, 2, 0, 0, True)
        partition_b = make_grid_partitions(width, height, 2, 2, 1, 1, True)
        self.partitions = [partition_a, partition_b]

        self.iteration = 0
        self.qubit_count = 0
        self.tile_to_qubit = dict()

        self.circuit = None
        self.probabilities = None
        self.shots = []

    def init(self, state):
        self.qubit_count = 0

        for i in range(self.width * self.height):
            self.grid[i] = char_to_classic(state[i])
            if self.grid[i] == 's':
                self.tile_to_qubit[i] = self.qubit_count
                self.qubit_count += 1

        self.circuit = QuantumCircuit(self.qubit_count)

        for i in range(self.width * self.height):
            if self.grid[i] == 's':
                if state[i] == '1':
                    self.circuit.x(self.tile_to_qubit[i])

    def apply_unitary(self, matrix, tiles):
        qubits = [self.tile_to_qubit[i] for i in tiles]
        self.circuit.unitary(matrix, qubits)

    def apply_remap_qubits(self, tile_mappings):
        old_mappings = dict(self.tile_to_qubit)
        for from_tile, to_tile in tile_mappings:
            del self.tile_to_qubit[from_tile]

        for from_tile, to_tile in tile_mappings:
            self.tile_to_qubit[to_tile] = old_mappings[from_tile]

    def apply_remap_grid(self, tile_mappings):
        old_mappings = [self.grid[from_tile] for (from_tile, to_tile) in tile_mappings]

        for from_tile, to_tile in tile_mappings:
            self.grid[from_tile] = '.'

        for i in range(len(tile_mappings)):
            from_tile, to_tile = tile_mappings[i]
            self.grid[to_tile] = old_mappings[i]

    def apply_remap(self, tile_mappings):
        self.apply_remap_qubits(tile_mappings)
        self.apply_remap_grid(tile_mappings)

    def step(self):
        partition = self.partitions[self.iteration % len(self.partitions)]
        for chunk in partition:
            context = ''.join(self.grid[i] for i in chunk)

            tiles = [i for i in chunk if self.grid[i] == 's']
            unitary = self.rule_set.get_unitary(context)
            if unitary is not None:
                self.apply_unitary(unitary, tiles)

            qubit_mappings = self.rule_set.get_qubit_mappings(context)
            if qubit_mappings is not None:
                tile_mappings = [(chunk[from_index], chunk[to_index]) for (from_index, to_index) in qubit_mappings]
                self.apply_remap(tile_mappings)

        self.iteration += 1

    def simulate(self, steps):
        for i in range(steps):
            self.step()

        self.circuit.measure_all()

        counts = simulate(self.circuit)

        self.probabilities = np.zeros(self.qubit_count)
        self.shots = niceify_shots(counts)
        for (bits, count) in counts.items():
            for i in range(len(bits)):
                if bits[-1-i] == '1':
                    self.probabilities[i] += count / 1000

        return self.probabilities

    def print(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                index = grid_pos_to_index(self.width, self.height, x, y)
                row += self.grid[index]


    # Returns an image of the current state, without trails
    def image(self):
        img = np.zeros((self.height, self.width, 3))
        for x in range(self.width):
            for y in range(self.height):
                index = grid_pos_to_index(self.width, self.height, x, y)
                match self.grid[index]:
                    case '.': img[y, x] = [1, 1, 0.98]
                    case '#': img[y, x] = [0, 0, 0]
                    case 's':
                        t = self.probabilities[self.tile_to_qubit[index]]
                        img[y, x] = signal_color(t)

        return img

    # Returns an array of triples of x and y coordinates and probability of signals
    def signals(self):
        res = []
        for x in range(self.width):
            for y in range(self.height):
                index = grid_pos_to_index(self.width, self.height, x, y)
                match self.grid[index]:
                    case 's':
                        t = self.probabilities[self.tile_to_qubit[index]]
                        res.append((x, y, t))

        return res