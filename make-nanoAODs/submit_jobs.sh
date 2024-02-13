#!/bin/bash

# Define path for job directories
#BASE_PATH=/afs/cern.ch/work/e/ecarrera/lw/ntuplizer/CMSSW_5_3_32/src/AcausalPOETAnalyzer/PhysObjectExtractor/joblaunch
BASE_PATH=/afs/cern.ch/user/p/pllerena/workspace/4tops/produce-nanoAODs/joblaunch
#BASE_PATH=/path/to/job/directory
mkdir -p $BASE_PATH

# Set processes
PROCESSES=( \
#      Run2015D_SingleMuon
#      TTTT
#       _TT_
	WJets
#       DYJets
	   
   )

# Create JDL files and job directories
for PROCESS in ${PROCESSES[@]}
do
    python3 create_job.py $PROCESS $BASE_PATH
done

# Submit jobs
THIS_PWD=$PWD
for PROCESS in ${PROCESSES[@]}
do
    cd $BASE_PATH/$PROCESS
    condor_submit job.jdl
    cd $THIS_PWD
done
