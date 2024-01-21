import numpy as np


def add_rule(context, outcomes, rotate, flip):
    pass


add_rule("0...", [(1, "...0")], True, False)
add_rule("1...", [(1, "...1")], True, False)

add_rule("##0.", [(1, "##.0")], True, True)
add_rule("##1.", [(1, "##.1")], True, True)

add_rule("#.0.", [(1, "#0..")], True, True)
add_rule("#.1.", [(1, "#1..")], True, True)

add_rule("#.0#", [(1/np.sqrt(2), "#0.#"), (1/np.sqrt(2), "#1.#")], True, False)
add_rule("#.1#", [(1/np.sqrt(2), "#0.#"), (-1/np.sqrt(2), "#1.#")], True, False)

add_rule("1.1.", [(np.exp(1j*np.pi/4), ".1.1")], True, False)
add_rule("1.0.", [(1, "0.1.")], True, False)
add_rule("0.1.", [(1, "1.0.")], True, False)
add_rule("0.0.", [(1, "0.0.")], True, False)