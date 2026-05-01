"""Main GA loop for the integer-coded stacking-sequence optimiser."""

import numpy as np

from optimization.mutate import mutate
from optimization.one_point_crossover import one_point_crossover
from optimization.random_individual import random_individual
from optimization.tournament_select import tournament_select


__all__ = ["evolve"]


def evolve(
    fitness_fn,
    *,
    N_plies,
    n_alleles,
    pop_size,
    n_generations,
    crossover_rate,
    mutation_rate,
    tournament_k,
    n_elite,
    rng,
):
    """Run the GA and return the best individual found plus convergence history.

    Per-generation flow:
      1. Score every individual with ``fitness_fn``.
      2. Record best & mean fitness for the convergence plot.
      3. Carry the top ``n_elite`` individuals over verbatim.
      4. Fill the rest of the new population by tournament selection,
         one-point crossover, and per-gene mutation.

    Termination is a fixed generation count; replace this loop with a
    no-improvement-for-N-generations rule if you need adaptive
    termination.

    Parameters
    ----------
    fitness_fn : callable(individual) -> float
        Scalar objective.  Larger is better (the runner usually
        passes a closure that decodes the integer chromosome to ply
        angles and calls ``evaluate_stacking``).
    N_plies : int
        Chromosome length.
    n_alleles : int
        Allele alphabet size (e.g. ``len(angle_set)``).
    pop_size : int
        Number of individuals per generation.
    n_generations : int
        Total number of generations to run.
    crossover_rate : float in [0, 1]
        Probability of crossover (else parents clone).
    mutation_rate : float in [0, 1]
        Per-gene mutation probability.
    tournament_k : int
        Tournament size (selection pressure).
    n_elite : int
        Number of best individuals copied verbatim each generation.
    rng : np.random.Generator
        Random source (seed ``np.random.default_rng(seed)`` for
        reproducibility).

    Returns
    -------
    best_individual : np.ndarray, shape (N_plies,), dtype int
        The fittest chromosome found.
    best_fitness : float
        Its fitness value.
    history : dict[str, list[float]]
        ``"best"`` and ``"mean"`` fitness per generation (length
        ``n_generations + 1``; the extra entry is the post-final
        generation).
    """
    # Initial random population, scored once
    pop  = np.array([random_individual(N_plies, n_alleles, rng)
                     for _ in range(pop_size)])
    fits = np.array([fitness_fn(ind) for ind in pop])

    history = {"best": [], "mean": []}

    for _ in range(n_generations):
        history["best"].append(fits.max())
        history["mean"].append(fits.mean())

        # Elitism: top n_elite copied verbatim
        elite_idx = np.argsort(fits)[-n_elite:][::-1]
        new_pop   = [pop[i].copy() for i in elite_idx]

        # Fill the rest by tournament + crossover + mutation
        while len(new_pop) < pop_size:
            p1 = tournament_select(pop, fits, tournament_k, rng)
            p2 = tournament_select(pop, fits, tournament_k, rng)
            c1, c2 = one_point_crossover(p1, p2, crossover_rate, rng)
            c1 = mutate(c1, mutation_rate, n_alleles, rng)
            c2 = mutate(c2, mutation_rate, n_alleles, rng)
            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        pop  = np.array(new_pop)
        fits = np.array([fitness_fn(ind) for ind in pop])

    # Append post-final-generation diagnostics
    history["best"].append(fits.max())
    history["mean"].append(fits.mean())

    best_i = int(np.argmax(fits))
    return pop[best_i], float(fits[best_i]), history
