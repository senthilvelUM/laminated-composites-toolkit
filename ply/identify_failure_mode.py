"""Identify the dominant first-ply failure mode at a given stress state.

This is a pedagogical companion to ``ply_failure_TsaiWu``.  Tsai-Wu
returns a single safety factor that accounts for stress interactions
through cross-terms in its quadratic envelope; it does *not* tell you
which mode (fibre / matrix / shear) is driving the failure.  The
function below answers the missing question by computing one
maximum-stress safety factor per independent mode -- the standard
post-mortem diagnostic in composite-failure textbooks.

Per-mode safety factors are decoupled by construction (each one looks
at one strength only), so the smallest of them, ``SF_mode``, is
generally NOT equal to the Tsai-Wu ``Sf``:

  * If interactions are *unfavourable* (e.g. sigma1 > 0 and sigma2 > 0
    in a typical UD ply), Sf < SF_mode.
  * If interactions are *favourable*, Sf > SF_mode.

Comparing the two is one of the most direct demonstrations in
composite-failure pedagogy of why interaction-aware criteria matter.
"""

import numpy as np


__all__ = ["identify_failure_mode"]


# Mode names (kept as module-level constants so callers and tests
# don't have to remember the spelling).
_MODES = (
    "fiber_tension",
    "fiber_compression",
    "matrix_tension",
    "matrix_compression",
    "shear",
)


def identify_failure_mode(ply, Sigma12):
    """Identify the dominant Tsai-Wu failure mode at one stress state.

    Computes the maximum-stress safety factor for each of the five
    independent failure modes (fibre tension, fibre compression,
    matrix tension, matrix compression, in-plane shear) and returns
    the mode with the smallest one.  Inactive modes (e.g. fibre
    compression when sigma1 > 0) are reported as ``inf`` and cannot
    be selected as dominant.

    Parameters
    ----------
    ply : dict
        Ply dictionary created by ``create_ply``.  Must contain the
        strength fields ``F1t``, ``F1c``, ``F2t``, ``F2c``, ``F6``.
    Sigma12 : array-like
        Stresses in the material (1-2) coordinate system,
        ``[sigma_1, sigma_2, tau_12]``, in the same units as the
        strengths.

    Returns
    -------
    mode : str
        Name of the dominant mode -- one of ``"fiber_tension"``,
        ``"fiber_compression"``, ``"matrix_tension"``,
        ``"matrix_compression"``, ``"shear"``, or ``"no_stress"``
        when ``Sigma12`` is identically zero.
    SF_mode : float
        The smallest active per-mode safety factor (``inf`` for the
        all-zero stress case).
    mode_SFs : dict[str, float]
        All five per-mode safety factors keyed by mode name;
        inactive modes carry ``float('inf')``.  Useful for printing
        the full breakdown alongside ``mode`` and ``SF_mode``.
    """
    sigma1 = float(Sigma12[0])
    sigma2 = float(Sigma12[1])
    tau12  = float(Sigma12[2])

    # Per-mode max-stress safety factors.  Each ratio is
    # strength / |stress| for the one component that strength acts on,
    # with inactive modes set to +inf so they never win the min().
    mode_SFs = {
        "fiber_tension":      (ply["F1t"] / sigma1)      if sigma1 > 0 else np.inf,
        "fiber_compression":  (ply["F1c"] / -sigma1)     if sigma1 < 0 else np.inf,
        "matrix_tension":     (ply["F2t"] / sigma2)      if sigma2 > 0 else np.inf,
        "matrix_compression": (ply["F2c"] / -sigma2)     if sigma2 < 0 else np.inf,
        "shear":              (ply["F6"]  / abs(tau12))  if tau12 != 0 else np.inf,
    }

    # Identify the dominant mode (smallest SF among the active ones)
    SF_mode = min(mode_SFs.values())
    if not np.isfinite(SF_mode):
        # All modes inactive -> the stress state is identically zero.
        return "no_stress", np.inf, mode_SFs

    mode = min(mode_SFs, key=mode_SFs.get)
    return mode, SF_mode, mode_SFs
