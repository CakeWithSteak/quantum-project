import numpy
from qiskit import QuantumCircuit

from src.simulate import simulate
from src.utils import make_grid_partitions, make_truth_table_update, apply_global_update, init_binary
from src.visualize import visualize_grid, visualize_grid_animation, visualize_line_multi

# local_update = make_truth_table_update([
#     '0000', '1000', '0100', '1100',
#     '0010', '1010', '1001', '1110',
#     '0001', '0110', '0101', '1101',
#     '0011', '1011', '0111', '1111'])

N = 10
T = 40

islands = [(2*i, 2*i+1) for i in range(N)]

partition1 = []
for i in range(N):
    l = islands[i]
    r = islands[(i+1) % N]
    partition1.append([l[1], r[0]])

partition2 = []
for i in range(N):
    l = islands[i]
    r = islands[(i+1) % N]
    partition2.append([l[0], r[1]])

# partition1 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]]
# partition2 = [[0, 3], [2, 5], [4, 7], [6, 9], [8, 1]]

print(partition2)

'''
(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)

     1-2     3-4     5-6      7-8    9-0
    
(1, 0), (3, 2), (5, 4), (7, 6), (9, 8) 

     0-3     2-5     4-7      6-9     8-1


'''

partitions = [partition1, partition2]

def test_update(circuit, qubits):
    epsilon = 1
    m = 1
    s = numpy.sin(m * epsilon)
    c = numpy.cos(m * epsilon)

    matrix = [[1, 0, 0, 0],
              [0, -1j * s, c, 0],
              [0, c, -1j * s, 0],
              [0, 0, 0, 1]]

    # matrix = [[1, 0, 0, 0],
    #           [0, 0, 1, 0],
    #           [0, 1, 0, 0],
    #           [0, 0, 0, 1]]

    circuit.unitary(matrix, qubits)

multiple_counts = []

for total_steps in range(T):
    circuit = QuantumCircuit(N*2)


    circuit.x(3)
    # circuit.x(16)
    # circuit.h(0)
    # circuit.h(15)

    for step in range(total_steps):
        apply_global_update(circuit, partitions[step % len(partitions)], test_update)

    circuit.measure_all()
    counts = simulate(circuit)
    multiple_counts.append(counts)

# print(multiple_counts)
visualize_line_multi(N*2, T, multiple_counts)
# visualize_grid_animation(N, N, multiple_counts)
