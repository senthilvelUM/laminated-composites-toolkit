"""Maximum-stress failure theory for a single ply."""

import numpy as np


__all__ = ["ply_failure_MaxStress"]


def ply_failure_MaxStress(ply, Sigma12):
    """Compute the maximum-stress factor of safety for a ply.

    The maximum-stress criterion declares failure when ANY single
    stress component reaches its allowable, treating each mode
    independently (no interaction between sigma_1, sigma_2, tau_12):

        -F1c <= sigma_1 <= F1t
        -F2c <= sigma_2 <= F2t
        -F6  <= tau_12  <= F6

    Under a uniform scaling Sf the stresses become
    ``[Sf*sigma_1, Sf*sigma_2, Sf*tau_12]``.  For each component, the
    smallest *positive* Sf that brings the component to one of its
    bounds is its forward failure scaling.  ``Sf`` is the minimum of
    those across all components -- the smallest positive scaling that
    triggers any single mode when the stress is scaled up.

    Companion / contrast with ``ply_failure_TsaiWu``: the API and
    return shape are identical -- both functions can be substituted
    at any call site -- but Tsai-Wu uses a single quadratic envelope
    that couples all stress components, while max-stress is fully
    decoupled.  Comparing the two scalars at the same stress state
    isolates the contribution of stress interactions: Tsai-Wu's
    Sf is usually (but not always) smaller than this Sf because
    interactions worsen the prediction.

    No quadratic to solve -- closed-form per-component ratios.

    Parameters
    ----------
    ply : dict
        Ply dictionary created by ``create_ply()``.  Must contain
        the strength fields ``F1t``, ``F1c``, ``F2t``, ``F2c``,
        ``F6`` (same fields used by Tsai-Wu).
    Sigma12 : array-like, shape (3,)
        Stresses in the material (1-2) coordinate system,
        ``[sigma_1, sigma_2, tau_12]``, in the same units as the
        strengths.

    Returns
    -------
    Sf : float
        Forward-scaling factor of safety (smallest positive Sf that
        causes any component to reach its bound).
    """
    sigma1 = float(Sigma12[0])
    sigma2 = float(Sigma12[1])
    tau12  = float(Sigma12[2])

    # Per-component positive failure-Sf (the forward direction).
    # A zero component contributes +inf -- it never triggers failure
    # under any finite scaling.

    # sigma_1 component: bounded by [-F1c, +F1t]
    if sigma1 > 0:
        Sf_pos_1 =  ply["F1t"] / sigma1
    elif sigma1 < 0:
        Sf_pos_1 = -ply["F1c"] / sigma1
    else:
        Sf_pos_1 = np.inf

    # sigma_2 component: bounded by [-F2c, +F2t]
    if sigma2 > 0:
        Sf_pos_2 =  ply["F2t"] / sigma2
    elif sigma2 < 0:
        Sf_pos_2 = -ply["F2c"] / sigma2
    else:
        Sf_pos_2 = np.inf

    # tau_12 component: symmetric envelope [-F6, +F6]
    if tau12 != 0:
        Sf_pos_6 = ply["F6"] / abs(tau12)
    else:
        Sf_pos_6 = np.inf

    # Smallest positive scaling fails first in the forward direction
    Sf = min(Sf_pos_1, Sf_pos_2, Sf_pos_6)
    return Sf
