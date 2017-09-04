import re
import netsnmp
from time import sleep
import socket
import fcntl
import struct
import os.path

def findIp():
	pattern = re.compile(r"lease ([0-9.]+) ")
	ipAddr = []
	with open("/var/lib/dhcp/dhcpd.leases") as f:
		for match in pattern.finditer(f.read()):
			ipAddr.append(match.group(1))
	for ip in ipAddr:
		session = netsnmp.Session(DestHost=ip, Version=1, Community='public', Retries=0)
		v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.1.0'))
		name = session.get(v)[0]
		if( name == "RPD control"):
			return ip
	return "RPD control not found"
def init():
    global rpdAddress
    rpdAddress = findIp()

def tftp_download(ip, filename, session):
	v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.11.0', val=ip, type='IPADDRESS'))	#set IP address
	session.set(v)
	v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.6.0', val=filename, type='OCTET STRING'))	#nadaje nazwe pliku
	session.set(v)
	v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.6.0')) #sprawdza co jest w miejscu nazwy pliku
	tmp = session.get(v)[0]
	while tmp != '15':
		if( tmp == 0):
			sleep(10)
		sleep(10)
		v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.6.0'))
		tmp = session.get(v)[0]
	sleep(5)
	v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.6.0')) #sprawdza co jest w miejscu nazwy pliku
	tmp = session.get(v)[0]
	while tmp != '15':
		if( tmp == 0):
			sleep(10)
		sleep(10)
		v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.6.0'))
		tmp = session.get(v)[0]
	v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.7.0', val='1', type='INTEGER')) #reset
	session.set(v)
	sleep(65)

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def get_lpc_version(firmware):
    if not os.path.isfile(firmware):
        raise IOError("File %s does not exist. Aborting." % (firmware))

    with open(firmware, 'rb') as f:
        f.seek(50855920)
        buff = f.read(16)
        version = struct.unpack('<LLLL', buff)

    print "LPC version from binary: %d.%d.%d.%d" % (version[0], version[1], version[2], version[3])
    return version