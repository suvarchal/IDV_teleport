def parseDateTimeFile(datefile):
    import datetime
    datelist=[]
    with open(datefile) as f:
        for ln in f.readlines():
            checkline=ln.strip().split('-')
            #print(checkline) 
            assert len(checkline)>1,"Time specified in inpute is not in valid format yyyy-mm-dd"
            datelist.append(ln)
    return datelist
        
def islString(BundleFile,timeStart,timeEnd,caseName=None,ULLat=None,ULLon=None,LRLat=None,LRLon=None):
    screencapture="""
def showImgWithFullWindow(width=None,height=None):
    from java.util import Base64 ##only in java8
    from javax.imageio import ImageIO
    from java.io import ByteArrayOutputStream
    from ucar.unidata.ui.ImageUtils import resize,toBufferedImage
    import java
    import java.awt.Robot as Robot
    import java.awt.Rectangle as Rectangle
    import java.awt.Toolkit as Toolkit
    from ucar.unidata.util import Misc
    from ucar.unidata.ui import ImageUtils
    VM=idv.getViewManager()
    myframe=VM.getDisplayWindow().getComponent()
    robotx = Robot(myframe.getGraphicsConfiguration().getDevice())
    VM.toFront();
    robotx.delay(250)
    #Misc.sleep(350)
    #pause()
    img=robotx.createScreenCapture(Rectangle( myframe.getX(),myframe.getY(),myframe.getWidth(),myframe.getHeight()))
    if width != None and height != None:
        img=toBufferedImage(resize(img,width,height))
    ImageUtils.writeImageToFile(img,'%s')"""%(caseName+".png")
    if not ULLat and not ULLon and not LRLat and not LRLon:
        XidvString="""<isl> 
                  <bundle file="%s" timedriverstart="%s" timedriverend="%s" />
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
                  <image file="%s1.png"/>
                  <save file="%s.xidv"/>
                  <pause/>
                  <jython><![CDATA[
                  %s
                  ]]>
                  </jython> 
                  <pause/>
                  <jython code="showImgWithFullWindow()"/>
                  <pause/>
                  <jython code="exit()"/>
                  </isl>"""%(BundleFile,timeStart,timeEnd,caseName,caseName,screencapture)
    else:
        XidvString="""<isl> 
                  <bundle file="%s" timedriverstart="%s" timedriverend="%s" bbox="%s,%s,%s,%s"/>
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
                  <image file="%s1.png"/>
                  <save file="%s.xidv"/>
                  <pause/>
                  <jython><![CDATA[
                  %s
                  ]]>
                  </jython> 
                  <pause/>
                  <jython code="showImgWithFullWindow()"/>
                  <pause/>
                  <jython code="exit()"/>
                  </isl>"""%(BundleFile,timeStart,timeEnd,ULLat,ULLon,LRLat,LRLon,caseName,caseName,screencapture)
    return XidvString
    
def parseDateTime(datetimelist,timedelta,parser):
    import sys
    import datetime
    match = re.match(r"(\d+)(\w+)", args.timedelta)
    try:
         timedelta,time_str=match.groups()
         dt=datetime.timedelta(**{time_str:int(timedelta)})
    except: 
         parser.print_usage()
         print("Please set -td or --timedelta as 1seconds or 1days....")
         sys.exit(2)
    startdates=[]
    enddates=[]
    ignorelist=[]
    centerdates=[]
    for time in datetimelist:
        try:
	    if len(time.strip())>10:
                timeC=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11-13]),int(time[14-16]),int(time[17-19]))
                timeS=timeC-dt
                timeE=timeC+dt
            else:
	        timeC=datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),0,0,0)
                timeS=timeC-dt
                timeE=timeC+dt
            startdates.append(timeS.strftime('%Y-%m-%d %H:%M:%S'))
            enddates.append(timeE.strftime('%Y-%m-%d %H:%M:%S'))
            centerdates.append(timeC.strftime('%Y-%m-%d-%H-%M-%S'))
        except:
            ignorelist.append(time.strip())
    return startdates,enddates,centerdates,ignorelist        
            
import argparse
import os 
import datetime 
import re
import tempfile
import sys
import subprocess

parser = argparse.ArgumentParser(description='Script to make time composite of IDV Bundles.',epilog="Simplest use case:python script.py -t timefile -b templatebundlefile")
parser.add_argument('-t','--time',type=str,help='Input time as YYYY-MM-DD or a text file with times one per line also optionally with hh:mm:ss',required=True)
parser.add_argument('-b','--bundle',nargs='+',help='IDV Bundle template file local or remote', required=True)
parser.add_argument('-td','--timedelta',help='Time delta as Nseconds, Ndays, Nweeks ...; output bundle will be centered around +- timedelta; default is 0seconds',default="0seconds",required=False)
parser.add_argument('-bbox','--boundingbox',nargs=4,type=float,help='Set the bounding box of the bundle with boundaries north, west, south, east',metavar=("NORTH","WEST","SOUTH","EAST"))
parser.add_argument('-case','--case_name',type=str,nargs='+',help='Case name to prefix the bundle; by default case name will be selected from bundle file',required=False)
parser.add_argument('-outdir','--output_directory',type=os.path.isdir,help='Set the output path to place the output;default is current directory from where the script is run',required=False)
parser.add_argument('-d','--debug',choices=("True","False"),default="False",help='Debug option; for each time in timefile IDV session will ONLY close manually',required=False)
parser.add_argument('-purl','--publish_url',help='Publish bundle and image at a RAMADDA server;Currently not implemented',required=False)
args = parser.parse_args()
try:
    idv=os.environ['IDV_HOME']
except:
    parser.print_usage()
    print("Please set environment variable IDV_HOME to IDV home directory")
    sys.exit(2)

#check if datefile is time or file
if os.path.isfile(args.time):
    datelist=parseDateTimeFile(args.time)
else:
    datelist=[args.time]

startdates,enddates,centerdates,ignorelist=parseDateTime(datelist,args.timedelta,parser)

if args.output_directory:
    output_directory=args.output_directory
else:
    output_directory=os.getcwd()

bundle=args.bundle[0]
for start,end,center in zip(startdates,enddates,centerdates):
    if args.case_name:
        case_name=os.path.join(output_directory,args.case_name[0]+center)
    else:
        case_name=os.path.join(output_directory,os.path.split(bundle)[-1].split('.')[0]+center)
    if args.boundingbox:
        isl=islString(bundle,start,end,case_name,args.boundingbox[0],args.boundingbox[1],args.boundingbox[2],args.boundingbox[3])
    else:
        isl=islString(bundle,start,end,case_name)

    wtf = tempfile.NamedTemporaryFile(mode="w+b",suffix=".isl",dir="./")
    wtf.file.write(isl)
    wtf.file.close()
    try: 
        subprocess.call([os.path.join(idv,"runIDV"),"-islinteractive","-noerrorsingui",wtf.name])

    except:
        pass
