#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Function: assemble   (1-based variant)
#
#   Purpose: Assemble a global matrix (stiffness or mass) from per-element
#            matrices using the element DOF/connectivity table.
#
#   Input:
#     ke    - 1-padded list of element matrices: ke[1], ke[2], ..., ke[ELEMENTS]
#             (ke[0] is a dummy slot, never accessed)
#     GDOF  - total number of global degrees of freedom
#     EDOF  - element DOF table:
#             column 0      : element number (1-based)
#             columns 1:end : corresponding global DOF numbers (1-based)
#     label   - "stiffness" (default) or "mass" — controls the wording of
#               the progress messages only.
#     verbose - if True (default False), prints a per-element progress
#               banner.  Useful when first learning the assembly process;
#               leave False for production runs to keep the output clean.
#
#   Output:
#     K    - assembled global matrix, tight shape (GDOF, GDOF), 0-based
#            internal indexing.
#*********************************************************************
import numpy as np



__all__ = ["assemble"]

def assemble(ke, GDOF, EDOF, label="stiffness", verbose=False):

    #------------------------------------------------
    # Basic consistency checks on the element table
    #------------------------------------------------
    # Reorder EDOF so element numbers are in ascending order
    EDOF = np.asarray(EDOF)
    EDOF = EDOF[EDOF[:, 0].argsort()]

    # Number of elements (column 0 stores 1-based labels, so the max IS the count)
    ELEMENTS = int(EDOF[:, 0].max())

    # Check that element numbers are unique
    if len(np.unique(EDOF[:, 0])) != EDOF.shape[0]:
        raise ValueError("The first column of EDOF must contain distinct element numbers.")

    #------------------------------------------------
    # Initialize the global stiffness matrix (tight, 0-based internal)
    #------------------------------------------------
    K = np.zeros((GDOF, GDOF))

    if verbose:
        print("\n------------------------------------------------")
        print(f"  Assembling the global {label} matrix")
        print("------------------------------------------------")

    #------------------------------------------------
    # Loop over all elements (1-based labels)
    #------------------------------------------------
    for e in range(1, ELEMENTS + 1):

        if verbose:
            # Display current element being assembled
            print(f"Inserting {label} matrix for element {e} into global matrix")

        # Element stiffness matrix for element e (ke is 1-padded)
        kelement = ke[e]

        # Number of DOFs associated with the element
        kdim = kelement.shape[0]

        # Row in EDOF whose column-0 label equals e
        matches = np.where(EDOF[:, 0] == e)[0]
        if matches.size == 0:
            raise ValueError(f"Element {e} not found in the first column of EDOF")
        eidx = matches[0]

        #------------------------------------------------
        # Loop over rows and columns of the element matrix
        #------------------------------------------------
        for i in range(kdim):

            # 1-based global DOF label for local row i
            P = int(EDOF[eidx, 1 + i])

            for j in range(kdim):

                # 1-based global DOF label for local column j
                Q = int(EDOF[eidx, 1 + j])

                # Bounds check (1-based labels)
                if P < 1 or P > GDOF or Q < 1 or Q > GDOF:
                    raise ValueError("Global DOF index exceeds GDOF during assembly. "
                                     "Check ENODES, EDOF and GDOF in the main script.")

                # Translate 1-based labels to 0-based K indices and accumulate
                K[P - 1, Q - 1] += kelement[i, j]

    return K
