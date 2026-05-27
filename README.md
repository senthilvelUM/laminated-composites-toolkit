# Companion Python Toolkit — *Laminated Composite Structures: Modeling, Simulation, and Optimization*

### Senthil S. Vel &nbsp;·&nbsp; Serge R. Maalouf

Python companion to the textbook *Analysis of Laminated Composite
Structures: Modeling, Simulation, and Optimization*. The toolkit covers
ply mechanics, classical lamination theory, three failure criteria,
progressive-failure analysis, stacking-sequence optimization, and
finite-element analysis of laminated beams and plates. The focus is
**transparent, single-purpose functions** that students can read
end-to-end alongside the corresponding chapters in the textbook.

## What's in here

| Layer | Folder / runner | Use it when… |
|---|---|---|
| Material → ply | `materials/` (YAML) + `ply/` + `run_ply.py` | learning ply mechanics: $[Q]$, $[\bar Q]$, off-axis transformations, three failure criteria (Tsai–Wu, max-stress, Hashin) and per-mode failure diagnostics |
| Plies → laminate | `laminate/` + `run_laminate.py` | computing $[A]$, $[B]$, $[D]$, mass moments $I_0, I_2$, through-thickness stresses, first-ply safety factor (any of the three criteria) |
| Stacking-sequence optimization | `optimization/` + `run_stacking_optimization_brute_force.py`, `run_stacking_optimization_genetic_algorithm.py` | given $(N, M)$, search for the stacking sequence that maximizes the first-ply safety factor (brute-force baseline + integer-coded GA) |
| Progressive failure analysis | `progressive_failure/` + 4 `run_coupon_*_pfa.py` / `run_bending_*_pfa.py` runners | track the full ply-failure sequence from FPF to LPF via total ply discount; load- or displacement-controlled coupon, moment- or curvature-controlled beam |
| Beam-FE | `fe_beams_clt/`, `fe_beams_clt_general/`, `fe_beams_fsdt/` + 9 `run_fe_beam_*.py` runners | static & vibration of laminated beams (Euler–Bernoulli or Timoshenko) |
| Plate-FE | `fe_plates_clt/`, `fe_plates_fsdt/` + 4 `run_fe_plate_*.py` runners | static & vibration of laminated plates (Kirchhoff/MZC or Mindlin/FSDT) |
| Textbook examples | `worked_examples/example_<topic>_<n>.py` | one-to-one Python reproductions of numbered worked examples from the theory chapters; outputs land in `worked_examples/results/` (kept separate from the main `results/`) |

## Quick start

```bash
pip install -r requirements.txt

# Single-ply analysis
python3 run_ply.py

# Full laminate (A, B, D, through-thickness, first-ply failure)
python3 run_laminate.py

# Stacking-sequence optimization: brute-force enumeration (N=4)
python3 run_stacking_optimization_brute_force.py

# Stacking-sequence optimization: integer-coded GA (default N=8)
python3 run_stacking_optimization_genetic_algorithm.py

# Progressive failure analysis: tensile coupon under increasing elongation
python3 run_coupon_elongation_pfa.py

# Progressive failure analysis: laminate beam under increasing curvature
python3 run_bending_curvature_pfa.py

# Simply-supported [0/90/90/0] CFRP plate, uniform pressure, MZC element
python3 run_fe_plate_clt_static.py

# Same plate, vibration analysis with mode shapes
python3 run_fe_plate_clt_vib.py
```

Every runner saves its output to `<runner_dir>/results/<runner_name>/`,
i.e. project-root runners write to `results/<runner_name>/` and
textbook examples in `worked_examples/` write to `worked_examples/results/<runner_name>/`.
The markdown transcript lives at `output.md` and any figures the runner
produces are saved alongside it as `fig01_*.png`, `fig02_*.png`, …. One
folder per analysis; nothing gets mixed across runners.

## Suggested reading order

1. **Start with `run_ply.py`.** Single ply, single material, single
   orientation. Read the runner end-to-end while consulting the theory
   chapter; you'll see every $[Q]$, $[\bar Q]$, and stress-transformation
   matrix printed explicitly.
2. **Then `run_laminate.py`.** Stack four plies and compute the laminate
   $[ABD]$, mass moments, and through-thickness Tsai–Wu safety factors.
3. **Then the optimization runners.** `run_stacking_optimization_brute_force.py`
   inverts the question of `run_laminate.py`: given the loads, what
   stacking sequence maximizes the first-ply safety factor? It
   enumerates every sequence in `12^N` (small `N`) and establishes
   the global optimum. `run_stacking_optimization_genetic_algorithm.py` runs a tiny
   integer-coded GA on the same problem; at small `N` it converges
   to the brute-force optimum, then scales to a problem brute force
   can't touch (`N=8` ⇒ 4×10⁸ stackings, GA explores 0.0004% of
   them in under a second).
4. **Then the progressive-failure runners.** Where
   `run_laminate.py` reports first-ply failure (FPF), the four PFA
   runners track the *full* failure sequence to last-ply failure
   (LPF) using total ply discount.  Two pairs by control mode:
   `run_coupon_load_pfa.py` (ramp `P`, horizontal `δ`-jumps) +
   `run_coupon_elongation_pfa.py` (ramp `δ`, sawtooth `P`-drops);
   `run_bending_moment_pfa.py` (ramp `M`, horizontal `κ`-jumps) +
   `run_bending_curvature_pfa.py` (ramp `κ`, sawtooth `M`-drops).
   The same physical events appear in both control modes — only
   the trajectory differs.  Default `[0/90]_s` coupon gives
   the canonical LPF/FPF ≈ 2 result.
5. **Then a beam-FE runner.** `run_fe_beam_clt_static.py` is the gentlest
   entry point — symmetric laminate, Euler–Bernoulli kinematics, 2 DOFs
   per node, cubic-Hermite shape functions. Walk through it slowly: it's
   the same FE pattern (mesh → BCs → loads → assemble → solve →
   post-process) you'll use everywhere else.
6. **Then a plate-FE runner.** `run_fe_plate_clt_static.py` extends the
   FE pattern to 2D with the four-noded MZC nonconforming plate
   element. The corresponding theory is in
   `reference/theory/FE_formulation_2D_plate_V4.tex`.
7. **Then FSDT versions.** `run_fe_beam_fsdt_static.py` and
   `run_fe_plate_fsdt_static.py` introduce shear deformation and the
   selective-reduced-integration trick that beats locking. Compare the
   default thin-plate result with `shear_integration="full"` to see
   locking in action; the chapter
   `reference/theory/FE_formulation_2D_plate_FSDT_V1.tex` explains why.
8. **Then vibration.** `run_fe_<beam|plate>_<theory>_vib.py` adds mass
   matrices and a generalized eigensolve, with FE-vs-Navier comparison.

## Project conventions

- **1-based labels.** Nodes, elements, and degrees of freedom are
  numbered from 1 at every point a student reads or modifies an array.
  Runners use 1-padded numpy arrays so that `D[5]` accesses the 5th
  global DOF directly. Internally the FE machinery stores tight
  0-based matrices; the translation is invisible to the runner.
- **One concept per function, one function per file.** Each FE
  toolkit holds 9–11 files containing **only** the kinematics-specific
  code (`ke_plate.py`, `me_plate_*.py`, `pressure_load_plate.py`, …).
  Grep for a function name and you'll find its source immediately.
  Generic FE machinery (assembly, EDOF tables, linear solver,
  eigensolver) lives once in `common/` and is shared by every toolkit.
  A runner does `from common import *` for the generic pieces, then
  `from fe_plates_clt import *` for the element-specific ones.
- **Naming.** Folder pattern `fe_<beams|plates>_<theory>[_<scope>]/`,
  runner pattern `run_fe_<beam|plate>_<theory>_<analysis>[_<variant>].py`.
  The `_general` qualifier in `fe_beams_clt_general/` means "any
  laminate" (relaxes the symmetric-only restriction); kinematics are
  still classical (CLT/Euler–Bernoulli).
- **Theory ↔ code parallelism.** Each FE chapter under `reference/theory/` has
  numbered equations whose labels are referenced from the
  corresponding code. The plate-FSDT chapter ends with a "Code map"
  paragraph that names the implementing functions one-to-one.

## Pedagogical toggles in the runners

Each runner exposes a small block of flags near the top of the file
(above `# DEFINE THE LAMINATE`) so students can experiment without
touching the rest of the script. Common toggles:

| Toggle | Toolkits | Values |
|---|---|---|
| `failure_criterion` | all laminate-level runners (`run_ply`, `run_laminate`, opt, PFA) | `"TsaiWu"` (default, interaction-aware quadratic envelope), `"MaxStress"` (decoupled per-component), or `"Hashin"` (per-mode quadratic with within-mode interaction). Threaded through every `Sf`-computing function; through-thickness axis labels track the choice |
| `shear_integration` | FSDT-beam, FSDT-plate | `"reduced"` (default, locking-free) or `"full"` (locks for thin elements — pedagogical counter-example) |
| `mass_matrix_type` | all vibration runners | `"consistent"` (more accurate at low modes) or `"lumped"` (diagonal, simpler) |
| `include_rotary_inertia` | EB-beam vib, CLT-plate vib | `True`/`False` (Rayleigh-beam / Rayleigh-plate refinement; default `False` because the CLT formulation is fine without it on slender problems). For FSDT vibration the rotary term is intrinsic and added unconditionally — turning it off would make the mass matrix singular |
| GA hyperparameters (`pop_size`, `n_generations`, `crossover_rate`, `mutation_rate`, `tournament_k`, `n_elite`, `seed`) | `run_stacking_optimization_genetic_algorithm.py` | Each annotated inline with its literature-typical range; defaults are mid-range textbook neutrals. Convergence plot makes the effect of any change immediate |
| `verbose` (on `assemble`, `generate_edofs`, `display_laminate_properties`) | all runners | `False` by default — set to `True` to see the assembly mechanics step by step (useful when first learning) |

## Verifying the toolkits

Two automated test scripts cover the plate-FE elements:

- `validate_fe_plate.py` — symmetry of $K$ and $k_e$, three
  constant-curvature patch tests, Kirchhoff–Love convergence for an
  isotropic SS plate.
- `validate_fe_plate_fsdt.py` — symmetry, patch tests, **shear-locking
  demonstration** (`shear_integration="full"` versus `"reduced"`),
  Navier convergence.

Both should print `ALL TESTS PASSED` in under a second.

## Repository layout

```
python_toolkit/
├── README.md                    ← you are here
├── requirements.txt             ← three packages: numpy, matplotlib, pyyaml
│
├── materials/                   ← YAML material files (CFRP, GFRP, foams)
├── ply/                         ← create_ply, three failure criteria, mode diagnostic, off-axis plots
├── laminate/                    ← create_laminate, ABD, through-thickness analysis (linear-elastic)
├── optimization/                ← stacking-sequence opt: fast evaluator, GA operators, brute-force search
├── progressive_failure/         ← progressive failure analysis: ply discount, PFA loop
├── common/                      ← shared display + generic FE machinery (assemble, solve, etc.)
│
├── fe_beams_clt/                ← Euler-Bernoulli beam FE (sym laminate)
├── fe_beams_clt_general/        ← Euler-Bernoulli beam FE (any laminate, 3 DOFs/node)
├── fe_beams_fsdt/               ← Timoshenko beam FE (sym laminate, shear deformation)
├── fe_plates_clt/               ← Kirchhoff/MZC plate FE
├── fe_plates_fsdt/              ← Mindlin/FSDT plate FE
│
├── run_ply.py                   ← single-ply analysis
├── run_laminate.py              ← multi-ply laminate analysis
├── run_stacking_optimization_brute_force.py    ← stacking-sequence opt: brute-force baseline
├── run_stacking_optimization_genetic_algorithm.py       ← stacking-sequence opt: integer-coded GA
├── run_coupon_load_pfa.py       ← PFA: tensile coupon, load controlled
├── run_coupon_elongation_pfa.py ← PFA: tensile coupon, displacement controlled (sawtooth)
├── run_bending_moment_pfa.py    ← PFA: laminate beam, moment controlled
├── run_bending_curvature_pfa.py ← PFA: laminate beam, curvature controlled (sawtooth)
├── run_fe_beam_*.py             ← 9 beam-FE runners (static + vibration)
├── run_fe_plate_*.py            ← 4 plate-FE runners (static + vibration)
├── validate_fe_plate*.py        ← element-level test suites
│
├── worked_examples/                    ← textbook-example runners (kept separate from main runners)
│   ├── CLT_example_strain_variation.py   ←   linear-through-thickness strain under combined extension + bending
│   ├── CLT_example_stress_variation.py   ←   stress distribution through a [45/0/-45] laminate
│   └── results/<runner_name>/            ←   per-example outputs (mirrors the project-root results/ pattern)
│
├── reference/theory/                      ← LaTeX chapters with the underlying theory
├── reference/FELT_code_snipetts/          ← reference snippets (read-only; not part of the toolkit)
└── results/                     ← runner output (auto-generated, .gitignored)
    └── <runner_name>/           ←   one subfolder per runner: output.md + figXX.png
```

## Materials shipped

- `unidirectional_carbon_epoxy` (IM7/8552 properties)
- `unidirectional_glass_epoxy`
- `fabric_carbon_epoxy`
- `fabric_glass_epoxy`
- `foam_core` (PMI-foam, used in sandwich-panel runners)

Material files live in `materials/` as YAML with a fixed schema; SI
units (Pa, kg/m³). Add a new material by dropping in a new YAML file
with the same fields.

## Where to look when something doesn't work

- **`ImportError: cannot find module …`** — you launched a runner from
  a directory other than the project root. Each runner does
  `sys.path.insert(0, "fe_<toolkit>")` relative to the cwd; run from
  the project root.
- **`UserWarning: FigureCanvasAgg is non-interactive`** — running
  headlessly. Already suppressed by the project's `show_figures()`
  helper; if you still see it, you're probably calling `plt.show()`
  directly somewhere.
- **Silent zero in a 1-padded array** — every array a runner touches
  has a dummy slot at index 0; `D[0] == 0` always. Index from 1.

## Further reading

- `reference/theory/FE_formulation_2D_plate_V4.tex` — Kirchhoff/MZC plate theory.
- `reference/theory/FE_formulation_2D_plate_FSDT_V1.tex` — Mindlin/FSDT plate
  theory, with worked examples and a code map at the end.

## License

Released under the MIT License — see [LICENSE](LICENSE).
