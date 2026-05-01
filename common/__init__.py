"""Shared infrastructure for the LaminateX toolkits.

Contents:
  * Display helpers: print_scalar, print_column, print_matrix
  * Output capture: start_results_file, end_results_file, save_all_figures, show_figures
  * Mesh + BC helpers (rectangular plate): generate_rectangular_mesh, simply_supported_bcs_plate, clamped_bcs_plate
  * Generic FE machinery: assemble, generate_edofs, extract_element_nodal_values, solve_global, solve_global_eigen
  * Misc utilities: one_based, Tee
"""

# --- generic FE machinery (toolkit-agnostic) ---
from common.assemble import assemble
from common.extract_element_nodal_values import extract_element_nodal_values
from common.generate_edofs import generate_edofs
from common.solve_global import solve_global
from common.solve_global_eigen import solve_global_eigen

# --- 1D-element (beam) mesh helpers ---
from common.element_lengths import element_lengths
from common.element_lengths_orientations import element_lengths_orientations
from common.which_element import which_element

# --- 2D rectangular-plate mesh + BC helpers ---
from common.fe_mesh_helpers import (
    generate_rectangular_mesh,
    simply_supported_bcs_plate,
    clamped_bcs_plate,
)

# --- display helpers ---
from common.print_column import print_column
from common.print_matrix import print_matrix
from common.print_scalar import print_scalar

# --- output capture ---
from common.results_file import start_results_file, end_results_file
from common.save_all_figures import save_all_figures
from common.show_figures import show_figures

# --- misc utilities ---
from common.one_based import one_based
from common.tee import Tee


__all__ = [
    # generic FE machinery
    "assemble",
    "extract_element_nodal_values",
    "generate_edofs",
    "solve_global",
    "solve_global_eigen",
    # 1D-element (beam) mesh helpers
    "element_lengths",
    "element_lengths_orientations",
    "which_element",
    # 2D rectangular-plate mesh + BC helpers
    "generate_rectangular_mesh",
    "simply_supported_bcs_plate",
    "clamped_bcs_plate",
    # display
    "print_column",
    "print_matrix",
    "print_scalar",
    # output capture
    "start_results_file",
    "end_results_file",
    "save_all_figures",
    "show_figures",
    # misc
    "one_based",
    "Tee",
]
