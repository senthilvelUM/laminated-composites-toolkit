#*********************************************************************
#                Finite Element Learning Toolkit
#
#                   Function: me_beam_lumped
#
#   Purpose: Generate the lumped mass matrix for a 2-node
#            Euler-Bernoulli beam element (transverse displacement
#            and rotation DOFs at each node).
#
#   Inputs:
#     rhoA - Linear mass density of the element (kg/m).  For an
#            isotropic beam this is rho * A.  For a symmetric laminate
#            of width b this is laminate["I0"] * b.
#     L    - Length of the element [m]
#
#   Output:
#     Me - 4x4 element lumped mass matrix
#          DOF ordering per node: [v  phi]
#
#   Notes:
#     The translational mass at each end node is rhoA*L/2 (half the
#     element mass).  The rotational mass is the standard textbook
#     L^2/12 multiplier on the translational half-mass:
#        rotational lump = (rhoA*L/2) * (L^2/12) = rhoA*L^3/24
#*********************************************************************
import numpy as np


__all__ = ["me_beam_lumped"]


def me_beam_lumped(rhoA, L):

    # Lumped mass matrix for an Euler-Bernoulli beam element
    Me = np.array([
        [rhoA * L / 2.0,  0.0,                   0.0,              0.0                  ],
        [0.0,             rhoA * L**3 / 24.0,    0.0,              0.0                  ],
        [0.0,             0.0,                   rhoA * L / 2.0,   0.0                  ],
        [0.0,             0.0,                   0.0,              rhoA * L**3 / 24.0   ],
    ])

    return Me
