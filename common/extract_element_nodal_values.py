#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: extract_element_nodal_values   (1-based variant)
#
#   Purpose: Extract the element nodal displacement vector d from the
#            global displacement vector D, and compute the corresponding
#            element nodal force vector f = Ke[n] @ d.
#
#   Input:
#     n    - element number (1-based: 1, 2, ..., ELEMENTS)
#     Ke   - 1-padded list of element stiffness matrices: Ke[1], Ke[2], ...
#            (Ke[0] is a dummy slot)
#     EDOF - element DOF table:
#            column 0      : element number (1-based)
#            columns 1:end : corresponding global DOF numbers (1-based)
#     D    - 1-padded global displacement vector (size GDOF + 1)
#
#   Output:
#     d    - element nodal displacement vector (tight, 0-based)
#     f    - internal element nodal forces (tight, 0-based)
#*********************************************************************
import numpy as np



__all__ = ["extract_element_nodal_values"]

def extract_element_nodal_values(n, Ke, EDOF, D):

    EDOF = np.asarray(EDOF)
    if n < 1 or n > EDOF.shape[0]:
        raise ValueError("Element number n is out of range. "
                         "It must satisfy 1 <= n <= ELEMENTS.")

    # Element stiffness matrix and number of element DOFs (Ke is 1-padded)
    kelement = Ke[n]
    kndof = kelement.shape[0]

    # Find the EDOF row whose column-0 label equals n
    matches = np.where(EDOF[:, 0] == n)[0]
    if matches.size == 0:
        raise ValueError(f"Element {n} not found in the first column of EDOF")
    eidx = int(matches[0])

    # Initialize and extract element nodal displacements from the padded
    # global vector. EDOF cols 1..end hold 1-based DOF labels; D is 1-padded
    # so D[label] reads the right slot directly.
    d = np.zeros(kndof)
    for i in range(kndof):
        gdof = int(EDOF[eidx, 1 + i])
        d[i] = D[gdof]

    # Compute internal element nodal forces (kelement is 0-based local)
    f = kelement @ d

    return d, f
