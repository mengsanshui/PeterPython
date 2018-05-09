#!/bin/python

import time
import subprocess
import struct
import os
import binascii
import threading
import signal
import socket
from scapy.all import *
from BTLE import *

def main():

	output = subprocess.check_output(['bash','-c', "hciconfig hci0 down"])
	s = BluetoothUserSocket()

	LEsetscanparam(s, "01")
	LEsetscan(s, "01", "00")
	BD_Addr = []

	while not keystop():
		try:
			data = None
			data = s.recv()
			data = str(data).encode("hex")

			addr = data[14:26]
			addr = ":".join(reversed([addr[i:i+2] for i in range(0, len(addr), 2)]))
			

			if data[2:4] == "3e":
				if data[10:12] == "04":
					if data[36:38] == "08":
						data_length = (int(data[34:36],16) - 1)*2
						name = data[38:38+data_length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

					if data[30:32] == "09":
						data_length = (int(data[28:30],16) - 1)*2
						name = data[32:32+data_length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

				elif data[10:12] == "00":
					length = int(data[34:36],16)*2
					if data[38+length:40+length] == "08":
						data_length = (int(data[36+length:38+length],16) - 1)*2
						name = data[40+length:40+data_length+length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

					elif data[38+length:40+length] == "09":
						data_length = (int(data[36+length:38+length],16) - 1)*2
						name = data[40+length:40+data_length+length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

				else:
					if addr not in BD_Addr:
						print addr + "   " + "Unknown"
						BD_Addr.append(addr)

		except KeyboardInterrupt:
			print "\nExiting"
			LEsetscan(s, "00", "00")
			disconnect(s)
			sys.exit()
			return() 

def keystop(delay = 0):
	return len(select.select([sys.stdin], [], [], delay)[0])

if __name__ == "__main__":
	while not keystop():
		try:
			main()
		except KeyboardInterrupt:
			print "\n Exiting"
		except IndexError:
			print "Error: Index"
		finally:
			sys.exit()