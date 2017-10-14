import ROOT
from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()


events = Events("file:/afs/cern.ch/work/k/koschwei/trigger/data/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root")

offEle_source, offEle_label             = Handle("vector<reco::GsfElectron>"), ("gedGsfElectrons")
offJets_source, offJets_label           = Handle("vector<reco::PFJet>"), ("ak4PFJets")
offbtag_source, offbtag_label           = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfCombinedInclusiveSecondaryVertexV2BJetTags")
offdeepbtag_source, offdeepbtag_label           = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfDeepCSVJetTags:probb")



eleID_source, eleID_label = Handle("<edm::ValueMap<bool> >"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose")

electron = None
electronID = None
for i,event in enumerate(events):
    print "Processing event {0}".format(i)
    if i == 100:
        break
    event.getByLabel(offEle_label, offEle_source)
    event.getByLabel(eleID_label, eleID_source)
    event.getByLabel(offJets_label, offJets_source)
    event.getByLabel(offbtag_label, offbtag_source)
    event.getByLabel(offdeepbtag_label, offdeepbtag_source)

    offbtags = offbtag_source.product()
    offdeepbtags = offdeepbtag_source.product()
    for ijet, jet in enumerate(offbtag_source.product()):
        jobj = jet.first.get()
        print jobj,jobj.pt(),offbtags.value(ijet), offdeepbtags.value(ijet)

    #raw_input("Next event")
