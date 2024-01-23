from qiskit import Aer, execute
from qiskit_ibm_runtime import QiskitRuntimeService


def simulate(circuit, use_real=False):
    if use_real:
        service = QiskitRuntimeService()
        simulator = service.least_busy(simulator=False, operational=True)
    else:
        simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    return counts
