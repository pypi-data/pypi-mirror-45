from __future__ import print_function
import sys
import os
path=os.environ["GIT_REPO"]
sys.path.insert(0, path+'/lib/paragon/Python')
import tcl
import paragon as p
try:
    p.connect("10.78.100.108", "10.106.213.195", 9000, 9990)
except:
    print("\nCould Not Connect to Paragon Instrument. Exiting")
    exit()
p.paragonset("SimulMeasImpairMode","MEASUREONLY")
p.paragonset("OperatingMode","PTP")
p.paragonset("MasterSlave Enabled","TRUE")
p.paragonset("Physical LineRate","1GBE")
p.paragonset("MasterSlave TestConfiguration","BOUNDARY_CLOCK")
p.paragonset("MasterSlave StandardsProfile","G.8275.1_PHASE_PROFILE")
p.paragonset("MasterSlave FlowFilter CaptureSlaveMAC","d0 00 00 00 00 01")
p.paragonset("MasterSlave FlowFilter CaptureMulticastAnnounce","TRUE")
p.paragonset("MasterSlave FlowFilter CaptureMulticastSync","TRUE")
p.paragonset("MasterSlave FlowFilter CaptureMulticastDelay","TRUE")
p.paragonset("MasterSlave FlowFilter CaptureMulticastAllSlaves","FALSE")
p.paragonset("MasterSlave FlowFilter CaptureMulticastSlavePortId","00 00 00 00 00 00 00 02 00 01")
p.paragonset("MasterSlave FlowFilter CaptureSet","TRUE")
p.paragonset("MasterSlave StartMeasurement","TRUE")
p.stopcapture()
p.paragonset("Cat Show", "TRUE")
p.paragonset("Cat Close")
p.paragonset("Cat", "1588TimeError")
p.waitforcat()
#p.paragonset("Cat TIMEERROR Enable", "TRUE")
#p.paragonset("Cat AVERAGEDTE Enable", "True")
#p.paragonset("Cat DTEMTIE Enable", "True")
#p.paragonset("Cat DTETDEV Enable", "True")
p.paragonset ("Cat SelectSlot", "2Way")
p.paragonset("Cat TransientResponse Enable", "True")
p.paragonset("Cat AVERAGEDTE AveragingPeriod", str(measure_time))
p.paragonset ("Cat Calculate")
p.stopcapture()
p.paragonset("MasterSlave Master #0 Enabled","FALSE")
