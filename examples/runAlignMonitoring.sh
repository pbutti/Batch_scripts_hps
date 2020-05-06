iteration=$1
tag=$2
datainfo=$3
listfiles=$4
runNumber=$5
basepath=$6

if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters"
    echo "runAlignmMonitoring.sh <iteration> <tag> <dataInfo> <listfiles> <runNumber> <basepath ~/ | /nfs/slac/g/hps2/pbutti/>"
    exit 1
fi



python scripts/submit_jobs.py --outdir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/ --listfiles ${listfiles} --step=recon --fileExt slcio --nevents -1 --isData 1 --year=2019 --extraFlags="-R $runNumber" --steeringFile "/nfs/slac/g/hps2/pbutti/alignment/hps-java/gbl_alignFromLCIO_newGeo.lcsim" --tmpPrefix ~/scratch  -d HPS_${tag}_$iteration 

ls -1 --color=never ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/submit_scripts/*.sh > list${tag}_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/Logs/ -p 10"

python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/Logs/ -p 10

cd ${basepath}/${runNumber}_AlignmentMonitoring_${datainfo}_MPIIdata_${tag}_$iteration/outputFiles
hadd AlignMonitoring_${runNumber}_${tag}_${iteration}.root output*/*.root

