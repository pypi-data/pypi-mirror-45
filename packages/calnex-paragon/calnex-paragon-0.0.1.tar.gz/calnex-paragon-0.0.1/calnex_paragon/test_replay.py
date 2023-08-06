################################################################################
#                                                                              #
#   test_replay.py                                                             #
#                                                                              #
#   "Timing replay"                                                            #
#                                                                              #
#   Python test script to interface with Calnex Paragon                        #
#                                                                              #
#   Copyright (c) Calnex Solutions Ltd 2013                                    #
#                                                                              # 
#   The contents of this file should not be copied or distributed              #
#   without permission being granted by Calnex Solutions Ltd.                  #
#                                                                              #
#   All rights reserved.                                                       #
#                                                                              #
################################################################################

import paragon as p

# Connect
p.connect("192.168.3.100")

try:
    p.paragonset("Rst")
    p.paragonset("OperatingMode", "CES")

    # Enable overwrite (thru-mode)
    p.paragonset("Impair EnableOverwrite", "TRUE")
    
    # Enable delay impairment on port 1
    p.paragonset("Impair VariableDelay #0 Enable", "TRUE")
    
    # Load impairment file to replay on Port1 incoming traffic
    #p.importimpairmentdata(1, "c:\\replay_traffic.cpd")
    # Perform a test
    #p.startimpairment()
    #p.stopimpairment()

    # Perform another test replaying profiles in Port 1 and Port 2 directions
    p.paragonset("Impair VariableDelay #0 Enable", "TRUE")
    p.paragonset("Impair VariableDelay #1 Enable", "TRUE")
    
    # Sawtooth Profile Beating,F on Port 1, offset 2.0 ppm
    p.paragonset("Impair VariableDelay #0 ProfileType", "SawTooth")
    p.paragonset("Impair VariableDelay #0 SawToothType", "Beating,F")
    p.paragonset("Impair VariableDelay #0 Offset", "2.0")
    
    # Sawtooth Profile Latency on Port 2,Magnitude 10uS, Ramp Period 0.4S
    p.paragonset("Impair VariableDelay #1 ProfileType", "Latency")
    p.paragonset("Impair VariableDelay #1 Magnitude", "10.0")
    p.paragonset("Impair VariableDelay #1 RampPeriod", "0.4")
    
    # Perform the test
    p.startimpairment()
    p.stopimpairment()

    # Switch to Services Mode, apply corruption on FilterFlow 3
    p.paragonset("OperatingMode", "SERVICES")
    
    # Set a flow filter to apply filter item 1 matching byte offset 9
    # and byte mask xx0xx0xx to the incoming traffic
    p.paragonset("Filter #2 #1 Offset", "9") 
    p.paragonset("Filter #2 #1 ByteMask", "00x00x00")
    p.paragonset("Filter #2 Direction", "P1P2")
    p.paragonset("Filter", "ApplyAll")
    
    # Perform test applying misordered packet for 10 seconds
    p.paragonset("Impair Corruption #2 ErrorEnable", "TRUE")
    p.paragonset("Impair Corruption #2 ErrorType", "MISORDERED")
    p.paragonset("Impair Corruption #2 Distribution Type", "BURST")
    p.paragonset("Impair Corruption #2 Distribution BurstSize", "10")

    p.startimpairment()
    p.stopimpairment()
    
finally:
    # And disconnect
    p.disconnect()
