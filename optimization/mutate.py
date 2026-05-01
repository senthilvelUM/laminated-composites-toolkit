"""Per-gene mutation operator for the GA."""

__all__ = ["mutate"]


def mutate(individual, mutation_rate, n_alleles, rng):
    """Replace each gene with probability ``mutation_rate`` by a random allele.

    The textbook integer-coded GA mutation: every gene is independently
    rolled against ``mutation_rate``; rolled genes are overwritten
    by a uniform random integer from ``0..n_alleles-1``.

    A common rule of thumb is ``mutation_rate = 1 / N_plies`` so each
    individual sees ~1 mutation on average per generation.  Higher
    rates accelerate exploration but disrupt good solutions; lower
    rates risk premature convergence.

    Parameters
    ----------
    individual : np.ndarray, shape (N_plies,), dtype int
        Chromosome to mutate.  Returned unchanged if no genes are
        rolled, otherwise a fresh copy with the rolled genes
        overwritten.
    mutation_rate : float in [0, 1]
        Per-gene mutation probability.
    n_alleles : int
        Size of the allele alphabet for the replacement draw.
    rng : np.random.Generator
        Random source.

    Returns
    -------
    np.ndarray, shape (N_plies,), dtype int
        The (possibly mutated) individual.
    """
    mask = rng.random(len(individual)) < mutation_rate
    if not mask.any():
        return individual

    mutated       = individual.copy()
    mutated[mask] = rng.integers(0, n_alleles, size=mask.sum())
    return mutated
