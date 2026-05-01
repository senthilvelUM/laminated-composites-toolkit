"""Fast min-Sf evaluator for one stacking sequence.

The textbook ``laminate.create_laminate`` builds *every* derived field
of a laminate (engineering moduli, mass moments, shear stiffness, ...)
which is overkill when an optimiser only needs the minimum first-ply
Tsai-Wu safety factor.  The function below is the optimisation-grade
distillation of that pipeline:

1. Look up each ply from a pre-built cache (the ply is fully defined
   by its material + angle + thickness; for fixed material and
   uniform thickness the cache is just one ply per candidate angle).
2. Sum ``QBar`` contributions across the layers to assemble ``A, B, D``
   directly (the textbook formulas).
3. Solve the 6x6 ``[ABD] [eps0; kappa] = [N; M]`` system once.
4. Sample Tsai-Wu Sf at top/middle/bottom of each ply (3 points;
   matches the high-resolution 500-point sweep of
   ``find_min_safety_factor`` to floating-point precision for the
   linear-strain through-the-thickness loadings of interest).

About 25 microseconds per call -- fast enough that brute-force
enumeration of 12^4 stackings finishes in ~3 seconds.
"""

import numpy as np

from ply.get_failure_function import get_failure_function


__all__ = ["evaluate_stacking"]


def evaluate_stacking(angles_deg, ply_cache, h_ply, NM, criterion="TsaiWu"):
    """Minimum first-ply safety factor for one stacking sequence.

    Parameters
    ----------
    angles_deg : iterable of int
        The N ply angles (degrees), in stacking order.  Every value
        must be a key in ``ply_cache``.
    ply_cache : dict[int, dict]
        Maps each candidate ply angle to a ply dict (as produced by
        ``ply.create_ply``).  Building this cache once and reusing it
        across many candidate stackings is the main speed-up over
        calling ``create_laminate`` per candidate.
    h_ply : float
        Uniform ply thickness (meters).  All plies share this value.
    NM : np.ndarray, shape (6,)
        Applied resultants ``[Nx, Ny, Nxy, Mx, My, Mxy]`` (N/m and N).
    criterion : str, optional
        Failure-criterion name passed to ``get_failure_function``;
        ``"TsaiWu"`` (default) or ``"MaxStress"``.

    Returns
    -------
    float
        The minimum Sf across the laminate thickness under the
        chosen criterion.
    """
    ply_failure = get_failure_function(criterion)
    angles = list(angles_deg)
    N      = len(angles)
    plies  = [ply_cache[a] for a in angles]

    # Ply interface z-coordinates (N+1 values, midplane at z = 0)
    z = -0.5 * h_ply * N + np.arange(N + 1) * h_ply

    # A, B, D as ply-thickness-weighted sums of QBar (textbook)
    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))
    for k in range(1, N + 1):
        QBar = plies[k-1]["QBar"]
        A += (z[k]    - z[k-1]   ) * QBar
        B += (z[k]**2 - z[k-1]**2) * QBar / 2
        D += (z[k]**3 - z[k-1]**3) * QBar / 3

    # Load-deformation: [ABD] [eps0; kappa] = [N; M]
    eps0kap     = np.linalg.solve(np.block([[A, B], [B, D]]), NM)
    eps0, kappa = eps0kap[:3], eps0kap[3:]

    # Min Sf: sample top / middle / bottom of every ply.
    # Strain is linear in z within a ply, so the critical Sf lives
    # very close to one of these three points for typical loadings.
    Sf_min = np.inf
    for k in range(1, N + 1):
        ply = plies[k-1]
        for t in (0.0, 0.5, 1.0):
            z_eval  = z[k-1] + t * h_ply
            EpsXY   = eps0 + z_eval * kappa
            Sigma12 = ply["Ts"] @ ply["QBar"] @ EpsXY
            Sf     = ply_failure(ply, Sigma12)
            if Sf < Sf_min:
                Sf_min = Sf
    return Sf_min
