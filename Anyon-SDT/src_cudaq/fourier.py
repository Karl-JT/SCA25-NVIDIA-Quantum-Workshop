"""
functions: 
    build_fourier_params
    fourier_amplitude_init
"""

import numpy as np


def build_fourier_params(amps, depth, q):
    """
    Reconstructs gamma and beta based on the FOURIER heuristics (Zhou et al (2019))
    """
    gammas = np.zeros(depth)
    betas = np.zeros(depth)

    uk = amps[:q]
    vk = amps[q:2*q]

    positions = (np.arange(1, depth + 1) - 0.5) / depth
    for k in range(1, q + 1):
        factor = np.pi * (k - 0.5)
        gammas += uk[k - 1] * np.sin(factor * positions)
        betas += vk[k - 1] * np.cos(factor * positions)

    return np.vstack([gammas, betas])


def fourier_amplitude_init(q):
    """
    Initializes the Fourier amplitudes within desired ranges.
    """
    amps = np.hstack([
        np.random.uniform(-np.pi/2, np.pi/2, q),   # gamma amplitudes (u_k)
        np.random.uniform(-np.pi/2, np.pi/2, q)    # beta amplitudes (v_k)
    ])
    return amps