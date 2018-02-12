#!/usr/bin/python
"""ntuplizerHLT 
Original Code by S. Donato - https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8

Code for making nTuples with offline variables (from AOD) and HLT objects (Rerun on RAW) using the heppy framework
"""
import ROOT
import itertools
import resource
import time
from array import array
from math import sqrt, pi, log10, log, exp
# load FWlite python libraries
from DataFormats.FWLite import Handle, Events
from utils import deltaR,SetVariable,DummyClass,productWithCheck,checkTriggerIndex


def launchNtupleFromHLT(fileOutput,filesInput, secondaryFiles, maxEvents,preProcessing=True, firstEvent=0, MC = False):
    t0 = time.time()
    bunchCrossing   = 12
    print "filesInput: ",filesInput
    print "fileOutput: ",fileOutput
    print "secondaryFiles: ",secondaryFiles
    print "maxEvents: ",maxEvents
    print "preProcessing: ",preProcessing
    print "firstEvent: ",firstEvent
        
    dataflags = ["MuonEG"] #NOTE: Add more flags if different data datasets are considered
        
    #isMC = bool(MC)

    if len(filesInput)>0 and (len(filter(lambda x: x in filesInput[0], dataflags)) >= 1):
        print "filesinput[0] has at least on of {0}".format(dataflags)
        isMC = False
        Signal = False
    else:
        isMC = True
        Signal = False

    print "isMC = {0}".format(isMC)

    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    from PhysicsTools.HeppyCore.framework.config import MCComponent    
    ## Pre-processing
    if preProcessing:


        if not isMC:
            cmsRun_config = "hlt_dump.py"
        else:
            cmsRun_config = "hlt_dump_mc.py"
        print "Using: {0}".format(cmsRun_config)
        preprocessor = CmsswPreprocessor(cmsRun_config)
        cfg = MCComponent("OutputHLT",filesInput, secondaryfiles=secondaryFiles)
        print "Run cmsswPreProcessing using:"
        print cfg.name
        print cfg.files
        print cfg.secondaryfiles
        print
        try:
            preprocessor.run(cfg,".",firstEvent,maxEvents)
        except:
            print "cmsswPreProcessing failed!"
            print "cat cmsRun_config.py"
            config = file(cmsRun_config)
            print config.read()
            print "cat cmsRun.log"
            log = file("cmsRun.log")
            print log.read()
            preprocessor.run(cfg,".",firstEvent,maxEvents)
            raise Exception("CMSSW preprocessor failed!")

    print "Time to preprocess: {0:10f} s".format(time.time()-t0)
    import os
    import imp
    dir_ = os.getcwd()
    print dir_
    print "Filesize of {0:8f} MB".format(os.path.getsize(dir_+"/cmsswPreProcessing.root") * 1e-6)
    t1 = time.time()
    deepCofig = "ConfFile_cfg.py"
    #cfgDeep = MCComponent("OutputDeepCSV",["file:"+dir_+"/cmsswPreProcessing.root"])
    #preprocessorDeep = CmsswPreprocessor(deepCofig)
    #preprocessorDeep.run(cfgDeep,".",firstEvent,maxEvents)



    cmsswConfig = imp.load_source("cmsRunProcess",os.path.expandvars(deepCofig))
    cmsswConfig.process.source.fileNames = ["file:"+dir_+"/cmsswPreProcessing.root"]
    cmsswConfig.process.TFileService.fileName = fileOutput

    configfile=dir_+"/mod_deepConf.py"
    f = open(configfile, 'w')
    f.write(cmsswConfig.process.dumpPython())
    f.close()

    #runstring="%s %s >& %s/cmsRun_Deepntuple.log" % ("cmsRun",configfile,dir_)
    runstring="{0} {1} >& {2}/cmsRun_Deepntuple.log".format("cmsRun",configfile, dir_)
    print "Running pre-processor: %s " %runstring
    ret=os.system(runstring)
    if ret != 0:
        print "CMSRUN failed"
        exit(ret)

    print "Time to deepNtuple {0:10f} s".format(time.time()-t1)
    print "Filesize of {0:8f} MB".format(os.path.getsize(dir_+"/"+fileOutput) * 1e-6)
    print "Total time: {0:10f} s".format(time.time()-t0)
        
if __name__ == "__main__":

    secondaryFiles = [
        "file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_RAW_300107_348E3CF3-6974-E711-80DE-02163E01A5DC.root",
        #"root://cms-xrd-global.cern.ch//store/data/Run2017E/MuonEG/RAW/v1/000/303/573/00000/C4D2E109-E69E-E711-B5D4-02163E019E5B.root",
        #"file:/afs/cern.ch/work/k/koschwei/public/RelValTTbar_13_GEN-SIM-DIGI-RAW-HLTDEBUG_LumiStarting1_EE64BF2D-7600-E811-90B8-0CC47A4D767E.root",
    ]
    filesInput = [
        "file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_AOD_300107_240EB136-3077-E711-A764-02163E01A500.root",
        #"root://cms-xrd-global.cern.ch//store/data/Run2017E/MuonEG/AOD/PromptReco-v1/000/303/573/00000/580460D1-79A0-E711-BCF8-02163E0143E8.root",
        #"file:/afs/cern.ch/work/k/koschwei/public/RelValTTbar_13_GEN-SIM-RECO_LumiStarting1_6A737BCB-9B00-E811-918C-0CC47A4D7638.root",
    ]
    
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17MiniAOD__92X_upgrade2017_MINIAOD_LS-starting2183.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_GEN-SIM-RAW_LS-1803to1803-2332to2332-2870to2871.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_GEN-SIM-RAW_LS-2183to2182.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/RelValTTbar_13_GEN-SIM-DIGI-RAW-HLTDEBUG_LumiStarting1_EE64BF2D-7600-E811-90B8-0CC47A4D767E.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_RAW_300107_348E3CF3-6974-E711-80DE-02163E01A5DC.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_GEN-SIM-RAW_LS-1803to1803-2332to2332-2870to2871.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_AODSIM_LS-1803to1803-2134to2134-2332to2332-2870to2871-4384to4385-6032to6033-6481to6481.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/RelValTTbar_13_GEN-SIM-RECO_LumiStarting1_6A737BCB-9B00-E811-918C-0CC47A4D7638.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_MiniAOD_300107_3E580A66-3477-E711-8027-02163E0142F6.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_MiniAOD_300107_3E580A66-3477-E711-8027-02163E0142F6.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17MiniAOD__92X_upgrade2017_MINIAOD_LS-starting2183.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root"]
    fileOutput = "tree_DeepnTuple_phase1.root"
    maxEvents = 10
    launchNtupleFromHLT(fileOutput,filesInput,secondaryFiles,maxEvents, preProcessing=True)

    
