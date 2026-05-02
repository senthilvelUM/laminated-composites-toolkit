"""Helper to print a 2D matrix."""

import numpy as np


def print_matrix(M, *, label=None, precision=3, width=10):
    """Print a 2D numerical matrix, one row per line.

    Each value is right-aligned in a fixed-width field with a fixed
    number of decimal places.

    Parameters
    ----------
    M : array-like
        The 2D matrix to print.
    label : str, optional
        If given, printed on its own line before the matrix.
    precision : int, optional
        Number of decimal places. Default: 3.
    width : int, optional
        Total field width per value. Default: 10.
    """
    if label is not None:
        print(label)
    M = np.asarray(M)
    for row in M:
        print("  " + "".join(f"{value:{width}.{precision}f}" for value in row))
