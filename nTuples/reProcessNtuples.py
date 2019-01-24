import ROOT
from array import array
import utils

import os, time
import json, yaml

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

def addLeptonSF(inputfile, debug = False, skipevents = 0):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()

    #LOAD all SFs
    rMuID = ROOT.TFile("RunBCDEF_SF_ID.root","READ")
    hMuID = rMuID.Get("NUM_TightID_DEN_genTracks_pt_abseta")
    rMuIso = ROOT.TFile("RunBCDEF_SF_ISO.root","READ")
    hMuIso = rMuIso.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")
    rEleID = ROOT.TFile("egammaEffi.txt_EGM2D_runBCDEF_passingTight94X.root","READ")
    hEleID = rEleID.Get("EGamma_SF2D")
    rEleReco = ROOT.TFile("egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root","READ")
    hEleReco = rEleReco.Get("EGamma_SF2D")

    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")
    rfile.cd()
    
    tree = rfile.Get("tree")

    #for brPrefix, lenvar in [("offTightElectrons", "offTightElectrons_num"), ("offTightMuons", "offTightMuons_num")]:
    nameMuID = "offTightMuons_IDSF[offTightMuons_num]"
    nameMuISO = "offTightMuons_ISOSF[offTightMuons_num]"
    nameMu = "offTightMuons_SF[offTightMuons_num]"
    nameEleID = "offTightElectrons_IDSF[offTightElectrons_num]"
    nameEleRECO = "offTightElectrons_RECOSF[offTightElectrons_num]"
    nameEle = "offTightElectrons_SF[offTightElectrons_num]"

    newBranchNames = [nameMuID, nameMuISO, nameEleID, nameEleRECO]
    arrays = {nameMuID :  array("f",40*[1.0]),
              nameMuISO :  array("f",40*[1.0]),
              nameMu :  array("f",40*[1.0]),
              nameEleID :  array("f",40*[1.0]),
              nameEleRECO :  array("f",40*[1.0]),
              nameEle :  array("f",40*[1.0])}
    newBrnaches = [tree.Branch(nameMuID,  arrays[nameMuID], nameMuID+"/F"),
                   tree.Branch(nameMuISO,  arrays[nameMuISO], nameMuISO+"/F"),
                   tree.Branch(nameMu,  arrays[nameMu], nameMu+"/F"),
                   tree.Branch(nameEleID,  arrays[nameEleID], nameEleID+"/F"),
                   tree.Branch(nameEleRECO,  arrays[nameEleRECO], nameEleRECO+"/F"),
                   tree.Branch(nameEle,  arrays[nameEle], nameEle+"/F")]
    nEvents = tree.GetEntries()
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()

        if debug:
            print "-------------------- New Event -->  {0} -----------------".format(iev)
            print "---------------------------------------------------------"
            
        for name in newBranchNames:
            utils.resetArray(arrays[name], 1.0)
            
        for imu in range(tree.offTightMuons_num):
            MuPt, MuEta = tree.offTightMuons_pt[imu], abs(tree.offTightMuons_eta[imu])
            arrays[nameMuID][imu] = hMuID.GetBinContent(hMuID.FindBin(MuPt, MuEta))
            arrays[nameMuISO][imu] = hMuIso.GetBinContent(hMuIso.FindBin(MuPt, MuEta))
            if arrays[nameMuID][imu] == 0:
                arrays[nameMuID][imu] = 1
            if arrays[nameMuISO][imu] == 0:
                arrays[nameMuISO][imu] = 1
            arrays[nameMu][imu] = arrays[nameMuID][imu] * arrays[nameMuISO][imu]
                
            if debug:
                print "Muon {0}: pt = {1}, eta = {2} --> IDSF = {3}, ISOSF = {4}, Prod = {5}".format(imu, MuPt, MuEta, arrays[nameMuID][imu], arrays[nameMuISO][imu], arrays[nameMu][imu])

        for iele in range(tree.offTightElectrons_num):
            ElePt, EleSCEta = tree.offTightElectrons_pt[iele], tree.offTightElectrons_superClusterEta[iele]
            arrays[nameEleID][iele] = hEleID.GetBinContent(hEleID.FindBin(EleSCEta, ElePt))
            arrays[nameEleRECO][iele] = hEleReco.GetBinContent(hEleReco.FindBin(EleSCEta, ElePt))
            if arrays[nameEleID][iele] == 0:
                arrays[nameEleID][iele] = 1
            if arrays[nameEleRECO][iele] == 0:
                arrays[nameEleRECO][iele] = 1
            arrays[nameEle][iele] = arrays[nameEleRECO][iele] * arrays[nameEleID][iele]
            if debug:
                print "Ele {0}: pt = {1}, SCeta = {2} --> IDSF = {3}, RECOSF = {4}, Prod = {5}".format(iele, ElePt, EleSCEta, arrays[nameEleID][iele], arrays[nameEleRECO][iele],  arrays[nameEle][iele])

                
        if debug:
            raw_input("Next Events....")
            pass
        

            
        for branch in newBrnaches:
            branch.Fill()


    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)

        

            
def addWPBTagSF(inputfile, debug = False, skipevents = 0,branchprefixandlen = [("offCleanJets", "offCleanJets_num")], algo = "CSV", wp = "MEDIUM"):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")

    if wp == "MEDIUM":
        print "Using meduim WP"
        readerWP = 1
    if wp == "TIGHT":
        print "Using tight WP"
        readerWP = 2

    nEvents = tree.GetEntries()
    
    ROOT.gSystem.Load('libCondFormatsBTauObjects') 
    ROOT.gSystem.Load('libCondToolsBTau')
    if algo == "CSV":
        calib = ROOT.BTagCalibration('csvv2', 'CSVv2_94XSF_V2_B_F.csv')
    if algo == "DeepCSV":
        calib = ROOT.BTagCalibration('deepcsv', 'DeepCSV_94XSF_V3_B_F.csv')
    
    v_sys = getattr(ROOT, 'vector<string>')()
    #v_sys.push_back('up')
    #v_sys.push_back('down')
    reader = ROOT.BTagCalibrationReader(
        readerWP,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
        "central",      # central systematic type
        v_sys,          # vector of other sys. types
    )
    
    reader.load(
        calib, 
        0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "comb"      # measurement type
    )
    reader.load(
        calib, 
        1,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "comb"      # measurement type
    )
    reader.load(
        calib, 
        2,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "incl"      # measurement type
    )


    newBrnaches = []
    newBranchNames = []
    arrays = {}
    for brPrefix, lenvar in branchprefixandlen:
        if algo == "CSV":
            name = brPrefix+"_csvv2SF"+wp+"["+lenvar+"]"
        if algo == "DeepCSV":
            name = brPrefix+"_deepcsvSF"+wp+"["+lenvar+"]"
        newBranchNames.append(name)
        arrays[name] = array("f",40*[1.0])
        newBrnaches.append(tree.Branch(name,  arrays[name], name+"/F"))


    # WCSVarray = array("f",[1.0])
    # if algo == "CSV":
    #     newBrnaches.append(tree.Branch("wCSVv2"+wp, WCSVarray, "wCSVv2"+wp+"/F"))
    # if algo == "DeepCSV":
    #     newBrnaches.append(tree.Branch("wDeepCSV"+wp, WCSVarray, "wDeepCSV"+wp+"/F"))
        
    print arrays[name]
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()
            
        evtW = 1.0
        
        for brPrefix, lenvar in branchprefixandlen:
            if algo == "CSV":
                name =  brPrefix+"_csvv2SF"+wp+"["+lenvar+"]"
            if algo == "DeepCSV":
                name =  brPrefix+"_deepcsvSF"+wp+"["+lenvar+"]"
            utils.resetArray(arrays[name], 1.0)
            nJets =tree.__getattr__(lenvar)
            if debug:
                print "-------------------- New Event --------------------------"
                print "---------------------------------------------------------"
                print "---- nJets {0} ---".format(nJets)
            for i in range(nJets):
                
                jetEta = tree.__getattr__(brPrefix+"_eta")[i]
                jetPt = tree.__getattr__(brPrefix+"_pt")[i]
                jetCsv = tree.__getattr__(brPrefix+"_csv")[i]
                jetDeepCsv = tree.__getattr__(brPrefix+"_deepcsv")[i]
                jetID = tree.__getattr__(brPrefix+"_passesTightLeptVetoID")[i]
                jetFlav = tree.__getattr__(brPrefix+"_hadronFlavour")[i]
                if abs(jetFlav) == 5:
                    btvFlav = 0
                if abs(jetFlav) == 4:
                    btvFlav = 1
                if abs(jetFlav) in [ 0, 1, 2, 3, 21 ]:
                    btvFlav = 2

                #print jetFlav
                if algo == "CSV":
                    sf = reader.eval_auto_bounds('central', btvFlav, jetEta, jetPt)
                if algo == "DeepCSV":
                    sf = reader.eval_auto_bounds('central', btvFlav, jetEta, jetPt)
                if debug:
                    if algo == "CSV":
                        print "Eta {0} | pt {1} | csv {2} | FLAV {4} (BTV {5}) | SF {3}".format(jetEta, jetPt, jetCsv, sf, jetFlav, btvFlav)
                    if algo == "DeepCSV":
                        print "Eta {0} | pt {1} | csv {2} | FLAV {4} (BTV {5}) | SF {3}".format(jetEta, jetPt, jetDeepCsv, sf, jetFlav, btvFlav)
                    #raw_input("Next JEt")
                if sf > 0:
                    arrays[name][i] = sf
                # if abs(jetEta) < 2.5 and jetPt > 30:
                #     evtW = evtW * arrays[name][i]
            #WCSVarray[0] = evtW
        for branch in newBrnaches:
            branch.Fill()

            
    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)

            

def addBTagSF(inputfile, debug = False, skipevents = 0,branchprefixandlen = [("offCleanJets", "offCleanJets_num")], algo = "CSV"):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")


    nEvents = tree.GetEntries()
    
    ROOT.gSystem.Load('libCondFormatsBTauObjects') 
    ROOT.gSystem.Load('libCondToolsBTau')
    if algo == "CSV":
        calib = ROOT.BTagCalibration('csvv2', 'CSVv2_94XSF_V2_B_F.csv')
    if algo == "DeepCSV":
        calib = ROOT.BTagCalibration('deepcsv', 'DeepCSV_94XSF_V3_B_F.csv')
    
    v_sys = getattr(ROOT, 'vector<string>')()
    #v_sys.push_back('up')
    #v_sys.push_back('down')
    reader = ROOT.BTagCalibrationReader(
        3,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
        "central",      # central systematic type
        v_sys,          # vector of other sys. types
    )
    reader.load(
        calib, 
        0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "iterativefit"      # measurement type
    )


    newBrnaches = []
    newBranchNames = []
    arrays = {}
    for brPrefix, lenvar in branchprefixandlen:
        if algo == "CSV":
            name = brPrefix+"_csvv2SF["+lenvar+"]"
        if algo == "DeepCSV":
            name = brPrefix+"_deepcsvSF["+lenvar+"]"
        newBranchNames.append(name)
        arrays[name] = array("f",40*[1.0])
        newBrnaches.append(tree.Branch(name,  arrays[name], name+"/F"))


    WCSVarray = array("f",[1.0])
    if algo == "CSV":
        newBrnaches.append(tree.Branch("wCSVv2", WCSVarray, "wCSVv2/F"))
    if algo == "DeepCSV":
        newBrnaches.append(tree.Branch("wDeepCSV", WCSVarray, "wDeepCSV/F"))
        
    print arrays[name]
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()
            
        evtW = 1.0
        
        for brPrefix, lenvar in branchprefixandlen:
            if algo == "CSV":
                name =  brPrefix+"_csvv2SF["+lenvar+"]"
            if algo == "DeepCSV":
                name =  brPrefix+"_deepcsvSF["+lenvar+"]"
            utils.resetArray(arrays[name], 1.0)
            nJets =tree.__getattr__(lenvar)
            if debug:
                print "-------------------- New Event --------------------------"
                print "---------------------------------------------------------"
                print "---- nJets {0} ---".format(nJets)
            for i in range(nJets):
                
                jetEta = tree.__getattr__(brPrefix+"_eta")[i]
                jetPt = tree.__getattr__(brPrefix+"_pt")[i]
                jetCsv = tree.__getattr__(brPrefix+"_csv")[i]
                jetDeepCsv = tree.__getattr__(brPrefix+"_deepcsv")[i]
                jetID = tree.__getattr__(brPrefix+"_passesTightLeptVetoID")[i]
                jetFlav = int(tree.__getattr_(brPrefix+"_hadronFlavour")[i])
                if algo == "CSV":
                    sf = reader.eval_auto_bounds('central', 0, jetEta, jetPt, jetCsv)
                if algo == "DeepCSV":
                    sf = reader.eval_auto_bounds('central', 0, jetEta, jetPt, jetDeepCsv)
                if debug:
                    if algo == "CSV":
                        print "Eta {0} | pt {1} | csv {2} | SF {3}".format(jetEta, jetPt, jetCsv, sf)
                    if algo == "DeepCSV":
                        print "Eta {0} | pt {1} | csv {2} | SF {3}".format(jetEta, jetPt, jetDeepCsv, sf)
                if sf > 0:
                    arrays[name][i] = sf
                if abs(jetEta) < 2.5 and jetPt > 30:
                    evtW = evtW * arrays[name][i]
            WCSVarray[0] = evtW
        for branch in newBrnaches:
            branch.Fill()

            
    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)
                
                
        
def filterLS(inputfile, jsonFile, debug = False, skipevents = 0, mc = False):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")


    nEvents = tree.GetEntries()
    
    newBrnaches = []
    newBranchNames = []
    barray = array("i",[-1])
    newBranch = tree.Branch("passJson", barray, "passJson/I")

    validLS = None
    
    with open(jsonFile, 'r') as f:
        validLS = yaml.safe_load(f) #json loads all entries as unicode (u'..')

    if debug:
        print validLS
        print validLS.keys()
        raw_input("press ret")
    
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()


        if mc is False:
            inJson = False
            if str(int(tree.run)) in validLS.keys():
                if debug:
                    print str(int(tree.run)) in validLS
                # ls 5 block [5,9] --> 5 >= 5 and 5 <= 9 --> yes
                # ls 9 block [5,9] --> 9 >= 5 and 9 <= 9 --> yes
                # ls 10 block [5,9] --> 10 >= 5 and 10 <= 9 --> no
                for block in validLS[str(int(tree.run))]:
                    if int(tree.lumi) >= block[0] and int(tree.lumi) <= block[1]:
                        inJson = True
                        break
        else:
            inJson = True            

            
        if debug:
            print int(tree.run), int(tree.lumi), inJson
        barray[0] = int(inJson)
        newBranch.Fill()


    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)


def vetoDoubleEvents(inputfile, debug, skipevents = 0):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")
    
    tree = rfile.Get("tree")


    nEvents = tree.GetEntries()
    
    newBrnaches = []
    newBranchNames = []
    barray = array("i",[-1])
    newBranch = tree.Branch("doubleEvt", barray, "doubleEvt/I")

    listofevents = {}
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()
            
        evt = tree.evt
        if not evt in listofevents:
            listofevents[evt] = 1
            double = False
        else:
            double = True
            if debug:
                print "Already seen event",evt


        barray[0] = int(double)

        newBranch.Fill()

    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)


        
def redomatching(inputfile, debug = False, skipevents = 0, branchprefixandlen = [("offJets", "offJets_num")]):
    t0 = time.time()
    print "Executing: cp {0}.root {0}_mod.root"
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")


    nEvents = tree.GetEntries()

    newBrnaches = []
    newBranchNames = []
    arrays = {}
    matchings = ["PF","Calo"]
    for brPrefix, lenvar in branchprefixandlen:
        for matching in matchings:
            name = brPrefix+"_match"+matching+"2["+lenvar+"]"
            newBranchNames.append(name)
            arrays[name] = array("i",20*[-1])
            newBrnaches.append(tree.Branch(name,  arrays[name], name+"/I"))


    print "Will add branches:"
    for name in newBranchNames:
        print name
        
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f}".format(iev, time.time()-t0,time.time()-tdiff)
            tdiff = time.time()

        for name in newBranchNames:
            utils.resetArray(arrays[name], -1)

        for brPrefix, lenvar in branchprefixandlen:

            nJets =tree.__getattr__(lenvar)
            nCaloJets = tree.__getattr__("caloJets_num")
            nPFJets = tree.__getattr__("pfJets_num")
            if debug:
                print "-------------------- New Event --------------------------"
                print "---------------------------------------------------------"
            for i in range(nCaloJets):
                offMatch =  tree.__getattr__("caloJets_matchOff")[i]
                if debug:
                    print "caloJet {0} has offMatch {1}".format(i, offMatch)
                if offMatch >= 0:
                    for name in newBranchNames:
                        if name.startswith(brPrefix):
                            if "Calo" in name:
                                if debug:
                                    print "Setting {0} at index {1} to {2}".format(name, offMatch, i)
                                arrays[name][offMatch] = i
            if debug:
                print "---------------------------------------------------------"
            for i in range(nPFJets):
                offMatch =  tree.__getattr__("pfJets_matchOff")[i]
                if debug:
                    print "pfJet {0} has offMatch {1}".format(i, offMatch)
                if offMatch >= 0:
                    for name in newBranchNames:
                        if name.startswith(brPrefix):
                            if "PF" in name:
                                if debug:
                                    print "Setting {0} at index {1} to {2}".format(name, offMatch, i)
                                arrays[name][offMatch] = i

            if debug:
                for name in newBranchNames:
                    print name, arrays[name]
                #raw_input("press ret")
        for branch in newBrnaches:
            branch.Fill()

    #    tree.Fill()

    tree.Write("",ROOT.TFile.kOverwrite)
    if debug:
        print brancharrays
    print "Total time to finish: {0:8f}".format(time.time()-t0)

def addCleanJets(inputfile, debug = False, skipevents = 0, branchPrefixIn = "offJets", branchPrefixOut = "cleanJets", selVar = "lepOverlap04Tight"):
    t0 = time.time()
    print "Running addCleanJets()"
    print "Executing: cp {0}.root {0}_mod.root".format(inputfile)
    os.system("cp {0}.root {0}_mod.root".format(inputfile))
    print "Time to copy {0:6f}".format(time.time()-t0)
    tdiff = time.time()
    rfile = ROOT.TFile("{0}_mod.root".format(inputfile), "update")

    tree = rfile.Get("tree")

    branchlist = []
    brancharrays = {}
    newBrnaches = []
    outBranchArrays = {}
    newBranchNames = []
    
    for branch in tree.GetListOfBranches():
        branchlist.append(branch.GetName())
        if branch.GetName().startswith(branchPrefixIn+"_num"):
            brancharrays[branch.GetName()] = array("i",[0])
        elif  branch.GetName().startswith(branchPrefixIn):
            if not "match" in branch.GetName() and not "mcFlavour" in branch.GetName():
                typearray = "f"
            else:
                typearray = "i"
            brancharrays[branch.GetName()] = array(typearray,20*[-99])
        if brancharrays.has_key(branch.GetName()):
            tree.SetBranchAddress( branch.GetName() , brancharrays[branch.GetName()] )    
        #print branch.GetName()
        if branch.GetName().startswith(branchPrefixIn):
            
            newBranchName = branch.GetName().replace(branchPrefixIn, branchPrefixOut)
            
            #print newBranchName
            newBranchNames.append(newBranchName)
            if branch.GetName().startswith(branchPrefixIn+"_num"):
                outBranchArrays[newBranchName] = array("i",[0])
                #print "---------------------",outBranchArrays[newBranchName], newBranchName
                #print "---------------------",newBranchName, outBranchArrays[newBranchName], newBranchName+"/I"
                newBrnaches.append(tree.Branch(newBranchName, outBranchArrays[newBranchName], newBranchName+"/I"))
            else:
                if not "match" in newBranchName and not "mcFlavour" in newBranchName:
                    typearray = "f"
                    typebranch = "F"
                else:
                    typearray = "i"
                    typebranch = "I"

                outBranchArrays[newBranchName] = array(typearray,20*[-99])
                #print newBranchName, outBranchArrays[newBranchName], newBranchName+"/"+typebranch
                newBrnaches.append(tree.Branch(newBranchName, outBranchArrays[newBranchName], newBranchName+"/"+typebranch))
    if debug:
        for branch in newBranchNames:
            print branch, outBranchArrays[branch]
    nEvents = tree.GetEntries()
    print "Starting event Loop"
    for iev in range(skipevents, nEvents):
        tree.GetEvent(iev)
        if iev%10000 == 0:
            print "Event {0:10d} | Total time: {1:8f} | Diff time {2:8f} | Time left {2:8f}".format(iev, time.time()-t0,time.time()-tdiff,(time.time()-tdiff)*(nEvents-iev))
            tdiff = time.time()

        nJets = tree.__getattr__(branchPrefixIn+"_num")
        #print nJets
        nNewJets = 0
        for i in range(nJets):
            printed = False
            if debug:
                print "cutting on:",branchPrefixIn+"_"+selVar," = ",tree.__getattr__(branchPrefixIn+"_"+selVar)[i]
            if tree.__getattr__(branchPrefixIn+"_"+selVar)[i] < 1:
                nNewJets += 1
        outBranchArrays[branchPrefixOut+"_num"][0] = int(nNewJets)
        index = -1
        for i in range(nJets):
            printed = False
            if debug:
                print "cutting on:",branchPrefixIn+"_"+selVar," = ",tree.__getattr__(branchPrefixIn+"_"+selVar)[i]
            if tree.__getattr__(branchPrefixIn+"_"+selVar)[i] < 1:
                index += 1
                for branch in newBranchNames:
                    if not  branch.startswith(branchPrefixOut+"_num"):
                        if debug:
                            if not printed:
                                print "{0} index {1} will be {2} index {3}".format( branchPrefixIn, i , branchPrefixOut, index)
                                printed = True
                        outBranchArrays[branch][index] = brancharrays[branch.replace(branchPrefixOut, branchPrefixIn)][i]


        for branch in newBrnaches:
            if debug:
                print "Filling:",branch
            branch.Fill()
        if debug:
            print "---------",branchPrefixOut+"_num", outBranchArrays[branchPrefixOut+"_num"]
            for branch in newBranchNames:
                print branch , outBranchArrays[branch]
            raw_input("")

            
    tree.Write("",ROOT.TFile.kOverwrite)
    print "Total time to finish: {0:8f}".format(time.time()-t0)



                                                
            
def addCleanJetsSorting(inputfile, debug = False, skipevents = 0):
    branchPrefixIn = "cleanJets"
    lenVar = "cleanJets_num"
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

            newbranchNameCSV = branch.GetName().replace("clean","cleanCSV")
            newbranchNameDeepCSV = branch.GetName().replace("clean","cleanDeepCSV")

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

        CSVbrancharrays[branchPrefixIn.replace("clean","cleanCSV")+"_num"][0] = brancharrays[branchPrefixIn+"_num"][0]
        DeepCSVbrancharrays[branchPrefixIn.replace("clean","cleanDeepCSV")+"_num"][0] = brancharrays[branchPrefixIn+"_num"][0]

        for ipair, pair in enumerate(CSVsortedtags):
            for branchname in branchlist:
                if not branchname.startswith(branchPrefixIn+"_num"):
                    #print branchname, CSVbrancharrays[branchname.replace("Clean","CleanCSV")]
                    CSVbrancharrays[branchname.replace("clean","cleanCSV")][ipair] = brancharrays[branchname][pair[0]]

        for ipair, pair in enumerate(DeepCSVsortedtags):
            for branchname in branchlist:
                if not branchname.startswith(branchPrefixIn+"_num"):
                    DeepCSVbrancharrays[branchname.replace("clean","cleanDeepCSV")][ipair] = brancharrays[branchname][pair[0]]
                    
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
    argumentparser.add_argument(
        "--addCleanJets",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--addCleanJetsSorting",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--addCSVSF",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--addDeepCSVSF",
        action = "store_true",
        help = "Enable Debug messages",
    )

    argumentparser.add_argument(
        "--addDeepCSVWPSF",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--addDeepCSVWPSFTight",
        action = "store_true",
        help = "Enable Debug messages",
    )

    argumentparser.add_argument(
        "--addCSVWPSF",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--addLeptonSF",
        action = "store_true",
        help = "Enable Debug messages",
    )
    
    argumentparser.add_argument(
        "--correctMatching",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--jsonfilter",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--double",
        action = "store_true",
        help = "Enable Debug messages",
    )
    argumentparser.add_argument(
        "--json",
        action = "store",
        help = "Paths to json file",
        type = str,
        required = False,
    )
    argumentparser.add_argument(
        "--mc",
        action = "store_true",
        help = "Enable Debug messages",
    )
    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    ##############################################################################################################
    if args.addCleanJetsSorting:
        addCleanJetsSorting(args.Inputfile, args.debug, args.skipevents)
    elif args.correctMatching:
        redomatching(args.Inputfile, args.debug, args.skipevents)
    elif args.addCleanJets:
        addCleanJets(args.Inputfile, args.debug, args.skipevents)
    elif args.jsonfilter:
        filterLS(args.Inputfile, args.json, args.debug, args.skipevents, args.mc)
    elif args.double:
        vetoDoubleEvents(args.Inputfile, args.debug, args.skipevents)
    elif args.addCSVSF:
        addBTagSF(args.Inputfile, args.debug, args.skipevents)
    elif args.addDeepCSVSF:
        addBTagSF(args.Inputfile, args.debug, args.skipevents, algo =  "DeepCSV")
    elif args.addDeepCSVWPSF:
        addWPBTagSF(args.Inputfile, args.debug, args.skipevents, algo =  "DeepCSV", wp = "MEDIUM")
    elif args.addCSVWPSF:
        addWPBTagSF(args.Inputfile, args.debug, args.skipevents, algo =  "CSV", wp = "MEDIUM")
    elif args.addDeepCSVWPSFTight:
        addWPBTagSF(args.Inputfile, args.debug, args.skipevents, algo =  "DeepCSV", wp = "TIGHT")
    elif args.addLeptonSF:
        addLeptonSF(args.Inputfile, args.debug, args.skipevents)
