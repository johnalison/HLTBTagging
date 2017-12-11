import os
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel
from ConfigParser import SafeConfigParser

def flavourComposition(loglev, doData, doCSV, doDeepCSV, plotinclusive, plotTagAndProbe, calcEfficiency, TagWPCSV = 0.8484, TagWPDeepCSV = 0.8958):
    import ROOT

    import modules.classes
    import modules.DataMC
    import modules.TagNProbe

    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")
    
    setup_logging(loglevel = loglev, logname = "shapeoutput", errname = "shapeerror")

    logger = logging.getLogger(__name__)

    logger.info("Starting flavour composition analysis")

    
    if not (doCSV or doDeepCSV):
        if __name__ == "__main__":
            logging.warning("At least on of the flags --CSV and --deepCSV should to be set")
        else:
            logging.warning("At least on of the paramters doCSV and doDeepCSV should to be set")
        logging.warning("Falling back the only CSV")
        doCSV = True

    ##############################################################################################################
    ############################################## Plotting Code #################################################
    ##############################################################################################################

    if loglev > 0:
        ROOT.gErrorIgnoreLevel = ROOT.kError# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
    
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/ttbar/phase1/ttbar_v1.root"
    #Run C-D
    DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/MuonEG_RunCD_phase1_part.root"
    puweight = "get_puWeight(pu)"
    globalPrefix = "DeepCSVMPresel_phase1_RunCD"
    basepath = "v5nTuples/FlavourSplitting/RunCD/" 
    
    #Run F
    #DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/RunF/phase1/MuonEG_RunF_phase1_part.root"
    #puweight = "wPURunF"
    #globalPrefix = "DeepCSVMPresel_phase1_RunF"
    #basepath = "v5nTuples/FlavourSplitting/RunF/" 
    
    #Run E
    #DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/RunE/phase1/MuonEG_RunE_phase1.root"
    #puweight = "wPURunE"
    #globalPrefix = "DeepCSVMPresel_phase1_RunE"
    #basepath = "v5nTuples/FlavourSplitting/RunE/" 

    
    #MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/ttbar/ttbar_v1.root"
    #DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/MuonEG_RunCD_part.root"


    

    
    MCSelection = "1"
    DataSelection = "1"
    VarSelection = "Sum$(offJets_deepcsv > 0.8958 && offJets_pt > 30 && abs(offJets_eta) < 2.4) >= 1 && Sum$(offJets_pt > 30 && abs(offJets_eta) < 2.4) >= 2"
    TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
    LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) > 0 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) > 0"

    offlineSelection = "abs(offJets_eta) < 2.4 && offJets_pt > 30 && offJets_passesTightLeptVetoID > 0"
    offlineSelectionIter = "abs(offJets_eta[?]) < 2.4 && offJets_pt[?] > 30 && offJets_passesTightLeptVetoID[?] > 0"

    MCsamples = []
    MCsamplesIter = []

    datalumi = 4591.622871124
    
    eventSelection = "({0}) && ({1}) && ({2}) && ({3})".format(VarSelection, TriggerSelection, LeptonSelection, MCSelection)
    MCsamples.append( modules.classes.Sample("ttbar_unmatchedJets", MCInput, "{0} && (  abs(offJets_mcFlavour[?]) != 21 && abs(offJets_mcFlavour[?]) > 5 )".format(eventSelection), 831.76, datalumi, ROOT.kWhite, 9767140, weight = puweight, legendText = "unmatched jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_udsgJets", MCInput, "{0} && ( abs(offJets_mcFlavour) == 21 || abs(offJets_mcFlavour) < 4)".format(eventSelection), 831.76, datalumi, ROOT.kBlue, 9767140, weight = puweight, legendText = "udsg jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_cJets", MCInput, "{0} && abs(offJets_mcFlavour) == 4".format(eventSelection), 831.76, datalumi, ROOT.kGreen+2, 9767140, weight = puweight, legendText = "c jets (t#bar{t})") )
    MCsamples.append( modules.classes.Sample("ttbar_bJets", MCInput, "{0} && abs(offJets_mcFlavour) == 5".format(eventSelection), 831.76, datalumi, ROOT.kRed, 9767140, weight = puweight, legendText = "b jets (t#bar{t})") )

    MCsamplesIter.append( modules.classes.Sample("ttbar_unmatchedJets", MCInput, "{0} && ( abs(offJets_mcFlavour[?]) != 21 && abs(offJets_mcFlavour[?]) > 5 )".format(eventSelection), 831.76, datalumi, ROOT.kWhite, 9767140, weight = puweight, legendText = "unmatched jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_udsgJets", MCInput, "{0} && ( abs(offJets_mcFlavour[?]) == 21 || abs(offJets_mcFlavour[?]) < 4)".format(eventSelection), 831.76, datalumi, ROOT.kBlue, 9767140, weight = puweight, legendText = "udsg jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_cJets", MCInput, "{0} && abs(offJets_mcFlavour[?]) == 4".format(eventSelection), 831.76, datalumi, ROOT.kGreen+2, 9767140, weight = puweight, legendText = "c jets (t#bar{t})") )
    MCsamplesIter.append( modules.classes.Sample("ttbar_bJets", MCInput, "{0} && abs(offJets_mcFlavour[?]) == 5".format(eventSelection), 831.76, datalumi, ROOT.kRed, 9767140, weight = puweight, legendText = "b jets (t#bar{t})") )


    if doData:
        eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
        dataSample = modules.classes.Sample("data", DataInput, eventSelection, color= ROOT.kBlue, legendText = "MuonEG")
    else:
        dataSample = None

    if plotinclusive:
        logging.info("Making inclusive stack plots")
        if doCSV:
            CSVOffline = modules.classes.PlotBase("offJets_csv", offlineSelection, "1", [20,0,1], "Offline jet csv value")
            CSVOfflineIter = modules.classes.PlotBase("offJets_csv", "1", "1", [20,0,1], "Offline jet csv value")
            CSVPF = modules.classes.PlotBase("pfJets_csv[offJets_matchPF]", "{0} && {1}".format(offlineSelection, "1"), "1", [20,0,1], "PF jet csv value")
            CSVPFIter = modules.classes.PlotBase("offJets_csv", "1", "1", [20,0,1], "PF jet csv value")
            CSVCaloIter = modules.classes.PlotBase("offJets_csv", "1", "1", [20,0,1], "Calo jet csv value")
            #modules.DataMC.makeStackDMCPlot(CSVOffline, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_csv", normalized = True)
            #modules.DataMC.makeStackDMCPlot(CSVPF, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVOfflineIter, MCsamplesIter,  "offJets_csv[?]", 15, offlineSelectionIter, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVPFIter, MCsamplesIter,  "pfJets_csv[offJets_matchPF[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offJets_matchPF[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVCaloIter, MCsamplesIter,  "caloJets_csv[offJets_matchCalo[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offJets_matchCalo[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_calo_sum_csv", normalized = True)
        if doDeepCSV:
            CSVOfflineIter = modules.classes.PlotBase("offJets_deepcsv", "1", "1", [20,0,1], "Offline jet DeepCSV value")
            CSVPFIter = modules.classes.PlotBase("offJets_deepcsv", "1", "1", [20,0,1], "PF jet DeepCSV value")
            CSVCaloIter = modules.classes.PlotBase("offJets_deepcsv", "1", "1", [20,0,1], "Calo jet DeepCSV value")
            #modules.DataMC.makeStackDMCPlot(CSVOffline, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_csv", normalized = True)
            #modules.DataMC.makeStackDMCPlot(CSVPF, MCsamples, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVOfflineIter, MCsamplesIter,  "offJets_csv[?]", 15, offlineSelectionIter, dataSample, drawRatio = True, outname = basepath+globalPrefix+"_off_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVPFIter, MCsamplesIter,  "pfJets_csv[offJets_matchPF[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offJets_matchPF[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_pf_sum_csv", normalized = True)
            modules.DataMC.makeSumDMCPlot(CSVCaloIter, MCsamplesIter,  "caloJets_csv[offJets_matchCalo[?]]", 15, "{0} && {1}".format(offlineSelectionIter, "offJets_matchCalo[?] >= 0"), dataSample, drawRatio = True, outname = basepath+globalPrefix+"_calo_sum_csv", normalized = True)

    ##############################################################################################################
    ##############################################################################################################
    ########################################### Tag&Probe plots ##################################################
    ##############################################################################################################
    ##############################################################################################################
            

    if plotTagAndProbe:
        logging.info("Making Tag&Probe plots")
        probeSel = offlineSelectionIter
        if doCSV:

            logging.info("Processing CSV plots")
            OffCSVnthJet = modules.classes.PlotBase("offJets_csv[?]", "1", "1", [20,0,1], "Probe offline jet CSV value")
            PFCSVnthJet = modules.classes.PlotBase("pfJets_csv[offJets_matchPF[?]]", "1", "1", [20,0,1], "PF jet matched to probe CSV value")
            CaloCSVnthJet = modules.classes.PlotBase("caloJets_csv[offJets_matchCalo[?]]", "1", "1", [20,0,1], "Calo jet matched to probe CSV value")


            #tagSel = "{0} && {1}".format(offlineSelectionIter, "offJets_csv[?] >= {0}".format(TagWPCSV))
            tagSel = "{0} && {1}".format(offlineSelectionIter, "offJets_deepcsv[?] >= {0}".format(TagWPDeepCSV))
            WPlabel = getLabel("Tag DeepCSV WP: {0}".format(TagWPDeepCSV),  styleconfig.getfloat("CMSLabel","xStart"), pos = "topSup", scale = 0.8)
            #tagSel = "1"
            if calcEfficiency:
                logging.info("Calculating PF Efficiency")
                modules.TagNProbe.getBEfficiency(PFCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchPF[?] >= 0"), tagSel,
                                                 "pfJets_csv[offJets_matchPF[?]]", [0.405, 0.840, 0.975], 3, data = dataSample, normalized = True,
                                                 outname = basepath+"PFCSV/"+globalPrefix+"_TnP_leading_pf_csv", label = [WPlabel])
                logging.info("Calculating Calo Efficiency")
                modules.TagNProbe.getBEfficiency(CaloCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchCalo[?] >= 0"), tagSel,
                                                 "caloJets_csv[offJets_matchCalo[?]]", [0.435, 0.840, 0.97], 3, data = dataSample, normalized = True,
                                                 outname = basepath+"CaloCSV/"+globalPrefix+"_TnP_leading_calo_csv", label = [WPlabel])
            else:
                modules.TagNProbe.LeadingProbe(OffCSVnthJet, MCsamplesIter, probeSel, tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leadingoff_csv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(PFCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchPF[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_pf_csv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(CaloCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchCalo[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_calo_csv", normalized = True, label = [WPlabel])
        if doDeepCSV:
            logging.info("Processing DeepCSV plots")
            WPlabel = getLabel("Tag DeepCSV WP: {0}".format(TagWPDeepCSV),  styleconfig.getfloat("CMSLabel","xStart"), pos = "topSup", scale = 0.8)
            OffDeepCSVnthJet = modules.classes.PlotBase("offJets_deepcsv[?]", "1", "1", [20,0,1], "Probe offline jet DeepCSV value")
            PFDeepCSVnthJet = modules.classes.PlotBase("pfJets_deepcsv[offJets_matchPF[?]]", "1", "1", [20,0,1], "PF jet matched to probe DeepCSV value")
            CaloDeepCSVnthJet = modules.classes.PlotBase("caloJets_deepcsv[offJets_matchCalo[?]]", "1", "1", [20,0,1], "Calo jet matched to probe DeepCSV value")


            tagSel = "{0} && {1}".format(offlineSelectionIter, "offJets_deepcsv[?] >= {0}".format(TagWPDeepCSV))
            #tagSel = "1"
            if calcEfficiency:
                logging.info("Calculating PF Efficiency")
                modules.TagNProbe.getBEfficiency(PFDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchPF[?] >= 0"), tagSel,
                                                 "pfJets_deepcsv[offJets_matchPF[?]]", [0.2, 0.67, 0.955], 3, data = dataSample, normalized = True,
                                                 outname = basepath+"PFDeepCSV/"+globalPrefix+"_TnP_leading_pf_deepcsv", label = [WPlabel])
                logging.info("Calculating Calo Efficiency")
                modules.TagNProbe.getBEfficiency(CaloDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchCalo[?] >= 0"), tagSel,
                                                 "caloJets_deepcsv[offJets_matchCalo[?]]", [0.205, 0.675, 0.95], 3, data = dataSample, normalized = True,
                                                 outname = basepath+"CaloDeepCSV/"+globalPrefix+"_TnP_leading_calo_deepcsv", label = [WPlabel])
            else:
                modules.TagNProbe.LeadingProbe(OffDeepCSVnthJet, MCsamplesIter, probeSel, tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leadingoff_deepcsv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(PFDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchPF[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_pf_deepcsv", normalized = True, label = [WPlabel])
                modules.TagNProbe.LeadingProbe(CaloDeepCSVnthJet, MCsamplesIter, "{0} && {1}".format(probeSel, "offJets_matchCalo[?] >= 0"), tagSel, data = dataSample, convertIterSelection = True,
                                               outname = basepath+globalPrefix+"_TnP_leading_calo_deepcsv", normalized = True, label = [WPlabel])
            

    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################

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
        help = "Define logging level: CRITICAL - 50, ERROR - 40, WARNING - 30, INFO - 20, DEBUG - 10, NOTSET - 0 \nSet to 0 to activate ROOT root messages",
        type=int,
        default=20
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
        "--inclusive",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--TnP",
        action = "store_true",
        help = "Call without argument!",
    )
    argumentparser.add_argument(
        "--eff",
        action = "store_true",
        help = "Call without argument!",
    )


    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################

        
    flavourComposition(loglev = args.logging, doData = args.data, doCSV = args.csv, doDeepCSV = args.deepcsv, plotinclusive = args.inclusive, plotTagAndProbe = args.TnP, calcEfficiency = args.eff)

    logging.info("Exiting flavourComp.py")
