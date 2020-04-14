12 Feb 2020


# Instructions

This package provides some configurable scripts to run some tools on the SLAC batch system such as:
- Various steps of hps-java reconstruction 
- SLIC
- Hpstr 

## How to run 

source ./setup.sh

### Running the reco on evio files

This is an example on how to send reconstruction on the batch for 2019 

```
python scripts/submit_jobs.py --outdir <outDir> --indir <inDir> --step=recon --year 2019 --fileExt evio --submit
```

The ```--submit``` actually sends the jobs to the batch. If the flag is omitted the scripts are generated but not shipped 
to the batch system and they can be used for local testing. One can also use ```--local``` to execute the jobs directly on 
the interactive node one after the other. 
Without specifying the number events with ```--nevents``` the jobs will process only 100 events. Set ```--nevents=-1``` to process all the events in an input file. 


### Running hpstr: ntuples and histograms

Running ntuplization:

```
python scripts/submit_jobs.py --outdir /nfs/slac/g/hps3/users/pbutti/physrun2019/Run_10031/hpstr_Ntuples/ --indir /nfs/slac/g/hps3/users/pbutti/physrun2019/Run_10031/outputFiles/ --step=hipster --fileExt slcio --nevents -1 --queue medium --isData 1 --hpstrCfg recoTuple_cfg.py --submit
```


Running the histograms:


```
python scripts/submit_jobs.py --outdir /nfs/slac/g/hps3/users/pbutti/physrun2019/Run_10031/hpstr_histos/ --indir /nfs/slac/g/hps3/users/pbutti/physrun2019/Run_10031/hpstr_Ntuples/outputFiles/ --step=hipster --fileExt root --nevents -1 --queue medium --isData 1 --submit 
```

In the case one wants to use different hpstr configuration, it is possible to specify them by ```--hpstrCfg <cfg>```
It's also possible to specify a list of input files instead of grepping the folder, just use ```--listfiles <list>```. The option can be combined with ```--indir``` to add files from a folder and from a list.
