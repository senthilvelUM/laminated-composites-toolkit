"""Helpers to mirror terminal output to a markdown results file.

Each runner gets its own subfolder under ``results/`` named after the
runner, e.g. ``results/run_fe_plate_clt_static/``, holding both the
markdown transcript ``output.md`` and the figures saved by
``save_all_figures()``.  All artefacts of a single analysis live in
one place.
"""

import os
import sys
from pathlib import Path

from common.tee import Tee


def start_results_file(runner_file, title):
    """Begin mirroring stdout to ``<runner_dir>/results/<runner_name>/output.md``.

    The runner_name is derived from the runner's ``__file__`` and
    the output is placed under the runner's own directory, so
    project-root runners write to ``<project>/results/<runner>/``
    and textbook examples in ``worked_examples/`` write to
    ``worked_examples/results/<runner>/``.  ``save_all_figures`` uses the
    same convention so transcript and figures co-locate.

    Writes a markdown H1 heading and an opening code fence to the
    file, then replaces sys.stdout so every subsequent print() is
    echoed to both the terminal and the file.

    Parameters
    ----------
    runner_file : str
        Pass the runner's ``__file__``.  The directory and name of
        the output file are derived from this.
    title : str
        Markdown H1 title written at the top of the output file.

    Returns
    -------
    file object
        The opened file handle.  Pass it to end_results_file() later.
    """
    runner_name = os.path.splitext(os.path.basename(runner_file))[0]
    runner_dir  = Path(runner_file).resolve().parent
    out_dir     = runner_dir / "results" / runner_name
    out_dir.mkdir(parents=True, exist_ok=True)
    f = open(out_dir / "output.md", "w")
    f.write(f"# {title}\n\n```\n")
    sys.stdout = Tee(sys.__stdout__, f)
    return f


def end_results_file(f):
    """Close the results file and restore stdout.

    Writes the closing code fence, closes the file, and points
    sys.stdout back at the terminal.

    Parameters
    ----------
    f : file object
        The file handle returned by start_results_file().
    """
    sys.stdout = sys.__stdout__
    f.write("```\n")
    f.close()
