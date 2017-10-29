# Modified from "data_browser.py" at 
# https://matplotlib.org/devdocs/gallery/event_handling/data_browser.html
# 
# Usage> instantiate by: picked_point = PickPoint(x_data, y_data), then pass
# picked_point.onpick as a callback funtion to mpl_connect()


import matplotlib.pyplot as plt

class PickPoint():
    def __init__(self, xArr, yArr):
    	self.xArr = xArr
    	self.yArr = yArr
        self.selected, = plt.gca().plot(self.xArr, self.yArr, 'o', 
        	markersize=12, alpha=0.5, color='yellow', visible=False)
    def onpick(self, event):
        dataind = event.ind
        print '> Selected point: (%s, %s)'%(self.xArr[dataind], self.yArr[dataind])
        self.selected.set_visible(True)
        self.selected.set_data(self.xArr[dataind], self.yArr[dataind])
        plt.gcf().canvas.draw()

if __name__ == "__main__":
	from random import randint
	# Generate test data
	x_data = range(10)
	y_data = [randint(2, 9) for _ in range(10)]
	# Make plot and connect to event
	line, = plt.plot(x_data, y_data, '-o', lw=2, picker=10)  # pixel tolerance
	picked_point = PickPoint(x_data, y_data)
	plt.gcf().canvas.mpl_connect('pick_event', picked_point.onpick)
	# Make the points easy to pick
	plt.xlim(-1,10)
	plt.ylim( 1,10)
	plt.show()