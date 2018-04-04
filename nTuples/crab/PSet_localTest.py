import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
#    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
#)



process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_MiniAOD_300107_3E580A66-3477-E711-8027-02163E0142F6.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:2-300107:3"),
    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_RAW_300107_348E3CF3-6974-E711-80DE-02163E01A5DC.root')
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

