import logging

import ROOT

class Sample:
    def __init__(self, name, filename, selection = "1", xs = 1, lumi = 1, color = 1, nGen = 1):
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

        
    def getSampleWeight(self):
        weight = (self.xsec * self.lumi)/self.nGen
        logging.debug("Calculated mcweight for {0} to be {1}".format(self.name, weight))
        return weight 



class PlotBase:
    """
    Container to hold all relevant information about a plot.
    """
    def __init__(self, variable, selection, weight, binning, AxisTitle):
        self.variable = variable
        self.selection = selection
        self.weight = weight
        self.binning = binning
        self.nbins = binning[0]
        self.firstbin = binning[1]
        self.secondbin = binning[2]
        self.xTitle = AxisTitle

    def printVarLog(self):
        logging.debug("Using variable {0}".format(self.variable))
        logging.debug("Using selection {0}".format(self.selection))
        logging.debug("Using weight {0}".format(self.weight))
        logging.debug("Using AxisTitle {0}".format(self.xTitle))
        
