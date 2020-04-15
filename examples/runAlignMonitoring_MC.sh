iteration=$1

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

python scripts/submit_jobs.py --outdir ~/TriTrig_AlignmentMonitoring_MPIIdata_AliTest_$iteration/ --listfiles triTrig_2019_nobeam_readout.txt --step=recon --fileExt slcio --nevents -1 --isData 0 --year=2019 --extraFlags="-R 10666" --steeringFile "/nfs/slac/g/hps2/pbutti/alignment/hps-java/gbl_alignReadout_newGeo.lcsim" --tmpPrefix ~/scratch  -d HPS_AliTest_$iteration 

ls -1 --color=never ~/TriTrig_AlignmentMonitoring_MPIIdata_AliTest_$iteration/submit_scripts/*.sh > triTrig_2019_nobeam_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList triTrig_2019_nobeam_$iteration.txt --logDir ~/TriTrig_AlignmentMonitoring_MPIIdata_AliTest_$iteration/Logs/ -p 10"

python ./scripts/run_shPool.py --fileList triTrig_2019_nobeam_$iteration.txt --logDir ~/TriTrig_AlignmentMonitoring_MPIIdata_AliTest_$iteration/Logs/ -p 10


echo "Adding the monitoring histogram..."
cd ~/TriTrig_AlignmentMonitoring_MPIIdata_AliTest_$iteration/outputFiles
hadd AlignMonitoring_10031.root output*/*.root

#Clean the LCIOs
echo "Cleaning slcios...."
rm output*/*.slcio
