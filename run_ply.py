"""Entry point for single-ply analysis: build a ply, apply a stress
state, transform between (x, y) and (1, 2) frames, and evaluate the
Tsai-Wu safety factor.
"""

import numpy as np

from common import *
from ply import *


results_file = start_results_file(__file__, "Ply Analysis Results")

# --- Define the ply ---
material_name     = "unidirectional_carbon_epoxy"
theta             = 30                              # ply orientation, deg
h                 = 0.2e-3                          # ply thickness, m
failure_criterion = "TsaiWu"                        # "TsaiWu" | "MaxStress" | "Hashin"

ply = create_ply(material_name, theta, h)
display_ply_properties(ply)

# --- Apply stresses, compute strains, transform between frames ---
SigmaXY = np.array([225, 50, 50]) * 1e6             # applied stresses, Pa
print_column(SigmaXY / 1e6,  label="Stresses in the X-Y coordinate system (MPa):")

Sigma12   = ply["Ts"]   @ SigmaXY
EpsilonXY = ply["SBar"] @ SigmaXY
Epsilon12 = ply["Te"]   @ EpsilonXY

print_column(Sigma12 / 1e6,   label="Stresses in the 1-2 coordinate system (MPa):")
print_column(EpsilonXY * 1e6, label="Strains in the X-Y coordinate system (micro):")
print_column(Epsilon12 * 1e6, label="Strains in the 1-2 coordinate system (micro):")

# --- Failure analysis ---
ply_failure = get_failure_function(failure_criterion)
Sf = ply_failure(ply, Sigma12)
print(f"\nFailure criterion: {failure_criterion}")
print_scalar(Sf, label="Safety factor for actual stress state, Sf:")

# --- Off-axis engineering properties ---
plot_off_axis_properties(ply)

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
