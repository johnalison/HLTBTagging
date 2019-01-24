import ROOT
from modules.plotting import moveOverUnderFlow


#ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
ROOT.gROOT.LoadMacro("modules/functions.h+")
outfileName = "CSVDist_FlavSplit_noBtag"

files = {
    "ttbar" : "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/ttbar/ttbar_98p0_mod_mod_mod_mod_mod_mod.root",
    "ST_tW" : "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/ST/ST_tW_part_mod_mod_mod.root",
    "ST_tbarW" : "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/SantiT/ST_antitW_mod_mod_mod.root"
}

nGen = {
    "ttbar" : 941634,
    "ST_tW" : 727212,
    "ST_tbarW" : 5603226,
    }
xsec = {
    "ttbar" : 88.34,
    "ST_tW" : 35.85,
    "ST_tbarW" : 35.85,
    }

VarSelection = "Sum$(offCleanJets_pt > 30 && abs(offCleanJets_eta) < 2.4) >= 2"
#VarSelection = "Sum$(offCleanJets_deepcsv > 0.8001 && offCleanJets_pt > 30 && abs(offCleanJets_eta) < 2.4) >= 1 && Sum$(offCleanJets_pt > 30 && abs(offCleanJets_eta) < 2.4) >= 2"
TriggerSelection = "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4 > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4 > 0"
LeptonSelection = "Sum$((abs(offTightElectrons_superClusterEta) <= 1.4442 || abs(offTightElectrons_superClusterEta) >= 1.5660) && offTightElectrons_pt > 30 && abs(offTightElectrons_eta) < 2.4) == 1 && Sum$(offTightMuons_iso < 0.25 && offTightMuons_pt > 20 && abs(offTightMuons_eta) < 2.4) == 1"

eventSelection = "({0}) && ({1}) && ({2})".format(VarSelection, TriggerSelection, LeptonSelection)
puweight = "get_puWeight_CDF(pu) * offTightElectrons_SF[0] * offTightMuons_SF[0]"


hBase = ROOT.TH1F("hBase","hBase",100, 0, 1)

histos = {
    "hAll" :  hBase.Clone("hAll"),
    "BJets" : hBase.Clone("hBJets"),
    "CJets" : hBase.Clone("hCJets"),
    "LJets" : hBase.Clone("hLJets"),
}
histosPF = {
    "BJets" : hBase.Clone("hBJetsPF"),
    "CJets" : hBase.Clone("hCJetsPF"),
    "LJets" : hBase.Clone("hLJetsPF"),
}
histosCalo = {
    "BJets" : hBase.Clone("hBJetsCalo"),
    "CJets" : hBase.Clone("hCJetsCalo"),
    "LJets" : hBase.Clone("hLJetsCalo"),
}

bJetIdent = "offCleanJets_hadronFlavour == 5"
cJetIdent = "offCleanJets_hadronFlavour == 4"
lJetIdent = "offCleanJets_hadronFlavour == 0"

for key in files:
    rFile = ROOT.TFile(files[key], "READ")
    tree = rFile.Get("tree")

    thisHistos = {}
    thisHistosPF = {}
    thisHistosCalo = {}
    
    for histoKey in histos:
        thisHistos[histoKey] = histos[histoKey].Clone(histos[histoKey].GetName()+"_"+key)
    for histoKey in histosPF:
        thisHistosPF[histoKey] = histos[histoKey].Clone(histos[histoKey].GetName()+"_"+key)
    for histoKey in histosCalo:
        thisHistosCalo[histoKey] = histos[histoKey].Clone(histos[histoKey].GetName()+"_"+key)

    print tree.Project(thisHistos["hAll"].GetName(),"offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, "1", 14000*xsec[key]/nGen[key]))
    print tree.Project(thisHistos["BJets"].GetName(),"offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, bJetIdent, 14000*xsec[key]/nGen[key]))
    print tree.Project(thisHistos["CJets"].GetName(),"offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, cJetIdent, 14000*xsec[key]/nGen[key]))
    print tree.Project(thisHistos["LJets"].GetName(),"offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, lJetIdent, 14000*xsec[key]/nGen[key]))

    print "offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, bJetIdent, 14000*xsec[key]/nGen[key])
    print "offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, cJetIdent, 14000*xsec[key]/nGen[key])
    print "offCleanJets_csv","({0} && {2}) * ({1} * {3})".format(eventSelection, puweight, lJetIdent, 14000*xsec[key]/nGen[key])
    
    tree.Project(thisHistosPF["BJets"].GetName(),"pfJets_csv","({0} && {2} && offCleanJets_matchPF >= 0 && pfJets_pt > 30 && abs(pfJets_eta) < 2.4) * ({1} * {3})".format(eventSelection, puweight, bJetIdent, 14000*xsec[key]/nGen[key]))
    tree.Project(thisHistosPF["CJets"].GetName(),"pfJets_csv","({0} && {2} && offCleanJets_matchPF >= 0 && pfJets_pt > 30 && abs(pfJets_eta) < 2.4) * ({1} * {3})".format(eventSelection, puweight, cJetIdent, 14000*xsec[key]/nGen[key]))
    tree.Project(thisHistosPF["LJets"].GetName(),"pfJets_csv","({0} && {2} && offCleanJets_matchPF >= 0 && pfJets_pt > 30 && abs(pfJets_eta) < 2.4) * ({1} * {3})".format(eventSelection, puweight, lJetIdent, 14000*xsec[key]/nGen[key]))

    tree.Project(thisHistosCalo["BJets"].GetName(),"caloJets_csv","({0} && {2} && offCleanJets_matchCalo >= 0 && caloJets_pt > 20) * ({1} * {3})".format(eventSelection, puweight, bJetIdent, 14000*xsec[key]/nGen[key]))
    tree.Project(thisHistosCalo["CJets"].GetName(),"caloJets_csv","({0} && {2} && offCleanJets_matchCalo >= 0 && caloJets_pt > 20) * ({1} * {3})".format(eventSelection, puweight, cJetIdent, 14000*xsec[key]/nGen[key]))
    tree.Project(thisHistosCalo["LJets"].GetName(),"caloJets_csv","({0} && {2} && offCleanJets_matchCalo >= 0 && caloJets_pt > 20) * ({1} * {3})".format(eventSelection, puweight, lJetIdent, 14000*xsec[key]/nGen[key]))

    moveOverUnderFlow(histos["hAll"])
    moveOverUnderFlow(histos["BJets"])
    moveOverUnderFlow(histos["CJets"])
    moveOverUnderFlow(histos["LJets"])

    moveOverUnderFlow(histosPF["BJets"])
    moveOverUnderFlow(histosPF["CJets"])
    moveOverUnderFlow(histosPF["LJets"])

    moveOverUnderFlow(histosCalo["BJets"])
    moveOverUnderFlow(histosCalo["CJets"])
    moveOverUnderFlow(histosCalo["LJets"])

    histos["hAll"].Add(thisHistos["hAll"])
    histos["BJets"].Add(thisHistos["BJets"])
    histos["CJets"].Add(thisHistos["CJets"])
    histos["LJets"].Add(thisHistos["LJets"])

    histosPF["BJets"].Add(thisHistosPF["BJets"])
    histosPF["CJets"].Add(thisHistosPF["CJets"])
    histosPF["LJets"].Add(thisHistosPF["LJets"])

    histosCalo["BJets"].Add(thisHistosCalo["BJets"])
    histosCalo["CJets"].Add(thisHistosCalo["CJets"])
    histosCalo["LJets"].Add(thisHistosCalo["LJets"])


outFile = ROOT.TFile(outfileName+".root","RECREATE")
outFile.cd()

histos["hAll"].Write()
histos["BJets"].Write()
histos["CJets"].Write()
histos["LJets"].Write()

histosPF["BJets"].Write()
histosPF["CJets"].Write()
histosPF["LJets"].Write()

histosCalo["BJets"].Write()
histosCalo["CJets"].Write()
histosCalo["LJets"].Write()
