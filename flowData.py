import os as os
import sys as sys
import json as json
import numpy as np 

class Params:
    def __init__(self):
        self.hbarc = 0.197327
        self.confNum = 0
        self.latSpacing = 0
        self.chiConst = 0
        self.beta = 0
        self.volume = 0
        self.nflows = 0
        self.size = 0
        self.tauFinal = 0
        self.epsilon = 0
        self.label = ""
    
    def __str__(self):
        return "Number of configurations:\t" + str(self.confNum) + "\n" + \
                "Size of Lattice:\t\t" + str(self.size) + "^3 x " + str(self.size*2) + "\n" + \
                "Beta Value: \t\t\t" + str(self.beta) + "\n" + \
                "Lattice Spacing: \t\t" + str(self.latSpacing) + "\n" + \
                "Final Flow Time: \t\t" + str(self.tauFinal) + "\n" + \
                "Flow Step Size: \t\t" + str(self.epsilon) + "\n" 


class FlowDataReader:
    def __init__(self, dir):
        print "Checking Data in \"" + dir + "\"..."
        self.params = Params()
        self.checkInputFolder(dir)
        self.parseJsonFile(dir + "/" + self.jsonInput)
        with open(dir + "/params.dat", "w") as outfile:
            json.dump(self.params.__dict__, outfile, indent = 4)
        print "Found Dataset with these Properties...\n"
        print self.params
        print "Loading Data..."
        self.loadData(dir)
        print "Computing Averages..."
        self.averageData()
    
    def checkInputFolder(self, dir):
        if not os.path.exists(dir + "/PerGF"):
            sys.exit("ERROR: No PerGF data folder found.")
        jsonFiles = [file for file in os.listdir(dir) if file.endswith('.json')]
        if len(jsonFiles) == 0:
            sys.exit("ERROR: No JSON file found.")
        elif len(jsonFiles) > 1:
            sys.exit("ERROR: Too many JSON files found.")
        self.jsonInput = jsonFiles[0]
        if not os.path.exists(dir + "/PerTau"):
            os.mkdir(dir + "/PerTau")
            self.createPerTauData(dir)
        self.params.confNum = len(os.listdir(dir + "/PerGF"))

    def createPerTauData(self, dir):
        print "Creating per flow time data..."
        for file in sorted(os.listdir(dir + "/PerGF")):
            if file.endswith(".dat"):
                data = np.loadtxt(dir + "/PerGF/"+file, skiprows=1)
                for i in data[:]:
                    outfile = open(dir + "/PerTau/"+str(i[0])+".dat", "a+")
                    #[outfile.write(str(j) + " ") for j in i]
                    outfile.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]) )
                    outfile.write("\n")

    def parseJsonFile(self, jsonFile):
        self.jsonInput = json.load(open(jsonFile))
        self.params.size = self.jsonInput["LatticeSize"]["x"]
        self.params.volume = 2 * self.params.size**4
        self.params.beta = self.jsonInput["Action"]["params"]["beta"]
        self.params.latSpacing = self.getLatticeSpacing(self.lnar0(self.params.beta))
        self.params.nFlows = int (self.jsonInput["App"]["params"]["tauFinal"] \
                                / self.jsonInput["App"]["params"]["epsilon"] )
        self.params.tauFinal = self.jsonInput["App"]["params"]["tauFinal"]
        self.params.epsilon = self.jsonInput["App"]["params"]["epsilon"]
        self.params.chiConst = self.params.hbarc/self.params.latSpacing/self.params.volume**(0.25)
        self.params.label = str(self.params.size) + "$^3$ x " + str(2*self.params.size) + "  $\\beta = $" + str(self.params.beta) 


    def lnar0 (self, beta):
    	return -1.6805 - 1.7139*(beta-6.0) + 0.8155*(beta-6)*(beta-6.0) - \
               0.6667*(beta-6.0)*(beta-6.0)*(beta-6.0)

    def getLatticeSpacing(self, fValue):
    	return np.exp(fValue)*0.5

    def loadData(self, dir):
        self.tau = np.linspace(0, self.params.tauFinal - self.params.epsilon, self.params.nFlows)
        self.tauScaled = np.sqrt(self.tau * 8) * self.params.latSpacing
        self.tauR0 = self.tau*4 * (self.params.latSpacing*self.params.latSpacing)
        self.plaquetteMatrix = np.zeros((self.params.nFlows, self.params.confNum))
        self.topChargeMatrix = np.zeros((self.params.nFlows, self.params.confNum))
        self.energyMatrix = np.zeros((self.params.nFlows, self.params.confNum))
        self.topChargeSquare = np.zeros((self.params.nFlows, self.params.confNum))
        for i, file in enumerate(sorted(os.listdir(dir + "/PerTau"))):
            data = np.loadtxt(dir + "/PerTau/" + file)
            self.plaquetteMatrix[i] = data[:,1]
            self.topChargeMatrix[i] = data[:,2]
            self.energyMatrix[i] = data[:,3] / 64
            self.topChargeSquare[i] = data[:,2] * data[:,2]

    def averageData(self):
        self.plaquette = np.average(self.plaquetteMatrix, axis=1)
        self.energy = np.average(self.energyMatrix, axis=1) / self.params.volume
        self.topCharge = np.average(self.topChargeMatrix, axis=1)
        self.topSuscep = np.average(self.topChargeSquare, axis=1) **(0.25) * self.params.chiConst
        self.energyTauSquare = np.abs(np.average(self.energyMatrix, axis=1) * self.tau * self.tau / self.params.volume ) #* self.params.latSpacing*self.params.latSpacing#* self.params.latSpacing*self.params.latSpacing
        self.plaquetteStd = np.std(self.plaquetteMatrix, axis=1)
        self.energyStd = np.std(self.energyMatrix, axis=1) / self.params.volume
        self.topChargeStd = np.std(self.topChargeMatrix, axis=1)
        self.topSuscepStd = np.std(self.topChargeSquare ** (0.25), axis=1)  * self.params.chiConst
        self.energyTauSquareStd = np.std(self.energyMatrix, axis=1) * self.tau * self.tau / self.params.volume  #* self.params.latSpacing*self.params.latSpacing#* self.params.latSpacing*self.params.latSpacing
