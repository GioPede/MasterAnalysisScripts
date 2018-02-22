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

def simpleContLimit(data):
    energyTauSquare = data.energyTauSquare - 0.3
    fitIndexes = np.where(np.logical_and(energyTauSquare>=-0.07, energyTauSquare<=0.07))
    fitDataX = np.take(data.tauR0, fitIndexes)[0]
    fitDataY = np.take(energyTauSquare, fitIndexes)[0]
    fitDataYStd = np.take(data.energyTauSquareStd, fitIndexes)[0]

    coeffs, matcov = optimize.curve_fit(linear, fitDataX, fitDataY, p0=[3,0], sigma=fitDataYStd)

    print matcov, coeffs    

    r0 = 0.5
    t0 = -coeffs[1] / coeffs[0]

    xx = np.linspace(min(fitDataX), max(fitDataX), 10001)
    maxFit = linear(xx, coeffs[0] + np.sqrt(matcov[0][0]), coeffs[1] + np.sqrt(matcov[1][1]))
    minFit = linear(xx, coeffs[0] - np.sqrt(matcov[0][0]), coeffs[1] - np.sqrt(matcov[1][1]))

    # sns.set()
    # plt.errorbar(fitDataX,fitDataY, yerr=fitDataYStd, fmt=".", color=sns.xkcd_rgb["denim blue"], lw=1)
    # plt.plot([(-0.03 - coeffs[1])/coeffs[0] ,(0.03- coeffs[1])/coeffs[0]],[-0.03,0.03], "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
    # plt.plot(xx, maxFit, "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
    # plt.plot(xx, minFit, "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
    # plt.show()

    for i in xrange(len(xx)):
        if maxFit[i] > 0:
            xstart = i
            break
    
    for i in reversed(xrange(len(xx))):
        if minFit[i] < 0:
            xfinish = i
            break
    
    t0Var = (maxFit[xfinish]/2.0 - minFit[xstart]/2.0)**2
    t0 *= r0**2
    t0Var *= r0**2
    x.append((data.params.latSpacing * 2)**2)
    y.append(np.sqrt(8*t0) *2) 
    yStd.append(np.sqrt( t0Var * np.sqrt(8) / np.sqrt(t0) )) # params.latSpacing




def continuumLimit(tauR0, energyBootMatrix, params):
    """
    xvals = np.zeros(energyBootMatrix.shape[1])
    yvals = np.zeros(energyBootMatrix.shape[1])
    yvalsStd = np.zeros(energyBootMatrix.shape[1])
    for i in xrange(len(xvals)):
        energyTauSquare = energyBootMatrix[:,i] - 0.3
        fitIndexes = np.where(np.logical_and(energyTauSquare>=-0.03, energyTauSquare<=0.03))
        fitDataX = np.take(tauR0, fitIndexes)[0]
        fitDataY = np.take(energyTauSquare, fitIndexes)[0]

        
        coeffs, matcov = optimize.curve_fit(linear, fitDataX, fitDataY, p0=[3,0])

        r0 = 0.5
        t0 = -coeffs[1] / coeffs[0]

        dt0da = coeffs[1] / coeffs[0]**2
        dt0db = - 1.0 / coeffs[0]
        t0Var = dt0da*dt0da*matcov[0][0] + dt0db*dt0db*matcov[1][1] + 2*dt0da*dt0db*matcov[0][1]

        # sns.set()
        # plt.plot(fitDataX,fitDataY, ".", color=sns.xkcd_rgb["denim blue"], lw=1)
        # plt.plot([(-0.03 - coeffs[1])/coeffs[0] ,(0.03- coeffs[1])/coeffs[0]],[-0.03,0.03], "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
        # plt.show()

        t0 *= r0**2
        t0Var *= r0**2
        xvals[i] = (params.latSpacing * 2)**2
        yvals[i] = np.sqrt(8*t0) *2 
        yvalsStd[i] =  np.sqrt( t0Var * np.sqrt(8) / np.sqrt(t0) ) # params.latSpacing
        


    x.append(np.average(xvals))
    y.append(np.average(yvals))
    yStd.append(np.std(yvals))
    """
    pass

    
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
