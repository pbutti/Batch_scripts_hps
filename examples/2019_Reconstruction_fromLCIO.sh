#java -XX:+UseSerialGC -Xmx3000m -jar distribution/target/hps-distribution-4.5-SNAPSHOT-bin.jar steeringFor2019_LCIO.lcsim -i /nfs/slac/g/hps3/users/pbutti/2019_data_10031/outputFiles/outputs_hps_010031._123_140916/hps_010031._123_recon.slcio -DoutputFile=debug_residuals_lcio -d HPS-PhysicsRun2019-v2-4pt5 -R 10031 -n 1000


# MC #
python scripts/submit_jobs.py --outdir /nfs/slac/g/hps3/users/pbutti/2019_tridents_from_LCIO_Residuals/ --indir /nfs/slac/g/hps_data2/mc/2016/forOmar/tritrig_beam/singles/4pt55/ --step=recon --fileExt slcio --nevents -1 --queue short --isData 0 --year=2019 --extraFlags="-R 10666" --steeringFile /nfs/slac/g/hps2/pbutti/alignment/hps-java/PhysicsRun2019MCRecon_LCIO.lcsim


# DATA #
python scripts/submit_jobs.py --outdir /nfs/slac/g/hps3/users/pbutti/2019_data_from_LCIO_Full/ --listfiles 10031_data_2019.txt --step=recon --fileExt slcio --nevents -1 --queue long --isData 1 --year=2019 --extraFlags="-R 10031" --steeringFile /nfs/slac/g/hps2/pbutti/alignment/hps-java/steeringFor2019_LCIO.lcsim
