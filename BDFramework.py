"""
    Pyrovalerone
    Framework for OS Detection and modularity
"""
from platform import system as platform_name

class BDFramework:

	def __init__(self, verbose=False):
		self.verbose = verbose
		self.modules = {
			"Windows": "BDModuleWindows",
			"Linux": "BDModuleLinux",
			"Darwin": "BDModuleDarwin",
			"PhoneOS": "BDModuleiPhoneOS",
			"Android": "BDModuleAndroid",
			"Default": "BDModuleDefault"
		}

	def GetCoreModule(self, platform=None) -> (object, str):

		if not platform:
			platform = platform_name()

		BDCoreModule = None
		if platform in self.modules.keys():
			try:
				print("Executing {}".format(self.modules[platform]))
				BDCoreModule = __import__(self.modules[platform], fromlist=[''])
			except Exception as exc:
				raise RuntimeError("Failed to import BDCoreModule: {}".format(exc))
				
		return (BDCoreModule, platform)