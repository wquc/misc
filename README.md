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
