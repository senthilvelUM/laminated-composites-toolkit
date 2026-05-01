"""Mesh-construction and boundary-condition helpers shared by the
plate-FE runners.  Both plate toolkits (CLT-MZC and FSDT-bilinear)
use the same axis-aligned rectangular mesh of 4-noded
quadrilateral elements with 3 DOFs per node, so the helpers below
are toolkit-agnostic.

Public functions:
    generate_rectangular_mesh(Lx, Ly, N_x, N_y)
    simply_supported_bcs_plate(N_x, N_y, NDOF, variant)
    clamped_bcs_plate(N_x, N_y, NDOF)
"""

import numpy as np


__all__ = ["generate_rectangular_mesh",
           "simply_supported_bcs_plate",
           "clamped_bcs_plate"]


def generate_rectangular_mesh(Lx, Ly, N_x, N_y):
    """Build an axis-aligned rectangular mesh of bilinear-quad elements.

    The plate occupies [0, Lx] x [0, Ly].  Nodes are arranged on a
    regular (N_x+1) by (N_y+1) grid, numbered row-major with x
    increasing fastest (so node (i, j) has 1-based label
    nid = i + j*(N_x+1) + 1, with i = 0..N_x and j = 0..N_y).
    Elements are CCW-numbered with corners at the lower-left,
    lower-right, upper-right, upper-left of each cell.

    Parameters
    ----------
    Lx, Ly : float
        Plate dimensions in x and y (m).
    N_x, N_y : int
        Number of elements in x and y.

    Returns
    -------
    NODALCOORDINATES : (NODES, 3) float ndarray
        1-based node table: column 0 = node id, columns 1 and 2 = x, y.
    ENODES : (ELEMENTS, 5) int ndarray
        1-based element connectivity table: column 0 = element id,
        columns 1..4 = the four corner-node ids in CCW order.
    """
    NODES_x = N_x + 1
    NODES_y = N_y + 1
    NODES   = NODES_x * NODES_y
    ELEMENTS = N_x * N_y

    NODALCOORDINATES = np.zeros((NODES, 3))
    for j in range(NODES_y):
        for i in range(NODES_x):
            nid = i + j * NODES_x + 1
            NODALCOORDINATES[nid - 1, 0] = nid
            NODALCOORDINATES[nid - 1, 1] = i * Lx / N_x
            NODALCOORDINATES[nid - 1, 2] = j * Ly / N_y

    ENODES = np.zeros((ELEMENTS, 5), dtype=int)
    e_id = 1
    for jy in range(N_y):
        for ix in range(N_x):
            n1 = ix     + jy       * NODES_x + 1
            n2 = (ix+1) + jy       * NODES_x + 1
            n3 = (ix+1) + (jy + 1) * NODES_x + 1
            n4 = ix     + (jy + 1) * NODES_x + 1
            ENODES[e_id - 1, :] = [e_id, n1, n2, n3, n4]
            e_id += 1

    return NODALCOORDINATES, ENODES


def simply_supported_bcs_plate(N_x, N_y, NDOF=3, variant="SS1"):
    """Build the EBCList for a simply-supported plate on a rectangular
    grid of N_x by N_y elements.

    Two SS variants are supported:

    - "SS1" (hard simply supported): w = 0 on all edges, plus the
      edge-tangential rotation/slope is constrained.  On edges
      parallel to the y-axis (x = const) the rotation phi_y is fixed;
      on edges parallel to the x-axis the rotation phi_x is fixed.
      This is the FSDT counterpart of the CLPT edge-tangential-slope
      condition.
    - "SS2" (soft simply supported): w = 0 on all edges; both
      rotations are left free.  Different from SS1 in FSDT (gives
      slightly lower frequencies for thick plates) but identical in
      the Kirchhoff thin-plate limit.

    Parameters
    ----------
    N_x, N_y : int
        Number of elements in x and y.
    NDOF : int, optional
        DOFs per node (default 3 for plates: w, phi_x, phi_y).
    variant : {"SS1", "SS2"}, optional
        Hard or soft simply supported.

    Returns
    -------
    EBCList : sorted list of int
        1-based DOF labels of the constrained DOFs.
    """
    if variant not in ("SS1", "SS2"):
        raise ValueError(f'variant must be "SS1" or "SS2"; got "{variant}"')

    NODES_x = N_x + 1
    NODES_y = N_y + 1
    EBCList = []
    for j in range(NODES_y):
        for i in range(NODES_x):
            nid = i + j * NODES_x + 1
            on_edge_x0  = (i == 0)
            on_edge_xLx = (i == N_x)
            on_edge_y0  = (j == 0)
            on_edge_yLy = (j == N_y)
            on_any_edge = on_edge_x0 or on_edge_xLx or on_edge_y0 or on_edge_yLy
            if on_any_edge:
                EBCList.append((nid - 1) * NDOF + 1)        # w = 0
            if variant == "SS1":
                if on_edge_x0 or on_edge_xLx:
                    EBCList.append((nid - 1) * NDOF + 3)    # phi_y = 0 on x-axis edges
                if on_edge_y0 or on_edge_yLy:
                    EBCList.append((nid - 1) * NDOF + 2)    # phi_x = 0 on y-axis edges
    return sorted(set(EBCList))


def clamped_bcs_plate(N_x, N_y, NDOF=3):
    """Build the EBCList for a fully clamped plate (w = phi_x = phi_y = 0
    on all four edges) on a rectangular grid of N_x by N_y elements.

    Parameters
    ----------
    N_x, N_y : int
        Number of elements in x and y.
    NDOF : int, optional
        DOFs per node (default 3).

    Returns
    -------
    EBCList : sorted list of int
        1-based DOF labels of the constrained DOFs.
    """
    NODES_x = N_x + 1
    NODES_y = N_y + 1
    EBCList = []
    for j in range(NODES_y):
        for i in range(NODES_x):
            nid = i + j * NODES_x + 1
            on_edge = (i == 0) or (i == N_x) or (j == 0) or (j == N_y)
            if on_edge:
                base = (nid - 1) * NDOF
                EBCList.append(base + 1)    # w = 0
                EBCList.append(base + 2)    # phi_x = 0
                EBCList.append(base + 3)    # phi_y = 0
    return sorted(set(EBCList))
