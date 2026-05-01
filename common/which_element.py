#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: which_element
#
#  Purpose:
#    Return the 1-based element number that contains a given
#    x-coordinate along the beam.
#
#  Inputs:
#    ENODES           - Element connectivity table (1-based labels).
#    NODALCOORDINATES - Nodal coordinate table (1-based labels).
#    x                - Target location along the beam.
#
#  Output:
#    e - 1-based element number whose span [x_i, x_j] contains x.
#
#  Notes:
#    If x falls exactly on an interior element-element interface, the
#    LEFT element is returned (the first element whose span includes
#    x, walking left-to-right).  Raises ValueError if x is outside
#    the beam's [x_min, x_max] span.
#*********************************************************************
import numpy as np



__all__ = ["which_element"]


def which_element(ENODES, NODALCOORDINATES, x):

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # Sanity-check that x is inside the beam span
    x_coords = NODALCOORDINATES[:, 1]
    x_min, x_max = x_coords.min(), x_coords.max()
    if x < x_min or x > x_max:
        raise ValueError(
            f"x = {x} is outside the beam span [{x_min}, {x_max}]")

    # Walk the elements left-to-right and return the first one whose
    # span [x_i, x_j] contains x.
    for n in range(ENODES.shape[0]):
        e  = int(ENODES[n, 0])  # 1-based element number
        i  = int(ENODES[n, 1])  # First  end-node (1-based)
        j  = int(ENODES[n, 2])  # Second end-node (1-based)
        xi = NODALCOORDINATES[i - 1, 1]
        xj = NODALCOORDINATES[j - 1, 1]
        if xi <= x <= xj:
            return e

    # Should not be reachable given the bounds check above.
    raise ValueError(f"No element contains x = {x}")
