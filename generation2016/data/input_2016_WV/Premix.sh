#!/bin/sh
# activate scram command
source /cvmfs/cms.cern.ch/cmsset_default.sh
export LC_ALL=C; unset LANGUAGE
# now run PREMIX step
echo "Opening CMSSW_8_0_31"
tar -xzvf CMSSW_8_0_31.tgz
rm CMSSW_8_0_31.tgz
cd CMSSW_8_0_31/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

# step 1
cmsRun SMP-RunIISummer16DR80Premix-00645_1_cfg.py

# step 2
cmsRun SMP-RunIISummer16DR80Premix-00645_2_cfg.py
