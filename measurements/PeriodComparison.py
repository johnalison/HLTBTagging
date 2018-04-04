import os
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel
from ConfigParser import SafeConfigParser

def perioComparison(loglev, doCSV, doDeepCSV):
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
    
    DataInput = []
    DataInput.append(("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/MuonEG_RunCD_phase1_part.root", "Run C+D"))
    DataInput.append(("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/RunE/phase1/MuonEG_RunE_phase1.root", "Run E"))
    DataInput.append(("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v5/MuonEG/RunF/phase1/MuonEG_RunF_phase1_part.root", "Run F"))


    MCSelection = "1"
    DataSelection = "1"
    VarSelection = "Sum$(offJets_deepcsv > 0.8958 && offJets_pt > 30 && abs(offJets_eta) < 2.4) >= 1 && Sum$(offJets_pt > 30 && abs(offJets_eta) < 2.4) >= 2"
    TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
    LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) > 0 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) > 0"

    offlineSelection = "abs(offJets_eta) < 2.4 && offJets_pt > 30 && offJets_passesTightLeptVetoID > 0"
    offlineSelectionIter = "abs(offJets_eta[?]) < 2.4 && offJets_pt[?] > 30 && offJets_passesTightLeptVetoID[?] > 0"

    dataSample = []
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+2]
    iInput = 0
    eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
    for inputData, inputname in DataInput: 
        dataSample.append(modules.classes.Sample("data"+inputname.replace(" ","_"), DataInput, eventSelection, color= colors[iInput], legendText = "MuonEG "+inputname))
        iInput += 1

    if doCSV:
        pass
    if doDeepCSV:
        pass
        
    
    

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

        
    flavourComposition(loglev = args.logging, doCSV = args.csv, doDeepCSV = args.deepcsv)

    logging.info("Exiting flavourComp.py")
