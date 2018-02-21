import flowAnalysis as flow
import analysisUtils as utils
import latticePlotter as latplot
from flowData import FlowDataReader
from flowResampler import FlowResampler
from autocorrAnalysis import Autocorrelation
from discretizationEffects import plotContLimit

 
# Plot and Save Flowed Data
def basicAnalysis(data, dataTag, folders):
    flow.plotData(data, folders.figures[dataTag], suffix="_avg")
    flow.saveData(data, folders.results, dataTag, suffix="_avg")

# Resample Data
def resampleAnalysis(data, dataTag, folders, bootstrap=True, jackknife=True):
    resampler = FlowResampler(data, bootstrap, jackknife)

    if bootstrap:
        # Plot and Save Bootsrapped Data
        flow.plotData(resampler.bootstrap.data, folders.figures[dataTag], suffix="_boot")
        flow.saveData(resampler.bootstrap.data, folders.results, dataTag, suffix="_boot")

    if jackknife:
        # Plot and Save Jacknife Data
        flow.plotData(resampler.jackknife.data, folders.figures[dataTag], suffix="_jkkf")
        flow.saveData(resampler.jackknife.data, folders.results, dataTag, suffix="_jkkf")
    return resampler

# Plots for Single Configuration Data
def singleConfAnalysis(data, dataTag, folders):
    flow.singleConfPlots(data, folders.figuresSingleConf[dataTag])

def topChargeHistograms(data, dataTag, folders):
    flow.topChargeHistograms(data, folders.figures[dataTag], step="initial")
    flow.topChargeHistograms(data, folders.figures[dataTag], step="final")

def MCHistoryAnalysis(data, dataTag, folders):
    flow.MCHistoryPlots(data, folders.figures[dataTag])

def autocorrelationAnalysis(data, dataTag, folders, resampler=None):
    autocorrData = Autocorrelation(data)
    autocorrData.plotAutocorrelation(folders.figures[dataTag], step="initial")
    autocorrData.plotAutocorrelation(folders.figures[dataTag], step="final")
    if resampler:
        autocorrData.adjustError(data, resampler)
        flow.plotData(resampler.jackknife.data, folders.figures[dataTag], suffix="_autocorr_jkkf")
        flow.saveData(resampler.jackknife.data, folders.results, dataTag, suffix="_jkkf")
        flow.plotData(resampler.bootstrap.data, folders.figures[dataTag], suffix="_autocorr_boot")
        flow.saveData(resampler.bootstrap.data, folders.results, dataTag, suffix="_boot")
    else:
        autocorrData.adjustError(data)

def collectiveAnalysis(dataSetTags, folders):
    params = utils.getParameters(folders, dataSetTags)
    flow.makeCollectivePlots(dataSetTags, folders, params)
    #flow.energyContinuumLimit(dataSetTags, folders, params)
    #flow.lambdaFit(dataSetTags, folders, params)
    

if __name__ == '__main__':
    latplot.init()
    dataSetTags = ["24_b6.00", "28_b6.10", "32_b6.20", ]#"48_b6.45"]
    folders = utils.Folders(dataSetTags)

    for dataTag in dataSetTags:
        # Load Data
        data = FlowDataReader(folders.data[dataTag])
        #basicAnalysis(data, dataTag, folders)
        resampler = resampleAnalysis(data, dataTag, folders)
        #singleConfAnalysis(data, dataTag, folders)
        #topChargeHistograms(data, dataTag, folders)
        #MCHistoryAnalysis(data, dataTag, folders)
        #autocorrelationAnalysis(data, dataTag, folders, resampler=resampler)
        print "\n\n"
    plotContLimit()
    collectiveAnalysis(dataSetTags, folders)
    
