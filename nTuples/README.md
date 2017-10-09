# nTupler
Creation of flat trees with HLT objects. For this the HLT has to be rerun on RAW. [Original Code](https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8)

## Usage
The following steps are necessary to produce the ntuples.
### HLT config
Creating of config dump for running the RAW+AOD files with HLT. The HLT tables and `--setup` depend on the usecase.
```bash
hltGetConfiguration /users/koschwei/CMSSW_9_2_10/HLT_TnP_BTag \
 --setup /dev/CMSSW_9_2_0/HLT \
 --data --globaltag auto:run2_hlt_GRun \
 --input root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root  \
 --process MYHLT --full --offline   \
 --unprescale --max-events 10 --output none > hltData2.py

edmConfigDump hltData.py > hlt_dump.py
```

Add the following to the end of the the config dumP:
```python
process.hltOutputFULL = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
    ),
    fileName = cms.untracked.string('./cmsswPreProcessing.root'),
    outputCommands = cms.untracked.vstring('drop *',
        'keep l1t*_*_*_*',
        'keep *_*Ht*_*_*',
        'keep *Jet*_*_*_*',
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
```bash

```
