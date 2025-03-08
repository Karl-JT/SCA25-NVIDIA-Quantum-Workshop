"""
functions:
    build_fourier_params
    fourier_amplitude_init
"""

import numpy as np


def build_fourier_params(amps, depth, q):
    """
    Reconstructs gamma, beta, a, b parameters based on the Fourier heuristics (Zhou et al. 2019).
    """
    gammas = np.zeros(depth)
    betas = np.zeros(depth)
    a_params = np.zeros(depth)
    b_params = np.zeros(depth)

    uk = amps[:q]
    vk = amps[q:2 * q]
    ak = amps[2 * q:3 * q]
    bk = amps[3 * q:4 * q]

    positions = (np.arange(1, depth + 1) - 0.5) / depth
    for k in range(1, q + 1):
        factor = np.pi * (k - 0.5)
        gammas += uk[k - 1] * np.sin(factor * positions)
        betas += vk[k - 1] * np.cos(factor * positions)
        a_params += ak[k - 1] * np.cos(factor * positions)
        b_params += bk[k - 1] * np.sin(factor * positions)

    return np.vstack([gammas, betas, a_params, b_params])


def fourier_amplitude_init(q):
    """
    Initializes the Fourier amplitudes within desired ranges.
    """
    amps = np.hstack([
        np.random.uniform(-np.pi, np.pi, q),   # gamma amplitudes (u_k)
        np.random.uniform(-np.pi, np.pi, q),   # beta amplitudes (v_k)
        np.random.uniform(0, 1, q),           # a amplitudes (a_k)
        np.random.uniform(0, 1, q)            # b amplitudes (b_k)
    ])
    return amps
