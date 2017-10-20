# Generate protein secondary structure scheme from SS sequence of PDB database.
# This script assumes the input file only contains protein secondary structure 
# info (may in multiple lines) like the following:
#"      SS   SS SS SEEEEEEEE SSS  EEEEEEESSHHHHHHHHHHHHTT SSS  EEE  BTTTTEEEEE
#E  "
##################################################
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import re

# sub function to draw alpha-helices
def draw_alpha(a_start, a_end, y_max, y_min):
	delta_y = y_max - y_min
	alpha_y_offset = -1. * delta_y * 0.04
	alpha_rectangle_thickness = delta_y * 0.03
	alpha_rectangle_linewidth = 2.
	#
	plt.gca().add_patch(mpatches.Rectangle((a_start, alpha_y_offset), a_end-a_start, 
		alpha_rectangle_thickness, 
		clip_on = False, 
		linewidth = alpha_rectangle_linewidth, 
		hatch = '/',
		facecolor = '#FFEB3B')
	)

# sub function to draw beta sheets
def draw_beta(b_start, b_end, y_max, y_min):
	delta_y = y_max - y_min
	beta_y_offset = -1. * delta_y * 0.025
	beta_body_width = delta_y * 0.03
	beta_head_width = beta_body_width
	beta_head_length = 1
	beta_overall_linewidth = 2.
	plt.gca().add_patch(mpatches.FancyArrow(b_start, beta_y_offset, b_end-b_start, 0, 
		width = beta_body_width,
		head_width = beta_head_width,
		head_length = beta_head_length,
		linewidth = beta_overall_linewidth,
		clip_on = False, 
		linestyle = 'solid',
		edgecolor = "black",
		length_includes_head = True,
		facecolor = '#9C27B0')
	)

# sub function to draw other secondary structures as line
def draw_other(x_max, x_min, y_max, y_min):
	delta_y = y_max - y_min
	other_y_offset = -1. * delta_y * 0.03
	other_rectangle_thickness = delta_y * 0.01
	plt.gca().add_patch(mpatches.Rectangle((x_min, other_y_offset), x_max-x_min, 
		other_rectangle_thickness, 
		clip_on = False, 
		color = 'black')
	)

# main function to retrieve SS from fasta-like files to add SS-info under X-axis.
def draw_protein_ss(ss_inp_name):
	print "DRAW_SS_INFO> Make sure to remove bottom X-ticks!"
	ss_info_raw = ''
	with open(ss_inp_name, 'r') as ss_inp_file:
		for each_line in ss_inp_file:
			ss_info_raw += each_line.rstrip('\n')
	ss_info_new = ss_info_raw.replace(" ", "-")
	#
	x_min, x_max = plt.gca().get_xlim()
	y_min, y_max = plt.gca().get_ylim()
	re_beta_match  = re.compile("E+")
	re_alpha_match = re.compile("H+")
	# Other secondary structures.
	draw_other(x_max, x_min, y_max, y_min)
	# Alpha helices
	for hit_alpha_match in re_alpha_match.finditer(ss_info_new):
		draw_alpha(hit_alpha_match.start()+1, hit_alpha_match.end()+1, y_max, y_min)
	# Beta sheets
	for hit_beta_match in re_beta_match.finditer(ss_info_new):
		draw_beta(hit_beta_match.start()+1, hit_beta_match.end()+1, y_max, y_min)
