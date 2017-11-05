# MISC
Miscellaneous scripts that make life easier

## draw_protein_ss.py

Draw protein secondary structure legend on X axis as is shown in the figure:

<img src="test_draw_protein_ss.png" width="60%" height="60%" alt="image of test_draw_protein_ss" align="center" />

## pick_point.py

Print the **x and y coordinates** of a selected point, or the **residue**(name+index) **and property** of that residue if a **FASTA file** and **offset** are specified, for example:

![image of test_pick_point](test_pick_point.png) 

### Tips for Ubuntu users
```bash
mkdir -p "`python -m site --user-site`"
```

`cd` to that folder, `mkdir` new directory with a given module name and copy the .py file to that folder with a dummy `__init__.py` file to make it as a python package.
