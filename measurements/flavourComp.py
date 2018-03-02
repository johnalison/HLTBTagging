import os
import time
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel
from ConfigParser import SafeConfigParser

def flavourComposition(loglev, run, doData, doCSV, doDeepCSV, plotinclusive, plotTagAndProbe, calcEfficiency, TagWPCSV = 0.8484, TagWPDeepCSV = 0.8958, test = False):
    import ROOT

    import modules.classes
    import modules.DataMC
    import modules.TagNProbe

    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")
    
    setup_logging(loglevel = loglev, logname = "shapeoutput", errname = "shapeerror")

    logger = logging.getLogger(__name__)
    #logging.getLogger(__name__).setLevel("SUBDEBUG")
    
    logger.info("Starting flavour composition analysis")
    t0 = time.time()
    
    if not (doCSV or doDeepCSV):
        if __name__ == "__main__":
            logging.warning("At least on of the flags --CSV and --deepCSV should to be set")
        else:
            logging.warning("At least on of the paramters doCSV and doDeepCSV should to be set")
        logging.warning("Falling back the only CSV")
        doCSV = True

    if run not in ["CD", "E", "F"]:
        logging.error("Run not supported!")
        exit()
    ##############################################################################################################
    ############################################## Plotting Code #################################################
    ##############################################################################################################

    if loglev > 0:
        ROOT.gErrorIgnoreLevel = ROOT.kError# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
    
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v7/ttbar/phase1/ttbar_0p6.root"

    #Run C-D
    if run == "CD":
        logging.info("Setting file, pu weight, name and basepath for Run CD")
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v7/MuonEG/MuonEG_RunCD_phase1.root"
        puweight = "get_puWeight(pu)"
        globalPrefix = "DeepCSVMPresel_phase1_RunCD"
        basepath = "v7nTuples_v2/FlavourSplitting/RunCD/" 
    
    #Run F
    if run == "F":
        logging.info("Setting file, pu weight, name and basepath for Run F")
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v7/MuonEG/RunF/phase1/MuonEG_RunF_phase1_avail.root"
        puweight = "wPURunF"
        globalPrefix = "DeepCSVMPresel_phase1_RunF"
        basepath = "v7nTuples_v2/FlavourSplitting/RunF/" 
    
    #Run E
    if run == "E":
        logging.info("Setting file, pu weight, name and basepath for Run E")
        DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v7/MuonEG/RunE/phase1/MuonEG_RunE_phase1_part.root"
        puweight = "wPURunE"
        globalPrefix = "DeepCSVMPresel_phase1_RunE"
        basepath = "v7nTuples_v2/FlavourSplitting/RunE/" 
    
    MCSelection = "1"
    DataSelection = "1"
    VarSelection = "Sum$(offCleanJets_deepcsv > 0.8958 && offCleanJets_pt > 30 && abs(offCleanJets_eta) < 2.4) >= 1 && Sum$(offCleanJets_pt > 30 && abs(offCleanJets_eta) < 2.4) >= 2"
    TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
    LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) > 0 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) > 0"


    
    offlineSelection = "abs(offCleanJets_eta) < 2.4 && offCleanJets_pt > 30 && offCleanJets_passesTightLeptVetoID > 0"
    offlineSelectionIter = "abs(offCleanJets_eta[?]) < 2.4 && offCleanJets_pt[?] > 30 && offCleanJets_passesTightLeptVetoID[?] > 0"

    MCsamples = []
    MCsamplesIter = []

    datalumi = 4591.622871124
    
    eventSelection = "({0}) && ({1}) && ({2}) && ({3})".format(VarSelection, TriggerSelection, LeptonSelection, MCSelection)
    #MCsamples.append( modules.classes.Sample("ttbar_unmatchedJets", MCInput, "{0} && (  abs(offCleanJets_mcFlavour[?]) != 21 && abs(offCleanJets_mcFlavour[?]) > 5 )".format(eventSelection), 831.76, datalumi, ROOT.kWhite, 9767140, weight = puweight, legendText = "unmatched jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_udsgJets", MCInput, "{0} && offCleanJets_hadronFlavour == 0".format(eventSelection), 831.76, datalumi, ROOT.kBlue, 9767140, weight = puweight, legendText = "light jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_cJets", MCInput, "{0} && offCleanJets_hadronFlavour == 4".format(eventSelection), 831.76, datalumi, ROOT.kGreen+2, 9767140, weight = puweight, legendText = "c jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_bJets", MCInput, "{0} && offCleanJets_hadronFlavour == 5".format(eventSelection), 831.76, datalumi, ROOT.kRed, 9767140, weight = puweight, legendText = "b jets (t#bar{t})") )

    #MCsamplesIter.append( modules.classes.Sample("ttbar_unmatchedJets", MCInput, "{0} && ( abs(offCleanJets_mcFlavour[?]) != 21 && abs(offCleanJets_mcFlavour[?]) > 5 )".format(eventSelection), 831.76, datalumi, ROOT.kWhite, 9767140, weight = puweight, legendText = "unmatched jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_udsgJets", MCInput, "{0} && offCleanJets_hadronFlavour[?] == 0".format(eventSelection), 831.76, datalumi, ROOT.kBlue, 9767140, weight = puweight, legendText = "light jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_cJets", MCInput, "{0} && offCleanJets_hadronFlavour[?] == 4".format(eventSelection), 831.76, datalumi, ROOT.kGreen+2, 9767140, weight = puweight, legendText = "c jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_bJets", MCInput, "{0} && offCleanJets_hadronFlavour[?] == 5".format(eventSelection), 831.76, datalumi, ROOT.kRed, 9767140, weight = puweight, legendText = "b jets (t#bar{t})") )


    if doData:
        eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
        dataSample = modules.classes.Sample("data", DataInput, eventSelection, color= ROOT.kBlue, legendText = "Data")
    else:
        dataSample = None

    if plotinclusive:
        logging.info("Making inclusive stack plots")
        if doCSV:
            CSVOffline = modules.classes.PlotBase("offCleanJets_csv", offlineSelection, "1", [20,0,1], "Offline jet csv value")
            CSVOfflineIter = modules.classes.PlotBase("offCleanJets_csv", "1", "1", [20,0,1], "Offline jet csv value")
            CSVPF = modules.classes.PlotBase("pfJets_csv[offCleanJets_matchPF]", "{0} && {1}".format(offlineSelection, "1"), "1", [20,0,1], "PF jet csv value")
            CSVPFIter = modules.classes.PlotBase("offCleanJets_csv", "1", "1", [20,0,1], "PF jet csv value")
            CSVCaloIter = modules.classes.PlotBase("offCleanJets_csv", "1", "1", [20,0,1], "Calo jet csv value")
            #modules.DataMC.makeStackDMCPlot(CSVOffline, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_csv", normalized = True)
            #modules.DataMC.makeStackDMCPlot(CSVPF, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVOfflineIter, MCsamplesIter,  "offCleanJets_csv[?]", 15, offlineSelectionIter, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVPFIter, MCsamplesIter,  "pfJets_csv[offCleanJets_matchPF[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offCleanJets_matchPF[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_inclusive_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVCaloIter, MCsamplesIter,  "caloJets_csv[offCleanJets_matchCalo[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offCleanJets_matchCalo[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_calo_inclusive_csv", normalized = True)
        if doDeepCSV:
            DeepCSVOfflineIter = modules.classes.PlotBase("offCleanJets_deepcsv", "1", "1", [20,0,1], "Offline jet DeepCSV value")
            DeepCSVPFIter = modules.classes.PlotBase("offCleanJets_deepcsv", "1", "1", [20,0,1], "PF jet DeepCSV value")
            DeepCSVCaloIter = modules.classes.PlotBase("offCleanJets_deepcsv", "1", "1", [20,0,1], "Calo jet DeepCSV value")
            #modules.DataMC.makeStackDMCPlot(CSVOffline, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_csv", normalized = True)
            #modules.DataMC.makeStackDMCPlot(CSVPF, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVOfflineIter, MCsamplesIter,  "offCleanJets_deepcsv[?]", 15, offlineSelectionIter, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(DeepCSVPFIter, MCsamplesIter,  "pfJets_deepcsv[offCleanJets_matchPF[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offCleanJets_matchPF[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_inclusive_deepcsv", normalized = True)
            modules.DataMC.makeSumDMCPlot(DeepCSVCaloIter, MCsamplesIter,  "caloJets_deepcsv[offCleanJets_matchCalo[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offCleanJets_matchCalo[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_calo_inclusive_deepcsv", normalized = True)

    ##############################################################################################################
    ##############################################################################################################
    ########################################### Tag&Probe plots ##################################################
    ##############################################################################################################
    ##############################################################################################################
            

    if plotTagAndProbe:
        lepoverfix = False
        logging.info("Making Tag&Probe plots")
        probeSel = offlineSelectionIter
        if doCSV:
            logging.info("Processing CSV plots")
            OffCSVnthJet = modules.classes.PlotBase("offCleanJets_csv[?]", "1", "1", [20,0,1], "Probe offline jet CSV value")
            PFCSVnthJet = modules.classes.PlotBase("pfJets_csv[offCleanJets_matchPF[?]]", "1", "1", [20,0,1], "PF jet matched to probe CSV value")
            CaloCSVnthJet = modules.classes.PlotBase("caloJets_csv[offCleanJets_matchCalo[?]]", "1", "1", [20,0,1], "Calo jet matched to probe CSV value")


            #tagSel = "{0} && {1}".format(offlineSelectionIter, "offCleanJets_csv[?] >= {0}".format(TagWPCSV))
            tagSel = "{0} && {1}".format(offlineSelectionIter, "offCleanJets_deepcsv[?] >= {0}".format(TagWPDeepCSV))
            WPlabel = getLabel("Tag DeepCSV WP: {0}".format(TagWPDeepCSV),  styleconfig.getfloat("CMSLabel","xStart"), pos = "topSup", scale = 0.8)
            #tagSel = "1"
            if calcEfficiency:
                logging.info("Calculating PF Efficiency")
                if not test:
                    pfCSVWPs = [0.405, 0.840, 0.975]
                else:
                    logging.warning("Test flag set! Only using one WP")
                    pfCSVWPs = [0.840]
                if not lepoverfix:
                    modules.TagNProbe.getBEfficiency(PFCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel,
                                                     "pfJets_csv[offCleanJets_matchPF[?]]", pfCSVWPs, 2, data = dataSample, normalized = True,
                                                     outname = basepath+"PFCSV/"+globalPrefix+"_TnP_leading_pf_csv", label = [WPlabel])
                else:
                    logging.info("Plotting with tmp. lepton overlap removal")
                    modules.TagNProbe.getBEfficiencyHack(PFCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel,
                                                             "pfJets_csv[offCleanJets_matchPF[?]]", pfCSVWPs, 2, lepveto, probeIndices = [0,1,2],
                                                             tagIndices = [[1,2,3],[2,3,4],[3]], data = dataSample, normalized = True,
                                                             outname = basepath+"PFCSV/"+globalPrefix+"_TnP_leading_pf_csv", label = [WPlabel])
                    


                

                if not test:
                    logging.info("Calculating Calo Efficiency")
                    if not lepoverfix:
                        modules.TagNProbe.getBEfficiency(CaloCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel,
                                                         "caloJets_csv[offCleanJets_matchCalo[?]]", [0.435, 0.840, 0.97], 2, data = dataSample, normalized = True,
                                                         outname = basepath+"CaloCSV/"+globalPrefix+"_TnP_leading_calo_csv", label = [WPlabel])
                    else:
                        logging.info("Plotting with tmp. lepton overlap removal")
                        modules.TagNProbe.getBEfficiencyHack(CaloCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel,
                                                             "caloJets_csv[offCleanJets_matchCalo[?]]", [0.435, 0.840, 0.97], 2, lepveto, probeIndices = [0,1,2],
                                                             tagIndices = [[1,2,3],[2,3],[3]], data = dataSample, normalized = True,
                                                             outname = basepath+"CaloCSV/"+globalPrefix+"_TnP_leading_calo_csv", label = [WPlabel])
                else:
                    logging.warning("Test flag set! Skipping calo efficiancy")
                
            else:
                modules.TagNProbe.LeadingProbe(OffCSVnthJet, MCsamplesIter, probeSel, tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leadingoff_csv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(PFCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_pf_csv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(CaloCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_calo_csv", normalized = True, label = [WPlabel])
        if doDeepCSV:
            logging.info("Processing DeepCSV plots")
            WPlabel = getLabel("Tag DeepCSV WP: {0}".format(TagWPDeepCSV),  styleconfig.getfloat("CMSLabel","xStart"), pos = "topSup", scale = 0.8)
            OffDeepCSVnthJet = modules.classes.PlotBase("offCleanJets_deepcsv[?]", "1", "1", [20,0,1], "Probe offline jet DeepCSV value")
            PFDeepCSVnthJet = modules.classes.PlotBase("pfJets_deepcsv[offCleanJets_matchPF[?]] + pfJets_deepcsv_bb[offCleanJets_matchPF[?]]", "1", "1", [20,0,1], "PF jet matched to probe DeepCSV value")
            CaloDeepCSVnthJet = modules.classes.PlotBase("caloJets_deepcsv[offCleanJets_matchCalo[?]] + caloJets_deepcsv_bb[offCleanJets_matchCalo[?]]", "1", "1", [20,0,1], "Calo jet matched to probe DeepCSV value")


            tagSel = "{0} && {1}".format(offlineSelectionIter, "offCleanJets_deepcsv[?] >= {0}".format(TagWPDeepCSV))
            #tagSel = "1"
            if calcEfficiency:
                logging.info("Calculating PF Efficiency")
                if not lepoverfix:
                    modules.TagNProbe.getBEfficiency(PFDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel,
                                                     "pfJets_deepcsv[offCleanJets_matchPF[?]] + pfJets_deepcsv_bb[offCleanJets_matchPF[?]]", [0.2, 0.67, 0.955], 2, data = dataSample, normalized = True,
                                                     outname = basepath+"PFDeepCSV/"+globalPrefix+"_TnP_leading_pf_deepcsv", label = [WPlabel])
                else:
                    modules.TagNProbe.getBEfficiencyHack(PFDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel,
                                                         "pfJets_deepcsv[offCleanJets_matchPF[?]] + pfJets_deepcsv_bb[offCleanJets_matchPF[?]]", [0.2, 0.67, 0.955], 2, lepveto, probeIndices = [0,1,2],
                                                         tagIndices = [[1,2,3],[2,3],[3]], data = dataSample, normalized = True,
                                                         outname = basepath+"PFDeepCSV/"+globalPrefix+"_TnP_leading_pf_deepcsv", label = [WPlabel])
                logging.info("Calculating Calo Efficiency")
                if not lepoverfix:
                    modules.TagNProbe.getBEfficiency(CaloDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel,
                                                     "caloJets_deepcsv[offCleanJets_matchCalo[?]] + caloJets_deepcsv_bb[offCleanJets_matchCalo[?]]", [0.205, 0.675, 0.95], 2, data = dataSample, normalized = True,
                                                     outname = basepath+"CaloDeepCSV/"+globalPrefix+"_TnP_leading_calo_deepcsv", label = [WPlabel])
                else:
                    modules.TagNProbe.getBEfficiencyHack(CaloDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel,
                                                         "caloJets_deepcsv[offCleanJets_matchCalo[?]] + caloJets_deepcsv_bb[offCleanJets_matchCalo[?]]", [0.205, 0.675, 0.95], 2, lepveto, probeIndices = [0,1,2],
                                                         tagIndices = [[1,2,3],[2,3],[3]] , data = dataSample, normalized = True,
                                                         outname = basepath+"CaloDeepCSV/"+globalPrefix+"_TnP_leading_calo_deepcsv", label = [WPlabel])
            else:
                modules.TagNProbe.LeadingProbe(OffDeepCSVnthJet, MCsamplesIter, probeSel, tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leadingoff_deepcsv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(PFDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchPF[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_pf_deepcsv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(CaloDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offCleanJets_matchCalo[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_calo_deepcsv", normalized = True, label = [WPlabel])
            

    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################

    logger.info("Runtime: {0:8f}s".format(time.time()-t0))
    logger.info("Closing falvour compostion analysis")


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
        help = "Define logging level: CRITICAL - 50, ERROR - 40, WARNING - 30, INFO - 20, DEBUG - 10, SUBDEBUG - 5,  NOTSET - 0 \nSet to 0 to activate ROOT root messages",
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
        "--data",
        action = "store_true",
        help = "Enable Data. Without this flag the sum of MC will be used as data. \n Call without argument!",
    )
    argumentparser.add_argument(
        "--csv",
        action = "store_true",
        help = "Enable CSV. Call without argument!",
     )
    argumentparser.add_argument(
        "--deepcsv",
        action = "store_true",
        help = "Enable DeepCSV. Call without argument!",
    )    
    argumentparser.add_argument(
        "--inclusive",
        action = "store_true",
        help = "Enable plotting of inclusive flavour split distributions for enabled taggers. Call without argument!",
    )
    argumentparser.add_argument(
        "--TnP",
        action = "store_true",
        help = "Enable Plotting with Tag&Probe method. Call without argument!",
    )
    argumentparser.add_argument(
        "--eff",
        action = "store_true",
        help = "Enable efficiency measurement with Tag&Probe method. Call this w/ --TnP for standard measurement! Call without argument!",
    )
    argumentparser.add_argument(
        "--test",
        action = "store_true",
        help = "With this flag set, calo plots/measruements will be skipped. Only works with --csv. Call without argument!",
    )


    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################

        
    flavourComposition(loglev = args.logging, run = args.run, doData = args.data, doCSV = args.csv, doDeepCSV = args.deepcsv, plotinclusive = args.inclusive, plotTagAndProbe = args.TnP, calcEfficiency = args.eff, test = args.test)

    logging.info("Exiting flavourComp.py")
