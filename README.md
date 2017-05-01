# IDV_bundle_composite
Given a time file and a bundle template file, this script makes new bundles for corresposnding times

Please use latest nightly version of [IDV](http://www.unidata.ucar.edu/software/idv/nightly/)

Usage:

      usage summary: bundlescript.py [-h] -t TIME -b BUNDLE [BUNDLE ...] [-td TIMEDELTA]
                       [-bbox NORTH WEST SOUTH EAST]
                       [-case CASE_NAME [CASE_NAME ...]]
                       [-outdir OUTPUT_DIRECTORY] [-d {True,False}]
                       [-purl PUBLISH_URL]

More Help: 

      python bundlescript.py -h
      
Simplest case:      

      python bundlescript.py -t timefile -b bundletemplate 
      
      
All options:
usage: bundlescript.py [-h] -t TIME -b BUNDLE [BUNDLE ...] [-td TIMEDELTA]
                       [-bbox NORTH WEST SOUTH EAST]
                       [-case CASE_NAME [CASE_NAME ...]]
                       [-outdir OUTPUT_DIRECTORY] [-d {True,False}]
                       [-purl PUBLISH_URL]

Script to make time composite of IDV Bundles.

optional arguments:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  Input time as YYYY-MM-DD or a text file with times one
                        per line also optionally with hh:mm:ss
  -b BUNDLE [BUNDLE ...], --bundle BUNDLE [BUNDLE ...]
                        IDV Bundle template file local or remote
  -td TIMEDELTA, --timedelta TIMEDELTA
                        Time delta as Nseconds, Ndays, Nweeks ...; output
                        bundle will be centered around +- timedelta; default
                        is 0seconds
  -bbox NORTH WEST SOUTH EAST, --boundingbox NORTH WEST SOUTH EAST
                        Set the bounding box of the bundle with boundaries
                        north, west, south, east
  -case CASE_NAME [CASE_NAME ...], --case_name CASE_NAME [CASE_NAME ...]
                        Case name to prefix the bundle; by default case name
                        will be selected from bundle file
  -outdir OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Set the output path to place the output;default is
                        current directory from where the script is run
  -d {True,False}, --debug {True,False}
                        Debug option; for each time in timefile IDV session
                        will ONLY close manually
  -purl PUBLISH_URL, --publish_url PUBLISH_URL
                        Publish bundle and image at a RAMADDA server;Currently
                        not implemented

Simplest use case:python script.py -t timefile -b templatebundlefile
