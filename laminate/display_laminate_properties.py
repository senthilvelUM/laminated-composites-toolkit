"""Display the properties of a laminate to the terminal."""

from common.print_matrix import print_matrix
from ply.display_ply_properties import display_ply_properties


def display_laminate_properties(laminate, verbose=True):
    """Print the contents of a laminate dictionary in a human-readable format.

    With ``verbose=True`` (default), first shows the full properties of
    each ply (with a ``--- Ply k ---`` header), then the aggregate laminate
    quantities (thickness, A/B/D matrices, compliances, mass moments,
    effective elastic properties).

    With ``verbose=False``, skips the per-ply detail and prints only the
    laminate-level summary -- useful in FE runners where the laminate is
    a fixed input and the focus is the FE result.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    verbose : bool, optional
        If True (default), include the per-ply detail.  If False, only
        the laminate-level summary is printed.
    """
    if verbose:
        # Show each ply's properties in order
        for k, ply in laminate["plies"].items():
            print()
            print(f"--- Ply {k} ---")
            display_ply_properties(ply)

    # Ply orientations derived from the ply collection
    orientations = [p["theta"] for p in laminate["plies"].values()]
    z_mm = [f"{v*1e3:.3f}" for v in laminate["z"]]

    print()
    print("****** Laminate properties ******")
    print()
    print(f"Number of plies: N = {laminate['N']}")
    print(f"Ply orientations (deg): {orientations}")
    print(f"Laminate thickness H = {laminate['H']*1e3:.3f} mm")
    print(f"z coordinates (mm): [{', '.join(z_mm)}]")

    print()
    print("-- Laminate rigidities --")
    print()
    print_matrix(laminate["A"] / 1e6,  label="A (10^6 N/m):")
    print()
    print_matrix(laminate["B"],        label="B (N):")
    print()
    print_matrix(laminate["D"] / 1e-3, label="D (10^-3 N-m):")

    print()
    print("-- Laminate compliances --")
    print()
    print_matrix(laminate["a"] / 1e-9, label="a (10^-9 m/N):")
    print()
    print_matrix(laminate["b"] / 1e-3, label="b (10^-3 1/N):")
    print()
    print_matrix(laminate["d"],        label="d (1/N-m):")

    print()
    print("-- Mass moments of inertia --")
    print(f"  I0 = {laminate['I0']:.4g} kg/m^2")
    print(f"  I1 = {laminate['I1']:.4g} kg/m")
    print(f"  I2 = {laminate['I2']:.4g} kg")

    print()
    print("-- Effective in-plane elastic moduli --")
    print(f"  ExBar   = {laminate['ExBar']/1e9:.2f} GPa")
    print(f"  EyBar   = {laminate['EyBar']/1e9:.2f} GPa")
    print(f"  GxyBar  = {laminate['GxyBar']/1e9:.2f} GPa")
    print(f"  NuxyBar = {laminate['NuxyBar']:.3f}")
    print(f"  NuyxBar = {laminate['NuyxBar']:.3f}")

    print()
    print("-- Effective flexural elastic moduli --")
    print(f"  Exfl    = {laminate['Exfl']/1e9:.2f} GPa")
    print(f"  Eyfl    = {laminate['Eyfl']/1e9:.2f} GPa")
    print()
