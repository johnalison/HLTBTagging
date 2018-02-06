import ROOT
from array import array

import os


def printDict(input_, nElem = 8, EIOs = ["csv","pt","deepcsv"]):
    for key in input_:
        printEle = False
        for EIO in EIOs:
            if EIO in key and not EIO+"_" in key and not "LeptVeto" in key:
                printEle = True

        if "num" in key and not "num]" in key:
            printEle = True
        elems = "[ "
        if len(input_[key]) < nElem:
            nE = len(input_[key])
        else:
            nE = nElem
        for i in range(nE):
            elems += str(input_[key][i]) + " "
        elems += "]"
        if printEle:
            print key, elems




def addCleanJetsSorting(inputfile, debug = False, skipevents = 0):
    branchPrefixIn = "offCleanJets"
    lenVar = "offCleanJets_num"

    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))

    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")


    branchlist = []
    brancharrays = {}
    CSVbrancharrays = {}
    DeepCSVbrancharrays = {}

    newBrnaches = []
    for branch in tree.GetListOfBranches():
        if branch.GetName().startswith(branchPrefixIn):
            branchlist.append(branch.GetName())
            if branch.GetName().startswith(branchPrefixIn+"_num"):
                brancharrays[branch.GetName()] = array("i",[0])
            else:
                brancharrays[branch.GetName()] = array("f",20*[-99])
            tree.SetBranchAddress( branch.GetName() , brancharrays[branch.GetName()] )    

            newbranchNameCSV = branch.GetName().replace("Clean","CleanCSV")
            newbranchNameDeepCSV = branch.GetName().replace("Clean","CleanDeepCSV")

            if branch.GetName().startswith(branchPrefixIn+"_num"):
                #print newbranchNameCSV
                #print newbranchNameDeepCSV
                CSVbrancharrays[newbranchNameCSV] = array("i",[0])
                DeepCSVbrancharrays[newbranchNameDeepCSV] = array("i",[0])

                #print DeepCSVbrancharrays



                newBrnaches.append(tree.Branch(newbranchNameCSV, CSVbrancharrays[newbranchNameCSV], newbranchNameCSV+"/I"))
                newBrnaches.append(tree.Branch(newbranchNameDeepCSV, DeepCSVbrancharrays[newbranchNameDeepCSV], newbranchNameDeepCSV+"/I"))
            else:
                CSVbrancharrays[newbranchNameCSV] = array("f",20*[-99])
                DeepCSVbrancharrays[newbranchNameDeepCSV] = array("f",20*[-99])

                newBrnaches.append(tree.Branch(newbranchNameCSV, CSVbrancharrays[newbranchNameCSV], newbranchNameCSV+"/F"))
                newBrnaches.append(tree.Branch(newbranchNameDeepCSV, DeepCSVbrancharrays[newbranchNameDeepCSV], newbranchNameDeepCSV+"/F"))

    if debug:
        print DeepCSVbrancharrays

    nEvents = tree.GetEntries()

    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%1000 == 0:
            print "Event ", iev

        #CSV
        nJets = brancharrays[branchPrefixIn+"_num"][0]
        CSVtagpairs = int(nJets)*[(-1,-20)]
        DeepCSVtagpairs = int(nJets)*[(-1,-20)]
        for i in range(nJets):
            CSVtagpairs[i] = (i, brancharrays[branchPrefixIn+"_csv["+branchPrefixIn+"_num]"][i])
            DeepCSVtagpairs[i] = (i, brancharrays[branchPrefixIn+"_deepcsv["+branchPrefixIn+"_num]"][i])

        #print CSVtagpairs
        #print DeepCSVtagpairs
        #raw_input("Press Ret to go on!")

        from operator import itemgetter
        CSVsortedtags = sorted(CSVtagpairs,key=itemgetter(1), reverse=True) 
        DeepCSVsortedtags = sorted(DeepCSVtagpairs,key=itemgetter(1), reverse=True)

        CSVbrancharrays[branchPrefixIn.replace("Clean","CleanCSV")+"_num"][0] = brancharrays[branchPrefixIn+"_num"][0]
        DeepCSVbrancharrays[branchPrefixIn.replace("Clean","CleanDeepCSV")+"_num"][0] = brancharrays[branchPrefixIn+"_num"][0]

        for ipair, pair in enumerate(CSVsortedtags):
            for branchname in branchlist:
                if not branchname.startswith(branchPrefixIn+"_num"):
                    #print branchname, CSVbrancharrays[branchname.replace("Clean","CleanCSV")]
                    CSVbrancharrays[branchname.replace("Clean","CleanCSV")][ipair] = brancharrays[branchname][pair[0]]

        for ipair, pair in enumerate(DeepCSVsortedtags):
            for branchname in branchlist:
                if not branchname.startswith(branchPrefixIn+"_num"):
                    DeepCSVbrancharrays[branchname.replace("Clean","CleanDeepCSV")][ipair] = brancharrays[branchname][pair[0]]
                    
        if debug:
            print "-----------------------------------------------"
            printDict(brancharrays)
            print "-----------------------------------------------"
            printDict(CSVbrancharrays)
            print "-----------------------------------------------"
            printDict(DeepCSVbrancharrays)
            print "-----------------------------------------------"
            raw_input("Press Ret")

        for branch in newBrnaches:
            branch.Fill()

    #    tree.Fill()

    tree.Write("",ROOT.TFile.kOverwrite)
    if debug:
        print brancharrays



if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Description'
    )


    argumentparser.add_argument(
        "--Inputfile",
        action = "store",
        help = "Paths to input file (do not add .root extention)",
        type = str,
        required = True,
    )
    argumentparser.add_argument(
        "--debug",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--skipevents",
        action = "store",
        help = "Skip events",
        type = int,
        default = 0,
    )

    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################

    addCleanJetsSorting(args.Inputfile, args.debug, args.skipevents)
    


    
