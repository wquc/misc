#!/usr/bin/env python

##################################################################
# Publication quality figure setup
#
# 1. Dependency:
#  1.1 matplotlib
#
# 2. Usage:
#  2.1 Make a folder in the site-packages folder of python,
#      e.g. $HOME/anaconda2/lib/python2.7/site-packages/user
#  2.2 Copy this file to that folder
#  2.3 Create a __init__.py file to make it a module
#
# 3. Troubleshooting:
#  3.1 Error : matplotlib - Font family [u'sans-serif'] not found
#  3.2 Solution:
#   (1) sudo apt-get install msttcorefonts -qq
#   (2) delete the content of .cache/matplotlib
##################################################################

def setup(label_font=16, tick_font=16, axis_width=2, 
	tick_major_width=2, tick_minor_width=1.5, 
	tick_major_size=5, tick_minor_size=4, showminorticks=False):
    from matplotlib import rcParams
    # Conversion of unicode minus sign
    rcParams['axes.unicode_minus']=False
    # canvas setup
    rcParams['axes.labelsize']=label_font
    rcParams['axes.linewidth']=axis_width
    # x ticks setup
    rcParams['xtick.labelsize']=tick_font
    rcParams['xtick.direction']='in'
    rcParams['xtick.top']=True
    rcParams['xtick.minor.visible']=showminorticks
    rcParams['xtick.major.width']=tick_major_width
    rcParams['xtick.major.size']=tick_major_size
    rcParams['xtick.minor.top']=True
    rcParams['xtick.minor.width']=tick_minor_width
    rcParams['xtick.minor.size']=tick_minor_size
    # y ticks setup
    rcParams['ytick.labelsize']=tick_font
    rcParams['ytick.direction']='in'
    rcParams['ytick.right']=True
    rcParams['ytick.minor.visible']=showminorticks
    rcParams['ytick.major.width']=tick_major_width
    rcParams['ytick.major.size']=tick_major_size
    rcParams['ytick.minor.right']=True
    rcParams['ytick.minor.width']=tick_minor_width
    rcParams['ytick.minor.size']=tick_minor_size
    # font family
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Times New Roman']
    rcParams['mathtext.fontset'] = 'cm'

def save(img_name):
    from matplotlib import pyplot
    pyplot.savefig(img_name+'.png', dpi=300, bbox_inches='tight')
    pyplot.savefig(img_name+'.pdf', dpi=300, bbox_inches='tight')
    pyplot.savefig(img_name+'.svg', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    setup()
    x = np.linspace(-100, 100, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()
