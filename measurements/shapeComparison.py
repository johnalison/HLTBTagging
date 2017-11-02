import os
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel

def shapeComparison(loglev, doMC, doData, doCSV, doDeepCSV, doperJetComp):
    import ROOT

    import modules.compPlot
    import modules.classes

    
    setup_logging(loglevel = loglev, logname = "shapeoutput", errname = "shapeerror")

    logger = logging.getLogger(__name__)

    logger.info("Starting shape comparison")

    if not (doMC or doData):
        if __name__ == "__main__":
            logging.warning("At least on of the flags --mc and --data should to be set")
            logging.warning("Falling back the only mc")
        else:
            logging.warning("At least on of the paramters doMC and doData should to be set")
            logging.warning("Falling back the only mc")
        doMC = True
    if not (doCSV or doDeepCSV):
        if __name__ == "__main__":
            logging.warning("At least on of the flags --CSV and --deepCSV should to be set")
        else:
            logging.warning("At least on of the paramters doCSV and doDeepCSV should to be set")
        logging.warning("Falling back the only CSV")
        doCSV = True


    doSampleComp = False
        
    if loglev > 0:
        ROOT.gErrorIgnoreLevel = ROOT.kError# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
    
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v2/ttbar/ttbar_v2.root"
    DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v2/MuonEG/MuonEG_v2.root"
    globalPrefix = "plotsv3/1TightTag_Nom_ltpt30_JetIDTightLep_sepSel_"

    MCSelection = "1"
    VarSelection = "1"
    TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
    LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) > 0 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) > 0"

    logging.info("Using: doMC: {0} | doData: {1} | doCSV: {2} | doDeepCSV: {3}".format(doMC, doData, doCSV, doDeepCSV))


    offlineSelection = "Sum$(offJets_pt > 30) > 2 && abs(offJets_eta) < 2.4 && offJets_pt > 30 && offJets_passesTightLeptVetoID > 0"
    pfSelection = "Sum$(pfJets_pt > 30) > 2 && abs(pfJets_eta) < 2.4 && pfJets_pt > 30 && pfJets_passesTightLeptVetoID > 0"
    caloSelection = "Sum$(caloJets_pt > 30) > 2 && abs(caloJets_eta) < 2.4 && caloJets_pt > 30"

    samples = []
    if doMC:
        eventSelection = "({0}) && ({1}) && ({2}) && ({3})".format(VarSelection, TriggerSelection, LeptonSelection, MCSelection)
        samples.append( (modules.classes.Sample("ttbar", MCInput, eventSelection, 831.76, 4591.622871124, ROOT.kRed, 9937324), "MC", "t#bar{t}") )
    if doData:
        eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
        samples.append( (modules.classes.Sample("data", DataInput, eventSelection),"MuonEG", "MuonEG") )

    
    plotVarSelection = "Sum$(offJets_csv > 0.9535) >= 1"
    if doCSV:
        logging.info("Plots: CSV for Offline, PF and Calo Jets")
        OffCSV = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "CSV value", ROOT.kBlue, "Offline jets")
        CaloCSV = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "CSV value", ROOT.kRed, "Calo jets")
        PFCSV = modules.classes.PlotBase("pfJets_csv","{0} && {1} && pfJets_csv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "CSV value", ROOT.kGreen+2, "PF jets")

        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffCSV, CaloCSV, PFCSV], sample, normalized = True, outname = globalPrefix+"JetTypeComp_OFFvPF_csv_"+postfix, label = label)

    if doData and doMC and doCSV and doSampleComp:
        logging.info("Making comparion of Offline jets CSV in data and MC")
        OffCSVMC = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kRed, "ttbar sample")
        OffCSVData = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([OffCSVMC, OffCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_OfflineJets_csv")


        logging.info("Making comparion of online pf jets CSV in data and MC")
        pfCSVMC = modules.classes.PlotBase("pfJets_csv", "{0} && {1} && pfJets_csv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet CSV value", ROOT.kRed, "ttbar sample")
        pfCSVData = modules.classes.PlotBase("pfJets_csv", "{0} && {1} && pfJets_csv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([pfCSVMC, pfCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_pfJets_csv")


        logging.info("Making comparion of online calo jets CSV in data and MC")
        CaloCSVMC = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet CSV value", ROOT.kRed, "ttbar sample")
        CaloCSVData = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([CaloCSVMC, CaloCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_caloJets_csv")


        if False:
            logging.info("Making comparion between different cuts")
            plotVarSelection1T = "Sum$(offJets_csv > 0.9535) >= 1"
            plotVarSelection0T = "1"
            plotVarSelection2M = "Sum$(offJets_csv > 0.8484) >= 2"
            OffCSVMC1T = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection1T, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kBlue, "One tight tag")
            OffCSVMC0T = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection0T, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kRed, "No tags requ.")
            OffCSVMC2M = modules.classes.PlotBase("offJets_csv", "{0} && {1} && offJets_csv >= 0".format(plotVarSelection2M, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kGreen+2, "Two medium tags")
            label = getLabel("Dataset: t#bar{t}", 0.7)
            modules.compPlot.compareSamples([OffCSVMC1T, OffCSVMC0T, OffCSVMC2M], [samples[0][0], samples[0][0], samples[0][0]], outname = globalPrefix+"TagCutComp_MC_OfflineJets_csv", label = label)
            label = getLabel("Dataset: MuonEG", 0.7)
            modules.compPlot.compareSamples([OffCSVMC1T, OffCSVMC0T, OffCSVMC2M], [samples[1][0], samples[1][0], samples[1][0]], outname = globalPrefix+"TagCutComp_Data_OfflineJets_csv", label = label)

    
    if doDeepCSV:
        logging.info("Plots: DeepCSV for Offline, PF and Calo Jets")
        plotVarSelection = "Sum$(offJets_deepcsv > 0.8958) >= 1"
        OffDeepCSV = modules.classes.PlotBase("offJets_deepcsv", "{0} && {1} && offJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "DeepCSV value", ROOT.kBlue, "Offline jets")
        CaloDeepCSV = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "DeepCSV value", ROOT.kRed, "Calo jets")
        PFDeepCSV = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "DeepCSV value", ROOT.kGreen+2, "PF jets")

        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffDeepCSV, CaloDeepCSV, PFDeepCSV], sample, normalized = True, outname = globalPrefix+"JetTypeComp_OFFvPF_deepcsv_"+postfix, label = label)

    if doData and doMC and doDeepCSV and doSampleComp:
        logging.info("Making comparion of Offline jets DeepCSV in data and MC")
        OffDeepCSVMC = modules.classes.PlotBase("offJets_deepcsv", "{0} && {1} && offJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet DeepCSV value", ROOT.kRed, "ttbar sample")
        OffDeepCSVData = modules.classes.PlotBase("offJets_deepcsv", "{0} && {1} && offJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([OffDeepCSVMC, OffDeepCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_OfflineJets_deepcsv")

        logging.info("Making comparion of online pf jets DeepCSV in data and MC")
        pfDeepCSVMC = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet DeepCSV value", ROOT.kRed, "ttbar sample")
        pfDeepCSVData = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([pfDeepCSVMC, pfDeepCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_pfJets_deepcsv")


        logging.info("Making comparion of online calo jets DeepCSV in data and MC")
        CaloDeepCSVMC = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet DeepCSV value", ROOT.kRed, "ttbar sample")
        CaloDeepCSVData = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([CaloDeepCSVMC, CaloDeepCSVData], [samples[0][0], samples[1][0]], outname = globalPrefix+"SampleComp_caloJets_deepcsv")

    if False:

        logging.info("Making offline csv plots with different pt cuts")
        plotVarSelection = "Sum$(offJets_csv > 0.6) >= 0"
        OffCSV15 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0  && offJets_matchGen>=0".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kBlue, "Offline jets p_{T} > 15 GeV")
        OffCSV20 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0  && offJets_matchGen>=0 && offJets_pt > 20".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kGreen+2, "Offline jets p_{T} > 20 GeV")
        OffCSV25 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0  && offJets_matchGen>=0 && offJets_pt > 25".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kRed, "Offline jets p_{T} > 25 GeV")
        OffCSV30 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0  && offJets_matchGen>=0 && offJets_pt > 30".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kCyan, "Offline jets p_{T} > 30 GeV")
        OffCSV35 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0  && offJets_matchGen>=0 && offJets_pt > 35".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kMagenta, "Offline jets p_{T} > 35 GeV")


        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffCSV15,OffCSV20,OffCSV25,OffCSV30,OffCSV35], sample, normalized = True, outname = "plots/0Tags_JetTypeComp_OFFptcut_wGenMatch_csv_"+postfix, label = label)

        
        logging.info("Making offline csv plots with different pt cuts")
        plotVarSelection = "Sum$(offJets_csv > 0.6) >= 0"
        OffCSV15 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kBlue, "Offline jets p_{T} > 15 GeV")
        OffCSV20 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0 && offJets_pt > 20".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kGreen+2, "Offline jets p_{T} > 20 GeV")
        OffCSV25 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0 && offJets_pt > 25".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kRed, "Offline jets p_{T} > 25 GeV")
        OffCSV30 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0 && offJets_pt > 30".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kCyan, "Offline jets p_{T} > 30 GeV")
        OffCSV35 = modules.classes.PlotBase("offJets_csv", "{0} && offJets_csv >= 0 && offJets_pt > 35".format(plotVarSelection), "1", [20,0,1], "CSV value", ROOT.kMagenta, "Offline jets p_{T} > 35 GeV")


        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffCSV15,OffCSV20,OffCSV25,OffCSV30,OffCSV35], sample, normalized = True, outname = "plots/0Tags_JetTypeComp_OFFptcut_woGenMatch_csv_"+postfix, label = label)

    if doperJetComp:
        if doCSV:
            plotVarSelection = "Sum$(offJets_csv > 0.9535) >= 1"
            plotObj = modules.classes.PlotBase2D("pfJets_csv", "offJets_csv", "{0} && {1}".format(plotVarSelection, offlineSelection), "1", [20,0,1], [20,0,1] , "Offline CSV", "PF CSV")

            modules.compPlot.make2DSummedPlot(plotObj, samples[0][0], "pfJets_csv[?]", "offJets_csv[pfJets_matchOff[?]]", 1, outname = globalPrefix+"2D_OFFvPF", iterSelection = "pfJets_csv[?] && pfJets_matchOff[?]")
        if doDeepCSV:
            pass
        
        
    logging.info("Closing shape comparison")



#def offJet(sample, 
    
if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Description'
    )

    argumentparser.add_argument(
        "--logging",
        action = "store",
        help = "Define logging level: CRITICAL - 50, ERROR - 40, WARNING - 30, INFO - 20, DEBUG - 10, NOTSET - 0 \nSet to 0 to activate ROOT root messages",
        type=int,
        default=20
    )

    argumentparser.add_argument(
        "--mc",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--data",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--CSV",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--deepCSV",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--perJetComp",
        action = "store_true",
        help = "Call without argument!",
    )
    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################

    
        
        
    shapeComparison(loglev = args.logging, doMC = args.mc, doData = args.data, doCSV = args.CSV, doDeepCSV = args.deepCSV, doperJetComp = args.perJetComp)

    logging.info("Exiting shapeComparion.py")
