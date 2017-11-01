# Generate protein secondary structure scheme from SS sequence of PDB database.
# This script assumes the input file only contains protein secondary structure 
# info (may in multiple lines) like the following:
#"      SS   SS SS SEEEEEEEE SSS  EEEEEEESSHHHHHHHHHHHHTT SSS  EEE  BTTTTEEEEE
#E  "
#
# Author: Qi Wang (wang2qi@mail.uc.edu)

import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import re

class DrawPorteinSSonXaxis(object):
	def __init__(self, ss_inp_name):
		if len(plt.get_fignums()):
			print "DRAW_SS_INFO> New instance of Draw_Portein_SS() created, make sure:"
			print "DRAW_SS_INFO> 1. The bottom X-ticks have been removed."
			print "DRAW_SS_INFO> 2. The x axis limit corresponds to the first and last residues."
		else:
			print "WARNING> No user-plotte figure was found."
			print "WARNING> Seoncdary structure legend will be plotted based on empty figure."
			print "DRAW_SS_INFO> Make sure to add the SS legend after "
		ss_info_raw = ''
		with open(ss_inp_name, 'r') as ss_inp_file:
			for each_line in ss_inp_file:
				ss_info_raw += each_line.rstrip('\n')
		self.ss_info_new = ss_info_raw.replace(" ", "-")
		self.x_min, self.x_max = plt.gca().get_xlim()
		self.y_min, self.y_max = plt.gca().get_ylim()
		self.re_beta_match  = re.compile("E+")
		self.re_alpha_match = re.compile("H+")
	def __draw_alpha(self, a_start, a_end, y_max, y_min):
		delta_y = y_max - y_min
		alpha_y_offset = -1. * delta_y * 0.04
		alpha_rectangle_thickness = delta_y * 0.03
		alpha_rectangle_linewidth = 2.
		plt.gca().add_patch(mpatches.Rectangle((a_start, alpha_y_offset), a_end-a_start, 
			alpha_rectangle_thickness, 
			clip_on = False, 
			linewidth = alpha_rectangle_linewidth, 
			hatch = '/', # Comment this line if "hatch" is not needed.
			facecolor = '#FFEB3B')
		)
	def __draw_beta(self, b_start, b_end, y_max, y_min):
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
	def __draw_other(self, x_max, x_min, y_max, y_min):
		delta_y = y_max - y_min
		other_y_offset = -1. * delta_y * 0.03
		other_rectangle_thickness = delta_y * 0.01
		plt.gca().add_patch(mpatches.Rectangle((x_min, other_y_offset), x_max-x_min, 
			other_rectangle_thickness, 
			clip_on = False, 
			color = 'black')
		)
	def draw(self):
		self.__draw_other(self.x_max, self.x_min, self.y_max, self.y_min)
		for hit_alpha_match in self.re_alpha_match.finditer(self.ss_info_new):
			self.__draw_alpha(hit_alpha_match.start()+1, hit_alpha_match.end()+1, self.y_max, self.y_min)
		for hit_beta_match in self.re_beta_match.finditer(self.ss_info_new):
			self.__draw_beta(hit_beta_match.start()+1, hit_beta_match.end()+1, self.y_max, self.y_min)

if __name__ == "__main__":
	from random import randint
# Generate data for test.
	test_ss_name = "test_draw_protein_ss.dat"
	x_data = range(150)
	y_data = [randint(0,150) for _ in range(150)]
# Make the plot, then add SS legend.
	plt.plot(x_data, y_data)
	plt.xlim(min(x_data), max(x_data))	# reszie the x-axis.
	plt.xticks([])	# remove xticks to avoid overlapping with SS legend.
	test_ss = DrawPorteinSSonXaxis(test_ss_name) # add the SS legend AFTER the plot.
	test_ss.draw()
	plt.savefig(filename='test_draw_protein_ss.png', dpi=150, bbox_inches='tight')