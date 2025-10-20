# Process description

Use `Pythia8` to generate H+jets events at LO, using default CMS tune and parameters for the shower and PDF. The generation in performed in bins of Higgs $p_{T}$ and with exclusive decays into a $\tau\tau$ final state. In addition, every job can set different random values for $m_{H}$ within a certain chosen range and according to a certain step size. This allows to uniformly sample the Higgs boson mass within a certain range

# Installation

```sh
cmsrel CMSSW_10_6_30;
cd CMSSW_10_6_30/src;
cmsenv;
git-cms-init;
git clone git@github.com:UniMiBAnalyses/CMSSWGeneration.git;
cd CMSSWGeneration/crab_miniaod_production/Era2018UL/GluGluHToTauTau_Variable_MH 
````

`Disclaimer`: base commands for the various steps are taken from [[McM]](https://cms-pdmv.cern.ch/mcm/) for the `RunIISummer20UL18MiniAODv2` production chain. 

# LHE+GEN step

* Generate the base configuration via:
  ```sh
  cd $CMSSW_BASE/src;
  curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer20UL18wmLHEGEN-01612 --retry 3 --create-dirs -o Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-01612-fragment.py
  scram b 
  cmsDriver.py Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-01612-fragment.py --python_filename HIG-RunIISummer20UL18wmLHEGEN-01612_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:HIG-RunIISummer20UL18wmLHEGEN-01612.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 1;
  ```
* Then, the `gen_step.py` is produced with the following settings:
  * `jobNum`: job number used to set the luminosity block
  * `jobEvents`: events generated in this job in total
  * `nEvents`: number of events that will be generated
  * `outputName`: name of the output GEN to be produced
  * `nThreads`: number of parallel threads
  * `higgsPtMin`: minimum pTHat used in the event generation (a measurement of the hardness of the event). Then, a GEN filter is applied asking post-shower Higgs $`p_{T}`$ to be above `higgsPtMin`.
  * `higgsPtMax`: maximum pTHat used in the event generation (a measurement of the hardness of the event). Then, a GEN filter is applied asking post-shower Higgs $`p_{T}`$ to be below `higgsPtMax`.
  * `higgsMassMin`: minimum mass of the Higgs boson that should be considered by the random sampling
  * `higgsMassMax`: maximum mass of the Higgs boson that should be considered by the random sampling
  * `higgsMassStepSize`: discrete step size that needs to be considered in the mass sampling
  * `generationStep`: integer number used to set the lumi-section value
  * The run number is set to be equal to the job number but, within each job, multiple mass values are sampled/generated. Each of them is identified by the luminosity value.

# SIM-step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18SIM-01019_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:HIG-RunIISummer20UL18SIM-01019.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:HIG-RunIISummer20UL18wmLHEGEN-01612.root --era Run2_2018 --runUnscheduled --no_exec --mc -n -1  
  ```
* Then, the `sim_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN events (local file)
  * `outputName`: name of the output GEN-SIM file to be produced

# DIGIRAW step
* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18DIGIPremix-01000_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:HIG-RunIISummer20UL18DIGIPremix-01000.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:HIG-RunIISummer20UL18SIM-01019.root --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;  
  ```
* Then, the `digi_raw_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN-SIM events (local file)
  * `outputName`: name of the output GEN-SIM-RAW-DIGI file to be produced
  * `pileupName`: name of the pileup file that by default is `pileup.py` as described below.
  * The list of pileup prexix files from `/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX` is provided as `pileup.py` file via:
    ```sh
    dasgoclient --query "file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" > ../pileup.py
    ```

# HLT step

* Generate the base configuration via:
  ```sh
  cmsrel CMSSW_10_2_16_UL
  cd CMSSW_10_2_16_UL/src
  eval `scram runtime -sh`
  cd -
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18HLT-01019_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:HIG-RunIISummer20UL18HLT-01019.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --geometry DB:Extended --filein file:HIG-RunIISummer20UL18DIGIPremix-01000.root --era Run2_2018 --no_exec --mc -n 1 ;
  ```
*Then, the `hlt_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN-SIM-DIGI-RAW events (local file)
  * `outputName`: name of the output GEN-SIM-RAW-DIGI file to be produced

# RECO step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18RECO-01019_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:HIG-RunIISummer20UL18RECO-01019.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:HIG-RunIISummer20UL18HLT-01019.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 1 ;
  ```
* Then, the `reco_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN-SIM-DIGI-RAW events (local file)
  * `outputName`: name of the output AODSIM file to be produced

# MINIAOD step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18MiniAODv2-01090_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:HIG-RunIISummer20UL18MiniAODv2-01090.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "dbs:/GluGluToRadionToHHTo2B2Tau_M-250_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n 1;
  ```
* Then, the `miniaod_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing RECO events (local file)
  * `outputName`: name of the output MINIAOD file to be produced
* Finally, copy `miniaod_step.py` into `miniaod_step_fake.py` in order to submit the crab jobs. The only difference between the two is replacing the `PoolSource` with an `EmptySource` module as expected for event generation

# Crab config files

* The production of MC events is performed via crab. It is enough to create and submit a private MC task as indicated by the example config files placed in the directory.
* There are example production configuration files, it is important in each of the to express
  * Name of the bash script that needs to be executed at the node `scriptExe.sh`
  * Parameters for the bash script provided as `scriptArgs`
  * Stage out folder on some computing center `T2_US_UCSD` used as default
  * Name of the DAS dataset that will be produced by crab publishing the miniAOD files
  * Number of events and events per-job that will be produced.