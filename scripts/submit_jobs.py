from configure import *
import scriptGenerator
import GeometryMapper
import os
import glob
import subprocess
#import json

config = OptParsing()

indir    = config.indir
outdir   = config.outdir
step     = config.step
nevents  = config.nevents
local    = config.local
submit   = config.submit
year     = config.year
wall     = config.wall
fileExt  = config.fileExt
hpstrCfg = config.hpstrCfg
isData   = config.isData
listfiles = config.listfiles
extraFlags = config.extraFlags
hpstrFolder = config.hpstrFolder
steeringFile = config.steeringFile
tmpPrefix  = config.tmpPrefix
theDetector = config.detector
nfsPath     = config.nfsPath

#jsonFile  = config.json

if (step=="recon" and steeringFile ==""):
    print "ERROR: missing steering file"
    exit(1)

if (local and submit):
    print "WARNING: setup both local and batch submission"
    print "Will set local submission to false."
    local = False
    
if not os.path.exists(outdir):
    os.makedirs(outdir)
    print "Created outdir", outdir

if (config.verbose):
    print "Indir", indir
    print "Outdir:", outdir
# MRSolt stdhep location:
#  /nfs/slac/g/hps_data2/mc_production/tritrig/4pt55/stdhep/00/tritrig_0000.stdhep

# Grep initial files
if (config.verbose):
    print "Grepping for:", "ls " + indir+"/*" + fileExt +"*"

inFileList = []

if (indir!="") : 

    inFileList = glob.glob(indir+"/*" + fileExt+"*")
    if (config.verbose):
        print inFileList
        if len(inFileList)==0:
            print "Try grepping for ls "+indir+"/*/*" + fileExt+"*"
            inFileList = glob.glob(indir+"/*/*" + fileExt+"*")
        print "Total number of file found=", len(inFileList)
    if (config.verbose):
        print inFileList

if (listfiles!=""):
    infile=open(listfiles)
    for line in infile.readlines():
        inFileList.append(line.strip())
    infile.close()

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
sG = scriptGenerator.scriptGenerator(step,scriptdir,outputfdir,nfsPath)

ifile_ID = 0
for ifile in inFileList:
    ifile_ID+=1
    filePrefix = ifile.split("/")[-1].split(fileExt)[0]
    filePrefix += "_"+str(ifile_ID)
    
    sG.setTmpPrefix(tmpPrefix)
    sG.generateScript(filePrefix)
    if ("stdhep" in step):
        sG.setupStdhepToSimul(ifile,filePrefix+"_simul",geoM.getGeoFile("nominal"),nevents)
    elif ("spacing" in step):
        sG.setupBunchSpacing(ifile,filePrefix+"_spacing")
    elif ("readout" in step):
        sG.setupReadout(ifile,filePrefix+"_readout",geoM.getGeoTag("nominal"))
    elif ("recon" in step):
        #sG.setSteeringFile("steering-files/src/main/resources/org/hps/steering/production/Run2019ReconPlusDataQuality.lcsim")
        if (year=="2016"):
            sG.detector="HPS-PhysicsRun2016-Pass2"
            sG.setHPSJavaDir(nfsPath+"/slac/g/hps2/pbutti/kalman/hps-java/")
            sG.setSteeringFile(steeringFile)
            #sG.setSteeringFile("/nfs/slac/g/hps2/pbutti/kalman/hps-java/PhysicsRun2016FullReconMC.lcsim")
            
        if (year=="2019"):
            #sG.setSteeringFile("steering-files/src/main/resources/org/hps/steering/production/Run2019Recon.lcsim")
            sG.setHPSJavaDir(nfsPath+"/slac/g/hps2/pbutti/alignment/hps-java/")
            #sG.detector="HPS-PhysicsRun2019-v2-4pt5"
            sG.detector=theDetector
            sG.setSteeringFile(steeringFile)
        sG.setupRecon(ifile,filePrefix+"_recon",nevents,fileExt,year,extraFlags)
    elif ("align" in step):
        sG.setHPSJavaDir(nfsPath+"/slac/g/hps2/pbutti/alignment/hps-java/")
        sG.setSteeringFile(nfsPath+"/slac/g/hps2/pbutti/alignment/hps-java/PhysicsRun2016_fromLCIO.lcsim")
        sG.setupRecon(ifile,filePrefix+"_align",nevents)
        #Move the millepede.bin
    elif ("hipster" in step):
        sG.setHpstrFolder(hpstrFolder)
        sG.runHipster(ifile,filePrefix+".root",hpstrCfg,isData,extraFlags)
    sG.closeScript()
    #rhel60 is deprecated
    #print "bsub -W "+wall+" -R rhel60 -q " + config.queue + " -o " + logdir + " -e " + logdir + " "+sG.scriptFileName
    
    print "bsub -W "+wall+" -R centos7 -q " + config.queue + " -o " + logdir + " -e " + logdir + " "+sG.scriptFileName
    if submit:
        subprocess.call(["bsub","-W",wall,"-R","centos7","-q",config.queue,"-o",logdir,"-e",logdir,sG.scriptFileName])
    if local:
        subprocess.call([sG.scriptFileName])
