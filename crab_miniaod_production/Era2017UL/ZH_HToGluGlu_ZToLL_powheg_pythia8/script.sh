#!/bin/bash
set -e
BASE=$PWD
RELEASE_BASE=$CMSSW_BASE

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

echo "setting up CMSSW environment"
cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

echo "cmsRun -e -j FrameworkJobReport.xml LHEGEN_step_cfg.py jobNum="$1" "$2" "$3" outputName=genStep.root" $5
cmsRun -e -j FrameworkJobReport.xml LHEGEN_step_cfg.py jobNum=$1 $2 $3 outputName=genStep.root $5

echo "cmsRun -e -j FrameworkJobReport.xml SIM_step_cfg.py "$3" inputName=genStep.root outputName=simStep.root"
cmsRun -e -j FrameworkJobReport.xml SIM_step_cfg.py $3 inputName=genStep.root outputName=simStep.root
rm genStep*.root

echo "cmsRun -e -j FrameworkJobReport.xml DIGI_RAW_premix_step_cfg.py "$3" inputName=simStep.root outputName=digirawStep.root"
cmsRun -e -j FrameworkJobReport.xml DIGI_RAW_premix_step_cfg.py $3 inputName=simStep.root outputName=digirawStep.root
rm simStep*.root

scram p CMSSW CMSSW_9_4_14_UL_patch1
cd CMSSW_9_4_14_UL_patch1/src
eval `scram runtime -sh`
cd ../../

# scram p CMSSW CMSSW_10_2_16_UL
# cd CMSSW_10_2_16_UL/src
# eval `scram runtime -sh`
# cd ../../

echo "cmsRun -e -j FrameworkJobReport.xml HLT_step_cfg.py "$3" inputName=digirawStep.root outputName=hltStep.root"
cmsRun -e -j FrameworkJobReport.xml HLT_step_cfg.py $3 inputName=digirawStep.root outputName=hltStep.root
rm digirawStep.root

cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

echo "cmsRun -e -j FrameworkJobReport.xml RECO_step_cfg.py "$3" inputName=hltStep.root outputName=recoStep.root"
cmsRun -e -j FrameworkJobReport.xml RECO_step_cfg.py $3 inputName=hltStep.root outputName=recoStep.root
rm hltStep.root

echo "cmsRun -e -j FrameworkJobReport.xml MINIAOD_step_cfg.py "$3" inputName=recoStep.root outputName=miniStep.root"
cmsRun -e -j FrameworkJobReport.xml MINIAOD_step_cfg.py $3 inputName=recoStep.root outputName=miniStep.root
rm recoStep.root

echo "cmsRun -e -j FrameworkJobReport.xml NANOAODv9_step_cfg.py "$3" inputName=miniStep.root "$4
cmsRun -e -j FrameworkJobReport.xml NANOAODv9_step_cfg.py $3 inputName=miniStep.root $4
rm miniStep.root



# #!/bin/bash
# set -e
# BASE=$PWD
# RELEASE_BASE=$CMSSW_BASE
#
# source /cvmfs/cms.cern.ch/cmsset_default.sh
#
# #cd $RELEASE_BASE
# #eval `scram runtime -sh`
# #cd $BASE
#
#
# mkdir tmp
# cd tmp
# cp ../CMSSW_10_6_26.tar.gz .
# tar -xzvf CMSSW_10_6_26.tar.gz
# rm CMSSW_10_6_26.tar.gz
# cd CMSSW_10_6_26/src/
# scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
# eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
# echo $CMSSW_BASE
# cd ../../../
#
#
# splits=($(echo $4 | tr "=" " "))
# gp=${splits[1]}
#
# xrdcp -f root://eoscms.cern.ch//store/group/offcomp_upgrade-sw/gpizzati/gps/${gp} .
#
# ls ./${gp}
#
# scram p CMSSW CMSSW_10_6_29
# cd CMSSW_10_6_29/src
# eval `scram runtime -sh`
# cd ../../
#
# cmsRun -e -j FrameworkJobReport.xml LHEGEN_step_cfg.py jobNum=$1 $2 $3 outputName=lheGenStep"_"$1.root gridpack=${gp}
#
#
# scram p CMSSW CMSSW_10_6_17_patch1
# cd CMSSW_10_6_17_patch1/src
# eval `scram runtime -sh`
# cd ../../
#
# cmsRun -e -j FrameworkJobReport.xml SIM_step_cfg.py $3 inputName=lheGenStep_$1.root outputName=simStep_$1.root
# rm lheGenStep"_"$1.root
#
# cmsRun -e -j FrameworkJobReport.xml DIGI_RAW_premix_step_cfg.py $3 inputName=simStep_$1.root outputName=digiRawStep_$1.root
# rm simStep"_"$1.root
#
#
# scram p CMSSW CMSSW_9_4_14_UL_patch1
# cd CMSSW_9_4_14_UL_patch1/src
# eval `scram runtime -sh`
# cd ../../
#
# echo "cmsRun -e -j FrameworkJobReport.xml HLT_step_cfg.py "$3" inputName=digiRawStep_"$1".root outputName=hltStep_"$1".root"
# cmsRun -e -j FrameworkJobReport.xml HLT_step_cfg.py $3 inputName=digiRawStep_$1.root outputName=hltStep_$1.root
# rm digiRawStep"_"$1.root
#
#
# cd CMSSW_10_6_17_patch1/src
# eval `scram runtime -sh`
# cd ../../
#
# echo "cmsRun -e -j FrameworkJobReport.xml RECO_step_cfg.py "$3" inputName=hltStep_"$1".root outputName=recoStep_"$1".root"
# cmsRun -e -j FrameworkJobReport.xml RECO_step_cfg.py $3 inputName=hltStep_$1.root outputName=recoStep_$1.root
# rm hltStep"_"$1.root
#
#
# scram p CMSSW CMSSW_10_6_20
# cd CMSSW_10_6_20/src
# eval `scram runtime -sh`
# cd ../../
#
# echo "cmsRun -e -j FrameworkJobReport.xml MINIAOD_step_cfg.py "$3" inputName=recoStep_"$1".root outputName=miniAODStep_"$1".root"
# cmsRun -e -j FrameworkJobReport.xml MINIAOD_step_cfg.py $3 inputName=recoStep_$1.root outputName=miniAODStep_$1.root
# rm recoStep"_"$1.root
#
#
# cd tmp/CMSSW_10_6_26/src
# eval `scram runtime -sh`
# cd ../../../
#
# cmsRun -e -j FrameworkJobReport.xml NANOAODv9_step_cfg.py $3 inputName=miniAODStep_$1.root $5

