# Stacking-sequence optimisation -- exhaustive enumeration

```
Problem setup
------------------------------------------------------------
  Material        : unidirectional_carbon_epoxy
  N_plies         : 4
  Ply thickness   : 0.125 mm
  Total thickness : 0.500 mm
  Angle set       : [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165] deg (12 values)
  Loads (N/m)     : Nx=500 kN/m, Ny=0 kN/m, Nxy=100 kN/m
  Loads (N)       : Mx=0, My=0, Mxy=0

12^N scaling of the design space:
------------------------------------------------------------
  N = 2:              144 stacking sequences
  N = 3:            1,728 stacking sequences
  N = 4:           20,736 stacking sequences  <-- this run
  N = 5:          248,832 stacking sequences
  N = 6:        2,985,984 stacking sequences
  N = 7:       35,831,808 stacking sequences
  N = 8:      429,981,696 stacking sequences

This run evaluates all 20,736 sequences.

Optimisation summary
------------------------------------------------------------
  Evaluations  : 20,736
  Wall time    : 2.52 s
  Eval rate    : 8,235 laminates/s

Best stacking sequence (max-min TsaiWu Sf):
  Angles (deg) : [15, 0, 0, 15]
  Sf_min       :      1.487

Reference stacks under the same loads:
  [0]_n              [0, 0, 0, 0] -> Sf_min = 0.4620
  [90]_n             [90, 90, 90, 90] -> Sf_min = 0.0688
  [0,90]_(n/2)       [0, 90, 0, 90] -> Sf_min = 0.2513
  [+45,-45]_(n/2)    [45, 135, 45, 135] -> Sf_min = 0.1563

============================================================
Properties of the optimum laminate
============================================================

****** Laminate properties ******

Number of plies: N = 4
Ply orientations (deg): [15.0, 0.0, 0.0, 15.0]
Laminate thickness H = 0.500 mm
z coordinates (mm): [-0.250, -0.125, 0.000, 0.125, 0.250]

-- Laminate rigidities --

A (10^6 N/m):
      79.177     3.960     9.092
       3.960     5.058     0.838
       9.092     0.838     4.783

B (N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000     0.000

D (10^-3 N-m):
    1570.718   119.728   331.478
     119.728   109.713    30.558
     331.478    30.558   136.868

-- Laminate compliances --

a (10^-9 m/N):
      16.460    -7.932   -29.901
      -7.932   207.458   -21.277
     -29.901   -21.277   269.659

b (10^-3 1/N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000     0.000

d (1/N-m):
       1.338    -0.594    -3.107
      -0.594     9.983    -0.789
      -3.107    -0.789    15.007

-- Mass moments of inertia --
  I0 = 0.794 kg/m^2
  I1 = 0 kg/m
  I2 = 1.654e-08 kg

-- Effective in-plane elastic moduli --
  ExBar   = 121.51 GPa
  EyBar   = 9.64 GPa
  GxyBar  = 7.42 GPa
  NuxyBar = 0.482
  NuyxBar = 0.038

-- Effective flexural elastic moduli --
  Exfl    = 71.77 GPa
  Eyfl    = 9.62 GPa


Failure criterion: TsaiWu
Sf_min                       :      1.487
  Layer where Sf_min occurs k:          2
  z (mm)                     :     -0.125
  z/H                        :     -0.250

  Dominant failure mode at z_min:           shear
  Max-stress SF for the dominant mode:         1.560
  Per-mode max-stress safety factors:
    fiber_tension           3.127
    fiber_compression       inactive
    matrix_tension          inactive
    matrix_compression      4.794
    shear                   1.560

Saved 5 figure(s) to /Users/vel/CompositesTextbook/BookProposalCode/results/run_stacking_optimization_brute_force/
```
