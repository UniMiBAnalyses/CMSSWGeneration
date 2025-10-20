from CRABClient.UserUtilities import config

config = config()

## General settings
config.General.requestName = 'rgerosa_crabConfig_ggHHToBBTauTau_kl_0p0'
config.General.transferOutputs = True
config.General.transferLogs = False
## PrivateMC type with a fake miniAOD step to circunvent crab requests (official data-tier for PrivateMC)
config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'miniaod_step_fake.py'
config.JobType.pyCfgParams = ['nThreads=4','outputName=miniaodStep.root']
## To be executed on node with Arguments
config.JobType.scriptExe   = 'scriptExe.sh'
config.JobType.scriptArgs  = ['nEvents=1000','nThreads=4','outputName=miniaodStep.root','inputGridpack=/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc700/13TeV/powheg/V2/ggHH_EWChL_NNPDF31_13TeV_M125_cHHH0/v3/ggHH_EWChL_cHHH0_slc6_amd64_gcc700_CMSSW_10_2_5_patch1_my_ggHH_EWChL.tgz']
config.JobType.inputFiles  = ['scriptExe.sh','gen_step.py','sim_step.py','digi_raw_step.py','hlt_step.py','reco_step.py','miniaod_step.py','../pileup.py']
## Output file to be collected
config.JobType.outputFiles = ["miniaodStep.root"]
config.JobType.disableAutomaticOutputCollection = True
## Memory, cores, cmssw
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5500
config.JobType.numCores    = 4
## Data
config.Data.splitting   = 'EventBased'
config.Data.unitsPerJob = 1000
config.Data.totalUnits  = 1500000
config.Data.outLFNDirBase = '/store/user/rgerosa/PrivateMC/RunIISummer20UL18MiniAODv2/'
config.Data.publication   = True
config.Data.outputPrimaryDataset = 'GluGluToHHTo2B2Tau_node_cHHH0_TuneCUETP8M1_PSWeights_13TeV-powheg-pythia8'
config.Data.outputDatasetTag = 'RunIISummer20UL18MiniAODv2_106X_upgrade2018_realistic_v11_L1v1-MINIAODSIM'
## Site
config.Site.storageSite = 'T2_US_UCSD'
