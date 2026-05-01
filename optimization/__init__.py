"""Stacking-sequence optimisation toolkit.

Given the in-plane and moment resultants ``(Nx, Ny, Nxy, Mx, My, Mxy)``
applied to a laminate, find the stacking sequence on a discrete angle
set that maximises the minimum first-ply Tsai-Wu safety factor.

Two search strategies share the same fast evaluator:

  * ``brute_force_search`` -- exhaustive enumeration over
    ``len(angle_set) ** N_plies`` stackings.  Guarantees the global
    optimum but only feasible for small ``N_plies``.

  * ``evolve`` -- integer-coded genetic algorithm built from four
    one-concept-one-file operators (``random_individual``,
    ``tournament_select``, ``one_point_crossover``, ``mutate``).
    Scales to large ``N_plies`` where brute force is hopeless.

Two plotting helpers visualise the search outcome:

  * ``plot_Sf_histogram``      -- distribution of Sf over the
                                   brute-force design space.
  * ``plot_GA_convergence``     -- best & population-mean Sf per
                                   generation of the GA.

The runners ``run_stacking_optimization_brute_force.py`` and
``run_stacking_optimization_genetic_algorithm.py`` each use this package via
``from optimization import *``.
"""

from optimization.brute_force_search import brute_force_search
from optimization.evaluate_stacking import evaluate_stacking
from optimization.evolve import evolve
from optimization.mutate import mutate
from optimization.one_point_crossover import one_point_crossover
from optimization.plot_GA_convergence import plot_GA_convergence
from optimization.plot_Sf_histogram import plot_Sf_histogram
from optimization.random_individual import random_individual
from optimization.tournament_select import tournament_select


__all__ = [
    "brute_force_search",
    "evaluate_stacking",
    "evolve",
    "mutate",
    "one_point_crossover",
    "plot_GA_convergence",
    "plot_Sf_histogram",
    "random_individual",
    "tournament_select",
]
