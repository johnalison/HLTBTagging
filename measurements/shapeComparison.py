import os
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel

def shapeComparison(loglev, run, doMC, doData, doCSV, doDeepCSV, doperJetComp,sameTaggerComp, crossTaggerComp, onlymatch, doSampleComp, skiponOffPlots, splitDeepCSV, looseSel):
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

    if crossTaggerComp and not (doCSV and doDeepCSV):
        if __name__ == "__main__":
            logging.warning("For cross tagger comparison both flags --CSV and --deepCSV have to be set")
        else:
            logging.warning("For cross tagger comparison both flags doCSV and doDeepCSV have to be set")
        logging.warning("Enabeling CSV and DeepCSV")
        doCSV = True
        doDeepCSV = True

    if not (doCSV or doDeepCSV):
        if __name__ == "__main__":
            logging.warning("At least on of the flags --CSV and --deepCSV should to be set")
        else:
            logging.warning("At least on of the paramters doCSV and doDeepCSV should to be set")
        logging.warning("Falling back the only CSV")
        doCSV = True

    if doperJetComp and not (sameTaggerComp or crossTaggerComp):
        if __name__ == "__main__":
            logging.warning("At least one of the flags --sameTagger and --crossTagger has to be set with --perJetComp enabled")
        else:
            logging.warning("At least one of the flags sameTaggerComp and crossTaggerComp has to be set with doJetcomp enabled")
        logging.warning("Falling back sameTagger")
        sameTaggerComp = True

    if run not in ["CD", "E", "F"]:
        logging.error("Run not supported!")
        exit()
    
    if loglev > 0:
        ROOT.gErrorIgnoreLevel = ROOT.kBreak# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;

    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v8/ttbar/phase1/ttbar_0p85_mod_mod_mod.root"
    if run == "CD":
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v8/MuonEG/MuonEG_RunCD_phase1_0p9970p996_mod_mod_mod.root"
        basepath = "v8nTuples/shapeComp/"
        puweight = "get_puWeight(pu)"
        globalPrefix = "DeepCSVMPresel_phase1_RunCD_"
        subfolder = "RunCD"
    if run == "E":
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v8/MuonEG/RunE/phase1/MuonEG_RunE_phase1_mod_mod_mod.root"
        basepath = "v8nTuples/shapeComp/"
        puweight = "wPURunE"
        globalPrefix = "DeepCSVMPresel_phase1_RunE_EmilSel_"
        subfolder = "RunE"
    if run == "F":
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v8/MuonEG/RunF/phase1/MuonEG_RunF_phase1_mod_mod_mod.root"
        basepath = "v7nTuples_v2/shapeComp/"
        puweight = "wPURunF"
        globalPrefix = "DeepCSVMPresel_phase1_RunF_"
        subfolder = "RunF"
    
    if looseSel:
        MCSelection = "1"
        DataSelection = "1"
        VarSelection = "1"
        TriggerSelection = "1"
        LeptonSelection = "1"

        logging.info("Using: doMC: {0} | doData: {1} | doCSV: {2} | doDeepCSV: {3}".format(doMC, doData, doCSV, doDeepCSV))

        offlineeventSelection = "1"
        offlineSelection = "{0} && abs(cleanJets_eta) < 2.4 && cleanJets_pt > 30".format(offlineeventSelection)
        pfSelection = "abs(pfJets_eta) < 2.4 && pfJets_pt > 30 && pfJets_passesTightLeptVetoID > 0"
        caloSelection = "abs(caloJets_eta) < 2.4 && caloJets_pt > 30"

    else:
        MCSelection = "1"
        DataSelection = "1"
        VarSelection = "1"
        TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
        LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) > 0 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) > 0"

        logging.info("Using: doMC: {0} | doData: {1} | doCSV: {2} | doDeepCSV: {3}".format(doMC, doData, doCSV, doDeepCSV))

        offlineeventSelection = "Sum$(cleanJets_pt > 30 && abs(cleanJets_eta) < 2.4) >= 2 "
        offlineSelection = "{0} && abs(cleanJets_eta) < 2.4 && cleanJets_pt > 30 && cleanJets_passesTightLeptVetoID > 0".format(offlineeventSelection)
        pfSelection = "Sum$(pfJets_pt > 30 && abs(pfJets_eta) < 2.4) > 2 && abs(pfJets_eta) < 2.4 && pfJets_pt > 30 && pfJets_passesTightLeptVetoID > 0"
        caloSelection = "Sum$(caloJets_pt > 30 && abs(caloJets_eta) < 2.4) > 2 && abs(caloJets_eta) < 2.4 && caloJets_pt > 30"

    samples = []
    if doMC:
        eventSelection = "({0}) && ({1}) && ({2}) && ({3})".format(VarSelection, TriggerSelection, LeptonSelection, MCSelection)
        samples.append( (modules.classes.Sample("ttbar", MCInput, eventSelection, 831.76, 4591.622871124, ROOT.kRed, 9937324, weight = puweight), "MC", "t#bar{t}") )
    if doData:
        eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
        samples.append( (modules.classes.Sample("data", DataInput, eventSelection, color= ROOT.kBlue),"MuonEG", "MuonEG") )

    
    plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958 && cleanJets_pt > 30 && abs(cleanJets_eta) < 2.4) >= 1"
    if doCSV and not skiponOffPlots and not onlymatch:
        logging.info("Plots: CSV for Offline, PF and Calo Jets")
        OffCSV = modules.classes.PlotBase("cleanJets_csv", "{0} && {1} && cleanJets_csv > 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "CSV value", ROOT.kBlue, "Offline jets")
        CaloCSV = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv > 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "CSV value", ROOT.kRed, "Calo jets")
        PFCSV = modules.classes.PlotBase("pfJets_csv","{0} && {1} && pfJets_csv > 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "CSV value", ROOT.kGreen+2, "PF jets")

        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffCSV, CaloCSV, PFCSV], sample, normalized = True, outname = basepath+globalPrefix+"JetTypeComp_OFFvPF_csv_"+postfix, label = label)

    if doData and doMC and doCSV and doSampleComp and not onlymatch:
        logging.info("Making comparion of Offline jets CSV in data and MC")
        OffCSVMC = modules.classes.PlotBase("cleanJets_csv", "{0} && {1} && cleanJets_csv > 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kRed, "t#bar{t} sample")
        OffCSVData = modules.classes.PlotBase("cleanJets_csv", "{0} && {1} && cleanJets_csv > 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([OffCSVMC, OffCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_OfflineJets_csv")


        logging.info("Making comparion of online pf jets CSV in data and MC")
        pfCSVMC = modules.classes.PlotBase("pfJets_csv", "{0} && {1} && pfJets_csv > 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet CSV value", ROOT.kRed, "t#bar{t} sample")
        pfCSVData = modules.classes.PlotBase("pfJets_csv", "{0} && {1} && pfJets_csv > 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([pfCSVMC, pfCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_pfJets_csv")


        logging.info("Making comparion of online calo jets CSV in data and MC")
        CaloCSVMC = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv > 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet CSV value", ROOT.kRed, "t#bar{t} sample")
        CaloCSVData = modules.classes.PlotBase("caloJets_csv", "{0} && {1} && caloJets_csv >  0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet CSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([CaloCSVMC, CaloCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_caloJets_csv")

    
    if doDeepCSV and not skiponOffPlots and not onlymatch:
        logging.info("Plots: DeepCSV for Offline, PF and Calo Jets")
        OffDeepCSV = modules.classes.PlotBase("cleanJets_deepcsv_b", "{0} && {1} && cleanJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "DeepCSV value", ROOT.kBlue, "Offline jets")
        CaloDeepCSV = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "DeepCSV value", ROOT.kRed, "Calo jets")
        PFDeepCSV = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "DeepCSV value", ROOT.kGreen+2, "PF jets")

        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)
            modules.compPlot.compareJetTypes([OffDeepCSV, CaloDeepCSV, PFDeepCSV], sample, normalized = True, outname = basepath+globalPrefix+"JetTypeComp_OFFvPF_deepcsv_"+postfix, label = label)

    if doData and doMC and doDeepCSV and doSampleComp and not onlymatch:
        logging.info("Making comparion of Offline jets DeepCSV in data and MC")
        OffDeepCSVMC = modules.classes.PlotBase("cleanJets_deepcsv_b", "{0} && {1} && cleanJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet DeepCSV value", ROOT.kRed, "t#bar{t} sample")
        OffDeepCSVData = modules.classes.PlotBase("cleanJets_deepcsv_b", "{0} && {1} && cleanJets_deepcsv >= 0".format(plotVarSelection, offlineSelection), "1", [20,0,1], "Offline jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([OffDeepCSVMC, OffDeepCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_OfflineJets_deepcsv")

        logging.info("Making comparion of online pf jets DeepCSV in data and MC")
        pfDeepCSVMC = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet DeepCSV value", ROOT.kRed, "t#bar{t} sample")
        pfDeepCSVData = modules.classes.PlotBase("pfJets_deepcsv", "{0} && {1} && pfJets_deepcsv >= 0".format(plotVarSelection, pfSelection), "1", [20,0,1], "pf jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([pfDeepCSVMC, pfDeepCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_pfJets_deepcsv")


        logging.info("Making comparion of online calo jets DeepCSV in data and MC")
        CaloDeepCSVMC = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet DeepCSV value", ROOT.kRed, "t#bar{t} sample")
        CaloDeepCSVData = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1} && caloJets_deepcsv >= 0".format(plotVarSelection, caloSelection), "1", [20,0,1], "calo jet DeepCSV value", ROOT.kBlue, "MuonEG sample")

        modules.compPlot.compareSamples([CaloDeepCSVMC, CaloDeepCSVData], [samples[0][0], samples[1][0]], outname = basepath+globalPrefix+"SampleComp_caloJets_deepcsv")



    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    ################################################################# PLOT ONLY IF ONLINE AND OFFLINE IS MATCHED #############################################################
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################

    if doCSV and not skiponOffPlots and onlymatch:
        commonJetSelection ="abs(cleanCSVJets_eta[?]) < 2.4 && cleanCSVJets_pt[?] > 30 && cleanCSVJets_passesTightLeptVetoID[?] > 0"
        commonPFJetSelection = commonJetSelection+" && cleanCSVJets_matchPF2[?] >= 0"
        commonCaloJetSelection =  commonJetSelection+" && cleanCSVJets_matchCalo2[?] >= 0"

        commonJetSelectionpt ="abs(cleanJets_eta[?]) < 2.4 && cleanJets_pt[?] > 30 && cleanJets_passesTightLeptVetoID[?] > 0"
        commonPFJetSelectionpt = commonJetSelectionpt+" && cleanJets_matchPF2[?] >= 0"
        commonCaloJetSelectionpt =  commonJetSelectionpt+" && cleanJets_matchCalo2[?] >= 0"

        #commonpfJetSelection = "pfJets_matchOff[?] >= 0"
        logging.info("Plots: CSV for Offline, PF Jets (matched!)")
        #plotVarSelection = "Sum$(cleanJets_csv > 0.9535) >= 1"
        
        OffCSV = modules.classes.PlotBase("cleanCSVJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "CSV value", ROOT.kBlue, "Offline jets")
        CaloCSV = modules.classes.PlotBase("caloJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "CSV value", ROOT.kRed, "Calo jets")
        PFCSV = modules.classes.PlotBase("pfJets_csv","{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "CSV value", ROOT.kGreen+2, "PF jets")
        PFCSVLeading = modules.classes.PlotBase("pfJets_csv","{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0,1], "leading CSV value", ROOT.kPink, "PF jets")
        """
        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)

            modules.compPlot.compareSumJetTypes([OffCSV, PFCSV], sample, ["cleanCSVJets_csv[?]", "pfJets_csv[cleanCSVJets_matchPF2[?]]"], 10,
                                                iterSelections = [commonPFJetSelection,commonPFJetSelection], normalized = False, outname = basepath+globalPrefix+"MatchedJetTypeComp_OffvPF_csv_"+postfix, label = label )
            modules.compPlot.compareSumJetTypes([OffCSV, CaloCSV], sample, ["cleanCSVJets_csv[?]", "caloJets_csv[cleanCSVJets_matchCalo2[?]]"], 10,
                                                iterSelections = [commonCaloJetSelection,commonCaloJetSelection], normalized = False, outname = basepath+globalPrefix+"MatchedJetTypeComp_OffvCalo_csv_"+postfix, label = label )
        """
        if doSampleComp and doMC and doData:
            logging.info("Doing sample comp")
#            modules.compPlot.compareSumJetSamples(PFCSV, samples, "pfJets_csv[cleanCSVJets_matchPF2[?]]", 10, commonPFJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_PF_csv_DataMC")
            modules.compPlot.compareSumJetSamples(PFCSVLeading, samples, "pfJets_csv[cleanJets_matchPF2[?]]", 1, commonPFJetSelectionpt, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_leadingpt_PF_csv_DataMC")
#            modules.compPlot.compareSumJetSamples(CaloCSV, samples, "caloJets_csv[cleanCSVJets_matchCalo2[?]]", 10, commonCaloJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_Calo_csv_DataMC")
#            modules.compPlot.compareSumJetSamples(OffCSV, samples, "cleanCSVJets_csv[?]", 10, commonJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_Off_csv_DataMC")
            
    if doDeepCSV and not skiponOffPlots and onlymatch:
        commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0"
        commonPFJetSelection = commonJetSelection+" && cleanDeepCSVJets_matchPF2[?] >= 0"
        commonCALOJetSelection = commonJetSelection+" && cleanDeepCSVJets_matchCalo2[?] >= 0"

        #commonpfJetSelection = "pfJets_matchOff[?] >= 0"
        logging.info("Plots: DeepCSV for Offline, PF Jets (matched!)")
        #plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958) >= 1"
        
        OffDeepCSV = modules.classes.PlotBase("cleanDeepCSVJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "DeepCSV value", ROOT.kBlue, "Offline jets")
        CaloDeepCSV = modules.classes.PlotBase("caloJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "DeepCSV value", ROOT.kRed, "Calo jets")
        PFDeepCSV = modules.classes.PlotBase("pfJets_deepcsv","{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], "DeepCSV value", ROOT.kGreen+2, "PF jets")
        for sample, postfix, nicename in samples:

            logging.info("Processing "+postfix)
            label = getLabel("Dataset: {0}".format(nicename), 0.7)

            modules.compPlot.compareSumJetTypes([OffDeepCSV, PFDeepCSV], sample, ["cleanDeepCSVJets_deepcsv[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]"], 10,
                                                iterSelections = [commonJetSelection,commonJetSelection], normalized = False, outname = basepath+globalPrefix+"MatchedJetTypeComp_OffvPF_deepcsv_"+postfix, label = label )
            modules.compPlot.compareSumJetTypes([OffDeepCSV, CaloDeepCSV], sample, ["cleanDeepCSVJets_deepcsv[?]", "caloJets_deepcsv[cleanDeepCSVJets_matchCalo2[?]]"], 10,
                                                iterSelections = [commonJetSelection,commonJetSelection], normalized = False, outname = basepath+globalPrefix+"MatchedJetTypeComp_OffvCalo_deepcsv_"+postfix, label = label )
        if doSampleComp and doMC and doData:
            logging.info("Doing sample comp")
            modules.compPlot.compareSumJetSamples(PFDeepCSV, samples, "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, commonPFJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_PF_deepcsv_DataMC")
            modules.compPlot.compareSumJetSamples(CaloDeepCSV, samples, "caloJets_deepcsv[cleanDeepCSVJets_matchCalo2[?]]", 10, commonCaloJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_Calo_deepcsv_DataMC")
            modules.compPlot.compareSumJetSamples(OffDeepCSV, samples, "cleanDeepCSVJets_deepcsv[?]", 10, commonJetSelection, normalized = True, outname = basepath+globalPrefix+"MatchedJetTypeComp_Off_deepcsv_DataMC")

            
    if doperJetComp:
        logging.info("Makeing perJetComp plots")
        ##########################################################################################################################################################################
        ########################################################################### Same tagger comparisons ######################################################################
        ##########################################################################################################################################################################
        if sameTaggerComp:
            logging.info("Same tagger comparison")
            csvZeroCut = "cleanCSVJets_csv[?] > 0 && pfJets_csv[cleanCSVJets_matchPF2[?]] > 0"
            if doCSV:
                logging.info("CSV comparisons per Jet")
                #plotVarSelection = "Sum$(cleanJets_csv > 0.9535) >= 1"
                if looseSel:
                    commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 &&  cleanDeepCSVJets_matchPF2[?] >= 0"
                    commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                else:
                    commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchPF2[?] >= 0"
                    commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                for sample, postfix, nicename in samples:
                    if postfix == "MC":
                        _subfolder = subfolder
                        subfolder = postfix
                    logging.info("Processing sample: "+sample.name)
                    DSlabel = getLabel("Dataset: {0}".format(nicename), 0.5)
                    #Define plots
                    CSV2DFullLog = modules.classes.PlotBase2D("cleanDeepCSVJets_csv","pfJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline CSV", "matched PF CSV")
                    CSV2DFullLogCalo = modules.classes.PlotBase2D("cleanDeepCSVJets_csv","caloJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline CSV", "matched Calo CSV")
                    CSV2DQ1 = modules.classes.PlotBase2D( "cleanDeepCSVJets_csv","pfJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0.5,1], [20,0.5,1] , "Offline CSV", "matched PF CSV")
                    CSV2DQ3 = modules.classes.PlotBase2D("cleanDeepCSVJets_csv", "pfJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0,0.5], [20,0,0.5] , "Offline CSV", "matched PF CSV")
                    #Make Plots
                    #Full range
                    modules.compPlot.make2DSummedPlot(CSV2DFullLog, sample, "cleanDeepCSVJets_csv[?]",  "pfJets_csv[cleanDeepCSVJets_matchPF2[?]]",10, outname = "{2}{3}/{0}_CSV_2D_OFFvPF_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = commonJetSelection, drawindividualhistos =  False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "CSV Value", iterStart = 1)
                    modules.compPlot.make2DSummedPlot(CSV2DFullLogCalo, sample, "cleanDeepCSVJets_csv[?]",  "caloJets_csv[cleanDeepCSVJets_matchCalo2[?]]",10, outname = "{2}{3}/{0}_CSV_2D_OFFvCalo_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = commonCaloJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "CSV Value", iterStart = 1)
                    # Partial range
                    modules.compPlot.make2DSummedPlot(CSV2DQ1, sample, "cleanDeepCSVJets_csv[?]", "pfJets_csv[cleanDeepCSVJets_matchPF2[?]]", 5, outname = "{2}{3}/{0}_CSV_2D_OFFvPF_Q1_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = "{0} && {1}".format(commonJetSelection, csvZeroCut), LogZ = True, label = DSlabel, iterStart = 1)
                    modules.compPlot.make2DSummedPlot(CSV2DQ3, sample, "cleanDeepCSVJets_csv[?]", "pfJets_csv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_CSV_2D_OFFvPF_Q3_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = "{0} && {1}".format(commonJetSelection, csvZeroCut), LogZ = True, label = DSlabel, iterStart = 1)
                    if postfix == "MC":
                        subfolder = _subfolder
            if doDeepCSV:
                logging.info("DeepCSV comparisons per Jet")
                #plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958) >= 1"
                if looseSel:
                    commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_matchPF2[?] >= 0"
                    commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                else:
                    commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchPF2[?] >= 0"
                    commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                for sample, postfix, nicename in samples:
                    if postfix == "MC":
                        _subfolder = subfolder
                        subfolder = postfix
                    logging.info("Processing sample: "+sample.name)
                    DSlabel = getLabel("Dataset: {0}".format(nicename), 0.5)
                    #Define plots
                    DeepCSV2DFullLog = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv", "pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV", "matched PF DeepCSV")
                    DeepCSV2DFullLogCalo = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv", "caloJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV", "matched calo DeepCSV")

                    DeepCSV2DQ1 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0.5,1], [20,0.5,1] , "Offline DeepCSV", "matched PF DeepCSV")
                    DeepCSV2DQ3 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0,0.5], [20,0,0.5] , "Offline DeepCSV", "matched PF DeepCSV")
                    #Make Plots
                    # Full range
                    modules.compPlot.make2DSummedPlot(DeepCSV2DFullLog, sample, "cleanDeepCSVJets_deepcsv[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_2D_OFFvPF_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = commonJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value", iterStart = 1)
                    modules.compPlot.make2DSummedPlot(DeepCSV2DFullLogCalo, sample, "cleanDeepCSVJets_deepcsv[?]", "caloJets_deepcsv[cleanDeepCSVJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_2D_OFFvCalo_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = commonCaloJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value", iterStart = 1)
                    # Partial range
                    modules.compPlot.make2DSummedPlot(DeepCSV2DQ1, sample, "cleanDeepCSVJets_deepcsv[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]", 5, outname = "{2}{3}/{0}_DeepCSV_2D_OFFvPF_Q1_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel, iterStart = 1)
                    modules.compPlot.make2DSummedPlot(DeepCSV2DQ3, sample, "cleanDeepCSVJets_deepcsv[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_2D_OFFvPF_Q3_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                      iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel, iterStart = 1)
                    if postfix == "MC":
                        subfolder = _subfolder
                if splitDeepCSV:
                     logging.info("DeepCSV (probb only)  comparisons per Jet")
                     #plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958) >= 1"
                     commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchPF2[?] >= 0"
                     commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                     for sample, postfix, nicename in samples:
                         if postfix == "MC":
                             _subfolder = subfolder
                             subfolder = postfix
                         logging.info("Processing sample: "+sample.name)
                         DSlabel = getLabel("Dataset: {0}".format(nicename), 0.5)
                         #Define plots
                         DeepCSV2DFullLog = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_b", "pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV (probb)", "matched PF DeepCSV")
                         DeepCSV2DFullLogCalo = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_b", "caloJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV (probb)", "matched Calo DeepCSV")
                         DeepCSV2DQ1 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_b","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0.5,1], [20,0.5,1] , "Offline DeepCSV (probb)", "matched PF DeepCSV")
                         DeepCSV2DQ3 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_b","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0,0.5], [20,0,0.5] , "Offline DeepCSV (probb)", "matched PF DeepCSV")
                         #Make Plots
                         # Full range
                         modules.compPlot.make2DSummedPlot(DeepCSV2DFullLog, sample, "cleanDeepCSVJets_deepcsv_b[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]+ pfJets_deepcsv_bb[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_b_2D_OFFvPF_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                           iterSelection = commonJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value (probb)")
                         modules.compPlot.make2DSummedPlot(DeepCSV2DFullLogCalo, sample, "cleanDeepCSVJets_deepcsv_b[?]", "caloJets_deepcsv[cleanDeepCSVJets_matchCalo2[?]] + caloJets_deepcsv_bb[cleanDeepCSVJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_b_2D_OFFvCalo_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                           iterSelection = commonCaloJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value (probb)")
                         # Partial range
                         #modules.compPlot.make2DSummedPlot(DeepCSV2DQ1, sample, "cleanDeepCSVJets_deepcsv_b[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 5, outname = "{2}{0}_DeepCSV_b_2D_OFFvPF_Q1_{1}".format(globalPrefix, postfix, basepath),
                         #                                  iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel)
                         #modules.compPlot.make2DSummedPlot(DeepCSV2DQ3, sample, "cleanDeepCSVJets_deepcsv_b[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{0}_DeepCSV_b_2D_OFFvPF_Q3_{1}".format(globalPrefix, postfix, basepath),
                         #                                  iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel)
                         if postfix == "MC":
                             subfolder = _subfolder
                     logging.info("DeepCSV (probbb only)  comparisons per Jet")
                     #plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958) >= 1"
                     commonJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchPF2[?] >= 0"
                     commonCaloJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchCalo2[?] >= 0"
                     for sample, postfix, nicename in samples:
                         if postfix == "MC":
                             _subfolder = subfolder
                             subfolder = postfix
                         logging.info("Processing sample: "+sample.name)
                         DSlabel = getLabel("Dataset: {0}".format(nicename), 0.5)
                         #Define plots
                         DeepCSV2DFullLog = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_bb", "pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV (probbb)", "matched PF DeepCSV")
                         DeepCSV2DFullLogCalo = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_bb", "caloJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1] , "Offline DeepCSV (probbb)", "matched Calo DeepCSV")
                         DeepCSV2DQ1 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_bb","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0.5,1], [20,0.5,1] , "Offline DeepCSV (probbb)", "matched PF DeepCSV")
                         DeepCSV2DQ3 = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv_bb","pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [20,0,0.5], [20,0,0.5] , "Offline DeepCSV (probbb)", "matched PF DeepCSV")
                         #Make Plots
                         # Full range
                         modules.compPlot.make2DSummedPlot(DeepCSV2DFullLog, sample, "cleanDeepCSVJets_deepcsv_bb[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_bb_2D_OFFvPF_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                           iterSelection = commonJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value (probbb)")
                         modules.compPlot.make2DSummedPlot(DeepCSV2DFullLogCalo, sample, "cleanDeepCSVJets_deepcsv_bb[?]", "caloJets_deepcsv[cleanDeepCSVJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_DeepCSV_bb_2D_OFFvCalo_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                           iterSelection = commonCaloJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = True, projectionTitle = "DeepCSV Value (probbb)")
                         # Partial range
                         #modules.compPlot.make2DSummedPlot(DeepCSV2DQ1, sample, "cleanDeepCSVJets_deepcsv_bb[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 5, outname = "{2}{0}_DeepCSV_bb_2D_OFFvPF_Q1_{1}".format(globalPrefix, postfix, basepath),
                         #                                  iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel)
                         #modules.compPlot.make2DSummedPlot(DeepCSV2DQ3, sample, "cleanDeepCSVJets_deepcsv_bb[?]", "pfJets_deepcsv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{0}_DeepCSV_bb_2D_OFFvPF_Q3_{1}".format(globalPrefix, postfix, basepath),
                         #                                  iterSelection = "{0}".format(commonJetSelection), LogZ = True, label = DSlabel)
                         if postfix == "MC":
                             subfolder = _subfolder

        ##########################################################################################################################################################################
        ########################################################################## Cross tagger comparisons ######################################################################
        ##########################################################################################################################################################################
        if crossTaggerComp and doCSV and doDeepCSV:
            logging.info("Cross tagger comparison")
            logging.info("CSV comparisons per Jet")
            sortfolder = "crossTagger/"
            #From CSV
            #plotVarSelection = "Sum$(cleanJets_deepcsv > 0.8958) >= 1"
            commonPFJetSelection = "abs(cleanCSVJets_eta[?]) < 2.4 && cleanCSVJets_pt[?] > 30 && cleanCSVJets_passesTightLeptVetoID[?] > 0 && cleanCSVJets_matchPF2[?] >= 0"
            commonCaloJetSelection = "abs(cleanCSVJets_eta[?]) < 2.4 && cleanCSVJets_pt[?] > 30 && cleanCSVJets_passesTightLeptVetoID[?] > 0 && cleanCSVJets_matchCalo2[?] >= 0"
            commonPFDeepJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchPF2[?] >= 0"
            commonCaloDeepJetSelection = "abs(cleanDeepCSVJets_eta[?]) < 2.4 && cleanDeepCSVJets_pt[?] > 30 && cleanDeepCSVJets_passesTightLeptVetoID[?] > 0 && cleanDeepCSVJets_matchCalo2[?] >= 0"

            for sample, postfix, nicename in samples:
                if postfix == "MC":
                    _subfolder = subfolder
                    subfolder = postfix
                logging.info("Processing sample: "+sample.name)
                DSlabel = getLabel("Dataset: {0}".format(nicename), 0.5)
                #Define Plots
                OffDeepCSVvPFCSV2DLog = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv", "pfJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Offline DeepCSV", "matched PF CSV")
                OffDeepCSVvCaloCSV2DLog = modules.classes.PlotBase2D("cleanDeepCSVJets_deepcsv", "caloJets_csv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Offline DeepCSV", "matched Calo CSV")
                OffCSVvPFDeepCSV2DLog = modules.classes.PlotBase2D("cleanCSVJets_csv", "pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Offline CSV", "matched PF DeepCSV")
                OffCSVvCaloDeepCSV2DLog = modules.classes.PlotBase2D("cleanCSVJets_deepcsv", "pfJets_deepcsv", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Offline CSV", "matched Calo DeepCSV")

                OfflineCSVvDeepCSV2DLog = modules.classes.PlotBase2D("cleanJets_csv", "cleanJets_deepCSV", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Offline CSV", "Offline DeepCSV")
                PFCSVvDeepCSV2DLog = modules.classes.PlotBase2D("pfJets_csv", "cleanJets_deepCSV", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "PF CSV", "PF DeepCSV")
                CaloCSVvDeepCSV2DLog = modules.classes.PlotBase2D("caloJets_csv", "caloJets_deepCSV", "{0} && {1}".format(plotVarSelection, offlineeventSelection), "1", [40,0,1], [40,0,1], "Calo CSV", "Calo DeepCSV")

                #Make plots
                modules.compPlot.make2DSummedPlot(OffDeepCSVvPFCSV2DLog, sample, "cleanDeepCSVJets_deepcsv[?]", "pfJets_csv[cleanDeepCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_CrossTag_OffDeepCSVvPFCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = commonPFDeepJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                modules.compPlot.make2DSummedPlot(OffDeepCSVvCaloCSV2DLog, sample, "cleanDeepCSVJets_deepcsv[?]", "caloJets_csv[cleanDeepCSVJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_CrossTag_OffDeepCSVvCaloCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = commonCaloDeepJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                modules.compPlot.make2DSummedPlot(OffCSVvPFDeepCSV2DLog, sample, "cleanCSVJets_csv[?]", "pfJets_deepcsv[cleanCSVJets_matchPF2[?]] + pfJets_deepcsv_bb[cleanCSVJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_CrossTag_OffCSVvPFDeepCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = commonPFJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                modules.compPlot.make2DSummedPlot(OffCSVvCaloDeepCSV2DLog, sample, "cleanCSVJets_csv[?]", "caloJets_deepcsv[cleanCSVJets_matchCalo2[?]] + caloJets_deepcsv_bb[cleanCSVJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_CrossTag_OffCSVvCaloDeepCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = commonCaloJetSelection, drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                

                modules.compPlot.make2DSummedPlot(OfflineCSVvDeepCSV2DLog, sample, "cleanJets_csv[?]", "cleanJets_deepcsv[?]", 10, outname = "{2}{0}_TagComp_OffJets_CSVvDeepCSV_2D_{1}".format(globalPrefix, postfix, basepath),
                                                  iterSelection = "abs(cleanJets_eta[?]) < 2.4 && cleanJets_pt[?] > 30 && cleanJets_passesTightLeptVetoID[?] > 0", drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                modules.compPlot.make2DSummedPlot(PFCSVvDeepCSV2DLog, sample, "pfJets_csv[cleanJets_matchPF2[?]]", "pfJets_deepcsv[cleanJets_matchPF2[?]] + pfJets_deepcsv_bb[cleanJets_matchPF2[?]]", 10, outname = "{2}{3}/{0}_TagComp_PFJets_CSVvDeepCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = "abs(cleanJets_eta[?]) < 2.4 && cleanJets_pt[?] > 30 && cleanJets_passesTightLeptVetoID[?] > 0 && cleanJets_matchPF2[?] >= 0", drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)
                modules.compPlot.make2DSummedPlot(CaloCSVvDeepCSV2DLog, sample, "caloJets_csv[cleanJets_matchCalo2[?]]", "caloJets_deepcsv[cleanJets_matchCalo2[?]] + caloJets_deepcsv_bb[cleanJets_matchCalo2[?]]", 10, outname = "{2}{3}/{0}_TagComp_CaloJets_CSVvDeepCSV_2D_{1}".format(globalPrefix, postfix, basepath, subfolder),
                                                  iterSelection = "abs(cleanJets_eta[?]) < 2.4 && cleanJets_pt[?] > 30 && cleanJets_passesTightLeptVetoID[?] > 0 && offJets_matchCalo2[?] >= 0", drawindividualhistos = False, LogZ = True, label = DSlabel, drawProjection = False)

                if postfix == "MC":
                    subfolder = _subfolder
                    
        
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
        "--run",
        action = "store",
        help = "Set Run for measurement. Option CD, E, F",
        type = str,
        default = "CD"
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
        "--csv",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--deepcsv",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--perJetComp",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--sameTagger",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--crossTagger",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--nomatch",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--sampleComp",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--skip1DComp",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--splitDeepCSV",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--looseSel",
        action = "store_true",
        help = "Removing most cuts on trigger, event, etc",
    )
    

    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################

        
    shapeComparison(loglev = args.logging, run = args.run, doMC = args.mc, doData = args.data, doCSV = args.csv, doDeepCSV = args.deepcsv,
                    doperJetComp = args.perJetComp, sameTaggerComp = args.sameTagger, crossTaggerComp = args.crossTagger, onlymatch = not args.nomatch,
                    doSampleComp = args.sampleComp, skiponOffPlots = args.skip1DComp, splitDeepCSV = args.splitDeepCSV, looseSel=  args.looseSel)

    logging.info("Exiting shapeComparion.py")
