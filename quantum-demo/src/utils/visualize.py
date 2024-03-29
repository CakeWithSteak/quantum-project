import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import PillowWriter
from matplotlib.ticker import MaxNLocator
from enum import Enum

from src.utils.utils import index_to_grid_pos, lerp_color


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


def visualize_image_animation(images, shots, *, trails=None, display_histogram):
    if display_histogram:
        fig, (image_ax, hist_ax) = plt.subplots(figsize=(8, 8), nrows=2, height_ratios=[3, 1])
    else:
        fig, image_ax = plt.subplots(figsize=(8, 8))

    if trails is not None:
        for i, image in enumerate(images):
            for j in range(i):
                for x, y, t in trails[j]:
                    image[y, x] = lerp_color([1, 1, 0.98], signal_color(t), 1 - 0.8 * ((i - j) / len(images)))

    fig.canvas.manager.set_window_title('Visualization')
    im = image_ax.imshow(images[0], origin='upper', extent=(0, images[0].shape[0], 0, images[0].shape[1]))
    image_ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    image_ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    if display_histogram:
        hist_ax.set_title("Possible signal states")
        hist_ax.set_ylabel("probability")

    def frame(i):
        im.set_array(images[i])
        image_ax.set_title(f'{i}/{len(images)}')
        if display_histogram:
            x, y = zip(*shots[i])
            hist_ax.clear()
            hist_ax.bar(x, y, width=0.2)
            hist_ax.set_ylim(0, 1.05)

        return [im]

    anim = animation.FuncAnimation(
        fig,
        frame,
        frames=len(images),
        interval=200
    )

    anim.save("demo.gif", writer=PillowWriter(fps=10))

    plt.show()


def signal_color(t):
    colors = np.array([[255, 93, 0], [162, 255, 84], [0, 137, 255]]) / 255
    if t < 0.5:
        return lerp_color(colors[0], colors[1], t*2)
    else:
        return lerp_color(colors[1], colors[2], (t-0.5) * 2)