from __future__ import print_function
import sys
import os
path="/ws/manalgup-bgl/NEW_TIME/cafykit/"
sys.path.insert(0, path+'/lib/paragon/Python')
sys.path.insert(0, path+'/lib/paragon/tcl_perf')

import paragon as p
try:
    p.connect("10.78.100.108", "10.106.213.195", 9000, 9990)
except:
    print("\nCould Not Connect to Paragon Instrument. Exiting")
    exit()
os.system("/bin/tclsh /ws/manalgup-bgl/NEW_TIME/cafykit/lib/paragon/tcl_perf/G.8273.2.tcl")
