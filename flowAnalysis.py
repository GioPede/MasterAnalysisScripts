import numpy as np
import scipy.optimize as optimize
import latticePlotter as latplot


import matplotlib.pyplot as plt
import seaborn as sns



# PLOT COLLECTIVE DATA
def saveData(data, folder, filename, suffix=""):
    dataMatrix = np.zeros((data.params.nFlows, 11))
    dataMatrix[:,0] = data.tau
    dataMatrix[:,1] = data.tauScaled
    dataMatrix[:,2] = data.topCharge
    dataMatrix[:,3] = data.topChargeStd
    dataMatrix[:,4] = data.topSuscep
    dataMatrix[:,5] = data.topSuscepStd
    dataMatrix[:,6] = data.energy
    dataMatrix[:,7] = data.energyStd
    dataMatrix[:,8] = data.energyTauSquare
    dataMatrix[:,9] = data.energyTauSquareStd
    dataMatrix[:,10] = data.tauR0
    np.savetxt(folder + filename + suffix + ".txt", dataMatrix)

def plotData(data, folder, suffix=""):
    latplot.plotFlowPlaquette(data.tauScaled, data.plaquette, \
                                errorbar=data.plaquetteStd, \
                                title="Mean Average Plaquette", \
                                fileName=folder + "/plaq" + suffix)
    latplot.plotFlowTopCharge(data.tauScaled, data.topCharge, \
                                errorbar=data.topChargeStd, \
                                title="Mean Topological Charge", \
                                fileName=folder + "/topc" + suffix)
    latplot.plotFlowTopSuscep(data.tauScaled, data.topSuscep,
                                errorbar=data.topSuscepStd,
                                title="Mean Topological Susceptibility", \
                                fileName=folder + "/tops" + suffix)
    latplot.plotFlowEnergy(data.tauScaled, data.energy,
                                errorbar=data.energyStd,
                                title="Mean Energy", \
                                fileName=folder + "/enrg" + suffix)
    latplot.plotFlowEnergyTauSquare(data.tauR0, \
                                data.energyTauSquare,
                                errorbar=data.energyTauSquareStd,
                                title="Mean Energy Density", \
                                fileName=folder + "/etsq" + suffix)

# PLOT INDIVIDUAL DATA SERIES
def singleConfPlots(data, folder):
    for i in xrange(data.params.confNum):
        suffix = "_" + str(i).zfill(4) 
        latplot.plotFlowPlaquette(data.tauScaled, data.plaquetteMatrix[:,i], \
                                title="Plaquette", \
                                fileName=folder + "/plaq" + suffix)
        latplot.plotFlowTopCharge(data.tauScaled, data.topChargeMatrix[:,i], \
                                title="Topological Charge", \
                                fileName=folder + "/topc" + suffix)


def topChargeHistograms(data, folder, step="initial"):
    if step == "initial":
        latplot.histTopCharge(data.topChargeMatrix[0, :], \
                              title="Initial Topological Charge Distribution", \
                              fileName=folder + "/topcHist_initial")
    if step == "final":
        topc = np.average(data.topChargeMatrix[-100:,:], axis=0)
        latplot.histTopCharge(topc, \
                              title="Final Topological Charge Distribution", \
                              fileName=folder + "/topcHist_final")

def MCHistoryPlots(data, folder):
    suffix = "_initial"
    latplot.plotMCTopCharge(range(data.params.confNum), data.topChargeMatrix[0,:], \
                                title="MC History Topological Charge $\\tau = 0$", \
                                fileName=folder + "/MCtopc" + suffix)
    latplot.plotMCEnergy(range(data.params.confNum), data.energyMatrix[0,:] / data.params.volume,
                                title="MC History Energy $\\tau = 0$", \
                                fileName=folder + "/MCenrg" + suffix)
    suffix = "_final"
    latplot.plotMCTopCharge(range(data.params.confNum), data.topChargeMatrix[-1,:],  \
                                title="MC History Topological Charge $\\tau = 10$", \
                                fileName=folder + "/MCtopc" + suffix)
    latplot.plotMCEnergy(range(data.params.confNum), data.energyMatrix[-1,:] / data.params.volume,
                                title="MC History Energy $\\tau = 10$", \
                                fileName=folder + "/MCenrg" + suffix)


def plotGathered(dataSetTags, params, folders, suffix="", show=False):
    labels = []
    tau = []
    tauScaled = []
    tauR0 = []
    plaquette = []
    topCharge = []
    topSuscep = []
    plaquetteStd = []
    topChargeStd = []
    topSuscepStd = []
    energyTauSquare = []
    energyTauSquareStd = []
    for dataSet in dataSetTags:
        results = np.loadtxt(folders.results + dataSet + suffix + ".txt")
        tau.append(results[:,0])
        tauR0.append(results[:,10])
        tauScaled.append(results[:,1])
        topCharge.append(results[:,2])
        topChargeStd.append(results[:,3])
        topSuscep.append(results[:,4])
        topSuscepStd.append(results[:,5])
        energyTauSquare.append(results[:,8] )
        energyTauSquareStd.append(results[:,9] )
        labels.append(params[dataSet].label)

    latplot.plotFlowTopChargeTotal(tauScaled, topCharge, \
                                topChargeStd, labels, \
                                title="Mean Topological Charge", \
                                fileName=folders.figuresRoot + "topc" + suffix,\
                                show=show)
    latplot.plotFlowTopSuscepTotal(tauScaled, topSuscep, \
                                topSuscepStd, labels, \
                                title="Mean Topological Susceptibility", \
                                fileName=folders.figuresRoot + "/tops" + suffix,\
                                show=show)
    latplot.plotFlowEnergyTauSquareTotal(tauR0, energyTauSquare, \
                                energyTauSquareStd, labels, \
                                title="Mean Energy Density", \
                                fileName=folders.figuresRoot + "/etsq" + suffix,\
                                show=show)

def makeCollectivePlots(dataSetTags, folders, params):
    print "Plotting Cumulative Plots..."
    plotGathered(dataSetTags, params, folders, suffix="_avg")
    plotGathered(dataSetTags, params, folders, suffix="_boot")
    plotGathered(dataSetTags, params, folders, suffix="_jkkf")

def energyContinuumLimit(dataSetTags, folders, params):
    linear = lambda x, a, b: a*x + b
    labels = []
    for suffix in ["_avg", "_boot", "_jkkf"]:
        xvals = []
        yvals = []
        yvalsStd = []
        for dataSet in dataSetTags:
            results = np.loadtxt(folders.results + dataSet + suffix + ".txt")
            energyTauSquare = results[:,8] 
            energyTauSquareStd = results[:,9] 
            tauR0 = results[:,10]
            labels.append(params[dataSet].label)

            fitIndexes = np.where(np.logical_and(energyTauSquare>=0.27, energyTauSquare<=0.33))
            fitDataX = np.take(tauR0, fitIndexes)[0,:]
            fitDataY = np.take(energyTauSquare, fitIndexes)[0,:]
            fitDataYErr = np.take(energyTauSquareStd, fitIndexes)[0,:]

            sns.set()
            coeffs, matcov = optimize.curve_fit(linear, fitDataX, fitDataY, p0=[3,0], sigma=fitDataYErr)
            t0 = (0.3 - coeffs[1]) / coeffs[0] / 4.0

            xvals.append((params[dataSet].latSpacing * 2)**2)
            yvals.append(np.sqrt(8*t0) *2 )

        coeffs, matcov = optimize.curve_fit(linear, xvals, yvals, p0=[0,1],)# sigma=yvalsStd)
        print yvals
        print coeffs, matcov
        plt.ylim([0.89, 0.97])
        plt.errorbar(xvals,y=yvals, yerr=np.zeros(len(yvals)), fmt=".", color=sns.xkcd_rgb["denim blue"], lw=1)
        plt.plot([0,0.05],[linear(0, coeffs[0], coeffs[1]),linear(0.05, coeffs[0], coeffs[1])], "-", color=sns.xkcd_rgb["pale red"], lw=0.5)
        plt.show()