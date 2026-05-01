"""Return a specific ply from a laminate by its 1-based number."""


def get_ply(laminate, k):
    """Return ply k from the laminate (1-based indexing).

    Equivalent to ``laminate["plies"][k]``, but raises a friendly
    IndexError if k is out of range.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    k : int
        1-based ply number (1 = bottom ply, N = top ply).

    Returns
    -------
    dict
        The ply dictionary for ply k.
    """
    if k < 1 or k > laminate["N"]:
        raise IndexError(
            f"Ply {k} does not exist: this laminate has "
            f"{laminate['N']} plies (1..{laminate['N']})."
        )
    return laminate["plies"][k]
