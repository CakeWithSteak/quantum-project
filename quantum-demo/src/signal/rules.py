import numpy as np

from src.utils.utils import str_to_classic


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
