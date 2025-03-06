"""
functions: 
    Q_to_Ising
    create_cost_Hamiltonian
    create_mixer_Hamiltonian
"""

import numpy as np
from cudaq import spin
from collections import defaultdict


def Q_to_Ising(Q, offset=0):
    """
    Converts the Q matrix in a QUBO problem into the coefficients in an Ising Hamiltonian
    """
    num_qubits = len(Q)
    h = defaultdict(int)
    J = defaultdict(int)

    for i in range(num_qubits):
        h[(i,)] -= Q[i, i] / 2
        offset += Q[i, i] / 2

        for j in range(i + 1, num_qubits):
            J[(i, j)] = Q[i, j] / 4
            h[(i,)] -= Q[i, j] / 4
            h[(j,)] -= Q[i, j] / 4
            offset += Q[i, j] / 4

    return h, J, offset


def create_cost_Hamiltonian(Q):
    """
    Based on the calculated Ising coefficients, constructs the cost Hamiltonian 
    """
    h, J, offset = Q_to_Ising(Q)
    coeff_max = max(abs(k) for k in list(h.values()) + list(J.values()))

    operator_terms = []
    pauli_words = []
    pauli_coeffs = []
    num_qubits = len(Q)

    for (i,), coeff in h.items():
        normalized_coeff = coeff / coeff_max
        operator_terms.append(normalized_coeff * spin.z(i))
        pauli_word = ['I'] * num_qubits
        pauli_word[i] = 'Z'
        pauli_words.append(''.join(pauli_word))
        pauli_coeffs.append(normalized_coeff)

    for (i, j), coeff in J.items():
        normalized_coeff = coeff / coeff_max
        op_string = ['I'] * num_qubits
        op_string[i] = 'Z'
        op_string[j] = 'Z'
        pauli_words.append(''.join(op_string))
        pauli_coeffs.append(normalized_coeff)
        operator_terms.append(normalized_coeff * spin.z(i) * spin.z(j))

    cost_operator = sum(operator_terms)

    return cost_operator, pauli_coeffs, pauli_words, coeff_max, offset


def create_mixer_Hamiltonian(num_qubits):
    """
    Constructs custom (a, b)-tunable mixer Hamiltonian 
    """
    operator_terms = []
    pauli_words = []

    for i in range(num_qubits):
        operator_terms.append((-1, spin.x(i)))

        x_word = ['I'] * num_qubits
        x_word[i] = 'X'
        pauli_words.append(''.join(x_word))
    return operator_terms, pauli_words