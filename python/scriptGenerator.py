import subprocess

class scriptGenerator:

    # Members
    
    scriptFile = ""
    scriptFileName = ""
    scriptdir      = ""
    outputdir      = ""
    step           = "stdhep"


    #Methods

    def __init__(self, step, scriptdir,outputdir):
        self.step           = step
        self.scriptdir      = scriptdir
        self.outputdir      = outputdir

    def setupStep(self):
        pass

    def generateScript(self,fileID):
        self.scriptFileName = self.scriptdir+"/script_submit_job_"+fileID+".sh"
        self.scriptFile = open(self.scriptFileName,"w")
        self.wline("#! /bin/bash")
        self.wline('JOBFILEDIR=`mktemp -d /scratch/${LSB_JOBID}_JobWork.XXXXXX`')
        self.wline('echo "Job file directory: $JOBFILEDIR"')
        self.wline('export HOME=$JOBFILEDIR')
        self.wline('cd $HOME')
        self.wline('OUTPUTDIR=$JOBFILEDIR/outputs_${LSB_JOBID}/; mkdir $OUTPUTDIR')
        self.wline('echo "Created $OUTPUTDIR"')
        
    def closeScript(self):
        self.wline('echo "Moving files to outputdir"')
        self.wline('mv $OUTPUTDIR ' + self.outputdir)
        self.wline('echo "Removing $JOBFILEDIR"')
        self.wline('rm -R $JOBFILEDIR')
        self.scriptFile.close()
        subprocess.call(["chmod","u+x",self.scriptFileName])


    def wline(self,line):
        self.scriptFile.write(line+"\n")
        
    def setupStdhepToSimul(self,stdhepFile,outFileName,detector,nEvents):
        #TODO-FIX THIS
        self.wline('cd /nfs/slac/g/hps2/pbutti/hps-java/')
        # Setup SLCIO
        self.wline('source /nfs/slac/g/hps/hps_soft/slic/build/slic-env.sh')
        self.runSlic(stdhepFile,outFileName,detector,nEvents)

    def runSlic(self,istdhep,ofile,det,nevs):
        self.wline('echo slic -g ' + det + ' -i ' + istdhep + ' -x -p $OUTPUTDIR/  -o ' + ofile + ' -r ' + str(nevs))
        self.wline('slic -g ' + det + " -i " + istdhep + " -x -p $OUTPUTDIR/ -o " + ofile + " -r " + str(nevs))
    
    