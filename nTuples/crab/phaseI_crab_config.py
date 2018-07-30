
#Define the datasets the following:
#list with
#     0th element: name
#     1st element: tuple containing primary and secondary DAS dataset name
#     2nd element: 0 if Data, 1 if MC
#Data = [
    #["MuonEG_HE",
     #("/MuonEG/CMSSW_10_1_7-101X_dataRun2_Prompt_v11_RelVal_muEG2018B-v1/MINIAOD","/MuonEG/CMSSW_10_1_7-101X_dataRun2_HLT_v7_RelVal_muEG2018B-v1/FEVTDEBUGHLT"),
     #"_HE",
     #True],
#]
# NOTE: Placeholder
Data = [["HEmiss_MCTT_v3",
       ("/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/MINIAODSIM",
        "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW"),
       "",
       False],
      #["HLT_Ntuple_BTagging_DiLepton_v10",
       ##("/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/AODSIM",
       #("/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-TSG_94X_mc2017_realistic_v11-v1/MINIAODSIM",
        #"/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17DRPremix-TSG_94X_mc2017_realistic_v11-v1/GEN-SIM-RAW"),
       #"",
       #False]
       ]



datasets = Data
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
        config.JobType.maxMemoryMB = 3000
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
            'hlt_dump_mc_HEmiss.py',
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
        config.Data.outLFNDirBase = '/store/user/dschafer/' + name + prefix
        config.Data.publication = False
        if dataset[3]:
            print "Using JSON"
            config.Data.lumiMask = '/afs/cern.ch/user/d/dschafer/CMSSW_10_1_7/src/HLTBTagging/nTuples/myjson.txt'
            #config.Data.lumiMask = '/afs/cern.ch/work/k/koschwei/public/test/CMSSW_9_2_12_patch1/src/HLTBTagging/nTuples/PU28to63_Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        config.Data.inputDataset = dataset[1][0]
        config.Data.secondaryInputDataset = dataset[1][1]
#       config.Data.publishDataName = config.General.requestName
        config.Data.outputDatasetTag = name
        config.Data.allowNonValidInputDataset = True
        #config.Site.blacklist = ['T0_*'] # didn"t work anymore when I wanted to submit jobs 
        #config.Site.blacklist = ['T2_BR_UERJ', 'T2_TR_MET', 'T2_RU_SINP', 'T2_RU_PNPI', 'T3_RU_FIAN', 'T3_US_MIT', 'T3_UK_London_UCL', 'T3_US_UCD', 'T3_CO_Uniandes', 'T3_US_Princeton_ARM', 'T3_ES_Oviedo', 'T3_US_N', 'T3_US_NotreDame', 'T3_KR_KISTI', 'T3_IN_PUHEP', 'T3_UK_ScotGrid_ECDF', 'T2_IT_Rome', 'T2_MY_UPM_BIRUNI', 'T2_TH_CUNSTDA', 'T3_CH_CERN_HelixNebula', 'T3_US_Princeton_ICSE', 'T3_IN_TIFRCloud', 'T0_CH_CERN', 'T3_GR_IASA', 'T3_CN_PK', 'T3_US_Kansas', 'T3_IR_IPM', 'T3_US_JH', 'T3_BY_NCPHEP', 'T3_US_FS', 'T3_KR_UOS', 'T3_CH_PSI']
        #For Run C
        #config.Site.ignoreGlobalBlacklist = True
        #config.Site.whitelist = ["T1_*","T2_RU_ITEP"]

        # use normally#
        #config.section_("Site")
        #config.Site.storageSite = "T2_DE_DESY"
        #use normally end#
        
        # use for copied mc sample#
        config.section_("Site") 
        config.Site.storageSite = 'T2_DE_DESY' 
        #config.Site.whitelist = ['T2_DE_DESY'] 
        #config.section_("User") 
        #config.User.voGroup = "dcms"
        # use for copied mc sample end#
        
        #config.Site.storageSite = "T3_CH_PSI"
        print "submitting ",dataset
        #crabCommand('submit',config = config,dryrun=True)
        crabCommand('submit',config = config)
        print "DONE ",dataset
    
