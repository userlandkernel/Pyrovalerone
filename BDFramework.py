"""
    Pyrovalerone
    Framework for OS Detection and modularity
"""
from platform import system as platform_name

class BDFramework:

	def __init__(self, verbose=False):
		self.verbose = verbose

		# These modules correspond to python files and will be loaded dynamically
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
			platform = platform_name() # Get the name of the victim Operating System

		BDCoreModule = None

		# Check if the module is installed
		if platform in self.modules.keys():

			# Try to load the module
			try:
				print("Loading {}".format(self.modules[platform]))
				BDCoreModule = __import__(self.modules[platform], fromlist=['']) # Return a handle to the module

			except Exception as exc:

				raise RuntimeError("Failed to import BDCoreModule: {}".format(exc)) # Importing failed

		else:
			BDCoreModule = __import__(self.modules["Default"], fromlist=['']) # Return handle to default module
			
		return (BDCoreModule, platform)