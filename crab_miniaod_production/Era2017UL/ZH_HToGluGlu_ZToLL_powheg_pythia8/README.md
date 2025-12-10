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

    crab checkwrite --site=T2_CH_CERN  --lfn=/store/user/amassiro/PrivateMC/RunIISummer20UL18NanoAODv9/


    crab submit -c crabConfig_VH_H_VToLL_VL_mg_pythia8.py


    crab status -d ./crab_amassiro_crabConfig_VH_H_VToLL_VL


    ls -alrth /eos/cms/store/user/amassiro/PrivateMC/RunIISummer20UL18NanoAODv9/


    /eos/cms/store/user/amassiro/PrivateMC/RunIISummer20UL18NanoAODv9/VH_H_VToLL_VL_mg_pythia8/RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v11_L1v1-MINIAODSIM/251023_085208/0000/nanoStep_231.root






== CMSSW: Running MG5_aMC for the 89 time
== CMSSW: produced_lhe  0 nevt  1000 submitting_event  1000  remaining_event  1000
== CMSSW: run.sh 1000 2970098
== CMSSW: Now generating 1000 events with random seed 2970098 and granularity 1
== CMSSW: python3: /lib64/libc.so.6: version `GLIBC_2.28' not found (required by /cvmfs/cms.cern.ch/el8_amd64_gcc10/cms/cmssw/CMSSW_12_4_8/external/el8_amd64_gcc10/lib/libpython3.9.so.1.0)
== CMSSW: python3: /lib64/libc.so.6: version `GLIBC_2.25' not found (required by /cvmfs/cms.cern.ch/el8_amd64_gcc10/cms/cmssw/CMSSW_12_4_8/external/el8_amd64_gcc10/lib/libpython3.9.so.1.0)
== CMSSW: python3: /lib64/libc.so.6: version `GLIBC_2.26' not found (required by /cvmfs/cms.cern.ch/el8_amd64_gcc10/cms/cmssw/CMSSW_12_4_8/external/el8_amd64_gcc10/lib/libpython3.9.so.1.0)
== CMSSW: python3: /lib64/libc.so.6: version `GLIBC_2.27' not found (required by /cvmfs/cms.cern.ch/el8_amd64_gcc10/cms/cmssw/CMSSW_12_4_8/external/el8_amd64_gcc10/lib/libpython3.9.so.1.0)
== CMSSW: mv: cannot stat './Events/GridRun_2970098/unweighted_events.lhe.gz': No such file or directory
== CMSSW: write ./events.lhe.gz
== CMSSW: gzip: events.lhe.gz: No such file or directory
== CMSSW: mv: cannot stat 'events.lhe.gz': No such file or directory
== CMSSW: run 89 finished, total number of produced events: 0/1000
== CMSSW:
== CMSSW: Running MG5_aMC for the 90 time
== CMSSW: produced_lhe  0 nevt  1000 submitting_event  1000  remaining_event  1000
== CMSSW: run.sh 1000 2970099
== CMSSW: Now generating 1000 events with random seed 2970099 and granularity 1



Local test:

    cmsRun gen_step.py      inputGridpack=VHpolar_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz      nEvents=10


    WARNING: Developer's area is created for architecture el8_amd64_gcc10 while your current OS is slc7_amd64.
    WARNING: You are trying to use SCRAM architecture 'el8' on host with operating system 'slc7'.
         This is not supported and likely will not work and you might get build/runtime errors. Please either
         - use correct SCRAM_ARCH to match your host's operating system.
         - OR use 'cmssw-el8' script to start a singularity container (http://cms-sw.github.io/singularity.html)
         - OR use host which has 'el8' installed e.g. lxplus8 for el8, lxplus9 for el9 or lxplus7 for slc7.




# build pileup list


    python3 generateDatasetFileList.py   --dataset  /Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX   -o mypileup.py



    /Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX












