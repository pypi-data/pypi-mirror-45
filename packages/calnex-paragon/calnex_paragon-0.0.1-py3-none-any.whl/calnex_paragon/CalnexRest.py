################################################################################
#                                                                              #
#   calnexRest.py                                                              #
#                                                                              #
#   Python interface to the new line of Calnex products                        #
#                                                                              #
#   Copyright (c) Calnex Solutions Ltd 2008 - 2018                             #
#                                                                              # 
#   The contents of this file should not be copied or distributed              #
#   without permission being granted by Calnex Solutions Ltd.                  #
#                                                                              #
#   All rights reserved.                                                       #
#                                                                              #
################################################################################

import requests, json

_lastErr    = "";
_instrument = "";

def _check_for_error(label):
    global _lastErr
    
    if len(_lastErr) > 0:
        raise Exception("%s : %s" %(label, _lastErr))

def argsToJSON(arg):
    i = iter(arg); d = dict(zip(i, i))
    return json.dumps(d)

def calnexInit(IpAddr):
    global _instrument
    global _lastErr
	
    _lastErr = ""
    if (IpAddr == ""):
       _lastErr = "Must specify an IP Address for the instrument"
    else:
       IpAddress = IpAddr
       _instrument = "http://" + IpAddress + "/api/"
       try:
            model = calnexGetVal("instrument/information", "HwType")
            sn = calnexGetVal("instrument/information", "SerialNumber")
       except requests.exceptions.RequestException as e:
            model = "Unknown"
            sn = "Unknown"
            _lastErr = str(e)
       print("%s %s" %(model, sn))

    _check_for_error("calnexInit")

def calnexGet(url, *arg):
    global _instrument
    global _lastErr
	
    _lastErr = ""
    if (_instrument == ""):
        _lastErr = "IP address not configured - call calnexInit before any other calls"
        ret = ""
    else:
        try:
            response = requests.get(
                "{0}{1}?format=json".format(_instrument, url), 
                data=argsToJSON(arg), 
                headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            ret = response.json()
        except requests.exceptions.RequestException as e:
            _lastErr = str(e)

    _check_for_error("calnexGet %s" %(url))
    return ret
	
def calnexGetVal(url, arg):
    global _instrument
    global _lastErr
    res = calnexGet(url, arg)
    ret = res
    if arg not in res:
        _lastErr = "\"" + arg + "\" does not exist in response: " + str(res)
    else:
        ret = res[arg]

    _check_for_error ("calnexGetVal %s %s" %(url, arg))
    return ret
	
def calnexSet(url, *arg):
    global _instrument
    global _lastErr
	
    _lastErr = ""
    if (_instrument == ""):
        _lastErr = "IP address not configured - call calnexInit before any other calls"
        ret = ""
    else:
        try: requests.put("{0}{1}?format=json".format(_instrument, url),
                argsToJSON(arg), headers={'Content-Type': 'application/json'}).raise_for_status()
        except requests.exceptions.RequestException as e:
            _lastErr = str(e)
    _check_for_error("calnexSet %s" %(url))
		
def calnexCreate(url, *arg):
    global _instrument
    requests.post("{0}{1}".format(_instrument, url),
        argsToJSON(arg), headers={'Content-Type': 'application/json'}).raise_for_status()
		
def calnexDel(url):
    global _instrument
    requests.delete("{0}{1}".format(_instrument, url), headers={'Content-Type': 'application/json'}).raise_for_status()
	
#
# Old syntax - kept for backwards compatibility
#

def p100get(url, *arg):	
	return calnexGet(url, *arg)
	
def p100set(url, *arg):
    calnexSet(url, *arg)
		
def p100create(url, *arg):
    calnexCreate(url, *arg)
		
def p100del(url):
    calnexDel(url)
	
def a100get(url, *arg):	
	return calnexGet(url, *arg)
	
def a100set(url, *arg):
    calnexSet(url, *arg)
		
def a100create(url, *arg):
    calnexCreate(url, *arg)
		
def a100del(url):
    calnexDel(url)