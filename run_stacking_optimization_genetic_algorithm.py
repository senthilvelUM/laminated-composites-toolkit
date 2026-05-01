"""Stacking-sequence optimisation by an integer-coded genetic algorithm.

Same problem as run_stacking_optimization_brute_force.py: maximise the
minimum first-ply Tsai-Wu safety factor over a discrete stacking
sequence.  At small N_plies the GA result matches the brute-force
optimum; at large N_plies the GA still runs in under a second on a
problem brute force can't touch.

Each design is encoded as an integer chromosome (gene = index into the
discrete angle set), so the GA respects the angle set without rounding.
The GA operators (random_individual, tournament_select,
one_point_crossover, mutate, evolve) live in the optimization/ package;
this runner only configures the problem and orchestrates the calls.
"""

import time

import numpy as np

from common import *
from laminate import *
from optimization import *
from ply import create_ply, display_failure_mode, identify_failure_mode


results_file = start_results_file(
    __file__, "Stacking-sequence optimisation -- integer-coded GA"
)

# --- Configuration ---
material  = "unidirectional_carbon_epoxy"
N_plies   = 8                                       # 12^8 ~ 4.3e8 (brute hopeless)
h_ply     = 0.125e-3                                # ply thickness, m
angle_set = [int(a) for a in range(0, 180, 15)]     # 0, 15, ..., 165 deg

Nx, Ny, Nxy = 500e3, 0.0, 100e3                     # in-plane resultants, N/m
Mx, My, Mxy =   0.0, 0.0,   0.0                     # moment resultants,  N

failure_criterion = "TsaiWu"                        # "TsaiWu" | "MaxStress" | "Hashin"

# --- GA hyperparameters (typical ranges in comments) ---
pop_size       = 30                # 20-200, ~5-10x chromosome length
n_generations  = 200               # raise if the convergence curve is still climbing
crossover_rate = 0.7               # 0.6-0.95
mutation_rate  = 1.0 / N_plies     # ~1 mutation per individual on average
tournament_k   = 3                 # 2-7; higher = stronger selection pressure
n_elite        = 2                 # 1-5% of pop_size; keeps best across generations
seed           = 0                 # RNG seed

# --- Ply cache + fitness function ---
ply_cache = {theta: create_ply(material, theta, h_ply) for theta in angle_set}
NM        = np.array([Nx, Ny, Nxy, Mx, My, Mxy])
n_alleles = len(angle_set)


def fitness(individual):
    """Decode an integer chromosome to ply angles and return Sf_min."""
    angles = [angle_set[g] for g in individual]
    return evaluate_stacking(angles, ply_cache, h_ply, NM,
                             criterion=failure_criterion)


# --- Report the problem ---
print("Problem setup")
print("-" * 60)
print(f"  Material        : {material}")
print(f"  N_plies         : {N_plies}")
print(f"  Ply thickness   : {h_ply*1e3:.3f} mm")
print(f"  Total thickness : {h_ply*N_plies*1e3:.3f} mm")
print(f"  Angle set       : {angle_set} deg ({n_alleles} values)")
print(f"  Loads (N/m)     : Nx={Nx/1e3:g} kN/m, Ny={Ny/1e3:g} kN/m, "
      f"Nxy={Nxy/1e3:g} kN/m")
print(f"  Loads (N)       : Mx={Mx:g}, My={My:g}, Mxy={Mxy:g}")

print("\nGA hyperparameters")
print("-" * 60)
print(f"  pop_size        : {pop_size}")
print(f"  n_generations   : {n_generations}")
print(f"  crossover_rate  : {crossover_rate}")
print(f"  mutation_rate   : {mutation_rate:.4f}")
print(f"  tournament_k    : {tournament_k}")
print(f"  n_elite         : {n_elite}")
print(f"  seed            : {seed}")

design_space_size = n_alleles ** N_plies
n_evals_GA        = pop_size * (n_generations + 1)
print(f"\n  Design space    : 12^{N_plies} = {design_space_size:,d} stackings")
print(f"  GA evaluations  : pop_size x (n_generations+1) = {n_evals_GA:,d}")
print(f"  Coverage        : {n_evals_GA / design_space_size * 100:.3g}% of design space\n")

# --- Run the GA ---
rng = np.random.default_rng(seed)
t0  = time.perf_counter()
best_indiv, best_Sf, history = evolve(
    fitness,
    N_plies        = N_plies,
    n_alleles      = n_alleles,
    pop_size       = pop_size,
    n_generations  = n_generations,
    crossover_rate = crossover_rate,
    mutation_rate  = mutation_rate,
    tournament_k   = tournament_k,
    n_elite        = n_elite,
    rng            = rng,
)
elapsed     = time.perf_counter() - t0
best_angles = [angle_set[g] for g in best_indiv]

print("Optimisation summary")
print("-" * 60)
print(f"  Wall time    : {elapsed:.2f} s")
print(f"  Eval rate    : {n_evals_GA/elapsed:,.0f} laminates/s\n")
print(f"Best stacking sequence (max-min {failure_criterion} Sf):")
print(f"  Angles (deg) : {best_angles}")
print_scalar(best_Sf, label="  Sf_min       :")

# --- Ground-truth check (only feasible at small N_plies) ---
if N_plies <= 5:
    print("\nValidation: brute-force enumeration of the design space ...")
    t0 = time.perf_counter()
    brute_best_angles, brute_best_Sf, _ = brute_force_search(
        angle_set, N_plies, ply_cache, h_ply, NM, criterion=failure_criterion
    )
    brute_elapsed = time.perf_counter() - t0
    gap = (brute_best_Sf - best_Sf) / brute_best_Sf * 100
    print(f"  Brute-force time  : {brute_elapsed:.2f} s "
          f"({design_space_size:,d} evaluations)")
    print(f"  Brute-force angles: {brute_best_angles}")
    print(f"  Brute-force Sf    : {brute_best_Sf:.6f}")
    print(f"  GA Sf             : {best_Sf:.6f}")
    print(f"  Gap (brute - GA) / brute = {gap:.4g}%")
else:
    print(f"\nN_plies = {N_plies} -> brute force is hopeless "
          f"({design_space_size:,d} stackings); skipping ground-truth check.")

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

# --- Plots: GA convergence and through-thickness profiles ---
plot_GA_convergence(history, N_plies, pop_size)
plot_through_thickness_variations(
    best_lam, best_eps0, best_kap,
    ["sigma_x", "sigma_y", "tau_xy", "Sf"],
    criterion=failure_criterion,
)

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
