import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
#    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
#)



process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring("file:/afs/cern.ch/work/k/koschwei/public/MuonEGRunC_AOD_300107_240EB136-3077-E711-A764-02163E01A500.root"),
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

