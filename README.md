9 Feb 2020

# Instructions

This package provides some configurable scripts to run some tools on the SLAC batch system such as:
- Various steps of hps-java reconstruction 
- SLIC
- Hpstr 

## How to run 

This is an example on how to send reconstruction on the batch for 2019 

```
python scripts/submit_jobs.py --outdir <outDir> --indir <inDir> --step=recon --year 2019 --fileExt evio --submit
```

The ```--submit``` actually sends the jobs to the batch. If the flag is omitted the scripts are generated but not shipped 
to the batch system and they can be used for local testing. One can also use ```--local``` to execute the jobs directly on 
the interactive node one after the other. 
Without specifying the number events with ```--nevents``` the jobs will process only 100 events. Set ```--nevents=-1``` to process all the events in an input file. 


