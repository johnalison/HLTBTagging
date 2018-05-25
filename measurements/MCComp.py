import time
import ROOT
import os


from DataFormats.FWLite import Handle, Events
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

def FillHistos(files, hpt, hcsv, hptLeading, hcsvLeading, hpu, maxEvents = -1):
    eventsOff = Events(files)

    
    pileUp_source, pileUp_label                         = Handle("vector<PileupSummaryInfo>"), ("slimmedAddPileupInfo")
    offJets_source, offJets_label = Handle("vector<pat::Jet>"), ("slimmedJets")

    for i,event in enumerate(eventsOff):
        if i%10000==0:
            print "Processing event {0:10}".format(i)
        if maxEvents != -1 and i > maxEvents:
            break
            
        event.getByLabel(offJets_label, offJets_source)
        event.getByLabel(pileUp_label, pileUp_source)
        bunchCrossing = 12
        if pileUp_source.isValid():
            if bunchCrossing>=pileUp_source.product().size() or pileUp_source.product().at(bunchCrossing).getBunchCrossing()!=0:
                    found=False
                    for bunchCrossing in range(pileUp_source.product().size()):
                        if pileUp_source.product().at(bunchCrossing).getBunchCrossing() == 0 :
                            found=True;
                            break
                    if not found:
                        Exception("Check pileupSummaryInfos!")
                    print "I'm using bunchCrossing=",bunchCrossing
            pu = pileUp_source.product().at(bunchCrossing).getTrueNumInteractions()
        else:
            print "!!!!!!"

        if pu < 20 or pu > 70:
            continue
        
        hpu.Fill(pu)
        if offJets_source.isValid():
            leadingFilled = False
            for Jet in offJets_source.product():
                if Jet.pt() > 30 and abs(Jet.eta()) < 2.4:
                    hpt.Fill(Jet.pt())
                    hcsv.Fill(Jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"))
                    if not leadingFilled:
                        hptLeading.Fill(Jet.pt())
                        hcsvLeading.Fill(Jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"))
                        leadingFilled = True
    return i

def drawInOrder(h1, h2, normalized = True):
    h1Zero = False
    h2Zero = False
    
    if normalized:
        try:
            i = 1/float(h1.Integral())
        except ZeroDivisionError:
            print "ZeroDivisionError h1"
        else:
            h1.Scale(1/float(h1.Integral()))
        try:
            i = 1/float(h2.Integral())
        except ZeroDivisionError:
            print "ZeroDivisionError h2"
        else:
            h2.Scale(1/float(h2.Integral()))
    
    max1 = h1.GetMaximum()
    max2 = h2.GetMaximum()

    if max1 > max2:
        h1.DrawNormalized("histoe")
        h2.DrawNormalized("histoesame")
    else:
        h2.DrawNormalized("histoe")
        h1.DrawNormalized("histoesame")

hOffPu = ROOT.TH1F("hOffPu", "hOffPu",70,10,80)
hTSGPu = ROOT.TH1F("hTSGPu", "hTSGPu", 70,10,80)

hOffpt = ROOT.TH1F("hOffpt","hOffpt",80,30,600)
hOffcsv = ROOT.TH1F("hOffcsv","hOffcsv",40,0,1)

hTSGpt = ROOT.TH1F("hTSGpt","hTSGpt",80,30,600)
hTSGcsv = ROOT.TH1F("hTSGcsv","hTSGcsv",40,0,1)

hOffpt_leading = ROOT.TH1F("hOffpt_leading","hOffpt_leading",100,30,500)
hOffcsv_leading = ROOT.TH1F("hOffcsv_leading","hOffcsv_leading",40,0,1)

hTSGpt_leading = ROOT.TH1F("hTSGpt_leading","hTSGpt_leading",100,30,500)
hTSGcsv_leading = ROOT.TH1F("hTSGcsv_leading","hTSGcsv_leading",40,0,1)

hTSGpt.SetLineColor(ROOT.kRed)
hTSGcsv.SetLineColor(ROOT.kRed)
hTSGpt_leading.SetLineColor(ROOT.kRed)
hTSGcsv_leading.SetLineColor(ROOT.kRed)
hTSGPu.SetLineColor(ROOT.kRed)

hOffPu.GetXaxis().SetTitle("PU")
hTSGPu.GetXaxis().SetTitle("PU")

hOffpt.GetXaxis().SetTitle("Jet pt")
hOffcsv.GetXaxis().SetTitle("Jet csv")
hOffpt_leading.GetXaxis().SetTitle("Leading jet pt")
hOffcsv_leading.GetXaxis().SetTitle("Leading jet csv")
hTSGpt.GetXaxis().SetTitle("Jet pt")
hTSGcsv.GetXaxis().SetTitle("Jet csv")
hTSGpt_leading.GetXaxis().SetTitle("Leading jet pt")
hTSGcsv_leading.GetXaxis().SetTitle("Leading jet csv")


hOffpt.GetYaxis().SetTitle("Normalized Units")
hOffcsv.GetYaxis().SetTitle("Normalized Units")
hOffpt_leading.GetYaxis().SetTitle("Normalized Units")
hOffcsv_leading.GetYaxis().SetTitle("Normalized Units")
hTSGpt.GetYaxis().SetTitle("Normalized Units")
hTSGcsv.GetYaxis().SetTitle("Normalized Units")
hTSGpt_leading.GetYaxis().SetTitle("Normalized Units")
hTSGcsv_leading.GetYaxis().SetTitle("Normalized Units")

hOffPu.SetTitle("")
hTSGPu.SetTitle("")
hOffpt.SetTitle("")
hOffcsv.SetTitle("")
hOffpt_leading.SetTitle("")
hOffcsv_leading.SetTitle("")
hTSGpt.SetTitle("")
hTSGcsv.SetTitle("")
hTSGpt_leading.SetTitle("")
hTSGcsv_leading.SetTitle("")

print "Starting with official MC"
iProcessedOff = FillHistos([ "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/523E450B-CB41-E811-AACA-001E6739B849.root"],
                           hOffpt,
                           hOffcsv,
                           hOffpt_leading,
                           hOffcsv_leading,
                           hOffPu,
#                           maxEvents = 5000
)

print "Starting with TSG MC"
iProcessedTSG = FillHistos(["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/TSG_94X_mc2017_realistic_v11-v1/30000/92D0311B-7E1F-E811-B892-FA163E296D08.root"],
                           hTSGpt,
                           hTSGcsv,
                           hTSGpt_leading,
                           hTSGcsv_leading,
                           hTSGPu,
#                           maxEvents = 5000
)



c1 = ROOT.TCanvas("c1", "c1", 800, 600)

leg = ROOT.TLegend(0.6,0.65,0.9,0.9)
leg.AddEntry(hOffpt, "Official MC ({0})".format(iProcessedOff))
leg.AddEntry(hTSGpt, "TSG MC ({0})".format(iProcessedTSG))

drawInOrder(hOffPu, hTSGPu)
leg.Draw("same")
c1.Update()
c1.Print("MCComp.pdf(","pdf")


drawInOrder(hOffpt, hTSGpt)
leg.Draw("same")
c1.Update()
c1.Print("MCComp.pdf","pdf")


drawInOrder(hOffpt_leading, hTSGpt_leading)
leg.Draw("same")
c1.Update()
c1.Print("MCComp.pdf","pdf")

leg = ROOT.TLegend(0.1,0.65,0.4,0.9)
leg.AddEntry(hOffpt, "Official MC ({0})".format(iProcessedOff))
leg.AddEntry(hTSGpt, "TSG MC ({0})".format(iProcessedTSG))

drawInOrder(hOffcsv, hTSGcsv)
leg.Draw("same")
c1.Update()
c1.Print("MCComp.pdf","pdf")

drawInOrder(hOffcsv_leading, hTSGcsv_leading)
leg.Draw("same")
c1.Update()
c1.Print("MCComp.pdf)","pdf")


    
