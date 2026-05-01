"""Generate a uniform-random integer chromosome for the GA."""

__all__ = ["random_individual"]


def random_individual(N_plies, n_alleles, rng):
    """Uniform-random integer chromosome of length ``N_plies``.

    Each gene is an integer in ``0..n_alleles-1``, decoded by the
    runner via ``angle_set[gene]`` to recover the ply angle.  Integer
    encoding is the natural fit for a discrete angle set: every gene
    value is on the design grid by construction, so no rounding
    heuristic is needed.

    Parameters
    ----------
    N_plies : int
        Number of plies (length of the chromosome).
    n_alleles : int
        Size of the allele alphabet (e.g. ``len(angle_set)``).
    rng : np.random.Generator
        Random source.  Pass a seeded ``np.random.default_rng(seed)``
        for reproducible runs.

    Returns
    -------
    np.ndarray, shape (N_plies,), dtype int
        The new individual.
    """
    return rng.integers(0, n_alleles, size=N_plies)
