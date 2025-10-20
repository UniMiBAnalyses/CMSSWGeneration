from CRABClient.UserUtilities import config

config = config()

## General settings
config.General.requestName     = 'rgerosa_ggHtt_pt_250_500'
config.General.transferOutputs = True
config.General.transferLogs    = False
## PrivateMC type with a fake miniAOD step to circunvent crab requests (official data-tier for PrivateMC)
config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'miniaod_step_fake.py'
config.JobType.pyCfgParams = ['nThreads=4','outputName=miniaodStep.root']
## To be executed on node with Arguments
config.JobType.scriptExe   = 'scriptExe.sh'
config.JobType.scriptArgs  = ['nEvents=1500','nThreads=4','outputName=miniaodStep.root','higgsPtMin=250','higgsPtMax=500','higgsMassMin=80','higgsMassMax=160','higgsMassStepSize=2','nMassesPerJob=10']
config.JobType.inputFiles  = ['scriptExe.sh', 'gen_step_gghtt.py','sim_step.py','digi_raw_step.py','hlt_step.py','reco_step.py','miniaod_step.py','../pileup.py']
## Output file to be collected
config.JobType.outputFiles = ["miniaodStep.root"]
config.JobType.disableAutomaticOutputCollection = True
## Memory, cores, cmssw
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5500
config.JobType.numCores    = 4
## Data
config.Data.splitting   = 'EventBased'
config.Data.unitsPerJob = 1500
config.Data.totalUnits  = 1500000
config.Data.outLFNDirBase = '/store/user/rgerosa/PrivateMC/RunIISummer20UL18MiniAODv2/'
config.Data.publication   = True
config.Data.outputPrimaryDataset = 'GluGluHToTauTau_PtH_250to500_mH_80to160_TuneCP5_pythia8_13TeV'
config.Data.outputDatasetTag     = 'RunIISummer20UL18MiniAODv2_106X_upgrade2018_realistic_v11_L1v1-MINIAODSIM'
## Site
config.Site.storageSite = 'T2_US_UCSD' 
