from qiskit import QuantumCircuit

from src.simulate import simulate
from src.utils import make_grid_partitions, make_truth_table_update, apply_global_update, init
from src.visualize import visualize_grid, visualize_grid_animation

N = 4

partitions_A = make_grid_partitions(N, N, 2, 2, 0, 0, False)
partitions_B = make_grid_partitions(N, N, 2, 2, 0, 1, False)
partitions_C = make_grid_partitions(N, N, 2, 2, 1, 0, False)
partitions_D = make_grid_partitions(N, N, 2, 2, 1, 1, False)

local_update = make_truth_table_update([
    '0000', '1000', '0100', '1100',
    '0010', '1010', '1001', '1110',
    '0001', '0110', '0101', '1101',
    '0011', '1011', '0111', '1111'])

partitions = [partitions_A, partitions_B, partitions_C, partitions_D]
multiple_counts = []

for total_steps in range(10):
    circuit = QuantumCircuit(N*N)

    init(circuit,
         '1001'
         '0000'
         '0000'
         '0000')

    # circuit.h(1)
    # circuit.cx(1, 0)

    for step in range(total_steps):
        apply_global_update(circuit, partitions[step % len(partitions)], local_update)

    circuit.measure_all()
    counts = simulate(circuit)
    multiple_counts.append(counts)

visualize_grid_animation(N, N, multiple_counts)
