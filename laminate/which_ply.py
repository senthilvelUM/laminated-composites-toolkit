"""Determine which ply contains a given thickness coordinate."""


def which_ply(laminate, z):
    """Return the 1-based ply number that contains the z-coordinate.

    Ply k occupies the interval [laminate["z"][k-1], laminate["z"][k]],
    so this function scans from ply 1 upward and returns the first k
    whose interval contains z.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    z : float
        Thickness coordinate in meters (within [-H/2, +H/2]).

    Returns
    -------
    int
        1-based ply number containing z.

    Raises
    ------
    ValueError
        If z lies outside the laminate bounds.
    """
    for k in range(1, laminate["N"] + 1):
        if laminate["z"][k-1] <= z <= laminate["z"][k]:
            return k
    raise ValueError(
        f"z = {z} m is outside the laminate bounds "
        f"[{laminate['z'][0]}, {laminate['z'][-1]}] m."
    )
