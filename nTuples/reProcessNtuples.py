import ROOT
from array import array

import os, time


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
    t0 = time.time()

    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
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
                if not "match" in branch.GetName() and not "mcFlavour" in branch.GetName():
                    typearray = "f"
                else:
                    typearray = "i"
                brancharrays[branch.GetName()] = array(typearray,20*[-99])
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
                if not "match" in newbranchNameCSV and not "mcFlavour" in newbranchNameCSV:
                    typearray = "f"
                    typebranch = "F"
                else:
                    #print newbranchNameCSV
                    typearray = "i"
                    typebranch = "I"

                CSVbrancharrays[newbranchNameCSV] = array(typearray,20*[-99])
                DeepCSVbrancharrays[newbranchNameDeepCSV] = array(typearray,20*[-99])

                newBrnaches.append(tree.Branch(newbranchNameCSV, CSVbrancharrays[newbranchNameCSV], newbranchNameCSV+"/"+typebranch))
                newBrnaches.append(tree.Branch(newbranchNameDeepCSV, DeepCSVbrancharrays[newbranchNameDeepCSV], newbranchNameDeepCSV+"/"+typebranch))


    if debug:
        print DeepCSVbrancharrays

    nEvents = tree.GetEntries()

    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()

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
    print "Total time to finish: {0:8f}".format(time.time()-t0)



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
    


    
