import logging

from ConfigParser import SafeConfigParser
from copy import deepcopy

import ROOT

#############################################################
# General ROOT config settings
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.LoadMacro("modules/functions.h+") 
#############################################################

myrnd = ROOT.TRandom3()

def getCanvas(name = "c1", ratio = False, colz = False):
    """
    Function for generation a TCanvas object.

    Parameters:
    -----------
    name : string
        Name of the canvas
    ratio : bool
        If True, the functions returns TCanvas with to pads. Pad 1 for 
        the plot and Pad 2 for the ratio
    """
    logging.debug("Creating canvas with name {0}".format(name))
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    cwidth = styleconfig.getint("Canvas","width")
    cheight = styleconfig.getint("Canvas","height")

    canvas = ROOT.TCanvas(name, name, cwidth, cheight)

    margins = [ styleconfig.getfloat("Canvas","topmargin"),
                styleconfig.getfloat("Canvas","rightmargin"),
                styleconfig.getfloat("Canvas","leftmargin"),
                styleconfig.getfloat("Canvas","bottommargin") ]
    
    
    if not ratio:
        logging.debug("Setting up single canvas")    
        canvas.SetTopMargin(margins[0])
        if colz:
            logging.debug("setting right border for 2D plot")
            canvas.SetRightMargin(margins[1]+0.075)
        else:
            canvas.SetRightMargin(margins[1])
        canvas.SetLeftMargin(margins[2])
        canvas.SetBottomMargin(margins[3])
        
    else:
        logging.debug("Setting up canvas with ratioplots")
        canvas.Divide(1,2)
        canvas.cd(1).SetPad(0.,0.3-0.02,1.0,0.983)
        canvas.cd(2).SetPad(0.,0.0,1.0,0.3*(1-0.02))
        canvas.cd(1).SetBottomMargin(0.02)
        canvas.cd(2).SetTopMargin(0.00)
        canvas.cd(1).SetTopMargin(margins[0])
        canvas.cd(2).SetBottomMargin(margins[3]*(1/0.3))
        canvas.cd(1).SetRightMargin(margins[1])
        canvas.cd(1).SetLeftMargin(margins[2])
        canvas.cd(2).SetRightMargin(margins[1])
        canvas.cd(2).SetLeftMargin(margins[2])
        canvas.cd(2).SetTicks(1,1)
        canvas.cd(1).SetTicks(1,1)
        canvas.cd(2).SetFillStyle(0)
        canvas.cd(1).SetFillStyle(0)
        canvas.cd(2).SetFillColor(0)
        canvas.cd(2).SetFrameFillStyle(4000)

    return canvas

def setStyle(histo, histoType, color = 1, xAxisTitle = "", yAxisTitle = ""):
    ROOT.gStyle.SetErrorX(0)
    """
    Function for setting the style of Histogram.

    How to set the style is defined by the histoType parameter which can be "Points",
    "Line", "Siolid" and "Stack". The parameters are defined in the plotting.cfg in
    the config folder in the root directory.

    Parameters
    ----------
    histo : ROOT.TH1
    histoType : string
        Options: Points, Line, Solid, Stack, 2D
    color : int
        ROOT color as int
        Default: Black
    xAxisTitle : string
    yAxisTitle : string
    
    Returns
    -------
    bool
       sucess flag
    """
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    logging.debug("Setting style for histo w/ name {0}".format(histo.GetName()))
    
    if histoType not in ["Points", "Line", "Solid", "Stack", "2D"]:
        logging.warning("Unknown HistoStyle! Input: {0}".format(histoType))
        return False

    histo.ResetAttMarker()
    histo.ResetAttLine()
    
    if histoType in ["Points", "Line", "Solid"]:
        isPoints = styleconfig.getboolean("{0}Style".format(histoType), "Points")
        isFilled = styleconfig.getboolean("{0}Style".format(histoType), "Filled")
        
        if isPoints:
            logging.debug("Setting point style")
            histo.SetMarkerColor(color)
            histo.SetLineColor(ROOT.kBlack)
            histo.SetMarkerStyle(styleconfig.getint("{0}Style".format(histoType),"MarkerStyle"))
            histo.SetMarkerSize(styleconfig.getint("{0}Style".format(histoType),"MarkerSize"))    
        elif isFilled:
            logging.debug("Setting filled style")
            histo.SetLineColor(ROOT.kBlack)
            histo.SetFillColor(color)
            histo.SetFillStyle(styleconfig.getint("{0}Style".format(histoType),"FillStyle"))
        else:
            logging.debug("Setting line style")
            histo.SetLineColor(color)
            histo.SetFillStyle(styleconfig.getint("{0}Style".format(histoType),"FillStyle"))

    elif histoType == "2D":
        pass
    else:
        pass
            
    histo.SetTitle("")
    histo.GetXaxis().SetTitle(xAxisTitle)
    histo.GetYaxis().SetTitle(yAxisTitle)
    histo.GetYaxis().SetTitleOffset(histo.GetYaxis().GetTitleOffset()*styleconfig.getfloat("HistoStyle","yTitleOffsetscale"))
    histo.GetXaxis().SetTitleOffset(histo.GetXaxis().GetTitleOffset()*styleconfig.getfloat("HistoStyle","xTitleOffsetscale"))
    logging.debug("Setting x label to: "+xAxisTitle)
    logging.debug("Setting y label to: "+yAxisTitle)
    
    return True

def getHistoFromTree(tree, variable, binning, selection, weight = "1", hname = None, normalized = False, moveOverUnderFlowBin = True):
    """
    Function for TTree projection into a TH1 hisogram.

    
    Parameters
    ----------
    tree : ROOT.TTree
    variable : string
        Variable that is projected to the TH1
    selection : string
        Selection that is used for the projection
    weight : string
        Weight that is used for the projection
    binning : list, int, len(3)
        Binning for the histogram with nBins, first bins, last bin
    hname : string
        If not set, a name will be generated from the variable parameter
        and random number
    normalized : bool
        If True, histogram is scaled to unity
    moveOverUnderFlowBin : bool
        If True, Overflow and Underflow bins will be moved to the first/last bin

    Returns
    -------
    TH1F
    """
    if hname is None:
        hname = "{0}_{1}".format(variable, ROOT.gRandom.Integer(10000))

    histo = ROOT.TH1F(hname, hname, binning[0], binning[1], binning[2])
    histo.Sumw2()
    logging.subdebug("Sel:"+selection)
    logging.subdebug("Var:"+variable)
    logging.subdebug("Wei:"+weight)
    nPassing = tree.Project(hname, variable,"({0})*({1})".format(selection, weight))


    if moveOverUnderFlowBin:
        moveOverUnderFlow(histo)
    
    
    logging.debug("Number of events passing this selection: {0}".format(nPassing))

    if normalized:
        logging.info("Normalizing {0}".format(histo.GetName()))
        try:
            i = 1/float(histo.Integral())
        except ZeroDivisionError:
            logging.warning("ZeroDevision Error. Not scaling histo")
        else:
            histo.Scale(1/float(histo.Integral()))

    return histo


def get2DHistoFromTree(tree, xVariable, yVariable, xBinning, yBinning, selection, weight = "1", hname = None, moveOverUnderFlowBin = True):
    """
    Function for TTree projection into a TH2 hisogram.

    Parameters
    ----------
    tree : ROOT.TTree
    xVariable : string
        Variable that is projected to the to the x-axis on the TH2F
    yVariable : string
        Variable that is projected to the to the y-axis on the TH2F
    weight : string
        Weight that is used for the projection
    xBinning : list, int, len(3)
        Binning for the x-axis of the 2D histogram with nBins, first bins, last bin
    yBinning : list, int, len(3)
        Binning for the y-axis of the 2D histogram with nBins, first bins, last bin
    selection : string
        Selection that is used for the projection
    hname : string
        If not set, a name will be generated from the variable parameter
        and random number
    moveOverUnderFlowBin : bool
        If True, Overflow and Underflow bins will be moved to the first/last bin
        ---> This included the the bins where both values went in overflow/underflow 
             or one in underflow and the other in overflow
             -> If unclear try with a 2*2bin 2D plot (it has 16 bins)

    Returns
    -------
    TH2F
    """
    if hname is None:
        hname = "{0}_{1}_{2}".format(xVariable, yVariable, ROOT.gRandom.Integer(10000))

    histo = ROOT.TH2F(hname, hname, xBinning[0], xBinning[1], xBinning[2], yBinning[0], yBinning[1], yBinning[2])
    histo.Sumw2()
    
    logging.debug(selection)
    logging.debug("Drawing TH2 with: x: {0} and y: {1}".format(xVariable, yVariable))
    nPassing = tree.Project(hname, "{0}:{1}".format(yVariable, xVariable),"({0})*({1})".format(selection, weight))

    if moveOverUnderFlowBin:
        moveOverUnderFlow2D(histo)
    
    logging.debug("Number of events passing this selection: {0}".format(nPassing))

    return histo



def drawHistos(orderedHistoList, stackindex = None, canvas = None, orderedRatioList = None, yTitle = None):
    """
    Function that draws all histograms that are given to it.

    Parameters
    ----------
    orderedHistolist : list, elements: tuples
        list with all histograms in order they have to be drawn. Each element
        is expected to be a tuple of ROOT.TH1 and DrawString
    orderedRatioList : list, elements: tuples
        list with all ratio histos. Each element is expected to be a tuple of 
        ROOT.TH1 and DrawString.
    stackindex : int
        if int is given the histogram with the index is expected to be a THStack#
    yTitle : sring
        Only needed for stack plots.


    Returns:
    --------
    ROOT.TCanvas
    """
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    #Get global maximal bin height
    maxval = 0
    for histo, drawstring in orderedHistoList:
        if histo.GetMaximum() > maxval:
            maxval = histo.GetMaximum()
    
            
    if canvas is None:
        if orderedRatioList is None:
            logging.debug("Creaing new canvas")
            thiscanvas = getCanvas()
        else:
            logging.debug("Creaing new canvas with ratio")
            thiscanvas = getCanvas(ratio = True)
    else:
        logging.debug("Using canvas given as parameter")
        thiscanvas = canvas


    if orderedRatioList is not None:        
        thiscanvas.cd(2)
        idrawn = 0
        drawpostfix = ""
        for ratio, drawstring in orderedRatioList:
            logging.debug("Drawing {0} with option {1}{2}".format(ratio.GetName(),drawstring, drawpostfix)) 
            ratio.Draw("{0}{1}".format(drawstring, drawpostfix))
            #ratio.GetYaxis().SetLabelSize(0) #TODO change to Data / MC or something
            ratio.GetYaxis().SetTitleSize(0) #TODO change to Data / MC or something
            if idrawn == 0:
                #drawpostfix = " same"
                pass
            idrawn += 1
    thiscanvas.Update()
    #raw_input("keep drawing")
    
    thiscanvas.cd(1)
    idrawn = 0
    drawpostfix = ""

    if stackindex is None:
        for histo, drawstring in orderedHistoList:
            logging.debug("Drawing {0} with option {1}{2}".format(histo.GetName(),drawstring, drawpostfix))
            if idrawn == 0:
                histo.GetYaxis().SetRangeUser(0, maxval *  styleconfig.getfloat("HistoStyle","maxValScale"))
            if idrawn == 0 and orderedRatioList is not None:
                histo.GetXaxis().SetLabelSize(0)
                histo.GetYaxis().SetTitleSize(histo.GetYaxis().GetTitleSize() * 1.4)
                histo.GetYaxis().SetTitleOffset(histo.GetYaxis().GetTitleOffset() * (1/styleconfig.getfloat("HistoStyle","yTitleOffsetscale")))
                histo.GetYaxis().SetLabelSize(histo.GetYaxis().GetLabelSize() * 1.4)
            histo.Draw("{0}{1}".format(drawstring, drawpostfix))
            if idrawn == 0:
                drawpostfix = " same"
            idrawn += 1
    else:
        if stackindex >= len(orderedHistoList):
            logging.error("Stackindex out of range")
        else:
            stack, drawstring = orderedHistoList[stackindex]
            stack.Draw(drawstring)
            stack.GetXaxis().SetLabelSize(0)
            stack.GetYaxis().SetTitleSize(histo.GetYaxis().GetTitleSize() * 1.4)
            stack.GetYaxis().SetTitleOffset(histo.GetYaxis().GetTitleOffset() * (1/styleconfig.getfloat("HistoStyle","yTitleOffsetscale")))
            stack.GetYaxis().SetLabelSize(histo.GetYaxis().GetLabelSize() * 1.4)
            stack.Draw(drawstring)
            drawpostfix = " same"
            for ihisto, hplusOptions in enumerate(orderedHistoList):
                histo, drawstring = hplusOptions
                if ihisto != stackindex:
                    histo.Draw("{0}{1}".format(drawstring, drawpostfix))
    thiscanvas.Update()
    return thiscanvas


def getRatioPlot(hRef, hList, invert = False):
    """
    Function for generating the histograms used in a ratioplot.

    Parameters
    ----------
    hRef : ROOT.TH1
        This histogram will be used as reference histo (unity line in the plot)
    hList : list, elements: ROOT.TH1
        This list contains all further histograms for the ratio plot
    invert : bool
        With this flag the ratio value will be inverted t 1/ratiovalue
    Returns:
    --------
    hRatioRef : ROOT.TH1F
        Reference line
    hRatioList : list, elements: ROOT.TH1
        List with all further histograms in the ratio plot
    div : tuple (maxdiv, mindiv)
        Tuple containing global maximum and minimum of all
        histos considered for the ratio
    """

    gRef = ROOT.TGraphErrors(hRef)
    
    line = hRef.Clone()
    line.SetName("ratioline_"+line.GetName())
    line.SetTitle("")
    line.Divide(hRef)
    line.SetLineColor(1)
    line.SetLineStyle(2)
    line.SetLineWidth(1)
    line.SetFillStyle(0)

    line.GetXaxis().SetLabelSize(line.GetXaxis().GetLabelSize()*(1/0.3))
    line.GetYaxis().SetLabelSize(line.GetYaxis().GetLabelSize()*(1/0.3))
    line.GetXaxis().SetTitleSize(line.GetXaxis().GetTitleSize()*(1/0.3))
    line.GetYaxis().SetTitleSize(line.GetYaxis().GetTitleSize()*(1/0.3))
    line.GetYaxis().SetNdivisions(505)
    #line.GetXaxis().SetNdivisions(config.getint("General","xNdiv"))


    
    
    for i in range(line.GetNbinsX()+1):
            line.SetBinContent(i,1)
            line.SetBinError(i,0)
    logging.debug("Ratio line generated: "+str(line))

    
    
    mindiv = 9999.
    maxdiv = -9999.

    hRatioList = []
    
    for h in hList:
        ref = ROOT.TGraphAsymmErrors(hRef)
        logging.debug("Making ratio for ratio plot from "+str(h))
        ratio = ref.Clone()
        ratio.SetName("ratio_"+h.GetName())
        ratio.SetMarkerStyle(21)
        ratio.SetMarkerColor(h.GetLineColor())
        ratio.SetLineColor(h.GetLineColor())
        x, y = ROOT.Double(0), ROOT.Double(0)
        for i in range(0,ref.GetN()):
            ref.GetPoint(i, x, y)
            currentBin = h.FindBin(x)
            currentBinContent = h.GetBinContent(currentBin)
            if currentBinContent > 0:
                ratioval = (y/currentBinContent)
                if invert:
                    ratioval = 1/ratioval
                ratio.SetPoint(i, x, ratioval)
                if ratioval > maxdiv and ratioval > 0:
                    maxdiv = round(ratioval, 1)
                if ratioval < mindiv and ratioval > 0:
                    mindiv = round(ratioval, 1)
                logging.debug("Ratio: i {0}, Bin {1}, bin value: {2}, y: {3}, ratioval: {4}".format(i, currentBin, currentBinContent, y, ratioval))
            else:
                ratio.SetPoint(i, x, -999)
                logging.debug("Ratio: i {0}, Bin {1}, bin value: {2}, y: {3}, ratioval: {4}".format(i, currentBin, currentBinContent, y, -999))
                
            if y > 0:
                if currentBinContent > 0:
                    ratio.SetPointEYlow(i, ref.GetErrorYlow(i)/currentBinContent)
                    ratio.SetPointEYhigh(i, ref.GetErrorYhigh(i)/currentBinContent)
                else:
                    ratio.SetPointEYlow(i, 1-(y-ref.GetErrorYlow(i))/y)
                    ratio.SetPointEYhigh(i, (y+ref.GetErrorYhigh(i))/y-1)
            else:
                ratio.SetPointEYlow(i, 0)
                ratio.SetPointEYhigh(i, 0)
        hRatioList.append(deepcopy(ratio))
        del ratio

    logging.debug("Maximum deviation is: +{0} -{1}".format(maxdiv, mindiv))
    #line.GetYaxis().SetRangeUser(mindiv, maxdiv)
    if maxdiv < 1.1 and mindiv > 0.9:
        line.GetYaxis().SetRangeUser(0.85,1.15)
    elif maxdiv < 1.25 and mindiv > 0.75:
        line.GetYaxis().SetRangeUser(0.7,1.3)
    elif maxdiv < 1.75 and mindiv > 0.25:
        line.GetYaxis().SetRangeUser(0.2,1.8)
    else:
        line.GetYaxis().SetNdivisions(503)
        line.GetYaxis().SetRangeUser(0,2.65)
    hRatioRef = line
        
    return hRatioRef, hRatioList, (mindiv, maxdiv)

def makeEffGraph(hpass, htot, yAxis):
    xTitle = hpass.GetXaxis().GetTitle()
    color = hpass.GetLineColor()
    
    
    graph = ROOT.TGraphAsymmErrors(hpass,htot)
    graph.SetName(str(ROOT.gRandom.Integer(10000)))
    graph.SetMarkerColor(color);
    graph.SetLineColor(color);
    graph.SetMarkerSize(2)
    graph.GetXaxis().SetTitle(xTitle)
    graph.GetYaxis().SetTitle(yAxis)
    graph.SetMarkerStyle(20);

    return graph


def moveOverUnderFlow(histo, moveOverFlow=True, moveUnderFlow=True):
    """
    Function for moving the overflow and (or) underflow bin to the first/last bin
    """
    nBins = histo.GetNbinsX()
    if moveUnderFlow:
        underflow = histo.GetBinContent(0)
        fistBinContent = histo.GetBinContent(1)
        histo.SetBinContent(1, fistBinContent+underflow)
        histo.SetBinContent(0, 0)
    if moveOverFlow:
        overflow = histo.GetBinContent(nBins+1)
        lastBinContent = histo.GetBinContent(nBins)
        histo.SetBinContent(nBins, lastBinContent+overflow)
        histo.SetBinContent(nBins+1, 0)


def moveOverUnderFlow2D(histo, moveOverFlow=True, moveUnderFlow=True):
    nBinsX = histo.GetNbinsX()
    nBinsY = histo.GetNbinsY()


    if moveUnderFlow:
        #Fist move overflow from the bins where one values was inside the histogram
        for iY in range(1,nBinsY+1):
            newBinContent = histo.GetBinContent(0,iY) + histo.GetBinContent(1,iY)
            histo.SetBinContent(1,iY, newBinContent)
            histo.SetBinContent(0,iY, 0)

        for iX in range(1,nBinsX+1):
            newBinContent = histo.GetBinContent(iX,0) + histo.GetBinContent(iX,1)
            histo.SetBinContent(iX,1, newBinContent)
            histo.SetBinContent(iX,0, 0)

        #Move the "corner" bins <-> where both values where outside the histgram
        newBinContent = histo.GetBinContent(0,0) + histo.GetBinContent(1,1)
        histo.SetBinContent(1,1, newBinContent)
        histo.SetBinContent(0, 0, 0)
        newBinContent = histo.GetBinContent(0,nBinsY+1) + histo.GetBinContent(1,nBinsY)
        histo.SetBinContent(1,nBinsY, newBinContent)
        histo.SetBinContent(0,nBinsY+1, 0)

    if moveOverFlow:
        #Fist move overflow from the bins where one values was inside the histogram
        for iY in range(1,nBinsY+1):
            newBinContent = histo.GetBinContent(nBinsX+1,iY) + histo.GetBinContent(nBinsX,iY)
            histo.SetBinContent(nBinsX,iY, newBinContent)
            histo.SetBinContent(nBinsX+1,iY, 0)

        for iX in range(1,nBinsX+1):
            newBinContent = histo.GetBinContent(iX,nBinsY+1) + histo.GetBinContent(iX,nBinsY)
            histo.SetBinContent(iX,nBinsY, newBinContent)
            histo.SetBinContent(iX,nBinsY+1, 0)

        #Move the "corner" bins <-> where both values where outside the histgram
        newBinContent = histo.GetBinContent(nBinsX+1,nBinsY+1) + histo.GetBinContent(nBinsX,nBinsY)
        histo.SetBinContent(nBinsX,nBinsY, newBinContent)
        histo.SetBinContent(nBinsX+1,nBinsY+1, 0)
        newBinContent = histo.GetBinContent(nBinsX+1,0) + histo.GetBinContent(nBinsX,1)
        histo.SetBinContent(nBinsX,1,newBinContent)
        histo.SetBinContent(nBinsX+1,0, 0)
    
