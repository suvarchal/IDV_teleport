# IDV_teleport
Script to relocate the space-time bounding box of one or more existing (‘template’) IDV bundles. User specifies -bbox in lat-lon space, and one or a list of temporal ranges. Time ranges are specified as a central time (-t) and temporal half width (-td). The temporal stride is set in the template BUNDLE.xidv, and can only be changed in the IDV GUI. 

Please use latest nightly version of [IDV](http://www.unidata.ucar.edu/software/idv/nightly/)

Usage:

       idv_teleport.py [-h] -t TIME -b BUNDLE [BUNDLE ...] [-td TIMEDELTA]
                       [-bbox NORTH WEST SOUTH EAST]
                       [-case CASE_NAME [CASE_NAME ...]]
                       [-outdir OUTPUT_DIRECTORY] [-d {True,False}]
                       [-purl PUBLISH_URL]
      
Optional arguments:

    -h, --help               show this help message and exit
    -b BUNDLE.xidv [BUNDLE2.xidv ...], --bundle BUNDLE.xidv [BUNDLE2.xidv ...]
                             IDV Bundle template file (local file or remote URL)
                             Can also be a .zidv file.               
    -bbox NORTH WEST SOUTH EAST, --boundingbox NORTH WEST SOUTH EAST
                             Set the bounding box of the bundle with boundaries
                             north, west, south, east
    -t TIME, --time TIME  Input central time as YYYY-MM-DD (optionally with hh:mm:ss),
                             or as a text file with times as above, one per line.
    -td TIMEDELTA, --timedelta TIMEDELTA
                             Time delta as Nseconds, Nhours, Ndays, Nweeks…
                             Output bundle will be centered (TIME +- TIMEDELTA).
                             Default is 0seconds. 
    -case CASE_NAME [CASE_NAME2 ...], --case_name CASE_NAME [CASE_NAME ...]
                             Case name to prefix the bundle; by default, the case name
                             will be selected from template bundle file
    -outdir OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                             Set the output path to place the output;default is
                             current directory from where the script is run
    -d {True,False}, --debug {True,False}
                             Debug option; for each time in timefile, IDV session
                             will remain open and MUST be closed manually
    -purl PUBLISH_URL, --publish_url PUBLISH_URL
                             Publish bundle and image at a RAMADDA server; Currently
                        not implemented.

Simplest use case: 

     python idv_teleport.py -b templatebundlefile.xidv -t YYYY-MM-DD_hh:mm:ss
