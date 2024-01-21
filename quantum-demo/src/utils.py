import numpy as np


def make_truth_table_matrix(bitmaps):
    matrix_size = len(bitmaps)
    binary_mapping_matrix = np.zeros((matrix_size, matrix_size), dtype=int)

    for input_idx, output_binary in enumerate(bitmaps):
        output_idx = int(output_binary, 2)
        binary_mapping_matrix[output_idx, input_idx] = 1

    return binary_mapping_matrix


def make_truth_table_update(bitmaps):
    matrix = make_truth_table_matrix(bitmaps)
    print(matrix)

    def local_update(circuit, qubits):
        circuit.unitary(matrix, qubits)

    return local_update


def grid_pos_to_index(grid_width, grid_height, x, y, loop):
    if loop:
        x %= grid_width
        y %= grid_height
    elif x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return -1

    return y*grid_width + x


def index_to_grid_pos(grid_width, grid_height, index):
    assert 0 <= index < grid_width * grid_height
    x = index % grid_width
    y = index // grid_width
    return x, y


def make_grid_partitions(grid_width, grid_height, partition_width, partition_height, shift_x, shift_y, loop=True):
    partitions = []

    start_x = shift_x % partition_width
    start_y = shift_y % partition_height

    if loop:
        assert grid_width % partition_width == 0 and grid_height % partition_height == 0
        partition_count_x = grid_width // partition_width
        partition_count_y = grid_height // partition_height
    else:
        partition_count_x = (grid_width-start_x) // partition_width
        partition_count_y = (grid_height-start_y) // partition_height

    for py in range(0, partition_count_y):
        for px in range(0, partition_count_x):
            sx = start_x + px*partition_width
            sy = start_y + py*partition_height
            partition = []

            for y in range(sy, sy+partition_height):
                for x in range(sx, sx+partition_width):
                    partition.append(grid_pos_to_index(grid_width, grid_height, x, y, loop))

            partitions.append(partition)

    return partitions


def apply_global_update(circuit, partitions, local_update):
    for qubits in partitions:
        local_update(circuit, qubits)


def init_binary(circuit, bitmap):
    for i in range(len(bitmap)):
        if bitmap[i] == '1':
            circuit.x(i)
