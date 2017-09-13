# DTP-SPOOF
dtp-spoof is a security tool to test the Dynamic Trunking Protocol (DTP) configuration of switches. If the target switch is configured to negotiate the port mode, you can potentially set the target switch's port to Trunk mode, thereby gaining access to additional VLANs.

DO NOT use this script for illegal activites! Use it only on networks you own or for which you have permission to audit.

Some tips:
- The switch might not send you any traffic to indicate you have successfully formed a trunk.

- If DTP has been disabled on a switchport, the script won't change anything.

- Asking for 'trunk' mode is the default option but 'desireable', 'auto', and 'access' modes are available.

- You must specifiy an interface to send the packets from. 

- You can, but do not have to, spoof your MAC address with the -m option. If you do so, the supplied mac address will be used for both the source address of the Ethernet frame and the neighbor MAC field within the DTP packet.


Examples:

python dtp-spoof.py -i eth0 //sends a DTP Trunk packet out eth0 using eth0's mac address

python dtp-spoof.py -i eth0 --desirable -m 00:05:3a:55:3a:1c //sends a DTP Dynamic Desirable packet out eth0 using 00:05:3a:55:3a:1c as the frame source and DTP neighbor mac addresses
