import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")
process.load("Configuration.Geometry.GeometryECALHCAL_cff")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #"/store/data/Run2017D/MuonEG/MINIAOD/17Nov2017-v1/50000/10A7ED13-90EB-E711-8BE5-484D7E8DF114.root",
        "/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/30000/0C1673EB-FA21-E811-8A85-0CC47A2B0392.root"
    ),
    lumisToProcess = cms.untracked.VLuminosityBlockRange( ),
    inputCommands = cms.untracked.vstring('keep *')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.output = cms.OutputModule("PoolOutputModule",
                                  dataset = cms.untracked.PSet(),
                                  fileName = cms.untracked.string('./output.root'),
                                  outputCommands = cms.untracked.vstring('keep *')
)

process.FULLOutput = cms.EndPath(process.output)


from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,applyEnergyCorrections=False,
                       applyVIDOnCorrectedEgamma=False,
                       isMiniAOD=True)


process.p = cms.Path(process.egammaPostRecoSeq)

"""
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
process.p = cms.Path(process.egmGsfElectronIDSequence)
"""
