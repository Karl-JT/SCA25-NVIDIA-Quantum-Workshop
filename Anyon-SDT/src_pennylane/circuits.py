"""
functions:
    qaoa_layer
    qaoa_layer_custom
    circuit
    circuit_custom
    cost_function
    cost_function_custom
    prob_populations
    prob_populations_custom
    calculate_cost
"""

import pennylane as qml
from pennylane import numpy as np
from pennylane import qaoa as qaoa
from src_pennylane.qaoa_converter import create_mixer_Hamiltonian


# ----- QAOA Layers -----

def qaoa_layer(gamma, beta, H_C, mixer_hamiltonian):
    qaoa.cost_layer(gamma, H_C)
    qaoa.mixer_layer(beta, mixer_hamiltonian)


def qaoa_layer_custom(gamma, beta, a, b, H_C, num_qubits):
    qaoa.cost_layer(gamma, H_C)
    mixer_hamiltonian = create_mixer_Hamiltonian(num_qubits, a, b)
    qaoa.mixer_layer(beta, mixer_hamiltonian)

# ----- Circuits -----

def circuit(params, depth, H_C, mixer_hamiltonian, wires):
    for w in range(wires):
        qml.Hadamard(w)
    for d in range(depth):
        gamma = params[0][d]
        beta = params[1][d]
        qaoa_layer(gamma, beta, H_C, mixer_hamiltonian)


def circuit_custom(params, depth, H_C, wires):
    num_qubits = wires
    for w in range(wires):
        qml.Hadamard(w)
    for d in range(depth):
        gamma = params[0][d]
        beta = params[1][d]
        a = params[2][d]
        b = params[3][d]
        qaoa_layer_custom(gamma, beta, a, b, H_C, num_qubits)

# ----- Cost Functions -----

def cost_function(params, depth, H_C, cost_hamiltonian, mixer_hamiltonian, wires, device, normalized=True):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit(params, depth, H_C, mixer_hamiltonian, wires)
        return qml.expval(H_C if normalized else cost_hamiltonian)
    return qaoa_circuit()


def cost_function_custom(params, depth, H_C, cost_hamiltonian, wires, device, normalized=True):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit_custom(params, depth, H_C, wires)
        return qml.expval(H_C if normalized else cost_hamiltonian)
    return qaoa_circuit()

# ----- Probability Functions -----

def prob_populations(params, depth, H_C, mixer_hamiltonian, wires, device):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit(params, depth, H_C, mixer_hamiltonian, wires)
        return qml.probs(wires=range(wires))
    return qaoa_circuit()


def prob_populations_custom(params, depth, H_C, wires, device):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit_custom(params, depth, H_C, wires)
        return qml.probs(wires=range(wires))
    return qaoa_circuit()

# ----- Cost Evaluation -----

def calculate_cost(spin_config, Q):
    spin_config = np.array(list(spin_config), dtype=int)
    return spin_config.T @ Q @ spin_config