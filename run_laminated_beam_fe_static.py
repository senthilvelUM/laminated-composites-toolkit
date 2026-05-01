"""Entry point for the static FE analysis of a laminated beam (2 DOFs/node:
v, phi -- bending only).  Uses the symmetric-laminate Euler-Bernoulli (CLT)
beam toolkit in fe_beams_clt/.  Suitable for symmetric stacks (B = 0)
under transverse load.
"""

import numpy as np
import matplotlib.pyplot as plt

from common import *
from laminate import *
from fe_beams_clt import *


results_file = start_results_file(__file__, "Beam FE Static Analysis (EB / CLT)")

# --- Define the laminate ---
N                = 4
ply_materials    = ["unidirectional_carbon_epoxy"] * N
ply_orientations = [45, 0, 0, 45]                       # bottom -> top
h                = 0.2e-3                                # ply thickness, m
ply_thicknesses  = [h] * N

check_laminate_inputs(N, ply_materials, ply_orientations, ply_thicknesses)
laminate = create_laminate(ply_materials, ply_orientations, ply_thicknesses)

# This 2-DOF beam runner requires a symmetric laminate (B = 0)
assert np.allclose(laminate["B"], 0.0, atol=1e-9), \
    "run_laminated_beam_fe_static.py requires a symmetric laminate (B = 0)"

display_laminate_properties(laminate, verbose=False)

# --- Beam cross-section ---
W          = 25e-3                          # beam width, m
H          = laminate["H"]                  # beam thickness, m
A_section  = W * H
I_section  = W * H**3 / 12
EI_section = laminate["Exfl"] * I_section   # bending rigidity

print("\nBeam cross-section:")
print_scalar(W * 1e3,    label="W (mm)        :")
print_scalar(H * 1e3,    label="H (mm)        :")
print_scalar(EI_section, label="EI (N.m^2)    :", precision=4)

# --- Mesh: 2-element cantilever, 1-based labels ---
ENODES = np.array([[1, 1, 2],
                   [2, 2, 3]])

NODALCOORDINATES = np.array([[1, 0.00, 0],
                             [2, 0.15, 0],
                             [3, 0.30, 0]], dtype=float)

ELEMENTS = int(ENODES[:, 0].max())
NODES    = int(ENODES[:, 1:].max())
NDOF     = 2                                 # DOFs per node: v, phi
GDOF     = NODES * NDOF

# Per-element bending rigidity (1-based; both elements share the same section)
EI = one_based([EI_section] * ELEMENTS)

# Boundary conditions: clamp nodes 1 and 3 (DOFs 1, 2 and 5, 6).  Generic
# DOF index for NDOF = 2: dof = (node - 1) * NDOF + k, k = 1 (v), 2 (phi).
EBCList = [1, 2, 5, 6]

D = np.zeros(GDOF + 1)   # global displacements (1-padded)
F = np.zeros(GDOF + 1)   # global nodal forces  (1-padded)
F[3] = -100.0            # transverse force at node 2 (v-DOF = 3)

EDOF = generate_edofs(ENODES, NDOF)
L    = element_lengths(ENODES, NODALCOORDINATES)
plot_beam_undeformed(ENODES, NODALCOORDINATES)

# --- Assemble [K], solve [K]{D} = {F} ---
ke = np.zeros((ELEMENTS + 1, 4, 4))
for n in range(1, ELEMENTS + 1):
    ke[n] = ke_beam(EI[n], L[n])

K = assemble(ke, GDOF, EDOF)
print_matrix(K, label="\nK =", width=14)

D, F = solve_global(K, D, F, EBCList)
print_column(D[1:], label="\nD =")
print_column(F[1:], label="\nF =", width=12)

# --- Element-level recovery and beam plots ---
d = np.zeros((ELEMENTS + 1, 4))
f = np.zeros((ELEMENTS + 1, 4))
for n in range(1, ELEMENTS + 1):
    d[n], f[n] = extract_element_nodal_values(n, ke, EDOF, D)

plot_beam_deflection      (ENODES, NODALCOORDINATES, D)
plot_beam_bending_moment  (ENODES, NODALCOORDINATES, EI, D)
plot_beam_shear_force     (ENODES, NODALCOORDINATES, EI, D)

# --- Beam curvature at a chosen x ---
# kappa_beam = v''(x); CLT curvature is kappa_CLT = -kappa_beam.
x_eval     = 0.1
kappa_beam = beam_curvature(ENODES, NODALCOORDINATES, D, x_eval)
print(f"\nx = {x_eval*1e3:6.1f} mm   kappa_beam = {kappa_beam:10.4f} 1/m")

# --- Through-thickness analysis at x_eval ---
# eps0 = 0 in the 2-DOF beam.  Lateral curvatures from M_y = M_xy = 0
# (which, for [B] = 0, gives kappa_y = (d12/d11) * kappa_x and similarly
# for kappa_xy):
d11 = laminate["d"][0, 0]
d12 = laminate["d"][0, 1]
d16 = laminate["d"][0, 2]

kappa_x_CLT = -kappa_beam
kappa_y     = (d12 / d11) * kappa_x_CLT
kappa_xy    = (d16 / d11) * kappa_x_CLT

print_scalar(kappa_x_CLT, label="  kappa_x_CLT (1/m):", precision=4)
print_scalar(kappa_y,     label="  kappa_y     (1/m):", precision=4)
print_scalar(kappa_xy,    label="  kappa_xy    (1/m):", precision=4)

Epsilon0 = np.zeros(3)
Kappa    = np.array([kappa_x_CLT, kappa_y, kappa_xy])

plot_variables = ["epsilon_x", "sigma_x", "Sf"]
plot_through_thickness_variations(laminate, Epsilon0, Kappa, plot_variables)

Sf_min, z_min, k_min = find_min_safety_factor(laminate, Epsilon0, Kappa)
print_scalar(Sf_min,              label="\nSf_min                       :")
print_scalar(k_min,                label="  Layer where Sf_min occurs k:", precision=0)
print_scalar(z_min*1e3,            label="  z (mm)                     :")
print_scalar(z_min/laminate["H"],  label="  z/H                        :")

save_all_figures(__file__, dpi=PLOT_SETTINGS["dpi"])
end_results_file(results_file)
show_figures()
