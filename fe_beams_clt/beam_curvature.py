#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: beam_curvature
#
#  Purpose:
#    Evaluate the beam curvature  kappa(x) = v''(x)  at a single
#    location x along the beam, using the second derivatives of the
#    cubic Hermite shape functions on the element that contains x.
#
#  Inputs:
#    ENODES           - Element connectivity table (1-based labels).
#    NODALCOORDINATES - Nodal coordinate table (1-based labels).
#    D                - Global nodal displacement vector (1-padded).
#                       NDOF = 2 per node (v, phi).
#    x                - Target location along the beam (same units as
#                       NODALCOORDINATES x-coordinate).
#
#  Output:
#    kappa - The beam curvature v''(x) at the requested location.
#
#  Notes:
#    If x falls exactly on an interior element-element interface, the
#    left element is used (v'' is generally discontinuous between
#    cubic Hermite elements). For x outside the beam span a
#    ValueError is raised.
#*********************************************************************
import numpy as np

from common.which_element import which_element



__all__ = ["beam_curvature"]


def beam_curvature(ENODES, NODALCOORDINATES, D, x):

    NDOF = 2  # Beam: 2 DOFs per node (v, phi)

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    D = np.asarray(D).ravel()

    # Locate which element contains x (left-element wins on interior
    # interfaces; raises ValueError if x is outside the beam span).
    e = which_element(ENODES, NODALCOORDINATES, x)

    # Pull that element's end-node numbers from the connectivity table
    row = np.where(ENODES[:, 0] == e)[0][0]
    i = int(ENODES[row, 1])  # First  end-node (1-based)
    j = int(ENODES[row, 2])  # Second end-node (1-based)
    xi = NODALCOORDINATES[i - 1, 1]
    xj = NODALCOORDINATES[j - 1, 1]

    # Local coordinate within the element (xi=0 at node i, xi=L at node j)
    L = xj - xi
    xi_local = x - xi

    # Element nodal displacements/rotations
    v1   = D[(i - 1) * NDOF + 1]
    phi1 = D[(i - 1) * NDOF + 2]
    v2   = D[(j - 1) * NDOF + 1]
    phi2 = D[(j - 1) * NDOF + 2]

    # Second derivatives of the cubic Hermite shape functions
    # times L^3 (so the final 1/L^3 normalises everything)
    B1 =  12 * xi_local      - 6 * L
    B2 =   6 * xi_local * L  - 4 * L**2
    B3 = -12 * xi_local      + 6 * L
    B4 =   6 * xi_local * L  - 2 * L**2

    # Curvature: kappa(x) = v''(x) = (1/L^3) * [B1 B2 B3 B4] * [v1 phi1 v2 phi2]^T
    kappa = (B1 * v1 + B2 * phi1 + B3 * v2 + B4 * phi2) / L**3

    return kappa
