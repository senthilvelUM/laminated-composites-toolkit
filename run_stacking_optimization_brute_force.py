"""Stacking-sequence optimisation by exhaustive enumeration.

Searches every stacking sequence on the discrete angle set
{0, 15, ..., 165} deg and returns the one that maximises the minimum
first-ply safety factor.  Guarantees the global optimum but the cost
scales as 12^N; the runner prints a 12^N table at the top so the
combinatorial blow-up is visible.

Pair this runner with run_stacking_optimization_genetic_algorithm.py,
which converges to the same optimum at large N in a tiny fraction of
the evaluations.  The fast min-Sf evaluator and the enumeration loop
live in the optimization/ package; this runner only configures the
problem and orchestrates the calls.
"""

import time

import numpy as np

from common import *
from laminate import *
from optimization import *
from ply import create_ply, display_failure_mode, identify_failure_mode


results_file = start_results_file(
    __file__, "Stacking-sequence optimisation -- exhaustive enumeration"
)

# --- Configuration ---
material  = "unidirectional_carbon_epoxy"
N_plies   = 4                                       # 12^4 = 20,736 evals
h_ply     = 0.125e-3                                # ply thickness, m
angle_set = [int(a) for a in range(0, 180, 15)]     # 0, 15, ..., 165 deg

Nx, Ny, Nxy = 500e3, 0.0, 100e3                     # in-plane resultants, N/m
Mx, My, Mxy =   0.0, 0.0,   0.0                     # moment resultants,  N

failure_criterion = "TsaiWu"                        # "TsaiWu" | "MaxStress" | "Hashin"

# --- Ply cache: one create_ply per candidate angle ---
ply_cache = {theta: create_ply(material, theta, h_ply) for theta in angle_set}
NM        = np.array([Nx, Ny, Nxy, Mx, My, Mxy])

# --- Report the problem ---
print("Problem setup")
print("-" * 60)
print(f"  Material        : {material}")
print(f"  N_plies         : {N_plies}")
print(f"  Ply thickness   : {h_ply*1e3:.3f} mm")
print(f"  Total thickness : {h_ply*N_plies*1e3:.3f} mm")
print(f"  Angle set       : {angle_set} deg ({len(angle_set)} values)")
print(f"  Loads (N/m)     : Nx={Nx/1e3:g} kN/m, Ny={Ny/1e3:g} kN/m, "
      f"Nxy={Nxy/1e3:g} kN/m")
print(f"  Loads (N)       : Mx={Mx:g}, My={My:g}, Mxy={Mxy:g}")

print("\n12^N scaling of the design space:")
print("-" * 60)
for n in range(2, 9):
    note = "  <-- this run" if n == N_plies else ""
    print(f"  N = {n}:  {len(angle_set)**n:>15,d} stacking sequences{note}")

n_total = len(angle_set) ** N_plies
print(f"\nThis run evaluates all {n_total:,d} sequences.\n")

# --- Exhaustive search ---
t0 = time.perf_counter()
best_angles, best_Sf, all_Sf = brute_force_search(
    angle_set, N_plies, ply_cache, h_ply, NM, criterion=failure_criterion
)
elapsed = time.perf_counter() - t0

# --- Report the best stacking ---
print("Optimisation summary")
print("-" * 60)
print(f"  Evaluations  : {n_total:,d}")
print(f"  Wall time    : {elapsed:.2f} s")
print(f"  Eval rate    : {n_total/elapsed:,.0f} laminates/s\n")
print(f"Best stacking sequence (max-min {failure_criterion} Sf):")
print(f"  Angles (deg) : {best_angles}")
print_scalar(best_Sf, label="  Sf_min       :")

# Reference stacks for context
print("\nReference stacks under the same loads:")
ref_stacks = {
    "[0]_n":           [0]   * N_plies,
    "[90]_n":          [90]  * N_plies,
    "[0,90]_(n/2)":    ([0, 90]   * (N_plies // 2 + 1))[:N_plies],
    "[+45,-45]_(n/2)": ([45, 135] * (N_plies // 2 + 1))[:N_plies],
}
for name, angles in ref_stacks.items():
    Sf = evaluate_stacking(angles, ply_cache, h_ply, NM, criterion=failure_criterion)
    print(f"  {name:<18s} {angles} -> Sf_min = {Sf:.4f}")

# --- Build the optimum laminate for reporting + plotting ---
best_lam = create_laminate([material]*N_plies, best_angles, [h_ply]*N_plies)
best_eps0, best_kap = midsurface_strains_curvatures(
    best_lam, Nx, Ny, Nxy, Mx, My, Mxy
)
print("\n" + "=" * 60)
print("Properties of the optimum laminate")
print("=" * 60)
display_laminate_properties(best_lam, verbose=False)

# Pinpoint Sf_min through the thickness, identify the dominant mode
Sf_min, z_min, k_min = find_min_safety_factor(
    best_lam, best_eps0, best_kap, criterion=failure_criterion
)
print(f"\nFailure criterion: {failure_criterion}")
print_scalar(Sf_min,              label="Sf_min                       :")
print_scalar(k_min,                label="  Layer where Sf_min occurs k:", precision=0)
print_scalar(z_min*1e3,            label="  z (mm)                     :")
print_scalar(z_min/best_lam["H"],  label="  z/H                        :")

_, _, _, Sigma12_min, _ = evaluate_strains_stresses_Sf(
    best_lam, best_eps0, best_kap, z_min, criterion=failure_criterion
)
critical_ply = best_lam["plies"][k_min]
mode, SF_mode, mode_SFs = identify_failure_mode(critical_ply, Sigma12_min)
display_failure_mode(mode, SF_mode, mode_SFs)

plot_through_thickness_variations(
    best_lam, best_eps0, best_kap,
    ["sigma_x", "sigma_y", "tau_xy", "Sf"],
    criterion=failure_criterion,
)
plot_Sf_histogram(all_Sf, best_Sf, N_plies)

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
