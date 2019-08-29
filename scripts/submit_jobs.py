from configure import *
import scriptGenerator
import GeometryMapper
import os
import glob
import subprocess

config = OptParsing()

indir   = config.indir
outdir  = config.outdir
step    = config.step
nevents = config.nevents

if not os.path.exists(outdir):
    os.makedirs(outdir)
    print "Created outdir", outdir

if (config.verbose):
    print "Indir", indir
    print "Outdir:", outdir
# MRSolt stdhep location:
#  /nfs/slac/g/hps_data2/mc_production/tritrig/4pt55/stdhep/00/tritrig_0000.stdhep

#InputFile extension
fileExt = ""
if ("stdhep" in step):
    fileExt = "stdhep"

# Grep initial files
if (config.verbose):
    print "Grepping for:", "ls " + indir+"/*" + fileExt
inFileList = glob.glob(indir+"*." + fileExt)

if (config.verbose):
    print inFileList

#Create the script directory, the log directory and the output file directory in the outdir
logdir = outdir+"/logs/"
outputfdir = outdir+"/outputFiles/"
scriptdir  = outdir+"/submit_scripts/"
if not os.path.exists(logdir):
    os.makedirs(logdir)
if not os.path.exists(outputfdir):
    os.makedirs(outputfdir)
if not os.path.exists(scriptdir):
    os.makedirs(scriptdir)


geoM = GeometryMapper.GeometryMapper()

# Generate running script

count=0
sG = scriptGenerator.scriptGenerator(step,scriptdir,outputfdir)

for ifile in inFileList:
    filePrefix = ifile.split("/")[-1].split(".stdhep")[0]
    sG.generateScript(filePrefix)
    sG.setupStdhepToSimul(ifile,filePrefix+"_simul",geoM.getGeoFile("nominal"),nevents)
    sG.closeScript()
    print "bsub -q " + config.queue + "-o " + logdir + " -e " + logdir + " "+sG.scriptFileName
    if config.submit:
        subprocess.call(["bsub","-q",config.queue,"-o",logdir,"-e",logdir,sG.scriptFileName])
