"""
functions:
    Q_to_Ising
    create_cost_Hamiltonian
    create_mixer_Hamiltonian
"""

import pennylane as qml
from pennylane import numpy as np
from collections import defaultdict


def Q_to_Ising(Q, offset=0):
    """
    Converts the Q matrix in a QUBO problem into Ising Hamiltonian coefficients.
    """
    num_qubits = len(Q)
    h = defaultdict(int)
    J = defaultdict(int)
    oneq_operators = []
    twoq_operators = []

    for i in range(num_qubits):
        h[(i,)] -= Q[i, i] / 2
        offset += Q[i, i] / 2
        oneq_operators.append(qml.PauliZ(i))

        for j in range(i + 1, num_qubits):
            J[(i, j)] = Q[i, j] / 4
            h[(i,)] -= Q[i, j] / 4
            h[(j,)] -= Q[i, j] / 4
            offset += Q[i, j] / 4
            twoq_operators.append(qml.PauliZ(i) @ qml.PauliZ(j))

    return h, J, offset, oneq_operators, twoq_operators


def create_cost_Hamiltonian(Q, converted=0, h=None, J=None, offset=0, oneq_operators=None, twoq_operators=None):
    """
    Creates the Ising Hamiltonian from the QUBO matrix or provided Ising coefficients.
    """
    if converted == 0:
        if Q is None:
            raise ValueError("Q must be provided if converted = 0")

        h, J, offset, oneq_operators, twoq_operators = Q_to_Ising(Q, offset=offset)

    if converted == 1:
        if (oneq_operators is None) or (twoq_operators is None):
            raise ValueError("Operator lists are required if Q is already converted.")

    coeffs = list(h.values()) + list(J.values())
    coeff_max = max(abs(c) for c in coeffs)
    operators = oneq_operators + twoq_operators

    return qml.Hamiltonian(coeffs, operators), offset, coeff_max


def create_mixer_Hamiltonian(num_qubits, a=1.0, b=0.0):
    """
    Creates a custom mixer Hamiltonian with tunable (a, b) coefficients. It is the typical mixer Hamiltonian by default.
    """
    coefficients = []
    operators = []

    for i in range(num_qubits):
        coefficients.append(-a)
        operators.append(qml.PauliX(i))
        coefficients.append(-b)
        operators.append(qml.PauliZ(i))

    return qml.Hamiltonian(coefficients, operators)
