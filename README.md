# CMSSWGeneration

Instructions on how to generate a private sample using crab in CMSSW 

Assumptions:

- LHE are available
- premixed library is available


Prepare to get premix library:

    voms-proxy-init -voms cms -rfc

LHE:

    example: /afs/cern.ch/user/g/govoni/myeos/samples/2019_EFT/SSeu/SM_limit/SSeu_SMlimit_results/1441466/SSeu_SMlimit_3/unweighted_events.lhe
    

Example of outputs for 2017 production

    https://github.com/latinos/LatinoAnalysis/blob/master/NanoGardener/python/framework/samples/fall17_102X_nAODv5.py

    From the name of the sample:
    /GluGluHToWWTo2L2Nu_M125_13TeV_powheg2_JHUGenV714_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
    Get the different steps (backward) in the generation:
    
    NanoAOD
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17NanoAODv5-00331&page=0&shown=127
    
    MiniAOD 
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17MiniAODv2-02464&page=0&shown=127
    
    PreMix 
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17DRPremix-02533&page=0&shown=127
    
    wmLHE
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17wmLHEGS-01920&page=0&shown=127
    
Instructions:

    NanoAOD
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Running_on_various_datasets_from
    
    


    

Produce (from RunTheMatrix):

    # in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --conditions auto:phase1_2017_realistic -n 10 --era Run2_2017 --eventcontent FEVTDEBUG --relval 9000,50 -s GEN,SIM --datatier GEN-SIM --beamspot Realistic25ns13TeVEarly2017Collision --io TTbar_13UP17.io --python TTbar_13UP17.py --fileout file:step1.root  --nThreads 8 > step1_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step2  --datamix PreMix --conditions auto:phase1_2017_realistic --pileup_input das:/RelValPREMIXUP17_PU25/CMSSW_10_6_0-PU25ns_106X_mc2017_realistic_v3-v1/PREMIX --era Run2_2017 --procModifiers premix_stage2 -s DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,HLT:@relval2017 --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --eventcontent FEVTDEBUGHLT --io DIGIPRMXUP17_PU25_RD.io --python DIGIPRMXUP17_PU25_RD.py -n 100  --filein  file:step1.root  --fileout file:step2.root  --nThreads 8 > step2_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step3  --conditions auto:phase1_2017_realistic -n 10 --era Run2_2017 --eventcontent RECOSIM,MINIAODSIM,DQM --runUnscheduled  --procModifiers premix_stage2 -s RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT,VALIDATION:@standardValidationNoHLT+@miniAODValidation,DQM:@standardDQMFakeHLT+@miniAODDQM --datatier GEN-SIM-RECO,MINIAODSIM,DQMIO --io RECOPRMXUP17_PU25.io --python RECOPRMXUP17_PU25.py --filein  file:step2.root  --fileout file:step3.root  --nThreads 8 > step3_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step4  --conditions auto:phase1_2017_realistic -s HARVESTING:@standardValidationNoHLT+@standardDQMFakeHLT+@miniAODValidation+@miniAODDQM --filetype DQM --geometry DB:Extended --era Run2_2017 --mc  --io HARVESTUP17_PU25.io --python HARVESTUP17_PU25.py -n 100  --filein file:step3_inDQM.root --fileout file:step4.root  > step4_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1

    

Where:

    /home/amassiro/Cern/Code/UniMiB/CMSSWGeneration
    
    /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Generation
    
    
-------------

# UL2020 SMEFTsim gridpack generation

In order to generate gradpacks for the LHE production stage one can take inspiration from https://github.com/GiacomoBoldrini/cmsgen .
The repo contains cards to produce gridpacks for inclusive WW with EFT contributions via SMEFTsim madgraph model.
The ReadMe describes the steps to produce gridpacks for the UL2020 campaign. For different campaigns or production one should carefully choose which branch of the genproduction to clone (UL2019 branch has mg 261 while master branch, as of  28/01/2020, has mg 265).
    
    
