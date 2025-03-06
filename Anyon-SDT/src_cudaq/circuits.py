"""
functions: 
    qaoa_fourier_circuit
    cost_function_fourier
    calculate_cost
"""

import cudaq
import numpy as np
from cudaq import spin
from src_cudaq.fourier import build_fourier_params
from src_cudaq.qaoa_converter import create_cost_Hamiltonian, create_mixer_Hamiltonian


def qaoa_fourier_kernel(depth, num_qubits, cost_terms, mixer_words):
    """
    Returns a CUDA-Q kernel for the QAOA Fourier ansatz.
    """
    param_count = 2 * depth  # gammas and betas
    kernel, params = cudaq.make_kernel(list)
    qubits = kernel.qalloc(num_qubits)

    # Initialize |+>^n state
    kernel.h(qubits)

    for layer in range(depth):
        gamma = params[layer]
        beta = params[depth + layer]

        # Apply cost Hamiltonian terms
        for coeff, op in cost_terms:
            kernel.exp_pauli(gamma * coeff, qubits, op)

        # Apply mixer Hamiltonian terms (all with -1 coefficient)
        for word in mixer_words:
            kernel.exp_pauli(-beta, qubits, word)

    return kernel, param_count
    

def cost_function_fourier(amps, depth, q, Q, num_qubits):
    params = build_fourier_params(amps, depth, q).flatten()

    cost_operator, cost_pauli_coeffs, cost_pauli_words, _, _ = create_cost_Hamiltonian(Q)
    _, mixer_words = create_mixer_Hamiltonian(num_qubits)  # standard X mixer
    kernel, param_count = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)

    result = cudaq.observe(kernel, cost_operator, parameter_values=params)

    return result.expectation()


def calculate_cost(spin_config, Q):
    """
    Calculates the cost of a spin configuration.
    """
    spin_config = np.array(list(spin_config), dtype=int)
    return spin_config.T @ Q @ spin_config



# def qaoa_fourier_circuit(gammas, betas, a_params, b_params, depth, cost_terms, num_qubits):
#     """
#     This is the Quantum circuit
#     """
#     @cudaq.kernel
#     def circuit():
#         qubits = cudaq.qvector(num_qubits)

#         # Initialize |+>^n state
#         for qubit in qubits:
#             cudaq.h(qubit)

#         for layer in range(depth):
#             # Apply cost Hamiltonian evolution
#             for coeff, op in cost_terms:
#                 cudaq.exp_pauli(coeff * gammas[layer], op)

#             # Update mixer for this layer with corresponding a, b
#             mixer_terms = create_mixer_Hamiltonian(a_params[layer], b_params[layer], num_qubits)
            
#             # Apply custom (a, b)-mixer Hamiltonian evolution
#             for coeff, op in mixer_terms:
#                 cudaq.exp_pauli(coeff * betas[layer], op)

#         return qubits

#     return circuit


# def cost_function_fourier(amps, depth, q, Q, num_qubits):
#     """
#     Builds parameters from Fourier amplitudes and returns the expected cost.
#     """
#     params = build_fourier_params(amps, depth, q)
#     gammas, betas, a_params, b_params = params

#     cost_terms, _ = create_cost_Hamiltonian(Q)

#     kernel = qaoa_fourier_circuit(gammas, betas, a_params, b_params, depth, cost_terms, num_qubits)
#     result = cudaq.observe(kernel, cost_terms)

#     return result.expectation()


def calculate_cost(spin_config, Q):
    """
    Calculates the cost of a spin configuration
    """
    spin_config = np.array(list(spin_config), dtype=int)
    return spin_config.T @ Q @ spin_config