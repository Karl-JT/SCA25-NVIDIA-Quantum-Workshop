"""QPE utility collection."""

from typing import (
    Optional,
    Union,
    Callable,
    Counter,
)
import numpy as np


def counts_to_lists(
    counts: Counter,
) -> tuple[list[list[int]], list[int]]:
    """Convert the shot counts to the lists of keys and values."""
    keys = []
    for k in counts.keys():
        v = tuple(int(i) for i in k)
        keys.append(v)
    vals = []
    for v in counts.values():
        vals.append(int(v))
    return (keys, vals)


# def get_mu_and_sigma(
#     prior: np.ndarray,
#     phi: np.ndarray | None = None,
# ) -> tuple[float, float]:
#     """Calculate the mean mu and standard deviation sigma.
#
#     Notes:
#         This is the ad-hoc implementation not concerning periodicity.
#         If the distribution is not localized, the results may not be accurate.
#     """
#     if phi is None:
#         phi = np.linspace(0, 2, len(prior)+1)[:-1]
#     dphi = 2 / len(phi)
#     mu = np.sum(np.array(prior) * phi) * dphi
#     sigma = np.sqrt(np.sum(prior * (phi - mu) ** 2) * dphi)
#     l = len(phi) // 2
#     phi1 = np.copy(phi)
#     phi1[:l] += 2.0
#     mu1 = np.sum(prior * phi1) * dphi
#     sigma1 = np.sqrt(np.sum(prior * (phi1 - mu) ** 2) * dphi)
#     if sigma1 < sigma:
#         mu = mu1
#         sigma = sigma1
#     return mu, sigma


def get_mu_and_sigma(
    prior: np.ndarray,
    phi: np.ndarray | None = None,
) -> tuple[float, float]:
    """Calculate the circular mean mu and square of Holevo variance sigma."""
    if phi is None:
        phi = np.linspace(0, 2, len(prior) + 1)[:-1]
    dphi = 2 / len(phi)
    # Circular mean.
    mu = np.angle(np.sum(np.exp(1.0j * np.pi * phi) * prior) * dphi * np.pi)
    mu /= np.pi
    # Holevo variance sigma^2.
    sigma2 = np.abs(np.sum(np.exp(1.0j * np.pi * phi) * prior) * dphi) ** -2 - 1
    sigma = np.sqrt(sigma2) / np.pi
    return mu, sigma


def binary_fraction(readout: list[int]) -> float:
    r"""Converts (BigEndian) bits into a fraction number [0, 2).

    Args:
       Readout: Bit string.

    Returns:
       Phase factor :math:`\phi` as a binary fraction.

    Examples:
        >>> binary_fraction([1, 0, 0])
        1.0
        >>> binary_fraction([0, 0, 1])
        0.25
    """
    phase = 0.0
    for i, r in enumerate(readout):
        phase += r * (0.5**i)
    return phase


def noise_aware_likelihood(
    k: int,
    beta: float,
    m: int,
    phi: Union[float, list],
    error_rate: Optional[Callable[[int], float]] = None,
) -> Union[float, list]:
    """Likelihood function for the noiseless simulation.

    Args:
        k:
            Multiple of the controlled unitary.
        beta:
            Rotation angle (in half turn) applied before the X measurement.
        m:
            Measurement outcome in {0, 1}.
        phi:
            phase.
        error_rate:
            Function to return error rate [0, 1].

    Returns:
        Likelihood function as a function of :code:`phi`.
    """
    q = 0.0
    if error_rate is not None:
        q = error_rate(k)
    phi = np.array(phi)
    val = 1 + (1 - q) * (-1) ** m * np.cos(np.pi * (k * phi + beta))
    val *= 0.5
    val = val.tolist()
    return val
