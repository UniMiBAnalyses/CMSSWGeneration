#!/bin/sh
# activate scram command
source /cvmfs/cms.cern.ch/cmsset_default.sh
export LC_ALL=C; unset LANGUAGE
echo "Opening CMSSW_7_1_47_PYTHIA240"
tar -xzvf CMSSW_7_1_47_PYTHIA240.tgz
rm CMSSW_7_1_47_PYTHIA240.tgz
cd CMSSW_7_1_47_PYTHIA240/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
cmsRun SMP-RunIISummer15GS-00266_1_cfg.py
