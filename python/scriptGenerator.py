import subprocess

class scriptGenerator:

    # Members
    
    scriptFile = ""
    scriptFileName = ""
    scriptdir      = ""
    outputdir      = ""
    step           = "stdhep"
    #Readout steering file: /nfs/slac/g/hps2/pbutti/MC_basic_generation/readoutFiles/Test_readout.lcsim
    #Recon   steering file: steering-files/src/main/resources/org/hps/steering/production/Run2019ReconPlusDataQuality.lcsim

    nfsPath   = "/nfs/"
    
    
    steeringFile   = nfsPath+"/slac/g/hps2/pbutti/MC_basic_generation/readoutFiles/Test_readout.lcsim"
    jarFile        = "distribution/target/hps-distribution-5.1-SNAPSHOT-bin.jar"
    hpsJavaDir     = nfsPath+"/slac/g/hps2/pbutti/hps-java/"
    detector       = "HPS-PhysicsRun2019-v1-4pt5"

    #Hipster 
    hpstrFolder    = nfsPath+"/slac/g/hps2/pbutti/hipster/"

    #tmpPrefix = where to create the temp folder
    tmpPrefix = "/scratch/"

    
    
    #Methods

    def __init__(self, step, scriptdir,outputdir,nfsPath):
        self.step           = step
        self.scriptdir      = scriptdir
        self.outputdir      = outputdir
        self.nfsPath        = nfsPath

    def setupStep(self):
        pass

    def generateScript(self,fileID):
        self.scriptFileName = self.scriptdir+"/script_submit_job_"+fileID+".sh"
        self.scriptFile = open(self.scriptFileName,"w")
        self.wline("#!/bin/bash")
        self.wline('JOBFILEDIR=`mktemp -d '+ self.tmpPrefix+ '${LSB_JOBID}_JobWork.XXXXXX`')
        self.wline('echo "Job file directory: $JOBFILEDIR"')
        self.wline('export HOME=$JOBFILEDIR')
        self.wline('cd $HOME')
        self.wline('export OUTPUTDIR=$JOBFILEDIR/outputs_'+fileID+'_${LSB_JOBID}/; mkdir $OUTPUTDIR')
        self.wline('echo "Created $OUTPUTDIR"')
        # Not needed I think!
        #self.wline('source /nfs/slac/g/hps3/software/setup.sh')
        self.wline('hostname')
        
    def closeScript(self):
        self.wline('echo "Moving files to outputdir"')
        #This has issues with maintaning permissions
        #self.wline('mv $OUTPUTDIR ' + self.outputdir)
        self.wline('cp -r $OUTPUTDIR ' + self.outputdir)
        self.wline('rm -r $OUTPUTDIR ')
        self.wline('echo "Removing $JOBFILEDIR"')
        self.wline('rm -R $JOBFILEDIR')
        self.scriptFile.close()
        subprocess.call(["chmod","u+x",self.scriptFileName])


    def wline(self,line):
        self.scriptFile.write(line+"\n")
        
    def setupStdhepToSimul(self,stdhepFile,outFileName,detector,nEvents):
        #TODO-FIX THIS
        self.wline('cd ' + self.hpsJavaDir)
        # Setup SLCIO
        self.wline('source ' +self.nfsPath+ '/slac/g/hps/hps_soft/slic/build/slic-env.sh')
        #self.wline('source /nfs/slac/g/hps2/pbutti/scripts/setups/slic-env.sh')
        #self.wline('export LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH')
        self.wline('env')
        self.wline('SLIC=`which slic`')
        self.wline('ldd $SLIC')
        #self.wline('locate libicui18n.so.42')
        self.wline('lsb_release -a')
        self.runSlic(stdhepFile,outFileName,detector,nEvents)

    def setupBunchSpacing(self,slcioFile,outFileName,spacing=250,Ecut=0.05,wOption=2000000):
                
        #TODO-FIX THIS
        self.wline('cd ' + self.hpsJavaDir)
        self.wline('java -DdisableSvtAlignmentConstants -XX:+UseSerialGC -Xmx1000m -cp '+ self.jarFile +' org.hps.util.FilterMCBunches -e'+str(spacing)+' '+slcioFile+' $OUTPUTDIR/'+ outFileName+'.slcio -d -E'+str(Ecut)+' -w'+str(wOption))
        

    def setupReadout(self,slcioFile,outFileName,detector,runNumber=9600):
        #TOD-FIX THIS
        self.wline('cd ' + self.hpsJavaDir)
        self.wline('java -jar '+self.jarFile+" "+self.steeringFile + " -i " + slcioFile + " -DoutputFile=$OUTPUTDIR/"+outFileName+" -R "+str(runNumber) +" -d "+detector)
        

    def setupReconLCIOList(self,inputFiles,outFileName,nevents=-1,fileExt="slcio",year="2019",extraFlags=""):

        jnaLib = '-Djna.library.path="/u/ea/pbutti/nfs/slac/g/hps2/pbutti/alignment/GeneralBrokenLines/cpp/lib/" '
        
        cmd = 'java -XX:+UseSerialGC -Xmx3000m '+jnaLib+' -jar ' + self.hpsJavaDir+"/"+self.jarFile + ' ' + self.steeringFile +"\\\n"
        for ifile in inputFiles:
            cmd+= ' -i ' + ifile +' \\\n'
            pass
        cmd += ' -DoutputFile=$OUTPUTDIR/' + outFileName
        cmd += ' -d ' + self.detector
        cmd += " " + extraFlags 

        if (nevents>0):
            cmd+=' -n ' + str(nevents)
        self.wline(cmd)
 
    def setupRecon(self,inputFilename,outFileName,nevents=-1,fileExt="slcio",year="2019",extraFlags=""):
        #self.wline('cd ' + self.hpsJavaDir)
        
        jnaLib = '-Djna.library.path="/u/ea/pbutti/nfs/slac/g/hps2/pbutti/alignment/GeneralBrokenLines/cpp/lib/" '
        
        #nominal reconstruction
        cmd = 'java -XX:+UseSerialGC -Xmx3000m '+jnaLib+' -jar ' + self.hpsJavaDir+"/"+self.jarFile + ' ' + self.steeringFile  +' -i ' + inputFilename + ' -DoutputFile=$OUTPUTDIR/'+outFileName
        cmd+=" -d " + self.detector
        cmd+=" "+extraFlags
        
        #from evio
        if (year=="2019"):
            if (fileExt=="evio"):
                cmd = 'java -Xmx3000m -DdisableSvtAlignmentConstants '+jnaLib+' -cp ' +self.hpsJavaDir+"/"+self.jarFile + ' org.hps.evio.EvioToLcio ' + inputFilename + ' -DoutputFile=$OUTPUTDIR/'+outFileName
                cmd+=" -d " + self.detector + " -x " + self.steeringFile
            else:
                cmd = 'java -DdisableSvtAlignmentConstants -XX:+UseSerialGC -Xmx3000m '+jnaLib+' -jar ' + self.hpsJavaDir + "/"+ self.jarFile + ' ' + self.steeringFile + ' -i ' + inputFilename + ' -DoutputFile=$OUTPUTDIR/'+outFileName
                cmd+=" -d " + self.detector
                cmd+=" "+extraFlags

        if (nevents>0):
            cmd+=' -n ' + str(nevents)
        self.wline(cmd)


    def runHipster(self,slcioFile,outFile,cfg,isData,extraFlags=""):
        self.wline('source '+self.hpstrFolder+'/hpstr_env_init.sh')
        cmd = 'hpstr ' +cfg + ' -i ' + slcioFile + ' -o' + ' $OUTPUTDIR/'+ outFile + ' -t ' + isData
        cmd += " "+extraFlags
        self.wline(cmd)
        
            
    def runSlic(self,istdhep,ofile,det,nevs):
        self.wline('echo slic -g ' + det + ' -i ' + istdhep + ' -x -p $OUTPUTDIR/  -o ' + ofile + ' -r ' + str(nevs))
        self.wline('slic -g ' + det + " -i " + istdhep + " -x -p $OUTPUTDIR/ -o " + ofile + " -r " + str(nevs))
    
    
    def setSteeringFile(self, steeringFile):
        self.steeringFile = steeringFile
    
    def setJarFile(self, jarFile):
        self.jarFile = jarFile

    def setHPSJavaDir(self, javaDir):
        self.hpsJavaDir = javaDir

    def setHpstrFolder(self, hpstrFolder):
        self.hpstrFolder = hpstrFolder

    def setTmpPrefix(self, tmpPrefix):
        self.tmpPrefix = tmpPrefix
