"""Tsai-Wu failure theory for a single ply."""

import numpy as np


def ply_failure_TsaiWu(ply, Sigma12):
    """Compute the Tsai-Wu factor of safety for a ply under given stresses.

    The Tsai-Wu criterion is an interactive quadratic failure criterion
    for orthotropic lamina, using tensile/compressive/shear strengths in
    the material principal directions.

    Parameters
    ----------
    ply : dict
        Ply dictionary created by create_ply(). Must contain the
        strength fields F1t, F1c, F2t, F2c, F6.
    Sigma12 : array-like
        Stresses in the material (1-2) coordinate system,
        [sigma_1, sigma_2, tau_12], in the same units as the strengths.

    Returns
    -------
    Sf : float
        Factor of safety for the actual state of stress (the smallest
        positive scaling that brings the stress state to the failure
        envelope).
    """
    # Stress components in the material coordinate system
    sigma1 = Sigma12[0]
    sigma2 = Sigma12[1]
    tau12  = Sigma12[2]

    # Tsai-Wu coefficients from the strength properties
    f1  = 1/ply["F1t"] - 1/ply["F1c"]
    f11 = 1/(ply["F1t"] * ply["F1c"])
    f2  = 1/ply["F2t"] - 1/ply["F2c"]
    f22 = 1/(ply["F2t"] * ply["F2c"])
    f66 = 1/(ply["F6"]**2)

    # Quadratic and linear parts of the Tsai-Wu criterion
    a = (f11*sigma1**2 + f22*sigma2**2 + f66*tau12**2
         - np.sqrt(f11*f22)*sigma1*sigma2)
    b = f1*sigma1 + f2*sigma2

    # Factor of safety for the actual stress state (positive root of
    # the Tsai-Wu quadratic).  The negative root, traditionally called
    # Sfr, is omitted; reverse-loading analysis is left to the textbook.
    Sf = (-b + np.sqrt(b**2 + 4*a)) / (2*a)

    return Sf
