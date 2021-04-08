import ctypes
from constants import *
from structures import *

# CreateCompatibleDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
windll.gdi32.CreateCompatibleDC.argtypes = [HDC]
windll.gdi32.CreateCompatibleDC.restypes = HDC

# CreateCompatibleBitmap
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
windll.gdi32.CreateCompatibleBitmap.argtypes = [HDC, INT, INT]
windll.gdi32.CreateCompatibleBitmap.restypes = HBITMAP

# SelectObject
SelectObject = windll.gdi32.SelectObject
windll.gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
windll.gdi32.SelectObject.restypes = HGDIOBJ

# BitBlt
BitBlt = windll.gdi32.BitBlt
windll.gdi32.BitBlt.argtypes = [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD]
windll.gdi32.BitBlt.restypes = BOOL

# DeleteObject
DeleteObject = windll.gdi32.DeleteObject
windll.gdi32.DeleteObject.argtypes = [HGDIOBJ]
windll.gdi32.DeleteObject.restypes = BOOL

# GetDIBits
GetDIBits = windll.gdi32.GetDIBits
windll.gdi32.GetDIBits.argtypes = [HDC, HBITMAP, UINT, UINT, ctypes.c_void_p, ctypes.POINTER(BITMAPINFO), UINT]
windll.gdi32.GetDIBits.restypes = INT