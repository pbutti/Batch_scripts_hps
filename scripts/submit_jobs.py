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
    fileExt = ".stdhep"
elif ("spacing" in step):
    fileExt = ".slcio"
elif ("readout" in step):
    fileExt = ".slcio"
elif ("recon" in step):
    fileExt = ".slcio"
else :
    print "ERROR: step not found! Select between stdhep,spacing,readout,recon"
    sys.exit(1)

# Grep initial files
if (config.verbose):
    print "Grepping for:", "ls " + indir+"/*" + fileExt
inFileList = glob.glob(indir+"/*" + fileExt)
if (config.verbose):
    print inFileList
if len(inFileList)==0:
    print "Try grepping for ls "+indir+"/*/*" + fileExt
    inFileList = glob.glob(indir+"/*/*" + fileExt)
    print "Total number of file found=", len(inFileList)
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
    filePrefix = ifile.split("/")[-1].split(fileExt)[0]
    sG.generateScript(filePrefix)
    if ("stdhep" in step):
        sG.setupStdhepToSimul(ifile,filePrefix+"_simul",geoM.getGeoFile("nominal"),nevents)
    elif ("spacing" in step):
        sG.setupBunchSpacing(ifile,filePrefix+"_spacing")
    elif ("readout" in step):
        sG.setupReadout(ifile,filePrefix+"_readout",geoM.getGeoTag("nominal"))
    elif ("recon" in step):
        sG.setSteeringFile("steering-files/src/main/resources/org/hps/steering/production/Run2019ReconPlusDataQuality.lcsim")
        sG.setupRecon(ifile,filePrefix+"_recon",-1)
    
    sG.closeScript()
    print "bsub -q " + config.queue + " -o " + logdir + " -e " + logdir + " "+sG.scriptFileName
    if config.submit:
        subprocess.call(["bsub","-q",config.queue,"-o",logdir,"-e",logdir,sG.scriptFileName])
