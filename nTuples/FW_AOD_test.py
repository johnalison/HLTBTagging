import ROOT
from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()


events = Events("file:/afs/cern.ch/work/k/koschwei/trigger/data/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root")

offEle_source, offEle_label             = Handle("vector<reco::GsfElectron>"), ("gedGsfElectrons")

eleID_source, eleID_label = Handle("<edm::ValueMap<bool> >"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose")

electron = None
electronID = None
for i,event in enumerate(events):
    print "Processing event {0}".format(i)
    if i == 100:
        break
    event.getByLabel(offEle_label, offEle_source)
    event.getByLabel(eleID_label, eleID_source)
    for ele in offEle_source.product():
        print ele
        #print ele.dEtaInSeed
        electron = ele
    electronID = eleID_source
    #exit()
