import os as os
import sys as sys
import json as json
from collections import namedtuple

def getParameters(folders, dataSets):
    params = {}
    for dataSet in dataSets:
        paramData = json.loads(open(folders.data[dataSet] + "/params.dat").read(), object_hook=lambda d: namedtuple('Params', d.keys())(*d.values()))
        params[dataSet] = paramData
    return params

class Folders:
    def __init__(self, dataSets):
        self.dataSets = dataSets
        self.dataRoot = "Data/"
        self.data = {}
        for dataSet in dataSets:
            if not os.path.exists(self.dataRoot + dataSet):
                sys.exit("ERROR: No \"" + dataSet + "\" dataset folder found.")
            self.data[dataSet] = self.dataRoot + dataSet + "/"

        self.figures, self.figuresSingleConf = self.createFiguresFolders()
        self.results = "Results/"
        if not os.path.exists(self.results):
            os.mkdir(self.results)
        
    def createFiguresFolders(self):
        self.figuresRoot = "Figures/"
        if not os.path.exists(self.figuresRoot):
            os.mkdir(self.figuresRoot)
    
        figuresFolders = {}
        figuresSingleConfFolders = {}
        # Single Dataset Folders
        for dataSet in self.dataSets:
            figuresFolders[dataSet] = self.figuresRoot + dataSet + "/"
            figuresSingleConfFolders[dataSet] = self.figuresRoot + dataSet + "/SingleConf/"
            if not os.path.exists(figuresFolders[dataSet]):
                os.mkdir(figuresFolders[dataSet])
            if not os.path.exists(figuresSingleConfFolders[dataSet]):
                os.mkdir(figuresSingleConfFolders[dataSet])
        
        return figuresFolders, figuresSingleConfFolders