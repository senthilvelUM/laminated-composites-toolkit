"""Exhaustive enumeration over a discrete stacking-sequence design space."""

import itertools

import numpy as np

from optimization.evaluate_stacking import evaluate_stacking


__all__ = ["brute_force_search"]


def brute_force_search(angle_set, N_plies, ply_cache, h_ply, NM, criterion="TsaiWu"):
    """Enumerate every stacking sequence and return the best.

    Visits all ``len(angle_set) ** N_plies`` sequences in lexicographic
    order via ``itertools.product``.  Used as the brute-force baseline
    paired with ``evolve`` (the GA): when the design space is small
    enough to enumerate, this guarantees the global optimum.

    Parameters
    ----------
    angle_set : sequence of int
        The discrete angle values (degrees) each ply may take.
    N_plies : int
        Number of plies in the laminate.
    ply_cache : dict[int, dict]
        See ``evaluate_stacking``.  Must contain every value of
        ``angle_set`` as a key.
    h_ply : float
        Uniform ply thickness (meters).
    NM : np.ndarray, shape (6,)
        Applied resultants ``[Nx, Ny, Nxy, Mx, My, Mxy]``.
    criterion : str, optional
        Failure-criterion name passed to ``evaluate_stacking``;
        ``"TsaiWu"`` (default) or ``"MaxStress"``.

    Returns
    -------
    best_angles : list of int
        Stacking sequence with the largest Sf_min.
    best_Sf : float
        The corresponding Sf_min.
    all_Sf : np.ndarray, shape (n_total,)
        Sf_min of every enumerated sequence, ordered the same way
        as ``itertools.product(angle_set, repeat=N_plies)``.  Useful
        for visualising the distribution of safety factors over the
        design space.
    """
    n_total     = len(angle_set) ** N_plies
    all_Sf     = np.empty(n_total, dtype=float)
    best_Sf    = -np.inf
    best_angles = None

    for i, angles in enumerate(itertools.product(angle_set, repeat=N_plies)):
        Sf = evaluate_stacking(angles, ply_cache, h_ply, NM, criterion=criterion)
        all_Sf[i] = Sf
        if Sf > best_Sf:
            best_Sf    = Sf
            best_angles = list(angles)

    return best_angles, best_Sf, all_Sf
