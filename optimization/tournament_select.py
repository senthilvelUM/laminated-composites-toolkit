"""Tournament-selection operator for the GA."""

import numpy as np


__all__ = ["tournament_select"]


def tournament_select(pop, fits, k, rng):
    """Pick ``k`` individuals at random and return a copy of the fittest.

    Tournament selection is the simplest selection scheme that has a
    tunable selection pressure: ``k = 1`` is purely random, ``k = pop_size``
    is fully greedy, and small ``k`` (2-4) is the standard sweet spot.
    No fitness scaling, no roulette wheel, no rank computation.

    Parameters
    ----------
    pop : np.ndarray, shape (pop_size, N_plies)
        Current population of integer chromosomes.
    fits : np.ndarray, shape (pop_size,)
        Fitness value (Sf_min) for each individual in ``pop``.
    k : int
        Tournament size.  Bigger ``k`` = stronger selection pressure
        = faster convergence but higher risk of premature stagnation.
    rng : np.random.Generator
        Random source.

    Returns
    -------
    np.ndarray, shape (N_plies,), dtype int
        A *copy* of the winning individual (so the caller can mutate
        it without disturbing ``pop``).
    """
    idx       = rng.integers(0, len(pop), size=k)
    winner_idx = idx[np.argmax(fits[idx])]
    return pop[winner_idx].copy()
