"""Bayesian QPE (including information theory QPE) utilities.

Grid-based bayesian QPE, not based on the more efficient Fourier respresentation
for the sake of simplicity.
"""

from typing import Callable
from pytket.backends.backendresult import BackendResult
import numpy as np
from ._utils import noise_aware_likelihood

PRECISION = 15
ATOL = 10**-PRECISION


def bayesian_update(
    phi: np.ndarray[float],
    prior: np.ndarray[float],
    k_list: list[int],
    beta_list: list[float],
    results: list[BackendResult],
    error_rate: Callable[[int], float] | None = None,
) -> np.ndarray[float]:
    """Bayesian update (high-level interface taking the BackendResults objects).

    Args:
        phi: Equi-distant grid points of the phase [0, 2), i.e., pytket conventions.
        prior: Prior distribution (not necesaliry normalized).
        k_list: list of k, the number of repeat of ctrl-U.
        beta_list: list of beta, the Rz rotation angle before the X measurement.
        results: list of Backend results
        error_rate: Error rate to be passed to the noise-aware likelihood.

    Returns:
        Posterior distribution (normalized).
    """
    (ks, betas, ms) = get_ms(k_list, beta_list, results)
    posterior = update(phi, prior, ks, betas, ms, error_rate=error_rate)
    return posterior


def get_ms(
    k_list: list[int],
    beta_list: list[float],
    results: list[BackendResult],
) -> tuple[list[int], list[float], list[int]]:
    """Create a list of (k, beta, m).

    Args:
        k_list: list of k, the number of repeat of ctrl-U.
        beta_list: list of beta, the Rz rotation angle before the X measurement.
        results: list of Backend results

    Returns:
        List of number-of-shots-aware list of (k, beta, m).
    """
    ks: list[int] = []
    betas: list[int] = []
    ms: list[int] = []
    for k, beta, result in zip(k_list, beta_list, results):
        counts = result.get_counts()
        for readout, count in counts.items():
            for _ in range(count):
                if readout == (0,):
                    m = 0
                else:
                    m = 1
                ks.append(k)
                betas.append(beta)
                ms.append(m)
    return (ks, betas, ms)


def update(
    phi: np.ndarray[float],
    prior: np.ndarray[float],
    ks: list[int],
    betas: list[float],
    ms: list[int | None],
    error_rate: Callable[[int], float] | None = None,
) -> np.ndarray[float]:
    """Update the probability distribution.

    Args:
        phi: Equi-distant grid points of the phase [0, 2), i.e., pytket conventions.
        prior: Prior distribution (not necesaliry normalized).
        k_list: list of k, the number of repeat of ctrl-U.
        beta_list: list of beta, the Rz rotation angle before the X measurement.
        ms: list of measurement outcomes {0, 1}.
        error_rate: Error rate to be passed to the noise-aware likelihood.

    Returns:
        Posterior distribution (normalized).
    """
    log_prior = np.log(prior)
    for k, beta, m in zip(ks, betas, ms):
        if m is None:
            continue
        likelihood = noise_aware_likelihood(
            k=k,
            beta=beta,
            m=m,
            phi=phi,
            error_rate=error_rate,
        )
        log_prior += np.log(
            np.maximum(likelihood, ATOL),
        )
    log_prior -= np.max(log_prior)
    posterior = np.exp(log_prior)
    # Normalize the posterior distribution.
    dphi = phi[1] - phi[0]
    posterior /= np.sum(posterior) * dphi
    posterior = np.round(posterior, PRECISION)
    return posterior


def generate_ks(
    k_max: int,
    n_samples: int,
    error_rate: Callable[[int], float] | None = None,
    discard_rate: Callable[[int], float] | None = None,
) -> list[int]:
    ks = list(range(1, k_max + 1))
    if error_rate is None:
        dist = np.ones(len(ks), dtype=float)
    else:
        dist = np.array([1 / np.log(2 - error_rate(k)) for k in ks])
    if discard_rate is None:
        dist *= np.ones(len(ks), dtype=float)
    else:
        dist *= np.array([1 / (1 - discard_rate(k)) for k in ks])
    dist /= np.sum(dist)
    k_list = np.random.choice(ks, size=n_samples, replace=True, p=dist)
    k_list = [int(k) for k in k_list]
    return k_list
