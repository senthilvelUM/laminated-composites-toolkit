"""Helper to print a single scalar value on one line (with optional label)."""


def print_scalar(value, *, label=None, precision=3, width=10):
    """Print a single scalar value, inline with an optional label.

    Produces a single line such as:
        Location z (mm):      0.100

    Use this for quantities that are naturally scalars (safety factors,
    non-dimensional ratios, ...). For column arrays use print_column,
    and for 2D matrices use print_matrix.

    Parameters
    ----------
    value : float
        The scalar value to print.
    label : str, optional
        If given, printed on the same line before the value.
    precision : int, optional
        Number of decimal places. Default: 3.
    width : int, optional
        Minimum field width for the value (for right-alignment). Default: 10.
    """
    if label is None:
        print(f"  {value:{width}.{precision}f}")
    else:
        print(f"{label} {value:{width}.{precision}f}")
