import matplotlib.pyplot as plt

class LabelResidue(object):
    ''' Member description:
        x : X axis data for plotting
        y : Y axis data for plotting
        p : Line2D objects to be toggled on/off for highlighting
        t : text label
        s : FASTA sequence
        o : Offset of FASTA sequence from 0
    '''
    def __init__(self, xdata, ydata, fasta_name, fasta_offset):
        self.x = xdata
        self.y = ydata
        self.p = plt.plot(self.x, self.y, 'o', ms=12, alpha=0.5, c='y', visible=False)[0]
        self.t = None
        self.o = fasta_offset
        with open(fasta_name, 'r') as fn:
            self.s = ''.join([l.strip() for l in fn if not l.startswith('>')])

    def onpick(self, event):
        self.i = event.ind[0]
        self.p.set_visible(True)
        self.p.set_data(self.x[self.i], self.y[self.i])
        self.label()
        plt.draw()

    def onpress(self, event):
        if event.dblclick:
            self.t.set_visible(False)
            self.p.set_visible(False)

    def label(self):
        if self.t:
            self.t.set_visible(False)
        resname = '%s%s'%(self.s[self.i], self.i+self.o)
        self.t = plt.text(self.x[self.i], self.y[self.i], resname)

if __name__ == "__main__":
    from random import randint
    ### 1. Generate test data and plot
    x_data = range(10)
    y_data = [randint(2, 9) for _ in range(10)]
    plt.plot(x_data, y_data, '-o', lw=2, picker=10)
    plt.xlim(-1,10)
    plt.ylim( 1,10)

    ### 2. Connect plot to matplotlib events
    fasta_name = "0-pick-point.fasta"
    fasta_offset = 2
    picked_residue = LabelResidue(x_data, y_data, fasta_name, fasta_offset)
    plt.gcf().canvas.mpl_connect('pick_event', picked_residue.onpick)
    plt.gcf().canvas.mpl_connect('button_press_event', picked_residue.onpress)
    plt.show()