# nTupler
Creation of flat trees with HLT objects. For this the HLT has to be rerun on RAW. [Original Code](https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8)

## Usage
The following steps are necessary to produce the ntuples.
### HLT config
Creating of config dump for running the RAW+AOD files with HLT. The HLT tables and `--setup` depend on the usecase.
For Data:
```bash
edmConfigDump hltData.py > hlt_dump.py
```
For MC:
```bash
hltGetConfiguration /dev/CMSSW_10_0_0/GRun  \ 
--globaltag 100X_upgrade2018_realistic_TSG_2018_01_24_13_08_07  \
--input file:/afs/cern.ch/work/k/koschwei/public/RelValTTbar_13_GEN-SIM-DIGI-RAW-HLTDEBUG_LumiStarting1_EE64BF2D-7600-E811-90B8-0CC47A4D767E.root  \
--process MYHLT --full --offline  \ 
--unprescale --max-events 10 --output none  \
--mc --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking > hltMC.py
edmConfigDump hltMC.py > hlt_dump_mc.py
```

For Data:
```bash
hltGetConfiguration /dev/CMSSW_10_0_0/GRun  \
--globaltag 100X_dataRun2_relval_ForTSG_v1 \
--path HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath \
--input root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root \
--process MYHLT --full --offline \ 
--data --unprescale --max-events 10 --output none \
--customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking > hltData.py

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
                                                                                "keep *ShallowTagInfo_*_*_*",
                                                                                "keep reco*Collection_*_*_*")

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

