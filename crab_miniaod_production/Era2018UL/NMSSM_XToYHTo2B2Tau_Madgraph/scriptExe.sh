#!/bin/bash                                                                                                                                                                                       
set -e
BASE=$PWD
RELEASE_BASE=$CMSSW_BASE

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

## produce the list of gridpacks
eval `scram unsetenv -sh`; 
echo "python copy_gridpacks.py -i "${10}" -o gridpack.list --"$5" --"$6" --"$7" --"$8
python copy_gridpacks.py -i ${10}  -o gridpack.list --$5 --$6 --$7 --$8

echo "Gridpack list to be considered by the job"
cat gridpack.list

echo "setting up CMSSW environment"
cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

nevents="$(echo $2 | cut -d'=' -f2)"
nloops="$(echo $9 | cut -d'=' -f2)"
nEventPerLoop=$((nevents/nloops))
nEventPerLoop=${nEventPerLoop%.*}
echo "Produce nevents="$nevents" in nsteps "$nloops" of n="$nEventPerLoop" events with a different mass"

filelist=""
for ((i=1;i<=$nloops;i++)); 
do    
    echo "cmsRun -e -j FrameworkJobReport.xml gen_step.py jobNum="$1" nEvents="$nEventPerLoop" "$3" outputName=genStep_"$i".root gridpacks=gridpack.list generationStep="$i" jobEvents="$nevents
    cmsRun -e -j FrameworkJobReport.xml gen_step.py jobNum=$1 nEvents=$nEventPerLoop $3 outputName=genStep"_"$i.root gridpacks=gridpack.list generationStep=$i jobEvents=$nevents 
    echo "cmsRun -e -j FrameworkJobReport.xml sim_step.py "$3" inputFiles=genStep_"$i".root outputName=simStep_"$i".root"
    cmsRun -e -j FrameworkJobReport.xml sim_step.py $3 inputName=genStep"_"$i.root outputName=simStep"_"$i.root
    filelist+="file:simStep_"$i".root,"
done
rm genStep*.root
filelist=${filelist::-1}

echo "cmsRun -e -j FrameworkJobReport.xml digi_raw_step.py "$3" inputFiles="$filelist" outputName=digirawStep.root"
cmsRun -e -j FrameworkJobReport.xml digi_raw_step.py $3 inputFiles=$filelist outputName=digirawStep.root
rm simStep*.root

scram p CMSSW CMSSW_10_2_16_UL
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`
cd ../../

echo "cmsRun -e -j FrameworkJobReport.xml hlt_step.py "$3" inputName=digirawStep.root outputName=hltStep.root"
cmsRun -e -j FrameworkJobReport.xml hlt_step.py $3 inputName=digirawStep.root outputName=hltStep.root
rm digirawStep.root

cd $RELEASE_BASE
eval `scram runtime -sh`
cd $BASE

echo "cmsRun -e -j FrameworkJobReport.xml reco_step.py "$3" inputName=hltStep.root outputName=recoStep.root"
cmsRun -e -j FrameworkJobReport.xml reco_step.py $3 inputName=hltStep.root outputName=recoStep.root
rm hltStep.root

echo "cmsRun -e -j FrameworkJobReport.xml miniaod_step.py "$3" inputName=recoStep.root "$4
cmsRun -e -j FrameworkJobReport.xml miniaod_step.py $3 inputName=recoStep.root $4
rm recoStep.root
