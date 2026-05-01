# Stacking-sequence optimisation -- integer-coded GA

```
Problem setup
------------------------------------------------------------
  Material        : unidirectional_carbon_epoxy
  N_plies         : 8
  Ply thickness   : 0.125 mm
  Total thickness : 1.000 mm
  Angle set       : [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165] deg (12 values)
  Loads (N/m)     : Nx=500 kN/m, Ny=0 kN/m, Nxy=100 kN/m
  Loads (N)       : Mx=0, My=0, Mxy=0

GA hyperparameters
------------------------------------------------------------
  pop_size        : 30
  n_generations   : 200
  crossover_rate  : 0.7
  mutation_rate   : 0.1250
  tournament_k    : 3
  n_elite         : 2
  seed            : 0

  Design space    : 12^8 = 429,981,696 stackings
  GA evaluations  : pop_size x (n_generations+1) = 6,030
  Coverage        : 0.0014% of design space

Optimisation summary
------------------------------------------------------------
  Wall time    : 1.44 s
  Eval rate    : 4,175 laminates/s

Best stacking sequence (max-min TsaiWu Sf):
  Angles (deg) : [30, 0, 0, 15, 15, 0, 0, 30]
  Sf_min       :      2.850

N_plies = 8 -> brute force is hopeless (429,981,696 stackings); skipping ground-truth check.

============================================================
Properties of the optimum laminate
============================================================

****** Laminate properties ******

Number of plies: N = 8
Ply orientations (deg): [30.0, 0.0, 0.0, 15.0, 15.0, 0.0, 0.0, 30.0]
Laminate thickness H = 1.000 mm
z coordinates (mm): [-0.500, -0.375, -0.250, -0.125, 0.000, 0.125, 0.250, 0.375, 0.500]

-- Laminate rigidities --

A (10^6 N/m):
     146.319    12.685    21.819
      12.685    12.619     5.311
      21.819     5.311    14.331

B (N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000    -0.000

D (10^-3 N-m):
   10719.381  1652.767  2499.885
    1652.767  1334.172   866.316
    2499.885   866.316  1789.893

-- Laminate compliances --

a (10^-9 m/N):
       9.000    -3.886   -12.262
      -3.886    95.566   -29.500
     -12.262   -29.500    99.382

b (10^-3 1/N):
      -0.000     0.000    -0.000
       0.000     0.000    -0.000
      -0.000    -0.000     0.000

d (1/N-m):
       0.143    -0.069    -0.166
      -0.069     1.126    -0.449
      -0.166    -0.449     1.007

-- Mass moments of inertia --
  I0 = 1.588 kg/m^2
  I1 = 0 kg/m
  I2 = 1.323e-07 kg

-- Effective in-plane elastic moduli --
  ExBar   = 111.11 GPa
  EyBar   = 10.46 GPa
  GxyBar  = 10.06 GPa
  NuxyBar = 0.432
  NuyxBar = 0.041

-- Effective flexural elastic moduli --
  Exfl    = 84.16 GPa
  Eyfl    = 10.65 GPa


Failure criterion: TsaiWu
Sf_min                       :      2.850
  Layer where Sf_min occurs k:          1
  z (mm)                     :     -0.500
  z/H                        :     -0.500

  Dominant failure mode at z_min:           shear
  Max-stress SF for the dominant mode:         3.627
  Per-mode max-stress safety factors:
    fiber_tension           5.732
    fiber_compression       inactive
    matrix_tension          inactive
    matrix_compression      5.895
    shear                   3.627

Saved 5 figure(s) to /Users/vel/CompositesTextbook/BookProposalCode/results/run_stacking_optimization_genetic_algorithm/
```
