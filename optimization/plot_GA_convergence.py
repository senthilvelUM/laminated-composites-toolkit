"""Convergence-history plot for the GA (best vs population-mean Sf)."""

import matplotlib.pyplot as plt
import numpy as np


__all__ = ["plot_GA_convergence"]


def plot_GA_convergence(history, N_plies, pop_size):
    """Plot the GA convergence curves: best-of-generation and population mean.

    The two curves together tell most of the GA story:
      * ``best`` should rise monotonically thanks to elitism.
      * ``mean`` reflects population-wide quality and tends to lag
        the best curve by a few generations.

    A long flat tail on ``best`` with ``mean`` still climbing
    indicates the population converging onto the basin of the
    incumbent.

    Parameters
    ----------
    history : dict[str, list[float]]
        Returned by ``evolve``; must contain keys ``"best"`` and
        ``"mean"``.
    N_plies : int
        Used in the figure title.
    pop_size : int
        Used in the figure title.
    """
    gens = np.arange(len(history["best"]))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(gens, history["best"], "-o",
            color="tab:red",  linewidth=2,   markersize=4,
            label="best of generation")
    ax.plot(gens, history["mean"], "-s",
            color="tab:blue", linewidth=1.5, markersize=4,
            label="population mean")
    ax.set_xlabel("Generation")
    ax.set_ylabel(r"Tsai-Wu safety factor $S_f$")
    ax.set_title(f"GA convergence (N_plies = {N_plies}, pop = {pop_size})")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
