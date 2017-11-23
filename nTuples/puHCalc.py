import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)


datafile = "/mnt/t3nfs01/data01/shome/koschwei/PUDataRunC2017.root"
mcfile = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v3/ttbar/ttbar_v3.root"

tdatafile = ROOT.TFile.Open(datafile)
tmcfile = ROOT.TFile.Open(mcfile)

hData = tdatafile.Get("pileup")
MCtree = tmcfile.Get("tree")

hMC = ROOT.TH1F("hMC","hMC",70,0,70)

MCtree.Project("hMC","pu")
outfile = ROOT.TFile("PUreweighting.root","recreate")
outfile.cd()


c1 = ROOT.TCanvas("c1","c1",800,600)
c1.cd()

nData = hData.Integral()
nMC = hMC.Integral()

hData.Scale(1/float(nData))
hMC.Scale(1/float(nMC))

hData.Write()
hMC.Write()

hData.Draw("")
c1.Update()
#raw_input("press ret")
hMC.Draw("")
c1.Update()
#raw_input("press ret")

hpuw = hData.Clone()
hpuw.SetName("weight")
hpuw.SetTitle("weight")

hpuw.Divide(hMC)
hpuw.Write()
hpuw.Draw("")
c1.Update()

print "std::map<int, float> weights;"
for i in range(70):
    print "weights[{0}] = {1};".format(i-1, hpuw.GetBinContent(i))
    

outfile.Write()

#raw_input("press ret")
