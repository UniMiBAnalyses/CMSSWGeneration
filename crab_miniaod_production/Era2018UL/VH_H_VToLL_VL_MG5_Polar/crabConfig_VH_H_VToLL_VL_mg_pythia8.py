from CRABClient.UserUtilities import config

config = config()

## General settings
config.General.requestName = 'amassiro_crabConfig_VH_H_VToLL_VL'
config.General.transferOutputs = True
config.General.transferLogs = False
## PrivateMC type with a fake miniAOD step to circunvent crab requests (official data-tier for PrivateMC)
config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'nanoaod_step_fake.py'
config.JobType.pyCfgParams = ['nThreads=4','outputName=nanoStep.root']
## To be executed on node with Arguments
config.JobType.scriptExe   = 'scriptExe.sh'
config.JobType.scriptArgs  = ['nEvents=1000','nThreads=4','outputName=nanoStep.root','inputGridpack=VHpolar_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz']
config.JobType.inputFiles  = ['scriptExe.sh','gen_step.py','sim_step.py','digi_raw_step.py','hlt_step.py','reco_step.py','miniaod_step.py','nanoaod_step.py','../pileup.py','VHpolar_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz']
## Output file to be collected
config.JobType.outputFiles = ["nanoStep.root"]
config.JobType.disableAutomaticOutputCollection = True
## Memory, cores, cmssw
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5500
config.JobType.numCores    = 4
## Data
config.Data.splitting   = 'EventBased'
config.Data.unitsPerJob = 1000
config.Data.totalUnits  = 500000
config.Data.outLFNDirBase = '/store/user/amassiro/PrivateMC/RunIISummer20UL18NanoAODv9/'
config.Data.publication   = True
config.Data.outputPrimaryDataset = 'VH_H_VToLL_VL_mg_pythia8_v2'
config.Data.outputDatasetTag = 'RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v11_L1v1-MINIAODSIM'
## Site
config.Site.storageSite = 'T2_CH_CERN' 

#T3_CH_CERNBOX
