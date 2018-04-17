import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
#    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
#)



process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_MiniAOD_ReReco_300107_221A60AF-A1EC-E711-9510-A4BF011259A8.root'),
    #lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:2-300107:3"),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(),
    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_RAW_300107_96AFE9F4-6974-E711-80D3-02163E01A3CB.root')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.PSet(
    numberOfThreads = cms.untracked.uint32(4)
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root')
)


process.out = cms.EndPath(process.output)

