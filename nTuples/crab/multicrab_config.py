#Define the datasets the following:
#list with
#     0th element: name
#     1st element: tuple containing primary and secondary DAS dataset name
#     2nd element: 0 if Data, 1 if MC
Data = [["HLT_Ntuple_BTagging_DiLepton_v2",
         ("/MuonEG/Run2017C-PromptReco-v2/AOD","/MuonEG/Run2017C-v1/RAW"),
         "0"]]
MC = [["HLT_Ntuple_BTagging_DiLepton_v2",
       ("/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/AODSIM",
        "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW"),
       "1"]]


datasets = Data+MC

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import config
    config = config()
    
    for dataset in datasets:
        name = dataset[0]
        config.section_("General")
        config.General.workArea = 'crab_'+name
        config.General.transferLogs=True
#       config.General.requestName = name+"_"+dataset.replace('/',"_")
        config.General.requestName = name + "_" + dataset[1][0].split('/')[1]

        config.section_("JobType")
#        config.JobType.numCores = 4
        config.JobType.numCores = 4
        config.JobType.maxMemoryMB = 10000
        config.JobType.pluginName = 'Analysis'
        config.JobType.psetName = 'crab_fake_pset.py'
        config.JobType.scriptExe = 'crab_script.sh'
        import os
        os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
        os.system("voms-proxy-info -path | xargs -i  cp {}  .")
        config.JobType.inputFiles = [
            'hlt_dump.py',
            'hlt_dump_mc.py',
            'fwlite_config.py',
            'script.py',
            'utils.py',
            'python.tar.gz',
        ]
        
        config.section_("Data")
        config.Data.inputDBS = 'global'
        config.Data.splitting = 'FileBased'
        config.Data.unitsPerJob = 2 ##FIXME: use 20

        config.Data.totalUnits = -1 #10*config.Data.unitsPerJob #FIXME: use -1
        config.Data.outLFNDirBase = '/store/user/koschwei/' + name
        config.Data.publication = False
        if not bool(dataset[2]):
            config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-304120_13TeV_PromptReco_Collisions17_JSON.txt' 
        config.Data.inputDataset = dataset[1][0]
        config.Data.secondaryInputDataset = dataset[1][1]
#       config.Data.publishDataName = config.General.requestName
        config.Data.outputDatasetTag = name
        config.Data.allowNonValidInputDataset = True
        config.Site.blacklist = ['T0_*', "T2_US_Vanderbilt"]
        
        config.section_("Site")
#       config.Site.storageSite = "T2_CH_CSCS"
        config.Site.storageSite = "T3_CH_PSI"
        print "submitting ",dataset
        crabCommand('submit',config = config)
        print "DONE ",dataset
    
