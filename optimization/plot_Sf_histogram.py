"""Histogram of Sf over the brute-force-enumerated design space."""

import matplotlib.pyplot as plt


__all__ = ["plot_Sf_histogram"]


def plot_Sf_histogram(all_Sf, best_Sf, N_plies):
    """Plot the distribution of Sf_min over a brute-force-enumerated design space.

    Visual companion to ``brute_force_search``: the histogram makes
    the *value* of optimisation visceral -- most random stackings
    have small Sf, the optimum sits in the right tail.  A vertical
    line marks the best Sf found.

    Parameters
    ----------
    all_Sf : np.ndarray
        The Sf_min of every enumerated stacking (returned by
        ``brute_force_search``).
    best_Sf : float
        The optimum Sf_min (drawn as a vertical reference line).
    N_plies : int
        Used in the figure title.
    """
    n_total = len(all_Sf)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(all_Sf, bins=60, color="tab:orange",
            edgecolor="black", linewidth=0.5)
    ax.axvline(best_Sf, color="tab:red", linewidth=2,
               label=f"best Sf = {best_Sf:.3f}")
    ax.set_xlabel(r"Minimum Tsai-Wu safety factor $S_f$")
    ax.set_ylabel("Number of stackings")
    ax.set_title(
        f"Sf distribution over {n_total:,d} stackings (N_plies = {N_plies})"
    )
    ax.legend()
    fig.tight_layout()
