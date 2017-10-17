# nTupler
Creation of flat trees with HLT objects. For this the HLT has to be rerun on RAW. [Original Code](https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8)

## Usage
The following steps are necessary to produce the ntuples.
### HLT config
Creating of config dump for running the RAW+AOD files with HLT. The HLT tables and `--setup` depend on the usecase.
For Data:
```bash
hltGetConfiguration /users/koschwei/CMSSW_9_2_10/HLT_TnP_BTag \
 --setup /dev/CMSSW_9_2_0/HLT \
 --data --globaltag auto:run2_hlt_GRun \
 --input root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root  \
 --process MYHLT --full --offline   \
 --unprescale --max-events 10 --output none > hltData.py

edmConfigDump hltData.py > hlt_dump.py
```
For MC:
```bash
hltGetConfiguration /users/koschwei/CMSSW_9_2_10/HLT_TnP_BTag \
 --setup /dev/CMSSW_9_2_0/HLT \
 --mc --globaltag auto:run2_mc_GRun \
 --input root://cms-xrd-global.cern.ch//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/0E7B7DB0-0EA1-E711-B23E-02163E00C2C1.root  \
 --process MYHLT --full --offline   \
 --unprescale --max-events 10 --output none > hltMC.py

edmConfigDump hltMC.py > hlt_dump_mc.py
```

Remove:
```python
process.DQMOutput = cms.EndPath(process.dqmOutput)
```
Add the following to the end of the the config dumP:
```python

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
dataFormat = DataFormat.AOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
process.p = cms.Path(process.egmGsfElectronIDSequence)


process.hltOutputFULL = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
    ),
    fileName = cms.untracked.string('./cmsswPreProcessing.root'),
	outputCommands = cms.untracked.vstring('drop *',
                                           'keep *Egamma*_*_*_*',
                                           'keep bool*ValueMap*_*Electron*_*_*',
                                           'keep l1t*_*_*_*',
                                           'keep *_*Ht*_*_*',
                                           'keep *Jet*_*_*_*',
                                           'keep *Electron*_*_*_*',
                                           'keep *Muon*_*_*_*',
                                           'keep *Track*_*_*_*',
                                           'drop *Track*_hlt*_*_*',
                                           'drop SimTracks_*_*_*',
										   'keep *SuperCluster*_*_*_*',
                                           'keep *MET*_*_*_*',
                                           'keep *Vertex*_*_*_*',
                                           'keep *_genParticles_*_*',
                                           'keep *genParticles_*_*_*',
                                           'keep *Trigger*_*_*_*',
                                           'keep recoJetedmRefToBaseProdTofloatsAssociationVector_*_*_*',
                                           'keep *_addPileupInfo_*_*',
                                           'drop *_*Digis*_*_*',
                                           'drop triggerTriggerEvent_*_*_*',
                                           'keep *_hltGtStage2Digis_*_*',
                                           'keep *_generator_*_*')
)
process.FULLOutput = cms.EndPath(process.hltOutputFULL)
```


### Local test
Edit `crab/PSet_localTest.py`to fit your needs.
```bash
cd crab
ln -s ../ntuplizerHLT.py fwlite_config.py
cp ../hlt_dump.py .
cp ../hlt_dump_mc.py .
python script.py 0 &> script.log
```


### CRAB
Edit 'crab/multicrab_config.py'. The main thing to check are:
* Datasets: Follow the description in the top of the file
* name
* `config.Data.unitsPerJob`
* `config.Data.unitsPerJob`
* `config.Data.outLFNDirBase`
* If data is processed: `config.Data.lumiMask`
* `config.Site.storageSite`

Run it with `python multicrab.py`



