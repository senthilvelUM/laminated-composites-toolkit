"""Helper to print a 1D array as a column (Matlab-style)."""

import numpy as np


def print_column(a, *, label=None, precision=3, width=10):
    """Print a numerical array as a column, one element per line.

    Mirrors the Matlab disp() style for column arrays. Accepts a
    1D array, a 2D column array, or any iterable of scalars.

    Parameters
    ----------
    a : array-like
        The array to print.
    label : str, optional
        If given, printed on its own line before the values.
    precision : int, optional
        Number of decimal places. Default: 3.
    width : int, optional
        Total field width per value. Default: 10.
    """
    if label is not None:
        print(label)
    for value in np.asarray(a).ravel():
        print(f"  {value:{width}.{precision}f}")
