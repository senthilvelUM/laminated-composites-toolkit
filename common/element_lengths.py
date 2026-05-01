#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: element_lengths   (1-based variant)
#
#   Purpose : Compute the length of each beam element from its end-node
#             coordinates. This is a beams-only convenience wrapper that
#             discards the orientation angle returned by
#             element_lengths_orientations(); it is intended for users
#             whose elements all lie along the x-axis (theta = 0).
#
#   Inputs:
#     ENODES           - Element connectivity table (1-based labels).
#     NODALCOORDINATES - Nodal coordinate table (1-based labels).
#
#   Output:
#     L  - 1-padded array of element lengths (size ELEMENTS+1).
#          L[n] is the length of element n for n = 1..ELEMENTS;
#          L[0] is an unused dummy slot.
#*********************************************************************
from .element_lengths_orientations import element_lengths_orientations
from common.print_column import print_column



__all__ = ["element_lengths"]


def element_lengths(ENODES, NODALCOORDINATES):

    # Compute lengths (and orientations) silently, then print only L.
    L, _ = element_lengths_orientations(ENODES, NODALCOORDINATES, verbose=False)

    print_column(L[1:], label="\n  Array of element lengths [L]")

    return L
