# Quantum Simulator
This is a simple quantum computer simulator written as a submission to accompany my application to the Quantum Open Source Foundation's Quantum Computing Mentorship program.


## Language and Dependencies
This program is written in Python 3. The following dependencies must be installed to run this simulator:
* numpy
* matplotlib

## Task Description

Task instructions are located [here](https://github.com/quantastica/qosf-mentorship/blob/master/qosf-simulator-task.ipynb). 
Below are the basic requirements the simulator must accomplish:
* Initialize state
* Read a program (circuit)
* Performs the following tasks for each gate in the circuit:
  * Calculate the matrix operator
  * Apply the operator to modify the state
* Perform a multi-shot measurement of all qubits using weighted random technique

The number of qubits simulated have an exponential effect on system requirements.
This was tested and ran smoothly up to at least 12 qubits.
It is also worth mentioning this circuit only needs to be able to perform single qubit operations (gates) and the CNOT (CX) operation/gate.

## Using the Simulator
As long as the proper dependencies are installed in the local environment, the two sourcecode files (QuantumComputer.py and main.py) are all that is necessary to run the simulator.
The only file that needs any modification is "main.py," which only requires the following user inputs:
* The circuit to be simulated
* The number of qubits for the circuit
* The number of shots to simulate

The simulator uses **big endian** encoding.

### Designing the Circuit
The circuit can accept the following gates:
Regular Unary Gates | Parameterized Unary Gates | Binary Gates
------------------- | ------------------------- | -------------
X, H, Y, Z, S, T | R, U3 | CNOT (CX), CY, CZ

The circuit should be programmed into a list, which each given as a dictionary with the following entries:
1. Gate - given as a lowercase string for the gate (x, h, y, z, s, t, r, u3, cx, cy, cz). 
2. target - given as a list. For binary operators, the first number is the control qubit, and the second number is the target qubit.
   The first qubit is represented by a zero, the second by a one, and so on. 
3. parameter - only needs to be included for operators that require parameters (r, u3).
    1. phi
    2. theta
    3. lamb (for lambda)

Here is a sample circuit:
```python
[
    {"gate": "h", "target": [0]},
    {"gate": "cx", "target": [0, 1]},
    {"gate": "u3", "target": [2], "parameters": {"phi": Numbers.HALF_PI, "theta": Numbers.HALF_PI, "lamb": Numbers.PI}}
]
```

### Running the Program
The simulator can either be used by making use of "main.py," or by making other use of the "QuantumComputer.py" file.

#### main.py
To use the simulator using "main.py," the following parameters should be modified to a user's liking:
* `NUMBER_OF_QUBITS` should be assigned an integer value representing the number of qubits desired for the circuit
* `NUMBER_OF_SHOTS` should be assigned an integer value representing the number of shots the simulation should make for the circuit.
* `circuit` should be assigned a list that represents a circuit as described in *Designing the Circuit* above.

With those value assigned, "main.py" should be run interpreted and executed like any other Python program.
Pi, Pi/2, and Pi/4 can be used as parameter values with Numbers.PI, Numbers.HALF_PI, and Numbers.QUARTER_PI respectively.

#### QuantumComputer.py
"QuantumComputer.py" contains the `Psi` class, which represents a quantum computer and can be instantiated as an object and used by a user in whatever way they wish.
The following public methods apply to the class:
* Constructor: a `Psi(number_of_quibits)` object should be passed an integer number parameter representing the number of qubits for that system when an object is instantiated.
* Method `run(circuit)`: should be passed a list that represents a circuit as described in *Designing the Circuit* above.
* Method `display_counts(number_of_shots)`: when run on a `Psi` object, this will return the result of `number_of_shots` runs of the circuit.

### Inspecting Requirements
Since there are several simulator requirements that are hidden inside the Psi class, the following were placed into the program to make assessment easier.
1. `Psi` contains a `print_state()` method that will print the current state of the circuit instead of a weighted-probability measurement.
This can be used, for example, to confirm the initial state of the system has been created properly or to check that an operators has changed the state of the system.
2. Uncomment line 106 to print the operator matrix for a single qubit in a unary gate, line 114 to print the whole operator matrix for a unary gate,
and line 132 to print the operator matrix for a binary gate.
3. While not necessary for observation, commenting line 30 will suppress graphing the result.

## References
The following references were used when writing this program:
* Korponaić, P. (2021, February 2). Task: Quantum Circuit Simulator. Retrieved 11:59, February 5, 2021,
  from https://github.com/quantastica/qosf-mentorship/blob/master/qosf-simulator-task.ipynb
* Wikipedia contributors. (2021, February 5). Quantum logic gate. In Wikipedia, The Free Encyclopedia.
  Retrieved 10:56, February 5, 2021, from https://en.wikipedia.org/w/index.php?title=Quantum_logic_gate&oldid=1004966881
* Hidary, J. D. (2019). Quantum Computing: An Applied Approach (pp. 22-25). Cham: Springer.