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
