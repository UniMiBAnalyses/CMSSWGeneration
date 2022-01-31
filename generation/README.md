# Some useful scripts to generate with Full Sim given a gridpack

## First Step: Download input files for a given year
Use `Downloader.py` to dowload input files if you want to change the configuration based on other flow than WLLJJ_WToLNu_EWK.
First you should change links in Steps.json. Then Downloader will take care of editing `SCRAM_ARCH`, `release` and `filename`.
You might specify all the steps at one time, but only one year.



# Full Sim generation
`Generate.py` uses the file `Steps.json` to create the configuration for the full generation given a name, the path to gridpack and the year.




## Input files
Since the generation flow was made to produce NanoAODv7 102x the final step will be nanoAODv7 with the use of CMSSW_10_2_22 (10_2_X).
Since 2018 input files came from [WLLJJ_WToLNu_EWK](https://cms-pdmv.cern.ch/mcm/chained_requests?contains=SMP-RunIIAutumn18NanoAODv7-00058&page=0&shown=15), I created input files for 2017 and 2016 based on [WLLJJ_WToLNu_EWK 2017 flow](https://cms-pdmv.cern.ch/mcm/chained_requests?contains=SMP-RunIIFall17NanoAODv7-00030&page=0&shown=15) and [WLLJJ_WToLNu_EWK 2016 flow](https://cms-pdmv.cern.ch/mcm/chained_requests?contains=SMP-RunIISummer16NanoAODv7-00241&page=0&shown=15) 


### Technical Things
For 2018 Generation using:
CMSSW_10_2_6 for LHE, Premix and miniAOD
CMSSW_10_2_22 for nanoAOD

2017:
CMSSW_9_3_4 for LHE
CMSSW_9_4_6_patch1 for Premix and miniAOD
CMSSW_10_2_22 for nanoAOD

2016 using:
CMSSW_7_1_21_patch2 for LHE
CMSSW_8_0_21 for Premix
CMSSW_9_4_9 for miniAOD
CMSSW_10_2_22 for nanoAOD