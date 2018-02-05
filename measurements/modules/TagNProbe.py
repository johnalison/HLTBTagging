import logging
from copy import deepcopy
import math
import ROOT

import modules.DataMC
import modules.plotting
from modules.utils import setup_logging, getLabel, addHistoList



def LeadingProbe(PlotBaseObj, Samples2Stack, probeSelection, tagSelection, plottag = False, convertIterSelection = True, probeIndex = 0, tagIndex = 1, data = None , normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, skipPlots = False):
    """
    Function for plotting a distribution of a porbe jet depending on a probe jet selection. Calls
    modules.DataMC.StackDMCPlotBase for plotting. 

    Parameters
    ----------
    PlotBaseObj : 
    Samples2Stack : list modules.classes.sample objects
    probeSelection : string
        Selection of the probe jets. I index of jet not fixed, use 
        convertIterSelection = True and the probeIndex to replace ?
        with the index
    tagSelection : string
        Selection of the tag jets. I index of jet not fixed, use 
        convertIterSelection = True and the tagIndex to replace ?
        with the index
    convertIterSelection : bool
        If true, selections are expected to have [?] instead of [index]
        which will be replaced with probeIndex or tagIndex.
    probeIndex : int
        Index of the probe Jet in the jet array
    tagIndex
        Index of the tag Jet in the jet array
    data : modules.classes.sample object
        If None is provide the sum of all stacked histograms (passed in
        Samples2Stack will be used as "data"
    """
    StackHistos = []
    StackSum = None
    
    if convertIterSelection:
        probeSelection = probeSelection.replace("?", str(probeIndex))
        tagSelection = tagSelection.replace("?", str(tagIndex))
        if plottag:
            xVarBase = PlotBaseObj.variable.replace("?", str(tagIndex))
            
        else:
            xVarBase = PlotBaseObj.variable.replace("?", str(probeIndex))
    else:
        xVarBase = PlotBaseObj.variable
    for isample, sample in enumerate(Samples2Stack):

        selection = "{0} && {1}".format(PlotBaseObj.selection, sample.selection).replace("?", str(probeIndex))
        
        StackHistos.append(getPorbeHisto( PlotBaseObj, sample, xVarBase, selection, probeSelection, tagSelection, isMC = True) )
        if isample == 0:
            logging.debug("Creating stacksum"+" with name "+str(sample.name))
            StackSum = StackHistos[0].Clone()
            StackSum.SetName("Stacksum_"+StackSum.GetName())
            StackSum.SetTitle("Stacksum_"+StackSum.GetTitle())
        else:
            logging.debug("Adding histo to stacksum "+str(isample)+" with name "+str(sample.name))
            StackSum.Add(StackHistos[isample])

    logging.subinfo("Stack histos finished")
    if data is None:
        logging.warning("No data set -> Setting data to Stacksum")
        hData = StackSum.Clone()
        hData.SetName("Data_"+StackSum.GetName())
    else:
        selection = "{0} && {1}".format(PlotBaseObj.selection, data.selection).replace("?", str(probeIndex))
        hData = getPorbeHisto( PlotBaseObj, data, xVarBase, selection, probeSelection, tagSelection, isMC = False)

    if not skipPlots:
        modules.DataMC.StackDMCPlotBase(StackSum, StackHistos, hData, PlotBaseObj, Samples2Stack, data, normalized, drawRatio, outname, outputformat, label)

    return StackSum, StackHistos, hData

def getPorbeHisto(PlotBaseObj, sample, xVarBase, selection, probeselection, tagselection, isMC):
    logging.subinfo("Making tag histo for sample: {0}".format(sample.name))
    if isMC:
        weight = "{0} * {1}".format(sample.getSampleWeight(), sample.weight)
    else:
        weight = "1"
    logging.subdebug("Probe Selection: {0}".format(tagselection))
    sel = "{0} && {1} && {2}".format(selection, probeselection, tagselection)
    return modules.plotting.getHistoFromTree(sample.tree, xVarBase, PlotBaseObj.binning, sel, weight = weight)




def getBEfficiencyHack(PlotBaseObj, Samples2Stack, probeSelection, tagSelection, addNumeratorSel, numWPs, bindex, probeSelVetoIter, convertIterSelection = True, probeIndices = [0], tagIndices = [[1]], data = None , normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, savetable = True):
    import itertools
    
    results = {}
    
    outfile = ROOT.TFile(outname+"_histos.root","RECREATE")
    initTagSelection = tagSelection
    initProbeSelection = probeSelection
    for WP in numWPs:
        results[WP] = {}
        logging.info("Processing WP: {0}".format(WP))
        #Getting denominator
        numWP = "{0} > {1}".format(addNumeratorSel, WP)

        StackSum_denom, StackHistos_denom, hData_denom = None, None, None
        StackSum_num, StackHistos_num, hData_num = None, None, None
        histosSet = False
        
        probeSelection = initProbeSelection

        prevProbes = []
        for iprobeIndex, probIndexElem in enumerate(probeIndices):
            logging.info("Making combinations for Tag/Probe selection w/ ProbeIndex {0} and TagIndex {1}".format(probIndexElem, tagIndices[iprobeIndex]))
            tagSelection = initTagSelection
            if len(prevProbes) > 0:
                probeSelection = probeSelection + " && (" + probeSelVetoIter.replace("?", str(prevProbes[-1])) + " != 0)"
                print "---------",probeSelVetoIter, prevProbes[-1]
            prevProbes.append(probIndexElem)
            for probeIndex, tagIndex in list(itertools.product([probIndexElem], tagIndices[iprobeIndex])):
                logging.info("Making histos w/ ProbeIndex {0} & TagIndex {1}".format(probeIndex, tagIndex))
                if not histosSet:
                    logging.debug("Setting histograms")
                    histosSet = True
                    
                    StackSum_denom, StackHistos_denom, hData_denom = LeadingProbe(PlotBaseObj, Samples2Stack, probeSelection, tagSelection,
                                                                                  False, convertIterSelection, probeIndex, tagIndex, data,
                                                                                  skipPlots = True)
                    StackSum_num, StackHistos_num, hData_num = LeadingProbe(PlotBaseObj, Samples2Stack, "{0} && {1}".format(probeSelection, numWP), tagSelection,
                                                                            False, convertIterSelection, probeIndex, tagIndex, data,
                                                                            skipPlots = True)
                else:
                    logging.debug("Adding histograms")
                    StackSum_denom_temp, StackHistos_denom_temp, hData_denom_temp = LeadingProbe(PlotBaseObj, Samples2Stack, probeSelection, tagSelection,
                                                                                                 False, convertIterSelection, probeIndex, tagIndex, data,
                                                                                                 skipPlots = True)
                    StackSum_num_temp, StackHistos_num_temp, hData_num_temp = LeadingProbe(PlotBaseObj, Samples2Stack, "{0} && {1}".format(probeSelection, numWP),
                                                                                           tagSelection, False, convertIterSelection, probeIndex, tagIndex, data,
                                                                                           skipPlots = True)


                    
                    
                    StackSum_denom.Add(StackSum_denom_temp)
                    addHistoList(StackHistos_denom ,StackHistos_denom_temp)
                    hData_denom.Add(hData_denom_temp)
                    StackSum_num.Add(StackSum_num_temp)
                    addHistoList(StackHistos_num ,StackHistos_num_temp)
                    hData_num.Add(hData_num_temp)

                    del StackSum_denom_temp, StackHistos_denom_temp, hData_denom_temp, StackSum_num_temp, StackHistos_num_temp, hData_num_temp
                tagSelection = tagSelection + " && (" + tagSelection.replace("?", str(tagIndex)) + " != 0)"
                logging.debug("Adding:  && (" + tagSelection.replace("?", str(tagIndex)) + " != 0)")
        outfile.cd()
        ##Normalization to data
        MCscale_denom = hData_denom.Integral()/StackSum_denom.Integral()

        NormLabel = getLabel("MC normalized to Data", 0.6, scale = 0.8)
        if label is None:
            label = [NormLabel]
        if label is isinstance(label,ROOT.TLatex):
            label = [label + NormLabel]
        else:
            label.append(NormLabel)

        logging.info("Scaling denom by {0}".format(MCscale_denom))
        StackSum_denom.Scale(MCscale_denom)
        for ihisto, histo in enumerate(StackHistos_denom):
            histo.Scale(MCscale_denom)
            
        #MCscale_num = hData_num.Integral()/StackSum_num.Integral()
        #logging.info("Scaling num by {0}".format(MCscale_num))
        StackSum_num.Scale(MCscale_denom)
        for ihisto, histo in enumerate(StackHistos_num):
            histo.Scale(MCscale_denom)


        calcEfficiencies(results, StackSum_denom, StackHistos_denom, hData_denom, StackSum_num, StackHistos_num, hData_num, PlotBaseObj, Samples2Stack, WP, bindex, data, normalized, drawRatio, outname, outputformat, label, savetable)


    if savetable:
        saveEffTable(numWPs, results, outname)
    outfile.Close()
        
            
     

def getBEfficiency(PlotBaseObj, Samples2Stack, probeSelection, tagSelection, addNumeratorSel, numWPs, bindex, convertIterSelection = True, probeIndex = 0, tagIndex = 1, data = None , normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, savetable = True):

    results = {}
    
    outfile = ROOT.TFile(outname+"_histos.root","RECREATE")
    for WP in numWPs:
        results[WP] = {}
        logging.info("Processing WP: {0}".format(WP))
        #Getting denominator
        numWP = "{0} > {1}".format(addNumeratorSel, WP)
        StackSum_denom, StackHistos_denom, hData_denom = LeadingProbe(PlotBaseObj, Samples2Stack, probeSelection, tagSelection, False, convertIterSelection, probeIndex, tagIndex, data, skipPlots = True)
        StackSum_num, StackHistos_num, hData_num = LeadingProbe(PlotBaseObj, Samples2Stack, "{0} && {1}".format(probeSelection, numWP), tagSelection, False, convertIterSelection, probeIndex, tagIndex, data, skipPlots = True)
        outfile.cd()
        ##Normalization to data
        MCscale_denom = hData_denom.Integral()/StackSum_denom.Integral()

        NormLabel = getLabel("MC normalized to Data", 0.6, scale = 0.8)
        if label is None:
            label = [NormLabel]
        if label is isinstance(label,ROOT.TLatex):
            label = [label + NormLabel]
        else:
            label.append(NormLabel)

        logging.info("Scaling denom by {0}".format(MCscale_denom))
        StackSum_denom.Scale(MCscale_denom)
        for ihisto, histo in enumerate(StackHistos_denom):
            histo.Scale(MCscale_denom)
            
        #MCscale_num = hData_num.Integral()/StackSum_num.Integral()
        #logging.info("Scaling num by {0}".format(MCscale_num))
        StackSum_num.Scale(MCscale_denom)
        for ihisto, histo in enumerate(StackHistos_num):
            histo.Scale(MCscale_denom)


        calcEfficiencies(results, StackSum_denom, StackHistos_denom, hData_denom, StackSum_num, StackHistos_num, hData_num, PlotBaseObj, Samples2Stack, WP,
                         bindex, data, normalized, drawRatio, outname, outputformat, label, savetable)


    if savetable:
        saveEffTable(numWPs, results, outname)
    outfile.Close()


def calcEfficiencies(results, StackSum_denom, StackHistos_denom, hData_denom, StackSum_num, StackHistos_num, hData_num, PlotBaseObj, Samples2Stack, WP,
                     bindex, data = None , normalized = False, drawRatio = True, outname = None, outputformat = "pdf", label = None, savetable = True):

    modules.DataMC.StackDMCPlotBase(StackSum_num, StackHistos_num, hData_num, PlotBaseObj, Samples2Stack, data,
                                    normalized = False, outname = outname+"_{0}_num".format(WP),  label = label)
    modules.DataMC.StackDMCPlotBase(StackSum_denom, StackHistos_denom, hData_denom, PlotBaseObj, Samples2Stack, data,
                                    normalized = False, outname = outname+"_{0}_denom".format(WP), label = label)


    logging.info("Calculating MC efficiency")
    logging.info("Using Sample: {0}".format(Samples2Stack[bindex].name))
    hBjets_denom = deepcopy(StackHistos_denom[bindex])
    hBjets_num = deepcopy(StackHistos_num[bindex])

    MCeff =  hBjets_num.Integral()/hBjets_denom.Integral()
    MCError = math.sqrt(MCeff*(1-MCeff)/hBjets_denom.GetEntries())
    results[WP]["MC"] = MCeff
    results[WP]["MCErr"] = MCError
    logging.info("btagging Effciency in MC = {0} +- {2} [{1}]".format(MCeff, WP, MCError))

    hBjets_denom.SetName("{0}_denom_MCb".format(WP))
    hBjets_num.SetName("{0}_num_MCb".format(WP))

    hBjets_denom.Write()
    hBjets_num.Write()

    logging.info("Calculating data efficiency")
    NonBsamples = deepcopy(Samples2Stack)
    NonBsamples.pop(bindex)

    #Denominator
    NonBHistos_denom = deepcopy(StackHistos_denom)
    NonBHistos_denom.pop(bindex)

    hNonB_denom = None
    for ihisto, histo in enumerate(NonBHistos_denom):
        if ihisto == 0:
            logging.debug("Initialzing sample {0} to NonB sum".format(NonBsamples[ihisto].name))
            hNonB_denom = histo.Clone()
        else:
            logging.debug("Adding sample {0} to NonB sum".format(NonBsamples[ihisto].name))
            hNonB_denom.Add(histo)

    logging.info("b purity: {0}".format(hBjets_denom.Integral()/hNonB_denom.Integral()))

    logging.debug("Getting denom b fraction data")
    hbData_denom = hData_denom.Clone()
    hbData_denom.Add(hNonB_denom, -1)


    hData_num.SetName("{0}_num_data".format(WP))
    hData_denom.SetName("{0}_denom_data".format(WP))

    hData_num.Write()
    hData_denom.Write()


    #Numerator
    NonBHistos_num = StackHistos_num
    NonBHistos_num.pop(bindex)

    hNonB_num = None
    for ihisto, histo in enumerate(NonBHistos_num):
        if ihisto == 0:
            logging.debug("Initialzing samples {0} to NonB sum".format(NonBsamples[ihisto].name))
            hNonB_num = histo.Clone()
        else:
            logging.debug("Adding sample {0} to NonB sum".format(NonBsamples[ihisto].name))
            hNonB_num.Add(histo)


    logging.debug("Getting denom b fraction data")
    hbData_num = hData_num.Clone()
    hbData_num.Add(hNonB_num, -1)

    Dataeff = hbData_num.Integral()/hbData_denom.Integral()
    DataError = math.sqrt(Dataeff*(1-Dataeff)/hData_denom.Integral())

    results[WP]["Data"] = Dataeff
    results[WP]["DataErr"] = DataError
    logging.info("btagging Effciency in Data = {0} +- {2} [{1}]".format(Dataeff, WP, DataError))

    hbData_num.SetName("{0}_num_data-nonb".format(WP))
    hbData_denom.SetName("{0}_denom_data-nonb".format(WP))


    hbData_num.Write()
    hbData_denom.Write()

    SF = Dataeff/MCeff
    MCerrElem = MCError/MCeff
    DataErrElem = DataError/Dataeff
    SFerr = math.sqrt(MCerrElem*MCerrElem + DataErrElem*DataErrElem)*SF
    results[WP]["SF"] = SF
    results[WP]["SFErr"] = SFerr
    logging.info("btagging Efficiency SF = {0} +- {1} [{2}]".format(SF, SFerr, WP))



def saveEffTable(numWPs, results, outname):
    table = "\\toprule \n"
    table += "WP & MC & Data & SF \\\\ \n"
    table += "\\midrule \n"
    for WP in numWPs:
        table += "{0} & {1:.4f} $\\pm$ {2:.4f}\\%  & {3:.4f} $\\pm$ {4:.4f}\\% & {5:.4f} $\\pm$ {6:.4f}\\% \\\\ \n".format(WP, results[WP]["MC"], results[WP]["MCErr"]*100, results[WP]["Data"], results[WP]["DataErr"]*100, results[WP]["SF"], results[WP]["SFErr"]*100 )
    table += "\\bottomrule"


    table2 = "\\toprule \n"
    table2 += "WP & MC & Data & SF \\\\ \n"
    table2 += "\\midrule \n"
    for WP in numWPs:
        table2 += "{0} & {1:.2f} $\\pm$ {2:.2f}  & {3:.2f} $\\pm$ {4:.2f} & {5:.2f} $\\pm$ {6:.2f} \\\\ \n".format(WP, results[WP]["MC"]*100, results[WP]["MCErr"]*100, results[WP]["Data"]*100, results[WP]["DataErr"]*100, results[WP]["SF"]*100, results[WP]["SFErr"]*100 )
    table2 += "\\bottomrule"



    if outname is not None:
        txtfilename = outname+".txt"
        logging.info("Writing "+txtfilename)
        with open(txtfilename,"w") as f:
            f.write("% calulated vaules\n")
            f.write(table)
            f.write("\n")
            f.write("% in percent\n")
            f.write(table2)

                
            
