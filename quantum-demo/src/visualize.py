import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from src.utils import index_to_grid_pos


def visualize_grid(grid_width, grid_height, counts):
    result = np.zeros((grid_width, grid_height))

    for qubits, count in counts.items():
        for i in range(len(qubits)):
            if qubits[-1-i] == '1':
                x, y = index_to_grid_pos(grid_width, grid_height, i)
                result[x, y] += count

    plt.imshow(result.T)
    plt.show()
