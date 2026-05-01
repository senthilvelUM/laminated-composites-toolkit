# Example 3.3 -- Design of a thin-walled [theta/-theta]_S laminated tube

```

Tube geometry and loading:
R  (mm)   :     50.000
L  (m)    :      0.500
P  (kN)   :     30.000
T  (kN.m) :      1.600

Force/moment resultants on a wall element:
Nx  (kN/m) :     95.493
Ny  (kN/m) :      0.000
Nxy (kN/m) :    101.859

Nxy / Nx = 1.067  (torsion-biased: Nxy > Nx)

============================================================
Part 1 -- Detailed walkthrough at theta = 45 deg
============================================================

--- Ply 1 ---

****** Ply properties ******

Material: Unidirectional Carbon/Epoxy (IM7/8552)
  type = unidirectional
  rho  = 1588.0 kg/m^3

-- Elastic properties --
  E1   = 167.40 GPa
  E2   = 9.50 GPa
  nu12 = 0.330
  nu21 = 0.019
  G12  = 4.80 GPa

-- Strength properties --
  F1t  = 2700.0 MPa
  F1c  = 1700.0 MPa
  F2t  = 70.0 MPa
  F2c  = 200.0 MPa
  F6   = 90.0 MPa

-- Ply geometry --
  theta = 45.0 deg
  h     = 0.200 mm

-- Reduced compliance matrix S (TPa^-1) --
       5.974    -1.971     0.000
      -1.971   105.263     0.000
       0.000     0.000   208.333

-- Reduced stiffness matrix Q (GPa) --
     168.441     3.154     0.000
       3.154     9.559     0.000
       0.000     0.000     4.800

-- Stress transformation matrix Ts --
       0.500     0.500     1.000
       0.500     0.500    -1.000
      -0.500     0.500     0.000

-- Strain transformation matrix Te --
       0.500     0.500     0.500
       0.500     0.500    -0.500
      -1.000     1.000     0.000

-- Inverse stress transformation matrix TsInv --
       0.500     0.500    -1.000
       0.500     0.500     1.000
       0.500    -0.500     0.000

-- Inverse strain transformation matrix TeInv --
       0.500     0.500    -0.500
       0.500     0.500     0.500
       1.000    -1.000     0.000

-- Off-axis compliance matrix SBar (TPa^-1) --
      78.907   -25.260   -49.645
     -25.260    78.907   -49.645
     -49.645   -49.645   115.180

-- Off-axis stiffness matrix QBar (GPa) --
      50.877    41.277    39.720
      41.277    50.877    39.720
      39.720    39.720    42.923

-- Elastic properties in the global (x-y) coordinate system --
  Ex   = 12.67 GPa
  Ey   = 12.67 GPa
  nuxy = 0.320
  Gxy  = 8.68 GPa


--- Ply 2 ---

****** Ply properties ******

Material: Unidirectional Carbon/Epoxy (IM7/8552)
  type = unidirectional
  rho  = 1588.0 kg/m^3

-- Elastic properties --
  E1   = 167.40 GPa
  E2   = 9.50 GPa
  nu12 = 0.330
  nu21 = 0.019
  G12  = 4.80 GPa

-- Strength properties --
  F1t  = 2700.0 MPa
  F1c  = 1700.0 MPa
  F2t  = 70.0 MPa
  F2c  = 200.0 MPa
  F6   = 90.0 MPa

-- Ply geometry --
  theta = -45.0 deg
  h     = 0.200 mm

-- Reduced compliance matrix S (TPa^-1) --
       5.974    -1.971     0.000
      -1.971   105.263     0.000
       0.000     0.000   208.333

-- Reduced stiffness matrix Q (GPa) --
     168.441     3.154     0.000
       3.154     9.559     0.000
       0.000     0.000     4.800

-- Stress transformation matrix Ts --
       0.500     0.500    -1.000
       0.500     0.500     1.000
       0.500    -0.500     0.000

-- Strain transformation matrix Te --
       0.500     0.500    -0.500
       0.500     0.500     0.500
       1.000    -1.000     0.000

-- Inverse stress transformation matrix TsInv --
       0.500     0.500     1.000
       0.500     0.500    -1.000
      -0.500     0.500     0.000

-- Inverse strain transformation matrix TeInv --
       0.500     0.500     0.500
       0.500     0.500    -0.500
      -1.000     1.000     0.000

-- Off-axis compliance matrix SBar (TPa^-1) --
      78.907   -25.260    49.645
     -25.260    78.907    49.645
      49.645    49.645   115.180

-- Off-axis stiffness matrix QBar (GPa) --
      50.877    41.277   -39.720
      41.277    50.877   -39.720
     -39.720   -39.720    42.923

-- Elastic properties in the global (x-y) coordinate system --
  Ex   = 12.67 GPa
  Ey   = 12.67 GPa
  nuxy = 0.320
  Gxy  = 8.68 GPa


--- Ply 3 ---

****** Ply properties ******

Material: Unidirectional Carbon/Epoxy (IM7/8552)
  type = unidirectional
  rho  = 1588.0 kg/m^3

-- Elastic properties --
  E1   = 167.40 GPa
  E2   = 9.50 GPa
  nu12 = 0.330
  nu21 = 0.019
  G12  = 4.80 GPa

-- Strength properties --
  F1t  = 2700.0 MPa
  F1c  = 1700.0 MPa
  F2t  = 70.0 MPa
  F2c  = 200.0 MPa
  F6   = 90.0 MPa

-- Ply geometry --
  theta = -45.0 deg
  h     = 0.200 mm

-- Reduced compliance matrix S (TPa^-1) --
       5.974    -1.971     0.000
      -1.971   105.263     0.000
       0.000     0.000   208.333

-- Reduced stiffness matrix Q (GPa) --
     168.441     3.154     0.000
       3.154     9.559     0.000
       0.000     0.000     4.800

-- Stress transformation matrix Ts --
       0.500     0.500    -1.000
       0.500     0.500     1.000
       0.500    -0.500     0.000

-- Strain transformation matrix Te --
       0.500     0.500    -0.500
       0.500     0.500     0.500
       1.000    -1.000     0.000

-- Inverse stress transformation matrix TsInv --
       0.500     0.500     1.000
       0.500     0.500    -1.000
      -0.500     0.500     0.000

-- Inverse strain transformation matrix TeInv --
       0.500     0.500     0.500
       0.500     0.500    -0.500
      -1.000     1.000     0.000

-- Off-axis compliance matrix SBar (TPa^-1) --
      78.907   -25.260    49.645
     -25.260    78.907    49.645
      49.645    49.645   115.180

-- Off-axis stiffness matrix QBar (GPa) --
      50.877    41.277   -39.720
      41.277    50.877   -39.720
     -39.720   -39.720    42.923

-- Elastic properties in the global (x-y) coordinate system --
  Ex   = 12.67 GPa
  Ey   = 12.67 GPa
  nuxy = 0.320
  Gxy  = 8.68 GPa


--- Ply 4 ---

****** Ply properties ******

Material: Unidirectional Carbon/Epoxy (IM7/8552)
  type = unidirectional
  rho  = 1588.0 kg/m^3

-- Elastic properties --
  E1   = 167.40 GPa
  E2   = 9.50 GPa
  nu12 = 0.330
  nu21 = 0.019
  G12  = 4.80 GPa

-- Strength properties --
  F1t  = 2700.0 MPa
  F1c  = 1700.0 MPa
  F2t  = 70.0 MPa
  F2c  = 200.0 MPa
  F6   = 90.0 MPa

-- Ply geometry --
  theta = 45.0 deg
  h     = 0.200 mm

-- Reduced compliance matrix S (TPa^-1) --
       5.974    -1.971     0.000
      -1.971   105.263     0.000
       0.000     0.000   208.333

-- Reduced stiffness matrix Q (GPa) --
     168.441     3.154     0.000
       3.154     9.559     0.000
       0.000     0.000     4.800

-- Stress transformation matrix Ts --
       0.500     0.500     1.000
       0.500     0.500    -1.000
      -0.500     0.500     0.000

-- Strain transformation matrix Te --
       0.500     0.500     0.500
       0.500     0.500    -0.500
      -1.000     1.000     0.000

-- Inverse stress transformation matrix TsInv --
       0.500     0.500    -1.000
       0.500     0.500     1.000
       0.500    -0.500     0.000

-- Inverse strain transformation matrix TeInv --
       0.500     0.500    -0.500
       0.500     0.500     0.500
       1.000    -1.000     0.000

-- Off-axis compliance matrix SBar (TPa^-1) --
      78.907   -25.260   -49.645
     -25.260    78.907   -49.645
     -49.645   -49.645   115.180

-- Off-axis stiffness matrix QBar (GPa) --
      50.877    41.277    39.720
      41.277    50.877    39.720
      39.720    39.720    42.923

-- Elastic properties in the global (x-y) coordinate system --
  Ex   = 12.67 GPa
  Ey   = 12.67 GPa
  nuxy = 0.320
  Gxy  = 8.68 GPa


****** Laminate properties ******

Number of plies: N = 4
Ply orientations (deg): [45.0, -45.0, -45.0, 45.0]
Laminate thickness H = 0.800 mm
z coordinates (mm): [-0.400, -0.200, 0.000, 0.200, 0.400]

-- Laminate rigidities --

A (10^6 N/m):
      40.702    33.022     0.000
      33.022    40.702     0.000
       0.000     0.000    34.338

B (N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000     0.000

D (10^-3 N-m):
    2170.763  1761.163  1271.055
    1761.163  2170.763  1271.055
    1271.055  1271.055  1831.371

-- Laminate compliances --

a (10^-9 m/N):
      71.886   -58.322     0.000
     -58.322    71.886     0.000
       0.000     0.000    29.122

b (10^-3 1/N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000    -0.000

d (1/N-m):
       1.451    -0.990    -0.320
      -0.990     1.451    -0.320
      -0.320    -0.320     0.990

-- Mass moments of inertia --
  I0 = 1.27 kg/m^2
  I1 = 1.355e-20 kg/m
  I2 = 6.775e-08 kg

-- Effective in-plane elastic moduli --
  ExBar   = 17.39 GPa
  EyBar   = 17.39 GPa
  GxyBar  = 42.92 GPa
  NuxyBar = 0.811
  NuyxBar = 0.811

-- Effective flexural elastic moduli --
  Exfl    = 16.15 GPa
  Eyfl    = 16.15 GPa


Mid-surface strains and curvatures:
Epsilon0 (micro):
    6864.632
   -5569.348
    2966.350
Kappa    (1/m)  :
       0.000
       0.000
      -0.000

Ply-by-ply stresses and Tsai-Wu safety factor:

Ply 1 (theta = +45 deg) at z = -0.300 mm:
  sigma_x (MPa) :    237.191
  sigma_y (MPa) :    117.825
  tau_xy  (MPa) :    178.773
  sigma_1 (MPa) :    356.281
  sigma_2 (MPa) :     -1.265
  tau_12  (MPa) :    -59.683
  Sf (Tsai-Wu)  :      1.558

Ply 2 (theta = -45 deg) at z = -0.100 mm:
  sigma_x (MPa) :      1.541
  sigma_y (MPa) :   -117.825
  tau_xy  (MPa) :     75.875
  sigma_1 (MPa) :   -134.016
  sigma_2 (MPa) :     17.733
  tau_12  (MPa) :     59.683
  Sf (Tsai-Wu)  :      1.261

Ply 3 (theta = -45 deg) at z = +0.100 mm:
  sigma_x (MPa) :      1.541
  sigma_y (MPa) :   -117.825
  tau_xy  (MPa) :     75.875
  sigma_1 (MPa) :   -134.016
  sigma_2 (MPa) :     17.733
  tau_12  (MPa) :     59.683
  Sf (Tsai-Wu)  :      1.261

Ply 4 (theta = +45 deg) at z = +0.300 mm:
  sigma_x (MPa) :    237.191
  sigma_y (MPa) :    117.825
  tau_xy  (MPa) :    178.773
  sigma_1 (MPa) :    356.281
  sigma_2 (MPa) :     -1.265
  tau_12  (MPa) :    -59.683
  Sf (Tsai-Wu)  :      1.558

First-ply failure (Tsai-Wu):
  Sf_min            :      1.261
  Critical ply k    :          2
  Critical ply theta: -45 deg
  z at Sf_min (mm)  :     -0.200

============================================================
Part 2 -- Comparison across candidate angles
============================================================

 theta     eps_x^0   gamma_xy^0     sigma_1    sigma_2     tau_12    Sf_min    crit ply
 (deg)     (micro)      (micro)       (MPa)      (MPa)      (MPa)         -       theta
-----------------------------------------------------------------------------------------------
    15         896         8885     -241.25       7.71      41.64     1.804         -15
    30        2322         3813     -136.22      -6.74      33.61     2.760         -30
    45        6865         2966     -134.02      17.73      59.68     1.261         -45
    60       11238         3813     -226.02      83.06      52.37     0.689         -60

Best  candidate: theta = 30 deg, Sf_min = 2.760
Worst candidate: theta = 60 deg, Sf_min = 0.689  (FAILS: Sf_min < 1)

============================================================
Part 3 -- Continuous sweep of theta over [0, 90] deg
============================================================

Continuous optimum: theta = 26 deg, Sf_min = 2.965
(Best of the four candidates: theta = 30 deg, Sf_min = 2.760)

Saved 9 figure(s) to /Users/vel/CompositesTextbook/BookProposalCode/worked_examples/results/CLT_Example_3/
```
