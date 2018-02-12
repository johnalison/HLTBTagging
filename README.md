# Code for running HLT b-tagging studies


## Setup w/ DeepNtupler
Setting up CMSSW like described in [GuideGlobalHLT](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT)

```bash
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_10_0_0 
cd CMSSW_10_0_0/src
cmsenv
git cms-init
git cms-merge-topic 21908
git cms-addpkg HLTrigger/Configuration

#Add code for running secondary file with Heppy
git cms-addpkg PhysicsTools/Heppy
git cms-addpkg PhysicsTools/HeppyCore
git remote add silvio-cmssw https://github.com/silviodonato/cmssw.git
git fetch silvio-cmssw
git cherry-pick 52c976ea1c1a5309dffd6e11e9aaf570499d0ef9 #Get code for using heppy with RAW+AOD

git clone -b DeepNtuples git@github.com:kschweiger/HLTBTagging.git 

git clone https://github.com/emilbols/DeepNTuples
cd DeepNTuples
git submodule init
git submodule update
cd $CMSSW_BASE/src 
#DeepCSV is already in the release, but with different names, which will become the defaults in the close future
#sed -i 's|deepFlavourJetTags|pfDeepCSVJetTags|g' DeepNTuples/DeepNtuplizer/production/DeepNtuplizer.py
#Fix some compilation error with inclusion of std::vector
sed -i 's|#include <cmath>|#include <cmath>\n#include <vector>|g' DeepNTuples/DeepNtuplizer/interface/sorting_modules.h

scram b -j 4
```


