import ctypes
from ctypes import windll, Structure, c_long, byref, wintypes, POINTER, c_void_p
from ctypes.wintypes import (BOOL, VARIANT_BOOL, WORD, DOUBLE, DWORD, HBITMAP, HDC, HGDIOBJ,  # noqa
                                 HWND, WCHAR, HMODULE, HANDLE, LPSTR, LPVOID, LPCSTR, LPCVOID, INT, LPARAM, ULONG, LONG, UINT, WORD, ULARGE_INTEGER, LPWSTR, LPDWORD, LPCWSTR)  # noqa
LPCSTR = LPCTSTR = ctypes.c_char_p
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
SIZE_T = ctypes.c_size_t

LPSECURITY_ATTRIBUTES = ctypes.POINTER
LPTHREAD_START_ROUTINE = LPVOID

SeShutdownPrivilege = 19

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = 0xFFFF
MEM_COMMIT = 0x1000 
MEM_DECOMMIT = 0x4000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000
PAGE_EXECUTE_READWRITE = 0x40
PAGE_READWRITE = 0x04
WAIT_FAILED = 0xFFFFFFFF
WAIT_TIMEOUT = 0x00000102
WAIT_OBJECT_0 = 0x00000000
WAIT_ABANDONED = 0x00000080
INFINITE = 0xFFFFFFFF
VIRTUAL_MEM = (0x1000|0x2000)

SRCCOPY = 13369376
DIB_RGB_COLORS = BI_RGB = 0

""" Virtual Keycodes """
VK_LBUTTON = 0x01 #Left mouse button
VK_RBUTTON = 0x02 #Right mouse button
VK_CANCEL = 0x03 #Control-break processing
VK_MBUTTON = 0x04 #Middle mouse button (three-button mouse)
VK_XBUTTON1 = 0x05 #X1 mouse button
VK_XBUTTON2 = 0x06 #X2 mouse button
VK_BACK = 0x08 #BACKSPACE key
VK_TAB = 0x09 #TAB key
VK_CLEAR = 0x0C #CLEAR key
VK_RETURN = 0x0D #ENTER key
VK_SHIFT = 0x10 #SHIFT key
VK_CONTROL = 0x11 #CTRL key
VK_MENU = 0x12 #ALT key
VK_PAUSE = 0x13 #PAUSE key
VK_CAPITAL = 0x14 #CAPS LOCK key
VK_KANA = 0x15 #IME Kana mode
VK_HANGUEL = 0x15 #IME Hanguel mode (maintained for compatibility; use VK_HANGUL)
VK_HANGUL = 0x15 #IME Hangul mode
VK_JUNJA = 0x17 #IME Junja mode
VK_FINAL = 0x18 #IME final mode
VK_HANJA = 0x19 #IME Hanja mode
VK_KANJI = 0x19 #IME Kanji mode
VK_ESCAPE = 0x1B #ESC key
VK_CONVERT = 0x1C #IME convert
VK_NONCONVERT = 0x1D #IME nonconvert
VK_ACCEPT = 0x1E #IME accept
VK_MODECHANGE = 0x1F #IME mode change request
VK_SPACE = 0x20 #SPACEBAR
VK_PRIOR = 0x21 #PAGE UP key
VK_NEXT = 0x22 #PAGE DOWN key
VK_END = 0x23 #END key
VK_HOME = 0x24 #HOME key
VK_LEFT = 0x25 #LEFT ARROW key
VK_UP = 0x26 #UP ARROW key
VK_RIGHT = 0x27 #RIGHT ARROW key
VK_DOWN = 0x28 #DOWN ARROW key
VK_SELECT = 0x29 #SELECT key
VK_PRINT = 0x2A #PRINT key
VK_EXECUTE = 0x2B #EXECUTE key
VK_SNAPSHOT = 0x2C #PRINT SCREEN key
VK_INSERT = 0x2D #INS key
VK_DELETE = 0x2E #DEL key
VK_HELP = 0x2F #HELP key
VK_0 = 0x30 #0 key
VK_1 = 0x31 #1 key
VK_2 = 0x32 #2 key
VK_3 = 0x33 #3 key
VK_4 = 0x34 #4 key
VK_5 = 0x35 #5 key
VK_6 = 0x36 #6 key
VK_7 = 0x37 #7 key
VK_8 = 0x38 #8 key
VK_9 = 0x39 #9 key
VK_A = 0x41
VK_B = 0x42
VK_C = 0x43
VK_D = 0x44
VK_E = 0x45
VK_F = 0x46
VK_G = 0x47
VK_H = 0x48
VK_I = 0x49
VK_J = 0x4A
VK_K = 0x4B
VK_L = 0x4C
VK_M = 0x4D
VK_N = 0x4E
VK_O = 0x4F
VK_P = 0x50
VK_Q = 0x51
VK_R = 0x52
VK_S = 0x53
VK_T = 0x54
VK_U = 0x55
VK_V = 0x56
VK_W = 0x57
VK_X = 0x58
VK_Y = 0x59
VK_Z = 0x5A
VK_LWIN = 0x5B #Left Windows key (Natural keyboard)
VK_RWIN = 0x5C #Right Windows key (Natural keyboard)
VK_APPS = 0x5D #Applications key (Natural keyboard)
VK_SLEEP = 0x5F #Computer Sleep key
VK_NUMPAD0 = 0x60 #Numeric keypad 0 key
VK_NUMPAD1 = 0x61 #Numeric keypad 1 key
VK_NUMPAD2 = 0x62 #Numeric keypad 2 key
VK_NUMPAD3 = 0x63 #Numeric keypad 3 key
VK_NUMPAD4 = 0x64 #Numeric keypad 4 key
VK_NUMPAD5 = 0x65 #Numeric keypad 5 key
VK_NUMPAD6 = 0x66 #Numeric keypad 6 key
VK_NUMPAD7 = 0x67 #Numeric keypad 7 key
VK_NUMPAD8 = 0x68 #Numeric keypad 8 key
VK_NUMPAD9 = 0x69 #Numeric keypad 9 key
VK_MULTIPLY = 0x6A #Multiply key
VK_ADD = 0x6B #Add key
VK_SEPARATOR = 0x6C #Separator key
VK_SUBTRACT = 0x6D #Subtract key
VK_DECIMAL = 0x6E #Decimal key
VK_DIVIDE = 0x6F #Divide key
VK_F1 = 0x70 #F1 key
VK_F2 = 0x71 #F2 key
VK_F3 = 0x72 #F3 key
VK_F4 = 0x73 #F4 key
VK_F5 = 0x74 #F5 key
VK_F6 = 0x75 #F6 key
VK_F7 = 0x76 #F7 key
VK_F8 = 0x77 #F8 key
VK_F9 = 0x78 #F9 key
VK_F10 = 0x79 #F10 key
VK_F11 = 0x7A #F11 key
VK_F12 = 0x7B #F12 key
VK_F13 = 0x7C #F13 key
VK_F14 = 0x7D #F14 key
VK_F15 = 0x7E #F15 key
VK_F16 = 0x7F #F16 key
VK_F17 = 0x80 #F17 key
VK_F18 = 0x81 #F18 key
VK_F19 = 0x82 #F19 key
VK_F20 = 0x83 #F20 key
VK_F21 = 0x84 #F21 key
VK_F22 = 0x85 #F22 key
VK_F23 = 0x86 #F23 key
VK_F24 = 0x87 #F24 key
VK_NUMLOCK = 0x90 #NUM LOCK key
VK_SCROLL = 0x91 #SCROLL LOCK key
VK_LSHIFT = 0xA0 #Left SHIFT key
VK_RSHIFT = 0xA1 #Right SHIFT key
VK_LCONTROL = 0xA2 #Left CONTROL key
VK_RCONTROL = 0xA3 #Right CONTROL key
VK_LMENU = 0xA4 #Left MENU key
VK_RMENU = 0xA5 #Right MENU key
VK_BROWSER_BACK = 0xA6 #Browser Back key
VK_BROWSER_FORWARD = 0xA7 #Browser Forward key
VK_BROWSER_REFRESH = 0xA8 #Browser Refresh key
VK_BROWSER_STOP = 0xA9 #Browser Stop key
VK_BROWSER_SEARCH = 0xAA #Browser Search key
VK_BROWSER_FAVORITES = 0xAB #Browser Favorites key
VK_BROWSER_HOME = 0xAC #Browser Start and Home key
VK_VOLUME_MUTE = 0xAD #Volume Mute key
VK_VOLUME_DOWN = 0xAE #Volume Down key
VK_VOLUME_UP = 0xAF #Volume Up key
VK_MEDIA_NEXT_TRACK = 0xB0 #Next Track key
VK_MEDIA_PREV_TRACK = 0xB1 #Previous Track key
VK_MEDIA_STOP = 0xB2 #Stop Media key
VK_MEDIA_PLAY_PAUSE = 0xB3 #Play/Pause Media key
VK_LAUNCH_MAIL = 0xB4 #Start Mail key
VK_LAUNCH_MEDIA_SELECT = 0xB5 #Select Media key
VK_LAUNCH_APP1 = 0xB6 #Start Application 1 key
VK_LAUNCH_APP2 = 0xB7 #Start Application 2 key
VK_OEM_1 = 0xBA #Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key
VK_OEM_PLUS = 0xBB #For any country/region, the '+' key
VK_OEM_COMMA = 0xBC #For any country/region, the ',' key
VK_OEM_MINUS = 0xBD #For any country/region, the '-' key
VK_OEM_PERIOD = 0xBE #For any country/region, the '.' key
VK_OEM_2 = 0xBF #Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key = 
VK_OEM_3 = 0xC0 #Used for miscellaneous characters; it can vary by keyboard. = For the US standard keyboard, the '`~' key
VK_OEM_4 = 0xDB #Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key
VK_OEM_5 = 0xDC #Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '\|' key
VK_OEM_6 = 0xDD #Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the ']}' key
VK_OEM_7 = 0xDE #Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the 'single-quote/double-quote' key
VK_OEM_8 = 0xDF #Used for miscellaneous characters; it can vary by keyboard.
VK_OEM_102 = 0xE2 #Either the angle bracket key or the backslash key on the RT 102-key keyboard 0xE3-E4 OEM specific
VK_PROCESSKEY = 0xE5 #IME PROCESS key 0xE6 = OEM specific #
VK_PACKET = 0xE7 #Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KEYUP #-
VK_ATTN = 0xF6 #Attn key
VK_CRSEL = 0xF7 #CrSel key
VK_EXSEL = 0xF8 #ExSel key
VK_EREOF = 0xF9 #Erase EOF key
VK_PLAY = 0xFA #Play key
VK_ZOOM = 0xFB #Zoom key
VK_NONAME = 0xFC #Reserved
VK_PA1 = 0xFD #PA1 key
VK_OEM_CLEAR = 0xFE #

""" MESSAGEBOX BUTTONS """
MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

""" MESSAGEBOX ICONS """
MB_ICONEXCLAMATION =0x00000030
MB_ICONWARNING =0x00000030
MB_ICONINFORMATION = 0x00000040
MB_ICONASTERISK = 0x00000040
MB_ICONQUESTION = 0x00000020
MB_ICONSTOP = 0x00000010
MB_ICONERROR = 0x00000010
MB_ICONHAND = 0x00000010

""" MESSAGEBOX DEFAULT BUTTON """
MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

""" MESSAGEBOX MODALITY """
MB_APPLMODAL = 0x00000000
MB_SYSTEMMODAL = 0x00001000
MB_TASKMODAL = 0x00002000

""" MESSAGEBOX OTHER """
MB_DEFAULT_DESKTOP_ONLY = 0x00020000
MB_RIGHT = 0x00080000
MB_RTLREADING = 0x00100000
MB_SETFOREGROUND = 0x00010000
MB_TOPMOST = 0x00040000
MB_SERVICE_NOTIFICATION = 0x00200000

""" WINDOW STYLES """
WS_OVERLAPPED = 0x00000000
WS_POPUP = 0x80000000
WS_CHILD = 0x40000000
WS_MINIMIZE = 0x20000000
WS_VISIBLE = 0x10000000
WS_DISABLED = 0x08000000
WS_CLIPSIBLINGS = 0x04000000
WS_CLIPCHILDREN = 0x02000000
WS_MAXIMIZE = 0x01000000
WS_BORDER = 0x00800000
WS_DLGFRAME = 0x00400000
WS_VSCROLL = 0x00200000
WS_HSCROLL = 0x00100000
WS_SYSMENU = 0x00080000
WS_THICKFRAME = 0x00040000
WS_GROUP = 0x00020000
WS_TABSTOP = 0x00010000

WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_CAPTION = WS_BORDER | WS_DLGFRAME
WS_TILED = WS_OVERLAPPED
WS_ICONIC = WS_MINIMIZE
WS_SIZEBOX = WS_THICKFRAME
WS_OVERLAPPEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
WS_TILEDWINDOW = WS_OVERLAPPEDWINDOW
WS_POPUPWINDOW = WS_POPUP | WS_BORDER | WS_SYSMENU
WS_CHILDWINDOW = WS_CHILD

# Extended Window Styles
WS_EX_DLGMODALFRAME = 0x00000001
WS_EX_NOPARENTNOTIFY = 0x00000004
WS_EX_TOPMOST = 0x00000008
WS_EX_ACCEPTFILES = 0x00000010
WS_EX_TRANSPARENT = 0x00000020

#if(WINVER >= 0x0400)

WS_EX_MDICHILD = 0x00000040
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_WINDOWEDGE = 0x00000100
WS_EX_CLIENTEDGE = 0x00000200
WS_EX_CONTEXTHELP = 0x00000400

WS_EX_RIGHT = 0x00001000
WS_EX_LEFT = 0x00000000
WS_EX_RTLREADING = 0x00002000
WS_EX_LTRREADING = 0x00000000
WS_EX_LEFTSCROLLBAR = 0x00004000
WS_EX_RIGHTSCROLLBAR = 0x00000000

WS_EX_CONTROLPARENT = 0x00010000
WS_EX_STATICEDGE = 0x00020000
WS_EX_APPWINDOW = 0x00040000

WS_EX_OVERLAPPEDWINDOW = (WS_EX_WINDOWEDGE | WS_EX_CLIENTEDGE)
WS_EX_PALETTEWINDOW = (WS_EX_WINDOWEDGE | WS_EX_TOOLWINDOW | WS_EX_TOPMOST)
#endif WINVER >= 0x0400

#if(WIN32WINNT >= 0x0500)
WS_EX_LAYERED = 0x00080000
#endif /* WIN32WINNT >= 0x0500 */

#if(WINVER >= 0x0500)
WS_EX_NOINHERITLAYOUT = 0x00100000, # Disable inheritence of mirroring by children
WS_EX_LAYOUTRTL = 0x00400000 # Right to left mirroring
#endif /* WINVER >= 0x0500 */

#if(WIN32WINNT >= 0x0500)
WS_EX_COMPOSITED = 0x02000000
WS_EX_NOACTIVATE = 0x08000000
#endif /* WIN32WINNT >= 0x0500 */

# Windows Input
INPUT_KEYBOARD = 1

# Windows Errors
ERROR_SUCCESS = 0

# Windows Registry
HKEY = ctypes.c_void_p
PHKEY = POINTER(HKEY)
REGSAM = DWORD
LPSECURITY_ATTRIBUTES = ctypes.c_void_p
LSTATUS = LONG

# Disposition values
REG_CREATED_NEW_KEY = 0x00000001
REG_OPENED_EXISTING_KEY = 0x00000002

HKEY_CURRENT_USER = c_void_p(0x80000001)
REG_OPTION_NON_VOLATILE = 0
KEY_ALL_ACCESS = 0x000F003F
