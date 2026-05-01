"""Hashin (1980) interaction-aware failure theory for a single ply.

Splits first-ply failure into four physically distinct modes
(fibre tension, fibre compression, matrix tension, matrix
compression), each with its own quadratic envelope.  Position on
the interaction spectrum:

    max-stress   (no interaction across components)
    Hashin       (interaction WITHIN a mode, NONE across modes)
    Tsai-Wu      (interaction across all components, single envelope)

So Hashin captures the physics that matrix cracking under
transverse tension is driven *jointly* by sigma_2 and tau_12,
while still keeping fibre and matrix failure modes algebraically
separate -- a middle ground between the all-or-nothing
alternatives.

Mode IV (matrix compression) is implemented in the **simplified**
form -- ``(sigma_2/F2c)^2 + (tau_12/F6)^2 = 1`` -- which avoids
the F23 (transverse-transverse shear strength) data not present
in LaminateX's ``materials/*.yaml`` files.  The full Hashin 1980
matrix-compression form requires F23 and reduces to a quadratic
solve; see the parked theory notes for the full equation if
needed later.
"""

import numpy as np


__all__ = ["ply_failure_Hashin"]


def ply_failure_Hashin(ply, Sigma12):
    """Compute the Hashin (1980) factor of safety for a ply.

    Each of the four physically distinct failure modes is checked
    in its activation regime; the smallest active per-mode safety
    factor is returned as ``Sf``.

    Mode summary:
      * Mode I   (sigma_1 >= 0):  ``(sigma_1/F1t)^2 + (tau_12/F6)^2 = 1``
      * Mode II  (sigma_1 <  0):  ``-sigma_1 = F1c``
      * Mode III (sigma_2 >= 0):  ``(sigma_2/F2t)^2 + (tau_12/F6)^2 = 1``
      * Mode IV  (sigma_2 <  0):  ``(sigma_2/F2c)^2 + (tau_12/F6)^2 = 1``
                                  (simplified, no F23 dependence)

    Parameters
    ----------
    ply : dict
        Ply dictionary created by ``create_ply()``.  Must contain
        the strength fields ``F1t``, ``F1c``, ``F2t``, ``F2c``,
        ``F6``.
    Sigma12 : array-like, shape (3,)
        Stresses in the material (1-2) coordinate system,
        ``[sigma_1, sigma_2, tau_12]``, in the same units as the
        strengths.

    Returns
    -------
    Sf : float
        Smallest active per-mode forward-scaling factor of safety.
    """
    sigma1 = float(Sigma12[0])
    sigma2 = float(Sigma12[1])
    tau12  = float(Sigma12[2])
    F1t = ply["F1t"]; F1c = ply["F1c"]
    F2t = ply["F2t"]; F2c = ply["F2c"]
    F6  = ply["F6"]

    # Per-mode Sf.  Inactive modes carry +inf and never win the min().
    Sf_I   = np.inf      # Mode I:   fibre tension
    Sf_II  = np.inf      # Mode II:  fibre compression
    Sf_III = np.inf      # Mode III: matrix tension
    Sf_IV  = np.inf      # Mode IV:  matrix compression (simplified)

    # Mode I (sigma1 >= 0): (sigma1/F1t)^2 + (tau12/F6)^2 = 1
    if sigma1 >= 0:
        s = (sigma1 / F1t) ** 2 + (tau12 / F6) ** 2
        if s > 0:
            Sf_I = 1.0 / np.sqrt(s)

    # Mode II (sigma1 < 0): -sigma1 = F1c
    if sigma1 < 0:
        Sf_II = F1c / abs(sigma1)

    # Mode III (sigma2 >= 0): (sigma2/F2t)^2 + (tau12/F6)^2 = 1
    if sigma2 >= 0:
        s = (sigma2 / F2t) ** 2 + (tau12 / F6) ** 2
        if s > 0:
            Sf_III = 1.0 / np.sqrt(s)

    # Mode IV (sigma2 < 0), simplified Hashin (drops F23 term):
    #   (sigma2/F2c)^2 + (tau12/F6)^2 = 1
    if sigma2 < 0:
        s = (sigma2 / F2c) ** 2 + (tau12 / F6) ** 2
        Sf_IV = 1.0 / np.sqrt(s)

    return min(Sf_I, Sf_II, Sf_III, Sf_IV)
