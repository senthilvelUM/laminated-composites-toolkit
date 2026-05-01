"""Display the properties of a ply to the terminal."""

from common.print_matrix import print_matrix


def display_ply_properties(ply):
    """Print the contents of a ply dictionary in a human-readable format.

    Parameters
    ----------
    ply : dict
        Ply dictionary created by create_ply().
    """
    print()
    print("****** Ply properties ******")
    print()
    print(f"Material: {ply['name']}")
    print(f"  type = {ply['type']}")
    print(f"  rho  = {ply['rho']:.1f} kg/m^3")

    print()
    print("-- Elastic properties --")
    print(f"  E1   = {ply['E1']/1e9:.2f} GPa")
    print(f"  E2   = {ply['E2']/1e9:.2f} GPa")
    print(f"  nu12 = {ply['nu12']:.3f}")
    print(f"  nu21 = {ply['nu21']:.3f}")
    print(f"  G12  = {ply['G12']/1e9:.2f} GPa")

    print()
    print("-- Strength properties --")
    print(f"  F1t  = {ply['F1t']/1e6:.1f} MPa")
    print(f"  F1c  = {ply['F1c']/1e6:.1f} MPa")
    print(f"  F2t  = {ply['F2t']/1e6:.1f} MPa")
    print(f"  F2c  = {ply['F2c']/1e6:.1f} MPa")
    print(f"  F6   = {ply['F6']/1e6:.1f} MPa")

    print()
    print("-- Ply geometry --")
    print(f"  theta = {ply['theta']:.1f} deg")
    print(f"  h     = {ply['h']*1e3:.3f} mm")

    print()
    print_matrix(ply["S"] * 1e12, label="-- Reduced compliance matrix S (TPa^-1) --")

    print()
    print_matrix(ply["Q"] / 1e9, label="-- Reduced stiffness matrix Q (GPa) --")

    print()
    print_matrix(ply["Ts"], label="-- Stress transformation matrix Ts --")

    print()
    print_matrix(ply["Te"], label="-- Strain transformation matrix Te --")

    print()
    print_matrix(ply["TsInv"], label="-- Inverse stress transformation matrix TsInv --")

    print()
    print_matrix(ply["TeInv"], label="-- Inverse strain transformation matrix TeInv --")

    print()
    print_matrix(ply["SBar"] * 1e12, label="-- Off-axis compliance matrix SBar (TPa^-1) --")

    print()
    print_matrix(ply["QBar"] / 1e9, label="-- Off-axis stiffness matrix QBar (GPa) --")

    print()
    print("-- Elastic properties in the global (x-y) coordinate system --")
    print(f"  Ex   = {ply['Ex']/1e9:.2f} GPa")
    print(f"  Ey   = {ply['Ey']/1e9:.2f} GPa")
    print(f"  nuxy = {ply['nuxy']:.3f}")
    print(f"  Gxy  = {ply['Gxy']/1e9:.2f} GPa")
    print()
