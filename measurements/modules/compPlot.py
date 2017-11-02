import logging

import modules.plotting
import modules.classes

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
    


def compareJetTypes(PlotBaseObjs, Sample, normalized = False, outname = None, outputformat = "pdf", label = None):
    hObjs = []

    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None
    
    yTitle = "Events"
    if normalized:
        yTitle = "normalized Units"

    
    logging.debug("Making hisograms from tree")
    for PlotBaseObj in PlotBaseObjs:
        hObjs.append(
            modules.plotting.getHistoFromTree(Sample.tree, PlotBaseObj.variable, PlotBaseObj.binning,
                                              "({0} && {1})".format(PlotBaseObj.selection, Sample.selection),
                                              normalized = normalized)
        )
    
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
                                                  normalized = normalized)
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

    hRet = modules.plotting.get2DHistoFromTree(Sample.tree, xVar, yVar, PlotBase2DObj.xBinning, PlotBase2DObj.yBinning, Selection, Weight)

    modules.plotting.setStyle(hRet, "2D", xAxisTitle = PlotBase2DObj.xTitle, yAxisTitle = PlotBase2DObj.yTitle)

    return hRet
     
def fillandSum2D(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection):    

    hRet = None

    
    Selection = "({0}) && ({1})".format(PlotBase2DObj.selection, Sample.selection)
    
    for i in range(nIter):
        if i == 0:
            hRet = fill2DPlot( PlotBase2DObj, Sample, xVarBase.replace("?",str(i)), yVarBase.replace("?",str(i)), "({0}) && ({1})".format(Selection, iterSelection.replace("?",str(i))), "1")
            logging.debug("--->"+xVarBase.replace("?",str(i)))
            logging.debug("--->"+yVarBase.replace("?",str(i)))
        else:
            hRet.Add(fill2DPlot( PlotBase2DObj, Sample, xVarBase.replace("?",str(i)), yVarBase.replace("?",str(i)), "({0}) && ({1})".format(Selection, iterSelection.replace("?",str(i))), "1" ))

    return hRet

def make2DSummedPlot(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection = "1", outname = None, outputformat = "pdf", label = None):
    if label is not None and not isinstance(label,ROOT.TLatex):
        logging.warning("The label param should be of type ROOT.TLatex")
        logging.warning("Ignoring additional label")
        label = None

    histo = fillandSum2D(PlotBase2DObj, Sample, xVarBase, yVarBase, nIter, iterSelection)

    
    canvas = modules.plotting.getCanvas(colz = True)
    canvas.cd()
    histo.Draw("colz")
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")
    if label is not None:
        label.Draw("same")
        
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
