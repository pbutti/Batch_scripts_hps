source /home/pbutti/src/Batch_scripts_hps/setup.sh

#DATA PROCESSING
#bash examples/runAlignMonitoring.sh iter0 V0Align v0Skims 10031_data_2019_v0skims.txt 10031 hps2 ""
#bash examples/runAlignMonitoring.sh iter3 V0Align v0Skims 10031_data_2019_v0skims.txt 10031 hps2 ""
#bash examples/runAlignMonitoring.sh iter3 V0Align v0SkimsLoose 10031_data_2019_v0skims_loose.txt 10031 hps2 ""
#bash examples/runAlignMonitoring.sh iter0 V0Align v0SkimsLooseMaria 10031_data_2019_v0skims_loose.txt 10031 hps2 ""
#bash examples/runAlignMonitoring.sh  iter0 V0Align_OPAngleBOT_m0_8mrad v0SkimsLoose 10031_data_2019_v0skims_loose.txt 10031 hps2 ""

#bash examples/runAlignMonitoring.sh  iter0  V0Align_OPAngleBOT_m1_5mrad  v0Skims 10031_data_2019_v0skims.txt 10031 hps2 ""
#bash examples/runAlignMonitoring.sh  iter2  V0Align_OPAngleBOT_m1_5mrad  v0Skims 10031_data_2019_v0skims.txt 10031 hps2 ""

#FEE DATA PROCESSING

## TEST
#bash examples/runAlignMonitoring.sh  iter0  V0Align  FEESkims listfeetest.txt 10103 home _FEE

## NOMINAL
#bash examples/runAlignMonitoring.sh  iter0  V0Align_OPAngleBOT_m1_5mrad  FEESkims 10103_data_2019_FEEskims.txt 10103 hps2 _FEE
#bash examples/runAlignMonitoring.sh  iter2  V0Align_OPAngleBOT_m1_5mrad  FEESkims 10103_data_2019_FEEskims.txt 10103 hps2 _FEE
#bash examples/runAlignMonitoring.sh  iter0  V0Align FEESkims 10103_data_2019_FEEskims.txt 10103 hps2 _FEE


## TO RUN ##
#bash examples/runAlignMonitoring.sh  iter0  V0Align FEESkims 10104_data_2019_FEEskims.txt 10104 hps2 _FEE
#bash examples/runAlignMonitoring.sh  iter0  V0Align_OPAngleBOT_m1_5mrad  FEESkims 10104_data_2019_FEEskims.txt 10104 hps2 _FEE
#bash examples/runAlignMonitoring.sh  iter2  V0Align_OPAngleBOT_m1_5mrad  FEESkims 10104_data_2019_FEEskims.txt 10104 hps2 _FEE
bash examples/runAlignMonitoring.sh  iter0   V0Align FEESkims 10104_data_2019_FEEskims.txt 10104 hps2 _FEE




#MC PROCESSING 
#bash examples/runAlignMonitoring.sh iter0 V0Align TriTrigNoBeam triTrig_2019_nobeam_readout.txt 10666 hps2 _MC
#bash examples/runAlignMonitoring.sh iter0 V0Align_OPAngleBOT_m1_5mrad TriTrigNoBeam triTrig_2019_nobeam_readout.txt 10666 hps2 _MC
#bash examples/runAlignMonitoring.sh iter0 AliTest_MC_GlobMov TriTrigNoBeam triTrig_2019_nobeam_readout.txt 10666 hps2 _MC
#bash examples/runAlignMonitoring.sh iter0 AliTest TriTrigNoBeam triTrig_2019_nobeam_readout.txt 10666 hps2 _MC
#bash examples/runAlignMonitoring.sh iter1 AliTest TriTrigNoBeam triTrig_2019_nobeam_readout.txt 10666 hps2 _MC




#bash examples/runAlignMonitoring.sh  iter0 V0Align_OPAngleBOT_m0_8mrad v0SkimsLoose 10031_data_2019_v0skims_loose.txt 10031 hps2 ""
