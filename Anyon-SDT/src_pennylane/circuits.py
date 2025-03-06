"""
functions:
    qaoa_layer
    qaoa_layer_custom_mixer
    circuit
    circuit_custom_mixer
    cost_function
    cost_function_custom_mixer
    prob_populations
    prob_populations_custom_mixer
    calculate_cost
"""

import pennylane as qml
import numpy as np


def qaoa_layer(gamma, beta, cost_hamiltonian, mixer_hamiltonian):
    qml.evolve(cost_hamiltonian, gamma)
    qml.evolve(mixer_hamiltonian, beta)
    

def circuit(params, depth, cost_hamiltonian, mixer_hamiltonian, wires):
    for w in range(wires):
        qml.Hadamard(w)
    for d in range(depth):
        gamma = params[0][d]
        beta = params[1][d]
        qaoa_layer(gamma, beta, cost_hamiltonian, mixer_hamiltonian)


def cost_function(params, depth, cost_hamiltonian, mixer_hamiltonian, wires, device, normalized=True):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit(params, depth, cost_hamiltonian, mixer_hamiltonian, wires)
        return qml.expval(cost_hamiltonian if normalized else cost_hamiltonian)

    return qaoa_circuit()


def prob_populations(params, depth, cost_hamiltonian, mixer_hamiltonian, wires, device):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit(params, depth, cost_hamiltonian, mixer_hamiltonian, wires)
        return qml.probs(wires=range(wires))

    return qaoa_circuit()


def qaoa_layer_cm(gamma, beta, a, b, cost_hamiltonian, wires):
    qml.evolve(cost_hamiltonian, gamma)
    mixer_hamiltonian = cm_mixer_hamiltonian_layer(a, b, wires)
    qml.evolve(mixer_hamiltonian, beta)


def circuit_cm(params, depth, cost_hamiltonian, wires):
    for w in range(wires):
        qml.Hadamard(w)
    for d in range(depth):
        gamma = params[0][d]
        beta = params[1][d]
        a = params[2][d]
        b = params[3][d]
        qaoa_layer_cm(gamma, beta, a, b, cost_hamiltonian, wires)


def cost_function_cm(params, depth, cost_hamiltonian, wires, device, normalized=True):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit_cm(params, depth, cost_hamiltonian, wires)
        return qml.expval(cost_hamiltonian if normalized else cost_hamiltonian)

    return qaoa_circuit()


def prob_populations_cm(params, depth, cost_hamiltonian, wires, device):
    @qml.qnode(device)
    def qaoa_circuit():
        circuit_cm(params, depth, cost_hamiltonian, wires)
        return qml.probs(wires=range(wires))

    return qaoa_circuit()


def calculate_cost(spin_config, Q):
    spin_config = np.array(list(spin_config), dtype=int)
    return spin_config.T @ Q @ spin_config
