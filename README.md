# DTP-SPOOF
dtp-spoof is a security tool that can be used to test the Dynamic Trunking Protocol (DTP) configuration of switches. By sending a Trunk # packet, you can potentially set the remote switch port to Trunk mode, thereby gaining access to additional VLANs.

DO NOT use this script for illegal activites! Use it only on networks you own or for which you have permission to audit.

Some tips:
- The switch might not send you any traffic to indicate you have successfully formed a trunk. To verify that it has, you should (from the switch) note the port's state before and after you run the script and see if it changes.

- If DTP has been disabled on a switchport, this script won't change anything.

- I imagine most users will just use the --trunk option. However, other DTP types can be selected (--desirable, --auto, --access) if you want to try them and see what your switch does. Trunk is the default if no DTP type is specified.

- You must specifiy an interface to send the packets from. 

- You can, but do not have to, spoof your MAC address with the -m option. If you do so, the supplied mac address will be used for both the source address of the Ethernet frame and the neighbor MAC field within the DTP packet.


Examples:

python dtp-spoof.py -i eth0 //sends a DTP Trunk packet out eth0 using eth0's mac address

python dtp-spoof.py -i eth0 --desirable -m 00:05:3a:55:3a:1c //sends a DTP Dynamic Desirable packet out eth0 using 00:05:3a:55:3a:1c as the frame source and DTP neighbor mac addresses

Thanks for reading!

John 3:16
