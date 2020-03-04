import sys,os

def OptParsing():
    
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option("--outdir",dest="outdir",help="outdir",default="")
    parser.add_option("--indir",dest="indir",help="indir",default="")
    parser.add_option("--listfiles",dest="listfiles",help="listfiles",default="")
    parser.add_option("--step",dest="step",help="stdhep,spacing,readout,recon,align,hipster",default="stdhep")
    parser.add_option("--nevents",dest="nevents",help="nevents",type="int",default=100)
    parser.add_option("--verbose",dest="verbose",help="verbose",default=False,action="store_true")
    parser.add_option("--submit",dest="submit",help="submit",default=False,action="store_true")
    parser.add_option("--local",dest="local",help="local",default=False,action="store_true")
    parser.add_option("--queue",dest="queue",help="queue: short, medium, long, xlong, xxl",default="medium")
    parser.add_option("--year",dest="year",help="Which year for steering job Option",default="2019")
    parser.add_option("--fileExt",dest="fileExt",help="Input File file extension:evio,slcio,stdhep,root",default="evio")
    parser.add_option("--hpstrCfg",dest="hpstrCfg",help="Hpstr Configuration to be used",default="anaVtxTuple_cfg.py")
    parser.add_option("--isData",dest="isData",help="Input file is a data File",default="0")
    parser.add_option("--extraFlags", dest="extraFlags",help="Extra flags for reconstruction", default = "")
    parser.add_option("-W","--wall",dest="wall",help="time wall in the format [hrs:]minutes, i.e. -W 60 for 1 h", default = "60")
    (config,sys.argv[1:]) = parser.parse_args(sys.argv[1:])
    return config
