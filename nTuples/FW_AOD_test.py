import ROOT
from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

makeitleak = True
onlyGet = False

events = Events(["/mnt/t3nfs01/data01/shome/koschwei/trigger/onlineBTV/CMSSW_9_4_0_patch1/src/HLTBTagging/nTuples/cmsswPreProcessing.root"])
caloJets_source, caloJets_label                     = Handle("vector<reco::CaloJet>"), ("hltAK4CaloJetsCorrectedIDPassed") #DeepNtupler: hltAK4CaloJetsCorrected as jetToken3
calobtag_source, calobtag_label                     = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltCombinedSecondaryVertexBJetTagsCalo")
calodeepbtag_source, calodeepbtag_label             = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>>"), ("hltDeepCombinedSecondaryVertexBJetTagsCalo:probb")

pfJets_source, pfJets_label                         = Handle("vector<reco::PFJet>"), ("hltAK4PFJetsLooseIDCorrected") #DeepNtupler: hltPFJetForBtag as jetToken2
#pfJets_source, pfJets_label                         = Handle("vector<reco::PFJet>"), ("hltPFJetForBtag") #DeepNtupler: hltPFJetForBtag as jetToken2
pfbtag_source, pfbtag_label                         = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltCombinedSecondaryVertexBJetTagsPF")
pfdeepbtag_source, pfdeepbtag_label                 = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>>"), ("hltDeepCombinedSecondaryVertexBJetTagsPF:probb")
offEle_source, offEle_label                         = Handle("vector<pat::Electron>"), ("slimmedElectrons")
offMu_source, offMu_label                           = Handle("vector<pat::Muon>"), ("slimmedMuons")
MuGlobalTracks_source, MuGlobalTracks_label         = Handle("vector<reco::Track>"), ("globalTracks")
if makeitleak:
    eleLooseID_source, eleLooseID_label                 = Handle("<edm::ValueMap<bool>>"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose::MYHLT")
    eleTightID_source, eleTightID_label                 = Handle("<edm::ValueMap<bool>>"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight::MYHLT")

offJets_source, offJets_label                       = Handle("vector<pat::Jet>"), ("slimmedJets")
VerticesOff_source, VerticesOff_label               = Handle("vector<reco::Vertex>"), ("offlineSlimmedPrimaryVertices")

triggerBits, triggerBitLabel                        = Handle("edm::TriggerResults"), ("TriggerResults::MYHLT")

for i,event in enumerate(events):
    print "Processing event {0}".format(i)
    #if i == 100:
    #    break
    event.getByLabel(offEle_label, offEle_source)
    event.getByLabel(offMu_label, offMu_source)
    event.getByLabel(MuGlobalTracks_label, MuGlobalTracks_source)
    if makeitleak:
        event.getByLabel(eleLooseID_label , eleLooseID_source)
        event.getByLabel(eleTightID_label , eleTightID_source)
    event.getByLabel(caloJets_label, caloJets_source)
    event.getByLabel(calobtag_label, calobtag_source)
    event.getByLabel(calodeepbtag_label, calodeepbtag_source)
    event.getByLabel(pfJets_label, pfJets_source)
    event.getByLabel(pfbtag_label, pfbtag_source)
    event.getByLabel(pfdeepbtag_label, pfdeepbtag_source)
    event.getByLabel(offJets_label, offJets_source)
    event.getByLabel(VerticesOff_label, VerticesOff_source)
    event.getByLabel(triggerBitLabel, triggerBits)
    if not onlyGet:
        bJets = {}
        if calobtag_source.isValid():
            for jet in caloJets_source.product():
                calobtags = calobtag_source.product()
                for ibjet in range(len(calobtags)):
                    jobj = calobtags.key(ibjet).get()
                    #print jobj,jobj.pt(),calobtags.value(ibjet)
                    bJets[ibjet] = (jobj.eta(), jobj.phi(), calobtags.value(ibjet))

        print bJets
        bJets = {}
        if calodeepbtag_source.isValid():
            for jet in caloJets_source.product():
                calobtags = calodeepbtag_source.product()
                for ibjet in range(len(calobtags)):
                    jobj = calobtags.key(ibjet).get()
                    #print jobj,jobj.pt(),calobtags.value(ibjet)
                    bJets[ibjet] = (jobj.eta(), jobj.phi(), calobtags.value(ibjet))

        print bJets
        bJets = {}
        if pfbtag_source.isValid(): 
            for jet in pfJets_source.product():
                pfbtags = pfbtag_source.product()
                for ibjet in range(len(pfbtags)):
                    jobj = pfbtags.key(ibjet).get()
                    #print jobj,jobj.pt(),pfbtags.value(ibjet)
                    bJets[ibjet] = (jobj.eta(), jobj.phi(), pfbtags.value(ibjet))

        print bJets
        bJets = {}
        if pfdeepbtag_source.isValid(): 
            for jet in pfJets_source.product():
                pfbtags = pfdeepbtag_source.product()
                for ibjet in range(len(pfbtags)):
                    jobj = pfbtags.key(ibjet).get()
                    #print jobj,jobj.pt(),pfbtags.value(ibjet)
                    bJets[ibjet] = (jobj.eta(), jobj.phi(), pfbtags.value(ibjet))

        print bJets
        #raw_input("Next event")
