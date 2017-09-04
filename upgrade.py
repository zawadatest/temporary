#zalozenie ze jest plik rpd.fw na serwerze tftp
import unittest
import rpdIp
import netsnmp
from time import sleep
import re
import os.path
#{ 11, { 1, 3, 6, 1, 4, 1, 11195, 2, 300, 1, 6,
import socket
import fcntl
import struct
#from rpdIp import RpdIp

class Upgrade(unittest.TestCase):	
	def setUp(self):
		self.session = netsnmp.Session(DestHost=rpdIp.rpdAddress, Version=1, Community='public', Retries=0)

	def tearDown(self):
		rpdIp.tftp_download(ip, 'rpd.fw', session)
		v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.4.0')) #sprawdzanie wersji softu na sprzecie
		v0 = self.session.get(v)[0]
		print("aktualnie: ", v0)

	def testUpgrade(self):
		versionOld = rpdIp.get_lpc_version('/var/tftp/rpd_2.fw')#sprawdzenie wersji softu w pliku na tftp
		ip = rpdIp.get_ip_address('eno1')	#get IP
		rpdIp.tftp_download(ip, 'rpd_2.fw', self.session) #download different version of working software
		v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.4.0')) #sprawdzanie wersji softu na sprzecie
		v0 = self.session.get(v)[0]
		#prepare versionOld string to compare
		versionOld = str(versionOld)
		versionOld = versionOld.replace(",", ".").replace("(", "").replace(")", "").replace(" ", "")
		if v0 == versionOld:
			print("test passed")
		assert v0 == versionOld, "Upgrade from %s to version: %s" % (v0, versionOld)

		#TODO do tearDown():
		#rpdIp.tftp_download(ip, 'rpd.fw', session)
		#v = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.11195.2.300.1.4.0')) #sprawdzanie wersji softu na sprzecie
		#v0 = self.session.get(v)[0]
		#print("aktualnie: ", v0)