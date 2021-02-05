from QuantumComputer import Numbers
from QuantumComputer import Psi

# Please enter the number of qubits for the circuit and the number of shots to be simulated
NUMBER_OF_QUBITS = 4
NUMBER_OF_SHOTS = 1024

# Please enter your circuit below. See readme for instructions
circuit = [
    {"gate": "h", "target": [0]},
    {"gate": "cx", "target": [0, 1]},
    {"gate": "u3", "target": [2], "parameters": {"phi": Numbers.HALF_PI, "theta": Numbers.HALF_PI, "lamb": Numbers.PI}}
]

# This code will run you circuit as many times as you desired and output the results
psi = Psi(NUMBER_OF_QUBITS)
psi.run(circuit)
psi.display_counts(NUMBER_OF_SHOTS)
