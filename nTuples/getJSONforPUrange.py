import json
import sys

pumin = 28
pumax = 63
minbiasXS = 69200

puFile = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt"
validFile = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"

puJSON = json.load(open(puFile))
validJSON = json.load(open(validFile))

print validJSON.keys()
output = {}
for run in validJSON.keys():
    print "Run:",run
    try:
        puJSON[run]
    except KeyError:
        continue
    else:
        puForRun = puJSON[run]
    validLS = validJSON[run]#
    puforLS = {}
    for LS in puForRun:
        puforLS[LS[0]] = LS[1::]
    #puforLS[113] = [0,0,0]
    #puforLS[82] = [0,0,0]
    validblocks = []
    for block in validLS:

        lastLS = block[0]
        validblock = [9999999, -1]
        for LS in range(block[0], block[1]+1):
            try:
                PUofLS = puforLS[LS][2] * minbiasXS
            except KeyError:
                PUofLS = -100
                print "KeyError. Setting PU of LS to -100"
            else:
                PUofLS = puforLS[LS][2] * minbiasXS
            #print LS, PUofLS
            if PUofLS >= pumin and PUofLS < pumax:
                if LS > lastLS+1:
                    #print "Hallo"
                    validblocks.append(validblock)
                    validblock = [9999999, -1]
                if LS < validblock[0]:
                    validblock[0] = LS
                if LS > validblock[1]:
                    validblock[1] = LS
                lastLS = LS
        validblocks.append(validblock)
    
    print "LS in PromptRecoJSON:",validLS
    validPULS = []
    for block in validblocks:
        if not (block[0] == 9999999 or block[1] == -1):
            validPULS.append(block)
    print "LS in PU range:",validPULS
    if len(validPULS) > 0:
        output[run] = validPULS


data = json.dumps(output)
with open("PU{0}to{1}_{2}".format(pumin, pumax, validFile.split("/")[-1]),"w") as f:
  f.write(data)




