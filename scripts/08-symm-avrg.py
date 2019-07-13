# -*- coding: utf-8 -*-
#!/usr/bin/env python

### Genrate symmetric averaged structure based on input coordinates
### Note: (1) The program takes CHARMM coordinate as input file
###       (2) The fold of symmetry will be determined from number of segments.
###       (3) Each segments should have EXACT the same number of atoms.
### Usage: Suppose the rotation is along Z-axis
###       ./sym-avrg.py input.cor 0 0 1

import numpy as np
import itertools
import sys
import re
import os

### Euler–Rodrigues rotation
def rot_mat(axis, theta):
    a = np.cos(0.5*theta)
    b, c, d = axis * np.sin(0.5*theta)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd,   2*(bc-ad),    2*(bd+ac)],
                     [  2*(bc+ad), aa+cc-bb-dd,    2*(cd-ab)],
                     [  2*(bd-ac),   2*(cd+ab), aa+dd-bb-cc]])

### CHARMM formatted coordinate
def write_chmcrd(out_name, header, natoms, 
	atomid, resnum, resname, atomtype, coord, segid, resid, weight):
	coord = coord.transpose()
	with open(out_name, 'w') as out_file:
		for hd in header:
			out_file.write("%s\n"%hd)
		out_file.write("%s\n"%natoms)
		for (atom, ires, resn, atomtype, crd, seg, resi, w) in \
			itertools.izip(atomid, resnum, resname, atomtype, coord, segid, resid, weight):
			out_file.write("%5d%5d %-4s %-4s%10.5f%10.5f%10.5f %-4s %-4d%10.5f\n" % \
				(atom, ires, resn, atomtype, crd[0], crd[1], crd[2], seg, resi, w))

### Process input
inp_name    = sys.argv[1]
rota_axis_x = float(sys.argv[2])
rota_axis_y = float(sys.argv[3])
rota_axis_z = float(sys.argv[4])

rot_axis = np.asarray([rota_axis_x, rota_axis_y, rota_axis_z])
rot_axis = rot_axis / np.linalg.norm(rot_axis)
out_pref = os.path.splitext(inp_name)[0]

### Format of CHARMM coordinate file
chmcrd_header   = []
chmcrd_natoms   = 0
chmcrd_atomid   = [] # I5
chmcrd_resnum   = [] # I5
                     # 1X
chmcrd_resname  = [] # A4
                     # 1X
chmcrd_atomtype = [] # A4
chmcrd_coord    = [] # 3(F10.5)
                     # 1X
chmcrd_segid    = [] # A4
                     # 1X
chmcrd_resid    = [] # A4
chmcrd_weight   = [] # F10.5

### Retrieve coordinate information
pattern_natoms = '^[0-9]+$'             # natom
pattern_coord  = '^\s*[0-9]+\s+[0-9]+'  # atomid & resid

with open(inp_name, 'r') as inp_file:
	for each_line in inp_file:
		if each_line.startswith('*'):
			chmcrd_header.append(each_line.strip())
		if re.match(pattern_natoms, each_line):
			chmcrd_natoms = int(each_line.strip())
		if re.match(pattern_coord, each_line):
			each_entry = each_line.split()
			chmcrd_atomid.append(int(each_entry[0]))
			chmcrd_resnum.append(int(each_entry[1]))
			chmcrd_resname.append(each_entry[2])
			chmcrd_atomtype.append(each_entry[3])
			chmcrd_coord.append(float(each_entry[4]))
			chmcrd_coord.append(float(each_entry[5]))
			chmcrd_coord.append(float(each_entry[6]))
			chmcrd_segid.append(each_entry[7])
			chmcrd_resid.append(int(each_entry[8]))
			chmcrd_weight.append(float(each_entry[9]))

### Retrive symmetry information
nfold = len(set(chmcrd_segid))
theta = np.radians(360./nfold)
shift = chmcrd_natoms / nfold

### Rotate and accumulate
coord = np.array(chmcrd_coord).reshape(chmcrd_natoms, 3).transpose()
avrg_coor = np.zeros(coord.shape)

for i in range(nfold):
	irot = i+1
	out_name = out_pref + "-rot%d.cor"%irot
	coord = np.dot(rot_mat(rot_axis, theta), coord)
	coord = np.roll(coord, -shift, axis=1)
	avrg_coor += coord

avrg_coor /= nfold
out_name = out_pref + "-avrg.cor"
write_chmcrd(out_name, chmcrd_header, chmcrd_natoms, chmcrd_atomid, 
		chmcrd_resnum, chmcrd_resname, chmcrd_atomtype, avrg_coor, 
		chmcrd_segid, chmcrd_resid, chmcrd_weight)