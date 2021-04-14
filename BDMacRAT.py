"""
	Pyrovalerone
	Python-based Windows Remote Administration Tool API
	Note: This code is not intended to be abused
"""
#!/usr/bin/env python3
import os
import sys
import struct
from random import randrange
import time
import BDMRatMelodies

class MacOSRAT:

	def injectDylib(self, pid:int, dll:str) -> bool:
		return False