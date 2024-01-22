import numpy as np

from src.signal.rules import RuleSet
from src.signal.signal import SignalSimulation

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

rule_set.apply()

# np.set_printoptions(precision=3)
# print(rule_set.rule_data["s.s."].unitary)
# print(rule_set.rule_data["s..."].qubit_mappings)

sim = SignalSimulation(4, 4, rule_set)
sim.init("1#.#"
         "#..#"
         "...."
         "....")

sim.print()
# print(sim.tile_to_qubit)

for s in range(1):
    sim.step()
    sim.print()
    # print(sim.tile_to_qubit)
    # print("")

# print(sim.circuit)

sim.show()


