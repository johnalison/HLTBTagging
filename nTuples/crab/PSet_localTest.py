import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
#    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
#)



process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_AODSIM_LS-1803to1803-2134to2134-2332to2332-2870to2871-4384to4385-6032to6033-6481to6481.root'),
    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_GEN-SIM-RAW_LS-1803to1803-2332to2332-2870to2871.root')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.options = cms.PSet(
    numberOfThreads = cms.untracked.uint32(4)
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root')
)


process.out = cms.EndPath(process.output)

