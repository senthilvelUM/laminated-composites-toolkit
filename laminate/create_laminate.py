"""Create a laminate dictionary from a stacking sequence of plies."""

import numpy as np

from ply.create_ply import create_ply


def create_laminate(ply_materials, ply_orientations, ply_thicknesses):
    """Create a laminate and evaluate its rigidities.

    Builds one ply per entry in the input lists (via create_ply), then
    computes the total thickness, ply interface z-coordinates, the
    laminate stiffness matrices A, B, D, the assembled 6x6 [ABD] and
    its inverse [abd], the mass moments of inertia I0, I1, I2, and the
    effective engineering properties in the global (x-y) frame.

    Plies are stored in a dict keyed by 1-based integers so that
    laminate["plies"][1], laminate["plies"][2], ... give ply 1, ply 2,
    etc. directly.

    Parameters
    ----------
    ply_materials : list of str
        Material names for each ply (matches files in materials/).
    ply_orientations : list of float
        Ply orientation angles in degrees.
    ply_thicknesses : list of float
        Ply thicknesses in meters.

    Returns
    -------
    dict
        Laminate dictionary with fields: plies, N, H, z, A, B, D, ABD,
        abd, a, b, c, d, I0, I1, I2, ExBar, EyBar, GxyBar, NuxyBar,
        NuyxBar. plies is a dict keyed 1..N; the numerical array z is
        0-based so ply k occupies the region z[k-1] <= z <= z[k].
    """
    laminate = {}

    # Number of plies
    laminate["N"] = len(ply_orientations)

    # Sanity check: the three parallel arrays must be the same length
    assert len(ply_materials) == laminate["N"], \
        "ply_materials and ply_orientations must have the same length"
    assert len(ply_thicknesses) == laminate["N"], \
        "ply_thicknesses and ply_orientations must have the same length"

    # Create each ply as a dict keyed by 1-based ply number
    laminate["plies"] = {
        k: create_ply(m, theta, h)
        for k, (m, theta, h) in enumerate(
            zip(ply_materials, ply_orientations, ply_thicknesses), start=1
        )
    }

    # Total laminate thickness
    laminate["H"] = sum(p["h"] for p in laminate["plies"].values())

    # z-coordinates of the ply interfaces (N+1 values, from -H/2 to +H/2).
    # Stored as a 0-based numpy array: ply k (1-based) occupies z[k-1]..z[k].
    z = np.zeros(laminate["N"] + 1)
    z[0] = -laminate["H"] / 2
    for k in range(1, laminate["N"] + 1):
        z[k] = z[k-1] + laminate["plies"][k]["h"]
    laminate["z"] = z

    # Layer-by-layer summation for the A, B, D stiffness matrices
    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))
    for k in range(1, laminate["N"] + 1):
        QBar = laminate["plies"][k]["QBar"]
        A = A + (z[k] - z[k-1]) * QBar
        B = B + (1/2) * (z[k]**2 - z[k-1]**2) * QBar
        D = D + (1/3) * (z[k]**3 - z[k-1]**3) * QBar
    laminate["A"] = A
    laminate["B"] = B
    laminate["D"] = D

    # Assemble the 6x6 [ABD] matrix
    laminate["ABD"] = np.block([[A, B], [B, D]])

    # Laminate compliances by inverting [ABD]
    abd = np.linalg.inv(laminate["ABD"])
    laminate["abd"] = abd
    laminate["a"] = abd[0:3, 0:3]
    laminate["b"] = abd[0:3, 3:6]
    laminate["c"] = abd[3:6, 0:3]
    laminate["d"] = abd[3:6, 3:6]

    # Mass moments of inertia (per unit area)
    I0 = 0.0
    I1 = 0.0
    I2 = 0.0
    for k in range(1, laminate["N"] + 1):
        rho = laminate["plies"][k]["rho"]
        I0 = I0 + rho * (z[k] - z[k-1])
        I1 = I1 + (1/2) * rho * (z[k]**2 - z[k-1]**2)
        I2 = I2 + (1/3) * rho * (z[k]**3 - z[k-1]**3)
    laminate["I0"] = I0
    laminate["I1"] = I1
    laminate["I2"] = I2

    # Transverse-shear stiffness matrix [A_s] of the laminate, used
    # by FSDT plate and Mindlin analyses.  This is the unscaled
    # ply-thickness-weighted sum
    #     A_s_alpha_beta = sum_k QsBar_alpha_beta(theta_k) * h_k,
    # alpha, beta in {4, 5}.  The shear correction factor kappa_s
    # (typically 5/6 for a rectangular cross-section) is NOT baked
    # in here -- the consuming runner multiplies by kappa_s when
    # assembling the section-level transverse-shear stiffness.
    A_s = np.zeros((2, 2))
    for k in range(1, laminate["N"] + 1):
        QsBar = laminate["plies"][k]["QsBar"]
        A_s = A_s + (z[k] - z[k-1]) * QsBar
    laminate["A_s"] = A_s

    # Effective engineering properties of the laminate
    a = laminate["a"]
    d = laminate["d"]
    H = laminate["H"]
    laminate["ExBar"]   = 1 / (a[0, 0] * H)
    laminate["EyBar"]   = 1 / (a[1, 1] * H)
    laminate["GxyBar"]  = 1 / (a[2, 2] * H)
    laminate["NuxyBar"] = -a[0, 1] / a[0, 0]
    laminate["NuyxBar"] = -a[0, 1] / a[1, 1]

    # Effective flexural moduli of the laminate
    laminate["Exfl"] = 12 / (d[0, 0] * H**3)
    laminate["Eyfl"] = 12 / (d[1, 1] * H**3)

    return laminate
