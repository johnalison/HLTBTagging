# nTupler
Creation of flat trees with HLT objects. For this the HLT has to be rerun on RAW. [Original Code](https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8)

## Usage
The following steps are necessary to produce the ntuples.
### HLT config
Creating of config dump for running the RAW+MiniAOD files with HLT. The HLT tables and `--setup` depend on the usecase.
For Data:

#### Run A - With V1 menu:
```bash
hltGetConfiguration /users/koschwei/CMSSW_10_1_0/HLT_BTag_18_V1Menu/V4 \
 --setup /dev/CMSSW_10_1_0/GRun/V1 \
 --data --globaltag 101X_dataRun2_HLT_v7 \
 --input root://cms-xrd-global.cern.ch//store/data/Run2018A/MuonEG/RAW/v1/000/315/506/00000/08090981-324D-E811-A7B1-02163E017FF8.root  \
 --process MYHLT --full --offline   \
 --unprescale --max-events 10 --output none > hltData.py
```

#### Run A - With V2 menu but L1 from V1 (as present in RunA RAW):
```bash
hltGetConfiguration /users/koschwei/CMMSW_10_1_2/HLT_bTag_18_L1RunA_3/V4  \
--setup /dev/CMSSW_10_1_0/GRun \
--data --globaltag 101X_dataRun2_HLT_v7 \
--input root://cms-xrd-global.cern.ch//store/data/Run2018A/MuonEG/RAW/v1/000/315/506/00000/08090981-324D-E811-A7B1-02163E017FF8.root \
--process MYHLT --full --offline  \
--unprescale --max-events 10 --output none > hltData.py
```


#### With V2 menu - (for CMSSW_10_1_7):
```bash
hltGetConfiguration /users/koschwei/CMSSW_10_1_7/HLT_GRunV56/V3 --setup /dev/CMSSW_10_1_0/GRun/V56 --data --globaltag 101X_dataRun2_HLT_HEmiss_v1 --input root://cms-xrd-global.cern.ch//store/relval/CMSSW_10_1_7/MuonEG/FEVTDEBUGHLT/101X_dataRun2_HLT_HEmiss_v1_RelVal_muEG2018B-v1/10000/00538A51-D57F-E811-B85D-0025905B8606.root  --process MYHLT --full --offline --unprescale --max-events 10 --output none > hltData.py
```
hltGetConfiguration /users/koschwei/CMSSW_10_1_7/HLT_GRunV56/V3 --setup /dev/CMSSW_10_1_0/GRun/V56 --data --globaltag 101X_dataRun2_HLT_v7 --input root://cms-xrd-global.cern.ch//store/relval/CMSSW_10_1_7/MuonEG/FEVTDEBUGHLT/101X_dataRun2_HLT_v7_RelVal_muEG2018B-v1/10000/008175B3-E67F-E811-9432-0025905AA9CC.root  --process MYHLT --full --offline --unprescale --max-events 10 --output none > hltData.py

hltGetConfiguration /users/koschwei/CMSSW_10_1_0/HLT_BTag_18_V1Menu/V4  --setup /dev/CMSSW_10_1_0/GRun/V1 --mc --globaltag 101X_mc2017_realistic_TSG_v1 --input root://cms-xrd-global.cern.ch//store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/FEDCCD34-BFA1-E711-93DE-FA163E3ECCF5.root --process MYHLT --full --offline   --unprescale --max-events 10 --output none > hltMC.py




```bash
edmConfigDump hltMC.py > hlt_dump_mc_HEmiss.py
cmsRun hlt_dump_mc_HEmiss.py &> cmsRunMC.log

edmConfigDump hltData.py > hlt_dump_phase1.py
cmsRun  hlt_dump_phase1.py &> cmsRunData.log
```

Check `cmsRunMC.log` and/or `cmsRunMC.log` if rerunning the HLT finishes without errors.

For runnning the nTupler the following changes to the configs are required:

__Add__ to the `process.source` in the __beginning of the file__ `lumisToProcess = cms.untracked.VLuminosityBlockRange( )`, so it looks like this:
```python
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2017C/MuonEG/RAW/v1/000/299/368/00000/00E9C4F1-E76B-E711-8952-02163E01A27B.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange( ),
    inputCommands = cms.untracked.vstring('keep *')
)
```

__Remove__
```python
process.DQMOutput = cms.EndPath(process.dqmOutput)
```


__Add__ the following to the __end of the the config__ dump:
```python
process.hltOutputFULL = cms.OutputModule("PoolOutputModule",
                                         dataset = cms.untracked.PSet(),
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
                                                                                #######
                                                                                'keep *_genParticles_*_*',#AOD
                                                                                'keep *_prunedGenParticles_*_*',#MINIAOD
                                                                                #######
                                                                                'keep *genParticles_*_*_*',
                                                                                'keep *Trigger*_*_*_*',
                                                                                'keep recoJetedmRefToBaseProdTofloatsAssociationVector_*_*_*',
                                                                                #######
                                                                                'keep *_addPileupInfo_*_*', #AOD
                                                                                'keep *_slimmedAddPileupInfo_*_*',#MINIAOD
                                                                                #######
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
python script_phaseI.py 0 &> script.log
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

Run it with `python phaseI_crab_config.py`


## Further infos

### PU reweighting
1. Get pilup JSON and PromptReco JSON from `/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/`
2. Edit the PrompReco JSON to only include the run(s) that will be processed 
3. Follow the instuction from [PUreweighting Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJSONFileforData)
4. Example : `pileupCalc.py --maxPileupBin 90 --numPileupBins 90 --minBiasXsec=69200 --inputLumiJSON=pileup_latest.txt --calcMode true -i ???_13TeV_PromptReco_Collisions17_JSON.txt output.root`
5. Use `puHCalc.py output.root`
6. To reweight, get the  `.getTrueNumInteractions()` from the `addPileupInfo`(in AOD) collection and find the *bin* in the PUHisto corrsesponding to that value. The bin height is the reweighting factor.

### Generate JSON file for limited PU range
If the MC sample is generated with a PU range smaller than in data, the script `getJSONforPUrange.py` can be used to remove all LS from the PromptReco JSON with PU outside a certain range, that can be set in script. This JSON can then be used as lumimask in the crab configuration.

## Rescaling of Datasets
### Calculating lumi for the processed data
If all job of the Data finished, the json with all processed lumi sections can be found using `crab report` which writes it to `results/inputDatasetLumis.json`.

With the JSON [file brilcalc](https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec) can be used to calculated the integrated lumi on *lxplus*:
```bash
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
#Check normtag on twiki page
brilcalc lumi -u /pb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -i pocessedLS.json 
```

### Getting number of events processed in MC dataset
The outputfiles contain a histogram with the count of processed events. 



