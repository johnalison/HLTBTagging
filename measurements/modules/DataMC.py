import logging

import modules.plotting
import modules.classes

import ROOT
from ConfigParser import SafeConfigParser

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

def makeSumDMCPlot(PlotBaseObj, Samples2Stack, xVarBase, nIter, iterSelection, data = None, normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, normalizetoData = False):

    StackHistos = []
    StackSum = None

    logging.info("Processing MC")
    for isample, sample in enumerate(Samples2Stack):
        logging.debug("Processing Sample: {}".format(sample.name))
        if normalized:
            thisweight = sample.weight
        else:
            thisweight = "{0} * {1}".format(sample.getSampleWeight(), sample.weight)


        for i in range(nIter):
            thisVarBase = xVarBase.replace("?",str(i))
            thisIterSelection = iterSelection.replace("?",str(i))
            selection = "({0} && {1} && {2})".format(PlotBaseObj.selection, sample.selection, thisIterSelection).replace("?",str(i))
            if i == 0:
                logging.debug("--->"+thisVarBase)
                logging.debug("--->"+thisIterSelection)
                StackHistos.append( modules.plotting.getHistoFromTree( sample.tree, thisVarBase, PlotBaseObj.binning,
                                                                       selection,
                                                                       weight = thisweight ) )
            else:
                StackHistos[isample].Add(modules.plotting.getHistoFromTree( sample.tree, thisVarBase, PlotBaseObj.binning,
                                                                            selection,
                                                                            weight = thisweight))
                
            
        if isample == 0:
            StackSum = StackHistos[0].Clone()
            StackSum.SetName("Stacksum_"+StackSum.GetName())
            StackSum.SetTitle("Stacksum_"+StackSum.GetTitle())
        else:
            StackSum.Add(StackHistos[isample])

    logging.info("Processing data")
    if data is None:
        logging.warning("No data set -> Setting data to Stacksum")
        hData = StackSum.Clone()
        hData.SetName("Data_"+StackSum.GetName())
    else:
        #Get Data from tree
        for i in range(nIter):
            thisVarBase = xVarBase.replace("?",str(i))
            thisIterSelection = iterSelection.replace("?",str(i))
            selection = "({0} && {1} && {2})".format(PlotBaseObj.selection, data.selection, thisIterSelection)
            selection = selection.replace("?",str(i))
            if i == 0:
                hData = modules.plotting.getHistoFromTree( data.tree, thisVarBase , PlotBaseObj.binning,
                                                           selection,
                                                           weight = data.weight)
            else:
                hData.Add(modules.plotting.getHistoFromTree( data.tree, thisVarBase , PlotBaseObj.binning,
                                                             selection,
                                                             weight = data.weight))
                
    StackDMCPlotBase(StackSum, StackHistos, hData, PlotBaseObj, Samples2Stack, data, normalized, drawRatio, outname, outputformat, label, normalizetoData)





def StackDMCPlotBase(StackSum, StackHistos, hData, PlotBaseObj, Samples2Stack, data = None, normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, normalizetoData = False):


    if label is not None and isinstance(label, list):
        for l in label:
            if not isinstance(l, ROOT.TLatex):
                logging.error("All labels are required to be of type ROOT.TLatex")
                label.remove(l)
    elif label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    elif (label is not None and isinstance(label, ROOT.TLatex)) or label is None:
        pass
    else:
        logging.error("Something is happening here... :(")

    logging.info("StackHistos: %s",StackHistos)
    
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    yTitle = "Events"
    if normalized:
        yTitle = "normalized Events"
    """ 
    if normalized:
        logging.debug("Calculating scale factor for stack")
        try:
            1/float(StackSum.Integral())
        except ZeroDivisionError:
            logging.error("ZeroDevision Error. Disableing scaling")
            normalized = False
        else:
            for ihisto, histo in enumerate(StackHistos):
                logging.debug("Normalizing {0} from {1}".format(histo.GetName(), Samples2Stack[ihisto].name))
                histo.Scale(1/float(StackSum.Integral()))
            StackSum.Scale(1/float(StackSum.Integral()))
    """
    if normalized:
        MCscale = hData.Integral()/StackSum.Integral()
        StackSum.Scale(MCscale)
        logging.warning("MCScale %s", MCscale)
        NormLabel = modules.utils.getLabel("MC normalized to Data", 0.6)
        if label is None:
            label = [NormLabel]
        if label is isinstance(label,ROOT.TLatex):
            label = [label + NormLabel]
        else:
            label.append(NormLabel)
            
    ##Make Stack
    ObjectsforLegend = []
    logging.debug("Making stack")
    HStack = ROOT.THStack("HStack_"+StackHistos[0].GetName(), "")
    for ihisto, histo in enumerate(StackHistos):
        #print "---------------------"
        #print Samples2Stack[ihisto].color, Samples2Stack[ihisto].name, histo.GetName()
        modules.plotting.setStyle(histo, "Solid", Samples2Stack[ihisto].color, PlotBaseObj.xTitle, yTitle)
        #print histo.Integral()
        if normalized:
            histo.Scale(MCscale)
        HStack.Add(histo)
        #print histo.Integral()
        ObjectsforLegend.append( (histo, Samples2Stack[ihisto].legend[0], "F") )
    #raw_input("....")
    modules.plotting.setStyle(StackSum, "Line", ROOT.kBlack, PlotBaseObj.xTitle, yTitle)

    if True:
        thisOutFile = ROOT.TFile("histos_"+str(outname.split("/")[-1])+"_"+str(ROOT.gRandom.Integer(1000))+str(".root"),  "RECREATE")
        print thisOutFile
        thisOutFile.cd()
        for ihisto, histo in enumerate(StackHistos):
            histo.Write()
        thisOutFile.Close()

    
    #Make Lumi label
    if data is None:
        ObjectsforLegend.append( (hData, "Data (Stacksum)", "P") )
    else:
        ObjectsforLegend.append( ( hData, data.legend[0], "P") )

    """
    if normalized:
        logging.debug("Calculating scale factor for data")
        try:
            1/float(hData.Integral())
        except ZeroDivisionError:
            logging.error("ZeroDevision Error. Disableing scaling")
            normalized = False
        else:
            logging.info("Normalizing Data!")
            hData.Scale(1/float(hData.Integral()))
    """
    modules.plotting.setStyle(hData, "Points", ROOT.kBlack, PlotBaseObj.xTitle, yTitle)
    if drawRatio:
        logging.debug("Making Ratio")
        ratioLine, ratios, div = modules.plotting.getRatioPlot(hData, [StackSum])

    StackErrorBand = modules.plotting.makeErrorband(StackSum)
    RatioErrorBand = modules.plotting.makeratioErrorband(StackErrorBand)
        
    canvas = modules.plotting.getCanvas(ratio = drawRatio)

    h2Draw = [ (HStack, "histo"), (StackErrorBand, "same"), (hData, "AE1X0") ]
    r2Draw = [ (ratioLine, "histoe") , (RatioErrorBand, "same2"), (ratios[0], "sameP") ]

    modules.plotting.drawHistos(h2Draw, stackindex = 0, canvas = canvas, orderedRatioList = r2Draw, yTitle = yTitle)
    HStack.GetYaxis().SetTitle(yTitle)
    HStack.GetYaxis().SetTitleOffset(1.3 *
                                     styleconfig.getfloat("HistoStyle","yTitleOffsetscale")*
                                     styleconfig.getfloat("HistoStyle","yRatioTitleOffsetscale"))
    canvas.cd(0)
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")
    if label is not None:
        if isinstance(label, list):
            for l in label:
                l.Draw("same")
        else:
            label.Draw("same")
    legpos = PlotBaseObj.LegendPosition
    legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3], False)
    legend.Draw("same")

    
    
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)



def makeStackDMCPlot(PlotBaseObj, Samples2Stack, data = None, normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, normalizetoData = False):
    StackHistos = []
    StackSum = None
    for isample, sample in enumerate(Samples2Stack):
        if normalized:
            thisweight = sample.weight
        else:
            thisweight = "{0} * {1}".format(sample.getSampleWeight(), sample.weight)
        StackHistos.append( modules.plotting.getHistoFromTree( sample.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                                               "({0} && {1})".format(PlotBaseObj.selection, sample.selection),
                                                               weight = thisweight) )
        if isample == 0:
            StackSum = StackHistos[0].Clone()
            StackSum.SetName("Stacksum_"+StackSum.GetName())
            StackSum.SetTitle("Stacksum_"+StackSum.GetTitle())
        else:
            StackSum.Add(StackHistos[isample])


    if data is None:
        logging.warning("No data set -> Setting data to Stacksum")
        hData = StackSum.Clone()
        hData.SetName("Data_"+StackSum.GetName())
    else:
        #Get Data from tree
        hData = modules.plotting.getHistoFromTree( data.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                                   "({0} && {1})".format(PlotBaseObj.selection, data.selection),
                                                   weight = data.weight)
        

    StackDMCPlotBase(StackSum, StackHistos, hData, PlotBaseObj, Samples2Stack, data, normalized, drawRatio, outname, outputformat, labels, normalizetoData)



"""
def makeStackDMCPlot(PlotBaseObj, Samples2Stack, data = None, normalized = False, drawRatio = True, outname = None, outputformat = "pdf", labels = None, normalizetoData = False):
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    yTitle = "Events"
    if normalized:
        yTitle = "normalized Events"
    

    StackHistos = []
    StackSum = None
    for isample, sample in enumerate(Samples2Stack):
        if normalized:
            thisweight = sample.weight
        else:
            thisweight = "{0} * {1}".format(sample.getSampleWeight(), sample.weight)
        StackHistos.append( modules.plotting.getHistoFromTree( sample.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                                               "({0} && {1})".format(PlotBaseObj.selection, sample.selection),
                                                               weight = thisweight) )
        if isample == 0:
            StackSum = StackHistos[0].Clone()
            StackSum.SetName("Stacksum_"+StackSum.GetName())
            StackSum.SetTitle("Stacksum_"+StackSum.GetTitle())
        else:
            StackSum.Add(StackHistos[isample])

    if normalized:
        logging.debug("Calculating scale factor for stack")
        try:
            1/float(StackSum.Integral())
        except ZeroDivisionError:
            logging.error("ZeroDevision Error. Disableing scaling")
            normalized = False
        else:
            for ihisto, histo in enumerate(StackHistos):
                logging.debug("Normalizing {0} from {1}".format(histo.GetName(), Samples2Stack[ihisto].name))
                histo.Scale(1/float(StackSum.Integral()))
            StackSum.Scale(1/float(StackSum.Integral()))

    ##Make Stack
    ObjectsforLegend = []
    logging.debug("Making stack")
    HStack = ROOT.THStack("HStack_"+StackHistos[0].GetName(), "")
    for ihisto, histo in enumerate(StackHistos):
        modules.plotting.setStyle(histo, "Solid", Samples2Stack[ihisto].color, PlotBaseObj.xTitle, yTitle)
        HStack.Add(histo)
        ObjectsforLegend.append( (histo, Samples2Stack[ihisto].legend[0], "F") )
        
    modules.plotting.setStyle(StackSum, "Line", ROOT.kBlack, PlotBaseObj.xTitle, yTitle)
    
    #Make Lumi label
    if data is None:
        logging.warning("No data set -> Setting data to Stacksum")
        hData = StackSum.Clone()
        hData.SetName("Data_"+StackSum.GetName())
        ObjectsforLegend.append( (hData, "Data (Stacksum)", "P") )
    else:
        #Get Data from tree
        hData = modules.plotting.getHistoFromTree( data.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                                   "({0} && {1})".format(PlotBaseObj.selection, data.selection),
                                                   weight = data.weight) 
        ObjectsforLegend.append( ( hData, data.legend[0], "P") )
        pass

    if normalized:
        logging.debug("Calculating scale factor for data")
        try:
            1/float(hData.Integral())
        except ZeroDivisionError:
            logging.error("ZeroDevision Error. Disableing scaling")
            normalized = False
        else:
            logging.info("Normalizing Data!")
            hData.Scale(1/float(hData.Integral()))

    modules.plotting.setStyle(hData, "Points", ROOT.kBlack, PlotBaseObj.xTitle, yTitle)
    if drawRatio:
        logging.debug("Making Ratio")
        ratioLine, ratios, div = modules.plotting.getRatioPlot(hData, [StackSum])

    canvas = modules.plotting.getCanvas(ratio = drawRatio)

    h2Draw = [ (HStack, "histo"), (hData, "AE0") ]
    r2Draw = [ (ratioLine, "histoe") , (ratios[0], "sameP") ]

    modules.plotting.drawHistos(h2Draw, stackindex = 0, canvas = canvas, orderedRatioList = r2Draw, yTitle = yTitle)
    HStack.GetYaxis().SetTitle(yTitle)
    HStack.GetYaxis().SetTitleOffset(HStack.GetYaxis().GetTitleOffset()*styleconfig.getfloat("HistoStyle","yTitleOffsetscale")*0.5)
    canvas.cd(0)
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")
    legpos = PlotBaseObj.LegendPosition
    legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3], False)
    legend.Draw("same")

    
    
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
"""
    

if __name__ == "__main__":
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/ttbar/ttbar_v1_partial.root"
    DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/MuonEG/MuonEG_v1_partial.root"

    MCSample = modules.classes.Sample("ttbar", MCInput, "1", 1, 1, ROOT.kRed)
    DataSample = modules.classes.Sample("MuonEG", DataInput, color = ROOT.kBlack)

    variable = "offJet_pt"
    binning = [30,0,300]
                
    

                                           
    makeDataMCPlot(variable, binning, DataSample, MCSample, normalized = True)
