#! /bin/bash
sed -i "12s/.*/Queue 3000 proc in ($1)/g" submit.jdl
mkdir -p output/$1
mkdir -p log/$1
chmod +x submit.jdl
chmod +x wrapper.sh
condor_submit submit.jdl 
