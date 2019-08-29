import sys,os

def OptParsing():
    
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option("--outdir",dest="outdir",help="outdir",default="")
    parser.add_option("--indir",dest="indir",help="indir",default="")
    parser.add_option("--step",dest="step",help="stdhep,simul,spacing,readout,recon",default="stdhep")
    parser.add_option("--nevents",dest="nevents",help="nevents",type="int",default=100)
    parser.add_option("--verbose",dest="verbose",help="verbose",default=False,action="store_true")
    parser.add_option("--submit",dest="submit",help="submit",default=False,action="store_true")
    parser.add_option("--queue",dest="queue",help="queue: short, medium, long, xlong, xxl",default="1nh")
    (config,sys.argv[1:]) = parser.parse_args(sys.argv[1:])
    return config
