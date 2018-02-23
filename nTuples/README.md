# nTupler
Creation of flat trees with HLT objects. For this the HLT has to be rerun on RAW. [Original Code](https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8)

## Usage
The following steps are necessary to produce the ntuples.

### HLT menu

In order to have the b-tagging information for every jet in every event it is required to run a HLT menu that includes paths the run the b-tagging sequences in every event (independent of L1 or other filters). One example for this is the menu __/users/koschwei/HLT_DeepCSVNoFilter_Phase1__ which includes __noFilter_*__ paths that are made exacly for this purpose.

### HLT config
Creating of config dump for running the RAW+AOD files with HLT. The HLT tables and `--setup` depend on the usecase.
w/ Phase 1 DeepCSV training (same as offline):
```bash
hltGetConfiguration /users/koschwei/HLT_DeepCSVNoFilter_Phase1 --setup /dev/CMSSW_10_0_0/GRun  \
--globaltag 100X_dataRun2_relval_ForTSG_v1 \
--input root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root \
--process MYHLT --full --offline \
--data --unprescale --max-events 10 --output none \
--customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking > hltData.py

edmConfigDump hltData.py > hlt_dump.py
```

Remove:
```python
process.DQMOutput = cms.EndPath(process.dqmOutput)
```
Add the following to the end of the the config dumP:
```python
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("RecoBTag/Configuration/RecoBTag_cff")
process.load("RecoBTag.Combined.deepFlavour_cff")

process.btagging = cms.Path(process.btagging)
process.deepFlav  = cms.Path(process.pfDeepFlavourTask)


process.hltOutputFULL = cms.OutputModule("PoolOutputModule",
                                         dataset = cms.untracked.PSet(),
                                         fileName = cms.untracked.string('./cmsswPreProcessing.root'),
                                         outputCommands = cms.untracked.vstring('drop *',
                                                                                'keep reco*_*_*_*',
                                                                                "drop *Tau*_*_*_*",
                                                                                "drop *Muon*_*_*_*",
                                                                                "drop *Electron*_*_*_*",
                                                                                "drop *MET*_*_*_*",
                                                                                "drop *Photons*_*_*_*",
                                                                                "drop *Cluster*_*_*_*",
                                                                                "drop *Ecal*_*_*_*")
)

process.FULLOutput = cms.EndPath(process.hltOutputFULL)
```
Add to the `process.source` in the beginning of the file `lumisToProcess = cms.untracked.VLuminosityBlockRange( )`, so it looks like this:
```python
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange( ),
    inputCommands = cms.untracked.vstring('keep *')
)
```

### Files
To rerun the HLT and get the offline variables AOD and RAW samples are needed. The files in the repo are for 
* /MuonEG/Run2017E-PromptReco-v1/AOD
* /MuonEG/Run2017E-v1/RAW
For other DS please check if the RAW DS is available.

### nTupler production

All files are located in the `crab/`folder (the cmssw configs are links to this folder)

#### Local test
Edit `crab/PSet_localTest.py`to fit your needs.
```bash
cd crab
ln -s ../ntuplizerHLT.py fwlite_config.py
cp ../hlt_dump.py .
python script.py 0 &> script.log
```


#### CRAB
Edit 'crab/multicrab_config.py'. The main thing to check are:
* Datasets: Follow the description in the top of the filename
* `config.Data.unitsPerJob`
* `config.Data.unitsPerJob`
* `config.Data.outLFNDirBase`
* If data is processed: `config.Data.lumiMask`
* `config.Site.storageSite`

Run it with `python multicrab.py`

