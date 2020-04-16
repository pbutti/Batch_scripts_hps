iteration=$1
tag=$2

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    exit 1
    fi

python scripts/submit_jobs.py --outdir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_${tag}_$iteration/ --listfiles 10031_data_2019_v0skims.txt --step=recon --fileExt slcio --nevents -1 --isData 1 --year=2019 --extraFlags="-R 10031" --steeringFile "/nfs/slac/g/hps2/pbutti/alignment/hps-java/gbl_alignFromLCIO_newGeo.lcsim" --tmpPrefix ~/scratch  -d HPS_${tag}_$iteration 

ls -1 --color=never ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_${tag}_$iteration/submit_scripts/*.sh > list${tag}_$iteration.txt
echo "python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_${tag}_$iteration/Logs/ -p 10"

python ./scripts/run_shPool.py --fileList list${tag}_$iteration.txt --logDir ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_${tag}_$iteration/Logs/ -p 10

cd ~/10031_AlignmentMonitoring_v0Skims_MPIIdata_${tag}_$iteration/outputFiles
hadd AlignMonitoring_10031.root output*/*.root
