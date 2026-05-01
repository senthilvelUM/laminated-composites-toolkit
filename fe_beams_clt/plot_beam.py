#*********************************************************************
#                Finite Element Learning Toolkit
#
#                Module: plot_beam
#
#  Bundles every plotting routine for the 2D Euler-Bernoulli beam
#  module into a single file. Edit PLOT_SETTINGS below to change the
#  look and feel of every plot in this module at once.
#
#  Public functions:
#    plot_beam_undeformed(ENODES, NODALCOORDINATES, TitleStr)
#    plot_beam_deflection(ENODES, NODALCOORDINATES, D)
#    plot_beam_bending_moment(ENODES, NODALCOORDINATES, EI, D)
#    plot_beam_shear_force(ENODES, NODALCOORDINATES, EI, D)
#*********************************************************************
import matplotlib.pyplot as plt
import numpy as np



__all__ = ["PLOT_SETTINGS", "plot_beam_undeformed", "plot_beam_deflection", "plot_beam_bending_moment", "plot_beam_shear_force", "plot_beam_mode_shape"]

# ---------------------------------------------------------------------
# User-configurable plot settings
# Edit any value here to change look-and-feel across every routine
# in this file.
# ---------------------------------------------------------------------
PLOT_SETTINGS = {
    "font_size":                          16,                 # Font size for axis labels, ticks, and node/element numbers
    "line_thickness":                     2.0,                # Thickness of element lines (undeformed beam)
    "deformed_line_thickness":            4.0,                # Thickness of the deflection / bending-moment / shear-force curve
    "marker_size":                        12,                 # Size of node dots
    "node_label_color":                   (0, 140 / 255, 0),  # RGB color for node-number labels
    "element_label_color":                (180 / 255, 0, 0),  # RGB color for element-number labels
    "curve_color":                        "#1f77b4",          # Color of the deflection / bending-moment / shear-force curve
    "axis_pad_fraction":                  0.1,                # Initial symmetric x/y padding around the geometry (also used for shear-force data range)
    "axis_pad_x":              0.05,               # Final horizontal padding (after labels are placed; also used for deflection / bending-moment data range)
    "axis_pad_y":           0.2,                # Final vertical padding (after labels are placed; also used for deflection / bending-moment data range)
    "label_offset_divisor":               30,                 # Label nudge = min(XRange, YRange) / this divisor
    "n_interpolation_points_deflection":  10000,              # Sample points per element along the deflection curve v(x)
    "n_interpolation_points_bending_moment": 1000,            # Sample points per element along M(x)
    "n_interpolation_points_shear_force": 1000,               # Sample points per element along V(x)
    "dpi":                                150,                # Resolution (dots per inch) of saved PNGs in <demo_dir>/results/
}


#*********************************************************************
#                Function: plot_beam_undeformed
#
#  Purpose:
#    Plot the undeformed geometry of a 2D beam structure using straight
#    line beam elements and nodal coordinates.
#
#  Inputs:
#    ENODES            - Element connectivity array
#                        column 0      : element number (1-based)
#                        columns 1-2   : global node numbers for the element
#
#    NODALCOORDINATES  - Nodal coordinate array
#                        column 0      : global node number (1-based)
#                        column 1      : x-coordinate
#                        column 2      : y-coordinate
#
#    TitleStr          - (Optional) Figure title string. Defaults to
#                        'Undeformed beam' if omitted.
#
#  Outputs:
#    None. The undeformed beam geometry is drawn on a NEW figure (created internally).
#
#  Notes:
#    This function assumes a planar (2D) beam model and plots the
#    centerline of each beam element in the undeformed configuration.
#*********************************************************************
def plot_beam_undeformed(ENODES, NODALCOORDINATES, TitleStr="Undeformed beam"):

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # Create a new figure and a fresh axes
    fig, ax = plt.subplots()

    FontSize = PLOT_SETTINGS["font_size"]
    LineThickness = PLOT_SETTINGS["line_thickness"]
    MarkerSize = PLOT_SETTINGS["marker_size"]

    # Determine the total number of elements and nodes
    NELEMENTS = ENODES.shape[0]
    NODES = NODALCOORDINATES.shape[0]

    # Loop through all elements and draw a line connecting the nodes
    for e in range(NELEMENTS):
        i = int(ENODES[e, 1])  # First node of beam element
        j = int(ENODES[e, 2])  # Second node of beam element
        xi = NODALCOORDINATES[i - 1, 1]
        yi = NODALCOORDINATES[i - 1, 2]
        xj = NODALCOORDINATES[j - 1, 1]
        yj = NODALCOORDINATES[j - 1, 2]
        ax.plot([xi, xj], [yi, yj], color="k", linewidth=LineThickness, solid_capstyle="round", solid_joinstyle="round")
        ax.plot([xi, xj], [yi, yj], "k.", markersize=MarkerSize)

    # Set figure properties
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    XRange = xlim[1] - xlim[0]
    YRange = ylim[1] - ylim[0]
    ax.set_xlim(xlim[0] - PLOT_SETTINGS["axis_pad_fraction"] * XRange,
                xlim[1] + PLOT_SETTINGS["axis_pad_fraction"] * XRange)
    ax.set_ylim(ylim[0] - PLOT_SETTINGS["axis_pad_fraction"] * YRange,
                ylim[1] + PLOT_SETTINGS["axis_pad_fraction"] * YRange)

    # Slightly offset the text from the selected coordinates
    label_div = PLOT_SETTINGS["label_offset_divisor"]
    Delta = min(XRange, YRange) / label_div if min(XRange, YRange) > 0 else XRange / label_div

    # Insert node numbers
    for n in range(NODES):
        xn = NODALCOORDINATES[n, 1]
        yn = NODALCOORDINATES[n, 2]
        ax.text(xn + Delta, yn, str(int(NODALCOORDINATES[n, 0])),
                fontsize=FontSize, fontweight="bold",
                color=PLOT_SETTINGS["node_label_color"])

    # Insert the element number near the center of each element
    for e in range(NELEMENTS):
        i = int(ENODES[e, 1])
        j = int(ENODES[e, 2])
        xi = NODALCOORDINATES[i - 1, 1]
        yi = NODALCOORDINATES[i - 1, 2]
        xj = NODALCOORDINATES[j - 1, 1]
        yj = NODALCOORDINATES[j - 1, 2]
        xm = 0.5 * xi + 0.5 * xj   # midpoint for element number placement
        ym = 0.5 * yi + 0.5 * yj
        ax.text(xm + Delta, ym, str(int(ENODES[e, 0])),
                fontsize=FontSize, fontweight="bold",
                color=PLOT_SETTINGS["element_label_color"])

    # Final figure properties
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    XRange = xlim[1] - xlim[0]
    YRange = ylim[1] - ylim[0]
    ax.set_xlim(xlim[0] - PLOT_SETTINGS["axis_pad_x"] * XRange,
                xlim[1] + PLOT_SETTINGS["axis_pad_x"] * XRange)
    ax.set_ylim(ylim[0] - PLOT_SETTINGS["axis_pad_y"] * YRange,
                ylim[1] + PLOT_SETTINGS["axis_pad_y"] * YRange)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.grid(True)

    # Insert figure caption
    ax.set_title(TitleStr)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5 * LineThickness)


#*********************************************************************
#                Function: plot_beam_deflection
#
#  Purpose: Plot the deflected shape of a 2D beam structure using the
#    nodal displacement solution obtained from a finite element analysis.
#
#  Inputs:
#    ENODES            - Element connectivity array
#                        column 0      : element number (1-based)
#                        columns 1-2   : global node numbers for the element
#
#    NODALCOORDINATES  - Nodal coordinate array
#                        column 0      : global node number (1-based)
#                        column 1      : x-coordinate
#                        column 2      : y-coordinate
#
#    D                 - Global nodal displacement vector
#
#  Outputs:
#    None. The beam deflection is drawn on a NEW figure (created internally).
#
#  Notes:
#    This function assumes a planar (2D) beam model. The plotted curve
#    represents the transverse deflection of the beam centerline.
#*********************************************************************
def plot_beam_deflection(ENODES, NODALCOORDINATES, D):

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # First plot the undeformed shape of the beam.  plot_beam_undeformed
    # creates a new figure and leaves it as the current figure, so the
    # deflection-drawing code below adds onto that same figure.
    plot_beam_undeformed(ENODES, NODALCOORDINATES)
    ax = plt.gca()

    LineThickness = PLOT_SETTINGS["deformed_line_thickness"]

    # Number of elements, DOF and sampling points
    NELEMENTS = ENODES.shape[0]    # Determine the number of beam elements
    NDOF = 2                       # Beam has 2 DOFs per node (v, phi)
    NPlotPoints = PLOT_SETTINGS["n_interpolation_points_deflection"]   # Number of sample points per element

    D = np.asarray(D).ravel()

    # Track the range of plotted deflection values so we can rescale the
    # axes around the data (plot_beam_undeformed set y-limits that are
    # much too tight or too loose for a deflection curve at a different scale)
    all_xs = []
    all_ys = []

    # Loop through all elements and plot the deflection for each element
    for e in range(NELEMENTS):
        i = int(ENODES[e, 1])  # First node of beam element
        j = int(ENODES[e, 2])  # Second node of beam element
        xi = NODALCOORDINATES[i - 1, 1]
        xj = NODALCOORDINATES[j - 1, 1]
        L = xj - xi            # length of beam element
        xs = np.linspace(xi, xj, NPlotPoints)

        # Element nodal displacements/rotations
        v1   = D[(i - 1) * NDOF + 1]
        phi1 = D[(i - 1) * NDOF + 2]
        v2   = D[(j - 1) * NDOF + 1]
        phi2 = D[(j - 1) * NDOF + 2]

        # Evaluate shape-function interpolated deflection at each sample point
        x = xs - xi
        N1 = (1 / L**3) * ( 2 * x**3 - 3 * x**2 * L + L**3)
        N2 = (1 / L**3) * ( x**3 * L - 2 * x**2 * L**2 + x * L**3)
        N3 = (1 / L**3) * (-2 * x**3 + 3 * x**2 * L)
        N4 = (1 / L**3) * ( x**3 * L - x**2 * L**2)

        # Calculate the deflection using shape functions
        ys = N1 * v1 + N2 * phi1 + N3 * v2 + N4 * phi2

        ax.plot(xs, ys, color=PLOT_SETTINGS["curve_color"], linewidth=LineThickness, solid_capstyle="round", solid_joinstyle="round")

        all_xs.append(xs)
        all_ys.append(ys)

    # Set axes based on the deflection data range (always include y=0 for the
    # undeformed reference line), then expand by a padding factor
    all_xs = np.concatenate(all_xs)
    all_ys = np.concatenate(all_ys)
    xmin, xmax = all_xs.min(), all_xs.max()
    ymin = min(all_ys.min(), 0.0)
    ymax = max(all_ys.max(), 0.0)
    XRange = xmax - xmin
    YRange = ymax - ymin if ymax > ymin else 1.0
    ax.set_xlim(xmin - PLOT_SETTINGS["axis_pad_x"] * XRange,
                xmax + PLOT_SETTINGS["axis_pad_x"] * XRange)
    ax.set_ylim(ymin - PLOT_SETTINGS["axis_pad_y"] * YRange,
                ymax + PLOT_SETTINGS["axis_pad_y"] * YRange)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"Deflection $v(x)$")
    ax.grid(True)

    # Insert figure caption
    ax.set_title("Beam deflection")


#*********************************************************************
#                Function: plot_beam_bending_moment
#
#  Purpose:
#    Plot the internal bending moment diagram for a 2D beam structure
#    based on the finite element displacement solution.
#
#  Inputs:
#    ENODES            - Element connectivity array
#                        column 0      : element number (1-based)
#                        columns 1-2   : global node numbers for the element
#
#    NODALCOORDINATES  - Nodal coordinate array
#                        column 0      : global node number (1-based)
#                        column 1      : x-coordinate
#                        column 2      : y-coordinate
#
#    EI                - Bending rigidity (E*I) for each beam element
#    D                 - Global nodal displacement vector
#
#  Outputs:
#    None. The beam bending moment diagram is drawn on a NEW figure (created internally).
#
#  Notes:
#    This function assumes a planar (2D) Euler-Bernoulli beam model.
#    Bending moments are computed from element-level internal forces.
#*********************************************************************
def plot_beam_bending_moment(ENODES, NODALCOORDINATES, EI, D):

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # First plot the undeformed shape of the beam.  plot_beam_undeformed
    # creates a new figure and leaves it as the current figure, so the
    # deflection-drawing code below adds onto that same figure.
    plot_beam_undeformed(ENODES, NODALCOORDINATES)
    ax = plt.gca()

    LineThickness = PLOT_SETTINGS["deformed_line_thickness"]

    # Number of elements, DOF and sampling points
    NELEMENTS = ENODES.shape[0]    # Determine the number of beam elements
    NDOF = 2                       # Beam has 2 DOFs per node (v, phi)
    NPlotPoints = PLOT_SETTINGS["n_interpolation_points_bending_moment"]   # Number of sample points per element

    D = np.asarray(D).ravel()

    # Track the range of plotted moment values so we can rescale the axes
    # around the data (plot_beam_undeformed set y-limits sized for the beam
    # geometry, which is the wrong scale for a bending moment diagram)
    all_xs = []
    all_Ms = []

    # Loop through all elements and plot the bending moment for each element.
    # `n` is a 0-based row index into the (sorted) ENODES table; the 1-based
    # element label lives in column 0, and indexes the 1-padded EI array.
    for n in range(NELEMENTS):
        eid = int(ENODES[n, 0])  # 1-based element label (for EI[])
        i = int(ENODES[n, 1])    # First node of beam element (1-based)
        j = int(ENODES[n, 2])    # Second node of beam element (1-based)
        xi = NODALCOORDINATES[i - 1, 1]
        xj = NODALCOORDINATES[j - 1, 1]
        L = xj - xi            # length of beam element
        xs = np.linspace(xi, xj, NPlotPoints)

        # Element nodal displacements/rotations
        v1   = D[(i - 1) * NDOF + 1]
        phi1 = D[(i - 1) * NDOF + 2]
        v2   = D[(j - 1) * NDOF + 1]
        phi2 = D[(j - 1) * NDOF + 2]

        # Calculate the bending moment at each point
        #    M(x) = EI * v''(x) = (EI/L^3) * [B1 B2 B3 B4] * [v1 phi1 v2 phi2]^T
        # where [B1..B4] are the second derivatives of the Hermite shape functions.
        x = xs - xi
        B1 =  12 * x - 6 * L
        B2 =   6 * x * L - 4 * L**2
        B3 = -12 * x + 6 * L
        B4 =   6 * x * L - 2 * L**2

        M = (EI[eid] / L**3) * (B1 * v1 + B2 * phi1 + B3 * v2 + B4 * phi2)

        ax.plot(xs, M, color=PLOT_SETTINGS["curve_color"], linewidth=LineThickness, solid_capstyle="round", solid_joinstyle="round")

        all_xs.append(xs)
        all_Ms.append(M)

    # Set axes based on the moment data range (always include M=0 for the
    # zero-moment reference line), then expand by a padding factor
    all_xs = np.concatenate(all_xs)
    all_Ms = np.concatenate(all_Ms)
    xmin, xmax = all_xs.min(), all_xs.max()
    ymin = min(all_Ms.min(), 0.0)
    ymax = max(all_Ms.max(), 0.0)
    XRange = xmax - xmin
    YRange = ymax - ymin if ymax > ymin else 1.0
    ax.set_xlim(xmin - PLOT_SETTINGS["axis_pad_x"] * XRange,
                xmax + PLOT_SETTINGS["axis_pad_x"] * XRange)
    ax.set_ylim(ymin - PLOT_SETTINGS["axis_pad_y"] * YRange,
                ymax + PLOT_SETTINGS["axis_pad_y"] * YRange)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"Bending Moment $M(x)$")
    ax.grid(True)

    # Insert figure caption
    ax.set_title("Bending moment diagram")


#*********************************************************************
#                Function: plot_beam_shear_force
#
#  Purpose:
#    Plot the internal shear force diagram for a 2D beam structure
#    based on the finite element displacement solution.
#
#  Inputs:
#    ENODES            - Element connectivity array
#                        column 0      : element number (1-based)
#                        columns 1-2   : global node numbers for the element
#
#    NODALCOORDINATES  - Nodal coordinate array
#                        column 0      : global node number (1-based)
#                        column 1      : x-coordinate
#                        column 2      : y-coordinate
#
#    EI                - Bending rigidity (E*I) for each beam element
#    D                 - Global nodal displacement vector
#
#  Outputs:
#    None. The beam shear force diagram is drawn on a NEW figure (created internally).
#
#  Notes:
#    This function assumes a planar (2D) Euler-Bernoulli beam model.
#    Shear forces are computed from element-level internal forces.
#*********************************************************************
def plot_beam_shear_force(ENODES, NODALCOORDINATES, EI, D):

    # Reorder ENODES so element numbers are in ascending order
    ENODES = np.asarray(ENODES)
    ENODES = ENODES[ENODES[:, 0].argsort()]

    # Reorder NODALCOORDINATES so node numbers are in ascending order
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    NODALCOORDINATES = NODALCOORDINATES[NODALCOORDINATES[:, 0].argsort()]

    # First plot the undeformed shape of the beam.  plot_beam_undeformed
    # creates a new figure and leaves it as the current figure, so the
    # deflection-drawing code below adds onto that same figure.
    plot_beam_undeformed(ENODES, NODALCOORDINATES)
    ax = plt.gca()

    LineThickness = PLOT_SETTINGS["deformed_line_thickness"]

    # Number of elements, DOF and sampling points
    NELEMENTS = ENODES.shape[0]    # Determine the number of beam elements
    NDOF = 2                       # Beam has 2 DOFs per node (v, phi)
    NPlotPoints = PLOT_SETTINGS["n_interpolation_points_shear_force"]   # Number of sample points per element

    D = np.asarray(D).ravel()

    # Track the range of plotted shear values so we can rescale the axes
    # around the data (plot_beam_undeformed set y-limits sized for the beam
    # geometry, which is the wrong scale for a shear force diagram)
    all_xs = []
    all_Vs = []

    # Loop through all elements and plot the shear force for each element.
    # `e` is a 0-based row index into the (sorted) ENODES table; the 1-based
    # element label lives in column 0, and indexes the 1-padded EI array.
    for e in range(NELEMENTS):
        eid = int(ENODES[e, 0])  # 1-based element label (for EI[])
        i = int(ENODES[e, 1])    # First node of beam element (1-based)
        j = int(ENODES[e, 2])    # Second node of beam element (1-based)
        xi = NODALCOORDINATES[i - 1, 1]
        xj = NODALCOORDINATES[j - 1, 1]
        L = xj - xi            # length of beam element
        xs = np.linspace(xi, xj, NPlotPoints)

        # Element nodal displacements/rotations
        v1   = D[(i - 1) * NDOF + 1]
        phi1 = D[(i - 1) * NDOF + 2]
        v2   = D[(j - 1) * NDOF + 1]
        phi2 = D[(j - 1) * NDOF + 2]

        # Calculate the shear force at each point
        #    V(x) = EI * v'''(x) = (EI/L^3) * [12, 6L, -12, 6L] * [v1 phi1 v2 phi2]^T
        # (constant over the element for Hermite cubic shape functions)
        V_const = (EI[eid] / L**3) * (12 * v1 + 6 * L * phi1
                                      - 12 * v2 + 6 * L * phi2)
        V = np.full_like(xs, V_const)

        ax.plot(xs, V, color=PLOT_SETTINGS["curve_color"], linewidth=LineThickness, solid_capstyle="round", solid_joinstyle="round")

        all_xs.append(xs)
        all_Vs.append(V)

    # Set axes based on the shear data range (always include V=0 for the
    # zero-shear reference line), then expand by a padding factor
    all_xs = np.concatenate(all_xs)
    all_Vs = np.concatenate(all_Vs)
    xmin, xmax = all_xs.min(), all_xs.max()
    ymin = min(all_Vs.min(), 0.0)
    ymax = max(all_Vs.max(), 0.0)
    XRange = xmax - xmin
    YRange = ymax - ymin if ymax > ymin else 1.0
    ax.set_xlim(xmin - PLOT_SETTINGS["axis_pad_fraction"] * XRange,
                xmax + PLOT_SETTINGS["axis_pad_fraction"] * XRange)
    ax.set_ylim(ymin - PLOT_SETTINGS["axis_pad_fraction"] * YRange,
                ymax + PLOT_SETTINGS["axis_pad_fraction"] * YRange)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"Shear Force $V(x)$")
    ax.grid(True)

    # Insert figure caption
    ax.set_title("Shear force diagram")


#*********************************************************************
#                Function: plot_beam_mode_shape
#
#  Purpose:
#    Plot a single FE-computed mode shape v(x) of the beam by
#    interpolating the cubic Hermite shape functions on each element.
#    A new figure is created.
#
#  Inputs:
#    ENODES, NODALCOORDINATES - the usual mesh tables
#    d                        - 1-padded global mode-shape vector
#                               (constrained DOFs zero, mass-normalized)
#    TitleStr                 - figure title
#*********************************************************************
def plot_beam_mode_shape(ENODES, NODALCOORDINATES, d, TitleStr):

    ENODES = np.asarray(ENODES)
    NODALCOORDINATES = np.asarray(NODALCOORDINATES, dtype=float)
    d = np.asarray(d, dtype=float).ravel()

    fig, ax = plt.subplots()
    ax.set_box_aspect(1.0 / 1.618)

    LineThickness = PLOT_SETTINGS["deformed_line_thickness"]

    NELEMENTS   = ENODES.shape[0]
    NDOF        = 2
    NPlotPoints = PLOT_SETTINGS["n_interpolation_points_deflection"]

    all_xs = []
    all_ys = []

    for e in range(NELEMENTS):
        i = int(ENODES[e, 1])
        j = int(ENODES[e, 2])
        xi = NODALCOORDINATES[i - 1, 1]
        xj = NODALCOORDINATES[j - 1, 1]
        L  = xj - xi

        # Sample within the element and evaluate the cubic Hermite shape functions
        xs = np.linspace(xi, xj, NPlotPoints)
        x  = xs - xi
        N1 = (1.0 / L**3) * ( 2.0 * x**3 - 3.0 * x**2 * L  +       L**3)
        N2 = (1.0 / L**3) * (       x**3 * L - 2.0 * x**2 * L**2 + x * L**3)
        N3 = (1.0 / L**3) * (-2.0 * x**3 + 3.0 * x**2 * L)
        N4 = (1.0 / L**3) * (       x**3 * L -       x**2 * L**2)

        v1   = d[(i - 1) * NDOF + 1]
        phi1 = d[(i - 1) * NDOF + 2]
        v2   = d[(j - 1) * NDOF + 1]
        phi2 = d[(j - 1) * NDOF + 2]

        ys = N1 * v1 + N2 * phi1 + N3 * v2 + N4 * phi2

        ax.plot(xs, ys, color=PLOT_SETTINGS["curve_color"], linewidth=LineThickness,
                solid_capstyle="round", solid_joinstyle="round")
        all_xs.append(xs)
        all_ys.append(ys)

    all_xs = np.concatenate(all_xs)
    all_ys = np.concatenate(all_ys)
    xmin, xmax = all_xs.min(), all_xs.max()
    ymin = min(all_ys.min(), 0.0)
    ymax = max(all_ys.max(), 0.0)
    XRange = xmax - xmin
    YRange = ymax - ymin if ymax > ymin else 1.0
    ax.set_xlim(xmin - PLOT_SETTINGS["axis_pad_x"] * XRange,
                xmax + PLOT_SETTINGS["axis_pad_x"] * XRange)
    ax.set_ylim(ymin - PLOT_SETTINGS["axis_pad_y"] * YRange,
                ymax + PLOT_SETTINGS["axis_pad_y"] * YRange)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"Mode shape $v(x)$")
    ax.set_title(TitleStr)
    ax.grid(True)
