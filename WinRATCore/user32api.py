import ctypes
from WinRATCore.constants import *
from WinRATCore.structures import *
INPUT_LEN = ctypes.sizeof(INPUT)
LPINPUT = ctypes.POINTER(INPUT)

# Functions

MessageBoxExW = ctypes.windll.user32.MessageBoxExW
MessageBoxA = ctypes.windll.user32.MessageBoxA

SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [wintypes.UINT, LPINPUT, ctypes.c_int]
SendInput.restype = wintypes.UINT

GetDesktopWindow = ctypes.windll.user32.GetDesktopWindow
GetDesktopWindow.restype = HWND

GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
GetForegroundWindow.restype = HWND

GetWindowDC = windll.user32.GetWindowDC
windll.user32.GetWindowDC.argtypes = [HWND]
windll.user32.GetWindowDC.restypes = HDC

GetClientRect = windll.user32.GetClientRect
GetWindowRect = windll.user32.GetWindowRect

EnumWindows = windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

PrintWindow = windll.user32.PrintWindow
IsWindowVisible = windll.user32.IsWindowVisible

GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId

ShowWindow = windll.user32.ShowWindow
ShowWindow.argtypes = HWND, INT