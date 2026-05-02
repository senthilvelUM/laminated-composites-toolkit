"""Example 4.1 -- Stress distribution through the thickness of a [45/0/-45]
three-ply IM7/8552 carbon/epoxy laminate (h = 0.2 mm per ply, H = 0.6 mm)
under prescribed mid-surface strain and curvature

    Epsilon0 = [1.0e-3, 0, 0],   Kappa = [1.0 1/m, 0, 0].

Strain is linear and continuous through the thickness; stress is
piecewise linear with discontinuous jumps at every ply interface.
"""

#  Make the project root importable when invoked from the project root.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import numpy as np

from common import *
from laminate import *


results_file = start_results_file(
    __file__,
    "Example 4.1 -- Stress distribution through the thickness of a [45/0/-45] laminate",
)

# --- Define the laminate ---
N = 3
ply_materials    = ["unidirectional_carbon_epoxy"] * N
ply_orientations = [45, 0, -45]                      # bottom -> top
h = 0.2e-3                                            # ply thickness, m
ply_thicknesses  = [h] * N

check_laminate_inputs(N, ply_materials, ply_orientations, ply_thicknesses)
laminate = create_laminate(ply_materials, ply_orientations, ply_thicknesses)

print(f"Laminate H = {laminate['H']*1e3:.3f} mm  ({N} plies of {h*1e3:.3f} mm)")
print(f"Stacking sequence (bottom -> top, deg): {ply_orientations}")

# --- Prescribed mid-surface kinematics ---
Epsilon0 = np.array([1.0e-3, 0.0, 0.0])
Kappa    = np.array([1.0,    0.0, 0.0])

print_column(Epsilon0 * 1e6, label="\nEpsilon0 (micro-strain):")
print_column(Kappa,           label="Kappa    (1/m)         :")

# --- Strain and stress at the top and bottom of each ply ---
print("\nStrain and stress at each ply boundary:")
eps = 1e-12   # tiny inward offset so the queried z lands inside the ply
for k in range(1, laminate["N"] + 1):
    theta = laminate["plies"][k]["theta"]
    z_bot = laminate["z"][k-1]
    z_top = laminate["z"][k]
    for label, z in [("bottom", z_bot + eps), ("top   ", z_top - eps)]:
        EpsXY, _, SigXY, _, _ = evaluate_strains_stresses_Sf(
            laminate, Epsilon0, Kappa, z
        )
        z_print = z_bot if label == "bottom" else z_top
        print(f"\nPly {k} (theta = {theta:+.0f} deg), {label}:  z = {z_print*1e3:+.3f} mm")
        print_scalar(EpsXY[0] * 1e6, label="  eps_x   (micro):")
        print_scalar(SigXY[0] / 1e6, label="  sigma_x (MPa)  :")
        print_scalar(SigXY[1] / 1e6, label="  sigma_y (MPa)  :")
        print_scalar(SigXY[2] / 1e6, label="  tau_xy  (MPa)  :")

# --- Through-thickness plots in laminate (x,y) and material (1,2) frames ---
plot_variables = ["epsilon_x",
                  "sigma_x", "sigma_y", "tau_xy",
                  "sigma_1", "sigma_2", "tau_12"]
plot_through_thickness_variations(laminate, Epsilon0, Kappa, plot_variables)

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
