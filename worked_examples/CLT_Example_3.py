"""Example 4.3 -- Design of a thin-walled [theta/-theta]_S laminated tube
under combined axial force and torque.

Tube of mean radius R = 50 mm, length L = 0.5 m, four-ply IM7/8552 wall
(h = 0.2 mm per ply, H = 0.8 mm), loaded by P = 30 kN axial + T = 1.6 kN.m
torque.  The fiber angle theta is the design variable.

The script:
  1. Walks through theta = 45 deg in detail (resultants, mid-surface
     strains, ply stresses in laminate and material frames, Tsai-Wu Sf,
     and through-thickness plots).
  2. Compares Sf_min across four candidate angles (15, 30, 45, 60 deg).
  3. Sweeps theta over [0, 90] deg and plots Sf_min vs theta.
"""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt

from common import *
from laminate import *


results_file = start_results_file(
    __file__,
    "Example 4.3 -- Design of a thin-walled [theta/-theta]_S laminated tube",
)

# --- Tube geometry and applied loads ---
R = 0.050    # mean radius, m
L = 0.500    # length,      m
P = 30.0e3   # axial force, N
T =  1.6e3   # torque,      N.m

material = "unidirectional_carbon_epoxy"   # IM7/8552
h        = 0.2e-3                           # ply thickness, m
N_plies  = 4                                # [theta/-theta]_S => 4 plies

# --- Force and moment resultants on a tube wall element ---
Nx  = P / (2 * np.pi * R)
Nxy = T / (2 * np.pi * R**2)
Ny  = 0.0
Mx  = My = Mxy = 0.0

print("\nTube geometry and loading:")
print_scalar(R*1e3,  label="R  (mm)   :")
print_scalar(L,      label="L  (m)    :")
print_scalar(P*1e-3, label="P  (kN)   :")
print_scalar(T*1e-3, label="T  (kN.m) :")

print("\nForce/moment resultants on a wall element:")
print_scalar(Nx *1e-3, label="Nx  (kN/m) :")
print_scalar(Ny *1e-3, label="Ny  (kN/m) :")
print_scalar(Nxy*1e-3, label="Nxy (kN/m) :")
print(f"\nNxy / Nx = {Nxy/Nx:.3f}  (torsion-biased: Nxy > Nx)")


def build_tube_laminate(theta):
    """Build a four-ply [+theta/-theta]_S laminate."""
    return create_laminate(
        [material] * N_plies,
        [+theta, -theta, -theta, +theta],   # bottom -> top
        [h] * N_plies,
    )


# === Part 1 -- detailed walkthrough at theta = 45 deg ===
print("\n" + "=" * 60)
print("Part 1 -- Detailed walkthrough at theta = 45 deg")
print("=" * 60)

laminate = build_tube_laminate(45.0)
display_laminate_properties(laminate)

Epsilon0, Kappa = midsurface_strains_curvatures(laminate, Nx, Ny, Nxy, Mx, My, Mxy)

print("\nMid-surface strains and curvatures:")
print_column(Epsilon0 * 1e6, label="Epsilon0 (micro):")
print_column(Kappa,           label="Kappa    (1/m)  :")

print("\nPly-by-ply stresses and Tsai-Wu safety factor:")
for k in range(1, laminate["N"] + 1):
    z_mid   = 0.5 * (laminate["z"][k-1] + laminate["z"][k])
    theta_k = laminate["plies"][k]["theta"]
    _, _, SigXY, Sig12, Sf = evaluate_strains_stresses_Sf(
        laminate, Epsilon0, Kappa, z_mid
    )
    print(f"\nPly {k} (theta = {theta_k:+.0f} deg) at z = {z_mid*1e3:+.3f} mm:")
    print_scalar(SigXY[0] / 1e6, label="  sigma_x (MPa) :")
    print_scalar(SigXY[1] / 1e6, label="  sigma_y (MPa) :")
    print_scalar(SigXY[2] / 1e6, label="  tau_xy  (MPa) :")
    print_scalar(Sig12[0] / 1e6, label="  sigma_1 (MPa) :")
    print_scalar(Sig12[1] / 1e6, label="  sigma_2 (MPa) :")
    print_scalar(Sig12[2] / 1e6, label="  tau_12  (MPa) :")
    print_scalar(Sf,             label="  Sf (Tsai-Wu)  :")

Sf_min, z_min, k_min = find_min_safety_factor(laminate, Epsilon0, Kappa)
theta_critical = laminate["plies"][k_min]["theta"]
print(f"\nFirst-ply failure (Tsai-Wu):")
print_scalar(Sf_min,    label="  Sf_min            :")
print_scalar(k_min,     label="  Critical ply k    :", precision=0)
print(f"  Critical ply theta: {theta_critical:+.0f} deg")
print_scalar(z_min*1e3, label="  z at Sf_min (mm)  :")

plot_through_thickness_variations(
    laminate, Epsilon0, Kappa,
    ["epsilon_x", "sigma_x", "sigma_y", "tau_xy",
     "sigma_1",   "sigma_2", "tau_12",  "Sf"],
)


# === Part 2 -- comparison across four candidate angles ===
print("\n" + "=" * 60)
print("Part 2 -- Comparison across candidate angles")
print("=" * 60)

candidate_angles = [15.0, 30.0, 45.0, 60.0]
table_rows = []
for theta in candidate_angles:
    lam       = build_tube_laminate(theta)
    eps0, kap = midsurface_strains_curvatures(lam, Nx, Ny, Nxy, Mx, My, Mxy)
    Sf_min_t, _, k_min_t = find_min_safety_factor(lam, eps0, kap)
    z_mid = 0.5 * (lam["z"][k_min_t-1] + lam["z"][k_min_t])
    _, _, _, Sig12, _ = evaluate_strains_stresses_Sf(lam, eps0, kap, z_mid)
    table_rows.append({
        "theta":      theta,
        "eps0_x":     eps0[0],
        "gamma0_xy":  eps0[2],
        "sigma_1":    Sig12[0],
        "sigma_2":    Sig12[1],
        "tau_12":     Sig12[2],
        "Sf_min":     Sf_min_t,
        "theta_crit": lam["plies"][k_min_t]["theta"],
    })

print()
print(f"{'theta':>6}  {'eps_x^0':>10}  {'gamma_xy^0':>11}  "
      f"{'sigma_1':>10}  {'sigma_2':>9}  {'tau_12':>9}  {'Sf_min':>8}  {'crit ply':>10}")
print(f"{'(deg)':>6}  {'(micro)':>10}  {'(micro)':>11}  "
      f"{'(MPa)':>10}  {'(MPa)':>9}  {'(MPa)':>9}  {'-':>8}  {'theta':>10}")
print("-" * 95)
for r in table_rows:
    print(f"{r['theta']:>6.0f}  "
          f"{r['eps0_x']*1e6:>10.0f}  "
          f"{r['gamma0_xy']*1e6:>11.0f}  "
          f"{r['sigma_1']/1e6:>10.2f}  "
          f"{r['sigma_2']/1e6:>9.2f}  "
          f"{r['tau_12']/1e6:>9.2f}  "
          f"{r['Sf_min']:>8.3f}  "
          f"{r['theta_crit']:>+10.0f}")

best  = max(table_rows, key=lambda r: r["Sf_min"])
worst = min(table_rows, key=lambda r: r["Sf_min"])
print(f"\nBest  candidate: theta = {best['theta']:.0f} deg, Sf_min = {best['Sf_min']:.3f}")
note = "  (FAILS: Sf_min < 1)" if worst["Sf_min"] < 1.0 else ""
print(f"Worst candidate: theta = {worst['theta']:.0f} deg, Sf_min = {worst['Sf_min']:.3f}" + note)


# === Part 3 -- continuous angle sweep ===
print("\n" + "=" * 60)
print("Part 3 -- Continuous sweep of theta over [0, 90] deg")
print("=" * 60)

theta_sweep = np.arange(0.0, 90.5, 1.0)
Sf_sweep    = np.zeros_like(theta_sweep)
for i, theta in enumerate(theta_sweep):
    lam       = build_tube_laminate(theta)
    eps0, kap = midsurface_strains_curvatures(lam, Nx, Ny, Nxy, Mx, My, Mxy)
    Sf_sweep[i], _, _ = find_min_safety_factor(lam, eps0, kap)

i_opt     = int(np.argmax(Sf_sweep))
theta_opt = theta_sweep[i_opt]
Sf_opt    = Sf_sweep[i_opt]

print(f"\nContinuous optimum: theta = {theta_opt:.0f} deg, Sf_min = {Sf_opt:.3f}")
print(f"(Best of the four candidates: theta = {best['theta']:.0f} deg, "
      f"Sf_min = {best['Sf_min']:.3f})")

# --- Plot Sf_min vs theta with candidate angles + continuous optimum ---
fig, ax = plt.subplots(figsize=(7.0, 4.5))
ax.plot(theta_sweep, Sf_sweep, "-", linewidth=1.8,
        label=r"$S_f^{\mathrm{min}}(\theta)$")
ax.axhline(1.0, linestyle="--", color="gray", linewidth=1.0,
           label=r"$S_f = 1$ (failure threshold)")

candidate_Sf = [r["Sf_min"] for r in table_rows]
ax.plot(candidate_angles, candidate_Sf, "o", markersize=8, color="C1",
        label="Four candidate angles")
for theta, sf in zip(candidate_angles, candidate_Sf):
    ax.annotate(f"  {theta:.0f}", (theta, sf),
                textcoords="offset points", xytext=(8, -2), fontsize=9)

ax.plot([theta_opt], [Sf_opt], "*", markersize=14, color="C2",
        label=f"Continuous optimum (theta = {theta_opt:.0f} deg)")

ax.set_xlabel(r"Fiber angle $\theta$ (deg)")
ax.set_ylabel(r"Minimum safety factor $S_f^{\mathrm{min}}$ (Tsai-Wu)")
ax.set_xlim(0, 90)
ax.set_xticks(np.arange(0, 91, 15))
ax.set_ylim(bottom=0.0)
ax.grid(True, alpha=0.3)
ax.legend(loc="best", fontsize=9)
ax.set_title(r"$[\theta/-\theta]_S$ tube: $S_f^{\mathrm{min}}$ vs fiber angle"
             "\nunder $P = 30$ kN, $T = 1.6$ kN$\\cdot$m")
fig.tight_layout()

save_all_figures(__file__)
end_results_file(results_file)
show_figures()
