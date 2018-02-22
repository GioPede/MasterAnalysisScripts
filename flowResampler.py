from copy import deepcopy
from flowData import FlowDataReader
import latticePlotter as latplot
import numpy as np
from tqdm import trange
from discretizationEffects import continuumLimit

class FlowResampler:
    def __init__(self, data, bootstrap=True, jacknife=True, bootSamples=200):
        if bootstrap:
            self.bootstrap = self.Bootstrap(data, bootSamples)
        if jacknife:
            self.jackknife = self.Jackknife(data)
    
    class Bootstrap:
        def __init__(self, data, nBoots):
            self.data = deepcopy(data)
            self.nBoots = nBoots
            self.indexLists = np.random.randint(self.data.params.confNum, size=(self.nBoots, self.data.params.confNum))
            self.createBootstraps()

        def createBootstraps(self):
            plaqBootstrap = np.zeros((self.data.params.nFlows, self.nBoots))    
            topCharBootstrap = np.zeros((self.data.params.nFlows, self.nBoots))
            topCharSquareBootstrap = np.zeros((self.data.params.nFlows, self.nBoots))
            energyBootstrap = np.zeros((self.data.params.nFlows, self.nBoots))
            energyBootMatrix = np.zeros((self.data.params.nFlows, self.nBoots))

            for i in trange(self.data.params.nFlows, desc="Bootstrap...".ljust(20), leave=False):
                for j in xrange(self.nBoots):
                    plaqBootstrap[i,j] = np.average(self.data.plaquetteMatrix[i][self.indexLists[j]])
                    energyBootstrap[i,j] = np.average(self.data.energyMatrix[i][self.indexLists[j]])
                    energyBootMatrix[i,j] = energyBootstrap[i,j] * self.data.tau[i]*self.data.tau[i] / self.data.params.volume 
                    topCharBootstrap[i,j] = np.average(self.data.topChargeMatrix[i][self.indexLists[j]])
                    topCharSquareBootstrap[i,j] = np.average(self.data.topChargeMatrix[i][self.indexLists[j]]*self.data.topChargeMatrix[i][self.indexLists[j]])
            
            self.data.plaquette = np.average(plaqBootstrap,axis=1)
            self.data.plaquetteStd	= np.std(plaqBootstrap,axis=1)
            self.data.energy = np.average(energyBootstrap,axis=1)/ self.data.params.volume
            self.data.energyStd	= np.std(energyBootstrap,axis=1)/ self.data.params.volume
            self.data.topCharge = np.average(topCharBootstrap,axis=1)
            self.data.topChargeStd	= np.std(topCharBootstrap,axis=1)
            self.data.topSuscep = np.average(topCharSquareBootstrap,axis=1)**(0.25)*self.data.params.chiConst
            self.data.topSuscepStd	= np.std(topCharSquareBootstrap**(0.25)*self.data.params.chiConst,axis=1)
            self.data.energyTauSquare = np.abs(np.average(energyBootstrap,axis=1))*self.data.tau*self.data.tau / self.data.params.volume 
            self.data.energyTauSquareStd	= np.std(energyBootstrap,axis=1)*self.data.tau*self.data.tau / self.data.params.volume 
            continuumLimit(self.data.tauR0, np.abs(energyBootMatrix), self.data.params)
            print "Bootstrap...".ljust(20), "DONE"

    class Jackknife:
        def __init__(self, data):
            self.data = deepcopy(data)
            self.createJackknife()

        def createJackknife(self):
            plaqJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))    
            topCharJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))
            topCharSquareJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))
            energyJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))

            for i in trange(self.data.params.nFlows, desc="Jackknife...".ljust(20), leave=False):
                for j in xrange(self.data.params.confNum):
                    plaqJackknife[i,j] = np.average(np.concatenate((self.data.plaquetteMatrix[i,:j], self.data.plaquetteMatrix[i,(j+1):])))
                    energyJackknife[i,j] = np.average(np.concatenate((self.data.energyMatrix[i,:j], self.data.energyMatrix[i,j+1:])))
                    topCharJackknife[i,j] = np.average(np.concatenate((self.data.topChargeMatrix[i,:j], self.data.topChargeMatrix[i,j+1:])))
                    topCharSquareJackknife[i,j] = np.average(np.concatenate((self.data.topChargeMatrix[i,:j], self.data.topChargeMatrix[i,j+1:]))*np.concatenate((self.data.topChargeMatrix[i,:j], self.data.topChargeMatrix[i,j+1:])))
            
            self.data.plaquette = np.average(plaqJackknife,axis=1)
            self.data.plaquetteStd	= np.std(plaqJackknife,axis=1)
            self.data.energy = np.average(energyJackknife,axis=1)/ self.data.params.volume
            self.data.energyStd	= np.std(energyJackknife,axis=1)/ self.data.params.volume
            self.data.topCharge = np.average(topCharJackknife,axis=1)
            self.data.topChargeStd	= np.std(topCharJackknife,axis=1)
            self.data.topSuscep = np.average(topCharSquareJackknife,axis=1)**(0.25)*self.data.params.chiConst
            self.data.topSuscepStd	= np.std(topCharSquareJackknife**(0.25)*self.data.params.chiConst,axis=1)
            self.data.energyTauSquare = np.abs(np.average(energyJackknife,axis=1))*self.data.tau*self.data.tau / self.data.params.volume 
            self.data.energyTauSquareStd	= np.std(energyJackknife,axis=1)*self.data.tau*self.data.tau  / self.data.params.volume 
            print "Jackknife...".ljust(20), "DONE"

    