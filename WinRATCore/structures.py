import ctypes
from ctypes import windll, Structure, c_long, byref, wintypes
from ctypes.wintypes import (BOOL, VARIANT_BOOL, WORD, DOUBLE, DWORD, HBITMAP, HDC, HGDIOBJ,  # noqa
                                 HWND, INT, LPARAM, ULONG, LONG, UINT, WORD, ULARGE_INTEGER, LPWSTR, LPCWSTR)  # noqa

""" Windows structs """
class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]

class POINT(Structure):
	_fields_ = [("x", c_long), ("y", c_long)]

class BITMAPINFOHEADER(ctypes.Structure):
	_fields_ = [
		('biSize', DWORD),
		('biWidth', LONG),
		('biHeight', LONG),
		('biPlanes', WORD), # 1
		('biBitCount', WORD), # 8
		('biCompression', DWORD), # BI_RGB = 0 for uncompressed format
		('biSizeImage', DWORD), # 0
		('biXPelsPerMeter', LONG), # 0
		('biYPelsPerMeter', LONG), # 0
		('biClrUsed', DWORD), # 0
		('biClrImportant', DWORD) # 0
	]

class BITMAPINFO(ctypes.Structure):
	_fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', DWORD * 3)]

class KEYBDINPUT(ctypes.Structure):
	_fields_ = [
		("wVk", wintypes.WORD),
		("wScan", wintypes.WORD),
		("dwFlags", wintypes.DWORD),
		("time", wintypes.DWORD),
		("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
	]


class INPUT(ctypes.Structure):
	_fields_ = [
		("type", wintypes.DWORD),
		("ki", KEYBDINPUT),
		("padding", ctypes.c_ubyte * 8)
	]
