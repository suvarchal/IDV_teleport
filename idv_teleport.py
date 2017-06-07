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
    screencapture = u"""
def screencapture(width=None,height=None):
    from ucar.unidata.ui.ImageUtils import resize,toBufferedImage
    import java
    import java.awt.Robot as Robot
    import java.awt.Rectangle as Rectangle
    import java.awt.Toolkit as Toolkit
    from ucar.unidata.util import Misc
    from java.awt import Point
    from java.awt import Toolkit
    from java.awt import GraphicsEnvironment

    VM=idv.getViewManager()
    VMC=VM.getContents()
    VMCC=VMC.getComponent(1) # the view and legend ; 0 is left most part of view window with controls for perspective views

    gc= VMCC.getGraphicsConfiguration()

    loc = VMCC.getLocationOnScreen()
    siz = VMCC.getSize()

    # could also capture window by using window
    # DW=VM.getDisplayWindow()
    # AW=DW.getActiveWindow()
    # active window can be made fullscreen
    # gcd=gcd.setFullScreenWindow(AW.getWindow()) #gcd=graphic control device
    # quality can be improved by setting full screen or unlimitedly
    # on virtual screens by setting big screen size
    loc.x -= gc.getBounds().x
    loc.y -= gc.getBounds().y


    robotx=Robot() #gc.getDevice())

    #VM.toFront()

    W=VM.getDisplayWindow().getActiveWindow().getWindow()
    W.setAlwaysOnTop(True)
    Misc.sleep(150)
    img=robotx.createScreenCapture(Rectangle(loc.x, loc.y,siz.width, siz.height))
    W.setAlwaysOnTop(False)

    if width != None and height != None:
        img=toBufferedImage(resize(img,width,height))
    return img

def screen_image(width=None,height=None):
    from ucar.unidata.ui import ImageUtils
    from threading import Lock
    VM=idv.getViewManager()
    anim=VM.getAnimation()
    anim.setCurrent(len(VM.getAnimationTimes())/2)
    lock=Lock()
    with lock:
        img = screencapture(width,height)
    ImageUtils.writeImageToFile(img,'{0:s}'+'.png')

def screen_animation(width=None,height=None):
    from ucar.unidata.ui import AnimatedGifEncoder
    from ij import ImagePlus
    from threading import Lock
    VM=idv.getViewManager()
    e=AnimatedGifEncoder()
    e.start('{0:s}'+'.gif')
    anim=VM.getAnimation()
    VM.getAnimationWidget().gotoBeginning()
    for t in range(len(VM.getAnimationTimes())):
        lock=Lock()
        anim.setCurrent(t)
        with lock:
            data=screencapture()
        e.addFrame(ImagePlus(str(t),data))
    """.format(case_name)
    if not ul_lat and not ul_lon and not lr_lat and not lr_lon:
        xidv_string = u"""<isl>
                  <bundle file="{0:s}" timedriverstart="{1:s}" timedriverend="{2:s}" />
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
<displayproperties display="class:ucar.unidata.idv.control.ColorPlanViewControl">
<property name="DisplayAreaSubset" value="true"/>
</displayproperties>
                  <image file="{3:s}1.png"/>
                  <movie file="{4:s}.gif"/>
                  <save file="{5:s}.zidv"/>
                  <pause seconds="60"/>
                  <pause/>
                  <jython><![CDATA[
                  {6:s}
                  ]]>
                  </jython>
                  <pause/>
                  <jython code="idv.waitUntilDisplaysAreDone()"/>
                  <jython code="screen_image()"/>
                  <jython code="screen_animation()"/>
                  <jython code="exit()"/>
                  </isl>""".format(bundle_file, time_start, time_end, case_name,
                                   case_name, case_name, screencapture)
    else:
        xidv_string = u"""<isl>
                  <bundle file="{0:s}" timedriverstart="{1:s}" timedriverend="{2:s}" bbox="{3:s},{4:s},{5:s},{6:s}"/>
                  <pause/>
                  <pause seconds="40"/>
                  <pause/>
<displayproperties display="class:ucar.unidata.idv.control.ColorPlanViewControl">
<property name="DisplayAreaSubset" value="true"/>
</displayproperties>
                  <image file="{7:s}1.png"/>
                  <movie file="{8:s}.gif"/>
                  <save file="{9:s}.zidv"/>
                  <pause seconds="60"/>
                  <pause/>
                  <jython code="idv.waitUntilDisplaysAreDone()"/>
                  <jython><![CDATA[
                  {10:s}
                  ]]>
                  </jython>
                  <jython code="screen_image()"/>
                  <jython code="screen_animation()"/>
                  <jython code="exit()"/>
                  </isl>""".format(bundle_file, time_start, time_end, str(ul_lat), str(ul_lon), str(lr_lat),
                                   str(lr_lon), case_name, case_name, case_name, screencapture)
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
    xvfb_executable += ' -screen 0 1800x1600x24'
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
