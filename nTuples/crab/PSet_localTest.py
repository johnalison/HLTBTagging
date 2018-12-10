import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")



# for testing missing HE sectors 
#process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('/store/relval/CMSSW_10_1_7/MuonEG/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_muEG2018B-v1/10000/44F4B3A0-3080-E811-8D3C-0CC47A4D762A.root'),
    #lumisToProcess = cms.untracked.VLuminosityBlockRange("317435:83-317435:83"),
    #secondaryFileNames = cms.untracked.vstring('/store/relval/CMSSW_10_1_7/MuonEG/FEVTDEBUGHLT/101X_dataRun2_HLT_HEmiss_v1_RelVal_muEG2018B-v1/10000/00538A51-D57F-E811-B85D-0025905B8606.root')
#)


## Working (johnda)
## for testing data without missing HE sectors
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/relval/CMSSW_10_1_7/MuonEG/MINIAOD/101X_dataRun2_Prompt_v11_RelVal_muEG2018B-v1/10000/4C2407F3-2580-E811-B9CB-0CC47A4D7614.root'),
#    lumisToProcess = cms.untracked.VLuminosityBlockRange("317435:2-317435:2"),
#    secondaryFileNames = cms.untracked.vstring('/store/relval/CMSSW_10_1_7/MuonEG/FEVTDEBUGHLT/101X_dataRun2_HLT_v7_RelVal_muEG2018B-v1/10000/008175B3-E67F-E811-9432-0025905AA9CC.root')
#)
#
#John 

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/mc/RunIIFall17DRPremix/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/AODSIM/TSG_94X_mc2017_realistic_v11-v1/70000/4EAA44A8-4F22-E811-8E2F-7CD30AD0A750.root'),
#    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:8695-1:8695"),
#    secondaryFileNames = cms.untracked.vstring('/store/mc/RunIIFall17DRPremix/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/TSG_94X_mc2017_realistic_v11-v1/30000/0416D117-B31E-E811-848B-3417EBE64CDB.root')
#)

#process.source = cms.Source("PoolSource",
#                            fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/70000/F065E54E-4622-E811-B1F8-008CFAFBE0DC.root'),
#                            lumisToProcess = cms.untracked.VLuminosityBlockRange("1:9225-1:9225"),
#                            secondaryFileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIIFall17DRPremix/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/TSG_94X_mc2017_realistic_v11-v1/30000/5A055FAF-B61E-E811-B1EA-3417EBE2F0C7.root'),
#                            )

## MC working
#process.source = cms.Source("PoolSource", 
#                            fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/70000/F065E54E-4622-E811-B1F8-008CFAFBE0DC.root'),
#                            lumisToProcess = cms.untracked.VLuminosityBlockRange("1:9225-1:9225"),
#                            secondaryFileNames = cms.untracked.vstring('/store/mc/RunIIFall17DRPremix/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/TSG_94X_mc2017_realistic_v11-v1/30000/5A055FAF-B61E-E811-B1EA-3417EBE2F0C7.root'),
#                            )


# 2018 Testing
process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring("root://cms-xrd-global.cern.ch//store/data/Run2018A/MuonEG/MINIAOD/PromptReco-v3/000/316/995/00000/6468B1E5-E166-E811-AC29-FA163EC1F063.root"),
                            lumisToProcess = cms.untracked.VLuminosityBlockRange("316995:327-316995:335"),
                            secondaryFileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2018A/MuonEG/RAW/v1/000/316/995/00000/FABFDCF7-E564-E811-A498-FA163EC31020.root'),
                            )




#process.source = cms.Source("PoolSource",
#                            fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/70000/F065E54E-4622-E811-B1F8-008CFAFBE0DC.root'),
#                            lumisToProcess = cms.untracked.VLuminosityBlockRange("1:9225-1:9225"),
#                            secondaryFileNames = cms.untracked.vstring('/store/relval/CMSSW_9_4_0/RelValProdTTbar_13/GEN-SIM-RAW/94X_mcRun2_asymptotic_v0-v1/10000/2C420C43-B8C8-E711-808F-0CC47A4D76A0.root '),
#                            )



##MC
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/C0D716E7-88A2-E711-A108-FA163EB5E2DE.root'),
#    #lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:2-300107:3"),
#    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:14344-1:14344"),
#    secondaryFileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/FEDCCD34-BFA1-E711-93DE-FA163E3ECCF5.root')
#)

#### for testing data run D:
###process.source = cms.Source("PoolSource",
###    fileNames = cms.untracked.vstring('/store/data/Run2018D/MuonEG/MINIAOD/PromptReco-v2/000/321/012/00000/70494CF3-F79C-E811-A87E-FA163EED9E90.root'),
###    lumisToProcess = cms.untracked.VLuminosityBlockRange("321012:1-321012:31"),
###    secondaryFileNames = cms.untracked.vstring('/store/data/Run2018D/MuonEG/MINIAOD/PromptReco-v2/000/321/012/00000/70494CF3-F79C-E811-A87E-FA163EED9E90.root')
###)


#MC
#process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/C0D716E7-88A2-E711-A108-FA163EB5E2DE.root'),
    ##lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:2-300107:3"),
    #lumisToProcess = cms.untracked.VLuminosityBlockRange("1:14344-1:14344"),
    #secondaryFileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/FEDCCD34-BFA1-E711-93DE-FA163E3ECCF5.root')
#)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

process.options = cms.PSet(
    numberOfThreads = cms.untracked.uint32(4)
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root')
)


process.out = cms.EndPath(process.output)

