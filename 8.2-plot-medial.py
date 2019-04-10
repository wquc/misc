import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import collections as mcollections
from matplotlib import colors as mcolors
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString

def plot_medial_axis(inp_name):
	## Read data into array ##
	trivial  = []
	segments = []
	vertices = []
	edges    = []
	with open(inp_name, 'r') as inp_file:
		for each_line in inp_file:
			if not len(each_line.strip()):
				continue
			each_entry = each_line.split()
			if each_entry[0]=="TRIV>":
				trivial.append((float(each_entry[1]), float(each_entry[2])))
			if each_entry[0]=="SGMT>":
				segments.append(LineString([(float(each_entry[1]), float(each_entry[2])), 
							     (float(each_entry[3]), float(each_entry[4]))]))
			if each_entry[0]=="VRTX>":
				vertices.append(Point(float(each_entry[1]), float(each_entry[2])))
			if each_entry[0]=="EDGE>":
				edges.append(LineString( [(float(each_entry[1]),float(each_entry[2])), 
							   			  (float(each_entry[3]),float(each_entry[4]))] ))
	## Data cleansing ##
	polygon   = Polygon([tv for tv in trivial])
	# Only keep vertices and edges inside polygon
	vertices  = [i for i in (vt for vt in vertices if polygon.contains(vt))]
	edges     = [eg for eg in edges if polygon.contains(eg)]
	dist_vrtx = [np.min([sgmt.distance(vrtx) for sgmt in segments]) for vrtx in vertices]
	# Collect info for plotting result
	r_max = np.max(dist_vrtx)
	v_max = np.argmax(dist_vrtx)
	coor_max = vertices[v_max].coords[:][0]
	print "R_max = %11.6f"%r_max
	print "coor_max = ", coor_max

	## Plot medial axis ##
	ax = plt.subplot()
	# Plot edges of Voronoi diagram
	lc_edges = mcollections.LineCollection(edges, colors='#D52A29', lw=5)
	ax.add_collection(lc_edges)
	# Plot outline of polygon
	lc_segments = mcollections.LineCollection(segments, colors='black', lw=5)
	ax.add_collection(lc_segments)
	# Plot max inscribed circle
	circle = plt.Circle(coor_max, r_max, color='#1E9CEF')
	ax.add_artist(circle)
	# misc.
	ax.autoscale()
	ax.set_frame_on(False)
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	ax.set_aspect('equal', adjustable='box')
	img_name = 'test.png'
	plt.savefig(img_name, dpi=800, transparent=True, bbox_inches='tight')

if __name__ == "__main__":
	inp_name = "vd_data_test.dat"
	plot_medial_axis(inp_name)