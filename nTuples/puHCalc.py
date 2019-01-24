import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(False)

import sys

cpp = True

datafile = sys.argv[1]
mcfile = [("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/ttbar/ttbar_98p0.root",88.34,941634),
          ("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/ST/ST_tW_part.root",35.85,727212),
          ("/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v10/SantiT/ST_antitW.root",35.85,5603226)]

print "Using datafile: {0}".format(datafile)
print "Using mcfile: {0}".format(mcfile)

tdatafile = ROOT.TFile.Open(datafile)


hData = tdatafile.Get("pileup")
iAdded = 0
hMCSum = ROOT.TH1F("hMC","hMC",90,0,90)
for mcf, xs, ngen in mcfile:
    tmcfile = ROOT.TFile.Open(mcf)
    MCtree = tmcfile.Get("tree")
    hMC = ROOT.TH1F("hMC_"+str(iAdded),"hMC_"+str(iAdded),90,0,90)
    MCtree.Project("hMC_"+str(iAdded),"pu",str(xs/ngen))
    iAdded += 1
    hMCSum.Add(hMC)



outfile = ROOT.TFile("PUreweighting_{0}".format(datafile),"recreate")
outfile.cd()


c1 = ROOT.TCanvas("c1","c1",800,600)
c1.cd()

nData = hData.Integral()
nMC = hMCSum.Integral()

hData.Scale(1/float(nData))
hMCSum.Scale(1/float(nMC))

hData.Write()
hMCSum.Write()

hData.Draw("")
c1.Update()
#raw_input("press ret")
hMCSum.Draw("")
c1.Update()
#raw_input("press ret")

hpuw = hData.Clone()
#hpuw.SetName("weight")
#hpuw.SetTitle("weight")

hpuw.Divide(hMCSum)
hpuw.Write()
hpuw.Draw("")
c1.Update()

if cpp:
    print "std::map<int, float> weights;"
    for i in range(100):
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
