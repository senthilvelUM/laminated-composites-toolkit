#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: generate_edofs   (1-based variant)
#
#   Purpose: Generate the element DOF table (EDOF) from the element
#            connectivity table (ENODES) and the number of DOFs per node.
#
#   Input:
#     ENODES  - element connectivity table:
#               column 0      : element number (1-based)
#               columns 1:end : global node numbers (local node order, 1-based)
#     NDOF    - number of degrees of freedom per node
#     verbose - if True (default False), prints a mesh summary and the
#               full EDOF table.  Useful when first learning the
#               assembly process; leave False for production runs.
#
#   Output:
#     EDOF   - element DOF table:
#              column 0      : element number (1-based)
#              columns 1:end : corresponding global DOF numbers (1-based)
#*********************************************************************
import numpy as np

from .print_matrix import print_matrix



__all__ = ["generate_edofs"]

def generate_edofs(enodes, ndof, verbose=False):

    # Reorder ENODES so element numbers are in ascending order
    enodes = np.asarray(enodes)
    enodes = enodes[enodes[:, 0].argsort()]

    #------------------------------------------------
    #  Input checks for element numbers
    #------------------------------------------------
    elem_nums = enodes[:, 0]

    # Check if element number starts at 1
    if elem_nums.min() != 1:
        raise ValueError(f"Invalid ENODES: element numbering must start at 1. "
                         f"Found minimum element number = {elem_nums.min()}.")

    # Check uniqueness
    if len(np.unique(elem_nums)) != len(elem_nums):
        raise ValueError("Invalid ENODES: duplicate element numbers detected.")

    # Check for missing element numbers within the range
    expected = np.arange(1, elem_nums.max() + 1)
    missing = np.setdiff1d(expected, elem_nums)
    if missing.size:
        raise ValueError(f"Invalid ENODES: missing element numbers: {missing.tolist()}")

    #------------------------------------------------
    # Input checks for node numbers in ENODES
    #------------------------------------------------
    # Check if there are at least 2 nodes per element
    if enodes.shape[1] < 2:
        raise ValueError("Invalid ENODES: must have at least two columns "
                         "[elementID, node1, ...].")

    ref_nodes = np.unique(enodes[:, 1:])   # unique node IDs referenced by elements

    # Lowest referenced node must be 1
    if ref_nodes[0] != 1:
        raise ValueError(f"Invalid ENODES: referenced node numbers must start at 1. "
                         f"Minimum referenced node = {ref_nodes[0]}.")

    # No missing node numbers: must be exactly 1..max(refNodes)
    expected = np.arange(1, ref_nodes[-1] + 1)
    missing = np.setdiff1d(expected, ref_nodes)
    if missing.size:
        raise ValueError(f"Invalid ENODES: missing referenced node numbers: "
                         f"{missing.tolist()}")

    elements, ncols = enodes.shape
    NODES = int(ref_nodes[-1])              # Total number of nodes (1-based labels)

    if verbose:
        print("\n------------------------------------------------")
        print("  Mesh summary (printout for verification)")
        print("------------------------------------------------")
        print(f"  Total number of elements    = {elements}")
        print(f"  Total number of nodes       = {NODES}")
        if ndof > 1:
            print(f"  Degrees of freedom per node = {ndof}")
            print(f"  Total degrees of freedom    = {ndof * NODES}")

    # Number of nodes per element
    num_elem_nodes = ncols - 1

    #------------------------------------------------
    # Initialize EDOF array (rows tightly packed, one row per element;
    # column 0 stores the 1-based element number; columns 1:end store
    # the 1-based global DOF labels)
    #------------------------------------------------
    edof = np.zeros((elements, 1 + num_elem_nodes * ndof), dtype=int)

    #------------------------------------------------
    # Build EDOF row-by-row
    #------------------------------------------------
    for row in range(elements):
        dof_array = []
        for a in range(num_elem_nodes):
            node = int(enodes[row, 1 + a])               # 1-based node label
            for k in range(1, ndof + 1):
                dof_array.append((node - 1) * ndof + k)  # 1-based DOF label

        edof[row, 0] = int(enodes[row, 0])               # 1-based element number
        edof[row, 1:] = dof_array

    if verbose and ndof > 1:
        print("\n  Global DOF numbering is contiguous:")
        print(f"  i.e., Node 1: DOFs 1–{ndof},   "
              f"Node 2: DOFs {ndof + 1}–{2 * ndof},  etc.")

        # Print the element DOF table
        print_matrix(edof, label="\n  Element degree-of-freedom table (EDOF)", width=6)
        print("  Note: Column 0 is the element number (1-based)")
        print("        Columns 1:end are the global DOF numbers for each element (1-based)")

    return edof
