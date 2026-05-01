"""Create a ply from a material name, orientation, and thickness."""

import numpy as np

from .load_material import load_material


def create_ply(material_name, theta, h):
    """Create a ply dictionary with all derived mechanical properties.

    The ply is a flat dict that starts from the loaded material and gets
    ply-specific fields added on top: orientation, thickness, minor
    Poisson's ratio, reduced compliance/stiffness matrices, stress and
    strain transformation matrices, off-axis compliance/stiffness
    matrices, and effective engineering properties in the global frame.

    Parameters
    ----------
    material_name : str
        Material name, e.g. "unidirectional_carbon_epoxy".
        Corresponds to materials/{material_name}.yaml.
    theta : float
        Ply orientation angle in degrees, measured from the global
        X-axis to the 1-material direction.
    h : float
        Ply thickness in meters.

    Returns
    -------
    dict
        Flat dict with material properties, ply geometry, and the
        derived fields: nu21, S, Q, Ts, Te, TsInv, TeInv, SBar, QBar,
        Ex, Ey, nuxy, Gxy.
    """
    ply = load_material(material_name)
    ply["material_name"] = material_name
    ply["theta"] = float(theta)
    ply["h"] = float(h)

    # Extract material properties for convenience
    E1 = ply["E1"]
    E2 = ply["E2"]
    nu12 = ply["nu12"]
    G12 = ply["G12"]

    # Minor Poisson's ratio from the reciprocal relation
    ply["nu21"] = nu12 * E2 / E1
    nu21 = ply["nu21"]

    # Reduced compliance matrix [S] (material axes, plane stress)
    S11 = 1 / E1
    S12 = -nu12 / E1
    S22 = 1 / E2
    S66 = 1 / G12
    ply["S"] = np.array([[S11, S12, 0],
                         [S12, S22, 0],
                         [0,   0,   S66]])

    # Reduced stiffness matrix [Q] (material axes, plane stress)
    Q11 = E1 / (1 - nu12 * nu21)
    Q12 = nu12 * E2 / (1 - nu12 * nu21)
    Q22 = E2 / (1 - nu12 * nu21)
    Q66 = G12
    ply["Q"] = np.array([[Q11, Q12, 0],
                         [Q12, Q22, 0],
                         [0,   0,   Q66]])

    # Cosine and sine of the ply angle
    m = np.cos(np.radians(theta))
    n = np.sin(np.radians(theta))

    # Strain transformation matrix [Te]: {eps_12} = Te {eps_xy}
    ply["Te"] = np.array([[m**2,    n**2,    m*n],
                          [n**2,    m**2,   -m*n],
                          [-2*m*n,  2*m*n,  m**2 - n**2]])

    # Inverse strain transformation matrix [TeInv]: {eps_xy} = TeInv {eps_12}
    ply["TeInv"] = np.array([[m**2,   n**2,   -m*n],
                             [n**2,   m**2,    m*n],
                             [2*m*n, -2*m*n,  m**2 - n**2]])

    # Stress transformation matrix [Ts]: {sig_12} = Ts {sig_xy}
    ply["Ts"] = np.array([[m**2,  n**2,    2*m*n],
                          [n**2,  m**2,   -2*m*n],
                          [-m*n,  m*n,    m**2 - n**2]])

    # Inverse stress transformation matrix [TsInv]: {sig_xy} = TsInv {sig_12}
    ply["TsInv"] = np.array([[m**2,  n**2,   -2*m*n],
                             [n**2,  m**2,    2*m*n],
                             [m*n,  -m*n,    m**2 - n**2]])

    # Off-axis compliance matrix [SBar] in the global (x-y) coordinate system
    SBar11 = S11*m**4 + (2*S12 + S66)*m**2*n**2 + S22*n**4
    SBar12 = (S11 + S22 - S66)*m**2*n**2 + S12*(m**4 + n**4)
    SBar16 = (2*S11 - 2*S12 - S66)*n*m**3 + (2*S12 - 2*S22 + S66)*n**3*m
    SBar22 = S11*n**4 + (2*S12 + S66)*n**2*m**2 + S22*m**4
    SBar26 = (2*S11 - 2*S12 - S66)*n**3*m + (2*S12 - 2*S22 + S66)*n*m**3
    SBar66 = 2*(2*S11 + 2*S22 - 4*S12 - S66)*n**2*m**2 + S66*(n**4 + m**4)
    ply["SBar"] = np.array([[SBar11, SBar12, SBar16],
                            [SBar12, SBar22, SBar26],
                            [SBar16, SBar26, SBar66]])

    # Off-axis stiffness matrix [QBar] in the global (x-y) coordinate system
    QBar11 = Q11*m**4 + 2*(Q12 + 2*Q66)*m**2*n**2 + Q22*n**4
    QBar12 = (Q11 + Q22 - 4*Q66)*m**2*n**2 + Q12*(m**4 + n**4)
    QBar16 = (Q11 - Q12 - 2*Q66)*n*m**3 + (Q12 - Q22 + 2*Q66)*n**3*m
    QBar22 = Q11*n**4 + 2*(Q12 + 2*Q66)*n**2*m**2 + Q22*m**4
    QBar26 = (Q11 - Q12 - 2*Q66)*n**3*m + (Q12 - Q22 + 2*Q66)*n*m**3
    QBar66 = (Q11 + Q22 - 2*Q12 - 2*Q66)*n**2*m**2 + Q66*(n**4 + m**4)
    ply["QBar"] = np.array([[QBar11, QBar12, QBar16],
                            [QBar12, QBar22, QBar26],
                            [QBar16, QBar26, QBar66]])

    # Effective engineering properties in the global coordinate system
    ply["Ex"] = 1 / SBar11
    ply["Ey"] = 1 / SBar22
    ply["nuxy"] = -SBar12 / SBar11
    ply["Gxy"] = 1 / SBar66

    # Transverse-shear stiffness matrix [Qs] in the material (1-2-3)
    # coordinate system.  With {tau_23, tau_13} = [Qs] {gamma_23,
    # gamma_13}, an orthotropic ply has Qs_44 = G23, Qs_55 = G13,
    # Qs_45 = 0.  Used by FSDT plate / Mindlin analyses.
    G13 = ply["G13"]
    G23 = ply["G23"]
    ply["Qs"] = np.array([[G23, 0.0],
                          [0.0, G13]])

    # Off-axis transverse-shear stiffness matrix [QsBar] in the
    # global (x-y-z) coordinate system, with row/column index
    # 1 -> (y-z) plane, 2 -> (x-z) plane.  Rotation by theta about
    # the z-axis gives the standard transformation
    #     QsBar_44 = G23 m^2 + G13 n^2
    #     QsBar_55 = G23 n^2 + G13 m^2
    #     QsBar_45 = (G13 - G23) m n
    # (see Reddy, Mechanics of Laminated Composite Plates and Shells,
    # eqs. 3.3.23-25).
    QsBar44 = G23 * m**2 + G13 * n**2
    QsBar55 = G23 * n**2 + G13 * m**2
    QsBar45 = (G13 - G23) * m * n
    ply["QsBar"] = np.array([[QsBar44, QsBar45],
                             [QsBar45, QsBar55]])

    return ply
