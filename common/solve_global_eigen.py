#*********************************************************************
#                Finite Element Learning Toolkit
#
#                  Function: solve_global_eigen   (1-based variant)
#
#  Purpose: Solve the generalized eigenvalue problem for the global
#           finite element system to obtain natural frequencies and
#           corresponding mode shapes.
#
#           [K - omega^2 * M] {D} = {0}
#
#  Inputs:
#    K        - global stiffness matrix, tight shape (GDOF, GDOF),
#               0-based internal indexing.
#    M        - global mass matrix,      tight shape (GDOF, GDOF),
#               0-based internal indexing.
#    EBCList  - list of 1-based DOF numbers subjected to essential
#               (displacement) boundary conditions.
#
#  Outputs:
#    omega - 1D array of natural frequencies (rad/s), sorted ascending.
#    D     - list of mode-shape vectors, one per natural frequency.
#            Each entry is 1-padded (size GDOF+1); index 0 is a dummy
#            slot, indices 1..GDOF carry the mode-shape values.
#            Constrained DOFs hold zeros and mode shapes are
#            mass-normalized so that D[k][1:].T @ M @ D[k][1:] = 1.
#*********************************************************************
import numpy as np



__all__ = ["solve_global_eigen"]

def solve_global_eigen(K, M, EBCList):

    K = np.asarray(K, dtype=float)
    M = np.asarray(M, dtype=float)

    GDOF = K.shape[0]

    # Translate 1-based EBCList to 0-based indices into K, M
    ebc0 = [int(dof) - 1 for dof in EBCList]

    # Create array of boundary conditions for each DOF (0-based, length GDOF)
    # 1 corresponds to displacement boundary condition
    # 0 corresponds to free DOF (retained in the reduced system)
    BCType = np.zeros(GDOF, dtype=int)
    for j in ebc0:
        BCType[j] = 1

    # Global DOFs that are free (retained) and constrained (removed)
    free = np.where(BCType == 0)[0]

    # Delete rows and columns of K and M corresponding to prescribed DOFs
    Kr = K[np.ix_(free, free)]
    Mr = M[np.ix_(free, free)]

    # Calculate the eigenvalues and eigenvectors of the reduced system
    # (convert K v = lambda M v to standard form A v = lambda v with
    # A = M^{-1} K; for symmetric K and symmetric positive definite M,
    # all eigenvalues are real and positive)
    A = np.linalg.solve(Mr, Kr)
    lam, V = np.linalg.eig(A)

    # Discard numerically small imaginary parts from round-off and
    # sort the modes by increasing eigenvalue (lowest frequency first)
    lam = np.real(lam)
    V   = np.real(V)
    order = np.argsort(lam)
    lam = lam[order]
    V   = V[:, order]

    # Mass-normalize each eigenvector so that v.T @ M @ v = 1
    for i in range(V.shape[1]):
        scale = np.sqrt(V[:, i].T @ Mr @ V[:, i])
        if scale > 0:
            V[:, i] = V[:, i] / scale

    # Natural frequencies (rad/s)
    omega = np.sqrt(np.abs(lam))

    # For each eigenvalue, populate the full 1-padded nodal displacement
    # vector with values from the reduced eigenvector. Index 0 is the
    # dummy slot; indices 1..GDOF carry the mode-shape values, with
    # zeros at constrained DOFs.
    NEIG = omega.size
    D = []
    for k in range(NEIG):
        d_full = np.zeros(GDOF + 1)
        d_full[1:][free] = V[:, k]
        D.append(d_full)

    return omega, D
