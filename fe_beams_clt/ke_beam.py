#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: ke_beam
#
#  Purpose:
#    This function generates the local stiffness matrix for a
#    two-node Euler–Bernoulli beam element in bending.
#
#  Inputs:
#    EI - Bending rigidity (Young's modulus x area moment of inertia) of
#         the element. For a laminated cross-section this is the section
#         bending stiffness as a whole; E and I have no separate meaning.
#    L  - Length of the element
#
#  Output:
#    ke - 4x4 element stiffness matrix
#*********************************************************************
import numpy as np



__all__ = ["ke_beam"]

def ke_beam(EI, L):

    # Generate element stiffness matrix for an Euler–Bernoulli beam element
    ke = (EI / L**3) * np.array([
        [ 12,       6 * L,   -12,       6 * L    ],
        [  6 * L,   4 * L*L,  -6 * L,   2 * L*L  ],
        [-12,      -6 * L,    12,      -6 * L    ],
        [  6 * L,   2 * L*L,  -6 * L,   4 * L*L  ],
    ])

    return ke
