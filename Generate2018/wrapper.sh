#!/bin/bash
# refer link: https://uscms.org/uscms_at_work/computing/setup/batch_systems.shtml#cmssw_Tar
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node

# get files
gridpack_name="$1_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
excute_file1="SMP-RunIIFall18wmLHEGS-00062_SM_1_cfg.py"
excute_file2="SMP-RunIIAutumn18DRPremix-00050_1_cfg.py"
excute_file3="SMP-RunIIAutumn18DRPremix-00050_2_cfg.py"
excute_file4="SMP-RunIIAutumn18MiniAOD-00050_1_cfg.py"
excute_file5="SMP-RunIIAutumn18NanoAODv7-00058_1_cfg.py"

sandbox_name1="CMSSW_10_2_6.tgz"
cmssw_version1="CMSSW_10_2_6"
sandbox_name2="CMSSW_10_6_20.tgz"
cmssw_version2="CMSSW_10_6_20"

# set environment
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "Opening CMSSW_10_2_6"
ls
# cd /home/abulla/CMSSWGeneration/Generate2018/input
pwd
tar -xzvf $sandbox_name1
rm $sandbox_name1
cd $cmssw_version1/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
echo $1
#sed -i "s/^.*tarball.tar.xz.*$/     args = cms.vstring(\'..\/$gridpack_name\'),/" -i $excute_file1
sed -i 's#^.*tarball.tar.xz.*$#    args = cms.vstring(\"..\/'${gridpack_name}'\"),#' -i $excute_file1 
# change the request events
echo "OOOOOOOOOOOOOOOO nevent = "$2
sed -i "s/int32(2500)/int32($2)/g" -i $excute_file1
date
cmsRun $excute_file1
date
cmsRun $excute_file2
rm $gridpack_name SMP-RunIIFall18wmLHEGS-00062.root SMP-RunIIFall18wmLHEGS-00062_inLHE.root
date
cmsRun $excute_file3
rm SMP-RunIIAutumn18DRPremix-00050_0.root
date
cmsRun $excute_file4
rm SMP-RunIIAutumn18DRPremix-00050.root
date

ls
rm -rf $cmssw_version1
tar -xzvf $sandbox_name2
rm $sandbox_name2
cd $cmssw_version2/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../

date
cmsRun $excute_file5
rm SMP-RunIIAutumn18MiniAOD-00050.root
rm -rf $cmssw_version2 *py
date
