import os
import json
import logging
import logging.config
from modules.utils import setup_logging

def generalTest(loglev):
    import ROOT

    import modules.DataMC
    import modules.classes

    
    setup_logging(loglevel = loglev, logname = "testoutput", errname = "testerror")

    logger = logging.getLogger(__name__)

    logger.info("Starting general test")
    
    if args.logging > 0:
        ROOT.gErrorIgnoreLevel = ROOT.kError# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
    
    MCInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/ttbar/ttbar_v1_partial.root"
    DataInput = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v1/MuonEG/MuonEG_v1_partial.root"

    logging.info("Testing if files exist")
    for fpath in [MCInput, DataInput]:
        if os.path.exists(fpath):
            logging.info("File {0} exists".format(fpath.split("/")[-1]))
        else:
            logging.error("File {0} does NOT exist".format(fpath.split("/")[-1]))
    
    MCSample = modules.classes.Sample("ttbar", MCInput, "1", 831.76, 4591.622871124, ROOT.kRed, 9937324)
    DataSample = modules.classes.Sample("MuonEG", DataInput, color = ROOT.kBlack)

    logging.info("Testing samples")
    for sample in [MCSample, DataSample]:
        if sample.tree != 0:
            logging.info("Tree for sample {0} exists".format(sample.name))
            logging.info("Tree has {0} entries".format(sample.nEvents))
        else:
            error.info("Tree for sample {0} does NOT exist".format(sample.name))
            
    
    OffpT = modules.classes.PlotBase("offJets_pt", "offJets_pt > 30 && Sum$(offJets_csv > 0.6) >= 2", "1", [30,0,300], "Offline Jet p_{T}")
    OffpT.printVarLog()

    logging.info("Drawing basic DataMC plot w/o ratio")
    modules.DataMC.makeDataMCPlot(OffpT, DataSample, MCSample, normalized = True, outname = "Test_DataMC")

    logging.info("Drawing basic DataMC plot w/ ratio")
    modules.DataMC.makeDataMCPlotwRatio(OffpT, DataSample, MCSample, outname = "Test_DataMCwRatio")

    logging.info("Closing general test")
    
    
if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Main script for the HEPPlotster'
    )

    argumentparser.add_argument(
        "--logging",
        action = "store",
        help = "Define logging level: CRITICAL - 50, ERROR - 40, WARNING - 30, INFO - 20, DEBUG - 10, NOTSET - 0 \nSet to 0 to activate ROOT root messages",
        type=int,
        default=20
    )


    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################
    
    generalTest(loglev = args.logging)

    logging.info("Exiting test.py")
