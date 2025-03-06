"""
functions:
    run_qaoa_vqe
"""

import numpy as np
import cudaq
from src_cudaq.fourier import build_fourier_params, fourier_amplitude_init
from src_cudaq.qaoa_converter import create_cost_Hamiltonian, create_mixer_Hamiltonian
from src_cudaq.circuits import qaoa_fourier_kernel


# def run_qaoa_vqe(depth, q, Q, num_qubits, max_iterations=200, seed=37):
#     """
#     Runs VQE using CUDA-Q optimizers on the QAOA Fourier ansatz.
#     """
#     param_count = 2 * depth  # gammas and betas

#     cudaq.set_random_seed(seed)
#     np.random.seed(seed)

#     init_amps = build_fourier_params(
#         fourier_amplitude_init(q),
#         depth, q
#     ).flatten()
    
#     cost_operator, cost_pauli_coeffs, cost_pauli_words, _, _ = create_cost_Hamiltonian(Q)
#     _, mixer_words = create_mixer_Hamiltonian(num_qubits)

#     kernel, _ = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)
    
#     optimizer = cudaq.optimizers.COBYLA()
#     optimizer.max_iterations = max_iterations
#     optimizer.initial_parameters = init_amps
#     optimizer.lower_bounds = [-2*np.pi] * depth + [-2*np.pi] * depth
#     optimizer.upper_bounds = [2*np.pi] * depth + [2*np.pi] * depth

#     init_amps = np.clip(init_amps, optimizer.lower_bounds, optimizer.upper_bounds)

#     print(f"Initial parameters: {len(init_amps)}")
#     print(f"Kernel parameter count: {param_count}")

#     optimal_value, optimal_parameters = cudaq.vqe(
#         kernel=kernel,
#         spin_operator=cost_operator,
#         optimizer=optimizer,
#         parameter_count=param_count
#     )

    # return optimal_value, optimal_parameters

from scipy.optimize import minimize
def run_qaoa_vqe(depth, q, Q, num_qubits, max_iterations=200, seed=37):
    cudaq.set_random_seed(seed)
    np.random.seed(seed)

    init_amps = fourier_amplitude_init(q)

    cost_operator, cost_pauli_coeffs, cost_pauli_words, _, _ = create_cost_Hamiltonian(Q)
    _, mixer_words = create_mixer_Hamiltonian(num_qubits)

    kernel, _ = qaoa_fourier_kernel(depth, num_qubits, zip(cost_pauli_coeffs, cost_pauli_words), mixer_words)

    def cost_function(amps):
        params = build_fourier_params(amps, depth, q).flatten()
        return cudaq.observe(kernel, cost_operator, params).expectation()

    bounds = [(-np.pi, np.pi)] * (2 * q)

    result = minimize(
        cost_function,
        init_amps,
        method='L-BFGS-B',
        bounds=bounds,
        options={'maxiter': max_iterations, 'disp': False}
    )

    optimal_value = result.fun
    optimal_amps = result.x
    optimal_params = build_fourier_params(optimal_amps, depth, q).flatten()

    return optimal_value, optimal_params



# def adam_optimizer(cost_function, init_amps, steps=200, stepsize=0.1, clip_range=None):
#     """
#     Runs the Adam optimizer on the Fourier amplitudes using PyTorch.
#     """
#     amps = torch.tensor(init_amps, dtype=torch.float32, requires_grad=True)
#     optimizer = torch.optim.Adam([amps], lr=stepsize)

#     for step in range(steps):
#         optimizer.zero_grad()
#         loss = cost_function(amps.detach().numpy())
#         loss_tensor = torch.tensor(loss, requires_grad=True)
#         loss_tensor.backward()
#         optimizer.step()

#         if clip_range:
#             lower, upper = clip_range
#             with torch.no_grad():
#                 amps.clamp_(lower, upper)

#         if step % 50 == 0:
#             print(f"Step {step}: Cost = {loss}")

#     final_cost = cost_function(amps.detach().numpy())
#     return amps.detach().numpy(), final_cost

# def cma_es_optimizer(cost_function, init_amps, sigma=0.5, maxiter=200):
#     """
#     Runs the CMA-ES optimizer on the Fourier amplitudes.
#     """
#     es = cma.CMAEvolutionStrategy(init_amps, sigma, {'maxiter': maxiter})
    
#     while not es.stop():
#         solutions = es.ask()
#         costs = [cost_function(s) for s in solutions]
#         es.tell(solutions, costs)
#         es.disp()
    
#     result_amps = es.result.xbest
#     final_cost = cost_function(result_amps)
#     return result_amps, final_cost