import numpy
import matplotlib.pyplot as plot
import collections
from enum import Enum


class Psi:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = numpy.zeros(2 ** num_qubits)
        self.state[0] = 1

    def run(self, circuit):
        error_returned = self._verify(circuit)
        if error_returned == Error.NONE:
            for operator in circuit:
                gate = operator.get("gate")
                if gate in Operators.SINGLE_PARAMETER or gate in Operators.THREE_PARAMETER:
                    self._operate(gate, operator.get("target"), operator.get("parameters"))
                else:
                    self._operate(gate, operator.get("target"))
        else:
            self._print_error(error_returned)

    def display_counts(self, num_shots):
        results = self._get_counts(num_shots)
        title = "Result of " + str(num_shots) + " Shots"
        Psi._print_counts(results, title, num_shots)
        Psi._plot_counts(results, title)

    def _verify(self, circuit):
        for operator in circuit:
            operator_keys = operator.keys()
            if "gate" not in operator_keys:
                return Error.OPERATOR_NOT_EXIST
            if operator.get("gate") not in Operators.UNARY and operator.get("gate") not in Operators.BINARY:
                return Error.WRONG_OPERATOR
            if "target" not in operator_keys:
                return Error.MISSING_PARAMETER
            targets = operator.get("target")
            if max(targets) > self.num_qubits - 1 or min(targets) < 0:
                return Error.TARGET_OUTSIDE_SCOPE
            if operator.get("gate") in Operators.UNARY:
                if len(targets) < 1:
                    return Error.NOT_ENOUGH_TARGETS
                elif len(targets) > 1:
                    return Error.TOO_MANY_TARGETS
            elif operator.get("gate") in Operators.BINARY:
                if len(targets) < 2:
                    return Error.NOT_ENOUGH_TARGETS
                elif len(targets) > 2:
                    return Error.TOO_MANY_TARGETS
            if operator.get("gate") in Operators.PARAMETERIZED:
                parameterized_verification = Psi._verify_parameterized(operator)
                if parameterized_verification != Error.NONE:
                    return parameterized_verification
        return Error.NONE

    @staticmethod
    def _verify_parameterized(operator):
        if "parameters" not in operator:
            return Error.MISSING_PARAMETER
        gate = operator.get("gate")
        parameters = operator.get("parameters")
        if "phi" not in parameters:
            return Error.MISSING_PARAMETER
        if gate in Operators.THREE_PARAMETER:
            if "theta" not in parameters or "lamb" not in parameters:
                return Error.MISSING_PARAMETER
        return Error.NONE

    @staticmethod
    def _print_error(error_returned):
        error_string_tuple = {
            Error.NOT_ENOUGH_TARGETS: "Your circuit is missing targets.",
            Error.OPERATOR_NOT_EXIST: "Your circuit is missing operators.",
            Error.MISSING_PARAMETER: "Your circuit is missing necessary parameters",
            Error.TARGET_OUTSIDE_SCOPE: "Your circuit has a target qubit that does not exist in this computer.",
            Error.TOO_MANY_TARGETS: "Your circuit includes more targets than allowed by a gate.",
            Error.WRONG_OPERATOR: "You circuit includes an illegal gate."
        }
        print("Please double check your circuit.")
        print(error_string_tuple.get(error_returned))

    def _operate(self, gate, targets, *args):
        if gate in Operators.SINGLE_PARAMETER or gate in Operators.THREE_PARAMETER:
            self.state = numpy.dot(self.state, self._get_unary_operator(gate, targets[0], args))
        elif gate in Operators.UNARY:
            self.state = numpy.dot(self.state, self._get_unary_operator(gate, targets[0]))
        elif gate in Operators.BINARY:
            self.state = numpy.dot(self.state, self._get_binary_operator(gate, targets))

    def _get_unary_operator(self, gate, target_qubit, *args):
        # return unitary operator of size 2**n x 2**n for given gate and target qubits
        phi, theta, lamb = [0, 0, 0]
        if gate in Operators.SINGLE_PARAMETER or gate in Operators.THREE_PARAMETER:
            phi = args[0][0].get("phi")
            if gate in Operators.THREE_PARAMETER:
                theta = args[0][0].get("theta")
                lamb = args[0][0].get("lamb")
        # Uncomment line below to see the single qubit operator matrix
        # print(gate + " Operator: \n", gate_tuple.get(gate))
        operator = 1
        for i in range(self.num_qubits):
            if i == target_qubit:
                operator = numpy.kron(operator, Operators.get(gate, phi, theta, lamb))
            else:
                operator = numpy.kron(operator, Matrices.identity)
        # Uncomment line below to see operator matrix
        # print(operator)
        return operator

    def _get_binary_operator(self, gate, targets):
        control, target = targets
        first_half = 1
        second_half = 1
        for i in range(self.num_qubits):
            if i == control:
                first_half = numpy.kron(first_half, Matrices.p0x0)
                second_half = numpy.kron(second_half, Matrices.p1x1)
            elif i == target:
                first_half = numpy.kron(first_half, Matrices.identity)
                second_half = numpy.kron(second_half, Operators.get(gate, 0, 0, 0))
            else:
                first_half = numpy.kron(first_half, Matrices.identity)
                second_half = numpy.kron(second_half, Matrices.identity)
        # Uncomment line below to see operator matrix
        # print(first half + second_half)
        return first_half + second_half

    def _measure_all(self):
        state = numpy.absolute(self.state) ** 2
        values = []
        for i in range(2 ** self.num_qubits):
            values.append(i)
        return numpy.random.choice(values, 1, p=state)[0]

    def _get_counts(self, num_shots):
        results = collections.OrderedDict()
        for i in range(num_shots):
            result = self._measure_all()
            if result not in results:
                results[result] = 0
            results[result] += 1
        for result in sorted(list(results.keys())):
            results['{0:b}'.format(result).zfill(self.num_qubits)] = results.pop(result)
        return results

    @staticmethod
    def _plot_counts(results, title):
        plot_x = numpy.arange(len(results.keys()))
        plot.bar(plot_x, results.values())
        plot.xticks(plot_x, results.keys())
        plot.ylabel('Shots')
        plot.xlabel('Outcome')
        plot.title(title)
        plot.show()

    @staticmethod
    def _print_counts(results, title, num_shots):
        print(title)
        for result in results:
            print("    ", result, ":", results.get(result), ",", results.get(result) / num_shots * 100, "%")


class Error(Enum):
    NONE = 0
    OPERATOR_NOT_EXIST = 1
    TARGET_OUTSIDE_SCOPE = 2
    TOO_MANY_TARGETS = 3
    NOT_ENOUGH_TARGETS = 4
    MISSING_PARAMETER = 5
    WRONG_OPERATOR = 6


class Matrices:
    x_gate = numpy.array([[0, 1], [1, 0]])
    y_gate = numpy.zeros((2, 2), dtype=numpy.complex_) + [[0, complex(0, -1)], [complex(0, 1), 0]]
    s_gate = numpy.zeros((2, 2), dtype=numpy.complex_) + [[1, 0], [0, complex(0, 1)]]
    t_gate = numpy.zeros((2, 2), dtype=numpy.complex_) + [[1, 0], [0, numpy.e**(numpy.pi*1j/4)]]
    z_gate = numpy.array([[1, 0], [0, -1]])
    h_gate = numpy.array([[1 / numpy.sqrt(2), 1 / numpy.sqrt(2)], [1 / numpy.sqrt(2), -1 / numpy.sqrt(2)]])
    p0x0 = numpy.array([[1, 0], [0, 0]])
    p1x1 = numpy.array([[0, 0], [0, 1]])
    identity = numpy.identity(2)

    @staticmethod
    def u3_operator(phi, theta, lamb):
        first_term = numpy.cos(theta / 2)
        second_term = -numpy.e**(complex(0, 1) * lamb) * numpy.sin(theta / 2)
        third_term = numpy.e**(complex(0, 1) * phi) * numpy.sin(theta / 2)
        fourth_term = numpy.e**(complex(0, 1) * (lamb + phi)) * first_term
        return numpy.array([[first_term, second_term], [third_term, fourth_term]])

    @staticmethod
    def r_operator(phi):
        return numpy.array([[1, 0], [0, 0]]) + [[0, 0], [0, numpy.e**(complex(0, 1) * phi)]]


class Operators:
    UNARY = ["x", "h", "y", "z", "s", "t", "u3", "r"]
    BINARY = ["cx", "cy", "cz"]
    SINGLE_PARAMETER = ["r"]
    THREE_PARAMETER = ["u3"]
    PARAMETERIZED = [SINGLE_PARAMETER, THREE_PARAMETER]

    @staticmethod
    def get(gate, phi, theta, lamb):
        operator_matricies = {
            "x": Matrices.x_gate,
            "h": Matrices.h_gate,
            "y": Matrices.y_gate,
            "z": Matrices.z_gate,
            "s": Matrices.s_gate,
            "t": Matrices.t_gate,
            "u3": Matrices.u3_operator(phi, theta, lamb),
            "r": Matrices.r_operator(phi),
            "cx": Matrices.x_gate,
            "cy": Matrices.y_gate,
            "cz": Matrices.z_gate
        }
        return operator_matricies.get(gate)


class Numbers:
    PI = numpy.pi
    HALF_PI = numpy.pi / 2
    QUARTER_PI = numpy.pi / 4
