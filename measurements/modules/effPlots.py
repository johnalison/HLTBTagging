import logging
from ConfigParser import SafeConfigParser

import ROOT

import modules.plotting
import modules.classes
import modules.utils



def makeEffPlot(PlotBaseObj, Sample, numSelection, outname = None, outputformat = "pdf", label = None, drawEff = True, forceColor = None, drawHistos = False, addSel = "1"):
    styleconfig = SafeConfigParser()
    styleconfig.read("config/plotting.cfg")


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
    
        
    yTitle = "Effciency"
    
    #In principle both PlotBaseObjs shoud have the same binning
    binning = PlotBaseObj.binning

    
    
    hdenominator = modules.plotting.getHistoFromTree(Sample.tree, PlotBaseObj.variable, binning, "({0} && {1} && {2})".format(PlotBaseObj.selection, Sample.selection, addSel))
    hnumerator = modules.plotting.getHistoFromTree(Sample.tree, PlotBaseObj.variable, binning, "(({0}) && ({1}) && ({2}) && {3})".format(PlotBaseObj.selection, Sample.selection, numSelection, addSel))

        
    if forceColor is not None:
        logging.debug("Forcing color: {0}".format(forceColor))
        color = forceColor
    else:
        color = PlotBaseObj.color

    
    
    modules.plotting.setStyle(hdenominator, "Line", color, PlotBaseObj.xTitle, yTitle)
    modules.plotting.setStyle(hnumerator, "Line", color, PlotBaseObj.xTitle, yTitle)
    
    if drawHistos:
        CMSL1, CMSL2 = modules.utils.getCMStext()
        canvas = modules.plotting.drawHistos([(hdenominator,"histoe")])
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")

        
        if outname is not None:
            modules.utils.savePlot(canvas, outname+"_hdenom", outputformat)
        del canvas
        canvas = modules.plotting.drawHistos([(hnumerator,"histoe")])
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")
                
        if outname is not None:
            modules.utils.savePlot(canvas, outname+"_hnum", outputformat)
        del canvas
    
    grEff = modules.plotting.makeEffGraph(hnumerator, hdenominator, yTitle)

    if drawEff:
        canvas = modules.plotting.getCanvas()
        canvas.cd()
        
        grEff.Draw("AP")
        grEff.GetHistogram().SetMaximum(styleconfig.getfloat("Efficiency", "yMax"))
        grEff.GetHistogram().SetMinimum(0.0)
        grEff.GetXaxis().SetRangeUser(binning[1], binning[2])
        grEff.Draw("AP")
        
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")

        if outname is not None:
            modules.utils.savePlot(canvas, outname, outputformat)

    return grEff


def makeEffSumPlot(PlotBaseObj, Sample, numSelection, nIter, outname = None, outputformat = "pdf", label = None, drawEff = True, forceColor = None, drawHistos = False, addSel = "1"):
    styleconfig = SafeConfigParser()
    styleconfig.read("config/plotting.cfg")


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
    
        
    yTitle = "Effciency"
    
    #In principle both PlotBaseObjs shoud have the same binning
    binning = PlotBaseObj.binning

    hdenominator = None
    hnumerator = None
    hset = False
    
    for i in range(nIter):
        logging.subdebug("Itervar from PlotBase: "+PlotBaseObj.variable)
        iterVar = str(PlotBaseObj.variable).replace("?",str(i))
        iterSel = str("({0} && {1} && ({2}))".format(PlotBaseObj.selection, Sample.selection, addSel)).replace("?",str(i))
        iterSelnum = str("(({0}) && ({1}) && ({2}) && ({3}))".format(PlotBaseObj.selection, Sample.selection, numSelection, addSel)).replace("?",str(i))
        if not hset:
            hdenominator = modules.plotting.getHistoFromTree(Sample.tree, iterVar, binning, iterSel)
            hnumerator = modules.plotting.getHistoFromTree(Sample.tree, iterVar, binning, iterSelnum)
            hset = True
        else:
            hdenominator.Add(modules.plotting.getHistoFromTree(Sample.tree, iterVar, binning, iterSel))
            hnumerator.Add(modules.plotting.getHistoFromTree(Sample.tree, iterVar, binning, iterSelnum))


        
    if forceColor is not None:
        logging.debug("Forcing color: {0}".format(forceColor))
        color = forceColor
    else:
        color = PlotBaseObj.color
            
    modules.plotting.setStyle(hdenominator, "Line", color, PlotBaseObj.xTitle, yTitle)
    modules.plotting.setStyle(hnumerator, "Line", color, PlotBaseObj.xTitle, yTitle)

    if drawHistos:
        CMSL1, CMSL2 = modules.utils.getCMStext()
        canvas = modules.plotting.drawHistos([(hdenominator,"histoe")])
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")

        
        if outname is not None:
            modules.utils.savePlot(canvas, outname+"_hdenom", outputformat)
        del canvas
        canvas = modules.plotting.drawHistos([(hnumerator,"histoe")])
        CMSL1.Draw("same")
        CMSL2.Draw("same")
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")
                
        if outname is not None:
            modules.utils.savePlot(canvas, outname+"_hnum", outputformat)
        del canvas
    
    grEff = modules.plotting.makeEffGraph(hnumerator, hdenominator, yTitle)

    if drawEff:
        canvas = modules.plotting.getCanvas()
        canvas.cd()
        
        grEff.Draw("AP")
        grEff.GetHistogram().SetMaximum(styleconfig.getfloat("Efficiency", "yMax"))
        grEff.GetHistogram().SetMinimum(0.0)
        grEff.GetXaxis().SetRangeUser(binning[1], binning[2])
        grEff.Draw("AP")
        
        if label is not None:
            if isinstance(label, list):
                for l in label:
                    l.Draw("same")
            else:
                label.Draw("same")
        CMSL1, CMSL2 = modules.utils.getCMStext()
        CMSL1.Draw("same")
        CMSL2.Draw("same")

        if outname is not None:
            modules.utils.savePlot(canvas, outname, outputformat)

    return grEff


    
def makeEffSCompPlot(PlotBaseObj, Samples, numSelection, outname = None, outputformat = "pdf", label = None, drawHistos = False, addSel = "1"):
    styleconfig = SafeConfigParser()
    styleconfig.read("config/plotting.cfg")

    binning = PlotBaseObj.binning
    
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

    graphs = []
    forlegend = []
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen-2]
    #TODO Make something to check num of samples against colors
    for isample, sample in enumerate(Samples):
        SampleLabel = modules.utils.getLabel(sample.legend[0], 0.7)
        graphs.append(makeEffPlot(PlotBaseObj, sample, numSelection, drawEff = False, forceColor = colors[isample], drawHistos = drawHistos, outname = outname+"_"+sample.name, label = [label, SampleLabel], addSel = addSel))
        forlegend.append((graphs[isample], sample.legend[0], "p"))
    
    canvas = modules.plotting.getCanvas()
    canvas.cd()

    logging.debug("Drawing graph 0")
    graphs[0].Draw("AP")
    graphs[0].GetHistogram().SetMaximum(styleconfig.getfloat("Efficiency", "yMax"))
    graphs[0].GetHistogram().SetMinimum(0.0)
    graphs[0].GetXaxis().SetRangeUser(binning[1], binning[2])
    graphs[0].Draw("AP")

    for i in range(1, len(graphs)):
        logging.debug("Drawing graph {0}".format(i))
        graphs[i].Draw("PSame")
     
    if label is not None:
        if isinstance(label, list):
            for l in label:
                l.Draw("same")
        else:
            label.Draw("same")
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")

    logging.debug("Making Legend")
    xstart = PlotBaseObj.LegendPosition[0]
    ystart = PlotBaseObj.LegendPosition[1]
    xend = PlotBaseObj.LegendPosition[2]
    yend = PlotBaseObj.LegendPosition[3]
    
    leg = modules.utils.getLegend(forlegend, xstart, ystart, xend, yend, usingPlotBase = False)
    leg.Draw("")
    
    
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)

def makeEffSummSCompPlot(PlotBaseObj, Samples, numSelection, nIter, outname = None, outputformat = "pdf", label = None, drawHistos = False, addSel = "1"):
    styleconfig = SafeConfigParser()
    styleconfig.read("config/plotting.cfg")

    binning = PlotBaseObj.binning
    
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

    graphs = []
    forlegend = []
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen-2]
    #TODO Make something to check num of samples against colors
    for isample, sample in enumerate(Samples):
        SampleLabel = modules.utils.getLabel(sample.legend[0], 0.7)
        graphs.append(makeEffSumPlot(PlotBaseObj, sample, numSelection, nIter, drawEff = False, forceColor = colors[isample], drawHistos = drawHistos, outname = outname+"_"+sample.name, label = [label, SampleLabel], addSel = addSel))
        forlegend.append((graphs[isample], sample.legend[0], "p"))

    canvas = modules.plotting.getCanvas()
    canvas.cd()

    logging.debug("Drawing graph 0")
    graphs[0].Draw("AP")
    graphs[0].GetHistogram().SetMaximum(styleconfig.getfloat("Efficiency", "yMax"))
    graphs[0].GetHistogram().SetMinimum(0.0)
    graphs[0].GetXaxis().SetRangeUser(binning[1], binning[2])
    graphs[0].Draw("AP")

    for i in range(1, len(graphs)):
        logging.debug("Drawing graph {0}".format(i))
        graphs[i].Draw("PSame")
     
    if label is not None:
        if isinstance(label, list):
            for l in label:
                l.Draw("same")
        else:
            label.Draw("same")
    CMSL1, CMSL2 = modules.utils.getCMStext()
    CMSL1.Draw("same")
    CMSL2.Draw("same")

    logging.debug("Making Legend")
    xstart = PlotBaseObj.LegendPosition[0]
    ystart = PlotBaseObj.LegendPosition[1]
    xend = PlotBaseObj.LegendPosition[2]
    yend = PlotBaseObj.LegendPosition[3]
    
    leg = modules.utils.getLegend(forlegend, xstart, ystart, xend, yend, usingPlotBase = False)
    leg.Draw("")
    
    
    if outname is not None:
        modules.utils.savePlot(canvas, outname, outputformat)
