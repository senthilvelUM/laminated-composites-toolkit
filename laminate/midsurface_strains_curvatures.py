"""Compute midsurface strains and curvatures from applied loads."""

import numpy as np


def midsurface_strains_curvatures(laminate, Nx, Ny, Nxy, Mx, My, Mxy):
    """Solve the laminate load-deformation relation.

    Uses the laminate compliance matrix [abd] = [ABD]^-1 to compute the
    midsurface strains and curvatures produced by the applied force and
    moment resultants:

        [Epsilon0; Kappa] = [abd] * [Nx; Ny; Nxy; Mx; My; Mxy]

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate(). Must contain
        the laminate compliance matrix "abd".
    Nx, Ny, Nxy : float
        In-plane force resultants per unit width [N/m].
    Mx, My, Mxy : float
        Moment resultants per unit width [N-m/m].

    Returns
    -------
    Epsilon0 : np.ndarray
        Midsurface strains [eps0_x, eps0_y, gamma0_xy] (shape (3,)).
    Kappa : np.ndarray
        Midsurface curvatures [kappa_x, kappa_y, kappa_xy] (shape (3,)).
    """
    # Assemble the 6-element load vector
    NM = np.array([Nx, Ny, Nxy, Mx, My, Mxy])

    # Apply the laminate compliance matrix
    EpsilonKappa = laminate["abd"] @ NM

    # Split into midsurface strains and curvatures
    Epsilon0 = EpsilonKappa[0:3]
    Kappa    = EpsilonKappa[3:6]

    return Epsilon0, Kappa
