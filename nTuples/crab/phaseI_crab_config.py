
#Define the datasets the following:
#list with
#     0th element: name
#     1st element: tuple containing primary and secondary DAS dataset name
#     2nd element: 0 if Data, 1 if MC
Data = [
    ["HLT_Ntuple_BTagging_DiLepton_v10",
     ("/MuonEG/Run2018A-PromptReco-v1/MINIAOD","/MuonEG/Run2018A-v1/RAW"),
     "_RunA",
     True],
]
"""NOTE: Placeholder
MC = [["HLT_Ntuple_BTagging_DiLepton_v10",
       #("/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/AODSIM",
       ("/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-TSG_94X_mc2017_realistic_v11-v1/MINIAODSIM",
        "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17DRPremix-TSG_94X_mc2017_realistic_v11-v1/GEN-SIM-RAW"),
       "",
       False],
      ["HLT_Ntuple_BTagging_DiLepton_v10",
       #("/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/AODSIM",
       ("/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-TSG_94X_mc2017_realistic_v11-v1/MINIAODSIM",
        "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17DRPremix-TSG_94X_mc2017_realistic_v11-v1/GEN-SIM-RAW"),
       "",
       False]]
"""


datasets = [Data[2]]
print datasets
raw_input("press ret to continue")
prefix = ""


if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import config
    config = config()
    
    for dataset in datasets:
        name = dataset[0]
        config.section_("General")
        config.General.workArea = 'crab_' + name + prefix 
        config.General.transferLogs=True
#       config.General.requestName = name+"_"+dataset.replace('/',"_")
        config.General.requestName = name + prefix + "_" + dataset[1][0].split('/')[1].split("-")[0] + dataset[2]

        print "Requestname: ", name + prefix + "_" + dataset[1][0].split('/')[1].split("-")[0] + dataset[2]
        #raw_input("press ret")
        
        config.section_("JobType")
#        config.JobType.numCores = 4
        config.JobType.numCores = 4
        config.JobType.maxMemoryMB = 10000
        config.JobType.maxJobRuntimeMin = 2000
        config.JobType.sendPythonFolder = True
        config.JobType.pluginName = 'Analysis'
        config.JobType.psetName = 'crab_fake_pset.py'
        config.JobType.scriptExe = 'crab_script_phaseI.sh'
        import os
        os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
        os.system("voms-proxy-info -path | xargs -i  cp {}  .")
        config.JobType.inputFiles = [
            'hlt_dump_phase1.py',
            'hlt_dump_mc_phase1.py',
            'fwlite_config_phaseI.py',
            'script_phaseI.py',
            'utils.py',
            'python.tar.gz',
        ]
        
        config.section_("Data")
        config.Data.inputDBS = 'global'
        #Data
        if dataset[3]:
            config.Data.splitting = 'LumiBased'
            config.Data.unitsPerJob = 40 ##FIXME: use 20
        #MC
        if not dataset[3]:
            config.Data.splitting = 'LumiBased'
            config.Data.unitsPerJob = 20
            ##FIXME: use 20
        

        config.Data.totalUnits = -1 #10*config.Data.unitsPerJob #FIXME: use -1
        config.Data.outLFNDirBase = '/store/user/koschwei/onlineBTV/' + name + prefix
        config.Data.publication = False
        if dataset[3]:
            print "Using JSON"
            config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
            #config.Data.lumiMask = '/afs/cern.ch/work/k/koschwei/public/test/CMSSW_9_2_12_patch1/src/HLTBTagging/nTuples/PU28to63_Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        config.Data.inputDataset = dataset[1][0]
        config.Data.secondaryInputDataset = dataset[1][1]
#       config.Data.publishDataName = config.General.requestName
        config.Data.outputDatasetTag = name
        config.Data.allowNonValidInputDataset = True
        config.Site.blacklist = ['T0_*']
        #config.Site.blacklist = ['T2_BR_UERJ', 'T2_TR_MET', 'T2_RU_SINP', 'T2_RU_PNPI', 'T3_RU_FIAN', 'T3_US_MIT', 'T3_UK_London_UCL', 'T3_US_UCD', 'T3_CO_Uniandes', 'T3_US_Princeton_ARM', 'T3_ES_Oviedo', 'T3_US_N', 'T3_US_NotreDame', 'T3_KR_KISTI', 'T3_IN_PUHEP', 'T3_UK_ScotGrid_ECDF', 'T2_IT_Rome', 'T2_MY_UPM_BIRUNI', 'T2_TH_CUNSTDA', 'T3_CH_CERN_HelixNebula', 'T3_US_Princeton_ICSE', 'T3_IN_TIFRCloud', 'T0_CH_CERN', 'T3_GR_IASA', 'T3_CN_PK', 'T3_US_Kansas', 'T3_IR_IPM', 'T3_US_JH', 'T3_BY_NCPHEP', 'T3_US_FS', 'T3_KR_UOS', 'T3_CH_PSI']
        #For Run C
        #config.Site.ignoreGlobalBlacklist = True
        #config.Site.whitelist = ["T1_*","T2_RU_ITEP"]

        
        config.section_("Site")
        config.Site.storageSite = "T2_CH_CSCS"
        #config.Site.storageSite = "T3_CH_PSI"
        print "submitting ",dataset
        crabCommand('submit',config = config)
        print "DONE ",dataset
    
