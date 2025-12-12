# Process description

Use `MG5+Pythia8` to generate LO+PS ZH events in which the Z-boson decays in pairs of leptons and the Higgs boson to gluons.

NB: use madspin for correct use of polarization


# Gridpack generation

See instructions in
https://cms-generators.docs.cern.ch/how-to-produce-gridpacks/mg5-amcnlo/


# Installation

```sh
cmssw-el7
cmsrel CMSSW_10_6_30;
cd CMSSW_10_6_30/src;
cmsenv;
git-cms-init;
git clone git@github.com:UniMiBAnalyses/CMSSWGeneration.git;
cd CMSSWGeneration/crab_miniaod_production/Era2017UL/ZH_HToGluGlu_ZToLL_powheg_pythia8/
````


`Disclaimer`: base commands for the various steps are taken from [[McM]](https://cms-pdmv.cern.ch/mcm/) for the `RunIISummer20UL18MiniAODv2` production chain.
TBU


# Crab config files

The production of MC events is performed via crab. It is enough to create and submit a private MC task as indicated by the example config files placed in the directory.

There are example production configuration files, it is important in each of the to express
  * Name of the bash script that needs to be executed at the node `scriptExe.sh`
  * Parameters for the bash script provided as `scriptArgs`
  * Stage out folder on some computing center `T2_CH_CERN` used as default
  * Name of the DAS dataset that will be produced by crab publishing the nanoAOD files
  * Number of events and events per-job that will be produced.

    vomsgrid

    crab checkwrite --site=T2_CH_CERN  --lfn=/store/user/amassiro/PrivateMC/RunIISummer20UL17NanoAODv9/


    crab submit -c crabConfig_ZH_HToGluGlu_ZToLL_powheg_pythia8.py


    crab status -d ./crab_amassiro_crabConfig_ZH_HToGluGlu_ZToLL


    ls -alrth /eos/cms/store/user/amassiro/PrivateMC/RunIISummer20UL17NanoAODv9/
    /eos/cms/store/user/amassiro/PrivateMC/RunIISummer20UL17NanoAODv9/ZH_HToGluGlu_ZToLL/RunIISummer20UL17NanoAODv9_106X_mc2017_realistic_v6-MINIAODSIM/251211_103240/0000/

    Result:
    /ZH_HToGluGlu_ZToLL/amassiro-RunIISummer20UL17NanoAODv9_106X_mc2017_realistic_v6-MINIAODSIM-00000000000000000000000000000000/USER


Local test:

    cmsRun LHEGEN_step_cfg.py      inputGridpack=HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg.tgz      nEvents=10

    cmsRun  SIM_step_cfg.py  inputName=genStep.root outputName=simStep.root

    cmsRun  DIGI_RAW_premix_step_cfg.py inputName=simStep.root outputName=digirawStep.root



# build pileup list


    python3 generateDatasetFileList.py   --dataset  /Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX   -o mypileup.py

    /Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX












