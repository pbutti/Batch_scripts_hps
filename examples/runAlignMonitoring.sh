iteration=$1

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
    fi

python scripts/submit_jobs.py --outdir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_AliTest_$iteration/ --listfiles 10031_data_2019_v0skims.txt --step=recon --fileExt slcio --nevents 100 --isData 1 --year=2019 --extraFlags="-R 10031" --steeringFile "/nfs/slac/g/hps2/pbutti/alignment/hps-java/gbl_alignFromLCIO_newGeo.lcsim" --tmpPrefix ~/scratch  -d HPS_AliTest_$iteration 

ls -1 --color=never ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_AliTest_$iteration/submit_scripts/*.sh > listAlign_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList listAlign_$iteration.txt --logDir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_AliTest_$iteration/Logs/ -p 10"

python ./scripts/run_shPool.py --fileList listAlign_$iteration.txt --logDir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_AliTest_$iteration/Logs/ -p 10

cd ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_AliTest_$iteration/outputFiles
hadd AlignMonitoring_10031.root output*/*.root
