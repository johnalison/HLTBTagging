import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root'),
#    secondaryFileNames = cms.untracked.vstring('file:/afs/cern.ch/user/k/koschwei/work/public/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root')
#)


"""
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/mnt/t3nfs01/data01/shome/koschwei/scratch/MuonEGRunC_MiniAODv2_ReReco_300107_4AABB4B6-5037-E811-9F4A-0CC47A5FBE35.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:1-300107:1"),
    secondaryFileNames = cms.untracked.vstring('file:/mnt/t3nfs01/data01/shome/koschwei/scratch/MuonEGRunC_RAW_300107_348E3CF3-6974-E711-80DE-02163E01A5DC.root')
)
"""

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/30000/AEA25818-FB21-E811-BBFB-848F69FD444B.root'),
    #lumisToProcess = cms.untracked.VLuminosityBlockRange("300107:2-300107:3"),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:261-1:261"),
    secondaryFileNames = cms.untracked.vstring('/store/mc/RunIIFall17DRPremix/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/TSG_94X_mc2017_realistic_v11-v1/30000/14E63E79-041E-E811-A72A-3417EBE5289A.root')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

process.options = cms.PSet(
    numberOfThreads = cms.untracked.uint32(4)
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root')
)


process.out = cms.EndPath(process.output)

