from copy import deepcopy
import latticePlotter as latplot
import numpy as np

class Autocorrelation:
    def __init__(self, data):
        self.autocorrMatrixTopChar = np.zeros((data.params.nFlows, data.params.confNum / 2))
        self.autocorrMatrixEnergy = np.zeros((data.params.nFlows, data.params.confNum / 2))
        # Compute the autocorrelation for different flow times
        for i in xrange(data.params.nFlows):
            for k in xrange(data.params.confNum / 2):
                self.autocorrMatrixTopChar[i,k] = np.corrcoef(np.array([data.topChargeMatrix[i, 0:data.params.confNum-k], \
                                            data.topChargeMatrix[i, k:data.params.confNum]]))[0,1]
                self.autocorrMatrixEnergy[i,k] = np.corrcoef(np.array([data.topChargeMatrix[i, 0:data.params.confNum-k], \
                                            data.topChargeMatrix[i, k:data.params.confNum]]))[0,1]
            print i

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


"""
    def autocorrelation(self):
        self.acf = np.zeros(len(self.data)/2)
        for k in range(0, len(self.data)/2):
            self.acf[k] = np.corrcoef(np.array([self.data[0:len(self.data)-k], \
                                            self.data[k:len(self.data)]]))[0,1]
    # Plot the Autocorrelation Function
    def plotAutocorrelation(self):
        font = {'fontname':'serif'}
        plt.plot(range(1, min(3000,len(self.data)/2)), self.acf[1: min(3000,len(self.data)/2)], 'r-')
        plt.ylim(-1, 1)
        plt.xlim(0,  min(3000,len(self.data)/2))
        plt.ylabel('Autocorrelation Function', **font)
        plt.xlabel('Lag', **font)
        plt.title('Autocorrelation', **font)
        plt.savefig(self.outName + "/autocorrelation.eps")
        plt.savefig(self.outName + "/autocorrelation.png")
        plt.clf()

"""