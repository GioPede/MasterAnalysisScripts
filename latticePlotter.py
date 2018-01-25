import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def init():
    sns.set()

def plotFlowPlaquette(t, plaq, errorbar=np.zeros(1), title="", fileName="", show=False):
    plt.ylabel('Plaquette Value')
    plt.ylim([0,1.1])
    plotFlow(t, plaq, errorbar=errorbar, title=title, fileName=fileName, show=show)

def plotFlowTopCharge(t, topc, errorbar=np.zeros(1), title="", fileName="", show=False):
    plt.ylabel('$\mathcal{Q}$')
    plt.ylim([-15, 15])
    plotFlow(t, topc, errorbar=errorbar, title=title, fileName=fileName, show=show)

def plotFlowTopSuscep(t, tops, errorbar=np.zeros(1), title="", fileName="", show=False):
    plt.ylabel('$\chi$ [GeV]')
    plt.ylim([0.1,0.35])
    plotFlow(t, tops, errorbar=errorbar, title=title, fileName=fileName, show=show)

def plotFlowEnergy(t, enrg, errorbar=np.zeros(1), title="", fileName="", show=False):
    plt.ylabel('$E$ [GeV]')
    #plt.ylim([-5,5])
    plotFlow(t, enrg, errorbar=errorbar, title=title, fileName=fileName, show=show)

def plotFlowEnergyTauSquare(t, data, errorbar=np.zeros(1), title="", fileName="", show=False):
    plt.ylabel('$t^2\langle E \\rangle$')
    plt.plot([0,0.35], [0.3,0.3], "--", lw=0.5)
    plt.ylim([0,1.2])
    plotFlow(t, data, errorbar=errorbar, title="", fileName=fileName, xlabel="$t/r_0^2$", show=show)

def plotMCEnergy(steps, data, title="", fileName="", show=False):
    plt.ylabel('$E$ [GeV]')
    #plt.ylim([-5,5])
    plotMCHistory(steps, data, title=title, fileName=fileName, show=show)

def plotMCTopCharge(steps, data, title="", fileName="", show=False):
    plt.ylabel('$\mathcal{Q}$')
    plt.ylim([-15, 15])
    plotMCHistory(steps, data, title=title, fileName=fileName, show=show)


def plotFlowTopChargeTotal(t, data, errorbars, labels, title="", fileName="", show=False):
    plt.ylabel('$\mathcal{Q}$')
    plt.ylim([-15, 15])
    plotFlowTotal(t, data, errorbars, labels, title=title, fileName=fileName, show=show)

def plotFlowTopSuscepTotal(t, data, errorbars, labels, title="", fileName="", show=False):
    plt.ylabel('$\chi$ [GeV]')
    plt.ylim([0.1,0.35])
    plotFlowTotal(t, data, errorbars, labels, title=title, fileName=fileName, show=show)

def plotFlowEnergyTauSquareTotal(t, data, errorbars, labels, title="", fileName="", show=False):
    plt.ylabel('$t^2\langle E \\rangle$')
    plt.plot([0,0.35], [0.3,0.3], "--", lw=0.5)
    plt.ylim([0,1.2])
    plotFlowTotal(t, data, errorbars, labels, title="", fileName=fileName, xlabel="$t/r_0^2$", show=show)

def plotFlowTotal(t, data, errorbars, labels, title="", fileName="", xlabel=None, show=False):
    for i in xrange(len(t)):
        plt.errorbar(t[i], y=data[i], yerr=errorbars[i], label=labels[i] ,fmt=".", lw=1)
        #plt.plot(t[i], data[i], "-", lw=0.5)
    plt.title(title)
    plt.xlim([0,0.9])
    if xlabel:
        plt.xlabel(xlabel)
    else:
        plt.xlabel('$\sqrt{8t}/r_0$ ')
    plt.legend()

    if fileName:
        plt.savefig(fileName + ".eps", dpi=300)
        plt.savefig(fileName + ".png", dpi=300)
    if show:
        plt.show()
    plt.close()


def plotFlow(t, data, errorbar=np.zeros(1), title="", fileName="", xlabel=None, show=False):
    if len(errorbar) == 1:
        plt.plot(t, data, '-o')
    else:
        plt.errorbar(t,y=data, yerr=errorbar, fmt=".", color=sns.xkcd_rgb["denim blue"], lw=1)
        plt.plot(t,data, "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
    plt.title(title)
    plt.xlim(left=0)
    if xlabel:
        plt.xlabel(xlabel)
    else:
        plt.xlabel('$\sqrt{8t}$ [fm]')

    if fileName:
        plt.savefig(fileName + ".eps", dpi=300)
        plt.savefig(fileName + ".png", dpi=300)
    if show:
        plt.show()
    plt.close()

def histTopCharge(topc, title="", fileName="", show=False):
    n, bins, patches = plt.hist(topc, bins=40, range=[-20,20])
    plt.title(title)
    plt.xlabel('Q')
    plt.ylim([0,100])

    if fileName:
        plt.savefig(fileName + ".eps", dpi=300)
        plt.savefig(fileName + ".png", dpi=300)
    if show:
        plt.show()
    plt.close()

def plotMCHistory(steps, data, title="", fileName="", show=False):
    plt.plot(steps, data, "-", color=sns.xkcd_rgb["denim blue"], lw=1)
    plt.title(title)
    plt.xlim(left=0)
    plt.xlabel('MC Steps')

    if fileName:
        plt.savefig(fileName + ".eps", dpi=300)
        plt.savefig(fileName + ".png", dpi=300)
    if show:
        plt.show()
    plt.close()

def autocorrPlot(data, title="", fileName="", show=False):
    plt.plot(range(len(data)), data, "-", color=sns.xkcd_rgb["denim blue"], lw=1)
    plt.title(title)
    plt.xlim(left=0)
    plt.xlabel('lag $h$')
    plt.ylabel('Autocorrelation')
    plt.ylim([-1,1])

    if fileName:
        plt.savefig(fileName + ".eps", dpi=300)
        plt.savefig(fileName + ".png", dpi=300)
    if show:
        plt.show()
    plt.close()