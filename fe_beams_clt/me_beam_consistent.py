#*********************************************************************
#                Finite Element Learning Toolkit
#
#                  Function: me_beam_consistent
#
#   Purpose: Generate the consistent mass matrix for a 2-node
#            Euler-Bernoulli beam element (transverse displacement
#            and rotation DOFs at each node).
#
#   Inputs:
#     rhoA - Linear mass density of the element (mass per unit length,
#            in kg/m).  For an isotropic beam this is rho * A.  For a
#            symmetric laminate of width b this is laminate["I0"] * b,
#            where I0 = sum_k rho_k * h_k is the laminate's areal
#            mass density.
#     L    - Length of the element [m]
#
#   Output:
#     Me - 4x4 element consistent mass matrix
#          DOF ordering per node: [v  phi]
#*********************************************************************
import numpy as np


__all__ = ["me_beam_consistent"]


def me_beam_consistent(rhoA, L):

    # Consistent mass matrix for an Euler-Bernoulli beam element
    Me = (rhoA * L / 420.0) * np.array([
        [156.0,    22.0 * L,    54.0,   -13.0 * L  ],
        [ 22.0*L,   4.0 * L*L,  13.0*L,  -3.0 * L*L],
        [ 54.0,    13.0 * L,   156.0,   -22.0 * L  ],
        [-13.0*L,  -3.0 * L*L, -22.0*L,   4.0 * L*L],
    ])

    return Me
