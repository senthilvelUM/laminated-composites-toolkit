#*********************************************************************
#                Finite Element Learning Toolkit
#
#                  Function: me_beam_rotary
#
#   Purpose: Generate the rotary-inertia consistent mass matrix for a
#            2-node Euler-Bernoulli beam element.  Adds the
#            cross-section rotational kinetic energy
#                T_rot = (1/2) integral rhoI * (dv/dx)_t**2 dx
#            to the standard translational mass matrix.  Together they
#            give the Rayleigh-beam mass matrix.
#
#   Inputs:
#     rhoI - Rotary inertia per unit length of the element (kg-m).
#            For an isotropic beam this is rho * I_section.  For a
#            symmetric laminate of width W this is laminate["I2"] * W,
#            where I2 = sum_k (rho_k / 3) * (z_k**3 - z_{k-1}**3) is
#            the laminate's second mass moment per unit area.
#     L    - Length of the element [m]
#
#   Output:
#     Me - 4x4 rotary-inertia mass matrix
#          DOF ordering per node: [v  phi]
#
#   Usage (typical):
#     me[n] = me_beam_consistent(rhoA[n], L[n])
#     me[n] += me_beam_rotary(rhoI[n], L[n])    # only if Rayleigh-beam
#*********************************************************************
import numpy as np


__all__ = ["me_beam_rotary"]


def me_beam_rotary(rhoI, L):

    # Rotary-inertia consistent mass matrix for an Euler-Bernoulli beam
    # element.  Comes from integrating rhoI * (N_i'(x) * N_j'(x)) over
    # the element using the cubic Hermite shape functions.
    Me = (rhoI / (30.0 * L)) * np.array([
        [ 36.0,    3.0 * L,    -36.0,     3.0 * L  ],
        [  3.0*L,  4.0 * L*L,   -3.0*L,  -1.0 * L*L],
        [-36.0,   -3.0 * L,     36.0,    -3.0 * L  ],
        [  3.0*L, -1.0 * L*L,   -3.0*L,   4.0 * L*L],
    ])

    return Me
