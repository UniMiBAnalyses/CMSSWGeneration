#!/bin/bash                                                                                                                                                                                       
set -e
BASE=$PWD
RELEASE_BASE=$CMSSW_BASE

export SCRAM_ARCH=el8_amd64_gcc10
source /cvmfs/cms.cern.ch/cmsset_default.sh

echo "setting up CMSSW environment"
cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

echo "cmsRun -e -j FrameworkJobReport.xml gen_sim_step.py jobNum="$1" "$2" "$3" outputName=genSimStep.root "$5
cmsRun -e -j FrameworkJobReport.xml gen_sim_step.py jobNum=$1 $2 $3 outputName=genSimStep.root $5

echo "cmsRun -e -j FrameworkJobReport.xml digi_raw_hlt_step.py "$3" inputName=genSimStep.root outputName=digirawStep.root"
cmsRun -e -j FrameworkJobReport.xml digi_raw_hlt_step.py $3 inputName=genSimStep.root outputName=digirawStep.root
rm genSimStep.root

echo "cmsRun -e -j FrameworkJobReport.xml reco_step.py "$3" inputName=digirawStep.root outputName=recoHltStep.root"
cmsRun -e -j FrameworkJobReport.xml reco_step.py $3 inputName=digirawStep.root outputName=recoHltStep.root
rm digirawStep.root

echo "cmsRun -e -j FrameworkJobReport.xml miniaod_step.py "$3" inputName=recoHltStep.root "$4
cmsRun -e -j FrameworkJobReport.xml miniaod_step.py $3 inputName=recoHltStep.root $4
rm recoHltStep.root
