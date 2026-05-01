"""Evaluate strains, stresses, and safety factor at a thickness coordinate."""

from laminate.which_ply import which_ply
from ply.get_failure_function import get_failure_function


def evaluate_strains_stresses_Sf(laminate, Epsilon0, Kappa, z, criterion="TsaiWu"):
    """Evaluate strains, stresses, and the safety factor at a z-coordinate.

    Applies the Kirchhoff assumption to get the strains in the global
    (x-y) frame from the midsurface strains and curvatures, then uses
    the transformation and stiffness matrices of the ply that contains
    this z-coordinate to compute the strains and stresses in both the
    x-y and 1-2 frames, and finally the safety factors using the
    chosen ply-level failure criterion.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    Epsilon0 : np.ndarray
        Midsurface strains [eps0_x, eps0_y, gamma0_xy] (shape (3,)).
    Kappa : np.ndarray
        Midsurface curvatures [kappa_x, kappa_y, kappa_xy] (shape (3,)).
    z : float
        Thickness coordinate in meters.
    criterion : str, optional
        Failure-criterion name passed to ``get_failure_function``;
        ``"TsaiWu"`` (default) or ``"MaxStress"``.

    Returns
    -------
    EpsilonXY : np.ndarray
        Strains in the global (x-y) coordinate system.
    Epsilon12 : np.ndarray
        Strains in the material (1-2) coordinate system.
    SigmaXY : np.ndarray
        Stresses in the global (x-y) coordinate system.
    Sigma12 : np.ndarray
        Stresses in the material (1-2) coordinate system.
    Sf : float
        Factor of safety for the actual state of stress (under
        ``criterion``).
    """
    # Identify the ply that contains z
    k = which_ply(laminate, z)
    ply = laminate["plies"][k]

    # Kirchhoff assumption: linear strain distribution through the thickness
    EpsilonXY = Epsilon0 + z * Kappa

    # Strains in the 1-2 coordinate system
    Epsilon12 = ply["Te"] @ EpsilonXY

    # Stresses in the x-y coordinate system
    SigmaXY = ply["QBar"] @ EpsilonXY

    # Stresses in the 1-2 coordinate system
    Sigma12 = ply["Ts"] @ SigmaXY

    # Safety factor using the ply's strength properties and the
    # user-selected failure criterion
    ply_failure = get_failure_function(criterion)
    Sf = ply_failure(ply, Sigma12)

    return EpsilonXY, Epsilon12, SigmaXY, Sigma12, Sf
