#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: element_lengths_orientations   (1-based variant)
#
#   Purpose : Compute the length and in-plane orientation angle for each
#             2D truss/bar element based on nodal coordinates.
#
#   Inputs:
#     ENODES           - Element connectivity table:
#                        column 0 : element number (1-based)
#                        column 1 : first node number (i, 1-based)
#                        column 2 : second node number (j, 1-based)
#     NODALCOORDINATES - Nodal coordinate table:
#                        column 0 : node number (1-based)
#                        column 1 : x-coordinate
#                        column 2 : y-coordinate
#
#   Outputs:
#     L      - 1-padded array of element lengths (size ELEMENTS+1).
#              L[n] is the length of element n for n = 1..ELEMENTS;
#              L[0] is an unused dummy slot.
#     theta  - 1-padded array of element orientations (degrees),
#              measured CCW from +x to the element axis (i -> j).
#              Same indexing convention as L.
#
#   Notes:
#     - This function does NOT assume node numbers equal row indices in
#       NODALCOORDINATES; it looks up rows using the node-number column.
#*********************************************************************
import numpy as np

from common.print_column import print_column



__all__ = ["element_lengths_orientations"]

def element_lengths_orientations(ENODES, NODALCOORDINATES, verbose=True):

    #------------------------------------------------
    # Reorder ENODES and NODALCOORDINATES if they are not contiguous
    #------------------------------------------------
    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # Determine the total number of elements (column 0 stores 1-based labels)
    ELEMENTS = int(ENODES[:, 0].max())

    #------------------------------------------------
    # Consistency checks on nodal coordinate table
    #------------------------------------------------
    node_nums = NODALCOORDINATES[:, 0].astype(int)

    # Check if node numbering starts at 1
    if node_nums.min() != 1:
        raise ValueError(f"Invalid NODALCOORDINATES: node numbering must start at 1. "
                         f"Found minimum node number = {node_nums.min()}.")

    # Check uniqueness
    if len(np.unique(node_nums)) != len(node_nums):
        raise ValueError("Invalid NODALCOORDINATES: duplicate node numbers detected "
                         "in column 0.")

    # Check for missing node numbers within the range
    expected = np.arange(1, node_nums.max() + 1)
    missing = np.setdiff1d(expected, node_nums)
    if missing.size:
        raise ValueError(f"Invalid NODALCOORDINATES: missing node numbers: "
                         f"{missing.tolist()}")

    # Verify that the highest node number referenced in ENODES matches
    # the total number of nodes defined in NODALCOORDINATES
    max_node_enodes = int(ENODES[:, 1:].max())
    max_node_nodal = int(node_nums.max())
    if max_node_enodes != max_node_nodal:
        raise ValueError(
            f"Node mismatch detected:\n"
            f"  Maximum node ID referenced in ENODES        = {max_node_enodes}\n"
            f"  Maximum node ID defined in NODALCOORDINATES = {max_node_nodal}\n"
            f"Check for missing or extra node numbers.")

    # Preallocate 1-padded outputs (index 0 is an unused dummy slot)
    L = np.zeros(ELEMENTS + 1)
    theta = np.zeros(ELEMENTS + 1)

    # Loop through all elements and calculate the length and orientation
    for row in range(ENODES.shape[0]):

        e = int(ENODES[row, 0])      # 1-based element number

        # Element end node numbers (i -> j), both 1-based labels
        i = int(ENODES[row, 1])
        j = int(ENODES[row, 2])

        # Locate the rows in NODALCOORDINATES corresponding to nodes i and j
        idxi = np.where(node_nums == i)[0]
        idxj = np.where(node_nums == j)[0]

        if idxi.size == 0 or idxj.size == 0:
            raise ValueError(
                f"Node number not found in NODALCOORDINATES for element "
                f"{e} (i={i}, j={j}).")

        # Coordinates of the two nodes
        xi = NODALCOORDINATES[idxi[0], 1]
        yi = NODALCOORDINATES[idxi[0], 2]

        xj = NODALCOORDINATES[idxj[0], 1]
        yj = NODALCOORDINATES[idxj[0], 2]

        # Differences
        dx = xj - xi
        dy = yj - yi

        # Element length
        L[e] = np.sqrt(dx * dx + dy * dy)

        # Element orientation (degrees), CCW from +x
        theta[e] = np.rad2deg(np.arctan2(dy, dx))

    # Print the element lengths and orientations (skip the dummy slot)
    if verbose:
        print_column(L[1:],     label="\n  Array of element lengths [L]")
        print_column(theta[1:], label="  Array of element orientations [theta] (in degrees)")

    return L, theta
