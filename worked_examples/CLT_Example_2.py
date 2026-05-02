"""Example 4.2 -- [ABD] and [abd] matrices for the [0/90]_S and [90/0]_S
cross-ply laminates.

Two four-ply IM7/8552 carbon/epoxy laminates, each ply 0.2 mm thick:
    [0/90]_S = [0, 90, 90, 0]    (stiff 0 deg plies on the outside)
    [90/0]_S = [90, 0, 0, 90]    (stiff 0 deg plies on the inside)

The script prints the per-laminate breakdown for each layup ([Q-bar],
[A], [B], [D], [a], [b], [d], engineering moduli), then closes with a
side-by-side comparison: [A] is identical, [D] differs by ~5x, and the
flexural modulus Ex_fl drops from 148 GPa to 29 GPa under reordering.
"""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import numpy as np

from common import *
from laminate import *


results_file = start_results_file(
    __file__,
    "Example 4.2 -- [ABD] and [abd] matrices for the [0/90]_S and [90/0]_S laminates",
)

# --- Shared parameters ---
N        = 4
material = "unidirectional_carbon_epoxy"   # IM7/8552
h        = 0.2e-3                           # ply thickness, m


def analyze_layup(label, ply_orientations):
    """Build a four-ply laminate, print its full breakdown, return key metrics."""
    print("\n" + "=" * 72)
    print(f"LAYUP: {label}   (bottom -> top: {ply_orientations})")
    print("=" * 72)

    ply_materials   = [material] * N
    ply_thicknesses = [h] * N
    check_laminate_inputs(N, ply_materials, ply_orientations, ply_thicknesses)
    laminate = create_laminate(ply_materials, ply_orientations, ply_thicknesses)

    print(f"Total H = {laminate['H']*1e3:.3f} mm  ({N} plies of {h*1e3:.3f} mm)")

    # Off-axis ply stiffness, one matrix per distinct orientation
    print("\nOff-axis ply stiffness QBar (GPa):")
    seen = set()
    for k in range(1, laminate["N"] + 1):
        theta = laminate["plies"][k]["theta"]
        if theta in seen:
            continue
        seen.add(theta)
        print()
        print_matrix(laminate["plies"][k]["QBar"] / 1e9,
                     label=f"QBar({theta:+.0f} deg):", precision=3)

    # Stiffness matrices [A], [B], [D]
    print("\nLaminate stiffness matrices:")
    print()
    print_matrix(laminate["A"] / 1e6, label="[A]  (MN/m):", precision=3)
    print()
    print_matrix(laminate["B"],       label="[B]  (N) -- should be zero:", precision=6)
    print()
    print_matrix(laminate["D"],       label="[D]  (N.m):", precision=4)
    print(f"\nMax |B_ij| = {np.max(np.abs(laminate['B'])):.3e} N (numerically zero)")

    # Compliance matrices [a], [b], [d]
    print("\nLaminate compliance matrices:")
    print()
    print_matrix(laminate["a"] * 1e9, label="[a]  (10^-9 m/N):", precision=4)
    print()
    print_matrix(laminate["b"],       label="[b]  (1/N) -- should be zero:", precision=6)
    print()
    print_matrix(laminate["d"],       label="[d]  (1/(N.m)):", precision=5)

    # Effective engineering moduli
    print("\nEffective laminate moduli (GPa):")
    print_scalar(laminate["ExBar"]  / 1e9, label="Ex_bar  :")
    print_scalar(laminate["EyBar"]  / 1e9, label="Ey_bar  :")
    print_scalar(laminate["GxyBar"] / 1e9, label="Gxy_bar :")
    print_scalar(laminate["NuxyBar"],       label="nuxy_bar:")
    print_scalar(laminate["Exfl"]   / 1e9, label="Ex_fl   :")
    print_scalar(laminate["Eyfl"]   / 1e9, label="Ey_fl   :")

    return {
        "A_11":   laminate["A"][0, 0], "A_12":   laminate["A"][0, 1], "A_66":  laminate["A"][2, 2],
        "D_11":   laminate["D"][0, 0], "D_22":   laminate["D"][1, 1], "D_66":  laminate["D"][2, 2],
        "Ex_bar": laminate["ExBar"],   "Ex_fl":  laminate["Exfl"],
    }


# --- Run both layups ---
r1 = analyze_layup("[0/90]_S", [0, 90, 90, 0])
r2 = analyze_layup("[90/0]_S", [90, 0, 0, 90])

# --- Comparison summary ---
print("\n" + "=" * 72)
print("COMPARISON SUMMARY")
print("=" * 72)
print(f"\n{'Quantity':<14}  {'[0/90]_S':>12}  {'[90/0]_S':>12}  {'ratio':>10}")
print("-" * 54)

def row(label, v1, v2):
    ratio = v2 / v1 if v1 != 0 else float("nan")
    print(f"{label:<14}  {v1:>12.3f}  {v2:>12.3f}  {ratio:>10.3f}")

row("A_11 (MN/m)",  r1["A_11"]   / 1e6, r2["A_11"]   / 1e6)
row("A_12 (MN/m)",  r1["A_12"]   / 1e6, r2["A_12"]   / 1e6)
row("A_66 (MN/m)",  r1["A_66"]   / 1e6, r2["A_66"]   / 1e6)
row("D_11 (N.m)",   r1["D_11"],         r2["D_11"]        )
row("D_22 (N.m)",   r1["D_22"],         r2["D_22"]        )
row("D_66 (N.m)",   r1["D_66"],         r2["D_66"]        )
row("Ex_bar (GPa)", r1["Ex_bar"] / 1e9, r2["Ex_bar"] / 1e9)
row("Ex_fl  (GPa)", r1["Ex_fl"]  / 1e9, r2["Ex_fl"]  / 1e9)

end_results_file(results_file)
