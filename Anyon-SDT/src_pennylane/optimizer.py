"""
functions:
    run_qaoa_custom_opt
    run_qaoa_opt
"""

from pennylane import numpy as np
import pennylane as qml
from src_pennylane.circuits import cost_function_custom
from src_pennylane.circuits import cost_function


def run_qaoa_custom_opt(
    wires,
    H_C,
    depth=10,
    steps=200,
    stepsize=0.2,
    device=None,
    normalized=False,
    verbose=True,
):
    """
    Runs QAOA optimization with a custom mixer using PennyLane's Adam optimizer.
    """
    wires = Q.shape[0]

    # Initialize parameters (heuristic linear schedules)
    gammas = np.linspace(np.pi / 2, 0, depth, endpoint=False)[::-1]
    betas = np.linspace(np.pi / 4, 0, depth)
    a_params = np.linspace(1, 0, depth)
    b_params = np.linspace(0, 0.4, depth)

    # Stack parameters into one array with gradients enabled
    params = np.array(np.vstack([gammas, betas, a_params, b_params]), requires_grad=True)

    # Setup optimizer
    optimizer = qml.AdamOptimizer(stepsize=stepsize)

    # Optimization loop
    for i in range(steps):
        params = optimizer.step(
            lambda p: cost_function_custom(p, depth, H_C, cost_hamiltonian, wires, device, normalized),
            params
        )
        if verbose and i % 10 == 0:
            current_cost = cost_function_custom(params, depth, H_C, cost_hamiltonian, wires, device, normalized)
            print(f"Step {i}: Cost = {current_cost}")

    # Final cost
    final_cost = cost_function_custom(params, depth, H_C, cost_hamiltonian, wires, device, normalized)
    print(f"\n✅ Final cost = {final_cost}")
    print(f"✅ Approximation ratio = {(100 * final_cost / -432247):.2f}% of the optimal value.")

    return final_cost, params 


def run_qaoa_opt(
    wires,
    H_C,
    mixer_hamiltonian,
    depth=10,
    steps=200,
    stepsize=0.2,
    device=None,
    normalized=False,
    verbose=True,
):
    """
    Runs standard QAOA optimization with the default mixer using PennyLane's Adam optimizer.
    """
    # Initialize parameters (heuristic linear schedules)
    gammas = np.linspace(np.pi / 2, 0, depth, endpoint=False)[::-1]
    betas = np.linspace(np.pi / 4, 0, depth)

    # Stack parameters into one array with gradients enabled
    params = np.array(np.vstack([gammas, betas]), requires_grad=True)

    # Setup optimizer
    optimizer = qml.AdamOptimizer(stepsize=stepsize)

    # Optimization loop
    for i in range(steps):
        params = optimizer.step(
            lambda p: cost_function(p, depth, H_C, cost_hamiltonian, mixer_hamiltonian, wires, device, normalized),
            params
        )
        if verbose and i % 10 == 0:
            current_cost = cost_function(p, depth, H_C, cost_hamiltonian, mixer_hamiltonian, wires, device, normalized)
            print(f"Step {i}: Cost = {current_cost}")

    # Final cost
    final_cost = cost_function(params, depth, H_C, cost_hamiltonian, mixer_hamiltonian, wires, device, normalized)
    print(f"\n✅ Final cost = {final_cost}")
    print(f"✅ Approximation ratio = {(100 * final_cost / -432247):.2f}% of the optimal value.")

    return final_cost, params