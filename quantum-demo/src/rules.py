import numpy as np
from qiskit import QuantumCircuit

from src.utils import grid_pos_to_index, make_grid_partitions


def char_to_classic(char):
    match char:
        case '0': return 's'
        case '1': return 's'
        case _: return char


def str_to_classic(string):
    return ''.join([char_to_classic(c) for c in string])


class RuleData:
    def __init__(self):
        self.quantum_rules = dict()

        # computed
        self.qubit_mappings = None
        self.unitary = None

    def add_rule(self, context, outcome):
        if context not in self.quantum_rules:
            self.quantum_rules[context] = []

        self.quantum_rules[context].append(outcome)

    def compute_qubit_mappings(self):
        context = list(self.quantum_rules.keys())[0]
        classic_context = str_to_classic(context)

        from_indices = []
        for i in range(len(classic_context)):
            if classic_context[i] == 's':
                from_indices.append(i)

        outcome = self.quantum_rules[context][0][1]
        classic_outcome = str_to_classic(outcome)

        to_indices = []
        for i in range(len(classic_outcome)):
            if classic_outcome[i] == 's':
                to_indices.append(i)

        assert len(from_indices) == len(to_indices)
        self.qubit_mappings = []
        for i in range(len(from_indices)):
            self.qubit_mappings.append((from_indices[i], to_indices[i]))

    def compute_raw_rules(self):
        raw_rules = dict()

        for (context, outcomes) in self.quantum_rules.items():
            raw_context = ''.join([context[m[0]] for m in self.qubit_mappings])
            raw_context_index = int(raw_context, 2)
            raw_rules[raw_context_index] = []

            for (coefficient, outcome) in outcomes:
                raw_outcome = ''.join([outcome[m[1]] for m in self.qubit_mappings])
                raw_outcome_index = int(raw_outcome, 2)
                raw_rules[raw_context_index].append((coefficient, raw_outcome_index))

        return raw_rules

    def compute_unitary(self):
        raw_rules = self.compute_raw_rules()

        n = 2 ** len(self.qubit_mappings)
        self.unitary = np.zeros((n, n), dtype=complex)

        for context_index in range(n):
            if context_index in raw_rules:
                for (coefficient, outcome_index) in raw_rules[context_index]:
                    self.unitary[outcome_index][context_index] = coefficient
            else:
                self.unitary[context_index][context_index] = 1

        # if identity ignore
        if np.all(np.equal(self.unitary, np.eye(n))):
            self.unitary = None

    def apply(self):
        self.compute_qubit_mappings()
        self.compute_unitary()


class RuleSet:
    def __init__(self):
        self.rule_data = dict()

    def add_rule(self, context, outcomes, rotate, flip):
        rotations = [[0, 1, 2, 3], [2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        flips = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]

        for r in range(len(rotations) if rotate else 1):
            for f in range(len(flips) if flip else 1):
                indices = [flips[f][i] for i in rotations[r]]
                transformed_context = ''.join(context[i] for i in indices)
                classic_context = str_to_classic(transformed_context)

                if classic_context not in self.rule_data:
                    self.rule_data[classic_context] = RuleData()

                for outcome in outcomes:
                    transformed_outcome = ''.join(outcome[1][i] for i in indices)
                    self.rule_data[classic_context].add_rule(transformed_context, (outcome[0], transformed_outcome))

    def apply(self):
        for rule in self.rule_data.values():
            rule.apply()

    def get_qubit_mappings(self, context):
        if context in self.rule_data:
            return self.rule_data[context].qubit_mappings

        return None  # identity

    def get_unitary(self, context):
        if context in self.rule_data:
            return self.rule_data[context].unitary

        return None  # identity


rule_set = RuleSet()

rule_set.add_rule("0...", [(1, "...0")], True, False)
rule_set.add_rule("1...", [(1, "...1")], True, False)

rule_set.add_rule("##0.", [(1, "##.0")], True, True)
rule_set.add_rule("##1.", [(1, "##.1")], True, True)

rule_set.add_rule("#.0.", [(1, "#0..")], True, True)
rule_set.add_rule("#.1.", [(1, "#1..")], True, True)

rule_set.add_rule("#.0#", [(1 / np.sqrt(2), "#0.#"), (1 / np.sqrt(2), "#1.#")], True, False)
rule_set.add_rule("#.1#", [(1 / np.sqrt(2), "#0.#"), (-1 / np.sqrt(2), "#1.#")], True, False)

rule_set.add_rule("1.1.", [(np.exp(1j * np.pi / 4), ".1.1")], True, False)
rule_set.add_rule("1.0.", [(1, ".0.1")], True, False)
rule_set.add_rule("0.1.", [(1, ".1.0")], True, False)
rule_set.add_rule("0.0.", [(1, ".0.0")], True, False)


# testing rule
# rule_set.add_rule("1.0.", [(1, "0.1.")], False, False)

# rule_set.add_rule("1.1.", [(np.exp(1j * np.pi / 4), ".1.1")], False, False)
# rule_set.add_rule("1.0.", [(1, ".0.1")], False, False)
# rule_set.add_rule("0.1.", [(1, ".1.0")], False, False)
# rule_set.add_rule("0.0.", [(1, ".0.0")], False, False)

# rule_set.add_rule("#.0#", [(1 / np.sqrt(2), "#0.#"), (1 / np.sqrt(2), "#1.#")], False, False)
# rule_set.add_rule("#.1#", [(1 / np.sqrt(2), "#0.#"), (-1 / np.sqrt(2), "#1.#")], False, False)

rule_set.apply()

# np.set_printoptions(precision=3)
# print(rule_set.rule_data["s.s."].unitary)
# print(rule_set.rule_data["s..."].qubit_mappings)


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = ['.' for i in range(width*height)]

        partition_a = make_grid_partitions(width, height, 2, 2, 0, 0, True)
        partition_b = make_grid_partitions(width, height, 2, 2, 1, 1, True)
        self.partitions = [partition_a, partition_b]

        self.iteration = 0

        self.tile_to_qubit = dict()

        self.circuit = None

    def init(self, state):
        qubit_count = 0

        for i in range(self.width * self.height):
            self.grid[i] = char_to_classic(state[i])
            if self.grid[i] == 's':
                self.tile_to_qubit[i] = qubit_count
                qubit_count += 1

        self.circuit = QuantumCircuit(qubit_count)

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
            unitary = rule_set.get_unitary(context)
            if unitary is not None:
                self.apply_unitary(unitary, tiles)

            qubit_mappings = rule_set.get_qubit_mappings(context)
            if qubit_mappings is not None:
                tile_mappings = [(chunk[from_index], chunk[to_index]) for (from_index, to_index) in qubit_mappings]
                self.apply_remap(tile_mappings)

        self.iteration += 1

    def print(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                index = grid_pos_to_index(self.width, self.height, x, y)
                row += self.grid[index]

            print(row)


sim = Simulation(4, 4)
sim.init("11.#"
         "...#"
         "...."
         "....")

sim.print()
print(sim.tile_to_qubit)

for s in range(4):
    sim.step()
    sim.print()
    print(sim.tile_to_qubit)
    print("")

print(sim.circuit)


