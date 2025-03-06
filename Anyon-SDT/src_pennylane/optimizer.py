"""
functions:
    run_qaoa_vqe_adiabatic
    run_qaoa_vqe_fourier
"""

import numpy as np
from pennylane.optimize import AdamOptimizer
from src_pennylane.circuits import cost_function, cost_function_cm
from src_pennylane.fourier import build_fourier_params, fourier_amplitude_init


def run_qaoa_vqe_fourier(depth, q, Q, num_qubits, device, cost_hamiltonian, max_iterations=200, seed=37, stepsize=0.1):
    np.random.seed(seed)

    init_amps = fourier_amplitude_init(q)
    params = build_fourier_params(init_amps, depth, q)

    optimizer = AdamOptimizer(stepsize)

    for i in range(max_iterations):
        params = optimizer.step(
            lambda p: cost_function_cm(p, depth, cost_hamiltonian, num_qubits, device),
            params
        )
        if i % 10 == 0:
            cost = cost_function_cm(params, depth, cost_hamiltonian, num_qubits, device)
            print(f"Iteration {i}: Cost = {cost}")

    final_cost = cost_function_cm(params, depth, cost_hamiltonian, num_qubits, device)
    return final_cost, params
