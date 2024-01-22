import numpy as np
from qiskit import QuantumCircuit

from src.utils.simulate import simulate
from src.utils.utils import make_grid_partitions, apply_global_update
from src.utils.visualize import visualize_line_over_time

N = 20
T = 50

partitions_A = make_grid_partitions(N, 1, 2, 1, 0, 0, True)
partitions_D = make_grid_partitions(N, 1, 2, 1, 1, 0, True)
partitions = [partitions_A, partitions_D]


def local_update(circuit, qubits):
    matrix = [
        [1, 0, 0, 0],
        [0, np.sqrt(1/2), np.sqrt(1/2), 0],
        [0, np.sqrt(1/2), -np.sqrt(1/2), 0],
        [0, 0, 0, 1] # np.exp(1j * np.pi / 4)
    ]

    circuit.unitary(matrix, qubits)


multiple_counts = []

for total_steps in range(T):
    circuit = QuantumCircuit(N)

    circuit.x(4)

    circuit.x(15)

    for step in range(total_steps):
        apply_global_update(circuit, partitions[step % len(partitions)], local_update)

    circuit.measure_all()
    counts = simulate(circuit)
    multiple_counts.append(counts)

visualize_line_over_time(N, T, multiple_counts)
