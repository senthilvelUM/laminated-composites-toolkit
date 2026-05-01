"""Find the minimum first-ply safety factor through the thickness of a laminate."""

import numpy as np

from laminate.evaluate_strains_stresses_Sf import evaluate_strains_stresses_Sf


# Sampling density and interface offset (same as used in the plots)
POINTS_PER_LAYER = 500
_EPS = 1e-12


def find_min_safety_factor(laminate, Epsilon0, Kappa, criterion="TsaiWu"):
    """Find the minimum first-ply safety factor through the thickness.

    Sweeps the thickness coordinate z in fine increments across every
    ply, evaluates Sf at each sample point under the chosen failure
    criterion, and returns the minimum value along with its location.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    Epsilon0 : np.ndarray
        Midsurface strains [eps0_x, eps0_y, gamma0_xy] (shape (3,)).
    Kappa : np.ndarray
        Midsurface curvatures [kappa_x, kappa_y, kappa_xy] (shape (3,)).
    criterion : str, optional
        Failure-criterion name passed to ``get_failure_function``;
        ``"TsaiWu"`` (default), ``"MaxStress"``, or ``"Hashin"``.

    Returns
    -------
    Sf_min : float
        Minimum Sf across the thickness.
    z_min : float
        z-coordinate where the minimum occurs (meters).
    k_min : int
        1-based ply number where the minimum occurs.
    """
    Sf_min = np.inf
    z_min = None
    k_min = None

    for k in range(1, laminate["N"] + 1):
        zloc = np.linspace(
            laminate["z"][k-1] + _EPS, laminate["z"][k] - _EPS, POINTS_PER_LAYER
        )
        for n in range(POINTS_PER_LAYER):
            _, _, _, _, Sf = evaluate_strains_stresses_Sf(
                laminate, Epsilon0, Kappa, zloc[n], criterion=criterion
            )
            if Sf < Sf_min:
                Sf_min = Sf
                z_min = zloc[n]
                k_min = k

    return Sf_min, z_min, k_min
