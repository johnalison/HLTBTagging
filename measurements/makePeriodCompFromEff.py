import os
import json
import logging
import logging.config
from modules.utils import setup_logging, getLabel
from ConfigParser import SafeConfigParser

import ROOT

import modules.DataMC
import modules.compPlot

styleconfig = SafeConfigParser()
#logging.debug("Loading style config")
styleconfig.read("config/plotting.cfg")


loglev = 20

setup_logging(loglevel = loglev, logname = "shapeoutput", errname = "shapeerror")

logger = logging.getLogger(__name__)

logger.info("Starting flavour composition analysis")

if loglev > 0:
    ROOT.gErrorIgnoreLevel = ROOT.kError# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;

basepath = "/mnt/t3nfs01/data01/shome/koschwei/trigger/onlineBTV/CMSSW_9_2_12_patch1/src/HLTBTagging/measurements/v5nTuples/lepoverlap/FlavourSplitting/"

runCDinput = ["RunCD/PFCSV/DeepCSVMPresel_phase1_RunCD_TnP_leading_pf_csv_histos.root",
              "RunCD/CaloCSV/DeepCSVMPresel_phase1_RunCD_TnP_leading_calo_csv_histos.root",
              "RunCD/PFDeepCSV/DeepCSVMPresel_phase1_RunCD_TnP_leading_pf_deepcsv_histos.root",
              "RunCD/CaloDeepCSV/DeepCSVMPresel_phase1_RunCD_TnP_leading_calo_deepcsv_histos.root"]

runEinput = ["RunE/PFCSV/DeepCSVMPresel_phase1_RunE_TnP_leading_pf_csv_histos.root",
             "RunE/CaloCSV/DeepCSVMPresel_phase1_RunE_TnP_leading_calo_csv_histos.root",
             "RunE/PFDeepCSV/DeepCSVMPresel_phase1_RunE_TnP_leading_pf_deepcsv_histos.root",
             "RunE/CaloDeepCSV/DeepCSVMPresel_phase1_RunE_TnP_leading_calo_deepcsv_histos.root"]

runFinput = ["RunF/PFCSV/DeepCSVMPresel_phase1_RunF_TnP_leading_pf_csv_histos.root",
             "RunF/CaloCSV/DeepCSVMPresel_phase1_RunF_TnP_leading_calo_csv_histos.root",
             "RunF/PFDeepCSV/DeepCSVMPresel_phase1_RunF_TnP_leading_pf_deepcsv_histos.root",
             "RunF/CaloDeepCSV/DeepCSVMPresel_phase1_RunF_TnP_leading_calo_deepcsv_histos.root"]

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen-2]

histoname = ["0.975_denom_data","0.97_denom_data","0.955_denom_data","0.95_denom_data"]

for iplot, plot in enumerate(["PFCSV", "CaloCSV", "PFDeepCSV", "CaloDeepCSV"]):
    logging.info("Making plot: {0}".format(plot))
    
    CDRfile = ROOT.TFile.Open(basepath+runCDinput[iplot])
    ERfile = ROOT.TFile.Open(basepath+runEinput[iplot])
    FRfile = ROOT.TFile.Open(basepath+runFinput[iplot])
    
    hCD = CDRfile.Get(histoname[iplot])
    hE = ERfile.Get(histoname[iplot])
    hF = FRfile.Get(histoname[iplot])

    hCD.GetYaxis().SetTitleOffset(hCD.GetYaxis().GetTitleOffset()*
                                  styleconfig.getfloat("HistoStyle","yTitleOffsetscale")*
                                  styleconfig.getfloat("HistoStyle","yRatioTitleOffsetscale"))
    
    modules.compPlot.compareHistos([hCD, hE, hF], ["MuonEG Run C+D", "MuonEG Run E", "MuonEG Run F"], colors,
                                   normalized = True, drawRatio = True, outname = basepath+"RunComp_{0}".format(plot))

WPdict = { "PFCSV" : [0.405, 0.840, 0.975],
           "CaloCSV" : [0.435, 0.840, 0.97],
           "PFDeepCSV" : [0.2, 0.67, 0.955],
           "CaloDeepCSV" : [0.205, 0.675, 0.95] }

results = {"PFCSV" : {},
           "CaloCSV" : {},
           "PFDeepCSV" : {},
           "CaloDeepCSV" : {}}

for iplot, plot in enumerate(["PFCSV", "CaloCSV", "PFDeepCSV", "CaloDeepCSV"]):
    logging.info("Esimating efficiency difference for {0}".format(plot))
    WPs = WPdict[plot]

    CDRfile = ROOT.TFile.Open(basepath+runCDinput[iplot])
    ERfile = ROOT.TFile.Open(basepath+runEinput[iplot])
    FRfile = ROOT.TFile.Open(basepath+runFinput[iplot])
    
    hCDfull = CDRfile.Get(histoname[iplot])
    hEfull = ERfile.Get(histoname[iplot])
    hFfull = FRfile.Get(histoname[iplot])
    
    CDSF = 1/hCDfull.Integral()
    ESF = 1/hEfull.Integral()
    FSF = 1/hFfull.Integral()

    hCDfull.Scale(CDSF)
    hEfull.Scale(ESF)
    hFfull.Scale(FSF)
    
    #hEfull.Draw("histoe")
    
    hpostfix = "_num_data"

    for WP in WPs:
        results[plot][WP] = {}
        logging.info("Processing WP {0}".format(WP))
        hCDonline = CDRfile.Get(str(WP)+hpostfix)
        hEonline = ERfile.Get(str(WP)+hpostfix)
        hFonline = FRfile.Get(str(WP)+hpostfix)

        hCDonline.Scale(CDSF)
        hEonline.Scale(ESF)
        hFonline.Scale(FSF)

        CDratio2CD = hCDonline.Integral()/hCDonline.Integral()
        Eratio2CD = hEonline.Integral()/hCDonline.Integral()
        Fratio2CD = hFonline.Integral()/hCDonline.Integral()

        results[plot][WP]["CD"] = CDratio2CD-1
        results[plot][WP]["E"] = Eratio2CD-1
        results[plot][WP]["F"] = Fratio2CD-1
        



for iplot, plot in enumerate(["PFCSV", "CaloCSV", "PFDeepCSV", "CaloDeepCSV"]):
    WPs = WPdict[plot]
    table  = "\\documentclass[11pt]{standalone} \n"
    table += "\\usepackage{booktabs} \n"
    table += "\\begin{document} \n"
    table += "\\begin{tabular}{ r c c } \n"
    table += "\\toprule \n"
    table += "WP & Run E  & Run F \\\\ \n"
    table += "\\midrule \n"
    for WP in WPs:
        table += "{0} & {1:.2f} \% & {2:.2f} \% \\\\ \n".format(WP, results[plot][WP]["E"]*100, results[plot][WP]["F"]*100) 
    table += "\\bottomrule \n"
    table += "\end{tabular} \n"
    table += "\end{document} \n"
    effestoutname = basepath+"effEstimation_{0}.tex".format(plot)
    with open(effestoutname, "w") as f:
        f.write(table)
        
        

