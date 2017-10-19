import logging

import modules.plotting
import modules.classes

import ROOT


def makeDataMCPlot(PlotBaseObj, Data, MC, normalized = False, drawHistos = True, outname = None, outputformat = "pdf"):
    variable = PlotBaseObj.variable
    binning = PlotBaseObj.binning
    varselection = PlotBaseObj.selection

    hMC =modules.plotting.getHistoFromTree(MC.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                           "({0} && {1})".format(PlotBaseObj.selection, MC.selection),
                                           weight = str(MC.getSampleWeight()), normalized = normalized)
    hData =modules.plotting.getHistoFromTree(Data.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                             "({0} && {1})".format(PlotBaseObj.selection, Data.selection), normalized = normalized)

    yTitle = "Events"
    if normalized:
        yTitle = "normalized Events"
    
    modules.plotting.setStyle(hMC, "Line", MC.color, PlotBaseObj.xTitle, yTitle)
    modules.plotting.setStyle(hData, "Points", Data.color, PlotBaseObj.xTitle, yTitle)
    
    h2Draw = [ (hMC, "histoe"), (hData, "P") ]
    if drawHistos:
        canvas = modules.plotting.drawHistos(h2Draw)


    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
        
    #raw_input(".....")
        
    return hMC, hData
        



def makeDataMCPlotwRatio(PlotBaseObj, Data, MC, normalized = False, outname = None, outputformat = "pdf"):
    variable = PlotBaseObj.variable
    binning = PlotBaseObj.binning
    varselection = PlotBaseObj.selection
    #Get histograms:
    hMC, hData = makeDataMCPlot(PlotBaseObj, Data, MC, normalized, drawHistos = False)

    ratioLine, ratios, div = modules.plotting.getRatioPlot(hData, [hMC])

    canvas = modules.plotting.getCanvas(ratio = True)

    h2Draw = [ (hMC, "histoe"), (hData, "P") ]
    r2Draw = [ (ratioLine, "histoe") , (ratios[0], "sameP") ]


    modules.plotting.drawHistos(h2Draw, orderedRatioList = r2Draw, canvas = canvas)

    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
    
    #raw_input("")
    

if __name__ == "__main__":
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/ttbar/ttbar_v1_partial.root"
    DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/MuonEG/MuonEG_v1_partial.root"

    MCSample = modules.classes.Sample("ttbar", MCInput, "1", 1, 1, ROOT.kRed)
    DataSample = modules.classes.Sample("MuonEG", DataInput, color = ROOT.kBlack)

    variable = "offJet_pt"
    binning = [30,0,300]
                
    

                                           
    makeDataMCPlot(variable, binning, DataSample, MCSample, normalized = True)
