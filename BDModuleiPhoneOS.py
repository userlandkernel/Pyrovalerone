from platform import system as platform_name

class BDFramework:

	def __init__(self, verbose=False):
		self.verbose = verbose
		self.modules = {
			"Windows": "import BDModuleWindows as BDCoreModule",
			"Linux": "import BDModuleLinux as BDCoreModule",
			"Darwin": "import BDModuleDarwin as BDCoreModule",
			"PhoneOS": "import BDModuleiPhoneOS as BDCoreModule",
			"Android": "import BDModuleAndroid as BDCoreModule",
			"Default": "import BDModuleDefault as BDCoreModule"
		}

	def GetCoreModule(self):
		module = platform_name()
		if module in self.modules.keys():
			try:
				exec(self.modules[module])
			except Exception as exc:
				raise RuntimeError("Failed to import BDCoreModule")
				BDCoreModule = None
				
		return BDCoreModule

		#return BDCoreModule