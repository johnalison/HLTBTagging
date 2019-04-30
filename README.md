# Code for running HLT b-tagging studies


## Setup
Setting up CMSSW like described in [GuideGlobalHLT](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT)

```bash
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_10_1_2_patch2
cd CMSSW_10_1_2_patch2/src
cmsenv

# HLT
git cms-addpkg HLTrigger/Configuration

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 6
```

Additional code for runnning the ntupler (by Silvio)

```bash
git clone git@github.com:kschweiger/HLTBTagging.git -b 10X #Clone this repo

git cms-addpkg PhysicsTools/Heppy
git cms-addpkg PhysicsTools/HeppyCore
cp HLTBTagging/HeppyFixes/94X/cmsswPreprocessor.py PhysicsTools/Heppy/python/utils/cmsswPreprocessor.py
cp HLTBTagging/HeppyFixes/94X/config.py PhysicsTools/HeppyCore/python/framework/config.py

git cms-addpkg RecoBTag/SecondaryVertex
#cp HLTBTagging/HeppyFixes/94X/

git cms-checkdeps -A -a
scram b -j 6
```
