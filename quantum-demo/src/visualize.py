import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import PillowWriter
from matplotlib.ticker import MaxNLocator

from src.utils import index_to_grid_pos


def counts_to_grid(grid_width, grid_height, counts):
    grid = np.zeros((grid_width, grid_height))

    for qubits, count in counts.items():
        for i in range(len(qubits)):
            if qubits[-1 - i] == '1':
                x, y = index_to_grid_pos(grid_width, grid_height, i)
                grid[x, y] += count

    return grid


def visualize_grid(grid_width, grid_height, counts):
    grid = counts_to_grid(grid_width, grid_height, counts)
    plt.imshow(grid.T)
    plt.show()


def visualize_grid_animation(grid_width, grid_height, multiple_counts):
    grids = [counts_to_grid(grid_width, grid_height, counts) for counts in multiple_counts]

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title('Visualization')
    im = ax.imshow(grids[0].T, origin='upper', extent=(0, grid_width, grid_height, 0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    def frame(i):
        im.set_array(grids[i].T)
        ax.set_title(f'{i}/{len(grids)}')
        return [im]

    anim = animation.FuncAnimation(
        fig,
        frame,
        frames=len(grids),
        interval=300
    )

    # anim.save("demo.gif", dpi=300, writer=PillowWriter(fps=10))

    plt.show()

