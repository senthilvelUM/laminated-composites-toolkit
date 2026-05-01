"""Plot the off-axis engineering properties of a ply vs the angle theta."""

import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# User-configurable plot settings. Edit these to change the look of the plots.
# ---------------------------------------------------------------------------

PLOT_SETTINGS = {
    "font_size":            14,                          # Font size for axis labels and ticks
    "line_width":           2.0,                         # Thickness of the data curve
    "line_color":           "tab:blue",                # Data curve color (matplotlib name)
    "vertical_axis_color":  (0.2, 0.2, 0.2),             # Color of the theta = 0 reference line
    "axes_line_width":      0.5,                         # Thickness of the reference line
    "grid_alpha":           0.3,                         # Grid line transparency
    "figure_size_single":   (6, 4),                      # Size (in inches) of each standalone plot
    "figure_size_combined": (10, 7),                     # Size (in inches) of the 2x2 combined plot
    "save_dpi":             300,                         # Resolution of saved PNG files
}


def plot_off_axis_properties(ply):
    """Plot Ex, Ey, Gxy, and nuxy as functions of the ply angle theta.

    Sweeps theta from -90 to 90 degrees and computes the global-frame
    engineering properties from the ply's reduced compliance matrix S
    (which is in the 1-2 material coordinate system and independent
    of theta).

    Saves a combined 2x2 figure and one standalone figure per property
    to results/figures/.

    Parameters
    ----------
    ply : dict
        Ply dictionary created by create_ply(). Must contain the
        reduced compliance matrix S.
    """
    # Reduced compliance components in the 1-2 (material) coordinate system
    S11 = ply["S"][0, 0]
    S12 = ply["S"][0, 1]
    S22 = ply["S"][1, 1]
    S66 = ply["S"][2, 2]

    # Sweep the ply angle theta from -90 to 90 degrees
    theta = np.arange(-90, 90.25, 0.25)
    m = np.cos(np.radians(theta))
    n = np.sin(np.radians(theta))

    # Off-axis compliance components (same formulas as in create_ply.py,
    # but evaluated for all angles at once)
    SBar11 = S11*m**4 + (2*S12 + S66)*m**2*n**2 + S22*n**4
    SBar12 = (S11 + S22 - S66)*m**2*n**2 + S12*(m**4 + n**4)
    SBar22 = S11*n**4 + (2*S12 + S66)*n**2*m**2 + S22*m**4
    SBar66 = 2*(2*S11 + 2*S22 - 4*S12 - S66)*n**2*m**2 + S66*(n**4 + m**4)

    # Off-axis engineering properties in the global (x-y) coordinate system
    Ex = 1 / SBar11
    Ey = 1 / SBar22
    Gxy = 1 / SBar66
    nuxy = -SBar12 / SBar11

    # The four property plots (short-name, y-values, y-axis label)
    plots = [
        ("Ex",   Ex / 1e9,   r"Extensional modulus $E_x$, GPa"),
        ("Ey",   Ey / 1e9,   r"Extensional modulus $E_y$, GPa"),
        ("Gxy",  Gxy / 1e9,  r"Shear modulus $G_{xy}$, GPa"),
        ("nuxy", nuxy,       r"Poisson's ratio $\nu_{xy}$"),
    ]

    # Apply user font-size setting to all plotting below
    with plt.rc_context({"font.size": PLOT_SETTINGS["font_size"]}):

        # Save each property as its own high-resolution figure
        for short_name, values, ylabel in plots:
            single_fig, ax = plt.subplots(figsize=PLOT_SETTINGS["figure_size_single"])
            ax.plot(theta, values,
                    color=PLOT_SETTINGS["line_color"],
                    linewidth=PLOT_SETTINGS["line_width"])
            ax.set_ylabel(ylabel)
            ax.set_xlabel(r"Angle $\theta$, degrees")
            ax.set_xlim(-90, 90)
            ax.set_xticks([-90, -45, 0, 45, 90])
            ax.axvline(0,
                       color=PLOT_SETTINGS["vertical_axis_color"],
                       linewidth=PLOT_SETTINGS["axes_line_width"])
            ax.grid(True, alpha=PLOT_SETTINGS["grid_alpha"])
            single_fig.tight_layout()
            plt.close(single_fig)
        # Combined 2x2 figure for on-screen viewing (also saved)
        fig, axes = plt.subplots(2, 2, figsize=PLOT_SETTINGS["figure_size_combined"])
        fig.suptitle(f"Off-axis engineering properties: {ply['name']}")
        for (_, values, ylabel), ax in zip(plots, axes.flat):
            ax.plot(theta, values,
                    color=PLOT_SETTINGS["line_color"],
                    linewidth=PLOT_SETTINGS["line_width"])
            ax.set_ylabel(ylabel)
            ax.set_xlabel(r"Angle $\theta$, degrees")
            ax.set_xlim(-90, 90)
            ax.set_xticks([-90, -45, 0, 45, 90])
            ax.axvline(0,
                       color=PLOT_SETTINGS["vertical_axis_color"],
                       linewidth=PLOT_SETTINGS["axes_line_width"])
            ax.grid(True, alpha=PLOT_SETTINGS["grid_alpha"])
        fig.tight_layout()
        plt.show()
