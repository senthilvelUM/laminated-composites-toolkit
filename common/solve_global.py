#*********************************************************************
#                Finite Element Learning Toolkit
#
#                   Function: solve_global   (1-based variant)
#
#   Purpose: Solves the global system of finite element equations subject
#            to essential (displacement) boundary conditions.
#
#  Inputs:  K - global stiffness matrix, tight shape (GDOF, GDOF), 0-based
#               internal indexing.
#           D - 1-padded nodal displacement array of size GDOF+1; index 0
#               is a dummy slot. D[i] for i = 1..GDOF carries any
#               prescribed displacements.
#           F - 1-padded nodal force array of size GDOF+1; same convention.
#           EBCList - list of 1-based DOF numbers subjected to essential
#               boundary conditions.
#
#  Outputs: D - 1-padded solution array (size GDOF+1) for the nodal
#               displacements.
#           F - 1-padded solution array (size GDOF+1) for the nodal
#               forces, with reactions written into the prescribed-DOF
#               slots.
#*********************************************************************
import warnings
import numpy as np



__all__ = ["solve_global"]

def solve_global(K, D, F, EBCList):

    print("\n------------------------------------------------")
    print("  Solving the global system of equations")
    print("------------------------------------------------")

    # -------------------------
    # Basic setup and bookkeeping
    # -------------------------
    K = np.array(K, dtype=float, copy=True)
    GDOF = K.shape[0]

    D = np.asarray(D, dtype=float)
    F = np.asarray(F, dtype=float)
    if D.size != GDOF + 1 or F.size != GDOF + 1:
        raise ValueError("D and F must be 1-padded (size GDOF + 1) on entry to solve_global.")

    # Tight 0-based working copies for the linear algebra
    D_tight = D[1:].copy()
    F_tight = F[1:].copy()
    K_work  = K.copy()
    F_work  = F_tight.copy()

    # Translate 1-based EBCList to 0-based indices for the tight system
    ebc0 = [int(i) - 1 for i in EBCList]

    # Create array of boundary conditions for each DOF (0-based, length GDOF)
    #   BCType[j] = 1  -> prescribed displacement (essential BC)
    #   BCType[j] = 0  -> applied force / free displacement DOF
    BCType = np.zeros(GDOF, dtype=int)
    for j in ebc0:
        BCType[j] = 1

    # Preserve original system for post-processing reactions
    K0    = K.copy()
    F0    = F_tight.copy()
    Dpres = D_tight.copy()

    # ---------------------------------------------------------
    # Enforce essential boundary conditions by modifying K and F
    # ---------------------------------------------------------
    # For each prescribed DOF j (0-based):
    #   1) Move contribution K[:,j]*Dpres[j] to the RHS (all rows)
    #   2) Zero out row j and column j
    #   3) Set K[j,j] = 1 and F[j] = Dpres[j] to enforce u_j = Dpres[j]
    for j in ebc0:

        # Move known displacement contribution to the RHS
        F_work = F_work - K_work[:, j] * Dpres[j]

        # Zero out column j and row j
        K_work[:, j] = 0.0
        K_work[j, :] = 0.0

        # Impose u_j = Dpres[j]
        K_work[j, j] = 1.0
        F_work[j] = Dpres[j]

    # Check the condition number of the modified matrix K_work
    if 1.0 / np.linalg.cond(K_work, 1) < 1e-12:
        warnings.warn("Matrix K is close to singular and the results may be inaccurate. "
                      "Double check the input variables, e.g. ELEMENTS, NODES, EBCList, etc., "
                      "to make sure they have been correctly specified.")

    # Solve for displacements
    D_solved = np.linalg.solve(K_work, F_work)

    # ---------------------------------------------------------
    # Compute reaction forces using the ORIGINAL equilibrium equations
    # ---------------------------------------------------------
    # R = K0 @ D_solved - F0 gives the reaction/residual at every DOF.
    R = K0 @ D_solved - F0

    # Build the output force vector (tight, 0-based):
    #   - free DOFs      : applied forces (same as input)
    #   - prescribed DOFs: reactions
    F_out_tight = F0.copy()
    for j in range(GDOF):
        if BCType[j] == 1:
            F_out_tight[j] = R[j]

    # Re-pad outputs so the caller can keep using 1-based indexing
    D_out = np.zeros(GDOF + 1)
    F_out = np.zeros(GDOF + 1)
    D_out[1:] = D_solved
    F_out[1:] = F_out_tight
    return D_out, F_out
