import BDModuleDefault

class ClientMain(BDModuleDefault.ClientMain):

	def __init__(self, handler):
		super().__init__(handler)

class ServerMain(BDModuleDefault.ServerMain):

	def __init__(self, handler):
		super().__init__(handler)