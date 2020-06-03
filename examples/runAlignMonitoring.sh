#!/bin/bash

iteration=$1
tag=$2
datainfo=$3
listfiles=$4
runNumber=$5
location=$6
MC=$7

if [ "$#" -ne 7 ]; then
    echo "Illegal number of parameters"
    echo "runAlignmMonitoring.sh <iteration> <tag> <dataInfo> <listfiles> <runNumber> <location home | hps2 | hps3 > <MC "" | _MC>"
    exit 1
fi

HOST=`hostname`
echo $HOST
tmpPref=""
fixPerms=false
threads="-p 5"

if [[ "$HOST" == *"cbravo-hps"* ]]; then
    echo "Running on Maria"
    tmpPref="--tmpPrefix ~/scratch"
    nfsPath=${HOME}"/nfs/"
    threads="-p 10"
elif [[ "$HOST" == *"cent"* ]]; then
    echo "Running on Centos"
    tmpPref=""
    nfsPath="/nfs/"
    threads="-p 10"
elif [[ "$HOST" = *"rdsrv30"* ]]; then
    echo "DAQ Machine"
    tmpPref="--tmpPrefix /tmp/scratch"
    nfsPath=${HOME}"/nfs/"
    threads="-p 20"
else
    echo "Machine not known"
    exit 1
fi


basepath=""

if [[ "$location" == "home" ]]; then
    echo "Outputs in local home"
    basepath=$HOME
elif [[ "$location" == "hps2" ]]; then
    basepath=$nfsPath"/slac/g/"$location"/"$USER
    echo "To "{$basepath}
elif [[ "$location" == "hps3" ]]; then
    basepath=$nfsPath"/slac/g/"$location"/users/"$USER
    echo "To "${basepath}
else
    echo "End point location not known"
    exit 1
fi

    

outputDirectory=${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/

python scripts/submit_jobs.py --nfsPath ${nfsPath} --outdir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/ --listfiles ${listfiles} --step=recon --fileExt slcio --nevents -1  --isData 1 --year=2019 --extraFlags="-R $runNumber" --steeringFile ${nfsPath}"slac/g/hps2/pbutti/alignment/hps-java/gbl_alignFromLCIO_newGeo$MC.lcsim" ${tmpPref}  -d HPS_${tag}_$iteration 

[ ! -e list${tag}_$iteration.txt ] || rm list${tag}_$iteration.txt

ls -1 --color=never ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/submit_scripts/*.sh > list${tag}_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/Logs/ ${threads}"

python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/Logs/ ${threads}

cd ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/outputFiles
hadd AlignMonitoring_${runNumber}_${tag}_${iteration}.root output*/*.root

#if [ ${fixPerms} = true ]; then
#    chmod g+w ${outputDirectory}
