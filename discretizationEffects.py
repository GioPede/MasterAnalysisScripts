import numpy as np
import scipy.optimize as optimize
import latticePlotter as latplot
from tqdm import trange
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from lmfit import Model

linear = lambda x, a, b: a*x + b
const  = lambda x, a: a
x = []
y = []
yStd = []

def continuumLimit(tauR0, energyBootMatrix, params):
    xvals = np.zeros(energyBootMatrix.shape[1]/5)
    yvals = np.zeros(energyBootMatrix.shape[1]/5)
    yvalsStd = np.zeros(energyBootMatrix.shape[1]/5)
    for i in xrange(len(xvals)):
        energyTauSquare = energyBootMatrix[:,i*5]
        fitIndexes = np.where(np.logical_and(energyTauSquare>=0.27, energyTauSquare<=0.33))
        fitDataX = np.take(tauR0, fitIndexes)[0]
        fitDataY = np.take(energyTauSquare, fitIndexes)[0]

        
        coeffs, matcov = optimize.curve_fit(linear, fitDataX, fitDataY, p0=[3,0])
        r0 = 0.5
        t0 = (0.3 - coeffs[1]) / coeffs[0] * r0**2
        dt0da = -r0**2 * (0.3-coeffs[1]) / coeffs[0]**2
        dt0db = -r0**2 / coeffs[0]
        t0Var = dt0da*dt0da*matcov[0][0] + dt0db*dt0db*matcov[1][1] - 2*dt0da*dt0db*matcov[0][1]

        # sns.set()
        # plt.plot(fitDataX,fitDataY, ".", color=sns.xkcd_rgb["denim blue"], lw=1)
        # plt.plot([(0.27- coeffs[1])/coeffs[0] ,(0.33- coeffs[1])/coeffs[0]],[0.27,0.33], "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
        # plt.show()

        xvals[i] = (params.latSpacing * 2)**2
        yvals[i] = np.sqrt(8*t0) *2 
        yvalsStd[i] =  np.sqrt( t0Var * np.sqrt(8) / np.sqrt(t0) ) # params.latSpacing
        


        x.append(xvals[i])
        y.append(yvals[i])
    yStd.append(np.std(yvals))

def plotContLimit():
    sns.set()
    coeffs, matcov = optimize.curve_fit(linear, x, y, p0=[0,1], sigma=yStd)
    print coeffs, matcov
    plt.ylim([0.89, 0.97])
    plt.xlim([-0.002, 0.05])
    plt.errorbar(x,y=y, yerr=yStd, fmt=".", color=sns.xkcd_rgb["denim blue"], lw=1)
    plt.plot([-0.,0.05],[linear(0, coeffs[0], coeffs[1]),linear(0.05, coeffs[0], coeffs[1])], "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
    plt.errorbar([0.0], [coeffs[1]], yerr=np.sqrt(matcov[1][1]))
    plt.show()
