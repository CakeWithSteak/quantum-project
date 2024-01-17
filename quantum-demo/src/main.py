
from qiskit import QuantumCircuit, Aer, execute
from src.utils import make_grid_partitions, make_truth_table_update, apply_global_update

partitions_A = make_grid_partitions(4, 2, 2, 1, 0, 0, True)
partitions_B = make_grid_partitions(4, 2, 2, 1, 1, 0, True)

local_update = make_truth_table_update(['01', '10', '11', '00'])

circuit = QuantumCircuit(8)
apply_global_update(circuit, partitions_A, local_update)
apply_global_update(circuit, partitions_B, local_update)

circuit.measure_all()
print(circuit.draw())

# simulate
simulator = Aer.get_backend('qasm_simulator')
job = execute(circuit, simulator, shots=1000)
result = job.result()
counts = result.get_counts(circuit)
print(counts)
