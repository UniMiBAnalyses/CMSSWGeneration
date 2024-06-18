#!/bin/bash
export EOS_MGM_URL=root://eosuser.cern.ch
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on lhe step

export LC_ALL=C; unset LANGUAGE

let seed=$1+1

eos cp /eos/user/g/gboldrin/gridpacks/WV/EFT/"$2"_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz .

mkdir temp_dir; tar -axvf "$2"_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz --directory temp_dir; cd temp_dir
# number of events requested, seed, number of cpus
./runcmsgrid.sh 250 $seed 2

mv cmsgrid_final.lhe ..; cd ..

ls
echo "Done"


#cleaning 
rm -rf temp_dir "$2"_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz

# now convert the LHE in a EDM tuple via pLHE step
# this needs to run on sl6 therefore we create a script that runs the following

# echo "Opening CMSSW_7_1_32"
# tar -xzvf CMSSW_7_1_32.tgz
# rm CMSSW_7_1_32.tgz
# cd CMSSW_7_1_32/src/
# scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
# eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
# echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
# cd ../../
# date
# cmsRun SMP-RunIIWinter15pLHE-00016_1_cfg.py

# but inside a singularity environment

singularity exec --contain --ipc --pid --home $PWD --bind /cvmfs  /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest ./LheToEDM.sh
rm cmsgrid_final.lhe

# now run pythia still in the container

# echo "Opening CMSSW_7_1_39"
# tar -xzvf CMSSW_7_1_39.tgz
# rm CMSSW_7_1_39.tgz
# cd CMSSW_7_1_39/src/
# scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
# eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
# echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
# cd ../../
# date
# cmsRun SMP-RunIISummer15GS-00266_1_cfg.py

singularity exec --contain --ipc --pid --home $PWD --bind /cvmfs  /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest ./Pythia.sh
rm SMP-RunIIWinter15pLHE-00016.root

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
rm  SMP-RunIISummer15GS-00266.root

# step 2
cmsRun SMP-RunIISummer16DR80Premix-00645_2_cfg.py
rm SMP-RunIISummer16DR80Premix-00645_0.root

# singularity exec --contain --ipc --pid --home $PWD --bind /cvmfs  /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el6:latest ./Premix.sh


# now run MINIAOD step
echo "Opening CMSSW_9_4_9"
tar -xzvf CMSSW_9_4_9.tgz
rm CMSSW_9_4_9.tgz
cd CMSSW_9_4_9/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

cmsRun SMP-RunIISummer16MiniAODv3-00478_1_cfg.py
rm SMP-RunIISummer16DR80Premix-00645.root

# now run NANOAOD step
echo "Opening CMSSW_10_2_24_patch1_ZV_EFT"
tar -xzvf CMSSW_10_2_24_patch1_ZV_EFT.tgz
rm CMSSW_10_2_24_patch1_ZV_EFT.tgz
cd CMSSW_10_2_24_patch1_ZV_EFT/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

cmsRun SMP-RunIISummer16NanoAODv7-00422_1_cfg.py  
rm SMP-RunIISummer16MiniAODv3-00478.root

#########

eos cp SMP-RunIISummer16NanoAODv7-00422.root /eos/user/g/gboldrin/nAOD_WV/"$2"/2016/"$2"_"$1".root

# rm SMP-RunIIWinter15pLHE-00016.root SMP-RunIISummer15GS-00266.root SMP-RunIISummer16DR80Premix-00645.root SMP-RunIISummer16DR80Premix-00645_0.root SMP-RunIISummer16MiniAODv3-00478.root

rm SMP-RunIISummer16NanoAODv7-00422.root
rm -rf CMSSW_10_2_24_patch1_ZV_EFT *py
date

echo "Done"
