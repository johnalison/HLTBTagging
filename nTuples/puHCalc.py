import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

import sys

cpp = False

datafile = sys.argv[1]
mcfile = "ttbar_v3.root"

print "Using datafile: {0}".format(datafile)
print "Using mcfile: {0}".format(mcfile)

tdatafile = ROOT.TFile.Open(datafile)
tmcfile = ROOT.TFile.Open(mcfile)

hData = tdatafile.Get("pileup")
MCtree = tmcfile.Get("tree")

hMC = ROOT.TH1F("hMC","hMC",90,0,90)

MCtree.Project("hMC","pu")
outfile = ROOT.TFile("PUreweighting_{0}".format(datafile),"recreate")
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

if cpp:
    print "std::map<int, float> weights;"
    for i in range(70):
        print "weights[{0}] = {1};".format(i-1, hpuw.GetBinContent(i))
else:
    string = "puWeights = {"
    non0bins = "pubins = ["
    for i in range(90):
        if hpuw.GetBinContent(i) != 0:
            non0bins += "{0},".format(i)
            string += "{0} : {1}, ".format(i-1, hpuw.GetBinContent(i))
    string = string[0:-2]+"}"
    non0bins = non0bins[0:-1]+"]"
    print non0bins
    print string
outfile.Write()

#raw_input("press ret")
