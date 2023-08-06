## @package paragon
#  paragon Python Module

################################################################################
#                                                                              #
#   paragon Python Module                                                      #
#                                                                              # 
#   Copyright (c) Calnex Solutions Ltd 2018                                    #
#                                                                              # 
#   The contents of this file should not be copied or distributed              #
#   without permission being granted by Calnex Solutions Ltd.                  #
#                                                                              #
#   All rights reserved.                                                       #
#                                                                              #
################################################################################

from __future__ import print_function

#import socket, sys, shlex, time, requests, json
import socket, sys, shlex, time

# PRIVATE Members and Functions
# -----------------------------
_revStr = "$Revision: 25438 $"

# Expected reply constants
_PARAGON_READY = "__PARAGON__";
_PARAGON_ERROR = "ERROR: ";

# Private module variables
_socket    = None;
_lastErr   = "";
_connected = False;
_instrumentType = "";
_instrumentIP = "";
_instrument = "";

# Debug enable/disable
_DEBUG = False;
#_DEBUG = True;

def _debug(msg):
    if _DEBUG == True:
        print(msg)
        sys.stdout.flush()

def _check_for_error(label):
    global _lastErr
    
    if len(_lastErr) > 0:
        raise Exception("%s : %s" %(label, _lastErr))

def _gui_connect(address, guiport):
    global _socket
    print("Connecting to %s:%s... " %(address, guiport))

    # Create a new socket and connect to the GUI
    _socket = socket.socket()
    _socket.connect((address, guiport))
    
    print("Success.")

    # Flush and check for errors
    _receive()
    _check_for_error("_gui_connect")

def _receive():
    global _lastErr, _socket

    response = "";
    _lastErr = "";
    
    # Create file from socket for convenience
    # and read each line from it
    file = _socket.makefile()
    for line in file:
        _debug("Received: %s" % line)        
        # Errors are returned as a string beginning 'ERROR: '
        # Ready is signalled by '__PARAGON__' prompt
        # Anything else is considered a response
        if line.find(_PARAGON_ERROR) >= 0:
            # Got an error
            _lastErr = line[len(_PARAGON_ERROR):len(line)]
        elif line.find(_PARAGON_READY) >= 0:
            # Got the ready prompt, OK to leave
            break
        else:
            # Got a response. Store it and continue
            response = line
    file.close()
    
    return response
    
if sys.version_info < (3, 0): # py2
    def _send(data):
        global _socket
        
        _debug("Sending %s... " % data)
        _socket.sendall("%s\n" % data)
        _debug("Done.")    
        return _receive().strip()
else: # py3
    def _send(data):
        global _socket
        
        _debug("Sending %s... " % data)
        _socket.sendall(bytes("%s\n" % data, "UTF-8"))
        _debug("Done.")    
        return _receive().strip()

def _is_connected(instrumentIP):
    response = _send("paragon.remoteprint(paragon.isconnected(\"%s\"))" % instrumentIP)
    _check_for_error("_is_connected")
    return int(response)

def _build_cmd_from_args(*args):
    cmd = ""
    for arg in args:
        # Indexed: 1st char is '#'
        if arg[0] == '#':
            arg = "__IDX____#__" + arg[1:len(arg)]
        # Append argument
        cmd = cmd + "__#__" + arg
    return cmd

def _instrument_connect(instAddr, instPort):
    print("Connecting to instrument %s:%s... " %(instAddr, instPort))
    _send("paragon.connect(\"%s\",\"%s\")" %(instAddr, instPort));
    _check_for_error("_instrument_connect %s:%s" %(instAddr, instPort))

def _instrument_disconnect():
    _send("paragon.disconnect()")
    _check_for_error("_instrument_disconnect")

def _query_errors():
    _send("paragon._queryerrors()")
    _check_for_error("_query_errors")

def _remote_control_on(rc):
    _send("paragon.on(%s)" % rc)
    _check_for_error("_remote_control_on")

def _remote_control_off():
    _send("paragon.off()")
    _check_for_error("_remote_control_off")

def _set_operating_mode(operatingMode):
    _send("paragon.CSettingParameter(\"__SET____#__OperatingMode__#__%s\")" % operatingMode)
    _check_for_error("_set_operating_mode %s" % operatingMode)

################################################################################
# The following routines are used to make the Rst process more robust
# There are occasions where Rst has issues when the instrument is active
# These routines try to make sure that the box is in an idle state before the 
# Rst is sent.
# Note: The Rst command is intercepted in paragonset; anything that is active on
# the instrument is then stopped and then the Rst is passed on.
# Since this file is also used for P100G, a number of the commands may fail
# if any given feature has not yet been implemented. This is avoided by making
# sure that errors are ignored in the appropriate places

##
# Check to see if any wander generation is running
# If so, stop it
def _stopWander():
	_debug("stopWander")
	isFreqOffsetRunning = "FALSE"
	tolSingleState  	= "IDLE"
	tolTableState  		= "IDLE"
	tolMtieTdevState  	= "IDLE"
	synceTransientState = "IDLE"
	transferSingleState = "IDLE"
	transferTableState 	= "IDLE"
	transferTdevState 	= "IDLE"
	
	try: isFreqOffsetRunning = paragonget("WanderGeneration FrequencyOffset Enable")
	except: pass
	try: tolSingleState = paragonget("WanderGeneration Tolerance Single State")
	except: pass
	try: tolTableState = paragonget("WanderGeneration Tolerance Table State")
	except: pass
	try: tolMtieTdevState = paragonget("WanderGeneration Tolerance MtieTdev State")
	except: pass
	try: synceTransientState = paragonget("WanderGeneration SyncETransient State")
	except: pass
	try: transferSingleState = paragonget("WanderGeneration Transfer Single State")
	except: pass
	try: transferTableState = paragonget("WanderGeneration Transfer Table State")
	except: pass
	try: transferTdevState = paragonget("WanderGeneration Transfer TDEV State")
	except: pass
	
	if (isFreqOffsetRunning != "FALSE"):
		paragonset("WanderGeneration FrequencyOffset Enable", "FALSE")
	
	if (tolSingleState != "IDLE"):
		paragonset("WanderGeneration Tolerance Single Enable", "FORCESTOP")
	
	if (tolTableState != "IDLE"):
		paragonset("WanderGeneration Tolerance Table Enable", "FORCESTOP")
	
	if (tolMtieTdevState != "IDLE"):
		paragonset("WanderGeneration Tolerance MtieTdev Enable", "STOP")
	
	if (synceTransientState != "IDLE"):
		paragonset("WanderGeneration SyncETransient Enable", "STOP")
	
	if (transferSingleState != "IDLE"):
		try: paragonset("WanderGeneration Transfer Single CalibrateEnable", "FORCESTOP")
		except: pass
		try: paragonset("WanderGeneration Transfer Single GenerateEnable", "FORCESTOP")
		except: pass
	
	if (transferTableState != "IDLE"):
		try: paragonset("WanderGeneration Transfer Table CalibrateEnable", "FORCESTOP")
		except: pass
		try: paragonset("WanderGeneration Transfer Table GenerateEnable", "FORCESTOP")
		except: pass
	
	if (transferTdevState != "IDLE"):
		paragonset("WanderGeneration Transfer TDEV Enable", "STOP")

def _stopPacketGeneration():
	_debug("stopPacketGeneration")
	isPort0Running = "FALSE"
	isPort1Running = "FALSE"
	
	try: isPort0Running = paragonget("PacketGeneration #0 Enable")
	except: pass
	try: isPort1Running = paragonget("PacketGeneration #1 Enable")
	except: pass

	if (isPort0Running != "FALSE"):
		paragonset("PacketGeneration #0 Enable", "FALSE")
	if (isPort1Running != "FALSE"):
		paragonset("PacketGeneration #1 Enable", "FALSE")

# Check to see if any jitter generation is running
# If so, stop it
def _stopJitter():
	_debug("stopJitter")
	tolSingleState  	= "IDLE"
	tolTableState  		= "IDLE"
	maxTolTableState  	= "IDLE"
	
	try: tolSingleState = paragonget ("Jitter Tolerance Single State")
	except: pass
	try: tolTableState  = paragonget ("Jitter Tolerance Table State")
	except: pass
	try: maxTolTableState = paragonget ("Jitter MaxTolerable Table State")
	except: pass
	
	if (tolSingleState != "IDLE"):
		paragonset ("Jitter Tolerance Single Enable", "FORCESTOP")
	if (tolTableState != "IDLE"):
		paragonset ("Jitter Tolerance Table Enable", "FORCESTOP")
	if (maxTolTableState != "IDLE"):
		paragonset ("Jitter MaxTolerable Table Enable", "FORCESTOP")
		
def _stopMSE():
	_debug("stopMSE")
	isMaster0Running = "FALSE"
	isMaster1Running = "FALSE"
	isSlaveRunning 	 = "FALSE"
	
	try: isMaster0Running = paragonget ("MasterSlave Master #0 Enabled")
	except: pass
	try: isMaster1Running = paragonget ("MasterSlave Master #1 Enabled")
	except: pass
	try: isSlaveRunning   = paragonget ("MasterSlave Slave Enabled")
	except: pass
	
	if (isMaster0Running != "FALSE"):
		paragonset ("MasterSlave Master #0 Enabled", "FALSE")
	if (isMaster1Running != "FALSE"):
		# Looks like the get doesn't return the correct status so ignore errors
		try: paragonset ("MasterSlave Master #1 Enabled", "FALSE")
		except: pass
	if (isSlaveRunning != "FALSE"):
		try: paragonset ("MasterSlave Slave Enabled", "FALSE")
		except: pass
		
def _stopCapture():
	_debug("stopCapture")
	#set retry 0
	stopcapture()
	#while {[paragonget InstrumentStatus Capture IsRunning] == TRUE && $retry < 6} {
	#	after 500
	#	stopcapture
	#	incr retry
	#}

def _stopImpairment():
	_debug("stopImpairment")
	try: stopimpairment()
	except: pass
	
## Before executing Rst, make sure that the instrument is idle
# - If a capture is in progress then we not idle.
# - If Thru mode is active we are not idle.
# - If import-export is active we are not idle.
#		We can't check for this and so we ignore it - unlikely to happen
# - If MSE is active we are not idle.
# - If impairments are running we are not idle.
# - If wander generation is active we are not idle.
# - If Jitter generation is active we are not idle.
# - If Packet Generation is active we are not idle.
def _doResetPreparation():
	_debug("doResetPreparation")
	
	# Stop anything that is running
	_stopCapture()
	_stopImpairment()
	_stopWander()
	_stopPacketGeneration()
	_stopJitter()
	_stopMSE()
		
	
def _rstTranslation(arguments):
	#set args [join $arguments]

	# We want bypass set to false.
	# Once we are done with the other reset actions, we want to execute the Rst normally
	bypass = False

	#if {[lindex $args 0 ] == "Rst"} {
	if "Rst " in arguments:
		_debug("rstTranslation." + arguments + ".")
		_doResetPreparation()
	
	return bypass

def _isguiconnected():
	global _socket
	
	if (_socket == None):
		resp = 0
		#print ("isguiconnected: No socket")
	else:
		# We still have a socket open but the connection may have been killed by the user
		# Try to figure out if the connection is still active
		resp = 1
		try:
			#print ("isguiconnected: Sending remote_control_on")
			_remote_control_on(1)
		except:
			resp = 0

	#print ("isguiconnected: resp = %s" % resp)
	return resp



	
  
# PUBLIC functions
# ================

# Get the instument type from the Idn string
def getInstrumentType():
	idnString = paragonget ("Idn")
	#print(idnString)
	idnParts = idnString.split(',')
	return idnParts[1]


## Makes a connection to the specified GUI and instrument.
#  @param instAddress required  This is the IP address of the Paragon instrument.
#  @param guiAddress  optional  This specifies the IP address of the PC that is hosting
#                               the GUI; if this parameter is not specified then a
#                               connection to the local machine is assumed.
#  @param guiport     optional  This specifies the remote control TCP Port used by the
#                               Paragon client application; if this parameter is not
#                               specified then port 9000 is assumed.
#  @param instPort    optional  This specifies the TCP Port on the Paragon instrument;
#                               if this parameter is not specified then port 9990 is assumed.
#  @throw Exception
## Modified to follow the same process as the Tcl wrapper; also updated to be more robust
## especially around connecting in demo mode
def connect(instAddress, guiAddress = "localhost", guiport = 9000, instPort = 9990, rc = 1):
	global _connected, _lastErr
	global _instrumentType, _instrumentIP
	global _revStr
	
	status = 0
	error = ""

	_gui_connect(guiAddress, guiport)
	
	try:
		_remote_control_on(rc)
	
		connStatus = _is_connected("")
		#print ("connect: connStatus = %d" % connStatus)
		if connStatus < 2:
			instStatus = _is_connected(instAddress)
			#print ("connect: instStatus = %d" % instStatus)
			if connStatus == 1 and instStatus == 0:
				currIp = paragonget("RmtIpAddress")
				error = "ERROR: another instrument (%s) is already connected" % currIp;
			elif instStatus == 0:
				_instrument_connect(instAddress, instPort)
				_connected = True
		else:
			_connected = True
	
	except:
		status = 1
	
	if (error != ""):
		_lastErr = error
		_check_for_error("connect")
		
	if (status == 0):
#	if _connected == 1:
		_debug("connected")
		_instrumentType = getInstrumentType()
		_instrumentIP = instAddress
		idnString = paragonget ("Idn")
		revParts = _revStr.split()
		#print("Connected to " + _instrumentType)
		print(idnString + ' (' + revParts[1] + ')')
		
	else:
		_debug("not connected")
		err = _lastErr
		disconnect()
		_lastErr = err
		_check_for_error("connect")

## Disconnnects the currently connected instrument.
def disconnect():

	global _socket, _connected
	global _instrumentType, _instrumentIP
	
	#if _connected == True:

	try: _instrument_disconnect()
	except: pass
	try: _remote_control_off()
	except: pass
	try: _socket.close()
	except: pass

	_socket    = None
	_connected = False
	_instrumentType = ""
	_instrumentIP = ""
        
	print("Disconnected.")

## Returns 1 if there is a connection to the instrument; 0 otherwise	
def isconnected(instrumentIP=""):
	resp = 0
	
	# Send generates an error if not connected to the GUI. For isconnected, we should simply return false
	if (instrumentIP == ""):
		ip = _instrumentIP
	else:
		ip = instrumentIP
		
	if (ip == ""):
		resp = 0
	else:
		guiConn = _isguiconnected()
		#print ("isconnected: guiConn = %d" % guiConn)
		if (guiConn == 0):
			resp = 0
		else:
			resp = _is_connected(instrumentIP)
			_check_for_error("isconnected")
		
	return resp

	
	
## Query an instrument setting. Most of the instrument's settings are read
#  using by this command. (Refer to the remote control manual for the complete list)
#  @param arg_str required  Setting to query (e.g "Physical LineRate").
#  @return Setting value.
#  @throw Exception
def paragonget(arg_str):
	_debug("paragonget " + arg_str)
	wireCmd = "paragon.CSettingParameter(\"__GET__"
	wireCmd += _build_cmd_from_args(*shlex.split(arg_str)) + "\")"
	
	_send(wireCmd)
	_check_for_error("paragonget %s" % wireCmd)
	
	response = _send("print(paragon.CSettingParameter_resp())")
	_check_for_error("paragonget %s" % response)
	
	# Ignore the type ID character at the start of the response
	return response[1:len(response)]

## Set an instrument setting. Most of the instrument's settings are controlled
#  using by this command. (Refer to the remote control manual for the complete list)
#  @param arg_str required  Setting to set (e.g "Physical LineRate").
#  @param value   required  The value to set.
#  @throw Exception
def paragonset(arg_str, value = None):
	_debug("paragonset " + arg_str)
	isBypass = False
	
	wireCmd = "paragon.CSettingParameter(\"__SET__"

	# Parse the incoming command such that specific actions can be taken for specific commands
	# In most cases, when a command is found, it will bypass further processing
	if (_instrumentType == "Paragon-X"):
		isBypass = _rstTranslation(arg_str)

	# Only send the command is it hasn't already been dealt with
	if (isBypass == False):
		wireCmd += _build_cmd_from_args(*shlex.split(arg_str))
		if (value != None):
			wireCmd += "__#__" + value
		wireCmd += "\")"

		_send(wireCmd)
		_check_for_error("paragonset %s" % wireCmd)

## Starts an ALL byte capture.
#  @throw Exception
def startpacketcapture():
    _send("paragon.startpacketcapture()")
    _check_for_error("startpacketcapture")

## Starts timing capture.
#  @throw Exception
def starttimingcapture():
    _send("paragon.starttimingcapture()")
    _check_for_error("starttimingcapture")

## Stops current capture.
#  @throw Exception
def stopcapture():
	_send("paragon.stopcapture()")
	_check_for_error("stopcapture")

## Enables the impairment as configured in the settings.
#  @throw Exception
def startimpairment():
    _send("paragon.startimpairment()")
    _check_for_error("startimpairment")

## Disables the impairment as configured in the settings.
#  @throw Exception
def stopimpairment():
    _send("paragon.stopimpairment()")
    _check_for_error("stopimpairment")

## Starts Time of Day capture.
#  @throw Exception
def starttodcapture():
    _send("paragon.starttodcapture()")
    _check_for_error("starttodcapture")

## Stops Time Of Day capture.
#  @throw Exception
def stoptodcapture():
    _send("paragon.stoptodcapture()")
    _check_for_error("stoptodcapture")

## Select the SONET STS1 tributary to impair.
#  @param trib required  STS1 tributary number.
#  @throw Exception
def setsonetowsts1trib(trib):
    _send("paragon.CSettingParameter(\"__SET____#___SonetSts1Trib__#__%s\")" % trib)
    _check_for_error("setsonetowsts1trib %s" % trib)

## Select the SONET VT1.5 tributary to impair.
#  @param trib required  VT1.5 tributary number.
#  @throw Exception
def setsonetowvttrib(trib):
    _send("paragon.CSettingParameter(\"__SET____#___SonetVtTrib__#__%s\")" % trib)
    _check_for_error("setsonetowvttrib %s" % trib)

## Set the SONET delay
#  @param delay required  Delay in uS.
#  @throw Exception
def setsonetdelay(delay):
    _send("paragon.CSettingParameter(\"__SET____#___SonetDelay__#__%s\")" % delay)
    _check_for_error("setsonetdelay %s" % delay)

## Saves the displayed captured data to a file.
#  @param filename required  Path and filename for a file on the local PC's
#                            file system. filename must be suffixed with a
#                            valid filename extension:
#                            - ".csv"
#                            - ".cpd"
#  @throw Exception
def exportdata(filename):
    filename = filename.replace("\\", "/")
    _send("paragon.exportdata(\"%s\")" % filename)
    _check_for_error("exportdata %s" % filename)

## Loads the captured data from a file.
#  The importdata is equivalent to using the GUI toolbar menu item File>Import. 
#  This is not port specific and in the bi-directional context is not intended
#  to be used for loading impairment data for replay.
#  @param filename required  Path and filename for a file on the local PC's
#                            file system. filename must be suffixed with a
#                            valid filename extension:
#                            - ".csv"
#                            - ".cpd"
#  @throw Exception
def importdata(filename):
    filename = filename.replace("\\", "/")
    _send("paragon.importdata(\"%s\")" % filename)
    _check_for_error("importdata %s" % filename)

## Stores the instrument settings to the file passed in using the filename
#  parameter. Settings are stored in the file system of the machine hosting
#  the GUI. The stored settings file can be recalled using the 'recall' command.
#  If the specified file already exists, then it will be overwritten.
#  @param filename required  Path and filename for a file on the local PC's
#                            file system.
#  @throw Exception
def store(filename):
    filename = filename.replace("\\", "/")
    _send("saveSettings(\"%s\")" % filename)
    _check_for_error("store %s" % filename)

## Recalls the instrument settings from the file passed in using the filename
#  parameter. Settings are stored in the file system of the machine hosting
#  the GUI. A stored settings file can be created by from the Paragon GUI
#  using Save on the Setup menu.
#  @param filename required  Path and filename for a file on the local PC's
#                            file system.
#  @throw Exception
def recall(filename):
    filename = filename.replace("\\", "/")
    _send("loadSettings(\"%s\")" % filename)
    _check_for_error("recall %s" % filename)

## Loads the capture data for replay. It will load files specifically to replay
#  delay profiles against defined message types on defined ports.
#  The loaded file will be replayed against incoming traffic on the given port.
#  The importimpairmentdata command is equivalent to using the "Import-Port1" and
#  "Import-Port2" buttons in the Add Impairments and Delay window
#  @param port     required  The Ethernet port (1 or 2).
#  @param filename required  Path to a capture file on the local PC's
#                            file system.
#  @throw Exception
def importimpairmentdata(port, filename):
    filename = filename.replace("\\", "/")
    _send("paragon.importimpairmentdata(\"%s\",\"%s\")" %(port, filename))
    _check_for_error("importimpairmentdata %s %s" %(port, filename))

## Wait for the completion of the current CAT operation. 
#  If a script is waiting for previous open operation or waiting for end of
#  previous calculation then this command should be always used. It is
#  recommended to call this after the calls below otherwise there is
#  possibility to get settings conflict error.
#  @throw Exception
def waitforcat():
	status = paragonget("Cat Status")[0]
	while(status == "1"):
		status = paragonget("Cat Status")[0]
		time.sleep(1)
	print("Wait operation completed")

