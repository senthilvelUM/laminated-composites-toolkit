"""Backend-aware wrapper around matplotlib.pyplot.show().

Calling plt.show() with the Agg (headless) backend triggers a
UserWarning: "FigureCanvasAgg is non-interactive, and thus cannot be
shown".  Students running runners over SSH or in CI invariably hit
this warning, which is noise -- they don't need to be reminded their
backend is non-interactive.

This helper checks the active backend and only calls plt.show() if
it is interactive.  Drop-in replacement for plt.show() at the end of
a runner.
"""

import matplotlib
import matplotlib.pyplot as plt


__all__ = ["show_figures"]


# Set of matplotlib backends classified as "non-interactive" -- a
# plt.show() call on these prints a UserWarning and does nothing useful.
_NON_INTERACTIVE_BACKENDS = {
    "agg", "cairo", "pdf", "pgf", "ps", "svg", "template",
}


def show_figures():
    """Call plt.show() only if the active matplotlib backend is interactive.

    Pedagogically: "show all open figures, but only if the runtime can
    actually display them."
    """
    backend = matplotlib.get_backend().lower()
    if backend not in _NON_INTERACTIVE_BACKENDS:
        plt.show()
