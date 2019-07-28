import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# dummy functions to setup the limit
def gen_lowerboundary(num):
    return num*1.01 if num < 0 else num*0.99

def gen_upperboundary(num):
    return num*0.99 if num < 0 else num*1.01

# 2D histogram
def h2dplot(x, y, nbins=40):
    xmin, xmax = gen_lowerboundary(x.min()), gen_upperboundary(x.max())
    ymin, ymax = gen_lowerboundary(y.min()), gen_upperboundary(y.max())
    extent = [xmin, xmax, ymin, ymax]
    fig, ax = plt.subplots()
    hist, xbins, ybins = np.histogram2d(x, y, bins=nbins, normed=True)
    im = ax.imshow(np.ma.masked_where(0==hist, hist).T, 
        interpolation='nearest', origin='lower', extent=extent, cmap='jet')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Z', fontsize=16, labelpad=-40, y=1.05, rotation=0)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect(1.0)
    # plt.show()
    plt.savefig("h2d.png", format='png', dpi=100, bbox_inches='tight')
    plt.close()

# Kernel density estimation
def kdeplot(x, y, nlevels=10, nbins=100):
    #----- Generate limits for plot and meshgrid -----
    xmin, xmax = gen_lowerboundary(x.min()), gen_upperboundary(x.max())
    ymin, ymax = gen_lowerboundary(y.min()), gen_upperboundary(y.max())

    #----- Generate meshgrid and run kernel density estimation -----
    xMesh, yMesh = np.mgrid[xmin:xmax:nbins*1j, ymin:ymax:nbins*1j]
    positions = np.vstack([xMesh.ravel(), yMesh.ravel()])
    values = np.vstack([xArr, yArr])
    kernel = st.gaussian_kde(values)
    zMesh = np.reshape(kernel(positions).T, xMesh.shape)

    #----- Plot the results -----
    # ax = plt.figure(figsize=(8, 6)).gca()
    ax = plt.figure().gca()
    levels = ax.contour(xMesh, yMesh, zMesh, nlevels, colors='k').levels
    levels = np.concatenate([[0.0], levels, [levels[-1]+levels[0]]])
    cfplot = ax.contourf(xMesh, yMesh, zMesh, levels[1:], cmap='jet')

    #----- Set up colorbar -----
    cbar = plt.colorbar(cfplot)
    cbar.ax.minorticks_off()
    cbar.ax.xaxis.set_ticks_position('top')
    cbar.ax.xaxis.set_label_position('top')
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, ha='right')
    cbar.ax.yaxis.set_tick_params(pad=40)
    cbar.set_label('Z', fontsize=16, labelpad=-50, y=1.05, rotation=0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect(1.0)
    # plt.show()
    plt.savefig("kde.png", format='png', dpi=100, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    np.random.seed(0)
    xArr = np.random.randn(1000)
    yArr = np.random.randn(1000)
    h2dplot(xArr, yArr)
    kdeplot(xArr, yArr)