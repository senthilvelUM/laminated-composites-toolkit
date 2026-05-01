"""Pretty-print the failure-mode diagnostic returned by ``identify_failure_mode``.

Sibling to ``identify_failure_mode`` -- one computes, the other
displays.  Mirrors the ``create_ply`` / ``display_ply_properties``
and ``create_laminate`` / ``display_laminate_properties`` pairs
already in the project.
"""

__all__ = ["display_failure_mode"]


def display_failure_mode(mode, SF_mode, mode_SFs, *, inactive_threshold=1e6):
    """Print the per-mode failure-mode breakdown in the standard runner format.

    Output looks like::

          Dominant failure mode at z_min:           matrix_tension
          Max-stress SF for the dominant mode:         1.400
          Per-mode max-stress safety factors:
            fiber_tension          27.000
            fiber_compression       inactive
            matrix_tension           1.400
            matrix_compression      inactive
            shear                    3.000

    Inactive modes (e.g. fibre compression when sigma1 > 0) are
    rendered verbatim as ``inactive``.  Modes whose per-mode SF
    exceeds ``inactive_threshold`` are also collapsed to
    ``inactive``: those SFs come from a stress component that is
    floating-point noise (e.g. tau12 ~ 1e-17 produces SF ~ 1e24),
    not a genuinely low utilisation.

    Parameters
    ----------
    mode : str
        Dominant mode name returned by ``identify_failure_mode``.
    SF_mode : float
        Smallest active per-mode SF returned by
        ``identify_failure_mode``.
    mode_SFs : dict[str, float]
        Per-mode SFs returned by ``identify_failure_mode``.
    inactive_threshold : float, optional
        SFs above this value print as ``inactive``.  Default 1e6,
        chosen so any pedagogically meaningful margin
        (textbook problems rarely exceed SF ~ 100) prints
        verbatim, while numerical-noise SFs get suppressed.
    """
    print(f"\n  Dominant failure mode at z_min:           {mode}")
    print(f"  Max-stress SF for the dominant mode:    {SF_mode:10.3f}")
    print("  Per-mode max-stress safety factors:")
    for m, sf in mode_SFs.items():
        if sf == float("inf") or sf > inactive_threshold:
            print(f"    {m:<20s}    inactive")
        else:
            print(f"    {m:<20s}    {sf:.3f}")
