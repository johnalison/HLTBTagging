import logging
from copy import deepcopy
from ConfigParser import SafeConfigParser

import modules.plotting
import modules.classes
import modules.utils

import ROOT


def makecompPlotwRatio(PlotBaseObj, Sample1, Sample2, normalized = False, outname = None, outputformat = "pdf"):
    variable = PlotBaseObj.variable
    binning = PlotBaseObj.binning
    varselection = PlotBaseObj.selection
    #Get histograms:
    hSample2, hSample1 = makecompPlot(PlotBaseObj, Sample1, Sample2, normalized, drawHistos = False)

    ratioLine, ratios, div = modules.plotting.getRatioPlot(hSample1, [hSample2])

    canvas = modules.plotting.getCanvas(ratio = True)

    h2Draw = [ (hSample2, "histoe"), (hSample1, "histoe") ]
    r2Draw = [ (ratioLine, "histoe") , (ratios[0], "sameP") ]


    modules.plotting.drawHistos(h2Draw, orderedRatioList = r2Draw, canvas = canvas)

    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
    


def compareJetTypes(PlotBaseObjs, Sample, normalized = False, outname = None, outputformat = "pdf", label = None, hObjects = None):
    hObjs = []

    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    
    yTitle = "Events"
    if normalized:
        yTitle = "normalized Units"

    ObjectsforLegend = []
    h2Draw = []

    if hObjects is None:
        logging.debug("Making hisograms from tree")
        for iPlotBaseObj, PlotBaseObj in enumerate(PlotBaseObjs):
            hObjs.append(
                modules.plotting.getHistoFromTree(Sample.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                                  "({0} && {1})".format(PlotBaseObj.selection, Sample.selection),
                                                  normalized = normalized, weight = Sample.weight)
            )
    else:
        hObjs = hObjects

    for iObj, hObj in enumerate(hObjs):
        modules.plotting.setStyle(hObj, "Line", PlotBaseObjs[iObj].color, PlotBaseObjs[iObj].xTitle, yTitle)
        ObjectsforLegend.append( (PlotBaseObjs[iObj], hObj) )
        h2Draw.append( (hObj, "histoe" ) )

    drawHistos = True
    if drawHistos:
        canvas = modules.plotting.drawHistos(h2Draw)
        legpos = PlotBaseObjs[0].LegendPosition
        legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3])
        legend.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            label.Draw("same")
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

def compareSumJetTypes(PlotBaseObjs, Sample, xVarBases, nIter, iterSelections = None, normalized = False, darindivhistos = False, outname = None, outputformat = "pdf", label = None):

    if iterSelections is None:
        len(PlotBaseObjs)*["1"]
    
    hObjs = []
        
    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    
    yTitle = "Events"
    if normalized:
        yTitle = "normalized Units"

    sphistos = len(PlotBaseObjs)*[[]]
    
    logging.debug("Making hisograms from tree")
    for i in range(nIter):
        if i == 0:
            for iPlotBaseObj, PlotBaseObj in enumerate(PlotBaseObjs):
                xVarBase = xVarBases[iPlotBaseObj]
                iterSelection = iterSelections[iPlotBaseObj]
                logging.debug("--->"+xVarBase.replace("?",str(i)))
                logging.debug("--->"+iterSelection.replace("?",str(i)))
                hRet = modules.plotting.getHistoFromTree(Sample.tree, xVarBase.replace("?",str(i)) , PlotBaseObj.binning,
                                                          "({0} && {1} && {2})".format(PlotBaseObj.selection, Sample.selection, iterSelection.replace("?",str(i))),
                                                          normalized = normalized, weight = Sample.weight)
                hObjs.append(hRet)
                sphistos[iPlotBaseObj].append(hRet.Clone())
        else:
            for iPlotBaseObj, PlotBaseObj in enumerate(PlotBaseObjs):
                xVarBase = xVarBases[iPlotBaseObj]
                iterSelection = iterSelections[iPlotBaseObj]
                htemp = modules.plotting.getHistoFromTree(Sample.tree, xVarBase.replace("?",str(i)) , PlotBaseObj.binning,
                                                          "({0} && {1} && {2})".format(PlotBaseObj.selection, Sample.selection, iterSelection.replace("?",str(i))),
                                                          normalized = normalized, weight = Sample.weight)
                hObjs[iPlotBaseObj].Add(htemp)
                sphistos[iPlotBaseObj].append(htemp)
                
    ObjectsforLegend = []
    h2Draw = []
    for iObj, hObj in enumerate(hObjs):
        modules.plotting.setStyle(hObj, "Line", PlotBaseObjs[iObj].color, PlotBaseObjs[iObj].xTitle, yTitle)
        ObjectsforLegend.append( (PlotBaseObjs[iObj], hObj) )
        h2Draw.append( (hObj, "histoe" ) )
        
    drawHistos = True
    if drawHistos:
        canvas = modules.plotting.drawHistos(h2Draw)
        legpos = PlotBaseObjs[0].LegendPosition
        legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3])
        legend.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            label.Draw("same")
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

    return h2Draw


def compareSumJetSamples(PlotBaseObj, Samples, xVarBase, nIter,  iterSelection = "1", normalized = False, darindivhistos = False, outname = None, outputformat = "pdf", label = None):
    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    
    yTitle = "Events"
    if normalized:
        yTitle = "normalized Units"

    logging.debug("iterSel:"+iterSelection)
    ObjectsforLegend = []
    h2Draw = []
    iSample = 0
    for sample, postfix, nicename in Samples:
        logging.debug("Summing histo for sample: {0}".format(nicename))
        h2Draw.append(compareSumJetTypes([PlotBaseObj], sample, [xVarBase], nIter, iterSelections = [iterSelection], normalized = normalized)[0])
        ObjectsforLegend.append( ( h2Draw[iSample][0], nicename, "l"  ) )
        modules.plotting.setStyle(h2Draw[iSample][0], "Line", sample.color, PlotBaseObj.xTitle, yTitle)
        iSample+=1

    drawHistos = True
    if drawHistos:
        canvas = modules.plotting.drawHistos(h2Draw)
        for i in range(1,len(h2Draw)):
            h2Draw[i][0].Draw("same"+h2Draw[i][1])
        legpos = PlotBaseObj.LegendPosition
        legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3], usingPlotBase = False)
        legend.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            label.Draw("same")
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

    
        
def compareSamples(PlotBaseObjs, Samples, normalized = True, outname = None, outputformat = "pdf", label = None):
    hObjs = []

    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    
    yTitle = "Events"
    if normalized:
        yTitle = "normalized Units"


    if len(PlotBaseObjs) == len(Samples):
        for i in range(len(Samples)):
            hObjs.append(
                modules.plotting.getHistoFromTree(Samples[i].tree, PlotBaseObjs[i].variable, PlotBaseObjs[i].binning,
                                                  "({0} && {1})".format(PlotBaseObjs[i].selection, Samples[i].selection),
                                                  normalized = normalized, weight = Samples[i].weight)
                )
    else:
        logging.error("Please set Number of PlotObjs equal to Samples")
        return False


    ObjectsforLegend = []
    h2Draw = []
    for iObj, hObj in enumerate(hObjs):
        modules.plotting.setStyle(hObj, "Line", PlotBaseObjs[iObj].color, PlotBaseObjs[iObj].xTitle, yTitle)
        ObjectsforLegend.append( (PlotBaseObjs[iObj], hObj) )
        h2Draw.append( (hObj, "histoe" ) )

    drawHistos = True
    if drawHistos:
        canvas = modules.plotting.drawHistos(h2Draw)
        legpos = PlotBaseObjs[0].LegendPosition
        legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3])
        legend.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            label.Draw("same")
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

def fill2DPlot(PlotBase2DObj, Sample, xVar = None, yVar = None, Selection = "1", Weight = "1"):
    hRet = None

    logging.debug("Making hisograms from tree")
    if xVar is None:
        xVar = PlotBase2DObj.xVariable
    if yVar is None:
        yVar = PlotBase2DObj.yVariable

    #logging.debug("--> "+Selection)
        
    hRet = modules.plotting.get2DHistoFromTree(Sample.tree, xVar, yVar, PlotBase2DObj.xBinning, PlotBase2DObj.yBinning, Selection, "({0} * {1})".format(Weight, Sample.weight))

    modules.plotting.setStyle(hRet, "2D", xAxisTitle = PlotBase2DObj.xTitle, yAxisTitle = PlotBase2DObj.yTitle)
    
    
    return hRet
     
def fillandSum2D(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection):    

    hRet = None
    sephistos = []
    
    Selection = "({0}) && ({1})".format(PlotBase2DObj.selection, Sample.selection)
    for i in range(nIter):
        if i == 0:
            hRet = fill2DPlot( PlotBase2DObj, Sample, xVarBase.replace("?",str(i)), yVarBase.replace("?",str(i)), "({0}) && ({1})".format(Selection, iterSelection.replace("?",str(i))), "1")
            sephistos.append(deepcopy(hRet.Clone()))
            logging.debug("--->"+xVarBase.replace("?",str(i)))
            logging.debug("--->"+yVarBase.replace("?",str(i)))
        else:
            htemp = fill2DPlot( PlotBase2DObj, Sample, xVarBase.replace("?",str(i)), yVarBase.replace("?",str(i)), "({0}) && ({1})".format(Selection, iterSelection.replace("?",str(i))), "1" )
            hRet.Add(htemp)
            sephistos.append(deepcopy(htemp))

    return hRet, sephistos

def make2DSummedPlot(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection = "1", outname = None, outputformat = "pdf", label = None, drawindividualhistos = False, LogZ = False, drawProjection = False, projectionTitle = None, printCorrelation = True):
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")
    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
        
    histo, sepHistos = fillandSum2D(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection)
    
    
    canvas = modules.plotting.getCanvas(colz = True)
    canvas.cd()
    if LogZ:
        canvas.SetLogz()
    histo.Draw("colz")
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")
    if label is not None:
        label.Draw("same")

    if printCorrelation:
        xstart = styleconfig.getfloat("CMSLabel","xStart")
        corrlabel = modules.utils.getLabel("Correlation: {0:.2f}".format(histo.GetCorrelationFactor()), xstart, pos = "top")
        corrlabel.Draw("same")
                                           
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

    if drawindividualhistos:
        logging.info("Drawing individual histograms"+str(drawindividualhistos))
        for ih, hist in enumerate(sepHistos):
            if LogZ:
                canvas.SetLogz(0)
            hist.GetXaxis().SetTitle(hist.GetXaxis().GetTitle()+"[{0}]".format(ih))
            #histo.GetYaxis().SetTitle(histo.GetYaxis().GetTitle()+"[{0}]".format(ih))
            hist.Draw("colz")
            CMSL1, CMSL2 = modules.utils.getCMStext()
            CMSL1.Draw("same")
            CMSL2.Draw("same")
            if label is not None:
                label.Draw("same")
            if printCorrelation:
                xstart = styleconfig.getfloat("CMSLabel","xStart")
                corrlabel = modules.utils.getLabel("Correlation: {0:.2f}".format(hist.GetCorrelationFactor()), xstart, pos = "top")
                corrlabel.Draw("same")

            canvas.Update()

            if outname is not None:
                modules.utils.savePlot(canvas, outname+"_"+str(ih), outputformat)

        
        
    if drawProjection:
        XPlotBaseObj, YPlotBaseObj = PlotBase2DObj.get1DObjects(xTitle = projectionTitle)
        
        compareJetTypes([XPlotBaseObj, YPlotBaseObj], Sample, normalized = False, outname = outname+"_projection", outputformat = "pdf", label = label,
                        hObjects = [histo.ProjectionX(), histo.ProjectionY()]
        )
        



def compareHistos(hList, legendList, colorList, normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None):
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

    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    yTitle = "Events"
    if normalized:
        yTitle = "normalized Events"

    if normalized:
        for histo in hList:
            try:
                1/float(histo.Integral())
            except ZeroDivisionError:
                logging.error("ZeroDevision Error. Disableing scaling")
                normalized = False
            else:
                logging.info("Normalizing")
                histo.Scale(1/float(histo.Integral()))


    canvas = modules.plotting.getCanvas(ratio = drawRatio)

    ObjectsforLegend = []
    h2Draw = []
    for ihisto, histo in enumerate(hList):
        modules.plotting.setStyle(histo, "Line", colorList[ihisto], histo.GetXaxis().GetTitle(), yTitle)
        ObjectsforLegend.append( (histo, legendList[ihisto], "L") )
        h2Draw.append( (histo, "histoe") )

        
    if drawRatio:
        logging.debug("Making Ratio")
        hList[0].GetYaxis().SetTitleOffset(hList[0].GetYaxis().GetTitleOffset()*
                                           styleconfig.getfloat("HistoStyle","yTitleOffsetscale")*
                                           styleconfig.getfloat("HistoStyle","yRatioTitleOffsetscale")*0.8)

        ratioLine, ratios, div = modules.plotting.getRatioPlot(hList[0], hList[1:])

    ratioLine.SetLineColor(colorList[0])
    r2Draw = [(ratioLine , "histoe")]
    for r in ratios:
        r2Draw.append( (r, "sameP") )

    modules.plotting.drawHistos(h2Draw, canvas = canvas, orderedRatioList = r2Draw, yTitle = yTitle)
    
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
    legpos = [0.6, 0.6, 0.9, 0.9]
    legend = modules.utils.getLegend(ObjectsforLegend, legpos[0],legpos[1],legpos[2],legpos[3], False)
    legend.Draw("same")

    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
