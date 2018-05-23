export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src
cmsenv
git cms-init

# HLT
git cms-addpkg HLTrigger/Configuration

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 6


git cms-merge-topic cms-egamma:EgammaPostRecoTools_940 #For adding 94X electron id to miniAODv1 (v2 already contains latest IDs)

git clone git@github.com:kschweiger/HLTBTagging.git #Clone this repo

git cms-addpkg PhysicsTools/Heppy
git cms-addpkg PhysicsTools/HeppyCore
cp HLTBTagging/HeppyFixes/94X/cmsswPreprocessor.py PhysicsTools/Heppy/python/utils/cmsswPreprocessor.py
cp HLTBTagging/HeppyFixes/94X/config.py PhysicsTools/HeppyCore/python/framework/config.py

git cms-checkdeps -A -a
scram b -j 6
