# Process description

Use `Madrgraph+Pythia8` to generate NMSSM heavy scalar X, with mass $m_{X}$, at LO in QCD+EW using default dynmaic QCD-scale, PDF set (NNPDF 3.1), and PS Tune adopted by the official UL production. The NMSSM scalar decays into two bosons: one Higgs boson with mass of 125 GeV, and one Y boson with mass $m_{Y}$. In `Pythia` the Higgs boson is decayed to a $bb$-pair while the Y boson decays to a $\tau\tau$ final state using the `ResonanceDecayFilter` module. Every job can generate different combinations of $m_{X}$ and $m_{Y}$ masses on the basis of the exsisting gridpacks.

# Installation

```sh
cmsrel CMSSW_10_6_30;
cd CMSSW_10_6_30/src;
cmsenv;
git-cms-init;
git clone git@github.com:UniMiBAnalyses/CMSSWGeneration.git;
cd CMSSWGeneration/crab_miniaod_production/Era2018UL/NMSSM_XToYHTo2B2Tau_Madgraph
````

# Gridpack generation

First checkout the genproduction repository used for the UL production (with the MG version for UL) and create a tarball in order to be copied to the condorHT node:

```sh
git clone https://github.com/cms-sw/genproductions.git -b mg265UL
tar -czvf genproductions.tar.gz genproductions
```
		
In order to produce the gridpacks of interest please follow the guidelines below:
* GEN-POG twiki with instructions for MG event generation [[MadGraph-Instructions]](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO)
* The directory `InputMadgraphCards` contains all run/proc/customize cards needed for each sample to be generated i.e. each $m_{X}$ and $m_{Y}$ value. These are the inputs needed for each gridpack generation
* The gridpack generation for each mass point happens using the CERN CondorHT batch by using the official CMS GEN group submission workflow contained in `genproductions/bin/MadGraph5_aMCatNLO/`. In particular, the `gridpack_generation.sh` and a custom CondorHT CERN submission scripts `produceGridpackJobs.py` are used;
* Submit gridpack generation: 
  ```sh
  cd CMSSWGeneration/crab_miniaod_production/Era2018UL/NMSSM_XToYHTo2B2Tau_Madgraph;
  python produceGridpackJobs.py -i input_cards -d /eos/cms/store/user/rgerosa/genproductions.tar.gz -j job_gridpack_mssm -o /eos/cms/store/user/rgerosa/NMSSM_XToYH_gridpacks/ --command submit -x 300 360 400 450 500 550 600 650 700 750 800 850 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2200 2400 2500 -y 105 110 115 120 130 135 140 145
  ```
  * `-i`: folder containing the base MG cards `input_cards`
  * `-d`: path to the `genproductions` tar archive that is created with the instructions listed above
  * `-s`: relative path to the gen production script to be used for MG
  * `-x`: list of $m_{X}$ that needs to be considered for the gridpack generation
  * `-y`: list of $m_{Y}$ that needs to be considered for the gridpack generation
  * `-j`: directory where condorHT job files are created
  * `-o`: output folder where the gridpacks are copied
  * `--command`: either `submit` or `none`
* Run the script from an `lxplus` machine and select the best scheduler available via `myschedd bump`

# Download of gridpacks

* In every crab job, the gridpacks for a certain number of mass hypothesis are downloaded locally in the job scratch directory and are used in the generation. This is performed via the `copy_gridpacks.py` script that takes as input arguments:
 ``` 
 * `-i`: directory where all gridpacks are located on a CMS Storage Element
 * `-o`: name of the output file containing the gridpacks used in the job that are copied locally in the scratch directory (job node)
 * `-g`: addres of the Storage Element that can be used by `gfal` 
 * `-xmin` and `-xmax`: min and max values of $m_{X}$ in the gridpacks that are considered
 * `-ymin` and `-ymax`: min and max values of $m_{Y}$ in the gridpacks that are considered
 * Example:
 ```sh
 python copy_gridpacks.py -i /store/user/rgerosa/NMSSM_XToYH_gridpacks/ -o gridpack.list --mxmin=1000 --mxmax=1500 --mymin=120 --mymax=130
 * Caveat: `gfal` can be used only before doing `cmsenv`

# LHE+GEN step

`Disclaimer`: base commands for the various steps are taken from [[McM]](https://cms-pdmv.cern.ch/mcm/) for the `RunIISummer20UL18MiniAODv2` production chain. 

* Generate the base configuration via:
  ```sh
  cd $CMSSW_BASE/src;
  curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer20UL18wmLHEGEN-08870 --retry 3 --create-dirs -o Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-08870-fragment.py
  scram b 
  cmsDriver.py Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-08870-fragment.py --python_filename HIG-RunIISummer20UL18wmLHEGEN-08870_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:HIG-RunIISummer20UL18wmLHEGEN-08870.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 1;
  ```
* Then, the `gen_step.py` is produced with the following settings:
  * `jobNum`: job number used to set the luminosity block
  * `jobEvents`: events generated in this job in total
  * `nEvents`: number of events that will be generated
  * `outputName`: name of the output GEN to be produced
  * `nThreads`: number of parallel threads
  * `generationStep`: integer number used to set the lumi-section value
  * `gridpacks`: file with the list of gridpack names to be considered in the random sampling
  * The run number is set to be equal to the job number but, within each job, multiple mass values are sampled/generated. Each of them is identified by the luminosity value.

# SIM-step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18SIM-01019_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:HIG-RunIISummer20UL18SIM-01019.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:HIG-RunIISummer20UL18wmLHEGEN-08870.root --era Run2_2018 --runUnscheduled --no_exec --mc -n -1  
  ```
* Then, the `sim_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN events (local file)
  * `outputName`: name of the output GEN-SIM file to be produced

# DIGIRAW step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename HIG-RunIISummer20UL18DIGIPremix-01000_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:HIG-RunIISummer20UL18DIGIPremix-01000.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:HIG-RunIISummer20UL18SIM-01019.root --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n 1 ;  
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