import ctypes
from WinRATCore.constants import *
from WinRATCore.structures import *

EnumProcesses = ctypes.windll.psapi.EnumProcesses
EnumProcesses.restype = BOOL

GetProcessImageFileName = ctypes.windll.psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = DWORD