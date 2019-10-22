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

def setup(label_font=18, tick_font=16, axis_width=2, 
    tick_major_width=2, tick_minor_width=1.5, 
    tick_major_size=5, tick_minor_size=4, 
    showmajorticks=True, showminorticks=False):
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
    rcParams['xtick.major.size']=tick_major_size if showmajorticks else 0
    rcParams['xtick.minor.top']=True
    rcParams['xtick.minor.width']=tick_minor_width
    rcParams['xtick.minor.size']=tick_minor_size
    # y ticks setup
    rcParams['ytick.labelsize']=tick_font
    rcParams['ytick.direction']='in'
    rcParams['ytick.right']=True
    rcParams['ytick.minor.visible']=showminorticks
    rcParams['ytick.major.width']=tick_major_width
    rcParams['ytick.major.size']=tick_major_size if showmajorticks else 0
    rcParams['ytick.minor.right']=True
    rcParams['ytick.minor.width']=tick_minor_width
    rcParams['ytick.minor.size']=tick_minor_size
    # font family
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Times New Roman']
    rcParams['mathtext.fontset'] = 'cm'

def label(axs, case='upper', xratio=0.005, yratio=0.85, fontsize=18):
    import numpy as np
    import sys
    if type(axs) is not np.ndarray:
        sys.stdout.write("Label setup ignored: Axs type is not np.ndarray.\n")
        return
    import string
    if 'upper'==case:
        labels = string.ascii_uppercase
    if 'lower'==case:
        labels = string.ascii_lowercase
    for i, ax in enumerate(axs.flatten()):
        ax.text(xratio, yratio, "(%s)"%labels[i], transform=ax.transAxes, size=fontsize)

def save(img_name, dpi=300, width=0, height=0):
    from matplotlib import pyplot
    if 0==width or 0==height:
        width, height = pyplot.gcf().get_size_inches()
    pyplot.gcf().set_size_inches(width, height)
    pyplot.savefig(img_name+'.png', dpi=dpi, bbox_inches='tight')

def save3(img_name, dpi=300, width=0, height=0):
    from matplotlib import pyplot
    if 0==width or 0==height:
        width, height = pyplot.gcf().get_size_inches()
    pyplot.gcf().set_size_inches(width, height)
    pyplot.savefig(img_name+'.png', dpi=dpi, bbox_inches='tight')
    pyplot.savefig(img_name+'.pdf', dpi=dpi, bbox_inches='tight')
    pyplot.savefig(img_name+'.svg', dpi=dpi, bbox_inches='tight')

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    ### setup() usage:
    setup(showmajorticks=False, showminorticks=False)    

    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.sin(2*x)
    fig, axs = plt.subplots(2,1)

    axs[0].plot(x, y1, linewidth=2, color="tab:blue")
    axs[0].set_xticks([0, np.pi, 2*np.pi])
    axs[0].set_xlim(x.min(), x.max())
    axs[0].set_xticklabels([0, "$\pi$", "$2\pi$"])
    axs[0].set_xlabel("$x$")
    axs[0].set_ylabel("sin($x$)")

    axs[1].plot(x, y2, linewidth=2, color="tab:red")
    axs[1].set_xticks([0, np.pi, 2*np.pi])
    axs[1].set_xlim(x.min(), x.max())
    axs[1].set_xticklabels([0, "$\pi$", "$2\pi$"])
    axs[1].set_xlabel("$x$")
    axs[1].set_ylabel("sin($2x$)")

    fig.align_ylabels(axs)
    label(axs)

    ### save() or save3() usage:
    save("demo-default-figsize")
    save("demo-custom-fig-size", 4, 3)