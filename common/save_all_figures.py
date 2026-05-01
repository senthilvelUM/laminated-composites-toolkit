"""Save every currently-open matplotlib figure to the runner's output
folder ``results/<runner_name>/``.

Pairs with ``start_results_file()`` so that every artefact of one
runner -- the markdown transcript ``output.md`` and the PNGs --
ends up in the same per-runner subfolder.  No more loose figures
piling up at the project root.
"""

import os

import matplotlib.pyplot as plt


__all__ = ["save_all_figures"]


def save_all_figures(demo_file, *, dpi=150):
    """Save every currently-open matplotlib figure to
    ``<demo_dir>/results/<demo_name>/fig<NN>_<title>.png``.

    Call this once per runner, immediately before ``show_figures()``.
    Files are named after the matplotlib figure number and (sanitised)
    axes title; figures with no title fall back to ``fig<NN>.png``.

    Output is placed under the runner script's own directory, so
    project-root runners save into ``<project>/results/<demo>/`` and
    textbook examples in ``worked_examples/`` save into
    ``worked_examples/results/<demo>/``.  ``start_results_file`` uses the
    same convention so transcript and figures co-locate.

    Parameters
    ----------
    demo_file : str
        Pass the runner's ``__file__``.  The directory and runner
        subfolder name are derived from this.
    dpi : int, optional
        Resolution of the saved PNGs (default: 150).
    """
    demo_dir = os.path.dirname(os.path.abspath(demo_file))
    demo_name = os.path.splitext(os.path.basename(demo_file))[0]
    out_dir = os.path.join(demo_dir, "results", demo_name)
    os.makedirs(out_dir, exist_ok=True)

    nums = plt.get_fignums()
    for n in nums:
        fig = plt.figure(n)
        title = fig.axes[0].get_title() if fig.axes else ""
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in title).strip("_")
        fname = f"fig{n:02d}_{safe}.png" if safe else f"fig{n:02d}.png"
        fig.savefig(os.path.join(out_dir, fname), dpi=dpi, bbox_inches="tight")

    if nums:
        print(f"\nSaved {len(nums)} figure(s) to {out_dir}/")
