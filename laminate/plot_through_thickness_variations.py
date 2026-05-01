"""Plot through-thickness variations of strains, stresses, and safety factors."""

import matplotlib.pyplot as plt
import numpy as np

from laminate.evaluate_strains_stresses_Sf import evaluate_strains_stresses_Sf


# ---------------------------------------------------------------------------
# User-configurable plot settings. Edit these to change the look of the plots.
# ---------------------------------------------------------------------------

PLOT_SETTINGS = {
    "font_size":            16,                        # Font size for axis labels and ticks
    "line_width":           3.0,                       # Thickness of the data curve
    "line_color":           "tab:orange",                # Data curve color (matplotlib name)
    "interface_color":      (0.40, 0.40, 0.40),        # Color of the ply-interface lines
    "interface_line_width": 1.0,                       # Thickness of the ply-interface lines
    "interface_alpha":      0.7,                       # Opacity of the ply-interface lines (0 transparent, 1 opaque)
    "midsurface_color":     (0.50, 0.50, 0.50),        # Color of the midsurface (z/H = 0) line
    "midsurface_line_width":0.75,                       # Thickness of the midsurface line
    "midsurface_dashes":    (12, 8),                    # Dash pattern for the midsurface line (on, off) in points
    "midsurface_alpha":     0.5,                       # Opacity of the midsurface line (0 transparent, 1 opaque)
    "show_midsurface":      True,                      # Draw the dashed midsurface line at z/H = 0?
                                                       #   Auto-suppressed when z = 0 coincides with a ply
                                                       #   interface (every even-N laminate), so set this False
                                                       #   only if you want to hide it for odd-N stacks too.
    "vertical_axis_color":  (0.20, 0.20, 0.20),        # Color of the vertical axis (x = 0) line
    "axes_line_width":      0.7,                       # Thickness of the vertical x = 0 reference line
    "points_per_layer":     10,                        # Sample points per ply for strain/stress plots
    "points_per_layer_Sf":  500,                       # Sample points per ply for safety-factor plots
    "figure_size_single":   (7, 5),                    # Size (in inches) of each plot
    "save_dpi":             300,                       # Resolution of saved PNG files
}


# Strain component metadata: component key -> (coord_system, index, xlabel, short_name)
_STRAIN_COMPONENTS = {
    "epsilon_x": ("XY", 0, r"Normal strain $\varepsilon_x$ ($\mu$)",    "epsilon_x"),
    "epsilon_y": ("XY", 1, r"Normal strain $\varepsilon_y$ ($\mu$)",    "epsilon_y"),
    "gamma_xy":  ("XY", 2, r"Shear strain $\gamma_{xy}$ ($\mu$rad)",    "gamma_xy"),
    "epsilon_1": ("12", 0, r"Normal strain $\varepsilon_1$ ($\mu$)",    "epsilon_1"),
    "epsilon_2": ("12", 1, r"Normal strain $\varepsilon_2$ ($\mu$)",    "epsilon_2"),
    "gamma_12":  ("12", 2, r"Shear strain $\gamma_{12}$ ($\mu$rad)",    "gamma_12"),
}

# Stress component metadata: component key -> (coord_system, index, xlabel, short_name)
_STRESS_COMPONENTS = {
    "sigma_x": ("XY", 0, r"Normal stress $\sigma_x$ (MPa)",  "sigma_x"),
    "sigma_y": ("XY", 1, r"Normal stress $\sigma_y$ (MPa)",  "sigma_y"),
    "tau_xy":  ("XY", 2, r"Shear stress $\tau_{xy}$ (MPa)",  "tau_xy"),
    "sigma_1": ("12", 0, r"Normal stress $\sigma_1$ (MPa)",  "sigma_1"),
    "sigma_2": ("12", 1, r"Normal stress $\sigma_2$ (MPa)",  "sigma_2"),
    "tau_12":  ("12", 2, r"Shear stress $\tau_{12}$ (MPa)",  "tau_12"),
}

# Small offset to avoid interface-ambiguity at the layer boundaries when sampling
_EPS = 1e-12

# Display string for each supported failure criterion (used in the Sf axis label)
_CRITERION_LABEL = {
    "TsaiWu":    "Tsai-Wu",
    "MaxStress": "Max-stress",
    "Hashin":    "Hashin",
}


def plot_through_thickness_variations(laminate, Epsilon0, Kappa, plot_variables,
                                       criterion="TsaiWu"):
    """Plot the through-thickness variation of selected quantities.

    For each entry in plot_variables, creates one figure with the
    quantity on the horizontal axis and z/H on the vertical axis.

    Parameters
    ----------
    laminate : dict
        Laminate dictionary created by create_laminate().
    Epsilon0 : np.ndarray
        Midsurface strains [eps0_x, eps0_y, gamma0_xy] (shape (3,)).
    Kappa : np.ndarray
        Midsurface curvatures [kappa_x, kappa_y, kappa_xy] (shape (3,)).
    plot_variables : list of str
        Each entry is one of:
            strains (x-y):   "epsilon_x", "epsilon_y", "gamma_xy"
            strains (1-2):   "epsilon_1", "epsilon_2", "gamma_12"
            stresses (x-y):  "sigma_x",   "sigma_y",   "tau_xy"
            stresses (1-2):  "sigma_1",   "sigma_2",   "tau_12"
            safety factor:   "Sf"
    criterion : str, optional
        Failure-criterion name passed to ``get_failure_function``;
        ``"TsaiWu"`` (default), ``"MaxStress"``, or ``"Hashin"``.
        Affects the Sf plot and its axis label.
    """
    # Apply user font-size setting to all plotting below
    with plt.rc_context({"font.size": PLOT_SETTINGS["font_size"]}):

        for var in plot_variables:
            if var in _STRAIN_COMPONENTS:
                _plot_strain(laminate, Epsilon0, Kappa, var, criterion)
            elif var in _STRESS_COMPONENTS:
                _plot_stress(laminate, Epsilon0, Kappa, var, criterion)
            elif var == "Sf":
                _plot_Sf(laminate, Epsilon0, Kappa, criterion)
            else:
                raise ValueError(
                    f"Unknown plot variable: '{var}'. "
                    f"Supported: {list(_STRAIN_COMPONENTS)} + "
                    f"{list(_STRESS_COMPONENTS)} + ['Sf']."
                )

    # Note: this function intentionally does NOT call show_figures().
    # The canonical runner pattern is plot -> save -> show, where the
    # runner itself calls save_all_figures() and show_figures() after
    # this function returns.  Calling show_figures() here would block
    # interactive backends and detach the figures before the runner
    # gets a chance to save (and before it can apply post-hoc
    # adjustments like axis-range overrides).


# ---------------------------------------------------------------------------
# Private helpers: one per plot family (strain / stress / Sf)
# ---------------------------------------------------------------------------

def _plot_strain(laminate, Epsilon0, Kappa, component_str, criterion):
    """Plot the through-thickness variation of a single strain component."""
    coord, comp, xlabel, short_name = _STRAIN_COMPONENTS[component_str]

    fig, ax = plt.subplots(figsize=PLOT_SETTINGS["figure_size_single"])
    N_pts = PLOT_SETTINGS["points_per_layer"]

    for k in range(1, laminate["N"] + 1):
        zloc = np.linspace(
            laminate["z"][k-1] + _EPS, laminate["z"][k] - _EPS, N_pts
        )
        strain = np.zeros(N_pts)
        for n in range(N_pts):
            EpsXY, Eps12, _, _, _ = evaluate_strains_stresses_Sf(
                laminate, Epsilon0, Kappa, zloc[n], criterion=criterion
            )
            strain[n] = EpsXY[comp] if coord == "XY" else Eps12[comp]

        ax.plot(strain / 1e-6, zloc / laminate["H"],
                color=PLOT_SETTINGS["line_color"],
                linewidth=PLOT_SETTINGS["line_width"],
                solid_capstyle="round")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$z/H$")
    _format_laminate_plot(ax, laminate)
    fig.tight_layout()
    # Reserve extra top margin so the plot isn't pinned under the window chrome
    fig.subplots_adjust(top=0.92)

def _plot_stress(laminate, Epsilon0, Kappa, component_str, criterion):
    """Plot the through-thickness variation of a single stress component."""
    coord, comp, xlabel, short_name = _STRESS_COMPONENTS[component_str]

    fig, ax = plt.subplots(figsize=PLOT_SETTINGS["figure_size_single"])
    N_pts = PLOT_SETTINGS["points_per_layer"]

    for k in range(1, laminate["N"] + 1):
        zloc = np.linspace(
            laminate["z"][k-1] + _EPS, laminate["z"][k] - _EPS, N_pts
        )
        stress = np.zeros(N_pts)
        for n in range(N_pts):
            _, _, SigXY, Sig12, _ = evaluate_strains_stresses_Sf(
                laminate, Epsilon0, Kappa, zloc[n], criterion=criterion
            )
            stress[n] = SigXY[comp] if coord == "XY" else Sig12[comp]

        ax.plot(stress / 1e6, zloc / laminate["H"],
                color=PLOT_SETTINGS["line_color"],
                linewidth=PLOT_SETTINGS["line_width"],
                solid_capstyle="round")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$z/H$")
    _format_laminate_plot(ax, laminate)
    fig.tight_layout()
    # Reserve extra top margin so the plot isn't pinned under the window chrome
    fig.subplots_adjust(top=0.92)

def _plot_Sf(laminate, Epsilon0, Kappa, criterion):
    """Plot Sf through-thickness."""
    fig, ax = plt.subplots(figsize=PLOT_SETTINGS["figure_size_single"])
    N_pts = PLOT_SETTINGS["points_per_layer_Sf"]

    Sf_min = np.inf
    Sf_max = 0.0
    z_min = None
    k_min = None

    for k in range(1, laminate["N"] + 1):
        zloc = np.linspace(
            laminate["z"][k-1] + _EPS, laminate["z"][k] - _EPS, N_pts
        )
        Sf_values = np.zeros(N_pts)
        for n in range(N_pts):
            _, _, _, _, Sf = evaluate_strains_stresses_Sf(
                laminate, Epsilon0, Kappa, zloc[n], criterion=criterion
            )
            Sf_values[n] = Sf
            if Sf < Sf_min:
                Sf_min, z_min, k_min = Sf, zloc[n], k
            if Sf > Sf_max:
                Sf_max = Sf

        ax.plot(Sf_values, zloc / laminate["H"],
                color=PLOT_SETTINGS["line_color"],
                linewidth=PLOT_SETTINGS["line_width"],
                solid_capstyle="round")

    # Cap the horizontal range if Sf varies wildly across the laminate
    if Sf_max / Sf_min > 100:
        ax.set_xlim(0, 100 * Sf_min)

    ax.set_xlabel(rf"{_CRITERION_LABEL[criterion]} safety factor $S_{{fa}}$")
    ax.set_ylabel(r"$z/H$")
    _format_laminate_plot(ax, laminate)
    fig.tight_layout()
    # Reserve extra top margin so the plot isn't pinned under the window chrome
    fig.subplots_adjust(top=0.92)

def _format_laminate_plot(ax, laminate):
    """Apply the shared through-thickness plot formatting to one axes."""
    # Snapshot the current x-limits so the reference lines don't stretch them
    xlim = ax.get_xlim()

    # Dashed midsurface line at z/H = 0.  Use an explicit long-dash
    # pattern so the midsurface is unambiguously distinguishable from
    # the solid ply-interface lines, even at the thin reference-line
    # width used here.  Skip the line entirely when the user has
    # disabled it via PLOT_SETTINGS, OR when z = 0 coincides with a
    # ply interface (every even-N laminate) -- otherwise the dashed
    # line lies on top of a solid interface line and reads as a
    # mysterious third feature instead of a kinematic reference.
    if PLOT_SETTINGS["show_midsurface"] and not _midsurface_at_interface(laminate):
        ax.axhline(0,
                   color=PLOT_SETTINGS["midsurface_color"],
                   linewidth=PLOT_SETTINGS["midsurface_line_width"],
                   dashes=PLOT_SETTINGS["midsurface_dashes"],
                   alpha=PLOT_SETTINGS["midsurface_alpha"],
                   zorder=0)

    # Interior ply-interface lines (skip the outer surfaces)
    for k in range(2, laminate["N"] + 1):
        ax.axhline(laminate["z"][k-1] / laminate["H"],
                   color=PLOT_SETTINGS["interface_color"],
                   linewidth=PLOT_SETTINGS["interface_line_width"],
                   alpha=PLOT_SETTINGS["interface_alpha"],
                   zorder=0)

    # Vertical axis (x = 0) reference line
    ax.axvline(0,
               color=PLOT_SETTINGS["vertical_axis_color"],
               linewidth=PLOT_SETTINGS["axes_line_width"],
               zorder=0)

    # y-tick locations: every interface if few enough plies, else just the
    # bottom / midsurface / top so the axis is not cluttered
    if laminate["N"] < 10:
        ax.set_yticks(laminate["z"] / laminate["H"])
    else:
        ax.set_yticks([-0.5, 0, 0.5])

    ax.set_xlim(xlim)
    ax.set_ylim(-0.5, 0.5)


def _midsurface_at_interface(laminate):
    """True when z = 0 coincides with a ply interface to within tol*H.

    For every even-N laminate the midsurface lies on a ply
    interface, so the dashed midsurface reference line would overlay
    a solid interface line.  In that case we suppress the dashed
    line so the figure shows only physically meaningful features.
    For odd-N laminates z = 0 is interior to a ply and the dashed
    line is a useful kinematic reference.
    """
    tol = 1e-6
    return np.min(np.abs(laminate["z"])) < tol * laminate["H"]
