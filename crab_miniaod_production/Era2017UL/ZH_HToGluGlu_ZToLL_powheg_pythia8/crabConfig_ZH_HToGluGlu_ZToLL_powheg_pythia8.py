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
config.JobType.scriptExe   = 'script.sh'
config.JobType.scriptArgs  = ['nEvents=1000','nThreads=4','outputName=nanoStep.root','inputGridpack=HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg.tgz']
config.JobType.inputFiles  = ['script.sh','LHEGEN_step_cfg.py','SIM_step_cfg.py','DIGI_RAW_premix_step_cfg.py','HLT_step_cfg.py','RECO_step_cfg.py','MINIAOD_step_cfg.py','NANOAODv9_step_cfg.py','../pileup.py','HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg.tgz']
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
config.Data.outputDatasetTag = 'RunIISummer20UL17NanoAODv9_106X_mc2017_realistic_v6-MINIAODSIM'
## Site
config.Site.storageSite = 'T2_CH_CERN'

# 106X_mc2017_realistic_v6

#T3_CH_CERNBOX




#
# from CRABClient.UserUtilities import config
#
# ## parameters
# nThreads = 4
# #configlhe = '../LHEGEN/' + datasetname + '_cfg.py'
# configlhe='LHEGEN_step_cfg.py'
# outputName = 'nanoAOD.root'
# _process = 'Zjj_UL_dim6'
# gp = _process + '_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
# datasetname = _process.upper()
# requestname = 'gpizzati_' + datasetname
# scriptExe = 'script.sh'
# nEvents = 2000
# nEventsTotal = 10000000
# year = '2017'
#
#
# ## config file
# config = config()
# ## General settings
# #config.General.requestName = 'gpizzati_ewk_lljj_' + gp.split('.')[0]
# config.General.requestName = requestname
# config.General.transferOutputs = True
# config.General.transferLogs = False
# ## PrivateMC type with a fake miniAOD step to circunvent crab requests (official data-tier for PrivateMC)
# config.JobType.pluginName  = 'PrivateMC'
# config.JobType.psetName    = configlhe
# config.JobType.pyCfgParams = ['nThreads='+str(nThreads), 'outputName='+outputName]
# ## To be executed on node with Arguments
# config.JobType.scriptExe   = scriptExe
# config.JobType.scriptArgs  = ['nEvents='+str(nEvents),'nThreads='+str(nThreads), 'gridpack=' + gp, 'outputName='+outputName]
# config.JobType.inputFiles  = [configlhe, 'CMSSW_10_6_26.tar.gz'] + ['DIGI_RAW_premix_step_cfg.py', 'HLT_step_cfg.py', 'MINIAOD_step_cfg.py', 'NANOAODv9_step_cfg.py', 'RECO_step_cfg.py', 'SIM_step_cfg.py']
# ## Output file to be collected
# config.JobType.outputFiles = [outputName]
# config.JobType.disableAutomaticOutputCollection = True
# ## Memory, cores, cmssw
# config.JobType.allowUndistributedCMSSW = True
# config.JobType.maxMemoryMB = 2000 * nThreads
# config.JobType.numCores    = nThreads
# ## Data
# config.Data.splitting   = 'EventBased'
# config.Data.unitsPerJob = nEvents
# config.Data.totalUnits  = nEventsTotal
# config.Data.outLFNDirBase = '/store/user/gpizzati/PrivateMC/EFT/' + _process
# config.Data.publication   = True
# config.Data.outputPrimaryDataset = datasetname
# # config.Data.outputDatasetTag = 'RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v11_NANOAODSIM'
# config.Data.outputDatasetTag = 'RunIISummer20UL_' + year + '_NANOAODSIM'
# ## Site
# #config.Site.storageSite = 'T2_US_UCSD'
# config.Site.storageSite = 'T3_IT_MIB'
