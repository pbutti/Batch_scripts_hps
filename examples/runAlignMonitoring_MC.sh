iteration=$1
tag=$2

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: runAlignMonitoring_MC.py <iter> <tag>"
    exit 1
fi

python scripts/submit_jobs.py --outdir ~/TriTrig_AlignmentMonitoring_MPIIdata_${tag}_$iteration/ --listfiles triTrig_2019_nobeam_readout.txt --step=recon --fileExt slcio --nevents -1 --isData 0 --year=2019 --extraFlags="-R 10666" --steeringFile "/nfs/slac/g/hps2/pbutti/alignment/hps-java/gbl_alignReadout_newGeo.lcsim" --tmpPrefix ~/scratch  -d HPS_${tag}_$iteration 

ls -1 --color=never ~/TriTrig_AlignmentMonitoring_MPIIdata_${tag}_$iteration/submit_scripts/*.sh > triTrig_2019_nobeam_${tag}_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList triTrig_2019_nobeam_${tag}_$iteration.txt --logDir ~/TriTrig_AlignmentMonitoring_MPIIdata_${tag}_$iteration/Logs/ -p 10"

python ./scripts/run_shPool.py --fileList triTrig_2019_nobeam_${tag}_$iteration.txt --logDir ~/TriTrig_AlignmentMonitoring_MPIIdata_${tag}_$iteration/Logs/ -p 10


echo "Adding the monitoring histogram..."
cd ~/TriTrig_AlignmentMonitoring_MPIIdata_${tag}_$iteration/outputFiles
hadd AlignMonitoring_10031.root output*/*.root

#Clean the LCIOs
echo "Cleaning slcios...."
rm output*/*.slcio

#Clean the root files
echo "Cleaning the root files...."
rm output*/*.root
