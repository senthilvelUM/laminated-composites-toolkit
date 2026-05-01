# Example 3.1 -- Stress distribution through the thickness of a [45/0/-45] laminate

```
Laminate H = 0.600 mm  (3 plies of 0.200 mm)
Stacking sequence (bottom -> top, deg): [45, 0, -45]

Epsilon0 (micro-strain):
    1000.000
       0.000
       0.000
Kappa    (1/m)         :
       1.000
       0.000
       0.000

Strain and stress at each ply boundary:

Ply 1 (theta = +45 deg), bottom:  z = -0.300 mm
  eps_x   (micro):    700.000
  sigma_x (MPa)  :     35.614
  sigma_y (MPa)  :     28.894
  tau_xy  (MPa)  :     27.804

Ply 1 (theta = +45 deg), top   :  z = -0.100 mm
  eps_x   (micro):    900.000
  sigma_x (MPa)  :     45.790
  sigma_y (MPa)  :     37.150
  tau_xy  (MPa)  :     35.748

Ply 2 (theta = +0 deg), bottom:  z = -0.100 mm
  eps_x   (micro):    900.000
  sigma_x (MPa)  :    151.597
  sigma_y (MPa)  :      2.839
  tau_xy  (MPa)  :      0.000

Ply 2 (theta = +0 deg), top   :  z = +0.100 mm
  eps_x   (micro):   1100.000
  sigma_x (MPa)  :    185.285
  sigma_y (MPa)  :      3.470
  tau_xy  (MPa)  :      0.000

Ply 3 (theta = -45 deg), bottom:  z = +0.100 mm
  eps_x   (micro):   1100.000
  sigma_x (MPa)  :     55.965
  sigma_y (MPa)  :     45.405
  tau_xy  (MPa)  :    -43.693

Ply 3 (theta = -45 deg), top   :  z = +0.300 mm
  eps_x   (micro):   1300.000
  sigma_x (MPa)  :     66.140
  sigma_y (MPa)  :     53.660
  tau_xy  (MPa)  :    -51.637

Saved 7 figure(s) to /Users/vel/CompositesTextbook/python_toolkit_intro/worked_examples/results/CLT_Example_1/
```
