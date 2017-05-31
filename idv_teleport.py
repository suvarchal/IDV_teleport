import argparse
import os
import re
import tempfile
import sys
import subprocess
from distutils import spawn
from random import randint


def parse_date_time_file(datefile):
    datelist = []
    with open(datefile) as fil:
        for line in fil.readlines():
            checkline = line.strip().split('-')
            assert len(checkline) > 1, "Time specified in input is not in valid format yyyy-mm-dd"
            datelist.append(line)
    return datelist


def isl_string(bundle_file, time_start, time_end, case_name=None,
               ul_lat=None, ul_lon=None, lr_lat=None, lr_lon=None):
    screencapture = """
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
    ImageUtils.writeImageToFile(img,'%s')""" % (case_name + ".png")
    if not ul_lat and not ul_lon and not lr_lat and not lr_lon:
        xidv_string = """<isl>
                  <bundle file="%s" timedriverstart="%s" timedriverend="%s" />
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
<displayproperties display="class:ucar.unidata.idv.control.ColorPlanViewControl">
<property name="DisplayAreaSubset" value="true"/>
</displayproperties>
                  <image file="%s1.png"/>
                  <movie file="%s.gif"/>
                  <save file="%s.zidv"/>
                  <pause/>
                  <jython><![CDATA[
                  %s
                  ]]>
                  </jython> 
                  <pause/>
                  <jython code="showImgWithFullWindow()"/>
                  <pause/>
                  <jython code="exit()"/>
                  </isl>""" % (bundle_file, time_start, time_end, case_name,
                               case_name, case_name, screencapture)
    else:
        xidv_string = """<isl>
                  <bundle file="%s" timedriverstart="%s" timedriverend="%s" bbox="%s,%s,%s,%s"/>
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
<displayproperties display="class:ucar.unidata.idv.control.ColorPlanViewControl">
<property name="DisplayAreaSubset" value="true"/>
</displayproperties>
                  <image file="%s1.png"/>
                  <movie file="%s.gif"/>
                  <save file="%s.zidv"/>
                  <pause/>
                  <jython><![CDATA[
                  %s
                  ]]>
                  </jython> 
                  <pause/>
                  <jython code="showImgWithFullWindow()"/>
                  <pause/>
                  <jython code="exit()"/>
                  </isl>""" % (bundle_file, time_start, time_end, ul_lat, ul_lon, lr_lat,
                               lr_lon, case_name, case_name, case_name, screencapture)
    return xidv_string


def parse_date_time(datetimelist, parser):
    import datetime

    match = re.match(r"(\d+)(\w+)", args.timedelta)
    try:
        timedelta, time_str = match.groups()
        dtime = datetime.timedelta(**{time_str: int(timedelta)})
    except:
        parser.print_usage()
        print("Please set -td or --timedelta as 1seconds or 1days....")
        sys.exit(2)
    startdates = []
    enddates = []
    ignorelist = []
    centerdates = []
    for time in datetimelist:
        try:
            if len(time.strip()) > 10:
                time_c = datetime.datetime(int(time[0:4]), int(time[5:7]), int(time[8:10]),
                                           int(time[11:13]), int(time[14:16]), int(time[17:19]))
                time_s = time_c - dtime
                time_e = time_c + dtime
            else:
                time_c = datetime.datetime(int(time[0:4]), int(time[5:7]), int(time[8:10]), 0, 0, 0)
                time_s = time_c - dtime
                time_e = time_c + dtime
            startdates.append(time_s.strftime('%Y-%m-%d %H:%M:%S'))
            enddates.append(time_e.strftime('%Y-%m-%d %H:%M:%S'))
            centerdates.append(time_c.strftime('%Y-%m-%d-%H-%M-%S'))
        except:
            ignorelist.append(time.strip())
    return startdates, enddates, centerdates, ignorelist


def run_xvfb():
    xvfb_proc = None
    xvfb_executable = spawn.find_executable('Xvfb')
    r_int = randint(10, 99)
    xvfb_executable += ' :' + str(r_int)
    xvfb_executable += ' -screen 0 1280x1024x24'
    # print(xvfb_executable)
    xvfb_proc = subprocess.Popen(xvfb_executable.split())
    # print(xvfb_proc.pid)

    if not xvfb_proc.poll():
        os.environ['DISPLAY'] = ':' + str(r_int) + '.0'
        return xvfb_proc
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to teleport time and space domain of an IDV Bundle.',
                                     epilog="Simplest use case:python IDV_teleport.py "
                                            "-t timefile "
                                            "-b templatebundlefile.xidv")

    parser.add_argument('-b', '--bundle', nargs='+',
                        help='IDV Bundle template file, local or remote',
                        required=True)

    parser.add_argument('-bbox', '--boundingbox', nargs=4, type=float,
                        help='Set the bounding box of the bundle with boundaries: '
                             'north, west, south, east',
                        metavar=("NORTH", "WEST", "SOUTH", "EAST"))

    parser.add_argument('-t', '--time', type=str,
                        help='Input time as YYYY-MM-DD or a text file with times '
                             'one per line also optionally with hh:mm:ss',
                        required=True)
    parser.add_argument('-td', '--timedelta',
                        help='Time delta (hald-duration) as Nseconds, Ndays, Nweeks ...;'
                             ' output bundle times will be central time +- timedelta;'
                             ' default is 0seconds',
                        default="0seconds", required=False)

    parser.add_argument('-case', '--case_name', type=str, nargs='+',
                        help='Case name to prefix the bundle;'
                             'By default case name will be selected from bundle file',
                        required=False)
    parser.add_argument('-outdir', '--output_directory', type=os.path.isdir,
                        help='Set the output path to place the output;'
                             'default is current directory from where the script is run',
                        required=False)
    parser.add_argument('-d', '--debug', choices=("True", "False"), default="False",
                        help='Debug option; '
                             'For each time in timefile IDV session will ONLY close manually',
                        required=False)
    parser.add_argument('-purl', '--publish_url',
                        help='Publish bundle and image at a RAMADDA server;'
                             'Currently not implemented',
                        required=False)
    args = parser.parse_args()
    try:
        idv_home = os.environ['IDV_HOME']
    except:
        parser.print_usage()
        print("Please set environment variable IDV_HOME to IDV home directory")
        sys.exit(2)

    orig_display_id = os.environ['DISPLAY']
    headless = not orig_display_id
    xvfb = run_xvfb()
    if headless and not xvfb:
        raise Exception('Headless environment detected and Xvfb not working, please check '
                        'if Xvfb is already running ')

    # check if datefile is time or file
    if os.path.isfile(args.time):
        datelist = parse_date_time_file(args.time)
    else:
        datelist = [str.join(' ', args.time.split('_'))]

    startdates, enddates, centerdates, ignorelist = parse_date_time(datelist, parser)

    if args.output_directory:
        output_directory = args.output_directory
    else:
        output_directory = os.getcwd()

    bundle_file = '\ '.join(args.bundle)
    for start, end, center in zip(startdates, enddates, centerdates):
        if args.case_name:
            case_name = os.path.join(output_directory, args.case_name[0])  # +'_'+center)
        else:
            case_name = os.path.join(output_directory,
                                     os.path.split(bundle_file)[-1].split('.')[0] + '_' + center)
        if args.boundingbox:
            isl = isl_string(bundle_file, start, end, case_name,
                             args.boundingbox[0], args.boundingbox[1],
                             args.boundingbox[2], args.boundingbox[3])
        else:
            isl = isl_string(bundle_file, start, end, case_name)

        wtf = tempfile.NamedTemporaryFile(mode="w", suffix=".isl", dir="./")
        wtf.file.write(isl)
        wtf.file.close()
        try:
            subprocess.call([os.path.join(idv_home, "runIDV"), "-islinteractive",
                             "-noerrorsingui", wtf.name.split('/')[-1]])
        except:

            pass
        if not xvfb.poll():
            xvfb.kill()
            os.environ['DISPLAY'] = orig_display_id  # imp otherwise headless
            # will not work next time
