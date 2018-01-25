from copy import deepcopy
from flowData import FlowDataReader
import latticePlotter as latplot
import numpy as np

class FlowResampler:
    def __init__(self, data, bootstrap=True, jacknife=True, bootSamples=500):
        if bootstrap:
            print "Bootstrapping Observables..."
            self.bootstrap = self.Bootstrap(data, bootSamples)
        if jacknife:
            print "Jackknifing Observables..."
            self.jacknife = self.Jacknife(data)
    
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

            for i in xrange(self.data.params.nFlows):
                for j in xrange(self.nBoots):
                    plaqBootstrap[i,j] = np.average(self.data.plaquetteMatrix[i][self.indexLists[j]])
                    energyBootstrap[i,j] = np.average(self.data.energyMatrix[i][self.indexLists[j]])
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

    class Jacknife:
        def __init__(self, data):
            self.data = deepcopy(data)
            self.createJackknife()

        def createJackknife(self):
            plaqJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))    
            topCharJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))
            topCharSquareJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))
            energyJackknife = np.zeros((self.data.params.nFlows, self.data.params.confNum))

            for i in xrange(self.data.params.nFlows):
                for j in xrange(self.data.params.confNum):
                    plaqJackknife[i,j] = np.average(np.delete(self.data.plaquetteMatrix[i,:], j))
                    energyJackknife[i,j] = np.average(np.delete(self.data.energyMatrix[i,:], j))
                    topCharJackknife[i,j] = np.average(np.delete(self.data.topChargeMatrix[i,:], j))
                    topCharSquareJackknife[i,j] = np.average(np.delete(self.data.topChargeMatrix[i,:], j)*np.delete(self.data.topChargeMatrix[i,:], j))
            
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

    