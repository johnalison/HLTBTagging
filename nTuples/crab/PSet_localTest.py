import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
)



#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/C4ACC891-4FA1-E711-BD6D-FA163E09A701.root'),
#    secondaryFileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/0E7B7DB0-0EA1-E711-B23E-02163E00C2C1.root')
#)


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

