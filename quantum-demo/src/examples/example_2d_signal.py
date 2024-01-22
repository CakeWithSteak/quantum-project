import numpy as np

from src.signal.rules import RuleSet
from src.signal.signal import SignalSimulation
from src.utils.visualize import visualize_image_animation

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

N = 4
T = 10

images = []

for total_steps in range(T):
    sim = SignalSimulation(N, N, rule_set)
    sim.init("1#.#"
             "#..#"
             "...."
             "....")

    sim.simulate(total_steps)
    images.append(sim.image())


visualize_image_animation(images)


