from copy import deepcopy
import latticePlotter as latplot
import numpy as np
from tqdm import trange


class Autocorrelation:
    def __init__(self, data):
        self.autocorrMatrixTopChar = np.zeros((data.params.nFlows, data.params.confNum / 2))
        self.autocorrMatrixEnergy = np.zeros((data.params.nFlows, data.params.confNum / 2))
        # Compute the autocorrelation for different flow times
        for i in trange(data.params.nFlows, desc="Autocorrelation...".ljust(20), leave=False):
            for k in xrange(data.params.confNum / 2):
                self.autocorrMatrixTopChar[i,k] = np.corrcoef(np.array([data.topChargeMatrix[i, 0:data.params.confNum-k], \
                                            data.topChargeMatrix[i, k:data.params.confNum]]))[0,1]
                self.autocorrMatrixEnergy[i,k] = np.corrcoef(np.array([data.energyMatrix[i, 0:data.params.confNum-k], \
                                            data.energyMatrix[i, k:data.params.confNum]]))[0,1]
        print "Autocorrelation...".ljust(20), "DONE"


    def plotAutocorrelation(self, folder, step="initial"):
        if step == "initial":
            latplot.autocorrPlot(self.autocorrMatrixTopChar[0, :], \
                                title="Initial Topological Charge Autocorrelation", \
                                fileName=folder + "/topc_autocorr_initial")
            latplot.autocorrPlot(self.autocorrMatrixEnergy[0, :], \
                                title="Initial Energy Autocorrelation", \
                                fileName=folder + "/energy_autocorr_initial")
        if step == "final":
            latplot.autocorrPlot(self.autocorrMatrixTopChar[-1, :], \
                                    title="Final Topological Charge Autocorrelation", \
                                    fileName=folder + "/topc_autocorr_final")
            latplot.autocorrPlot(self.autocorrMatrixEnergy[-1, :], \
                                title="Final Energy Autocorrelation", \
                                fileName=folder + "/energy_autocorr_final")

    def tauInt(self, rho, N, lambdaMax=100):
        tauInt = 0.5
        for t in xrange(1, len(rho)):
            dRhoT = 0
            for k in xrange(t + lambdaMax):
                dRhoT += (rho[t+k] + rho[abs(t-k)] - rho[t]*rho[k])**2
            dRhoT /= N
            if np.sqrt(dRhoT) > rho[t]:
                break
            else:
                tauInt += rho[t]
        return tauInt

    def adjustError(self, data, resampler=None):
        tauIntTopChar = np.zeros(data.params.nFlows)
        tauIntEnergy = np.zeros(data.params.nFlows)
        lambdaMax = 100
        for i in trange(data.params.nFlows, desc="Autocorr. Error...".ljust(20), leave=False):
            tauIntTopChar[i] = self.tauInt(self.autocorrMatrixTopChar[i,:], data.params.confNum)
            tauIntEnergy[i] = self.tauInt(self.autocorrMatrixEnergy[i,:], data.params.confNum)
        if resampler:
            resampler.bootstrap.data.topChargeStd *= np.sqrt(2*tauIntTopChar)
            resampler.jackknife.data.topChargeStd *= np.sqrt(2*tauIntTopChar)
            resampler.bootstrap.data.energyStd *= np.sqrt(2*tauIntEnergy)
            resampler.jackknife.data.energyStd *= np.sqrt(2*tauIntEnergy)
            resampler.bootstrap.data.energyTauSquareStd *= np.sqrt(2*tauIntEnergy)
            resampler.jackknife.data.energyTauSquareStd *= np.sqrt(2*tauIntEnergy)
            self.errCorr=np.sqrt(2*tauIntEnergy)
        
        