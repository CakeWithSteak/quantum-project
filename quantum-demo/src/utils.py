import numpy as np


def make_truth_table_matrix(bitmaps):
    matrix_size = len(bitmaps)
    binary_mapping_matrix = np.zeros((matrix_size, matrix_size), dtype=int)

    for input_idx, output_binary in enumerate(bitmaps):
        output_idx = int(output_binary, 2)
        binary_mapping_matrix[output_idx, input_idx] = 1

    return binary_mapping_matrix


def make_basis(restrictions):
    basis = []
    bits_n = len(restrictions)

    for input_index in range(2 ** bits_n):
        valid = True
        for bit_index in range(bits_n):
            restriction = restrictions[bit_index]
            if restriction != -1 and not bit_equal(input_index, bit_index, restriction):
                valid = False
                break

        if valid:
            basis.append(input_index)

    return basis


def compress_matrix(matrix, basis):
    n = len(basis)
    compressed = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            compressed[i, j] = matrix[basis[i], basis[j]]

    return compressed


def make_truth_table_update(bitmaps):
    matrix = make_truth_table_matrix(bitmaps)

    def local_update(circuit, qubits, outside=0):
        restrictions = [outside if qubits[i] == -1 else -1 for i in range(len(qubits))]
        basis = make_basis(restrictions)

        compressed_matrix = compress_matrix(matrix, basis)
        compressed_qubits = [q for q in qubits if q != -1]
        circuit.unitary(compressed_matrix, compressed_qubits)

    return local_update


def bit_equal(number, index, target):
    return (number >> index) & 1 == target


def get_grid_index(grid_width, grid_height, x, y):
    if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
        return -1

    return y*grid_width + x


def make_grid_partitions(grid_width, grid_height, partition_width, partition_height, shift_x, shift_y):
    partitions = []

    start_x = shift_x % -partition_width
    start_y = shift_y % -partition_height

    for y in range(start_y, grid_height, partition_height):
        for x in range(start_x, grid_width, partition_width):
            partition = []

            for sy in range(y, y + partition_height):
                for sx in range(x, x+partition_width):
                    partition.append(get_grid_index(grid_width, grid_height, sx, sy))

            partitions.append(partition)

    return partitions


def apply_global_update(circuit, partitions, local_update, outside=0):
    for qubits in partitions:
        local_update(circuit, qubits, outside)
