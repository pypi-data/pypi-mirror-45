################################################################################
#                                                                              #
#   test_simple.py                                                             #
#                                                                              #
#   "Timing capture"                                                           #
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

from __future__ import print_function

import paragon as p

# Connect
p.connect("192.168.3.100")

# Retrieve and print the instrument serial number
print("Instrument serial number: " + p.paragonget("Idn"))

# Test performing a capture for 1 second
p.paragonset("OperatingMode", "CES")

p.paragonset("Capture Control Mode", "Fixed")
p.paragonset("Capture Control FixedPeriod", "1SEC")

p.starttimingcapture()

# And disconnect
p.disconnect()
