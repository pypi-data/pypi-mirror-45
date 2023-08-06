Instrumet_IpAddress = "10.105.230.45"
#import .py files
import paragon as p
import CalnexRest as pRest
#connect to Instrument from machine where Python running
p.connect("localhost", Instrumet_IpAddress)
pRest.calnexInit (Instrumet_IpAddress)
#to reset instrument
p.paragonset("Rst")
#set device mode
p.paragonset("OperatingMode", "PTP")
#Set interface
p.paragonset("Physical InterfaceExtended", "QSFP28")

#select g8273.2
pRest.calnexSet ("instrument/preset", "Name", "Conformance Test - G.8273.2 Standard")

#select Noise transfer test
pRest.calnexSet ("app/conformance/test", "Test", 'PTP to PTP Noise Transfer')

#start noise transfer test
pRest.calnexSet ("app/conformance/generation/start")

pRest.calnexSet("app/conformance/generation/stop")
pRest.calnexSet ("app/conformance/generation/start")
pRest.calnexSet ("app/conformance/measurement/start")
pRest.calnexSet ("app/conformance/measurement/stop")
pRest.calnexSet ("app/conformance/generation/stop")
pRest.calnexSet("cat/measurement/DelayReq/D/PTPNoiseTransfer/-/mask", "MaskName", 'G.8273.2 Class A,B T-BCs Noise Transfer')
pRest.calnexSet("cat/measurement/DelayReq/D/PTPNoiseTransfer/-/visiblewindow", "XMin", 0, "XMax", 0, "YMin", 0, "YMax", 0)
#To openCAT
#pRest.calnexSet("cat/general/tclparse", "TclCommand", 'paragonset Cat Show TRUE')
#pRest.calnexSet("cat/measurement/1ppsTEAbsolute/F/PTPNoiseTransfer/-/enable", "Value", True)
#pRest.calnexSet("cat/measurement/1ppsTEAbsolute/F/PTPNoiseTransfer/-/enable", "Value", False)

#to apply mask
#pRest.calnexSet("cat/measurement/1ppsTEAbsolute/F/PTPNoiseTransfer/-/mask", "MaskName", 'G.8273.2 Class A,B T-BCs Noise Transfer')
#pRest.calnexSet("cat/measurement/1ppsTEAbsolute/F/PTPNoiseTransfer/-/visiblewindow", "XMin", 0, "XMax", 0, "YMin", 0, "YMax", 0)

#to Get amsk result
#pRest.calnexGet("cat/measurement/1ppsTEAbsolute/F/PTPNoiseTransfer/-/mask", "MaskName", 'G.8273.2 Class A,B T-BCs Noise Transfer')
