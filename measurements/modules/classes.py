import logging

import ROOT

class Sample:
    def __init__(self, name, filename, selection = "1", xs = 1, lumi = 1, color = 1, nGen = 1, legendText = None, legendstyle = "l", weight = "1"):
        logging.debug("Setting up sample class: {0}".format(name))
        self.filename = filename
        self.name = name
        self.xsec = xs
        self.selection = selection
        self.lumi = lumi
        self.color = color
        
        self.rootfile = ROOT.TFile.Open(self.filename)
        self.tree = self.rootfile.Get("tree")
        self.nEvents = self.tree.GetEntries()
        self.nGen = nGen

        self.weight = weight
        
        if legendText is None:
            self.legend = [self.name]
        else:
            self.legend = [legendText]

        self.legendstyle = legendstyle

        
    def getSampleWeight(self):
        weight = (self.xsec * self.lumi)/self.nGen
        logging.subdebug("Calculated mcweight for {0} to be {1}".format(self.name, weight))
        return weight 



class PlotBase:
    """
    Container to hold all relevant information about a plot.
    """
    def __init__(self, variable, selection, weight, binning, AxisTitle, color = ROOT.kBlack, legendText = None, LegendPosition = [0.6,0.6,0.9,0.9]):
        self.variable = variable
        self.selection = selection
        self.weight = weight
        self.binning = binning
        self.nbins = binning[0]
        self.firstbin = binning[1]
        self.secondbin = binning[2]
        self.xTitle = AxisTitle
        self.color = color
        
        if legendText is None:
            self.legend = [self.variable]
        else:
            self.legend = [legendText]

        self.legendstyle = "l"

        self.LegendPosition = LegendPosition

    def printVarLog(self):
        logging.debug("Using variable {0}".format(self.variable))
        logging.debug("Using selection {0}".format(self.selection))
        logging.debug("Using weight {0}".format(self.weight))
        logging.debug("Using AxisTitle {0}".format(self.xTitle))
        

class PlotBase2D:
    def __init__(self, xVariable, yVariable, selection, weight, xBinning, yBinning, xAxisTitle, yAxisTitle, legendText = None, LegendPosition = [0.6,0.6,0.9,0.9]):
        self.xVariable = xVariable
        self.yVariable = yVariable
        self.selection = selection
        self.weight = weight
        
        self.xBinning =xBinning
        self.xNbins = xBinning[0]
        self.xFirstbin = xBinning[1]
        self.xSecondbin = xBinning[2]
        self.xTitle = xAxisTitle

        self.yBinning =yBinning
        self.yNbins = yBinning[0]
        self.yFirstbin = yBinning[1]
        self.ySecondbin = yBinning[2]
        self.yTitle = yAxisTitle
        
        
        if legendText is None:
            self.legend = ["{0}_{1}".format(self.xVariable,self.yVariable)]
        else:
            self.legend = [legendText]

        self.legendstyle = "l"

        self.LegendPosition = LegendPosition

    def printVarLog(self):
        logging.debug("Using x variables:")
        logging.debug("Using variable {0}".format(self.xVariable))
        logging.debug("Using AxisTitle {0}".format(self.xTitle))
        logging.debug("Using y variables:")
        logging.debug("Using variable {0}".format(self.yVariable))
        logging.debug("Using AxisTitle {0}".format(self.yTitle))
        logging.debug("Common:")
        logging.debug("Using selection {0}".format(self.selection))
        logging.debug("Using weight {0}".format(self.weight))

    def get1DObjects(self, xName = None, yName = None, xColor = ROOT.kRed, yColor = ROOT.kBlue, xTitle = None):
        if xName is None:
            xName = self.xVariable
        if yName is None:
            yName = self.yVariable
        if xTitle is None:
            xTitle = self.xTitle
        xObj = PlotBase(self.xVariable, self.selection, self.weight, self.xBinning, xTitle,  xColor, legendText = self.xTitle,  LegendPosition = self.LegendPosition)
        yObj = PlotBase(self.yVariable, self.selection, self.weight, self.yBinning, xTitle,  yColor, legendText = self.yTitle, LegendPosition = self.LegendPosition)
        return xObj, yObj

        
        
class StackBase:
    def __init__(self):
        pass

    def setLegend(self):
        pass
