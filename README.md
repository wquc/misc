# MISC
Miscellaneous scripts that make life easier

## 0-dssp.py

Draw protein secondary structure legend on X axis as is shown in the figure:

<img src="demo/0-draw-protein-ss.png" width="60%" height="60%" alt="image of test_draw_protein_ss" align="center" />

The asthetics are set by `3-pubfig.py`.

## 1-data-picker.py

Print the **x and y coordinates** of a selected point, or the **residue**(name+index) **and property** of that residue if a **FASTA file** and **offset** are specified, for example:

<img src="demo/1-pick-point.png" width="60%" height="60%" alt="image of test_pick_point" align="center" />

## 2-retrive-viewpoint.py
For macromolecules with irregular shapes without proper alignment with respect to principal axis (X, Y or Z), it will be easier to use manually determined view perspectives. To re-use this view point, it is handy to save the matrix.

## 3-pubfig.py
Publication quality asthetics setup for scientific data visualization as shown below.

<img src="demo/3-pubfig-demo.png" width="60%" height="60%" alt="image of pubfig" align="center" />

- Possible error: matplotlib - Font family [u'sans-serif'] not found

- Solution:
1. `sudo apt-get install msttcorefonts -qq`
2. Then delete the content of `.cache/matplotlib`

## 4-qatdcd.cpp
Similar as CatDCD (https://www.ks.uiuc.edu/Development/MDTools/catdcd/) but CHARMM compatible

## 5-nfile.cpp
Edit the `NFILE` entry of dcd header such that it corresponds to the actual frames of that trajectory file. Useful when dealing with CHARMM AFM simulations.

## 6-overlay.py
Overlay foreground and background images for fancy result visualization. Note that RGB codes for white color rendered by VMD is not always `255, 255, 255` (sometimes `254, 254, 254`). Thus tools like `gpick` is helpful to determine the actualy color codes to setup transparency pixels in the foreground images.

<img src="demo/6-demo-overlay.gif" width="60%" height="60%" alt="image of overlay" align="center" />

## 7-symm-avrg.py
Calculate symmetrical average coordinate after rotation along an axis.

- Input structure before averaging:

<img src="demo/7-symm-avrg-before.png" width="40%" height="40%" alt="structure before averaging" align="center" />

- Averaged structure after 7 rotations:

<img src="demo/7-symm-avrg-after.png" width="40%" height="40%" alt="structure after averaging" align="center" />

## 8-measure-pore
### 8.1-medial-axis.cpp
Voronoi tessellation of polygon defined by connecting atoms of interest encompassing the pore of molecular machines.

input demo:<br>
```
51.737  29.350
46.354  26.340
47.869  21.474
52.073  16.979
57.530  19.933
55.936  24.811
```
### 8.2-plot-medial.py
Draw the tessellated polygon with the largest inscribed circle as shown below:

<img src="demo/8-medial-demo.png" width="80%" height="80%" alt="Voronoi tessellation of polygon of pore" align="center" />

## 9-calc-rmsf
Calculate root mean square fluctuations (RMSF).
Usage: 
1. Compile with `g++ calc-rmsf.cpp -o calc-rmsf`
2. Run with `./calc-rmsf ${mode} ${psfname} ${dcdname} ${outname}`

Currently implemented values for `mode` are `-1` (debugging with all atoms), `0` (CA atoms) and `1` (heavy atoms).

## 10-read-traj.py
Processing DCD format molecular dynamics trajectories with Python.

## 11-orient-channel.py
For a macromolecule machine with a channel, put its geometric center at `(0, 0, 0)` and rotate the system such that the channel vector is aligned with a certain principal axis in the Cartesian coordinate system.

The following demo uses Hsp104 (PDB:5VJH) as an example, where the channel is defined as the best fitted 3D line from the coordinates of the CA atoms of the substrate. The `channel.dat` has the following format:
```
137.456 120.919 80.596
136.939 121.250 84.346
135.002 123.114 87.020
...
121.993 129.784 156.530
```
and can be obtained by 
```
grep ' CA ' 5vjh.pdb | grep ' P ' | awk '{print $7, $8, $9}' > channel.dat
```

For a system without substrate present, channel residue atoms can also be used to find the channel vector. Below is a demo, where the origin `(0, 0, 0)` is shown as black bead and the arrow represents the Z axis.

<img src="demo/11-orient-channel.png" width="80%" height="80%" alt="Before and after alignment of channel" align="center" />