# Process description

Use `Madrgraph+Pythia8` to generate NMSSM heavy scalar X, with mass $m_{X}$, at LO in QCD+EW using default dynmaic QCD-scale, PDF set (NNPDF 3.1), and PS Tune adopted by the official UL production. The NMSSM scalar decays into two bosons: one Higgs boson with mass of 125 GeV, and one Y boson with mass $m_{Y}$. In `Pythia` the Higgs boson is decayed to a $bb$-pair while the Y boson decays to a $\tau\tau$ final state using the `ResonanceDecayFilter` module. Every job can generate different combinations of $m_{X}$ and $m_{Y}$ masses on the basis of the exsisting gridpacks.

# Installation

```sh
cmsrel CMSSW_12_4_14_patch2;
cd CMSSW_12_4_14_patch2/src;
cmsenv;
git-cms-init;
git clone git@github.com:UniMiBAnalyses/CMSSWGeneration.git;
cd CMSSWGeneration/crab_miniaod_production/Era2022EE/QCD_HTbinned_BEnriched_Madgraph
````

# Gridpack generation

First checkout the genproduction repository used for the UL production (with the MG version for UL) and create a tarball in order to be copied to the condorHT node. Checkout outside a cmssw release.

```sh
git clone https://github.com/cms-sw/genproductions.git 
tar -czvf genproductions_run3.tar.gz genproductions
```
		
In order to produce the gridpacks please follow the guidelines below:
* GEN-POG twiki with instructions for MG event generation [[MadGraph-Instructions]](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO)

In order to automatically submit gridpacks generation as condor-jobs you can use the following recipe. Please be aware that this works well for fast processes i.e. every job computes the gridpack locally without splitting in many child condor tasks. In case heavy gridpacks needs to be built, please look the second part of this guideline
* Run the script from an `lxplus` machine and select the best scheduler available via `myschedd bump`
* Submit gridpack generation: 
  ```sh
  cd CMSSWGeneration/crab_miniaod_production/Era2022EE/QCD_HTbinned_BEnriched_Madgraph;
  voms-proxy-init -voms cms --valid 192:00
  python3 produceGridpackJobs.py -i input_cards -d /eos/cms/store/user/rgerosa/genproductions_run3.tar.gz -j job_gridpack_qcd -o /eos/cms/store/user/rgerosa/QCD_HTbinned_BEnriched_gridpacks --command submit --njet 2 3 4 5 --htbin 200,350 350,500 500,750 750,1000 1000,-1 --proxy /tmp/x509up_u21491 --ncpu 4 --gridpack-script genproductions/bin/MadGraph5_aMCatNLO/gridpack_generation.sh
  ```
  * `-i`: folder containing the base MG cards `input_cards`
  * `-d`: path to the `genproductions` tar archive that is created with the instructions listed above
  * `-s`: relative path to the gen production script to be used for MG
  * `--njet`: list of njets card that needs to be considered for the gridpack generation
  * `--nbjet`: list of nbjets card that needs to be considered for the gridpack generation. Each process contains 3,4,5 jet events with nbjet as hadron flavour multiplicity
  * `--htbin`: list of htbin card that needs to be considered for the gridpack generation
  * `-j`: directory where condorHT job files are created
  * `--ncpu`: number of cpus to use
  * `--proxy`: ship the proxy file if needed
  * `--options-for-gridpack`: options that needs to be give for the gridpack production
  * `-o`: output folder where the gridpacks are copied
  * `--command`: either `submit` or `none`

In the case of heavy gridpacks, like b-quark enriched with up to 6 jets in the final state, gripacks needs to be run manually as tmux session on lxplus machines or a local machine that can be interfaced with condor job. In order to do so, please consider the following guideline to create a keytab credential file:
* Procedure is described here [[AFS Permissions]](https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO#Monitoring_afs_permissions_for_c)
* This creates a ktmux session that can be used to run the official `submit_condor_gridpack_generation.sh` with condor script
* In order to submit the gridpack production, all the input run/proc/customized cards need to be produced as follows
  ```sh
  cd CMSSWGeneration/crab_miniaod_production/Era2022EE/QCD_HTbinned_BEnriched_Madgraph;
  scp /eos/cms/store/user/rgerosa/genproductions_run3.tar.gz ./
  tar -xf genproductions_run3.tar.gz
  python3 produceGridpackJobs.py -i input_cards -j card_for_gridpacks --command card --nbjet 2 3 --htbin 200,350 350,500 500,750 750,1000 1000,-1
  ```
* Finally, each gridpack generation needs to be launched within a tmux session as follows:
  ```sh
  ktmux;
  cd /tmp/rgerosa/;
  scp -r /eos/cms/store/user/rgerosa/genproductions_run3.tar.gz ./
  tar -xf genproductions_run3.tar.gz
  rm -rf genproductions_run3.tar.gz
  cd -;
  scp -r card_for_gridpacks/* /tmp/rgerosa/genproductions/bin/MadGraph5_aMCatNLO/;
  cd -;
  cd genproductions/bin/MadGraph5_aMCatNLO/;
  ./submit_condor_gridpack_generation.sh QCD_bEnriched_2bjet_HT_200_350 QCD_bEnriched_2bjet_HT_200_350
  ```

# LHE+GEN+SIM step

`Disclaimer`: base commands for the various steps are taken from [[McM]](https://cms-pdmv.cern.ch/mcm/) for the `Run3Summer22EEDRPremix` production chain. 

* Generate the base configuration via:
  ```sh
  cd $CMSSW_BASE/src;
  curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/EGM-Run3Summer22EEwmLHEGS-00001 --retry 3 --create-dirs -o Configuration/GenProduction/python/EGM-Run3Summer22EEwmLHEGS-00001-fragment.py
  scram b
  cmsDriver.py Configuration/GenProduction/python/EGM-Run3Summer22EEwmLHEGS-00001-fragment.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:EGM-Run3Summer22EEwmLHEGS-00001.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n 100
  ```
* Then, the `gen_step.py` is produced with the following settings:
  * `jobNum`: job number used to set the luminosity block
  * `nEvents`: number of events that will be generated
  * `outputName`: name of the output GEN to be produced
  * `nThreads`: number of parallel threads
  * `gridpack`: gridpack that needs to be used for the event simulation
  * The run number is set to be equal to the job number with number of events equal to nEvents apart from the ME/PS matching efficiency (MLM)

# DIGI-RAW-HLT step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename EGM-Run3Summer22EEDRPremix-00004_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-Run3Summer22EEDRPremix-00004_0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v14 --procModifiers premix_stage2,siPixelQualityRawToDigi --geometry DB:Extended --filein file:EGM-Run3Summer22EEwmLHEGS-00001.root --datamix PreMix --era Run3 --no_exec --mc -n 100
  ```
* Then, the `digi_raw_hlt_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN-SIM events (local file)
  * `outputName`: name of the output GEN-SIM-RAW-DIGI file to be produced
  * `pileupName`: name of the pileup file that by default is `pileup.py` as described below.
  * The list of pileup prexix files from `/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX` is provided as `pileup.py` file via:
    ```sh
    dasgoclient --query "file dataset=/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX" > ../pileup.py
    ```

# RECO-AOD step

* Generate the base configuration via:
  ```sh
  cmsDriver.py  --python_filename EGM-Run3Summer22EEDRPremix-00004_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-Run3Summer22EEDRPremix-00004.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM --procModifiers siPixelQualityRawToDigi --geometry DB:Extended --filein file:EGM-Run3Summer22EEDRPremix-00004_0.root --era Run3 --no_exec --mc -n 1 ;
  ```
* Then, the `reco_step.py` is produced with the following settings:
  * `nThreads`: number of parallel threads
  * `inputName`: name of the input file containing GEN-SIM-DIGI-RAW events (local file)
  * `outputName`: name of the output AODSIM file to be produced

# MINIAOD step

* Generate the base configuration via:
  ```sh
cmsDriver.py  --python_filename EGM-Run3Summer22EEMiniAODv3-00016_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-Run3Summer22EEMiniAODv3-00016.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step PAT --geometry DB:Extended --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22EEDRPremix-forPOG_124X_mcRun3_2022_realistic_postEE_v1-v2/AODSIM" --era Run3 --no_exec --mc -n 1 ;
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