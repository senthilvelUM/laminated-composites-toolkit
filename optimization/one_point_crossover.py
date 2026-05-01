"""One-point crossover operator for the GA."""

import numpy as np


__all__ = ["one_point_crossover"]


def one_point_crossover(p1, p2, crossover_rate, rng):
    """One-point crossover applied with probability ``crossover_rate``.

    Picks a random cut point ``c`` in ``1..N-1`` and produces two
    children: child 1 = head of ``p1`` + tail of ``p2``; child 2 =
    head of ``p2`` + tail of ``p1``.  With probability
    ``1 - crossover_rate`` the parents are returned unchanged
    (cloning).

    The simplest and most popular crossover for fixed-length
    integer chromosomes.  Uniform crossover or two-point variants are
    drop-in replacements with the same signature.

    Parameters
    ----------
    p1, p2 : np.ndarray, shape (N_plies,), dtype int
        Parent chromosomes.
    crossover_rate : float in [0, 1]
        Probability of actually performing crossover; otherwise the
        parents are cloned.
    rng : np.random.Generator
        Random source.

    Returns
    -------
    c1, c2 : np.ndarray, shape (N_plies,), dtype int
        The two children (always returned as fresh arrays).
    """
    N = len(p1)
    if rng.random() >= crossover_rate or N < 2:
        return p1.copy(), p2.copy()

    cut = rng.integers(1, N)              # 1..N-1
    c1 = np.concatenate([p1[:cut], p2[cut:]])
    c2 = np.concatenate([p2[:cut], p1[cut:]])
    return c1, c2
