import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.ticker import MaxNLocator

from src.utils.utils import index_to_grid_pos


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


def counts_to_line(line_length, counts):
    line = np.zeros(line_length)

    for qubits, count in counts.items():
        for i in range(len(qubits)):
            if qubits[-1 - i] == '1':
                line[i] += count

    return line


def counts_to_line_over_time(line_length, time_steps, multiple_counts):
    grid = np.empty((time_steps, line_length))

    for t in range(time_steps):
        grid[t] = counts_to_line(line_length, multiple_counts[t])

    return grid


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


def visualize_line_over_time(line_length, time_steps, multiple_counts):
    grid = counts_to_line_over_time(line_length, time_steps, multiple_counts)
    # column_pairs = [(i, i+1) for i in range(0, line_length, 2)]
    # result_array = np.sum(grid[:, column_pairs], axis=2)

    plt.imshow(grid)
    plt.show()


def visualize_image_animation(images):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title('Visualization')
    im = ax.imshow(images[0], origin='upper')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    def frame(i):
        im.set_array(images[i])
        ax.set_title(f'{i}/{len(images)}')
        return [im]

    anim = animation.FuncAnimation(
        fig,
        frame,
        frames=len(images),
        interval=300
    )

    # anim.save("demo.gif", dpi=300, writer=PillowWriter(fps=10))

    plt.show()
