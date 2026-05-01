# Beam FE Static Analysis (EB / CLT)

```

****** Laminate properties ******

Number of plies: N = 4
Ply orientations (deg): [45.0, 0.0, 0.0, 45.0]
Laminate thickness H = 0.800 mm
z coordinates (mm): [-0.400, -0.200, 0.000, 0.200, 0.400]

-- Laminate rigidities --

A (10^6 N/m):
      87.727    17.773    15.888
      17.773    24.175    15.888
      15.888    15.888    19.089

B (N):
       0.000     0.000     0.000
       0.000     0.000     0.000
       0.000     0.000     0.000

D (10^-3 N-m):
    2797.770  1557.842  1482.898
    1557.842  1950.400  1482.898
    1482.898  1482.898  1628.050

-- Laminate compliances --

a (10^-9 m/N):
      13.771    -5.720    -6.701
      -5.720    93.696   -73.224
      -6.701   -73.224   118.908

b (10^-3 1/N):
      -0.000     0.000    -0.000
       0.000    -0.000     0.000
      -0.000     0.000    -0.000

d (1/N-m):
       0.727    -0.251    -0.433
      -0.251     1.754    -1.369
      -0.433    -1.369     2.256

-- Mass moments of inertia --
  I0 = 1.27 kg/m^2
  I1 = 1.355e-20 kg/m
  I2 = 6.775e-08 kg

-- Effective in-plane elastic moduli --
  ExBar   = 90.77 GPa
  EyBar   = 13.34 GPa
  GxyBar  = 10.51 GPa
  NuxyBar = 0.415
  NuyxBar = 0.061

-- Effective flexural elastic moduli --
  Exfl    = 32.24 GPa
  Eyfl    = 13.36 GPa


Beam cross-section:
W (mm)        :     25.000
H (mm)        :      0.800
EI (N.m^2)    :     0.0344

  Array of element lengths [L]
       0.150
       0.150

K =
         122.269         9.170      -122.269         9.170         0.000         0.000
           9.170         0.917        -9.170         0.459         0.000         0.000
        -122.269        -9.170       244.538         0.000      -122.269         9.170
           9.170         0.459         0.000         1.834        -9.170         0.459
           0.000         0.000      -122.269        -9.170       122.269        -9.170
           0.000         0.000         9.170         0.459        -9.170         0.917

------------------------------------------------
  Solving the global system of equations
------------------------------------------------

D =
       0.000
       0.000
      -0.409
       0.000
       0.000
       0.000

F =
        50.000
         3.750
      -100.000
         0.000
        50.000
        -3.750

x =  100.0 mm   kappa_beam =    36.3497 1/m
  kappa_x_CLT (1/m):   -36.3497
  kappa_y     (1/m):    12.5560
  kappa_xy    (1/m):    21.6723

Sf_min                       :      0.578
  Layer where Sf_min occurs k:          1
  z (mm)                     :     -0.400
  z/H                        :     -0.500

Saved 7 figure(s) to /Users/vel/CompositesTextbook/BookProposalCode/results/run_laminated_beam_fe_static/
```
