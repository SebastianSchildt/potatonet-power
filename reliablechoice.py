#!/bin/python3

#TP-Link interface
import urllib.request as h
import time




TP_LINK_HOST="172.18.1.1"
USER="admin"
PASS="admin"

timeout=60

_lastlogin=0

#Humand readable states (from TP_LINK)
_trunk_info = ["", " (LAG1)", " (LAG2)", " (LAG3)", " (LAG4)", " (LAG5)", " (LAG6)", " (LAG7)", " (LAG8)"]
_state_info = ["Disabled", "Enabled"]
_speed_info = ["Link Down", "Auto", "10Half", "10Full", "100Half", "100Full", "1000Full", ""]
_flow_info  = ["Off", "On"];

def login():
	global _lastlogin
	req=h.Request("http://"+TP_LINK_HOST+"/logon.cgi")
	res=h.urlopen(req,data=bytes("username="+USER+"&password="+PASS+"&logon=Login","utf-8"),timeout=timeout)
	
	if res.status != 200:
		print("Error logging in "+str(res.status))
		return False

	_lastlogin=time.time()
	print("set last login to "+str(_lastlogin))
	return True

#returns a list form Port 0 to 23. True means enabled, False means off
#hmm, link status?
def getState():
	#check login
	currtime=time.time()
	print("now is "+str(currtime)+" last was "+str(_lastlogin))
	if (currtime-_lastlogin) >= timeout:
		print("need to login first")
		if not login():
			print("Not working :(")
			return ([],[])

	res=h.urlopen("http://"+TP_LINK_HOST+"/PortSettingRpm.htm")
	if res.status != 200:
		print("Error getting port data "+str(res.status))
		return False

	data=res.read(16384)
	f=open("out.tmp","wb")
	f.write(data)
	f.close()

	p_info=data.decode("latin-1")
	start=p_info.find("var tmp_info =")

	if start == -1:
		print("data not found")
		print(p_info)
		return ([],[])

	end=p_info.find("\";",start)
	
	if end == -1:
		print("data weird")
		return ([],[])


	p_info=p_info[ start+16:end-1]

	raw_list=p_info.split()
	enabled_list=[]
	link_list=[]
	
	for port in range(0,24):	
		#TP-Link Code
		state        = raw_list[port * 6 + 1];
		speed_config = raw_list[port * 6 + 2];
		speed_actual = raw_list[port * 6 + 3];
		flow_config  = raw_list[port * 6 + 4];
		flow_actual  = raw_list[port * 6 + 5];
		print("Port "+str(port)+" is "+_state_info[int(state)]+". Link speed: "+_speed_info[int(speed_actual)])
		enabled_list.append(state)
		link_list.append(speed_actual)
		
	
	return (enabled_list,link_list)

#Port between 0 and 23, 0 is locked
def setPort(portnum, enabled):
	print("set port "+str(portnum)+" to "+str(enabled))
	if portnum == 0 and not enabled:
		print("Can not disable management port")
		return False

	if portnum < 0 or portnum > 23:
		print("Portnum out of range")
		return False


	currtime=time.time()
	if (currtime-_lastlogin) >= timeout:
		print("need to login first")
		if not login():
			print("Not working :(")
			return False

	if enabled:
		state=1
	else:
		state=0
	post="portid="+str(portnum+1)+"&state="+str(state)+"&speed=7&flowcontrol=7";
	
	res=h.urlopen("http://"+TP_LINK_HOST+"/port_setting.cgi",data=bytes(post,"utf-8"))
	if res.status != 200:
		print("Error setting port state "+str(res.status))
		return False

	#This is needed, and the TP-Link WebIF does the same. Otherwise reading states will not return the new state. Yes, it sucks that much
	time.sleep(1)
	return True


#setPort(3,False)
#(enabled,link)=getState()
#setPort(0,False)
#setPort(3,True)
#(enabled,link)=getState()
#setPort(3,False)
#(enabled,link)=getState()
#print("Enabled list "+str(enabled))
#print("Link states "+str(link))
