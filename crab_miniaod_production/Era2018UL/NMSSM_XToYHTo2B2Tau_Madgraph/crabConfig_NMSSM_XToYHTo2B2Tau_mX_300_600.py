from CRABClient.UserUtilities import config

config = config()

## General settings
config.General.requestName = 'rgerosa_NMSSM_XToYHTo2B2Tau_mX_300_600'
config.General.transferOutputs = True
config.General.transferLogs = False
## PrivateMC type with a fake miniAOD step to circunvent crab requests (official data-tier for PrivateMC)
config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'miniaod_step_fake.py'
config.JobType.pyCfgParams = ['nThreads=4','outputName=miniaodStep.root']
## To be executed on node with Arguments
config.JobType.scriptExe   = 'scriptExe.sh'
config.JobType.scriptArgs  = ['nEvents=1000','nThreads=4','outputName=miniaodStep.root','mxmin=300','mxmax=600','mymin=90','mymax=150','nGridpacksPerJob=10','inputGridpacks=/store/user/rgerosa/NMSSM_XToYH_gridpacks']
config.JobType.inputFiles  = ['scriptExe.sh','copy_gridpacks.py','gen_step.py','sim_step.py','digi_raw_step.py','hlt_step.py','reco_step.py','miniaod_step.py','../pileup.py']
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
config.Data.totalUnits  = 1000000
config.Data.outLFNDirBase = '/store/user/rgerosa/PrivateMC/RunIISummer20UL18MiniAODv2/'
config.Data.publication   = True
config.Data.outputPrimaryDataset = 'NMSSM_XToYHTo2B2Tau_MX_300_600_MY_90_150_TuneCP5_madgraph-pythia8_13TeV'
config.Data.outputDatasetTag = 'RunIISummer20UL18MiniAODv2_106X_upgrade2018_realistic_v11_L1v1-MINIAODSIM'
## Site
config.Site.storageSite = 'T2_US_UCSD' 

