"""1-based array convention helper."""

import numpy as np


__all__ = ["one_based"]


def one_based(values):
    """Prepend a numerical zero to ``values`` so the result is 1-indexable.

    Lets the user write quantities indexed by element/node number using
    the bare textbook list, while still addressing entries with 1-based
    indices:

        k = one_based([100.0, 200.0])     # k[1] = 100.0,  k[2] = 200.0

    The dummy 0.0 inserted at index 0 is never read by the FE machinery
    (every loop runs from 1..N), so its actual value does not matter.
    """
    return np.r_[0.0, np.asarray(values, dtype=float).ravel()]
