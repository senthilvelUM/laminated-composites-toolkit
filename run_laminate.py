"""Entry point for laminate analysis: build a laminate from a stacking
sequence, apply force and moment resultants, evaluate strains, stresses,
and safety factor through the thickness, and identify the critical ply
under the chosen failure criterion.
"""

from common import *
from laminate import *
from ply import display_failure_mode, identify_failure_mode


results_file = start_results_file(__file__, "Laminate Analysis Results")

# --- Define the laminate ---
N                = 4
ply_materials    = ["unidirectional_carbon_epoxy"] * N
ply_orientations = [0, 90, 90, 0]                       # bottom -> top
h                = 0.2e-3                                # ply thickness, m
ply_thicknesses  = [h] * N
failure_criterion = "TsaiWu"                             # "TsaiWu" | "MaxStress" | "Hashin"

check_laminate_inputs(N, ply_materials, ply_orientations, ply_thicknesses)
laminate = create_laminate(ply_materials, ply_orientations, ply_thicknesses)
display_laminate_properties(laminate)

# Access an individual ply with: ply = get_ply(laminate, k)

# --- Applied force and moment resultants ---
Nx,  Ny,  Nxy = 0.0, 0.0, 0.0    # in-plane resultants, N/m
Mx,  My,  Mxy = 2.0, 0.0, 0.0    # moment resultants,  N

Epsilon0, Kappa = midsurface_strains_curvatures(laminate, Nx, Ny, Nxy, Mx, My, Mxy)
print_column(Epsilon0 * 1e6, label="Midsurface strains Epsilon0 (micro):")
print_column(Kappa,           label="Midsurface curvatures Kappa (1/m):")

# --- Strains, stresses and Sf at a specified z ---
z = 0.1e-3   # thickness coordinate, m
EpsilonXY, Epsilon12, SigmaXY, Sigma12, Sf = evaluate_strains_stresses_Sf(
    laminate, Epsilon0, Kappa, z, criterion=failure_criterion
)
print(f"\nQuantities at z = {z*1e3:.3f} mm (z/H = {z/laminate['H']:.3f}):")
print_column(EpsilonXY * 1e6, label="EpsilonXY (micro):")
print_column(SigmaXY  / 1e6,  label="SigmaXY   (MPa):")
print_column(Sigma12  / 1e6,  label="Sigma12   (MPa):")
print_scalar(Sf,              label="Sf:")

# --- Through-thickness plots ---
plot_variables = ["epsilon_x", "sigma_x", "tau_12", "Sf"]
plot_through_thickness_variations(
    laminate, Epsilon0, Kappa, plot_variables, criterion=failure_criterion
)

# --- Minimum Sf and the critical ply (FPF) ---
Sf_min, z_min, k_min = find_min_safety_factor(
    laminate, Epsilon0, Kappa, criterion=failure_criterion
)
print(f"\nFailure criterion: {failure_criterion}")
print_scalar(Sf_min,              label="Sf_min                       :")
print_scalar(k_min,                label="  Layer where Sf_min occurs k:", precision=0)
print_scalar(z_min*1e3,            label="  z (mm)                     :")
print_scalar(z_min/laminate["H"],  label="  z/H                        :")

# --- Dominant failure mode at the critical point ---
# Tsai-Wu is interaction-aware; identify_failure_mode reports the dominant
# decoupled max-stress mode for context.
_, _, _, Sigma12_min, _ = evaluate_strains_stresses_Sf(
    laminate, Epsilon0, Kappa, z_min, criterion=failure_criterion
)
critical_ply = laminate["plies"][k_min]
mode, SF_mode, mode_SFs = identify_failure_mode(critical_ply, Sigma12_min)
display_failure_mode(mode, SF_mode, mode_SFs)

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
