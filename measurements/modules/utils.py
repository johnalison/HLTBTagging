import logging
import logging.config
import os
import json
import ROOT
from ConfigParser import SafeConfigParser

def setup_logging( default_path='config/logging.json', default_level=logging.INFO,
                   logname = "output", errname = "error", loglevel = 20):
    """
    Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        #Overwrite config definitions with command line arguments (Default is same as in config)
        config["handlers"]["info_file_handler"]["filename"] = "logs/"+logname+".log"
        config["handlers"]["error_file_handler"]["filename"] = "logs/"+errname+".log"
        config["handlers"]["console"]["level"] = loglevel
        config["handlers"]["info_file_handler"]["level"] = loglevel
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



def savePlot(canvas, outputname, outputformat):
    #TODO: Make something with multipage pdf support
    logging.info("Writing file {0}.{1}".format(outputname.replace(".",""), outputformat))
    canvas.Print("{0}.{1}".format(outputname.replace(".",""), outputformat))



def getLegend(ObjetList, xstart, ystart, xend, yend, usingPlotBase = True):
    leg = ROOT.TLegend(xstart, ystart, xend, yend)
    if usingPlotBase:
        for Object, histo in ObjetList:
            if len(Object.legend) == 1:
                leg.AddEntry(histo, Object.legend[0], Object.legendstyle)
    else:
        for  obj, text, style in ObjetList:
            leg.AddEntry(obj, text, style)        

    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetFillStyle(0)
            
    return leg


def getCMStext(WiP = True, additionaltext = ""):
    styleconfig = SafeConfigParser()
    #logging.debug("Loading style config")
    styleconfig.read("config/plotting.cfg")

    CMSscale = styleconfig.getfloat("CMSLabel","cmsScale")
    
    if additionaltext not in ["", "Prelim","Supp","Sim"]:
        logging.warning("CMS additinal text required in {0}".format(["WiP","Prelim","Supp","Sim"]))
        logging.warning("Ignoring additional Text")

    firstline = '#scale['+str(CMSscale)+']{#bf{CMS}}'
    if additionaltext == "Sim":
        firstline += " #it{Simulation}"
    elif additionaltext == "Supp":
        firstline += " #it{Supplementary}"
    elif additionaltext == "Prelim":
        firstline += " #it{Preliminary}"
    else:
        pass

    xstart = styleconfig.getfloat("CMSLabel","xStart")
    
    cmsfistLine = ROOT.TLatex(xstart, styleconfig.getfloat("CMSLabel","yStartFirstLine"), firstline)
    cmsfistLine.SetTextFont(42)
    cmsfistLine.SetTextSize(styleconfig.getfloat("CMSLabel","textsize"))
    cmsfistLine.SetNDC()

    if WiP:
        cmssecondline = ROOT.TLatex(xstart, styleconfig.getfloat("CMSLabel","yStartSecondLine"), '#it{work in progress}')
    else:
        cmssecondline = ROOT.TLatex(xstart, styleconfig.getfloat("CMSLabel","yStartSecondLine"), '')
    cmssecondline.SetTextFont(42)
    cmssecondline.SetTextSize(styleconfig.getfloat("CMSLabel","textsize"))
    cmssecondline.SetNDC()

    return cmsfistLine, cmssecondline

def getLabel(text, xstart, pos = "top", scale = 1):
    if pos in ["top", "topSup", "under"]:
        postouse = pos
    elif isinstance(pos, float) or isinstance(pos, int):
        postouse = float(pos)
    else:
        logging.warning("Position parameter required in {0} or of type float/int".format(["top", "topSup", "under"]))
        logging.warning("Falling back to top position")
        postouse = "top"

        
    styleconfig = SafeConfigParser()
    styleconfig.read("config/plotting.cfg")

    if pos == "top":
        ystart = styleconfig.getfloat("GeneralLabel","topPos")
    elif pos == "topSup":
        ystart = styleconfig.getfloat("GeneralLabel","topSupPos")
        scale = scale * styleconfig.getfloat("GeneralLabel","topSupScale")
    else:
        ystart = styleconfig.getfloat("GeneralLabel","underPos")

    label = ROOT.TLatex(xstart, ystart, '#scale['+str(scale)+']{'+text+'}')
        
    label.SetTextFont(42)
    label.SetTextSize(styleconfig.getfloat("CMSLabel","textsize"))
    label.SetNDC()

    return label


def getAxisTitle(variable, number, order = "pt"):
    numberDictPt = {0 : "leading",
                    1 : "second",
                    2 : "third",
                    3 : "fourth",
                    4 : "fifth",
                    5 : "sixth",
                    6 : "seventh"}
    numberDictCSV = {0 : "",
                     1 : "second",
                     2 : "third",
                     3 : "fourth",
                     4 : "fifth",
                     5 : "sixth",
                     6 : "seventh"}

    nicevars = {"pt" : "p_{T}",
                "csv" : "CSV Value",
                "deepcsv" : "DeepCSV Value"}

    if not variable in nicevars.keys():
        logging.waring("Variables not in dict with nice names. Just using the variable")
        nicename = variable
    else:
        nicename = nicevars[variable]

    if not number in numberDictPt.keys():
        logging.waring("Variables not in dict with nice number Just using the number")
        nicenumber = number
    else:
        if numberDictPt:
            nicenumber = numberDictPt[number]
        else:
            nicenumber = numberDictCSV[number]
            
    if order == "pt":
        return "{0} of {1} jet".format(nicename, nicenumber)
    elif order == "csv":
        return "{0} of jet with {1} highest CSV".format(nicename, nicenumber)
    elif order == "deepcsv":
        return "{0} of jet with {1} highest DeepCSV".format(nicename, nicenumber)
    else:
        logging.error("Order not defined. Returning empty sting")
        return ""


def tupleList2List(tuplelist, index):
    if index >= len(tuplelist[0]):
        logging.warning("Index >= number of elements in tuple. Setting index to highest number!")
        index = len(tuplelist[0])-1
    retlist = []
    for elem in tuplelist:
        retlist.append(elem[index])

    return retlist
    
