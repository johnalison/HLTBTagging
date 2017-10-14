# Code for running HLT b-tagging studies


## Setup
Setting up CMSSW like described in [GuideGlobalHLT](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT)

```bash
export SCRAM_ARCH=slc6_amd64_gcc530 #Important! With gcc630 referneces to jets for btagging are not working
cmsrel CMSSW_9_2_12_patch1
cd CMSSW_9_2_12_patch1/src
cmsenv
git cms-init

git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v96.35-CMSSW_9_2_12
git cms-addpkg L1Trigger/L1TCommon
git cms-addpkg L1Trigger/L1TMuon
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TMuon.git L1Trigger/L1TMuon/data

git cms-addpkg L1Trigger/L1TGlobal

# HLT
git cms-addpkg HLTrigger/Configuration

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 6
rehash
```

Additional code for runnning the ntupler (by Silvio)

```bash
git cms-addpkg PhysicsTools/Heppy
git cms-addpkg PhysicsTools/HeppyCore
git remote add silvio-cmssw https://github.com/silviodonato/cmssw.git
git fetch silvio-cmssw
git cherry-pick 52c976ea1c1a5309dffd6e11e9aaf570499d0ef9 #Get code for using heppy with RAW+AOD

git cms-checkdeps -A -a
scram b -j 6
```
