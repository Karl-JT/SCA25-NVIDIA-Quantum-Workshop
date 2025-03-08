"""
functions:
    run_qaoa_cudaq_opt
    run_qaoa_opt
    run_qaoa_glob_opt
"""

import numpy as np
import cudaq
from src_cudaq.fourier import build_fourier_params, fourier_amplitude_init
from src_cudaq.qaoa_converter import create_cost_Hamiltonian, create_mixer_Hamiltonian
from src_cudaq.circuits import qaoa_fourier_kernel


def run_qaoa_cudaq_opt(depth, q, num_qubits, cost_operator, cost_pauli_coeffs, cost_pauli_words, mixer_words, offset, optimum_known, max_iterations=200, seed=37, verbose=False):
    cudaq.set_random_seed(seed)
    np.random.seed(seed)

    # Initial Fourier amplitudes
    init_amps = fourier_amplitude_init(q)

    # Build the kernel once (shared across evaluations)
    kernel, _ = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)

    # Define objective function: Fourier amps -> params -> cost
    def objective(amps):
        params = build_fourier_params(amps, depth, q).flatten()
        return cudaq.observe(kernel, cost_operator, params).expectation() + offset

    # CUDA-Q optimizer (COBYLA as example)
    optimizer = cudaq.optimizers.COBYLA()
    optimizer.max_iterations = max_iterations
    optimizer.initial_parameters = init_amps

    optimal_value, optimal_amps = optimizer.optimize(
        dimensions=len(init_amps),
        function=objective
    )

    return optimal_value, optimal_amps


from scipy.optimize import minimize,differential_evolution

def run_qaoa_opt(depth, q, num_qubits, cost_operator, cost_pauli_coeffs, cost_pauli_words, mixer_words, offset, optimum_known, max_iterations=200, seed=37, verbose=False):        
    cudaq.set_random_seed(seed)
    np.random.seed(seed)

    init_amps = fourier_amplitude_init(q)
    
    kernel, _ = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)

    def cost_function(amps):
        params = build_fourier_params(amps, depth, q).flatten()
        return cudaq.observe(kernel, cost_operator, params).expectation() + offset

    bounds = [(-np.pi, np.pi)] * (2 * q)

    result = minimize(
        cost_function,
        init_amps,
        method='L-BFGS-B',
        bounds=bounds,
        options={'maxiter': max_iterations, 'disp': verbose},
    )

    optimal_value = result.fun
    optimal_amps = result.x
    optimal_params = build_fourier_params(optimal_amps, depth, q).flatten()

    return optimal_value, optimal_params


def run_qaoa_glob_opt(depth, q, num_qubits, cost_operator, cost_pauli_coeffs, cost_pauli_words, mixer_words, offset, optimum_known, max_iterations=200, seed=37, verbose=False):        
        
    cudaq.set_random_seed(seed)
    np.random.seed(seed)

    init_amps = fourier_amplitude_init(q)

    kernel, _ = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)

    def cost_function(amps):
        params = build_fourier_params(amps, depth, q).flatten()
        return cudaq.observe(kernel, cost_operator, params).expectation()

    bounds = [(-np.pi, np.pi)] * (2 * q)

    result = differential_evolution(
        cost_function,
        bounds=bounds,
        maxiter=max_iterations,
        seed=seed,
        disp=verbose,
        polish=True  # optional, tries to refine result at the end with L-BFGS-B
    )

    optimal_value = result.fun
    optimal_amps = result.x
    optimal_params = build_fourier_params(optimal_amps, depth, q).flatten()
    return optimal_value, optimal_params
    
    
    