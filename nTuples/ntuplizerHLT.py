#!/usr/bin/python
"""ntuplizerHLT 
Original Code by S. Donato - https://github.com/silviodonato/usercode/tree/NtuplerFromHLT2017_V8

Code for making nTuples with offline variables (from AOD) and HLT objects (Rerun on RAW) using the heppy framework
"""
import ROOT
import itertools
import resource
from array import array
from math import sqrt, pi, log10, log, exp
# load FWlite python libraries
from DataFormats.FWLite import Handle, Events
from utils import deltaR,SetVariable,DummyClass,productWithCheck,checkTriggerIndex

#ROOT.gROOT.LoadMacro("/scratch/sdonato/NtupleForPaolo/CMSSW_8_0_3_patch1/src/DataFormats/L1Trigger/interface/EtSumHelper.h")

Handle.productWithCheck = productWithCheck

maxJets         = 50
bunchCrossing   = 0
pt_min          = 20

def FillVector(source,variables,minPt=pt_min):
    variables.num[0] = 0
    for obj in source.productWithCheck():
        if obj.pt()<minPt: continue
        if variables.num[0]<len(variables.pt):
            for (name,var) in variables.__dict__.items():
                if name == "pt" :                     var[variables.num[0]] = obj.pt()
                elif name == "eta" :                  var[variables.num[0]] = obj.eta()
                elif name == "phi" :                  var[variables.num[0]] = obj.phi()
                elif name == "mass" :                 var[variables.num[0]] = obj.mass()
                elif name == "neHadEF" :              var[variables.num[0]] = obj.neutralHadronEnergyFraction()
                elif name == "neEmEF" :               var[variables.num[0]] = obj.neutralEmEnergyFraction()
                elif name == "chHadEF" :              var[variables.num[0]] = obj.chargedHadronEnergyFraction()
                elif name == "chEmEF" :               var[variables.num[0]] = obj.chargedEmEnergyFraction()
                elif name == "muEF" :                 var[variables.num[0]] = obj.muonEnergyFraction()
                elif name == "mult" :                 var[variables.num[0]] = obj.chargedMultiplicity()+obj.neutralMultiplicity();
                elif name == "neMult" :               var[variables.num[0]] = obj.neutralMultiplicity()
                elif name == "chMult" :               var[variables.num[0]] = obj.chargedMultiplicity()
                elif name == "passesTightID":         var[variables.num[0]] = passJetID(obj, "tight")
                elif name == "passesTightLeptVetoID": var[variables.num[0]] = passJetID(obj, "tightLepVeto")
                elif name == "passesLooseID":         var[variables.num[0]] = passJetID(obj, "loose")
                
            variables.num[0] += 1
            
def FillBtag(btags_source, jets, jet_btags, jet_btagsRank = None, JetIndexVars = None, nBtagsgeNull = None):
    """
    In this function the btags_source product is called for every time it is needed.
    For some reason, if stored (e.g. btags = btags_source.productWithCheck()), the objects
    starts leaking in memory. Especially when getting the the referenced jet, this leads 
    to segmentations violations.
    """
    jetB = None
    tagpairs = int(jets.num[0])*[(-1,-20)]
    for i in range(jets.num[0]):
        jet_btags[i] = -20.
        dRmax = 0.3
        for ibjet in range(len(btags_source.productWithCheck())):
            jetB = btags_source.productWithCheck().key(ibjet).get()
            dR = deltaR(jetB.eta(),jetB.phi(),jets.eta[i],jets.phi[i])
            if dR<dRmax:
                jet_btags[i] = max(0.,btags_source.productWithCheck().value(ibjet))
                tagpairs[i] = (i, jet_btags[i])
                dRmax = dR
            del jetB

    if jet_btagsRank is not None:
        if JetIndexVars is not None and isinstance(JetIndexVars, list):
            for var in JetIndexVars:
                var[0] = -1
        if nBtagsgeNull is not None:
            nBtagsgeNull[0] = 0
        from operator import itemgetter
        sortedtags = sorted(tagpairs,key=itemgetter(1), reverse=True) #This list is ordered by csv value, starting with the highest
        for ipair, pair in enumerate(sortedtags):
            jet_btagsRank[pair[0]] = ipair
            if JetIndexVars is not None and isinstance(JetIndexVars, list):
                if len(JetIndexVars) >= ipair+1:
                    JetIndexVars[ipair][0] = pair[0]
            if nBtagsgeNull is not None:
                if pair[1] >= 0:
                    nBtagsgeNull[0] += 1
                


def passJetID(jet, requestedID):
    PFJetIDLoose = False
    PFJetIDTight = False
    PFJetIDTightLepVeto = False
    if (jet.chargedMultiplicity()+jet.neutralMultiplicity()) > 1 and jet.chargedMultiplicity() > 0 and jet.chargedHadronEnergyFraction() > 0:
        if jet.neutralHadronEnergyFraction() < 0.99 and jet.neutralEmEnergyFraction() < 0.99 and jet.chargedEmEnergyFraction() < 0.99:
            PFJetIDLoose = True
        if jet.neutralHadronEnergyFraction() < 0.90 and jet.neutralEmEnergyFraction() < 0.90 and jet.chargedEmEnergyFraction() < 0.99:
            PFJetIDTight = True
            if jet.muonEnergyFraction() < 0.8 and jet.chargedEmEnergyFraction() < 0.90:
                PFJetIDTightLepVeto =  True
    if requestedID == "tight":
        return PFJetIDTight
    elif requestedID == "tightLepVeto":
        return PFJetIDTightLepVeto
    elif requestedID == "loose":
        return PFJetIDLoose
    

def FillMuonVector(source, variables, vertex, muonid = "tight"):
    if vertex is None:
        return False
    variables.num[0] = 0
    for obj in source.productWithCheck():
        passesID = False
        #Sometimes (in MC) there is no track saved/accessable for the muon. This prevents to code from crashing
        if obj.globalTrack().isNull():
            print "Track is NULL"
        else:
            if muonid == "tight":
                if ( obj.globalTrack().normalizedChi2() < 10 and obj.isPFMuon() and
                     obj.globalTrack().hitPattern().numberOfValidMuonHits() > 0 and
                     obj.numberOfMatchedStations() > 1 and obj.isGlobalMuon()  and
                     abs(obj.muonBestTrack().dxy(vertex.position())) < 0.2 and
                     abs(obj.muonBestTrack().dz(vertex.position())) < 0.5 and
                     obj.innerTrack().hitPattern().numberOfValidPixelHits() > 0 and
                     obj.innerTrack().hitPattern().trackerLayersWithMeasurement() > 5 ):
                    passesID = True
            if muonid == "loose":
                if ( obj.isPFMuon() and ( obj.isGlobalMuon() or obj.isTrackerMuon() )):
                    passesID = True
        if passesID:
            for (name, var) in variables.__dict__.items():
                #See https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
                if name == "pt" :           var[variables.num[0]] = obj.pt()
                elif name == "eta" :        var[variables.num[0]] = obj.eta()
                elif name == "phi" :        var[variables.num[0]] = obj.phi()
                elif name == "mass" :       var[variables.num[0]] = obj.mass()
                elif name == "iso" :        var[variables.num[0]] = getMuonIso(obj)
            variables.num[0] += 1
        return True

def getMuonIso(muon):
    MuIsoVars = muon.pfIsolationR04()
    iso = (MuIsoVars.sumChargedHadronPt + max(0.0, MuIsoVars.sumNeutralHadronEt + MuIsoVars.sumPhotonEt - 0.5 * MuIsoVars.sumPUPt)) / muon.pt();
    return iso

    
def FillElectronVector(source, variables, electronids):
    #see https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
    variables.num[0] = 0
    for iobj, obj in enumerate(source.productWithCheck()):
        if electronids.get(iobj):
            #print obj, obj.pt(), electronids.get(iobj)
            for (name, var) in variables.__dict__.items():
                if name == "pt" :                var[variables.num[0]] = obj.pt()
                elif name == "eta" :             var[variables.num[0]] = obj.eta()
                elif name == "phi" :             var[variables.num[0]] = obj.phi()
                elif name == "mass" :            var[variables.num[0]] = obj.mass()
                elif name == "superClusterEta" : var[variables.num[0]] = obj.superCluster().eta()
                
            variables.num[0] += 1
        
def Matching(phi, eta, jets):
    index = -1
    for i in range(jets.num[0]):
        dRmax = 0.3
        dR = deltaR(eta,phi,jets.eta[i],jets.phi[i])
        if dR<dRmax:
            index = i
            dRmax = dR
    return index

def getVertex(vertex_source):
    vertices = vertex_source.productWithCheck()
    if vertices.size()>0:
        return vertices.at(0).z()
    else:
        return -1000

def WithFallback(product,method="pt"):
    if product.size()>0:
        return getattr(product[0],method)()
    else:
        return -10

def BookVector(tree,name="vector",listMembers=[]):
    obj = DummyClass()
    obj.num   = SetVariable(tree,name+'_num' ,'I')
    for member in listMembers:
        if "match" in name:
            setattr(obj,member,SetVariable(tree,name+'_'+member  ,'I',name+'_num',maxJets))
        else:
            setattr(obj,member,SetVariable(tree,name+'_'+member  ,'F',name+'_num',maxJets))
    return obj

    ##########################################################################

def launchNtupleFromHLT(fileOutput,filesInput, secondaryFiles, maxEvents,preProcessing=True, firstEvent=0, MC = False):
    bunchCrossing   = 12
    print "filesInput: ",filesInput
    print "fileOutput: ",fileOutput
    print "secondaryFiles: ",secondaryFiles
    print "maxEvents: ",maxEvents
    print "preProcessing: ",preProcessing
    print "firstEvent: ",firstEvent

    doTriggerCut = True
    if doTriggerCut:
        print "+-----------------------------------------------------------------------------------------+"
        print "| TriggerCut is active. All events passing none of the triggers in the menu are discarded!|"
        print "| Note: If --setup is used only the path in the actual menu are considered for this.      |" 
        print "|       Not the ones in the setup.                                                        |"
        print "+-----------------------------------------------------------------------------------------+"

    dataflags = ["MuonEG"] #NOTE: Add more flags if different data datasets are considered
        
    #isMC = bool(MC)

    if len(filesInput)>0 and (len(filter(lambda x: x in filesInput[0], dataflags)) >= 1):
        print "filesinput[0] has at least on of {0}".format(dataflags)
        isMC = False
        Signal = False
    else:
        isMC = True
        Signal = False

    print "isMC = {0}".format(isMC)

    ## Pre-processing
    if preProcessing:
        from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
        from PhysicsTools.HeppyCore.framework.config import MCComponent
        if not isMC:
            cmsRun_config = "hlt_dump.py"
        else:
            cmsRun_config = "hlt_dump_mc.py"
        print "Using: {0}".format(cmsRun_config)
        preprocessor = CmsswPreprocessor(cmsRun_config)
        cfg = MCComponent("OutputHLT",filesInput, secondaryfiles=secondaryFiles)
        print "Run cmsswPreProcessing using:"
        print cfg.name
        print cfg.files
        print cfg.secondaryfiles
        print
        try:
            preprocessor.run(cfg,".",firstEvent,maxEvents)
        except:
            print "cmsswPreProcessing failed!"
            print "cat cmsRun_config.py"
            config = file(cmsRun_config)
            print config.read()
            print "cat cmsRun.log"
            log = file("cmsRun.log")
            print log.read()
            preprocessor.run(cfg,".",firstEvent,maxEvents)
            raise Exception("CMSSW preprocessor failed!")

    f = ROOT.TFile(fileOutput,"recreate")
    tree = ROOT.TTree("tree","tree")

    nGenHisto = ROOT.TH1F("nGen","nGen",1,1,2)
    nPassHisto = ROOT.TH1F("nPass","nPass",1,1,2)
    
    fwLiteInputs = ["cmsswPreProcessing.root"]
    if len(filesInput)==0: exit
    import os.path
    if not os.path.isfile(fwLiteInputs[0]):
        raise Exception( fwLiteInputs[0] + " does not exist.")
    events = Events (fwLiteInputs)

    ### list of input variables ###
    ### TODO: Streamline this
    #L1
    l1HT_source, l1HT_label                             = Handle("BXVector<l1t::EtSum>"), ("hltGtStage2Digis","EtSum")
    l1Jets_source, l1Jets_label                         = Handle("BXVector<l1t::Jet>"), ("hltGtStage2Digis","Jet")
    
    #Leptons
    offEle_source, offEle_label                         = Handle("vector<reco::GsfElectron>"), ("gedGsfElectrons")
    offMu_source, offMu_label                           = Handle("vector<reco::Muon>"), ("muons")
    MuGlobalTracks_source, MuGlobalTracks_label         = Handle("vector<reco::Track>"), ("globalTracks")
    eleLooseID_source, eleLooseID_label                 = Handle("<edm::ValueMap<bool> >"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose")
    eleTightID_source, eleTightID_label                 = Handle("<edm::ValueMap<bool> >"), ("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight")

    #Jets
    caloJets_source, caloJets_label                     = Handle("vector<reco::CaloJet>"), ("hltAK4CaloJetsCorrectedIDPassed")
    calobtag_source, calobtag_label                     = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltCombinedSecondaryVertexBJetTagsCalo")
    calodeepbtag_source, calodeepbtag_label             = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsCalo:probb")
    calodeepbtag_bb_source, calodeepbtag_bb_label       = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsCalo:probbb")
    calodeepbtag_udsg_source, calodeepbtag_udsg_label   = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsCalo:probudsg")
    caloPUid_source, caloPUid_label                     = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltCaloJetFromPV")

    pfJets_source, pfJets_label                         = Handle("vector<reco::PFJet>"), ("hltAK4PFJetsLooseIDCorrected")
    pfbtag_source, pfbtag_label                         = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltCombinedSecondaryVertexBJetTagsPF")
    pfdeepbtag_source, pfdeepbtag_label                 = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsPF:probb")
    pfdeepbtag_bb_source, pfdeepbtag_bb_label           = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsPF:probbb")
    pfdeepbtag_udsg_source, pfdeepbtag_udsg_label       = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("hltDeepCombinedSecondaryVertexBJetTagsPF:probudsg")

    offJets_source, offJets_label                       = Handle("vector<reco::PFJet>"), ("ak4PFJetsCHS")
    offJetsnoCHS_source, offJetsnoCHS_label             = Handle("vector<reco::PFJet>"), ("ak4PFJets")
    offbtag_source, offbtag_label                       = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfCombinedInclusiveSecondaryVertexV2BJetTags")
    offdeepbtag_source, offdeepbtag_label               = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfDeepCSVJetTags:probb")
    offdeepbtag_bb_source, offdeepbtag_bb_label         = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfDeepCSVJetTags:probbb")
    offdeepbtag_udsg_source, offdeepbtag_udsg_label     = Handle("edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>"), ("pfDeepCSVJetTags:probudsg")
    
    #MET and HT
    offMet_source, offMet_label                         = Handle("vector<reco::PFMET>"), ("pfMet")
    pfMet_source, pfMet_label                           = Handle("vector<reco::PFMET>"), ("hltPFMETProducer")
    pfMht_source, pfMht_label                           = Handle("vector<reco::MET>"), ("hltPFMHTTightID")
    caloMet_source, caloMet_label                       = Handle("vector<reco::CaloMET>"), ("hltMet")
    caloMht_source, caloMht_label                       = Handle("vector<reco::MET>"), ("hltMht")
    caloMhtNoPU_source, caloMhtNoPU_label               = Handle("vector<reco::MET>"), ("hltMHTNoPU")

    #Vertex
    pileUp_source, pileUp_label                         = Handle("vector<PileupSummaryInfo>"), ("addPileupInfo")
    FastPrimaryVertex_source, FastPrimaryVertex_label   = Handle("vector<reco::Vertex>"), ("hltFastPrimaryVertex")
    FPVPixelVertices_source, FPVPixelVertices_label     = Handle("vector<reco::Vertex>"), ("hltFastPVPixelVertices")
    PixelVertices_source, PixelVertices_label           = Handle("vector<reco::Vertex>"), ("hltPixelVertices")
    VerticesPF_source, VerticesPF_label                 = Handle("vector<reco::Vertex>"), ("hltVerticesPF")
    VerticesL3_source, VerticesL3_label                 = Handle("vector<reco::Vertex>"), ("hltVerticesL3")
    VerticesOff_source, VerticesOff_label               = Handle("vector<reco::Vertex>"), ("offlinePrimaryVertices")
    
    #Gen
    genJets_source, genJets_label                       = Handle("vector<reco::GenJet>"), ("ak4GenJetsNoNu")
    genMet_source, genMet_label                         = Handle("vector<reco::GenMET>"), ("genMetTrue")
    genParticles_source, genParticles_label             = Handle("vector<reco::GenParticle>"), ("genParticles")
    generator_source, generator_label                   = Handle("GenEventInfoProduct"), ("generator")
    
    #The rest
    triggerBits, triggerBitLabel                        = Handle("edm::TriggerResults"), ("TriggerResults::MYHLT")


    ### create output variables ###
    #Leptons
    offTightElectrons   = BookVector(tree, "offTightElectrons", ['pt','eta', 'phi', "superClusterEta"])
    offLooseElectrons   = BookVector(tree, "offLooseElectrons", ['pt','eta', 'phi', "superClusterEta"])
    offTightMuons       = BookVector(tree, "offTightMuons", ['pt','eta', 'phi', 'iso'])
    offLooseMuons       = BookVector(tree, "offLooseMuons", ['pt','eta', 'phi', 'iso'])
    
    #Jets:
    l1Jets              = BookVector(tree,"l1Jets",['pt','eta','phi','matchOff','matchGen'])
    caloJets            = BookVector(tree,"caloJets",['pt','eta','phi','mass','matchOff','matchGen','puId','csv','deepcsv','deepcsv_bb','deepcsv_udsg',"rankCSV", "rankDeepCSV"])
    pfJets              = BookVector(tree,"pfJets",['pt','eta','phi','mass','matchOff','matchGen','neHadEF','neEmEF','chHadEF','chEmEF','muEF','mult','neMult','chMult','csv','deepcsv','deepcsv_bb','deepcsv_udsg',"passesTightID","passesTightLeptVetoID", "passesLooseID", "rankCSV", "rankDeepCSV"])
    offJets             = BookVector(tree,"offJets",['pt','eta','phi','mass','csv','deepcsv','deepcsv_bb','deepcsv_udsg','matchGen','neHadEF','neEmEF','chHadEF','chEmEF','muEF','mult','neMult','chMult',"passesTightID","passesTightLeptVetoID", "passesLooseID", "rankCSV", "rankDeepCSV"])
    offTightJets        = BookVector(tree,"offTightJets",['pt','eta','phi','mass','csv','deepcsv','deepcsv_bb','deepcsv_udsg','matchGen','neHadEF','neEmEF','chHadEF','chEmEF','muEF','mult','neMult','chMult',"passesTightID","passesTightLeptVetoID", "passesLooseID", "rankCSV", "rankDeepCSV"])

    CSVleadingCaloJet = SetVariable(tree, "caloJets_ileadingCSV")
    CSVleadingPFJet = SetVariable(tree, "pfJets_ileadingCSV")
    CSVleadingOffJet = SetVariable(tree, "offJets_ileadingCSV")
    CSVleadingOffTightJet = SetVariable(tree, "offTightJets_ileadingCSV")
    CSVsecondCaloJet = SetVariable(tree, "caloJets_isecondCSV")
    CSVsecondPFJet = SetVariable(tree, "pfJets_isecondCSV")
    CSVsecondOffJet = SetVariable(tree, "offJets_isecondCSV")
    CSVsecondOffTightJet = SetVariable(tree, "offTightJets_isecondCSV")
    CSVthirdCaloJet = SetVariable(tree, "caloJets_ithirdCSV")
    CSVthirdPFJet = SetVariable(tree, "pfJets_ithirdCSV")
    CSVthirdOffJet = SetVariable(tree, "offJets_ithirdCSV")
    CSVthirdOffTightJet = SetVariable(tree, "offTightJets_ithirdCSV")
    CSVfourthCaloJet = SetVariable(tree, "caloJets_ifourthCSV")
    CSVfourthPFJet = SetVariable(tree, "pfJets_ifourthCSV")
    CSVfourthOffJet = SetVariable(tree, "offJets_ifourthCSV")
    CSVfourthOffTightJet = SetVariable(tree, "offTightJets_ifourthCSV")

    nCSVCalogeZero = SetVariable(tree, "caloJets_nCSVgeZero")
    nCSVPFgeZero = SetVariable(tree, "pfJets_nCSVgeZero")
    #nCSVOffgeZero = SetVariable(tree, "offJets_nCSVgeZero")
    nCSVOffTightgeZero = SetVariable(tree, "offTightJets_nCSVgeZero")

    
    DeepCSVleadingCaloJet = SetVariable(tree, "caloJets_ileadingDeepCSV")
    DeepCSVleadingPFJet = SetVariable(tree, "pfJets_ileadingDeepCSV")
    DeepCSVleadingOffJet = SetVariable(tree, "offJets_ileadingDeepCSV")
    DeepCSVleadingOffTightJet = SetVariable(tree, "offTightJets_ileadingDeepCSV")
    DeepCSVsecondCaloJet = SetVariable(tree, "caloJets_isecondDeepCSV")
    DeepCSVsecondPFJet = SetVariable(tree, "pfJets_isecondDeepCSV")
    DeepCSVsecondOffJet = SetVariable(tree, "offJets_isecondDeepCSV")
    DeepCSVsecondOffTightJet = SetVariable(tree, "offTightJets_isecondDeepCSV")
    DeepCSVthirdCaloJet = SetVariable(tree, "caloJets_ithirdDeepCSV")
    DeepCSVthirdPFJet = SetVariable(tree, "pfJets_ithirdDeepCSV")
    DeepCSVthirdOffJet = SetVariable(tree, "offJets_ithirdDeepCSV")
    DeepCSVthirdOffTightJet = SetVariable(tree, "offTightJets_ithirdDeepCSV")
    DeepCSVfourthCaloJet = SetVariable(tree, "caloJets_ifourthDeepCSV")
    DeepCSVfourthPFJet = SetVariable(tree, "pfJets_ifourthDeepCSV")
    DeepCSVfourthOffJet = SetVariable(tree, "offJets_ifourthDeepCSV")
    DeepCSVfourthOffTightJet = SetVariable(tree, "offTightJets_ifourthDeepCSV")

    nDeepCSVCalogeZero = SetVariable(tree, "caloJets_nDeepCSVgeZero")
    nDeepCSVPFgeZero = SetVariable(tree, "pfJets_nDeepCSVgeZero")
    #nDeepCSVOffgeZero = SetVariable(tree, "offJets_nDeepCSVgeZero")
    nDeepCSVOffTightgeZero = SetVariable(tree, "offTightJets_nDeepCSVgeZero")

    
    
    if isMC:
        genJets             = BookVector(tree,"genJets",['pt','eta','phi','mass','mcFlavour','mcPt'])

    #MET and HT
    l1HT                = SetVariable(tree,'l1HT')
    caloMet             = BookVector(tree,"caloMet",['pt','phi'])
    caloMht             = BookVector(tree,"caloMht",['pt','phi'])
    caloMhtNoPU         = BookVector(tree,"caloMhtNoPU",['pt','phi'])
    pfMet               = BookVector(tree,"pfMet",['pt','phi'])
    pfMht               = BookVector(tree,"pfMht",['pt','phi'])
    l1Met               = SetVariable(tree,'l1Met')
    l1Met_phi           = SetVariable(tree,'l1Met_phi')
    l1Mht               = SetVariable(tree,'l1Mht')
    l1Mht_phi           = SetVariable(tree,'l1Mht')
    offMet              = BookVector(tree,"offMet",['pt','phi'])
    if isMC:
        genMet              = BookVector(tree,"genMet",['pt','phi'])
    
    #Vertex
    FastPrimaryVertex   = SetVariable(tree,'FastPrimaryVertex')
    FPVPixelVertices    = SetVariable(tree,'FPVPixelVertices')
    PixelVertices       = SetVariable(tree,'PixelVertices')
    VerticesPF          = SetVariable(tree,'VerticesPF')
    VerticesL3          = SetVariable(tree,'VerticesL3')
    VerticesOff         = SetVariable(tree,'VerticesOff')
    trueVertex          = SetVariable(tree,'trueVertex')

    #General event variables
    evt                 = SetVariable(tree,'evt')
    lumi                = SetVariable(tree,'lumi')
    run                 = SetVariable(tree,'run')

    if isMC:
        pu              = SetVariable(tree,'pu')
        ptHat           = SetVariable(tree,'ptHat')
        maxPUptHat      = SetVariable(tree,'maxPUptHat')

    f.cd()

    ##get trigger names
    events.to(0)
    for event in events: break
    event.getByLabel(triggerBitLabel, triggerBits)
    names = event.object().triggerNames(triggerBits.product())
    triggerNames = names.triggerNames()
    for name in triggerNames: name = name.split("_v")[0]
    nTriggers = len(triggerNames)
    triggerVars = {}
    for trigger in triggerNames:
        triggerVars[trigger]=array( 'i', [ 0 ] )
        tree.Branch( trigger, triggerVars[trigger], trigger+'/O' )

    ##event loop
    print "Starting event loop"
    for iev,event in enumerate(events):
        #raw_input("start event")
        if iev>maxEvents and maxEvents>=0: break
        nGenHisto.Fill(1)
        #print "Event: {0}".format(iev)
        ####################################################
        ####################################################
        #Getting L1 handles
        event.getByLabel(l1Jets_label, l1Jets_source)
        event.getByLabel(l1HT_label, l1HT_source)

        #Getting Lepton handles
        event.getByLabel(offEle_label, offEle_source)
        event.getByLabel(offMu_label, offMu_source)
        event.getByLabel(MuGlobalTracks_label, MuGlobalTracks_source)
        event.getByLabel(eleLooseID_label , eleLooseID_source)
        event.getByLabel(eleTightID_label , eleTightID_source)

        #Getting Jet handles
        event.getByLabel(caloJets_label, caloJets_source)
        event.getByLabel(calobtag_label, calobtag_source)
        event.getByLabel(calodeepbtag_label, calodeepbtag_source)
        event.getByLabel(calodeepbtag_bb_label, calodeepbtag_bb_source)
        event.getByLabel(calodeepbtag_udsg_label, calodeepbtag_udsg_source)
        event.getByLabel(caloPUid_label, caloPUid_source)

        event.getByLabel(pfJets_label, pfJets_source)
        event.getByLabel(pfbtag_label, pfbtag_source)
        event.getByLabel(pfdeepbtag_label, pfdeepbtag_source)
        event.getByLabel(pfdeepbtag_bb_label, pfdeepbtag_bb_source)
        event.getByLabel(pfdeepbtag_udsg_label, pfdeepbtag_udsg_source)

        event.getByLabel(offJets_label, offJets_source)
        event.getByLabel(offJetsnoCHS_label, offJetsnoCHS_source)
        event.getByLabel(offbtag_label, offbtag_source)
        event.getByLabel(offdeepbtag_label, offdeepbtag_source)
        event.getByLabel(offdeepbtag_bb_label, offdeepbtag_bb_source)
        event.getByLabel(offdeepbtag_udsg_label, offdeepbtag_udsg_source)

        #Getting MET and HT handles
        event.getByLabel(caloMet_label, caloMet_source)
        event.getByLabel(caloMht_label, caloMht_source)
        event.getByLabel(caloMhtNoPU_label, caloMhtNoPU_source)
        event.getByLabel(pfMet_label, pfMet_source)
        event.getByLabel(pfMht_label, pfMht_source)
        event.getByLabel(offMet_label, offMet_source)

        #Getting Vertex handles
        event.getByLabel(FastPrimaryVertex_label, FastPrimaryVertex_source)
        event.getByLabel(FPVPixelVertices_label, FPVPixelVertices_source)
        event.getByLabel(PixelVertices_label, PixelVertices_source)
        event.getByLabel(VerticesPF_label, VerticesPF_source)
        event.getByLabel(VerticesL3_label, VerticesL3_source)
        event.getByLabel(VerticesOff_label, VerticesOff_source)

        #Getting Gen handles
        if isMC:
            event.getByLabel(genJets_label, genJets_source)
            event.getByLabel(genMet_label, genMet_source)
            event.getByLabel(genParticles_label, genParticles_source)
            event.getByLabel(generator_label, generator_source)
            event.getByLabel(pileUp_label, pileUp_source)


        event.getByLabel(triggerBitLabel, triggerBits)


        #####################################################
        #####################################################
        
        names = event.object().triggerNames(triggerBits.product())
        triggerspassing = []
        for i,triggerName in enumerate(triggerNames):
            index = names.triggerIndex(triggerName)
#            print "index=",index
            if checkTriggerIndex(triggerName,index,names.triggerNames()):
                triggerVars[triggerName][0] = triggerBits.product().accept(index)
                #print triggerName,"acc:",triggerBits.product().accept(index)
                if triggerName.startswith("HLT") and not ( triggerName.startswith("NoFilter") or triggerName.endswith("FirstPath") or triggerName.endswith("FinalPath")):
                    if triggerBits.product().accept(index):
                        triggerspassing.append(triggerName)
            else:
                triggerVars[triggerName][0] = 0

        # NOTE: Remove this if no trigger selection is required
        if doTriggerCut:
            if len(triggerspassing) < 1: 
                continue

        ####################################################
        ####################################################


        run[0]          = event.eventAuxiliary().run()
        lumi[0]         = event.eventAuxiliary().luminosityBlock()
        evt[0]          = event.eventAuxiliary().event()

        FastPrimaryVertex[0] = getVertex(FastPrimaryVertex_source)
        FPVPixelVertices[0] = getVertex(FPVPixelVertices_source)
        PixelVertices[0] = getVertex(PixelVertices_source)
        VerticesPF[0] = getVertex(VerticesPF_source)
        VerticesL3[0] = getVertex(VerticesL3_source)
        VerticesOff[0] = getVertex(VerticesOff_source)
        
        if isMC:
            trueVertex[0] = genParticles_source.productWithCheck().at(2).vertex().z()

        ####################################################
        ####################################################
        # Lepton Vectors
        offVertex = None
        if VerticesOff[0] > 0:
            offVertex = VerticesOff_source.productWithCheck().at(0)

        #print "Filling tight electrons"
        FillElectronVector(offEle_source, offTightElectrons, eleTightID_source.productWithCheck())
        #print "Filling loose electrons"
        FillElectronVector(offEle_source, offLooseElectrons, eleLooseID_source.productWithCheck())
        FillMuonVector(offMu_source, offTightMuons, offVertex, "tight")
        FillMuonVector(offMu_source, offLooseMuons, offVertex, "loose")

        ####################################################
        ####################################################

        
        FillVector(caloMet_source,caloMet, 0)
        FillVector(caloMht_source,caloMht, 0)
        FillVector(caloMhtNoPU_source,caloMhtNoPU, 0)
        FillVector(pfMet_source,pfMet, 0)
        FillVector(pfMht_source,pfMht, 0)

        l1Met[0],l1Met_phi[0],l1Mht[0],l1Mht_phi[0],l1HT[0] = -1,-1,-1,-1,-1
        for et in l1HT_source.productWithCheck():
            if et.getType()==ROOT.l1t.EtSum.kMissingEt:
                (l1Met[0],l1Met_phi[0]) = (et.et(),et.phi())
            elif et.getType()==ROOT.l1t.EtSum.kMissingHt:
                (l1Mht[0],l1Mht_phi[0]) = (et.et(),et.phi())
            elif et.getType()==ROOT.l1t.EtSum.kTotalEt:
                pass
            elif et.getType()==ROOT.l1t.EtSum.kTotalHt:
                l1HT[0] = et.et()

        FillVector(offMet_source,offMet, 0)

        if isMC:
            FillVector(genMet_source,genMet, 0)

        ####################################################
        ####################################################
        # Jets

        FillVector(caloJets_source,caloJets)
        FillVector(pfJets_source,pfJets)
        FillVector(l1Jets_source,l1Jets)
        FillVector(offJets_source,offJets,20)
        FillVector(offJets_source,offTightJets,30)

        
        FillBtag(calobtag_source, caloJets, caloJets.csv, caloJets.rankCSV,
                 [CSVleadingCaloJet, CSVsecondCaloJet, CSVthirdCaloJet, CSVfourthCaloJet], nCSVCalogeZero )
        FillBtag(calodeepbtag_source, caloJets, caloJets.deepcsv, caloJets.rankDeepCSV,
                 [DeepCSVleadingCaloJet, DeepCSVsecondCaloJet, DeepCSVthirdCaloJet, DeepCSVfourthCaloJet], nDeepCSVCalogeZero)
        FillBtag(calodeepbtag_bb_source, caloJets, caloJets.deepcsv_bb)
        FillBtag(calodeepbtag_udsg_source, caloJets, caloJets.deepcsv_udsg)
        FillBtag(caloPUid_source, caloJets, caloJets.puId)
        
        FillBtag(pfbtag_source, pfJets, pfJets.csv, pfJets.rankCSV,
                 [CSVleadingPFJet, CSVsecondPFJet, CSVthirdPFJet, CSVfourthPFJet], nCSVPFgeZero)        
        FillBtag(pfdeepbtag_source, pfJets, pfJets.deepcsv, pfJets.rankDeepCSV,
                 [DeepCSVleadingPFJet, DeepCSVsecondPFJet, DeepCSVthirdPFJet, DeepCSVfourthPFJet], nDeepCSVPFgeZero)
        FillBtag(pfdeepbtag_bb_source, pfJets, pfJets.deepcsv_bb)
        FillBtag(pfdeepbtag_udsg_source, pfJets, pfJets.deepcsv_udsg)
        
        FillBtag(offbtag_source, offJets, offJets.csv, offJets.rankCSV,
                 [CSVleadingOffJet, CSVsecondOffJet, CSVthirdOffJet, CSVfourthOffJet])#, nCSVOffgeZero)
        FillBtag(offdeepbtag_source, offJets, offJets.deepcsv, offJets.rankDeepCSV,
                 [DeepCSVleadingOffJet, DeepCSVsecondOffJet, DeepCSVthirdOffJet, DeepCSVfourthOffJet])#, nDeepCSVOffgeZero)
        FillBtag(offdeepbtag_bb_source, offJets, offJets.deepcsv_bb)
        FillBtag(offdeepbtag_udsg_source, offJets, offJets.deepcsv_udsg)

        FillBtag(offbtag_source, offTightJets, offTightJets.csv, offTightJets.rankCSV,
                 [CSVleadingOffTightJet, CSVsecondOffTightJet, CSVthirdOffTightJet, CSVfourthOffTightJet], nCSVOffTightgeZero)
        FillBtag(offdeepbtag_source, offTightJets, offTightJets.deepcsv, offTightJets.rankDeepCSV,
                 [DeepCSVleadingOffTightJet, DeepCSVsecondOffTightJet, DeepCSVthirdOffTightJet, DeepCSVfourthOffTightJet], nDeepCSVOffTightgeZero)
        FillBtag(offdeepbtag_bb_source, offTightJets, offTightJets.deepcsv_bb)
        FillBtag(offdeepbtag_udsg_source, offTightJets, offTightJets.deepcsv_udsg)

        
        
        if isMC:
            FillVector(genJets_source,genJets,15)

        #Matching calo jets to off and gen jets
        for i in range(caloJets.num[0]):
            caloJets.matchOff[i] = Matching(caloJets.phi[i],caloJets.eta[i],offJets)
            caloJets.matchGen[i] = -1

        #Matching pf jets to off and gen jets
        for i in range(pfJets.num[0]):
            pfJets.matchOff[i] = Matching(pfJets.phi[i],pfJets.eta[i],offJets)
            pfJets.matchGen[i] = -1

        #Matching l1 jets to off and gen jets
        for i in range(l1Jets.num[0]):
            l1Jets.matchOff[i] = Matching(l1Jets.phi[i],l1Jets.eta[i],offJets)
            l1Jets.matchGen[i] = -1

        if isMC:
            ####################################################
            # Gen patricle for Jet
            for i in range(genJets.num[0]):
                genJets.mcFlavour[i] = -100
                genJets.mcPt[i] = -100

            for i in range(caloJets.num[0]):
                caloJets.matchGen[i] = Matching(caloJets.phi[i],caloJets.eta[i],genJets)

            #Matching pf jets to off and gen jets
            for i in range(pfJets.num[0]):
                pfJets.matchGen[i] = Matching(pfJets.phi[i],pfJets.eta[i],genJets)

            #Matching l1 jets to off and gen jets
            for i in range(l1Jets.num[0]):
                l1Jets.matchGen[i] = Matching(l1Jets.phi[i],l1Jets.eta[i],genJets)
        
            #Matching gen jets to off jets
            for i in range(offJets.num[0]):
                offJets.matchGen[i] = Matching(offJets.phi[i],offJets.eta[i],genJets)

            for genParticle in genParticles_source.productWithCheck():
                if genParticle.pt()<5: continue
                if not (abs(genParticle.pdgId()) in [21,1,2,3,4,5,11,13,15]): continue
                if genParticle.mother().pt()>5 and (abs(genParticle.mother().pdgId()) in [21,1,2,3,4,5,11,13]): continue
                if evt[0]==7826939:
                    print "genParticle:"
                    print genParticle.pt(),genParticle.eta(),genParticle.phi(),genParticle.pdgId()
                    print "genJets:"
                for i in range(genJets.num[0]):
                    if genParticle.pt()<0.2*genJets.pt[i]: continue
                    if deltaR(genParticle.eta(),genParticle.phi(),genJets.eta[i],genJets.phi[i])<0.4:
                        if evt[0]==7826939:
                            print genJets.pt[i],genJets.eta[i],genJets.eta[i],genJets.mcFlavour[i]
                            print "not (int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1]):",not (int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1])
                        if abs(genParticle.pdgId())==5:
                            if genJets.mcFlavour[i]!=5 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId())==4 and not int(abs(genJets.mcFlavour[i])) in [5]:
                            if genJets.mcFlavour[i]!=4 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId())==3 and not int(abs(genJets.mcFlavour[i])) in [5,4]:
                            if genJets.mcFlavour[i]!=3 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId())==2 and not int(abs(genJets.mcFlavour[i])) in [5,4,3]:
                            if genJets.mcFlavour[i]!=2 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId())==1 and not int(abs(genJets.mcFlavour[i])) in [5,4,3,2]:
                            if genJets.mcFlavour[i]!=1 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId())==21 and not (int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1]):
                            if genJets.mcFlavour[i]!=21 or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId()) in [11,13] and not int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1,21]:
                            if not (genJets.mcFlavour[i] in [11,13]) or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId()) in [15] and not int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1,21,11,13]:
                            if not (genJets.mcFlavour[i] in [15]) or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        elif abs(genParticle.pdgId()) in [22] and not int(abs(genJets.mcFlavour[i])) in [5,4,3,2,1,21,11,13,15]:
                            if not (genJets.mcFlavour[i] in [22]) or genParticle.pt()>genJets.mcPt[i]:
                                genJets.mcFlavour[i] = genParticle.pdgId()
                                genJets.mcPt[i]      = genParticle.pt()
                        if evt[0]==7826939:
                            print "newFlav:",genJets.mcFlavour[i]

        ####################################################
        ####################################################


        
        if isMC:
            if bunchCrossing>=pileUp_source.productWithCheck().size() or pileUp_source.productWithCheck().at(bunchCrossing).getBunchCrossing()!=0:
                found=False
                for bunchCrossing in range(pileUp_source.productWithCheck().size()):
                    if pileUp_source.productWithCheck().at(bunchCrossing).getBunchCrossing() == 0 :
                        found=True;
                        break
                if not found:
                    Exception("Check pileupSummaryInfos!")
                print "I'm using bunchCrossing=",bunchCrossing
            pu[0] = pileUp_source.productWithCheck().at(bunchCrossing).getTrueNumInteractions()
            ptHat[0]    = generator_source.product().qScale()

            maxPUptHat[0] = -1
            for ptHat_ in pileUp_source.productWithCheck().at(bunchCrossing).getPU_pT_hats():
                maxPUptHat[0] = max(maxPUptHat[0],ptHat_)
                
        if iev%10==1: print "Event: ",iev," done."
        nPassHisto.Fill(1)
        tree.Fill()
        
    f.Write()
    f.Close()

if __name__ == "__main__":
    secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_GEN-SIM-RAW_LS-1803to1803-2332to2332-2870to2871.root"]
    #secondaryFiles = ["file:/afs/cern.ch/work/k/koschwei/trigger/data/MuonEG_Run299368_v1_Run2017C_RAW_LS-79to90.root"]
    filesInput = ["file:/afs/cern.ch/work/k/koschwei/public/ttbar_RunIISummer17DRStdmix_92X_upgrade2017_AODSIM_LS-1803to1803-2134to2134-2332to2332-2870to2871-4384to4385-6032to6033-6481to6481.root"]
    #filesInput = ["file:/afs/cern.ch/work/k/koschwei/trigger/data/MuonEG_Run299368_PromptReco-v1_Run2017C_AOD_LS-79to90-115to129.root"]
    fileOutput = "tree.root"
    maxEvents = 100
    launchNtupleFromHLT(fileOutput,filesInput,secondaryFiles,maxEvents, preProcessing=False, MC=True)
