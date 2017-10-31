# Modified from "data_browser.py" at 
# https://matplotlib.org/devdocs/gallery/event_handling/data_browser.html
# 
# Author: Qi Wang (wang2qi@mail.uc.edu)

import matplotlib.pyplot as plt

class PickPoint(object):
    def __init__(self, xArr, yArr):
    	self.xArr = xArr
    	self.yArr = yArr
        self.selected, = plt.gca().plot(self.xArr, self.yArr, 'o', 
        	markersize=12, alpha=0.5, color='yellow', visible=False)
    def onpick(self, event):
        self.dataind = event.ind
        self.print_coor()
        self.selected.set_visible(True)
        self.selected.set_data(self.xArr[self.dataind], self.yArr[self.dataind])
        plt.gcf().canvas.draw()
    def print_coor(self):
    	print '> Selected point: (%s, %s)'%(self.xArr[self.dataind], self.yArr[self.dataind])

class PickPointSequence(PickPoint):
	def __init__(self, xArr, yArr, fasta_name, fasta_offset):
		super(PickPointSequence, self).__init__(xArr, yArr)
		self.fasta_name = fasta_name
		self.fasta_seq  = []
		with open(self.fasta_name, 'r') as fasta_file:
			for each_line in fasta_file:
				if each_line.startswith('>'):
					continue
				self.fasta_seq += each_line.strip()
	def print_coor(self):
		print '> Selected point: residue %s%s (%s)'%(self.fasta_seq[self.dataind], 
			self.xArr[self.dataind]+fasta_offset, self.yArr[self.dataind])

if __name__ == "__main__":
	from random import randint
	# Generate test data
	x_data = range(10)
	y_data = [randint(2, 9) for _ in range(10)]
	# Make plot and connect to event
	line, = plt.plot(x_data, y_data, '-o', lw=2, picker=10)  # pixel tolerance
	
	fasta_name = "test_peptide.fasta"
	fasta_offset = 2 # fasta_offset = nterm_id - x_1
	# picked_point = PickPoint(x_data, y_data)	# example1 without fasta sequence
	picked_point = PickPointSequence(x_data, y_data, fasta_name, fasta_offset)	# example2 with fasta sequence

	plt.gcf().canvas.mpl_connect('pick_event', picked_point.onpick)
	# Make the points easy to pick
	plt.xlim(-1,10)
	plt.ylim( 1,10)
	plt.show()