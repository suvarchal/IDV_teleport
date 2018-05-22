#!/bin/bash
curl -s ftp://ftp.unidata.ucar.edu/pub/idv/nightly_idv_5.5/idv_5_5_linux64_installer.sh>idv.sh
chmod +x idv.sh
echo `pwd`
printf 'o\n\n1\n'`pwd`'/IDV\n'|./idv.sh
wkdir=`echo pwd`
export IDV_HOME=${wrkdir}/IDV
cd test
idv_teleport -b NOAA_sst.xidv -t 2011-01-01
