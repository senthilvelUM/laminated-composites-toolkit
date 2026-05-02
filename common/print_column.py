"""Helper to print a 1D array as a column."""

import numpy as np


def print_column(a, *, label=None, precision=3, width=10):
    """Print a numerical array as a column, one element per line.

    Right-aligns each value in a fixed-width field with a fixed number
    of decimal places. Accepts a 1D array, a 2D column array, or any
    iterable of scalars.

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
